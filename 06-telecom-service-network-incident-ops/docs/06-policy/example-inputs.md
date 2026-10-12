# Example inputs

| Field | Value |
|---|---|
| Stage | S04-06 — Policy as code (Challenge 6), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. 23 fixtures, written out in full. Each of the five policy areas has at least one allow and one deny. The `ai_action` area has ten, one for each outcome path in the playbook. A throwaway script parsed all 23 blocks as JSON and applied the outcome table to the ten `ai_action` fixtures. All ten matched their expected outcome. The script is not in the repo. |
| Evidence sources | `docs/06-policy/policy-catalogue.md`; `docs/06-policy/ai-action-policy-design.md`; `docs/03-identity/policy-input-model.md`; `docs/03-identity/target-access-matrix.md`; `docs/03-identity/negative-access-test-plan.md`; `docs/04-secrets/sensitive-field-handling-checklist.md`; `semantic-layer/ai-context-policy.yaml`; `semantic-layer/access-semantics.yaml`; `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md` |
| Assumptions | Half B writes each block below as one JSON file under `policy/tests/fixtures/`. The expected values follow the outcome table in `ai-action-policy-design.md` and the rows TA-01 to TA-34. The key names for areas 3, 4, and 5 are PROPOSED. Owner: Team-Force. |
| Unresolved issues | The approval id format is Unknown. The fixtures use the placeholder `APR-EXAMPLE-0001`. The running policy version string is Unknown. The fixtures use the PROPOSED string `0.1.0-proposed`. Areas 3, 4, and 5 have no Rego in Half B, so their fixtures check a small Python comparison or only load as JSON. |
| Residual risks | A fixture proves the table, not the running API. The API only meets the table after Half B wires `policy.py`. The fixture for area 5 is a design example. No readiness check runs today. |

## What this file is

This file holds the example inputs the policy tests will use. Each fixture is a JSON object with four keys. `name` is the fixture name. `area` is one of the five policy areas. `input` is what the policy reads. `expected` is the answer the policy must give.

Half A writes the fixtures. The files under `policy/tests/fixtures/` and the tests come in Half B.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Index

| Fixture | File name Half B writes | Area | Expected | Table row or matrix row |
|---|---|---|---|---|
| AC-01 | `ac-01-allow-noc-operator-reads-device.json` | Access | allow | TA-01 |
| AC-02 | `ac-02-allow-ai-agent-recommends-incident.json` | Access | allow | TA-33 |
| AC-03 | `ac-03-deny-clinician-reads-device.json` | Access | deny | No TA row. `removed_roles`. |
| AC-04 | `ac-04-deny-admin-reads-device.json` | Access | deny | No TA row. `role.admin` has no grant. |
| AC-05 | `ac-05-deny-automation-service-executes-without-approval.json` | Access | deny | TA-24 with an empty approval id |
| AI-01 | `ai-01-execute-with-all-checks.json` | AI approval | EXECUTE | O3. Worked combination W14. |
| AI-02 | `ai-02-block-execute-without-approval-id.json` | AI approval | BLOCK | B8. W10. The playbook done test. |
| AI-03 | `ai-03-recommend-only-summary.json` | AI approval | RECOMMEND_ONLY | O1. W1. |
| AI-04 | `ai-04-hold-recommendation-for-review.json` | AI approval | HOLD_FOR_REVIEW | O2. W2. |
| AI-05 | `ai-05-hold-on-timeout.json` | AI approval | HOLD_FOR_REVIEW | H1 and H2. W5. |
| AI-06 | `ai-06-block-stale-topology.json` | AI approval | BLOCK | B5. W3. |
| AI-07 | `ai-07-block-ai-agent-execute.json` | AI approval | BLOCK | B2 and B6. W11. |
| AI-08 | `ai-08-block-forbidden-field-in-prompt.json` | AI approval | BLOCK | B4. W7. |
| AI-09 | `ai-09-block-execute-audit-row-missing.json` | AI approval | BLOCK | B9. W12. |
| AI-10 | `ai-10-block-execute-approval-not-required.json` | AI approval | BLOCK | B7. W13. |
| DU-01 | `du-01-allow-prompt-allow-list-only.json` | Data use | allow | `policy.prompt_fields` allowed list |
| DU-02 | `du-02-deny-prompt-holds-mgmt-ip.json` | Data use | deny | `rule.forbidden_fields_never_enter_prompt` |
| DU-03 | `du-03-allow-network-engineer-response-sensitive-fields.json` | Data use | allow | TA-15 |
| DU-04 | `du-04-deny-noc-operator-response-sensitive-fields.json` | Data use | deny | TA-01 has no sensitive-field read. Defect F10. |
| OS-01 | `os-01-allow-live-change-with-all-checks.json` | Operational safety | allow | `outcome.execute` |
| OS-02 | `os-02-deny-live-change-plan-not-reversible-validated.json` | Operational safety | deny | `outcome.execute`, fourth check |
| PR-01 | `pr-01-allow-release-with-all-evidence.json` | Production readiness | allow | Design example |
| PR-02 | `pr-02-deny-release-with-missing-evidence.json` | Production readiness | deny | Design example |

## Area 1 — Access

The input shape is the one in `docs/03-identity/policy-input-model.md`. The key is `role`. AC-01, AC-03, and AC-05 reuse the JSON from that file and from `negative-access-test-plan.md` (NA-01, NA-02, NA-05).

### AC-01. noc_operator reads a device (allow)

```json
{
  "name": "ac-01-allow-noc-operator-reads-device",
  "area": "access",
  "input": {
    "role": "persona.noc_operator",
    "action": "action.read",
    "resource": "resource.device",
    "purpose": "purpose.incident_triage",
    "scope": "scope.all_records",
    "risk": "risk.read_only"
  },
  "expected": { "decision": "allow", "matrix_row": "TA-01" }
}
```

### AC-02. ai_agent recommends on an incident (allow)

```json
{
  "name": "ac-02-allow-ai-agent-recommends-incident",
  "area": "access",
  "input": {
    "role": "persona.ai_agent",
    "action": "action.recommend",
    "resource": "resource.incident",
    "purpose": "purpose.ai_assistance",
    "scope": "scope.assigned_incident",
    "risk": "risk.recommendation"
  },
  "expected": { "decision": "allow", "matrix_row": "TA-33" }
}
```

### AC-03. clinician reads a device (deny)

```json
{
  "name": "ac-03-deny-clinician-reads-device",
  "area": "access",
  "input": {
    "role": "role.clinician",
    "action": "action.read",
    "resource": "resource.device",
    "purpose": "purpose.incident_triage",
    "scope": "scope.all_records",
    "risk": "risk.read_only"
  },
  "expected": { "decision": "deny", "matrix_row": null }
}
```

### AC-04. admin reads a device (deny)

Today the Python list and `access.rego` both allow `admin`. The target matrix gives `role.admin` no row. This fixture records the target. K02 says `admin` reads `REC-0001` today, so Half B changes that result. See `exception-handling-model.md` for the decision on a dated waiver.

```json
{
  "name": "ac-04-deny-admin-reads-device",
  "area": "access",
  "input": {
    "role": "role.admin",
    "action": "action.read",
    "resource": "resource.device",
    "purpose": "purpose.incident_triage",
    "scope": "scope.all_records",
    "risk": "risk.read_only"
  },
  "expected": { "decision": "deny", "matrix_row": null }
}
```

### AC-05. automation_service executes with no approval id (deny)

The six fields match TA-24. The empty approval id makes the decision deny.

```json
{
  "name": "ac-05-deny-automation-service-executes-without-approval",
  "area": "access",
  "input": {
    "role": "persona.automation_service",
    "action": "action.execute",
    "resource": "resource.device",
    "purpose": "purpose.scheduled_automation",
    "scope": "scope.assigned_incident",
    "risk": "risk.live_network_change",
    "approval_id": null
  },
  "expected": { "decision": "deny", "matrix_row": "TA-24" }
}
```

## Area 2 — AI approval (`ai_action`)

Every fixture here has the 15 inputs from `ai-action-policy-design.md`. Fixtures AI-01 to AI-09 follow worked combinations W14, W10, W1, W2, W5, W3, W11, W7, and W12. AI-10 follows W13.

### AI-01. Execute with all checks (EXECUTE)

```json
{
  "name": "ai-01-execute-with-all-checks",
  "area": "ai_action",
  "input": {
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
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "EXECUTE",
    "reasons": ["ai_use.remediation_execution"]
  }
}
```

### AI-02. Execute with an empty approval id (BLOCK)

This is the done test in the playbook. Everything is the same as AI-01 except `approval_id`.

```json
{
  "name": "ai-02-block-execute-without-approval-id",
  "area": "ai_action",
  "input": {
    "persona": "persona.automation_service",
    "action": "action.execute",
    "resource": "resource.device",
    "risk": "risk.live_network_change",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": true,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["rule.ai_recommendation_needs_policy_approval_audit_before_state_change"]
  }
}
```

### AI-03. Summary (RECOMMEND_ONLY)

```json
{
  "name": "ai-03-recommend-only-summary",
  "area": "ai_action",
  "input": {
    "persona": "persona.noc_operator",
    "action": "action.summarize",
    "resource": "resource.incident",
    "risk": "risk.recommendation",
    "policy_result": "allow",
    "approval_required": false,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": false,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "RECOMMEND_ONLY",
    "reasons": ["ai_use.incident_summary"]
  }
}
```

### AI-04. Recommendation held for a person (HOLD_FOR_REVIEW)

```json
{
  "name": "ai-04-hold-recommendation-for-review",
  "area": "ai_action",
  "input": {
    "persona": "persona.noc_operator",
    "action": "action.recommend",
    "resource": "resource.incident",
    "risk": "risk.recommendation",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": false,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "HOLD_FOR_REVIEW",
    "reasons": ["ai_use.next_action_recommendation", "ai_use.configuration_suggestion"]
  }
}
```

### AI-05. Model timed out (HOLD_FOR_REVIEW)

```json
{
  "name": "ai-05-hold-on-timeout",
  "area": "ai_action",
  "input": {
    "persona": "persona.noc_operator",
    "action": "action.recommend",
    "resource": "resource.incident",
    "risk": "risk.recommendation",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": false,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": null,
    "timeout_hit": true,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "HOLD_FOR_REVIEW",
    "reasons": ["failmode.timeout", "failmode.schema_failure"]
  }
}
```

### AI-06. Stale topology flag is true (BLOCK)

```json
{
  "name": "ai-06-block-stale-topology",
  "area": "ai_action",
  "input": {
    "persona": "persona.noc_operator",
    "action": "action.recommend",
    "resource": "resource.device",
    "risk": "risk.recommendation",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": false,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": true,
    "output_schema_ok": null,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["failmode.stale_topology_true", "rule.stale_topology_blocks_recommendation"]
  }
}
```

### AI-07. ai_agent asks to execute (BLOCK)

```json
{
  "name": "ai-07-block-ai-agent-execute",
  "area": "ai_action",
  "input": {
    "persona": "persona.ai_agent",
    "action": "action.execute",
    "resource": "resource.device",
    "risk": "risk.live_network_change",
    "policy_result": "deny",
    "approval_required": true,
    "approval_id": "APR-EXAMPLE-0001",
    "audit_row_written": true,
    "change_plan_ok": true,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["provenance.policy_result", "rule.ai_output_cannot_execute"]
  }
}
```

### AI-08. Forbidden field found in the prompt (BLOCK)

```json
{
  "name": "ai-08-block-forbidden-field-in-prompt",
  "area": "ai_action",
  "input": {
    "persona": "persona.noc_operator",
    "action": "action.recommend",
    "resource": "resource.device",
    "risk": "risk.recommendation",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": null,
    "audit_row_written": true,
    "change_plan_ok": false,
    "record_found": true,
    "forbidden_field_in_prompt": true,
    "stale_topology_flag": false,
    "output_schema_ok": null,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["failmode.forbidden_field_in_prompt", "rule.forbidden_fields_never_enter_prompt"]
  }
}
```

### AI-09. Execute with the audit row missing (BLOCK)

```json
{
  "name": "ai-09-block-execute-audit-row-missing",
  "area": "ai_action",
  "input": {
    "persona": "persona.automation_service",
    "action": "action.execute",
    "resource": "resource.circuit",
    "risk": "risk.live_network_change",
    "policy_result": "allow",
    "approval_required": true,
    "approval_id": "APR-EXAMPLE-0001",
    "audit_row_written": false,
    "change_plan_ok": true,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["rule.ai_recommendation_needs_policy_approval_audit_before_state_change"]
  }
}
```

### AI-10. Execute with approval not required (BLOCK)

The caller sends `approval_required` false and a set approval id. Row B7 refuses it.

```json
{
  "name": "ai-10-block-execute-approval-not-required",
  "area": "ai_action",
  "input": {
    "persona": "persona.automation_service",
    "action": "action.execute",
    "resource": "resource.device",
    "risk": "risk.live_network_change",
    "policy_result": "allow",
    "approval_required": false,
    "approval_id": "APR-EXAMPLE-0001",
    "audit_row_written": true,
    "change_plan_ok": true,
    "record_found": true,
    "forbidden_field_in_prompt": false,
    "stale_topology_flag": false,
    "output_schema_ok": true,
    "timeout_hit": false,
    "policy_version": "0.1.0-proposed"
  },
  "expected": {
    "outcome": "BLOCK",
    "reasons": ["rule.ai_recommendation_needs_policy_approval_audit_before_state_change"]
  }
}
```

## Area 3 — Data use

The input keys `persona`, `destination`, and `fields` are PROPOSED. The field ids are the `field.*` ids in `semantic-layer/entities.yaml`. The prompt allow list and forbidden list are `policy.prompt_fields`.

### DU-01. Prompt holds only allow-listed fields (allow)

```json
{
  "name": "du-01-allow-prompt-allow-list-only",
  "area": "data_use",
  "input": {
    "persona": "persona.ai_agent",
    "destination": "prompt",
    "fields": [
      "field.device.device_id",
      "field.device.hostname",
      "field.device.vendor",
      "field.device.stale_topology_flag",
      "field.alarm.alarm_id",
      "field.alarm.severity"
    ]
  },
  "expected": { "decision": "allow", "reasons": [] }
}
```

### DU-02. Prompt holds `mgmt_ip` (deny)

```json
{
  "name": "du-02-deny-prompt-holds-mgmt-ip",
  "area": "data_use",
  "input": {
    "persona": "persona.ai_agent",
    "destination": "prompt",
    "fields": [
      "field.device.device_id",
      "field.device.hostname",
      "field.device.mgmt_ip"
    ]
  },
  "expected": {
    "decision": "deny",
    "reasons": ["rule.forbidden_fields_never_enter_prompt"]
  }
}
```

### DU-03. network_engineer receives the sensitive fields in a response (allow)

```json
{
  "name": "du-03-allow-network-engineer-response-sensitive-fields",
  "area": "data_use",
  "input": {
    "persona": "persona.network_engineer",
    "destination": "response",
    "fields": [
      "field.device.device_id",
      "field.device.mgmt_ip",
      "field.device.credential_profile"
    ]
  },
  "expected": { "decision": "allow", "matrix_row": "TA-15" }
}
```

### DU-04. noc_operator receives the sensitive fields in a response (deny)

Today the API returns both cells to this caller (defect F10). The target matrix allows them for `persona.network_engineer` only.

```json
{
  "name": "du-04-deny-noc-operator-response-sensitive-fields",
  "area": "data_use",
  "input": {
    "persona": "persona.noc_operator",
    "destination": "response",
    "fields": [
      "field.device.device_id",
      "field.device.mgmt_ip",
      "field.device.credential_profile"
    ]
  },
  "expected": { "decision": "deny", "matrix_row": null }
}
```

## Area 4 — Operational safety

The input keys are the same names as in area 2. The decision is allow or deny for a change to a live device or circuit.

### OS-01. Live change with every check present (allow)

```json
{
  "name": "os-01-allow-live-change-with-all-checks",
  "area": "operational_safety",
  "input": {
    "persona": "persona.automation_service",
    "action": "action.execute",
    "risk": "risk.live_network_change",
    "approval_id": "APR-EXAMPLE-0001",
    "audit_row_written": true,
    "change_plan_ok": true
  },
  "expected": { "decision": "allow" }
}
```

### OS-02. Live change that is not reversible and validated (deny)

```json
{
  "name": "os-02-deny-live-change-plan-not-reversible-validated",
  "area": "operational_safety",
  "input": {
    "persona": "persona.automation_service",
    "action": "action.execute",
    "risk": "risk.live_network_change",
    "approval_id": "APR-EXAMPLE-0001",
    "audit_row_written": true,
    "change_plan_ok": false
  },
  "expected": { "decision": "deny" }
}
```

## Area 5 — Production readiness

The input keys are PROPOSED. The section slugs come from the headings of `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md`. The YAML has no ids for them. See "Open questions for S03" in `policy-catalogue.md`.

### PR-01. Release with all evidence (allow)

```json
{
  "name": "pr-01-allow-release-with-all-evidence",
  "area": "production_readiness",
  "input": {
    "evidence_sections_missing": [],
    "policy_tests_result": "pass",
    "secret_pattern_test_result": "pass",
    "ci_run_seen": true
  },
  "expected": { "decision": "allow" }
}
```

### PR-02. Release with missing evidence (deny)

The input is a smaller version of today's state. Today all 15 sections are empty and no CI run has been seen (IG-09).

```json
{
  "name": "pr-02-deny-release-with-missing-evidence",
  "area": "production_readiness",
  "input": {
    "evidence_sections_missing": ["policy_as_code_evidence", "ci_cd_and_supply_chain_evidence"],
    "policy_tests_result": "not_run",
    "secret_pattern_test_result": "pass",
    "ci_run_seen": false
  },
  "expected": { "decision": "deny" }
}
```

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| EI-01 | Every policy area has at least one allow fixture and one deny fixture. | Verified Fact. Fixtures AC-01 to PR-02 above. | The done test for Half A is met for fixtures. | A fixture for an area with no Rego (3, 4, 5) proves only the table. | High | None. |
| EI-02 | The playbook done test is fixture AI-02. | Verified Fact. Playbook line 110. `approval_id` null and `action` `action.execute` give BLOCK by row B8. | The suite holds a named test for the done test. | Half B could write a weaker test. | High | None. |
| EI-03 | AC-04 changes what `admin` can do on `GET /records/{id}`. | Verified Fact. K02. `target-access-matrix.md` "Callers with no allow row". `access-semantics.yaml` `maps_to_persona: null`. | Existing tests that send `X-User-Role: admin` will fail once the policy is wired. | A rushed fix could add an admin row and undo least privilege. | High | Whether admin keeps read access through a dated waiver is a decision for acceptance. |
| EI-04 | The fixtures use placeholders for the approval id and the policy version. | Verified Fact for the strings. The repo defines neither format. | Half B must hold both strings in one place. | A real approval id with a different shape. | High | The approval id format is Unknown. |

## Lifecycle

This file cites `docs/03-identity/policy-input-model.md` and `docs/03-identity/negative-access-test-plan.md` for the access fixtures, and `ai-action-policy-design.md` for the `ai_action` fixtures. Stage S04-06 Half B turns each block into a file under `policy/tests/fixtures/`. Stage S05-13 collects the tests. Stage S09 cites AI-01 and AI-02 as D4 proof.
