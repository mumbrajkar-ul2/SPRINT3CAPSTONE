# S06 — Product Requirements Document (product path step 2, D5)

Phase 6 in `Execution Plan.md`. The PRD is written from the semantic layer and the Phase 4 and 5 designs. Both the first app and the second model build from it.

## Inputs

- `Project_Intent.md` (sections 3.1, 5.2, 5.3, 6.3)
- `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf` (product path)
- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
- `06-telecom-service-network-incident-ops/docs/03-identity/target-access-matrix.md`
- `06-telecom-service-network-incident-ops/docs/06-policy/ai-action-policy-design.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/unsafe-output-handling-rules.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/degraded-mode-design.md`
- `06-telecom-service-network-incident-ops/docs/14-audit/decision-provenance-model.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/slo-proposal.md`

## Prompt

```text
# Stage S06 — Product Requirements Document

## Objective
Write the PRD for the governed application. Every requirement cites a semantic-layer id. Every acceptance check names a test. The PRD picks the demo flow and says which routes the app will not implement.

## Scope
Include: the semantic layer; the S2Q table; the Phase 4 and 5 designs listed as inputs.
Exclude: code; any term or status word that is not in the YAML; any requirement with no YAML id.

## Required analysis
1. Classify the four flows and the three AI products as in Project_Intent.md 5.2, using ai-qualification.md as the only source for the AI pick and agency.
2. Pick the demo flow. Recommended: topology lookup to AI recommendation, extended to a human decision, with alarm-storm dedupe as the deterministic analysis step. State why, or pick another flow and state why.
3. Write the PRD sections:
   - Users: the personas from access-semantics.yaml, what each does in the flow, what each may see.
   - Workflows: the demo flow step by step with the verb (analyse, recommend, decide, execute) per step and the persona per step.
   - AI limits: for every AI use, quote the pick, agency, and approval point from ai-qualification.md; the four outcomes; fail-to-person; forbidden fields.
   - Data: entities and fields used, from entities.yaml; which are read-only; honesty label of each displayed number.
   - Risk: from the risk registers; what the app leaves visible as an inherited gap.
   - Non-functional needs: the SLO proposals (PROPOSED with owner), degraded mode, audit-before-state-change.
   - Acceptance checks: one per requirement; each names an existing or planned test file and test name.
   - Success metrics: metric ids from metrics.yaml.
4. Routes: the list the app will implement (/health, /records/{id} with 404, /alarms/storms/{storm_batch_id}, /ai/recommend/{id}, /approvals/{id}, /audit/{correlation_id}) and the list it will not implement, with the reason. No EXECUTE route unless all four gates exist; if listed, it is reversible and validated.
5. Traceability: a table requirement id to YAML id to acceptance test to Phase 4 design file.
For each requirement: id, text, YAML id, test, source design.

## Evidence rules
- Every requirement cites at least one YAML id.
- Label other claims: Verified Fact, Inference, Assumption, Unknown.
- Every displayed number in the workflow carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.

## Constraints and guardrails
- Plain speech. A new reader must know what to picture after one pass.
- Do not define a term. Use the glossary. If a needed term is missing, write it as an open question for S03, not in the PRD.
- No invented cutoff or threshold. PROPOSED with owner only.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Four flows | order to provisioning; alarm storm to incident; topology to AI recommendation; approved remediation to validation |
| Four verbs | analyse, recommend, decide, execute |
| Four outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Irreversible action | live network change; human approves |
| Code implements today | health, device-row read, synthetic summary; none of the four flows end to end |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/prd/prd.md`
2. `06-telecom-service-network-incident-ops/docs/prd/traceability.md`

## Completion gate
PASS when every requirement has a YAML id and a named test, the PRD and the YAML do not disagree on any term, and the demo flow is picked with a reason. CONDITIONAL PASS when one acceptance test is "planned" with the stage that writes it. BLOCKED when any requirement has no YAML id or the PRD defines a term on its own.

## Lifecycle linkage
Cite ai-qualification.md, the semantic-layer files by id, and the Phase 4 and 5 design files. Stage S06R reviews this PRD before S07. Stage S07 builds only what this PRD names. Stage S08 gives the same PRD to the second model.

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
| `prd.md` | Header. Eight sections. Demo flow with reason. Routes implemented and not implemented. Every requirement has an id, a YAML id, and a test. |
| `traceability.md` | Header. Requirement → YAML id → test → design file. |

## Done test

Pick any requirement. Its YAML id resolves to an item in `semantic-layer/`. Its test name exists or is marked planned with a stage.
