"""Tests for the S04-06 policy. Stage S04-06 Half B.

These tests run the Python copy of the policy, so they pass without the `opa`
binary. The Rego files are tested by access_test.rego and ai_action_test.rego
(run with `opa test policy/opa policy/tests`). When `opa` is on the PATH, the
last section of this file also runs both engines on the same inputs and checks
that they agree.

Fixtures are the JSON files in policy/tests/fixtures. They come from
docs/06-policy/example-inputs.md.
"""

import itertools
import json
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit, domain_service, policy

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures"
# Each file holds one object keyed by the fixture name. That lets `opa test`
# merge all the files into data.fixtures. The Rego tests read the same files.
FIXTURES = {}
for fixture_path in sorted(FIXTURE_DIR.glob("*.json")):
    loaded = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert list(loaded) == [fixture_path.stem]
    FIXTURES.update(loaded)
ACCESS_FIXTURES = {k: v for k, v in FIXTURES.items() if v["area"] == "access"}
AI_FIXTURES = {k: v for k, v in FIXTURES.items() if v["area"] == "ai_action"}
NOT_EVALUATED = {
    k: v
    for k, v in FIXTURES.items()
    if v["area"] in ("data_use", "operational_safety", "production_readiness")
}

client = TestClient(app)

EXECUTE_ALL_CHECKS = FIXTURES["ai-01-execute-with-all-checks"]["input"]
SUMMARIZE_OK = FIXTURES["ai-03-recommend-only-summary"]["input"]


def with_changes(base, **changes):
    result = dict(base)
    result.update(changes)
    return result


@pytest.fixture(autouse=True)
def python_engine(monkeypatch):
    """Run the Python copy unless a test says otherwise."""
    monkeypatch.setenv("POLICY_ENGINE", "python")


@pytest.fixture
def audit_log(tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "LOG", tmp_path / "audit.log")

    def rows():
        path = tmp_path / "audit.log"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text().splitlines()]

    return rows


# ---------------------------------------------------------------------------
# Fixture counts
# ---------------------------------------------------------------------------


def test_fixture_counts():
    assert len(FIXTURES) == 23
    assert len(ACCESS_FIXTURES) == 5
    assert len(AI_FIXTURES) == 10
    assert len(NOT_EVALUATED) == 8


# ---------------------------------------------------------------------------
# Access policy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(ACCESS_FIXTURES))
def test_access_fixture(name):
    fixture = ACCESS_FIXTURES[name]
    result = policy.evaluate_access(fixture["input"])
    assert ("allow" if result["allow"] else "deny") == fixture["expected"]["decision"]
    expected_row = fixture["expected"]["matrix_row"]
    assert result["matrix_rows"] == ([expected_row] if expected_row else [])


def test_admin_has_no_blanket_access():
    """policy.opa.admin_any is gone. role.admin matches no row."""
    base = ACCESS_FIXTURES["ac-01-allow-noc-operator-reads-device"]["input"]
    for action in ("action.read", "action.summarize", "action.recommend", "action.execute"):
        result = policy.evaluate_access(with_changes(base, role="role.admin", action=action))
        assert result["allow"] is False
        assert result["matrix_rows"] == []


def test_every_matrix_row_is_allowed_with_its_own_fields():
    """Each of the 34 rows allows the exact call it describes. TA-24 and TA-25 need an approval id."""
    assert len(policy.ACCESS["grants"]) == 34
    for grant in policy.ACCESS["grants"]:
        payload = {name: grant[name] for name in ("role", "action", "resource", "purpose", "scope", "risk")}
        payload["approval_id"] = "APR-EXAMPLE-0001"
        result = policy.evaluate_access(payload)
        assert result["allow"] is True, grant["row"]
        assert grant["row"] in result["matrix_rows"]


def test_changing_any_one_field_of_a_row_denies():
    """A row is an exact match on six fields. One changed value gives deny."""
    for grant in policy.ACCESS["grants"]:
        payload = {name: grant[name] for name in ("role", "action", "resource", "purpose", "scope", "risk")}
        payload["approval_id"] = "APR-EXAMPLE-0001"
        for name in ("role", "action", "resource", "purpose", "scope", "risk"):
            changed = with_changes(payload, **{name: "value.not_in_any_row"})
            assert policy.evaluate_access(changed)["allow"] is False, (grant["row"], name)


@pytest.mark.parametrize("approval_id", [None, "", "   "])
def test_execute_rows_need_an_approval_id(approval_id):
    for row in ("TA-24", "TA-25"):
        grant = next(g for g in policy.ACCESS["grants"] if g["row"] == row)
        payload = {name: grant[name] for name in ("role", "action", "resource", "purpose", "scope", "risk")}
        payload["approval_id"] = approval_id
        result = policy.evaluate_access(payload)
        assert result["allow"] is False
        assert result["matrix_rows"] == [row]
    payload.pop("approval_id")
    assert policy.evaluate_access(payload)["allow"] is False


def test_missing_role_is_denied():
    base = ACCESS_FIXTURES["ac-01-allow-noc-operator-reads-device"]["input"]
    payload = {k: v for k, v in base.items() if k != "role"}
    assert policy.evaluate_access(payload)["allow"] is False
    assert policy.evaluate_access(with_changes(base, role=None))["allow"] is False


def test_live_role_ids_stand_for_their_persona():
    base = ACCESS_FIXTURES["ac-01-allow-noc-operator-reads-device"]["input"]
    assert policy.evaluate_access(with_changes(base, role="role.operator"))["allow"] is True
    assert policy.evaluate_access(with_changes(base, role="role.clinician"))["allow"] is False


# ---------------------------------------------------------------------------
# AI action policy: the four outcomes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", sorted(AI_FIXTURES))
def test_ai_action_fixture(name):
    fixture = AI_FIXTURES[name]
    result = policy.evaluate_ai_action(fixture["input"])
    assert result["outcome"] == fixture["expected"]["outcome"]
    assert result["reasons"] == sorted(fixture["expected"]["reasons"])
    assert result["policy_version"] == policy.POLICY_VERSION


@pytest.mark.parametrize("name", sorted(NOT_EVALUATED))
def test_other_areas_are_recorded_but_not_evaluated(name):
    """Half B builds access and ai_action only. These fixtures stay as data for S05R and later."""
    fixture = NOT_EVALUATED[name]
    assert set(fixture) == {"name", "area", "input", "expected"}
    assert fixture["expected"]["decision"] in ("allow", "deny")


def test_summarize_is_recommend_only():
    assert policy.evaluate_ai_action(SUMMARIZE_OK)["outcome"] == "RECOMMEND_ONLY"


def test_recommend_is_held_for_review():
    payload = with_changes(SUMMARIZE_OK, action="action.recommend")
    assert policy.evaluate_ai_action(payload)["outcome"] == "HOLD_FOR_REVIEW"


# ---------------------------------------------------------------------------
# Gate test: an AI remediation recommendation becomes a change
# ---------------------------------------------------------------------------


def test_remediation_becomes_a_change_with_all_checks_allow():
    """PASS gate, allow case. Every check is present, so the outcome is EXECUTE."""
    result = policy.evaluate_ai_action(EXECUTE_ALL_CHECKS)
    assert result["outcome"] == "EXECUTE"
    assert result["reasons"] == ["ai_use.remediation_execution"]
    assert EXECUTE_ALL_CHECKS["approval_id"] == "APR-EXAMPLE-0001"


def test_remediation_does_not_become_a_change_without_approval_id_deny():
    """PASS gate, deny case. No approval id, so the outcome is BLOCK."""
    fixture = AI_FIXTURES["ai-02-block-execute-without-approval-id"]
    result = policy.evaluate_ai_action(fixture["input"])
    assert result["outcome"] == "BLOCK"
    assert "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" in result["reasons"]


@pytest.mark.parametrize("approval_id", [None, "", " ", "\t\n", 0, False, [], {}])
def test_execute_is_unreachable_without_an_approval_id(approval_id):
    payload = with_changes(EXECUTE_ALL_CHECKS, approval_id=approval_id)
    assert policy.evaluate_ai_action(payload)["outcome"] != "EXECUTE"


def test_execute_is_unreachable_when_the_approval_id_key_is_missing():
    payload = {k: v for k, v in EXECUTE_ALL_CHECKS.items() if k != "approval_id"}
    result = policy.evaluate_ai_action(payload)
    assert result["outcome"] == "BLOCK"
    assert result["reasons"] == ["input_invalid"]


def test_each_missing_key_blocks():
    for key in policy.AI["required_keys"]:
        payload = {k: v for k, v in EXECUTE_ALL_CHECKS.items() if k != key}
        result = policy.evaluate_ai_action(payload)
        assert result["outcome"] == "BLOCK", key
        assert result["reasons"] == ["input_invalid"], key


@pytest.mark.parametrize(
    "changes",
    [
        {"action": "action.approve"},
        {"action": "action.delete"},
        {"persona": "persona.unknown"},
        {"resource": "resource.incident"},
        {"risk": "risk.read_only"},
        {"policy_result": "maybe"},
        {"policy_version": 1},
        {"approval_required": "true"},
        {"audit_row_written": 1},
        {"stale_topology_flag": "false"},
        {"output_schema_ok": 0},
    ],
)
def test_invalid_values_block(changes):
    result = policy.evaluate_ai_action(with_changes(EXECUTE_ALL_CHECKS, **changes))
    assert result["outcome"] == "BLOCK"
    assert result["reasons"] == ["input_invalid"]


def test_input_that_is_not_an_object_blocks():
    for payload in (None, [], "EXECUTE", 5):
        assert policy.evaluate_ai_action(payload)["outcome"] == "BLOCK"


def test_one_missing_check_stops_execute_each_time():
    for name, bad in (
        ("policy_result", "deny"),
        ("approval_required", False),
        ("approval_id", None),
        ("audit_row_written", False),
        ("change_plan_ok", False),
        ("record_found", False),
        ("forbidden_field_in_prompt", True),
        ("stale_topology_flag", True),
        ("persona", "persona.ai_agent"),
    ):
        result = policy.evaluate_ai_action(with_changes(EXECUTE_ALL_CHECKS, **{name: bad}))
        assert result["outcome"] == "BLOCK", name


def test_hold_rows():
    for name, value in (
        ("timeout_hit", True),
        ("output_schema_ok", False),
        ("output_schema_ok", None),
        ("stale_topology_flag", None),
        ("policy_version", "0.0.9"),
    ):
        result = policy.evaluate_ai_action(with_changes(EXECUTE_ALL_CHECKS, **{name: value}))
        assert result["outcome"] == "HOLD_FOR_REVIEW", (name, value)


def test_block_wins_over_hold():
    payload = with_changes(EXECUTE_ALL_CHECKS, timeout_hit=True, audit_row_written=False)
    result = policy.evaluate_ai_action(payload)
    assert result["outcome"] == "BLOCK"
    assert "failmode.timeout" not in result["reasons"]


def test_the_model_cannot_set_its_own_outcome():
    payload = with_changes(SUMMARIZE_OK, outcome="EXECUTE")
    assert policy.evaluate_ai_action(payload)["outcome"] == "RECOMMEND_ONLY"


# ---------------------------------------------------------------------------
# Gate test: every combination of the two small lists and the flags
# ---------------------------------------------------------------------------


def all_combinations():
    pairs = [
        ("action.summarize", "resource.device"),
        ("action.recommend", "resource.incident"),
        ("action.execute", "resource.device"),
        ("action.execute", "resource.circuit"),
    ]
    personas = ["persona.automation_service", "persona.ai_agent", "persona.noc_operator"]
    approval_ids = [None, "", "APR-EXAMPLE-0001"]
    flags = [False, True]
    stale = [False, True, None]
    schema = [True, False, None]
    versions = [policy.POLICY_VERSION, "0.0.9"]
    for persona, (action, resource), policy_result, required, approval_id in itertools.product(
        personas, pairs, ["allow", "deny"], flags, approval_ids
    ):
        risk = policy.AI["risk_for"][action]
        for audit_row, change_plan, found, forbidden, stale_flag, ok, timeout, version in itertools.product(
            flags, flags, flags, flags, stale, schema, flags, versions
        ):
            yield {
                "persona": persona,
                "action": action,
                "resource": resource,
                "risk": risk,
                "policy_result": policy_result,
                "approval_required": required,
                "approval_id": approval_id,
                "audit_row_written": audit_row,
                "change_plan_ok": change_plan,
                "record_found": found,
                "forbidden_field_in_prompt": forbidden,
                "stale_topology_flag": stale_flag,
                "output_schema_ok": ok,
                "timeout_hit": timeout,
                "policy_version": version,
            }


def test_execute_is_reached_by_exactly_the_all_checks_inputs():
    """BLOCKED gate. No input reaches EXECUTE without an approval id."""
    total = 0
    executes = []
    for payload in all_combinations():
        total += 1
        result = policy.evaluate_ai_action(payload)
        assert result["outcome"] in {"RECOMMEND_ONLY", "HOLD_FOR_REVIEW", "BLOCK", "EXECUTE"}
        if result["outcome"] == "EXECUTE":
            executes.append(payload)
    assert total == 3 * 4 * 2 * 2 * 3 * 2**4 * 3 * 3 * 2 * 2
    assert len(executes) == 2  # resource.device and resource.circuit
    for payload in executes:
        assert payload["approval_id"] == "APR-EXAMPLE-0001"
        assert payload["persona"] == "persona.automation_service"
        assert payload["action"] == "action.execute"
        assert payload["policy_result"] == "allow"
        assert payload["approval_required"] is True
        assert payload["audit_row_written"] is True
        assert payload["change_plan_ok"] is True
        assert payload["record_found"] is True
        assert payload["forbidden_field_in_prompt"] is False
        assert payload["stale_topology_flag"] is False
        assert payload["output_schema_ok"] is True
        assert payload["timeout_hit"] is False
        assert payload["policy_version"] == policy.POLICY_VERSION


# ---------------------------------------------------------------------------
# Engine behaviour
# ---------------------------------------------------------------------------


def test_engine_failure_denies(monkeypatch):
    """If opa is chosen but cannot run, the answer is deny and BLOCK."""
    monkeypatch.setenv("POLICY_ENGINE", "opa")
    monkeypatch.setenv("PATH", "")
    access = policy.evaluate_access(ACCESS_FIXTURES["ac-01-allow-noc-operator-reads-device"]["input"])
    assert access["allow"] is False
    assert access["reasons"] == ["policy_engine_error"]
    ai = policy.evaluate_ai_action(EXECUTE_ALL_CHECKS)
    assert ai["outcome"] == "BLOCK"
    assert ai["reasons"] == ["policy_engine_error"]


def test_engine_name_follows_the_setting(monkeypatch):
    monkeypatch.setenv("POLICY_ENGINE", "python")
    assert policy.engine_name() == "python"
    monkeypatch.setenv("POLICY_ENGINE", "opa")
    assert policy.engine_name() == "opa"
    monkeypatch.setenv("POLICY_ENGINE", "auto")
    assert policy.engine_name() == ("opa" if shutil.which("opa") else "python")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


def test_record_route_allows_operator_and_writes_read_row(audit_log):
    response = client.get("/records/REC-0001", headers={"X-User-Role": "operator"})
    assert response.status_code == 200
    assert [row["action"] for row in audit_log()] == ["record.read"]


@pytest.mark.parametrize("role", ["clinician", "admin", "automation_service", "vendor"])
def test_record_route_denies_with_403_and_audit_row(role, audit_log):
    response = client.get("/records/REC-0001", headers={"X-User-Role": role})
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["role"] == role
    assert rows[0]["resource"] == "resource.device"
    assert rows[0]["correlation_id"]
    assert rows[0]["outcome"] is None


def test_record_route_keeps_missing_header_default_operator(audit_log):
    """Still open for S04-03. PB-04 proposes refusing a missing header."""
    assert client.get("/records/REC-0001").status_code == 200


@pytest.mark.parametrize("role", ["operator", "ai_agent"])
def test_summarize_route_allows_roles_with_a_row(role, audit_log):
    response = client.post("/ai/summarize/REC-0001", headers={"X-User-Role": role})
    assert response.status_code == 200
    assert "summary" in response.json()
    rows = audit_log()
    assert [row["action"] for row in rows] == ["ai.summary"]
    assert rows[0]["outcome"] == "RECOMMEND_ONLY"
    assert rows[0]["role"] == role


@pytest.mark.parametrize("role", [None, "admin", "clinician", "vendor"])
def test_summarize_route_denies_roles_without_a_row(role, audit_log):
    headers = {"X-User-Role": role} if role else {}
    response = client.post("/ai/summarize/REC-0001", headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["role"] == role
    assert rows[0]["outcome"] is None


def test_summarize_route_blocks_a_device_with_a_stale_flag(audit_log):
    assert domain_service.load_record("DEV-00003")["stale_topology_flag"] == "true"
    response = client.post("/ai/summarize/DEV-00003", headers={"X-User-Role": "operator"})
    assert response.status_code == 403
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["outcome"] == "BLOCK"


def test_summarize_route_blocks_an_id_that_does_not_exist(audit_log):
    response = client.post("/ai/summarize/DOES-NOT-EXIST", headers={"X-User-Role": "operator"})
    assert response.status_code == 403
    assert audit_log()[0]["action"] == "policy.deny"
    assert audit_log()[0]["outcome"] == "BLOCK"


def test_summarize_route_holds_a_device_with_a_blank_stale_flag(audit_log):
    assert domain_service.load_record("DEV-BAD1")["stale_topology_flag"] == ""
    response = client.post("/ai/summarize/DEV-BAD1", headers={"X-User-Role": "operator"})
    assert response.status_code == 202
    assert response.json()["outcome"] == "HOLD_FOR_REVIEW"
    assert response.json()["reasons"] == ["failmode.stale_topology_blank"]
    assert [row["action"] for row in audit_log()] == ["policy.hold"]


def test_no_route_can_execute():
    paths = [getattr(route, "path", "") for route in app.routes]
    assert all("execute" not in path for path in paths)


# ---------------------------------------------------------------------------
# Agreement between the two engines. Runs only when `opa` is on the PATH.
# ---------------------------------------------------------------------------

needs_opa = pytest.mark.skipif(shutil.which("opa") is None, reason="opa binary not on PATH")


def access_inputs():
    """Every matrix row, plus each row with one field changed, plus the denied list."""
    fields = ("role", "action", "resource", "purpose", "scope", "risk")
    for grant in policy.ACCESS["grants"]:
        base = {name: grant[name] for name in fields}
        for approval_id in ("APR-EXAMPLE-0001", None, "  "):
            yield with_changes(base, approval_id=approval_id)
        for name in fields:
            yield with_changes(base, **{name: "value.not_in_any_row"})
    for fixture in ACCESS_FIXTURES.values():
        yield fixture["input"]
    for live_role in ("role.operator", "role.engineer", "role.ai_agent", "role.admin", "role.clinician"):
        yield {
            "role": live_role,
            "action": "action.read",
            "resource": "resource.device",
            "purpose": "purpose.incident_triage",
            "scope": "scope.all_records",
            "risk": "risk.read_only",
        }
    yield {"action": "action.read"}


def run_opa_on_list(query, payloads):
    """One opa call for many inputs. The query reads the list from `input`."""
    import subprocess

    proc = subprocess.run(
        [
            shutil.which("opa"),
            "eval",
            "--format", "json",
            "--data", str(policy.POLICY_DIR),
            "--stdin-input",
            query,
        ],
        input=json.dumps(payloads),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)["result"][0]["expressions"][0]["value"]


@needs_opa
def test_opa_and_python_agree_on_access():
    payloads = list(access_inputs())
    query = "[r | some c in input; r := data.workshop.access.decision with input as c]"
    opa_results = run_opa_on_list(query, payloads)
    assert len(opa_results) == len(payloads)
    for payload, opa_result in zip(payloads, opa_results):
        assert opa_result == policy._access_python(payload), payload


@needs_opa
def test_opa_and_python_agree_on_every_ai_action_combination():
    payloads = list(all_combinations()) + [
        {k: v for k, v in EXECUTE_ALL_CHECKS.items() if k != key} for key in policy.AI["required_keys"]
    ]
    query = "[r | some c in input; r := data.workshop.ai_action.result with input as c]"
    opa_results = run_opa_on_list(query, payloads)
    assert len(opa_results) == len(payloads)
    for payload, opa_result in zip(payloads, opa_results):
        assert opa_result == policy._ai_action_python(payload), payload
