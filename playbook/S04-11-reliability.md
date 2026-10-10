# S04-11 — Reliability and failure engineering (Challenge 11)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `Project_Intent.md` (section 3.1 row 8)
- `06-telecom-service-network-incident-ops/docs/runbooks/failure-injection-drills.md`
- `06-telecom-service-network-incident-ops/docs/runbooks/incident-response.md`
- `06-telecom-service-network-incident-ops/apps/api/` (after S04-09)
- `06-telecom-service-network-incident-ops/etl/run_daily_batch.py`
- `06-telecom-service-network-incident-ops/semantic-layer/business-rules.yaml`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/unsafe-output-handling-rules.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/trace-design.md`
- `06-telecom-service-network-incident-ops/docs/10-performance/load-scenarios.md`

## Prompt

```text
# Stage S04-11 — Reliability and failure engineering (Challenge 11)

## Objective
Half A: catalogue how the system fails, design idempotency, retry, circuit breaking, and degraded mode, and complete the incident-response runbook. Half B: turn each failure drill into a test and record the recovery evidence.

## Scope
Include: the five drills in failure-injection-drills.md; the AI timeout path from S04-09; dedupe_key and retry_count; event replay by correlation_id; the ETL partial-batch case.
Exclude in Half A: any code change. Exclude in Half B: a message queue or external breaker library (PROPOSED only); new routes (S07).

## Required analysis (Half A)
1. Failure-mode catalogue: missing correlation id, AI timeout, duplicate replay, stale master data, partial batch failure, plus any the runbook misses (CSV file missing, policy engine unavailable). Per mode: trigger, what the user sees today, what data could be wrong, business effect, detection, YAML rule id.
2. Idempotency plan: alarm by dedupe_key within storm_batch_id; order by order id plus retry_count; event replay by correlation_id plus event sequence. State what a retry would duplicate today and how the count will be proven (this answers defence question 4).
3. Retry and circuit-breaker strategy: which calls retry, how many times, with what backoff (PROPOSED with owner), and when the breaker opens and what it returns.
4. Degraded-mode design: per dependency (AI gateway, policy engine, CSV files, audit log): what continues, what returns HOLD_FOR_REVIEW, what stops. AI down: /health and /records continue; recommendation returns HOLD_FOR_REVIEW with no summary. Audit log unwritable: the request fails, because audit comes before state change.
5. Complete docs/runbooks/incident-response.md: severity levels (named, no numeric cutoff without PROPOSED), triage steps, rollback steps, comms, and the evidence to collect. Mark every section that the repo left empty as "written in S04-11".
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. `tests/reliability/test_drills.py`: one test per drill. Missing correlation id: a UUID is created and logged. AI timeout: HOLD_FOR_REVIEW, no summary, /health still 200. Duplicate replay: the same alarm sent twice yields one alarm by dedupe_key (use a small in-memory dedupe helper in apps/api/services/dedupe.py). Stale master data: stale_topology_flag true yields HOLD_FOR_REVIEW. Partial batch failure: a CSV with one bad row makes the ETL report the bad row and continue with the rest (add a quarantine count to run_daily_batch.py without changing the existing count output). Impossible alarm timestamp: a row shaped like ALA-00002, where last_seen_at is before first_seen_at, is flagged and does not become an incident. Cite the business-rules.yaml id for that rule. This drill is separate from the stale_topology_flag drill.
2. Add the breaker as a small in-process helper in apps/api/services/breaker.py with the PROPOSED thresholds read from settings.
3. Run the drills. Record each run in docs/11-reliability/recovery-evidence.md.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line, a drill name, or a test name.
- Drill output is REAL.

## Constraints and guardrails
- Plain speech.
- No numeric retry count, backoff, or breaker threshold without PROPOSED and an owner.
- No fake safe summary on any failure path.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| AI-down behaviour today | Unknown as a designed mode; no timeout, no breaker, no fail-to-person |
| Routes that do not call the model | /health, /records/{id} |
| Drills named | missing correlation ids, AI timeout, duplicate replay, stale master data, partial batch failure, plus the impossible-timestamp case ALA-00002 (last_seen_at before first_seen_at) |
| Runbook sections missing | severity, triage, rollback, comms, evidence |
| ETL today | counts blanks, does not quarantine |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/11-reliability/`:
1. `failure-mode-catalogue.md`
2. `idempotency-plan.md`
3. `retry-and-circuit-breaker-strategy.md`
4. `degraded-mode-design.md`
5. completed `docs/runbooks/incident-response.md`
Half B:
6. `tests/reliability/test_drills.py`, `apps/api/services/dedupe.py`, `apps/api/services/breaker.py`, ETL quarantine count
7. `docs/11-reliability/recovery-evidence.md`

## Completion gate
Half A PASS when the degraded-mode design states what continues for every dependency and the runbook has all five sections. Half B PASS when every drill test passes, including the impossible-timestamp test, and the recovery evidence shows each run. CONDITIONAL PASS when a threshold is PROPOSED with an owner. BLOCKED when the AI-timeout drill returns a summary.

## Lifecycle linkage
Cite docs/09-ai-guardrails/unsafe-output-handling-rules.md, docs/08-observability/trace-design.md, docs/10-performance/load-scenarios.md, and business-rules.yaml ids. Stage S07 uses dedupe.py in /alarms/storms. Stage S09 cites the degraded-mode design. Stage S10 answers defence questions 4 and 8 from here.

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
| `failure-mode-catalogue.md` | Header. At least seven modes. Business effect per mode. |
| `idempotency-plan.md` | Header. Three keys. What a retry duplicates today. How the count is proven. |
| `retry-and-circuit-breaker-strategy.md` | Header. Per-call retry rules, all PROPOSED with owner. |
| `degraded-mode-design.md` | Header. Per dependency: continues, HOLD, stops. |
| `incident-response.md` | All five sections filled. |
| `test_drills.py` | Six passing drills. The sixth flags a last-seen-before-first-seen alarm and does not open an incident. |
| `recovery-evidence.md` | Header. One run per drill. |

## Done test

Stop the AI stub (monkeypatch it to sleep). `/health` returns 200. The recommendation returns HOLD_FOR_REVIEW with `summary: null`. The test that proves it passes.
