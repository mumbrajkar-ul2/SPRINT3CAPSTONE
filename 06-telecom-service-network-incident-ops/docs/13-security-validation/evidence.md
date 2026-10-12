# Security validation evidence

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. `pytest -m security` gives 159 passed and 0 skipped on this machine, with `opa` 1.21.1 on the PATH. Stage 6 of the pipeline now fails on any skipped security test. Three scans still exit 1 on real findings (ruff 11, pip-audit 9 advisories, bandit 2 LOW). None is switched off. 20 backlog rows stay open with an owner (`remediation-backlog.md`). Owner: Team-Force. |
| Evidence sources | `evidence/junit-security.xml`; `evidence/junit-tests.xml`; `evidence/junit-policy.xml`; `evidence/opa-test.json`; `evidence/ruff.json`; `evidence/pip-audit.json`; `evidence/bandit.json`; `evidence/run-info.txt`; `evidence/exit-codes.txt`; the proof runs below; `scripts/evidence.ps1`; `scripts/check_junit_no_skips.py` |
| Assumptions | Every output below comes from a command run on 2026-10-11 on one Windows machine (Python 3.13.5). The Linux run and the GitHub run did not happen in this stage. `make` is not installed here, so the `make security` target was not run. |
| Unresolved issues | The workflow has not run on GitHub (CI-01). Make was not run. With `opa` on the PATH the app is much slower (`SB-20`). |
| Residual risks | A passing test shows the control works for the inputs the test uses. Three decisions by Mangesh (FDE) on 2026-10-11 are in effect: narrow `docs/` patterns (`BL-03`), skip guard (`SB-10`), `opa` on the user PATH. |

## What this file is

This file records what Half B changed and the real output of each run. Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a test file and test name, or an output file.

Half A files: `security-test-suite-plan.md`, `negative-tests.md`, `scanning-checklist.md`, `abuse-case-evidence.md`, `remediation-backlog.md`, and `security/threat-model.md`.

## 1. `opa` on this machine

| Item | Value |
|---|---|
| Version | `opa` 1.21.1 (`Version: 1.21.1`, Go 1.27.1, Rego `v1`, `windows/amd64`) |
| Source | `https://github.com/open-policy-agent/opa/releases/download/v1.21.1/opa_windows_amd64.exe` |
| Check | The published `opa_windows_amd64.exe.sha256` and `Get-FileHash -Algorithm SHA256` of the downloaded file both give `25406f7c6e147d687fd7fd546f835bafa160a6242c605ee94a23ba6cd7bccdcd`. They match. |
| Install method | Downloaded with `Invoke-WebRequest` into `C:\Users\mange\tools\opa\opa.exe`. That folder was added to the user PATH with `[Environment]::SetEnvironmentVariable("Path", ..., "User")`. New terminals see it. |
| `Get-Command opa` | `C:\Users\mange\tools\opa\opa.exe` |
| In the pipeline | `evidence/run-info.txt` line `opa=Version: 1.21.1`. |
| CI | `.github/workflows/ci.yml` already installs the same version (`OPA_VERSION: "1.21.1"`) with `sha256sum -c`. It runs before stage 0. Half B did not change that step. It changed the stage 6 name and comment. |

## 2. What Half B changed

| Change | Where |
|---|---|
| Marker text now describes the whole suite and says no test may skip or fail by design | `pyproject.toml` |
| `pytestmark = pytest.mark.security` on 3 whole files (6, 83, and 3 tests) | `tests/access/test_negative_access.py`, `policy/tests/test_policy_python.py`, `tests/observability/test_audit_schema.py` |
| `@pytest.mark.security` on 3 tests | `tests/characterization/test_current_behaviour.py`: `test_clinician_role_is_denied_on_record_read`, `test_ai_summarize_refuses_request_with_no_role_header`, `test_legacy_script_reads_password_from_environment` |
| 12 new tests | `tests/security/test_audit_log_security.py` (6, `NG-01` and `NG-03`), `test_client_flags_ignored.py` (2, `NG-02`), `test_secret_detector.py` (2, `NG-04` and `SB-18`), `test_docs_secret_scan.py` (2, `BL-03`) |
| Secret scan tests the path below the repo root, and checks it read more than 50 files | `tests/security/test_secret_patterns.py` (`SB-18`) |
| Skip guard | `scripts/check_junit_no_skips.py`, called by `scripts/evidence.sh` and `scripts/evidence.ps1` in the security stage (`SB-10`). 8 tests in `tests/ci/test_skip_guard.py`. |
| `make security` | `Makefile`. Runs `bash scripts/evidence.sh security`. |
| CI stage 6 name and comment | `.github/workflows/ci.yml` |
| Test fix: reset the cached `opa` path around every policy test | `policy/tests/test_policy_python.py`, fixture `python_engine` (see section 5) |
| Test setup: run the Python copy of the policy for every test under `tests/` | `tests/conftest.py`, fixture `python_policy_engine` (`SB-20`, section 5) |
| Counts updated | `docs/07-cicd/evidence.md`, section "Update from S05-13 Half B" |

No file under `apps/` changed. No security test is skipped. No test is marked to fail.

## 3. Suite output

**Verified Fact.** The command was `scripts\evidence.ps1` (all stages). The security stage printed:

```text
159 passed, 97 deselected, 80 warnings in 67.83s (0:01:07)
security gate ok: ...\evidence\junit-security.xml has no skipped test
== stage security exit code 0
```

`evidence/junit-security.xml` holds `errors="0" failures="0" skipped="0" tests="159"`.

| Test file | Tests in the security run |
|---|---|
| `tests/ai/test_guardrails.py` | 51 |
| `policy/tests/test_policy_python.py` | 83 |
| `tests/access/test_negative_access.py` | 6 |
| `tests/observability/test_audit_schema.py` | 3 |
| `tests/characterization/test_current_behaviour.py` | 3 |
| `tests/security/test_audit_log_security.py` | 6 |
| `tests/security/test_client_flags_ignored.py` | 2 |
| `tests/security/test_secret_detector.py` | 2 |
| `tests/security/test_docs_secret_scan.py` | 2 |
| `tests/security/test_secret_patterns.py` | 1 |
| Total | 159 |

**Worked example.** Before Half B, `pytest -m security` ran 52 tests. 52 + 6 + 83 + 3 + 3 = 147 existing tests, plus 12 new tests, gives 159. The plan said 151. It said 4 new tests. The 12 are the 4 designs (6 tests, because `NG-01` has 3 inputs, and `NG-03` has a planted-name test and a real-log test), plus `NG-02` second test, `NG-04` second test (`SB-18`), and the two `docs/` tests (`BL-03`).

**The two tests that need `opa`.** **Verified Fact.** `evidence/junit-security.xml`: `test_opa_and_python_agree_on_access` ran in 0.133 s and has no `skipped` tag. `test_opa_and_python_agree_on_every_ai_action_combination` ran in 43.414 s and has no `skipped` tag. On 2026-10-11 before `opa` was installed, `junit-policy.xml` showed `skipped="2"` for the same two tests.

**Other stages, same run.**

| Stage | Result | File |
|---|---|---|
| tests | `97 passed, 76 deselected` (0 skipped) | `evidence/junit-tests.xml` |
| semantic_layer | `35 passed` | `evidence/junit-semantic-layer.xml` |
| policy | `83 passed` (0 skipped). `opa test`: `PASS: 30/30` | `evidence/junit-policy.xml`, `evidence/opa-test.json` |
| security | `159 passed` | `evidence/junit-security.xml` |
| lint | exit 1, 11 findings | `evidence/ruff.json` |
| pip_audit | exit 1, 9 unique advisories on 3 packages | `evidence/pip-audit.json` |
| bandit | exit 1, 2 LOW results | `evidence/bandit.json` |

`evidence/exit-codes.txt` has `lint=1`, `pip_audit=1`, `bandit=1`, and 0 for every other stage.

**Done test.** `pytest -m security -q` passes. `evidence/junit-security.xml` exists. No security test is skipped, including the two that need `opa`. The `opa` command is on the PATH. The part "after `make security`" was not run, because Make is not installed here. The stage ran through `scripts\evidence.ps1`, which does the same work.

## 4. Proof runs

Each new control has a proof: take the control away in a scratch copy of the project and check that the test fails. The scratch copy sat in the temp folder and used the same `.venv`. The repo files were not touched.

| Test | What was changed in the scratch copy | Result |
|---|---|---|
| `NG-01` `test_write_event_refuses_an_empty_correlation_id` | `audit.py`: the empty-id check replaced by `if False:` | 3 failed (`DID NOT RAISE <class 'ValueError'>`) |
| `NG-02` `test_no_route_reads_an_approval_id_from_the_caller` | `main.py`: `ai_summary` takes `approval_id` as a query value | 1 failed, 1 passed |
| `NG-03` `test_real_audit_log_holds_no_forbidden_name` | A line with `mgmt_ip=10.1.1.1` added to `logs/audit.log` | 1 failed |
| `NG-04` `test_secret_scan_finds_planted_values_and_ignores_the_placeholder` | `SK_RE` replaced by a pattern that matches nothing | 2 failed |
| `SB-18` `test_secret_scan_reads_files_when_a_parent_folder_is_named_docs` | The scan tests `path.parts` again, not the path below the repo | 1 failed, 1 passed |
| `BL-03` `test_docs_have_no_real_secret_formats` | A `docs/planted.md` file with a `sk-` key of 24 characters | 1 failed, 1 passed |
| `SB-10` skip guard | `scripts\evidence.ps1 -Stage security` with the `opa` folder removed from the PATH | `157 passed, 2 skipped`. `security gate FAILED: 2 security test(s) skipped:` and the two test names. `security=1`. Exit 1. |

After each proof the file was put back, and `tests/security` gave `13 passed` again.

## 5. Findings from Half B

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| EV-01 | With `opa` on the PATH the app calls `opa eval` as a new program for every decision. A record read takes a median 150 ms. With the Python copy it takes 10 ms. A summary takes 401 ms against 26 ms. | **Verified Fact.** A timing script (15 record reads and 8 summaries per engine, `TestClient`, a temporary audit log). The `tests/reliability/test_breaker.py::test_route_a_hung_model_does_not_hold_every_route_thread` test failed 4 of 4 reruns with route times of 0.2 to 1.9 s against a 0.2 s limit. | Making `opa` available changes how fast the app answers. S04-10 measured only the PATH search, which `opa` absent hid. | Medium. Real traffic with `POLICY_ENGINE` unset would be about 15 times slower. | High | Whether production runs `opa` as a long-lived server is Unknown. Backlog row `SB-20`. |
| EV-02 | A test under `policy/tests` passed only when `opa` was missing. | **Verified Fact.** `test_engine_name_follows_the_setting` failed with `assert 'python' == 'opa'`. `test_engine_failure_denies` empties the PATH, and the cached `opa` search kept the answer "not found". | Without the fix, installing `opa` made a security test fail. | Low. Fixed by resetting the cache around each test. | High | None. |
| EV-03 | `tests/` now runs the Python copy of the policy by default (`tests/conftest.py`). The route tests do not exercise the Rego copy. The Rego copy is tested by `opa test` (30 of 30) and the two agreement tests. | **Verified Fact.** `tests/conftest.py`. `SB-20`. | The timing tests measure the app and not the engine. | Low. | High | None. |
| EV-04 | `test_missing_role_header_keeps_operator_default` is in `tests/access/`, which is now marked `security`. It passes because the route returns 200 for a call with no role header. It locks a known gap (`SB-01`). | **Verified Fact.** Its assertion is `status_code == 200`. | The security run counts a test that proves an unwanted behavior. | Medium. A reader of the 159 count could think the gap is closed. | High | None. It changes to expect 403 when `SB-01` is fixed. |
| EV-05 | The pipeline's `prepare` stage deleted `evidence/linux-py311/` (13 tracked files) on the first run. | **Verified Fact.** `git status` showed 13 deletions. I restored them with `git checkout -- evidence/linux-py311`. | The Linux run record is intact. | Low. Each full run replaces the Windows files in `evidence/`. | High | `evidence.sh prepare` deletes sub-folders as well as files. Whether it should keep `linux-py311/` is for the owner of S04-07. |
| EV-06 | The ruff count is now 11, not 12. | **Verified Fact.** `evidence/ruff.json`. The 2 `ai_gateway.py` findings are no longer in the file. `breaker.py` `SIM114` is new (S04-11). The two findings in `test_secret_patterns.py` moved to line 53. | `BL-10` text said 12. | Low. | High | None. |
| EV-07 | Each run of the access and characterization tests appends 12 rows to the real `logs/audit.log`. | **Verified Fact.** 240 lines before. 252 after one `pytest -m security` run. `git diff` showed added rows. | The tracked file changes on every run (`BL-09`). | Low. I restored it with `git checkout -- logs/audit.log` after the runs. It has 240 lines. | High | The decision on 2026-10-11 is to leave it tracked. |

## 6. Lifecycle

Stage S09 copies `evidence/junit-security.xml` into the pack and cites the test names in `abuse-case-evidence.md` for each security claim. The remaining open rows are in `remediation-backlog.md`.

Open question for S03: none beyond those already filed in the Half A files.
