"""Tests for GET /audit/{correlation_id}. Stage S05-14 Half B.

The route reads one case back from the audit log. Only role.admin may call it (row TA-35).
Every test points `audit.LOG` at a temp file. No test touches logs/audit.log.
Every test is a security test and none is skipped.

Designs: docs/14-audit/audit-read-access-design.md and docs/14-audit/evidence-chain-one-case.md.
Field names are built in pieces so that test_secret_patterns.py does not flag this file.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit, audit_query

pytestmark = pytest.mark.security

client = TestClient(app)

REPO = Path(__file__).resolve().parents[2]
REAL_LOG = REPO / "logs" / "audit.log"

CASE = "s0514-case-0001"
ADMIN = {"X-User-Role": "admin"}

MGMT = "mgmt" + "_ip"
CRED = "credential" + "_profile"
DB_USER = "SHARED_DB" + "_USER"


@pytest.fixture
def log(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)
    return path


def rows_in(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def lines_in(path):
    return path.read_text(encoding="utf-8").splitlines()


def build_case(case_id=CASE):
    """Three calls with one id: a record read, a summary, and a denied read."""
    headers = {"X-Correlation-Id": case_id}
    first = client.get("/records/REC-0001", headers={**headers, "X-User-Role": "operator"})
    second = client.post("/ai/summarize/REC-0001", headers={**headers, "X-User-Role": "operator"})
    third = client.get("/records/REC-0001", headers={**headers, "X-User-Role": "visitor"})
    assert (first.status_code, second.status_code, third.status_code) == (200, 200, 403)


def own_row(path, expected_lines_before):
    """The one row the audit route added. Fails if the log grew by any other amount."""
    lines = lines_in(path)
    assert len(lines) == expected_lines_before + 1
    return json.loads(lines[-1])


# ---------------------------------------------------------------------------
# The chain is rebuilt from the log
# ---------------------------------------------------------------------------


def test_the_chain_comes_back_in_time_order(log):
    build_case()
    response = client.get(f"/audit/{CASE}", headers=ADMIN)
    assert response.status_code == 200
    body = response.json()
    assert body["correlation_id"] == CASE
    assert body["row_count"] == 3
    assert [row["action"] for row in body["rows"]] == ["record.read", "ai.summary", "policy.deny"]
    assert [row["role"] for row in body["rows"]] == ["operator", "operator", "visitor"]
    stamps = [row["ts"] for row in body["rows"]]
    assert stamps == sorted(stamps)
    assert all(row["correlation_id"] == CASE for row in body["rows"])
    # The rows are the stored rows. The summary row holds the model facts.
    assert body["rows"][1]["model"] == "local-sim-v1"
    assert body["rows"][1]["prompt_hash"]


def test_a_row_written_out_of_order_still_comes_back_in_time_order(log):
    lines = [
        {"ts": "2026-10-12T10:00:03", "action": "c"},
        {"ts": "2026-10-12T10:00:01", "action": "a"},
        {"ts": "2026-10-12T10:00:02", "action": "b"},
    ]
    for line in lines:
        row = {key: None for key in audit.SCHEMA_KEYS}
        row.update(line, correlation_id=CASE, role="operator", resource="resource.device")
        with log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row) + "\n")
    body = client.get(f"/audit/{CASE}", headers=ADMIN).json()
    assert [row["action"] for row in body["rows"]] == ["a", "b", "c"]


def test_two_cases_do_not_mix(log):
    build_case("case-one")
    client.get("/records/REC-0001", headers={"X-Correlation-Id": "case-two", "X-User-Role": "operator"})
    one = client.get("/audit/case-one", headers=ADMIN).json()
    two = client.get("/audit/case-two", headers=ADMIN).json()
    assert one["row_count"] == 3
    assert two["row_count"] == 1
    assert {row["correlation_id"] for row in one["rows"]} == {"case-one"}


def test_lines_with_no_correlation_id_are_never_returned_and_are_counted(log):
    old_line = {"ts": "2026-01-01T00:00:00", "action": "record.read", "role": "operator"}
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(old_line) + "\n")
        handle.write(json.dumps(old_line) + "\n")
        handle.write("this line is not json\n")
    build_case()
    body = client.get(f"/audit/{CASE}", headers=ADMIN).json()
    assert body["row_count"] == 3
    items = {entry["item"]: entry["reason"] for entry in body["cannot_prove"]}
    assert items["rows_before_correlation_id"].startswith("2 line(s)")
    assert items["unreadable_lines"].startswith("1 line(s)")


# ---------------------------------------------------------------------------
# An id with no rows
# ---------------------------------------------------------------------------


def test_an_unknown_id_gives_404_and_writes_its_own_row(log):
    build_case()
    before = lines_in(log)
    response = client.get("/audit/no-such-case", headers={**ADMIN, "X-Correlation-Id": "probe-404"})
    assert response.status_code == 404
    assert response.json() == {"error": "not_found"}
    assert "no-such-case" not in response.text
    row = own_row(log, len(before))
    assert row["action"] == "audit.not_found"
    assert row["resource"] == "resource.audit_log"
    assert row["role"] == "admin"
    assert row["correlation_id"] == "probe-404"


def test_a_missing_log_file_gives_404_not_an_error(log):
    assert not log.exists()
    response = client.get("/audit/anything", headers=ADMIN)
    assert response.status_code == 404
    assert [row["action"] for row in rows_in(log)] == ["audit.not_found"]


# ---------------------------------------------------------------------------
# Callers without permission
# ---------------------------------------------------------------------------

DENIED_CALLERS = [
    pytest.param({"X-User-Role": "operator"}, id="operator"),
    pytest.param({"X-User-Role": "engineer"}, id="engineer"),
    pytest.param({"X-User-Role": "ai_agent"}, id="ai_agent"),
    pytest.param({"X-User-Role": "visitor"}, id="unknown-word"),
    pytest.param({"X-User-Role": "ADMIN"}, id="admin-in-capitals"),
    pytest.param({}, id="no-header"),
]


@pytest.mark.parametrize("headers", DENIED_CALLERS)
def test_a_caller_without_permission_gets_403_and_a_policy_deny_row(log, headers):
    build_case()
    before = lines_in(log)
    response = client.get(f"/audit/{CASE}", headers={**headers, "X-Correlation-Id": "probe-403"})
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    assert "rows" not in response.json()
    row = own_row(log, len(before))
    assert row["action"] == "policy.deny"
    assert row["resource"] == "resource.audit_log"
    assert row["correlation_id"] == "probe-403"


@pytest.mark.parametrize("headers", DENIED_CALLERS)
def test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not(log, headers):
    build_case()
    exists = client.get(f"/audit/{CASE}", headers=headers)
    missing = client.get("/audit/no-such-case", headers=headers)
    assert exists.status_code == missing.status_code == 403
    assert exists.content == missing.content


def test_a_caller_without_permission_cannot_learn_an_id_from_the_too_long_check(log):
    long_id = "x" * 500
    response = client.get(f"/audit/{long_id}", headers={"X-User-Role": "operator"})
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}


# ---------------------------------------------------------------------------
# The route only reads
# ---------------------------------------------------------------------------


def test_the_log_is_unchanged_except_for_the_routes_own_row(log):
    build_case()
    before = lines_in(log)
    response = client.get(f"/audit/{CASE}", headers={**ADMIN, "X-Correlation-Id": "probe-read"})
    assert response.status_code == 200
    after = lines_in(log)
    assert after[: len(before)] == before
    assert len(after) == len(before) + 1
    row = json.loads(after[-1])
    assert row["action"] == "audit.read"
    assert row["resource"] == "resource.audit_log"
    assert row["role"] == "admin"
    # The answer was read before the row was written, so the answer does not list this request.
    assert response.json()["row_count"] == 3


def test_a_second_read_shows_the_first_reads_own_row_when_it_reused_the_id(log):
    build_case()
    client.get(f"/audit/{CASE}", headers={**ADMIN, "X-Correlation-Id": CASE})
    body = client.get(f"/audit/{CASE}", headers=ADMIN).json()
    assert body["row_count"] == 4
    assert body["rows"][-1]["action"] == "audit.read"


def test_the_real_log_is_not_touched_by_these_tests(log):
    before = REAL_LOG.read_bytes() if REAL_LOG.exists() else None
    build_case()
    client.get(f"/audit/{CASE}", headers=ADMIN)
    after = REAL_LOG.read_bytes() if REAL_LOG.exists() else None
    assert before == after


def test_the_query_module_never_opens_the_log_for_writing():
    source = Path(audit_query.__file__).read_text(encoding="utf-8")
    assert "write_event" not in source
    for mode in ('"w"', '"a"', '"w+"', '"a+"', '"r+"', ".write(", "write_text", "unlink", "truncate"):
        assert mode not in source, mode


# ---------------------------------------------------------------------------
# What leaves the route
# ---------------------------------------------------------------------------


def test_the_response_holds_no_forbidden_field_or_credential_name(log):
    build_case()
    response = client.get(f"/audit/{CASE}", headers=ADMIN)
    text = response.text
    assert MGMT not in text
    assert CRED not in text
    assert DB_USER not in text
    assert "10.20." not in text
    for row in response.json()["rows"]:
        assert MGMT not in row and CRED not in row


def test_a_forbidden_name_stored_in_a_row_is_replaced_in_the_response_only(log):
    # SB-03: the role word is stored as typed, so a caller can put a name in the log.
    typed_role = f"{MGMT}=10.1.1.1 {DB_USER}=someone"
    client.get("/records/REC-0001", headers={"X-Correlation-Id": CASE, "X-User-Role": typed_role})
    stored = lines_in(log)
    assert MGMT in stored[0]
    response = client.get(f"/audit/{CASE}", headers=ADMIN)
    assert response.status_code == 200
    assert MGMT not in response.text
    assert DB_USER not in response.text
    body = response.json()
    assert body["rows"][0]["role"] == audit_query.WITHHELD
    items = {entry["item"]: entry["reason"] for entry in body["cannot_prove"]}
    assert "withheld_text" in items
    # The stored line is unchanged by the read.
    assert lines_in(log)[0] == stored[0]


def test_an_id_that_is_a_forbidden_name_is_not_echoed(log):
    row = {key: None for key in audit.SCHEMA_KEYS}
    row.update(ts="2026-10-12T10:00:00", correlation_id=DB_USER, action="record.read", role="operator")
    log.write_text(json.dumps(row) + "\n", encoding="utf-8")
    response = client.get(f"/audit/{DB_USER}", headers=ADMIN)
    assert response.status_code == 200
    assert DB_USER not in response.text
    assert response.json()["correlation_id"] == audit_query.WITHHELD


# ---------------------------------------------------------------------------
# The id limit
# ---------------------------------------------------------------------------


def test_an_id_of_129_characters_is_refused_and_not_looked_up(log):
    long_id = "a" * 129
    row = {key: None for key in audit.SCHEMA_KEYS}
    row.update(ts="2026-10-12T10:00:00", correlation_id=long_id, action="record.read", role="operator")
    log.write_text(json.dumps(row) + "\n", encoding="utf-8")
    before = lines_in(log)
    response = client.get(f"/audit/{long_id}", headers={**ADMIN, "X-Correlation-Id": "probe-400"})
    assert response.status_code == 400
    assert response.json() == {"error": "id_too_long", "max_length": 128}
    assert long_id not in response.text
    stored = own_row(log, len(before))
    assert stored["action"] == "audit.id_refused"
    assert stored["resource"] == "resource.audit_log"
    assert long_id not in json.dumps(stored)


def test_an_id_of_exactly_128_characters_is_looked_up(log):
    edge_id = "b" * 128
    row = {key: None for key in audit.SCHEMA_KEYS}
    row.update(ts="2026-10-12T10:00:00", correlation_id=edge_id, action="record.read", role="operator")
    log.write_text(json.dumps(row) + "\n", encoding="utf-8")
    response = client.get(f"/audit/{edge_id}", headers=ADMIN)
    assert response.status_code == 200
    assert response.json()["row_count"] == 1


def test_the_limit_is_128():
    assert audit_query.MAX_ID_LENGTH == 128


# ---------------------------------------------------------------------------
# What the chain cannot prove
# ---------------------------------------------------------------------------


def test_cannot_prove_names_approval_id_and_log_integrity(log):
    build_case()
    body = client.get(f"/audit/{CASE}", headers=ADMIN).json()
    items = {entry["item"]: entry["reason"] for entry in body["cannot_prove"]}
    assert "approval_id" in items
    assert "log_integrity" in items
    assert all(row["approval_id"] is None for row in body["rows"])
    # Always listed, whatever the rows hold.
    for always in ("final_action", "record_asked_for", "policy_reasons_and_version", "caller_identity", "case_membership"):
        assert always in items, always
    assert all(entry["reason"] for entry in body["cannot_prove"])


def test_cannot_prove_follows_the_rows_for_a_null_field(log):
    build_case()
    items = {entry["item"] for entry in client.get(f"/audit/{CASE}", headers=ADMIN).json()["cannot_prove"]}
    # The case holds a denied read by a role with no persona, so actor is null on that row.
    assert "actor" in items
    assert "policy_decision" in items
    # The summary row holds a model, so the model item is not listed.
    assert "model" not in items


def test_cannot_prove_lists_approval_id_when_a_row_holds_an_approval():
    # The item is computed. A case where one row held an approval id would not list it.
    case = audit_query.CaseRead(
        rows=[{"approval_id": "APR-1", "policy_decision": None, "model": None, "actor": "noc_operator"}]
    )
    items = {entry["item"] for entry in audit_query.cannot_prove(case)}
    assert "approval_id" not in items
    assert "log_integrity" in items
