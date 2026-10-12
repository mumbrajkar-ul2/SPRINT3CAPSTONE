# AI risk register

| Field | Value |
|---|---|
| Stage | S04-09 — AI security and guardrails (Challenge 9), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Nine risks each have a control and a YAML id. The test pack covers each control. The timeout number stays unset. Owner: Team-Force. Label: PROPOSED. |
| Evidence sources | `apps/api/services/ai_gateway.py`; `apps/api/main.py`; `apps/api/services/policy.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `semantic-layer/ai-context-policy.yaml`; `semantic-layer/business-rules.yaml`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/defect-list.md`; `docs/04-secrets/sensitive-field-handling-checklist.md`; `docs/06-policy/ai-action-policy-design.md`; `docs/08-observability/log-schema.md`; `security/threat-model.md`; `data/synthetic/ai_invocations.csv`; `data/synthetic/devices.csv`; `Project_Intent(sections 5.3, Appendix C).md` |
| Assumptions | A true `stale_topology_flag` stays BLOCK, which is the YAML outcome and the running policy. The playbook Half B sentence that says HOLD_FOR_REVIEW for a true flag is recorded as a conflict and is not applied here. A blank or missing flag stays HOLD_FOR_REVIEW. The model call is skipped for both. |
| Unresolved issues | The production timeout number is null. `prompt_template_version` has no YAML id. The hash algorithm for `prompt_hash` has no YAML id. There is no command list and no failmode id for an execute verb inside recommendation text. |
| Residual risks | `gateway_flags_until_s0409` still tells the policy that the prompt is clean, the schema passed, and the call did not time out. A call that reaches `summarize_record` still places `mgmt_ip` and `credential_profile` in the prompt string. This half does not change that code. |

## What this file is

This file lists the ways the live summary call can mislead a person or leak a device field. Each row names the control that stops that path, and the YAML id for that control. Half A writes this list. No Python file changes in this half.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

The playbook locked facts say the prompt is the whole row, `guardrail_status` is `not_enforced`, the role check is none, and the timeout is none. The role-check sentence is older than the current route. **Verified Fact:** `main.py` lines 66 to 70 call `policy.check_summarize` and return HTTP 403 when the access result is deny. The other three locked facts still match the gateway. **Verified Fact:** `ai_gateway.py` lines 4, 7, and 17.

## How to read one row

Take AIR-02. The finding is that the prompt string contains the whole device row. The evidence is `ai_gateway.py` line 7. The impact is that `mgmt_ip` and `credential_profile` are in that string. The control is the allow list plus a stop when a forbidden field would enter the text. The YAML ids are `policy.prompt_fields` and `failmode.forbidden_field_in_prompt`. The test is GR-02 in `guardrail-test-pack.md`.

## Summary

| Id | Finding | Control | YAML id | Test |
|---|---|---|---|---|
| AIR-01 | Instruction text in `hostname` or `vendor` can enter the prompt, because those two fields are on the allow list. | The output must match the schema. The route outcome word is never EXECUTE. The text is not written to a device. | `policy.prompt_fields`; `policy.output_schema`; `rule.ai_output_cannot_execute` | GR-01 |
| AIR-02 | The live prompt contains `mgmt_ip` and `credential_profile`. | Build the prompt from the allow list. If either field would enter the text, stop with BLOCK and do not call the model. | `policy.prompt_fields`; `failmode.forbidden_field_in_prompt`; `rule.forbidden_fields_never_enter_prompt` | GR-02 |
| AIR-03 | A recommendation can be written from a device whose topology flag is true, or from a blank flag. | True flag: BLOCK before the model. Blank or missing flag: HOLD_FOR_REVIEW before the model. | `failmode.stale_topology_true`; `failmode.stale_topology_blank`; `rule.stale_topology_blocks_recommendation`; `field.device.stale_topology_flag` | GR-03, GR-08 |
| AIR-04 | The stub returns a fixed sentence with no schema check. A later worker can treat that JSON as an instruction. | Validate the answer against `policy.output_schema`. A bad answer is discarded. The outcome is HOLD_FOR_REVIEW and `summary` is null. | `policy.output_schema`; `failmode.schema_failure`; `policy.fail_to_person` | GR-04 |
| AIR-05 | The gateway waits 0.01 seconds and has no deadline. | The model call has a timeout. On timeout the outcome is HOLD_FOR_REVIEW and `summary` is null. The number of seconds stays unset. | `failmode.timeout`; `policy.fail_to_person` | GR-05 |
| AIR-06 | The audit row has columns for model provenance and writes null in each of them. | Write `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` on a call that reached the model. Leave them null when the model was not called. | `policy.provenance`; `provenance.model`; `provenance.model_version`; `provenance.prompt_hash`; `provenance.tokens`; `provenance.latency_ms` | GR-11 |
| AIR-07 | The route checks the role. The gateway function does not. The playbook locked fact still says the route check is none. | Keep the route check. A missing header stays denied. A caller with no summarize grant gets HTTP 403. The gateway is not called. | `rule.no_default_role`; `action.summarize`; `provenance.policy_result` | GR-06 |
| AIR-08 | The recommendation sentence can be copied into a change ticket. | The summarize route never returns EXECUTE. No approval id is written by the model. A device change waits for the four gates on `outcome.execute`. | `rule.ai_output_cannot_execute`; `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `outcome.execute` | GR-07, GR-09 |
| AIR-09 | The policy is called with three flags forced to "clean", so it cannot see a dirty prompt, a bad answer, or a timeout. | Delete that placeholder once the gateway computes the three flags from the real call. | `failmode.forbidden_field_in_prompt`; `failmode.schema_failure`; `failmode.timeout` | GR-02, GR-04, GR-05 |

Worked example for the summary table. AIR-02's control is the allow list. `REC-0001` is a real device row and it has both forbidden columns (`devices.csv` line 2). Today `summarize_record` places that whole row in the prompt. After Half B, the prompt text for that call leaves both columns out. If a builder still inserts either value, the outcome is BLOCK and the model does not run.

## AIR-01 — Instruction text in an allowed field

| Field | Value |
|---|---|
| Finding | `hostname` and `vendor` may enter the prompt. A sentence typed into either cell travels with the prompt. |
| Evidence | **Verified Fact.** `policy.prompt_fields` allowed list includes `field.device.hostname` and `field.device.vendor` (`ai-context-policy.yaml` lines 46 and 47). The live template interpolates the whole row (`ai_gateway.py` line 7). `devices.csv` line 2 has hostname `legacy` for `REC-0001`. The cells in this file are status words, not instruction sentences. |
| Impact | The model reads the cell as part of the prompt. The stub does not follow the sentence. It returns one fixed summary (`ai_gateway.py` lines 13 and 14). A later hosted model could follow the sentence. |
| Risk | The allow list is doing what it says. The harm starts if the answer is treated as a command. Likelihood: Unknown. The synthetic hostnames checked in this file are single words. |
| Confidence | High for "the field is allowed". Medium for harm, because the live model is a stub (`policy.model_today`). |
| Control | Schema check on the answer. The route outcome word is never EXECUTE. The sentence is not applied to a device. |
| YAML id | `policy.prompt_fields`; `policy.output_schema`; `rule.ai_output_cannot_execute` |
| Open questions | Open question for S03: there is no failmode id for instruction text inside an allowed field. This design needs that id so a test can name the reason when `hostname` holds a command sentence. |

## AIR-02 — Sensitive fields in the prompt

| Field | Value |
|---|---|
| Finding | Every call that reaches `summarize_record` puts `mgmt_ip` and `credential_profile` in the prompt string. |
| Evidence | **Verified Fact.** `ai_gateway.py` lines 4 and 7. `policy.prompt_fields` forbids both fields (lines 79 to 82). `rule.forbidden_fields_never_enter_prompt` has `enforced_today: false`. Defect F12. Checklist SF-01 in `sensitive-field-handling-checklist.md`. |
| Impact | The management address and the credential-profile label are in the text the model is given. The stub does not send that text to a network (`policy.model_today`). The audit row does not store the two cells (`audit.py` lines 52 to 56). |
| Risk | The leak is present on every call that reaches the gateway. Likelihood of a hosted model using the address later: Unknown. The checklist says who may read the two cells is Unknown. Owner: Team-Force. |
| Confidence | High |
| Control | The prompt is built only from the allowed field ids. If `mgmt_ip`, `credential_profile`, or a credential name from `forbidden_credential_names` would appear in the prompt text, the outcome is BLOCK, `summary` is null, and the model is not called. |
| YAML id | `policy.prompt_fields`; `failmode.forbidden_field_in_prompt`; `rule.forbidden_fields_never_enter_prompt` |
| Open questions | None new. Who may read the two cells on `GET /records/{id}` stays the open item from the checklist. This stage owns the prompt, not that read. |

The running policy cannot see this leak yet. `gateway_flags_until_s0409` sets `forbidden_field_in_prompt` to false (`policy.py` lines 328 to 344). That is AIR-09.

## AIR-03 — Stale topology

| Field | Value |
|---|---|
| Finding | A summary can describe a device whose stored topology flag is true. A blank flag has no owner decision. |
| Evidence | **Verified Fact.** `ai-qualification.md` line 44: `stale_topology_flag` is true on 192 rows, false on 161, blank on 1. `devices.csv` line 4: `DEV-00003` has the flag true. `rule.stale_topology_blocks_recommendation` says no branch reads the flag and `enforced_today` is false. The route does read it now: `decide_summarize` passes `stale_topology_flag_of(record)` (`policy.py` lines 317 to 325 and 360). A true flag adds `failmode.stale_topology_true` and the outcome is BLOCK (`policy.py` lines 197 to 199). |
| Impact | `POST /ai/summarize/DEV-00003` with an allowed role is BLOCK before `summarize_record`, when the policy engine runs. A direct call to `summarize_record` still summarizes that row. |
| Risk | 192 devices are marked stale. A summary of one of them can send a person to the wrong site. Likelihood for a direct gateway call: the function has no flag check, so the summary is returned. Likelihood on the route: the policy already returns BLOCK for true. |
| Confidence | High for the counts and the policy branch. The blank-flag treatment is PROPOSED in the YAML. Owner: Team-Force. |
| Control | True: BLOCK, model not called, `summary` null. Blank or missing key: HOLD_FOR_REVIEW, model not called, `summary` null. |
| YAML id | `failmode.stale_topology_true`; `failmode.stale_topology_blank`; `rule.stale_topology_blocks_recommendation`; `field.device.stale_topology_flag` |
| Open questions | The playbook Half B sentence says a true flag returns HOLD_FOR_REVIEW. The YAML and `policy.py` say BLOCK. This design follows the YAML. Changing that outcome is an owner decision, not a new status word. S04-06 already asked whether a true flag blocks `ai_use.incident_summary`. The running policy applies the block to summarize. This design keeps that. |

`security/threat-model.md` line 7 names `stale_topology` and assigns no control. This row is that control.

## AIR-04 — Unvalidated output

| Field | Value |
|---|---|
| Finding | The gateway returns a fixed summary and the sentence `Review and approve before action` with `guardrail_status` `not_enforced`. Nothing checks the shape. |
| Evidence | **Verified Fact.** `ai_gateway.py` lines 11 to 17. `policy.output_schema` lists the required fields and says a missing field or a wrong type hands the case to a person. `gateway_flags_until_s0409` sets `output_schema_ok` to true (`policy.py` line 342), so the policy treats the stub as valid. |
| Impact | The caller receives a sentence that looks like a next step. Appendix C says that sentence must not become an operational decision. The live body has no `outcome` field, so the caller sees the sentence without a policy outcome. **Verified Fact:** `main.py` lines 82 to 84 return the gateway dict on the RECOMMEND_ONLY path. |
| Risk | A worker can open a change from that JSON. Likelihood: the sentence is the same for every id (`ai-qualification.md`, next-action row). The path is open on every allowed summarize of a fresh, found device. |
| Confidence | High |
| Control | A Pydantic model matches `policy.output_schema`. Malformed JSON, a missing field, or a wrong type is a schema failure. The model answer is discarded. Outcome HOLD_FOR_REVIEW. `summary` is null. The stored text is not a replacement sentence. |
| YAML id | `policy.output_schema`; `failmode.schema_failure`; `policy.fail_to_person` |
| Open questions | Open question for S03: `output_schema_ok` is not a field id. S04-06 already filed this. This design uses the same name as that policy input. |

The schema says the model's `outcome` value may be one of the four outcome ids, and EXECUTE is never set by the model (`ai-context-policy.yaml` lines 117 to 121). A model JSON whose `outcome` is EXECUTE fails that rule and follows the same HOLD path as any other schema failure. The policy's own outcome word is the one the route returns (`ai-action-policy-design.md`, finding AA-06).

## AIR-05 — No timeout

| Field | Value |
|---|---|
| Finding | The gateway has no deadline. It sleeps 0.01 seconds and returns. |
| Evidence | **Verified Fact.** `ai_gateway.py` line 9. `fail_to_person.timeout_seconds` is null (`ai-context-policy.yaml` line 272). The note on that key says this file does not invent the number. `gateway_flags_until_s0409` sets `timeout_hit` to false. |
| Impact | A model that never answers would hold the request. The stub always answers, so the live call does not hang. Stage S04-11 reuses this path as the AI-down drill. |
| Risk | Likelihood of a hang on the stub: the sleep is fixed at 0.01 seconds, so the stub returns. Likelihood after a real model is attached: Unknown. |
| Confidence | High for "no deadline exists". The number of seconds is Unknown. |
| Control | The call runs under a timeout. The production number stays null until Team-Force sets it. Label: PROPOSED. Owner: Team-Force. When the deadline is hit, the outcome is HOLD_FOR_REVIEW, `summary` is null, and the reason is `failmode.timeout`. A test may pass its own short deadline. That test number is not the production default. |
| YAML id | `failmode.timeout`; `policy.fail_to_person` |
| Open questions | Open question for S03: `timeout_hit` is not a field id. S04-06 already filed this. The number of seconds is a value, and the YAML already has the key `timeout_seconds` set to null. This design does not fill that null. |

## AIR-06 — Provenance missing on the audit row

| Field | Value |
|---|---|
| Finding | The response body names the model. The audit row writes null for the provenance columns. |
| Evidence | **Verified Fact.** Response keys are `model`, `summary`, `recommendation`, `token_estimate`, `source_count`, `guardrail_status` (`ai_gateway.py` lines 11 to 17). `model` is `local-sim-v1`. `audit.write_event` sets `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` to null (`audit.py` lines 69 to 74). `provenance.model` is the only provenance field with `present_today: true` on the answer. `provenance.tokens` is present as `token_estimate`, which is a different name, and the note says it is not on the audit row. `data/synthetic/ai_invocations.csv` line 1 has no `prompt_hash`, `model_version`, `latency_ms`, or `policy_version`. Line 2 puts the word `not_enforced` in the `model` column. |
| Impact | A reviewer cannot show which prompt was sent, which version answered, or how long it took. `prompt_hash` is the stand-in for the prompt text (`log-schema.md`). The prompt text stays out of the log. |
| Risk | A disputed summary cannot be tied to the exact prompt. Likelihood: every new audit row from `write_event` has those nulls. |
| Confidence | High |
| Control | On a call that reached the model, write `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms`. The prompt text is not written. On a stop before the model, those five stay null and `outcome` is set. |
| YAML id | `policy.provenance` and the five `provenance.*` ids named in the summary table. `policy_version` and `prompt_template_version` are in the playbook list and are absent from `policy.provenance`. See the open questions. |
| Open questions | Open question for S03: `prompt_template_version` has no id. This design needs it so the audit row can name which prompt wording was used. Open question for S03: the hash algorithm for `prompt_hash` has no id. This design needs the algorithm name so two runs of the same prompt can be compared. Open question for S03: `policy_version` has no id and no value format. S04-06 already filed this. The string in code is the policy bundle's version. A model version is a separate string. |

`log-schema.md` says `model_version` stays null until a separate version exists. The only version string in the repo is `local-sim-v1`, and `provenance.model_version` says that string doubles as the name. **Assumption:** Half B writes `local-sim-v1` in both `model` and `model_version`, and the evidence file says they are the same string.

## AIR-07 — Role check

| Field | Value |
|---|---|
| Finding | The route refuses a caller who fails the access check. The gateway function takes a record and no role. The playbook locked fact says the route check is none. That sentence matches defect F16. The current route checks the role. |
| Evidence | **Verified Fact.** `main.py` lines 61 to 70: a missing `X-User-Role` has default None, `check_summarize` runs, and a deny returns HTTP 403 with an audit row. The record is not loaded on that deny. `ai_gateway.summarize_record` takes `record` only (line 6). `rule.no_default_role` still says the summary route checks no role, and `enforced_today` is false. That YAML sentence is older than `main.py`. `policy_data.json` row TA-06 allows `persona.noc_operator` to summarize a device. `role.clinician` has no persona, so it matches no grant (`policy_data.json` comment on `persona_of`). |
| Impact | Header `clinician`, header `admin`, and a missing header are denied before the model. An allowed caller still receives the unvalidated stub body when the policy outcome is RECOMMEND_ONLY. |
| Risk | A process that imports `summarize_record` skips the role check. Likelihood of that import: the route is the only caller in `main.py`. Other callers are Unknown. |
| Confidence | High for the route. Medium for "no other caller", because this pass did not search every script. |
| Control | The route keeps the S04-06 check. Half B does not add a second role list inside the gateway. The gateway runs only after access allow. The response on deny stays HTTP 403, body `error` `forbidden`, audit action `policy.deny`. |
| YAML id | `rule.no_default_role`; `action.summarize`; `provenance.policy_result` |
| Open questions | None new. The desk job `persona.noc_operator` for the reader of a summary stays PROPOSED. Owner: Team-Force. |

The playbook also asks for a caller who lacks recommend permission. `persona.customer_support` has `action.recommend` on its denied list (`access-semantics.yaml`). That case is GR-06b. The live route checks `action.summarize`, not `action.recommend`.

## AIR-08 — Recommendation used as a change ticket

| Field | Value |
|---|---|
| Finding | The stub recommendation is a sentence in JSON. Nothing in this packet turns it into a device change. A later worker still can. |
| Evidence | **Verified Fact.** Appendix C: recommendations must not silently become operational decisions. `rule.ai_output_cannot_execute`: text from a model is a recommendation, and `enforced_today` is false. `main.py` has no execute route. `ai_use.remediation_execution` says the model stops at the recommendation rows. `outcome.execute` names four gates: policy allow, human approval id, audit row written first, and a reversible validated change. |
| Impact | `POST /ai/summarize/{id}` returns text. It does not push a config. The harm is a person or a script treating the JSON as the approval. |
| Risk | The worked example in `Project_Intent.md` section 3.1, cited by the qualification file, is that path. Likelihood on this route: no code writes a ticket. Likelihood if a worker copies the sentence: the sentence is present on every successful stub response. |
| Confidence | High |
| Control | This route never returns the outcome word EXECUTE. The model does not write `approval_id`. A change waits for the four gates. Half B returns the policy outcome on every path that gets past the role check. |
| YAML id | `rule.ai_output_cannot_execute`; `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `outcome.execute`; `outcome.recommend_only` |
| Open questions | Open question for S03: there is no failmode id and no command list for an execute verb inside the recommendation string. This design needs that list so a test can decide that a sentence is a command. Until the list exists, GR-07 uses the one sentence the playbook names, and the route outcome is HOLD_FOR_REVIEW with `summary` null because `policy.output_schema` says the recommendation is never a command. This file does not define the list. |

## AIR-09 — The policy is shown a clean call

| Field | Value |
|---|---|
| Finding | Before the gateway runs, the route tells the policy that the prompt has no forbidden field, the schema passed, and the call did not time out. |
| Evidence | **Verified Fact.** `policy.py` lines 328 to 344, function `gateway_flags_until_s0409`. The comment says S04-09 replaces it. `decide_summarize` merges those three values into the policy input (lines 363 to 364). |
| Impact | Rows B4, H1, and H2 of the outcome table cannot fire on the live route. A dirty prompt still reaches `summarize_record` when the other rows allow the call. `REC-0001` with role `operator` is that call: the flag is false (`devices.csv` line 2), the id matches, and the placeholder flags are clean, so the outcome can be RECOMMEND_ONLY and the stub body is returned. |
| Risk | The policy looks enforced while the three gateway checks are not. Likelihood: every live summarize uses this function. |
| Confidence | High |
| Control | The gateway computes `forbidden_field_in_prompt`, `output_schema_ok`, and `timeout_hit` from the call it actually made. The route passes those values into `ai_action` and returns that outcome. The placeholder function is retired in Half B. |
| YAML id | `failmode.forbidden_field_in_prompt`; `failmode.schema_failure`; `failmode.timeout` |
| Open questions | None beyond the three already filed for those flag names. |

## Findings index

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| AIR-01 | Allowed fields can carry instruction text. | `policy.prompt_fields` lines 46 and 47. | The model reads the cell. | Unknown until a hosted model exists. | High / Medium | Failmode id for instruction text in an allowed field. |
| AIR-02 | Forbidden device fields are in the live prompt. | `ai_gateway.py` line 7. F12. | Both cells are in the prompt string. | Certain on every gateway call. | High | Viewer of the two cells stays Unknown. |
| AIR-03 | Stale and blank topology flags need a stop before the model. | 192 true, 161 false, 1 blank. `policy.py` lines 197 to 199. | A stale device can be summarized if the gateway is called directly. | 192 rows. | High | Playbook HOLD versus YAML BLOCK for a true flag. |
| AIR-04 | The stub body is not checked against the schema. | `ai_gateway.py` lines 11 to 17. | The sentence is returned with no policy outcome. | Open on every allowed fresh device. | High | `output_schema_ok` has no field id. |
| AIR-05 | There is no deadline. | `ai_gateway.py` line 9. `timeout_seconds: null`. | The stub returns. A later model might not. | Unknown after a real model. | High | The number stays unset. PROPOSED. Owner: Team-Force. |
| AIR-06 | Provenance columns on the audit row are null. | `audit.py` lines 69 to 74. | A reviewer cannot prove the prompt. | Every new row. | High | `prompt_template_version`, hash algorithm, `policy_version`. |
| AIR-07 | The route checks the role. The gateway does not. | `main.py` lines 66 to 70. `ai_gateway.py` line 6. | Denied callers stop. Allowed callers still get the stub. | Direct import skips the check. | High | Desk job for the summary reader stays PROPOSED. |
| AIR-08 | The sentence can be copied into a ticket. | Appendix C. No execute route. | No device change from this route. | The sentence is on every stub success. | High | No command list. |
| AIR-09 | Three policy flags are forced clean. | `policy.py` lines 328 to 344. | The policy cannot see the leak, the schema, or the timeout. | Every live summarize. | High | Same three flag-name questions as S04-06. |

## Status after Half B

Half B ran on 2026-10-11. The table says whether each control now exists and which test shows it. Test output is in `evidence.md`.

| Risk | Control in place | Test (all PASSED) |
|---|---|---|
| AIR-01 | Yes. The schema check holds an answer that repeats the injection. The one command sentence the playbook names is held. Other sentences are not detected. | `test_gr01_instruction_in_hostname_is_data_and_not_execute`; `test_gr01_a_model_that_obeys_the_injection_is_held` |
| AIR-02 | Yes. The prompt uses the YAML allow list. A forbidden name or value stops the call. | `test_gr02_every_device_row_builds_a_clean_prompt`; `test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked` |
| AIR-03 | Yes. A true flag is BLOCK. A blank or missing flag is HOLD_FOR_REVIEW. | `test_gr03_stale_flag_true_is_blocked_before_the_model`; `test_gr08_blank_or_missing_stale_flag_is_held_before_the_model` |
| AIR-04 | Yes. The `ModelAnswer` model checks every answer. | `test_gr04_malformed_model_output_is_held_with_no_summary` |
| AIR-05 | Yes. The default is 10 seconds, PROPOSED, owner Team-Force, set by `AI_MODEL_TIMEOUT_SECONDS`. The YAML slot stays null. | `test_gr05_timeout_is_held_with_no_summary` |
| AIR-06 | Yes. The audit row holds `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` when the model ran. | `test_gr11_audit_row_has_provenance_and_no_prompt_text` |
| AIR-07 | Yes. The route check from S04-06 is unchanged. | `test_gr06_denied_caller_gets_403_and_the_model_is_not_called` |
| AIR-08 | Yes for this route. The response type has no EXECUTE value. | `test_gr07_response_type_and_routes_cannot_express_execute`; `test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row` |
| AIR-09 | Yes. `gateway_flags_until_s0409` is removed. The policy gets the three flags the gateway measured. | `test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text` |

The register above is the Half A record. Where a sentence there says "today" or "live", it describes the code before Half B.

## Lifecycle

This file cites `docs/02-baseline/ai-qualification.md` (incident summary, next-action recommendation, remediation execution), `docs/06-policy/ai-action-policy-design.md` (rows B3, B4, B5, H1, H2, H3, O1, and finding AA-06), `docs/08-observability/log-schema.md` (the five provenance columns), and `docs/04-secrets/sensitive-field-handling-checklist.md` (SF-01). Stage S04-11 reuses the timeout path. Stage S05-13 collects the tests. Stage S07 builds `/ai/recommend` on this gateway. Stage S10 uses this register for defence questions 7 and 8.
