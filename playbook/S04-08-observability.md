# S04-08 — Observability and traceability (Challenge 8)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `06-telecom-service-network-incident-ops/apps/api/services/audit.py`
- `06-telecom-service-network-incident-ops/apps/api/main.py`
- `06-telecom-service-network-incident-ops/observability/otel-notes.md`
- `06-telecom-service-network-incident-ops/logs/audit.log` (from S00)
- `06-telecom-service-network-incident-ops/data/synthetic/events.jsonl`
- `06-telecom-service-network-incident-ops/semantic-layer/metrics.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/ai-context-policy.yaml`
- `06-telecom-service-network-incident-ops/docs/02-baseline/data-quality-baseline.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/business-flow-reconstruction.md`

## Prompt

```text
# Stage S04-08 — Observability and traceability (Challenge 8)

## Objective
Half A: design one trace id that follows a request from the UI through the API, the policy, the model, the approval, and the audit row, and design the log schema and metrics that make a business event explainable from stored rows. Half B: make `audit.py` write that schema and make every route take or create a `correlation_id`.

## Scope
Include: `audit.py`; the routes in `main.py`; `events.jsonl` fields; `metrics.yaml` ids; the SLO proposal.
Exclude in Half A: any code change. Exclude in Half B: a tracing backend or dashboard tool (PROPOSED only); new routes (S07).

## Required analysis (Half A)
1. Trace design: one `correlation_id` created at the first hop or accepted from the `X-Correlation-Id` header, carried to policy, AI, approval, and audit. State where it is created, where it is read, and what happens when it is missing (events.jsonl shows blank ids today; count them from the baseline).
2. Log schema: ts, correlation_id, actor, role, action, resource, policy_decision, approval_id, model, model_version, prompt_hash, tokens, latency_ms, outcome. Per field: type, source, required or optional, and the YAML id it maps to.
3. Metric catalogue: from metrics.yaml. Per metric: id, source fields, how it is computed from the log schema, and no target value unless PROPOSED with owner.
4. Dashboard sketch: a text layout of panels and the metric id each shows.
5. SLO proposal: API availability, recommendation latency, audit completeness. Each number PROPOSED with the owner who must confirm. Say what the repo gives today (Unknown if nothing).
6. One incident reconstruction: pick one correlation_id in events.jsonl that has more than one event. Lay out the chain from the first event to the last. Mark the gaps where a hop has no row.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Change `apps/api/services/audit.py` to write the log schema as one JSON object per line. Keep it append-only. Keep the file path `logs/audit.log`.
2. Add middleware or a dependency in `main.py` that reads `X-Correlation-Id` or creates a UUID, and makes it available to every handler and to audit.
3. Update the existing routes to pass actor, role, action, resource, and correlation_id into audit. Leave fields that do not exist yet (policy_decision, approval_id) as null until S04-06 and S07 fill them.
4. Add `tests/observability/test_audit_schema.py`: every audit row has every required field; a request with a header keeps the id; a request without one gets a UUID.
5. Replay the four S00 calls. Save the new audit lines in `docs/08-observability/evidence.md` next to the old ones.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path, a log line, a metric id, or a test name.
- Counts from events.jsonl are REAL.

## Constraints and guardrails
- Plain speech.
- No invented SLO number without PROPOSED and an owner.
- Never log mgmt_ip, credential_profile, or a secret. Cite ai-context-policy.yaml.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Audit row today | ts, action, details (record id, model name) — no actor, no correlation id, no approval id |
| events.jsonl | 3000 rows; some correlation_id null or blank |
| Model | local-sim-v1 |
| Token formula | len(prompt.split()) * 2 (EDUCATIONAL) |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/08-observability/`:
1. `trace-design.md`
2. `log-schema.md`
3. `metric-catalogue.md`
4. `dashboard-sketch.md`
5. `slo-proposal.md`
6. `incident-reconstruction.md`
Half B:
7. `apps/api/services/audit.py` (rewritten), middleware in `main.py`
8. `tests/observability/test_audit_schema.py`
9. `docs/08-observability/evidence.md`

## Completion gate
Half A PASS when the incident reconstruction explains one business event end to end from stored rows and marks every gap. Half B PASS when every audit row has every required field and the tests pass. CONDITIONAL PASS when the reconstruction has a gap that no stored row can fill and that is written. BLOCKED when any route writes an audit row without a correlation_id.

## Lifecycle linkage
Cite docs/02-baseline/data-quality-baseline.md for blank ids and metrics.yaml ids. Stage S04-09 writes model, model_version, prompt_hash, tokens, latency_ms into this schema. Stage S04-12 computes cost from it. Stage S05-14 rebuilds a case from it.

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
| `trace-design.md` | Header. Create / read / missing rules for the id. Hop list. |
| `log-schema.md` | Header. Fourteen fields with type, source, required, YAML id. |
| `metric-catalogue.md` | Header. One row per metrics.yaml id. |
| `dashboard-sketch.md` | Header. Panel layout in text. |
| `slo-proposal.md` | Header. Three SLOs, each PROPOSED with owner. |
| `incident-reconstruction.md` | Header. One chain with gaps marked. |
| `audit.py`, middleware | Writes the schema. |
| `test_audit_schema.py` | Passing. |
| `evidence.md` | Header. Old and new audit lines side by side. |

## Done test

Call `/records/REC-0001` with `X-Correlation-Id: demo-123`. The new audit line contains `"correlation_id": "demo-123"` and every required field.
