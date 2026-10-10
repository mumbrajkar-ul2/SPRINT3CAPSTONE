# S05-14 — Auditability and compliance evidence (Challenge 14)

Phase 5 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted". After this stage one case can be rebuilt from stored rows.

## Inputs

- `Project_Intent.md` (section 3.3 question 5)
- `06-telecom-service-network-incident-ops/apps/api/services/audit.py` (after S04-08)
- `06-telecom-service-network-incident-ops/apps/api/main.py`
- `06-telecom-service-network-incident-ops/logs/audit.log`
- `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/behaviour-snapshot.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/log-schema.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/model-provenance-design.md`
- `06-telecom-service-network-incident-ops/docs/06-policy/ai-action-policy-design.md`
- `06-telecom-service-network-incident-ops/docs/transformation-roadmap.md`

## Prompt

```text
# Stage S05-14 — Auditability and compliance evidence (Challenge 14)

## Objective
Half A: state what the audit trail could not prove before, design the decision provenance record, and show the evidence chain for one case. Half B: add a route that rebuilds a case from stored rows by correlation_id.

## Scope
Include: the old audit row shape; the S04-08 log schema; the S04-09 provenance fields; the S04-06 policy result; the approval id (null until S07).
Exclude in Half A: any code change. Exclude in Half B: the approvals route itself (S07); a database or external store (PROPOSED only).

## Required analysis (Half A)
1. Audit gap report: the old row had timestamp, action, record id, model name. For each provenance question (who, what request, what data, which model and version, which policy result, which approval, what final action, which trace id) say whether the old row could answer it. Cite docs/00-setup/replay-log.md.
2. Decision provenance model: the fields a complete record needs, grouped as actor, request, data used, model, policy, approval, final action, trace, and a "cannot be proven" list. Map each field to the log schema field and YAML id.
3. Evidence chain for one case: take the correlation_id from one guardrail test run or one replayed call after S04-09. List every stored row in order. Show the chain. Mark what is still missing (approval_id is null; final action is none).
4. Compliance evidence mapping: for each control area in the challenge guide (identity, secrets, policy, AI, audit) name the stored evidence that proves it and where a reviewer finds it.
5. Before-and-after audit example: POST /ai/summarize/REC-0001 from S00 (before) next to the same call after S04-09 (after). Show both rows in full, secrets redacted.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Add apps/api/services/audit_query.py that reads logs/audit.log and returns every row for a correlation_id in time order.
2. Add GET /audit/{correlation_id} in main.py. It requires a role allowed to read audit (from the S04-03 matrix), calls the policy, writes its own audit row, and returns the chain plus a cannot_prove list computed from null fields.
3. Add tests/audit/test_audit_rebuild.py: a known chain is returned in order; an unknown id returns 404; a role without audit permission gets 403.
4. Run it for the case from Half A. Record in docs/14-audit/evidence.md.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a log line, a route response, or a test name.
- Stored rows are REAL. The model summary inside them is SIMULATED.

## Constraints and guardrails
- Plain speech.
- The audit route never alters the log. Read only.
- Redact secrets in every pasted row.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Old audit row | ts, action, details (record id, model name) |
| New schema (S04-08) | ts, correlation_id, actor, role, action, resource, policy_decision, approval_id, model, model_version, prompt_hash, tokens, latency_ms, outcome |
| Approval route | not built until S07; approval_id is null in this stage |
| Defence question 5 | actor, request, data used, model and version, policy result, approval, final action, trace id, what cannot be proven |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/14-audit/`:
1. `audit-gap-report.md`
2. `decision-provenance-model.md`
3. `evidence-chain-one-case.md`
4. `compliance-evidence-mapping.md`
5. `before-and-after-audit-example.md`
Half B:
6. `apps/api/services/audit_query.py`, GET /audit/{correlation_id} in main.py
7. `tests/audit/test_audit_rebuild.py`
8. `docs/14-audit/evidence.md`

## Completion gate
Half A PASS when the chain for one case shows what happened, who or what influenced it, and the unproven items. Half B PASS when the route returns that chain and the tests pass. CONDITIONAL PASS when approval_id is null and that is listed under cannot_prove. BLOCKED when the route can return a chain without a policy check or writes no audit row for itself.

## Lifecycle linkage
Cite docs/00-setup/replay-log.md, docs/02-baseline/behaviour-snapshot.md, docs/08-observability/log-schema.md, docs/09-ai-guardrails/model-provenance-design.md. Stage S07 fills approval_id and final action. Stage S09 uses the compliance mapping as the pack's index. Stage S10 answers defence question 5 from the route output.

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
| `audit-gap-report.md` | Header. Eight provenance questions, each answered yes/no for the old row. |
| `decision-provenance-model.md` | Header. Grouped fields with log field and YAML id. "Cannot be proven" list. |
| `evidence-chain-one-case.md` | Header. Ordered rows for one correlation_id. Missing items marked. |
| `compliance-evidence-mapping.md` | Header. Control area to stored evidence to location. |
| `before-and-after-audit-example.md` | Header. Two rows, full, redacted. |
| `audit_query.py`, route | Read only. Policy checked. Own audit row. |
| `test_audit_rebuild.py` | Three passing tests. |
| `evidence.md` | Header. Route output for the case. |

## Done test

`GET /audit/<id>` for the case returns the ordered rows and a `cannot_prove` list that includes `approval_id`. The call itself appears as the last row on the next query.
