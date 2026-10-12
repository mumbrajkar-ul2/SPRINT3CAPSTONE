"""Policy evaluation for the API. Stage S04-06 Half B.

Two questions are answered here.

1. Access. May this caller take this action on this resource for this purpose,
   over this scope, at this risk? Answer: allow or deny.
   Rego: policy/opa/access.rego.
2. AI action. What happens to one AI call? Answer: RECOMMEND_ONLY,
   HOLD_FOR_REVIEW, BLOCK, or EXECUTE. Rego: policy/opa/ai_action.rego.
   Design: docs/06-policy/ai-action-policy-design.md.

Engine. When the `opa` binary is on the PATH, this file runs `opa eval` on the
Rego files. When it is absent, this file applies the same decision table in
Python. The environment variable POLICY_ENGINE can force `python` or `opa`.
If the opa run fails, the answer is deny or BLOCK. The code never allows a
call because the engine failed.

Both engines read the same value lists from policy/opa/policy_data.json.
"""

import functools
import json
import os
import shutil
import subprocess
from pathlib import Path

POLICY_DIR = Path(__file__).resolve().parents[3] / "policy" / "opa"
DATA = json.loads((POLICY_DIR / "policy_data.json").read_text(encoding="utf-8"))
ACCESS = DATA["access_matrix"]
AI = DATA["ai_action_tables"]

# PROPOSED. Owner: Team-Force. The repo sets no policy version format.
POLICY_VERSION = AI["policy_version"]

ACCESS_FIELDS = ("action", "resource", "purpose", "scope", "risk")
APPROVAL_RULE = "rule.ai_recommendation_needs_policy_approval_audit_before_state_change"


class PolicyEngineError(Exception):
    """The opa run failed. The caller turns this into deny or BLOCK."""


# ---------------------------------------------------------------------------
# Engine choice
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _opa_path():
    """Where the `opa` program is, or None. The PATH is searched once per process.

    Stage S04-10 Half B (SR-02). One search cost 5.6 ms on the measuring machine
    and ran on every access decision. Only this lookup is cached. Decisions are
    not cached, and POLICY_ENGINE is still read on every call. A program
    installed after the app starts is found after a restart or reset_engine_cache().
    If the program is removed after the app starts, the opa run fails and the
    answer is deny or BLOCK.
    """
    return shutil.which("opa")


def reset_engine_cache():
    """Search the PATH again on the next call. Tests use this."""
    _opa_path.cache_clear()


def engine_name() -> str:
    wanted = os.environ.get("POLICY_ENGINE", "auto").strip().lower()
    if wanted == "python":
        return "python"
    if wanted == "opa":
        return "opa"
    return "opa" if _opa_path() else "python"


def _opa_eval(query: str, payload: dict):
    command = [
        _opa_path() or "opa", "eval",
        "--format", "json",
        "--data", str(POLICY_DIR),
        "--stdin-input",
        query,
    ]
    try:
        proc = subprocess.run(
            command,
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as err:
        raise PolicyEngineError(f"opa could not start: {err}") from err
    if proc.returncode != 0:
        raise PolicyEngineError(f"opa exited with {proc.returncode}")
    try:
        return json.loads(proc.stdout)["result"][0]["expressions"][0]["value"]
    except (KeyError, IndexError, ValueError) as err:
        raise PolicyEngineError("opa returned no value") from err


# ---------------------------------------------------------------------------
# Access policy. Python copy of policy/opa/access.rego.
# ---------------------------------------------------------------------------


def _approval_id_present(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _access_python(payload: dict) -> dict:
    role = payload.get("role")
    caller = None
    if isinstance(role, str):
        caller = ACCESS["persona_of"].get(role, role)
    rows = []
    if caller is not None:
        for grant in ACCESS["grants"]:
            if grant["role"] == caller and all(
                grant[name] == payload.get(name) for name in ACCESS_FIELDS
            ):
                rows.append(grant["row"])
    rows.sort()
    denied_list = ACCESS["denied_actions"].get(caller, []) if caller else []
    on_denied_list = payload.get("action") in denied_list
    execute_without_approval = payload.get("action") == "action.execute" and not (
        _approval_id_present(payload.get("approval_id"))
    )
    allow = bool(rows) and not on_denied_list and not execute_without_approval
    reasons = set()
    if not rows:
        reasons.add("policy.opa.default_deny")
    if on_denied_list:
        reasons.add("action_on_denied_list")
    if rows and execute_without_approval:
        reasons.add(APPROVAL_RULE)
    return {"allow": allow, "matrix_rows": rows, "reasons": sorted(reasons)}


def evaluate_access(payload: dict) -> dict:
    """Return {"allow": bool, "matrix_rows": [...], "reasons": [...]}."""
    try:
        if engine_name() == "opa":
            return _opa_eval("data.workshop.access.decision", payload)
        return _access_python(payload)
    except PolicyEngineError:
        return {"allow": False, "matrix_rows": [], "reasons": ["policy_engine_error"]}


# ---------------------------------------------------------------------------
# AI action policy. Python copy of policy/opa/ai_action.rego.
# Row ids B1 to B10, H1 to H4, O1 to O3 are the rows of the outcome table.
# ---------------------------------------------------------------------------


def _is_bool(value) -> bool:
    return value is True or value is False


def _tri_state(value) -> bool:
    return value is True or value is False or value is None


def _ai_input_valid(payload) -> bool:
    if not isinstance(payload, dict):
        return False
    if not all(key in payload for key in AI["required_keys"]):
        return False
    action = payload["action"]
    if action not in AI["ai_actions"]:
        return False
    if payload["persona"] not in AI["known_callers"]:
        return False
    if payload["resource"] not in AI["resources_for"][action]:
        return False
    if payload["risk"] != AI["risk_for"][action]:
        return False
    if payload["policy_result"] not in ("allow", "deny"):
        return False
    if not (payload["approval_id"] is None or isinstance(payload["approval_id"], str)):
        return False
    if not isinstance(payload["policy_version"], str):
        return False
    for name in (
        "approval_required",
        "audit_row_written",
        "change_plan_ok",
        "record_found",
        "forbidden_field_in_prompt",
        "timeout_hit",
    ):
        if not _is_bool(payload[name]):
            return False
    return _tri_state(payload["stale_topology_flag"]) and _tri_state(
        payload["output_schema_ok"]
    )


def _ai_action_python(payload: dict) -> dict:
    if not _ai_input_valid(payload):
        return {
            "outcome": "BLOCK",
            "reasons": ["input_invalid"],
            "policy_version": POLICY_VERSION,
        }
    block = set()
    hold = set()
    is_execute = payload["action"] == "action.execute"
    if payload["policy_result"] != "allow":  # B2
        block.add("provenance.policy_result")
    if payload["record_found"] is not True:  # B3
        block.add("failmode.missing_id")
    if payload["forbidden_field_in_prompt"] is True:  # B4
        block.add("failmode.forbidden_field_in_prompt")
        block.add("rule.forbidden_fields_never_enter_prompt")
    if payload["stale_topology_flag"] is True:  # B5
        block.add("failmode.stale_topology_true")
        block.add("rule.stale_topology_blocks_recommendation")
    if is_execute:
        if payload["persona"] != "persona.automation_service":  # B6
            block.add("rule.ai_output_cannot_execute")
        if payload["approval_required"] is not True:  # B7
            block.add(APPROVAL_RULE)
        if not _approval_id_present(payload["approval_id"]):  # B8
            block.add(APPROVAL_RULE)
        if payload["audit_row_written"] is not True:  # B9
            block.add(APPROVAL_RULE)
        if payload["change_plan_ok"] is not True:  # B10
            block.add(APPROVAL_RULE)
    if payload["timeout_hit"] is True:  # H1
        hold.add("failmode.timeout")
    if payload["output_schema_ok"] is not True:  # H2
        hold.add("failmode.schema_failure")
    if payload["stale_topology_flag"] is None:  # H3
        hold.add("failmode.stale_topology_blank")
    if payload["policy_version"] != POLICY_VERSION:  # H4
        hold.add("policy_version_differs")
    if block:
        outcome, reasons = "BLOCK", block
    elif hold:
        outcome, reasons = "HOLD_FOR_REVIEW", hold
    else:  # O1, O2, O3
        outcome = AI["outcome_for_action"][payload["action"]]
        reasons = set(AI["reasons_for_action"][payload["action"]])
    return {
        "outcome": outcome,
        "reasons": sorted(reasons),
        "policy_version": POLICY_VERSION,
    }


def evaluate_ai_action(payload: dict) -> dict:
    """Return {"outcome": one of four words, "reasons": [...], "policy_version": str}."""
    try:
        if engine_name() == "opa":
            return _opa_eval("data.workshop.ai_action.result", payload)
        return _ai_action_python(payload)
    except PolicyEngineError:
        return {
            "outcome": "BLOCK",
            "reasons": ["policy_engine_error"],
            "policy_version": POLICY_VERSION,
        }


# ---------------------------------------------------------------------------
# Helpers for the two routes
# ---------------------------------------------------------------------------

# The live header is X-User-Role. The policy input holds a YAML id.
# docs/03-identity/policy-input-model.md, "Header word to role id".
HEADER_ROLE_IDS = {
    "admin": "role.admin",
    "operator": "role.operator",
    "engineer": "role.engineer",
    "clinician": "role.clinician",
    "ai_agent": "persona.ai_agent",
}

# Purpose and scope on a live call are the values of the target row for that
# caller (docs/03-identity/negative-access-test-plan.md, assumptions). The live
# routes do not send either field. A caller with no row of its own is checked
# with the TA-01 values, so the deny comes from the role.
_RECORD_READ = {
    "role.operator": ("resource.device", "purpose.incident_triage", "scope.all_records"),
    "role.engineer": ("resource.device", "purpose.network_change_planning", "scope.all_records"),
    "persona.ai_agent": ("resource.device", "purpose.ai_assistance", "scope.assigned_incident"),
}
_RECORD_READ_DEFAULT = _RECORD_READ["role.operator"]

_SUMMARIZE = {
    "role.operator": ("resource.device", "purpose.incident_triage", "scope.assigned_incident"),
    "persona.ai_agent": ("resource.device", "purpose.ai_assistance", "scope.assigned_incident"),
    "role.engineer": ("resource.device", "purpose.network_change_planning", "scope.assigned_incident"),
}
_SUMMARIZE_DEFAULT = _SUMMARIZE["role.operator"]


def role_id_from_header(word):
    """Map the X-User-Role word to a YAML role id. A missing or blank word gives None."""
    if word is None or not str(word).strip():
        return None
    word = str(word).strip()
    return HEADER_ROLE_IDS.get(word, "role." + word)


def check_record_read(role_id) -> dict:
    """Access decision for GET /records/{id}. TA-01, TA-11, and TA-28 are the allow rows."""
    resource, purpose, scope = _RECORD_READ.get(role_id, _RECORD_READ_DEFAULT)
    return evaluate_access(
        {
            "role": role_id,
            "action": "action.read",
            "resource": resource,
            "purpose": purpose,
            "scope": scope,
            "risk": "risk.read_only",
        }
    )


def check_summarize(role_id) -> dict:
    """Access decision for POST /ai/summarize/{id}. TA-06 and TA-32 are the allow rows."""
    resource, purpose, scope = _SUMMARIZE.get(role_id, _SUMMARIZE_DEFAULT)
    return evaluate_access(
        {
            "role": role_id,
            "action": "action.summarize",
            "resource": resource,
            "purpose": purpose,
            "scope": scope,
            "risk": "risk.recommendation",
        }
    )


def stale_topology_flag_of(record: dict):
    """The CSV cell as true, false, or None for a blank or unknown word."""
    word = str(record.get("stale_topology_flag", "")).strip().lower()
    if word == "true":
        return True
    if word == "false":
        return False
    return None


# Stage S04-09. The gateway calls the policy twice. The first call is a
# pre-flight, before the model runs. No gateway check has run yet, so the three
# flags say "nothing has failed". The pre-flight decides only the rows that
# read the record and the caller: a missing id, a stale flag, a denied access.
# Its answer never leaves the gateway as a recommendation. The second call
# passes the flags the gateway measured. That answer is the outcome of the call.
PREFLIGHT_GATEWAY_FLAGS = {
    "forbidden_field_in_prompt": False,
    "output_schema_ok": True,
    "timeout_hit": False,
}


def decide_summarize(
    role_id, record_id: str, record: dict, access: dict, gateway_flags=None
) -> dict:
    """Run ai_action for one summarize call. `access` is the result of check_summarize.

    `gateway_flags` holds forbidden_field_in_prompt, output_schema_ok, and
    timeout_hit as the gateway measured them. None means a pre-flight call.
    """
    payload = {
        "persona": role_id,
        "action": "action.summarize",
        "resource": "resource.device",
        "risk": "risk.recommendation",
        "policy_result": "allow" if access.get("allow") else "deny",
        "approval_required": False,
        "approval_id": None,
        "audit_row_written": False,
        "change_plan_ok": False,
        "record_found": record.get("device_id") == record_id,
        "stale_topology_flag": stale_topology_flag_of(record),
        "policy_version": POLICY_VERSION,
    }
    payload.update(PREFLIGHT_GATEWAY_FLAGS if gateway_flags is None else gateway_flags)
    return evaluate_ai_action(payload)
