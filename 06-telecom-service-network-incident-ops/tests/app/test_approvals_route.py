"""POST /approvals/{id}. Stage S07. PRD RQ-32 to RQ-35, RQ-38, RQ-39.

A decision is stored only for a recommendation that was shown with text under the same
X-Correlation-Id. Each test first asks for a recommendation with that id.
"""

import hashlib
import json
from pathlib import Path

import pytest

from apps.api.services import approvals, policy
from tests.app.helpers import ADMIN, BLANK_FLAG_ID, ENGINEER, GOOD_ID, OPERATOR, STALE_ID

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
CASE = "approval-case-1"
FIVE_KEYS = {"approval_id", "decision", "approver", "record_id", "correlation_id"}


def show_recommendation(client, record_id=GOOD_ID, case=CASE):
    response = client.post(
        f"/ai/recommend/{record_id}", headers={**OPERATOR, "X-Correlation-Id": case}
    )
    assert response.status_code == 202
    return response


def decide(client, decision, record_id=GOOD_ID, case=CASE, headers=OPERATOR, body="default"):
    payload = {"decision": decision} if body == "default" else body
    return client.post(
        f"/approvals/{record_id}",
        headers={**headers, "X-Correlation-Id": case},
        json=payload,
    )


def data_hashes():
    return {
        str(path.relative_to(DATA)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(DATA.rglob("*"))
        if path.is_file()
    }


def test_yes_is_stored_with_decision_approver_and_a_server_made_id(client, audit_log, approvals_file):
    show_recommendation(client)
    response = decide(client, "yes")
    assert response.status_code == 200
    body = response.json()
    assert set(body) == FIVE_KEYS
    assert body["decision"] == "yes"
    assert body["approver"] == "persona.noc_operator"
    assert body["record_id"] == GOOD_ID
    assert body["correlation_id"] == CASE
    assert body["approval_id"].startswith(approvals.APPROVAL_ID_PREFIX)
    stored = approvals.read_all()
    assert len(stored) == 1
    assert {key: stored[0][key] for key in FIVE_KEYS} == body
    # The audit row came first and holds the id the server made.
    row = [r for r in audit_log() if r["action"] == "ai.approval"][0]
    assert row["approval_id"] == body["approval_id"]
    assert row["record_id"] == GOOD_ID
    assert row["resource"] == "resource.ai_invocation"
    assert row["correlation_id"] == CASE
    assert row["final_action"] == "none"


def test_the_caller_cannot_choose_the_approver_or_the_approval_id(client):
    show_recommendation(client)
    response = decide(
        client, "yes", body={"decision": "yes", "approver": "persona.admin", "approval_id": "APR-CALLER-CHOSE"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["approver"] == "persona.noc_operator"
    assert body["approval_id"] != "APR-CALLER-CHOSE"
    assert "APR-CALLER-CHOSE" not in json.dumps(approvals.read_all())


def test_a_no_is_stored_as_no_with_no_approval_id(client, audit_log):
    show_recommendation(client)
    response = decide(client, "no")
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "no"
    assert body["approval_id"] is None
    assert approvals.read_all()[0]["decision"] == "no"
    assert approvals.read_all()[0]["approval_id"] is None
    row = [r for r in audit_log() if r["action"] == "ai.approval"][0]
    assert row["approval_id"] is None


def test_a_no_never_unlocks_the_approval_check(client):
    show_recommendation(client)
    body = decide(client, "no").json()
    fixture = json.loads(
        (REPO / "policy" / "tests" / "fixtures" / "ai-01-execute-with-all-checks.json").read_text(encoding="utf-8")
    )["ai-01-execute-with-all-checks"]["input"]
    # The approval id a no gives the policy is null. With every other check true, the policy
    # still does not answer EXECUTE.
    result = policy.evaluate_ai_action({**fixture, "approval_id": body["approval_id"]})
    assert result["outcome"] != "EXECUTE"
    assert body["approval_id"] is None
    # Limit. The policy checks only that the approval id is not blank. It does not look the id up
    # in the approvals store. This is why no route may take an approval id from the caller
    # (RQ-38) and why the reply of a no carries null. Recorded as a risk in docs/demo/evidence.md.


def test_a_second_call_stores_a_second_record(client):
    show_recommendation(client)
    first = decide(client, "yes").json()
    second = decide(client, "yes").json()
    stored = approvals.read_all()
    assert len(stored) == 2
    assert first["approval_id"] != second["approval_id"]


@pytest.mark.parametrize("body", [None, {}, {"decision": "maybe"}, {"decision": "YES"}, {"decision": True}, {"decision": ["yes"]}, ["yes"], "yes"])
def test_a_bad_body_returns_422_and_stores_nothing(client, audit_log, approvals_file, body):
    show_recommendation(client)
    response = decide(client, None, body=body)
    assert response.status_code == 422
    assert approvals.read_all() == []
    assert [r["action"] for r in audit_log()] == ["ai.recommendation"]


def test_an_unreadable_body_returns_422(client):
    show_recommendation(client)
    response = client.post(
        f"/approvals/{GOOD_ID}",
        headers={**OPERATOR, "X-Correlation-Id": CASE, "Content-Type": "application/json"},
        content=b"{not json",
    )
    assert response.status_code == 422
    assert approvals.read_all() == []


def test_the_role_check_runs_before_the_body_check(client, audit_log):
    response = decide(client, None, headers=ADMIN, body={"decision": "maybe"})
    assert response.status_code == 403


def test_decision_without_a_shown_recommendation_returns_404(client, audit_log):
    # No recommendation under this case id.
    response = decide(client, "yes", case="never-recommended")
    assert response.status_code == 404
    assert response.json() == {"error": "not_found"}
    assert approvals.read_all() == []
    # A recommendation for another device under the same case id does not count.
    show_recommendation(client, GOOD_ID, case="other-device")
    assert decide(client, "yes", record_id="DEV-00019", case="other-device").status_code == 404
    # A recommendation that was held with no text does not count.
    client.post(f"/ai/recommend/{BLANK_FLAG_ID}", headers={**OPERATOR, "X-Correlation-Id": "held-case"})
    assert decide(client, "yes", record_id=BLANK_FLAG_ID, case="held-case").status_code == 404
    # A recommendation that was blocked does not count.
    client.post(f"/ai/recommend/{STALE_ID}", headers={**OPERATOR, "X-Correlation-Id": "blocked-case"})
    assert decide(client, "yes", record_id=STALE_ID, case="blocked-case").status_code == 404
    assert approvals.read_all() == []
    assert not [r for r in audit_log() if r["action"] == "ai.approval"]


def test_a_call_with_no_correlation_id_gets_404(client):
    show_recommendation(client)
    response = client.post(f"/approvals/{GOOD_ID}", headers=OPERATOR, json={"decision": "yes"})
    assert response.status_code == 404


def test_other_roles_get_403_and_a_deny_row(client, audit_log):
    show_recommendation(client)
    for headers in (ENGINEER, ADMIN, {"X-User-Role": "ai_agent"}, {"X-User-Role": "automation_service"}, {}):
        response = decide(client, "yes", headers=headers)
        assert response.status_code == 403
        assert response.json() == {"error": "forbidden"}
    rows = [r for r in audit_log() if r["action"] != "ai.recommendation"]
    assert [r["action"] for r in rows] == ["policy.deny"] * 5
    assert {r["resource"] for r in rows} == {"resource.ai_invocation"}
    assert rows[-1]["role"] is None
    assert approvals.read_all() == []


def test_an_approval_leaves_every_data_file_unchanged(client):
    before = data_hashes()
    assert before  # the data folder has files
    show_recommendation(client)
    decide(client, "yes")
    decide(client, "no")
    assert data_hashes() == before


def test_the_approval_store_is_not_under_data(approvals_file):
    assert DATA not in approvals_file.parents
    assert DATA not in approvals.STORE.parents
