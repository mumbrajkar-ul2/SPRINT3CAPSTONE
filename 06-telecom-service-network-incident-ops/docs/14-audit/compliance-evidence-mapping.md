# Compliance evidence mapping

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Five control areas are mapped: identity, secrets, policy, AI, and audit. 34 duties each name a stored evidence file, a place to find it, and a test file and test name where a test proves it. Each limit names a backlog id or a finding id. Two duties fail today and are listed as failures (`SB-01`, `SB-06`). |
| Evidence sources | `docs/04-secrets/evidence.md`; `docs/06-policy/evidence.md`; `docs/08-observability/evidence.md`; `docs/09-ai-guardrails/evidence.md`; `docs/11-reliability/recovery-evidence.md`; `docs/12-finops/evidence.md`; `docs/13-security-validation/evidence.md`; `docs/13-security-validation/abuse-case-evidence.md`; `docs/13-security-validation/remediation-backlog.md`; `security/threat-model.md`; `evidence/junit-security.xml` (159 tests, 0 skipped, run 2026-10-11 23:06 local time); `How the product spine addresses the 16 challenges - plain speak.md` (section 14); `docs/00-contract/challenge-to-spine-crosswalk.md` (row `docs/14-audit/`, verdict Partial) |
| Assumptions | A test name that appears in `evidence/junit-security.xml` with no failure and no skip is a Verified Fact for the run of 2026-10-11 on one Windows machine. A test outside that file is a Verified Fact only for the run the named evidence file records. This stage reran no test. |
| Unresolved issues | The five control areas are the ones named in the playbook for this stage: identity (challenge 3), secrets (4), policy (6), AI (9), and audit (14). The other 11 challenges are not mapped here. |
| Residual risks | A passing test proves the control for the inputs the test uses. It does not prove that no other input gets through. Every grant in the access matrix is PROPOSED. Owner: Team-Force. |

## What this file is

This file answers one question per duty: "Where is the stored evidence that this duty is met?" A reviewer reads a row, opens the file in the third column, and finds the proof.

Stage S09 uses this file as the index of the evidence pack.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## How to read a row

| Column | Meaning |
|---|---|
| Duty | One thing the system must do. |
| Stored evidence | The document that records the proof. |
| Where to find it | The section or line a reviewer opens. |
| Test | `file::test_name`, from the repo root of `06-telecom-service-network-incident-ops/`. |
| In `junit-security.xml` | Yes means the test is in the security run of 2026-10-11. No means the proof is in the named evidence file only. |
| Limit | What the proof does not cover. A backlog id (`SB-nn`, `BL-nn`) or a finding id from this stage. |

Worked example. Duty: "A role with no matrix row cannot read a device record." The stored evidence is `docs/13-security-validation/abuse-case-evidence.md`. Row `SV-01` there names the test `policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[clinician]`. That test sends `X-User-Role: clinician`. It asserts HTTP 403, the body `{"error": "forbidden"}`, and one audit row with the action `policy.deny`. The test is in `junit-security.xml`. The limit is `SB-09`: the role is a word the caller types.

## 1. Identity (Challenge 3)

| Duty | Stored evidence | Where to find it | Test | In `junit-security.xml` | Limit |
|---|---|---|---|---|---|
| A role with no matrix row cannot read a device record. | `abuse-case-evidence.md` row `SV-01`, `SV-02` | Table "Evidence by row" | `policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[clinician]`, `[admin]`, `[automation_service]`, `[vendor]`; `tests/access/test_negative_access.py::test_clinician_role_is_denied_on_record_read` | Yes | `SB-09`. Grants are PROPOSED. |
| `admin` has no blanket access. | `docs/06-policy/evidence.md` | "Routes through the opa engine" | `policy/tests/test_policy_python.py::test_admin_has_no_blanket_access` | Yes | None. |
| A summary request with no role header is refused and audited. | `abuse-case-evidence.md` row `SV-04` | "Evidence by row" | `tests/characterization/test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header`; `policy/tests/test_policy_python.py::test_summarize_route_denies_roles_without_a_row[None]` | Yes | `SB-01`. |
| Each matrix row allows only its own six fields. | `docs/03-identity/target-access-matrix.md`; `policy/opa/policy_data.json` | Rows TA-01 to TA-34 | `policy/tests/test_policy_python.py::test_every_matrix_row_is_allowed_with_its_own_fields`; `::test_changing_any_one_field_of_a_row_denies` | Yes | Rows are PROPOSED. Owner: Team-Force. |
| A call with no role header on `GET /records/{id}` is still treated as `operator`. | `remediation-backlog.md` `SB-01` | "Gaps that stop a test from showing a deny" | `tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default` (documents the gap) | Yes | Open. This is a known failure of the duty, not a proof. |
| The AI agent may not execute. | `abuse-case-evidence.md` row `SV-20` | "Evidence by row", and finding `AE-04` | `policy/tests/test_policy_python.py::test_no_route_can_execute`. `tests/access/test_negative_access.py::test_ai_agent_may_not_execute` calls a stand-in function. | Yes | Cite the policy test. The stand-in is not policy evidence (`AE-04`). |
| A denied call is stored. | `docs/08-observability/evidence.md` | "The four S00 calls" | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | Yes | The row holds `policy_decision` null (finding `AG-02`). |

## 2. Secrets (Challenge 4)

| Duty | Stored evidence | Where to find it | Test | In `junit-security.xml` | Limit |
|---|---|---|---|---|---|
| No secret value in committed code or `.env.example`. | `docs/04-secrets/evidence.md` | "Pattern test on the cleaned repo" and "after a known string is put back" | `tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns` | Yes | The old password and old key stay in git history. |
| No real key format in `docs/`. | `docs/13-security-validation/evidence.md` | Section on `BL-03` | `tests/security/test_docs_secret_scan.py::test_docs_have_no_real_secret_formats` | Yes | A password written in plain prose is not found (`BL-03`). |
| The scanner finds a planted value and ignores the placeholder. | `docs/13-security-validation/evidence.md` | Section on `SB-18` | `tests/security/test_secret_detector.py::test_secret_scan_finds_planted_values_and_ignores_the_placeholder`; `::test_secret_scan_reads_files_when_a_parent_folder_is_named_docs` | Yes | None. |
| The legacy script reads its password from the environment. | `docs/04-secrets/evidence.md` | "What the runs show" | `tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment` | Yes | Where a rotation is recorded is Unknown (`SB-17`). |
| The audit log holds no forbidden name. | `security/threat-model.md` `T-B8-03`, `T-B8-04` | Section "B8 Approval to audit" | `tests/security/test_audit_log_security.py::test_real_audit_log_holds_no_forbidden_name`; `::test_forbidden_name_finder_finds_a_planted_name` | Yes | `SB-03`: header text is stored unchanged, with no length limit. |
| The prompt holds only allowed fields. | `docs/09-ai-guardrails/evidence.md` | "What changed" | `tests/ai/test_guardrails.py::test_gr02_prompt_has_only_allowed_fields` | Yes | `SB-14`. |
| `mgmt_ip` and `credential_profile` stay out of the response. | `remediation-backlog.md` `SB-06` | "Gaps in what the app does" | None. The duty fails today. `GET /records/{id}` returns both cells to every allowed role. | No | Open. `SB-06`. |

## 3. Policy (Challenge 6)

| Duty | Stored evidence | Where to find it | Test | In `junit-security.xml` | Limit |
|---|---|---|---|---|---|
| The Rego policy and the Python policy give the same answer on every input tested. | `docs/06-policy/evidence.md`; `evidence/opa-test.json` (30 of 30) | "Rego and Python agree" | `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access`; `::test_opa_and_python_agree_on_every_ai_action_combination` | Yes | `SB-20`: with `opa` on the PATH, each decision is slow. The tests use the Python copy by default. |
| EXECUTE is unreachable without an approval id. | `abuse-case-evidence.md` row `SV-06` | "Evidence by row" and the worked example | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` (8 values); `::test_execute_is_reached_by_exactly_the_all_checks_inputs`; `::test_remediation_does_not_become_a_change_without_approval_id_deny` | Yes | `SB-08`: an approval id is checked for presence only. |
| No route can execute. | `docs/06-policy/evidence.md` finding `HB-04` | "Findings" | `policy/tests/test_policy_python.py::test_no_route_can_execute` | Yes | The test checks route paths only. |
| A policy engine failure denies. | `abuse-case-evidence.md` row `SV-21` | "Evidence by row" | `policy/tests/test_policy_python.py::test_engine_failure_denies` | Yes | None. |
| A client cannot send a policy field. | `abuse-case-evidence.md` Half B update, row `SV-24` | "Half B update" | `tests/security/test_client_flags_ignored.py::test_client_sent_policy_fields_change_nothing`; `::test_no_route_reads_an_approval_id_from_the_caller` | Yes | None. |
| A refusal is stored with the answer. | `docs/06-policy/evidence.md` | "Routes through the opa engine" | `policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row[clinician]` | Yes | The row stores the action word `policy.deny`. `policy_decision` is null (`AG-02`). |

## 4. AI (Challenge 9)

| Duty | Stored evidence | Where to find it | Test | In `junit-security.xml` | Limit |
|---|---|---|---|---|---|
| Instruction text in a field is data and never EXECUTE. | `abuse-case-evidence.md` row `SV-07` | "Evidence by row" | `tests/ai/test_guardrails.py::test_gr01_instruction_in_hostname_is_data_and_not_execute` | Yes | `SB-05`: one command sentence is detected. |
| A true or blank stale flag stops the call before the model. | `abuse-case-evidence.md` row `SV-16` | "Evidence by row" | `tests/ai/test_guardrails.py::test_gr03_stale_flag_true_is_blocked_before_the_model`; `::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model[blank]` | Yes | None. |
| A bad model answer is held with no summary. | `abuse-case-evidence.md` row `SV-18` | "Evidence by row" | `tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary[not-json]` (10 cases) | Yes | `SB-04`: the answer is not checked for forbidden values. |
| A slow model is held at the timeout. | `docs/11-reliability/recovery-evidence.md` row `DR-2` | Section "Drills" | `tests/ai/test_guardrails.py::test_gr05_timeout_is_held_with_no_summary` (in the run); `tests/reliability/test_drills.py::test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up` | The first: Yes. The second: No. | The 10-second default is PROPOSED. Owner: Team-Force. |
| Every path returns a policy outcome. | `abuse-case-evidence.md` row `SV-22` | "Evidence by row" | `tests/ai/test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text` | Yes | None. |
| A model call is stored with model, hash, and tokens, and no prompt text. | `docs/09-ai-guardrails/evidence.md`; `security/threat-model.md` `T-B4-03`, `T-B8-09` | "Before and after" | `tests/ai/test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text` | Yes | Version equals name (`SB-15`). The model is a stub. Its text is SIMULATED. |
| Token and cost figures are labelled as estimates. | `docs/12-finops/evidence.md` | Status line and "Assumptions" | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` (asserts `token_estimate_method`); `tests/finops/test_metrics_from_audit.py` | The first: Yes. The second: No. | Every token number is EDUCATIONAL. |

## 5. Audit (Challenge 14)

| Duty | Stored evidence | Where to find it | Test | In `junit-security.xml` | Limit |
|---|---|---|---|---|---|
| Every new row has the 15 keys and a `correlation_id`. | `docs/08-observability/evidence.md`; `abuse-case-evidence.md` row `SV-12` | "What the file holds after this half" | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | Yes | 96 old lines have 3 keys (`AG-01`). |
| A sent id is kept. A missing or blank id becomes a UUID. | `docs/08-observability/evidence.md` | "Done test" | `tests/observability/test_audit_schema.py::test_request_with_header_keeps_the_id`; `::test_request_without_header_gets_a_uuid`; `tests/reliability/test_drills.py::test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it` | The first two: Yes. The third: No. | A 500 response has no id (`RF-04`). The caller chooses the id (`AG-05`). |
| The writer refuses an empty id. | `abuse-case-evidence.md` row `SV-23` | "Half B update" | `tests/security/test_audit_log_security.py::test_write_event_refuses_an_empty_correlation_id[]`, `[   ]`, `[None]` | Yes | None. |
| Eight threads writing at once lose no row. | `docs/11-reliability/recovery-evidence.md` | Section on the audit write lock | `tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row` | No | One process only. Two server processes share the file with no lock (`SB-12`). |
| The log has no prompt text and no forbidden value. | `abuse-case-evidence.md` row `SV-14` | "Evidence by row" | `tests/ai/test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text`; `tests/security/test_audit_log_security.py::test_real_audit_log_holds_no_forbidden_name` | Yes | `SB-03`. |
| A threat at B8 is covered or open. | `security/threat-model.md` | Section "B8 Approval to audit" | Covered by test: `T-B8-01`, `02`, `03`, `04`, `09`. Open: `T-B8-05`, `06`, `07`, `08`. | Mixed | The four open rows are the gaps in `audit-gap-report.md`. |
| One case can be rebuilt from stored rows by id. | `docs/14-audit/evidence-chain-one-case.md` (Half A, by hand). Half B adds the route. | The chain section | Half B: `tests/audit/test_audit_rebuild.py` (not written yet) | No | Log integrity and completeness cannot be proven (`SB-12`). |

## Evidence file index

Each evidence file the stage names, with the control areas it supports.

| File | Stage | Areas | What a reviewer finds |
|---|---|---|---|
| `docs/04-secrets/evidence.md` | S04-04 | Secrets | The before and after pytest runs and the failing run with a planted value. |
| `docs/06-policy/evidence.md` | S04-06 | Identity, policy | Test counts, the Rego checks, the engine agreement run, and the routes through the opa engine. |
| `docs/08-observability/evidence.md` | S04-08 | Audit | The four S00 calls, the old line and the new line for each. |
| `docs/09-ai-guardrails/evidence.md` | S04-09 | AI, audit | The old and new summary response and the new audit row. |
| `docs/11-reliability/recovery-evidence.md` | S04-11 | AI, audit | The drills, the audit write lock test, and the 500 case. |
| `docs/12-finops/evidence.md` | S04-12 | AI, audit | The 15th key, `token_estimate_method`, and the token labels. |
| `docs/13-security-validation/evidence.md` | S05-13 | All five | The security run, 159 tests, 0 skipped, and the probes. |
| `docs/13-security-validation/abuse-case-evidence.md` | S05-13 | All five | One row per abuse case with the test name and the assertion. |
| `docs/13-security-validation/remediation-backlog.md` | S05-13 | All five | Every open gap with an owner. |
| `security/threat-model.md` | S05-13 | All five | Threats by boundary. B8 covers audit. |
| `evidence/junit-security.xml` | S05-13 | All five | The machine-readable result of the 159 tests. |

## Gaps no stored evidence closes

| Gap | Area | Id |
|---|---|---|
| The role is a typed word. | Identity, audit | `SB-09` |
| `mgmt_ip` and `credential_profile` go to every allowed role. | Secrets, identity | `SB-06` |
| The log is a plain file and can be edited. | Audit | `SB-12` |
| The log is tracked by git, and test runs add rows. | Audit | `BL-09` |
| Header text is stored whole. | Audit, secrets | `SB-03` |
| No approval store exists. | Policy, audit | `SB-08` |
| The model is a stub. | AI | `SB-15` |
| The record id and the reasons are not on the row. | Audit | `AG-02`, `AG-03` |
| The 500 error has no id and no row. | Audit | `RF-04` |
| The access grants are PROPOSED and not accepted in writing. | Identity, policy | `docs/03-identity/target-access-matrix.md` |
| Nobody can read the audit log through the app. | Audit | `audit-read-access-design.md` |

## Findings

### CE-01

| | |
|---|---|
| Finding | All five control areas have stored evidence with a test name. The audit area has a rebuild test only after Half B. |
| Evidence | **Verified Fact.** The five tables above name 40 test functions. Every name exists in the repo. 37 are in `evidence/junit-security.xml`. The other 3 are in `tests/reliability/` and are recorded in `docs/11-reliability/recovery-evidence.md`. A read-only script checked the names on 2026-10-12. |
| Impact | A reviewer can follow any row to a file and a test. |
| Risk | Low for the rows with a passing test. Medium for the duties marked "No" in the junit column, because the proof is in an evidence file and not in the machine-readable run. |
| Confidence | High |
| Open questions | None. |

### CE-02

| | |
|---|---|
| Finding | Two duties are listed as known failures and not as proofs: no default role on `GET /records/{id}` (`SB-01`), and no `mgmt_ip` or `credential_profile` in the response (`SB-06`). |
| Evidence | **Verified Fact.** `remediation-backlog.md`. `test_missing_role_header_keeps_operator_default` passes because it documents the gap. |
| Impact | A reviewer who reads only the test name `test_missing_role_header_keeps_operator_default` could take the passing test as a proof of the duty. |
| Risk | Medium. |
| Confidence | High |
| Open questions | None. |

### CE-03

| | |
|---|---|
| Finding | The audit area cannot prove completeness or integrity. No test covers them. |
| Evidence | **Verified Fact.** `SB-12`. `T-B8-06`. `T-B8-07`. |
| Impact | A claim "every decision is in the log" has no proof. |
| Risk | Medium. |
| Confidence | High |
| Open questions | None. A database or an external store is PROPOSED only. |

## Lifecycle

Stage S09 uses this file as the index of the pack. Half B adds one row to the audit table for the route test and updates the junit counts. Stage S05R folds the open questions into the YAML.
