# Remediation backlog

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A |
| Date / version | 2026-10-11, v1.0. v1.1 after S05-13 Half B: 5 rows closed, 1 decided, `SB-20` added. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. 20 rows are open after Half B (25 at Half A, 5 closed, 1 decided, 1 added). Each has an owner and a stage that should fix it. 6 rows carry over from `docs/07-cicd/pipeline-improvement-plan.md` (`BL-03`, `BL-07`, `BL-09`, `BL-10`, `BL-11`, `BL-12`). 19 rows are new (`SB-01` to `SB-19`). Owner of every row: Team-Force (`operating-contract.md` row 10). |
| Evidence sources | `security-test-suite-plan.md`; `negative-tests.md`; `scanning-checklist.md`; `abuse-case-evidence.md`; `security/threat-model.md`; `docs/07-cicd/pipeline-improvement-plan.md` (rows `BL-01` to `BL-13`); `docs/02-baseline/defect-list.md`; `docs/04-secrets/sensitive-field-handling-checklist.md`; `docs/06-policy/ai-action-policy-design.md`; `docs/09-ai-guardrails/evidence.md`; the three probes of 2026-10-11 |
| Assumptions | Team-Force owns every proposed item until the packet names a person. The "stage that should fix it" column is PROPOSED. Owner: Team-Force. |
| Unresolved issues | Who rules on the three red scans is Unknown. Whether the packet wants authentication is Unknown (`SB-09`). |
| Residual risks | A row on this list is a known gap. A gap not found by a test or a probe is not on the list. |

## What this file is

This file lists every gap that Half A found, with an owner and the stage that should fix it. A row here is not a design for a new control. If a row needs a new control, the control is not written in this stage.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Id rule. `BL-nn` rows keep the id they have in `pipeline-improvement-plan.md`. `SB-nn` rows are new in this stage.

## Gaps that stop a test from showing a deny

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| SB-01 | A call to `GET /records/{id}` with no role header is treated as `operator` and returns the row, including `mgmt_ip` and `credential_profile`. | **Verified Fact.** `apps/api/main.py` line 59. Probe 1: no header, HTTP 200, body holds `mgmt_ip`. `test_negative_access.py::test_missing_role_header_keeps_operator_default`. Defect F15. Plan row `SV-03`. | Any caller who reaches the route reads a device row without naming a role. | High. The summarize route denies the same call (`SV-04`), so the two routes disagree. | High | Whether the default is for a local demo or a deployed caller is Unknown (F15). Open question for S03 already filed in S04-03: there is no role id for "no header". |
| SB-02 | The default role is set in code, in three places. | **Verified Fact.** `main.py` line 59 (`Header(default="operator")`). `policy.py` line 290 (`_RECORD_READ_DEFAULT`) and line 297 (`_SUMMARIZE_DEFAULT`) hold the `operator` values. Lines 310 and 325 use them for a role id that has no entry. Plan row `SV-10`. | Removing the header default alone leaves the two fallbacks. | Low to medium. The policy decision still comes from the matrix, which denies a role with no row (`SV-01`, `SV-02`). **Inference:** the fallback only fills the resource, purpose, and scope fields. |  High | None. |
| SB-10 | Nothing fails the build when a security test skips. | **Verified Fact.** `scripts/evidence.sh` line 105 runs `pytest -m security` and returns its exit code. `evidence/junit-policy.xml`: `skipped="2"` with `policy=0` in `exit-codes.txt`. Plan row `SV-27`. | The two Python-versus-Rego tests skip on a machine with no `opa`, and the stage is green. | Medium. The playbook calls any skipped security test BLOCKED. | High | None. |

## Gaps in what the app does

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| SB-03 | Text in `X-User-Role` and `X-Correlation-Id` is written to `logs/audit.log` unchanged, with no length limit. | **Verified Fact.** Probe 1: a role of `mgmt_ip=10.1.1.1 password=hunter2` and a correlation id of 5000 characters were stored whole. `main.py` `_role_word`; `audit.py` `correlation_id_from_header`. | A caller can plant a secret-looking string or a very long string in the audit log. JSON encoding stops a forged new line. | Medium. | High | What length and character rules an id should have is Unknown. |
| SB-04 | A model answer is not checked for forbidden values or credential names. The prompt is. | **Verified Fact.** Probe 2: an answer holding the `mgmt_ip` value and an answer holding `SHARED_DB_PASSWORD` both returned 200 RECOMMEND_ONLY. `ai_gateway.py` `find_forbidden` runs on the prompt only. | A real model could repeat a field the prompt never held, or a value from its own training. The route would return it. | Medium once a real model exists. Low with the stub. | High | None. |
| SB-05 | Only one sentence is detected as a command in a model answer. | **Verified Fact.** `ai_gateway.py` `COMMAND_PHRASES` holds one sentence. Probe 2: "Reboot the core router now and clear the config" returned 200 RECOMMEND_ONLY. | The text reaches the caller as a recommendation. No code turns it into a change, which is the real barrier. | Low today. Rises when S07 shows the text to a person who may act on it. | High | Open question for S03 already filed in S04-09: a command list and a failmode id for an execute verb. |
| SB-06 | `GET /records/{id}` returns `mgmt_ip` and `credential_profile` to every allowed role. | **Verified Fact.** Probe 1. Defect F10. `sensitive-field-handling-checklist.md` `SF-02`. | Both cells leave the API for every role that may read a record, and also for a caller with no header (`SB-01`). | Medium. The policy that decides who may read the two cells does not exist. | High | Who may read the two cells is Unknown. |
| SB-07 | `GET /records/{id}` with an id that does not exist returns the first row. | **Verified Fact.** Probe 1: HTTP 200, `device_id` `REC-0001`. `test_current_behaviour.py::test_missing_id_returns_first_row`. `tests/performance/test_load_once.py::test_missing_id_still_returns_the_first_row`. Defect F01. | A caller can take a missing device for `REC-0001`. The summarize route already refuses this (`SV-17`). | Medium. | High | `operating-contract.md` row 2 allows a later 404. Which stage edits it is Unknown. |
| SB-08 | The approval id is checked only for being non-empty. No approval store exists. An approval record has no decision field and no approver field. | **Verified Fact.** `policy.py` `_approval_id_present`. `ai-action-policy-design.md` findings `AA-02` and `AA-09`. | A rejected approval id would pass the id check. A held recommendation has no reviewer to reach. | Low today, because no route reaches EXECUTE. High when S07 adds the approval write. | High | Open question for S03 already filed in S04-06: a decision field and an approver field. |
| SB-09 | The role is a word the caller types. Nothing proves who the caller is. | **Verified Fact.** `main.py` reads `X-User-Role` and nothing else. **Inference:** no authentication exists in the repo. | Any caller can claim `operator`. Every access test proves the policy for a stated role. None proves the caller holds it. | High if the app is reachable by more than the team. | Medium | **Unknown.** Whether authentication is in scope for this packet. |
| SB-12 | The audit log is a plain file. Anyone with file access can edit or delete lines. Two server processes share the file with no lock between them. 96 old lines have no `correlation_id`. | **Verified Fact.** `audit.py` (append mode; the lock covers one process). Probe 1: 240 lines, 96 with 3 keys. | A reader cannot prove that the log is complete or unchanged. | Medium. | High | None. Stage S05-14 is the audit chain. |
| SB-13 | No limit on request rate, prompt size, or answer size. | **Verified Fact.** `breaker.py` limits model calls in flight only (`test_breaker.py::test_many_threads_never_go_past_the_in_flight_limit`). **Inference.** The routes have no rate limit and the prompt cells are not cut to a length. | A flood or a very long cell can slow the route. | Low to medium. | Medium | Production traffic figures are Unknown (`docs/10-performance/`). |
| SB-14 | A secret value typed into an allowed field (for example `hostname`) is not found. The YAML has no prompt rule for the service-order `customer_id`. | **Verified Fact.** `ai_gateway.py` `find_forbidden` docstring: "A forbidden value copied inside an allowed field's own value is not found." `sensitive-field-handling-checklist.md` `SF-04`. | The prompt can carry a secret that is not in the forbidden list. | Low today. | High | Open question for S03 already filed in S04-04 (`SF-04`). |
| SB-15 | The model name and the model version have the same value (`local-sim-v1`). A swapped model would answer under the same name. Prompt text would leave the process for a hosted model. | **Verified Fact.** `ai_gateway.py` `MODEL_NAME` and `MODEL_VERSION`. **Inference.** The stub sends nothing out. | Both threats start when a hosted model is added. | Low today. | High | Whether a hosted model is used is Unknown. `S2Q` says three uses may use GenAI at recommend only. |
| SB-19 | No security test or threat boundary covers duplicate ticket creation, one of the six brownfield concerns. | **Verified Fact.** The app has 3 routes (`/health`, `GET /records/{id}`, `POST /ai/summarize/{id}`) and none creates a ticket. `security/threat-model.md` starter list. | No harm today. The threat starts when stage S07 adds a route that creates tickets. | Low today. | High | The ticket route and its key are Unknown until the PRD names them. |
| SB-17 | Where a credential is rotated and recorded is Unknown. | **Verified Fact.** `docs/04-secrets/` status: "Rotation store is Unknown." | A committed value was removed. Nothing shows the old value was replaced where it was used. | Medium. | High | Rotation store is Unknown. |

## Gaps in the test and evidence pipeline

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| SB-20 | With `opa` on the PATH and `POLICY_ENGINE` unset, every access and AI decision starts a new `opa eval` program. A record read takes a median 150 ms (10 ms with the Python copy). A summary takes 401 ms (26 ms). | **Verified Fact.** `docs/13-security-validation/evidence.md` EV-01. `tests/reliability/test_breaker.py::test_route_a_hung_model_does_not_hold_every_route_thread` failed 4 of 4 reruns before `tests/conftest.py` set the Python engine. | The policy of record (Rego) is slow in the app. S04-10 measured the PATH search only. | Medium. About 15 times the latency on this machine. | High | Whether production runs `opa` as a long-lived server is Unknown. **Measured 2026-10-11 (read-only):** a local `opa run --server` answered an access decision in a median 6.3 ms (p95 30.7 ms, 50 calls). The Python copy answered in a median 0.005 ms. **Recommendation (FDE):** keep the Python copy as the default engine for now, set `POLICY_ENGINE` explicitly instead of relying on `auto`, and keep the Rego copy as the checked policy of record through the agreement tests. Decision by Mangesh (FDE) is pending. Open question for S03: none. |
| SB-11 | The files in `evidence/` are out of date. `junit-security.xml` shows 1 test. `docs/07-cicd/evidence.md` says the `tests` stage has 20 tests. | **Verified Fact.** `junit-security.xml`: `tests="1"`, 13:32 on 2026-10-11. Today: 52 marked tests. `pytest tests --collect-only`: 153 tests, 101 not marked security. | S09 would copy a stale file. | Medium. | High | None. |
| SB-16 | Several rules in `business-rules.yaml` say `enforced_today: false` and describe code that has since changed. | **Verified Fact.** `rule.forbidden_fields_never_enter_prompt`, `rule.stale_topology_blocks_recommendation`, `rule.denied_access_is_audited`, `rule.ai_output_cannot_execute`, and `rule.audit_row_names_actor_and_correlation` are `enforced_today: false`. The tests in `abuse-case-evidence.md` prove the controls run. `rule.no_default_role` is still not enforced for `GET /records/{id}` (`SB-01`). | A reader of the YAML believes controls are off that are on. | Low. | High | None. Stage S05R folds the corrections into the YAML. This stage does not edit the YAML. |
| SB-18 | The secret scan reads no file when the repo path holds a folder named `docs`, `venv`, `.venv`, or `.git`. | **Verified Fact.** `test_secret_patterns.py` line 40 tests `path.parts` of an absolute path. Probe 3. Finding `SVF-09`. | A checkout under `C:\docs\...` passes with no scan. | Low on this machine. | High | None. |
| BL-03 | A secret in a Markdown file under `docs/` is not found. | **Verified Fact.** `test_secret_patterns.py` lines 9 to 16 skip `docs`. A read-only trial of the three patterns on `docs/` gives 4 hits, none a secret: 3 in `docs/04-secrets/evidence.md` (the stand-in text `sk-temp-should-fail`) and 1 in `docs/12-finops/cost_baseline.py` (a constant named `EDU_UNITS_PER_1K_TOKENS`). | A secret written in a document is not caught by pattern. The semantic-layer test catches the two known values only. | Medium. | High | **Decision needed from Team-Force.** A `docs/` scan with the same patterns fails on those 4 lines. Choices: (a) narrow the patterns for `docs/` to real key formats, (b) list the 4 lines as reviewed exceptions with a reason, (c) reword the 3 lines. Each is a change to a test or to a document. None is a skip. |
| BL-07 | `opa` is not available on developer machines. CI installs it. | **Verified Fact.** `ci.yml` installs `opa` 1.21.1 with a checksum. `evidence/run-info.txt`: `opa=not on PATH`. | 2 security tests skip locally. | Medium. | High | None. Decision by Mangesh (FDE), 2026-10-11: Half B makes `opa` available locally and in CI. |
| BL-09 | `logs/audit.log` is tracked by git. `.gitignore` lists `logs/`, and that has no effect on a tracked file. | **Verified Fact.** `.gitignore` line 23. `git ls-files logs` lists `logs/audit.log`. Tests in `tests/` append to it. | `NG-03` reads the real log, and the tests change it. | Low. | High | Whether to run `git rm --cached logs/audit.log` is a Team-Force decision. |

## Gaps the scans found

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| BL-10 | 11 `ruff` findings (12 at S04-07). 2 are in `tests/security/test_secret_patterns.py` line 53. | **Verified Fact.** `evidence/ruff.json`. `docs/07-cicd/evidence.md`. | `lint=1` makes the job red. | Low. | High | Which rule set the team wants is Unknown. |
| BL-11 | 9 `pip-audit` advisories on 3 packages: `pytest` 1, `python-dotenv` 1, `starlette` 7. | **Verified Fact.** `evidence/pip-audit.json`. | `pip_audit=1`. Starlette is held below 0.39 by FastAPI 0.115.0, so a fix needs a FastAPI upgrade. | Medium. Whether the app runs the affected code is Unknown. | High | Nobody has read the advisory text. |
| BL-12 | 2 `bandit` results, both LOW severity and HIGH confidence, in `apps/api/services/policy.py` (`B404` line 24, `B603` line 66). | **Verified Fact.** `evidence/bandit.json`. | `bandit=1`. | Low. **Inference:** the command is fixed and the input goes in on stdin. | High | A person must rule on it. No `# nosec` is allowed without a recorded review. |

## Owner and fix stage

| Id | Owner | Stage that should fix it (PROPOSED) | Test that shows the fix | Status |
|---|---|---|---|---|
| SB-01 | Team-Force | S07 (next stage that edits `main.py`), after Team-Force decides | `test_negative_access.py::test_missing_role_header_keeps_operator_default` changes to expect 403 with a `policy.deny` row and `role` null | Open. Decision needed. |
| SB-02 | Team-Force | S07, with `SB-01` | Same test | Open |
| SB-03 | Team-Force | S05-14 | A new test: a role or correlation header with a forbidden name is not stored as sent | Open |
| SB-04 | Team-Force | S07 | A new test: an answer holding a forbidden value is held | Open |
| SB-05 | Team-Force | S05R (YAML list) then S07 | `test_guardrails.py::test_gr07_*` gains the list | Open |
| SB-06 | Team-Force | S07 | A new test per role for the two cells | Open. Decision needed. |
| SB-07 | Team-Force | S07 | `test_missing_id_returns_first_row` changes to expect a 404 | Open |
| SB-08 | Team-Force | S07 | A policy test for a rejected approval id | Open |
| SB-09 | Team-Force | Unknown | None | Open. Scope unknown. |
| SB-10 | Team-Force | S05-13 Half B | `scripts/check_junit_no_skips.py`, called by `evidence.sh` and `evidence.ps1`. Proof: `evidence.ps1 -Stage security` with `opa` off the PATH gave `security=1` and named the 2 skipped tests (`evidence.md` section 4). Tests: `tests/ci/test_skip_guard.py` (8). | **Closed** 2026-10-11 (S05-13 Half B). |
| SB-11 | Team-Force | S05-13 Half B | Rerun of all stages; `docs/07-cicd/evidence.md` counts updated. `evidence/junit-security.xml` now shows 159 tests. | **Closed** 2026-10-11 (S05-13 Half B). |
| SB-12 | Team-Force | S05-14 | The audit-chain tests | Open |
| SB-13 | Team-Force | S04-10 follow-up or S07 | A load test | Open |
| SB-14 | Team-Force | S05R then S07 | A prompt test for the service-order id | Open |
| SB-15 | Team-Force | S08 (second model) | A model-identity test | Open |
| SB-16 | Team-Force | S05R | `semantic-layer/tests` | Open |
| SB-17 | Team-Force | S04-04 follow-up | None | Open |
| SB-19 | Team-Force | S07 | A duplicate-ticket test on the new route | Open |
| SB-20 | Team-Force | S07, or the performance follow-up of S04-10 | A timing test with `POLICY_ENGINE=opa` against a limit the team sets | Open |
| SB-18 | Team-Force | S05-13 Half B | `test_secret_patterns.py` now tests the path below the repo root. `test_secret_detector.py::test_secret_scan_reads_files_when_a_parent_folder_is_named_docs`. | **Closed** 2026-10-11 (S05-13 Half B). |
| BL-03 | Team-Force | S05-13 Half B | `test_docs_secret_scan.py` (2 tests). Decision (a): narrow patterns for real key formats. The 4 old false hits no longer match. | **Closed** 2026-10-11 (S05-13 Half B). The `docs/` scan finds real formats only. A password written in plain prose is not found. |
| BL-07 | Team-Force | S05-13 Half B | `junit-policy.xml` shows `skipped="0"`. `run-info.txt` says `opa=Version: 1.21.1`. Installed to `C:\Users\mange\tools\opa`, on the user PATH. | **Closed** for this machine and for the workflow (S05-13 Half B). |
| BL-09 | Team-Force | S05-13 Half B notes it | None | **Decided** 2026-10-11: leave the file tracked. Each run of the access and characterization tests adds 12 rows (`evidence.md` EV-07). |
| BL-10 | Team-Force | Unknown | `evidence/ruff.json` empty or ruled on | Open. Scan stays on. |
| BL-11 | Team-Force | Unknown | `evidence/pip-audit.json` | Open. Scan stays on. |
| BL-12 | Team-Force | Unknown | `evidence/bandit.json` | Open. Scan stays on. |

**Worked example (`SB-01`).** Today `GET /records/REC-0001` with no role header returns HTTP 200 and the row. After the fix, the same call returns 403, writes one `policy.deny` audit row, and stores `role` null. The summarize route already does this. The test above changes from "200" to "403". That is a new control, so this stage writes it in this list and does not build it.

## Lifecycle

Half B closed `SB-10`, `SB-11`, `SB-18`, `BL-03`, and `BL-07`, and recorded the decision on `BL-09`. It added `SB-20`. Every other row waits for the stage named above. Stage S05R folds the open questions into the YAML. Stage S09 carries the open rows into the readiness decision.

Open question for S03: none beyond those already filed.
