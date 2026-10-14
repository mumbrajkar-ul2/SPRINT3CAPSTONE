# Defence answers: ten questions with evidence

| Field | Value |
|---|---|
| Stage | S10. Presentation and defence (`Project_Intent.md` section 3.3). |
| Date / version | 2026-10-14, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | PASS. Each of the ten answers names at least one file or test and names what is still unproven. No answer is "not proven". The S09 gate stays CONDITIONAL PASS, because 41 risk owners are PROPOSED. |
| Evidence sources | `PRODUCTION_EVIDENCE_PACK.md`; `docs/15-readiness/` (`go-no-go-decision.md`, `risk-owner-table.md`, `residual-risk-register.md`, `readiness-checklist.md`, `operating-contract-check.md`, `deferred-work-list.md`); `docs/16-evidence-pack/` (`hash-recheck.md`, `audit-log-record.md`, `path-check.md`); `docs/00-contract/operating-contract.md` v1.4; `docs/demo/demo-script.md`; `docs/demo/evidence.md`; `docs/14-audit/evidence.md`; `docs/11-reliability/idempotency-plan.md`; `docs/11-reliability/degraded-mode-design.md`; `docs/09-ai-guardrails/approval-workflow.md`; `docs/model-comparison/` (`app-comparison.md`, `second-model-run-log.md`, `second-model-load-fix.md`, `yaml-hashes-before.md`, `yaml-hashes-after.md`); `docs/02-baseline/defect-list.md`; `docs/prd/prd.md` v1.9; `../Project_Intent.md` sections 3.3 and 6.3; `../AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf`; `../playbook/STATUS.md`. |
| Assumptions | (1) This file adds no new claim. Every claim comes from a file, a test or a stored run that is named next to it. (2) Four numbers were counted again in S10, and each is marked "rechecked in S10" or "counted in S10": the line count and hash of `logs/audit.log`, the row counts of `risk-owner-table.md` (22 and 41, and 12 of the 22 that rest on an Inference), and the 26 `DW-` rows of `deferred-work-list.md`. (3) A number that is an id or a time stamp, such as `STO-00002`, is a name and carries no label. (4) "The lab demo" means the governed app in `apps/api/` on one machine, with synthetic data, the stand-in model `local-sim-v1`, one server process, and a person who types the role word. |
| Unresolved issues | Seven PRD gaps are open (G-1 to G-4, G-6, G-8, G-9). 41 of 63 open risks have a PROPOSED owner and no written acceptance. The refreshed `evidence/` folder has no commit (`S09-1`). `playbook/STATUS.md` has no row for S05-14 in the log written when the stage ran. The S09 files still say item 11 of `Project_Intent.md` section 6.3 is not ready. They are S09 files and S10 does not edit them. |
| Residual risks | The same team proposes, owns and accepts each risk (`CR-10`). One person reviews every code change (`CR-7`). Every model text, time and token count comes from the stand-in model. The old shared database password text sits in `../transcript/chat_transcript.md` (`S09-5`). This file does not copy it. |

Paths are relative to the project folder (`06-telecom-service-network-incident-ops`) unless they start with `../`.

**Claim labels.** Verified Fact names a file or a test. Inference is a conclusion drawn from facts. Assumption is a stated starting point. Unknown means the packet has no evidence.

**Number labels.** REAL is a count or a measure taken from a run or a file. PRECOMPUTED is a value copied from a stored report. SIMULATED is a value that the stand-in model produces. EDUCATIONAL is a teaching figure and not money.

**How each answer is laid out.** The answer is three to six sentences. The evidence table lists each claim with its label and its file or test. The last part says what is still unproven.

---

## Question 1. What event did you route, and which facts existed at decision time?

**Answer.** The demo routed one alarm storm, `STO-00002`. The storm holds one alarm row, `ALA-00002`, for device `DEV-00002`. The row is flagged `last_seen_before_first_seen`, because its last seen time is earlier than its first seen time. At decision time the operator had three facts: the storm counts (raw 1, deduped 1, flagged 1, all REAL), ten fields of the device row with `stale_topology_flag` set to `false`, and one next-action sentence from the stand-in model `local-sim-v1`. The operator had no incident row, because the join from an alarm to an incident is Unknown. The question put to the person was whether to act on the sentence for `DEV-00002`.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| The case is storm `STO-00002`, device `DEV-00002`, asked by a NOC operator who sends the word `operator`. | Verified Fact | `docs/demo/demo-script.md` section 2 |
| The storm reply gave raw count 1, deduped count 1 and flagged count 1. | Verified Fact (REAL) | `docs/demo/demo-script.md` section 3 step 1; `tests/app/test_storm_route.py::test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` |
| The storm route reads six alarm fields: `storm_batch_id`, `alarm_id`, `device_id`, `dedupe_key`, `first_seen_at`, `last_seen_at`. Each row of its reply shows `alarm_id`, `device_id`, `dedupe_key` and a flag. | Verified Fact | `docs/demo/demo-script.md` section 3 step 1; `docs/prd/prd.md` section 8; `tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids` |
| The device lookup returns ten fields. `mgmt_ip` and `credential_profile` stay out for the role `operator`. Only the role `engineer` gets them back (TA-15). | Verified Fact | `docs/prd/prd.md` section 8 (RQ-05, RQ-06); `docs/demo/demo-script.md` section 3 step 2 |
| The prompt carries the same ten fields. The alarm fields stay out of the prompt. | Verified Fact | `docs/prd/prd.md` section 8; `docs/demo/demo-script.md` section 3 step 3 |
| The join from an alarm to an incident is Unknown, so no incident is opened or merged. | Verified Fact | `docs/prd/prd.md` section 9 ("Incident open, merge or close" row) |
| The data files are synthetic and the app reads them without writing. | Verified Fact | `docs/prd/prd.md` section 8; `docs/15-readiness/operating-contract-check.md` row 6 |

**Still unproven.**
- Real alarm storms. The demo uses synthetic rows (`docs/demo/demo-script.md` assumption 3).
- Whether a storm with more than one alarm behaves the same way in front of an operator. The demo storm has one alarm row.
- How many alarms make a storm. The packet does not set a number (`docs/11-reliability/idempotency-plan.md`, "Key 1 - Alarm", limit).
- `ALA-00002` is one of 166 alarm rows whose last seen time is earlier than the first seen time (`docs/02-baseline/defect-list.md` F08, REAL). Why the data holds so many is Unknown.

---

## Question 2. Which of the four flows did the demo run, and which routes still do not implement that flow?

**Answer.** The demo ran flow 3: topology lookup, then an AI recommendation, then a human decision. Its first step is the alarm-storm deduplication from flow 2. Flow 2 is built in part, because the storm route groups and flags alarms and opens, merges and closes no incident. Flow 1 (customer order to provisioning) did not run. No route implements it, because no route reads `service_orders.csv` or `circuits.csv`. Flow 4 (approved remediation to validation) did not run either. No route implements it, because the app applies no live change, so no result exists to check.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| Flow 3 is the demo flow. The PRD marks it "Yes. This is the demo flow." | Verified Fact | `docs/prd/prd.md` section 3 table, section 4 |
| Flow 2 is "Partly". The storm route dedupes and flags and opens no incident. | Verified Fact | `docs/prd/prd.md` section 3 table |
| Flow 1 and flow 4 are marked "No". | Verified Fact | `docs/prd/prd.md` section 3 table |
| The "Not built" table lists 12 rows: order provisioning, remediation validation, any EXECUTE route, incident open or merge or close, configuration suggestion, capacity forecast, reads of incidents and other files, write routes, a login route, a held-case inbox, a waiver route and batch summary of alarms. Each row has a reason. | Verified Fact (REAL: 12 rows) | `docs/prd/prd.md` section 9 ("Routes this PRD will not implement") |
| The app has 9 routes: `GET /`, `GET /health`, `GET /ready`, `GET /records/{id}`, `GET /alarms/storms/{storm_batch_id}`, `POST /ai/summarize/{id}`, `POST /ai/recommend/{id}`, `POST /approvals/{id}`, `GET /audit/{correlation_id}`. | Verified Fact (REAL) | `apps/api/main.py`; `data/contracts/openapi-fragment.yaml`; `tests/app/test_openapi_fragment.py` |
| No route can reach EXECUTE. | Verified Fact | `policy/tests/test_policy_python.py::test_no_route_can_execute` |
| The operating contract bars a qualify, provision, retry, rollback or fix-check route. | Verified Fact | `docs/00-contract/operating-contract.md` row 2 |

**Still unproven.**
- The "Not built" table is a written list. The two tests above check the route list and EXECUTE only. No test checks that each unbuilt flow has no code.
- What "validated" means for a change is Unknown (`docs/prd/prd.md` section 9, rule for EXECUTE).
- Configuration Assistant and Capacity Intelligence are not built. The names are an Inference from `docs/architecture/known-gaps.md` and `current-state.md` (`docs/prd/prd.md` section 3).

---

## Question 3. What action cannot be undone, and where does a human approve it?

**Answer.** The action that cannot be undone is a live network change: a configuration push, an automated fix, a provisioning change, or the close of an incident that hides a real outage. No route in the app does any of these. The operating contract says a named person with the desk job `network_engineer` must approve such a change by writing a stored approval id. The only human decision the app has is `POST /approvals/{id}`, where the role `operator` answers yes or no to the model's next-action sentence. That route stores the decision and changes no device and no data file. The route that would use a `network_engineer` approval to change a device is not built.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| The irreversible action is a live network change. A named human approves it before the change, and the system stores an approval id. | Verified Fact | `docs/00-contract/operating-contract.md` row 9 (Prohibited); `../Project_Intent.md` section 3.1 row 3 |
| The approver's desk job is `network_engineer`. Mangesh (FDE) confirmed it on 2026-10-10. | Verified Fact | `docs/00-contract/operating-contract.md` row 9 (v1.4) |
| A live change waits for four gates together: a policy allow, a human approval id, an audit row written first, and a reversible validated change. | Verified Fact | `docs/00-contract/operating-contract.md` row 2 and "Approval chain"; `docs/09-ai-guardrails/approval-workflow.md` "What the approval unlocks" |
| Three gates exist after S07. The fourth does not, because the policy input sets `change_plan_ok` to false. | Verified Fact | `docs/prd/prd.md` section 9 ("Rule for EXECUTE") |
| The approvals route stores a yes with a decision, an approver and a server-made id, and the caller cannot choose the approver or the id. | Verified Fact | `tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id`; `tests/app/test_approvals_route.py::test_the_caller_cannot_choose_the_approver_or_the_approval_id` |
| Only the role `operator` may store a decision. Other roles get 403 and a `policy.deny` row. | Verified Fact | `tests/app/test_approvals_route.py::test_other_roles_get_403_and_a_deny_row` |
| The audit row is on disk before the approval is stored. | Verified Fact | `tests/app/test_audit_before_state_change.py::test_the_audit_row_is_on_disk_when_the_approval_is_stored` |
| An approval changes no data file. | Verified Fact | `tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged` |
| EXECUTE is unreachable without an approval id, and no route can reach it. | Verified Fact | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id`; `policy/tests/test_policy_python.py::test_no_route_can_execute` |

**Still unproven.**
- No route lets a `network_engineer` approve a live change. A yes to the next-action sentence is not an approval to change a device (`docs/09-ai-guardrails/approval-workflow.md` finding AW-01).
- The policy checks that an approval id is not blank. It does not look the id up in the approval store. This holds only while no route takes an id from a caller (`docs/demo/evidence.md` section 8; risk `SB-08`, owner PROPOSED).
- The approver is a claim. The role is a word the caller types (`SB-09`, accepted by Mangesh (FDE) for Team-Force in ADR 0003 decision 1).
- If the store fails after the audit row, the row holds an id for an approval that does not exist (`tests/app/test_audit_before_state_change.py::test_audit_row_exists_when_the_approval_write_fails`).

---

## Question 4. What would a retry duplicate, and how did you prove the count?

**Answer.** A retry of `POST /ai/summarize/{id}` costs one more model call and one more audit row, and it creates no business row. A retry of a yes on `POST /approvals/{id}` stores a second approval record with a different id, because the PRD asks for that behaviour. A second pass over the alarm data would add alarms: the 354 alarm rows hold 3 repeated pairs and 1 row with a blank key. The count was proved by feeding all 354 alarm rows to `dedupe.py`, which gave 350 new, 3 repeats and 1 held aside, and 350 + 3 + 1 = 354 (REAL). The live storm route shows the same grouping: `STO-00005` returns raw count 2 and deduped count 1 (REAL). A test sends five identical summary calls and finds five model calls and five audit rows (REAL).

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| A repeat of the summary route duplicates one model call and one audit row. It writes no business row. | Verified Fact (REAL: 5 calls, 5 model calls, 5 rows) | `docs/11-reliability/idempotency-plan.md` ("What a retry duplicates today", probe P4); `tests/reliability/test_drills.py::test_dr3_the_summary_route_has_no_key_so_five_calls_cost_five_model_calls_and_five_rows` |
| The recommend route uses the same gateway, so a repeat there should cost the same. The 300 second answer store that would prevent it is deferred. | Inference | `docs/ADR/0004-defer-rq-31-answer-store.md`; risk `FM-05` (accepted, `docs/15-readiness/risk-owner-table.md` section 2) |
| The alarm key is the pair (`dedupe_key`, `storm_batch_id`). 354 rows give 350 groups, 3 repeats and 1 held aside (`ALA-BAD1`). | Verified Fact (REAL) | `tests/reliability/test_drills.py::test_dr3_all_354_alarm_rows_give_350_new_3_repeats_1_held_aside` |
| The order key is the pair (`order_id`, `retry_count`). 354 rows give 351 new, 2 repeats and 1 held aside (`SER-BAD1`). | Verified Fact (REAL) | `tests/reliability/test_drills.py::test_dr3_all_354_order_rows_give_351_new_2_repeats_1_held_aside` |
| The event key is `event_id`. Two passes over 3000 lines give 3000 new and 3000 repeats. | Verified Fact (REAL) | `tests/reliability/test_drills.py::test_dr3_replaying_the_event_file_twice_gives_3000_new_and_3000_repeats` |
| The storm route returns raw count 2 and deduped count 1 for `STO-00005`, whose rows `ALA-00005` and `ALA-00004` share the key `DED-00005`. | Verified Fact (REAL) | `tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids`; `docs/demo/demo-script.md` section 4.3 |
| A second yes stores a second record with a different approval id. | Verified Fact | `tests/app/test_approvals_route.py::test_a_second_call_stores_a_second_record`; `docs/prd/prd.md` RQ-32 |
| In the browser run the agent clicked "Read storm" twice. The chain then held 2 `record.storm_read` rows. A repeat of a storm read adds one audit row and no alarm. | Verified Fact (REAL: 2 rows) | `docs/demo/evidence.md` sections 2 and 4 |

**Still unproven.**
- The duplicate memory lives in one process and is empty after a restart. A second server process has its own copy (`FM-06`, `ID-05`; owner PROPOSED).
- The event stream has no sequence field. 1992 of 3000 event lines have no usable correlation id (REAL, `FM-02`).
- `retry_count` is a number the caller sends. A caller that always sends 0 defeats the order key (`docs/11-reliability/idempotency-plan.md` finding ID-04).
- Whether `ORD-00004`, which appears twice with different counts, is one order or two attempts is Unknown.
- Whether the repeat of a yes on the approvals route is an accepted risk is Unknown. The PRD states it as the designed behaviour (RQ-32). The risk register has no row that names it.
- No demo run repeated a summarize, recommend or approvals call. The counts for those routes come from tests, and the alarm, order and event counts come from the data files.

---

## Question 5. Rebuild one case: actor, request, data used, model and version, policy result, approval, final action, trace id, and what you still cannot prove.

**Answer.** The case is the main demo case for `STO-00002`. The actor is `noc_operator`, a name the server derives from the word `operator` that the page sends. The case has five calls under one correlation id, which is the trace id of this packet. The stand-in model `local-sim-v1` gave a next-action sentence, the policy outcome was HOLD_FOR_REVIEW, the person said yes, the server made an approval id, and the final action is `none` on every row. The real `logs/audit.log` holds 308 lines after the S09 restore (REAL). The demo run wrote to a temporary log, so the tracked file holds no row of this case.

**Evidence: the rebuilt case.**

| Item | What the packet shows | Label | File or test |
|---|---|---|---|
| Actor | Row `actor` is `noc_operator`, row `role` is `operator`. The page sends the role as the header `X-User-Role`. | Verified Fact. The role is a claim. | `docs/demo/evidence.md` section 4 (audit rows); `docs/demo/demo-script.md` section 2 |
| Request | Five calls with one `X-Correlation-Id`: `GET /alarms/storms/STO-00002`, `GET /records/DEV-00002`, `POST /ai/recommend/DEV-00002`, `POST /approvals/DEV-00002` with the body `{"decision": "yes"}`, and `GET /audit/{case id}` as `admin`. | Verified Fact | `docs/demo/demo-script.md` section 3; `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` |
| Data used | Six alarm fields and ten device fields (Question 1). The row of `record.read` holds `record_id` `DEV-00002`. The prompt hash starts with `7258bfe8f606`. The audit row holds no prompt text. | Verified Fact | `docs/demo/evidence.md` section 4; `docs/prd/prd.md` section 8 |
| Model and version | Model `local-sim-v1`, model version `local-sim-v1`. Tokens 90 (EDUCATIONAL). Latency 23 ms (SIMULATED). | Verified Fact | `docs/demo/evidence.md` section 4, step 3 and the `ai.recommendation` row |
| Policy result | The role `operator` has allow rows for reading alarms (TA-02) and for storing a decision (TA-09). The AI outcome is HOLD_FOR_REVIEW with the reason `ai_use.next_action_recommendation` (policy row O2). The audit row stores the outcome and does not store the reasons or the policy version. | Verified Fact | `docs/demo/demo-script.md` section 3 (policy column); `docs/14-audit/evidence.md` ("cannot_prove" table) |
| Approval | Row `ai.approval` on `resource.ai_invocation`. Decision `yes`. Approver `persona.noc_operator`. Approval id starts with `APR-` (the value is redacted in the evidence file). The audit row is written first and the approval is stored after it. | Verified Fact | `docs/demo/evidence.md` section 4; `tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id` |
| Final action | The key `final_action` is `none` on every row. No route changes a device. | Verified Fact | `docs/demo/evidence.md` section 4 (audit table); `docs/prd/prd.md` section 8 |
| Trace id | The chain id is the string `correlation_id`. The audit row has 17 keys and no separate trace id key. The test uses the id `demo-case-1`. The browser run's id is replaced by `case-1` in the evidence file. | Verified Fact (REAL: 17 keys) | `docs/08-observability/trace-design.md`; `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field`; `tests/app/test_demo_flow.py` |
| Chain on screen | The clean test run returns 4 rows: `record.storm_read`, `record.read`, `ai.recommendation`, `ai.approval`. The browser run returned 5 rows, because the agent clicked "Read storm" twice. The row of the chain read itself (`audit.read`) is written after the read, so the chain does not hold it. | Verified Fact (REAL) | `docs/demo/evidence.md` sections 2 and 4; `tests/app/test_demo_flow.py` |
| Audit log after S09 | `logs/audit.log` holds 308 lines and SHA-256 `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` after the restore. The final evidence run added 6 rows (lines 309 to 314) and the agent restored the saved copy. Rechecked in S10: 308 lines and the same SHA-256. | Verified Fact (REAL) | `docs/16-evidence-pack/audit-log-record.md` |
| Where the case rows are | The demo run used a temporary audit log and a temporary approvals file. The repo files `logs/audit.log` and `logs/approvals.jsonl` hold nothing from it. `logs/approvals.jsonl` is created at the first yes decision, so none exists in the tree. | Verified Fact | `docs/demo/evidence.md` assumption 2; `docs/15-readiness/operating-contract-check.md` section 1 (worked example) |

**What the audit route says it cannot prove about this case.** The browser run listed eight items: `policy_decision`, `final_action`, `record_asked_for`, `policy_reasons_and_version`, `caller_identity`, `case_membership`, `log_integrity` and `rows_before_correlation_id`. After a yes, the list leaves out `approval_id`. (Verified Fact: `docs/demo/evidence.md` section 4, step 5; `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id`.)

**Still unproven.**
- Who the caller was. The role is a typed word, so `actor`, `approver` and `role` are claims (`SB-09`).
- That the case is complete and unchanged. The log is a plain file that anyone with file access can edit (`SB-12`, `RK-08`).
- That the case holds only one caller's rows. The caller chooses the case id, so a second caller can add a row to it (`case_membership`).
- That the approval exists after the audit row. The row can hold an id whose store write failed (`docs/demo/evidence.md` section 8).
- The model version. The name and the version are the same text (`SB-15`), and the model is a stand-in.
- The case in the tracked log. The demo rows live in the evidence file and in the test, and the tracked file does not hold them.
- `playbook/STATUS.md` has no row for S05-14 in the log written when the stage ran. The S05-14 result comes from `docs/14-audit/evidence.md` and not from a STATUS row.

---

## Question 6. Which inherited gap did you leave visible until a spec closed it?

**Answer.** The gap I left visible longest is F01: a request for a missing device id returned the first device row, `REC-0001`, with HTTP 200. The S02 baseline wrote it in the defect list and locked it with a test that passed, so nobody could change it by accident. The PRD (RQ-03) then asked for a 404, and S07 replaced that test with `test_missing_id_returns_404`. The gap F15 followed the same path: a call with no role header used to get the role `operator`, and now gets 403 and a `policy.deny` row. Seven PRD gaps are still open (G-1 to G-4, G-6, G-8, G-9), and ADR 0006 closed G-5 and G-7. The deferred-work list holds 39 items.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| F01 and F15 sit in the Fix list. The Keep list and the Fix list share no row. | Verified Fact | `docs/02-baseline/defect-list.md` (F01, F15, "Rows that are in one list only") |
| The baseline test that locked the old behaviour passed at S02. | Verified Fact | `docs/02-baseline/defect-list.md` F01 evidence (`test_missing_id_returns_first_row` PASSED) |
| S07 swapped the old test for `test_missing_id_returns_404` and changed 7 other tests on purpose. The PRD (O-4) names all eight. | Verified Fact (REAL: 8 tests) | `docs/demo/evidence.md` section 5; `tests/characterization/test_current_behaviour.py::test_missing_id_returns_404` |
| A missing id returns 404 and writes no row. A call with no role header returns 403 and a `policy.deny` row. | Verified Fact | `tests/app/test_records_route.py::test_missing_id_returns_404_and_no_row`; `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` |
| Seven PRD gaps have no owner answer: G-1, G-2, G-3, G-4, G-6, G-8, G-9. This is why S07 is CONDITIONAL PASS. | Verified Fact (REAL: 7) | `docs/demo/evidence.md` section 7 |
| ADR 0006 accepted answers for G-5 and G-7 on 2026-10-13. | Verified Fact | `docs/demo/evidence.md` section 7; `docs/ADR/0006-s07-gaps-g5-g7.md` |
| The deferred-work list holds 39 items: 26 in section 1 and 13 in section 2. | Verified Fact (REAL: 26 + 13 = 39) | `docs/15-readiness/deferred-work-list.md` section 3 |
| The role `clinician` left `main.py`. The shared password left the source file of `legacy/reconcile_legacy.py`. | Verified Fact | `docs/03-identity/evidence.md`; `tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment` |

**Still unproven.**
- None of the seven open gaps has an owner answer. S07 built the smallest choice for six of them and stopped on G-1 for half of the work.
- The old shared password stays in git history (commit `e61ba2e`) and in the chat transcript (`S09-5`).
- The data faults stay in the files, because the data is read-only (contract row 6). One example is the 166 alarm rows with an impossible time order (F08).
- S10 did not recheck the other defects of the Fix list one by one. Their present state is Unknown from this file set.

---

## Question 7. How does a person contest an AI recommendation?

**Answer.** A person contests a recommendation by choosing Reject (no), which sends `POST /approvals/{id}` with the word `no`. The server stores the decision `no` with the approver `persona.noc_operator` and no approval id, and it writes the `ai.approval` audit row first. A no never unlocks the approval check: a test gives the policy a no and every other check true, and the outcome is not EXECUTE. Only the role `operator` may decide, and only for a recommendation that was shown with text under the same case id. The approval record has five keys, and none holds a reason for the no.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| A no is stored as `no` with a null approval id. The audit row also holds a null approval id. | Verified Fact | `tests/app/test_approvals_route.py::test_a_no_is_stored_as_no_with_no_approval_id` |
| A no stays in the audit chain with no approval id. | Verified Fact | `tests/app/test_demo_flow.py::test_a_no_decision_is_in_the_chain_with_no_approval_id`; `docs/demo/demo-script.md` section 4.4 |
| A no never unlocks the approval check. | Verified Fact | `tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check` |
| A decision for a recommendation that was never shown returns 404 and stores nothing. | Verified Fact | `tests/app/test_approvals_route.py::test_decision_without_a_shown_recommendation_returns_404` |
| A bad body returns 422 and stores nothing. | Verified Fact | `tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing` |
| The stored record has five keys: `approval_id`, `decision`, `approver`, `record_id`, `correlation_id`. | Verified Fact | `tests/app/test_approvals_route.py` (`FIVE_KEYS`); `docs/prd/prd.md` RQ-32 |
| The design says the `noc_operator` accepts or rejects the next-action sentence, and a rejection writes no approval id. The design was written before the route existed. S07 built the route. | Verified Fact | `docs/09-ai-guardrails/approval-workflow.md` ("How a person contests a recommendation"); `docs/demo/evidence.md` section 1 |

**Still unproven.**
- The record holds no reason for a no. A reviewer cannot learn why a person rejected a sentence (`docs/prd/prd.md` RQ-32 lists no reason key).
- Nobody reviews a no. A held case has no inbox, so a person must know where to look (`RF-08` and `RK-10`, accepted by Mangesh (FDE) for Team-Force).
- The person is a claimed role (`SB-09`).
- A person contests a summarize answer by leaving the record unchanged. The summarize route has no reject button (`docs/09-ai-guardrails/approval-workflow.md`).
- Contest of a configuration suggestion by a `network_engineer` is not built.

---

## Question 8. What still runs if the AI gateway times out?

**Answer.** `GET /health`, `GET /ready`, `GET /records/{id}` and `GET /alarms/storms/{storm_batch_id}` still run, because none of them calls the model. The recommend route returns HTTP 202 with the outcome HOLD_FOR_REVIEW, no summary and no recommendation text. The audit read still works and shows a `policy.hold` row for the case. A decision on `POST /approvals/{id}` returns 404 and stores nothing, because no sentence was shown. A circuit breaker and a limit on calls in flight cover repeated failures. No fake safe recommendation is stored.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| A timeout returns HOLD_FOR_REVIEW with a null summary and a null recommendation. | Verified Fact | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` |
| In the demo flow, the lookup still returns 200, the decision returns 404 with nothing stored, and the chain ends with `policy.hold`. | Verified Fact | `tests/app/test_demo_flow.py::test_ai_timeout_variant_holds_with_no_summary_and_no_approval_is_possible`; `docs/demo/demo-script.md` section 4.1 |
| The browser run with a 0.001 second deadline gave lookup 200, recommend 202, decision 404, chain 3 rows and health 200. | Verified Fact (REAL) | `docs/demo/evidence.md` section 4 (case-5) |
| The drill proves a timeout holds the case and `/health` stays up. A model error does the same. | Verified Fact | `tests/reliability/test_drills.py::test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up`; `tests/reliability/test_drills.py::test_dr2_a_model_error_is_held_and_health_stays_up` |
| A model error and an open breaker also return HOLD_FOR_REVIEW. | Verified Fact | `tests/app/test_recommend_route.py::test_model_error_and_open_breaker_return_hold_for_review` |
| A breaker and an in-flight limit cover the model call. The values (5 failures, 30 seconds, 10 calls) are PROPOSED. | Verified Fact | `tests/reliability/test_breaker.py`; `.env.example`; `docs/11-reliability/recovery-evidence.md` |
| `/health`, `/records/{id}` and the summarize route follow the same table of what continues and what holds. This design was written at S04-11 Half A, before the recommend route existed. The recommend results come from the S07 tests above. | Verified Fact | `docs/11-reliability/degraded-mode-design.md` ("What continues, for every dependency") |
| `GET /ready` checks `devices.csv`, `alarms.csv`, a writable audit log and a loaded policy. It does not call the model. | Verified Fact | `docs/demo/evidence.md` section 1; `tests/app/test_readiness_route.py` |

**Still unproven.**
- The 10 second timeout is PROPOSED and nobody measured it against a real model (`AIR-05`, accepted by Mangesh (FDE) for Team-Force). The stand-in waits 0.01 seconds, so the demo timeout of 0.001 seconds is a test setting.
- A held case has no inbox. A person sees it only in the 202 body, one audit row and the page (`RF-08`).
- A model error and a timeout give reason ids that differ from the PRD failure table (`docs/model-comparison/app-comparison.md` finding F-4, `Q-4`).
- Behaviour under many callers at once and with two server processes is Unknown. The drills ran with one process (`PRODUCTION_EVIDENCE_PACK.md`, Reliability section).

---

## Question 9. How did the second model use the same semantic layer, and what changed in the second app?

**Answer.** The second model (GPT-5.6 Sol) received the same semantic layer `1.2.1` and PRD v1.9, and neither changed: 36 of 36 hashes match, and S09 checked them again with the same result (REAL). It built `apps/api_model_b/`, and the two apps return identical bodies for 351 device reads and 352 storm reads and give the same answer in all 108 role-and-route cells (REAL). The apps differ in 16 places: 3 are listed PRD gaps (G-4, G-6, G-8) and 13 are unlisted. At first, 78 tests of the second app could not load, and a load fix made them load, but 24 of those tests run a copy of the first app's `dedupe.py` and say nothing about the second model. Test counts: the first app passes 469 with `opa` installed, and the second app passes 378, fails 89 (35 differences a user can see, 54 internal names) and skips 2. The S08 Part 3 verdict is CONDITIONAL PASS: meanings did not drift in outcome words, failure ids, audit keys, role grants and data rows, and did drift in rare inputs and list contents.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| 36 hashes (20 files in `semantic-layer/`, `docs/prd/prd.md` and 15 other files) match before and after S08. | Verified Fact (REAL: 36 of 36) | `docs/model-comparison/yaml-hashes-before.md`; `docs/model-comparison/yaml-hashes-after.md` |
| S09 hashed the same 36 files again and found 0 mismatches. | Verified Fact (REAL: 36 of 36) | `docs/16-evidence-pack/hash-recheck.md` |
| The second model passed 21 of the 22 named tests. The first app passed 22. The failed test is `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id`. | Verified Fact (REAL: 22; 21) | `docs/model-comparison/second-model-run-log.md`; `docs/model-comparison/app-comparison.md` section 3.2 |
| 78 tests of the second app did not load: 40 in `test_command_phrases.py`, 14 in `test_metrics_from_audit.py` and 24 in `test_drills.py`. The load fix made all 469 tests load. | Verified Fact (REAL: 78) | `docs/model-comparison/second-model-load-fix.md` sections 1 to 3 |
| `apps/api_model_b/services/dedupe.py` is a copy of the first app's file. No route of the second app calls it. | Verified Fact (REAL: 24 tests) | `docs/model-comparison/second-model-load-fix.md` section 2, change 3 |
| First app: 469 pass, 0 skip in the final run. In S08 it passed 467 and skipped 2, because `opa` was not installed. | Verified Fact (REAL) | `docs/model-comparison/app-comparison.md` section 3.1; `PRODUCTION_EVIDENCE_PACK.md` (Second-Model Comparison Evidence) |
| Second app: 378 pass, 89 fail, 2 skip, 0 not loaded. 378 + 89 + 2 = 469. | Verified Fact (REAL) | `docs/model-comparison/app-comparison.md` sections 3.1 and 3.3 |
| The 89 failures are 35 differences (D) and 54 internal names (H). | Verified Fact (REAL: 35; 54) | `docs/model-comparison/app-comparison.md` section 3.3 |
| The 16 differences are D-01 to D-16. The listed ones are D-01 (G-4), D-02 (G-6) and D-10 (G-8). | Verified Fact (REAL: 16; 3; 13) | `docs/model-comparison/app-comparison.md` section 5 |
| No status word falls outside the YAML in either app. | Verified Fact (REAL: 0 words) | `docs/model-comparison/app-comparison.md` section 4.1 |
| Verdict: CONDITIONAL PASS. 6 of the 16 differences change which text a caller receives, which reason an audit shows, or whether an audit row survives (D-06, D-08, D-09, D-10, D-11, D-12). | Verified Fact (REAL: 6) | `docs/model-comparison/app-comparison.md` section 7; `../playbook/STATUS.md` row S08 Part 3 |
| The second app keeps 1927 of 2000 audit rows when 8 threads write at once. The first app keeps 2000 of 2000. | Verified Fact (REAL) | `docs/model-comparison/app-comparison.md` finding F-7; `tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row` |

**Still unproven.**
- The second app was not rerun with `opa` installed. Whether its 2 skipped tests pass is Unknown.
- The 24 dedupe tests say nothing about the second model, and no second-model dedupe exists.
- The second model was asked to pass 22 named tests. The other 47 tests that the PRD names were not asked of it, because they patch first-app internals or check first-app page text (`docs/model-comparison/second-model-test-split.md`).
- The tests were written for the first app, so the first app passes by construction. A failure on the second app shows a difference. It does not prove the second app is wrong (`docs/model-comparison/app-comparison.md` assumption 1).
- Thirteen questions, Q-1 to Q-13, wait for an owner answer and a later ADR.
- A hash match proves the bytes are the same. It does not prove the content is right (`docs/16-evidence-pack/hash-recheck.md`).

---

## Question 10. Is the system production-ready? What risk is accepted, and who owns it?

**Answer.** No. The S09 decision is no-go for production, and go for the lab demo and this defence under seven conditions, C1 to C7. 63 risks are open (REAL): 22 have a named acceptor, and 41 have a PROPOSED owner who has not agreed in writing, 38 for Team-Force and 3 for Mangesh (FDE). Team-Force owns the 22 accepted risks, and Mangesh (FDE) accepted them for it, although for 12 rows the acceptance is an Inference from one instruction in ADR 0003. The S09 gate is CONDITIONAL PASS, because 41 owners are PROPOSED. The pack names five biggest risks: the role is a typed word, the model is a stand-in, the audit log is a plain file, the GitHub run ended red on three scans, and the policy only checks that an approval id is not blank.

**Evidence.**

| Claim | Label | File or test |
|---|---|---|
| The decision is no-go for production and go for the lab demo under seven conditions. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` sections 1 and 2 |
| C1: say "stand-in model". C2: say "synthetic data" and "one process". C3: say the role is a typed word. C4: say the GitHub run ended red on lint, dependency scan and static scan. C5: commit and push `evidence/`. C6: Team-Force accepts 38 risks, and Mangesh (FDE) closes 3. C7: decide whether to keep or redact the old password in the transcript, and decide the exception for 3 routes and 4 files. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` section 2 |
| 63 risks are open. 22 are accepted (section 2 of the owner table). 41 have a PROPOSED owner (section 3). 22 + 41 = 63. Rechecked in S10: the owner table holds 22 and 41 rows, and the count check reads 63. | Verified Fact (REAL: 63; 22; 41) | `docs/15-readiness/risk-owner-table.md` sections 2 to 4; `docs/15-readiness/residual-risk-register.md` section 4 |
| Team-Force owns every PROPOSED item. Mangesh (FDE) acts for Team-Force. A business owner outside the team is Unknown. | Verified Fact | `docs/00-contract/operating-contract.md` row 10; `docs/15-readiness/risk-owner-table.md` section 1 |
| Of the 22 accepted rows, 10 name a dated decision or an ADR as the acceptance, and 12 rest on the instruction "proceed with the recommendations for the Risks" in ADR 0003, which the owner table reads as an Inference. Counted in S10. | Verified Fact (REAL: 10; 12) | `docs/15-readiness/risk-owner-table.md` section 2 and assumption 3; `docs/ADR/0003-s06-risk-recommendations.md` |
| The pack names five biggest risks: the typed role (`SB-09`), the stand-in model (`AIR-01`), the plain-file audit log (`SB-12`), the red GitHub run, and the approval id that the policy does not look up (`SB-08`). | Verified Fact | `PRODUCTION_EVIDENCE_PACK.md` (Executive summary, "Biggest risks") |
| Accepted risks include `SB-09` (typed role), `SB-12` (plain-file audit log), `AIR-05` (unmeasured 10 second timeout), `AIR-08` (short command list), `RF-08` (no inbox), `CR-7` (one reviewer) and `CR-10` (the team accepts its own risks). | Verified Fact | `docs/15-readiness/risk-owner-table.md` section 2 |
| The S09 gate is CONDITIONAL PASS. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` section 5 |
| The final run gave 469 tests, 0 skipped, on commit `ec56a34`. Lint (30 findings), the dependency scan (9 advisory ids) and the static scan (40 findings) exit 1. The GitHub run on that commit ended red. | Verified Fact (REAL) | `PRODUCTION_EVIDENCE_PACK.md` (Release Summary); `docs/16-evidence-pack/ci-run-38521594275.txt` |
| 2 of 12 control areas are ready for the lab demo (policy and audit). None is ready for production. | Verified Fact (REAL: 2 of 12) | `docs/15-readiness/readiness-checklist.md` section 1 |
| No change crossed a Prohibited row of the operating contract. | Verified Fact | `docs/15-readiness/operating-contract-check.md` section 1 |
| All 150 paths named in the evidence pack exist. | Verified Fact (REAL: 150) | `docs/16-evidence-pack/path-check.md`; `../playbook/STATUS.md` row S09 |

**Still unproven.**
- Written acceptance of the 41 PROPOSED owners by Team-Force (`C6`).
- Behaviour with real users, a real model and two server processes. Encryption at rest and in transit has no evidence (Unknown).
- An outside check of the business numbers. The team that proposes an item also owns and accepts it (`CR-10`).
- The final tree on GitHub. The refreshed `evidence/` folder has no commit (`S09-1`).
- A full S06R review of PRD v1.9. The last full review ran against v1.8 (`S09-2`).

---

## Answer index and gate check

| Question | Primary evidence | What is still unproven (first item) | Result |
|---|---|---|---|
| 1. Event and facts | `docs/demo/demo-script.md`; `docs/prd/prd.md` section 8 | Real storms | Answered |
| 2. Flows and missing routes | `docs/prd/prd.md` sections 3 and 9 | A test that each unbuilt flow has no code | Answered |
| 3. Irreversible action and approver | `docs/00-contract/operating-contract.md` row 9; `tests/app/test_approvals_route.py` | No `network_engineer` route | Answered |
| 4. Retry count | `docs/11-reliability/idempotency-plan.md`; `tests/reliability/test_drills.py` | Two server processes | Answered |
| 5. Case rebuild | `docs/14-audit/evidence.md`; `docs/demo/evidence.md` section 4; `tests/app/test_demo_flow.py` | Caller identity | Answered |
| 6. Inherited gap | `docs/02-baseline/defect-list.md`; `docs/demo/evidence.md` section 7 | Seven open PRD gaps | Answered |
| 7. Contest | `tests/app/test_approvals_route.py` | No reason stored for a no | Answered |
| 8. AI timeout | `tests/app/test_recommend_route.py`; `docs/11-reliability/degraded-mode-design.md` | Timeout value not measured on a real model | Answered |
| 9. Second model | `docs/model-comparison/app-comparison.md` | Second app with `opa` installed | Answered |
| 10. Readiness | `docs/15-readiness/go-no-go-decision.md`; `docs/15-readiness/risk-owner-table.md` | Acceptance of 41 owners | Answered |

**Gate result: PASS.** All ten answers cite a file or a test, and all ten name what is still unproven. No answer is "not proven".

**Effect on item 11 of `../Project_Intent.md` section 6.3.** The item reads "You can answer the section 3.3 questions". `docs/15-readiness/readiness-checklist.md` section 3 marked it Not ready, because this file did not exist. This PASS closes the item. Eleven of 11 items are now ready. The files `docs/15-readiness/readiness-checklist.md` (section 3, row 11), `PRODUCTION_EVIDENCE_PACK.md` (the table of 11 items) and `docs/15-readiness/deferred-work-list.md` (DW-24) still carry the old words. They are S09 files, and S10 leaves them as they are. The owner updates them if the pack must show 11 of 11.

**What this PASS does not change.** The S09 result stays CONDITIONAL PASS and the production decision stays no-go.

## Lifecycle linkage

This file cites `PRODUCTION_EVIDENCE_PACK.md` and the files named in each question. `docs/defence/slide-outline.md` turns these answers into the walkthrough of D1 to D8. S10 is the last stage.
