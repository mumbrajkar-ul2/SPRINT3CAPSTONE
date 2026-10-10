# S03F — Semantic layer fixes

A fix pass for Phase 3. Run this stage only when a semantic-layer review has a FAIL row. It applies the "Fixes required" list from that review and nothing else. Then S03R runs again in a fresh chat.

This file is reused every round. The prompt does not hold any fix. It reads the fix list from the newest review file. The only part you edit is the "Decisions for this round" block.

## When to run it

| Situation | Fix source | After this stage |
|---|---|---|
| S03R has a FAIL row. S04 has not started. | `docs/02-baseline/semantic-layer-review.md` | Run S03R again in a fresh chat. S04 waits for PASS, or CONDITIONAL PASS with fixes applied. |
| S05R reran the S03R rows and one is FAIL. S06 has not started. | `docs/02-baseline/semantic-layer-revision.md` | Run S03R again in a fresh chat. S06 waits for PASS, or CONDITIONAL PASS with fixes applied. |
| S06 or a later stage has already cited the version. | Do not run this stage. | The change goes through S05R with an ADR under `docs/ADR/`, and the version is raised. |

Why the last row stops. S06 writes the version into the PRD header. S08 checks that the semantic-layer version equals the version in the PRD and in `semantic-layer-revision.md`. This stage keeps the version as it is. A change after S06 under the same version would give two different trees the same version string.

## Before you paste

Fill in the "Decisions for this round" block in the prompt. Write one line for each fix that offers a choice between options. Example: `Fix 4: Option A.` Write `None` if no fix offers options. Leave the rest of the prompt as it is.

You do not need a line when a fix only needs a business owner's name. S03F uses the business owner in `docs/00-contract/operating-contract.md` row 10. Today that owner is Team-Force. Write a line only to name a different owner for one fix.

## Inputs

- `playbook/S03-semantic-layer.md` (the rules the tree must keep)
- `playbook/S03R-semantic-layer-review.md` (the fifteen checks)
- `playbook/README.md` (the failure list)
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-review.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md` (only if S05R has run)
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-fixes.md` (only if an earlier round exists)
- `06-telecom-service-network-incident-ops/semantic-layer/` (the whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md` (row 10 names the business owner)
- Every other file the fix list names

## Prompt

```text
# Stage S03F — Semantic layer fixes

## Decisions for this round
<!-- Fill in before pasting. One line per fix that offers a choice between options. Write "None" if no fix offers options. A fix that only needs a business owner uses operating-contract.md row 10. -->
None

## Objective
Apply the "Fixes required" list from the newest semantic-layer review to `semantic-layer/` and to the other files the list names. Change nothing else. Keep the version. Rebuild and retest. Record each edit so the next S03R reviewer can check it. Do not review the tree. S03R does that in a fresh chat.

## Scope
Include: every file under `semantic-layer/`; any file outside it that a fix names by path; the "Decisions for this round" block above.
Exclude: any item the review passed, unless a fix names it; any file no fix names; advisories, unless the Decisions block says to apply one; application code; `policy/`; `data/`; the review file itself.

## Required analysis
1. Find the fix source. Compare `docs/02-baseline/semantic-layer-review.md` and, if it exists, `docs/02-baseline/semantic-layer-revision.md`. Use the one written last. Record its path, its header date and version, and its stage status. Copy its numbered "Fixes required" list word for word into the artifact. If the source has a FAIL row and no matching fix, write the fix as "Missing from the review" and stop that row.
2. Check the version. Read `version:` from `semantic-layer/README.md`. If `docs/prd/prd.md` exists and cites that version, stop. The status is BLOCKED. The change goes through S05R with an ADR.
3. Decide each fix. Mark it one of: apply; waiting for a decision (the fix offers options, and the Decisions block has no line for it); cannot apply (give the reason in one sentence). Do not pick an option for the owner. A fix that only needs a business owner's name uses the owner in `docs/00-contract/operating-contract.md` row 10, unless the Decisions block names another. Write that owner next to the word PROPOSED. Naming the owner does not approve the number.
4. Apply. For each fix marked apply, edit only the files and ids the fix names. A fix that adds an id also needs the rest of the S03 rules for that id: a `source:` list, `proposed: true` with `owner:` when the term is not in the repo, a glossary row in everyday words, a schema rule if the shape is new, and a test if the item is required. Record each edit: fix number, file, line or id, the old text, the new text.
5. Protect citations. For every id you changed, search `semantic-layer/`, `docs/`, `policy/`, `tests/`, and `apps/` for it. List each file that cites it. Do not rename or remove an id that a file cites.
6. Version and change log. Keep the `version:` string in every YAML file and in `README.md` as it is. Add one row to the README change log: date, the same version, "S03R fixes applied, round N", and the fix numbers. Update the README header if the status it states has changed.
7. Rebuild and test. Delete `generated/`. Run `python semantic-layer/build.py`. Run `python semantic-layer/build.py --check`. Run `pytest semantic-layer/tests -q`. Paste all three outputs. Replace the "Last build" block in `README.md` with this output.
8. Run the S03 done test. Change one status word in `glossary.md` only. Run the tests. Paste the failing test name. Restore the word. Run the tests again and paste the pass line.
9. Map fixes to rows. For each FAIL row in the fix source, name the fix numbers and edits that address it. Do not mark any row PASS. The next S03R does that.

## Evidence rules
- Every edit names the fix number, the file, and the line or id.
- Every item added carries a `source:` list of file paths.
- Every item not in the inherited repo carries `proposed: true` and `owner:`.
- Label claims: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line, a YAML id, a test name, or pasted command output.

## Constraints and guardrails
- The tree stays exactly the capture-PDF tree plus `generated/` and `build.py`. Add no file under `semantic-layer/`.
- Keep the version string. Raising it is the job of S05R.
- Do not change the meaning of an id unless a fix names that id and says how.
- No AI use may gain execute agency. The agency and approval point for each AI use still match `docs/02-baseline/ai-qualification.md`.
- No invented cutoff, threshold, or target number. A fix that needs a number uses the Decisions block. A number appears only as PROPOSED with a named owner. The default owner is in `docs/00-contract/operating-contract.md` row 10.
- Do not edit the review file the fixes came from.
- No hand edits under `generated/`. `build.py` writes it.
- Redact secrets. No password, key, or token value anywhere in the tree or the artifact.
- Plain speech in Markdown and in YAML `description:` fields. Short sentences. Everyday words.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from the S03 prompt; read, do not re-derive)
| Constant | Value |
|---|---|
| Tree | README.md, glossary.md, entities.yaml, relationships.yaml, status-taxonomy.yaml, business-rules.yaml, metrics.yaml, access-semantics.yaml, ai-context-policy.yaml, schemas/semantic-layer.schema.json, tests/test_semantic_layer.py, plus generated/ and build.py |
| Version before S05R | 1.0.0 |
| Four AI outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Fields never in a prompt | mgmt_ip, credential_profile |

## Required artifacts
1. The fixed files under `06-telecom-service-network-incident-ops/semantic-layer/`, with the version unchanged and one new row in the README change log.
2. Any file outside the tree that a fix names, edited only as the fix says.
3. `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-fixes.md`. Add one section per round, titled "Round N, <date>". Keep earlier rounds. Each section holds: the fix source path and status; the fix list copied word for word; the Decisions block as pasted; the decision per fix; the edit list; the citation check; the build, check, and test output; the done-test output; and the map from FAIL rows to fixes. Write the header table once at the top of the file. Update its Status and Date / version each round.

## Completion gate
PASS when every fix is applied, the build and the tests pass, `build.py --check` passes after the rebuild, the S03 done test fails and then passes as expected, and no file outside the fix list changed. CONDITIONAL PASS when every fix is applied and the only open items are advisories. BLOCKED when a fix is waiting for a decision or cannot be applied, a test fails, a file outside the fix list changed, or a later stage has cited the version.

## Lifecycle linkage
Cite the fix source by path, `semantic-layer/` files by path and id, and `docs/02-baseline/ai-qualification.md`. Stage S03R runs next, in a fresh chat, against the fixed tree. It overwrites `semantic-layer-review.md`. The round sections in `semantic-layer-fixes.md` keep the history. S04 starts only when S03R reads PASS, or CONDITIONAL PASS with fixes applied. When S05R's rerun rows fail, this stage runs with `semantic-layer-revision.md` as the fix source, then S03R runs again before S06. After S06 cites the version, this stage does not run. S05R handles the change with an ADR.

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
| `semantic-layer/*` | Every fix applied. Version unchanged. README change-log row for this round. README "Last build" from this round. |
| Files outside the tree named by a fix | Only the edit the fix names. |
| `docs/02-baseline/semantic-layer-fixes.md` | Header table. One "Round N" section with the fix source, the fix list, the Decisions block, the decision per fix, the edit list, the citation check, the build, check, and test output, the done-test output, and the map from FAIL rows to fixes. |

## Done test

Every fix number in the fix source has an edit row or a stated reason. Delete `generated/`, run `build.py`, run the tests. Everything passes. Change one status word in the glossary only. The tests fail. Then open a fresh chat and run S03R.
