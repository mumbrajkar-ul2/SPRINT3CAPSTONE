"""Python policy copy built from the semantic-layer access grants."""

from __future__ import annotations

import os
import shutil
from typing import Any

POLICY_VERSION = "0.1.0-proposed"

ROLE_IDS = {
    "operator": "persona.noc_operator",
    "engineer": "persona.network_engineer",
    "ai_agent": "persona.ai_agent",
    "admin": "role.admin",
    "clinician": "role.clinician",
}


def _expanded_grants() -> list[dict[str, str]]:
    definitions = [
        ("persona.noc_operator", "action.read", ["resource.device", "resource.alarm", "resource.incident", "resource.circuit"], "purpose.incident_triage", "scope.all_records", "risk.read_only"),
        ("persona.noc_operator", "action.summarize", ["resource.incident", "resource.device"], "purpose.incident_triage", "scope.assigned_incident", "risk.recommendation"),
        ("persona.noc_operator", "action.recommend", ["resource.incident", "resource.device"], "purpose.incident_triage", "scope.assigned_incident", "risk.recommendation"),
        ("persona.noc_operator", "action.approve", ["resource.ai_invocation"], "purpose.incident_triage", "scope.assigned_incident", "risk.decision"),
        ("persona.noc_operator", "action.write", ["resource.incident"], "purpose.incident_triage", "scope.assigned_incident", "risk.decision"),
        ("persona.network_engineer", "action.read", ["resource.device", "resource.circuit", "resource.alarm", "resource.incident", "resource.sensitive_device_fields"], "purpose.network_change_planning", "scope.all_records", "risk.read_only"),
        ("persona.network_engineer", "action.recommend", ["resource.device"], "purpose.network_change_planning", "scope.all_records", "risk.recommendation"),
        ("persona.network_engineer", "action.approve", ["resource.approval"], "purpose.network_change_planning", "scope.all_records", "risk.decision"),
        ("persona.field_engineer", "action.read", ["resource.device", "resource.alarm"], "purpose.field_repair", "scope.one_site", "risk.read_only"),
        ("persona.customer_support", "action.read", ["resource.circuit", "resource.service_order", "resource.incident"], "purpose.customer_enquiry", "scope.one_customer", "risk.read_only"),
        ("persona.automation_service", "action.read", ["resource.device"], "purpose.scheduled_automation", "scope.all_records", "risk.read_only"),
        ("persona.automation_service", "action.execute", ["resource.device", "resource.circuit"], "purpose.scheduled_automation", "scope.assigned_incident", "risk.live_network_change"),
        ("persona.vendor_account", "action.read", ["resource.device", "resource.alarm"], "purpose.vendor_support", "scope.own_vendor_devices", "risk.read_only"),
        ("persona.ai_agent", "action.read", ["resource.device", "resource.alarm", "resource.incident"], "purpose.ai_assistance", "scope.assigned_incident", "risk.read_only"),
        ("persona.ai_agent", "action.summarize", ["resource.incident", "resource.device"], "purpose.ai_assistance", "scope.assigned_incident", "risk.recommendation"),
        ("persona.ai_agent", "action.recommend", ["resource.incident", "resource.device"], "purpose.ai_assistance", "scope.assigned_incident", "risk.recommendation"),
        ("role.admin", "action.read", ["resource.audit_log"], "purpose.audit_review", "scope.all_records", "risk.read_only"),
    ]
    grants: list[dict[str, str]] = []
    for role, action, resources, purpose, scope, risk in definitions:
        for resource in resources:
            grants.append(
                {
                    "row": f"TA-{len(grants) + 1:02d}",
                    "role": role,
                    "action": action,
                    "resource": resource,
                    "purpose": purpose,
                    "scope": scope,
                    "risk": risk,
                }
            )
    return grants


ACCESS = {"grants": _expanded_grants()}
AI = {
    "required_keys": [
        "persona",
        "action",
        "resource",
        "risk",
        "policy_result",
        "approval_required",
        "approval_id",
        "audit_row_written",
        "change_plan_ok",
        "record_found",
        "forbidden_field_in_prompt",
        "stale_topology_flag",
        "output_schema_ok",
        "timeout_hit",
        "policy_version",
    ],
    "risk_for": {
        "action.summarize": "risk.recommendation",
        "action.recommend": "risk.recommendation",
        "action.execute": "risk.live_network_change",
    },
}


def engine_name() -> str:
    setting = os.getenv("POLICY_ENGINE", "python")
    if setting == "auto":
        return "opa" if shutil.which("opa") else "python"
    return setting


def reset_engine_cache() -> None:
    return None


def evaluate_access(payload: dict[str, Any]) -> dict[str, Any]:
    if engine_name() == "opa" and shutil.which("opa") is None:
        return {"allow": False, "matrix_rows": [], "reasons": ["policy_engine_error"]}
    role = payload.get("role")
    role = ROLE_IDS.get(role, role)
    matched = []
    fields = ("action", "resource", "purpose", "scope", "risk")
    for grant in ACCESS["grants"]:
        if grant["role"] == role and all(payload.get(name) == grant[name] for name in fields):
            matched.append(grant["row"])
    allow = bool(matched)
    if payload.get("action") == "action.execute" and not _present(payload.get("approval_id")):
        allow = False
    return {"allow": allow, "matrix_rows": matched, "reasons": [] if allow else ["policy.opa.default_deny"]}


def _present(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_ai(payload: Any) -> bool:
    if not isinstance(payload, dict) or any(key not in payload for key in AI["required_keys"]):
        return False
    if payload["action"] not in AI["risk_for"]:
        return False
    if payload["risk"] != AI["risk_for"][payload["action"]]:
        return False
    if payload["persona"] not in {"persona.automation_service", "persona.ai_agent", "persona.noc_operator"}:
        return False
    if payload["policy_result"] not in {"allow", "deny"}:
        return False
    for name in ("approval_required", "audit_row_written", "change_plan_ok", "record_found", "forbidden_field_in_prompt", "timeout_hit"):
        if type(payload[name]) is not bool:
            return False
    if payload["stale_topology_flag"] not in (True, False, None):
        return False
    if payload["output_schema_ok"] not in (True, False, None):
        return False
    return isinstance(payload["policy_version"], str)


def _ai_action_python(payload: Any) -> dict[str, Any]:
    if not _valid_ai(payload):
        return {"outcome": "BLOCK", "reasons": ["input_invalid"], "policy_version": POLICY_VERSION}
    if payload["policy_result"] != "allow" or not payload["record_found"] or payload["forbidden_field_in_prompt"]:
        reason = "failmode.missing_id" if not payload["record_found"] else "failmode.forbidden_field_in_prompt"
        return {"outcome": "BLOCK", "reasons": [reason], "policy_version": POLICY_VERSION}
    if payload["stale_topology_flag"] is True:
        return {"outcome": "BLOCK", "reasons": ["failmode.stale_topology_true"], "policy_version": POLICY_VERSION}
    if payload["policy_version"] != POLICY_VERSION:
        return {"outcome": "HOLD_FOR_REVIEW", "reasons": ["policy_version_differs"], "policy_version": POLICY_VERSION}
    if payload["timeout_hit"]:
        return {"outcome": "HOLD_FOR_REVIEW", "reasons": ["failmode.timeout"], "policy_version": POLICY_VERSION}
    if payload["output_schema_ok"] is not True:
        return {"outcome": "HOLD_FOR_REVIEW", "reasons": ["failmode.schema_failure"], "policy_version": POLICY_VERSION}
    if payload["stale_topology_flag"] is None:
        return {"outcome": "HOLD_FOR_REVIEW", "reasons": ["failmode.stale_topology_blank"], "policy_version": POLICY_VERSION}
    if payload["action"] == "action.summarize":
        return {"outcome": "RECOMMEND_ONLY", "reasons": ["ai_use.incident_summary"], "policy_version": POLICY_VERSION}
    if payload["action"] == "action.recommend":
        return {"outcome": "HOLD_FOR_REVIEW", "reasons": ["ai_use.next_action_recommendation"], "policy_version": POLICY_VERSION}
    execute = (
        payload["persona"] == "persona.automation_service"
        and payload["approval_required"]
        and _present(payload["approval_id"])
        and payload["audit_row_written"]
        and payload["change_plan_ok"]
    )
    return {
        "outcome": "EXECUTE" if execute else "BLOCK",
        "reasons": ["ai_use.remediation_execution"] if execute else ["rule.ai_recommendation_needs_policy_approval_audit_before_state_change"],
        "policy_version": POLICY_VERSION,
    }


def evaluate_ai_action(payload: Any) -> dict[str, Any]:
    if engine_name() == "opa" and shutil.which("opa") is None:
        return {"outcome": "BLOCK", "reasons": ["policy_engine_error"], "policy_version": POLICY_VERSION}
    return _ai_action_python(payload)


def check_audit_read(role: str | None) -> dict[str, Any]:
    return evaluate_access(
        {
            "role": role,
            "action": "action.read",
            "resource": "resource.audit_log",
            "purpose": "purpose.audit_review",
            "scope": "scope.all_records",
            "risk": "risk.read_only",
        }
    )
