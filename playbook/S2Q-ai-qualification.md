# S2Q — AI versus no AI, per capability

Phase 2Q in `Execution Plan.md`. Spine stage 8. This is the decision point the trainer guidance calls the real one: for each capability, does it need a model at all, and how much may it do on its own?

## Inputs

- `Project_Intent.md` (sections 3.1, 5.2, 5.3, Appendix C)
- `06-telecom-service-network-incident-ops/docs/architecture/current-state.md`
- `06-telecom-service-network-incident-ops/docs/domain-specific-spec.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/business-flow-reconstruction.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/ai-subsystem-discovery.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
- `06-telecom-service-network-incident-ops/docs/00-contract/cost-envelope.md`

## Prompt

```text
# Stage S2Q — AI versus no AI, per capability

## Objective
Decide, for each capability in the four business flows and the three named AI products, whether it needs a model at all, which kind, and how much agency it may have. Do this before any architecture, before the semantic layer's AI policy, and before the PRD.

## Scope
Include: the four flows (order to provisioning; alarm storm to incident; topology to AI recommendation; approved remediation to validation) and the three AI products in `docs/architecture/current-state.md`.
Exclude: choosing a vendor or model name; writing code; designing routes.

## Required analysis
Build one table with these rows: order qualification; provisioning retry and rollback; alarm dedupe; alarm-to-incident correlation; topology lookup; incident summary; next-action recommendation; configuration suggestion; capacity forecast; remediation execution; remediation validation.
Columns:
1. What it does today — cite the file, or write "Not implemented".
2. Options considered — from: rules, workflow automation, deterministic code, classical ML, GenAI, agentic AI.
3. Pick.
4. Why this pick needs no more intelligence than stated. If the pick is GenAI or agentic AI, name the need that rules cannot meet (uncertainty, free text, reasoning over varied inputs, generation).
5. Agency allowed — one of: analyse, recommend, decide, execute.
6. Human approval point — the role and the moment. Required for every row with agency above analyse.
7. Reversibility and risk if wrong.
Then reconcile `docs/00-contract/cost-envelope.md`: remove or zero the AI cost rows for every capability the table assigns to rules or deterministic code. Keep the honesty labels.
Expected shape, to be confirmed against evidence, not assumed: alarm dedupe by dedupe_key and storm_batch_id is deterministic; missing-id handling is deterministic; incident summary and next-action recommendation may use GenAI with RECOMMEND_ONLY or HOLD_FOR_REVIEW; remediation execution is never AI-executed in this packet.
For each pick: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, or Unknown.
- A Verified Fact names a file path or a discovery or baseline artifact.
- Every cost number keeps its honesty label.

## Constraints and guardrails
- Plain speech. Short sentences. Everyday words.
- Do not pick AI because the project is about AI. Every GenAI or agentic pick must name a need rules cannot meet.
- No row may give execute agency to a model. The irreversible action is a live network change. A human approves it.
- No invented cutoff or threshold. Mark proposals PROPOSED with an owner.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md; read, do not re-derive)
| Fact | Value |
|---|---|
| Four flows | order to provisioning; alarm storm to incident; topology to AI recommendation; approved remediation to validation |
| Three AI products | named in docs/architecture/current-state.md |
| Four verbs | analyse, recommend, decide, execute (kept separate) |
| Four AI outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Irreversible action | live network change |
| Current execute route | none |
| Current AI | local-sim-v1 stub; prompt interpolates the whole row; guardrail_status not_enforced |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md` — the table, a short note per GenAI pick, and a list of capabilities that stay deterministic.
2. Update `06-telecom-service-network-incident-ops/docs/00-contract/cost-envelope.md` — revised rows, status changed from PROVISIONAL to REVISED-S2Q, change log at the bottom.

## Completion gate
PASS when every row has a pick and a reason, no GenAI or agentic pick lacks a stated need, and every row with agency above analyse names a human approval point. CONDITIONAL PASS when one row is Unknown because the capability is not described anywhere in the repo. BLOCKED when any row gives execute agency to a model.

## Lifecycle linkage
Cite `docs/01-discovery/business-flow-reconstruction.md`, `docs/02-baseline/defect-list.md`, and `docs/00-contract/cost-envelope.md`. Stage S03 writes `ai-context-policy.yaml` from this table. Stage S04-09 cites the row for each AI use. Stage S06 quotes the pick and agency in the PRD's AI limits section.

## Required final response
End with exactly these seven items:
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
| `docs/02-baseline/ai-qualification.md` | Header. Eleven-row table with seven columns. A note per GenAI pick naming the need rules cannot meet. A list of deterministic capabilities. |
| `docs/00-contract/cost-envelope.md` | Status REVISED-S2Q. AI cost rows removed or zeroed for rule-based capabilities. Change log. |

## Done test

No row says "execute" under agency for a model. Alarm dedupe is not GenAI. Every GenAI row has a human approval point.
