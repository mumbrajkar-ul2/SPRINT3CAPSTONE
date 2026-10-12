# Tests for policy/opa/access.rego. Stage S04-06 Half B.
# Run: opa test policy/opa policy/tests
# The fixtures in policy/tests/fixtures are loaded as data.fixtures.

package workshop.access_test

import rego.v1

noc_read := {
	"role": "persona.noc_operator",
	"action": "action.read",
	"resource": "resource.device",
	"purpose": "purpose.incident_triage",
	"scope": "scope.all_records",
	"risk": "risk.read_only",
}

automation_execute := {
	"role": "persona.automation_service",
	"action": "action.execute",
	"resource": "resource.device",
	"purpose": "purpose.scheduled_automation",
	"scope": "scope.assigned_incident",
	"risk": "risk.live_network_change",
	"approval_id": "APR-EXAMPLE-0001",
}

# TA-01
test_noc_operator_may_read_a_device if {
	data.workshop.access.allow with input as noc_read
	data.workshop.access.decision.matrix_rows == ["TA-01"] with input as noc_read
}

# The live header word operator is role.operator. It stands for persona.noc_operator.
test_live_operator_role_may_read_a_device if {
	data.workshop.access.allow with input as object.union(noc_read, {"role": "role.operator"})
}

# policy.opa.admin_any is gone.
test_admin_is_denied if {
	not data.workshop.access.allow with input as object.union(noc_read, {"role": "role.admin"})
}

test_clinician_is_denied if {
	not data.workshop.access.allow with input as object.union(noc_read, {"role": "role.clinician"})
}

test_missing_role_is_denied if {
	not data.workshop.access.allow with input as object.remove(noc_read, ["role"])
}

test_one_changed_field_is_denied if {
	every name in ["role", "action", "resource", "purpose", "scope", "risk"] {
		not data.workshop.access.allow with input as object.union(noc_read, {name: "value.not_in_any_row"})
	}
}

# TA-24
test_automation_may_execute_with_an_approval_id if {
	data.workshop.access.allow with input as automation_execute
}

test_automation_may_not_execute_without_an_approval_id if {
	every empty in [null, "", "  "] {
		not data.workshop.access.allow with input as object.union(automation_execute, {"approval_id": empty})
	}
	not data.workshop.access.allow with input as object.remove(automation_execute, ["approval_id"])
}

test_ai_agent_may_not_execute if {
	changed := object.union(automation_execute, {
		"role": "persona.ai_agent",
		"purpose": "purpose.ai_assistance",
	})
	not data.workshop.access.allow with input as changed
}

# TA-35. S05-14 Half B. The audit-read row. Only role.admin may read the audit log.
audit_read := {
	"role": "role.admin",
	"action": "action.read",
	"resource": "resource.audit_log",
	"purpose": "purpose.audit_review",
	"scope": "scope.all_records",
	"risk": "risk.read_only",
}

test_admin_may_read_the_audit_log if {
	data.workshop.access.allow with input as audit_read
	data.workshop.access.decision.matrix_rows == ["TA-35"] with input as audit_read
}

test_operator_may_not_read_the_audit_log if {
	every role in ["role.operator", "role.engineer", "persona.ai_agent", "role.clinician"] {
		not data.workshop.access.allow with input as object.union(audit_read, {"role": role})
	}
}

# Every one of the 35 rows allows the call it describes.
row_failures contains grant.row if {
	some grant in data.access_matrix.grants
	call := {
		"role": grant.role,
		"action": grant.action,
		"resource": grant.resource,
		"purpose": grant.purpose,
		"scope": grant.scope,
		"risk": grant.risk,
		"approval_id": "APR-EXAMPLE-0001",
	}
	not data.workshop.access.allow with input as call
}

test_all_35_rows_were_loaded if {
	count(data.access_matrix.grants) == 35
}

test_every_row_allows_its_own_call if {
	count(row_failures) == 0
}

# Every access fixture gives the expected decision and row.
access_fixture_failures contains name if {
	some name, fixture in data.fixtures
	fixture.area == "access"
	d := data.workshop.access.decision with input as fixture.input
	not d.allow == (fixture.expected.decision == "allow")
}

access_fixture_failures contains name if {
	some name, fixture in data.fixtures
	fixture.area == "access"
	d := data.workshop.access.decision with input as fixture.input
	expected_rows := [row | row := fixture.expected.matrix_row; row != null]
	not d.matrix_rows == expected_rows
}

test_access_fixtures_were_loaded if {
	count({name | some name, fixture in data.fixtures; fixture.area == "access"}) == 7
}

test_access_fixtures_give_expected_results if {
	count(access_fixture_failures) == 0
}
