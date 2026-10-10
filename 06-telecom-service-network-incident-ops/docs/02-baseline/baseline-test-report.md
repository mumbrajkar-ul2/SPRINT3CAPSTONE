# Baseline test report

| Field | Value |
|---|---|
| Stage | S02 — Behavioural baseline (Execution Plan Phase 2; spine stage 7) |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The test commands passed. Five labels in `data/quality_issues.json` were not found in the files. That condition is written in `data-quality-baseline.md`. |
| Evidence sources | `python -m pytest -q -v` before the new tests; `python -m pytest --collect-only -q`; `python -m pytest -q`; `python -m pytest -v --tb=no -p no:cacheprovider`; `tests/test_api_contract.py`; `tests/test_characterization.py`; `tests/characterization/test_current_behaviour.py`; `docs/00-setup/replay-log.md` |
| Assumptions | The `.venv` in this repo already has `httpx`. This stage did not repeat the clean-install collection error from the replay. |
| Unresolved issues | The replay log names `test_missing_record_returns_first_row`. The file defines `test_legacy_missing_record_behavior_is_characterized`. This stage did not edit that file. |
| Residual risks | These tests lock current behaviour. A later fix of the missing-id return will fail `test_missing_id_returns_first_row` until that test is replaced. |

## What this file is

This file records the test run for the inherited repo on 2026-10-10. The first run happened before any new test file existed. The second run includes the five new characterization tests. No application file was edited. `tests/test_api_contract.py` and `tests/test_characterization.py` were not edited.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Run before the new tests

Command, from `06-telecom-service-network-incident-ops`, with `PYTHONDONTWRITEBYTECODE=1`:

```text
python -m pytest -q -v
```

Result: **3 passed, 2 warnings in 0.98s**. Exit code 0. **Verified Fact.**

The same tree, collected before the new file existed:

```text
python -m pytest --collect-only -q
```

```text
tests/test_api_contract.py::test_health_contract
tests/test_api_contract.py::test_ai_summary_has_minimum_contract
tests/test_characterization.py::test_legacy_missing_record_behavior_is_characterized

3 tests collected in 0.66s
```

**Verified Fact.** Three tests exist in the inherited suite. The replay log section 1.3 also says three tests passed. The name in that log is `test_missing_record_returns_first_row`. The name in the file today is `test_legacy_missing_record_behavior_is_characterized`. **Verified Fact:** `docs/00-setup/replay-log.md` section 1.3 and `tests/test_characterization.py` lines 3 to 7. `docs/01-discovery/brownfield-risk-register.md` row R24 already records this difference.

| Test | Result |
|---|---|
| `tests/test_api_contract.py::test_health_contract` | PASSED |
| `tests/test_api_contract.py::test_ai_summary_has_minimum_contract` | PASSED |
| `tests/test_characterization.py::test_legacy_missing_record_behavior_is_characterized` | PASSED |

The two warnings in that run (**Verified Fact**, pytest output):

- `starlette/testclient.py:40` — an anyio alias warning inside the installed library.
- `apps/api/services/audit.py:9` — `datetime.utcnow()` is deprecated. The warning fired on `test_ai_summary_has_minimum_contract`, because that test calls the summary route and the route writes an audit line.

`test_health_contract` checks `GET /health` returns 200 and `status` equal to `ok` (`tests/test_api_contract.py` lines 6 to 8).

`test_ai_summary_has_minimum_contract` posts `/ai/summarize/REC-0001` and checks that `summary`, `model`, and `guardrail_status` are present (lines 11 to 16).

`test_legacy_missing_record_behavior_is_characterized` calls `domain_service.load_record('DOES-NOT-EXIST')` and asserts the result is a non-empty dict (lines 3 to 7). It does not assert `device_id` `REC-0001`. The new test below does assert that id.

## Run after the new tests

Command:

```text
python -m pytest -q
```

Result: **8 passed, 5 warnings in 1.21s**. Exit code 0. **Verified Fact.** The output line is eight dots, then the warning block, then `8 passed, 5 warnings in 1.21s`.

Named results from the same tree:

```text
python -m pytest -v --tb=no -p no:cacheprovider
```

**8 passed, 5 warnings in 1.32s**. Exit code 0. **Verified Fact.**

| Test | Result | Where it comes from |
|---|---|---|
| `tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row` | PASSED | New in this stage |
| `tests/characterization/test_current_behaviour.py::test_clinician_role_is_accepted_on_record_read` | PASSED | New in this stage |
| `tests/characterization/test_current_behaviour.py::test_ai_summarize_accepts_request_with_no_role_header` | PASSED | New in this stage |
| `tests/characterization/test_current_behaviour.py::test_etl_counts_blank_fields_and_does_not_quarantine` | PASSED | New in this stage |
| `tests/characterization/test_current_behaviour.py::test_legacy_script_holds_password_constant` | PASSED | New in this stage |
| `tests/test_api_contract.py::test_health_contract` | PASSED | Inherited |
| `tests/test_api_contract.py::test_ai_summary_has_minimum_contract` | PASSED | Inherited |
| `tests/test_characterization.py::test_legacy_missing_record_behavior_is_characterized` | PASSED | Inherited |

Count: **3 inherited tests + 5 new characterization tests = 8 passed.**

Each new test docstring is: `characterization: locks current behaviour; replace when the defect is fixed`.

The five warnings in the full run are one anyio library warning plus four `datetime.utcnow()` warnings. The four tests that write an audit line are the three new route tests and `test_ai_summary_has_minimum_contract`. **Verified Fact:** the pytest warning block names those four tests.

This run used Python 3.13.5 and pytest 8.3.2, from the pytest header. **Verified Fact.** `.github/workflows/ci.yml` names Python 3.11. Whether this suite passes on 3.11 was not run in this stage. **Unknown.**

## What the new tests lock

| Test | Behaviour it locks |
|---|---|
| `test_missing_id_returns_first_row` | `load_record("DOES-NOT-EXIST")` and `GET /records/DOES-NOT-EXIST` with role `operator` both return `device_id` `REC-0001`. |
| `test_clinician_role_is_accepted_on_record_read` | `GET /records/REC-0001` with `X-User-Role: clinician` returns HTTP 200 and `device_id` `REC-0001`. |
| `test_ai_summarize_accepts_request_with_no_role_header` | `POST /ai/summarize/REC-0001` with no role header returns HTTP 200 and a body that contains `summary`. |
| `test_etl_counts_blank_fields_and_does_not_quarantine` | `etl/run_daily_batch.py --sample` sets `processed` to the row count, sets `malformed` to the number of rows with a blank field, leaves `devices.csv` byte-for-byte the same, and adds no file under `data/`. |
| `test_legacy_script_holds_password_constant` | `legacy/reconcile_legacy.py` assigns the name `SHARED_DB_PASSWORD` to a non-empty string. The test does not read that string into the assertion message. |

The password value is not printed in this report.

## Side effect of the test run

The route tests append lines to `logs/audit.log`. **Verified Fact:** `apps/api/services/audit.py` lines 7 to 12, and the warning on `audit.py` line 9. This stage copied the log before the first pytest and restored that copy after the runs. The file on disk is again the 13-line log from the start of the stage. Four of those lines are timestamped `2026-10-10T05:51`. They were already in the file before this stage's commands. The lines this stage wrote, and then removed by the restore, are quoted in `behaviour-snapshot.md`.

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and the test files under `tests/`. Stage S03 harvests status words from `data-quality-baseline.md`. Stage S04 Half A cites `defect-list.md`. Stages S05 to S14 use `behaviour-snapshot.md` as the before picture.
