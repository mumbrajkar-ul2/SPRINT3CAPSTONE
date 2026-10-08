# S06R — PRD review

Review gate after Phase 6. Run this in a fresh chat so the reviewer has not seen the drafting conversation. A FAIL row blocks Phase 7.

## Inputs

- `06-telecom-service-network-incident-ops/docs/prd/prd.md`
- `06-telecom-service-network-incident-ops/docs/prd/traceability.md`
- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-review.md`
- `playbook/README.md` (the failure list)

## Prompt

```text
# Stage S06R — PRD review

## Objective
Review the PRD as an independent reader. Decide whether a builder, human or model, could build the governed application from the PRD plus the semantic layer with no other source. Do not fix anything. Report.

## Scope
Include: prd.md; traceability.md; the semantic layer; the S2Q table.
Exclude: any edit to the PRD. If you find a problem, write it as a FAIL row with the fix needed.

## Required analysis
Write one row per check. Each row: check id, PASS / FAIL / NOT APPLICABLE, file and line or id cited, one-sentence reason.
Checks:
P1. Every requirement has a requirement id, a YAML id that resolves in semantic-layer/, and a test name.
P2. Every term and status word in the PRD appears in glossary.md or a YAML file with the same meaning. List any that do not.
P3. The AI limits section quotes pick, agency, and approval point from ai-qualification.md with no change in meaning.
P4. No AI use has execute agency. No EXECUTE route is listed without the four gates (policy, approval, audit before state change, reversible and validated).
P5. The demo flow is named with a reason, and its steps each carry a verb and a persona.
P6. The routes-not-implemented list exists and gives a reason per route.
P7. Every displayed number carries an honesty label.
P8. No cutoff, threshold, or target appears without PROPOSED and an owner.
P9. The acceptance checks cover: 404 on missing id; clinician denied; HOLD_FOR_REVIEW on timeout with no summary; audit row before state change; one case rebuilt by correlation_id.
P10. Inherited gaps the app leaves visible are listed.
P11. Plain speech: pick three requirements at random and state whether a reader new to telecom knows what to picture.
P12. Failure-list check from playbook/README.md: items 1 to 8, one row each.

## Evidence rules
- Every row cites a file and an id or line.
- Label the reason: Verified Fact (you read or resolved it) or Inference.

## Constraints and guardrails
- Do not edit prd.md or traceability.md.
- Plain speech. Short sentences.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/prd/prd-review.md` — the review table and a "Fixes required" list for every FAIL.

## Completion gate
PASS when no row is FAIL. CONDITIONAL PASS when every FAIL is in P8 or P11 only and each has a one-line fix. BLOCKED when any of P1, P3, P4, P9 is FAIL.

## Lifecycle linkage
Cite prd.md requirement ids and semantic-layer ids. Stage S07 may start only when this review is PASS or CONDITIONAL PASS with fixes applied. Stage S08 gives the second model the PRD that passed this review.

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
| `docs/prd/prd-review.md` | Header. Twelve check rows plus eight failure-list rows. "Fixes required" list. |

## Done test

Every row has a citation. If any row is FAIL, return to S06 with the fix list, then re-run S06R. Do not start S07 until this file says PASS or CONDITIONAL PASS with fixes applied.
