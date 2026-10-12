# Security test suite plan

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A |
| Date / version | 2026-10-11, v1.0. v1.1 after S05-13 Half B: the "exists" column for `SV-23` to `SV-27` now says yes. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every abuse case has a test, a test design, or a backlog row with an owner. 27 rows. At Half A, 20 had a passing test, 4 needed a new test (`NG-01` to `NG-04`), and 3 were backlog. After Half B, 25 have a passing test (`SV-23` to `SV-26` are written, and `SV-27` is the skip guard) and 2 stay backlog because the repo has no control to prove (`SV-03`, `SV-10`). Owner of every backlog row: Team-Force. |
| Evidence sources | `pytest -m security -q` run on 2026-10-11: `52 passed, 184 deselected`; `pytest <folder> --collect-only` for each test folder; `pytest policy/tests -rs -q`: `81 passed, 2 skipped`; `tests/access/test_negative_access.py`; `tests/security/test_secret_patterns.py`; `tests/ai/test_guardrails.py`; `tests/observability/test_audit_schema.py`; `tests/characterization/test_current_behaviour.py`; `tests/reliability/test_drills.py`; `policy/tests/test_policy_python.py`; `policy/tests/access_test.rego`; `policy/tests/ai_action_test.rego`; `apps/api/main.py`; `apps/api/services/policy.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `pyproject.toml`; `Makefile`; `scripts/evidence.sh`; `.github/workflows/ci.yml`; `docs/03-identity/negative-access-test-plan.md`; `docs/09-ai-guardrails/guardrail-test-pack.md`; `docs/06-policy/ai-action-policy-design.md`; `docs/07-cicd/security-scan-plan.md`; three read-only probes against the running app with a temporary audit log (described under "Probes") |
| Assumptions | Half A changes no code. Test counts come from `pytest --collect-only` on this machine (Windows, Python 3.13.5, no `opa` program). The owner name "Team-Force" follows `operating-contract.md` row 10. |
| Unresolved issues | Two tests that compare the Python policy with the Rego policy skip on this machine because `opa` is missing. Half B installs `opa` (decision by Mangesh, 2026-10-11). The `security` marker covers 52 tests today. The plan needs it on 147 existing tests plus 4 new ones. |
| Residual risks | A passing test shows one case works on one day. The plan does not claim the app is safe. Five rows have no control, so no test can show a deny for them. |

## What this file is

This file lists every abuse case the security suite must cover. For each case it names the test that covers it, the control the test proves, the rule id in the YAML files, and whether the test exists.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

**The "Exists" column has three values.**

| Value | Meaning |
|---|---|
| yes | A test exists today and passes (or passes with the 2 skip exception on `SV-15`). |
| no | The repo has the control. No test proves it. `negative-tests.md` holds the test design. |
| backlog | The repo has no control to prove. A test cannot show a deny. `remediation-backlog.md` holds a row with an owner. |

**Where each test file lives.**

| File name used below | Path |
|---|---|
| `test_negative_access.py` | `tests/access/test_negative_access.py` |
| `test_secret_patterns.py` | `tests/security/test_secret_patterns.py` |
| `test_guardrails.py` | `tests/ai/test_guardrails.py` |
| `test_policy_python.py` | `policy/tests/test_policy_python.py` |
| `test_audit_schema.py` | `tests/observability/test_audit_schema.py` |
| `test_current_behaviour.py` | `tests/characterization/test_current_behaviour.py` |
| `test_drills.py` | `tests/reliability/test_drills.py` |
| `test_breaker.py` | `tests/reliability/test_breaker.py` |
| `access_test.rego` and `ai_action_test.rego` | `policy/tests/` (run by `opa test`, not by pytest) |

## The suite plan

The first 15 rows are the abuse cases the playbook names. Rows 16 to 22 are cases the Phase 4 tests already cover and the suite should keep. Rows 23 to 26 are tests to write. Row 27 is a gap in the CI gate.

| Row | Abuse case | Test that covers it (file and name) | Control it proves | YAML rule id | Exists |
|---|---|---|---|---|---|
| SV-01 | A role with no matrix row (`admin`, `automation_service`, `vendor`) reads a device record. | `test_policy_python.py::test_record_route_denies_with_403_and_audit_row` (four roles). `test_policy_python.py::test_admin_has_no_blanket_access`. | The access policy denies a role with no row. The route returns 403 and writes one audit row with action `policy.deny`. | `rule.denied_access_is_audited`; `rule.shared_admin_not_least_privilege`; `policy.opa.default_deny` | yes |
| SV-02 | The removed role `clinician` reads a device record. | `test_negative_access.py::test_clinician_role_is_denied_on_record_read`. `test_current_behaviour.py::test_clinician_role_is_denied_on_record_read`. The `clinician` case inside `test_policy_python.py::test_record_route_denies_with_403_and_audit_row`. The `clinician` case inside `test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called`. | `clinician` is outside the grant list on both routes. Status 403, body `{"error":"forbidden"}`. | `role.clinician` (under `removed_roles`); `rule.denied_access_is_audited` | yes |
| SV-03 | A call to `GET /records/{id}` sends no role header. | Today's tests lock the allow: `test_negative_access.py::test_missing_role_header_keeps_operator_default` and `test_policy_python.py::test_record_route_keeps_missing_header_default_operator`. They show the call is allowed, so they cannot show a deny. | None. The route fills in `operator`. The owner decision in S04-03 keeps this. | `rule.no_default_role` | backlog (`SB-01`) |
| SV-04 | A call to `POST /ai/summarize/{id}` sends no role header. | `test_policy_python.py::test_summarize_route_denies_roles_without_a_row` (the `None` case). `test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called` (the empty-header case). `test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header`. | The summarize route has no default role. A missing header is a 403. The model is not called. The audit row has `role` null, not `operator`. | `rule.no_default_role`; `provenance.policy_result` | yes |
| SV-05 | An AI call by a caller with no recommend permission (`persona.customer_support`). | `test_guardrails.py::test_gr06_caller_without_recommend_permission_is_blocked`. | The access policy denies `action.recommend` for that persona. The AI policy then returns BLOCK with reason `provenance.policy_result`. No HTTP route for recommend exists, so the test calls the policy functions. | `action.recommend`; `provenance.policy_result` | yes |
| SV-06 | EXECUTE with no approval id. | `test_policy_python.py::test_remediation_does_not_become_a_change_without_approval_id_deny`. `test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` (8 values). `test_policy_python.py::test_execute_is_unreachable_when_the_approval_id_key_is_missing`. `test_policy_python.py::test_execute_rows_need_an_approval_id`. `test_policy_python.py::test_execute_is_reached_by_exactly_the_all_checks_inputs`. `test_negative_access.py::test_automation_service_may_not_execute_without_approval_id`. `ai_action_test.rego::test_remediation_blocked_without_approval_id`. | An execute call without a non-empty approval id is BLOCK. Of 82,944 input combinations, exactly 2 reach EXECUTE, and both carry an approval id and an audit row. | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `outcome.execute` | yes |
| SV-07 | Prompt injection: an instruction sentence sits in the `hostname` cell. | `test_guardrails.py::test_gr01_instruction_in_hostname_is_data_and_not_execute`. `test_guardrails.py::test_gr01_stub_model_with_injected_hostname_passes_the_schema`. `test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held` (3 cases). | The hostname text enters the prompt as data. The route outcome is never EXECUTE. A model answer that repeats the command is held, and `summary` is null. | `policy.prompt_fields`; `policy.output_schema`; `rule.ai_output_cannot_execute` | yes |
| SV-08 | `mgmt_ip` or `credential_profile` reaches the prompt. | `test_guardrails.py::test_gr02_prompt_has_only_allowed_fields`. `test_guardrails.py::test_gr02_every_device_row_builds_a_clean_prompt` (354 rows). `test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked`. `test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked` (5 cases). `test_guardrails.py::test_gr02_newline_in_a_value_stays_on_one_line`. | The prompt comes from the allow list. A forbidden field name or value in the prompt gives BLOCK. The model is not called. | `rule.forbidden_fields_never_enter_prompt`; `failmode.forbidden_field_in_prompt`; `policy.prompt_fields` | yes |
| SV-09 | A secret value or secret pattern sits in a committed file. | `test_secret_patterns.py::test_repo_has_no_secret_patterns`. `test_current_behaviour.py::test_legacy_script_reads_password_from_environment`. | No file outside the skip list holds a `sk-` key, a `password` or `token` assignment, or a named secret with a real value. The legacy script reads its password from the environment. | None. Open question for S03: no rule id says "no secret value is committed". This plan needs one so `SV-09` can name the rule it proves. | yes |
| SV-10 | Insecure default: the old default role header (`Header(default="operator")`). | Same two tests as `SV-03`. They lock the default and show no deny. | None. The default is at `apps/api/main.py` line 59. `policy.py` lines 290 and 297 also send an unknown role to the `operator` values. | `rule.no_default_role` | backlog (`SB-02`) |
| SV-11 | Unsafe AI action: the model output holds an execute verb. | `test_guardrails.py::test_gr07_execute_sentence_with_outcome_execute_is_held`. `test_guardrails.py::test_gr07_route_returns_block_if_the_policy_ever_said_execute`. `test_guardrails.py::test_gr07_response_type_and_routes_cannot_express_execute`. | The model's own outcome word is ignored. The response type has no EXECUTE value. No route name holds `execute`. The one command sentence in `COMMAND_PHRASES` is held. | `policy.output_schema`; `rule.ai_output_cannot_execute`; `failmode.schema_failure` | yes |
| SV-12 | An audit row has no `correlation_id`. | `test_audit_schema.py::test_every_audit_row_has_every_required_field`. `test_audit_schema.py::test_request_with_header_keeps_the_id`. `test_audit_schema.py::test_request_without_header_gets_a_uuid`. `test_drills.py::test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it`. `test_drills.py::test_dr1_a_blank_correlation_id_is_replaced_and_a_sent_one_is_kept`. | Every route call gets an id. A missing or blank header becomes a UUID. Every new row has 15 keys, and `correlation_id` is not empty. | `rule.audit_row_names_actor_and_correlation`; `provenance.correlation_id`; `field.event.correlation_id` | yes |
| SV-13 | A caller sends `approval_required` as false (finding `AA-01`). | `test_policy_python.py::test_one_missing_check_stops_execute_each_time` (the `approval_required` false case). `test_policy_python.py::test_invalid_values_block` (the string `"true"` case). `test_policy_python.py::test_execute_is_reached_by_exactly_the_all_checks_inputs`. `ai_action_test.rego::test_approval_must_be_required`. | An execute call with `approval_required` not true is BLOCK (row B7). This closes the loophole in the playbook wording. | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | yes |
| SV-14 | `mgmt_ip`, `credential_profile`, or a password written into `logs/audit.log` by the app's own code. | `test_audit_schema.py::test_every_audit_row_has_every_required_field` (exact key list, and neither field name in the row). `test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text`. `test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked` (the value is absent from the log text). `test_secret_patterns.py::test_repo_has_no_secret_patterns` (reads `logs/audit.log` for password and token assignments). | The audit row has fixed keys. It has no place for a device field or a secret. The prompt text is not stored. `prompt_hash` stands in for it. | None for the log. Open question for S03: no rule id says "the audit log holds no forbidden field". This plan needs one. | yes |
| SV-15 | The Python copy and the Rego copy of the policy give different answers. | `test_policy_python.py::test_opa_and_python_agree_on_access`. `test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination` (82,959 inputs). `opa test`: 30 Rego tests. | Both copies read one data file (`policy_data.json`) and return the same result. | None. Open question for S03: no rule id says "both copies of the policy agree". This plan needs one. | yes. Both pytest tests skip on this machine (`opa` missing). Half B fixes that. |
| SV-16 | Policy bypass on a stale device: the flag is true, blank, or missing. | `test_guardrails.py::test_gr03_stale_flag_true_is_blocked_before_the_model`. `test_guardrails.py::test_gr03_a_direct_gateway_call_is_stopped_too`. `test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model` (4 cases). `test_guardrails.py::test_gr08_the_blank_cell_in_the_data_file_is_held`. | True gives BLOCK. Blank or missing gives HOLD_FOR_REVIEW. The model is not called in either case. | `rule.stale_topology_blocks_recommendation`; `failmode.stale_topology_true`; `failmode.stale_topology_blank` | yes |
| SV-17 | A summary request for an id that does not exist. | `test_guardrails.py::test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row`. `test_policy_python.py::test_summarize_route_blocks_an_id_that_does_not_exist`. | The summary route returns BLOCK with `summary` null. It is not a summary of `REC-0001`. | `failmode.missing_id`; `rule.missing_id_not_other_device` | yes |
| SV-18 | The model returns a bad answer: not JSON, an extra key, a wrong type, or an answer about another record. | `test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary` (10 cases). `test_guardrails.py::test_gr04_a_model_that_raises_is_held`. | A bad answer is discarded. The outcome is HOLD_FOR_REVIEW. The body holds no made-up summary. | `policy.output_schema`; `failmode.schema_failure`; `policy.fail_to_person` | yes |
| SV-19 | The model does not answer in time. | `test_guardrails.py::test_gr05_timeout_is_held_with_no_summary`. `test_guardrails.py::test_gr05_timeout_argument_on_the_gateway`. `test_breaker.py::test_many_threads_never_go_past_the_in_flight_limit`. | The call stops at the deadline. The outcome is HOLD_FOR_REVIEW. | `failmode.timeout`; `policy.fail_to_person` | yes |
| SV-20 | The AI agent asks to execute, or a route that executes exists. | `test_negative_access.py::test_ai_agent_may_not_execute`. `test_policy_python.py::test_no_route_can_execute`. `test_policy_python.py::test_one_missing_check_stops_execute_each_time` (the `persona.ai_agent` case). `ai_action_test.rego::test_ai_agent_cannot_execute`. | `persona.ai_agent` is denied `action.execute`. No route path holds the word `execute`. | `rule.ai_output_cannot_execute`; `outcome.execute` | yes |
| SV-21 | The policy engine fails (the `opa` call errors). | `test_policy_python.py::test_engine_failure_denies`. | A failed engine gives deny for access and BLOCK for the AI policy. It never gives allow. | `provenance.policy_result`; `policy.opa.default_deny` | yes |
| SV-22 | A path returns a summary with no policy outcome, or an audit row with no model provenance. | `test_guardrails.py::test_gr10_success_body_has_the_policy_outcome_and_no_not_enforced`. `test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text`. `test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text`. | Every body past the role check carries an outcome. Only RECOMMEND_ONLY carries text. A model call writes `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms`. | `outcome.recommend_only`; `policy.provenance`; `provenance.prompt_hash` | yes |
| SV-23 | `audit.write_event` is called with an empty `correlation_id`. | None. | `write_event` raises `ValueError` and appends no row (`audit.py` lines 82 and 83). No test calls it with an empty id. | `rule.audit_row_names_actor_and_correlation` | yes (`NG-01`, written in Half B: `test_write_event_refuses_an_empty_correlation_id`) |
| SV-24 | A caller sends policy fields in the request (`approval_required` false, a made-up `approval_id`, `outcome` EXECUTE). | None at the HTTP level. `SV-13` covers the policy functions only. | The server ignores any client-sent flag. The body has `outcome` RECOMMEND_ONLY and `approval_id` null. | `provenance.approval_id`; `rule.ai_output_cannot_execute` | yes (`NG-02`, written in Half B: `test_client_sent_policy_fields_change_nothing`) |
| SV-25 | The real `logs/audit.log` holds a forbidden field name or a credential name. | None. `SV-14` tests rows written into a temporary file. The secret scan reads the real log for assignments, not for these names. | Nothing the app wrote to the real log names `mgmt_ip`, `credential_profile`, or a credential name. | None. Same open question as `SV-14`. | yes (`NG-03`, written in Half B: `test_real_audit_log_holds_no_forbidden_name`) |
| SV-26 | The secret scan stops finding secrets (a regex edit breaks it). | None. S04-04 ran the proof by hand (`docs/04-secrets/evidence.md`). | The scan finds a planted `sk-` value, a `PASSWORD` assignment, and a `KEY` assignment, and ignores the `CHANGE_ME` placeholder. | None. Same open question as `SV-09`. | yes (`NG-04`, written in Half B: `test_secret_scan_finds_planted_values_and_ignores_the_placeholder`) |
| SV-27 | A security test skips and the stage still exits 0. | None. | The CI gate fails when `junit-security.xml` shows any skipped test. | None. | yes (`SB-10` closed in Half B: `scripts/check_junit_no_skips.py`, `tests/ci/test_skip_guard.py`) |

## Count check

| Value | Rows | How many |
|---|---|---|
| yes | SV-01, 02, 04, 05, 06, 07, 08, 09, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 | 20 |
| no | SV-23, 24, 25, 26 | 4 |
| backlog | SV-03, 10, 27 | 3 |
| Total | | 27 |

The playbook expects two backlog rows (`SV-03` and `SV-10`). A third (`SV-27`) is a gap in the CI gate that this stage found. Other gaps are not abuse cases a test can name today. They are in `remediation-backlog.md`.

## Marker plan for Half B

The marker `security` exists in `pyproject.toml`. **Verified Fact.** Today it marks 52 tests: 51 in `test_guardrails.py` and 1 in `test_secret_patterns.py`.

| File | Tests | Marked today | Half B action |
|---|---|---|---|
| `tests/ai/test_guardrails.py` | 51 | 51 (file-level `pytestmark`) | None. |
| `tests/security/test_secret_patterns.py` | 1 | 1 | None. |
| `tests/access/test_negative_access.py` | 6 | 0 | Mark the whole file. |
| `policy/tests/test_policy_python.py` | 83 (37 test functions) | 0 | Mark the whole file. Three housekeeping tests ride along: `test_fixture_counts`, `test_other_areas_are_recorded_but_not_evaluated`, `test_engine_name_follows_the_setting`. Marking by file keeps the plan simple. |
| `tests/observability/test_audit_schema.py` | 3 | 0 | Mark the whole file. |
| `tests/characterization/test_current_behaviour.py` | 5 | 0 | Mark three by name: `test_clinician_role_is_denied_on_record_read`, `test_ai_summarize_refuses_request_with_no_role_header`, `test_legacy_script_reads_password_from_environment`. |
| New tests under `tests/security/` | 4 or more | n/a | Mark every test (rows `SV-23` to `SV-26`). |

**Worked example.** Today `pytest -m security` runs 52 tests. After Half B it runs 52 + 6 + 83 + 3 + 3 = 147 existing tests, plus 4 new tests. That is 151.

**Effect on the `tests` stage.** **Inference.** `scripts/evidence.sh tests` runs `pytest tests -m "not security"`. The folder holds 153 tests today, and 101 are not marked. Marking 12 more moves the count to 89 (6 + 3 + 3 = 12 fewer). The 4 new tests are marked, so they do not change it. The `policy` stage runs `pytest policy/tests` with no marker filter, so it stays at 83. `docs/07-cicd/evidence.md` says the `tests` stage has 20 tests. That number is already out of date (S04-08 onward added tests). Half B updates the number.

The marker text in `pyproject.toml` today is: "scans committed files for secret values and secret patterns, and runs the AI guardrail tests". Half B adds access and policy decisions, audit row contents, and the legacy password check.

## What the suite does not cover

| Gap | Where it is recorded |
|---|---|
| No test shows a deny for a call with no role header on `GET /records/{id}` (`SV-03`, `SV-10`). | `SB-01`, `SB-02` |
| A model answer that repeats `mgmt_ip` or a credential name passes the schema (probe result below). | `SB-04` |
| Only one command sentence is detected in a model answer. | `SB-05` |
| Text sent in `X-User-Role` or `X-Correlation-Id` is written to the audit log unchanged (probe result below). | `SB-03` |
| A secret written in a Markdown file under `docs/` is not scanned (`BL-03`). | `BL-03` |
| A security test can skip with exit code 0. | `SB-10` |
| The secret scan reads no file when the repo path holds a folder named `docs`, `venv`, `.venv`, or `.git`. | `SB-18` |

## Probes

Three read-only probes ran on 2026-10-11 against the running app with a temporary audit log. They changed no file in the repo. `logs/audit.log` still has 240 lines.

**Verified Fact (probe 1).**

| Request | Result |
|---|---|
| `GET /records/REC-0001`, header `X-User-Role: mgmt_ip=10.1.1.1 password=hunter2`, header `X-Correlation-Id` of 5000 characters | HTTP 403. The audit row stores that role text unchanged, and a `correlation_id` of 5000 characters. |
| `GET /records/REC-0001`, no role header | HTTP 200. The body holds the key `mgmt_ip`. |
| `GET /records/DOES-NOT-EXIST`, role `operator` | HTTP 200. `device_id` is `REC-0001`. |
| `POST /ai/summarize/REC-0001`, role `operator`, JSON body with `approval_required` false, `approval_id` `APR-1`, `outcome` EXECUTE | HTTP 200. `outcome` is RECOMMEND_ONLY. `approval_id` is null. `approval_required` is false. |

**Verified Fact (probe 2).** The model function was replaced with one that returns a schema-valid answer.

| Answer text | Result |
|---|---|
| A summary that holds the device's `mgmt_ip` value | HTTP 200, RECOMMEND_ONLY. The body holds that value. The audit row does not. |
| A recommendation: "Reboot the core router now and clear the config" | HTTP 200, RECOMMEND_ONLY. The body holds that sentence. |
| A summary that holds the name `SHARED_DB_PASSWORD` | HTTP 200, RECOMMEND_ONLY. |

The real `mgmt_ip` cell for `REC-0001` is the word `gamma`. The probe used a made-up value in a copy of the row.

**Verified Fact (probe 3).** Checks for the new tests and for the secret scan.

| Check | Result |
|---|---|
| `audit.write_event` with `correlation_id` of `""`, `"   "`, and `None` | Each raised `ValueError: correlation_id is required`. No log file was created. |
| `POST /ai/summarize/REC-0001?approval_id=APR-FORGED-1&approval_required=false&outcome=EXECUTE`, role `operator` | HTTP 200. `outcome` RECOMMEND_ONLY. `approval_id` null. The audit text does not hold `APR-FORGED-1`. |
| Secret scan on the real repo | 164 files scanned. |
| Secret scan on a folder `.../ok/proj` with one planted `PASSWORD = '...'` file | 1 file scanned, 2 hits. |
| Secret scan on a folder `.../docs/proj` with the same file | 0 files scanned, 0 hits. |

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| SVF-01 | 52 tests carry the `security` marker. The plan needs 147 existing tests marked. | **Verified Fact.** `pytest -m security`: 52 passed, 184 deselected. `pytest -m security --collect-only -q` lists 51 tests in `tests/ai/test_guardrails.py` and 1 in `tests/security/test_secret_patterns.py`, and none from any other file. | `evidence/junit-security.xml` leaves out the access, policy, and audit tests. Stage S09 would cite a suite that is smaller than the real one. | A reviewer reads "1 passed" and thinks the suite is one test. | High | None. |
| SVF-02 | `evidence/junit-security.xml` is out of date. It shows 1 test, written at 13:32 on 2026-10-11, before the guardrail tests existed. | **Verified Fact.** The file: `tests="1"`. Today's run: 52. | S09 would copy a 1-test file. | The pack understates the suite. | High | None. Half B reruns the stage. |
| SVF-03 | Two rows cannot show a deny: `SV-03` and `SV-10`. They are one code line seen two ways. | **Verified Fact.** `main.py` line 59. `test_missing_role_header_keeps_operator_default` asserts HTTP 200. Probe 1: no header, HTTP 200, body has `mgmt_ip`. | A call with no header reads the device row, including the two sensitive cells. | High. Any caller reaches the row without naming a role. | High | The decision to keep the default belongs to S04-03 (owner Team-Force). |
| SVF-04 | The summarize route does deny a call with no role header. The playbook says "request with no role header" cannot show a deny. That is true for `GET /records/{id}` only. | **Verified Fact.** `test_policy_python.py::test_summarize_route_denies_roles_without_a_row` (`None` case). | `SV-04` is a passing row that the playbook did not name. | None. | High | None. |
| SVF-05 | Text in `X-User-Role` and `X-Correlation-Id` reaches `logs/audit.log` without a length limit or a content check. | **Verified Fact.** Probe 1. `main.py` `_role_word` and `audit.correlation_id_from_header` strip spaces and nothing else. `test_policy_python.py::test_record_route_denies_with_403_and_audit_row` asserts the role is stored unchanged. | A caller can plant a secret-looking string or a very long string in the audit log. JSON encoding stops a new-line forgery. | Medium. | High | None. |
| SVF-06 | The prompt is checked for forbidden fields. The model answer is not. | **Verified Fact.** `ai_gateway.py` `find_forbidden` runs on the prompt only (`_run_model`, line 293). Probe 2. | A real model could repeat `mgmt_ip` in a summary, and the route would return it. | Medium today (the model is a stub). The stub never repeats a field. | High | The same limit is stated in `docs/09-ai-guardrails/evidence.md` for a value inside an allowed field. |
| SVF-07 | `ruff` is not one of the five checks in `security-scan-plan.md`. The playbook lists it as one of the five. | **Verified Fact.** The five checks are the secret test, `pip-audit`, `bandit`, the policy tests, and the semantic-layer tests. Ruff is pipeline stage 2. | Two of the five exit 1 (`pip-audit`, `bandit`). Ruff is a third red stage. | Low. | High | None. `scanning-checklist.md` lists ruff in its own row. |
| SVF-09 | The secret scan reads the folder names of the full path, not the path inside the repo. If the repo sits in a folder named `docs`, `venv`, `.venv`, or `.git`, the scan reads no file and the test passes. | **Verified Fact.** `test_secret_patterns.py` line 40 tests `path.parts` of an absolute path. Probe 3: the same planted `PASSWORD = '...'` file gave 1 file scanned and 2 hits under `.../ok/proj`, and 0 files scanned and 0 hits under `.../docs/proj`. The real repo scans 164 files today. | A checkout under a path such as `C:\docs\capstone` would pass the test with no scan. | Low on this machine (no such folder in the path). Medium for a stranger's checkout or a CI path. | High | None. `NG-04` asserts that at least one file was scanned, and `SB-18` records the fix. |
| SVF-08 | The two Python-versus-Rego tests skip on this machine and exit 0. | **Verified Fact.** `pytest policy/tests -rs`: `SKIPPED ... opa binary not on PATH` at lines 524 and 534. | The Rego copy is the policy of record. Without `opa`, nothing compares it with the Python copy. | The two copies can drift. The first `opa test` run in S04-06 failed 1 of 30 while Python was green (`docs/06-policy/evidence.md`). | High | None. Half B installs `opa`. |

## Lifecycle

Half B marks the tests in the "Marker plan" table, writes `NG-01` to `NG-04`, adds a `make security` target, and installs `opa` locally and in CI. Stage S09 copies `evidence/junit-security.xml` and cites this suite for each security claim. Stage S05R folds the open questions into the YAML.

Open question for S03: no rule id says "no secret value is committed to the repo". This plan needs it for `SV-09` and `SV-26`.

Open question for S03: no rule id says "the audit log holds no forbidden field". This plan needs it for `SV-14` and `SV-25`.

Open question for S03: no rule id says "the Python copy and the Rego copy of the policy agree". This plan needs it for `SV-15`.
