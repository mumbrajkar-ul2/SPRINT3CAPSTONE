# Bottleneck list

| Field | Value |
|---|---|
| Stage | S04-10 — Performance and scalability (Challenge 10), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS for this file. All seven rows have a measured cost and a business effect. |
| Evidence sources | `performance-baseline.md` (run 3 unless a row says otherwise); `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/main.py`; `semantic-layer/entities.yaml`; `docs/01-discovery/business-flow-reconstruction.md`; `docs/08-observability/slo-proposal.md` |
| Assumptions | A bottleneck here is a step that sets how many requests finish per minute, or how long one request takes. Business effects are Inferences. The repo has no production traffic, so no effect is measured on real users. |
| Unresolved issues | Production request rate, storm size, and model latency are Unknown. Rows BN-04, BN-06, and BN-07 depend on figures the repo does not hold. |
| Residual risks | Rank is by measured cost on this machine. A Linux server with a short PATH could change the rank of BN-02. |

## What this file is

This file lists the steps that cost time in the current code. Each row names the place in the code, the measured cost, what the cost grows with, and the effect on the business.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Measured numbers are **REAL**.

Added after Half B: this list describes the code before Half B. Rows BN-01 and BN-02 are answered by the two changes in `evidence.md`. The line numbers in this file are the old ones.

The business story the rows share comes from the flow in `docs/01-discovery/business-flow-reconstruction.md`. A person who triages a service problem looks up a device, and may ask for a summary of it. The record also carries `stale_topology_flag`. The incident row has `sla_breach_risk`, the score for how likely the service promise to a customer will be broken (`semantic-layer/entities.yaml`, `field.incident.sla_breach_risk`). Time lost at the lookup is time added before anyone acts on the incident.

## The list, ranked by cost per request

| ID | Finding | Where in the code | Measured cost (REAL) | What the cost grows with | Business effect |
|---|---|---|---|---|---|
| BN-01 | The access decision searches the PATH for the `opa` program on every call, and the answer never changes while the app runs. | `policy.py` line 54 (`engine_name`), called at lines 124 and 236. | 5.867 ms per search. 5.644 ms per access decision. That is 40% of `GET /records/{id}` (14.280 ms) and 38% of `POST /ai/summarize/{id}` (three decisions, 16.9 of 44.788 ms). | Number of policy decisions, times the number of folders on the PATH. | Every device lookup and every summary starts about 6 ms late. During an alarm storm the lookups that decide where to act each wait that extra time, so the first action on an incident comes later and the risk of breaking the service promise on its circuit rises a little. |
| BN-02 | `load_record` reads and parses the whole of `devices.csv` on every call, then uses one row. | `domain_service.py` lines 8 to 10. | 2.170 ms per call. 1.726 ms of it is the read. One call allocates a peak of 404.1 KiB. Run 1: 1.718 ms. | Rows in `devices.csv` (354 today), times calls. | Each lookup costs a fixed 2 ms, so the number of lookups per minute that one server process can finish is capped. At 2.170 ms the cap is 27,656 per minute. Threads do not raise it (3.058 ms per call on 8 threads). During a large storm, later lookups queue behind earlier ones and triage slows. |
| BN-03 | A summary call keeps one of the 40 route threads for the whole model wait. | `ai_gateway.py` line 172 (stub wait); `main.py` line 73 (`def` route); `ai_gateway.py` line 295 (new pool per call). | Stub 10.680 ms. Whole gateway call 29.343 ms. Whole route 44.788 ms. Thread limit 40. A real model's wait is Unknown. | Model wait, times the number of summaries asked at the same time. | While 40 summaries wait on the model, a lookup that arrives needs a free thread and waits too. With the PROPOSED 2000 ms for 95 of 100 summaries (`slo-proposal.md`), 40 threads finish 20 summaries a second. At the PROPOSED 10 second timeout they finish 4 a second. A storm that asks for many summaries then delays plain lookups for the same incidents. |
| BN-04 | `load_record` scans all 12 cells of every row for a match, so a missing id costs more. | `domain_service.py` lines 12 and 15. | 2.858 ms for a missing id against 2.170 ms for an id that exists (32% more). | Rows times 12 cells. | A wrong or retired id costs more and still gets an answer, the first device row (defect F01). Triage that acts on that answer works on the wrong device. The time is small. The wrong answer is the larger effect. |
| BN-05 | Each request opens the audit file, appends one line, and closes it. | `audit.py` line 92. | 0.526 ms per row. 4% of `GET /records/{id}`. | Number of requests. | The cost is small. The audit row is the proof of who read what, so the step stays. A storm of 2000 lookups spends about 1 second here (2000 × 0.526 ms). The effect on triage is small. |
| BN-06 | A storm summary built on the same read-per-request pattern would re-read `alarms.csv` on each request. No route does this today. | No code yet. `alarms.csv` has 354 rows. The measured pattern is the one in `measure.py`. | 1.690 ms to group 354 alarms by `storm_batch_id`. 1.705 ms by `dedupe_key`. | Alarm rows, times requests. | Stage S07 plans `/alarms/storms`. If it re-reads the file on each call, the storm view is slowest exactly while a storm runs. At 354 rows the delay is under 2 ms, so the effect today is none. At a production row count the cost is Unknown. |
| BN-07 | Replaying the event log reads and parses every line. | `events.jsonl`, 3000 lines, 792,328 bytes. No route reads it. `scripts/sanity_check.py` line 29 counts its lines. | 13.032 ms for 3000 lines (4.3 microseconds a line). | Number of event lines. | A 3000 event replay finishes in 13 ms, so it does not delay an incident review. It becomes a delay only at a size far above this file. At 1000 times the lines the same code would take about 13 seconds (straight-line growth, **EDUCATIONAL**). |

Worked example for BN-01 and BN-02 together. One `GET /records/{id}` call measured 14.280 ms. The access decision took 5.644 ms and `load_record` took 2.170 ms. Together that is 7.8 ms, or 55 percent of the call. Half B's change (load once) removes about 1.7 ms of the 14.3 ms. That is 12 percent. The access decision is more than three times that saving.

## Risk, confidence, and open questions

| ID | Risk | Confidence | Open questions |
|---|---|---|---|
| BN-01 | Medium. The cost is the same on every call, and it is paid on the record route and on the summary route. | High on this machine. Unknown on a server with a short PATH. | Which machine production runs on. Unknown. With `opa` installed, each decision also starts a process, and that cost is Unknown (the program is absent here). |
| BN-02 | Medium. Small at 354 rows. Grows with rows and with calls. | High. Run 2 was noisy, and runs 1 and 3 agree that the read is most of the cost. | How many device rows production holds. Unknown. |
| BN-03 | High once a real model replaces the stub. Low today. | Medium. The 40-thread limit is measured. The model wait is the **Assumption** that the PROPOSED numbers describe it. | Real model latency. Unknown. How many summaries run at the same time in production. Unknown. |
| BN-04 | Low for time. High for the wrong row. | Medium. The gap was 32%, 36%, and 8% in runs 3, 1, and 2. | Which column is the key of a record read (open under F17). |
| BN-05 | Low. | High. | Whether many threads writing to one file at once interleave lines. Not measured. Unknown. |
| BN-06 | Low today. Medium when S07 builds the route. | Medium. The measurement is real. The route does not exist yet. | Production alarm volume. Unknown. How many alarms make a storm is not in the repo (`concept.storm`). |
| BN-07 | Low. | High for the measurement. | How often anyone replays the log and how large it grows. Unknown. |

## Not a bottleneck here

- **`list_recent`** (`domain_service.py` lines 17 to 19) also reads the whole file, but no route calls it and no test calls it. Verified Fact. It carries no cost today.
- **Prompt policy file.** `ai_gateway.py` lines 85 and 108 read `ai-context-policy.yaml` once, when the module loads. `policy.py` line 28 reads `policy_data.json` once at load. Neither is repeated per request. Verified Fact.

## Lifecycle

`scaling-recommendations.md` answers each row. `load-scenarios.md` puts these costs into calls per minute. Stage S04-11 reuses the storm scenario as a drill.
