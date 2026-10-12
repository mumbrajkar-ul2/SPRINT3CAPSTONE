# Scaling recommendations

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Five changes are PROPOSED. Owner of each: Team-Force (operating contract row 10). No code changed in Half A. The savings are Inferences from measured costs. Half B measures them. |
| Evidence sources | `bottleneck-list.md`; `performance-baseline.md`; `load-scenarios.md`; `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `apps/api/services/ai_gateway.py`; `data/synthetic/alarms.csv`; `docs/02-baseline/defect-list.md` (F01, F06, F17); `docs/08-observability/slo-proposal.md`; `docs/01-discovery/data-and-integration-map.md` |
| Assumptions | Team-Force owns every PROPOSED item. A saving is the measured cost of the step that goes away. It does not include new costs the change brings. |
| Unresolved issues | Two decisions for Half B are open (see "Decisions before Half B"). Two terms are missing from the YAML (see "Open questions for S03"). |
| Residual risks | Load once makes the app read the file only at the first call. A change to `devices.csv` after that is not seen until the app restarts. The repo has no writer for that file (`data-and-integration-map.md`), so today nothing changes it while the app runs. |

## What this file is

This file proposes changes that answer the rows in `bottleneck-list.md`. Each change says what business effect it protects, what it saves, who owns it, and whether Half B makes it.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Measured numbers are **REAL**.

Half B is limited to one change: SR-01. The playbook excludes async rewrites, caching layers, and new routes from Half B, so SR-03, SR-04, and SR-05 are proposals only. SR-02 is outside the Half B scope as written. It changes `policy.py`. Half B makes it only if Team-Force accepts it.

## The proposals

| ID | Change | Business effect it protects | Expected saving (Inference) | Owner | Made in Half B? |
|---|---|---|---|---|---|
| SR-01 | Load `devices.csv` once and index its rows by `device_id`. Keep the function name and arguments. | A device lookup during an alarm storm no longer waits for a file read. Triage reaches the device row sooner. | About 1.7 ms per lookup. That is 12% of `GET /records/{id}` (14.280 ms) and 4% of `POST /ai/summarize/{id}` (44.788 ms). It also removes the 404.1 KiB allocation made on each call. | Team-Force | Yes |
| SR-02 | Decide once per process whether `opa` is installed, instead of searching the PATH on every access decision. | Every device lookup and every summary stops paying a PATH search before it starts. Triage starts sooner. | About 5.6 ms per access decision. That is 40% of `GET /records/{id}` and 38% of `POST /ai/summarize/{id}` (three decisions, 16.9 ms). | Team-Force | Only if Team-Force accepts it |
| SR-03 | In a batch of alarms, keep one alarm for each `dedupe_key` and count the repeats. | One incident for a repeated alarm, and one summary instead of many. A storm does not turn into a pile of identical work. | In `alarms.csv`: 3 rows of 354 (0.8%). The saving in production is Unknown. | Team-Force | No. No route reads alarms today. Stage S07 builds one. |
| SR-04 | Run the model call in the background and let the caller fetch the result. A queue holds the waiting calls. | While summaries wait on a model, device lookups still get a thread. Triage keeps working during a storm. | Frees one of the 40 route threads for the whole model wait. At a 10 s wait, 40 threads finish 4 summaries a second today (`load-scenarios.md` 1b). | Team-Force | No. The playbook excludes async rewrites and new routes. |
| SR-05 | Raise capacity with more server processes, not more threads. | More device lookups per minute when the load rises. | None per call. Eight threads gave no gain on the read (PB-03). | Team-Force | No. This is a deployment choice. |

## Detail for each proposal

### SR-01 — Load once and index by id

| | |
|---|---|
| Finding | The file is read and parsed on each call (`domain_service.py` lines 8 to 10). The call then uses one row of 354. |
| Evidence | **Verified Fact. REAL.** 2.170 ms per call, of which 1.726 ms is the read (run 3). One row of 354 is used, which is 0.3%. |
| Impact | Per lookup, the 1.7 ms goes away. At 27,656 lookups a minute (cost A) the file read stops being the limit for one process. |
| Risk | Medium. Four behaviours must stay the same or be changed on purpose. (1) `load_record` matches the id against every cell of the row (`domain_service.py` line 12, defect F17). An index on `device_id` only matches that one column, so an id such as `SIT-00002` stops finding row 2. The calls to `load_record` and the route calls in `tests/` and `policy/tests/` that this stage searched send only `device_id` values (`REC-0001`, `DEV-00003`, `DEV-BAD1`) or the missing id `DOES-NOT-EXIST`. **Verified Fact.** Half B re-runs the whole suite to confirm. (2) Three ids appear twice (`DEV-00004`, `DEV-00013`, `DEV-00019`, defect F06). Today the first row wins. The index must keep the first row. (3) A missing id returns the first row (line 15, defect F01). Half B keeps that, as the playbook says, unless S04-03 or S07 changed it. They have not. (4) The index must hand back a copy of the row. A caller that edited a shared row would change every later answer. |
| Confidence | High that the read is most of `load_record`. Medium for the 12 percent route saving, which is a subtraction from noisy runs. |
| Open questions | Does a restart-only reload satisfy the owner? See "Decisions before Half B". |

### SR-02 — Choose the policy engine once

| | |
|---|---|
| Finding | `engine_name()` searches the PATH for `opa` each time it runs (`policy.py` line 54). The answer is the same for the life of the app. |
| Evidence | **Verified Fact. REAL.** 5.867 ms per search and 5.644 ms per access decision (run 3). 8.153 ms and 8.976 ms (run 2). The tests in `policy/tests/test_policy_python.py` lines 382 to 388 check that `engine_name()` follows `POLICY_ENGINE`, so the change has to keep the setting read on each call and cache only the PATH search. |
| Impact | The biggest fixed cost inside both routes on this machine. |
| Risk | Low. The environment variable still decides. Only the PATH search is saved. A program installed after the app starts is not noticed until restart. |
| Confidence | High on this machine. Unknown on a Linux server with a short PATH. |
| Open questions | Whether Team-Force wants this inside Half B. It is outside the playbook's Half B list. |

### SR-03 — Dedupe alarms in a batch by `dedupe_key`

| | |
|---|---|
| Finding | Alarms that share a `dedupe_key` are the same alarm repeated (`entities.yaml`, `field.alarm.dedupe_key`). No code collapses them. |
| Evidence | **Verified Fact. REAL.** 354 rows. 350 non-blank keys. Three keys appear twice. One key is blank. Grouping takes 1.705 ms. |
| Impact | At this size, 3 rows. The value is in a real storm where one fault raises the same alarm many times. Each avoided row is one less lookup and one less summary. |
| Risk | Medium. Keeping one row and counting the rest must not hide a real second alarm. 166 rows have `last_seen_at` earlier than `first_seen_at` (defect F08), so a time window rule is unsafe until the dates are repaired. The blank key cannot be grouped. |
| Confidence | Medium. The grouping is measured. The production repeat rate is Unknown. |
| Open questions | How wide a window counts as "the same alarm". Unknown. Owner: Team-Force. |

### SR-04 — Make the model call asynchronous with a queue

| | |
|---|---|
| Finding | The summary route is a `def` route, so it holds one of 40 threads until the model answers (`main.py` line 73; `ai_gateway.py` line 295). |
| Evidence | **Verified Fact. REAL.** The thread limit is 40. The stub wait is 10.680 ms. **Inference:** a real model with a 2 s wait lets 40 threads finish 20 summaries a second; at 10 s, 4 a second. |
| Impact | Lookups for the same incident wait when 40 summaries are in flight. |
| Risk | High if built carelessly. A queue adds job states and a way to fetch the answer. Both policy checks from S04-09 must still run before and after the model. The correlation id, the audit row, and the timeout outcome HOLD_FOR_REVIEW must survive the hand-off. No approval or execute path may open. |
| Confidence | Medium. The thread limit is measured. The effect needs a real model to show. |
| Open questions | See "Open questions for S03". |

### SR-05 — More processes, not more threads

| | |
|---|---|
| Finding | Eight threads were no faster than one on the record read (3.058 ms against 2.170 ms per call in run 3). |
| Evidence | **Verified Fact. REAL.** Three runs, none showed a gain. See PB-03. |
| Impact | A deployment that raises the thread count to meet load will not raise lookups per minute. |
| Risk | Low. It needs a decision on how the app is started. |
| Confidence | Medium. |
| Open questions | How production starts the app. Unknown. |

## PROPOSED targets

| Target | Number | Owner | Basis |
|---|---|---|---|
| `load_record` time per call after SR-01, median of 5 rounds on this machine | At most 0.1 ms | Team-Force | The read and parse (1.726 ms) is gone. What is left is a dictionary lookup and one row copy. Half B checks the number. It is an engineering check, not a service level. |
| Summary latency, 95 of 100 calls | 2000 ms | Team-Force | Already PROPOSED in `docs/08-observability/slo-proposal.md`. This stage adds no new number for it. |

No target is proposed for the record route as a whole. The test client adds about 3.9 ms the live server does not, and the repo has no production figure to base one on.

## Decisions before Half B

**Decided 2026-10-11 by Mangesh (FDE): the recommended choice for all three items below.** Id matching: `device_id` only. Reload: restart-only, with a reset function for tests. SR-02: included in Half B as a second, separate step. Half B has not started. It starts when Mangesh replies "Half A accepted".

1. **Id matching.** Today any cell can match the id (F17). The playbook says to index by `device_id`. Recommended: index by `device_id` only, keep the first row for a repeated id, keep the missing-id behaviour, and record in `evidence.md` that matching on other columns stopped. The other choice is to index every cell value to keep today's behaviour exactly.
2. **Reload.** Recommended: read the file at the first call and again only on restart, with a function the tests can call to reset it. The repo has no writer for `devices.csv`, so nothing changes it while the app runs.
3. **SR-02.** Include it in Half B or leave it as a proposal. Recommended: include it as a separate, small change, because it saves more per request than SR-01. It touches `policy.py`, which is outside the playbook's Half B list.

## Open questions for S03

Open question for S03: the YAML has no metric id for record read latency. This design proposes a target for it (the 0.1 ms check above) and needs an id to hold it, the way `metric.recommendation_latency` holds the model call.

Open question for S03: the YAML has no resource id for a model-call queue and no status words for a queued call (queued, running, done). SR-04 needs them to name the queue in access, audit, and policy rows.

## Lifecycle

Half B makes SR-01, and SR-02 if accepted, and records before and after in `evidence.md`. Stage S07 builds `/alarms/storms` on the indexed loader, and SR-03 applies there. Stage S09 cites the before and after.
