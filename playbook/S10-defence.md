# S10 — Presentation and defence

Phase 10 in `Execution Plan.md`. Answers to the ten defence questions, each with a file or test pointer, and a slide outline for the D1 to D8 walkthrough.

## Inputs

- `Project_Intent.md` (section 3.3)
- `06-telecom-service-network-incident-ops/PRODUCTION_EVIDENCE_PACK.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/go-no-go-decision.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/risk-owner-table.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/residual-risk-register.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/readiness-checklist.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/operating-contract-check.md`
- `06-telecom-service-network-incident-ops/docs/15-readiness/deferred-work-list.md`
- `06-telecom-service-network-incident-ops/docs/16-evidence-pack/hash-recheck.md`
- `06-telecom-service-network-incident-ops/docs/16-evidence-pack/audit-log-record.md`
- `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md`
- `06-telecom-service-network-incident-ops/docs/demo/demo-script.md`
- `06-telecom-service-network-incident-ops/docs/demo/evidence.md`
- `06-telecom-service-network-incident-ops/docs/14-audit/evidence.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/idempotency-plan.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/degraded-mode-design.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/app-comparison.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/second-model-run-log.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/second-model-load-fix.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/yaml-hashes-before.md`
- `06-telecom-service-network-incident-ops/docs/model-comparison/yaml-hashes-after.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
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
2. Which of the four flows did the demo run, and which routes still do not implement that flow? (prd.md section 9, the "Not built" table)
3. What action cannot be undone, and where does a human approve it? (operating-contract.md, approval-workflow.md, /approvals route test)
4. What would a retry duplicate, and how did you prove the count? (idempotency-plan.md, test_drills.py duplicate replay, /alarms/storms response)
5. Rebuild one case: actor, request, data used, model and version, policy result, approval, final action, trace id, and what you still cannot prove. (docs/14-audit/evidence.md, /audit route output). `playbook/STATUS.md` has no row for S05-14, so cite `docs/14-audit/evidence.md` for that stage and not a STATUS row. State that `logs/audit.log` holds 308 lines after the S09 restore (`docs/16-evidence-pack/audit-log-record.md`).
6. Which inherited gap did you leave visible until a spec closed it? (docs/02-baseline/defect-list.md, the open PRD gaps in docs/demo/evidence.md section 7, docs/15-readiness/deferred-work-list.md). Seven PRD gaps are open (G-1 to G-4, G-6, G-8, G-9). ADR 0006 closed G-5 and G-7. The deferred-work list holds 39 items.
7. How does a person contest an AI recommendation? (approval-workflow.md, /approvals reject path)
8. What still runs if the AI gateway times out? (degraded-mode-design.md, timeout test)
9. How did the second model use the same semantic layer, and what changed in the second app? (app-comparison.md, yaml-hashes-before.md and yaml-hashes-after.md, second-model-run-log.md, second-model-load-fix.md). The answer states the hash result (36 of 36 match, re-checked in S09 in `docs/16-evidence-pack/hash-recheck.md`), the 16 differences (3 listed gaps, 13 unlisted), that 78 tests of the second app first failed to load and were fixed, that the 24 dedupe tests use a copied file, the test counts (first app 469 pass with `opa` installed; second app 378 pass, 89 fail of which 35 are differences and 54 are internal names, 2 skip), and the S08 Part 3 verdict.
10. Is the system production-ready? What risk is accepted, and who owns it? (docs/15-readiness/go-no-go-decision.md, docs/15-readiness/risk-owner-table.md). The answer states the S09 decision: no-go for production, go for the lab demo under seven conditions (C1 to C7, `go-no-go-decision.md` section 2). It states that 63 risks are open, 22 have a named acceptor and 41 have a PROPOSED owner (`risk-owner-table.md` section 3), and that the S09 gate is CONDITIONAL PASS.
Slide outline: one slide per deliverable D1 to D8, plus opening (the brief and the irreversible action) and closing (the decision). Per slide: title as a fact, three bullets, the file to show.

## Evidence rules
- Every answer names at least one file or test.
- Label claims: Verified Fact, Inference, Assumption, Unknown.
- Every number carries its honesty label.

## Constraints and guardrails
- Plain speech. Titles state the fact, not a slogan.
- No answer may cite an opinion as proof.
- Redact secrets. The old shared database password text sits in `transcript/chat_transcript.md`. Do not copy it into any answer or slide (risk `S09-5`).
- Each doc starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/defence/defence-answers.md`
2. `06-telecom-service-network-incident-ops/docs/defence/slide-outline.md`

## Completion gate
PASS when every answer cites evidence and names its unproven part, and the slide outline covers D1 to D8. CONDITIONAL PASS when one answer is "not proven" with the missing artifact named. BLOCKED when any answer has no file or test pointer. A PASS closes item 11 of the `Project_Intent.md` 6.3 checklist ("you can answer the section 3.3 questions"), which `docs/15-readiness/readiness-checklist.md` marks not ready. Report that change in the final response.

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
