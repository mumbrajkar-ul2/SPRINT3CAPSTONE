# Load scenarios

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. All three scenarios are worked out in calls per minute. None rests on a production figure, because the repo has none. Each is marked Unknown where it needs one. |
| Evidence sources | `docs/10-performance/measure-before.json` (`data_facts`, `scenarios`); `performance-baseline.md`; `data/synthetic/alarms.csv`, `service_orders.csv`, `events.jsonl`; `semantic-layer/entities.yaml`; `docs/01-discovery/business-flow-reconstruction.md`; `docs/08-observability/slo-proposal.md` |
| Assumptions | Every scenario assumes one device lookup (or one summary) for each alarm, event, or retry. No route does that today. The Assumption is there so the arithmetic has a shape. Per-call times are the run 3 medians from this machine. |
| Unresolved issues | Production alarm rate, storm size, number of callers, replay frequency, retry timing, model latency, and the number of server processes are all Unknown. |
| Residual risks | A reader can treat the multipliers (N = 10, 100, 1000) as forecasts. They are chosen to show where the current code stops coping. They are **EDUCATIONAL**, not predictions. |

## What this file is

This file turns the measured per-call costs into calls per minute for three situations the data names: an alarm storm, a replay of the event log, and order retries.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A measured number is **REAL**. An extrapolation is **EDUCATIONAL**.

## Three costs the scenarios use

| Name | What it is | Per call, ms (REAL) | Calls per minute, one after another |
|---|---|---|---|
| A | `load_record` alone | 2.170 | 27,656 |
| B | Route `GET /records/{id}` (includes about 3.9 ms of test client time, so this is an upper bound on server cost) | 14.280 | 4,202 |
| C | Route `POST /ai/summarize/{id}` with the 10 ms stub | 44.788 | 1,340 |

Worked example: 60,000 ms in a minute divided by 14.280 ms is 4,202 calls. That is the most one caller, working alone, can finish in a minute at cost B.

Threads do not raise these figures for the read, because the 8-thread test took 3.058 ms per call against 2.170 ms for one thread (`performance-baseline.md`). Waits on a model do free the thread. So the summary path can run many calls at once, up to the 40 route threads.

## Scenario 1 — Alarm storm

**What the data says.** `alarms.csv` has 354 rows. **Verified Fact. REAL.** 350 non-blank `storm_batch_id` values appear. 347 appear once. Three appear twice: `STO-00005`, `STO-00013`, `STO-00019`. One row is blank. The largest storm is 2 alarms.

**Assumption.** Each alarm in a storm needs one device lookup, so a storm of S alarms needs S lookups. A larger storm is the largest storm times N.

**1a. Device lookups during a storm** (EDUCATIONAL)

| N | Alarms in the storm (2 × N) | Lookups needed in one minute | Time at cost A, one after another | Time at cost B, one after another | Fits in one minute at B? |
|---|---|---|---|---|---|
| 1 (the data as it is) | 2 | 2 per minute | 0.004 s | 0.029 s | Yes |
| 10 | 20 | 20 per minute | 0.043 s | 0.286 s | Yes |
| 100 | 200 | 200 per minute | 0.43 s | 2.86 s | Yes |
| 1000 | 2000 | 2000 per minute | 4.3 s | 28.6 s | Yes |
| 2100 | 4200 | 4200 per minute | 9.1 s | 60.0 s | Barely |
| 2101 or more | 4202 or more | 4202 or more per minute | | more than 60 s | No |

Worked example for N = 1000: 2000 alarms × 14.280 ms is 28,560 ms, which is 28.6 seconds. That is under one minute, so the lookups fit.

**Reading.** At the real storm size (2 alarms) the read path is not strained. One caller would need a storm above 4,200 alarms in a minute to fill a minute at cost B. At cost A alone, N could reach 13,828 (27,656 ÷ 2) before the lookups fill a minute.

**1b. Summaries during a storm** (EDUCATIONAL)

**Assumption.** Each alarm asks for one summary. The model wait is the PROPOSED 2000 ms or the PROPOSED 10 second timeout, from `slo-proposal.md` and `ai_gateway.py` line 53. Both are PROPOSED, with owner Team-Force. The repo has no real model wait.

At 40 threads, the most summaries finished each second are 40 divided by the wait: 20 a second (1,200 a minute) at 2 seconds, and 4 a second (240 a minute) at 10 seconds.

| N | Alarms (2 × N) | Time to finish at a 2 s wait | Time to finish at a 10 s wait |
|---|---|---|---|
| 1 | 2 | 0.1 s | 0.5 s |
| 10 | 20 | 1 s | 5 s |
| 100 | 200 | 10 s | 50 s |
| 1000 | 2000 | 100 s | 500 s (8.3 minutes) |

Worked example for N = 1000 at 10 seconds: 2000 summaries ÷ 4 a second is 500 seconds. During those 500 seconds all 40 route threads are in use. A device lookup that arrives needs a thread and waits.

Largest N that fits in one minute: 600 at a 2 s wait (1,200 ÷ 2), 120 at a 10 s wait (240 ÷ 2), and 670 for the current stub taken one call after another (1,340 ÷ 2).

**Unknown.** How many alarms arrive per minute in production, how many make a storm, how many people triage at once, and what the model's wait is.

## Scenario 2 — Replay of the event log

**What the data says.** `events.jsonl` has 3000 lines. **Verified Fact. REAL.** Flow counts: Topology lookup to AI recommendation 782, Approved remediation to validation 771, Customer order to provisioning 741, Alarm storm to incident correlation 706.

An event line has nine fields: `event_id`, `business_entity`, `event_type`, `severity`, `correlation_id`, `actor`, `latency_ms`, `cost_units`, `payload_hash` (`entities.yaml`, `entity.event`). **Verified Fact.** None of them is a device id. A replay therefore has no key to look up a device row with.

| Question | Answer (EDUCATIONAL unless marked) |
|---|---|
| Handler calls if the replay must finish in one minute | 3000 per minute |
| Cost of reading and parsing the whole file (REAL) | 13.032 ms |
| Cost of the handler calls | A no-op handler adds almost nothing. A real handler's cost is Unknown. |
| Cost if each event also read a device row at cost A | 3000 × 2.170 ms = 6.5 s |
| Cost if each event also read a device row at cost B | 3000 × 14.280 ms = 42.8 s, which is 71% of a minute |

**Reading.** The replay itself is cheap. It costs real time only if each event triggers another read. This data gives no key to do that, so the second case is an **Assumption** about a design that does not exist.

**Unknown.** How often anyone replays the log, how large production's log is, and what a real handler does.

## Scenario 3 — Order retries

**What the data says.** `service_orders.csv` has 354 rows. 353 `retry_count` values are numbers and one is blank (`SER-BAD1`). **Verified Fact. REAL.** The values run from 32 to 4995. 294 rows are at or above 1000. The sum of the 353 values is 943,094. No code reads this file (`business-flow-reconstruction.md`, Flow 1).

**Assumption.** Each retry needs one device lookup. The repo does not say it does.

| Retries spread over | Lookups per minute | Share of one process at cost A | Share of one process at cost B |
|---|---|---|---|
| 24 hours | 655 | 2.4% | 15.6% |
| 1 hour | 15,718 | 56.8% | 374% (3.7 times what one process can do) |

Worked example for 24 hours: 943,094 retries ÷ 1,440 minutes is 655 a minute. 655 × 14.280 ms is 9.35 seconds of work in each 60-second minute, which is 15.6 percent.

If the retry count were capped at the PROPOSED bound of 1000 (`defect-list.md` F18, owner Team-Force), the sum would be 324,735:

| Retries spread over | Lookups per minute | Share of one process at cost A | Share of one process at cost B |
|---|---|---|---|
| 24 hours | 226 | 0.8% | 5.4% |
| 1 hour | 5,412 | 19.6% | 129% |

**Reading.** This is the one scenario where the read cost matters for a short window. 943,094 retries in one hour would need 15,718 lookups a minute. One process at cost B finishes 4,202. The scenario assumes retries exist at that rate. The 294 values at or above 1000 may be data defects (F18), in which case the real sum is lower.

**Unknown.** How the retries are spread in time, whether a retry needs a device lookup, whether the large values are real, and how many server processes run.

## What stays Unknown

| Unknown | Why it matters | Who can supply it |
|---|---|---|
| Alarms per minute in production | Sets N in scenario 1 | Team-Force (owner of every PROPOSED number), from the operations team |
| Number of alarms that make a storm | `concept.storm` says the repo does not say | Team-Force |
| Simultaneous callers | Sets how many threads are busy | Team-Force |
| Model wait | Sets the summary rate in scenario 1b | Team-Force, after a real model is chosen |
| Retry timing and its link to a lookup | Sets scenario 3 | Team-Force |
| Replay frequency and log size | Sets scenario 2 | Team-Force |
| Server processes and hardware | Sets how far one process's figures scale | Team-Force |

## After Half B (added 2026-10-11)

Everything above uses the costs measured before Half B. Half B made two changes (`evidence.md`). The costs are now:

| Name | Before, ms | After, ms (REAL) | Calls per minute, one after another, after |
|---|---|---|---|
| A, `load_record` alone | 2.170 | 0.0003 | The read no longer limits the rate. |
| B, route `GET /records/{id}` | 14.280 | 5.805 | 10,336 |
| C, route `POST /ai/summarize/{id}` with the 10 ms stub | 44.788 | 29.038 | 2,066 |

What changes in the scenarios (EDUCATIONAL arithmetic from these costs):

| Scenario | Before | After |
|---|---|---|
| 1a, largest N that fits in one minute at cost B | 2,101 | 5,168 (10,336 ÷ 2) |
| 1b, largest N for the stub taken one call after another (cost C) | 670 | 1,033 (2,066 ÷ 2) |
| 1b, thread-bound figures at a 2 s or 10 s model wait | 1,200 and 240 a minute | Unchanged. Half B did not change the model wait or the 40 threads. |
| 3, retries over 24 hours, share of one process at cost B | 15.6% | 6.3% |
| 3, retries over 1 hour (15,718 lookups a minute) against cost B | 3.7 times what one process can do | 1.5 times (15,718 ÷ 10,336) |
| 3, capped at 1000, over 1 hour (5,412 a minute) against cost B | 129% | 52% |

Worked example for the 1-hour retry case: 15,718 ÷ 10,336 is 1.52. One process still cannot finish those lookups in an hour of retries. It now falls short by about a third (it finishes 10,336 of 15,718). The Assumption is unchanged: each retry needs one lookup, and the repo does not say it does.

The Unknown items in the table above are unchanged.

## Lifecycle

`scaling-recommendations.md` names the changes these scenarios call for. Stage S04-11 reuses scenario 1 as a drill. Stage S07 builds `/alarms/storms` on the indexed loader. Stage S09 cites the before and after.
