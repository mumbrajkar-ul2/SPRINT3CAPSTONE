# Data access findings

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS for this file. Every route is traced to the files and lookups it uses. Counts of file reads come from reading the code and from `grep` across the repo's `*.py` files. |
| Evidence sources | `apps/api/main.py`; `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `etl/run_daily_batch.py`; `legacy/reconcile_legacy.py`; `scripts/sanity_check.py`; `docs/01-discovery/data-and-integration-map.md`; `performance-baseline.md` |
| Assumptions | A "read" means opening a file and parsing it. A read of the PATH (looking for the `opa` program) is counted on its own line because it costs time too. |
| Unresolved issues | Whether several threads writing `logs/audit.log` at once keep each line whole is not tested. Unknown. |
| Residual risks | Load once (SR-01) makes the app see `devices.csv` as it was at the first call. Nothing in the repo writes that file, so the risk is low today. |

## What this file is

This file lists, for each route, which files it reads and writes, how often, and whether any read repeats inside one request.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Measured numbers are **REAL**.

Added after Half B: this file describes the code before Half B. Today `devices.csv` is read once per process, not once per request, and the PATH search runs once per process (`evidence.md`). The line numbers are the old ones.

## Routes and the data they touch

| Route | Reads of a data file in one request | PATH searches in one request | Writes in one request | Repeated inside one request? |
|---|---|---|---|---|
| `GET /health` (`main.py` line 54) | None | None | None | No |
| `GET /records/{id}` (`main.py` lines 58 to 70) | `devices.csv` once, all 354 rows (`main.py` line 68; `domain_service.py` lines 8 to 10) | 1 (`main.py` line 64 calls `policy.check_record_read`) | One line appended to `logs/audit.log` (`audit.py` line 92) | No |
| `POST /ai/summarize/{id}` (`main.py` lines 72 to 99) | `devices.csv` once, all 354 rows (`main.py` line 85) | 3 (`main.py` line 81; `ai_gateway.py` lines 419 and 425) | One line appended to `logs/audit.log` | The access decision runs three times. The PATH search runs three times. The file is read once. |

**Verified Fact** for every cell above: the line numbers name the call. A PATH search happens inside each policy decision (`policy.py` lines 54, 124, and 236).

Worked example. One `POST /ai/summarize/DEV-00002` opens `devices.csv` once, runs three policy decisions, and appends one audit line. Run 3 measured the whole call at 44.788 ms. The three PATH searches are about 16.9 ms of it (3 × 5.644 ms).

## Files with no reader in the app

| File | Rows or lines | Who reads it | Read per request? |
|---|---|---|---|
| `data/synthetic/alarms.csv` | 354 | `docs/02-baseline/profile_data.py`; tests in `semantic-layer/tests` | No. No route or service opens it. |
| `data/synthetic/service_orders.csv` | 354 | `docs/02-baseline/profile_data.py`; tests in `semantic-layer/tests` | No |
| `data/synthetic/events.jsonl` | 3000 | `scripts/sanity_check.py` line 29 (counts lines); `docs/02-baseline/profile_data.py` | No |
| `data/synthetic/devices.csv` | 354 | The API; `etl/run_daily_batch.py` line 8; `legacy/reconcile_legacy.py` line 17; `scripts/sanity_check.py` | Yes, on both routes |

**Verified Fact.** A search of `*.py` for each file name found the lines above. The API reads `devices.csv` only (`entities.yaml`, `entity.device.api_reads_today`).

Two files are read when the module loads, not per request: `policy_data.json` (`policy.py` line 28) and `ai-context-policy.yaml` (`ai_gateway.py` lines 85 and 108). **Verified Fact.**

## Findings

### DA-01

| | |
|---|---|
| Finding | Each device lookup reads the whole `devices.csv`, and nothing keeps the result for the next request. |
| Evidence | **Verified Fact.** `domain_service.py` lines 8 to 10. **REAL.** 354 rows, 41,883 bytes. One lookup uses 1 row, which is 0.3% of what it reads. 1000 lookups read 41.9 MB. |
| Impact | The cost per lookup is the same however many callers ask for the same device. At 4,202 lookups a minute (the most one caller can finish at cost B) the app would read about 176 MB a minute. That figure is **EDUCATIONAL**. |
| Risk | Medium. It grows with file size and with request rate. |
| Confidence | High. |
| Open questions | Production file size and request rate. Unknown. |

### DA-02

| | |
|---|---|
| Finding | One summary request runs the same engine lookup three times. |
| Evidence | **Verified Fact.** Three policy decisions: `main.py` line 81 (`check_summarize`), `ai_gateway.py` line 419 (pre-flight), and line 425 (final). Each calls `engine_name()`, which searches the PATH (`policy.py` line 54). **REAL.** 5.644 ms per decision. |
| Impact | About 16.9 ms of 44.788 ms is spent on lookups with the same answer each time. |
| Risk | Medium. When `opa` is installed, each decision also starts a process (`policy.py` line 66) and searches the PATH a second time (line 59). That cost is Unknown. |
| Confidence | High for the count. The `opa` path is not measured. |
| Open questions | Cost of the `opa` path. Unknown. |

### DA-03

| | |
|---|---|
| Finding | Alarms, orders, and events cause no data access in the running app today. |
| Evidence | **Verified Fact.** No route and no service opens `alarms.csv`, `service_orders.csv`, or `events.jsonl`. `docs/01-discovery/business-flow-reconstruction.md` Flows 1 and 2 agree. |
| Impact | The storm, replay, and retry scenarios in `load-scenarios.md` describe load the app does not yet receive. They become real when Stage S07 adds routes. |
| Risk | Medium. A route built the way `load_record` is built would read its file on every request. |
| Confidence | High. |
| Open questions | None. |

### DA-04

| | |
|---|---|
| Finding | `list_recent` reads the whole file and nothing calls it. |
| Evidence | **Verified Fact.** `domain_service.py` lines 17 to 19. A search of `*.py` finds no caller. `data-and-integration-map.md` line 22 says the same. |
| Impact | No cost today. |
| Risk | Low. A future caller would pay the same read per call. |
| Confidence | High. |
| Open questions | None. Half B changes `load_record` only. `list_recent` is left as it is unless the owner asks. |

### DA-05

| | |
|---|---|
| Finding | Each request opens `logs/audit.log`, appends one line, and closes the file. |
| Evidence | **Verified Fact.** `audit.py` line 92. **REAL.** 0.526 ms per row. |
| Impact | Small. 0.526 ms of 14.280 ms on the record route. The audit line is the proof of who did what, so the write stays. |
| Risk | Low for time. The effect of many threads writing at once on line integrity is not tested. |
| Confidence | High for the cost. Unknown for line integrity under load. |
| Open questions | Do concurrent writes keep each line whole? Unknown. |

### DA-06

| | |
|---|---|
| Finding | Load once makes `devices.csv` fixed for the life of the process. Today nothing changes the file while the app runs. |
| Evidence | **Verified Fact.** `data-and-integration-map.md` line 26: "No writer in the repo." The daily batch reads the file and does not rewrite it (defect F04). |
| Impact | If a real data feed later writes the file, the app shows old rows until restart. |
| Risk | Low today. |
| Confidence | High for the repo. Unknown for production. |
| Open questions | Does production replace `devices.csv` while the app runs? Unknown. This is decision 2 in `scaling-recommendations.md`. |

## Lifecycle

`bottleneck-list.md` uses DA-01 and DA-02. `scaling-recommendations.md` answers them with SR-01 and SR-02. Half B changes the first read pattern and re-measures it.
