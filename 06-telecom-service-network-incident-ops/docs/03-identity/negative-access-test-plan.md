# Negative access test plan

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half A |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Each case below names role, resource, purpose, scope, and risk with a YAML id. The no-header case keeps the current default `role.operator`. The proposed change is to refuse that call. Owner: Team-Force. |
| Evidence sources | `docs/03-identity/target-access-matrix.md`; `docs/03-identity/policy-input-model.md`; `apps/api/main.py`; `tests/characterization/test_current_behaviour.py`; `docs/02-baseline/defect-list.md`; `semantic-layer/access-semantics.yaml`; `semantic-layer/business-rules.yaml` |
| Assumptions | Half B can change `main.py` only by taking `clinician` out of the list on line 13. Every other live result in this plan stays as it is today. Purpose and scope on a live HTTP call are the target-row values. The live route does not send those two fields. |
| Unresolved issues | The playbook done-test line says `clinician` returns 403. Half B cannot change the status code. The live deny stays HTTP 200 with body `{"error":"forbidden"}` until S04-06. The proposed no-header deny has no role id. See the open question in `policy-input-model.md` finding PI-03. |
| Residual risks | Cases NA-03, NA-04, and NA-05 record a target decision. The live app has no recommend route and no execute route, so those three do not prove a policy engine. S04-06 is the stage that enforces the JSON. |

## What this file is

This file lists the access cases Half B will put in `tests/access/test_negative_access.py`. Each case names the role, the resource, the purpose, the scope, and the risk. The action is named too, because the grants are per action.

Half A writes this plan. It adds no test file and runs no pytest. The before-and-after output belongs in `evidence.md` during Half B.

The choice for a request with no role header is stated in NA-06. The call keeps the current default. It is filled in as `role.operator`. The proposed change is to refuse it. Owner: Team-Force. `rule.no_default_role`.

## What Half B is allowed to change

Half B takes `clinician` out of the list in `apps/api/main.py` line 13. It makes no other change in that file. After that edit, a `clinician` header takes the path on line 17.

That path returns HTTP 200 and the body `{"error":"forbidden"}`. **Verified Fact:** `main.py` line 17. F14. The status code stays 200 because Half B does not edit line 17. Stage S04-06 is the stage whose deny returns 403. `rule.denied_access_is_audited` is stage S04-08. That rule also asks for an audit row. Half B does not add one.

The characterization test `test_clinician_role_is_accepted_on_record_read` locks the allow. Half B replaces it with a test that asserts the forbidden body. The new test's docstring says it replaces that characterization test.

## Cases

### NA-01. noc_operator may read a record

| Field | Id |
|---|---|
| Role | `persona.noc_operator`. The live header is the word `operator`, id `role.operator`. The map is an Inference. |
| Action | `action.read` |
| Resource | `resource.device` |
| Purpose | `purpose.incident_triage` |
| Scope | `scope.all_records` |
| Risk | `risk.read_only` |
| Target row | TA-01. Decision allow. |
| Half B test | `test_noc_operator_mapped_role_may_read_record` |
| What the test calls | `GET /records/REC-0001` with header `X-User-Role: operator`. |
| Result the test asserts | HTTP 200 and `device_id` `REC-0001`. This is K02. Half B does not change it. |

The header `noc_operator` is refused today. F14. The done-test line allows the mapped API role. This case uses that mapped role so the test can pass.

### NA-02. clinician is denied

| Field | Id |
|---|---|
| Role | `role.clinician` |
| Action | `action.read` |
| Resource | `resource.device` |
| Purpose | `purpose.incident_triage` |
| Scope | `scope.all_records` |
| Risk | `risk.read_only` |
| Target row | No TA row. `removed_roles`. Decision deny. |
| Half B test | `test_clinician_role_is_denied_on_record_read` |
| What the test calls | `GET /records/REC-0001` with header `X-User-Role: clinician`. |
| Result the test asserts | HTTP 200 and body `{"error":"forbidden"}`. |

Purpose and scope are the fields of the read this caller is asking for. `role.clinician` has no grant for them. **Assumption:** the test names TA-01's purpose and scope so the five fields are filled with real ids. The deny comes from the role.

Docstring note for the swap. This test replaces `test_clinician_role_is_accepted_on_record_read`, which locked HTTP 200 and `device_id` `REC-0001`. The new test locks the forbidden body.

Worked example. Before Half B, that call returns the `REC-0001` row. After Half B, the same call returns `{"error":"forbidden"}` and the status stays 200. The audit line for a forbidden call stays absent. F14.

### NA-03. ai_agent may recommend

| Field | Id |
|---|---|
| Role | `persona.ai_agent` |
| Action | `action.recommend` |
| Resource | `resource.incident` |
| Purpose | `purpose.ai_assistance` |
| Scope | `scope.assigned_incident` |
| Risk | `risk.recommendation` |
| Target row | TA-33. Decision allow. |
| Half B test | `test_ai_agent_may_recommend` |
| What the test calls | No recommend route exists. The test builds the JSON from the table above and asserts the decision string `allow` for TA-33. It also calls `GET /records/REC-0001` with header `ai_agent` and asserts HTTP 200 and `device_id` `REC-0001` (K02). |

The live summary route is `action.summarize`, and it checks no role. F16. This case does not treat that route as the recommend allow. AI qualification says the recommend outcome is HOLD_FOR_REVIEW and the agency is recommend. The model does not execute.

### NA-04. ai_agent may not execute

| Field | Id |
|---|---|
| Role | `persona.ai_agent` |
| Action | `action.execute` |
| Resource | `resource.device` |
| Purpose | `purpose.ai_assistance` |
| Scope | `scope.assigned_incident` |
| Risk | `risk.live_network_change` |
| Target row | Denied list for `persona.ai_agent` includes `action.execute`. Decision deny. |
| Half B test | `test_ai_agent_may_not_execute` |
| What the test calls | The test builds this JSON and asserts the decision string `deny`. It also asserts the live app's routes do not include an execute path. `main.py` exposes `/health`, `/records/{record_id}`, and `/ai/summarize/{record_id}` only. K08. |

The scope is the one on the agent's own grants. The deny is the action. `risk.live_network_change` is the risk on the execute grants TA-24 and TA-25, which belong to `persona.automation_service`.

### NA-05. automation_service may not execute without an approval id

| Field | Id |
|---|---|
| Role | `persona.automation_service` |
| Action | `action.execute` |
| Resource | `resource.device` |
| Purpose | `purpose.scheduled_automation` |
| Scope | `scope.assigned_incident` |
| Risk | `risk.live_network_change` |
| Approval | `provenance.approval_id` is null. Extra key `approval_id`. |
| Target row | TA-24 matches the six fields. The empty approval id makes the decision deny. Rule `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. |
| Half B test | `test_automation_service_may_not_execute_without_approval_id` |
| What the test calls | The test builds this JSON with `approval_id` null and asserts the decision string `deny`. It asserts the live app has no execute route. It also calls `GET /records/REC-0001` with header `automation_service` and asserts HTTP 200 and body `{"error":"forbidden"}`. |

The forbidden body on the record route is today's allow list. R06. F14. That assertion locks the list. It is a separate fact from the empty approval id. The docstring says both facts.

The same six fields with a stored approval id would be the TA-24 allow. Half B does not add a route that performs it. Operating contract row 9. No execute route in this packet.

### NA-06. no role header keeps the current default

| Field | Id |
|---|---|
| Role | `role.operator`. The server writes this when the header is absent. `status.code.role_header_default.operator`. |
| Action | `action.read` |
| Resource | `resource.device` |
| Purpose | `purpose.incident_triage` |
| Scope | `scope.all_records` |
| Risk | `risk.read_only` |
| Choice | Keep the current default for the test Half B runs. The proposed change is to refuse the call. Owner: Team-Force. PROPOSED. `rule.no_default_role`, whose `enforcement_stage` is S04-03. Half B's edit list does not include the header default. |
| Half B test | `test_missing_role_header_keeps_operator_default` |
| What the test calls | `GET /records/REC-0001` with no `X-User-Role` header. |
| Result the test asserts | HTTP 200 and `device_id` `REC-0001`. F15. The behaviour is unchanged. |

Worked example. A call to `GET /records/REC-0001` with no role header is filled in as `operator`. The route then returns the `REC-0001` device row. The proposed rule refuses that call before any row is loaded. Half B keeps the first behaviour. Team-Force owns the proposed rule. Backlog item PB-04.

Open question for S03: there is no id for a call that sends no role header. This design needs that id so a deny rule can name the role field when the header is absent, without first storing `role.operator`.

## What "pass" means for Half B

| Case | Pass condition after the clinician edit |
|---|---|
| NA-01 | Header `operator` still returns the `REC-0001` row. |
| NA-02 | Header `clinician` returns the forbidden body. Status 200. |
| NA-03 | The JSON for TA-33 is marked allow. Header `ai_agent` still returns the `REC-0001` row. |
| NA-04 | The execute JSON for `persona.ai_agent` is marked deny. The route list has no execute path. |
| NA-05 | The execute JSON with a null approval id is marked deny. Header `automation_service` returns the forbidden body. |
| NA-06 | A call with no role header still returns the `REC-0001` row. |

`admin` and `engineer` stay on the list. K02 stays true for those two headers. Half B does not add a test that removes them.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| NT-01 | Six cases each name role, resource, purpose, scope, and risk with an id from `access-semantics.yaml`. | Verified Fact. NA-01 through NA-06. Rows TA-01, TA-24, TA-33. | Half B can write the tests without inventing a persona or a scope. | NA-03, NA-04, and NA-05 do not exercise a live policy engine. | High | None for the five fields on these six cases. |
| NT-02 | The clinician deny that Half B can prove is the existing forbidden body, with HTTP 200. | Verified Fact. `main.py` line 17. F14. Half B scope: one list edit. | The test will fail if it expects 403. | A client that checks the status code still sees success. R13. | High | Which status a real client expects is Unknown. S04-06 is the 403 change. |
| NT-03 | The no-header case is left as `role.operator`, with a proposed deny and an owner. | Verified Fact. `main.py` line 11. F15. `rule.no_default_role`. Owner Team-Force from operating contract row 10. | Half B stays inside its edit list. The gap stays open on purpose. | A caller with no header can still read the device row, including the two sensitive cells. | High | Open question for S03: there is no id for a call that sends no role header. This design needs that id so a deny rule can name the role field when the header is absent, without first storing `role.operator`. |

## Lifecycle

Stage S05-13 collects these tests into the security suite. Stage S04-06 turns NA-03, NA-04, and NA-05 into policy fixtures and is the stage that returns 403. This plan cites `docs/02-baseline/defect-list.md` F14, F15, and F16, and `docs/02-baseline/ai-qualification.md` on recommend versus execute.
