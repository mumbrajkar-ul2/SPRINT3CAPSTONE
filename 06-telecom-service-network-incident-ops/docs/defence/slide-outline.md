# Slide outline: walkthrough of D1 to D8

| Field | Value |
|---|---|
| Stage | S10. Presentation and defence (`Project_Intent.md` section 3.2, row "Presentation"). |
| Date / version | 2026-10-14, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | PASS. The outline has 10 slides: an opening, one slide for each deliverable D1 to D8, and a closing. Each slide has a title that states a fact, three bullets and the file to show. Every bullet comes from a file named on the slide or in `docs/defence/defence-answers.md`. |
| Evidence sources | `docs/defence/defence-answers.md`; `PRODUCTION_EVIDENCE_PACK.md`; `docs/01-discovery/component-inventory.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/data-quality-baseline.md`; `semantic-layer/README.md`; `docs/prd/prd.md` v1.9; `docs/demo/demo-script.md`; `docs/demo/evidence.md`; `docs/model-comparison/app-comparison.md`; `docs/16-evidence-pack/hash-recheck.md`; `docs/15-readiness/go-no-go-decision.md`; `docs/15-readiness/risk-owner-table.md`; `docs/00-contract/operating-contract.md`; `../Project_Intent.md` sections 2.7, 3.2 and 3.3; `../playbook/STATUS.md`. |
| Assumptions | (1) The talk lasts about 30 minutes, so each slide takes about 3 minutes. This length is an Assumption, because the packet gives none. (2) The presenter shows the named file on screen and does not read it aloud. (3) Every number on a slide keeps the label that the source file gives it. A label is written next to the number. (4) The model is the stand-in `local-sim-v1` on every slide that shows a model answer (condition C1 of `docs/15-readiness/go-no-go-decision.md`). |
| Unresolved issues | Seven PRD gaps are open (G-1 to G-4, G-6, G-8, G-9). 41 of 63 open risks have a PROPOSED owner. The slides use the S09 numbers and do not recount them, except where `docs/defence/defence-answers.md` says "rechecked in S10". |
| Residual risks | A slide shows a count that a later test run changes. The counts come from the final evidence run on commit `ec56a34` (2026-10-14T06:32:03Z). The old shared database password text sits in `../transcript/chat_transcript.md`. No slide shows it, and the presenter must not open that file on screen (`S09-5`). |

Paths are relative to the project folder (`06-telecom-service-network-incident-ops`) unless they start with `../`.

**Number labels.** REAL is a count or a measure from a run or a file. PRECOMPUTED is copied from a stored report. SIMULATED comes from the stand-in model. EDUCATIONAL is a teaching figure and not money.

## Slide order

| Slide | Part | Defence questions it supports |
|---|---|---|
| 1 | Opening: the brief and the irreversible action | 1, 3 |
| 2 | D1. Repo discovery dossier | 2 |
| 3 | D2. Behavioural baseline | 6 |
| 4 | D3. Semantic layer | 9 |
| 5 | D4. Spine controls | 3, 4, 8 |
| 6 | D5. PRD | 1, 2 |
| 7 | D6. Working application and demo | 1, 5, 7, 8 |
| 8 | D7. Second-model test and app comparison | 9 |
| 9 | D8. Production evidence pack | 10 |
| 10 | Closing: the decision | 10 |

---

## Slide 1. Opening: a live network change is the one action nobody can undo, and no route in the app does it

- **The brief.** The inherited program had 3 routes: `GET /health`, `GET /records/{id}` and `POST /ai/summarize/{id}`. The summarize route had no role check and returned `guardrail_status` `not_enforced` (`docs/02-baseline/defect-list.md` K08, F12, F16).
- **The irreversible action.** It is a live network change: a configuration push, an automated fix, a provisioning change, or an incident close that hides a real outage. A named person with the desk job `network_engineer` must approve it with a stored approval id (`docs/00-contract/operating-contract.md` row 9).
- **The result.** The governed app has 9 routes (REAL) and no route can reach EXECUTE (`policy/tests/test_policy_python.py::test_no_route_can_execute`). The decision at the end is no-go for production.

**File to show:** `docs/00-contract/operating-contract.md` (the table row for question 9).

## Slide 2. D1: the discovery dossier mapped 55 components, and none has a named owner

- **What D1 holds.** Six documents: current-state architecture, component inventory, business flow reconstruction, data and integration map, AI subsystem discovery and the brownfield risk register. Every row cites a file, a test, a log or a replay result (`../playbook/STATUS.md` row S01).
- **The count.** The component inventory has 55 rows (REAL). The owner is Unknown on all 55, because the repo names no component owner (`docs/01-discovery/component-inventory.md`).
- **The four flows.** The dossier reconstructs the four business flows. At the start the running program read `devices.csv` only, and no route read orders, circuits, alarms or incidents (`../Project_Intent.md` section 2.7; `docs/01-discovery/business-flow-reconstruction.md`).

**File to show:** `docs/01-discovery/component-inventory.md`.

## Slide 3. D2: the baseline separates 8 behaviours to keep from 23 defects to fix

- **Two lists.** The Keep list has K01 to K08 and the Fix list has F01 to F23 (REAL). The two lists share no row (`docs/02-baseline/defect-list.md`).
- **One defect in detail.** F01: a request for a missing device id returned the first device row, `REC-0001`, with HTTP 200. A test locked that behaviour at S02, and S07 replaced it with a 404 after the PRD asked for it (`docs/demo/evidence.md` section 5).
- **The data.** The profile confirmed 19 of 24 seeded quality labels and did not find 5 (REAL). 166 alarm rows have a last seen time earlier than the first seen time (REAL, F08) (`docs/02-baseline/data-quality-baseline.md`).

**File to show:** `docs/02-baseline/defect-list.md` (the Fix table, row F01).

## Slide 4. D3: one semantic layer of 765 ids defines every word that both apps use

- **What it holds.** Seven YAML files: entities, relationships, status taxonomy, business rules, metrics, access semantics and AI context policy. Version 1.2.1 defines 765 ids and 281 glossary rows (REAL) (`docs/demo/evidence.md` section 6).
- **How it is checked.** A schema validates the YAML. `build.py --check` passes, and 41 semantic-layer tests pass (REAL) (`semantic-layer/README.md`; `evidence/junit-semantic-layer.xml`).
- **Why it matters later.** The second model got these same files. 36 of 36 hashes still match after S08 and after S09 (REAL) (`docs/16-evidence-pack/hash-recheck.md`).

**File to show:** `semantic-layer/README.md`.

## Slide 5. D4: two copies of the policy agree, and the AI path holds a case for a person when it fails

- **Policy.** 87 Python policy tests pass with 0 skipped and 32 of 32 Rego tests pass (REAL). A test shows the two copies agree on access (`policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access`).
- **AI guardrails.** 51 guardrail tests pass (REAL). A timeout returns HOLD_FOR_REVIEW with no summary. A retry of the summarize route costs one model call and one audit row, and 354 alarm rows give 350 new, 3 repeats and 1 held aside (REAL) (`tests/reliability/test_drills.py`).
- **What is red.** The GitHub run on commit `ec56a34` ended red. Lint (30 findings), the dependency scan (9 advisory ids) and the static scan (40 findings) exit 1 on real findings, and none is switched off (REAL) (`docs/16-evidence-pack/ci-run-38521594275.txt`).

**File to show:** `PRODUCTION_EVIDENCE_PACK.md` (sections "Policy-as-Code Evidence" and "AI Security and Guardrails Evidence").

## Slide 6. D5: the PRD v1.9 holds 73 requirements, and each one names a YAML id and a test

- **The demo flow.** Topology lookup, then an AI recommendation, then a human decision. Alarm-storm deduplication is the first step (`docs/prd/prd.md` section 4).
- **The count.** 73 requirements: 29 tests exist, 43 are planned and 1 is deferred (REAL) (`docs/prd/prd.md` header). The last full review (S06R) ran against v1.8 (`docs/prd/prd-review.md`).
- **What is not built.** 12 rows in the "Not built" table, among them order provisioning, remediation validation and any EXECUTE route. Each row has a reason (`docs/prd/prd.md` section 9).

**File to show:** `docs/prd/prd.md` (section 9, the "Not built" table).

## Slide 7. D6: the demo takes one alarm storm to one human decision in five steps

- **The five steps.** Read storm `STO-00002`, look up device `DEV-00002`, ask for a recommendation, press Approve (yes), read the audit chain. A yes stores an approval id that starts with `APR-`. The approval changes no device (`docs/demo/demo-script.md` section 3).
- **The order.** The audit row is written before the approval is stored. The variants show a timeout (HOLD_FOR_REVIEW, no summary, decision returns 404), a missing device (`STO-00001`, BLOCK), a stale device (`STO-00005`, BLOCK) and a no (`docs/demo/demo-script.md` section 4).
- **The labels.** The model is the stand-in `local-sim-v1`. Latency is SIMULATED and tokens are EDUCATIONAL. The role is a word the caller types (`docs/demo/evidence.md` section 4).

**File to show:** `docs/demo/demo-script.md` (section 3, the steps table).

## Slide 8. D7: the second model got the same 36 files, and the two apps differ in 16 places

- **Same input.** 36 of 36 hashes match before and after (REAL). The second model (GPT-5.6 Sol) built `apps/api_model_b/`. Both apps return identical bodies for 351 device reads and 352 storm reads, and agree in 108 of 108 role-and-route cells (REAL) (`docs/model-comparison/app-comparison.md` section 1).
- **Differences.** 16 differences: 3 listed gaps and 13 unlisted (REAL). The second app passes 378 of 469 tests and fails 89 (35 differences, 54 internal names). 78 tests first failed to load. 24 passing dedupe tests run a copy of the first app's file (REAL) (`docs/model-comparison/second-model-load-fix.md`).
- **Verdict.** CONDITIONAL PASS. Meanings did not drift in outcome words, failure ids, audit keys, role grants and data rows. They drifted in rare inputs and list contents. The second app keeps 1927 of 2000 audit rows when 8 threads write (REAL) (`docs/model-comparison/app-comparison.md` section 7).

**File to show:** `docs/model-comparison/app-comparison.md` (section 5, the difference register).

## Slide 9. D8: the evidence pack has 16 sections and every path in it exists

- **Contents.** The pack has the 15 sections of the template plus a second-model section. Each claim carries a label, a file or a test, and a line on what is still unproven (`PRODUCTION_EVIDENCE_PACK.md`).
- **The numbers.** 469 tests pass with 0 skipped in the final run. All 150 paths named in the pack exist (REAL) (`evidence/junit-tests.xml`; `docs/16-evidence-pack/path-check.md`).
- **The audit log.** The final run added 6 rows to `logs/audit.log`. The file went from 308 to 314 lines and was restored to 308 lines (REAL) (`docs/16-evidence-pack/audit-log-record.md`).

**File to show:** `PRODUCTION_EVIDENCE_PACK.md` (the Executive summary).

## Slide 10. Closing: the decision is no-go for production and go for the lab demo under seven conditions

- **The decision.** No-go for production. Go for the lab demo and this defence under conditions C1 to C7 (`docs/15-readiness/go-no-go-decision.md` section 2).
- **The risk.** 63 risks are open (REAL). 22 have a named acceptor. 41 have a PROPOSED owner who has not agreed in writing: 38 for Team-Force and 3 for Mangesh (FDE) (`docs/15-readiness/risk-owner-table.md`).
- **The gate.** The S09 gate is CONDITIONAL PASS, and this defence is PASS. All ten answers cite a file or a test and name what is still unproven (`docs/defence/defence-answers.md`).

**File to show:** `docs/15-readiness/go-no-go-decision.md` (section 1).

---

## Coverage check

| Deliverable | Slide | File shown |
|---|---|---|
| D1. Repo discovery dossier | 2 | `docs/01-discovery/component-inventory.md` |
| D2. Behavioural baseline | 3 | `docs/02-baseline/defect-list.md` |
| D3. Semantic layer | 4 | `semantic-layer/README.md` |
| D4. Spine controls | 5 | `PRODUCTION_EVIDENCE_PACK.md` |
| D5. PRD | 6 | `docs/prd/prd.md` |
| D6. Working application and demo | 7 | `docs/demo/demo-script.md` |
| D7. Second-model test and app comparison | 8 | `docs/model-comparison/app-comparison.md` |
| D8. Production evidence pack | 9 | `PRODUCTION_EVIDENCE_PACK.md` |
| Opening | 1 | `docs/00-contract/operating-contract.md` |
| Closing | 10 | `docs/15-readiness/go-no-go-decision.md` |

Check: 8 deliverable slides + 1 opening + 1 closing = 10 slides.

## Lifecycle linkage

The answers behind each slide are in `docs/defence/defence-answers.md`. The proof for each number is in `PRODUCTION_EVIDENCE_PACK.md`. S10 is the last stage.
