# Threat Model

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A. The starter text from the brownfield pack is kept below. |
| Date / version | 2026-10-11, v1.0 (starter extended) |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. 51 threats are listed across boundaries B1 to B9. Each has a status. 32 are covered by a test, 2 are covered by a scan with the finding still open, and 17 are open with a backlog row and an owner. Half B (2026-10-11) moved 4 threats from open to covered by test. MAESTRO is not mapped (see the open question below). Owner of every open row: Team-Force. |
| Evidence sources | `docs/09-ai-guardrails/trust-boundary-diagram.md` (boundaries B1 to B9); `docs/13-security-validation/abuse-case-evidence.md` (rows `SV-nn`, test names); `docs/13-security-validation/security-test-suite-plan.md`; `docs/13-security-validation/negative-tests.md` (`NG-nn`); `docs/13-security-validation/scanning-checklist.md`; `docs/13-security-validation/remediation-backlog.md` (`SB-nn`, `BL-nn`); `docs/09-ai-guardrails/ai-risk-register.md` (`AIR-nn`); `docs/06-policy/ai-action-policy-design.md` (`AA-nn`); `docs/02-baseline/defect-list.md` |
| Assumptions | A "covered by test" status means a test named in `abuse-case-evidence.md` passed on 2026-10-11, or the test is named there with the skip noted. The threat list holds the threats Half A found by reading the code and running probes. It does not claim that the list is complete. |
| Unresolved issues | The MAESTRO letters are Unknown (below). The `ai_use` for hosted models is Unknown. |
| Residual risks | A threat that Half A did not think of is not on the list. A "covered by test" row shows that one input is stopped. It does not show that every input is stopped. |

## What this file is

This file lists the threats at each of the nine trust boundaries of the summary call. For each threat it names the control that exists today, the test or scan that shows the control works, and the status.

The six STRIDE letters are: S spoofing (pretending to be someone), T tampering (changing data), R repudiation (denying an action with no record to show otherwise), I information disclosure (data reaching a reader who should not see it), D denial of service (the service is too slow or stops), E elevation of privilege (doing something the role is not allowed to do).

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Status words:

- **Covered by test.** A named test passed on 2026-10-11 and proves the control for the input it uses.
- **Covered by scan.** A scan covers the threat. The scan result is listed.
- **Open.** No test or scan covers the threat today, or a test covers it and the result is not a pass. The row names a backlog id.

## Boundaries

The boundary list is from `docs/09-ai-guardrails/trust-boundary-diagram.md`.

| Boundary | From | To | Control named in the diagram |
|---|---|---|---|
| B1 | Caller | Route | Role check |
| B2 | Route | Retrieved record | Missing id and stale flag |
| B3 | Retrieved record | Prompt builder | Allow list |
| B4 | Prompt builder | Model | Timeout |
| B5 | Model | Output validator | Schema |
| B6 | Output validator | Policy | Policy outcome |
| B7 | Policy | Approval | Approval id |
| B8 | Approval | Audit | Provenance |
| B9 | Audit | Device change | Four gates |

## STRIDE per boundary

### B1 Caller to route

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B1-01 | S | A caller types a role word they do not hold. | None. The route trusts the header. | **Verified Fact.** `main.py` reads `X-User-Role` and nothing else. | Open. `SB-09` |
| T-B1-02 | S | A call with no role header on `GET /records/{id}` is treated as `operator`. | None. `Header(default="operator")`. | **Verified Fact.** `test_negative_access.py::test_missing_role_header_keeps_operator_default` shows HTTP 200. | Open. `SB-01`, `SB-02` |
| T-B1-03 | S | A call with no role header on `POST /ai/summarize/{id}`. | The route denies it with 403 and writes a `policy.deny` row. | **Verified Fact.** `test_ai_summarize_refuses_request_with_no_role_header`. | Covered by test. `SV-04` |
| T-B1-04 | E | A role with no matrix row (`clinician`, `admin`, `vendor`, `automation_service`) reads a record. | The policy matrix denies the role. | **Verified Fact.** `test_record_route_denies_with_403_and_audit_row[...]`; `test_clinician_role_is_denied_on_record_read`; `test_admin_has_no_blanket_access`. | Covered by test. `SV-01`, `SV-02` |
| T-B1-05 | E | A caller without recommend permission uses the AI route. | The policy denies the call before the model. | **Verified Fact.** `test_gr06_caller_without_recommend_permission_is_blocked`. | Covered by test. `SV-05` |
| T-B1-06 | E | The AI agent asks to execute. | No route executes. The target decision is deny. | **Verified Fact.** `test_ai_agent_may_not_execute`; `test_no_route_can_execute`. | Covered by test. `SV-20` |
| T-B1-07 | R | A denied call leaves no record. | Every deny writes one `policy.deny` row. | **Verified Fact.** The same tests assert `[row["action"] for row in rows] == ["policy.deny"]`. | Covered by test. `SV-01` |
| T-B1-08 | I | A record read returns `mgmt_ip` and `credential_profile` to every allowed role and to a no-header caller. | None. | **Verified Fact.** Defect F10; `SB-06`. | Open. `SB-06` |
| T-B1-09 | D | A flood of calls, or a very long header, slows the service. | None for rate. A length limit does not exist. | **Inference.** No rate limit in `main.py`. | Open. `SB-13` |
| T-B1-10 | Unknown | A known advisory in the web framework (Starlette 7 advisories) or the test tool. | `pip-audit` finds it. | **Verified Fact.** `evidence/pip-audit.json`: 9 advisories on 3 packages. The advisory text has not been read, so the STRIDE letter is **Unknown**. This row has no letter. | Covered by scan, finding open. `BL-11` |

STRIDE letters with no threat listed for B1: T. **Inference:** the starting point of a change to data is the record store (B2). The B1 header text is covered at B8 (`T-B8-05`).

### B2 Route to retrieved record

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B2-01 | T | The summary route is asked about an id that does not exist, and a different row is summarized. | The route and policy return BLOCK with `failmode.missing_id`. | **Verified Fact.** `test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row`. | Covered by test. `SV-17` |
| T-B2-02 | T | `GET /records/{id}` with a missing id returns the first row. | None. | **Verified Fact.** `test_missing_id_returns_first_row`. Defect F01. | Open. `SB-07` |
| T-B2-03 | E | A recommendation is made from a device row marked stale. | A true stale flag is BLOCK before the model. | **Verified Fact.** `test_gr03_stale_flag_true_is_blocked_before_the_model`. | Covered by test. `SV-16` |
| T-B2-04 | T | A blank or missing stale flag is read as "not stale". | A blank or missing flag is HOLD_FOR_REVIEW. | **Verified Fact.** `test_gr08_blank_or_missing_stale_flag_is_held_before_the_model`. | Covered by test. `SV-16` |

STRIDE letters with no threat listed for B2: S, R, I, D. **Inference:** the boundary reads one row by key from a file inside the process.

### B3 Retrieved record to prompt builder

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B3-01 | T | Instruction text in `hostname` is treated as an order. | The text is data inside the allow-listed prompt. The outcome comes from the policy. | **Verified Fact.** `test_gr01_instruction_in_hostname_is_data_and_not_execute`. | Covered by test. `SV-07` |
| T-B3-02 | I | `mgmt_ip` or `credential_profile` reaches the prompt. | Allow-list builder. A forbidden value in the prompt is BLOCK. | **Verified Fact.** `test_gr02_prompt_has_only_allowed_fields`; `test_gr02_every_device_row_builds_a_clean_prompt`; `test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked`. | Covered by test. `SV-08` |
| T-B3-03 | I | A forbidden name sits inside an allowed field. | Blocked when the name is a forbidden credential name. | **Verified Fact.** `test_gr02_a_forbidden_name_inside_an_allowed_field_is_blocked`. | Covered by test. `SV-08` |
| T-B3-04 | I | A secret value typed into an allowed field, or the service-order `customer_id`, enters the prompt. | None. | **Verified Fact.** `find_forbidden` docstring. `SF-04`. | Open. `SB-14` |
| T-B3-05 | D | A very long cell makes a very long prompt. | None. | **Inference.** No length cut in the prompt builder. | Open. `SB-13` |

STRIDE letters with no threat listed for B3: S, R. **Inference:** the boundary is a function call inside one process.

### B4 Prompt builder to model

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B4-01 | D | The model does not answer. | A deadline. The call returns HOLD_FOR_REVIEW. | **Verified Fact.** `test_gr05_timeout_is_held_with_no_summary`. | Covered by test. `SV-19` |
| T-B4-02 | D | Many calls reach the model at once. | An in-flight limit and a circuit breaker. | **Verified Fact.** `test_many_threads_never_go_past_the_in_flight_limit`. | Covered by test. `SV-19` |
| T-B4-03 | R | The prompt text is stored where a reader can see it, or no trace of the prompt exists. | The row holds the SHA-256 hash. The text is not stored. | **Verified Fact.** `test_gr11_audit_row_has_provenance_and_no_prompt_text`. | Covered by test. `SV-22` |
| T-B4-04 | I | Prompt text leaves the process for a hosted model. | None. The stub sends nothing out. | **Inference.** `local-sim-v1` is a stub. | Open. `SB-15` |
| T-B4-05 | S | A different model answers under the same name. | None. The name and version have the same value. | **Verified Fact.** `ai_gateway.py` lines 48 and 50. | Open. `SB-15` |
| T-B4-06 | I | The model key is written in a committed file. | The secret-pattern test reads code, config, and test files. | **Verified Fact.** `test_repo_has_no_secret_patterns`. Half B: the scan tests the path below the repo root (`SB-18` closed), and `test_docs_have_no_real_secret_formats` scans `docs/` for real key formats (`BL-03` closed). A password written in plain prose in a document is not found. | Covered by test. `SV-09` |

STRIDE letters with no threat listed for B4: E.

### B5 Model to output validator

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B5-01 | T | The model answer is malformed or missing a field. | The answer is discarded. The route returns HOLD_FOR_REVIEW and no summary. | **Verified Fact.** `test_gr04_malformed_model_output_is_held_with_no_summary` (10 cases). | Covered by test. `SV-18` |
| T-B5-02 | E | The model answer sets its own outcome to EXECUTE. | The schema refuses the word. The policy ignores the model's outcome. | **Verified Fact.** `test_gr01_a_model_that_obeys_the_injection_is_held[model-sets-execute]`; `test_the_model_cannot_set_its_own_outcome`. | Covered by test. `SV-07`, `SV-11` |
| T-B5-03 | E | An execute verb in the recommendation text. | One command sentence is detected. | **Verified Fact.** `test_gr07_execute_sentence_with_outcome_execute_is_held`. Probe 2: a different command sentence passed. | Covered by test for one sentence. The wider gap is open. `SB-05` |
| T-B5-04 | I | The answer repeats `mgmt_ip` or a credential name. | The prompt is checked. The answer is not. | **Verified Fact.** Probe 2. | Open. `SB-04` |

STRIDE letters with no threat listed for B5: S, R, D. D is covered at B4.

### B6 Output validator to policy

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B6-01 | T | A caller sends `approval_required` as false, or as the string `"true"`. | The policy ignores caller values and requires a Boolean true from the gateway. | **Verified Fact.** `test_one_missing_check_stops_execute_each_time`; `test_invalid_values_block[changes7]`. | Covered by test. `SV-13` |
| T-B6-02 | T | The route reads `approval_required` from the request. | Not read. | **Inference.** `main.py` does not read the field. No test sends it to the route today. | Covered by test. `NG-02`: `test_client_sent_policy_fields_change_nothing`; `test_no_route_reads_an_approval_id_from_the_caller`. Passed 2026-10-11 (S05-13 Half B). |
| T-B6-03 | T | The Python and Rego copies of the policy give different answers. | Two tests compare the copies on every input. | **Verified Fact.** Half B: `test_opa_and_python_agree_on_access` and `test_opa_and_python_agree_on_every_ai_action_combination` ran and passed with `opa` 1.21.1 (`evidence/junit-security.xml`, `skipped="0"`). Before Half B both skipped. | Covered by test. `SV-15`. The skip guard (`SB-10`) fails the stage if they skip again. |
| T-B6-04 | D | The policy engine fails. | The call is denied. | **Verified Fact.** `test_engine_failure_denies`. | Covered by test. `SV-21` |
| T-B6-05 | T | The code that starts the `opa` program takes unsafe input. | A fixed command, with the input sent on standard input. | **Verified Fact.** `evidence/bandit.json`: `B404` and `B603`, both LOW. **Inference:** the command is fixed. | Covered by scan, finding open. `BL-12` |

STRIDE letters with no threat listed for B6: S, R, I, E. E is covered at B7 and B9.

### B7 Policy to approval

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B7-01 | E | EXECUTE is reached with no approval id. | EXECUTE needs a non-empty approval id. | **Verified Fact.** `test_execute_is_unreachable_without_an_approval_id` (8 values); `test_remediation_does_not_become_a_change_without_approval_id_deny`. | Covered by test. `SV-06` |
| T-B7-02 | E | The automation account executes without an approval id. | The target decision is deny. | **Verified Fact.** `test_automation_service_may_not_execute_without_approval_id`. | Covered by test. `SV-06` |
| T-B7-03 | S | A made-up approval id is accepted. | Only "non-empty" is checked. No approval store exists. | **Verified Fact.** `policy.py` `_approval_id_present`; `AA-02`. | Open. `SB-08` |
| T-B7-04 | R | A held recommendation has no named reviewer on record. | None. | **Verified Fact.** `AA-09`. | Open. `SB-08` |

STRIDE letters with no threat listed for B7: T, I, D.

### B8 Approval to audit

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B8-01 | R | An audit row has no `correlation_id`. | The app makes a UUID when the header is missing. `write_event` refuses an empty id. | **Verified Fact.** `test_every_audit_row_has_every_required_field`; `test_request_without_header_gets_a_uuid`; `test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it`. | Covered by test. `SV-12` |
| T-B8-02 | R | `write_event` accepts an empty `correlation_id` from code. | `write_event` raises. | **Verified Fact.** `test_write_event_refuses_an_empty_correlation_id` (3 inputs). Passed 2026-10-11 (S05-13 Half B). | Covered by test. `NG-01` |
| T-B8-03 | I | `mgmt_ip`, `credential_profile`, or a password is written to the audit log by the app. | Rows hold no prompt text and no forbidden value. | **Verified Fact.** `test_gr11_audit_row_has_provenance_and_no_prompt_text`; `test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked`. | Covered by test. `SV-14` |
| T-B8-04 | I | A forbidden name is already in the real `logs/audit.log`. | A test checks rows written during the test only. | **Verified Fact.** `test_real_audit_log_holds_no_forbidden_name` reads the real `logs/audit.log`. Passed 2026-10-11 (S05-13 Half B). | Covered by test. `NG-03` |
| T-B8-05 | T | A caller's header text (a forbidden name, or 5000 characters) is stored whole. | None. | **Verified Fact.** Probe 1. | Open. `SB-03` |
| T-B8-06 | T | Someone with file access edits or deletes lines. | None. | **Verified Fact.** `audit.py` appends to a plain file. | Open. `SB-12` |
| T-B8-07 | R | 96 old lines have no `correlation_id`. | New rows have one. | **Verified Fact.** Probe 1: 240 lines, 96 with 3 keys. | Open. `SB-12` |
| T-B8-08 | S | The `role` in a row is the caller's claim, not a proven identity. | None. | **Verified Fact.** Same as `T-B1-01`. | Open. `SB-09` |
| T-B8-09 | R | A model call has no provenance. | The row holds model, model version, prompt hash, tokens, latency, outcome. | **Verified Fact.** `test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text`; `test_gr11_*`. | Covered by test. `SV-22` |

STRIDE letters with no threat listed for B8: D. **Unknown:** what happens when the log file grows without a limit.

### B9 Audit to device change

| Id | STRIDE | Threat | Control today | Evidence | Status |
|---|---|---|---|---|---|
| T-B9-01 | E | A route exists that can change a device. | None exists. | **Verified Fact.** `test_no_route_can_execute`. | Covered by test. `SV-20` |
| T-B9-02 | E | An AI recommendation becomes a change without the four gates. | The route returns text and the code has no path to a change. | **Verified Fact.** `test_gr07_response_type_and_routes_cannot_express_execute`; `test_execute_is_reached_by_exactly_the_all_checks_inputs` (2 of 82,944 inputs). | Covered by test. `SV-06`, `SV-11` |
| T-B9-03 | E | A secret for a device login sits in a committed file. | The legacy script reads its password from the environment. The pattern test passes. | **Verified Fact.** `test_legacy_script_reads_password_from_environment`; `test_repo_has_no_secret_patterns`. | Covered by test. `SV-09` |
| T-B9-04 | S | A removed credential is not replaced where it was used. | None known. | **Unknown.** Rotation store (`SB-17`). | Open. `SB-17` |

STRIDE letters with no threat listed for B9: T, R, I, D. **Inference:** no change route exists, so these threats start when S07 adds one.

### Count

| Status | Count | Rows |
|---|---|---|
| Covered by test | 32 | `T-B1-03`, `04`, `05`, `06`, `07`; `T-B2-01`, `03`, `04`; `T-B3-01`, `02`, `03`; `T-B4-01`, `02`, `03`, `06`; `T-B5-01`, `02`, `03`; `T-B6-01`, `02`, `03`, `04`; `T-B7-01`, `02`; `T-B8-01`, `02`, `03`, `04`, `09`; `T-B9-01`, `02`, `03` |
| Covered by scan, finding open | 2 | `T-B1-10` (`BL-11`), `T-B6-05` (`BL-12`) |
| Open | 17 | `T-B1-01`, `02`, `08`, `09`; `T-B2-02`; `T-B3-04`, `05`; `T-B4-04`, `05`; `T-B5-04`; `T-B7-03`, `04`; `T-B8-05`, `06`, `07`, `08`; `T-B9-04` |

**Worked example.** `T-B1-04` says a role with no matrix row cannot read a record. `test_record_route_denies_with_403_and_audit_row[clinician]` sends a record read with `X-User-Role: clinician`. It asserts HTTP 403, the body `{"error": "forbidden"}`, and one `policy.deny` audit row. The test ties the control to one role. The roles `admin`, `automation_service`, and `vendor` have the same test, so the control is shown for four roles.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| TM-01 | Every boundary has at least one threat with a status. | **Verified Fact.** The tables above. | Gate 1 of Half A: every STRIDE threat has a status. | Every boundary has letters with no threat listed. Each boundary section names those letters and the reason. | Medium | None. |
| TM-02 | The two highest-risk open threats are `T-B1-01` (the role is a typed word) and `T-B1-02` (no header means `operator`). | **Verified Fact.** `SB-09`; `SB-01`. | Every access test proves the policy for a stated role. None proves the caller holds that role. | High if the app is reachable by more than the team. | Medium | Whether the packet wants authentication is Unknown. |
| TM-03 | The Python-versus-Rego threat (`T-B6-03`) now has a pass on this machine (Half B). With `opa` on the PATH the app answers about 15 times slower (`SB-20`). | **Verified Fact.** `evidence/junit-security.xml`; `docs/13-security-validation/evidence.md` EV-01. | The Rego copy is the policy of record, and it now runs. | Medium. The slow path is a denial-of-service risk (`T-B1-09`). | High | None. |
| TM-04 | The audit log has no tamper check, 96 old lines have no correlation id, and no tamper check exists. `NG-03` ran and passed (Half B). | **Verified Fact.** `T-B8-06`, `07`. | A reader cannot prove the log is complete. | Medium. | High | None. Stage S05-14 is the audit chain. |

## Known Brownfield Concerns

These six names are the starter's list. Each now has a status.

| Concern | Where it sits | Status | Evidence |
|---|---|---|---|
| alarm_storms | B1 (flood of calls) and a future batch route | Open. `SB-13` | No route for storm batches exists yet (`GET /alarms/storms/{storm_batch_id}` is for S07). |
| static_ssh_credentials | B9 and B4 | Covered by test for committed secrets. Rotation is open. `SB-17` | `test_legacy_script_reads_password_from_environment`; `test_repo_has_no_secret_patterns`. |
| stale_topology | B2 | Covered by test. `SV-16` | `test_gr03_*`; `test_gr08_*`. |
| risky_ai_config_suggestion | B5 and B9 | Covered by test for one sentence. The wider gap is open. `SB-05` | `test_gr07_*`. |
| duplicate_tickets | Not on a boundary. No route creates a ticket today. | Open. `SB-19` | **Verified Fact.** The app has 3 routes: `/health`, `GET /records/{id}`, and `POST /ai/summarize/{id}`. |
| overpowered_automation_account | B7 | Covered by test. `SV-06` | `test_automation_service_may_not_execute_without_approval_id`; `test_policy_python.py::test_record_route_denies_with_403_and_audit_row[automation_service]`. |

## MAESTRO

Open question for S03: the MAESTRO letters and layers have no id and no definition in the YAML. This file does not map to MAESTRO and does not expand the letters. Stage S03 must give the list before a map is written.

## Expected Participant Work

Starter text: "Map these to STRIDE/MAESTRO, add controls, tests, and evidence."

Done in S05-13 Half A: STRIDE map, status per threat, the evidence list, and the backlog. Done in S05-13 Half B: the negative tests `NG-01` to `NG-04` and the `opa` pass. Left for S03: the MAESTRO list.
