"""The demo flow, end to end. Stage S07. PRD RQ-48 and RQ-62.

Each test plays the steps the page plays, with one X-Correlation-Id, and then reads the chain.
"""

import time

from apps.api.services import ai_gateway, approvals
from tests.app.helpers import ADMIN, GOOD_ID, MISSING_ID, OPERATOR

CHAIN_WITH_TEXT = ["record.storm_read", "record.read", "ai.recommendation", "ai.approval"]


def walk(client, case, storm="STO-00002", record_id=GOOD_ID, decision="yes"):
    """The steps of the page. Returns the reply of each step."""
    headers = {**OPERATOR, "X-Correlation-Id": case}
    replies = {}
    replies["storm"] = client.get(f"/alarms/storms/{storm}", headers=headers)
    replies["lookup"] = client.get(f"/records/{record_id}", headers=headers)
    replies["recommend"] = client.post(f"/ai/recommend/{record_id}", headers=headers)
    if decision:
        replies["decide"] = client.post(
            f"/approvals/{record_id}", headers=headers, json={"decision": decision}
        )
    # The page reads the chain with the same case id. This test sends a different id in the
    # header, so the reader's own audit row stays out of the chain it reads.
    replies["audit"] = client.get(
        f"/audit/{case}", headers={**ADMIN, "X-Correlation-Id": "reader-" + case}
    )
    return replies


def test_one_case_rebuilds_from_one_correlation_id(client, audit_log):
    replies = walk(client, "demo-case-1")
    expected = {"storm": 200, "lookup": 200, "recommend": 202, "decide": 200, "audit": 200}
    assert {name: reply.status_code for name, reply in replies.items()} == expected
    storm = replies["storm"].json()
    # The page lists the different device ids from the storm reply.
    assert {row["device_id"] for row in storm["rows"]} == {GOOD_ID}
    chain = replies["audit"].json()
    assert chain["row_count"] == 4
    assert [row["action"] for row in chain["rows"]] == CHAIN_WITH_TEXT
    assert {row["correlation_id"] for row in chain["rows"]} == {"demo-case-1"}
    assert [row["ts"] for row in chain["rows"]] == sorted(row["ts"] for row in chain["rows"])
    approval = chain["rows"][-1]
    assert approval["approval_id"] == replies["decide"].json()["approval_id"]
    assert approval["role"] == "operator"
    assert "audit.read" not in [row["action"] for row in chain["rows"]]
    names = [item["item"] for item in chain["cannot_prove"]]
    assert "caller_identity" in names
    # A yes put an approval id on the chain, so the list leaves the "null on every row" item out.
    assert "approval_id" not in names


def test_a_no_decision_is_in_the_chain_with_no_approval_id(client):
    replies = walk(client, "demo-case-no", decision="no")
    assert replies["decide"].status_code == 200
    chain = replies["audit"].json()
    rows = chain["rows"]
    assert [row["action"] for row in rows] == CHAIN_WITH_TEXT
    assert rows[-1]["approval_id"] is None
    assert "approval_id" in [item["item"] for item in chain["cannot_prove"]]
    assert approvals.read_all()[0]["decision"] == "no"


def test_ai_timeout_variant_holds_with_no_summary_and_no_approval_is_possible(client, monkeypatch):
    monkeypatch.setenv(ai_gateway.TIMEOUT_ENV, "0.05")

    def slow(prompt):
        time.sleep(0.4)

    monkeypatch.setattr(ai_gateway, "call_model", slow)
    replies = walk(client, "demo-case-timeout")
    body = replies["recommend"].json()
    assert replies["recommend"].status_code == 202
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["summary"] is None
    assert body["recommendation"] is None
    assert "failmode.timeout" in body["reasons"]
    # Nothing was shown with text, so the decision has nothing to attach to.
    assert replies["decide"].status_code == 404
    assert approvals.read_all() == []
    rows = replies["audit"].json()["rows"]
    assert [row["action"] for row in rows] == ["record.storm_read", "record.read", "policy.hold"]
    assert rows[-1]["outcome"] == "HOLD_FOR_REVIEW"
    assert replies["lookup"].status_code == 200  # the other steps keep working


def test_a_device_with_no_row_is_listed_and_then_refused(client):
    # RQ-62 example. Storm STO-00001 lists DEV-00001. devices.csv has no DEV-00001.
    replies = walk(client, "demo-case-missing", storm="STO-00001", record_id=MISSING_ID)
    assert [row["device_id"] for row in replies["storm"].json()["rows"]] == [MISSING_ID]
    assert replies["lookup"].status_code == 404
    assert replies["recommend"].status_code == 403
    assert replies["recommend"].json()["outcome"] == "BLOCK"
    assert replies["recommend"].json()["recommendation"] is None
    assert replies["decide"].status_code == 404
    rows = replies["audit"].json()["rows"]
    assert [row["action"] for row in rows] == ["record.storm_read", "policy.deny"]


def test_a_stale_device_is_blocked_and_the_chain_says_so(client):
    # Storm STO-00005 lists DEV-00005. Its stale_topology_flag is true.
    replies = walk(client, "demo-case-stale", storm="STO-00005", record_id="DEV-00005")
    assert replies["recommend"].status_code == 403
    assert replies["recommend"].json()["outcome"] == "BLOCK"
    assert replies["decide"].status_code == 404
    rows = replies["audit"].json()["rows"]
    assert rows[-1]["action"] == "policy.deny"
    assert rows[-1]["outcome"] == "BLOCK"
