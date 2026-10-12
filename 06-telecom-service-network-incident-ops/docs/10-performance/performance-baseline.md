# Performance baseline

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every number below is measured on this machine. The repo has no production figure, so no number here says how the live system behaves under real load. |
| Evidence sources | `docs/10-performance/measure.py`; `docs/10-performance/measure-before.json` (run 3); `apps/api/services/domain_service.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/policy.py`; `apps/api/services/audit.py`; `apps/api/main.py`; `data/synthetic/devices.csv`, `alarms.csv`, `service_orders.csv`, `events.jsonl`; `semantic-layer/entities.yaml`; `docs/01-discovery/business-flow-reconstruction.md` |
| Assumptions | The three runs below used the same machine, the same code, and the data in the repo. FastAPI `TestClient` calls stand in for HTTP calls. The test client adds time that a real server would not add (see "What the numbers do not show"). |
| Unresolved issues | Production request rate, production file sizes, and real model latency are Unknown. The `opa` program is not installed here, so the cost of the OPA path is Unknown. Open question for S03: the YAML has no metric id for record read latency. This stage proposes a target for it (in `scaling-recommendations.md`) and needs an id to hold it. |
| Residual risks | A reader can quote a millisecond figure as if it were a service level. It is a measurement on one machine. The machine was busy during the runs, so single numbers move by up to 40 percent from run to run. |

## What this file is

This file reports how long the current code takes to do its work. `measure.py` runs each item many times and reports wall time and time per call.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Measured numbers are **REAL**. A **Verified Fact** that is a measurement names `measure.py`.

The script changes no repo file. Its route calls write audit rows to a temporary folder, not to `logs/audit.log`.

Added after Half B: this file is the baseline, measured on the code before Half B. The line numbers are the old ones. The after numbers and the new lines are in `evidence.md`.

## The machine and the runs

| Item | Value |
|---|---|
| Machine | Windows 11 (build 26200), Python 3.13.5, 8 CPUs |
| Policy engine used by the code | `python` (the `opa` program is not on this machine's PATH) |
| Run 1 | 2026-10-11 18:29, 3 rounds per item. The policy items were not yet in the script. |
| Run 2 | 2026-10-11 18:31, 3 rounds per item |
| Run 3 | 2026-10-11 18:34, 5 rounds per item. This is the run of record. Its full output is `measure-before.json`. |

Each item runs in rounds. The table shows the middle round. "Min" and "max" are the fastest and slowest round in run 3.

## Measured numbers (run 3, REAL)

| Item | Calls | Wall time, seconds | Per call, ms | Min, ms | Max, ms |
|---|---|---|---|---|---|
| `load_record` for an id that exists (`DEV-00002`) | 1000 | 2.170 | 2.170 | 1.555 | 2.681 |
| `load_record` for an id that is missing | 1000 | 2.858 | 2.858 | 2.593 | 3.079 |
| `load_record`, same 1000 calls shared by 8 threads | 1000 | 3.058 | 3.058 | 1.872 | 3.807 |
| Read `devices.csv` into rows, no search | 1000 | 1.726 | 1.726 | 1.458 | 1.863 |
| Group `alarms.csv` by `storm_batch_id` | 100 | 0.169 | 1.690 | 1.666 | 1.737 |
| Group `alarms.csv` by `dedupe_key` | 100 | 0.171 | 1.705 | 1.655 | 1.815 |
| Replay `events.jsonl` (3000 lines, handler does nothing) | 20 | 0.261 | 13.032 | 12.954 | 13.261 |
| `shutil.which("opa")` (one PATH search) | 200 | 1.173 | 5.867 | 5.741 | 7.878 |
| `policy.check_record_read` (one access decision, python engine) | 200 | 1.129 | 5.644 | 5.412 | 7.363 |
| `ai_gateway.call_model` (the stub) | 100 | 1.068 | 10.680 | 10.634 | 10.693 |
| `ai_gateway.summarize_record` (whole gateway call) | 100 | 2.934 | 29.343 | 28.730 | 33.604 |
| Route `GET /health` | 200 | 0.785 | 3.925 | 3.642 | 5.166 |
| Route `GET /records/{id}` | 200 | 2.856 | 14.280 | 13.807 | 14.453 |
| Route `POST /ai/summarize/{id}` | 100 | 4.479 | 44.788 | 44.133 | 45.338 |
| `audit.write_event` (one row) | 1000 | 0.526 | 0.526 | 0.513 | 0.546 |

Other measured values from run 3:

| Item | Value |
|---|---|
| Memory one `load_record` call allocates at its peak | 404.1 KiB |
| One `events.jsonl` replay, per line | 4.3 microseconds |
| Default number of threads AnyIO gives to routes written with `def` | 40 |
| Rows in each CSV | 354 |
| Bytes in `devices.csv`, `alarms.csv`, `service_orders.csv`, `events.jsonl` | 41,883; 41,006; 24,418; 792,328 |

How to read the 8-thread row: 1000 calls shared by 8 threads finish in 3.058 seconds. One thread finishes the same 1000 calls in 2.170 seconds. The threads gave no speed-up.

## Run to run

| Item | Run 1, ms | Run 2, ms | Run 3, ms |
|---|---|---|---|
| `load_record`, id exists | 1.718 | 1.616 | 2.170 |
| `load_record`, id missing | 2.331 | 1.742 | 2.858 |
| Read `devices.csv` alone | 1.504 | 2.632 | 1.726 |
| Replay of 3000 events | 12.664 | 16.476 | 13.032 |
| `shutil.which("opa")` | not measured | 8.153 | 5.867 |
| Route `GET /records/{id}` | 14.657 | 16.503 | 14.280 |
| Route `POST /ai/summarize/{id}` | 41.373 | 47.736 | 44.788 |

The same item moved by as much as 40 percent between runs (`load_record`, id exists: 1.616 to 2.170). In run 2 the read alone (2.632) was slower than the whole `load_record` call (1.616). That cannot be the real order of cost, so run 2 had interference. **Verified Fact:** another process wrote rows to `logs/audit.log` between 18:28:55 and 18:29:25 local time, which overlaps run 1. The script did not write them. **Inference:** other work was using the machine during the runs.

Half B must compare before and after with the same command and 5 rounds, and must read the ranges, not one number.

## Where the time goes on one route call

Each row in this table is a subtraction of numbers measured above. The remainder is labelled.

| Piece | `GET /records/{id}`, ms | Share |
|---|---|---|
| Test client and framework (the `GET /health` time) | 3.93 | 28% |
| Access decision (`policy.check_record_read`) | 5.64 | 40% |
| `load_record` | 2.17 | 15% |
| Audit row | 0.53 | 4% |
| Remainder (route code, JSON, middleware) | 2.01 | 14% |
| Total measured | 14.28 | 100% |

Worked example: 3.93 + 5.64 + 2.17 + 0.53 = 12.27. The route took 14.28. The remaining 2.01 ms is what is left over, so it is an **Inference** and not a separate measurement.

Of the 14.28 ms, the file read and parse inside `load_record` is 1.73 ms. That is 12 percent. The access decision costs 5.64 ms, which is 2.6 times as much as `load_record`.

On `POST /ai/summarize/{id}` the policy runs three times (`main.py` line 81, `ai_gateway.py` lines 419 and 425). Three times 5.64 ms is 16.9 ms of the 44.79 ms. That is 38 percent. The stub wait is 10.68 ms (24 percent). The `load_record` call is 2.17 ms (5 percent).

## What the numbers do not show

- **The test client adds time.** `GET /health` does no file work and takes 3.9 ms. A production server adds a different amount. Unknown.
- **The `shutil.which` cost depends on the machine.** It searches every folder on the PATH. This machine has 62 PATH folders. A Linux container with few folders is likely faster. **Assumption.** Not measured.
- **The OPA path is Unknown.** When `opa` is installed, `engine_name()` returns `opa`. Each policy call then starts an `opa` program as a new process (`policy.py` line 66) and searches the PATH a second time (line 59). That cost is not measured because the program is absent here.
- **The model is a stub.** `call_model` sleeps 0.01 seconds (`ai_gateway.py` line 172). A real model's time is Unknown.
- **One thread of load.** Each item ran one call after another. The numbers do not show how the app behaves when many callers arrive together.

## Findings

### PB-01

| | |
|---|---|
| Finding | `load_record` reads and parses all of `devices.csv` on every call. The read is most of its cost. |
| Evidence | **Verified Fact. REAL.** `domain_service.py` lines 8 to 10 open the file and build a list of 354 rows on each call. Run 3: 2.170 ms per call; the read alone 1.726 ms. Run 1: 1.718 ms and 1.504 ms. One call allocates a peak of 404.1 KiB. |
| Impact | Each device lookup costs about 2 ms, whatever the id. 1000 lookups read 41,883 bytes 1000 times, which is 41.9 MB. |
| Risk | Medium. At 354 rows the cost is small. It grows with the number of rows and the number of calls. |
| Confidence | High for the read being most of the cost in runs 1 and 3. Run 2 was noisy. |
| Open questions | How many device rows production holds. Unknown. |

### PB-02

| | |
|---|---|
| Finding | An id that is missing costs about 30 percent more than an id that exists. |
| Evidence | **Verified Fact. REAL.** Run 3: 2.858 ms against 2.170 ms. Run 1: 2.331 ms against 1.718 ms. Run 2: 1.742 ms against 1.616 ms. `domain_service.py` line 12 tests `record_id in row.values()`, which looks at all 12 cells of each row. Line 15 then returns the first row. **Inference:** the extra time is the full scan of 354 rows times 12 cells. An id that exists stops the scan early. |
| Impact | A wrong id costs more and also returns the wrong device (defect F01). The cost matters less than the wrong answer. |
| Risk | Low for time. High for the wrong row, which `docs/02-baseline/defect-list.md` already records. |
| Confidence | Medium. The gap changes by run. It was small in run 2. |
| Open questions | None beyond F01 and F17. |

### PB-03

| | |
|---|---|
| Finding | Adding threads does not speed up `load_record`. |
| Evidence | **Verified Fact. REAL.** 1000 calls on 8 threads took 3.058 s in run 3, 2.077 s in run 2, and 2.049 s in run 1. One thread took 2.170 s, 1.616 s, and 1.718 s. **Inference:** the work is Python code that parses text, and one Python process runs that kind of code on one thread at a time. |
| Impact | Raising the thread count of the server does not raise the number of record reads per minute. The only gains are less work per call (load once) or more server processes. |
| Risk | Medium. A team could add threads and see no change. |
| Confidence | Medium. The runs are noisy, but none showed a gain. |
| Open questions | How many server processes production would run. Unknown. |

### PB-04

| | |
|---|---|
| Finding | The access decision costs more than the file read. It spends its time searching the PATH for the `opa` program. |
| Evidence | **Verified Fact. REAL.** `policy.py` line 54 runs `shutil.which("opa")` inside `engine_name()`. `engine_name()` runs on every access decision (lines 124 and 236). Run 3: the PATH search 5.867 ms; the whole access decision 5.644 ms. Run 2: 8.153 ms and 8.976 ms. The two figures are close because the search is nearly all of the decision. |
| Impact | `GET /records/{id}` spends 40 percent of its time here. `POST /ai/summarize/{id}` spends 38 percent, because it runs three decisions. |
| Risk | Medium. The answer to the search never changes while the app runs. The app repeats it anyway. |
| Confidence | High that the search is the cost on this machine. Unknown on a Linux server. |
| Open questions | Which machine production runs on, and how long its PATH is. Unknown. |

### PB-05

| | |
|---|---|
| Finding | The summary call spends 29.3 ms inside the gateway, of which the stub is 10.7 ms. |
| Evidence | **Verified Fact. REAL.** Run 3: `summarize_record` 29.343 ms, `call_model` 10.680 ms. The gateway runs the policy twice (`ai_gateway.py` lines 419 and 425), builds a prompt, hashes it, and starts a new one-thread pool for each call (line 295). Two policy decisions are 11.3 ms (2 × 5.644). That leaves about 7.4 ms for the prompt, the hash, the pool, and the output check. The script does not split those four. |
| Impact | A real model that takes seconds would make the call length almost all model wait. The wait holds one of the 40 route threads for its whole length. |
| Risk | Medium. The stub hides the effect. |
| Confidence | High for the measured parts. Unknown for a real model. |
| Open questions | Real model latency and its spread. Unknown. |

### PB-06

| | |
|---|---|
| Finding | Grouping alarms and replaying events are cheap at the data size in the repo. |
| Evidence | **Verified Fact. REAL.** Grouping 354 alarms by `storm_batch_id` takes 1.690 ms. Replaying 3000 event lines takes 13.032 ms, which is 4.3 microseconds a line. |
| Impact | At this size neither step delays anyone. |
| Risk | Low today. Both grow in a straight line with the row count. |
| Confidence | High for the measurement. The straight-line growth is an **Inference**. |
| Open questions | Production alarm volume and event volume. Unknown. |

## How to run it again

From the folder `06-telecom-service-network-incident-ops`:

```text
.venv\Scripts\python.exe docs\10-performance\measure.py --rounds 5 --json docs\10-performance\measure-after.json
```

Half B writes `measure-after.json` with this command and compares it with `measure-before.json`.

## Lifecycle

`bottleneck-list.md` turns these findings into a ranked list with business effects. `load-scenarios.md` uses the per-call figures here. Stage S09 cites the before and after numbers.
