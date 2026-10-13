"""Audit row keys and the temporary log. Stage S07. PRD RQ-40, RQ-41, RQ-69, RQ-72."""

import uuid

from apps.api.services import audit
from tests.app.helpers import ADMIN, ENGINEER, GOOD_ID, OPERATOR

REAL_LOG = audit.LOG
LONG_ID = "x" * 129


def every_route(client, case="keys-case-1"):
    """Call each route once so each kind of row is written."""
    headers = {**OPERATOR, "X-Correlation-Id": case}
    client.get("/health")
    client.get(f"/records/{GOOD_ID}", headers=headers)
    client.get("/alarms/storms/STO-00002", headers=headers)
    client.post(f"/ai/summarize/{GOOD_ID}", headers=headers)
    client.post(f"/ai/recommend/{GOOD_ID}", headers=headers)
    client.post(f"/approvals/{GOOD_ID}", headers=headers, json={"decision": "yes"})
    client.get(f"/audit/{case}", headers={**ADMIN, "X-Correlation-Id": case})
    client.get(f"/records/{GOOD_ID}", headers={"X-Correlation-Id": case})
    client.get(f"/audit/{case}", headers={**OPERATOR, "X-Correlation-Id": case})


def test_every_row_has_record_id_as_the_16th_key(client, audit_log):
    every_route(client)
    rows = audit_log()
    assert len(rows) >= 8
    for row in rows:
        keys = list(row)
        assert keys[15] == "record_id"
        assert len(keys) == 17
    assert list(audit.SCHEMA_KEYS)[15] == "record_id"
    reads = {r["action"]: r for r in rows}
    # A read of one device writes that device id.
    assert reads["record.read"]["record_id"] == GOOD_ID
    assert reads["ai.summary"]["record_id"] == GOOD_ID
    assert reads["ai.recommendation"]["record_id"] == GOOD_ID
    assert reads["ai.approval"]["record_id"] == GOOD_ID
    # A row that names no device keeps the key and holds null.
    assert reads["record.storm_read"]["record_id"] is None
    assert reads["audit.read"]["record_id"] is None


def test_every_row_has_final_action_none(client, audit_log):
    every_route(client)
    rows = audit_log()
    assert len(rows) >= 8
    for row in rows:
        assert list(row)[16] == "final_action"
        assert row["final_action"] == "none"
    assert list(audit.SCHEMA_KEYS)[16] == "final_action"


def test_unknown_role_word_is_not_stored_as_sent(client, audit_log):
    # RQ-69. The test sends a correlation id of 129 characters. The audit row and the response
    # header hold a new UUID. The long text appears nowhere. The call is not refused.
    response = client.get(
        f"/records/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": LONG_ID}
    )
    assert response.status_code == 200
    header = response.headers["x-correlation-id"]
    assert uuid.UUID(header).version == 4
    assert LONG_ID not in header
    rows = audit_log()
    assert rows[0]["correlation_id"] == header
    assert LONG_ID not in audit_log.path.read_text(encoding="utf-8")
    assert LONG_ID not in response.text


def test_a_correlation_id_of_128_characters_is_kept(client, audit_log):
    kept = "y" * 128
    response = client.get(f"/records/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": kept})
    assert response.headers["x-correlation-id"] == kept
    assert audit_log()[0]["correlation_id"] == kept


def test_every_route_answers_with_the_correlation_id_header(client):
    sent = {"X-Correlation-Id": "header-case-1"}
    calls = [
        client.get("/health", headers=sent),
        client.get("/", headers=sent),
        client.get("/ready", headers=sent),
        client.get(f"/records/{GOOD_ID}", headers={**OPERATOR, **sent}),
        client.get("/alarms/storms/STO-00002", headers={**OPERATOR, **sent}),
        client.get("/alarms/storms/STO-NOPE", headers={**OPERATOR, **sent}),
        client.post(f"/ai/recommend/{GOOD_ID}", headers={**OPERATOR, **sent}),
        client.post(f"/approvals/{GOOD_ID}", headers={**OPERATOR, **sent}, json={}),
        client.get("/audit/header-case-1", headers={**ADMIN, **sent}),
    ]
    assert [c.headers["x-correlation-id"] for c in calls] == ["header-case-1"] * len(calls)


def test_app_tests_do_not_write_to_the_real_audit_log(client, audit_log):
    # RQ-72. The fixture in tests/app/conftest.py points the log at a temporary file.
    assert audit.LOG != REAL_LOG
    assert audit.LOG == audit_log.path
    before = REAL_LOG.stat().st_size if REAL_LOG.exists() else None
    every_route(client, case="real-log-check")
    after = REAL_LOG.stat().st_size if REAL_LOG.exists() else None
    assert after == before
    assert audit_log.path.exists()
    assert "real-log-check" not in (REAL_LOG.read_text(encoding="utf-8") if REAL_LOG.exists() else "")


def test_the_engineer_role_is_stored_as_the_word_sent_and_its_persona(client, audit_log):
    client.get(f"/records/{GOOD_ID}", headers=ENGINEER)
    row = audit_log()[0]
    assert (row["role"], row["actor"]) == ("engineer", "network_engineer")
