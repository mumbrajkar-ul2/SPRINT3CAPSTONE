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
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py` (after S04-09)

## Prompt

```text
# Stage S04-12 — Cost and AI FinOps (Challenge 12)

## Objective
Half A: build the AI cost baseline from the data in the repo and state cost per business outcome, not only as a total. Half B: make the gateway record tokens and latency per call so the metrics in metrics.yaml can be computed from the audit log.

## Scope
Include: token_count and cost fields in ai_invocations.csv and events.jsonl; retry_count in service_orders.csv; metrics.yaml ids; the cost envelope from S0B as revised in S2Q.
Exclude in Half A: any code change. Exclude in Half B: a billing integration or real tokenizer (PROPOSED only).

## Required analysis (Half A)
1. AI cost baseline: write docs/12-finops/cost_baseline.py. Sum token_count by model and by risk level in ai_invocations.csv. Sum cost fields in events.jsonl by event_type and by actor. Label every number: the CSV and JSONL figures are SIMULATED (synthetic data); any rate you apply is EDUCATIONAL.
2. Cost per workflow: map event_type values to the four business flows. State cost per flow and per correlated incident (metric id from metrics.yaml). Where the mapping is unclear, write Unknown.
3. Retry cost analysis: from service_orders.retry_count, state how many retries the data shows, what each retry would cost if it called the model, and the business effect (a stuck order delays a customer circuit).
4. Optimization backlog: cache repeated prompts by prompt_hash; batch alarm summaries per storm_batch_id; do not call the model for capabilities the S2Q table assigned to rules; each with the saving mechanism, the metric that will show it, and an owner. No saving number without a label.
5. FinOps dashboard fields: the fields from the S04-08 log schema that feed each metric: tokens, latency_ms, model, model_version, outcome, correlation_id.
6. Reconcile with docs/00-contract/cost-envelope.md: state where this baseline agrees and disagrees, and update the envelope's change log.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Confirm ai_gateway.py writes tokens and latency_ms into the audit row (added in S04-09). If any field is missing, add it.
2. Add docs/12-finops/metrics_from_audit.py: reads logs/audit.log and computes tokens per invocation, cost per correlated incident (with an EDUCATIONAL rate read from settings), recommendation latency. Prints a table with labels.
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
| ai_invocations.csv | 354 rows; fields include model, tokens, risk, approval, guardrail |
| events.jsonl | 3000 rows; latency and cost fields; four flows mixed |
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
Cite docs/00-contract/cost-envelope.md, docs/02-baseline/ai-qualification.md, docs/08-observability/log-schema.md, and metrics.yaml ids. Stage S07 shows one labelled cost number in the demo. Stage S09 cites the per-outcome cost.

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
