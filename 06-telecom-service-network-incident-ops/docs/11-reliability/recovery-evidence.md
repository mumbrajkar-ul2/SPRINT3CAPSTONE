# Recovery evidence

| Field | Value |
|---|---|
| Stage | S04-11 Reliability and failure engineering (Challenge 11), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), built with Cursor |
| Status | CONDITIONAL PASS. All 46 reliability tests pass, including the impossible-timestamp drill. The full suite passes (255 passed, 2 skipped). The AI-timeout drill returns no summary. Three numbers are PROPOSED and need an owner decision (see "Open items"). |
| Evidence sources | `tests/reliability/test_drills.py` (24 tests); `tests/reliability/test_breaker.py` (22 tests); `docs/11-reliability/proof_runs.py`; `apps/api/services/breaker.py`; `apps/api/services/dedupe.py`; `apps/api/services/audit.py`; `apps/api/services/ai_gateway.py`; `etl/run_daily_batch.py`; `semantic-layer/business-rules.yaml`; Half A files in this folder |
| Assumptions | Python 3.13.5 on Windows. Tests replace the model function and the audit log path. They call the real routes and read the real data files. Nothing is written under `data/synthetic/`. |
| Unresolved issues | OQ-1: a refused model call reports `timeout_hit` true. That is an interim reason. The three breaker numbers are PROPOSED. Owner: Team-Force. |
| Residual risks | Durations come from one machine. The dedupe memory and the audit lock cover one process only. A second server process would repeat both problems. Production traffic and model wait times are Unknown. |

## How to repeat every run

From `06-telecom-service-network-incident-ops/`:

```text
.venv\Scripts\python.exe -m pytest tests/reliability -v -p no:cacheprovider
.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q -p no:cacheprovider
.venv\Scripts\python.exe docs/11-reliability/proof_runs.py
```

## Run 1. The drills (46 tests, all passed)

Result line: `46 passed in 10.29s`.

| Drill | Failure injected | Test names (all PASSED) | What the test checks |
|---|---|---|---|
| DR-1 | Request with no correlation id | `test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it`; `test_dr1_a_blank_correlation_id_is_replaced_and_a_sent_one_is_kept`; `test_dr1_the_event_stream_has_blank_ids_and_the_dedupe_key_does_not_use_them` | The API creates a UUID and writes it to the audit row. A sent id is kept. 1992 of 3000 events have a blank id, so the event key uses `event_id`. |
| DR-2 | AI model does not answer in time | `test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up`; `test_dr2_a_model_error_is_held_and_health_stays_up` | Status 202, outcome HOLD_FOR_REVIEW. Summary and recommendation are null. The text has none of "Synthetic summary for", "Review and approve before action", or "SIMULATED". `/health` and `/records/{id}` return 200. The audit action is `policy.hold`. |
| DR-3 | Same message sent twice | `test_dr3_the_same_alarm_sent_twice_is_one_alarm_by_dedupe_key`; `test_dr3_same_dedupe_key_in_another_storm_is_a_different_alarm`; `test_dr3_a_blank_key_part_is_held_aside_and_never_recorded`; `test_dr3_all_354_alarm_rows_give_350_new_3_repeats_1_held_aside`; `test_dr3_all_354_order_rows_give_351_new_2_repeats_1_held_aside`; `test_dr3_replaying_the_event_file_twice_gives_3000_new_and_3000_repeats`; `test_dr3_the_summary_route_has_no_key_so_five_calls_cost_five_model_calls_and_five_rows` | Alarms 350 new, 3 repeat, 1 held aside. Orders 351, 2, 1. Events replayed twice: 3000 new, 3000 repeat. The summary route has no key, so five calls cost five model calls (Half A finding, left as it is). |
| DR-4 | Stale master data | `test_dr4_a_true_stale_flag_is_blocked_and_the_model_is_not_called`; `test_dr4_a_blank_stale_flag_is_held_for_review_and_the_model_is_not_called`; `test_dr4_a_false_flag_still_gets_a_summary`; `test_dr4_192_rows_are_true_and_1_is_blank` | `stale_topology_flag` true gives 403 BLOCK (DEV-00003) and the model is called 0 times. Blank gives 202 HOLD (DEV-BAD1). False gives 200. The file has 192 true and 1 blank. This keeps decision D-1. |
| DR-5 | Partial batch failure | `test_dr5_one_bad_row_is_reported_and_the_rest_are_processed`; `test_dr5_short_long_and_undecodable_rows_are_held_aside_and_the_run_goes_on`; `test_dr5_the_real_file_keeps_its_old_counts_and_adds_one_quarantined_row` | On a temp copy, one blank cell gives `{"processed":4,"malformed":1,"sample":True,"quarantined":1}`. Short, long, and undecodable rows are held aside: processed 6, quarantined 3. The real file gives processed 354, malformed 1, quarantined 1. Each held row is named on stderr. No file is written. |
| DR-6 | Impossible timestamp (ALA-00002) | `test_dr6_ala_00002_is_flagged_and_does_not_become_an_incident`; `test_dr6_the_rule_id_exists_in_business_rules_yaml`; `test_dr6_equal_times_are_fine_and_later_last_seen_is_fine`; `test_dr6_blank_or_unreadable_times_are_flagged_for_review`; `test_dr6_the_real_file_has_166_rows_before_and_1_unreadable_and_none_become_incidents` | ALA-00002 has `last_seen_at` before `first_seen_at`. It is flagged with rule id `rule.alarm_last_seen_not_before_first_seen`, which exists in `business-rules.yaml`. It does not become an incident candidate. Equal times pass. Blank or mixed-zone times are flagged. In the real file 166 rows are last-before-first and 1 is unreadable. All 354 rows are accounted for. |

Other tests in `test_breaker.py` (22): nine breaker unit tests with a fake clock, one defaults test, seven bad-setting tests, four route tests, and the audit-lock test.

## Run 2. The full suite

Command: `.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q -p no:cacheprovider`

Result: `255 passed, 2 skipped`. Before this half: 209 passed, 2 skipped. The difference is 46, the new reliability tests. The 2 skips need the `opa` binary, which this machine does not have. No earlier test needed a change to pass, except one rename (see "Changes to earlier files").

## Run 3. Proof runs: each drill fails when its protection is off

A drill that still passes with its protection off proves nothing. `proof_runs.py` turns one protection off inside the test process and runs the matching drill. Nothing on disk changes.

| Protection turned off | Test that guards it | Result | Failure shown |
|---|---|---|---|
| Audit write lock | `test_eight_threads_writing_the_audit_log_lose_no_row` | 1 failed | `JSONDecodeError: Expecting value: line 1 column 1` |
| Breaker and in-flight limit | The four `route_` tests | 3 failed, 1 passed | `assert 'closed' == 'open'` (twice). `/health` took 1.43 s, test limit 0.5 s |
| New ETL (original file from git HEAD put back for one run) | The three `dr5` tests | 3 failed | Counts differ; `quarantined` key is missing (`KeyError: 'quarantined'`) |

The one route test that passes with the breaker off is `test_route_a_bad_answer_does_not_open_the_breaker`. That is correct. It checks that the breaker stays closed, and a missing breaker is always closed.

After the ETL proof run the new `etl/run_daily_batch.py` was restored. A later run of the real file printed the new counts.

## Run 4. Before and after, in numbers

| Item | Before (original code) | After (this half) | How measured |
|---|---|---|---|
| Audit rows written by 8 threads, 250 each (2000 expected) | 1849 lines when the lock is off (151 rows lost). One earlier run raised a parse error. | 2000 lines, 2000 distinct ids, in 3 repeats | One run, Windows. The number lost varies from run to run. |
| `/health` while 50 summaries hang the model for 2 s | 1.43 s (breaker and limit off) | Under 0.5 s (limit 10 calls at once). Model called 10 times. 10 answers 200, 40 answers 202 with no summary. | `test_route_a_hung_model_does_not_hold_every_route_thread` |
| Model calls after the breaker opens (threshold 2) | Every call reaches the model | 0 new calls. Answer returns in under 0.2 s with HOLD_FOR_REVIEW. | `test_route_the_model_is_not_called_once_the_breaker_is_open` |
| ETL real file output | `{"processed":354,"malformed":1,"sample":...}` | `{'processed': 354, 'malformed': 1, 'sample': False, 'quarantined': 1}` plus `quarantined: file line 353: blank cell` on stderr | `python etl/run_daily_batch.py` |
| ETL on one short row, one long row, or one byte that is not UTF-8 | Short and long rows counted as processed with nothing reported. One bad byte stopped the run. | Each row is held aside and named. The run continues. | `test_dr5_short_long_and_undecodable_...` |
| Alarm rows with last time before first time (166) | Pass through intake with no check | Flagged with the rule id. None become candidates. | `test_dr6_the_real_file_has_166_...` |

## What each failure now does

| Failure | Reply to the user | What is recorded | What stays up |
|---|---|---|---|
| Model times out or errors | 202, HOLD_FOR_REVIEW, no summary | Audit row `policy.hold` with reason `failmode.timeout` | `/health`, `/records/{id}` |
| Breaker open or 10 calls already running | 202, HOLD_FOR_REVIEW, no summary, no model name | Audit row `policy.hold`, model null | `/health`, `/records/{id}` |
| Stale flag true | 403 BLOCK | Audit row `policy.deny` | All other routes |
| Stale flag blank | 202 HOLD_FOR_REVIEW | Audit row `policy.hold` | All other routes |
| Bad ETL row | Row named on stderr | Counted in `quarantined` | The rest of the batch |
| Duplicate alarm, order, or event | Counted as repeat | Not entered twice in the dedupe memory | Intake |
| Alarm times out of order | Flagged with the rule id | Not a candidate | Intake |

## Changes to earlier files

- `tests/characterization/test_current_behaviour.py`: the ETL test was renamed from `test_etl_counts_blank_fields_and_does_not_quarantine` to `test_etl_counts_blank_fields_and_keeps_its_old_count_meaning`. The old name said the ETL does not quarantine. It now does. The test still locks the three old keys.
- `apps/api/services/audit.py`: writes go through one lock (decision D-3).
- `apps/api/services/ai_gateway.py`: the model call asks the breaker first.
- `apps/api/settings.py`: two helper functions read whole-number and decimal settings.
- `tests/conftest.py`: new. It clears the breaker before and after every test, so failure counts do not carry from one test to the next.
- `.env.example`: three new names with PROPOSED comments.
- `logs/audit.log`: grew by 186 lines. Older tests that call the real routes write to this file. The new drills write to temporary files.

## Open items

| Item | Value now | Status | Owner |
|---|---|---|---|
| `BREAKER_FAILURE_THRESHOLD` | 5 failures in a row | PROPOSED | Team-Force |
| `BREAKER_OPEN_SECONDS` | 30 | PROPOSED | Team-Force |
| `MODEL_MAX_IN_FLIGHT` | 10 | PROPOSED | Team-Force |
| `AI_MODEL_TIMEOUT_SECONDS` | 10 (from S04-09) | PROPOSED | Team-Force |
| OQ-1: reason name for a breaker refusal | `timeout_hit` true as an interim | Open | Team-Force |
| One server process only | Dedupe memory and audit lock do not span processes | Known limit | S07 build decides storage |
| Summary route has no idempotency key | Five calls cost five model calls | Known limit, kept as is | S07 |
| Missing id on `GET /records/{id}` returns the first row (F01) | Unchanged | Left for S07 | Team-Force |
