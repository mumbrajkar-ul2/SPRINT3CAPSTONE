
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
