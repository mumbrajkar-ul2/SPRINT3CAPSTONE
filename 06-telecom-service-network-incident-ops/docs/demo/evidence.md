# Demo evidence: stage S07

| Field | Value |
|---|---|
| Stage | S07. Application and demo. This file holds the test output, the audit rows of the demo run, the list of changed tests and the PRD gaps. |
| Date / version | 2026-10-13, v1.0. Semantic layer 1.2.0. PRD v1.8. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | **CONDITIONAL PASS.** All four gate conditions hold (section 2). The "PRD gaps" table (section 7) has rows with no owner answer, and the PRD says S07 reports PASS only when every row has an owner answer. |
| Evidence sources | The full test run in section 9 (`pytest tests policy/tests semantic-layer/tests`, 2026-10-13). A browser run of the page against the live app on 2026-10-13 (section 4). `docs/prd/prd.md`, `docs/prd/traceability.md`. `apps/api/`, `tests/app/`, `data/contracts/openapi-fragment.yaml`, `docs/ADR/0005-s07-yaml-additions.md`. |
| Assumptions | (1) The model is the stub `local-sim-v1`. (2) The demo run used a temporary audit log and approvals file, so the repo files `logs/audit.log` and `logs/approvals.jsonl` hold nothing from it. (3) The test run used the Python copy of the policy (`POLICY_ENGINE=python`, set by `tests/conftest.py`). (4) A number that is an id or a time stamp, such as `STO-00002` or `22:35:05`, is a name and not a measure. It carries no label. |
| Unresolved issues | Nine PRD gaps with no owner answer (section 7). The near-miss phrase list is a draft that needs Team-Force review (ADR 0005). |
| Residual risks | Section 8 lists eight limits found while building. The largest: the policy checks only that an approval id is not blank, and the page tests read the page source and do not run its script. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Test output and counts are REAL.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. What S07 built

| Route | What it does | Requirements | Tests |
|---|---|---|---|
| `GET /` | Serves `apps/api/static/index.html`, one page that walks the five demo steps and labels every number. | RQ-62 to RQ-65 | `tests/app/test_page.py` |
| `GET /health` | Unchanged. Calls no model and no policy. | RQ-01 | `tests/test_api_contract.py` |
| `GET /ready` | Checks `devices.csv`, `alarms.csv`, a writable audit log and a loaded policy. Returns 503 when one fails. | RQ-73 | `tests/app/test_readiness_route.py` |
| `GET /records/{id}` | 404 on a missing id. 403 and a `policy.deny` row on no role. Leaves out `mgmt_ip` and `credential_profile` except for `engineer`. Writes `record_id` on its row. | RQ-03, RQ-05, RQ-06, RQ-68 | `tests/app/test_records_route.py` |
| `GET /alarms/storms/{storm_batch_id}` | Raw, deduped and flagged counts, `rows` and `held_aside`. Groups by `dedupe_key` through `apps/api/services/dedupe.py`. Changes no file. | RQ-08 to RQ-15 | `tests/app/test_storm_route.py` |
| `POST /ai/summarize/{id}` | Kept. Now writes `record_id` on its rows. A missing id gives BLOCK with no model call. | RQ-16, RQ-17 | existing tests |
| `POST /ai/recommend/{id}` | New. Policy, prompt allow list, model under timeout and breaker, answer shape, answer content checks, policy again, audit row, reply. HOLD_FOR_REVIEW with the sentence, HOLD_FOR_REVIEW with no text, or BLOCK. Never RECOMMEND_ONLY, never EXECUTE. | RQ-18 to RQ-30, RQ-70, RQ-71 | `tests/app/test_recommend_route.py`, `tests/app/test_command_phrases.py` |
| `POST /approvals/{id}` | New. The only route that stores state. Role check, body check, shown-recommendation check, audit row, then the stored decision. | RQ-32 to RQ-39 | `tests/app/test_approvals_route.py`, `tests/app/test_audit_before_state_change.py` |
| `GET /audit/{correlation_id}` | Unchanged apart from rows with 17 keys. | RQ-42 to RQ-52 | existing tests, `tests/app/test_demo_flow.py` |
| EXECUTE | No route. No path holds the word `execute`. | RQ-57, RQ-58 | `policy/tests/test_policy_python.py::test_no_route_can_execute`, `tests/app/test_openapi_fragment.py` |

Other changes: the audit row has 17 keys (`record_id` is the 16th, `final_action` is the 17th). A correlation id of more than 128 characters gets a new UUID. The approvals file is `logs/approvals.jsonl` (append only). The contract `data/contracts/openapi-fragment.yaml` lists every route.

## 2. Gate check

| Gate condition | Result | Proof |
|---|---|---|
| The demo completes one flow to a human decision. | **PASS.** Steps 1 to 5 ran in a browser. A yes was stored with an approval id. The chain came back with five rows in the browser run (the agent clicked "Read storm" twice) and with four rows in the clean run of the test. | Section 4; `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` |
| The audit-before-state-change test passes. | **PASS.** | `tests/app/test_audit_before_state_change.py` (the PRD names three of its tests: RQ-36, RQ-37 and RQ-56; the file count is in section 3) |
| The AI-timeout variant returns HOLD_FOR_REVIEW with no summary. | **PASS.** HTTP 202, `summary` null, `recommendation` null. The page says a person must review. | Section 4, case-5; `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` |
| Every page number has a label. | **PASS** for the source and for the run. | `tests/app/test_page.py::test_every_number_on_the_page_has_a_label`; section 4 |
| BLOCKED if a route returns a recommendation without a policy outcome. | Not triggered. Every body of `/ai/recommend` and `/ai/summarize` carries `outcome`, `reasons` and `policy_version`. | `tests/ai/test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text`; `tests/app/test_recommend_route.py` |
| BLOCKED if a state change comes before its audit row. | Not triggered. | `tests/app/test_audit_before_state_change.py::test_the_audit_row_is_on_disk_when_the_approval_is_stored` |

## 3. Tests

Full run: **467 passed, 2 skipped** (REAL). The two skips are `test_opa_and_python_agree_on_access` and `test_opa_and_python_agree_on_every_ai_action_combination`. Both need the `opa` program, which is not on this machine. A skipped test counts as not run (PRD section 10, RQ-59). The full output is in section 9.

New tests under `tests/app/`: 136 (REAL). Count of each file:

| File | Tests that passed |
|---|---|
| `tests/app/test_approvals_route.py` | 20 |
| `tests/app/test_audit_before_state_change.py` | 9 |
| `tests/app/test_audit_row_keys.py` | 7 |
| `tests/app/test_command_phrases.py` | 40 |
| `tests/app/test_demo_flow.py` | 5 |
| `tests/app/test_openapi_fragment.py` | 7 |
| `tests/app/test_page.py` | 4 |
| `tests/app/test_readiness_route.py` | 6 |
| `tests/app/test_recommend_route.py` | 20 |
| `tests/app/test_records_route.py` | 7 |
| `tests/app/test_storm_route.py` | 11 |

The tests the PRD names for S07, and their result in the full run (43 of 43 planned tests passed; RQ-31 is deferred):

| Requirement | Test | Result |
|---|---|---|
| RQ-33 | `tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check` | PASSED |
| RQ-39 | `tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged` | PASSED |
| RQ-34 | `tests/app/test_approvals_route.py::test_decision_without_a_shown_recommendation_returns_404` | PASSED |
| RQ-35 | `tests/app/test_approvals_route.py::test_other_roles_get_403_and_a_deny_row` | PASSED |
| RQ-32 | `tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id` | PASSED |
| RQ-36 | `tests/app/test_audit_before_state_change.py::test_audit_row_exists_when_the_approval_write_fails` | PASSED |
| RQ-37 | `tests/app/test_audit_before_state_change.py::test_no_approval_is_stored_when_the_audit_row_cannot_be_written` | PASSED |
| RQ-56 | `tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written` | PASSED (4 cases) |
| RQ-72 | `tests/app/test_audit_row_keys.py::test_app_tests_do_not_write_to_the_real_audit_log` | PASSED |
| RQ-40 | `tests/app/test_audit_row_keys.py::test_every_row_has_final_action_none` | PASSED |
| RQ-41 | `tests/app/test_audit_row_keys.py::test_every_row_has_record_id_as_the_16th_key` | PASSED |
| RQ-69 | `tests/app/test_audit_row_keys.py::test_unknown_role_word_is_not_stored_as_sent` | PASSED |
| RQ-71 | `tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held` | PASSED (22 cases) |
| RQ-30 | `tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text` | PASSED (7 cases) |
| RQ-48 | `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` | PASSED |
| RQ-63 | `tests/app/test_page.py::test_every_number_on_the_page_has_a_label` | PASSED |
| RQ-64 | `tests/app/test_page.py::test_held_case_shows_the_reason_and_no_text` | PASSED |
| RQ-62 | `tests/app/test_page.py::test_page_serves_and_names_every_demo_step` | PASSED |
| RQ-65 | `tests/app/test_page.py::test_page_shows_the_cannot_prove_list_and_the_role_it_sent` | PASSED |
| RQ-73 | `tests/app/test_readiness_route.py::test_readiness_returns_503_when_devices_csv_is_missing` | PASSED |
| RQ-31 | `tests/app/test_recommend_cache.py::test_second_identical_request_within_300_seconds_makes_no_model_call` | not built (RQ-31 deferred, ADR 0004) |
| RQ-22 | `tests/app/test_recommend_route.py::test_blank_stale_flag_is_held_and_the_model_is_not_called` | PASSED |
| RQ-26 | `tests/app/test_recommend_route.py::test_forbidden_value_in_prompt_is_blocked_and_not_logged` | PASSED |
| RQ-70 | `tests/app/test_recommend_route.py::test_forbidden_value_in_the_answer_is_held_with_no_text` | PASSED |
| RQ-18 | `tests/app/test_recommend_route.py::test_healthy_recommend_is_hold_for_review_with_the_sentence` | PASSED |
| RQ-20 | `tests/app/test_recommend_route.py::test_missing_id_is_blocked_and_the_model_is_not_called` | PASSED |
| RQ-24 | `tests/app/test_recommend_route.py::test_model_error_and_open_breaker_return_hold_for_review` | PASSED |
| RQ-19 | `tests/app/test_recommend_route.py::test_recommend_never_returns_execute` | PASSED |
| RQ-28 | `tests/app/test_recommend_route.py::test_roles_without_a_recommend_row_get_403` | PASSED |
| RQ-25 | `tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text` | PASSED (5 cases) |
| RQ-21 | `tests/app/test_recommend_route.py::test_stale_true_is_blocked_and_the_model_is_not_called` | PASSED |
| RQ-23 | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` | PASSED |
| RQ-68 | `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` | PASSED |
| RQ-03 | `tests/app/test_records_route.py::test_missing_id_returns_404_and_no_row` | PASSED |
| RQ-06 | `tests/app/test_records_route.py::test_network_engineer_read_returns_mgmt_ip_and_credential_profile` | PASSED |
| RQ-05 | `tests/app/test_records_route.py::test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile` | PASSED |
| RQ-09 | `tests/app/test_storm_route.py::test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` | PASSED |
| RQ-14 | `tests/app/test_storm_route.py::test_missing_alarms_file_returns_500_and_health_stays_200` | PASSED |
| RQ-11 | `tests/app/test_storm_route.py::test_roles_without_an_alarm_read_row_get_403` | PASSED |
| RQ-12 | `tests/app/test_storm_route.py::test_storm_read_leaves_alarms_csv_unchanged` | PASSED |
| RQ-15 | `tests/app/test_storm_route.py::test_storm_read_writes_one_audit_row` | PASSED |
| RQ-13 | `tests/app/test_storm_route.py::test_storm_response_has_no_size_flag` | PASSED |
| RQ-08 | `tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids` | PASSED |
| RQ-10 | `tests/app/test_storm_route.py::test_unknown_storm_returns_404` | PASSED |

Tests in `tests/app/` write to a temporary audit log and a temporary approvals file (RQ-72, `tests/app/conftest.py`). **Verified Fact.** `logs/approvals.jsonl` does not exist after the full run. `logs/audit.log` grew from 80126 to 82826 bytes during the full run. The growth comes from older tests outside `tests/app/` that write to the real log. RQ-72 covers only `tests/app/`.

## 4. The demo run

**How it ran.** The agent started the app twice with a helper script outside the repo that points the audit log and the approvals file at a temporary folder. The second run set `AI_MODEL_TIMEOUT_SECONDS=0.001`. The agent opened `http://127.0.0.1:8077/` and `http://127.0.0.1:8078/` in a browser, clicked the buttons and read the text of each result. The policy engine was the Python copy. After the run, the agent changed two pieces of page text: the example list under the storm box, and one sentence under the row count of the audit chain. The script of the page did not change. `tests/app/test_page.py` passed after the change.

**Main case, storm `STO-00002`, claimed role `operator` (Verified Fact, from the browser run).**

| Step | Reply on the page |
|---|---|
| 1. Read storm | HTTP status 200 (REAL). Raw count 1 (REAL). Deduped count 1 (REAL). Flagged count 1 (REAL). Alarm ids listed 1 (REAL). Row `ALA-00002`, device `DEV-00002`, key `DED-00002`, flag `last_seen_before_first_seen`. |
| 2. Look up device | HTTP status 200 (REAL). Ten fields. `mgmt_ip` and `credential_profile` left out. `stale_topology_flag` `false`. |
| 3. Recommendation | HTTP status 202 (REAL). `HOLD_FOR_REVIEW`. Sentence "Review and approve before action" (SIMULATED). Summary "Synthetic summary for DEV-00002" (SIMULATED). Reason `ai_use.next_action_recommendation`. Model `local-sim-v1`. Tokens 90 (EDUCATIONAL). Latency 23 ms (SIMULATED). |
| 4. Approve (yes) | HTTP status 200 (REAL). Decision `yes`. Approver `persona.noc_operator`. Approval id `APR-[redacted]`. Device `DEV-00002`. |
| 5. Audit chain, claimed role `admin` | HTTP status 200 (REAL). Rows in this chain 5 (REAL; the agent had clicked "Read storm" twice, so two storm rows). `HOLD_FOR_REVIEW` 1 (REAL). The other three outcomes 0 (REAL). The "cannot prove" list named `policy_decision`, `final_action`, `record_asked_for`, `policy_reasons_and_version`, `caller_identity`, `case_membership`, `log_integrity` and `rows_before_correlation_id`. |

**Variants (Verified Fact, from the browser run).**

| Case | Storm | Result |
|---|---|---|
| case-2 | `STO-00001` | Storm: raw 1, deduped 1, flagged 0 (REAL). Lookup of `DEV-00001`: HTTP 404 (REAL). Recommendation: HTTP 403 (REAL), `BLOCK`, reason `failmode.missing_id`, no text, no model values. Decision: HTTP 404 (REAL). Chain: 2 rows (REAL). |
| case-3 | `STO-00005` | Storm: raw 2, deduped 1, flagged 0 (REAL). Lookup of `DEV-00005`: HTTP 200 (REAL), flag `true`. Recommendation: HTTP 403 (REAL), `BLOCK`, reasons `failmode.stale_topology_true` and `rule.stale_topology_blocks_recommendation`, no text. Decision: HTTP 404 (REAL). Chain: 3 rows (REAL). |
| case-4 | `STO-NOPE` | Storm: HTTP 404 (REAL). The chain read: HTTP 404 (REAL), "Run steps one to four first". |
| case-5 (timeout) | `STO-00002`, run with `AI_MODEL_TIMEOUT_SECONDS=0.001` | Lookup: HTTP 200 (REAL). Recommendation: HTTP 202 (REAL), `HOLD_FOR_REVIEW`, reasons `failmode.schema_failure` and `failmode.timeout`, **no summary and no recommendation**. The page said "A person must review this case. The system shows no summary and no recommendation text." Decision: HTTP 404 (REAL), nothing stored. Chain: 3 rows (REAL), the third is `policy.hold`. Health: HTTP 200 (REAL). |

**Audit rows of the demo run, redacted.** Case ids are replaced by `case-1` to `case-5`. Approval ids are replaced by `APR-[redacted]`. Prompt hashes are cut to 12 characters. The time of day is kept. The full date and time and the case ids are left out. No row holds a prompt text, `mgmt_ip`, `credential_profile` or a secret (Verified Fact: the rows are listed in full below, and `tests/security/test_audit_log_security.py` checks the real log).

| Case | Server run | ts (time of day) | action | role | actor | resource | outcome | record_id | approval_id | model | prompt_hash | tokens | latency_ms | token_estimate_method | final_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| case-1 | main | 22:34:52 | `record.storm_read` | operator | noc_operator | resource.alarm | null | null | null | null | null | null | null | null | none |
| case-1 | main | 22:35:03 | `record.storm_read` | operator | noc_operator | resource.alarm | null | null | null | null | null | null | null | null | none |
| case-1 | main | 22:35:04 | `record.read` | operator | noc_operator | resource.device | null | DEV-00002 | null | null | null | null | null | null | none |
| case-1 | main | 22:35:05 | `ai.recommendation` | operator | noc_operator | resource.device | HOLD_FOR_REVIEW | DEV-00002 | null | local-sim-v1 | 7258bfe8f606... | 90 | 23 | word_count_x2_EDUCATIONAL | none |
| case-1 | main | 22:35:05 | `ai.approval` | operator | noc_operator | resource.ai_invocation | null | DEV-00002 | APR-[redacted] | null | null | null | null | null | none |
| case-1 | main | 22:35:06 | `audit.read` | admin | null | resource.audit_log | null | null | null | null | null | null | null | null | none |
| case-2 | main | 22:35:17 | `record.storm_read` | operator | noc_operator | resource.alarm | null | null | null | null | null | null | null | null | none |
| case-2 | main | 22:35:18 | `policy.deny` | operator | noc_operator | resource.device | BLOCK | DEV-00001 | null | null | null | null | null | null | none |
| case-2 | main | 22:35:20 | `audit.read` | admin | null | resource.audit_log | null | null | null | null | null | null | null | null | none |
| case-3 | main | 22:35:20 | `record.storm_read` | operator | noc_operator | resource.alarm | null | null | null | null | null | null | null | null | none |
| case-3 | main | 22:35:21 | `record.read` | operator | noc_operator | resource.device | null | DEV-00005 | null | null | null | null | null | null | none |
| case-3 | main | 22:35:21 | `policy.deny` | operator | noc_operator | resource.device | BLOCK | DEV-00005 | null | null | null | null | null | null | none |
| case-3 | main | 22:35:23 | `audit.read` | admin | null | resource.audit_log | null | null | null | null | null | null | null | null | none |
| case-4 | main | 22:35:26 | `audit.not_found` | admin | null | resource.audit_log | null | null | null | null | null | null | null | null | none |
| case-5 | timeout | 22:35:42 | `record.storm_read` | operator | noc_operator | resource.alarm | null | null | null | null | null | null | null | null | none |
| case-5 | timeout | 22:35:43 | `record.read` | operator | noc_operator | resource.device | null | DEV-00002 | null | null | null | null | null | null | none |
| case-5 | timeout | 22:35:43 | `policy.hold` | operator | noc_operator | resource.device | HOLD_FOR_REVIEW | DEV-00002 | null | local-sim-v1 | 7258bfe8f606... | 90 | 18 | word_count_x2_EDUCATIONAL | none |
| case-5 | timeout | 22:35:45 | `audit.read` | admin | null | resource.audit_log | null | null | null | null | null | null | null | null | none |

Case-4 has no `record.storm_read` row, because the storm was unknown and the route writes no row for a 404 (gap G-2). Its chain read wrote `audit.not_found`. The `audit.read` rows are the reads of a chain by the claimed role `admin`.

## 5. Tests that S07 changed

The PRD (O-4) names four tests. S07 changed those four and five more that also locked behaviour that RQ-03, RQ-40 and RQ-41 remove. Each change keeps the test name close to the old one and says what it replaced.

| Test | Old behaviour locked | New behaviour locked | In PRD O-4 |
|---|---|---|---|
| `tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row` | HTTP 200 and the first row `REC-0001` for an id that does not exist. | Replaced by `test_missing_id_returns_404` in the same file. HTTP 404, body `{"error": "not_found"}`, loader returns `None`. **This is the swap the playbook asks to note.** | Yes |
| `tests/performance/test_load_once.py::test_missing_id_still_returns_the_first_row` | Loader gives the first row for a missing id. | Replaced by `test_missing_id_returns_nothing`. Loader gives `None`. | Yes |
| `tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default` | HTTP 200 for a call with no role header. | Replaced by `test_missing_role_header_is_refused`. HTTP 403, a `policy.deny` row, role null. | Yes |
| `policy/tests/test_policy_python.py::test_record_route_keeps_missing_header_default_operator` | HTTP 200 for a call with no role header. | Replaced by `test_record_route_refuses_a_missing_header`. HTTP 403 and a `policy.deny` row. | Yes |
| `tests/test_characterization.py::test_legacy_missing_record_behavior_is_characterized` | The loader returns a non-empty dict for a missing id. | Replaced by `test_missing_record_returns_nothing`. | No (gap G-5) |
| `tests/performance/test_load_once.py::test_empty_file_gives_the_error_body` | Loader returns `{"error": "missing"}` on an empty file. | Replaced by `test_empty_file_returns_nothing`. Loader returns `None`. | No (gap G-5) |
| `tests/performance/test_load_once.py::test_only_device_id_is_matched` | A site id or a hostname gives the first row. | Same name. A site id or a hostname gives `None`. A device id still gives its row. | No (gap G-5) |
| `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | Rows have 15 keys. | Same name. Rows have 17 keys, and `final_action` is `none`. The PRD (RQ-50) calls this test "existing" and expects it to pass unchanged. | No (gap G-5) |

The four tests that the PRD names for the 404 and the no-header change now have a second test in `tests/app/` (`test_missing_id_returns_404_and_no_row`, `test_missing_header_returns_403_and_a_deny_row`).

## 6. Semantic layer

| Item | Value |
|---|---|
| Version | 1.2.0 (raised from 1.1.1). `build.py --check` passes. |
| Defined ids | 765 (757 before). |
| Glossary rows | 281 (273 before). |
| Semantic-layer tests | 41 passed. |
| Decision record | `docs/ADR/0005-s07-yaml-additions.md`. |
| Rules turned on (`enforced_today: true`) | `rule.missing_id_not_other_device`, `rule.alarm_last_seen_not_before_first_seen`, `rule.duplicate_dedupe_key_in_storm_is_one_alarm`, `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`, `rule.no_default_role`. Six rules stay `false`. |

## 7. PRD gaps

The PRD (section 15, "How S07 reports a gap") says S07 stops work on a requirement when the PRD, the YAML and the ADRs do not fix a choice. In the rows marked "built" below, S07 built the smallest choice so that the flow runs. Each one is a few lines of code. The owner answer column is empty until the owner fills it.

| Gap | Requirement id | What the PRD lacks | Sources that disagree | What S07 did | Owner answer |
|---|---|---|---|---|---|
| G-1 | RQ-69 | The word to store for a role header that is not in the known list. The PRD calls it an Open question for S03. | None disagree. `docs/prd/prd.md` line 412 (RQ-69) and line 587 (Open question) both say it is open. | **Stopped on this half.** An unknown role word, or a very long one, is stored as the caller sent it. Built only the half the PRD fixes: a correlation id of more than 128 characters gets a new UUID. The test `test_unknown_role_word_is_not_stored_as_sent` covers that half. | |
| G-2 | RQ-03, RQ-10, RQ-32, RQ-34, RQ-73 | Whether a 404 (missing device, unknown storm, no shown recommendation), a 422, a call of `GET /` or a call of `GET /ready` writes an audit row. RQ-45 says it only for the audit route. `rule.denied_access_is_audited` covers denies only. | None disagree. `docs/prd/prd.md` lines 285, 301, 341, 343 and 416 are silent. | **Built:** these calls write no row. A refused role still writes `policy.deny`. | |
| G-3 | RQ-15, RQ-41 | The value of `record_id` on a storm read and on an audit read, and where the storm id is recorded. RQ-41 says only that a read of one device writes the device id. | None disagree. `docs/prd/prd.md` lines 306 and 350 are silent. | **Built:** `record_id` is null on a storm read and an audit read. The audit chain does not say which storm was read. | |
| G-4 | RQ-73 | The status words of the `/ready` body. The PRD calls it an Open question for S03. | None disagree. `docs/prd/prd.md` line 416 and line 591. | **Built:** body `status` is `ok` or `Degraded` (the ids `status.code.health.ok` and `status.code.runbook_level.degraded` already exist), and `checks` holds four true or false values. | |
| G-5 | O-4 (and RQ-50) | The list of tests to change is incomplete. Four tests are named. Four more existing tests lock behaviour that RQ-03 and RQ-40 and RQ-41 remove (section 5). RQ-50 calls `test_every_audit_row_has_every_required_field` "existing" and expects it to pass. | `docs/prd/prd.md` line 421 (four tests) against lines 368 (RQ-50) and 285 (RQ-03). | **Changed** the four named tests and the four others (section 5). | |
| G-6 | RQ-32, RQ-37 | The body of the 422 reply, the body of a 500 when the approval cannot be stored, and what to do with extra keys in the approvals body. RQ-32 says the body has one key. | None disagree. `docs/prd/prd.md` lines 341 and 346 are silent. | **Built:** 422 body `{"detail": "decision must be the word yes or the word no"}`. 500 body `{"error": "approval not stored"}` (PROPOSED wording; owner Team-Force). An extra key is ignored. The server never reads an approver or an approval id from the body. | |
| G-7 | RQ-63 (section 8) | Section 8 says the page shows the share of audit rows with every key filled and the share of rows whose `prompt_hash` was seen before. No route in section 9 returns them. The script `docs/12-finops/metrics_from_audit.py` computes the second one over the whole log. The formula of `metric.audit_completeness` names `policy_result`, which no audit row stores. Section 8 also says the outcome counts come from the whole log, and the audit route returns one case. | `docs/prd/prd.md` lines 224 and 225 against section 9 (lines 240 to 250) and `semantic-layer/metrics.yaml` lines 86 to 109. | **Stopped on these two numbers.** The page shows neither. The row count and the calls per outcome cover the rows of the case id the page sent, and the page says so. A new route is outside the PRD (playbook "Exclude"). | |
| G-8 | RQ-30, RQ-70, RQ-71 | How a phrase or a forbidden value is matched in the model text: whole words or any part, with or without capitals. The device values of `mgmt_ip` and `credential_profile` are plain words such as `alpha`. | None disagree. `docs/prd/prd.md` lines 330, 413 and 414 are silent. | **Built:** whole words, any capitals, any white space between words. A harmless sentence that holds such a plain word is held for review. This is the safe side. The near-miss list is a draft (ADR 0005). | |
| G-9 | RQ-62 | The PRD says nothing about `apps/web/src/app/api.service.ts`. It sends no `X-User-Role` header, so after RQ-68 every call of it gets 403. | None disagree. `docs/prd/prd.md` has no mention of `apps/web`. | **Left unchanged.** The playbook excludes wiring the Angular scaffold. The served page is the demo. | |

## 8. Limits found while building

| Limit | Label | Where it shows |
|---|---|---|
| The policy treats any non-blank text as an approval id. It does not look the id up in `logs/approvals.jsonl`. A route that took an approval id from a caller would let any text through. No route does (RQ-38), and the reply of a no carries null. | **Verified Fact** | `tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check` |
| The audit row of a yes holds the approval id before the approval is stored. If the store then fails, the row holds an id for an approval that does not exist. The PRD asks for this order (RQ-36). The chain cannot prove that a stored approval exists. | **Verified Fact** | `tests/app/test_audit_before_state_change.py::test_audit_row_exists_when_the_approval_write_fails` |
| The approvals route reads the whole audit log for each call, to look for the `ai.recommendation` row. The cost grows with the log. | **Inference** (from the code in `apps/api/services/audit_query.py`) | `recommendation_was_shown` |
| The caller chooses the case id. A second caller can write a recommendation row under another caller's case id, and then a decision under it. | **Verified Fact** (it is the `case_membership` item of the "cannot prove" list) | section 4, step 5 |
| The role is a word the caller types. `actor`, `approver` and `role` are claims. | **Verified Fact** | `caller_identity` item |
| The page tests read the page source. They do not run its script. The browser run in section 4 is the only run of the script, and a person must repeat it after a change to the page. | **Verified Fact** | `tests/app/test_page.py` |
| Older tests outside `tests/app/` append rows to the real `logs/audit.log` (2700 bytes in one run). | **Verified Fact** | section 3 |
| The stub model never produces command text, a forbidden value or an `EXECUTE` answer by itself. The tests make it do so with a stand-in. A real model is Unknown. | **Verified Fact** | `tests/app/conftest.py::FakeModel` |

## 9. Full pytest output

Command, from the project folder: `.\.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -v -p no:cacheprovider -W ignore::DeprecationWarning --no-header`.

```text
﻿========================================================================================= test session starts =========================================================================================
collecting ... collected 469 items

tests/access/test_negative_access.py::test_noc_operator_mapped_role_may_read_record PASSED                                                                                                       [  0%]
tests/access/test_negative_access.py::test_clinician_role_is_denied_on_record_read PASSED                                                                                                        [  0%]
tests/access/test_negative_access.py::test_ai_agent_may_recommend PASSED                                                                                                                         [  0%]
tests/access/test_negative_access.py::test_ai_agent_may_not_execute PASSED                                                                                                                       [  0%]
tests/access/test_negative_access.py::test_automation_service_may_not_execute_without_approval_id PASSED                                                                                         [  1%]
tests/access/test_negative_access.py::test_missing_role_header_is_refused PASSED                                                                                                                 [  1%]
tests/ai/test_guardrails.py::test_gr01_instruction_in_hostname_is_data_and_not_execute PASSED                                                                                                    [  1%]
tests/ai/test_guardrails.py::test_gr01_stub_model_with_injected_hostname_passes_the_schema PASSED                                                                                                [  1%]
tests/ai/test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held[recommendation-is-the-command] PASSED                                                                            [  1%]
tests/ai/test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held[summary-is-the-command] PASSED                                                                                   [  2%]
tests/ai/test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held[model-sets-execute] PASSED                                                                                       [  2%]
tests/ai/test_guardrails.py::test_gr02_prompt_has_only_allowed_fields PASSED                                                                                                                     [  2%]
tests/ai/test_guardrails.py::test_gr02_every_device_row_builds_a_clean_prompt PASSED                                                                                                             [  2%]
tests/ai/test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked PASSED                                                                                                   [  2%]
tests/ai/test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked[mgmt_ip] PASSED                                                                                       [  3%]
tests/ai/test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked[show credential_profile now] PASSED                                                                   [  3%]
tests/ai/test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked[AI_GATEWAY_KEY] PASSED                                                                                [  3%]
tests/ai/test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked[x\nmgmt_ip: 1.2.3.4] PASSED                                                                           [  3%]
tests/ai/test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked[SHARED_DB_PASSWORD is set] PASSED                                                                     [  4%]
tests/ai/test_guardrails.py::test_gr02_newline_in_a_value_stays_on_one_line PASSED                                                                                                               [  4%]
tests/ai/test_guardrails.py::test_gr02_allow_list_in_code_matches_the_yaml PASSED                                                                                                                [  4%]
tests/ai/test_guardrails.py::test_gr03_stale_flag_true_is_blocked_before_the_model PASSED                                                                                                        [  4%]
tests/ai/test_guardrails.py::test_gr03_a_direct_gateway_call_is_stopped_too PASSED                                                                                                               [  4%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[not-json] PASSED                                                                                           [  5%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[empty] PASSED                                                                                              [  5%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[json-list] PASSED                                                                                          [  5%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[missing-fields] PASSED                                                                                     [  5%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[extra-key] PASSED                                                                                          [  5%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[wrong-type] PASSED                                                                                         [  6%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[bool-is-not-an-int] PASSED                                                                                 [  6%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[blank-summary] PASSED                                                                                      [  6%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[answer-about-another-record] PASSED                                                                        [  6%]
tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[unknown-outcome] PASSED                                                                                    [  7%]
tests/ai/test_guardrails.py::test_gr04_a_model_that_raises_is_held PASSED                                                                                                                        [  7%]
tests/ai/test_guardrails.py::test_gr05_timeout_is_held_with_no_summary PASSED                                                                                                                    [  7%]
tests/ai/test_guardrails.py::test_gr05_timeout_argument_on_the_gateway PASSED                                                                                                                    [  7%]
tests/ai/test_guardrails.py::test_gr05_default_timeout_is_proposed_and_comes_from_the_environment PASSED                                                                                         [  7%]
tests/ai/test_guardrails.py::test_gr05_yaml_timeout_slot_stays_null_in_this_stage PASSED                                                                                                         [  8%]
tests/ai/test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called[headers0] PASSED                                                                                       [  8%]
tests/ai/test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called[headers1] PASSED                                                                                       [  8%]
tests/ai/test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called[headers2] PASSED                                                                                       [  8%]
tests/ai/test_guardrails.py::test_gr06_caller_without_recommend_permission_is_blocked PASSED                                                                                                     [  8%]
tests/ai/test_guardrails.py::test_gr07_execute_sentence_with_outcome_execute_is_held PASSED                                                                                                      [  9%]
tests/ai/test_guardrails.py::test_gr07_route_returns_block_if_the_policy_ever_said_execute PASSED                                                                                                [  9%]
tests/ai/test_guardrails.py::test_gr07_response_type_and_routes_cannot_express_execute PASSED                                                                                                    [  9%]
tests/ai/test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model[blank] PASSED                                                                                        [  9%]
tests/ai/test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model[spaces] PASSED                                                                                       [ 10%]
tests/ai/test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model[missing] PASSED                                                                                      [ 10%]
tests/ai/test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model[unknown-word] PASSED                                                                                 [ 10%]
tests/ai/test_guardrails.py::test_gr08_the_blank_cell_in_the_data_file_is_held PASSED                                                                                                            [ 10%]
tests/ai/test_guardrails.py::test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row PASSED                                                                                        [ 10%]
tests/ai/test_guardrails.py::test_gr10_success_body_has_the_policy_outcome_and_no_not_enforced PASSED                                                                                            [ 11%]
tests/ai/test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text PASSED                                                                                          [ 11%]
tests/ai/test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text PASSED                                                                                                        [ 11%]
tests/ai/test_guardrails.py::test_gr11_same_prompt_gives_the_same_hash PASSED                                                                                                                    [ 11%]
tests/ai/test_guardrails.py::test_response_model_has_every_field_in_the_yaml_output_schema PASSED                                                                                                [ 11%]
tests/ai/test_guardrails.py::test_model_answer_fields_are_a_subset_of_the_yaml_schema_with_the_same_types PASSED                                                                                 [ 12%]
tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id PASSED                                                                                         [ 12%]
tests/app/test_approvals_route.py::test_the_caller_cannot_choose_the_approver_or_the_approval_id PASSED                                                                                          [ 12%]
tests/app/test_approvals_route.py::test_a_no_is_stored_as_no_with_no_approval_id PASSED                                                                                                          [ 12%]
tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check PASSED                                                                                                             [ 13%]
tests/app/test_approvals_route.py::test_a_second_call_stores_a_second_record PASSED                                                                                                              [ 13%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[None] PASSED                                                                                                   [ 13%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body1] PASSED                                                                                                  [ 13%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body2] PASSED                                                                                                  [ 13%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body3] PASSED                                                                                                  [ 14%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body4] PASSED                                                                                                  [ 14%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body5] PASSED                                                                                                  [ 14%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[body6] PASSED                                                                                                  [ 14%]
tests/app/test_approvals_route.py::test_a_bad_body_returns_422_and_stores_nothing[yes] PASSED                                                                                                    [ 14%]
tests/app/test_approvals_route.py::test_an_unreadable_body_returns_422 PASSED                                                                                                                    [ 15%]
tests/app/test_approvals_route.py::test_the_role_check_runs_before_the_body_check PASSED                                                                                                         [ 15%]
tests/app/test_approvals_route.py::test_decision_without_a_shown_recommendation_returns_404 PASSED                                                                                               [ 15%]
tests/app/test_approvals_route.py::test_a_call_with_no_correlation_id_gets_404 PASSED                                                                                                            [ 15%]
tests/app/test_approvals_route.py::test_other_roles_get_403_and_a_deny_row PASSED                                                                                                                [ 15%]
tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged PASSED                                                                                                      [ 16%]
tests/app/test_approvals_route.py::test_the_approval_store_is_not_under_data PASSED                                                                                                              [ 16%]
tests/app/test_audit_before_state_change.py::test_the_audit_row_is_on_disk_when_the_approval_is_stored PASSED                                                                                    [ 16%]
tests/app/test_audit_before_state_change.py::test_audit_row_exists_when_the_approval_write_fails PASSED                                                                                          [ 16%]
tests/app/test_audit_before_state_change.py::test_no_approval_is_stored_when_the_audit_row_cannot_be_written PASSED                                                                              [ 17%]
tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written[get-/records/DEV-00002-headers0-DEV-00002] PASSED                     [ 17%]
tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written[get-/alarms/storms/STO-00005-headers1-ALA-00005] PASSED               [ 17%]
tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written[post-/ai/summarize/DEV-00002-headers2-Synthetic summary] PASSED       [ 17%]
tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written[post-/ai/recommend/DEV-00002-headers3-Review and approve before action] PASSED [ 17%]
tests/app/test_audit_before_state_change.py::test_the_audit_route_returns_500_when_its_own_row_cannot_be_written PASSED                                                                          [ 18%]
tests/app/test_audit_before_state_change.py::test_a_denied_call_also_returns_500_when_the_deny_row_cannot_be_written PASSED                                                                      [ 18%]
tests/app/test_audit_row_keys.py::test_every_row_has_record_id_as_the_16th_key PASSED                                                                                                            [ 18%]
tests/app/test_audit_row_keys.py::test_every_row_has_final_action_none PASSED                                                                                                                    [ 18%]
tests/app/test_audit_row_keys.py::test_unknown_role_word_is_not_stored_as_sent PASSED                                                                                                            [ 18%]
tests/app/test_audit_row_keys.py::test_a_correlation_id_of_128_characters_is_kept PASSED                                                                                                         [ 19%]
tests/app/test_audit_row_keys.py::test_every_route_answers_with_the_correlation_id_header PASSED                                                                                                 [ 19%]
tests/app/test_audit_row_keys.py::test_app_tests_do_not_write_to_the_real_audit_log PASSED                                                                                                       [ 19%]
tests/app/test_audit_row_keys.py::test_the_engineer_role_is_stored_as_the_word_sent_and_its_persona PASSED                                                                                       [ 19%]
tests/app/test_command_phrases.py::test_the_start_list_is_the_seven_phrases_of_decision_d_08 PASSED                                                                                              [ 20%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[reboot] PASSED                                                                                                   [ 20%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[restart] PASSED                                                                                                  [ 20%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[shut down] PASSED                                                                                                [ 20%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[delete] PASSED                                                                                                   [ 20%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[clear config] PASSED                                                                                             [ 21%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[push config] PASSED                                                                                              [ 21%]
tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text[apply] PASSED                                                                                                    [ 21%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[reboot] PASSED                                                                                     [ 21%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[restart] PASSED                                                                                    [ 21%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[shut down] PASSED                                                                                  [ 22%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[delete] PASSED                                                                                     [ 22%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[clear config] PASSED                                                                               [ 22%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[push config] PASSED                                                                                [ 22%]
tests/app/test_command_phrases.py::test_a_listed_phrase_in_capitals_or_in_the_summary_is_held[apply] PASSED                                                                                      [ 23%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[reboots] PASSED                                                                                                               [ 23%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[rebooting] PASSED                                                                                                             [ 23%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[rebooted] PASSED                                                                                                              [ 23%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[restarts] PASSED                                                                                                              [ 23%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[restarting] PASSED                                                                                                            [ 24%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[restarted] PASSED                                                                                                             [ 24%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[shutdown] PASSED                                                                                                              [ 24%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[shut-down] PASSED                                                                                                             [ 24%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[shuts down] PASSED                                                                                                            [ 24%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[shutting down] PASSED                                                                                                         [ 25%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[deletes] PASSED                                                                                                               [ 25%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[deleting] PASSED                                                                                                              [ 25%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[deleted] PASSED                                                                                                               [ 25%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[clear the config] PASSED                                                                                                      [ 26%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[clearing config] PASSED                                                                                                       [ 26%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[clears config] PASSED                                                                                                         [ 26%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[push the config] PASSED                                                                                                       [ 26%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[pushing config] PASSED                                                                                                        [ 26%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[pushes config] PASSED                                                                                                         [ 27%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[applies] PASSED                                                                                                               [ 27%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[applying] PASSED                                                                                                              [ 27%]
tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held[applied] PASSED                                                                                                               [ 27%]
tests/app/test_command_phrases.py::test_the_near_miss_list_is_not_empty_and_shares_no_entry_with_the_start_list PASSED                                                                           [ 27%]
tests/app/test_command_phrases.py::test_a_phrase_inside_a_longer_word_is_not_held PASSED                                                                                                         [ 28%]
tests/app/test_command_phrases.py::test_a_phrase_that_is_not_on_either_list_gets_through PASSED                                                                                                  [ 28%]
tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id PASSED                                                                                                               [ 28%]
tests/app/test_demo_flow.py::test_a_no_decision_is_in_the_chain_with_no_approval_id PASSED                                                                                                       [ 28%]
tests/app/test_demo_flow.py::test_ai_timeout_variant_holds_with_no_summary_and_no_approval_is_possible PASSED                                                                                    [ 28%]
tests/app/test_demo_flow.py::test_a_device_with_no_row_is_listed_and_then_refused PASSED                                                                                                         [ 29%]
tests/app/test_demo_flow.py::test_a_stale_device_is_blocked_and_the_chain_says_so PASSED                                                                                                         [ 29%]
tests/app/test_openapi_fragment.py::test_the_fragment_lists_every_route_of_the_app_and_no_other PASSED                                                                                           [ 29%]
tests/app/test_openapi_fragment.py::test_no_path_is_named_execute PASSED                                                                                                                         [ 29%]
tests/app/test_openapi_fragment.py::test_the_audit_row_schema_has_the_same_17_keys_in_the_same_order_as_the_code PASSED                                                                          [ 30%]
tests/app/test_openapi_fragment.py::test_the_model_routes_name_no_execute_outcome PASSED                                                                                                         [ 30%]
tests/app/test_openapi_fragment.py::test_the_ai_response_schema_matches_the_body_model_in_the_code PASSED                                                                                        [ 30%]
tests/app/test_openapi_fragment.py::test_the_approval_request_allows_only_the_decision_key PASSED                                                                                                [ 30%]
tests/app/test_openapi_fragment.py::test_every_ref_points_to_a_part_that_exists PASSED                                                                                                           [ 30%]
tests/app/test_page.py::test_page_serves_and_names_every_demo_step PASSED                                                                                                                        [ 31%]
tests/app/test_page.py::test_every_number_on_the_page_has_a_label PASSED                                                                                                                         [ 31%]
tests/app/test_page.py::test_held_case_shows_the_reason_and_no_text PASSED                                                                                                                       [ 31%]
tests/app/test_page.py::test_page_shows_the_cannot_prove_list_and_the_role_it_sent PASSED                                                                                                        [ 31%]
tests/app/test_readiness_route.py::test_readiness_is_200_when_all_four_checks_pass PASSED                                                                                                        [ 31%]
tests/app/test_readiness_route.py::test_readiness_returns_503_when_devices_csv_is_missing PASSED                                                                                                 [ 32%]
tests/app/test_readiness_route.py::test_readiness_returns_503_when_alarms_csv_is_missing PASSED                                                                                                  [ 32%]
tests/app/test_readiness_route.py::test_readiness_returns_503_when_the_audit_log_cannot_be_written PASSED                                                                                        [ 32%]
tests/app/test_readiness_route.py::test_readiness_returns_503_when_the_policy_is_not_loaded PASSED                                                                                               [ 32%]
tests/app/test_readiness_route.py::test_when_the_policy_engine_fails_readiness_is_503_and_every_role_route_is_403 PASSED                                                                         [ 33%]
tests/app/test_recommend_route.py::test_healthy_recommend_is_hold_for_review_with_the_sentence PASSED                                                                                            [ 33%]
tests/app/test_recommend_route.py::test_recommend_never_returns_execute PASSED                                                                                                                   [ 33%]
tests/app/test_recommend_route.py::test_recommend_has_no_recommend_only_outcome PASSED                                                                                                           [ 33%]
tests/app/test_recommend_route.py::test_missing_id_is_blocked_and_the_model_is_not_called PASSED                                                                                                 [ 33%]
tests/app/test_recommend_route.py::test_stale_true_is_blocked_and_the_model_is_not_called PASSED                                                                                                 [ 34%]
tests/app/test_recommend_route.py::test_blank_stale_flag_is_held_and_the_model_is_not_called PASSED                                                                                              [ 34%]
tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary PASSED                                                                                                   [ 34%]
tests/app/test_recommend_route.py::test_model_error_and_open_breaker_return_hold_for_review PASSED                                                                                               [ 34%]
tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text[this is not json] PASSED                                                                             [ 34%]
tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text[{"record_id": "DEV-00002", "summary": "x"}] PASSED                                                   [ 35%]
tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text[{"record_id": "DEV-00002", "summary": "", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1}] PASSED [ 35%]
tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text[{"record_id": "DEV-00002", "summary": "x", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1, "extra": 1}] PASSED [ 35%]
tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text[{"record_id": "DEV-OTHER", "summary": "x", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1}] PASSED [ 35%]
tests/app/test_recommend_route.py::test_forbidden_value_in_prompt_is_blocked_and_not_logged PASSED                                                                                               [ 36%]
tests/app/test_recommend_route.py::test_forbidden_value_in_the_answer_is_held_with_no_text PASSED                                                                                                [ 36%]
tests/app/test_recommend_route.py::test_a_forbidden_field_name_in_the_answer_is_held_with_no_text PASSED                                                                                         [ 36%]
tests/app/test_recommend_route.py::test_roles_without_a_recommend_row_get_403 PASSED                                                                                                             [ 36%]
tests/app/test_recommend_route.py::test_roles_with_a_recommend_row_reach_the_model[headers0] PASSED                                                                                              [ 36%]
tests/app/test_recommend_route.py::test_roles_with_a_recommend_row_reach_the_model[headers1] PASSED                                                                                              [ 37%]
tests/app/test_recommend_route.py::test_roles_with_a_recommend_row_reach_the_model[headers2] PASSED                                                                                              [ 37%]
tests/app/test_records_route.py::test_missing_id_returns_404_and_no_row PASSED                                                                                                                   [ 37%]
tests/app/test_records_route.py::test_an_id_that_is_only_in_alarms_csv_returns_404 PASSED                                                                                                        [ 37%]
tests/app/test_records_route.py::test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile PASSED                                                                                         [ 37%]
tests/app/test_records_route.py::test_network_engineer_read_returns_mgmt_ip_and_credential_profile PASSED                                                                                        [ 38%]
tests/app/test_records_route.py::test_admin_read_does_not_return_the_sensitive_fields PASSED                                                                                                     [ 38%]
tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row PASSED                                                                                                           [ 38%]
tests/app/test_records_route.py::test_a_blank_header_is_treated_as_no_role PASSED                                                                                                                [ 38%]
tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids PASSED                                                                                                   [ 39%]
tests/app/test_storm_route.py::test_flagged_alarm_is_listed_and_is_not_an_incident_candidate PASSED                                                                                              [ 39%]
tests/app/test_storm_route.py::test_a_row_with_a_blank_dedupe_key_goes_to_held_aside PASSED                                                                                                      [ 39%]
tests/app/test_storm_route.py::test_unknown_storm_returns_404 PASSED                                                                                                                             [ 39%]
tests/app/test_storm_route.py::test_roles_without_an_alarm_read_row_get_403 PASSED                                                                                                               [ 39%]
tests/app/test_storm_route.py::test_network_engineer_may_read_a_storm PASSED                                                                                                                     [ 40%]
tests/app/test_storm_route.py::test_storm_read_leaves_alarms_csv_unchanged PASSED                                                                                                                [ 40%]
tests/app/test_storm_route.py::test_storm_response_has_no_size_flag PASSED                                                                                                                       [ 40%]
tests/app/test_storm_route.py::test_missing_alarms_file_returns_500_and_health_stays_200 PASSED                                                                                                  [ 40%]
tests/app/test_storm_route.py::test_storm_read_writes_one_audit_row PASSED                                                                                                                       [ 40%]
tests/app/test_storm_route.py::test_the_alarm_file_has_the_columns_the_service_reads PASSED                                                                                                      [ 41%]
tests/audit/test_audit_rebuild.py::test_the_chain_comes_back_in_time_order PASSED                                                                                                                [ 41%]
tests/audit/test_audit_rebuild.py::test_a_row_written_out_of_order_still_comes_back_in_time_order PASSED                                                                                         [ 41%]
tests/audit/test_audit_rebuild.py::test_two_cases_do_not_mix PASSED                                                                                                                              [ 41%]
tests/audit/test_audit_rebuild.py::test_lines_with_no_correlation_id_are_never_returned_and_are_counted PASSED                                                                                   [ 42%]
tests/audit/test_audit_rebuild.py::test_an_unknown_id_gives_404_and_writes_its_own_row PASSED                                                                                                    [ 42%]
tests/audit/test_audit_rebuild.py::test_a_missing_log_file_gives_404_not_an_error PASSED                                                                                                         [ 42%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[operator] PASSED                                                                              [ 42%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[engineer] PASSED                                                                              [ 42%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[ai_agent] PASSED                                                                              [ 43%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[unknown-word] PASSED                                                                          [ 43%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[admin-in-capitals] PASSED                                                                     [ 43%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row[no-header] PASSED                                                                             [ 43%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[operator] PASSED                                                                         [ 43%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[engineer] PASSED                                                                         [ 44%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[ai_agent] PASSED                                                                         [ 44%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[unknown-word] PASSED                                                                     [ 44%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[admin-in-capitals] PASSED                                                                [ 44%]
tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not[no-header] PASSED                                                                        [ 44%]
tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_cannot_learn_an_id_from_the_too_long_check PASSED                                                                            [ 45%]
tests/audit/test_audit_rebuild.py::test_the_log_is_unchanged_except_for_the_routes_own_row PASSED                                                                                                [ 45%]
tests/audit/test_audit_rebuild.py::test_a_second_read_shows_the_first_reads_own_row_when_it_reused_the_id PASSED                                                                                 [ 45%]
tests/audit/test_audit_rebuild.py::test_the_real_log_is_not_touched_by_these_tests PASSED                                                                                                        [ 45%]
tests/audit/test_audit_rebuild.py::test_the_query_module_never_opens_the_log_for_writing PASSED                                                                                                  [ 46%]
tests/audit/test_audit_rebuild.py::test_the_response_holds_no_forbidden_field_or_credential_name PASSED                                                                                          [ 46%]
tests/audit/test_audit_rebuild.py::test_a_forbidden_name_stored_in_a_row_is_replaced_in_the_response_only PASSED                                                                                 [ 46%]
tests/audit/test_audit_rebuild.py::test_an_id_that_is_a_forbidden_name_is_not_echoed PASSED                                                                                                      [ 46%]
tests/audit/test_audit_rebuild.py::test_an_id_of_129_characters_is_refused_and_not_looked_up PASSED                                                                                              [ 46%]
tests/audit/test_audit_rebuild.py::test_an_id_of_exactly_128_characters_is_looked_up PASSED                                                                                                      [ 47%]
tests/audit/test_audit_rebuild.py::test_the_limit_is_128 PASSED                                                                                                                                  [ 47%]
tests/audit/test_audit_rebuild.py::test_cannot_prove_names_approval_id_and_log_integrity PASSED                                                                                                  [ 47%]
tests/audit/test_audit_rebuild.py::test_cannot_prove_follows_the_rows_for_a_null_field PASSED                                                                                                    [ 47%]
tests/audit/test_audit_rebuild.py::test_cannot_prove_lists_approval_id_when_a_row_holds_an_approval PASSED                                                                                       [ 47%]
tests/characterization/test_current_behaviour.py::test_missing_id_returns_404 PASSED                                                                                                             [ 48%]
tests/characterization/test_current_behaviour.py::test_clinician_role_is_denied_on_record_read PASSED                                                                                            [ 48%]
tests/characterization/test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header PASSED                                                                                   [ 48%]
tests/characterization/test_current_behaviour.py::test_etl_counts_blank_fields_and_keeps_its_old_count_meaning PASSED                                                                            [ 48%]
tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment PASSED                                                                                      [ 49%]
tests/ci/test_evidence_contract.py::test_both_scripts_name_every_output_file PASSED                                                                                                              [ 49%]
tests/ci/test_evidence_contract.py::test_both_scripts_run_every_stage PASSED                                                                                                                     [ 49%]
tests/ci/test_evidence_contract.py::test_checklist_lists_every_output_file PASSED                                                                                                                [ 49%]
tests/ci/test_evidence_contract.py::test_makefile_has_an_evidence_target PASSED                                                                                                                  [ 49%]
tests/ci/test_evidence_contract.py::test_dev_requirements_pin_every_tool PASSED                                                                                                                  [ 50%]
tests/ci/test_evidence_contract.py::test_workflow_calls_every_stage_when_it_exists PASSED                                                                                                        [ 50%]
tests/ci/test_skip_guard.py::test_a_clean_run_passes PASSED                                                                                                                                      [ 50%]
tests/ci/test_skip_guard.py::test_a_skipped_test_fails_and_is_named PASSED                                                                                                                       [ 50%]
tests/ci/test_skip_guard.py::test_an_empty_run_fails PASSED                                                                                                                                      [ 50%]
tests/ci/test_skip_guard.py::test_a_missing_file_fails PASSED                                                                                                                                    [ 51%]
tests/ci/test_skip_guard.py::test_main_returns_the_exit_code PASSED                                                                                                                              [ 51%]
tests/ci/test_skip_guard.py::test_both_scripts_call_the_guard_in_the_security_stage[evidence.sh] PASSED                                                                                          [ 51%]
tests/ci/test_skip_guard.py::test_both_scripts_call_the_guard_in_the_security_stage[evidence.ps1] PASSED                                                                                         [ 51%]
tests/ci/test_skip_guard.py::test_makefile_has_a_security_target_that_runs_the_security_stage PASSED                                                                                             [ 52%]
tests/finops/test_metrics_from_audit.py::test_the_token_method_word_is_the_one_the_playbook_names PASSED                                                                                         [ 52%]
tests/finops/test_metrics_from_audit.py::test_a_model_call_row_carries_the_method_and_a_held_row_does_not PASSED                                                                                 [ 52%]
tests/finops/test_metrics_from_audit.py::test_method_is_dropped_when_tokens_is_null PASSED                                                                                                       [ 52%]
tests/finops/test_metrics_from_audit.py::test_held_rows_are_counted_apart_and_do_not_lower_the_mean PASSED                                                                                       [ 52%]
tests/finops/test_metrics_from_audit.py::test_a_row_with_no_tokens_that_is_not_held_is_its_own_kind PASSED                                                                                       [ 53%]
tests/finops/test_metrics_from_audit.py::test_cost_per_chain_uses_the_rate_and_groups_by_correlation_id PASSED                                                                                   [ 53%]
tests/finops/test_metrics_from_audit.py::test_the_rate_comes_from_settings_and_a_bad_value_gives_the_default PASSED                                                                              [ 53%]
tests/finops/test_metrics_from_audit.py::test_latency_percentiles_and_outcome_split PASSED                                                                                                       [ 53%]
tests/finops/test_metrics_from_audit.py::test_outcome_counts_name_all_four_words_and_unknown_words_are_kept_apart PASSED                                                                         [ 53%]
tests/finops/test_metrics_from_audit.py::test_the_two_metrics_with_no_audit_source_are_named_as_gaps PASSED                                                                                      [ 54%]
tests/finops/test_metrics_from_audit.py::test_an_empty_log_gives_unknown_and_not_zero PASSED                                                                                                     [ 54%]
tests/finops/test_metrics_from_audit.py::test_every_printed_metric_line_has_a_label PASSED                                                                                                       [ 54%]
tests/finops/test_metrics_from_audit.py::test_json_output_parses PASSED                                                                                                                          [ 54%]
tests/finops/test_metrics_from_audit.py::test_repeat_prompt_calls_are_counted_from_prompt_hash PASSED                                                                                            [ 55%]
tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field PASSED                                                                                                   [ 55%]
tests/observability/test_audit_schema.py::test_request_with_header_keeps_the_id PASSED                                                                                                           [ 55%]
tests/observability/test_audit_schema.py::test_request_without_header_gets_a_uuid PASSED                                                                                                         [ 55%]
tests/performance/test_engine_lookup_once.py::test_many_access_decisions_search_the_path_once PASSED                                                                                             [ 55%]
tests/performance/test_engine_lookup_once.py::test_many_ai_decisions_search_the_path_once PASSED                                                                                                 [ 56%]
tests/performance/test_engine_lookup_once.py::test_the_setting_is_still_read_on_every_call PASSED                                                                                                [ 56%]
tests/performance/test_engine_lookup_once.py::test_a_program_found_on_the_path_chooses_opa PASSED                                                                                                [ 56%]
tests/performance/test_engine_lookup_once.py::test_reset_searches_again PASSED                                                                                                                   [ 56%]
tests/performance/test_engine_lookup_once.py::test_a_cached_program_that_is_gone_fails_closed PASSED                                                                                             [ 56%]
tests/performance/test_load_once.py::test_file_is_read_once_across_many_calls PASSED                                                                                                             [ 57%]
tests/performance/test_load_once.py::test_real_file_is_read_once_across_many_calls PASSED                                                                                                        [ 57%]
tests/performance/test_load_once.py::test_reset_makes_the_next_call_read_again PASSED                                                                                                            [ 57%]
tests/performance/test_load_once.py::test_eight_threads_on_the_first_call_read_once PASSED                                                                                                       [ 57%]
tests/performance/test_load_once.py::test_routes_read_the_file_once PASSED                                                                                                                       [ 57%]
tests/performance/test_load_once.py::test_result_is_a_copy PASSED                                                                                                                                [ 58%]
tests/performance/test_load_once.py::test_repeated_id_returns_the_first_row PASSED                                                                                                               [ 58%]
tests/performance/test_load_once.py::test_missing_id_returns_nothing PASSED                                                                                                                      [ 58%]
tests/performance/test_load_once.py::test_empty_file_returns_nothing PASSED                                                                                                                      [ 58%]
tests/performance/test_load_once.py::test_only_device_id_is_matched PASSED                                                                                                                       [ 59%]
tests/performance/test_load_once.py::test_every_device_id_in_the_real_file_finds_its_first_row PASSED                                                                                            [ 59%]
tests/performance/test_load_once.py::test_a_missing_file_raises_and_is_not_cached PASSED                                                                                                         [ 59%]
tests/reliability/test_breaker.py::test_it_opens_after_the_threshold_of_failures_in_a_row PASSED                                                                                                 [ 59%]
tests/reliability/test_breaker.py::test_a_success_resets_the_count PASSED                                                                                                                        [ 59%]
tests/reliability/test_breaker.py::test_a_refused_answer_is_neutral_it_neither_counts_nor_resets PASSED                                                                                          [ 60%]
tests/reliability/test_breaker.py::test_it_half_opens_after_the_open_time_and_lets_one_test_call_through PASSED                                                                                  [ 60%]
tests/reliability/test_breaker.py::test_a_failed_test_call_opens_it_again_for_the_full_time PASSED                                                                                               [ 60%]
tests/reliability/test_breaker.py::test_a_neutral_test_call_frees_the_probe_slot_and_stays_half_open PASSED                                                                                      [ 60%]
tests/reliability/test_breaker.py::test_the_in_flight_limit_refuses_without_waiting_and_frees_on_finish PASSED                                                                                   [ 60%]
tests/reliability/test_breaker.py::test_a_ticket_reports_once PASSED                                                                                                                             [ 61%]
tests/reliability/test_breaker.py::test_many_threads_never_go_past_the_in_flight_limit PASSED                                                                                                    [ 61%]
tests/reliability/test_breaker.py::test_the_proposed_defaults_and_the_environment_names PASSED                                                                                                   [ 61%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[] PASSED                                                                                                                 [ 61%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[abc] PASSED                                                                                                              [ 62%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[0] PASSED                                                                                                                [ 62%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[-3] PASSED                                                                                                               [ 62%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[nan] PASSED                                                                                                              [ 62%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[inf] PASSED                                                                                                              [ 62%]
tests/reliability/test_breaker.py::test_a_bad_setting_gives_the_default[2.5] PASSED                                                                                                              [ 63%]
tests/reliability/test_breaker.py::test_route_the_model_is_not_called_once_the_breaker_is_open PASSED                                                                                            [ 63%]
tests/reliability/test_breaker.py::test_route_a_test_call_after_the_open_time_closes_the_breaker PASSED                                                                                          [ 63%]
tests/reliability/test_breaker.py::test_route_a_bad_answer_does_not_open_the_breaker PASSED                                                                                                      [ 63%]
tests/reliability/test_breaker.py::test_route_a_hung_model_does_not_hold_every_route_thread PASSED                                                                                               [ 63%]
tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row PASSED                                                                                                   [ 64%]
tests/reliability/test_drills.py::test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it PASSED                                                                                              [ 64%]
tests/reliability/test_drills.py::test_dr1_a_blank_correlation_id_is_replaced_and_a_sent_one_is_kept PASSED                                                                                      [ 64%]
tests/reliability/test_drills.py::test_dr1_the_event_stream_has_blank_ids_and_the_dedupe_key_does_not_use_them PASSED                                                                            [ 64%]
tests/reliability/test_drills.py::test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up PASSED                                                                                  [ 65%]
tests/reliability/test_drills.py::test_dr2_a_model_error_is_held_and_health_stays_up PASSED                                                                                                      [ 65%]
tests/reliability/test_drills.py::test_dr3_the_same_alarm_sent_twice_is_one_alarm_by_dedupe_key PASSED                                                                                           [ 65%]
tests/reliability/test_drills.py::test_dr3_same_dedupe_key_in_another_storm_is_a_different_alarm PASSED                                                                                          [ 65%]
tests/reliability/test_drills.py::test_dr3_a_blank_key_part_is_held_aside_and_never_recorded PASSED                                                                                              [ 65%]
tests/reliability/test_drills.py::test_dr3_all_354_alarm_rows_give_350_new_3_repeats_1_held_aside PASSED                                                                                         [ 66%]
tests/reliability/test_drills.py::test_dr3_all_354_order_rows_give_351_new_2_repeats_1_held_aside PASSED                                                                                         [ 66%]
tests/reliability/test_drills.py::test_dr3_replaying_the_event_file_twice_gives_3000_new_and_3000_repeats PASSED                                                                                 [ 66%]
tests/reliability/test_drills.py::test_dr3_the_summary_route_has_no_key_so_five_calls_cost_five_model_calls_and_five_rows PASSED                                                                 [ 66%]
tests/reliability/test_drills.py::test_dr4_a_true_stale_flag_is_blocked_and_the_model_is_not_called PASSED                                                                                       [ 66%]
tests/reliability/test_drills.py::test_dr4_a_blank_stale_flag_is_held_for_review_and_the_model_is_not_called PASSED                                                                              [ 67%]
tests/reliability/test_drills.py::test_dr4_a_false_flag_still_gets_a_summary PASSED                                                                                                              [ 67%]
tests/reliability/test_drills.py::test_dr4_192_rows_are_true_and_1_is_blank PASSED                                                                                                               [ 67%]
tests/reliability/test_drills.py::test_dr5_one_bad_row_is_reported_and_the_rest_are_processed PASSED                                                                                             [ 67%]
tests/reliability/test_drills.py::test_dr5_short_long_and_undecodable_rows_are_held_aside_and_the_run_goes_on PASSED                                                                             [ 68%]
tests/reliability/test_drills.py::test_dr5_the_real_file_keeps_its_old_counts_and_adds_one_quarantined_row PASSED                                                                                [ 68%]
tests/reliability/test_drills.py::test_dr6_ala_00002_is_flagged_and_does_not_become_an_incident PASSED                                                                                           [ 68%]
tests/reliability/test_drills.py::test_dr6_the_rule_id_exists_in_business_rules_yaml PASSED                                                                                                      [ 68%]
tests/reliability/test_drills.py::test_dr6_equal_times_are_fine_and_later_last_seen_is_fine PASSED                                                                                               [ 68%]
tests/reliability/test_drills.py::test_dr6_blank_or_unreadable_times_are_flagged_for_review PASSED                                                                                               [ 69%]
tests/reliability/test_drills.py::test_dr6_the_real_file_has_166_rows_before_and_1_unreadable_and_none_become_incidents PASSED                                                                   [ 69%]
tests/security/test_audit_log_security.py::test_write_event_refuses_an_empty_correlation_id[] PASSED                                                                                             [ 69%]
tests/security/test_audit_log_security.py::test_write_event_refuses_an_empty_correlation_id[   ] PASSED                                                                                          [ 69%]
tests/security/test_audit_log_security.py::test_write_event_refuses_an_empty_correlation_id[None] PASSED                                                                                         [ 69%]
tests/security/test_audit_log_security.py::test_write_event_with_an_id_writes_exactly_one_row PASSED                                                                                             [ 70%]
tests/security/test_audit_log_security.py::test_forbidden_name_finder_finds_a_planted_name PASSED                                                                                                [ 70%]
tests/security/test_audit_log_security.py::test_real_audit_log_holds_no_forbidden_name PASSED                                                                                                    [ 70%]
tests/security/test_client_flags_ignored.py::test_client_sent_policy_fields_change_nothing PASSED                                                                                                [ 70%]
tests/security/test_client_flags_ignored.py::test_no_route_reads_an_approval_id_from_the_caller PASSED                                                                                           [ 71%]
tests/security/test_docs_secret_scan.py::test_docs_scan_finds_planted_values_and_ignores_placeholders PASSED                                                                                     [ 71%]
tests/security/test_docs_secret_scan.py::test_docs_have_no_real_secret_formats PASSED                                                                                                            [ 71%]
tests/security/test_secret_detector.py::test_secret_scan_finds_planted_values_and_ignores_the_placeholder PASSED                                                                                 [ 71%]
tests/security/test_secret_detector.py::test_secret_scan_reads_files_when_a_parent_folder_is_named_docs PASSED                                                                                   [ 71%]
tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns PASSED                                                                                                                  [ 72%]
tests/test_api_contract.py::test_health_contract PASSED                                                                                                                                          [ 72%]
tests/test_api_contract.py::test_ai_summary_has_minimum_contract PASSED                                                                                                                          [ 72%]
tests/test_characterization.py::test_missing_record_returns_nothing PASSED                                                                                                                       [ 72%]
policy/tests/test_policy_python.py::test_fixture_counts PASSED                                                                                                                                   [ 72%]
policy/tests/test_policy_python.py::test_access_fixture[ac-01-allow-noc-operator-reads-device] PASSED                                                                                            [ 73%]
policy/tests/test_policy_python.py::test_access_fixture[ac-02-allow-ai-agent-recommends-incident] PASSED                                                                                         [ 73%]
policy/tests/test_policy_python.py::test_access_fixture[ac-03-deny-clinician-reads-device] PASSED                                                                                                [ 73%]
policy/tests/test_policy_python.py::test_access_fixture[ac-04-deny-admin-reads-device] PASSED                                                                                                    [ 73%]
policy/tests/test_policy_python.py::test_access_fixture[ac-05-deny-automation-service-executes-without-approval] PASSED                                                                          [ 73%]
policy/tests/test_policy_python.py::test_access_fixture[ac-06-allow-admin-reads-audit-log] PASSED                                                                                                [ 74%]
policy/tests/test_policy_python.py::test_access_fixture[ac-07-deny-operator-reads-audit-log] PASSED                                                                                              [ 74%]
policy/tests/test_policy_python.py::test_admin_has_no_blanket_access PASSED                                                                                                                      [ 74%]
policy/tests/test_policy_python.py::test_audit_read_is_allowed_for_admin_only PASSED                                                                                                             [ 74%]
policy/tests/test_policy_python.py::test_audit_read_row_allows_only_the_read_action PASSED                                                                                                       [ 75%]
policy/tests/test_policy_python.py::test_every_matrix_row_is_allowed_with_its_own_fields PASSED                                                                                                  [ 75%]
policy/tests/test_policy_python.py::test_changing_any_one_field_of_a_row_denies PASSED                                                                                                           [ 75%]
policy/tests/test_policy_python.py::test_execute_rows_need_an_approval_id[None] PASSED                                                                                                           [ 75%]
policy/tests/test_policy_python.py::test_execute_rows_need_an_approval_id[] PASSED                                                                                                               [ 75%]
policy/tests/test_policy_python.py::test_execute_rows_need_an_approval_id[   ] PASSED                                                                                                            [ 76%]
policy/tests/test_policy_python.py::test_missing_role_is_denied PASSED                                                                                                                           [ 76%]
policy/tests/test_policy_python.py::test_live_role_ids_stand_for_their_persona PASSED                                                                                                            [ 76%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-01-execute-with-all-checks] PASSED                                                                                                 [ 76%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-02-block-execute-without-approval-id] PASSED                                                                                       [ 76%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-03-recommend-only-summary] PASSED                                                                                                  [ 77%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-04-hold-recommendation-for-review] PASSED                                                                                          [ 77%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-05-hold-on-timeout] PASSED                                                                                                         [ 77%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-06-block-stale-topology] PASSED                                                                                                    [ 77%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-07-block-ai-agent-execute] PASSED                                                                                                  [ 78%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-08-block-forbidden-field-in-prompt] PASSED                                                                                         [ 78%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-09-block-execute-audit-row-missing] PASSED                                                                                         [ 78%]
policy/tests/test_policy_python.py::test_ai_action_fixture[ai-10-block-execute-approval-not-required] PASSED                                                                                     [ 78%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[du-01-allow-prompt-allow-list-only] PASSED                                                                   [ 78%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[du-02-deny-prompt-holds-mgmt-ip] PASSED                                                                      [ 79%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[du-03-allow-network-engineer-response-sensitive-fields] PASSED                                               [ 79%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[du-04-deny-noc-operator-response-sensitive-fields] PASSED                                                    [ 79%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[os-01-allow-live-change-with-all-checks] PASSED                                                              [ 79%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[os-02-deny-live-change-plan-not-reversible-validated] PASSED                                                 [ 79%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[pr-01-allow-release-with-all-evidence] PASSED                                                                [ 80%]
policy/tests/test_policy_python.py::test_other_areas_are_recorded_but_not_evaluated[pr-02-deny-release-with-missing-evidence] PASSED                                                             [ 80%]
policy/tests/test_policy_python.py::test_summarize_is_recommend_only PASSED                                                                                                                      [ 80%]
policy/tests/test_policy_python.py::test_recommend_is_held_for_review PASSED                                                                                                                     [ 80%]
policy/tests/test_policy_python.py::test_remediation_becomes_a_change_with_all_checks_allow PASSED                                                                                               [ 81%]
policy/tests/test_policy_python.py::test_remediation_does_not_become_a_change_without_approval_id_deny PASSED                                                                                    [ 81%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[None] PASSED                                                                                              [ 81%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[] PASSED                                                                                                  [ 81%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[ ] PASSED                                                                                                 [ 81%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[\t\n] PASSED                                                                                              [ 82%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[0] PASSED                                                                                                 [ 82%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[False] PASSED                                                                                             [ 82%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[approval_id6] PASSED                                                                                      [ 82%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[approval_id7] PASSED                                                                                      [ 82%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_when_the_approval_id_key_is_missing PASSED                                                                                       [ 83%]
policy/tests/test_policy_python.py::test_each_missing_key_blocks PASSED                                                                                                                          [ 83%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes0] PASSED                                                                                                                   [ 83%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes1] PASSED                                                                                                                   [ 83%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes2] PASSED                                                                                                                   [ 84%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes3] PASSED                                                                                                                   [ 84%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes4] PASSED                                                                                                                   [ 84%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes5] PASSED                                                                                                                   [ 84%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes6] PASSED                                                                                                                   [ 84%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes7] PASSED                                                                                                                   [ 85%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes8] PASSED                                                                                                                   [ 85%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes9] PASSED                                                                                                                   [ 85%]
policy/tests/test_policy_python.py::test_invalid_values_block[changes10] PASSED                                                                                                                  [ 85%]
policy/tests/test_policy_python.py::test_input_that_is_not_an_object_blocks PASSED                                                                                                               [ 85%]
policy/tests/test_policy_python.py::test_one_missing_check_stops_execute_each_time PASSED                                                                                                        [ 86%]
policy/tests/test_policy_python.py::test_hold_rows PASSED                                                                                                                                        [ 86%]
policy/tests/test_policy_python.py::test_block_wins_over_hold PASSED                                                                                                                             [ 86%]
policy/tests/test_policy_python.py::test_the_model_cannot_set_its_own_outcome PASSED                                                                                                             [ 86%]
policy/tests/test_policy_python.py::test_execute_is_reached_by_exactly_the_all_checks_inputs PASSED                                                                                              [ 86%]
policy/tests/test_policy_python.py::test_engine_failure_denies PASSED                                                                                                                            [ 87%]
policy/tests/test_policy_python.py::test_engine_name_follows_the_setting PASSED                                                                                                                  [ 87%]
policy/tests/test_policy_python.py::test_record_route_allows_operator_and_writes_read_row PASSED                                                                                                 [ 87%]
policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[clinician] PASSED                                                                                            [ 87%]
policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[admin] PASSED                                                                                                [ 88%]
policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[automation_service] PASSED                                                                                   [ 88%]
policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[vendor] PASSED                                                                                               [ 88%]
policy/tests/test_policy_python.py::test_record_route_refuses_a_missing_header PASSED                                                                                                            [ 88%]
policy/tests/test_policy_python.py::test_summarize_route_allows_roles_with_a_row[operator] PASSED                                                                                                [ 88%]
policy/tests/test_policy_python.py::test_summarize_route_allows_roles_with_a_row[ai_agent] PASSED                                                                                                [ 89%]
policy/tests/test_policy_python.py::test_summarize_route_denies_roles_without_a_row[None] PASSED                                                                                                 [ 89%]
policy/tests/test_policy_python.py::test_summarize_route_denies_roles_without_a_row[admin] PASSED                                                                                                [ 89%]
policy/tests/test_policy_python.py::test_summarize_route_denies_roles_without_a_row[clinician] PASSED                                                                                            [ 89%]
policy/tests/test_policy_python.py::test_summarize_route_denies_roles_without_a_row[vendor] PASSED                                                                                               [ 89%]
policy/tests/test_policy_python.py::test_summarize_route_blocks_a_device_with_a_stale_flag PASSED                                                                                                [ 90%]
policy/tests/test_policy_python.py::test_summarize_route_blocks_an_id_that_does_not_exist PASSED                                                                                                 [ 90%]
policy/tests/test_policy_python.py::test_summarize_route_holds_a_device_with_a_blank_stale_flag PASSED                                                                                           [ 90%]
policy/tests/test_policy_python.py::test_no_route_can_execute PASSED                                                                                                                             [ 90%]
policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access SKIPPED (opa binary not on PATH)                                                                                         [ 91%]
policy/tests/test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination SKIPPED (opa binary not on PATH)                                                                    [ 91%]
semantic-layer/tests/test_semantic_layer.py::test_tree_is_exactly_the_capture_layout_plus_generated_and_build PASSED                                                                             [ 91%]
semantic-layer/tests/test_semantic_layer.py::test_every_yaml_carries_version_and_readme_repeats_it PASSED                                                                                        [ 91%]
semantic-layer/tests/test_semantic_layer.py::test_schema_validates_every_yaml_file PASSED                                                                                                        [ 91%]
semantic-layer/tests/test_semantic_layer.py::test_schema_rejects_proposed_item_without_owner PASSED                                                                                              [ 92%]
semantic-layer/tests/test_semantic_layer.py::test_schema_rejects_six_entities PASSED                                                                                                             [ 92%]
semantic-layer/tests/test_semantic_layer.py::test_schema_rejects_missing_source PASSED                                                                                                           [ 92%]
semantic-layer/tests/test_semantic_layer.py::test_required_entities_present PASSED                                                                                                               [ 92%]
semantic-layer/tests/test_semantic_layer.py::test_required_personas_present PASSED                                                                                                               [ 92%]
semantic-layer/tests/test_semantic_layer.py::test_required_statuses_present PASSED                                                                                                               [ 93%]
semantic-layer/tests/test_semantic_layer.py::test_required_rules_present PASSED                                                                                                                  [ 93%]
semantic-layer/tests/test_semantic_layer.py::test_required_metrics_present_with_source_fields PASSED                                                                                             [ 93%]
semantic-layer/tests/test_semantic_layer.py::test_four_outcomes_present_and_model_never_executes PASSED                                                                                          [ 93%]
semantic-layer/tests/test_semantic_layer.py::test_every_agency_and_pick_word_is_defined PASSED                                                                                                   [ 94%]
semantic-layer/tests/test_semantic_layer.py::test_eleven_ai_uses_copied_from_qualification PASSED                                                                                                [ 94%]
semantic-layer/tests/test_semantic_layer.py::test_collisions_block_has_the_four_named_entries PASSED                                                                                             [ 94%]
semantic-layer/tests/test_semantic_layer.py::test_api_roles_today_and_clinician_removed PASSED                                                                                                   [ 94%]
semantic-layer/tests/test_semantic_layer.py::test_five_access_value_lists_have_ids PASSED                                                                                                        [ 94%]
semantic-layer/tests/test_semantic_layer.py::test_every_persona_grant_uses_defined_value_list_ids PASSED                                                                                         [ 95%]
semantic-layer/tests/test_semantic_layer.py::test_forbidden_prompt_fields_locked PASSED                                                                                                          [ 95%]
semantic-layer/tests/test_semantic_layer.py::test_api_reads_today_is_true_for_devices_only PASSED                                                                                                [ 95%]
semantic-layer/tests/test_semantic_layer.py::test_model_today_matches_code PASSED                                                                                                                [ 95%]
semantic-layer/tests/test_semantic_layer.py::test_every_id_is_dot_form_and_unique PASSED                                                                                                         [ 95%]
semantic-layer/tests/test_semantic_layer.py::test_every_referenced_id_is_defined PASSED                                                                                                          [ 96%]
semantic-layer/tests/test_semantic_layer.py::test_every_item_has_a_source_list_of_existing_paths PASSED                                                                                          [ 96%]
semantic-layer/tests/test_semantic_layer.py::test_every_proposed_item_names_an_owner PASSED                                                                                                      [ 96%]
semantic-layer/tests/test_semantic_layer.py::test_no_metric_has_a_target_value PASSED                                                                                                            [ 96%]
semantic-layer/tests/test_semantic_layer.py::test_fail_to_person_sets_no_timeout_number_without_owner PASSED                                                                                     [ 97%]
semantic-layer/tests/test_semantic_layer.py::test_glossary_and_yaml_agree_on_every_term PASSED                                                                                                   [ 97%]
semantic-layer/tests/test_semantic_layer.py::test_generated_json_matches_each_yaml PASSED                                                                                                        [ 97%]
semantic-layer/tests/test_semantic_layer.py::test_generated_manifest_hashes_match_yaml_bytes PASSED                                                                                              [ 97%]
semantic-layer/tests/test_semantic_layer.py::test_entity_fields_match_csv_headers PASSED                                                                                                         [ 97%]
semantic-layer/tests/test_semantic_layer.py::test_every_word_in_every_word_column_is_in_the_taxonomy PASSED                                                                                      [ 98%]
semantic-layer/tests/test_semantic_layer.py::test_observed_counts_match_the_csv PASSED                                                                                                           [ 98%]
semantic-layer/tests/test_semantic_layer.py::test_every_status_word_appears_where_it_says PASSED                                                                                                 [ 98%]
semantic-layer/tests/test_semantic_layer.py::test_no_secret_value_anywhere_in_the_tree PASSED                                                                                                    [ 98%]
semantic-layer/tests/test_semantic_layer.py::test_a_deprecated_item_names_a_defined_replacement PASSED                                                                                           [ 98%]
semantic-layer/tests/test_semantic_layer.py::test_schema_rejects_deprecated_without_replacement PASSED                                                                                           [ 99%]
semantic-layer/tests/test_semantic_layer.py::test_audit_row_fields_are_the_keys_the_code_writes PASSED                                                                                           [ 99%]
semantic-layer/tests/test_semantic_layer.py::test_cannot_prove_ids_match_the_item_names_in_the_code PASSED                                                                                       [ 99%]
semantic-layer/tests/test_semantic_layer.py::test_audit_action_words_in_main_py_all_have_an_id PASSED                                                                                            [ 99%]
semantic-layer/tests/test_semantic_layer.py::test_every_id_the_code_policy_and_tests_name_is_still_defined PASSED                                                                                [100%]

=================================================================================== 467 passed, 2 skipped in 31.75s ===================================================================================
```
