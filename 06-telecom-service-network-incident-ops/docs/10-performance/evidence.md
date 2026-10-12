# Evidence — Half B

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The after measurement is recorded for both changes. The load-once tests pass (12 of 12). The full suite passes (209 passed, 2 skipped). Measured on one Windows machine. |
| Evidence sources | `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `tests/performance/test_load_once.py`; `tests/performance/test_engine_lookup_once.py`; `docs/10-performance/measure.py`; `measure-before.json`; `measure-before-rerun.json`; `measure-after-step1.json`; `measure-after.json`; `docs/10-performance/scaling-recommendations.md` |
| Assumptions | The four timing runs measure the same code paths with the same script. The machine was shared with other work, so single numbers move by up to 40 percent. Ranges and a back-to-back rerun are shown for that reason. |
| Unresolved issues | The refresh rule for `devices.csv` in production is Unknown. The cost of the `opa` path is Unknown (`opa` is not installed here). The speed-up on a Linux server is Unknown. |
| Residual risks | The app shows `devices.csv` as it was at the first call until it restarts. A program `opa` installed after the app starts is not noticed until it restarts. Both are stated limits, with a reset function for each. |

## What this file is

This file records what Half B changed, what the tests show, and the before and after measurements.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A measured number is **REAL**. A **Verified Fact** names a file path with a line, a test name, or a number from `measure.py`.

Decisions applied, as confirmed by Mangesh (FDE) on 2026-10-11 (`scaling-recommendations.md`, "Decisions before Half B"):

1. Id matching uses `device_id` only. The first row wins for a repeated id.
2. Reload is restart-only, with a reset function for tests.
3. The PATH-search cache in `policy.py` is a second, separate step with its own measurement.

## What changed

| Step | File | What it does |
|---|---|---|
| 1 (SR-01) | `apps/api/services/domain_service.py` lines 16 to 47 | Reads `devices.csv` once, at the first call. Builds an index from `device_id` to row (line 28, `setdefault`, so the first row wins). Returns a copy of the row (line 45). `reset_cache()` (line 33) makes the next call read again. A lock keeps eight threads on the first call to one read. A missing file raises at the first call and is not cached. |
| 2 (SR-02) | `apps/api/services/policy.py` lines 49 to 79 | `_opa_path()` searches the PATH for `opa` once per process (`lru_cache`). `engine_name()` (line 68) and `_opa_eval` (line 79) use it. `POLICY_ENGINE` is still read on every call. Access decisions are not cached. `reset_engine_cache()` (line 63) searches again on the next call. |

The public function `load_record(record_id: str)` keeps its name and argument. `list_recent` is unchanged (DA-04 in `data-access-findings.md`).

**Missing-id behaviour is unchanged.** An id that is not in the index returns the first row, as before (`domain_service.py` lines 46 and 47). **Verified Fact:** S04-03 Half B changed the role list only, and S07 has not run. Defect F01 stays open for S07.

## Behaviour check against the old code

Run once, with the old algorithm written out in the check (`record_id in row.values()`, first row wins):

| Check | Result |
|---|---|
| Rows in `devices.csv` | 354 |
| Distinct `device_id` values | 351 |
| `device_id` values where the new answer differs from the old | 0 of 351 |
| Other cell values tried (site ids, timestamps, status words, blank) | 729 |
| Of those, values whose answer changed | 718 |
| Id `DOES-NOT-EXIST` | Returns the first row (`REC-0001`), as before |

**Verified Fact. REAL.** The 718 changed answers are decision 1. An id such as `SIT-00002` used to return row 2. It now returns the first row, as any missing id does. The other 11 values return the first row under both rules.

## Tests

| Run | Result |
|---|---|
| Before Half B, `tests policy/tests semantic-layer/tests` | 191 passed, 2 skipped |
| `tests/performance/test_load_once.py` on the new code | 12 passed |
| The same file with the old loader put back for one run | 6 failed, 6 passed. The six that count reads or check the id rule fail. |
| `tests/performance/test_engine_lookup_once.py` on the new code | 6 passed |
| The same file with the cache switched off for one run | 5 failed, 1 passed. The one that passes checks the fail-closed answer. |
| After step 1, full suite | 203 passed, 2 skipped |
| After step 2, full suite | 209 passed, 2 skipped |

The two skips are the two Rego tests that need the `opa` program, which is not installed here. **Verified Fact.**

What each test file proves:

| Test | What it checks |
|---|---|
| `test_file_is_read_once_across_many_calls` | 1000 calls, existing and missing ids mixed, open the file once. |
| `test_real_file_is_read_once_across_many_calls` | The same on the real `devices.csv`. |
| `test_routes_read_the_file_once` | 20 calls to `GET /records/{id}` and one summary call open the file once. |
| `test_eight_threads_on_the_first_call_read_once` | Eight threads at the first call cause one read. |
| `test_reset_makes_the_next_call_read_again` | After `reset_cache()` the file is read again. |
| `test_result_is_a_copy` | A caller that edits the result cannot change the next answer. |
| `test_repeated_id_returns_the_first_row`, `test_missing_id_still_returns_the_first_row`, `test_empty_file_gives_the_error_body` | The first-row rules and the empty-file answer. |
| `test_only_device_id_is_matched` | A site id or hostname no longer finds a row (decision 1). |
| `test_every_device_id_in_the_real_file_finds_its_first_row` | All 351 ids return the first row for that id. |
| `test_a_missing_file_raises_and_is_not_cached` | The failure shows at the first call. The next call tries again. |
| `test_many_access_decisions_search_the_path_once` and `test_many_ai_decisions_search_the_path_once` | 200 access decisions and 100 AI decisions search the PATH once. |
| `test_the_setting_is_still_read_on_every_call` | `POLICY_ENGINE` still decides on every call. |
| `test_reset_searches_again`, `test_a_program_found_on_the_path_chooses_opa` | The stated limit and the reset. |
| `test_a_cached_program_that_is_gone_fails_closed` | When the cached program is gone, the answer is deny with reason `policy_engine_error`. |

The tests that touch routes write audit rows to a temporary folder. Running the full suite three times added 24 rows to `logs/audit.log` (163 to 187). The older tests write there, as `docs/09-ai-guardrails/` notes.

## Measurements

Same command for every run: `measure.py --rounds 5`. Median per call in milliseconds, with the fastest and slowest round in brackets.

| Item | Before, run 3 (18:34) | Before, rerun (19:02) | After step 1 (19:05) | After step 2 (19:07) |
|---|---|---|---|---|
| `load_record`, id exists | 2.170 (1.555 to 2.681) | 2.352 (1.505 to 2.394) | 0.0005 (0.0005 to 0.0037) | 0.0003 (0.0003 to 0.0021) |
| `load_record`, id missing | 2.858 (2.593 to 3.079) | 2.924 (2.470 to 3.666) | 0.0006 | 0.0003 |
| `load_record`, 8 threads, 1000 calls | 3.058 | 3.755 | 0.032 | 0.015 |
| `policy.check_record_read` | 5.644 (5.412 to 7.363) | 7.155 (6.063 to 10.584) | 6.125 (5.865 to 6.501) | 0.012 (0.009 to 0.045) |
| `ai_gateway.summarize_record` | 29.343 | 29.824 | 29.930 | 12.901 |
| Route `GET /health` | 3.925 | 4.188 | 3.975 | 3.569 |
| Route `GET /records/{id}` | 14.281 (13.807 to 14.453) | 16.031 (15.279 to 16.622) | 13.366 (13.176 to 14.190) | 5.805 (5.725 to 6.213) |
| Route `POST /ai/summarize/{id}` | 44.788 (44.133 to 45.338) | 46.615 (46.349 to 53.062) | 44.618 (43.451 to 53.677) | 29.038 (28.789 to 31.392) |
| `audit.write_event` | 0.526 | 0.691 | 0.630 | 0.594 |
| Peak memory of one `load_record` call | 404.1 KiB | 404.1 KiB | 0.5 KiB | 0.5 KiB |

All numbers are **REAL**. The files are `measure-before.json`, `measure-before-rerun.json`, `measure-after-step1.json`, and `measure-after.json`.

The `load_record` rows in the two "after" columns are calls that find the rows already loaded. The first call of the process still reads the file, once. The `GET /health` row did not change, as expected, because that route touches none of the changed code.

### What each step saved

| Step | Route | Saved per call, against the rerun | Saved per call, against run 3 | Predicted in Half A (Inference) |
|---|---|---|---|---|
| 1, load once | `GET /records/{id}` | 2.7 ms (17%) | 0.9 ms (6%) | About 1.7 ms (12%) |
| 1, load once | `POST /ai/summarize/{id}` | 2.0 ms (4%) | 0.2 ms (0.4%) | About 1.7 ms (4%) |
| 2, PATH search once | `GET /records/{id}` | 7.6 ms (57% of the step 1 figure) | same | About 5.6 ms (40%) |
| 2, PATH search once | `POST /ai/summarize/{id}` | 15.6 ms (35%) | same | About 16.9 ms (38%) |
| Both steps | `GET /records/{id}` | 10.2 ms (64%) | 8.5 ms (59%) | |
| Both steps | `POST /ai/summarize/{id}` | 17.6 ms (38%) | 15.8 ms (35%) | |

Worked example for both steps on `GET /records/{id}`: the rerun measured 16.031 ms before and 5.805 ms after. That is 10.226 ms less, or 64 percent. Against run 3 (14.281 ms) it is 8.476 ms less, or 59 percent.

Part of the route time is the test client, which `GET /health` shows at about 3.6 to 4.2 ms. Take that away and the work done by the route is about 11.8 ms before (16.031 − 4.188) and 2.2 ms after (5.805 − 3.569). **Inference:** the subtraction is only a guide, because the two figures come from different runs.

### Target check

| Target | Number | Owner | Result |
|---|---|---|---|
| `load_record` time per call, median of 5 rounds on this machine | At most 0.1 ms (PROPOSED) | Team-Force | Met. 0.0003 to 0.0005 ms, which is 0.3 to 0.5 microseconds. |

This is an engineering check, not a service level.

## Findings

### HB-01

| | |
|---|---|
| Finding | Load once removes the file read from every device lookup. |
| Evidence | **Verified Fact. REAL.** `load_record` fell from 2.170 and 2.352 ms to 0.0005 ms per call. Peak memory per call fell from 404.1 KiB to 0.5 KiB. The 12 tests in `test_load_once.py` pass. |
| Impact | The lookup no longer limits how many requests one process can finish. Route time fell by 0.9 to 2.7 ms. The saving matches the Half A prediction of about 1.7 ms, within the noise. |
| Risk | Low. The app shows the file as it was at the first call. Nothing in the repo writes the file (`data-and-integration-map.md` line 26). |
| Confidence | High for the counts and the per-call figure. Medium for the route saving, which moves between runs. |
| Open questions | Does production replace `devices.csv` while the app runs? Unknown. Owner of the refresh rule: Team-Force. |

### HB-02

| | |
|---|---|
| Finding | Caching the PATH search saved more than load once. |
| Evidence | **Verified Fact. REAL.** The access decision fell from 5.644 and 7.155 ms to 0.012 ms. `GET /records/{id}` fell from 16.031 to 5.805 ms against the rerun. `POST /ai/summarize/{id}` fell from 46.615 to 29.038 ms. The tests count one search across 100 and 200 decisions. |
| Impact | Triage reads and summaries start about 6 ms sooner for each access decision. The summary route runs three, so it gains about 16 ms. |
| Risk | Low. Decisions are not cached. `POLICY_ENGINE` is still read each time. If the cached program disappears, the answer is deny with `policy_engine_error` (`test_a_cached_program_that_is_gone_fails_closed`). |
| Confidence | High that the step saved this time on this machine. The saving is larger than the 5.6 ms search measured alone, and part of the extra is noise. The cause of the rest is Unknown. |
| Open questions | The saving on a Linux server with a short PATH. Unknown. The cost of the `opa` path. Unknown. |

### HB-03

| | |
|---|---|
| Finding | Matching on other columns has stopped, as decided. |
| Evidence | **Verified Fact. REAL.** 718 of 729 non-id cell values now return the first row. All 351 `device_id` values return the same row as before. `test_only_device_id_is_matched` and `test_every_device_id_in_the_real_file_finds_its_first_row` pass. |
| Impact | A site id, a timestamp, or a status word typed as an id can no longer return a device at random. It gets the first row, as any missing id does. That wrong answer is defect F01. |
| Risk | Medium until S07 turns the missing-id answer into a 404. The first-row answer still hides a bad id. |
| Confidence | High. |
| Open questions | Which stage returns the 404. S07 is the stage named in the defect list. |

### HB-04

| | |
|---|---|
| Finding | The summary route still waits on the model while holding a route thread. Half B did not change this. |
| Evidence | **Verified Fact.** Step 2 changed the policy only. The stub wait is still 10.6 ms (`ai_gateway.call_model`, unchanged). The thread limit of 40 is unchanged. |
| Impact | The thread-bound figures in `load-scenarios.md` section 1b still hold: 20 summaries a second at a 2 second wait, 4 at a 10 second wait. |
| Risk | High once a real model replaces the stub. Low today. |
| Confidence | Medium. The model wait is Unknown. |
| Open questions | SR-04 stays a proposal. The playbook excludes async rewrites. |

## What the numbers do not show

- **One machine.** Windows 11, Python 3.13.5, 8 CPUs, shared with other work. A Linux server with a short PATH would show a smaller step 2 gain. Not measured.
- **Test client time.** Every route figure includes about 3.6 to 4.2 ms of it.
- **The `opa` path.** Not measured. The program is absent here.
- **Real load.** Each item ran one call after another. The numbers do not show many callers at once.
- **Run to run.** The same code measured 14.281 and 16.031 ms on `GET /records/{id}` in two runs. Read the ranges.

## Effect on the Half A documents

- **Line numbers.** `performance-baseline.md`, `bottleneck-list.md`, `load-scenarios.md`, and `data-access-findings.md` cite lines of the code before Half B (`domain_service.py` lines 8 to 15, `policy.py` lines 54, 59, 124, and 236). They describe the baseline and stay as written. The new lines are in the table "What changed" above.
- **Costs in `load-scenarios.md`.** The costs A, B, and C are the before costs. A note at the end of that file gives the after costs.

## How to run it again

From `06-telecom-service-network-incident-ops`:

```text
.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q
.venv\Scripts\python.exe docs\10-performance\measure.py --rounds 5 --json docs\10-performance\measure-after.json
```

Open question for S03: the YAML has no metric id for record read latency. The 0.1 ms check above needs an id to hold it, the way `metric.recommendation_latency` holds the model call. (Repeated from `scaling-recommendations.md`.)

## Lifecycle

Stage S04-11 reuses `load-scenarios.md` and the loader. Its "CSV file missing" mode now fails at the first call and not on every call (`test_a_missing_file_raises_and_is_not_cached`). Its "policy engine unavailable" mode fails closed, as the test above shows. Stage S07 builds `/alarms/storms` on the indexed loader and turns the missing-id answer into a 404. Stage S09 cites the before and after in this file.
