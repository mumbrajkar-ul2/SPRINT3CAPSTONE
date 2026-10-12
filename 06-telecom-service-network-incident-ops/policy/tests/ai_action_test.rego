# Tests for policy/opa/ai_action.rego. Stage S04-06 Half B.
# Run: opa test policy/opa policy/tests
# The fixtures in policy/tests/fixtures are loaded as data.fixtures.

package workshop.ai_action_test

import rego.v1

# The input where every check is present. It is the fixture ai-01.
all_checks := {
	"persona": "persona.automation_service",
	"action": "action.execute",
	"resource": "resource.device",
	"risk": "risk.live_network_change",
	"policy_result": "allow",
	"approval_required": true,
	"approval_id": "APR-EXAMPLE-0001",
	"audit_row_written": true,
	"change_plan_ok": true,
	"record_found": true,
	"forbidden_field_in_prompt": false,
	"stale_topology_flag": false,
	"output_schema_ok": true,
	"timeout_hit": false,
	"policy_version": "0.1.0-proposed",
}

# PASS gate, allow case: every check is present, so the outcome is EXECUTE.
test_remediation_becomes_a_change_with_all_checks if {
	r := data.workshop.ai_action.result with input as all_checks
	r.outcome == "EXECUTE"
	r.reasons == ["ai_use.remediation_execution"]
}

# PASS gate, deny case: no approval id, so the outcome is BLOCK.
test_remediation_blocked_without_approval_id if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"approval_id": null})
	r.outcome == "BLOCK"
}

# EXECUTE is unreachable without an approval id, whatever the value is.
test_execute_unreachable_with_empty_approval_ids if {
	every empty in [null, "", " ", "\t", 0, false, [], {}] {
		r := data.workshop.ai_action.result with input as object.union(all_checks, {"approval_id": empty})
		r.outcome != "EXECUTE"
	}
}

test_execute_unreachable_when_approval_id_key_is_missing if {
	r := data.workshop.ai_action.result with input as object.remove(all_checks, ["approval_id"])
	r.outcome == "BLOCK"
	r.reasons == ["input_invalid"]
}

test_each_missing_key_blocks if {
	every key in data.ai_action_tables.required_keys {
		r := data.workshop.ai_action.result with input as object.remove(all_checks, [key])
		r.outcome == "BLOCK"
		r.reasons == ["input_invalid"]
	}
}

test_ai_agent_cannot_execute if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"persona": "persona.ai_agent"})
	r.outcome == "BLOCK"
	"rule.ai_output_cannot_execute" in r.reasons
}

test_audit_row_must_come_first if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"audit_row_written": false})
	r.outcome == "BLOCK"
}

test_change_plan_must_be_ok if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"change_plan_ok": false})
	r.outcome == "BLOCK"
}

test_approval_must_be_required if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"approval_required": false})
	r.outcome == "BLOCK"
}

test_stale_true_blocks if {
	r := data.workshop.ai_action.result with input as object.union(all_checks, {"stale_topology_flag": true})
	r.outcome == "BLOCK"
}

test_hold_rows if {
	every change in [
		{"timeout_hit": true},
		{"output_schema_ok": false},
		{"output_schema_ok": null},
		{"stale_topology_flag": null},
		{"policy_version": "0.0.9"},
	] {
		r := data.workshop.ai_action.result with input as object.union(all_checks, change)
		r.outcome == "HOLD_FOR_REVIEW"
	}
}

test_block_wins_over_hold if {
	changed := object.union(all_checks, {"timeout_hit": true, "audit_row_written": false})
	r := data.workshop.ai_action.result with input as changed
	r.outcome == "BLOCK"
	not "failmode.timeout" in r.reasons
}

test_summarize_is_recommend_only if {
	changed := object.union(all_checks, {
		"action": "action.summarize",
		"risk": "risk.recommendation",
	})
	r := data.workshop.ai_action.result with input as changed
	r.outcome == "RECOMMEND_ONLY"
}

test_recommend_is_held_for_review if {
	changed := object.union(all_checks, {
		"action": "action.recommend",
		"resource": "resource.incident",
		"risk": "risk.recommendation",
	})
	r := data.workshop.ai_action.result with input as changed
	r.outcome == "HOLD_FOR_REVIEW"
}

test_the_model_cannot_set_its_own_outcome if {
	changed := object.union(all_checks, {
		"action": "action.summarize",
		"risk": "risk.recommendation",
		"outcome": "EXECUTE",
	})
	r := data.workshop.ai_action.result with input as changed
	r.outcome == "RECOMMEND_ONLY"
}

# Every ai_action fixture gives the expected outcome and reasons.
ai_fixture_failures contains name if {
	some name, fixture in data.fixtures
	fixture.area == "ai_action"
	r := data.workshop.ai_action.result with input as fixture.input
	not r.outcome == fixture.expected.outcome
}

ai_fixture_failures contains name if {
	some name, fixture in data.fixtures
	fixture.area == "ai_action"
	r := data.workshop.ai_action.result with input as fixture.input
	not r.reasons == sort(fixture.expected.reasons)
}

test_ai_fixtures_were_loaded if {
	count({name | some name, fixture in data.fixtures; fixture.area == "ai_action"}) == 10
}

test_ai_fixtures_give_expected_results if {
	count(ai_fixture_failures) == 0
}
