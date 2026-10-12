# Idempotency plan

| Field | Value |
|---|---|
| Stage | S04-11 — Reliability and failure engineering (Challenge 11), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Three keys are defined (alarm, order, event). The count of what a retry would duplicate today is measured. The proof method for Half B is written out. The event key cannot use a sequence number, because the data has none. |
| Evidence sources | `docs/11-reliability/probe_half_a.py` and `probe-output.json` (checks D1, D2, D3, P4); `semantic-layer/business-rules.yaml` (`rule.duplicate_dedupe_key_in_storm_is_one_alarm`, `rule.one_row_per_key`); `semantic-layer/entities.yaml` (`entity.alarm`, `entity.service_order`, `entity.event`); `semantic-layer/metrics.yaml` (`metric.retry_count`, `metric.alarm_storm_size`); `docs/10-performance/load-scenarios.md` scenarios 1 and 3; `docs/02-baseline/defect-list.md` F06, F18; `data/synthetic/alarms.csv`, `service_orders.csv`, `events.jsonl` |
| Assumptions | A retry means the same input arrives again. An alarm is one alarm shown more than once when the `dedupe_key` and the `storm_batch_id` are both equal. Team-Force owns every PROPOSED item. |
| Unresolved issues | There is no event sequence field (open question OQ-2 in `failure-mode-catalogue.md`). There is no rule id for a repeated event or a repeated order attempt (OQ-3). Whether `ORD-00004` with two different `retry_count` values is one order or two attempts is Unknown. |
| Residual risks | The helper planned for Half B keeps its memory inside one process. A restart empties it. A second server process has its own copy. A durable store is Unknown and belongs to a later stage. |

## What this file is

This file says how each repeated input becomes one result. It also states what a retry would duplicate today, and how Half B proves the count. That answers defence question 4: "What would a retry duplicate, and how did you prove the count?"

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A measured number is **REAL**. A Verified Fact names a file with a line, a test name, or a probe check id.

No code changes in Half A.

## What a retry duplicates today

| Path | What one repeat duplicates today | Proof |
|---|---|---|
| `POST /ai/summarize/{id}` | One model call and one audit row. | **Verified Fact. REAL.** Probe P4: 5 identical calls with the same `X-Correlation-Id` gave 5 answers, 5 model calls, and 5 audit rows. |
| Alarm intake | Nothing. No code reads or writes alarms. | **Verified Fact.** Probe P4: 0 files in `apps/` mention `alarms.csv`, `service_orders.csv`, `incidents.csv`, or `events.jsonl`. |
| Order retry | Nothing. No code retries an order. | Same check. `docs/01-discovery/business-flow-reconstruction.md` Flow 1. |
| Event replay | Nothing. No code reads the event file except `scripts/sanity_check.py`, which counts lines. | Same check. `data-access-findings.md` DA-03. |

The summary route changes no stored business row. A repeat costs money and adds audit rows. It does not create a second alarm, order, or incident.

## What a repeat would duplicate once readers exist

These counts are **REAL** counts of the files. The reading of them as duplicates is an **Assumption**, because no reader exists.

| Input | Rows or lines | Repeats in the file | What a second pass would add without a key |
|---|---|---|---|
| Alarms | 354 rows | 3 pairs share `dedupe_key` and `storm_batch_id` (`DED-00005`, `DED-00013`, `DED-00019`). 1 row (`ALA-BAD1`) has a blank key. | 3 extra alarms in a first pass. A full second pass adds 354 more. |
| Orders | 354 rows, 353 with a number in `retry_count` | 2 pairs share `order_id` and `retry_count` (`ORD-00013` with 3061, `ORD-00019` with 3246). `ORD-00004` appears twice with 1810 and 1604. 1 row (`SER-BAD1`) has a blank `retry_count`. | 2 extra attempts in a first pass. |
| Events | 3000 lines | 0 repeated `event_id`. 0 repeated `payload_hash`. 1992 lines have no `correlation_id`. | A second pass of the file adds 3000 events. |

Worked example for orders: 353 rows have a number. 2 of them repeat an earlier `order_id` and `retry_count`. That leaves 351 distinct attempts. One more row has a blank `retry_count` and is held aside. 351 + 2 + 1 = 354 rows.

The `retry_count` column sums to 943,094 across the 353 numeric rows (probe D2). If a retry were sent for each retry the file records, the repeat would be 943,094 attempts. That is **EDUCATIONAL**. `load-scenarios.md` scenario 3 uses the same figure.

## Key 1 — Alarm

| | |
|---|---|
| Key | The pair (`dedupe_key`, `storm_batch_id`). |
| Rule | Two rows with the same pair are one alarm shown twice. They count once. The rows stay on disk. **Verified Fact:** `rule.duplicate_dedupe_key_in_storm_is_one_alarm`. |
| What the helper does | The first row with a pair is new. Every later row with the same pair is a repeat. The helper counts the repeats for that pair. |
| Blank key | A row with a blank `dedupe_key` or a blank `storm_batch_id` cannot be grouped. The helper does not group it. It reports the row as "held aside". What a blank key should mean is Unknown. |
| Real data | 354 rows give 350 groups, 3 repeats, and 1 row held aside (`ALA-BAD1`). 350 + 3 + 1 = 354. |
| Limit | How many alarms make a storm is Unknown (`metric.alarm_storm_size`). This plan sets no number. |

Example from the file. `ALA-00004` appears on two lines. The second line has `dedupe_key` `DED-00005` and `storm_batch_id` `STO-00005`, the same pair as `ALA-00005`. Grouping by the pair keeps `ALA-00005` as the first row and counts the second `ALA-00004` line as its repeat. Grouping by `alarm_id` (`rule.one_row_per_key`) names the same line as the duplicate. Both rules drop the same row here.

## Key 2 — Order

| | |
|---|---|
| Key | The pair (`order_id`, `retry_count`). |
| Meaning | Attempt number N of order X is one attempt. Sending it twice counts once. The next real retry carries `retry_count` N + 1, so it is a new attempt. |
| Rule id | None. Open question OQ-3. |
| What the helper does | Same as Key 1 with a different pair. |
| Blank key | A blank `retry_count` is held aside. `SER-BAD1` is the one row. |
| Real data | 353 numeric rows give 351 distinct pairs and 2 repeats. `ORD-00004` has two different counts, so the helper treats it as two attempts. Whether that is right is Unknown. |
| Limit | `retry_count` is a number the caller sends. A caller that always sends 0 defeats the key. 294 rows are at or above 1000, which is the PROPOSED bound in defect F18. Owner: Team-Force. The key does not check the size of the number. |

## Key 3 — Event

| | |
|---|---|
| Key | `event_id`. |
| Why not (`correlation_id`, sequence) | The playbook names the chain id plus the event sequence. The event has nine fields and none is a sequence (probe D3, `has_a_sequence_field` false). 1992 of 3000 lines have no chain id. A key built on the chain id covers 1008 lines only. |
| What `event_id` gives | `event_id` is filled and distinct on all 3000 lines. A second pass of the file is caught for every line. |
| Order inside a chain | Where a chain id exists, the position in the file is the order. This is an **Assumption** taken from `trace-design.md`. A sequence field would make it exact. Open question OQ-2. |
| Real data | 3000 lines, 3000 new on the first pass, 3000 repeats on the second. |
| Limit | `payload_hash` cannot detect a copy of the content. It is distinct on all 3000 lines, so it does not repeat even where two events could carry the same content. |

## The summary route

The summary route has no key and gets none. The route reads the record and writes one audit row. It changes no stored business row. A repeat costs one model call and one audit row (probe P4).

The correlation id is a request chain id. It is not an idempotency key. Five calls with one id gave five audit rows.

A client that wants to avoid the repeat can wait for the first answer. The route returns HTTP 202 on a hold, so a client can tell a held case from a lost one.

## The helper in Half B

File: `apps/api/services/dedupe.py`. Scope in Half B:

| Item | Rule |
|---|---|
| Storage | A dictionary in memory. One lock around every read and write. |
| Calls | One call to check a key and record it. One call to read the repeat count. One call to clear it (tests use this). |
| Key shape | A tuple of strings. The caller builds the tuple. |
| Blank part | A tuple with a blank part is never recorded. The call returns "held aside". |
| Size limit | None in Half B. The production volume is Unknown. |
| Alarm intake checks | The impossible-timestamp check sits in the same file (decision D-5 in `failure-mode-catalogue.md`). |

## How Half B proves the count

| Test | Input | Expected |
|---|---|---|
| Same alarm twice | One alarm with a pair, sent two times. | One new, one repeat. The repeat count is 1. |
| All alarm rows | The 354 rows of `alarms.csv` in file order. | 350 new, 3 repeats, 1 held aside. |
| All order rows | The 354 rows of `service_orders.csv`. | 351 new, 2 repeats, 1 held aside. |
| Events twice | The 3000 lines of `events.jsonl`, two passes. | 3000 new, 3000 repeats. |
| Summary five times | The same request, five times. | 5 model calls, 5 audit rows. This shows the route has no key. |
| Blank key | An alarm with a blank `dedupe_key`. | Held aside, not counted as new, not counted as repeat. |

The tests read the data files. They do not write to them.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| ID-01 | A retry of the summary route duplicates one model call and one audit row. It duplicates no business row. | **Verified Fact. REAL.** Probe P4. | Cost and audit noise only. | Low | High | Cost per model call. Unknown until S04-12. |
| ID-02 | No code writes or reads alarms, orders, or events, so no business row can be duplicated yet. | **Verified Fact.** Probe P4, `alarm_incident_or_order_writers_in_apps` is 0. | The duplicate counts above describe the files, not live behaviour. | Medium. A reader added in S07 would duplicate on its first replay. | High | None. |
| ID-03 | The event file has no sequence field. | **Verified Fact. REAL.** Probe D3. | The playbook key cannot be built. `event_id` replaces it. | Medium | High | OQ-2. |
| ID-04 | `retry_count` is a caller-supplied number. | **Verified Fact.** `service_orders.csv` values run from 32 to 4995 (`defect-list.md` F18). | The order key does not stop a caller that sends a fresh number each time. | Medium | High for the data. Unknown for a real caller. | The legal maximum. Owner: Team-Force. |
| ID-05 | The helper forgets everything at restart. | **Inference.** It is an in-memory dictionary. | A replay after a restart is accepted again. | Medium | High | Durable store. Unknown. |
| ID-06 | One blank key row exists in each of two files (`ALA-BAD1`, `SER-BAD1`). | **Verified Fact. REAL.** Probe D1 and D2. | A blank key cannot be grouped. | Low | High | What a blank key should do. Unknown. |

## Lifecycle

`failure-mode-catalogue.md` FM-05 and FM-06 name the failures this plan answers. Half B writes `dedupe.py` and the tests above. Stage S07 uses `dedupe.py` in `GET /alarms/storms/{storm_batch_id}`. Stage S10 answers defence question 4 from the table "What a retry duplicates today" and the Half B test results.
