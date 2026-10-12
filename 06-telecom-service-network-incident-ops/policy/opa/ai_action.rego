# AI action policy. Stage S04-06 Half B.
#
# It looks at one AI call and returns one of four outcomes:
# RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE.
# The design is docs/06-policy/ai-action-policy-design.md. Row ids B1 to B10,
# H1 to H4, and O1 to O3 below are the row ids in that file's outcome table.
#
# How the rows combine:
#   If any BLOCK row matches, the outcome is BLOCK.
#   Otherwise, if any HOLD row matches, the outcome is HOLD_FOR_REVIEW.
#   Otherwise the action decides: summarize, recommend, or execute.
#
# No row compares a number. The timeout is a true or false flag from the gateway.
# The value lists are in policy_data.json, the same file Python reads.

package workshop.ai_action

import rego.v1

# PROPOSED. Owner: Team-Force. The repo sets no policy version format.
# Open question for S03: policy_version has no id and no value format.
policy_version := data.ai_action_tables.policy_version

# If nothing below gives an answer, refuse.
default outcome := "BLOCK"

default reasons := ["input_invalid"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

is_execute if input.action == "action.execute"

# provenance.approval_id. An empty string, spaces, null, or a missing key count as empty.
approval_id_present if {
	is_string(input.approval_id)
	trim_space(input.approval_id) != ""
}

null_or_string(value) if value == null

null_or_string(value) if is_string(value)

# Every row below except B1 needs a valid input, so an invalid input reports
# input_invalid and nothing else.
#
# A key that is missing makes the whole input invalid.
# A key set to null is valid only for approval_id, stale_topology_flag,
# and output_schema_ok.
input_valid if {
	every key in data.ai_action_tables.required_keys {
		key in object.keys(input)
	}
	input.action in data.ai_action_tables.ai_actions
	input.persona in data.ai_action_tables.known_callers
	input.resource in data.ai_action_tables.resources_for[input.action]
	input.risk == data.ai_action_tables.risk_for[input.action]
	input.policy_result in {"allow", "deny"}
	is_boolean(input.approval_required)
	null_or_string(input.approval_id)
	is_boolean(input.audit_row_written)
	is_boolean(input.change_plan_ok)
	is_boolean(input.record_found)
	is_boolean(input.forbidden_field_in_prompt)
	input.stale_topology_flag in {true, false, null}
	input.output_schema_ok in {true, false, null}
	is_boolean(input.timeout_hit)
	is_string(input.policy_version)
}

# ---------------------------------------------------------------------------
# BLOCK rows
# ---------------------------------------------------------------------------

# B1. The action, persona, resource, or risk is not one the YAML lists, or the
# resource or risk does not fit the action, or a required key is missing.
# Open question for S03: no failmode id exists for an invalid input.
block_reasons contains "input_invalid" if not input_valid

# B2. The access policy did not allow this caller to take this action.
# provenance.policy_result
block_reasons contains "provenance.policy_result" if {
	input_valid
	not input.policy_result == "allow"
}

# B3. No row has the requested id.
# failmode.missing_id
block_reasons contains "failmode.missing_id" if {
	input_valid
	not input.record_found == true
}

# B4. The prompt builder found a forbidden field.
# failmode.forbidden_field_in_prompt, rule.forbidden_fields_never_enter_prompt
block_reasons contains "failmode.forbidden_field_in_prompt" if {
	input_valid
	input.forbidden_field_in_prompt == true
}

block_reasons contains "rule.forbidden_fields_never_enter_prompt" if {
	input_valid
	input.forbidden_field_in_prompt == true
}

# B5. The stale topology flag is true. The YAML names this for recommend.
# PROPOSED for summarize and execute. Owner: Team-Force.
# failmode.stale_topology_true, rule.stale_topology_blocks_recommendation
block_reasons contains "failmode.stale_topology_true" if {
	input_valid
	input.stale_topology_flag == true
}

block_reasons contains "rule.stale_topology_blocks_recommendation" if {
	input_valid
	input.stale_topology_flag == true
}

# B6. Only persona.automation_service may execute (ai_use.remediation_execution).
# The model never holds the execute action.
# rule.ai_output_cannot_execute
block_reasons contains "rule.ai_output_cannot_execute" if {
	input_valid
	is_execute
	input.persona != "persona.automation_service"
}

# B7. An execute call must say approval is required. Operating contract row 9:
# every live network change needs an approval id. PROPOSED mechanism.
# rule.ai_recommendation_needs_policy_approval_audit_before_state_change
block_reasons contains "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" if {
	input_valid
	is_execute
	not input.approval_required == true
}

# B8. An execute call needs a stored approval id. Only a named person writes it.
# rule.ai_recommendation_needs_policy_approval_audit_before_state_change
block_reasons contains "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" if {
	input_valid
	is_execute
	not approval_id_present
}

# B9. An execute call needs an audit row written first.
# rule.ai_recommendation_needs_policy_approval_audit_before_state_change
block_reasons contains "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" if {
	input_valid
	is_execute
	not input.audit_row_written == true
}

# B10. An execute call needs a change that is reversible and validated.
# rule.ai_recommendation_needs_policy_approval_audit_before_state_change
# Open question for S03: change_plan_ok has no id and "validated" has no meaning in the YAML.
block_reasons contains "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" if {
	input_valid
	is_execute
	not input.change_plan_ok == true
}

# ---------------------------------------------------------------------------
# HOLD rows
# ---------------------------------------------------------------------------

# H1. The model did not answer in time.
# failmode.timeout
hold_reasons contains "failmode.timeout" if {
	input_valid
	input.timeout_hit == true
}

# H2. The answer did not match the output schema, or there is no answer.
# failmode.schema_failure
hold_reasons contains "failmode.schema_failure" if {
	input_valid
	input.output_schema_ok != true
}

# H3. The stale topology flag is blank. What a blank flag should do is Unknown.
# The YAML marks this treatment PROPOSED. Owner: Team-Force.
# failmode.stale_topology_blank
hold_reasons contains "failmode.stale_topology_blank" if {
	input_valid
	input.stale_topology_flag == null
}

# H4. The caller used a policy version this policy does not hold.
# PROPOSED. Owner: Team-Force.
# Open question for S03: no id exists for a policy version mismatch.
hold_reasons contains "policy_version_differs" if {
	input_valid
	input.policy_version != policy_version
}

# ---------------------------------------------------------------------------
# Rows O1 to O3 and the answer
# ---------------------------------------------------------------------------

outcome := "BLOCK" if count(block_reasons) > 0

outcome := "HOLD_FOR_REVIEW" if {
	count(block_reasons) == 0
	count(hold_reasons) > 0
}

# O1 summarize: RECOMMEND_ONLY (ai_use.incident_summary)
# O2 recommend: HOLD_FOR_REVIEW (ai_use.next_action_recommendation, ai_use.configuration_suggestion)
# O3 execute: EXECUTE (ai_use.remediation_execution)
# EXECUTE is reached only when no BLOCK row and no HOLD row matched. That means
# an approval id is present and an audit row was written first.
outcome := data.ai_action_tables.outcome_for_action[input.action] if {
	count(block_reasons) == 0
	count(hold_reasons) == 0
}

# The reasons come from the group that decided the outcome.
# If a BLOCK row matched, only the BLOCK rows are listed. If only HOLD rows
# matched, only the HOLD rows are listed. If no row matched, the reason is the
# YAML id of the action (ai_use.incident_summary and so on).
reasons := sort(block_reasons) if count(block_reasons) > 0

reasons := sort(hold_reasons) if {
	count(block_reasons) == 0
	count(hold_reasons) > 0
}

reasons := sort(data.ai_action_tables.reasons_for_action[input.action]) if {
	count(block_reasons) == 0
	count(hold_reasons) == 0
}

# The model's own "outcome" word is never read here.
# policy.output_schema says EXECUTE is never set by the model.
result := {
	"outcome": outcome,
	"reasons": reasons,
	"policy_version": policy_version,
}
