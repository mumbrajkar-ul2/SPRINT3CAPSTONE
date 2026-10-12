# Target access matrix

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half A |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every allow row names a YAML id for role, action, resource, purpose, scope, and risk. A call with no role header stays the current default `operator`. The proposed change is to refuse that call. Owner: Team-Force. |
| Evidence sources | `semantic-layer/access-semantics.yaml` personas and the five value lists; `semantic-layer/business-rules.yaml`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/defect-list.md`; `docs/01-discovery/brownfield-risk-register.md`; `docs/00-contract/operating-contract.md` row 9 and row 10 |
| Assumptions | A call is allowed only when role, action, resource, purpose, scope, and risk all match one row below. The grants stay PROPOSED. Copying them into this file does not accept them. Owner: Team-Force. Operating contract row 10. |
| Unresolved issues | No YAML id means "the role header was absent". The alarm-to-incident join is Unknown, so `scope.assigned_incident` can name the incident row only. The `vendor` column holds status words, so `scope.own_vendor_devices` cannot be computed yet. Whether `role.engineer` remains the API string for `persona.network_engineer` is Unknown. |
| Residual risks | The live API still uses the five-name list in `current-role-matrix.md`. These rows do not change that list. `role.admin` has no row here, and the OPA file still allows any admin until S04-06. |

## What this file is

This file is the target. Each allow row says who may do what, to which resource, for which purpose, over which records, and at which risk. Every id is copied from `semantic-layer/access-semantics.yaml`. This stage adds no persona, no resource name, and no scope value.

Least privilege means a caller can take only the actions on these rows. The live API still follows `apps/api/main.py` line 13. Half A writes this document. The Python files stay as they are.

The seven persona grants are PROPOSED. Owner: Team-Force. The YAML says stage S04-03 confirms the mappings. This file confirms the copy: the ids below match the grants, and the labels on the API-role map stay as the YAML wrote them. The grants stay PROPOSED until Team-Force accepts them in writing.

## How to read a row

| Column | Value set in the YAML | What the cell means |
|---|---|---|
| Role | `personas` | The caller. Example: `persona.noc_operator` is a person in the network operations centre. |
| Action | `actions` | What they ask to do. `action.read` looks at a stored row. `action.execute` would change a live device or circuit. |
| Resource | `resources` | What they do it to. `resource.device` is a device row. |
| Purpose | `purposes` | Why. `purpose.incident_triage` is working out what is wrong on an open incident. |
| Scope | `scopes` | Which rows. `scope.all_records` is every row of that resource. |
| Risk | `risks` | How much harm a wrong action can do. `risk.read_only` means nothing changes. |

Worked example for one allow. `persona.noc_operator` reads `resource.device` for `purpose.incident_triage`, scope `scope.all_records`, risk `risk.read_only`. That is row TA-01. On the live API the header word for that person is `operator`, and the map is an Inference. `GET /records/REC-0001` with that header returns the `REC-0001` device row today, including `mgmt_ip` and `credential_profile`. Row TA-01 does not include `resource.sensitive_device_fields`. The only allow for those two cells is TA-15, `persona.network_engineer`.

## Persona index

| Persona | Plain name | API role today | Map label | Actions the YAML denies |
|---|---|---|---|---|
| `persona.noc_operator` | noc_operator | `role.operator` | Inference | `action.execute` |
| `persona.network_engineer` | network_engineer | `role.engineer` | Inference | `action.execute` |
| `persona.field_engineer` | field_engineer | none (`api_role_today: null`) | Verified Fact | `action.approve`, `action.execute`, `action.write` |
| `persona.customer_support` | customer_support | none | Verified Fact | `action.approve`, `action.execute`, `action.write`, `action.recommend` |
| `persona.automation_service` | automation_service | none | Verified Fact | `action.approve` |
| `persona.vendor_account` | vendor_account | none | Verified Fact | `action.approve`, `action.execute`, `action.write`, `action.recommend` |
| `persona.ai_agent` | ai_agent | `role.ai_agent` | Verified Fact | `action.approve`, `action.execute`, `action.write` |

`role.admin` has `maps_to_persona: null`. It has no allow row. `role.clinician` is under `removed_roles`. It has no allow row.

## Allow rows

Each row is one resource taken from a grant. The purpose, scope, and risk are the ones on that grant. All 34 rows are PROPOSED. Owner: Team-Force.

| Row | Role | Action | Resource | Purpose | Scope | Risk |
|---|---|---|---|---|---|---|
| TA-01 | `persona.noc_operator` | `action.read` | `resource.device` | `purpose.incident_triage` | `scope.all_records` | `risk.read_only` |
| TA-02 | `persona.noc_operator` | `action.read` | `resource.alarm` | `purpose.incident_triage` | `scope.all_records` | `risk.read_only` |
| TA-03 | `persona.noc_operator` | `action.read` | `resource.incident` | `purpose.incident_triage` | `scope.all_records` | `risk.read_only` |
| TA-04 | `persona.noc_operator` | `action.read` | `resource.circuit` | `purpose.incident_triage` | `scope.all_records` | `risk.read_only` |
| TA-05 | `persona.noc_operator` | `action.summarize` | `resource.incident` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.recommendation` |
| TA-06 | `persona.noc_operator` | `action.summarize` | `resource.device` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.recommendation` |
| TA-07 | `persona.noc_operator` | `action.recommend` | `resource.incident` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.recommendation` |
| TA-08 | `persona.noc_operator` | `action.recommend` | `resource.device` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.recommendation` |
| TA-09 | `persona.noc_operator` | `action.approve` | `resource.ai_invocation` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.decision` |
| TA-10 | `persona.noc_operator` | `action.write` | `resource.incident` | `purpose.incident_triage` | `scope.assigned_incident` | `risk.decision` |
| TA-11 | `persona.network_engineer` | `action.read` | `resource.device` | `purpose.network_change_planning` | `scope.all_records` | `risk.read_only` |
| TA-12 | `persona.network_engineer` | `action.read` | `resource.circuit` | `purpose.network_change_planning` | `scope.all_records` | `risk.read_only` |
| TA-13 | `persona.network_engineer` | `action.read` | `resource.alarm` | `purpose.network_change_planning` | `scope.all_records` | `risk.read_only` |
| TA-14 | `persona.network_engineer` | `action.read` | `resource.incident` | `purpose.network_change_planning` | `scope.all_records` | `risk.read_only` |
| TA-15 | `persona.network_engineer` | `action.read` | `resource.sensitive_device_fields` | `purpose.network_change_planning` | `scope.all_records` | `risk.read_only` |
| TA-16 | `persona.network_engineer` | `action.recommend` | `resource.device` | `purpose.network_change_planning` | `scope.all_records` | `risk.recommendation` |
| TA-17 | `persona.network_engineer` | `action.approve` | `resource.approval` | `purpose.network_change_planning` | `scope.all_records` | `risk.decision` |
| TA-18 | `persona.field_engineer` | `action.read` | `resource.device` | `purpose.field_repair` | `scope.one_site` | `risk.read_only` |
| TA-19 | `persona.field_engineer` | `action.read` | `resource.alarm` | `purpose.field_repair` | `scope.one_site` | `risk.read_only` |
| TA-20 | `persona.customer_support` | `action.read` | `resource.circuit` | `purpose.customer_enquiry` | `scope.one_customer` | `risk.read_only` |
| TA-21 | `persona.customer_support` | `action.read` | `resource.service_order` | `purpose.customer_enquiry` | `scope.one_customer` | `risk.read_only` |
| TA-22 | `persona.customer_support` | `action.read` | `resource.incident` | `purpose.customer_enquiry` | `scope.one_customer` | `risk.read_only` |
| TA-23 | `persona.automation_service` | `action.read` | `resource.device` | `purpose.scheduled_automation` | `scope.all_records` | `risk.read_only` |
| TA-24 | `persona.automation_service` | `action.execute` | `resource.device` | `purpose.scheduled_automation` | `scope.assigned_incident` | `risk.live_network_change` |
| TA-25 | `persona.automation_service` | `action.execute` | `resource.circuit` | `purpose.scheduled_automation` | `scope.assigned_incident` | `risk.live_network_change` |
| TA-26 | `persona.vendor_account` | `action.read` | `resource.device` | `purpose.vendor_support` | `scope.own_vendor_devices` | `risk.read_only` |
| TA-27 | `persona.vendor_account` | `action.read` | `resource.alarm` | `purpose.vendor_support` | `scope.own_vendor_devices` | `risk.read_only` |
| TA-28 | `persona.ai_agent` | `action.read` | `resource.device` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.read_only` |
| TA-29 | `persona.ai_agent` | `action.read` | `resource.alarm` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.read_only` |
| TA-30 | `persona.ai_agent` | `action.read` | `resource.incident` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.read_only` |
| TA-31 | `persona.ai_agent` | `action.summarize` | `resource.incident` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.recommendation` |
| TA-32 | `persona.ai_agent` | `action.summarize` | `resource.device` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.recommendation` |
| TA-33 | `persona.ai_agent` | `action.recommend` | `resource.incident` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.recommendation` |
| TA-34 | `persona.ai_agent` | `action.recommend` | `resource.device` | `purpose.ai_assistance` | `scope.assigned_incident` | `risk.recommendation` |

**Row added in S05-14 Half B.** The table above has 34 rows and stays as written. `policy/opa/policy_data.json` now holds one more row, TA-35. TA-35 does not come from the YAML. It comes from `docs/14-audit/audit-read-access-design.md`, and Mangesh (FDE) accepted it on 2026-10-12.

| Row | Role | Action | Resource | Purpose | Scope | Risk |
|---|---|---|---|---|---|---|
| TA-35 | `role.admin` | `action.read` | `resource.audit_log` | `purpose.audit_review` | `scope.all_records` | `risk.read_only` |

The role is the live header word `admin`. It has no persona, so it matches only a row whose role is `role.admin`. TA-35 is the only such row. PROPOSED. Owner: Team-Force. Open question for S03: the YAML has no id for `resource.audit_log` or `purpose.audit_review`.

## Notes copied with the rows

| Rows | Note from the YAML | Label |
|---|---|---|
| TA-09 | This approve accepts or rejects the recommendation text. The live-change approval is TA-17. | Verified Fact that the YAML note says this. The grant is PROPOSED. |
| TA-15 | The only proposed read of `mgmt_ip` and `credential_profile`. Those fields are `field.device.mgmt_ip` and `field.device.credential_profile` on `resource.sensitive_device_fields`. | PROPOSED. Owner: Team-Force. This stage copies that single allow as the S04-03 answer for who may read those cells. The YAML description still says the question is Unknown in the source repo. Acceptance in writing is still Team-Force, under operating contract row 10. |
| TA-17 | The approval of a live network change. The desk job is `network_engineer`, confirmed on 2026-10-10. Stage S04-09 uses this title. | Verified Fact for the desk job. The grant is PROPOSED. |
| TA-24, TA-25 | Allow only when a stored human approval id already exists. The rule is `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. The account leaves the approval id empty. No execute route exists today. An empty approval id makes these two rows a deny. | Verified Fact for the rule id and for "no execute route". The grant is PROPOSED. |
| TA-28, TA-29, TA-30 | The read uses the prompt allow list in `ai-context-policy.yaml`. | PROPOSED note on the grant. The live summary still places the whole device row in the prompt. F12. |

`scope.assigned_incident` filters on `field.incident.incident_id`. The alarm-to-incident join is Unknown, so today this scope can name the incident row only. **Verified Fact:** the scope description in `access-semantics.yaml`. Rows TA-05 through TA-10, TA-24, TA-25, and TA-28 through TA-34 use that scope.

`scope.own_vendor_devices` filters on `field.device.vendor`. That column holds status words today, so the filter cannot be computed until the column holds supplier names. **Verified Fact:** the scope description. Defect F22. Rows TA-26 and TA-27 use that scope.

## Denied actions

The YAML `denied` list names actions. It does not name a resource. A matching allow row is also refused when the action is on this list.

| Role | Denied action ids |
|---|---|
| `persona.noc_operator` | `action.execute` |
| `persona.network_engineer` | `action.execute` |
| `persona.field_engineer` | `action.approve`, `action.execute`, `action.write` |
| `persona.customer_support` | `action.approve`, `action.execute`, `action.write`, `action.recommend` |
| `persona.automation_service` | `action.approve` |
| `persona.vendor_account` | `action.approve`, `action.execute`, `action.write`, `action.recommend` |
| `persona.ai_agent` | `action.approve`, `action.execute`, `action.write` |

An action with no allow row is refused as well. Worked example. `persona.customer_support` asks for `action.summarize` on `resource.incident`, purpose `purpose.customer_enquiry`, scope `scope.one_customer`, risk `risk.recommendation`. No row TA-01 through TA-34 matches. The decision is deny. The denied list does not have to name `action.summarize` for that result. **Assumption:** the match must be exact on all six fields. Owner of that match rule: Team-Force. PROPOSED.

## Callers with no allow row

| Caller | Result in this target | Proof |
|---|---|---|
| `role.admin` | No grant. `rule.shared_admin_not_least_privilege` says an admin role that is allowed every action breaks least privilege. S04-06 replaces admin-any with these rows. | Verified Fact: `maps_to_persona: null`. `policy.opa.admin_any`. The rule id. |
| `role.clinician` | No grant. `removed_roles` says S04-03 removes it from the allow list. Half B does that removal. | Verified Fact: `removed_roles`. F03. |
| `app_shared` | No persona id, so no row. Splitting it is backlog item PB-02. | Verified Fact: the user name is in three files. The link to a persona is Unknown. |
| `OT_VENDOR_TOKEN` | The token has no persona id. The target gives it no row. | Verified Fact: `current-role-matrix.md` finding CR-07. |
| Header absent | The live value stays `role.operator` until the proposed change. See the backlog. The proposed refuse has no role id yet. | Verified Fact for the live default. The proposal is PROPOSED. Owner: Team-Force. |

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| TA-F1 | The target has 34 allow rows, one per persona-resource pair on the grants. Each row names role, action, resource, purpose, scope, and risk with a YAML id. | Verified Fact. Rows TA-01 to TA-34 match `access-semantics.yaml` `personas`. | S04-06 can turn each row into a rule. | A partial match would allow a caller the grant does not name. The match rule above is PROPOSED. | High for the copy. Medium for the match rule, because the YAML does not spell out partial matches. | None for the 34 ids. |
| TA-F2 | Only `persona.network_engineer` may read `resource.sensitive_device_fields`. That is TA-15. | Verified Fact that the YAML grant lists that resource on this persona only. PROPOSED. Owner: Team-Force. | Other personas' device reads do not include `mgmt_ip` and `credential_profile`. | Today every allowed API role receives both cells. F10. R14. This file does not change that return. | High for the copy. The live exposure stays until a later stage masks the row. | The YAML description still says which personas may read them is Unknown in the source. This table is the proposal S04-03 copies. |
| TA-F3 | `persona.ai_agent` may recommend (TA-33, TA-34) and is denied `action.execute`. | Verified Fact. The grants and the `denied` list. AI qualification: the model stops at the sentence. Agency recommend. | A recommendation is text. A live change stays on TA-24 and TA-25, and only after an approval id. | A later worker can still treat the summary JSON as a change ticket. F12. Operating contract row 9 forbids that step. | High | None for these ids. |
| TA-F4 | `persona.automation_service` may execute only on TA-24 and TA-25, and only when an approval id is already stored. | Verified Fact. The grant's `requires_rule`. Operating contract row 9. AI qualification remediation execution row. | With an empty approval id the decision is deny. | No execute route exists, so the live app cannot apply this row yet. The account is also absent from the Python allow list. R06. | High | Whether this persona is `app_shared` is Unknown. |
| TA-F5 | `persona.noc_operator` may read a device (TA-01). The live header for that read is `operator`. The header `noc_operator` is refused today. | Verified Fact for TA-01. The map is Inference (`mapping_label` on `role.operator`). F14. | The negative test that can pass in Half B sends `operator`. | A caller who sends the persona name is refused by the current list. | High for the two strings. Medium for treating them as one caller. | Which string the demo user will send is the open question on R20. |

## Lifecycle

This file cites `docs/01-discovery/brownfield-risk-register.md` (R06, R14, R20), `docs/02-baseline/defect-list.md` (F03, F10, F12, F14, F22), and `docs/02-baseline/ai-qualification.md` (incident summary, next-action recommendation, remediation execution). Stage S04-06 consumes these rows with `policy-input-model.md`. Stage S05-13 collects the negative tests. Stage S06 cites this matrix.
