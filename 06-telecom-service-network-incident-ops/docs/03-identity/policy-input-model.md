# Policy input model

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half A |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The JSON shape names a YAML id for each value set. A call with no role header stays the current default `operator`. The proposed change is to refuse that call. Owner: Team-Force. |
| Evidence sources | `semantic-layer/access-semantics.yaml`; `policy/opa/access.rego`; `apps/api/main.py`; `semantic-layer/business-rules.yaml`; `semantic-layer/ai-context-policy.yaml` (`provenance.approval_id`); `docs/03-identity/target-access-matrix.md` |
| Assumptions | OPA will receive one JSON object per call. A decision is allow only when that object matches one row TA-01 to TA-34 on role, action, resource, purpose, scope, and risk. That match rule is PROPOSED. Owner: Team-Force. |
| Unresolved issues | There is no role id for a header that was never sent. TA-24 and TA-25 also need the approval id, which lives outside the five access value lists. |
| Residual risks | Today's OPA file reads `input.role` and `input.action` only. It compares the header word `admin`. The YAML id is `role.admin`. S04-06 maps the header word onto the id, or the new rules will miss. |

## What this file is

This file is the JSON object OPA will receive for an access decision. The fields are role, action, resource, purpose, scope, and risk. Stage S04-06 reads this shape and extends `policy/opa/access.rego`.

Half A writes this document. The Rego file stays as it is.

Today the file allows any `admin`, and `operator` when the action is `read`. **Verified Fact:** `access.rego` lines 6 to 11. `policy.opa.admin_any`. `policy.opa.operator_read`. The comment on line 5 says participants should add resource and purpose constraints. This shape is those constraints, plus scope and risk.

## Value set for each field

| JSON field | Value set | YAML id of the set | Each value looks like |
|---|---|---|---|
| `role` | The seven personas, plus the five API roles where the caller is one of those roles | `personas` and `api_roles_today` in `access-semantics.yaml` | `persona.noc_operator` or `role.clinician` |
| `action` | `actions` | The `actions` list. Six ids. | `action.read` |
| `resource` | `resources` | The `resources` list. Ten ids. | `resource.device` |
| `purpose` | `purposes` | The `purposes` list. Eight ids. | `purpose.incident_triage` |
| `scope` | `scopes` | The `scopes` list. Six ids. | `scope.all_records` |
| `risk` | `risks` | The `risks` list. Four ids. | `risk.read_only` |

The six action ids are `action.read`, `action.summarize`, `action.recommend`, `action.approve`, `action.write`, `action.execute`.

The ten resource ids are `resource.device`, `resource.circuit`, `resource.alarm`, `resource.incident`, `resource.service_order`, `resource.ai_invocation`, `resource.event`, `resource.audit_log`, `resource.approval`, `resource.sensitive_device_fields`.

The eight purpose ids are `purpose.incident_triage`, `purpose.network_change_planning`, `purpose.field_repair`, `purpose.customer_enquiry`, `purpose.scheduled_automation`, `purpose.vendor_support`, `purpose.ai_assistance`, `purpose.audit_review`.

The six scope ids are `scope.all_records`, `scope.one_site`, `scope.one_customer`, `scope.assigned_incident`, `scope.own_vendor_devices`, `scope.none`.

The four risk ids are `risk.read_only`, `risk.recommendation`, `risk.decision`, `risk.live_network_change`.

`action` is in the shape because every grant has an action and today's Rego already reads `input.action`. The five fields the next stage names are role, resource, purpose, scope, and risk. Action stays beside them.

## Header word to role id

The live header is `X-User-Role`. The JSON `role` field stores the YAML id. The table below maps each header word to that id.

| Header word today | JSON `role` | Persona on the target row | Label |
|---|---|---|---|
| `admin` | `role.admin` | none | Verified Fact. `maps_to_persona: null`. |
| `operator` | `role.operator` for the live call. The target row uses `persona.noc_operator`. | `persona.noc_operator` | Map is Inference. |
| `clinician` | `role.clinician` | none | Verified Fact. `removed_roles`. |
| `engineer` | `role.engineer` for the live call. The target row uses `persona.network_engineer`. | `persona.network_engineer` | Map is Inference. |
| `ai_agent` | `persona.ai_agent` | `persona.ai_agent` | Verified Fact. The header word and the persona name are the same string. |
| header absent | `role.operator` | `persona.noc_operator` | Verified Fact for the fill-in. `main.py` line 11. `status.code.role_header_default.operator`. |

S04-06 compares the JSON id. A rule that still compares the header word `admin` will not match the id `role.admin`.

## Shape

```json
{
  "role": "persona.noc_operator",
  "action": "action.read",
  "resource": "resource.device",
  "purpose": "purpose.incident_triage",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

That object is row TA-01. The decision is allow.

Worked example. A caller sends `GET /records/REC-0001` with header `operator`. The API today treats the header as the word `operator` and returns the `REC-0001` row. The policy input for the target row is the JSON above. The link from the word `operator` to `persona.noc_operator` is an Inference.

## Decision rule

Start from `default allow = false`. **Verified Fact:** `access.rego` line 3.

The decision is allow when one row TA-01 to TA-34 has the same role, action, resource, purpose, scope, and risk as the JSON. Otherwise the decision is deny.

Two extra stops sit on top of that match.

1. TA-24 and TA-25 match the six fields and the decision is still deny while the approval id is empty. The id for that string is `provenance.approval_id` in `semantic-layer/ai-context-policy.yaml`. The resource of the stored approval is `resource.approval`. The rule is `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`.
2. An action on the persona's `denied` list is deny even when some other field matches.

`scope.none` means no records. It is the scope for an action a persona may never take. A denied execute can also be written with the caller's real scope. The negative test uses the caller's real scope so the deny is about the action.

## Examples the negative tests use

Allow. `persona.noc_operator` reads a device. Decision allow. Row TA-01.

```json
{
  "role": "persona.noc_operator",
  "action": "action.read",
  "resource": "resource.device",
  "purpose": "purpose.incident_triage",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

Deny. `role.clinician` asks for the same read. No TA row has `role.clinician`. Decision deny.

```json
{
  "role": "role.clinician",
  "action": "action.read",
  "resource": "resource.device",
  "purpose": "purpose.incident_triage",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

Allow. `persona.ai_agent` recommends on an incident. Decision allow. Row TA-33.

```json
{
  "role": "persona.ai_agent",
  "action": "action.recommend",
  "resource": "resource.incident",
  "purpose": "purpose.ai_assistance",
  "scope": "scope.assigned_incident",
  "risk": "risk.recommendation"
}
```

Deny. `persona.ai_agent` asks to execute. `action.execute` is on that persona's denied list. Decision deny.

```json
{
  "role": "persona.ai_agent",
  "action": "action.execute",
  "resource": "resource.device",
  "purpose": "purpose.ai_assistance",
  "scope": "scope.assigned_incident",
  "risk": "risk.live_network_change"
}
```

Deny. `persona.automation_service` asks to execute and the approval id is empty. The six fields match TA-24. The empty approval id makes the decision deny.

```json
{
  "role": "persona.automation_service",
  "action": "action.execute",
  "resource": "resource.device",
  "purpose": "purpose.scheduled_automation",
  "scope": "scope.assigned_incident",
  "risk": "risk.live_network_change",
  "approval_id": null
}
```

`approval_id` is an extra key for TA-24 and TA-25. It is not one of the six access fields. The value `null` means `provenance.approval_id` is absent. The key name is the one stage S04-06 already uses on the AI action input.

Current call with no role header. The server fills in `operator`. The JSON uses `role.operator`. The target persona on that read is `persona.noc_operator` (TA-01). The choice for Half B is to keep this fill-in. The proposed change is to refuse the call under `rule.no_default_role`. Owner: Team-Force.

```json
{
  "role": "role.operator",
  "action": "action.read",
  "resource": "resource.device",
  "purpose": "purpose.incident_triage",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| PI-01 | The access decision needs six fields, and each field has a value set with ids in `access-semantics.yaml`. | Verified Fact. The five lists plus `personas` and `api_roles_today`. Today's Rego reads two of them: `input.role` and `input.action`. | S04-06 can write rules against these ids. | A rule that compares a header word to a YAML id will miss. | High | None for the six sets. |
| PI-02 | TA-24 and TA-25 need an approval id on the input. That id is `provenance.approval_id` in the AI context file. The five access lists name the stored approval as `resource.approval`. | Verified Fact. `ai-context-policy.yaml` `provenance.approval_id`. `resource.approval`. The grant's `requires_rule`. | An execute input can show an empty approval id. The id already exists. | A reader of only the five access lists will miss the approval-id string. | High | None. The id exists in the other YAML file. |
| PI-03 | A missing role header has a current JSON role, `role.operator`, and no separate id that means "header absent". | Verified Fact. `main.py` line 11. `rule.no_default_role`. `status.code.role_header_default.operator` points at `role.operator`. | The test case can name `role.operator`. A future deny of the empty header cannot name a role id of its own. | If S04-06 fills `role.operator` before the check, the proposed deny never sees an empty header. | High | Open question for S03: there is no id for a call that sends no role header. This design needs that id so a deny rule can name the role field when the header is absent, without first storing `role.operator`. |

## Lifecycle

Stage S04-06 consumes this shape for `access.rego` and for the access half of its fixtures. The AI action policy in that stage adds its own inputs, including `approval_id`. Stage S05-13 collects the tests that send this JSON. Stage S06 cites the target matrix these inputs point at.
