"""Security test: client-sent policy fields are ignored. Stage S05-13 Half B (NG-02).

The server works out every policy field. A caller who sends `approval_required`,
`approval_id`, `outcome`, or a policy result in the body or the query string
changes nothing. Design: docs/13-security-validation/negative-tests.md.
"""

import json

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit

pytestmark = pytest.mark.security

FORGED_ID = "APR-FORGED-" + "1"
FORGED_BODY = {
    "approval_required": False,
    "approval_id": FORGED_ID,
    "outcome": "EXECUTE",
    "policy_result": "allow",
    "audit_row_written": True,
    "change_plan_ok": True,
}
FORGED_QUERY = f"?approval_id={FORGED_ID}&approval_required=false&outcome=EXECUTE"


def test_client_sent_policy_fields_change_nothing(tmp_path, monkeypatch):
    log = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", log)
    client = TestClient(app)
    headers = {"X-User-Role": "operator"}

    # A: a forged body on the summarize route.
    a = client.post("/ai/summarize/REC-0001", headers=headers, json=FORGED_BODY)
    # B: forged values in the query string of the same route.
    b = client.post("/ai/summarize/REC-0001" + FORGED_QUERY, headers=headers)
    # C: forged values in the query string of the record route.
    c = client.get("/records/REC-0001" + FORGED_QUERY, headers=headers)

    assert a.status_code == 200
    assert b.status_code == 200
    assert c.status_code == 200
    for body in (a.json(), b.json()):
        assert body["outcome"] == "RECOMMEND_ONLY"
        assert body["approval_id"] is None
        assert body["approval_required"] is False
    assert c.json()["device_id"] == "REC-0001"

    text = log.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in text.splitlines()]
    assert len(rows) == 3
    assert [row["action"] for row in rows] == ["ai.summary", "ai.summary", "record.read"]
    assert [row["outcome"] for row in rows] == ["RECOMMEND_ONLY", "RECOMMEND_ONLY", None]
    assert all(row["approval_id"] is None for row in rows)
    assert FORGED_ID not in text


def test_no_route_reads_an_approval_id_from_the_caller():
    """The routes take no body model and no query value named like a policy field."""
    names = {"approval_id", "approval_required", "outcome", "policy_result"}
    checked = 0
    for route in app.routes:
        dependant = getattr(route, "dependant", None)
        if dependant is None:
            continue
        checked += 1
        parameters = {p.name for p in dependant.query_params + dependant.body_params}
        assert parameters.isdisjoint(names), f"{route.path} reads {parameters & names}"
    # FastAPI adds its own docs routes. The three app routes are among those checked.
    assert checked >= 3
