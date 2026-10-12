# Failure-mode catalogue

| Field | Value |
|---|---|
| Stage | S04-11 — Reliability and failure engineering (Challenge 11), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Fifteen failure modes are listed. Each has a trigger, what the user sees, what data could be wrong, the business effect, how it is detected, and a YAML id or an open question. Thresholds proposed elsewhere in this stage are PROPOSED with owner Team-Force. |
| Evidence sources | `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `etl/run_daily_batch.py`; `semantic-layer/business-rules.yaml`; `semantic-layer/ai-context-policy.yaml`; `semantic-layer/metrics.yaml`; `docs/runbooks/failure-injection-drills.md`; `docs/09-ai-guardrails/unsafe-output-handling-rules.md`; `docs/08-observability/trace-design.md`; `docs/10-performance/load-scenarios.md`; `docs/10-performance/evidence.md`; `docs/11-reliability/probe_half_a.py` and its output `probe-output.json` (run 2026-10-11, Windows, Python 3.13.5) |
| Assumptions | The probe calls the app in memory with the real routes and real data files. It replaces only the model function and the audit log path. A probe result is a Verified Fact about this machine. A different operating system can behave differently. Team-Force owns every PROPOSED item (operating contract row 10). |
| Unresolved issues | The playbook says a true `stale_topology_flag` gives HOLD_FOR_REVIEW. The YAML and the running code say BLOCK (finding FM-07). The locked fact "no timeout, no fail-to-person" describes the repo before S04-09. Both are explained under "Two statements that need a decision". Seven open questions for S03 are listed at the end. |
| Residual risks | The probe ran each failure once, or three times where stated. It is not a load test. Production request rates, model wait, and server layout are Unknown. |

## What this file is

This file lists how the system fails today. It does not change any code.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file with a line, a test name, or a probe check id from `probe-output.json`. A measured number is **REAL**.

The probe script is `docs/11-reliability/probe_half_a.py`. It writes audit rows to a temporary folder. It changed no repo file. Check Z in the output shows `logs/audit.log` grew by 0 bytes during the run.

## Two statements that need a decision

**1. The locked fact about AI-down behaviour is out of date.** The locked fact says the repo has no timeout, no breaker, and no fail-to-person path. That was true at the baseline (`Project_Intent - Section 3.1 Row 8.md`). Since S04-09 the gateway has a timeout (`ai_gateway.py` lines 53 and 299) and a hold path (`ai_gateway.py` line 383). The breaker is still absent. This stage records both the baseline and the code as it is now.

**2. The playbook and the YAML disagree on a true stale flag.** Half B says "stale_topology_flag true yields HOLD_FOR_REVIEW". The YAML id `failmode.stale_topology_true` says BLOCK. The running code returns BLOCK with HTTP 403 (probe check P10). A blank flag returns HOLD_FOR_REVIEW (`failmode.stale_topology_blank`). This stage keeps the YAML meaning. The Half B drill will expect BLOCK for a true flag and HOLD_FOR_REVIEW for a blank flag. `unsafe-output-handling-rules.md` finding UO-02 already made the same choice.

## Summary table

| Id | Failure mode | User sees today | Worst effect | Severity of effect |
|---|---|---|---|---|
| FM-01 | Request has no correlation id | Normal answer. A new UUID is on the response header. | None on success. A 500 error has no id. | Low |
| FM-02 | Event line has no correlation id | Nothing. No code reads events. | 1992 of 3000 lines cannot be grouped into a chain. | Medium |
| FM-03 | AI call times out | HTTP 202, HOLD_FOR_REVIEW, no summary. | No recommendation. Nobody is told. | Medium |
| FM-04 | AI call raises an error | HTTP 202, HOLD_FOR_REVIEW, reason says schema failure. | A model outage looks like a bad answer. | Medium |
| FM-05 | A caller sends the same summary request again | Each send gets a full answer. | One extra model call and one extra audit row per send. | Low |
| FM-06 | Replay of events, alarms, or orders | No code reads these files. | 3000 duplicate events per pass if a reader existed. | Medium |
| FM-07 | Stale topology data | Summary BLOCK (true) or HOLD (blank). The record read shows the row with no warning. | An operator can trust a stale device row. | High |
| FM-08 | Daily batch hits a bad row | Short and long rows count as good. A bad line stops the run and prints nothing. | The batch loses all its counts. | High |
| FM-09 | Alarm with last_seen_at before first_seen_at | No code reads alarms. | 166 of 354 rows would give a negative duration. | Medium |
| FM-10 | `devices.csv` is missing | HTTP 500 plain text. No audit row. | Both business routes stop. `/health` still says ok. | High |
| FM-11 | Policy engine fails | HTTP 403 `forbidden` for every caller. | An outage looks like a refusal. | High |
| FM-12 | Audit log cannot be written | HTTP 500 on every business route. | No answer without an audit row. The model has already run on a summary. | High |
| FM-13 | Several threads write the audit log at once | Nothing visible. | 71 to 109 of 2000 rows lost per round. | High |
| FM-14 | The model hangs | Summaries return HOLD after the deadline. Other routes slow down. | `/health` and `/records` wait for a free thread. | High |
| FM-15 | Device id not found | Record read returns the first row with HTTP 200. | A person acts on the wrong device. | High |

Worked example for FM-13: 8 threads each wrote 250 rows, so 2000 rows were expected. The three rounds recovered 1891, 1929, and 1915 distinct rows. That is 109, 71, and 85 rows lost.

## FM-01 — Request has no correlation id

| | |
|---|---|
| Trigger | A caller sends no `X-Correlation-Id` header, or sends only spaces. |
| What the user sees today | The normal answer. The response header `X-Correlation-Id` holds a new UUID. A sent value such as `demo-123` is kept. A blank value is replaced. **Verified Fact:** `main.py` lines 13 to 19; probe P1. |
| What data could be wrong | None on a successful call. The audit row for a record read holds the id (probe P1b). |
| Business effect | Before S04-08 an audit row could not be tied to a request. That gap is closed for success paths. A 500 error response has no `X-Correlation-Id` header, because the middleware sets the header only after the route returns (`main.py` lines 17 to 18; probe P7 check `record_read_has_correlation_header` and probe P8 check `has_correlation_header_on_500`). The caller cannot quote an id for a failed call. |
| Detection today | None for a missing header. The id is created, so no row is blank. For a 500 error there is no detection. |
| YAML id | `rule.audit_row_names_actor_and_correlation`; `metric.audit_completeness` |
| Drill | Missing correlation id (Half B drill 1). |
| Confidence | High |
| Open questions | None new. |

## FM-02 — Event line has no correlation id

| | |
|---|---|
| Trigger | A line in `events.jsonl` has `correlation_id` null or an empty string. |
| What the user sees today | Nothing. No route reads the file. **Verified Fact:** `data-access-findings.md` DA-03. |
| What data could be wrong | A group-by on `correlation_id` that treats blank as one id merges unrelated lines. **Verified Fact. REAL:** 1992 of 3000 lines have no id (probe D3). 1008 have one. |
| Business effect | Those 1992 lines cannot be placed in a request chain. A replay cannot use the chain id to find a duplicate for them. |
| Detection today | A count of blank ids. Nothing runs it on a schedule. |
| YAML id | `field.event.correlation_id` is a field, not a rule. No rule id exists for the event stream. See open question OQ-3. |
| Drill | Missing correlation id in event streams (`failure-injection-drills.md` line 3). The Half B drill covers the request path. The event stream is covered by the idempotency plan. |
| Confidence | High |
| Open questions | OQ-3. |

## FM-03 — AI call times out

| | |
|---|---|
| Trigger | The model does not answer before `AI_MODEL_TIMEOUT_SECONDS`. The default is 10 seconds. It is PROPOSED. Owner: Team-Force. |
| What the user sees today | HTTP 202. `outcome` HOLD_FOR_REVIEW. `summary` null. `recommendation` null. The call returned after 113 ms with a 0.1 s deadline. **Verified Fact:** `ai_gateway.py` lines 295 to 301; probe P2; test `test_gr05_timeout_is_held_with_no_summary`. |
| What data could be wrong | Nothing is stored. The audit row has `outcome` HOLD_FOR_REVIEW and `prompt_hash` set (probe P2, `audit_outcome`). |
| Business effect | The person who triages gets no recommendation and does the work by hand. No inbox, queue, or notice exists for the held case. The case exists only as the HTTP 202 body and one audit row. **Verified Fact:** `main.py` has three routes and none lists held cases. |
| Detection today | An audit row with action `policy.hold`. No alert reads it. `otel-notes.md` says there are no service levels and no dashboard as code. |
| YAML id | `failmode.timeout`; `policy.fail_to_person`; `outcome.hold_for_review` |
| Extra finding | `reasons` holds two ids: `failmode.schema_failure` and `failmode.timeout`. The schema was never checked on a timeout. The policy treats an unset schema flag as "not ok" (`policy.py` line 233). The existing test checks only that `failmode.timeout` is present, so it does not catch the extra id. |
| Drill | AI timeout (Half B drill 2). |
| Confidence | High |
| Open questions | Whether the extra reason id is acceptable. It belongs to S04-09. This stage reports it and does not change it. |

## FM-04 — AI call raises an error

| | |
|---|---|
| Trigger | The model call raises an error, for example a refused connection. |
| What the user sees today | HTTP 202. HOLD_FOR_REVIEW. `summary` null. `reasons` is `failmode.schema_failure` only. **Verified Fact:** `ai_gateway.py` line 303 catches every error and sets the schema flag false; probe P3; test `test_gr04_a_model_that_raises_is_held`. |
| What data could be wrong | None. |
| Business effect | A person reading the reason thinks the model gave a bad answer. The model was not reachable. A model outage and a bad answer need different action. |
| Detection today | The audit row has `outcome` HOLD_FOR_REVIEW and `latency_ms`. It does not hold the reason. |
| YAML id | Nearest id is `failmode.schema_failure`. No id says the model was unavailable. Open question OQ-1. |
| Drill | Part of Half B drill 2. |
| Confidence | High |
| Open questions | OQ-1. |

## FM-05 — A caller sends the same summary request again

| | |
|---|---|
| Trigger | A client retries `POST /ai/summarize/{id}` after a slow answer or a lost response. |
| What the user sees today | A full answer each time. Five identical calls with the same correlation id gave five HTTP 200 answers, five model calls, and five audit rows (probe P4). |
| What data could be wrong | No stored business row changes. No code in `apps/` mentions `alarms.csv`, `service_orders.csv`, `incidents.csv`, or `events.jsonl` (probe P4, `alarm_incident_or_order_writers_in_apps` is 0). |
| Business effect | Each extra send costs one model call and adds one audit row. The cost per call is Unknown until S04-12. The audit trail shows five identical summaries for one request chain. |
| Detection today | Count audit rows by `correlation_id`. Nothing does it automatically. |
| YAML id | None. The summary route changes no state, so no business rule applies. |
| Drill | Duplicate replay (Half B drill 3) uses an alarm, not this route. This row answers defence question 4 for the live route. |
| Confidence | High for the count. |
| Open questions | None. |

## FM-06 — Replay of events, alarms, or orders

| | |
|---|---|
| Trigger | A reader processes `events.jsonl`, `alarms.csv`, or `service_orders.csv` more than once, or a feed delivers a line twice. |
| What the user sees today | Nothing. No code reads these files. **Verified Fact:** probe P4 check above; `data-access-findings.md` DA-03. |
| What data could be wrong | **Verified Fact. REAL** (probe D1 to D3). Events: 3000 lines, 3000 distinct `event_id`, 3000 distinct `payload_hash`. Alarms: 354 rows. Three `dedupe_key` and `storm_batch_id` pairs appear twice. Orders: 353 numeric `retry_count` values add up to 943,094. Three order ids appear twice. |
| Business effect | A second pass over the event file would add 3000 duplicate events. A replay of the alarm file with no grouping would add 3 duplicate alarms, each needing a device lookup and a summary. If a retry were sent for every retry the order file records, the repeat would be 943,094 attempts. That last figure is **EDUCATIONAL**. Nothing builds those attempts today. |
| Detection today | None. |
| YAML id | `rule.duplicate_dedupe_key_in_storm_is_one_alarm`; `rule.one_row_per_key`; `metric.retry_count`. No rule id covers a repeated event or a repeated order attempt. Open question OQ-3. |
| Drill | Duplicate replay (Half B drill 3). |
| Confidence | High for the counts. |
| Open questions | OQ-2 (event sequence), OQ-3 (rule id). |

## FM-07 — Stale topology data

| | |
|---|---|
| Trigger | A device row has `stale_topology_flag` true (192 rows) or blank (1 row, `DEV-BAD1`). 161 rows are false. **Verified Fact. REAL:** probe D4. |
| What the user sees today | Summary for a true flag: HTTP 403, outcome BLOCK, `summary` null, reasons `failmode.stale_topology_true` and `rule.stale_topology_blocks_recommendation`. Summary for a blank flag: HTTP 202, HOLD_FOR_REVIEW, reason `failmode.stale_topology_blank`. **Verified Fact:** probe P10. |
| What data could be wrong | The record read for `DEV-00003` returns HTTP 200 and the row, with `stale_topology_flag` `true` as one cell among eleven. Nothing in the response says the row is stale (probe P10). |
| Business effect | The AI path refuses stale rows. The read path does not warn about them. An operator who reads the row first can act on a stale topology. |
| Detection today | A count of true flags. The summary route writes `policy.deny` for BLOCK. |
| YAML id | `rule.stale_topology_blocks_recommendation`; `failmode.stale_topology_true`; `failmode.stale_topology_blank` |
| Drill | Stale master data (Half B drill 4). It is separate from the impossible-timestamp drill. |
| Confidence | High |
| Open questions | Whether the record read should show a stale warning. That is a change to a route body. It belongs to S07. |

## FM-08 — Daily batch hits a bad row

| | |
|---|---|
| Trigger | `devices.csv` holds a row with a blank cell, a short row, a long row, or a line that is not valid UTF-8. |
| What the user sees today | A blank cell is counted in `malformed`. A short row and a long row are not counted. A line that is not valid UTF-8 stops the run with exit code 1 and prints nothing, so the counts for every good row are lost. A missing file also exits with code 1 and prints nothing. **Verified Fact:** `run_daily_batch.py` lines 10 to 17; probe P11a, P11b, P11c. |
| What data could be wrong | In probe P11a three of six rows were bad (one blank cell, one short, one long). The batch printed `malformed` 1. Two bad rows passed as good. The reason: a short row gives `None` for the missing cells and a long row gives a list under a `None` key. Neither equals an empty string (`run_daily_batch.py` line 13). |
| Business effect | The batch tells the operator the data is cleaner than it is. One bad byte makes the whole run fail with no partial result. |
| Detection today | The exit code and the printed counts. Nothing writes a file of bad rows. **Verified Fact:** test `test_etl_counts_blank_fields_and_does_not_quarantine`. |
| YAML id | `metric.quarantine_rate`; `rule.one_row_per_key`. No rule id says a bad row is held aside and the batch goes on. Open question OQ-4. |
| Drill | Partial batch failure (Half B drill 5). |
| Confidence | High |
| Open questions | Where a held-aside row is recorded. The operating contract (row 1 and row 6) bars changes to the CSV files, so the record must go elsewhere. Unknown. |

## FM-09 — Alarm with last_seen_at before first_seen_at

| | |
|---|---|
| Trigger | An alarm row whose `last_seen_at` is earlier than `first_seen_at`. `ALA-00002` on file line 3 is the example: first 2026-07-31T23:45:00, last 2026-02-23T09:35:00. |
| What the user sees today | Nothing. No code reads `alarms.csv`. |
| What data could be wrong | **Verified Fact. REAL** (probe D1): 166 of 354 rows break the rule. One row (`ALA-BAD1`) has blank timestamps and cannot be compared. A duration made from these rows is negative. |
| Business effect | If alarms became incidents without this check, 166 rows would produce incidents with impossible times. Storm size and age figures would be wrong. |
| Detection today | None. |
| YAML id | `rule.alarm_last_seen_not_before_first_seen` (enforcement stage S04-11). The flag compares two timestamps. It needs no cutoff. |
| Drill | Impossible alarm timestamp (Half B drill 6). A blank timestamp cannot be compared. What to do with it is Unknown. This stage proposes: flag it for review. |
| Confidence | High |
| Open questions | Whether a blank timestamp counts as an impossible row. Unknown. |

## FM-10 — `devices.csv` is missing

| | |
|---|---|
| Trigger | The file is absent or cannot be opened at the first call. |
| What the user sees today | `GET /records/{id}` and `POST /ai/summarize/{id}` return HTTP 500 with the text `Internal Server Error`. No `X-Correlation-Id` header. No audit row is written. The model is not called. `/health` returns 200 `ok`. **Verified Fact:** `domain_service.py` line 24; probe P7. |
| What data could be wrong | None stored. A file that has only a header row behaves differently: the record read returns HTTP 200 with the body `{"error": "missing"}`, and the summary returns BLOCK with `failmode.missing_id` (probe P7b). |
| Business effect | Both business routes stop. The health check says the service is fine. A failed first load is not kept, so the next request tries again (test `test_a_missing_file_raises_and_is_not_cached`). |
| Detection today | A 500 in the web server log. No audit row exists for the failure. |
| YAML id | None. Open question OQ-5. |
| Drill | Not one of the five named drills. The degraded-mode design covers it. |
| Confidence | High |
| Open questions | OQ-5. |

## FM-11 — Policy engine fails

| | |
|---|---|
| Trigger | `POLICY_ENGINE` is `opa` (or `opa` is found on the PATH) and the `opa` run fails. |
| What the user sees today | HTTP 403 with body `{"error": "forbidden"}` on both business routes, for every role. `/health` returns 200. The audit row is `policy.deny`. It does not hold the reason. **Verified Fact:** `policy.py` lines 93 to 96, 147 to 148, and 259 to 264; probe P6 (`opa` was not on the PATH, so the probe forced `POLICY_ENGINE=opa`). |
| What data could be wrong | None. The engine never allows a call because it failed. |
| Business effect | Every operator is refused. A refusal caused by an outage and a refusal caused by a wrong role look the same on the wire and in the log. |
| Detection today | A sudden run of `policy.deny` rows for roles that worked an hour ago. No alert reads it. |
| YAML id | `rule.denied_access_is_audited` covers the audit row. The reason `policy_engine_error` is a code string with no YAML id. Open question OQ-5. |
| Drill | Not one of the five named drills. The degraded-mode design covers it. |
| Confidence | High for the Python path and the forced-`opa` path with `opa` absent. The path with a real `opa` that returns an error is Unknown, because `opa` is not installed here. |
| Open questions | OQ-5. |

## FM-12 — Audit log cannot be written

| | |
|---|---|
| Trigger | The `logs` folder is read-only, the disk is full, or the path is blocked. |
| What the user sees today | HTTP 500 on `GET /records/{id}` and on `POST /ai/summarize/{id}`. The body holds no device data and no summary. `/health` returns 200. **Verified Fact:** `audit.py` lines 75 and 92; `main.py` lines 69 and 90; probe P8. |
| What data could be wrong | None is returned. On a summary the model ran once before the write failed (probe P8, `model_calls_before_the_failure` is 1). |
| Business effect | No audit row means no answer. That keeps the rule that evidence exists before any state change. It also spends a model call for nothing. |
| Detection today | A 500 in the web server log. |
| YAML id | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `rule.audit_row_names_actor_and_correlation` |
| Drill | Not one of the five named drills. The degraded-mode design covers it. |
| Confidence | High |
| Open questions | None. |

## FM-13 — Several threads write the audit log at once

| | |
|---|---|
| Trigger | Two or more requests append to `logs/audit.log` at the same moment. |
| What the user sees today | Nothing. |
| What data could be wrong | Rows are lost and a few lines are cut. Three rounds of 8 threads writing 250 rows each: 2000 expected. The file held 1893, 1931, and 1919 lines. 2, 2, and 4 lines did not parse. Distinct rows recovered: 1891, 1929, 1915. Rows lost: 109, 71, and 85. **Verified Fact. REAL:** probe P9, on Windows. |
| Business effect | The audit trail is the proof of who did what. Between 3.6 and 5.5 percent of rows vanished under 8-way writing. `data-access-findings.md` DA-05 listed this as Unknown. It is now measured on this machine. |
| Detection today | None. A missing row leaves no mark. |
| YAML id | `metric.audit_completeness`; `rule.audit_row_names_actor_and_correlation` |
| Drill | Not one of the five named drills. This stage recommends a Half B drill and a small fix (decision D-3). |
| Confidence | High that the loss happens on this machine. Unknown on Linux. The Linux behaviour for small appends can differ. |
| Open questions | Does the loss happen on the target server? Unknown. |

## FM-14 — The model hangs

| | |
|---|---|
| Trigger | The model call takes longer than the deadline, for many callers at once. |
| What the user sees today | Each summary returns HTTP 202 after the deadline. While 50 summaries waited, `/health` took about 825 ms three times and `/records/{id}` took about 830 ms three times. Idle, both took about 10 ms. All six calls returned HTTP 200. **Verified Fact. REAL:** probe P5 (route thread limit 40, model wait 3 s, deadline 1.5 s). |
| What data could be wrong | None. |
| Business effect | A route `def` holds one of 40 threads for the whole wait (`main.py` line 73). With a 10 s deadline, 4 summaries a second fill all 40 threads (`load-scenarios.md`, scenario 1b). `/health` and `/records` then wait for a free thread. The statement "these routes keep working while AI is down" holds only while the model fails fast or arrivals stay below that rate. |
| Second effect | Each call creates a one-worker pool and does not wait for it (`ai_gateway.py` lines 295 and 310). The worker thread keeps running after the call returns. The probe counted 3 threads before, 138 during, 76 right after the last answer, and 1 three seconds later. **Verified Fact. REAL:** probe P5. A model that never returns would keep each thread for good. That last step is an **Inference**. |
| Detection today | None. |
| YAML id | None. No rule or failure id covers thread use. |
| Drill | Part of Half B drill 2 and the breaker test. |
| Confidence | High for the measured delay. Medium for production, where model wait and traffic are Unknown. |
| Open questions | The production model wait. Unknown. |

## FM-15 — Device id not found

| | |
|---|---|
| Trigger | `GET /records/{id}` with an id that matches no `device_id`. |
| What the user sees today | HTTP 200 and the first row, `REC-0001`. **Verified Fact:** `domain_service.py` lines 46 and 47; test `test_missing_id_still_returns_the_first_row`. The summary route does not do this: it returns BLOCK with `failmode.missing_id` (test `test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row`). |
| What data could be wrong | The caller receives a different device than the one asked for. |
| Business effect | A person can read the topology of the wrong device and act on it. |
| Detection today | The audit row for the read stores the action and not the id found. |
| YAML id | `rule.missing_id_not_other_device` (`enforcement_stage` S04-11 in the YAML). |
| Drill | Not one of the five named drills. `evidence.md` of S04-10 says defect F01 stays open for S07. This is decision D-6. |
| Confidence | High |
| Open questions | D-6. |

## Open questions for S03

Open question for S03 (OQ-1): the YAML has no failure id for "the model was not reachable or the breaker is open". This design needs it so a model outage is not reported as `failmode.schema_failure`.

Open question for S03 (OQ-2): `entities.yaml` `entity.event` has nine fields and none is an event sequence number. The playbook names "event sequence" as part of the replay key. This design needs a field id for the position of an event inside its chain.

Open question for S03 (OQ-3): the YAML has no rule id for "an event seen twice is one event" and none for "an order attempt with the same `order_id` and `retry_count` is one attempt". This design needs both.

Open question for S03 (OQ-4): the YAML has no rule id for "a bad row is held aside and the batch goes on". `metric.quarantine_rate` counts such rows, but no rule says what must happen.

Open question for S03 (OQ-5): the YAML has no failure id for "a data file is missing", "the policy engine failed" (the code string is `policy_engine_error`), or "the audit log cannot be written".

Open question for S03 (OQ-6): the YAML has no status words for a dependency state (closed, open, half open) and no metric id for how often the model path was held open.

Open question for S03 (OQ-7): the YAML has no names for incident severity levels. Alarm severity words (`gold`, `bronze`, and others) and event severity words (`debug` to `critical`) are different scales. The runbook uses four PROPOSED level names (see `incident-response.md`).

## Decisions before Half B

Each decision has a recommended answer. If you reply "Half A accepted" with no change, Half B uses the recommended answer.

| Id | Decision | Recommended answer | Why |
|---|---|---|---|
| D-1 | A true `stale_topology_flag`: HOLD_FOR_REVIEW (playbook) or BLOCK (YAML and code)? | BLOCK. A blank flag stays HOLD_FOR_REVIEW. | The YAML is the source of truth. `UO-02` already chose this. |
| D-2 | May the locked fact about AI-down behaviour be read as the baseline, with the current code described next to it? | Yes. | The code has had a timeout and a hold path since S04-09. |
| D-3 | May Half B add a lock around the audit write in `audit.py`? | Yes. It is a few lines. The drill then shows 0 rows lost. | `audit.py` is not on the playbook's Half B list. The loss is measured (RF-01). A lock in one process does not protect two processes. |
| D-4 | May `breaker.py` also limit how many model calls run at once? | Yes. The PROPOSED limit is 10 (see `retry-and-circuit-breaker-strategy.md`). | The breaker alone does not protect `/health` and `/records` in the first seconds of a hang (RF-02). |
| D-5 | Where does the impossible-timestamp check live? | A function in `apps/api/services/dedupe.py`, named for alarm intake checks. | The playbook names no file for it. One file keeps the alarm checks together. |
| D-6 | Does Half B also change the missing-id fallback so a record read returns 404? | No. Leave it for S07, as S04-10 decided. | The playbook scope for Half B does not list it. The inherited test would fail and must be replaced. The YAML names S04-11 as the enforcement stage, so this needs your word. |
| D-7 | What counts as a bad ETL row, and where is it recorded? | A blank cell (as today), a short row, a long row, and a line that is not valid UTF-8. Half B adds a `quarantined` count to the printed result. `processed` and `malformed` keep their meaning. No file is written. | The operating contract bars writes under `data/synthetic/`. A count needs no new file. |

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| RF-01 | The audit log loses rows when threads write at once. | **Verified Fact. REAL.** Probe P9: 109, 71, and 85 of 2000 rows lost. `audit.py` lines 92 and 93. | The proof of who did what is incomplete. | High | High on this machine | Linux behaviour. Unknown. |
| RF-02 | A hanging model slows `/health` and `/records` for everyone. | **Verified Fact. REAL.** Probe P5: about 825 ms against about 10 ms idle. | The AI-down promise "other routes continue" is true but slow. It can become a full stop at higher rates. | High | High for the delay. Medium for production. | Model wait and request rate. Unknown. |
| RF-03 | A timeout reports two reasons, and a model error reports the wrong one. | **Verified Fact.** Probe P2 and P3. `policy.py` line 233. `ai_gateway.py` line 303. | A person reads the wrong cause. | Medium | High | OQ-1. |
| RF-04 | The 500 error response carries no correlation id and writes no audit row. | **Verified Fact.** Probe P7 and P8. `main.py` lines 17 and 18. | A failed call cannot be traced. | Medium | High | None. |
| RF-05 | The batch hides short and long bad rows and loses all counts on one bad byte. | **Verified Fact.** Probe P11a and P11b. | The batch under-reports bad data. | High | High | OQ-4. |
| RF-06 | A policy outage and an access refusal look the same. | **Verified Fact.** Probe P6. | An operator cannot tell an outage from a wrong role. | Medium | High | OQ-5. |
| RF-07 | The health route says ok when both business routes fail. | **Verified Fact.** Probe P6, P7, P8: `/health` is 200 in each. | A monitor that calls `/health` sees no outage. | High | High | A readiness check is a new route. It belongs to S07. |
| RF-08 | A held case has no person to receive it. | **Verified Fact.** `main.py` has three routes. None lists or delivers holds. | Fail-to-person ends at an HTTP 202 body and an audit row. | High | High | The inbox is Unknown. It belongs to S07. |
| RF-09 | The playbook and the YAML disagree on a true stale flag. | **Verified Fact.** `ai-context-policy.yaml` line 290 to 294; probe P10. | The Half B drill must pick one. | Low | High | Decision D-1. |

## Lifecycle

`idempotency-plan.md` answers FM-05 and FM-06. `retry-and-circuit-breaker-strategy.md` answers FM-03, FM-04, and FM-14. `degraded-mode-design.md` answers FM-10, FM-11, and FM-12. `docs/runbooks/incident-response.md` tells a person what to do for each mode. Half B turns the five named drills and the impossible-timestamp case into tests.
