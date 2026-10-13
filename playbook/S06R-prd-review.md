# S06R — PRD review

Review gate after Phase 6. Run this in a fresh chat so the reviewer has not seen the drafting conversation. A FAIL row blocks Phase 7. The reviewer reads the ADRs and the risk file as context. The reviewer does not edit them.

## Inputs

- `06-telecom-service-network-incident-ops/docs/prd/prd.md`
- `06-telecom-service-network-incident-ops/docs/prd/traceability.md`
- `06-telecom-service-network-incident-ops/docs/prd/Risk Management.md`
- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-review.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md`
- `06-telecom-service-network-incident-ops/docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`
- `06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md`
- `06-telecom-service-network-incident-ops/docs/ADR/0004-defer-rq-31-answer-store.md`
- `06-telecom-service-network-incident-ops/docs/prd/prd-fixes.md` (context only: it records what each fix round changed. Judge the PRD on its own text.)
- `06-telecom-service-network-incident-ops/docs/12-finops/optimization-backlog.md`
- `06-telecom-service-network-incident-ops/docs/12-finops/evidence.md` (report any file that disagrees with the PRD)
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md` (line 76 says "A rejection writes no approval id". The PRD must say the same.)
- `Project_Acronyms.md`
- `Project_Intent.md` (Appendix B, the four honesty labels)
- `playbook/README.md` (the failure list)

## Prompt

```text
# Stage S06R — PRD review

## Objective
Review the PRD as an independent reader. Decide whether a builder, human or model, could build the governed application from the PRD plus the semantic layer with no other source. Do not fix anything. Report.

## Scope
Include: prd.md; traceability.md; Risk Management.md; the semantic layer; the S2Q table; ADR 0002; ADR 0003; ADR 0004; prd-fixes.md (context only); optimization-backlog.md; evidence.md; approval-workflow.md; Project_Acronyms.md; S05R_Decisions_Taken.md; semantic-layer-revision.md; Project_Intent.md Appendix B.
Exclude: any edit to prd.md, traceability.md, Risk Management.md, any ADR, or any file under semantic-layer/. If you find a problem, write it as a FAIL row with the fix needed.

## Required analysis
Write one row per check. Each row: check id, PASS / FAIL / NOT APPLICABLE, file and line or id cited, one-sentence reason.
Checks:
P1. Every requirement has a requirement id, a YAML id that resolves in semantic-layer/, and a test name. Read the PRD version from the Date / version row of the `prd.md` header, and record it. The set is RQ-01 to RQ-73. RQ-68 to RQ-73 must be present. A planned S07 test name still counts. A deferred test name (RQ-31, ADR 0004) still counts.
P2. Every term and status word in the PRD appears in glossary.md or a YAML file with the same meaning. List any that do not. Two exceptions, and only these two, are PASS when they are listed and not defined: (1) a word on an "Open question for S03:" line in the PRD, if the PRD does not invent the missing id; (2) the four honesty labels REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL as Project_Intent.md Appendix B writes them.
P3. The AI limits section quotes pick, agency, and approval point from ai-qualification.md with no change in meaning.
P4. No AI use has execute agency. No EXECUTE route is listed without the four gates (policy, approval, audit before state change, reversible and validated).
P5. The demo flow is named with a reason, and its steps each carry a verb and a persona.
P6. The routes-not-implemented list exists and gives a reason per route. When the demo is topology lookup plus alarm dedupe, the list includes both sentences: order provisioning stays unimplemented because no route reads service_orders.csv or circuits.csv; remediation validation stays unimplemented because this packet does not apply a live change. If the PRD picked another demo flow, that flow is on the implement list and the reason is written. The implement list includes GET /ready (RQ-73). GET /records/{id} names the no-header 403 (RQ-68). A login or token route is on the will-not-implement list (D-07).
P7. Every displayed number carries an honesty label.
P8. No cutoff, threshold, or target appears without PROPOSED and an owner.
P9. The acceptance checks cover: 404 on missing id; clinician denied; HOLD_FOR_REVIEW on timeout with no summary; audit row before state change; one case rebuilt by correlation_id.
P10. Inherited gaps the app leaves visible are listed. POST /ai/summarize/{id} is kept. /ai/recommend/{id} is the new route the demo page calls. GET /ready is on the implement list (RQ-73). GET /records/{id} names the no-header 403 (RQ-68). A login or token route is on the will-not-implement list (D-07, ADR 0003). No qualify, provision, retry, rollback, or fix-validation route is required.
P11. Plain speech: pick three requirements at random and state whether a reader new to telecom knows what to picture.
P12. Failure-list check from playbook/README.md: items 1 to 8, one row each.
P13. The PRD header version matches semantic-layer/README.md and the header of semantic-layer-revision.md. The current version is 1.1.1. ADR 0003 added no YAML id. The PRD states ADR 0003 with the same meaning: login is out of scope; GET /records/{id} refuses a call with no header; the 300 second answer store never stores an answer that has no text (BLOCK, or HOLD_FOR_REVIEW with no sentence), and ADR 0004 defers the build of the store (RQ-31 is marked deferred, S07 does not build it). ADR 0004 added no YAML id. `prd.md` and `traceability.md` agree on 29 existing, 43 planned and 1 deferred test. Any other input file that says S07 builds the answer store is listed as a finding, with its file and line. The 13 deferred items stay deferred (D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20). D-07 is decided and is not in that list. The PRD also gives the same key names for the reply of `GET /alarms/storms/{storm_batch_id}` in every place that names them (RQ-08, RQ-62, section 15), and the same approval id rule for a yes and a no in every place that states it (RQ-32, RQ-33, section 6 step 4, section 8). See the locked facts "Storm reply keys" and "Approval id". Any place that differs is a finding, with its file and line. A key name or a rule that differs between two places of the PRD makes P13 FAIL.

## Evidence rules
- Every row cites a file and an id or line.
- Label the reason: Verified Fact (you read or resolved it) or Inference.

## Constraints and guardrails
- Do not edit prd.md, traceability.md, Risk Management.md, any ADR, or any file under semantic-layer/.
- Read the version from semantic-layer/README.md. It must equal the version in the PRD header Evidence sources and in the header of semantic-layer-revision.md. The newest ADR that changed the YAML is ADR 0002. ADR 0003 and ADR 0004 added no YAML id. Mark P13 FAIL and the stage BLOCKED if the three version strings differ.
- Plain speech. Short sentences.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Semantic layer version | 1.1.1. ADR 0002 changed one YAML sentence. ADR 0003 added no YAML id. |
| PRD version | The version in the Date / version row of the `prd.md` header. `traceability.md` must carry the same version. Requirements RQ-01 to RQ-73. |
| D-07 | Login is out of scope. The role stays a word the caller types. |
| F15 | GET /records/{id} refuses a call with no header (RQ-68). |
| RQ-31 | Deferred by ADR 0004 (2026-10-13). S07 does not build the answer store. The row stays in the PRD with its test name, marked deferred. The rules stay for a later build: it never holds an answer that has no text (BLOCK, or HOLD_FOR_REVIEW with no sentence), the lifetime is 300 seconds, and the cap is PROPOSED with no number. |
| Test counts (from PRD v1.8) | 29 exist, 43 are planned for S07, 1 is deferred (RQ-31). |
| Storm reply keys (RQ-08, PRD v1.8) | The reply of `GET /alarms/storms/{storm_batch_id}` is a JSON body with five keys: `raw_count`, `deduped_count`, `flagged_count`, `rows` and `held_aside`. Each entry of `rows` and `held_aside` has `alarm_id`, `device_id`, `dedupe_key` and `flag`. A blank `dedupe_key` goes in `held_aside`. Every other row goes in `rows`, flagged or not. The names are PROPOSED. Owner: Team-Force. They are reply keys, not YAML ids. |
| Approval id (RQ-32 and RQ-33, PRD v1.8) | Only a yes gets an approval id. For a no, `approval_id` is null in the reply, in the stored record and in the audit row. `approval-workflow.md` line 76 says "A rejection writes no approval id." |
| Honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL. Project_Intent.md Appendix B. No YAML id. |
| No EXECUTE route | The four gates are not all present. |
| Deferred items | 13 items. D-07 is decided. |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/prd/prd-review.md` — the review table and a "Fixes required" list for every FAIL.

## Completion gate
PASS when no row is FAIL. CONDITIONAL PASS when every FAIL is in P8 or P11 only and each has a one-line fix. BLOCKED when any of P1, P2, P3, P4, P9, or P13 is FAIL.

## Lifecycle linkage
Cite prd.md requirement ids, semantic-layer ids, ADR 0002, ADR 0003, ADR 0004, and the version in semantic-layer/README.md. When a row is FAIL, stage S06F applies the "Fixes required" list and this review runs again in a fresh chat. Stage S07 may start only when this review is PASS or CONDITIONAL PASS with fixes applied. Stage S08 gives the second model the PRD that passed this review.

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
| `docs/prd/prd-review.md` | Header. Thirteen check rows plus eight failure-list rows. P6 and P10 cite the two "will not implement" sentences, the kept summarize route, GET /ready, the no-header 403, and the login route off the implement list. P13 cites the version string, the three ADR 0003 decisions, the ADR 0004 deferral, the test counts (29, 43, 1), the storm reply key names and the approval id rule. "Fixes required" list. |

## Done test

Every row has a citation. If any row is FAIL, run `S06F-prd-fixes.md` with the fix list, then re-run S06R in a fresh chat. Do not start S07 until this file says PASS or CONDITIONAL PASS with fixes applied.
