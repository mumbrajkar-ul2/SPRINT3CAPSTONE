# S09 — Production readiness gate and evidence pack (Challenges 15 and 16, D8)

Phase 9 in `Execution Plan.md`. This stage decides what is ready and assembles the proof. No new work. Every claim points at a file.

## Inputs

- `Project_Intent.md` (section 6.3)
- `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf` (final standard)
- `06-telecom-service-network-incident-ops/PRODUCTION_EVIDENCE_PACK_TEMPLATE.md`
- `06-telecom-service-network-incident-ops/docs/` (every folder 00 to 14, prd, demo, model-comparison)
- `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md`
- `06-telecom-service-network-incident-ops/docs/00-contract/challenge-to-spine-crosswalk.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/brownfield-risk-register.md`
- `06-telecom-service-network-incident-ops/docs/13-security-validation/remediation-backlog.md`
- `06-telecom-service-network-incident-ops/docs/14-audit/compliance-evidence-mapping.md`
- `06-telecom-service-network-incident-ops/evidence/`
- `playbook/STATUS.md`

## Prompt

```text
# Stage S09 — Production readiness gate and evidence pack

## Objective
Challenge 15: decide what is ready for production, what is not, and which risk is accepted by whom. Challenge 16: fill PRODUCTION_EVIDENCE_PACK.md so a reviewer can check every claim from the pack without a spoken tour.

## Scope
Include: every artifact from stages S00 to S08; the stage statuses in playbook/STATUS.md; the evidence/ folder.
Exclude: new work; any claim without a file pointer; any change to code or YAML.

## Required analysis (Challenge 15)
1. Readiness checklist: one row per control area (identity, secrets, IaC, policy, CI/CD, observability, AI guardrails, performance, reliability, FinOps, security validation, audit). Per row: ready / not ready / partial; the file or test that proves it; the stage status from STATUS.md.
2. Residual risk register: merge the open items from docs/01-discovery/brownfield-risk-register.md, docs/09-ai-guardrails/ai-risk-register.md, docs/11-reliability/failure-mode-catalogue.md, and docs/13-security-validation/remediation-backlog.md. Per risk: still open, mitigated by what, accepted by whom (or Unknown).
3. Go/no-go decision: one paragraph. Ready for what, not ready for what, under which conditions. No hedging word without a stated reason.
4. Risk owner table: every accepted risk with a named owner role. Unknown where the packet names none, with PROPOSED.
5. Deferred work list: everything the plan named and did not finish, with the stage and the reason.
6. Check every change made against docs/00-contract/operating-contract.md. List any change that crossed a Prohibited or PROVISIONAL boundary.

## Required work (Challenge 16)
7. Copy PRODUCTION_EVIDENCE_PACK_TEMPLATE.md to PRODUCTION_EVIDENCE_PACK.md. Fill every heading. Per section: the claim, the evidence file or test (path), the honesty label of any number, and what is still unproven.
8. Add an executive summary at the top and the challenge-to-spine crosswalk at the end.
9. Verify every path in the pack exists. Write the check output into docs/16-evidence-pack/path-check.md.
10. Run make evidence one final time so evidence/ is current. Note the run id in the pack.
For each finding: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path or a test name. No claim in the pack is without one.
- Every number carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.

## Constraints and guardrails
- Plain speech. A reviewer new to the project must follow the pack alone.
- No new control, test, or fix in this stage.
- Say "not ready" where it is true. A pack that claims ready without a test fails the gate.
- Redact secrets.
- Each doc starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Template headings | Release Summary; Behavioural Baseline; IAM; Secrets; IaC; Policy-as-Code; CI/CD and Supply Chain; Observability; AI Security; Performance; Reliability; AI FinOps; Automated Security Validation; Auditability; Production Readiness Decision |
| Final standard (challenge guide) | A reviewer can verify the transformation from the pack without a verbal tour |
| 6.3 items | D1 to D8 exist; AI cannot silently execute; timeout sends to a person; labels on demo numbers; owners on accepted risk |

## Required artifacts
Challenge 15, under `06-telecom-service-network-incident-ops/docs/15-readiness/`:
1. `readiness-checklist.md`
2. `residual-risk-register.md`
3. `go-no-go-decision.md`
4. `risk-owner-table.md`
5. `deferred-work-list.md`
6. `operating-contract-check.md`
Challenge 16:
7. `06-telecom-service-network-incident-ops/PRODUCTION_EVIDENCE_PACK.md`
8. `06-telecom-service-network-incident-ops/docs/16-evidence-pack/path-check.md`
9. `evidence/` current

## Completion gate
PASS when the decision states ready, not ready, and accepted risk with owners, every pack claim has a path that exists, and every 6.3 item is ticked or marked not ready. CONDITIONAL PASS when an owner is PROPOSED. BLOCKED when any pack path does not exist or any claim has no evidence.

## Lifecycle linkage
Cite every stage's completion gate result from playbook/STATUS.md and docs/00-contract/operating-contract.md. Stage S10 presents from this pack.

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
| `readiness-checklist.md` | Header. Twelve control rows with status, proof, stage status. |
| `residual-risk-register.md` | Header. Merged open risks. Accepted-by column. |
| `go-no-go-decision.md` | Header. One paragraph decision. Conditions. |
| `risk-owner-table.md` | Header. Owner per accepted risk. |
| `deferred-work-list.md` | Header. Unfinished items with stage and reason. |
| `operating-contract-check.md` | Header. Changes vs boundaries. |
| `PRODUCTION_EVIDENCE_PACK.md` | Executive summary. Every heading filled with claim, path, label, unproven. Crosswalk at the end. |
| `path-check.md` | Header. Every pack path checked. |

## Done test

Give the pack to someone who has not seen the project. They pick three claims. Each one resolves to a file or test that proves it.
