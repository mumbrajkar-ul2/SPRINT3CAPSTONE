# S06 — Product Requirements Document (product path step 2, D5)

Phase 6 in `Execution Plan.md`. The PRD is written from the semantic layer at its current version and the Phase 4 and 5 designs. The current version is the `version:` string in `semantic-layer/README.md`. It is `1.1.1` after ADR 0002, which changed one YAML sentence after S05R. Both the first app and the second model build from it.

## Inputs

- `Project_Intent.md` (sections 3.1, 5.2, 5.3, 6.3)
- `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf` (product path)
- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree, at the current version; read the version from `semantic-layer/README.md`)
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md` (the S05R record; its header also names the current version)
- `06-telecom-service-network-incident-ops/docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` (the owner's decisions on the deferred and PROPOSED items)
- `06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md` (each decision with its reason)
- `06-telecom-service-network-incident-ops/docs/04-secrets/rotation-log.md` (the rotation log; it has no entries)
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
Include: the semantic layer; the S2Q table; the Phase 4 and 5 designs listed as inputs; ADR 0002 and `S05R_Decisions_Taken.md`.
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
4. Routes: the list the app will implement (/health, /records/{id} with 404, /alarms/storms/{storm_batch_id}, /ai/recommend/{id}, /approvals/{id}, /audit/{correlation_id}). `GET /health`, `GET /records/{id}`, `POST /ai/summarize/{id}`, and `GET /audit/{correlation_id}` exist in `apps/api/main.py` today. POST /ai/summarize/{id} stays. S04-09 hardened it. The routes `/ai/recommend`, `/approvals/{id}`, and `/alarms/storms/{storm_batch_id}` do not exist yet. /ai/recommend is a new route. The demo page calls /ai/recommend. The list the app will not implement, each with a reason. When the demo stays the recommended flow, two sentences are required: order provisioning stays unimplemented because no route reads service_orders.csv or circuits.csv; remediation validation stays unimplemented because this packet does not apply a live change, so there is no result to check. If the PRD picks the order flow or the remediation flow as the demo instead, say why, and move that flow into the implement list. Every flow is either implemented or named, with a reason, on the will-not-implement list. No EXECUTE route unless all four gates exist; if listed, it is reversible and validated.
5. Traceability: a table requirement id to YAML id to acceptance test to Phase 4 design file.
6. Decisions and limits. Read ADR 0002 and `S05R_Decisions_Taken.md`. The PRD states each of these, with its YAML id where one exists:
   - D-07: whether a login system is in scope. Today the caller identity is a claim from a header, and `status.code.cannot_prove.caller_identity` says so. Decide the scope here, or write it as Unknown with owner Team-Force.
   - D-03, D-06, D-08: decided in ADR 0002 and built in S07. The approval record gets `decision` (yes or no) and `approver` (a persona id). The audit row gets `record_id` as a 16th key. A short PROPOSED list of command phrases is written. Mark each as a planned requirement with stage S07. S07 adds the YAML ids under a new ADR.
   - D-05: the audit log mixes test rows and real rows. Final action is built at S07. The other three facts stay deferred.
   - D-08: a short phrase list misses some phrases.
   - D-12: production would keep rotation records in a secret manager. The lab uses `docs/04-secrets/rotation-log.md`, which has no entries.
   - P-02: four scopes need data that the CSV files do not hold.
   - P-10: three rules have `enforced_today: false` (`rule.policy_copies_agree`, `rule.repeat_event_is_one_event`, `rule.order_attempt_same_retry_is_one_attempt`).
   - The 13 deferred items (D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20) listed as open items, each with its trigger. D-07 is decided in ADR 0003 and is not on this list.
   Every number the PRD cites that is in ADR 0002 keeps the word PROPOSED, with owner Team-Force, unless the table says it is decided.
For each requirement: id, text, YAML id, test, source design.

## Evidence rules
- Every requirement cites at least one YAML id.
- Label other claims: Verified Fact, Inference, Assumption, Unknown.
- Every displayed number in the workflow carries REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.

## Constraints and guardrails
- Plain speech. A new reader must know what to picture after one pass.
- Do not define a term. Use the glossary. If a needed term is missing, stop. Write it as an "Open question for S03:" line in the PRD draft, rerun S05R so the term enters the YAML with a source list, then record the change in a new ADR under `docs/ADR/`, then continue. The PRD does not define the term itself.
- Write the semantic-layer version string into the PRD header table under Evidence sources. Read it from `semantic-layer/README.md`. It must equal the current version named in the header of `docs/02-baseline/semantic-layer-revision.md` and in the newest ADR that changed the YAML. Stop if they differ. Every YAML id in the PRD resolves at that version.
- No invented cutoff or threshold. PROPOSED with owner only.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Four flows | order to provisioning; alarm storm to incident; topology to AI recommendation; approved remediation to validation |
| Four verbs | analyse, recommend, decide, execute |
| Four outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Irreversible action | live network change; human approves |
| Code implements today | health, device-row read, synthetic summary, audit case read (`GET /audit/{correlation_id}`); none of the four flows end to end |
| Audit row | 15 keys, written by `apps/api/services/audit.py` |
| Access rows | 35 allow rows, TA-01 to TA-35, in `policy/opa/policy_data.json` |
| Audit action words (S05-14) | `audit.read`, `audit.not_found`, `audit.id_refused` (new); `policy.deny` is reused. The route is `GET /audit/{correlation_id}`. The id limit is 128 characters. |
| Semantic layer version | the `version:` string in `semantic-layer/README.md` (`1.1.1` after ADR 0002) |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/prd/prd.md`
2. `06-telecom-service-network-incident-ops/docs/prd/traceability.md`

## Completion gate
PASS when every requirement has a YAML id and a named test, the PRD and the YAML do not disagree on any term, the demo flow is picked with a reason, and the two required "will not implement" sentences are present. CONDITIONAL PASS when one acceptance test is "planned" with the stage that writes it. BLOCKED when any requirement has no YAML id or the PRD defines a term on its own.

## Lifecycle linkage
Cite ai-qualification.md, `semantic-layer/README.md` and semantic-layer-revision.md for the version, ADR 0002 for the decisions, the semantic-layer files by id, and the Phase 4 and 5 design files. ADR 0002 is the last YAML change before this PRD. Any later YAML change needs a new ADR, and the version in the PRD header must then change with it. Stage S06R reviews this PRD before S07. When S06R has a FAIL row, stage S06F applies its "Fixes required" list, then S06R runs again. Stage S07 builds only what this PRD names. Stage S08 gives the same PRD and the same YAML version to the second model.

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
| `prd.md` | Header, with the current semantic-layer version (from `semantic-layer/README.md`) under Evidence sources. Eight sections. Demo flow with reason. Routes implemented and not implemented. The order-provisioning sentence and the remediation-validation sentence, each with its reason. POST /ai/summarize kept. Every requirement has an id, a YAML id, and a test. |
| `traceability.md` | Header. Requirement → YAML id → test → design file. |

## Done test

Pick any requirement. Its YAML id resolves to an item in `semantic-layer/`. Its test name exists or is marked planned with a stage. The PRD states both required limits: order provisioning is not built, and remediation validation is not built, each with the reason above.
