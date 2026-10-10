
*** Introduction of S03F and S05R STAGES for RECURRING ***
CURSOR:
I've written `playbook/S03F-semantic-layer-fixes.md` and linked it from every file that describes the review loop. Nothing under `semantic-layer/` was changed; applying those fixes is S03F's job.

One change from what I said last turn. I said S03F would write an ADR (a short written decision record) for each fix once the version is above `1.0.0`. Instead, S03F always keeps the version, and it stops running once the PRD cites that version. After that, a change goes through S05R with an ADR. The reason is S08: it checks that the semantic-layer version matches the PRD header and the S05R revision file. Changing the tree after S06 without raising the version would break that check.

**What S03F does:**
- It reads the numbered "Fixes required" list from the newest review file. That is `semantic-layer-review.md`, or `semantic-layer-revision.md` once S05R has run.
- It applies only those fixes and keeps the version. Then it rebuilds, runs the tests, and runs the S03 glossary done test.
- It records each round as "Round N" in a new file, `docs/02-baseline/semantic-layer-fixes.md`. S03R overwrites its review file on every run, so this file keeps the history.
- The only part you edit is the "Decisions for this round" block at the top of the prompt. If a fix needs a choice that isn't recorded there, S03F skips that fix and reports BLOCKED.

**Files updated:**
- **`playbook/README.md`:**
  - A new S03F row in the stage table. The S03R and S06 "Depends on" cells now include S03F.
  - How-to step 6 now says how to clear a failed review.
  - A paragraph on S03F in the review section.
  - A new line in the D3 checklist item.
- **`playbook/README(the failure list).md`:** the same paragraph and checklist line, so the copy you attach to review chats matches.
- **`playbook/S03R-semantic-layer-review.md`:** fixes must be numbered. Any fix you must decide is marked "Choice needed". The done test and the lifecycle section now point to S03F.
- **`playbook/S05R-semantic-layer-revision.md`:** when its rerun S03R rows fail, it now writes a numbered fix list. The loop then runs S03F and S03R before S06.
- **`Execution Plan.md`:**
  - the phase diagram label
  - the stage list
  - the review paragraph
  - the Phase 3 lifecycle and gate
  - the Phase 5R steps
- **`Project_Intent.md`** and its Appendix E excerpt: one paragraph on the fix loop.
- **`Telecom Application Modernization.md`:** the semantic-layer row names S03F.
- **`docs/02-baseline/semantic-layer-review.md`:** the fix list now points to S03F. Fix 4 is marked "Choice needed" with options A and B.
- **`playbook/STATUS.md`:** the S03R note now says "run S03F", and there is a new row for this playbook change.

I left `operating-contract.md` alone, because its row 7 already covers your review of each change. S06 and S08 also stay as they are, because S03F keeps the version they cite.

This turn is added to `transcript/chat_transcript.md`.

**Next step:** open a new chat and attach the S03F inputs. Fill the Decisions block with your choice for fix 4, for example `Fix 4: Option A.` 


*** will S03R, S03F and S05R stages need to be iterated multiple times? ***
CURSOR:
Yes, they can repeat. The playbook does not limit how many times. Each stage repeats for a different reason.

**S03R and S03F repeat until the review passes.** One round is: run S03F, then run S03R again in a fresh chat. Expect one or two rounds this time. The seven fixes are small, and each one names its files and lines. A second round happens in two cases:
- The new reviewer finds something the first reviewer missed. This can happen because a fresh chat has no memory of the earlier review.
- A fix creates a new problem. For example, a new glossary row might not match the YAML.

**S05R normally runs once.** It runs after S05-14 and raises the version, for example to `1.1.0`. Two things can bring it back:
- **Its own rerun S03R rows fail.** Then S03F and S03R run again at the S05R version. S05R itself does not run again.
- **S06 finds a term the YAML lacks.** `S06-prd.md` says to stop, write an "Open question for S03" line, and run S05R again. Each S05R run raises the version, for example to `1.2.0`. The S03R rows are checked again, and S03F runs if any fail.

The longest realistic path looks like this:
1. Two S03F and S03R rounds before S04.
2. One S05R run, perhaps followed by one more S03F round.
3. One more S05R run if the PRD finds a missing term.

After S06 cites a version, S03F stops running. Every later change goes through S05R with an ADR.

**Nothing in the playbook stops the loop.** A reviewer could find small issues round after round. You could add a cap to S03F, for example: "If round 3 still has a FAIL, stop. The owner decides whether to accept the remaining FAIL rows as named risks or change the check." That decision would go in `STATUS.md` and in the review file's header.

Do you want me to add that cap to S03F and the README?

This turn is added to `transcript/chat_transcript.md`.

