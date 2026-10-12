# Negative tests

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A |
| Date / version | 2026-10-11, v1.0. v1.1 after S05-13 Half B: all four designs are written and pass. See `evidence.md` sections 3 and 4. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Four test designs, one for each row marked "no" in `security-test-suite-plan.md` (`SV-23` to `SV-26`). Each design names its input, the expected status, and the expected audit row. Three backlog rows have no test design, because the repo has no control to prove (`SV-03`, `SV-10`, `SV-27`). |
| Evidence sources | `security-test-suite-plan.md`; `apps/api/services/audit.py` lines 82 and 83; `apps/api/main.py`; `tests/security/test_secret_patterns.py`; `semantic-layer/ai-context-policy.yaml` (`forbidden_credential_names`); three read-only probes on 2026-10-11 (see `security-test-suite-plan.md`, "Probes") |
| Assumptions | The tests go under `tests/security/` and carry `@pytest.mark.security`. Each test points the audit log at a temporary file with `monkeypatch.setattr(audit, "LOG", ...)`, except `NG-03`, which reads the real file. No test skips and none is marked expected-to-fail. |
| Unresolved issues | The tests are designs. None is written, so none has run. Each "expected" value below comes from a probe or from reading the code. It is not a test result. |
| Residual risks | A test that passes today shows the control works today. It does not show the control cannot be removed. Each design has a proof run that removes the control and checks that the test fails. |

## What this file is

This file says what Half B writes for the four rows that have a control and no test. Each design has the input, the expected HTTP status, the expected audit row, and a proof run.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

How the tests avoid a false pass. Each one asserts a positive fact first (for example, that the scan read at least one file). A test that only asserts "nothing was found" can pass when nothing was looked at.

## NG-01 — `write_event` refuses an empty correlation id

| Field | Value |
|---|---|
| Plan row | `SV-23` |
| New test file | `tests/security/test_audit_log_security.py`, test `test_write_event_refuses_an_empty_correlation_id` |
| Input | `audit.write_event("record.read", correlation_id=value, actor=None, role=None, resource="resource.device")` for `value` in `""`, `"   "`, and `None`. The audit log is a temporary file that does not exist yet. |
| Expected status | Not an HTTP call. Each call raises `ValueError` with the message `correlation_id is required`. |
| Expected audit row | None. The temporary log file does not exist after the three calls. |
| Also asserts | One call with `correlation_id="demo-123"` appends exactly one row whose `correlation_id` is `demo-123`. This proves the log path works, so "no file" is not an accident of the setup. |
| Control it proves | `audit.py` lines 82 and 83. `rule.audit_row_names_actor_and_correlation`. |
| Expected today | **Verified Fact (probe 3).** All three values raised `ValueError`. No log file was created. |
| Proof run | In a scratch copy, delete the `if correlation_id is None ...` check. The test fails because a row is written. Restore the check. |

Worked example. A code change adds a new route and forgets to pass the id. Without the check, the route writes a row with `correlation_id` null, and `SV-12` still passes, because `SV-12` only drives the existing routes. `NG-01` fails at the function, before any route can use it.

## NG-02 — Client-sent policy fields are ignored

| Field | Value |
|---|---|
| Plan row | `SV-24` |
| New test file | `tests/security/test_client_flags_ignored.py`, test `test_client_sent_policy_fields_change_nothing` |
| Input A | `POST /ai/summarize/REC-0001` with header `X-User-Role: operator` and JSON body `{"approval_required": false, "approval_id": "APR-FORGED-1", "outcome": "EXECUTE", "policy_result": "allow", "audit_row_written": true, "change_plan_ok": true}`. |
| Input B | The same route with the query string `?approval_id=APR-FORGED-1&approval_required=false&outcome=EXECUTE`. |
| Input C | `GET /records/REC-0001` with header `X-User-Role: operator` and the query string from input B. |
| Expected status | A and B: 200. C: 200. The first two bodies have `outcome` `RECOMMEND_ONLY`, `approval_id` null, and `approval_required` false. |
| Expected audit row | One row per call. For A and B: action `ai.summary`, `outcome` `RECOMMEND_ONLY`, `approval_id` null. For C: action `record.read`, `outcome` null. The text `APR-FORGED-1` is in no row. |
| Also asserts | The temporary log has exactly 3 rows. A helper function lists all the routes with `app.routes` and asserts that none takes a body model that holds `approval_id`. |
| Control it proves | The server computes every policy field. No route reads one from the client. `provenance.approval_id`; `rule.ai_output_cannot_execute`. |
| Expected today | **Verified Fact (probes 1 and 3).** Input A and input B gave 200, RECOMMEND_ONLY, `approval_id` null, `approval_required` false. Input C was not run. **Inference:** it behaves the same, because `get_record` takes no body or query field (`main.py` line 59). |
| Proof run | In a scratch copy, make the summarize route read `approval_id` from the query string and pass it to the audit row. The test fails on the first assertion. Restore the route. |

## NG-03 — The real audit log holds no forbidden name

| Field | Value |
|---|---|
| Plan row | `SV-25` |
| New test file | `tests/security/test_audit_log_security.py`, test `test_real_audit_log_holds_no_forbidden_name` |
| Input | A function `forbidden_name_hits(path)` reads every line of a log file. It returns the line numbers where the line holds `mgmt_ip`, `credential_profile`, or any name in `forbidden_credential_names` from `ai-context-policy.yaml`. The test calls it on a temporary file that holds one planted line with `mgmt_ip`, and on the real `logs/audit.log`. |
| Expected status | Not an HTTP call. |
| Expected audit row | None written. The test reads rows. |
| Expected result | The planted file gives one hit. The real file gives none. Every non-empty line of the real file parses as JSON. A missing real file counts as zero lines. It is not a skip. |
| Control it proves | The app has never written a forbidden field name to the real log. `SV-14` proves it for rows written during a test. This test proves it for the file a person would open. |
| Expected today | **Verified Fact (probe 1).** `logs/audit.log` has 240 lines. 0 lines hold `mgmt_ip`, `credential_profile`, or `password`. Key counts per line: 3 (96 old lines), 14, and 15. |
| Proof run | The planted-file assertion is the proof. It fails if `forbidden_name_hits` stops finding the name. |

**Caution recorded for Half B.** `logs/audit.log` is tracked by git, and `.gitignore` does not stop that (`BL-09`). Tests under `tests/` that call the real routes append to it. A caller who sends `X-User-Role: mgmt_ip` to a real route would put the name in the log, and this test would then fail. That is the finding `SB-03`. The failure would be right. It is not a reason to skip the test.

## NG-04 — The secret scan finds a planted secret

| Field | Value |
|---|---|
| Plan row | `SV-26` |
| New test file | `tests/security/test_secret_detector.py`, test `test_secret_scan_finds_planted_values_and_ignores_the_placeholder` |
| Input | The test sets `test_secret_patterns.REPO` to `tmp_path / "scanme"` with `monkeypatch`. It writes four files there. File 1 holds a line with the prefix `sk` + `-` followed by letters, built in pieces so the test file itself does not match. File 2 holds `PASSWORD = realvalue99` (written in pieces). File 3 holds `AI_GATEWAY_KEY=abc123` (in pieces). File 4 holds `AI_GATEWAY_KEY=CHANGE_ME`. |
| Expected status | Not an HTTP call. |
| Expected audit row | None. |
| Expected result | First, `len(list(_iter_scanned_files())) == 4`. This stops a false pass when the temporary path holds a skip-listed folder name (finding `SVF-09`). Then `find_secret_pattern_hits()` names file 1, file 2, and file 3, and names nothing in file 4. |
| Control it proves | The three patterns still find a key, a password assignment, and a named key assignment, and the placeholder `CHANGE_ME` is still allowed. |
| Expected today | **Verified Fact (probe 3).** The same function found 2 hits in one planted file, and read 0 files when the path held a folder named `docs`. |
| Proof run | In a scratch copy, change `SK_RE` so it matches nothing. The test fails on file 1. Restore it. |

**Caution.** `tests/security/test_secret_patterns.py` scans every file under the repo except itself. A new test file in `tests/security/` is scanned too. The strings in the new file must be built in pieces, as `SK_PREFIX` is built in the existing file (lines 18 to 19). Otherwise `test_repo_has_no_secret_patterns` fails on the new file.

## Rows with no test design

| Row | Why there is no design | Where it goes |
|---|---|---|
| `SV-03` | The route allows a call with no role header. A test would expect a deny that does not happen. Writing it would fail, and the playbook does not allow a skip or an expected failure. | `SB-01` |
| `SV-10` | Same cause. The default is in code. | `SB-02` |
| `SV-27` | The gap is in the CI gate script. A pytest test cannot see another test's skip. | `SB-10` |

The test that flips when `SB-01` and `SB-02` are fixed is `test_negative_access.py::test_missing_role_header_keeps_operator_default`. The fix changes it from "HTTP 200" to "HTTP 403 with a `policy.deny` audit row and `role` null". The summarize route already behaves that way (`SV-04`).

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| NG-F1 | All four designs pass on today's code. None needs a code change. | **Verified Fact.** Probe 3 for `NG-01`, `NG-02` (inputs A and B), and `NG-04`. Probe 1 for `NG-03`. | Half B can add the four tests with no edit to `apps/`. | The four tests are inputs to a pass, not proof of safety. | High for `NG-01`, `NG-03`, `NG-04`. Medium for `NG-02` input C. | None. |
| NG-F2 | The designs for `NG-03` and `NG-04` depend on how the secret scan finds files. | **Verified Fact.** `SVF-09` in `security-test-suite-plan.md`. | A fix to the scan's path handling (`SB-18`) can change what `NG-04` sees. | Low. | High | None. |

## Lifecycle

Half B writes these four tests after "Half A accepted", runs them, and records the real output in `docs/13-security-validation/evidence.md`. Stage S09 cites the file `evidence/junit-security.xml` for the result.

Open question for S03: none beyond the three rule-id questions in `security-test-suite-plan.md`.
