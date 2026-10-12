# Abuse-case evidence

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A |
| Date / version | 2026-10-11, v1.0. v1.1 after S05-13 Half B: see the section "Half B update" at the end. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. 20 abuse cases already have a test. 19 of them passed in runs on 2026-10-11. `SV-15` skipped because `opa` is missing, and its last pass is the S04-06 Docker run. |
| Evidence sources | Run 1: `pytest -m security -q -p no:cacheprovider`: `52 passed, 184 deselected`. Run 2: `pytest tests/access tests/observability tests/characterization tests/reliability/test_drills.py tests/reliability/test_breaker.py policy/tests -v`: `141 passed, 2 skipped`. `evidence/opa-test.json`. `docs/06-policy/evidence.md`. The test files named in each row. |
| Assumptions | A test name that shows PASSED in run 1 or run 2 is a Verified Fact for 2026-10-11 on this machine (Windows, Python 3.13.5, no `opa`). Run 2 appended to `logs/audit.log` and the file was restored afterwards. `git status` shows it unchanged. |
| Unresolved issues | The 2 tests that need `opa` skipped. Half B makes them run. |
| Residual risks | Each assertion proves one case. It does not prove that no other input gets through. Rows `SV-06` and `SV-13` also have an all-inputs test that raises the confidence. |

## What this file is

This file pastes the passing test name and the assertion that proves the control, for each abuse case that already has a test. Row numbers match `security-test-suite-plan.md`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Result of the runs

| Run | Command | Result |
|---|---|---|
| 1 | `pytest -m security -q -p no:cacheprovider` | 52 passed, 184 deselected, 47 warnings |
| 2 | `pytest tests/access tests/observability tests/characterization tests/reliability/test_drills.py tests/reliability/test_breaker.py policy/tests -v -p no:cacheprovider` | 141 passed, 2 skipped, 6106 warnings |
| 3 | `pytest policy/tests -rs -q -p no:cacheprovider` | 81 passed, 2 skipped. Both skips: `opa binary not on PATH` |

Count of the 20 rows with a test: 19 passed in run 1 or run 2. 1 row (`SV-15`) skipped.

## Evidence by row

Each test name below showed PASSED in run 1 or run 2 unless the row says otherwise.

| Row | Abuse case | Passing test | The assertion that proves the control |
|---|---|---|---|
| SV-01 | A role with no matrix row reads a device record. | `test_policy_python.py::test_record_route_denies_with_403_and_audit_row[admin]`, `[automation_service]`, `[vendor]`. `test_policy_python.py::test_admin_has_no_blanket_access`. | `assert response.status_code == 403`; `assert response.json() == {"error": "forbidden"}`; `assert [row["action"] for row in rows] == ["policy.deny"]`. For admin: `assert result["allow"] is False` and `assert result["matrix_rows"] == []` for every action. |
| SV-02 | `clinician` reads a device record. | `test_negative_access.py::test_clinician_role_is_denied_on_record_read`. `test_current_behaviour.py::test_clinician_role_is_denied_on_record_read`. `test_policy_python.py::test_record_route_denies_with_403_and_audit_row[clinician]`. | `assert response.status_code == 403`; `assert response.json() == {"error": "forbidden"}`. |
| SV-04 | A summary request with no role header. | `test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header`. `test_policy_python.py::test_summarize_route_denies_roles_without_a_row[None]`. `test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called[headers2]`. | `assert response.status_code == 403`; `assert [row["action"] for row in rows] == ["policy.deny"]`; `assert rows[0]["role"] is None`. In the guardrail test: `assert model.prompts == []`, so the model was not called. |
| SV-05 | An AI call by a caller with no recommend permission. | `test_guardrails.py::test_gr06_caller_without_recommend_permission_is_blocked`. | `assert access["allow"] is False`; `assert result["outcome"] == "BLOCK"`; `assert "provenance.policy_result" in result["reasons"]`. |
| SV-06 | EXECUTE with no approval id. | `test_policy_python.py::test_remediation_does_not_become_a_change_without_approval_id_deny`. `test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` (8 values, all passed). `test_policy_python.py::test_execute_is_unreachable_when_the_approval_id_key_is_missing`. `test_policy_python.py::test_execute_is_reached_by_exactly_the_all_checks_inputs`. `test_negative_access.py::test_automation_service_may_not_execute_without_approval_id`. | `assert result["outcome"] == "BLOCK"` and the reason list holds `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. For the 8 values: `assert policy.evaluate_ai_action(payload)["outcome"] != "EXECUTE"`. For the all-inputs test: `assert len(executes) == 2`, and each one has `payload["approval_id"] == "APR-EXAMPLE-0001"`. |
| SV-07 | Instruction text in `hostname`. | `test_guardrails.py::test_gr01_instruction_in_hostname_is_data_and_not_execute`. `test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held[recommendation-is-the-command]`, `[summary-is-the-command]`, `[model-sets-execute]`. | `assert body["outcome"] != "EXECUTE"`; `assert INJECTION in prompt`; `assert "mgmt_ip" not in prompt`; `assert INJECTION not in audit_rows.path.read_text(encoding="utf-8")`. For a model that obeys: `assert response.status_code == 202` and `assert "failmode.schema_failure" in response.json()["reasons"]`. |
| SV-08 | `mgmt_ip` or `credential_profile` reaches the prompt. | `test_guardrails.py::test_gr02_prompt_has_only_allowed_fields`. `test_guardrails.py::test_gr02_every_device_row_builds_a_clean_prompt`. `test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked`. `test_guardrails.py::test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked` (5 cases). | `assert name not in prompt` for `mgmt_ip`, `credential_profile`, `customer_id`. For 354 rows: `assert ai_gateway.find_forbidden(prompt, row) == []`. For a builder that adds the value: `assert response.status_code == 403`; `assert "failmode.forbidden_field_in_prompt" in body["reasons"]`; `assert model.prompts == []`. |
| SV-09 | A secret in a committed file. | `test_secret_patterns.py::test_repo_has_no_secret_patterns`. `test_current_behaviour.py::test_legacy_script_reads_password_from_environment`. | `assert hits == [], hits`. For the legacy script: `assert not is_literal, "SHARED_DB_PASSWORD string constant is present"`. The scan skipped the `docs` folder (see `BL-03`). |
| SV-11 | An execute verb in the model output. | `test_guardrails.py::test_gr07_execute_sentence_with_outcome_execute_is_held`. `test_guardrails.py::test_gr07_route_returns_block_if_the_policy_ever_said_execute`. `test_guardrails.py::test_gr07_response_type_and_routes_cannot_express_execute`. | `assert body["outcome"] != "EXECUTE"`; the device file bytes are the same before and after. `assert body["reasons"] == ["rule.ai_output_cannot_execute"]` when the policy is forced to say EXECUTE. `assert "EXECUTE" not in ai_gateway.AiResponse.model_fields["outcome"].annotation.__args__`. Limit: only one command sentence is detected (`SB-05`). |
| SV-12 | An audit row with no `correlation_id`. | `test_audit_schema.py::test_every_audit_row_has_every_required_field`. `test_audit_schema.py::test_request_without_header_gets_a_uuid`. `test_drills.py::test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it`. | `assert tuple(row) == REQUIRED_KEYS` (15 keys); `assert row["correlation_id"]`; `assert parsed.version == 4`; `assert rows[0]["correlation_id"] == created`. |
| SV-13 | A caller sends `approval_required` as false. | `test_policy_python.py::test_one_missing_check_stops_execute_each_time`. `test_policy_python.py::test_invalid_values_block[changes7]` (the string `"true"`). `test_policy_python.py::test_ai_action_fixture[ai-10-block-execute-approval-not-required]`. | The loop sets `approval_required` to `False` and asserts `result["outcome"] == "BLOCK", name`. The fixture `ai-10` expects BLOCK. The all-inputs test lets only `payload["approval_required"] is True` reach EXECUTE. |
| SV-14 | `mgmt_ip`, `credential_profile`, or a password in the audit log, written by the app. | `test_audit_schema.py::test_every_audit_row_has_every_required_field`. `test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text`. `test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked`. | `assert "mgmt_ip" not in text` and `assert "credential_profile" not in text` for each row. `assert prompt not in log_text`; `assert SENTINEL_MGMT_IP not in log_text`; `assert SENTINEL_CREDENTIAL not in log_text`. |
| SV-15 | The Python and Rego policy copies disagree. | `test_policy_python.py::test_opa_and_python_agree_on_access`. `test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination`. **SKIPPED today.** | The assertion is `assert opa_result == policy._access_python(payload), payload` for every input. It did not run. **Verified Fact for the last pass:** `docs/06-policy/evidence.md`: with Docker-backed OPA 1.21.1, 98 passed and 0 skipped, and the two copies agreed on 82,959 AI inputs. `evidence/opa-test.json`: 30 Rego tests, 0 failed. |
| SV-16 | A stale or blank topology flag. | `test_guardrails.py::test_gr03_stale_flag_true_is_blocked_before_the_model`. `test_guardrails.py::test_gr03_a_direct_gateway_call_is_stopped_too`. `test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model` (4 cases). | True: `assert response.status_code == 403`; `assert "failmode.stale_topology_true" in body["reasons"]`; `assert model.prompts == []`. Blank or missing: `assert response.status_code == 202`; `assert body["reasons"] == ["failmode.stale_topology_blank"]`. |
| SV-17 | A summary request for an id that does not exist. | `test_guardrails.py::test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row`. `test_policy_python.py::test_summarize_route_blocks_an_id_that_does_not_exist`. | `assert response.status_code == 403`; `assert "REC-0001" not in json.dumps(body)`; `assert body["reasons"] == ["failmode.missing_id"]`; `assert model.prompts == []`. |
| SV-18 | A bad model answer. | `test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary` (10 cases). `test_guardrails.py::test_gr04_a_model_that_raises_is_held`. | `assert response.status_code == 202`; `assert body["reasons"] == ["failmode.schema_failure"]`; `assert rows[0]["outcome"] == "HOLD_FOR_REVIEW"`. `assert_failure_body` also asserts `summary` and `recommendation` are null. |
| SV-19 | The model does not answer in time. | `test_guardrails.py::test_gr05_timeout_is_held_with_no_summary`. `test_guardrails.py::test_gr05_timeout_argument_on_the_gateway`. `test_breaker.py::test_many_threads_never_go_past_the_in_flight_limit`. | `assert "failmode.timeout" in body["reasons"]`; `assert 40 <= rows[0]["latency_ms"] < 350`, so the call stopped at the deadline and not when the slow model finished. |
| SV-20 | The AI agent asks to execute. | `test_negative_access.py::test_ai_agent_may_not_execute`. `test_policy_python.py::test_no_route_can_execute`. | `assert target_decision(AI_AGENT_EXECUTE) == "deny"`; `assert all("execute" not in path for path in paths)`. |
| SV-21 | The policy engine fails. | `test_policy_python.py::test_engine_failure_denies`. | `assert access["allow"] is False`; `assert ai["outcome"] == "BLOCK"`; `assert ai["reasons"] == ["policy_engine_error"]`. |
| SV-22 | A path with no policy outcome, or a model row with no provenance. | `test_guardrails.py::test_gr10_success_body_has_the_policy_outcome_and_no_not_enforced`. `test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text`. `test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text`. | `assert body["guardrail_status"] != "not_enforced"`; `assert body["outcome"] in ALLOWED_OUTCOMES` for 6 paths; `assert row["prompt_hash"] == hashlib.sha256(prompt.encode("utf-8")).hexdigest()`. |

Seven plan rows are not in this table, because they have no passing test. `SV-23` to `SV-26` need a new test (`negative-tests.md`). `SV-03`, `SV-10`, and `SV-27` are backlog.

**Worked example (row `SV-06`).** The playbook done test for S04-06 was "an AI remediation recommendation becomes a change". `test_remediation_becomes_a_change_with_all_checks_allow` shows the allow case: EXECUTE with all checks. `test_remediation_does_not_become_a_change_without_approval_id_deny` shows the deny case: the same input with no approval id gives BLOCK. The all-inputs test then shows that of 82,944 combinations only 2 reach EXECUTE, and both carry an approval id.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| AE-01 | 19 of the 20 rows with a test passed today. The 20th (`SV-15`) skipped. | **Verified Fact.** Run 1, run 2, and run 3 above. | The evidence for all rows except `SV-15` is real, current, and tied to a test name. | A row that skips shows no proof today. | High | None. |
| AE-02 | The `SV-15` proof rests on a run from S04-06, not on today. | **Verified Fact.** `docs/06-policy/evidence.md`; `evidence/opa-test.json`. | The last pass is a few hours old and ran through Docker. | The Rego copy can change without notice, until `opa` is on the PATH. | High | None. Half B fixes it. |
| AE-03 | Rows `SV-09` and `SV-14` prove "no secret in the files read" and "no forbidden name in the rows written during a test". They do not prove that the files a person opens are clean. | **Verified Fact.** `test_repo_has_no_secret_patterns` skips `docs`. The audit tests write to a temporary file. | `NG-03` closes the audit side. `BL-03` closes the `docs` side. | Medium. | High | None. |
| AE-04 | The access tests in `tests/access/` for `NA-03`, `NA-04`, and `NA-05` call a stand-in function (`target_decision`) and not the policy. | **Verified Fact.** `test_negative_access.py` lines 46 to 67. | These three tests prove a target decision written in the test file. The real proof is in `test_policy_python.py`. | A reader could cite `NA-03` as policy evidence. | High | None. The plan cites the policy tests for `SV-05`, `SV-06`, and `SV-20`. |

## Lifecycle

Half B marks these tests, reruns them with `opa` available, and records the real counts in `docs/13-security-validation/evidence.md`. Stage S09 cites the test names above for each security claim.

Open question for S03: none beyond the three in `security-test-suite-plan.md`.

## Half B update

**Verified Fact.** These results are from `scripts\evidence.ps1` on 2026-10-11 with `opa` 1.21.1 on the PATH. `evidence/junit-security.xml`: `tests="159" skipped="0" failures="0"`.

| Row | Change since Half A | Test name | The assertion that proves the control |
|---|---|---|---|
| SV-15 | The two tests now run and pass. At Half A they skipped. | `test_policy_python.py::test_opa_and_python_agree_on_access` (0.133 s). `test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination` (43.414 s). | `assert opa_result == policy._access_python(payload), payload` for every input. `opa test`: `PASS: 30/30` (`evidence/opa-test.json`). |
| SV-23 | New test. | `test_audit_log_security.py::test_write_event_refuses_an_empty_correlation_id[]`, `[   ]`, `[None]` | `pytest.raises(ValueError, match="correlation_id is required")`, then `assert not log.exists()`. |
| SV-24 | New test. | `test_client_flags_ignored.py::test_client_sent_policy_fields_change_nothing`. `test_no_route_reads_an_approval_id_from_the_caller`. | `body["outcome"] == "RECOMMEND_ONLY"`; `body["approval_id"] is None`; `body["approval_required"] is False`; `len(rows) == 3`; `FORGED_ID not in text`. No route takes a query or body value named `approval_id`, `approval_required`, `outcome`, or `policy_result`. |
| SV-25 | New test. | `test_audit_log_security.py::test_real_audit_log_holds_no_forbidden_name`. `test_forbidden_name_finder_finds_a_planted_name`. | `assert forbidden_name_hits(REAL_LOG) == []`; every non-empty line parses as a JSON object. The finder returns `[(2, <name>)]` for a planted line. |
| SV-26 | New test. | `test_secret_detector.py::test_secret_scan_finds_planted_values_and_ignores_the_placeholder`. `test_secret_scan_reads_files_when_a_parent_folder_is_named_docs`. | `assert len(list(scan._iter_scanned_files())) == 4`; hits name `one.txt`, `two.txt`, and `three.txt`, and not `four.txt` (the placeholder). |
| SV-27 | Closed by a script, not a test. | `tests/ci/test_skip_guard.py` (8 tests) check the guard. The proof run is in `evidence.md` section 4. | `check_text` of a run with 1 skipped test returns `1 security test(s) skipped: a.b::t_opa`. `evidence.ps1 -Stage security` without `opa` exits 1 and names both skipped tests. |
| SV-09 | The scan reads the path below the repo root. A second test scans `docs/` for real key formats. | `test_secret_patterns.py::test_repo_has_no_secret_patterns`. `test_docs_secret_scan.py::test_docs_have_no_real_secret_formats`. | `assert len(list(_iter_scanned_files())) > 50`; `assert hits == []`. For `docs/`: `assert len(files) > 50`; `assert hits == []`. |

Findings `AE-02` and `AE-03` of Half A are updated: `AE-02` (SV-15 last pass) now has a pass today. The `docs/` gap in `AE-03` is closed for real key formats only.
