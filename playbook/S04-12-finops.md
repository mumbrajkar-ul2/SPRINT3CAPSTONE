# S04-12 — Cost and AI FinOps (Challenge 12)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `Project_Intent.md` (Appendix B)
- `06-telecom-service-network-incident-ops/data/synthetic/ai_invocations.csv`
- `06-telecom-service-network-incident-ops/data/synthetic/events.jsonl`
- `06-telecom-service-network-incident-ops/data/synthetic/service_orders.csv`
- `06-telecom-service-network-incident-ops/semantic-layer/metrics.yaml`
- `06-telecom-service-network-incident-ops/docs/00-contract/cost-envelope.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/log-schema.md`
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py` (after S04-09 and S04-11; it now asks the breaker before each model call)
- `06-telecom-service-network-incident-ops/docs/11-reliability/recovery-evidence.md` (a held call makes no model call, so its audit row has `tokens` and `latency_ms` null)
- `06-telecom-service-network-incident-ops/docs/11-reliability/idempotency-plan.md` (the summary route has no idempotency key, so a repeat call costs a model call)
- `06-telecom-service-network-incident-ops/docs/11-reliability/retry-and-circuit-breaker-strategy.md` (model calls are not retried; PROPOSED breaker numbers cap calls during an outage)
- `06-telecom-service-network-incident-ops/docs/08-observability/trace-design.md` and `06-telecom-service-network-incident-ops/semantic-layer/entities.yaml` (definitions of the four business flows for item 2)

## Prompt

```text
# Stage S04-12 — Cost and AI FinOps (Challenge 12)

## Objective
Half A: build the AI cost baseline from the data in the repo and state cost per business outcome, not only as a total. Half B: make the gateway record tokens and latency per call so the metrics in metrics.yaml can be computed from the audit log.

## Scope
Include: `token_count` in ai_invocations.csv; `cost_units` and `latency_ms` in events.jsonl; retry_count in service_orders.csv; metrics.yaml ids; the cost envelope from S0B as revised in S2Q.
Exclude in Half A: any code change. Exclude in Half B: a billing integration or real tokenizer (PROPOSED only).

## Required analysis (Half A)
1. AI cost baseline: write docs/12-finops/cost_baseline.py. Sum token_count by model and by risk level in ai_invocations.csv. Before you group, check the `model` column and the risk columns (see the locked facts below). If a column holds status words instead of model names, say so, group by what it really holds, and write Unknown for the model name. Sum `cost_units` in events.jsonl by event_type and by actor. Also report `latency_ms`. events.jsonl has no token field. Label every number: the CSV and JSONL figures are SIMULATED (synthetic data); any rate you apply is EDUCATIONAL.
2. Cost per workflow: map event_type values to the four business flows. State cost per flow and per correlated incident (metric id from metrics.yaml). Take the flow definitions from trace-design.md and entities.yaml. Where the mapping is unclear, write Unknown. Count a held call (timeout, breaker open, in-flight limit) as 0 tokens, because it makes no model call.
3. Retry cost analysis: from service_orders.retry_count, state how many retries the data shows, what each retry would cost if it called the model, and the business effect (a stuck order delays a customer circuit). S04-11 says the gateway does not retry model calls, so this cost is a what-if. Label it EDUCATIONAL.
4. Optimization backlog: cache repeated prompts by prompt_hash (S04-11 drill DR-3 shows five identical summary calls cost five model calls); batch alarm summaries per storm_batch_id; do not call the model for capabilities the S2Q table assigned to rules; each with the saving mechanism, the metric that will show it, and an owner. No saving number without a label.
5. FinOps dashboard fields: the fields from the S04-08 log schema that feed each metric: tokens, latency_ms, model, model_version, outcome, correlation_id.
6. Reconcile with docs/00-contract/cost-envelope.md: state where this baseline agrees and disagrees, and add a new row to the envelope's change log. The file is already REVISED-S2Q at v1.1, so do not rewrite earlier rows.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Confirm ai_gateway.py writes tokens and latency_ms into the audit row (added in S04-09). If any field is missing, add it.
2. Add docs/12-finops/metrics_from_audit.py: reads logs/audit.log and computes tokens per invocation, cost per correlated incident (with an EDUCATIONAL rate read from settings), recommendation latency. Prints a table with labels. Count held rows (tokens null) separately, so they do not lower the average. For `metric.quarantine_rate`, say where the number comes from. The ETL `quarantined` count (S04-11) prints to stdout and is not in the audit log. Write that as a gap or an Open question for S03. Do not read it from the audit log.
3. Mark the token formula len(prompt.split()) * 2 as EDUCATIONAL in a code comment and in the audit row (field token_estimate_method: "word_count_x2_EDUCATIONAL").
4. Run both scripts. Record in docs/12-finops/evidence.md.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file, a column, a metric id, or a script output.
- Every number carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.

## Constraints and guardrails
- Plain speech.
- No budget, rate card, or saving target without PROPOSED and an owner.
- Cost is stated per business outcome. A total alone does not pass.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Token formula | len(prompt.split()) * 2 (EDUCATIONAL) |
| ai_invocations.csv | 354 rows. Columns: ai_call_id, incident_id, use_case, model, topology_snapshot_id, alarm_count, token_count, recommendation_risk, approval_required, guardrail_status. No cost column. Any rate is EDUCATIONAL with an owner. |
| ai_invocations.csv `model` column | Values seen on 2026-10-11 include `not_enforced`, `pending`, `legacy`, `standard`. These look like status words, not model names. Treat the real model name as Unknown until checked. Verify in Half A. |
| ai_invocations.csv risk level | `recommendation_risk` and `use_case` both hold risk-like words. Half A states which column it used and why. |
| events.jsonl | 3000 rows. Fields: event_id, business_entity, event_type, severity, correlation_id, actor, latency_ms, cost_units, payload_hash. No token field. Four event_type values (one per business flow): Topology lookup to AI recommendation (782), Approved remediation to validation (771), Customer order to provisioning (741), Alarm storm to incident correlation (706). |
| Held AI calls (S04-11) | A timeout, an open breaker, or the in-flight limit gives HOLD_FOR_REVIEW with no model call. Audit row: `tokens` and `latency_ms` null. |
| Summary route idempotency (S04-11) | No key. Repeat calls each cost a model call. |
| Breaker numbers (S04-11) | 5 failures in a row, 30 s open, 10 calls at once. All PROPOSED, owner Team-Force. |
| Cost envelope | `docs/00-contract/cost-envelope.md` is REVISED-S2Q, v1.1. |
| Live gateway writes ai_invocations.csv | No |
| Metrics (metrics.yaml) | tokens per invocation, cost per correlated incident, quarantine rate, retry count, audit completeness, recommendation latency |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/12-finops/`:
1. `cost_baseline.py`
2. `ai-cost-baseline.md`
3. `cost-per-workflow.md`
4. `retry-cost-analysis.md`
5. `optimization-backlog.md`
6. `finops-dashboard-fields.md`
7. updated `docs/00-contract/cost-envelope.md` change log
Half B:
8. `metrics_from_audit.py`, gateway field check, token_estimate_method field
9. `docs/12-finops/evidence.md`

## Completion gate
Half A PASS when cost is stated per flow and per correlated incident with labels, and the backlog names a metric per item. Half B PASS when metrics_from_audit.py computes the metrics.yaml metrics from real audit rows. CONDITIONAL PASS when the event_type-to-flow mapping has Unknown rows. BLOCKED when any number lacks a label or cost appears only as a total.

## Lifecycle linkage
Cite docs/00-contract/cost-envelope.md, docs/02-baseline/ai-qualification.md, docs/08-observability/log-schema.md, docs/11-reliability/recovery-evidence.md, and metrics.yaml ids. Stage S07 shows one labelled cost number in the demo. Stage S09 cites the per-outcome cost.

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
| `cost_baseline.py` | Runs. Prints sums with labels. |
| `ai-cost-baseline.md` | Header. Tokens by model and risk. Cost by event_type and actor. Labels. |
| `cost-per-workflow.md` | Header. Four flows. Cost per correlated incident. Unknown rows. |
| `retry-cost-analysis.md` | Header. Retry count, cost if modelled, business effect. |
| `optimization-backlog.md` | Header. Three items with mechanism, metric id, owner. |
| `finops-dashboard-fields.md` | Header. Field to metric map. |
| `metrics_from_audit.py` | Runs against `logs/audit.log`. |
| `evidence.md` | Header. Both script outputs. |

## Done test

`cost-per-workflow.md` has a cost figure per flow, each with a label. No figure appears only as a grand total.
