# Second-model test split (owner note, do not paste)

| Field | Value |
|---|---|
| Stage | S08 Part 1. This note explains why the brief asks the second model to pass 22 tests and not all of the tests the PRD names. Part 3 reads it. |
| Date / version | 2026-10-13. Semantic layer `1.2.1`. PRD `v1.9`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Decided by Mangesh on 2026-10-13: "HTTP only". The brief gives the second model one interface fact. Tests that patch first-app internals are not asked of it. |
| Evidence sources | `docs/prd/prd.md` section 10 (the test named in each `RQ` row); every file under `tests/` and `policy/tests/`; a script that walks each test with Python `ast` (kept at `C:\Users\mange\AppData\Local\Temp\s08\classify.py`); hand reading of the doubtful tests named in section 3 |
| Assumptions | (1) The second model has repository access and obeys the rule "read only the attached files". Nothing blocks it from opening `apps/api/`. (2) A test that names no first-app module, uses no patch and uses no stand-in model is a test that needs only HTTP. |
| Unresolved issues | How Part 3 points the 22 tests at `apps/api_model_b/`. Section 4 lists what the setup must supply. |
| Residual risks | Section 6 lists them. The main one: some of the 22 tests assert text that the PRD and the semantic layer do not give. A failure there shows a gap in the PRD, not proof that a meaning drifted. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Why a split is needed

**Verified Fact.** Every test file that drives the app depends on `apps.api`. It imports `apps.api.main` or `apps.api.services.*`, or it gets its `client` from `tests/app/conftest.py`, which does. Many tests patch names inside those modules: `audit.LOG`, `approvals.STORE`, `ai_gateway.call_model`, `alarm_service.DATA_DIR`, `breaker`, `policy`, `domain_service`. `tests/app/conftest.py` does the same for every test under `tests/app/`. The PRD names none of these. A second model cannot match them from the PRD and the semantic layer. S08 Part 1 forbids the brief from adding them.

## 2. The split

**Verified Fact.** A script read the `RQ` rows of `docs/prd/prd.md`. It found 73 rows. They name 69 different tests.

| Group | Tests | What the group holds |
|---|---|---|
| Asked of the second model | 22 | Tests that call the app through HTTP, read the data files, and read audit rows. They name no first-app module inside the test body. They are listed in section 4 of the brief. |
| Page tests | 4 | `tests/app/test_page.py` (`RQ-62` to `RQ-65`). They search the page source for exact first-app text, for example `data.rows.concat(data.held_aside)` and `if (!LABELS.includes(label)) { throw`. The PRD does not give that text. |
| Repo-level tests | 3 | `RQ-51` (`test_real_audit_log_holds_no_forbidden_name` reads the real `logs/audit.log`), `RQ-60` (`test_docs_have_no_real_secret_formats` scans `docs/`), `RQ-67` (`test_latency_percentiles_and_outcome_split` calls the first app's metrics script). None of them runs the second app. |
| Patch-based tests | 40 | Tests that patch a first-app module, use `fake_model`, use `monkeypatch`, or import a first-app module inside the test. |

The four numbers add up: 22 + 4 + 3 + 40 = 69.

Patch-based tests by file:

| File | Tests |
|---|---|
| `tests/app/test_recommend_route.py` | 10 |
| `tests/app/test_approvals_route.py` | 4 |
| `policy/tests/test_policy_python.py` | 4 |
| `tests/app/test_audit_before_state_change.py` | 3 |
| `tests/app/test_audit_row_keys.py` | 3 |
| `tests/audit/test_audit_rebuild.py` | 3 |
| `tests/ai/test_guardrails.py` | 2 |
| `tests/app/test_command_phrases.py` | 2 |
| `tests/observability/test_audit_schema.py` | 2 |
| `tests/app/test_readiness_route.py` | 1 |
| `tests/app/test_storm_route.py` | 1 |
| `tests/characterization/test_current_behaviour.py` | 1 |
| `tests/performance/test_load_once.py` | 1 |
| `tests/reliability/test_breaker.py` | 1 |
| `tests/reliability/test_drills.py` | 1 |
| `tests/security/test_client_flags_ignored.py` | 1 |
| **Total** | **40** |

**Inference.** The PRD rows these 40 tests cover can still be checked on the second app in Part 3. Probe the same behaviour with HTTP calls and record the result as "probe", not as "test passed".

## 3. How the 22 were checked

**Verified Fact.** The script marked a test as patch-based when its body names a first-app module, uses `monkeypatch`, `fake_model`, `approvals_file` or another patch fixture, or imports inside the function. I then read the doubtful tests by hand and kept these in the asked group: the four records tests (`RQ-03`, `RQ-05`, `RQ-06`, `RQ-68`); the seven storm tests (`RQ-08` to `RQ-13` and `RQ-15`); `RQ-01`; `RQ-04`; `RQ-18`; `RQ-38`; `RQ-39`; `RQ-42`; `RQ-46`; `RQ-47`; `RQ-48`; `RQ-57`; `RQ-69`. The script first marked three more tests as HTTP (`RQ-51`, `RQ-60`, `RQ-67`). The hand reading moved them to the repo-level group. The script also marked the four page tests as HTTP. They stay in their own group because they check first-app page text.

**Verified Fact.** Baseline on the first app. Command: `pytest -q -p no:cacheprovider` with the 22 test ids from the brief. Result: `22 tests collected`, then `22 passed, 43 warnings in 1.09s`, run on 2026-10-13. The run appended one row to `logs/audit.log`. I removed that row, so the file is as it was before the run.

Two of the 22 read the route table of the app object and not a reply: `RQ-57` (`app.routes`) and `RQ-38` (`route.dependant`). They work on any FastAPI application. This is why the brief says the object is a FastAPI application.

## 4. What the setup in Part 3 must supply

The 22 tests cannot run on `apps/api_model_b/` without a setup step. Each need below is **Verified Fact** from the named file.

| Need | Where the tests ask for it |
|---|---|
| The application object `app` from `apps.api_model_b.main`, in place of `apps.api.main` | `tests/test_api_contract.py`, `tests/access/test_negative_access.py`, `tests/audit/test_audit_rebuild.py`, `policy/tests/test_policy_python.py`, `tests/security/test_client_flags_ignored.py`, and the `client` fixture in `tests/app/conftest.py` |
| First-app modules imported at the top of a file that has an asked test | `tests/app/test_storm_route.py` imports `alarm_service` and reads `alarm_service.DATA_DIR` at import time. `tests/app/test_recommend_route.py`, `tests/app/test_approvals_route.py`, `tests/app/test_demo_flow.py` and `tests/app/test_audit_row_keys.py` import `ai_gateway`, `approvals`, `policy`, `domain_service` or `audit`. Without a change, these files fail to load. |
| A way to send the audit log of the second app to a temporary file | The autouse fixture `audit_log` in `tests/app/conftest.py` and the fixture `log` in `tests/audit/test_audit_rebuild.py` |
| A way to send the approvals record of the second app to a temporary file | The autouse fixture `approvals_file` in `tests/app/conftest.py` |
| The folder of `alarms.csv` | `RQ-12` reads `ALARMS.read_bytes()` and lists the folder |

**Inference.** The simplest setup is a copy of the 22 tests (and the files they load) with only the imports and the fixtures changed. The assertions stay the same. Part 3 must say so, and must say which lines changed.

## 5. What the brief adds beyond the PRD

**Verified Fact.** One interface fact: the module path `apps/api_model_b/main.py`, a FastAPI object named `app`. The PRD does not name a framework. The brief also asks for a Python package. Nothing else in the brief comes from outside the PRD and the semantic layer.

The brief also attaches the two data files `devices.csv` and `alarms.csv`. The playbook (Part 2, step 2) lists only the semantic layer, the PRD, the traceability file and the tests. The app needs the two data files to run, and the tests name rows in them (`DEV-00002`, `STO-00005`, `STO-00019`).

## 6. Residual risks

| Risk | Label | Evidence | Effect on Part 3 |
|---|---|---|---|
| `RQ-18` asserts `body["summary"] == "Synthetic summary for " + GOOD_ID`. | **Verified Fact** that a search of `docs/prd/*.md`, `semantic-layer/*.yaml`, `glossary.md` and `README.md` found no such text. | `tests/app/test_recommend_route.py::test_healthy_recommend_is_hold_for_review_with_the_sentence` | A second app that writes another summary text fails this test. The failure shows a missing sentence in the PRD. It does not show that a meaning drifted. Mark it "unlisted" unless `docs/demo/evidence.md` lists it. |
| The storm tests assert the order of rows (`ALA-00005`, then `ALA-00004`) and the exact error body `{"error": "not_found"}`. | **Inference.** The PRD gives the error body (`RQ-03`). The row order is not stated in the rows read. | `tests/app/test_storm_route.py` | Same effect as the row above for the order. |
| The attached test files show first-app names (`alarm_service.DATA_DIR`, `audit.LOG`, `ai_gateway.call_model`). `conftest.py` is not attached. | **Verified Fact** | `tests/app/test_storm_route.py` line 5, `tests/audit/test_audit_rebuild.py` lines 36 to 39 | The second model may copy a module name. Part 3 should compare module names and say whether the copy happened. |
| The second model can open any file in the repository. The rule "read only the attached files" is not enforced. | **Assumption** | Brief section 2 | Part 3 should read the run log for any file outside the attached list. |
| `logs/audit.log` is tracked and changes on any run. If the second app writes the PRD path, it appends to the same file. | **Verified Fact** that the first app's log is tracked and modified (`git status`). **Unknown** whether the second app uses that path. | `docs/13-security-validation/evidence.md` (BL-09) | Restore the file with `git checkout -- logs/audit.log` after the run. |
| The 1.2.1 tree is not committed. | **Verified Fact** | `yaml-hashes-before.md`, header, "Residual risks" | Commit before Part 2. |

## 7. Part 3 follow-up

Part 3 should report the 22 results per app. It should list the 40 patch-based tests as "not run on the second app" and give the probe result for each PRD row they cover. It should list the page tests as "not run" and compare the two pages by reading them. This follows the decision in the header.
