# S06F — PRD fixes

A fix pass for Phase 6. Run this stage when the PRD review (S06R) has a FAIL row, or when the owner decides to fix the review's "Other findings" before S07 starts. It applies the fixes to `prd.md` and `traceability.md`, and nothing else. Then S06R runs again in a fresh chat.

This file is reused every round. The prompt does not hold any fix. It reads the "Fixes required" list from `docs/prd/prd-review.md`. When that list says None, the fixes are the lines of the "Decisions for this round" block. The only part you edit is that block.

## When to run it

| Situation | Fix source | After this stage |
|---|---|---|
| S06R is BLOCKED, or has a FAIL row in P8 or P11. S07 has not started. | `docs/prd/prd-review.md` | Run S06R again in a fresh chat. S07 waits for PASS, or CONDITIONAL PASS with fixes applied. |
| S06R has no FAIL row ("Fixes required: None"), and the owner chooses to settle "Other findings" before S07 starts. | The "Decisions for this round" block. Each line names the "Other findings" row it closes (for example R3-1). | Run S06R again in a fresh chat. S07 waits for that run. |
| A fix needs a new YAML id or a changed YAML sentence. | Do not edit `semantic-layer/` in this stage. | Run S05R and write a new ADR under `docs/ADR/`. The layer version rises. Then run this stage again, so the PRD header carries the new version. Then run S06R. |
| S07 has already started. | Do not run this stage. | A PRD change needs an ADR under `docs/ADR/` that names the requirement id and the reason. S07 then follows the changed PRD. |

Why this stage is separate from S06. S06 writes the whole PRD from the semantic layer. Running it again could rewrite parts that the review passed. This stage changes only what a fix names.

## Before you paste

Fill in the "Decisions for this round" block in the prompt. Write one line for each fix that offers a choice between options, or that the review marks as optional. Write `None` if there are no such fixes.

Example for round 1. The review's F-1 lets rows 3 and 4 either get an "Open question for S03:" line or use a word the glossary already has. A line for it reads: `F-1 rows 3 and 4: use the Open question line.` The review's F-8 is marked optional. To apply it, write: `F-8: apply.` If the block has no line for F-8, this stage leaves F-8 alone.

Example for round 7. The review (v5.0) says "Fixes required: None". It lists X-3, X-4 and X-7 as "Other findings". The block has one line for each of them with the exact words to write. It also has one line that says "Do not apply" for X-5, X-6, X-8 and X-9. This stage applies X-3, X-4 and X-7 and records the other four as "left as it is".

A fix that offers a choice and has no line in the block is marked "waiting for a decision". The stage then ends BLOCKED. That is the intended result. The owner is Team-Force (`docs/00-contract/operating-contract.md` row 10).

## Inputs

- `playbook/S06-prd.md` (the rules the PRD must keep)
- `playbook/S06R-prd-review.md` (the thirteen checks)
- `playbook/README.md` (the failure list)
- `06-telecom-service-network-incident-ops/docs/prd/prd-review.md` (the fix source; for round 7 it is v5.0, PASS, "Fixes required: None", and its "Other findings" X-3, X-4 and X-7 are the rows to close)
- `06-telecom-service-network-incident-ops/docs/prd/prd.md`
- `06-telecom-service-network-incident-ops/docs/prd/traceability.md`
- `06-telecom-service-network-incident-ops/docs/prd/prd-fixes.md` (rounds 1 to 6 exist. Read the newest round for the locked values)
- `06-telecom-service-network-incident-ops/docs/prd/Risk Management.md` (read only)
- `06-telecom-service-network-incident-ops/semantic-layer/` (the whole tree, read only)
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md` (read only)
- `06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md` (read only)
- `06-telecom-service-network-incident-ops/docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`
- `06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md`
- `06-telecom-service-network-incident-ops/docs/ADR/0004-defer-rq-31-answer-store.md` (RQ-31 build is deferred. Test counts are 29 existing, 43 planned, 1 deferred)
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/approval-workflow.md` (read only, to check line 76 that decision X-4 cites: "A rejection writes no approval id.")
- `06-telecom-service-network-incident-ops/docs/12-finops/evidence.md` (read only, the answer store lines the owner edited on 2026-10-13)
- `Project_Acronyms.md` (read only, to check that lines 312, 386 and 388 agree with the PRD after round 7. Do not edit it)
- `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md` (row 10 names the business owner)
- `06-telecom-service-network-incident-ops/data/synthetic/alarms.csv` (read only, to check the worked examples a decision gives)
- `06-telecom-service-network-incident-ops/data/synthetic/devices.csv` (read only, to check that a device id a decision names exists)
- `06-telecom-service-network-incident-ops/docs/12-finops/optimization-backlog.md` (read only, to check the lines a decision cites)
- `06-telecom-service-network-incident-ops/apps/api/` (read only, to check the file and line a decision cites)
- `playbook/S07-application-and-demo.md` (read only, to check the file and section a decision names, and to check that lines 35, 38 and 106 agree with the PRD after round 7)
- `Project_Intent - Appendix B.md` (the four honesty labels)
- Every design file and test file that a fix names

## Prompt

```text
# Stage S06F — PRD fixes

## Decisions for this round
<!-- Fill in before pasting. One line per fix that offers a choice between options, or that the review marks optional. Write "None" if there are none. A fix that only needs a business owner uses operating-contract.md row 10. A line may give the exact words to write. Use those words as written. Find each place by heading or requirement id. The line numbers are hints, and they move after an edit. -->
Round 7. The review (`docs/prd/prd-review.md`, v5.0, PASS) lists "Fixes required: None". The lines below close "Other findings" X-3, X-4 and X-7 from that review. The owner closed X-1 and X-2 by hand on 2026-10-13, in files outside this stage. The owner also made the matching edits for X-3 and X-4 in `playbook/S07-application-and-demo.md` and `Project_Acronyms.md` on the same day. X-5, X-6, X-8 and X-9 are left as they are. Apply X-3, X-4 and X-7. Edit only prd.md, traceability.md and prd-fixes.md. Then add one row for this round at the end of the table in `playbook/STATUS.md` (step 11). Make no other edit to STATUS.md.

X-3 (key names in the storm reply). Apply. Decision: the reply of `GET /alarms/storms/{storm_batch_id}` is a JSON body with the keys below. The key names are PROPOSED. Owner: Team-Force. They are reply keys and not YAML ids. The PRD invents no YAML id.
  a) RQ-08. Replace the sentence "The reply lists each row with `alarm_id`, `device_id`, `dedupe_key` and its flag word (empty when none)." with: "The reply is a JSON body with five keys: `raw_count`, `deduped_count` and `flagged_count` (each a whole number), and `rows` and `held_aside` (each a list). Each entry of `rows` and of `held_aside` has four keys: `alarm_id`, `device_id`, `dedupe_key` and `flag`. `flag` holds the flag word, or an empty string when the row has none. A row with a blank `dedupe_key` goes in `held_aside` and not in `rows`. Every other row goes in `rows`, flagged or not. These key names are PROPOSED. Owner: Team-Force." Keep every other sentence of the cell. Before you write, read the RQ-08 cell and the section 8 storm example, and check that no other sentence of the cell says a row is flagged and also held aside.
  b) RQ-62. After "the page lists the different `device_id` values from the storm reply" add "(read from `rows` and `held_aside`)". Keep the rest of the cell.
  c) Section 15, the Open question line about "raw count and flagged count". Before the words "Action: rerun S05R" add: "The reply key names are in RQ-08. They are PROPOSED. Owner: Team-Force. They are not YAML ids." The count of Open question lines stays 13.
  d) Section 6, step 1 names no key and stays as it is. `traceability.md` needs no row change, because the test name stays. S07 may add checks for the key names.

X-4 (the approval id on a "no"). Apply. Decision: only a yes gets an approval id. A no stores `decision`, `approver`, `record_id` and `correlation_id`, and `approval_id` is null in the reply, in the stored record and in the audit row. Read `docs/09-ai-guardrails/approval-workflow.md` line 76 before you write. It says the same: "A rejection writes no approval id." If the line differs, the file wins. Change the sentence to match and record the change.
  a) RQ-32. In the sentence that starts "The server sets `approver`", replace "(always `persona.noc_operator`, the only allowed role, RQ-35) and makes the approval id." with "(always `persona.noc_operator`, the only allowed role, RQ-35). When `decision` is `yes`, the server makes the approval id. When `decision` is `no`, the server makes no approval id and `approval_id` is null." After the sentence that lists the five keys of the reply, add "The key `approval_id` is null for a no." Replace "The call writes one `ai.approval` audit row first (RQ-36)." with "The call writes one `ai.approval` audit row first (RQ-36). For a yes, the server makes the approval id before it writes the row, and the row holds the id. For a no, the row holds `approval_id` null."
  b) RQ-33. After the first sentence add: "A no has `approval_id` null in the reply, in the stored record and in the audit row."
  c) Section 6, step 4. Replace "The server sets the approver and makes the approval id." with "The server sets the approver. For a yes it makes the approval id. For a no it makes none."
  d) Section 8, table row "Approval record". Replace "the approval id" with "the approval id (a yes only, null for a no)".
  e) Search prd.md for "approval id" and "approval_id". Every hit must agree with this decision. Where a hit says the server makes the id on every call, change it to match. Leave test names as they are. RQ-47 stays as it is. `traceability.md` needs no row change.

X-7 (HTTP status numbers on the page). Apply. Decision: add one row to the label table in section 8, directly after the row "Status code of `GET /health`": "HTTP status of each other reply the page shows (for example 200, 202, 403, 404) | REAL | A live call at the request, not a stored value. | not applicable". RQ-63 stays as it is.

X-5, X-6, X-8 and X-9. Do not apply. Decision: no edit. Record each as "left as it is" and say the owner chose to close only X-3, X-4 and X-7 in this round.

Owner edits outside this stage. None open. The owner closed X-1 and X-2 by hand on 2026-10-13. The owner also made the follow-up edits for X-3 and X-4 by hand on 2026-10-13, in two files. The review file keeps its original text. Make none of these edits. The edits are:
  - `playbook/S07-application-and-demo.md` line 35 (the storm route) names the five reply keys and the four entry keys. Line 38 (the approvals route) says the server makes the approval id for a yes only, and `approval_id` is null for a no. Line 106 (the demo script) says the demo approves, so it is a yes.
  - `Project_Acronyms.md` line 388 (the `POST /approvals/{id}` row) and line 312 (the `APR-` row) say the approval id is made for a yes only. Line 386 (the storm route row) names the five reply keys, puts a blank `dedupe_key` row in `held_aside`, and keeps a flagged row in `rows`.
  These lines were written before round 7, from the Decisions text above. After you edit the PRD, read each line once and compare it with the new RQ-08 and RQ-32 text. If a key name or a rule differs, do not edit the line. List the difference in the Residual risks row of the `prd-fixes.md` header, with the file and line. If none differs, write "Owner edits agree with the PRD" in that row.

Version and checks for this round. Raise the version of prd.md and traceability.md from 1.7 to 1.8, once, with the same number in both. In the Date / version row write "2026-10-13, v1.8. S06R fixes applied, round 7. Round 7 closes X-3, X-4 and X-7 of review v5.0." Add no RQ row, no YAML id and no test name. Keep 73 RQ rows, 29 existing tests, 43 planned tests, 1 deferred test, 757 ids, 13 Open question lines and layer version 1.1.1. After the edits, search prd.md and traceability.md for "approval id", "approval_id", "raw_count", "deduped_count", "flagged_count", "held_aside", "five keys", "flag word", "13" and "Thirteen". Every hit must agree with the text above. Every term in the new text must appear in the glossary, in the YAML, or on an Open question for S03 line. No new sentence may define a word.

## Objective
Apply the "Fixes required" list from the newest PRD review to `prd.md` and `traceability.md`. When that list says None, apply the lines of the Decisions block instead. Change nothing else. Keep the semantic-layer version. Re-run the PRD checks that a script can run. Record each edit so the next S06R reviewer can check it. Do not review the PRD. S06R does that in a fresh chat.

## Scope
Include: `docs/prd/prd.md`; `docs/prd/traceability.md`; `docs/prd/prd-fixes.md`; one new row at the end of the table in `playbook/STATUS.md`; the "Decisions for this round" block above.
Exclude: any item the review passed, unless a fix names it; any fix the review marks optional, unless the Decisions block names it; the review file; `Risk Management.md`; every ADR; `S05R_Decisions_Taken.md`; `semantic-layer-revision.md`; `Project_Acronyms.md`; every file under `playbook/`, except the one new row in `playbook/STATUS.md`; every file under `docs/12-finops/`; every file under `semantic-layer/`, `apps/`, `policy/`, `tests/`, and `data/`.

## Required analysis
1. Find the fix source. Open `docs/prd/prd-review.md`. Record its path, its header date and version, and its stage status. Copy its numbered "Fixes required" list word for word into the artifact. If a fix names rows of "Other findings" (for example O-1 to O-5 in round 1, R2-2 in round 2, R3-1 to R3-8 in round 3, X-1 to X-8 in round 5, or X-3, X-4 and X-7 in round 7), copy those rows word for word too. If the list says None, write "Fixes required: None" and say that the fixes come from the Decisions block. Treat each Decisions line as one fix. A line that names a finding the review does not have (for example R3-9 in round 3) is a fix that the owner raised after the review. Say so in the record. A line may also say "Do not apply" for a finding (for example X-8 in round 5, or X-5, X-6, X-8 and X-9 in round 7). Record that line as "left as it is", with its reason. If the review has a FAIL row and no matching fix, write the fix as "Missing from the review" and stop that row.
2. Check the versions. Read `version:` from `semantic-layer/README.md`. It must equal the version in the PRD header under Evidence sources, in the header of `traceability.md`, and in the header of `semantic-layer-revision.md`. It must equal the version the review recorded. Read the newest ADR that changed the YAML. If any of these differ, stop. The status is BLOCKED. Write which two differ.
3. Decide each fix. Mark it one of: apply; waiting for a decision (the fix offers options, or the review marks it optional, and the Decisions block has no line for it); needs S05R (the fix needs a new YAML id or a changed YAML sentence); cannot apply (give the reason in one sentence, for example the fix names a file this stage may not edit). Do not pick an option for the owner. A fix that only needs a business owner's name uses the owner in `docs/00-contract/operating-contract.md` row 10, unless the Decisions block names another. Write that owner next to the word PROPOSED. Naming the owner does not approve a number.
4. Apply. For each fix marked apply, edit only the places the fix names in `prd.md` and `traceability.md`. Find each place by requirement id or section heading. Lines move after an edit, so a line number alone is not enough. Record each edit: fix number, file, requirement id or section, line, the old text, the new text. Follow these rules:
   - A fix that writes an "Open question for S03:" line uses the form of the existing lines in the PRD. It names the word, says what the word is needed for, says what the PRD does instead, and says what action the owner takes. The PRD does not define the word. It does not invent a YAML id.
   - A fix that rewrites a requirement keeps its RQ id, its YAML ids, and its test name, unless the fix names a change. If the rewrite changes what the test must check, change the matching row in `traceability.md` the same way and say so in the edit record.
   - A fix that adds a number or a limit writes PROPOSED and an owner next to it. It does not choose a new number.
   - A fix that adds a row to a label table uses only REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.
5. Keep the places that state one fact in agreement. For every edit, search `prd.md` and `traceability.md` for the same claim stated somewhere else. Example: the 128 character limit appears in RQ-44, RQ-69, section 11, and section 13. If a fix changes how one place states it, check the others and change them to match, or write why they stay. Also check every text that states a name or an owner that you changed, in the same file.
6. Protect ids. Do not renumber, delete, or merge any RQ id. List every RQ id you touched. For each one, list the files that cite it. Do not add a requirement row unless a fix says so. If a fix adds one, give it the next free RQ number and a YAML id, a test name marked planned with its stage, and a design file.
7. Version and header. Keep the semantic-layer version string in both headers as it is. Raise the document version of `prd.md` and `traceability.md` by one minor step (for example v1.1 to v1.2. Round 7 goes from v1.7 to v1.8). Use the same new version in both. In the "Date / version" row of each header, write the date, the new version, "S06R fixes applied, round N", and the fix numbers. Update the Status row. If a fix changes a statement in the PRD's own completion-gate section, change that statement to match.
8. Re-run the checks that a script can run. Paste the output of each one.
   a. Count the `RQ-nn` rows in `prd.md` section 10. Each id appears once. The count equals the count in `traceability.md` section 1.
   b. Collect every `id:` in the seven YAML files. Look up every YAML id cited in `prd.md` and `traceability.md`. All resolve. Look up every backticked id-shaped token in the text you changed. Audit action words such as `policy.deny` resolve through `status.code.audit_action.*`. One exception: a word that a Decisions line gives as PROPOSED and that sits on an "Open question for S03:" line has no YAML id yet (rounds 3 and 5: `record.storm_read`, `ai.recommendation`, `ai.approval`). List each such word as an expected miss, with the Open question line that names it. Any other miss is a failure. Reply key names that a Decisions line gives as PROPOSED are not YAML ids, and they have no dot in them (round 7: `raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside`, `alarm_id`, `device_id`, `dedupe_key`, `flag`, `approval_id`). Do not look them up as ids. List them once as "reply keys, not ids", with RQ-08 and RQ-32 as the places that name them.
   c. Compare `traceability.md` section 1 with `prd.md` section 10 row by row: YAML ids, test name, existing or planned, design file.
   d. Check that each design file named in a row exists, that each `existing` test is a function in the named file, and that no `planned` test already exists.
   e. Run `python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`. The layer must be unchanged.
   f. Run the existing tests the PRD names with `pytest`. Copy `logs/audit.log` first. Restore it after. Its line count must be the same before and after. Run `pytest` from `06-telecom-service-network-incident-ops`. The last S06R run read 40 passed and 1 skipped (the `opa` test, RQ-59) and `logs/audit.log` had 240 lines before and after. A different number is not a failure of this stage when no test file changed. Write the number and say so.
   g. Find out which files you changed. Run `git status --short -uall` from the repository root (`SPRINT3CAPSTONE`) before you start and after you finish. Use `-uall`. The folder `docs/prd/` is untracked, so plain `git status --short` shows it as one folder and hides which file inside it changed. Before you start, also take a SHA-256 hash of every file the first output lists, for example: `git status --short -uall | ForEach-Object { $_.Substring(3).Trim('"') } | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | ForEach-Object { Get-FileHash -LiteralPath $_ -Algorithm SHA256 }`. Run the same command after you finish. Compare the two hash lists and the two file lists. The only files with a different hash, and the only new files, are `docs/prd/prd.md`, `docs/prd/traceability.md`, `docs/prd/prd-fixes.md` and `playbook/STATUS.md`. For `playbook/STATUS.md` the only difference is the one new row at the end of the table. Every other file in the first list must have the same hash after. That covers the ADR files, `Project_Acronyms.md`, `S05R_Decisions.md`, `S05R_Decisions_Taken.md`, `docs/12-finops/evidence.md`, `docs/12-finops/optimization-backlog.md`, `docs/prd/Risk Management.md`, the other `playbook/` files and `logs/audit.log` (restored after the test run). Test runs rewrite `.pytest_cache` and `__pycache__` files. List them as already present and do not count them as a difference. `transcript/chat_transcript.md` is appended after your final response, so it is outside this check. Write the two file lists and any difference in the artifact.
   h. Count the "Open question for S03:" lines in `prd.md` section 15. The count must equal the number the Decisions block states. Search `prd.md` and `traceability.md` for every place that states that count in words or digits. All must agree.
9. Map fixes to rows. For each FAIL row in the fix source, name the fix numbers and the edits that address it. When the review has no FAIL row, map each Decisions line to the "Other findings" row it closes, and name the lines that close none. Do not mark any row PASS. The next S06R does that.
10. Run the done test. In one requirement row of `prd.md`, change one YAML id to a name that does not exist. Run check 8b. Paste the failing line. Restore the id. Run check 8b again. Paste the pass line.
11. Log the round in `playbook/STATUS.md`. Do this last, after the checks and the done test, so the status is known. Open the file and read its last rows. Add one row at the end of the table. Use the same four columns: Date, Stage, Status, Note. Date is today's date. Stage is `S06F round N`. Status is the stage status of your final response (PASS, CONDITIONAL PASS or BLOCKED). The Note is plain speech and follows the round 6 row: the new version of `prd.md` and `traceability.md`; the fixes closed, by number, and the fixes left as they are; whether the owner edits agree with the PRD (none are open at the start of round 7); the check 8a to 8h counts; the test numbers (passed and skipped); whether the done test failed and then passed; that the layer stays at its version; the record (`docs/prd/prd-fixes.md`, Round N); and "Next: S06R in a fresh chat against vX.Y". Add the row only. Do not edit, reorder or delete any other row. Do not log the S06R runs or any owner edit. If the stage is BLOCKED, still add the row and say why. Name the row you added in the artifact.

## Evidence rules
- Every edit names the fix number, the file, and the requirement id or section.
- Label claims: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line, a YAML id, a test name, or pasted command output.
- Every number the PRD shows keeps its honesty label. Every cutoff keeps PROPOSED and an owner.

## Constraints and guardrails
- Edit only `prd.md`, `traceability.md`, and `prd-fixes.md`, and add the one STATUS.md row (step 11). A fix that needs any other file is "cannot apply" or "needs S05R". Write the file name and the stage that owns it. If the Decisions block names one other file and one edit, make only that edit.
- The PRD does not define a term. A missing term becomes an "Open question for S03:" line, or the PRD uses a word the glossary already has.
- Keep the semantic-layer version string. Raising it is the job of S05R with a new ADR.
- Do not change the meaning of any ADR 0002, ADR 0003 or ADR 0004 decision. The three ADR 0003 decisions stay as the locked facts state them. ADR 0004 defers the build of the RQ-31 answer store. Its rules stay in RQ-31.
- Keep the quotes of section 7 word for word from `ai-qualification.md`. A fix that adds a row to section 7 also quotes that file word for word. No AI use gains execute agency. No EXECUTE route is added.
- A Decisions line may give exact words to write. Write them as given. Before you write a sentence that cites a file and line, or a row of a data file, read that place. If it differs from the sentence, the file wins. Change the sentence to match and record the change.
- A Decisions line that gives a PROPOSED name keeps PROPOSED and the owner next to it. The name is not a YAML id. The PRD does not invent an id for it.
- The "Owner edits outside this stage" line is not a fix. Make none of those edits. Name any difference you find, and any edit still open, in the Residual risks row of the `prd-fixes.md` header.
- Keep what S06R found as PASS: the two "will not implement" sentences, `POST /ai/summarize/{id}` kept, `GET /ready` on the implement list, the no-header 403 on `GET /records/{id}`, the login route on the will-not-implement list, and the deferred RQ-31 test (ADR 0004).
- No invented cutoff, threshold, or target number. A fix that needs a number uses the Decisions block. A number appears only as PROPOSED with a named owner.
- Do not edit the review file the fixes came from.
- Redact secrets. No password, key, or token value anywhere in the files or the artifact.
- Plain speech. Short sentences. Everyday words. A reader new to telecom must know what to picture after one pass.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
These are the values at S06R round 1, with the changes that rounds 2 to 7 add. If an earlier S06F round changed one, use the value in the newest round of `prd-fixes.md`.

| Item | Value |
|---|---|
| Semantic layer version | `1.1.1`. ADR 0002 changed one YAML sentence. ADR 0003 and ADR 0004 added no YAML id. |
| YAML ids at `1.1.1` | 757 |
| PRD version before round 1 | v1.1. Requirements RQ-01 to RQ-73. 29 tests exist. 44 are planned for S07. |
| PRD version before round 2 | v1.2, set by round 1. Round 2 raises it to v1.3 in `prd.md` and `traceability.md`. |
| PRD version before round 3 | v1.3, set by round 2. Round 3 raises it to v1.4 in `prd.md` and `traceability.md`. |
| PRD version before round 4 | v1.4, set by round 3. Round 4 raised it to v1.5 in `prd.md` and `traceability.md`. |
| PRD version before round 5 | v1.5, set by round 4. Round 5 raises it to v1.6 in `prd.md` and `traceability.md`. |
| PRD version before round 6 | v1.6, set by round 5. Round 6 raised it to v1.7 in `prd.md` and `traceability.md`. |
| PRD version before round 7 | v1.7, set by round 6. Round 7 raises it to v1.8 in `prd.md` and `traceability.md`. |
| Test counts from round 6 | 29 exist, 43 are planned for S07, and 1 is deferred (RQ-31, ADR 0004). Rows stay at 73. A deferred test is neither existing nor planned in check 8c and 8d. |
| "Open question for S03:" lines | 13 since round 3 (round 3 deleted O-1 and O-2 from 15). Rounds 5 to 7 add none and keep 13. Round 7 adds one sentence to an existing line (X-3 c) and no new line. |
| Review fix list at round 3 | "Fixes required: None". The fixes were the Decisions lines. They closed R3-1 to R3-8, and R3-9, which the owner raised after the review. |
| Review fix list at round 5 | `prd-review.md` v4.0, BLOCKED. "Fixes required": F-1 (P2 and P12.8). The Decisions lines also close the other findings X-1 to X-7. X-8 is left as it is. |
| Review fix list at round 7 | `prd-review.md` v5.0, PASS. "Fixes required: None". The Decisions lines close the other findings X-3, X-4 and X-7. X-1 and X-2 were closed by the owner by hand on 2026-10-13. The owner also edited `playbook/S07-application-and-demo.md` (lines 35, 38, 106) and `Project_Acronyms.md` (lines 312, 386, 388) the same day, to match X-3 and X-4. No owner edit is open. X-5, X-6, X-8 and X-9 are left as they are. |
| Storm reply keys (round 7) | `raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside`. Each entry of `rows` and `held_aside` has `alarm_id`, `device_id`, `dedupe_key`, `flag`. PROPOSED. Owner: Team-Force. Reply keys, not YAML ids. They are written into RQ-08 in round 7. |
| Approval id (round 7) | Only a yes gets an approval id. For a no, `approval_id` is null in the reply, in the stored record and in the audit row. `docs/09-ai-guardrails/approval-workflow.md` line 76 says "A rejection writes no approval id." |
| S06R baseline run | 40 passed and 1 skipped (41 test items). The skip is the `opa` test (RQ-59). `semantic-layer/tests`: 41 passed. `logs/audit.log` had 240 lines before and after. The round 5 review (v5.0) read the same numbers, and `build.py --check` passed. |
| Four AI outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Four honesty labels | REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL (`Project_Intent - Appendix B.md`). No YAML id. |
| ADR 0003 decision 1 | Login is out of scope. The role stays a word the caller types (D-07). |
| ADR 0003 decision 2 | `GET /records/{id}` refuses a call with no header (RQ-68). |
| ADR 0003 decision 3 | The 300 second answer store stays. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence) (RQ-31). The cap is PROPOSED and has no number. The owner confirmed this reading in round 2. A healthy recommend answer is HOLD_FOR_REVIEW with a sentence (RQ-18), and the store holds it. From round 3 the store serves `POST /ai/recommend/{id}` only, and an entry is found by `prompt_hash` alone. ADR 0004 (2026-10-13) moves the build out of S07. The rules stay as the rules for a later build. |
| Deferred items | 13 items: D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20. D-07 is decided. |
| S06R gate | BLOCKED when any of P1, P2, P3, P4, P9, P13 is FAIL. CONDITIONAL PASS only when every FAIL is in P8 or P11. |
| Business owner | Team-Force (`operating-contract.md` row 10) |

## Required artifacts
1. The fixed `06-telecom-service-network-incident-ops/docs/prd/prd.md` and `traceability.md`. The semantic-layer version is unchanged. The document version is raised once per round, in both files.
2. `06-telecom-service-network-incident-ops/docs/prd/prd-fixes.md`. Add one section per round, titled "Round N, <date>". Keep earlier rounds. Each section holds: the fix source path and status; the fix list copied word for word; the Decisions block as pasted; the decision per fix; the edit list; the version check; the check 8a to 8h output; the done-test output; and the map from FAIL rows (or, when there is none, from the "Other findings" rows) to fixes. Write the header table once at the top of the file. Update its Status and Date / version each round.
3. `playbook/STATUS.md`. One new row at the end of the table for this round (step 11). No other change to that file.

## Completion gate
PASS when every fix is applied, the version strings are equal and unchanged, checks 8a to 8h pass with the same counts as the locked facts (or the counts a fix explains), the done test fails and then passes as expected, the one STATUS.md row is added, and no other file outside the fix list changed. CONDITIONAL PASS when every fix is applied and the only open items are optional fixes or other findings that the fix list did not name. BLOCKED when a fix is waiting for a decision, needs S05R, or cannot be applied; a check fails; a file outside the fix list changed; or the version strings differ.

## Lifecycle linkage
Cite the fix source by path, the PRD requirement ids, the semantic-layer ids, ADR 0002, ADR 0003, ADR 0004, `docs/09-ai-guardrails/approval-workflow.md` (round 7), and `docs/02-baseline/ai-qualification.md`. Stage S06R runs next, in a fresh chat, against the fixed PRD. It overwrites `prd-review.md`. The round sections in `prd-fixes.md` keep the history. S07 starts only when S06R reads PASS, or CONDITIONAL PASS with fixes applied. When a fix needs a YAML change, S05R and a new ADR run first, and this stage runs again with the new version. After S07 starts, this stage does not run. Stage S08 gives the second model the PRD that passed S06R, at the same semantic-layer version.

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
| `docs/prd/prd.md` | Every fix marked apply is in the text. Semantic-layer version unchanged in the header. Document version raised once. "Date / version" row names the round and the fix numbers. |
| `docs/prd/traceability.md` | Same document version as `prd.md`. A row changed only where a fix changed a requirement. Round 7 changes the header only, because no test name changes. |
| `playbook/STATUS.md` | One new row at the end of the table: `S06F round N`, the stage status, and a plain-speech note with the version, the fixes closed, the check counts, the test numbers, the done-test result and "Next: S06R in a fresh chat against vX.Y". No other row changed. |
| Round 7 edits in `docs/prd/prd.md` | RQ-08 names the five reply keys and the four entry keys. RQ-62 reads `device_id` from `rows` and `held_aside`. The raw count Open question line names the keys as PROPOSED. RQ-32 and RQ-33 say a no has `approval_id` null. Section 6 step 4 and the section 8 "Approval record" row say the same. The section 8 label table has the new row for the HTTP status of other replies. The version is v1.8. Rows 73, existing 29, planned 43, deferred 1, ids 757, Open question lines 13. |
| `docs/prd/prd-fixes.md` | Header table. One "Round N" section with the fix source, the fix list, the Decisions block, the decision per fix, the edit list, the version check, the output of checks 8a to 8h, the done-test output, and the map from FAIL rows (or "Other findings" rows) to fixes. |

## Done test

Every fix number in the fix source has an edit row or a stated reason. Change one YAML id in a requirement row to a name that does not exist. The id check fails. Restore it. The id check passes. Then open a fresh chat and run S06R.
