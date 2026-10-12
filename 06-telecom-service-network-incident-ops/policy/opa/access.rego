# Access policy. Stage S04-06 Half B.
#
# This file replaces the two brownfield rules (any admin; operator plus read).
# It answers one question: may this caller take this action on this resource,
# for this purpose, over this scope, at this risk? The answer is allow or deny.
#
# The input is the JSON object in docs/03-identity/policy-input-model.md.
# The allow rows TA-01 to TA-35 live in policy_data.json, in the same folder.
# TA-01 to TA-34 are copied from docs/03-identity/target-access-matrix.md.
# TA-35 (role.admin reads resource.audit_log) comes from docs/14-audit/audit-read-access-design.md.
# Python reads the same JSON file, so the two engines cannot disagree on a row.
#
# Every grant is PROPOSED. Owner: Team-Force (operating-contract.md row 10).

package workshop.access

import rego.v1

# policy.opa.default_deny (kept from the old file)
# Nothing is allowed unless a rule below says so.
default allow := false

# ---------------------------------------------------------------------------
# Who is calling
# ---------------------------------------------------------------------------

# access-semantics.yaml api_roles_today, mapping_label Inference.
# Three live API role ids stand for a persona. The rows are written for the
# persona, so the caller is swapped for its persona before matching.
# role.admin and role.clinician stay as they are. They have no persona, so
# they match no row.
caller := data.access_matrix.persona_of[input.role] if data.access_matrix.persona_of[input.role]

caller := input.role if not data.access_matrix.persona_of[input.role]

# rule.no_default_role
# This file never fills in a role. A call with no role has no caller, matches
# no row, and is denied. The API decides what to send when a header is absent.

# ---------------------------------------------------------------------------
# Which rows match
# ---------------------------------------------------------------------------

# rule.shared_admin_not_least_privilege
# A row matches only when role, action, resource, purpose, scope, and risk all
# equal the input. The only row for role.admin is TA-35 (read the audit log).
# An admin matches no other row.
# The old rule policy.opa.admin_any is gone.
matched_rows contains grant.row if {
	some grant in data.access_matrix.grants
	grant.role == caller
	grant.action == input.action
	grant.resource == input.resource
	grant.purpose == input.purpose
	grant.scope == input.scope
	grant.risk == input.risk
}

# ---------------------------------------------------------------------------
# Extra stops on top of a matching row
# ---------------------------------------------------------------------------

# rule.ai_output_cannot_execute (for persona.ai_agent) and the denied list of
# every other persona in access-semantics.yaml.
# A matching row is still refused when its action is on the caller's denied list.
action_on_denied_list if input.action in data.access_matrix.denied_actions[caller]

# rule.ai_recommendation_needs_policy_approval_audit_before_state_change
# Rows TA-24 and TA-25 are execute rows. They need a stored approval id.
# An empty string, a string of spaces, null, or a missing key all count as empty.
approval_id_present if {
	is_string(input.approval_id)
	trim_space(input.approval_id) != ""
}

execute_without_approval_id if {
	input.action == "action.execute"
	not approval_id_present
}

# ---------------------------------------------------------------------------
# The decision
# ---------------------------------------------------------------------------

# policy.opa.operator_read and policy.opa.admin_any are replaced by the rows.
allow if {
	count(matched_rows) > 0
	not action_on_denied_list
	not execute_without_approval_id
}

# Why a call was refused. Ids are YAML ids where the YAML has one.
# Open question for S03: "action_on_denied_list" has no YAML id.
reasons contains "policy.opa.default_deny" if count(matched_rows) == 0

reasons contains "action_on_denied_list" if action_on_denied_list

reasons contains "rule.ai_recommendation_needs_policy_approval_audit_before_state_change" if {
	count(matched_rows) > 0
	execute_without_approval_id
}

# The object the API reads. rule.denied_access_is_audited is kept by the API:
# it writes an audit row for every refusal. This file only answers.
decision := {
	"allow": allow,
	"matrix_rows": sort(matched_rows),
	"reasons": sort(reasons),
}
