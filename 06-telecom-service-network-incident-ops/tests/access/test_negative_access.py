"""Negative access cases from docs/03-identity/negative-access-test-plan.md.

The recommend and execute decisions are the target rows. The live app has no
recommend route and no execute route. S04-06 is the stage that enforces them
in policy. These tests record the target decision and check the live routes.
"""

import json

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit

# Stage S05-13 Half B: every test in this file is part of the security suite.
pytestmark = pytest.mark.security

client = TestClient(app)

TA_33 = {
    "role": "persona.ai_agent",
    "action": "action.recommend",
    "resource": "resource.incident",
    "purpose": "purpose.ai_assistance",
    "scope": "scope.assigned_incident",
    "risk": "risk.recommendation",
}

AI_AGENT_EXECUTE = {
    "role": "persona.ai_agent",
    "action": "action.execute",
    "resource": "resource.device",
    "purpose": "purpose.ai_assistance",
    "scope": "scope.assigned_incident",
    "risk": "risk.live_network_change",
}

AUTOMATION_EXECUTE_WITHOUT_APPROVAL = {
    "role": "persona.automation_service",
    "action": "action.execute",
    "resource": "resource.device",
    "purpose": "purpose.scheduled_automation",
    "scope": "scope.assigned_incident",
    "risk": "risk.live_network_change",
    "approval_id": None,
}

AI_AGENT_DENIED_ACTIONS = {"action.approve", "action.execute", "action.write"}
FIVE_FIELDS = ("role", "resource", "purpose", "scope", "risk")


def target_decision(payload):
    """Target decision for the three policy cases in this file.

    persona.ai_agent is denied action.execute (and approve and write).
    persona.automation_service execute with an empty approval id is deny.
    The TA-33 field set is allow. S04-06 replaces this function with Rego.
    """
    if (
        payload.get("role") == "persona.ai_agent"
        and payload.get("action") in AI_AGENT_DENIED_ACTIONS
    ):
        return "deny"
    if (
        payload.get("role") == "persona.automation_service"
        and payload.get("action") == "action.execute"
        and payload.get("approval_id") is None
    ):
        return "deny"
    fields = {name: payload[name] for name in ("role", "action", *FIVE_FIELDS)}
    if fields == TA_33:
        return "allow"
    return "deny"


def route_paths():
    return [getattr(route, "path", "") for route in app.routes]


def test_noc_operator_mapped_role_may_read_record():
    """NA-01. The mapped API role for persona.noc_operator may read a device.

    role: persona.noc_operator (live header operator, role.operator, Inference)
    action: action.read
    resource: resource.device
    purpose: purpose.incident_triage
    scope: scope.all_records
    risk: risk.read_only
    target: TA-01 allow
    """
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "operator"},
    )
    assert response.status_code == 200
    assert response.json()["device_id"] == "REC-0001"


def test_clinician_role_is_denied_on_record_read():
    """NA-02. role.clinician is denied on a device read.

    role: role.clinician
    action: action.read
    resource: resource.device
    purpose: purpose.incident_triage
    scope: scope.all_records
    risk: risk.read_only
    """
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "clinician"},
    )
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}


def test_ai_agent_may_recommend():
    """NA-03. persona.ai_agent may recommend. The live read still returns the row.

    role: persona.ai_agent
    action: action.recommend
    resource: resource.incident
    purpose: purpose.ai_assistance
    scope: scope.assigned_incident
    risk: risk.recommendation
    target: TA-33 allow
    """
    assert target_decision(TA_33) == "allow"
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "ai_agent"},
    )
    assert response.status_code == 200
    assert response.json()["device_id"] == "REC-0001"


def test_ai_agent_may_not_execute():
    """NA-04. persona.ai_agent may not execute. The live app has no execute route.

    role: persona.ai_agent
    action: action.execute
    resource: resource.device
    purpose: purpose.ai_assistance
    scope: scope.assigned_incident
    risk: risk.live_network_change
    """
    assert target_decision(AI_AGENT_EXECUTE) == "deny"
    paths = route_paths()
    assert "/health" in paths
    assert "/records/{record_id}" in paths
    assert "/ai/summarize/{record_id}" in paths
    assert all("execute" not in path for path in paths)


def test_automation_service_may_not_execute_without_approval_id():
    """NA-05. persona.automation_service may not execute when the approval id is empty.

    The record-route forbidden body is a separate fact: the header is outside
    the allow list. The empty approval id is the target deny for TA-24.
    role: persona.automation_service
    action: action.execute
    resource: resource.device
    purpose: purpose.scheduled_automation
    scope: scope.assigned_incident
    risk: risk.live_network_change
    approval_id: null (provenance.approval_id)
    """
    assert AUTOMATION_EXECUTE_WITHOUT_APPROVAL["approval_id"] is None
    assert target_decision(AUTOMATION_EXECUTE_WITHOUT_APPROVAL) == "deny"
    assert all("execute" not in path for path in route_paths())
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "automation_service"},
    )
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}


def test_missing_role_header_is_refused(tmp_path, monkeypatch):
    """NA-06. Replaces test_missing_role_header_keeps_operator_default (S07, PRD O-4, RQ-01).

    That test locked HTTP 200 for a call with no role header, because the route
    defaulted to role.operator. A call with no role has no caller. The route returns
    403 and writes a policy.deny row with a null role. rule.no_default_role.
    """
    monkeypatch.setattr(audit, "LOG", tmp_path / "audit.log")
    response = client.get("/records/REC-0001")
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    rows = [json.loads(line) for line in (tmp_path / "audit.log").read_text().splitlines()]
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["role"] is None
