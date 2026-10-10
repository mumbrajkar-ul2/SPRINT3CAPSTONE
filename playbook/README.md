# Playbook

This folder is the how-to. `Project_Intent.md` says what the assignment is. `Execution Plan.md` says the method and the order. This folder holds one prompt per stage. After you run every stage, you have deliverables D1 to D8 and the defence answers.

Plain speak applies to every file you write.

## How to use this folder

1. Open a new Cursor chat for each stage file.
2. Attach the files listed under **Inputs** in that stage file.
3. Paste the prompt in the fenced block. Do not trim any part of it.
4. Check the output against **Expected output** and the **Done test**.
5. Read the seven-item final response the model returns. Record the stage status (PASS, CONDITIONAL PASS, or BLOCKED) in `playbook/STATUS.md`.
6. If the status is BLOCKED, clear the block before the next stage. Do not skip ahead. When S03R has a FAIL row, or the S03R rows that S05R reruns have one, you clear it by running `S03F-semantic-layer-fixes.md` and then S03R again in a fresh chat.
7. Append the turn to `transcript/chat_transcript.md`.

Each prompt is built from the eight parts in `Assignment Material/Prompt_Anatomy.pdf`: Action, Scope, Constraints, Analysis Dimensions, Evidence Rules, Artifact Generation, Completion Gate, Lifecycle Linkage. Each prompt uses the shell in `Assignment Material/Prompt Template.pdf`.

## Stage order

| Stage file | Phase in Execution Plan | What it produces | Depends on |
|---|---|---|---|
| `S00-setup-and-replay.md` | Phase 0 | `docs/00-setup/` | nothing |
| `S0B-operating-contract.md` | Phase 0B | `docs/00-contract/` | S00 |
| `S01-discovery.md` | Phase 1 (Challenge 1) | `docs/01-discovery/` | S0B |
| `S02-baseline.md` | Phase 2 (Challenge 2) | `docs/02-baseline/`, `tests/characterization/` | S01 |
| `S2Q-ai-qualification.md` | Phase 2Q | `docs/02-baseline/ai-qualification.md` | S02 |
| `S03-semantic-layer.md` | Phase 3 | `semantic-layer/` | S2Q |
| `S03R-semantic-layer-review.md` | Phase 3 review | `docs/02-baseline/semantic-layer-review.md` | S03, or S03F |
| `S03F-semantic-layer-fixes.md` | Phase 3 fix pass. Runs only when a review has a FAIL row. | `semantic-layer/` (fixed, same version), `docs/02-baseline/semantic-layer-fixes.md` | S03R with a FAIL row, or S05R with a FAIL row. Then S03R runs again. |
| `S04-03-identity.md` | Phase 4, Challenge 3 | `docs/03-identity/`, `tests/access/` | S03R PASS |
| `S04-04-secrets.md` | Phase 4, Challenge 4 | `docs/04-secrets/` | S03R PASS |
| `S04-05-iac.md` | Phase 4, Challenge 5 | `docs/05-iac/` | S03R PASS |
| `S04-06-policy.md` | Phase 4, Challenge 6 | `docs/06-policy/`, `policy/` | S04-03 |
| `S04-07-cicd.md` | Phase 4, Challenge 7 | `docs/07-cicd/`, `evidence/` | S04-04 |
| `S04-08-observability.md` | Phase 4, Challenge 8 | `docs/08-observability/` | S03R PASS |
| `S04-09-ai-guardrails.md` | Phase 4, Challenge 9 | `docs/09-ai-guardrails/`, `tests/ai/` | S04-06, S04-08 |
| `S04-10-performance.md` | Phase 4, Challenge 10 | `docs/10-performance/` | S03R PASS |
| `S04-11-reliability.md` | Phase 4, Challenge 11 | `docs/11-reliability/`, `tests/reliability/` | S04-09 |
| `S04-12-finops.md` | Phase 4, Challenge 12 | `docs/12-finops/` | S04-08 |
| `S05-13-security-validation.md` | Phase 5, Challenge 13 | `docs/13-security-validation/` | all S04 |
| `S05-14-audit-chain.md` | Phase 5, Challenge 14 | `docs/14-audit/` | S04-08, S04-09 |
| `S05R-semantic-layer-revision.md` | Phase 5R | `semantic-layer/` (revised, version raised), `docs/02-baseline/semantic-layer-revision.md` | S05-13, S05-14 |
| `S06-prd.md` | Phase 6 | `docs/prd/` | S05R PASS, or S03R PASS after an S03F round that fixed S05R rows |
| `S06R-prd-review.md` | Phase 6 review | `docs/prd/prd-review.md` | S06 |
| `S07-application-and-demo.md` | Phase 7 | `apps/api/`, `docs/demo/` | S06R PASS |
| `S08-second-model.md` | Phase 8 | `apps/api_model_b/`, `docs/model-comparison/` | S07 |
| `S09-readiness-and-evidence-pack.md` | Phase 9 | `docs/15-readiness/`, `PRODUCTION_EVIDENCE_PACK.md` | S08 |
| `S10-defence.md` | Phase 10 | `docs/defence/` | S09 |

Repo paths above sit under `06-telecom-service-network-incident-ops/`.

## Parts every prompt shares

Every prompt in this folder contains these parts in full. They are listed here once so you can see what to expect.

**Artifact header.** Every file the model writes starts with a table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

**Evidence labels.** Every claim carries one of: Verified Fact (backed by a file path, test name, log line, or replay result), Inference, Assumption, Unknown.

**Finding format.** Every material finding states: finding, evidence, impact, risk, confidence, open questions.

**Final response.** Every stage ends with seven items: stage status (PASS, CONDITIONAL PASS, BLOCKED), key findings, major risks, assumptions and unknowns, artifacts created, blocking issues, recommended next action.

**Locked facts.** Each prompt copies the rows from `Project_Intent.md` section 4.3 that the stage uses. The model reads those values. It does not re-derive them.

**Standing constraints.** No invented severity cutoff or SLA threshold. Proposed numbers are marked PROPOSED with an owner. The owner of every PROPOSED item, whether a business number or a design proposal, is Team-Force. Team-Force is the FDE team Mangesh belongs to (`docs/00-contract/operating-contract.md` row 10). A business owner named later by the packet or the trainer replaces it for business numbers. Naming the owner does not approve the item. YAML in `semantic-layer/` is the source of truth. Honesty labels REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL on every demo number. Plain speech.

**Open questions for S03.** A Phase 4 or Phase 5 design that needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks does not define it. It writes one line that starts with "Open question for S03:" and names the term and what the design needs it for. Stage S05R collects every such line, folds the accepted ones into the YAML, and raises the version. The PRD and the second model receive that version.

## Review stages

`S03R` and `S06R` are review prompts. `S05R` is a revision prompt that ends by rerunning the S03R rows. The reviewer reads the draft against this failure list and writes one row per item with PASS, FAIL, or NOT APPLICABLE and a file citation:

1. Code written before its analysis gate.
2. Architecture or design decided before the AI-versus-no-AI table (S2Q).
3. AI chosen for a capability because the project is about AI, with no stated need rules cannot meet.
4. A claim with no evidence label, or a Verified Fact with no file, test, log, or replay pointer.
5. A required artifact missing or at the wrong path.
6. A completion gate skipped or not stated.
7. A severity cutoff, SLA threshold, or business number invented without PROPOSED and an owner.
8. A term or status word used with a meaning that is not in the YAML.

A FAIL row blocks the next stage until it is fixed.

`S03F` is the fix pass for the semantic layer. It reads the numbered "Fixes required" list from the newest review file. It applies those fixes and nothing else, keeps the version, and rebuilds and retests. Then S03R runs again in a fresh chat. The same file is used every round. The only part you edit is its "Decisions for this round" block, where you record any choice a fix asks the owner to make. S03F does not run after S06 has cited the version. From then on, a YAML change goes through S05R with an ADR.

## Status log

Record each stage result in `playbook/STATUS.md` as one line: date, stage id, status, one-line note. Create the file on the first run.

## Final hand-back checklist

Tick these only after S10.

- [ ] `docs/00-setup/` and `docs/00-contract/` exist with the operating contract, cost envelope, and crosswalk.
- [ ] D1: six discovery files exist under `docs/01-discovery/`. Every row cites a file, test, log, or replay result.
- [ ] D2: baseline report, snapshot, data-quality baseline, defect list, and characterization tests exist. Kept behaviour and defects are in different lists.
- [ ] `docs/02-baseline/ai-qualification.md` exists. Every capability has a pick, a reason, an agency level, and a human approval point.
- [ ] D3: `semantic-layer/` matches the capture PDF tree plus `generated/` and `build.py`. Schema tests pass. S03R has no open FAIL. Every S03F round is recorded in `docs/02-baseline/semantic-layer-fixes.md`. S05R folded in the terms the Phase 4 and 5 designs introduced, the version was raised, and `docs/02-baseline/semantic-layer-revision.md` records the diff.
- [ ] D4: `docs/03-identity/` to `docs/12-finops/` exist. Each has a Half A design and Half B evidence. At least one high-risk decision has allow and deny policy tests.
- [ ] `docs/13-security-validation/` and `docs/14-audit/` exist. `pytest -m security` runs in CI. `/audit/{correlation_id}` rebuilds a case.
- [ ] D5: `docs/prd/prd.md` and `traceability.md` exist. Every requirement cites a YAML id. S06R has no open FAIL.
- [ ] D6: the app runs one flow to a human decision. The audit row is written before any state change. An AI timeout returns HOLD_FOR_REVIEW with no fake summary.
- [ ] D7: `docs/model-comparison/` has the brief, run log, and comparison. The YAML hashes match the S05R version before and after the test.
- [ ] D8: `PRODUCTION_EVIDENCE_PACK.md` is filled. `docs/15-readiness/` states ready, not ready, and accepted risk with owners.
- [ ] `docs/defence/defence-answers.md` answers all ten questions with file or test pointers.
- [ ] Every demo number carries an honesty label.
- [ ] No invented cutoff anywhere. Every PROPOSED number names an owner.
- [ ] `transcript/chat_transcript.md` has every turn.
