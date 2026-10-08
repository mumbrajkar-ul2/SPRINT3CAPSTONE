# S03R — Semantic layer review

Review gate after Phase 3. Run this in a fresh chat so the reviewer has not seen the drafting conversation. A FAIL row blocks Phase 4.

## Inputs

- `Semantic_Layer_capture.pdf`
- `Project_Intent.md` (section 6.2)
- `06-telecom-service-network-incident-ops/semantic-layer/` (the whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/data-quality-baseline.md`
- `playbook/README.md` (the failure list)

## Prompt

```text
# Stage S03R — Semantic layer review

## Objective
Review `semantic-layer/` as an independent reader. Decide whether it is fit to be the single source of truth for the PRD, the policies, the app, and a second model. Do not fix anything. Report.

## Scope
Include: every file under `semantic-layer/`; the S2Q table; the data-quality baseline.
Exclude: any edit to the tree. If you find a problem, write it as a FAIL row with the fix needed.

## Required analysis
Write one row per check. Each row: check id, PASS / FAIL / NOT APPLICABLE, file and line or id cited, one-sentence reason.
Checks:
R1. The tree matches the capture PDF exactly, plus only generated/ and build.py, and the README says why those two exist.
R2. Every YAML item has a source list or proposed: true with an owner.
R3. Every status word that appears in the CSVs (per data-quality-baseline.md) appears in status-taxonomy.yaml, or is listed as a collision.
R4. The collisions block names gold/bronze severity, status words in hostname and vendor, REC-0001 reused, and clinician.
R5. business-rules.yaml holds the six required rules, each with an id.
R6. access-semantics.yaml covers all seven personas and lists clinician under removed_roles.
R7. ai-context-policy.yaml forbids mgmt_ip and credential_profile, names the four outcomes, names fail-to-person, and copies agency and approval point per AI use from ai-qualification.md with no change in meaning.
R8. No AI use in the YAML has execute agency.
R9. The glossary defines every term the YAML uses, in everyday words, and the meanings agree.
R10. The schema validates every YAML file. Run the tests and build; paste the output.
R11. Deleting generated/ and running build.py reproduces identical files.
R12. No target number, cutoff, or threshold appears without PROPOSED and an owner.
R13. No password, key, or token value appears anywhere in the tree.
R14. Failure-list check from playbook/README.md: items 1 to 8, one row each.
R15. Plain speech: pick three glossary entries at random and state whether a reader new to telecom would know what to picture.

## Evidence rules
- Every row cites a file and an id or line.
- Label the reason: Verified Fact (you ran or read it) or Inference.

## Constraints and guardrails
- Do not edit any file under semantic-layer/.
- Plain speech. Short sentences.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-review.md` — the review table, the test and build output, and a "Fixes required" list for every FAIL.

## Completion gate
PASS when no row is FAIL. CONDITIONAL PASS when every FAIL is in R12 or R15 only and each has a one-line fix. BLOCKED when any of R1, R5, R7, R8, R10, R11, R13 is FAIL.

## Lifecycle linkage
Cite semantic-layer/ files by path and id. Stage S04 (every challenge) may start only when this review is PASS or CONDITIONAL PASS with fixes applied. Stage S08 gives the second model the tree that passed this review.

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
| `docs/02-baseline/semantic-layer-review.md` | Header. Fifteen check rows plus eight failure-list rows. Test and build output pasted. "Fixes required" list. |

## Done test

Every row has a file citation. If any row is FAIL, go back to S03 with the fix list, then re-run S03R. Do not start S04 until this file says PASS or CONDITIONAL PASS with fixes applied.
