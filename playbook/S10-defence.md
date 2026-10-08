# S10 — Presentation and defence

Phase 10 in `Execution Plan.md`. Answers to the ten defence questions, each with a file or test pointer, and a slide outline for the D1 to D8 walkthrough.

## Inputs

- `Project_Intent.md` (section 3.3)
- `06-telecom-service-network-incident-ops/PRODUCTION_EVIDENCE_PACK.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/go-no-go-decision.md`
- `06-telecom-service-network-incident-ops/docs/demo/demo-script.md`
- `06-telecom-service-network-incident-ops/docs/demo/evidence.md`
- `06-telecom-service-network-incident-ops/docs/14-audit/evidence.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/idempotency-plan.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/degraded-mode-design.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/app-comparison.md`
- `06-telecom-service-network-incident-ops/docs/prd/prd.md`

## Prompt

```text
# Stage S10 — Presentation and defence

## Objective
Answer the ten defence questions in Project_Intent.md 3.3 with evidence, not opinion. Write the slide outline for a walkthrough of D1 to D8.

## Scope
Include: the evidence pack and every artifact it points to.
Exclude: any new claim not already in an artifact. If a question cannot be answered from an artifact, the answer says so and names what is missing.

## Required analysis
For each of the ten questions write: the answer in plain speech (three to six sentences); the evidence (file path, test name, or audit row); what is still unproven.
1. What event did you route, and which facts existed at decision time? (demo-script.md, prd.md data section)
2. Which of the four flows did the demo run, and which routes still do not implement that flow? (prd.md routes-not-implemented)
3. What action cannot be undone, and where does a human approve it? (operating-contract.md, approval-workflow.md, /approvals route test)
4. What would a retry duplicate, and how did you prove the count? (idempotency-plan.md, test_drills.py duplicate replay, /alarms/storms response)
5. Rebuild one case: actor, request, data used, model and version, policy result, approval, final action, trace id, and what you still cannot prove. (docs/14-audit/evidence.md, /audit route output)
6. Which inherited gap did you leave visible until a spec closed it? (defect-list.md, prd.md inherited gaps, deferred-work-list.md)
7. How does a person contest an AI recommendation? (approval-workflow.md, /approvals reject path)
8. What still runs if the AI gateway times out? (degraded-mode-design.md, timeout test)
9. How did the second model use the same semantic layer, and what changed in the second app? (app-comparison.md, yaml hashes)
10. Is the system production-ready? What risk is accepted, and who owns it? (go-no-go-decision.md, risk-owner-table.md)
Slide outline: one slide per deliverable D1 to D8, plus opening (the brief and the irreversible action) and closing (the decision). Per slide: title as a fact, three bullets, the file to show.

## Evidence rules
- Every answer names at least one file or test.
- Label claims: Verified Fact, Inference, Assumption, Unknown.
- Every number carries its honesty label.

## Constraints and guardrails
- Plain speech. Titles state the fact, not a slogan.
- No answer may cite an opinion as proof.
- Redact secrets.
- Each doc starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/defence/defence-answers.md`
2. `06-telecom-service-network-incident-ops/docs/defence/slide-outline.md`

## Completion gate
PASS when every answer cites evidence and names its unproven part, and the slide outline covers D1 to D8. CONDITIONAL PASS when one answer is "not proven" with the missing artifact named. BLOCKED when any answer has no file or test pointer.

## Lifecycle linkage
Cite PRODUCTION_EVIDENCE_PACK.md and the files listed per question. This is the last stage.

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
| `defence-answers.md` | Header. Ten answers, each with evidence and unproven part. |
| `slide-outline.md` | Header. Ten slides: opening, D1 to D8, closing. Fact titles. File per slide. |

## Done test

Read answer 5 aloud. Every item in the list (actor, request, data, model and version, policy, approval, final action, trace id, unproven) has a value or "cannot prove" with a reason.
