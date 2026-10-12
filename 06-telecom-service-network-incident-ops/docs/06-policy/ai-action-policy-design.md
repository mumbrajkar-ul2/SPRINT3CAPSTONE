# AI action policy design

| Field | Value |
|---|---|
| Stage | S04-06 — Policy as code (Challenge 6), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The outcome table has 17 rows. Every input combination the design names gets exactly one of the four outcomes. A design check over 73,728 combinations found one combination that reaches EXECUTE, and it has an approval id and an audit row. Twelve terms the YAML lacks are listed as open questions for S03. |
| Evidence sources | `semantic-layer/ai-context-policy.yaml` (`outcomes`, `fail_to_person`, `output_schema`, `provenance`, `ai_uses`); `semantic-layer/business-rules.yaml`; `semantic-layer/access-semantics.yaml`; `docs/02-baseline/ai-qualification.md`; `docs/03-identity/policy-input-model.md`; `docs/03-identity/target-access-matrix.md`; `docs/00-contract/operating-contract.md` rows 2, 8, 9, 10; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `docs/02-baseline/defect-list.md`; `Project_Intent(sections 5.3, Appendix C).md` |
| Assumptions | The server sets every input. A client never sends `approval_id`, `audit_row_written`, or any flag. Rows B7, H4, and the use of `stale_topology_flag` on all three actions are PROPOSED. Owner: Team-Force. The design check is a throwaway script and not a repo test. |
| Unresolved issues | No approval store exists, so nothing can confirm that an approval id names a real yes. The model timeout number is not set. The running policy version string is not set. Whether a true stale flag blocks a summary is not in the YAML. |
| Residual risks | The policy trusts the six flags the server computes. A route that sets `audit_row_written` to true without writing a row defeats row B9. Half B sets that flag inside `policy.py` after `audit.write_event` returns. No execute route exists, so no code reaches EXECUTE today. |

## What this file is

This file designs `ai_action`. It is the policy that looks at one AI call and returns one outcome. The four outcomes are RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, and EXECUTE. They are locked in `Project_Intent(sections 5.3, Appendix C).md` and in `outcome.*` in `ai-context-policy.yaml`.

Half A writes this design. No Rego file or Python file changes in this half.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. PROPOSED items name an owner. The owner is Team-Force (`operating-contract.md` row 10).

## Inputs

The first nine inputs are the ones the playbook names. The next six are inputs the playbook's own sentences need. Without them the design cannot say "forbidden field in the prompt", "approval required", or "audit row written first".

| # | Input | Values | Who sets it | YAML id it maps to |
|---|---|---|---|---|
| 1 | `persona` | A persona id such as `persona.noc_operator`, or an API role id such as `role.operator` | The server, from the role header, using the map in `policy-input-model.md` | `personas`, `api_roles_today` in `access-semantics.yaml` |
| 2 | `action` | `action.summarize`, `action.recommend`, `action.execute` | The route | `actions` in `access-semantics.yaml` |
| 3 | `resource` | A `resource.*` id | The route | `resources` in `access-semantics.yaml` |
| 4 | `risk` | A `risk.*` id | The route | `risks` in `access-semantics.yaml` |
| 5 | `approval_id` | A string, or null. An empty string and a string of spaces count as empty. | The server, from the stored approval record, never from a client field | `provenance.approval_id` |
| 6 | `policy_version` | A string | The server, from the policy bundle it loaded | None. See the open question below. |
| 7 | `stale_topology_flag` | true, false, or null for a blank cell | The server, from the device row | `field.device.stale_topology_flag` |
| 8 | `output_schema_ok` | true, false, or null when the model gave no answer | The gateway | `policy.output_schema`; `failmode.schema_failure` |
| 9 | `timeout_hit` | true or false | The gateway | `failmode.timeout` |
| 10 | `policy_result` | `allow` or `deny` | The server, from the access policy run just before on the same call | `policy_result` in `output_schema`; `provenance.policy_result` |
| 11 | `approval_required` | true or false | The server | `approval_required` in `output_schema` |
| 12 | `audit_row_written` | true or false | The server, after `audit.write_event` returns | `concept.audit_row` |
| 13 | `forbidden_field_in_prompt` | true or false | The prompt builder | `failmode.forbidden_field_in_prompt` |
| 14 | `record_found` | true or false | The record lookup | `failmode.missing_id` |
| 15 | `change_plan_ok` | true or false | The change workflow | Fourth gate in `outcome.execute` |

A key that is missing from the input is invalid. A key set to null is valid only for `approval_id`, `stale_topology_flag`, and `output_schema_ok`.

S04-03 names the caller field `role`. This stage's playbook names it `persona`. Both hold the same ids. **Proposed:** `role` in the access input and `persona` in the `ai_action` input. Owner: Team-Force.

### Open questions for S03

Open question for S03: `policy_version` has no id and no value format. This design needs it so a call made under an old copy of the policy goes to a person.

Open question for S03: `output_schema_ok` is not a field id. This design needs a name for "the model answer matched `policy.output_schema`".

Open question for S03: `timeout_hit` is not a field id. This design needs a name for "the model did not answer in time". The timeout number is `null` in `fail_to_person` and stays unset here.

Open question for S03: `forbidden_field_in_prompt` is not a field id. This design needs a name for "the prompt builder found a forbidden field".

Open question for S03: `record_found` is not a field id. This design needs a name for "a row has the requested id".

Open question for S03: `audit_row_written` is not a field id. This design needs a name for "the audit row for this request exists".

Open question for S03: `change_plan_ok` is not a field id, and "validated" has no meaning in the YAML. `ai_use.remediation_validation` says the expected state is not defined. This design needs a name and a meaning for "the change is reversible and validated".

Open question for S03: `approval_required` exists as an output field. The CSV column with the same name holds status words such as `manual` and `pending`. This design needs a boolean input with a name that does not collide.

Open question for S03: an approval record has no decision field and no approver field. This design needs both so that an id for a rejected approval cannot unlock EXECUTE, and so that the approver can be checked as `persona.network_engineer`.

Open question for S03: a blocked call because the input is invalid or incomplete has no `failmode.*` id. This design needs one for row B1.

Open question for S03: `stale_topology_flag` true is a block condition on `ai_use.next_action_recommendation` and `ai_use.configuration_suggestion` only. This design needs a yes or no on whether it also blocks `ai_use.incident_summary`.

Open question for S03: the `ai_action` input has no `ai_use` id. This design needs it only to pick the reviewer for a held recommendation: `persona.noc_operator` for a next-action sentence, `persona.network_engineer` for a configuration suggestion. The decision itself does not read it.

## Output

The policy returns one object.

```json
{
  "outcome": "HOLD_FOR_REVIEW",
  "reasons": ["failmode.timeout"],
  "policy_version": "0.1.0-proposed"
}
```

`outcome` is one of the four words. `reasons` lists every row that matched in the group that decided the outcome, using the YAML id in the "Reason" column. When a BLOCK row decides, the HOLD rows that also matched are left out. Example: a missing record also leaves `output_schema_ok` null, so row H2 matches, and only row B3 appears in `reasons`. `policy_version` is the version string the policy itself holds. The string `0.1.0-proposed` is PROPOSED. Owner: Team-Force.

The policy ignores any `outcome` word inside the model's own answer. `policy.output_schema` says EXECUTE is never set by the model. **Verified Fact:** `ai-context-policy.yaml`, field `outcome` under `output_schema`.

## Outcome table

The policy checks every row. If any BLOCK row matches, the outcome is BLOCK. If no BLOCK row matches and any HOLD row matches, the outcome is HOLD_FOR_REVIEW. If neither matches, the row for the action decides.

| Row | Condition | Outcome | Reason | Basis |
|---|---|---|---|---|
| B1 | The action is not `action.summarize`, `action.recommend`, or `action.execute`. Or `persona`, `resource`, or `risk` is not in its YAML list. Or the resource does not fit the action: summarize and recommend take `resource.incident` or `resource.device`, and execute takes `resource.device` or `resource.circuit`. Or the risk does not fit the action: `risk.recommendation` for summarize and recommend, `risk.live_network_change` for execute. Or a required key is missing. | BLOCK | None yet. Open question above. | The resources and risks are the ones on the grants in `access-semantics.yaml`. PROPOSED mechanism. |
| B2 | `policy_result` is not `allow`. The caller may not take this action. | BLOCK | `provenance.policy_result` | Playbook: BLOCK when the actor may not recommend. |
| B3 | `record_found` is false. | BLOCK | `failmode.missing_id` | `ai-context-policy.yaml`. Defect F02. |
| B4 | `forbidden_field_in_prompt` is true. | BLOCK | `failmode.forbidden_field_in_prompt`; `rule.forbidden_fields_never_enter_prompt` | `ai-context-policy.yaml`. Playbook. |
| B5 | `stale_topology_flag` is true. | BLOCK | `failmode.stale_topology_true`; `rule.stale_topology_blocks_recommendation` | YAML for recommend. PROPOSED for summarize and execute. |
| B6 | The action is `action.execute` and `persona` is not `persona.automation_service`. | BLOCK | `rule.ai_output_cannot_execute` | `ai_use.remediation_execution` names `persona.automation_service` as the executor. |
| B7 | The action is `action.execute` and `approval_required` is not true. | BLOCK | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | Operating contract row 9: every live change needs an approval id. PROPOSED mechanism. |
| B8 | The action is `action.execute` and `approval_id` is empty. | BLOCK | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | Operating contract row 9. Playbook done test. |
| B9 | The action is `action.execute` and `audit_row_written` is not true. | BLOCK | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `outcome.execute`: an audit row written first. |
| B10 | The action is `action.execute` and `change_plan_ok` is not true. | BLOCK | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `outcome.execute`: a reversible validated change. |
| H1 | `timeout_hit` is true. | HOLD_FOR_REVIEW | `failmode.timeout` | `ai-context-policy.yaml`. Playbook. |
| H2 | `output_schema_ok` is not true. It is false, or null with no timeout. | HOLD_FOR_REVIEW | `failmode.schema_failure` | `ai-context-policy.yaml`. Playbook. |
| H3 | `stale_topology_flag` is null. | HOLD_FOR_REVIEW | `failmode.stale_topology_blank` | `ai-context-policy.yaml`. The YAML marks the treatment PROPOSED. |
| H4 | `policy_version` is not the version the policy holds. | HOLD_FOR_REVIEW | None yet. Open question above. | PROPOSED. Owner: Team-Force. |
| O1 | No BLOCK or HOLD row matched. The action is `action.summarize`. | RECOMMEND_ONLY | `ai_use.incident_summary` | `outcome.recommend_only` |
| O2 | No BLOCK or HOLD row matched. The action is `action.recommend`. | HOLD_FOR_REVIEW | `ai_use.next_action_recommendation`; `ai_use.configuration_suggestion` | `outcome.hold_for_review` |
| O3 | No BLOCK or HOLD row matched. The action is `action.execute`. | EXECUTE | `ai_use.remediation_execution` | `outcome.execute` |

A call with no BLOCK row and no HOLD row matches exactly one of O1, O2, and O3. Row B1 catches every other action. So every input gets one outcome.

No row uses a number. The timeout is a true or false flag that the gateway sets. The policy never compares a duration or a count.

### Why BLOCK and not HOLD_FOR_REVIEW for a missing approval id

HOLD_FOR_REVIEW means a named person must accept or reject the text. An execute call with no approval id is a request to run a change that nobody approved. The right answer is to stop it and give the reason. The approval is written by a person through a separate step. After that step, the same execute call is asked again. The playbook done test allows either BLOCK or HOLD_FOR_REVIEW. This design picks BLOCK. **Proposed.** Owner: Team-Force.

### Why row B7 exists

The playbook says EXECUTE needs "an approval_id when approval_required is true". That wording lets a caller send `approval_required` false and skip the approval. Operating contract row 9 says every live network change needs an approval id. Row B7 closes the gap. An execute call with `approval_required` false is BLOCK. **Verified Fact:** playbook line 31 and `operating-contract.md` row 9.

## EXECUTE conditions

One combination of inputs returns EXECUTE. All of these hold at once.

1. `action` is `action.execute`.
2. `persona` is `persona.automation_service`.
3. `policy_result` is `allow`. The access policy matched TA-24 or TA-25.
4. `resource` is `resource.device` or `resource.circuit`, and `risk` is `risk.live_network_change`.
5. `record_found` is true.
6. `forbidden_field_in_prompt` is false.
7. `stale_topology_flag` is false. A true flag is B5. A blank flag is H3.
8. `approval_required` is true.
9. `approval_id` is not empty.
10. `audit_row_written` is true.
11. `change_plan_ok` is true.
12. `timeout_hit` is false.
13. `output_schema_ok` is true. For an execute call, this flag and `timeout_hit` describe the stored recommendation that the person approved. **Assumption.**
14. `policy_version` is the version the policy holds.

Conditions 8, 9, and 10 are the three the playbook names. Conditions 11 to 14 add the fourth check from the YAML and the stops from the fail modes.

### Design check

I ran a throwaway script over every combination of the inputs the table reads. It is not in the repo and is not the Half B test. The script applies the table above. The domains were: action (4 values), caller is `persona.automation_service` (2), `policy_result` (2), inputs valid (2), `record_found` (2), `forbidden_field_in_prompt` (2), `stale_topology_flag` (3), `timeout_hit` (2), `output_schema_ok` (3), `policy_version` matches or differs (2), `approval_required` (2), `approval_id` empty or set (2), `audit_row_written` (2), `change_plan_ok` (2).

REAL output of that run:

| Outcome | Combinations |
|---|---|
| BLOCK | 72,168 |
| HOLD_FOR_REVIEW | 1,527 |
| RECOMMEND_ONLY | 32 |
| EXECUTE | 1 |
| Total | 73,728 |

The one EXECUTE combination is the 14 conditions above. In that run, 0 combinations reached EXECUTE without an approval id, and 0 reached EXECUTE without an audit row. Half B repeats this as a real test and records its output in `docs/06-policy/evidence.md`.

## Worked combinations

All rows start from a healthy call: `policy_result` `allow`, `record_found` true, `forbidden_field_in_prompt` false, `stale_topology_flag` false, `timeout_hit` false, `output_schema_ok` true, `policy_version` matching. For an execute call the healthy call also has `approval_required` true, `approval_id` set, `audit_row_written` true, and `change_plan_ok` true. The "Change" column says what differs.

| # | Change from the healthy call | Outcome | Rows matched |
|---|---|---|---|
| W1 | `action.summarize`, caller `persona.noc_operator`. | RECOMMEND_ONLY | O1 |
| W2 | `action.recommend`, caller `persona.noc_operator`. | HOLD_FOR_REVIEW | O2 |
| W3 | `action.recommend`, `stale_topology_flag` true. | BLOCK | B5 |
| W4 | `action.recommend`, `stale_topology_flag` null. | HOLD_FOR_REVIEW | H3 |
| W5 | `action.recommend`, `timeout_hit` true, `output_schema_ok` null. | HOLD_FOR_REVIEW | H1, H2 |
| W6 | `action.recommend`, `output_schema_ok` false. | HOLD_FOR_REVIEW | H2 |
| W7 | `action.recommend`, `forbidden_field_in_prompt` true. | BLOCK | B4 |
| W8 | `action.recommend`, caller `persona.customer_support`, `policy_result` `deny`. | BLOCK | B2 |
| W9 | `action.summarize`, `record_found` false, `output_schema_ok` null. This is the `DOES-NOT-EXIST` call from defect F02. | BLOCK | B3 and H2 both match. BLOCK wins, so `reasons` holds B3 only. |
| W10 | `action.execute`, caller `persona.automation_service`, `approval_id` null. This is the playbook done test. | BLOCK | B8 |
| W11 | `action.execute`, caller `persona.ai_agent`, `policy_result` `deny`. | BLOCK | B2, B6 |
| W12 | `action.execute`, `approval_id` set, `audit_row_written` false. | BLOCK | B9 |
| W13 | `action.execute`, `approval_id` set, `approval_required` false. | BLOCK | B7 |
| W14 | `action.execute`, caller `persona.automation_service`, `approval_id` set, `approval_required` true, `audit_row_written` true, `change_plan_ok` true. | EXECUTE | O3 |
| W15 | W14, with `stale_topology_flag` null. | HOLD_FOR_REVIEW | H3 |
| W16 | `action.summarize`, `policy_version` differs. | HOLD_FOR_REVIEW | H4 |
| W17 | `action.write` on an AI call. | BLOCK | B1 |

Rows W1 to W17 are the cases the fixtures in `example-inputs.md` encode. Fixtures AI-01 to AI-09 there follow W14, W10, W1, W2, W5, W3, W11, W7, and W12. Fixture AI-10 follows W13.

## The high-risk decision: an AI remediation recommendation becomes a change

### Allow case, in words

A noc_operator opens an incident and asks for a recommendation on one device. The record exists. The stale flag is false. The prompt holds only allow-listed fields. The model answers in time with a valid answer. The policy returns HOLD_FOR_REVIEW (row O2). No change exists yet.

A person with the desk job `network_engineer` reads the recommendation and writes an approval. The system stores an approval id. The person is the approver on TA-17. The model and the `automation_service` account never write that id.

The change workflow prepares one change for that device. The change is reversible and validated, so `change_plan_ok` is true. The server asks the access policy about `persona.automation_service` executing on `resource.device` for `purpose.scheduled_automation`, scope `scope.assigned_incident`. Row TA-24 matches, and `policy_result` is `allow`. The server writes an audit row that names the actor, the approval id, and the request chain. Then the server asks `ai_action` with `audit_row_written` true. All 14 conditions hold, so the policy returns EXECUTE (row O3). The change runs. A second audit row records the result.

### Deny cases, in words

1. The same workflow, but `approval_id` is empty. Nobody approved the change. The policy returns BLOCK (row B8). The recommendation text cannot fill the id. The `automation_service` account cannot fill it either. Only a person can.
2. `persona.ai_agent` asks for `action.execute`. The model never holds the execute action. The access policy denies it (TA matrix, denied list). The policy returns BLOCK (rows B2 and B6).
3. The approval id exists but the audit row was not written. The policy returns BLOCK (row B9). The server writes the row and asks again.
4. The approval id exists but the stale flag is blank. The policy returns HOLD_FOR_REVIEW (row H3). A person decides what a blank flag means. The YAML says what a blank flag should do is Unknown.

**Today.** No route reaches EXECUTE. No route writes an approval id. **Verified Fact:** `apps/api/main.py` has three routes. `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` says `current_behaviour`: all three gates are absent. The allow case describes the later path. It is a design case and a test case. It is not a live path.

## How today's two AI-related calls would score

| Call today | What the design returns | Why |
|---|---|---|
| `POST /ai/summarize/REC-0001` with no role header | BLOCK | The route takes no role, so `persona` is missing. Row B1. Half B must add a role. Whether a missing role is refused or filled in as `role.operator` is PROPOSED. Owner: Team-Force. `rule.no_default_role`. |
| `POST /ai/summarize/DOES-NOT-EXIST` | BLOCK | `record_found` is false. Row B3. Today the call returns a summary of `REC-0001` (F02). |

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| AA-01 | The playbook wording lets a caller skip the approval by sending `approval_required` false. | Verified Fact. Playbook line 31. `operating-contract.md` row 9. | Row B7 blocks an execute call with `approval_required` false. | If Half B copies the playbook wording, EXECUTE is reachable without an approval id. | High | None. |
| AA-02 | An approval id string does not prove that a person said yes. | Verified Fact. `concept.approval` says an approval is a yes or no. `provenance.approval_id` is a string. No approval store or route exists. | A rejected approval with an id would pass row B8 and B9. | EXECUTE after a rejection. | High | Open question for S03 on the approval decision and approver fields. |
| AA-03 | The playbook lists three EXECUTE conditions. The YAML lists four checks. | Verified Fact. Playbook line 31. `outcome.execute` names a policy allow, a human approval id, an audit row written first, and a reversible validated change. | Row B10 adds the fourth check. | A change that cannot be undone could run. | High | Appendix C says "reversible or validated". The YAML and operating contract row 2 say "reversible validated". This design uses the stricter reading. Inference. |
| AA-04 | The order in the YAML is access allow, approval id, audit row, then change. `ai_action` is the last look before the change. | Verified Fact. `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` statement. | Row B9 is a safety net when a caller asks before writing the row. | A caller that sets the flag without writing a row. | Medium. The flag is set by server code. Assumption. | None. |
| AA-05 | Stale topology blocks recommend in the YAML. The YAML is silent on summarize and execute. | Verified Fact. `block_conditions` on `ai_use.next_action_recommendation` and `ai_use.configuration_suggestion`. None on `ai_use.incident_summary`. | The design applies row B5 to all three actions. | A summary of stale data could mislead a reader. | Medium. PROPOSED. Owner: Team-Force. | Open question for S03 above. |
| AA-06 | The model's answer carries an `outcome` field. A model could write EXECUTE there. | Verified Fact. `output_schema` field `outcome`. | The policy ignores that word and uses its own table. | A gateway that copies the model's word onto the response. | High | None. |
| AA-07 | The repo sets no timeout number. | Verified Fact. `fail_to_person` has `timeout_seconds: null`. | The policy reads `timeout_hit` as true or false. | None for the policy. The gateway owns the number. | High | Stage S04-09 sets the number. |
| AA-08 | Only one of 73,728 input combinations reaches EXECUTE. | Verified Fact for the script output above. The script is not in the repo. | The EXECUTE path is narrow and testable. | The script and the Rego could differ. Half B's test applies the table to the Rego or the Python evaluator. | High for the table. Medium for the Rego until Half B. | None. |
| AA-09 | A held recommendation needs a named reviewer, and the reviewer differs by use. | Verified Fact. `approver` on `ai_use.next_action_recommendation` and `ai_use.configuration_suggestion`. | The policy returns the outcome. The gateway picks the reviewer. | A recommendation held with no reviewer. | Medium | Open question for S03 on `ai_use` above. |

## Lifecycle

This file cites `docs/03-identity/policy-input-model.md` for the access input shape, `docs/03-identity/target-access-matrix.md` for TA-17, TA-24, and TA-25, and `docs/02-baseline/ai-qualification.md` for the pick and the outcome of each AI use. Stage S04-06 Half B writes `policy/opa/ai_action.rego` from the table. Stage S04-09 calls it from the gateway. Stage S05-14 adds the audit fields that rows B9 and the allow case rely on. Stage S09 cites the allow test (W14) and the deny test (W10) as D4 proof.
