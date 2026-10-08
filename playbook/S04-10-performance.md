# S04-10 — Performance and scalability (Challenge 10)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `06-telecom-service-network-incident-ops/apps/api/services/domain_service.py`
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py`
- `06-telecom-service-network-incident-ops/data/synthetic/devices.csv`
- `06-telecom-service-network-incident-ops/data/synthetic/alarms.csv`
- `06-telecom-service-network-incident-ops/data/synthetic/service_orders.csv`
- `06-telecom-service-network-incident-ops/data/synthetic/events.jsonl`
- `06-telecom-service-network-incident-ops/semantic-layer/entities.yaml`
- `06-telecom-service-network-incident-ops/docs/01-discovery/business-flow-reconstruction.md`

## Prompt

```text
# Stage S04-10 — Performance and scalability (Challenge 10)

## Objective
Half A: measure how the current code behaves under the data it has, list the bottlenecks, and tie each one to a business effect. Half B: make the one change the design names (load the CSV once and index by id) and measure again.

## Scope
Include: `domain_service.py` read path; `ai_gateway.py` latency; alarm storms by `storm_batch_id`; event replay; order retries.
Exclude in Half A: any code change. Exclude in Half B: async rewrites, caching layers, or new routes (PROPOSED only).

## Required analysis (Half A)
1. Performance baseline: write `docs/10-performance/measure.py`. It times: 1000 calls to `load_record` for an existing id and for a missing id (the code re-reads `devices.csv` each call); grouping `alarms.csv` by `storm_batch_id` and counting the largest storm; replaying `events.jsonl` (3000 rows) through a no-op handler; the AI stub call. Report wall time and per-call time. Label the numbers REAL.
2. Bottleneck list: per bottleneck: where in the code, the measured cost, the data size it scales with, and the business effect (for example: a slower record read during an alarm storm delays triage and raises SLA breach risk on the affected circuit).
3. Load scenarios: alarm storm (largest storm_batch_id times N), 3000-event replay, order retries (sum of retry_count), described in terms of calls per minute. State what is Unknown because the repo has no production figure.
4. Scaling recommendations: load once and index by id; dedupe alarms in batch by dedupe_key; make the AI call asynchronous with a queue; each with the business effect it protects and an owner.
5. Data-access findings: which routes read which files, how often, and whether any read is repeated inside one request.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Change `domain_service.py` to load `devices.csv` once (module-level or cached) and index rows by `device_id`. Keep the public function signature. Keep the missing-id behaviour as it is in this stage if S04-03 or S07 has not yet changed it; say so.
2. Re-run `measure.py`. Record before and after in `docs/10-performance/evidence.md`.
3. Add `tests/performance/test_load_once.py`: the file is read once across many calls (monkeypatch open or count reads).

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line or a measured number from measure.py.
- Measured numbers are REAL. Load scenario extrapolations are EDUCATIONAL.

## Constraints and guardrails
- Plain speech.
- Every bottleneck row has a filled business-impact column. No row without one.
- No invented SLA threshold. A target latency is PROPOSED with an owner.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Record read | re-reads devices.csv on every call (domain_service.py) |
| Rows | 354 per CSV; 3000 events |
| AI stub | sleeps 0.01s |
| Alarm fields | storm_batch_id, dedupe_key |
| Order field | retry_count (values in the thousands appear) |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/10-performance/`:
1. `measure.py`
2. `performance-baseline.md`
3. `bottleneck-list.md`
4. `load-scenarios.md`
5. `scaling-recommendations.md`
6. `data-access-findings.md`
Half B:
7. `apps/api/services/domain_service.py` (load once, index)
8. `tests/performance/test_load_once.py`
9. `docs/10-performance/evidence.md`

## Completion gate
Half A PASS when every bottleneck row has a measured cost and a business impact. Half B PASS when the after measurement is recorded and the load-once test passes. CONDITIONAL PASS when a load scenario has no production figure and is marked Unknown. BLOCKED when any bottleneck row lacks a business impact.

## Lifecycle linkage
Cite docs/01-discovery/business-flow-reconstruction.md and entities.yaml. Stage S04-11 reuses the storm scenario as a drill. Stage S07 builds /alarms/storms on the indexed loader. Stage S09 cites the before and after.

## Required final response (after each half)
1. Stage status: PASS, CONDITIONAL PASS, or BLOCKED, with one sentence why.
2. Key findings.
3. Major risks.
4. Assumptions and unknowns.
5. Artifacts created, with paths.
6. Blocking issues.
7. Recommended next action.
```

## Expected output

| File | Must contain |
|---|---|
| `measure.py` | Runs. Prints four timings. |
| `performance-baseline.md` | Header. Timings labelled REAL. |
| `bottleneck-list.md` | Header. Every row has code location, cost, scales-with, business impact. |
| `load-scenarios.md` | Header. Three scenarios. Unknown where no figure. |
| `scaling-recommendations.md` | Header. Three items with business effect and owner. |
| `data-access-findings.md` | Header. Route × file × frequency. |
| `domain_service.py` | Load once, dict index. |
| `test_load_once.py` | Passing. |
| `evidence.md` | Header. Before and after timings. |

## Done test

The 1000-call timing in `evidence.md` is lower after the change, and the load-once test proves the file was read once.
