# S07 — Application and demo (product path steps 3 and 4, D6)

Phase 7 in `Execution Plan.md`. The app is built only from the PRD. The demo walks one flow to a human decision.

## Inputs

- `06-telecom-service-network-incident-ops/docs/prd/prd.md`
- `06-telecom-service-network-incident-ops/docs/prd/traceability.md`
- `06-telecom-service-network-incident-ops/docs/prd/prd-review.md`
- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree)
- `06-telecom-service-network-incident-ops/apps/api/` (after Phases 4 and 5)
- `06-telecom-service-network-incident-ops/apps/web/src/app/api.service.ts`
- `06-telecom-service-network-incident-ops/data/contracts/openapi-fragment.yaml`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/degraded-mode-design.md`
- `06-telecom-service-network-incident-ops/docs/12-finops/finops-dashboard-fields.md`

## Prompt

```text
# Stage S07 — Application and demo

## Objective
Build the governed application the PRD describes inside apps/api/, serve a small page that walks the demo flow, update the OpenAPI contract, and write the demo script. Every route behaves as the PRD says. The audit row is written before any state change.

## Scope
Include: the routes the PRD lists; a small served page (static HTML or FastAPI templates); data/contracts/openapi-fragment.yaml; docs/demo/.
Exclude: any route the PRD does not name; any EXECUTE path before the four gates exist; wiring the Angular scaffold, unless all four conditions in docs/00-contract/operating-contract.md row 5 are met (document it as a scaffold until then); any new term not in the YAML.

## Required work
1. Routes, each with tests under tests/app/:
   - GET /health.
   - GET /records/{id}: 404 on a missing id (this replaces the characterization test that locked the first-row fallback; note the swap). Role check via the S04-03 matrix and S04-06 policy.
   - GET /alarms/storms/{storm_batch_id}: groups alarms by dedupe_key using apps/api/services/dedupe.py; returns raw count, deduped count, and the alarm ids. Numbers labelled REAL.
   - POST /ai/summarize/{id}: keep this route. S04-09 hardens it. Do not remove it.
   - POST /ai/recommend/{id}: new route on the same gateway. Runs policy, prompt allow-list, schema, timeout; returns one of RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK; never EXECUTE from this route; writes the audit row with provenance before returning. The demo page calls this route.
   - POST /approvals/{id}: a named human persona records approve or reject with a reason; writes an audit row with approval_id; returns the decision. It does not execute anything.
   - GET /audit/{correlation_id}: from S05-14.
   - No EXECUTE route unless the PRD lists it and all four gates exist. If built, it is reversible and validated, and a test proves it refuses without approval_id.
2. Every route reads or creates X-Correlation-Id and passes it through. Every state-changing route writes its audit row first, then changes state. A test proves the order (make the state change fail and assert the audit row exists).
3. Page: one served page at / that lets a person pick a storm_batch_id, see the dedupe result, request a recommendation for one device or incident, see the outcome and provenance, approve or reject, and view the audit chain. Every number on the page shows its honesty label next to it.
4. Update data/contracts/openapi-fragment.yaml to the full route set with request and response schemas that match the YAML output schema.
5. Demo script: one case, step by step: the event, the data used (fields and labels), the policy result, the model and version, the human decision, the audit rebuild. Each number has its label. Include the AI-timeout variant: the recommendation returns HOLD_FOR_REVIEW with summary null and the page says a person must review.
6. Recording notes: what to show on screen at each step, which file proves it, and what not to claim.

## Evidence rules
- Label every claim in docs: Verified Fact, Inference, Assumption, Unknown.
- Every number the page or script shows carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. The model summary is SIMULATED (stub).
- Test output is REAL.

## Constraints and guardrails
- Plain speech in docs and in page text.
- Build only what the PRD names. If a route needs something the PRD lacks, stop and write it as an open question for S06.
- No fake safe summary on any failure path.
- No invented cutoff. PROPOSED with owner only.
- Redact secrets.
- Each doc starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Routes today | /health, /records/{id} (first-row fallback), /ai/summarize/{id} |
| Four outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Irreversible action | live network change; human approves |
| Model | local-sim-v1 (stub); summary is SIMULATED |
| Alarm keys | storm_batch_id, dedupe_key |

## Required artifacts
1. Code and tests in apps/api/ and tests/app/
2. The served page (apps/api/static/index.html or templates)
3. data/contracts/openapi-fragment.yaml (full)
4. `06-telecom-service-network-incident-ops/docs/demo/demo-script.md`
5. `06-telecom-service-network-incident-ops/docs/demo/demo-recording-notes.md`
6. `06-telecom-service-network-incident-ops/docs/demo/evidence.md` (full pytest output, the demo run's audit rows, redacted)

## Completion gate
PASS when the demo completes one flow to a human decision, the audit-before-state-change test passes, the AI-timeout variant returns HOLD_FOR_REVIEW with no summary, and every page number has a label. The served page alone can reach PASS. An unwired Angular scaffold does not lower the result. If the PRD names a screen or navigation need that the served page cannot meet, write it under "Recommended next action" as the Angular wiring step that operating-contract.md row 5 allows after this PASS. BLOCKED when any route returns a recommendation without a policy outcome, or any state change happens before its audit row.

## Lifecycle linkage
Cite prd.md requirement ids, semantic-layer ids, and the Phase 4 Half B tests. Stage S08 runs the same tests against the second model's app. Stage S09 cites the demo evidence. Stage S10 answers defence questions 1, 2, 3, 7 from here.

## Required final response
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
| Routes and tests | Summarize kept. Recommend added. 404 on missing id. Audit-first test. Timeout test. No EXECUTE without gates. No order or fix-validation route. |
| Served page | Storm pick, dedupe result, recommendation, approve/reject, audit chain. Labels on numbers. |
| `openapi-fragment.yaml` | All routes with schemas. |
| `demo-script.md` | Header. One case, six steps, labels. Timeout variant. |
| `demo-recording-notes.md` | Header. Per-step screen, proof file, do-not-claim. |
| `evidence.md` | Header. pytest output. Audit rows from the run. |

## Done test

Run the demo. Approve the recommendation. `GET /audit/<id>` shows: record read, recommendation with model_version and prompt_hash, approval with approval_id, and the audit query itself. Nothing executed.
