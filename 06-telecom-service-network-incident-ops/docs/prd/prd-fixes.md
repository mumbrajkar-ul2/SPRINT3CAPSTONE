# PRD fixes (S06F)

| Field | Value |
|---|---|
| Stage | S06F. Apply the "Fixes required" list from `docs/prd/prd-review.md` to `prd.md` and `traceability.md`. This file records each round. |
| Date / version | 2026-10-13, v7.0 of this file. Round 7 added. Round 7 raised the PRD and traceability document version from v1.7 to v1.8. Round 6 added. Round 6 raised the PRD and traceability document version from v1.6 to v1.7. Round 5 added. Round 5 raised the PRD and traceability document version from v1.5 to v1.6. Round 1 raised the PRD and traceability document version from v1.1 to v1.2. Round 2 raised it from v1.2 to v1.3. Round 3 raised it from v1.3 to v1.4. Round 4 raised it from v1.4 to v1.5. Semantic layer version stays `1.1.1`. |
| Author | Round 1: Cursor agent (Cursor Grok 4.6) for Mangesh (FDE). Rounds 2 to 7: Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | **CONDITIONAL PASS.** Round 7 applied the three Decisions lines X-3, X-4 and X-7 of review v5.0 (PASS, "Fixes required: None"). X-3 gives the storm reply its key names (RQ-08, RQ-62, section 15). X-4 says only a yes gets an approval id (RQ-32, RQ-33, section 6, section 8). X-7 adds a label row for the HTTP status of each reply (section 8). X-5, X-6, X-8 and X-9 are left as they are by owner decision. Checks 8a to 8h match the locked counts (73 rows, 757 ids, 29 existing, 43 planned and 1 deferred test, 13 Open question lines, 40 passed and 1 skipped). The done test failed, then passed. The status is not PASS because S06R must run again in a fresh chat and score the round 7 edits, and because four other findings stay open by decision. Round 6 applied R6-1: RQ-31 (the answer store) is deferred under ADR 0004, and the four `Project_Acronyms.md` lines named in round 5 are fixed. Checks 8a to 8h match the new counts (73 rows, 757 ids, 29 existing, 43 planned and 1 deferred test, 13 Open question lines, 40 passed and 1 skipped). The done test failed, then passed. The status is not PASS because S06R must run again in a fresh chat and score the round 5 and round 6 edits. Round 5: applied F-1 (the one FAIL row, P2, and the same finding in P12.8) and X-1 to X-7 of review v4.0. X-8 is left as it is, with its reason. Checks 8a to 8h match the locked counts (73 rows, 757 ids, 29 existing and 44 planned tests, 13 Open question lines, 40 passed and 1 skipped). The done test failed, then passed. The status is not PASS for two reasons. S06R must run again in a fresh chat and score the round 5 edits. And `Project_Acronyms.md`, which is outside the fix list, still holds the words "a healthy call" and "never holds a BLOCK or HOLD answer". Round 4: Round 4 closed the two risks named in the round 3 final response. R4-1: the reason of a held answer is in the response body, and the audit row holds the action word and the outcome only (RQ-30, RQ-70, section 7, section 15). R4-2: the owner edits in nine files outside the PRD are made, including four more lines of the same kind that the list did not name. Checks 8a to 8h match the locked counts (73 rows, 757 ids, 29 existing and 44 planned tests, 13 Open question lines, 40 passed and 1 skipped). The done test failed, then passed. The status is not PASS, because the next S06R must confirm the round 4 edits, and because the audit row still has no key for a reason (see "Items for the next S06R" in round 4). |
| Evidence sources | Round 7: `docs/prd/prd-review.md` (2026-10-13, review v5.0, PASS, "Fixes required: None", X-3, X-4 and X-7). `docs/prd/prd.md` v1.7 and `docs/prd/traceability.md` v1.7 (the files before the edits). `semantic-layer/README.md` version `1.1.1`. `docs/09-ai-guardrails/approval-workflow.md` line 76. `playbook/S07-application-and-demo.md` lines 35, 38 and 106. `Project_Acronyms.md` lines 312, 386 and 388. `docs/12-finops/evidence.md` line 265. `docs/00-contract/operating-contract.md` row 10. Round 6: the owner's request of 2026-10-13 in chat ("Defer RQ-31"). `docs/ADR/0004-defer-rq-31-answer-store.md`. `docs/prd/prd.md` v1.6 and `docs/prd/traceability.md` v1.6 (the files before the edits). `semantic-layer/README.md` version `1.1.1`. `docs/12-finops/optimization-backlog.md`. Round 5: `docs/prd/prd-review.md` (2026-10-13, review v4.0, BLOCKED, F-1 and X-1 to X-8). `docs/prd/prd.md` v1.5 and `docs/prd/traceability.md` v1.5 (the files before the edits). `semantic-layer/README.md` version `1.1.1`. `docs/02-baseline/ai-qualification.md`. `semantic-layer/ai-context-policy.yaml` (the `outcome` of each `ai_use`). `data/synthetic/alarms.csv` lines 1, 2 and 353. `data/synthetic/devices.csv`. `docs/12-finops/optimization-backlog.md` lines 125, 127, 128. `playbook/S07-application-and-demo.md` line 36. `docs/00-contract/operating-contract.md` row 10. `docs/ADR/0003-s06-risk-recommendations.md`. Round 4: the owner's request of 2026-10-13 in chat ("Do the fixes for Risk 1 and Risk 2"). `docs/prd/prd.md` v1.5. `docs/prd/traceability.md` v1.5. `apps/api/services/audit_query.py` line 128. `apps/api/services/policy.py` and `apps/api/services/ai_gateway.py` (the reasons list). The nine files outside the PRD named in the round 4 edit list. Round 3: `docs/prd/prd-review.md` (2026-10-13, review v3.0, PASS, "Fixes required: None"). `docs/prd/prd.md` v1.4. `docs/prd/traceability.md` v1.4. `semantic-layer/README.md` version `1.1.1`. `data/synthetic/alarms.csv` lines 3, 20 and 355. `apps/api/services/policy.py`, `apps/api/services/ai_gateway.py`, `apps/api/services/breaker.py` and `apps/api/services/audit_query.py`. `docs/02-baseline/ai-qualification.md`. `playbook/S07-application-and-demo.md`. `docs/00-contract/operating-contract.md` row 10. Earlier rounds. Round 1: `docs/prd/prd-review.md` (2026-10-12, review v1.0, BLOCKED). Round 2: `docs/prd/prd-review.md` (2026-10-12, review v2.0, BLOCKED). `docs/prd/prd.md` v1.3. `docs/prd/traceability.md` v1.3. `semantic-layer/README.md` version `1.1.1`. `docs/02-baseline/semantic-layer-revision.md`. `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`. `docs/00-contract/operating-contract.md` row 10. The seven YAML files. The four test files named in O-4. |
| Assumptions | Round 7: (13) The Decisions block pasted in the prompt is the fix list, because the review says "Fixes required: None". (14) The block gives exact words for X-3, X-4 and X-7, and I wrote them as given, because the one file the block asks me to read (`approval-workflow.md` line 76) agrees with it. (15) The reply key names are PROPOSED. Owner: Team-Force. They are reply keys and not YAML ids. Round 6: (11) "Defer" means the row stays in the PRD and S07 does not build it, as ADR 0004 says. (12) A deferred test counts as neither existing nor planned. Round 5: (8) The Decisions block pasted in the prompt is the decision for every fix. The review's "Fixes required" list holds F-1, and the block closes X-1 to X-7. (9) Where the block says "the file wins", a file I read on 2026-10-13 beats the sentence in the block. This happened once, for X-1. (10) The owner edits that the block lists as outside this stage were already made when I read the files. Round 4: (5) Option A from the chat answer is the decision for R4-1. The owner confirmed it in chat on 2026-10-13. (6) The owner asked for the owner edits in the same request, so the round 3 rule "this stage makes none of them" does not apply to round 4. (7) The edits use the words of the round 3 Decisions block. Where those words did not fit the sentence, the edit list says so. Round 3: (3) The Decisions block pasted in the prompt is the fix list, because the review says "Fixes required: None". (4) The words `record.storm_read`, `ai.recommendation`, `ai.approval` and `final_action` are PROPOSED names. Owner: Team-Force. They are not YAML ids. Rounds 1 and 2: (1) The Decisions block pasted in the prompt was `None`. The owner then answered three choices in chat on 2026-10-12. Those answers count as the Decisions for this round. (2) "PRD line" means the physical line number after the edits in this round. |
| Unresolved issues | Round 7: none of the fixes is waiting. X-5, X-6, X-8 and X-9 of review v5.0 stay open by owner decision. The owner closed X-1 and X-2 by hand on 2026-10-13. `docs/12-finops/evidence.md` line 265 now says the store build is deferred, so the round 6 note below about that line is out of date. Round 6: none of the fixes is waiting. `docs/12-finops/evidence.md` line 265 still says the store is built in S07 (see "Items for the next S06R" in round 6). Round 5: none of the fixes is waiting. Two open items remain, and neither is a fix of this round. First, `Project_Acronyms.md` lines 93, 387 and 394 hold old wording (see "Items for the next S06R" in round 5). Second, X-8 is left as it is by decision. Round 4: the audit row stores no reason. A person who reads `logs/audit.log` cannot see why a case was held. A later ADR may add a key for it (option B in the chat answer). This PRD adds none. Round 3: RQ-30 and RQ-70 asked the audit row for a reason, and the section 7 paragraph said the audit row stores none. Closed in round 4 (R4-1). The PRD now has thirteen Open question lines (O-1 and O-2 are closed). Round 4 removed the section 15 list that held the two "output policy" hits. Earlier rounds: Round 2: F-4 (optional, the same as round 1 F-8: quote the approval point for the six other AI uses) was left alone by owner decision. The three design points in `prd.md` section 15 (R2-1) stay open by owner decision. R2-3 and R2-4 of the review need edits in `Risk Management.md`, `S05R_Decisions_Taken.md` and `semantic-layer-revision.md`. This stage may not edit those files. Round 1: F-8 is optional and was not applied. The fifteen Open questions in `prd.md` section 15 stay open. The stale lines in `docs/02-baseline/semantic-layer-revision.md` and `docs/02-baseline/S05R_Decisions_Taken.md` stay. S05R owns those files. |
| Residual risks | Round 7: Owner edits agree with the PRD (`playbook/S07-application-and-demo.md` lines 35, 38 and 106, and `Project_Acronyms.md` lines 312, 386 and 388; no key name or rule differs). Two items remain. (a) RQ-08 says a held-aside row has a `flag` key, and an older sentence of the same cell says a held-aside row is "counted in the raw count only", while the flagged count counts every row with a flag word. A blank-key row that also has a flag word is read two ways. No such row exists in `alarms.csv`. (b) The storm reply key names and the `approval_id` rule are PROPOSED (Team-Force) and are not YAML ids. A planned test is not evidence until S07 writes it. Round 6: (a) The deferred test has no stage and no date. ADR 0004 lists what a later stage must do. (b) Round 5 item (b), that S07 adds the cache flag before it ships RQ-31, no longer applies in S07. Round 5: (a) The owner edits that the block names outside this stage are `docs/12-finops/optimization-backlog.md` lines 125, 127 and 128, and `playbook/S07-application-and-demo.md` line 36. Both files were already changed (08:47 and 08:44 on 2026-10-13) when this round read them. Lines 127 and 128 equal the block. Line 125 lacks the last two words "in this packet". Same meaning. This stage did not edit either file. (b) S07 must add the cache flag as a YAML id under a new ADR before it ships RQ-31. (c) The test `test_unknown_role_word_is_not_stored_as_sent` now has a second case (the 129 character header id). S07 writes both. Round 4: (1) S07 must add the YAML ids for `record.storm_read`, `ai.recommendation`, `ai.approval` and `final_action` under a new ADR. That raises the layer version, and the PRD, `traceability.md` and the S08 hash step must follow. (2) The audit row has no reason key, so the audit log alone cannot explain a hold. The response body holds the reason. (3) Lines of the same kind that this round did not touch: `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` line 94 and `docs/02-baseline/S05R_Decisions.md` line 649 say 14 deferred items. `playbook/STATUS.md` lines 63 and 64 say the same, and `playbook/S06-prd.md` line 51 still asks the PRD to decide D-07. They are records of what was true on the day they were written. Earlier risks: A planned test is not evidence until it exists and passes. 44 of 73 tests are planned. S07 YAML additions raise the layer version. The PRD header, `traceability.md` and the S08 hash step must then follow. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/` unless they start with `playbook/` or `Project_Intent`.

## Round 1, 2026-10-12

### Fix source

| Field | Value |
|---|---|
| Path | `docs/prd/prd-review.md` |
| Header date and version | 2026-10-12, v1.0 of this review. Semantic layer version read from `semantic-layer/README.md`: `1.1.1`. |
| Stage status | **BLOCKED.** P2 is FAIL. P7, P8 and P11 are also FAIL. P1, P3, P4, P5, P6, P9, P10, P12 (rows 1 to 7) and P13 are PASS. |

### Fixes required (copied word for word)

| # | For | Fix needed |
|---|---|---|
| F-1 | P2 rows 1 to 4 | For each of answer store, near-miss list, claimed role, and raw and flagged count: write an "Open question for S03:" line that names the word and what it is needed for. Then run S05R and record a new ADR if Team-Force wants a YAML id. The PRD must not define the word itself. Alternative for rows 3 and 4: replace the word with one the glossary already has. |
| F-2 | P2 rows 5 to 7 | Write one "Open question for S03:" line each for the `decision` and `approver` fields, `record_id`, and the final-action key name. Say that S07 adds the ids under a new ADR (`prd.md` line 563 already says this, but not as an Open question line). |
| F-3 | P2, P12.6 | Change line 40 ("Section 15 lists the two terms the glossary lacks") and the gate row at line 578 so they match the new list of Open questions. |
| F-4 | P7 | Add a row to the label table at lines 203 to 214: "Counts inside the `cannot_prove` text (log lines with no correlation id, log lines that cannot be read): REAL, counted from `logs/audit.log` at the request." |
| F-5 | P8 | In RQ-69 add "The 128 limit is PROPOSED. Owner: Team-Force." |
| F-6 | P11, RQ-40 | Rewrite RQ-40 so it says what a final action is, names the key, and gives the value `none` with the reason that no route changes a device. Make the route scope match the test name. |
| F-7 | P11, RQ-54 | Rewrite RQ-54 to say what the breaker does: after a run of failed model calls the app stops calling the model for a while and returns HOLD_FOR_REVIEW. Keep the numbers PROPOSED (N-05). |
| F-8 | P3 (observation) | Optional. Quote the approval point for the six uses that section 7 skips, or state that section 3 is the whole list for them. `S06-prd.md` asks for a quote for every AI use. |
| F-9 | Other findings O-1 to O-5 | Close the five gaps below before S07. |

### Other findings O-1 to O-5 (copied word for word)

| # | Finding | Evidence | Impact | Label |
|---|---|---|---|---|
| O-1 | Nothing links step 1 to step 2 of the demo. RQ-08 returns the raw count, the deduped count and "the alarm ids". The lookup in step 2 needs a `device_id`. The storm response is not required to carry one. | `prd.md` RQ-08 (283), section 6 (122, 123), RQ-62 (382). `alarms.csv` has a `device_id` column (for example `ALA-00005` has `DEV-00005`). | A builder must guess how the page learns which device to look up. Two builders will guess differently. | **Verified Fact** for the text. **Inference** for the impact. |
| O-2 | The approval route has no written input or output. `{id}` is not defined (device id, recommendation id, or invocation id). The PRD does not say whether the caller sends `approver` or the server sets it from the header. The reply shape is not given. S07 chooses where the approval record lives and how the route finds the recommendation. | RQ-32 (325), RQ-34 (327), section 8 (line 198) | The only human decision in the demo has the least detail. The second model in S08 gets the same gap. | **Verified Fact** for the text (the PRD says RQ-34 is left to S07). **Inference** for the impact. |
| O-3 | Audit row names are not fixed. The final-action key has no name and no position. The action words for the storm read, the recommendation and the approval are not named. RQ-52 says S07 adds the ids first. | RQ-40 (333), RQ-41 (334), RQ-52 (354). `audit_query.py` and `main.py` use words such as `policy.deny`. | The test `test_audit_action_words_in_main_py_all_have_an_id` will fail or pass depending on words the PRD never states. | **Verified Fact** for the text. **Inference** for the impact. |
| O-4 | Four existing tests lock the behaviour that RQ-03 and RQ-68 remove. The PRD names none of them. ADR 0003 names two, for RQ-68 only. Nothing names the two that lock the missing-id first-row behaviour. | `tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row` (line 21); `tests/performance/test_load_once.py::test_missing_id_still_returns_the_first_row` (line 124); `tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default` (line 177); `policy/tests/test_policy_python.py::test_record_route_keeps_missing_header_default_operator` (line 453) | S07 will break four tests that the PRD still counts as the baseline. A builder with only the PRD does not know they must change. | **Verified Fact** (function names found with a search). **Inference** for the impact. |
| O-5 | The semantic layer version will move during S07. RQ-52, D-03, D-05, D-06, D-08 and D-18 each add YAML ids under a new ADR. The PRD header, `traceability.md` and the S08 hash step then need the new version. A stale line already says S08 hashes the tree at `1.1.0`. | `prd.md` line 563; `semantic-layer-revision.md` line 442; `S05R_Decisions_Taken.md` line 26 (still lists D-07 as deferred and counts 14) | S08 can receive a PRD and a YAML tree at different versions. | **Verified Fact** for the stale lines. **Inference** for the risk. |

### Decisions for this round

Pasted in the prompt:

```
None
```

Decisions given in chat, 2026-10-12:

- F-1 rows 3 and 4: write an Open question for S03 line for all four words. Do not swap rows 3 and 4 to glossary words.
- F-8: skip. List it as waiting for a decision. Optional.
- F-9 O-1 and O-2: add Open question lines. Do not pick a design.

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| F-1 | apply | Owner chose the Open question line for all four words. Four new lines in section 15. Pointers on RQ-08, RQ-31, RQ-65 and RQ-71. No word is defined. No YAML id is invented. |
| F-2 | apply | Three new Open question lines in section 15. Each says S07 adds the id under a new ADR. Adding the ids themselves needs S05R and is not done here. |
| F-3 | apply | Section 2 and the gate row now name the new Open question list. Header counts go from five to fifteen. |
| F-4 | apply | One REAL row added to the section 8 label table. YAML ids are existing ids only. |
| F-5 | apply | RQ-69 now has "The 128 limit is PROPOSED. Owner: Team-Force." Owner from `operating-contract.md` row 10. |
| F-6 | apply | RQ-40 rewritten. YAML ids and test name stay. The test check does not change, so the `traceability.md` RQ-40 row stays. |
| F-7 | apply | RQ-54 rewritten. Numbers stay PROPOSED (N-05). Owner: Team-Force. YAML ids and test name stay. |
| F-8 | waiting for a decision | Optional. The Decisions block has no apply line. Not edited. |
| F-9 O-1 | apply | Open question line. No `device_id` field is made required. |
| F-9 O-2 | apply | Open question line. No input or reply shape is chosen. |
| F-9 O-3 | apply | Open question line. RQ-52 already says S07 adds the ids. Adding the ids needs S05R and is not done here. |
| F-9 O-4 | apply | The four existing tests are named in `prd.md` section 10 and in `traceability.md` after section 1. Each function name exists. **Verified Fact.** |
| F-9 O-5 PRD side | apply | Section 15 now says S07 YAML additions raise the layer version and that the PRD header, `traceability.md` and the S08 hash step must follow. |
| F-9 O-5 stale files | cannot apply | The stale lines sit in `docs/02-baseline/semantic-layer-revision.md` and `docs/02-baseline/S05R_Decisions_Taken.md`. This stage may not edit them. S05R owns both files. |

### Edit list

Line numbers are the lines after the edit. **Verified Fact.**

| Fix | File | Requirement id or section | Line | Old text | New text |
|---|---|---|---|---|---|
| F-1 | `prd.md` | section 15 | 571 | (no line) | **Open question for S03:** the words answer store, stored answer and cache have no YAML id and no glossary row. RQ-31 needs a name for the place that holds a recent model answer so a second call with the same prompt hash can reuse it. This PRD uses those words and does not explain them. Action: rerun S05R and record a new ADR if Team-Force wants a YAML id. This does not block the PRD. |
| F-1 | `prd.md` | section 15 | 573 | (no line) | **Open question for S03:** the words near-miss phrase and near-miss list have no YAML id and no glossary row. RQ-71 needs a name for a phrase that is close to a listed command phrase. This PRD uses those words and does not explain them. Action: rerun S05R and record a new ADR if Team-Force wants a YAML id. This does not block the PRD. |
| F-1 | `prd.md` | section 15 | 575 | (no line) | **Open question for S03:** the words claimed role have no YAML id and no glossary row. RQ-65 needs a name for a role word the caller typed that no login proved. This PRD uses those words and does not explain them. Action: rerun S05R and record a new ADR if Team-Force wants a YAML id. This does not block the PRD. |
| F-1 | `prd.md` | section 15 | 577 | (no line) | **Open question for S03:** the words raw count and flagged count have no YAML id and no glossary row. RQ-08 needs names for the count of every alarm row in a storm and the count of rows that carry a flag. This PRD uses those words and does not explain them. The YAML id `metric.alarm_storm_size` is the count after duplicates are dropped. Action: rerun S05R and record a new ADR if Team-Force wants YAML ids. This does not block the PRD. |
| F-1 | `prd.md` | RQ-08 | 284 | ...left out of the deduped count. | ...left out of the deduped count. The words raw count and flagged count are an Open question for S03. |
| F-1 | `prd.md` | RQ-31 | 316 | ...No number is set. | ...No number is set. The words answer store, stored answer and cache are an Open question for S03. |
| F-1 | `prd.md` | RQ-65 | 386 | ...shown as claimed role (D-07, ADR 0003). | ...shown as claimed role (D-07, ADR 0003). The words claimed role are an Open question for S03. |
| F-1 | `prd.md` | RQ-71 | 399 | ...under a later ADR. | ...under a later ADR. The words near-miss phrase and near-miss list are an Open question for S03. |
| F-2 | `prd.md` | section 15 | 579 | (no line) | **Open question for S03:** the field names `decision` and `approver` on an approval record have no YAML id. RQ-32 needs them so a yes or no and the person who chose it can be stored. This PRD uses the field names from ADR 0002 D-03 and does not invent ids. Action: S07 adds the ids under a new ADR. This does not block the PRD. |
| F-2 | `prd.md` | section 15 | 581 | (no line) | **Open question for S03:** the field name `record_id` as the 16th audit key has no YAML id. RQ-41 needs it so each audit row names the device that was asked for. This PRD uses the name from ADR 0002 D-06 and does not invent an id. Action: S07 adds the id under a new ADR. This does not block the PRD. |
| F-2 | `prd.md` | section 15 | 583 | (no line) | **Open question for S03:** the final-action key name has no YAML id. RQ-40 needs a name for the audit key that records what last happened to a device. This PRD uses the words final-action key from ADR 0002 D-05 and does not invent an id. Action: S07 adds the id under a new ADR. This does not block the PRD. |
| F-3 | `prd.md` | section 2 | 40 | Section 15 lists the two terms the glossary lacks. | Section 15 lists every word that the glossary and the YAML lack, each on an Open question for S03 line. |
| F-3 | `prd.md` | section 15 gate | 607 | PASS. The version is `1.1.1` in all places. No term is defined here. | The version is `1.1.1` in all places. This PRD does not define a term. Section 15 lists every word that the glossary and the YAML lack, each on an Open question for S03 line. |
| F-3 | `prd.md` | header, Unresolved issues | 12 | Five Open questions for S03 stay open | Fifteen Open questions for S03 stay open |
| F-3 | `traceability.md` | header, Unresolved issues | 11 | Five Open questions for S03 | Fifteen Open questions for S03 |
| F-4 | `prd.md` | section 8 label table | 213 | (no row) | Counts inside the `cannot_prove` text (log lines with no correlation id, log lines that cannot be read): REAL, counted from `logs/audit.log` at the request. YAML ids: `status.code.cannot_prove.log_integrity`; `status.code.cannot_prove.rows_before_correlation_id`. |
| F-5 | `prd.md` | RQ-69 | 397 | A correlation id longer than 128 characters is refused when the audit row is written, not only when it is read. The word to store | A correlation id longer than 128 characters is refused when the audit row is written, not only when it is read. The 128 limit is PROPOSED. Owner: Team-Force. The word to store |
| F-6 | `prd.md` | RQ-40 | 334 | Every audit row written by the recommend, approval and storm routes carries a final-action key. Its value is `none` on every route in this PRD (decision D-05). | Every audit row carries a final-action key. The key records what last happened to a device. The key name is an Open question for S03. The value is `none` on every row because no route in this PRD changes a device (decision D-05). |
| F-7 | `prd.md` | RQ-54 | 366 | Once the breaker is open, the model is not called and the route answers HOLD_FOR_REVIEW at once. | After a run of failed model calls, the breaker opens. The app then stops calling the model for a while. `POST /ai/recommend/{id}` returns HOLD_FOR_REVIEW at once and does not call the model. The numbers (opens after 5 failures, stays open 30 seconds, allows 10 calls at once) are PROPOSED (N-05). Owner: Team-Force. |
| F-8 | none | none | — | — | Not applied. Waiting for a decision. |
| F-9 O-1 | `prd.md` | section 15 | 585 | (no line) | **Open question for S03:** how the page learns a `device_id` after the storm step (O-1). RQ-08 returns the raw count, the deduped count and the alarm ids. Step 2 of the demo looks up a device and needs a `device_id`. The storm response is not required to carry one. This PRD does not pick a way. Action: S07 chooses how the page gets a `device_id` and writes it in the page test (RQ-62). This does not block the PRD. |
| F-9 O-2 | `prd.md` | section 15 | 587 | (no line) | **Open question for S03:** the input and reply of `POST /approvals/{id}` (O-2). `{id}` is not defined as a device id, a recommendation id or an invocation id. The PRD does not say whether the caller sends `approver` or the server sets it from the header. The reply shape is not given. This PRD does not pick those values. Action: S07 chooses them and writes them in the approval tests (RQ-32, RQ-34). This does not block the PRD. |
| F-9 O-3 | `prd.md` | section 15 | 589 | (no line) | **Open question for S03:** the audit action words for the storm read, the recommendation and the approval, and the name and position of the final-action key (O-3). RQ-52 says S07 adds the ids under a new ADR before it ships the route. This PRD does not invent those words or a key name. Action: S07 adds the ids under a new ADR. This does not block the PRD. |
| F-9 O-4 | `prd.md` | section 10 | 406 to 411 | (no note) | **Tests S07 must change (O-4).** Four existing tests lock the behaviour that RQ-03 and RQ-68 remove. The four function names from the review are listed. |
| F-9 O-4 | `traceability.md` | after section 1 | 96 | (no note) | The same four function names. They are not acceptance tests for RQ-03 or RQ-68. |
| F-9 O-5 | `prd.md` | section 15 planned additions | 591 | The existing test `test_audit_action_words_in_main_py_all_have_an_id` fails if S07 ships an action word with no id. | That sentence, plus: Each of those additions raises the semantic layer version under the new ADR. The PRD header, `traceability.md` and the S08 hash step must then carry the new version. |
| F-9 O-5 | `prd.md` | section 15 stale text | 594, 596 | (one stale line for `semantic-layer-revision.md`) | The `1.1.0` S08 hash line and the `S05R_Decisions_Taken.md` D-07 line are named. Both files stay unedited. |
| version | `prd.md` | header | 7, 9 | v1.1. CONDITIONAL PASS. | v1.2. S06R fixes applied, round 1. Fixes F-1 to F-7, F-9. F-8 skipped. Status names the same. |
| version | `traceability.md` | header | 6, 8 | v1.1. CONDITIONAL PASS. | v1.2. S06R fixes applied, round 1. Fixes F-1 to F-7, F-9. F-8 skipped. Status names the same. |

### RQ ids touched

No RQ id was added, removed, merged or renumbered.

| RQ id | What changed | Files that cite it |
|---|---|---|
| RQ-08 | Pointer to the Open question. Return contract stays. | `prd.md` (section 6, section 9, section 10, section 14, section 15). `traceability.md` (section 1, section 2, section 3). |
| RQ-31 | Pointer to the Open question. 300 second store and cap stay. | `prd.md` (section 6, section 9, section 10, section 12 RK-14, section 13, header). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-40 | Requirement text rewritten. YAML ids, test name and design file stay. | `prd.md` (section 10, section 13 D-05). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-54 | Requirement text rewritten. YAML ids, test name and design file stay. | `prd.md` (section 10, section 11, section 13 N-05). `traceability.md` (section 1, section 3). |
| RQ-65 | Pointer to the Open question. D-07 meaning stays. | `prd.md` (section 9, section 10, section 12 RK-01, section 13). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-69 | Added PROPOSED and Team-Force on the 128 limit. | `prd.md` (section 10, section 11, section 12 RK-03, section 13 N-01). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-71 | Pointer to the Open question. Near-miss list stays PROPOSED. | `prd.md` (section 10, section 12 RK-05). `traceability.md` (section 1, section 2, section 4). |
| RQ-03 | Named in the O-4 note only. Row text stays. | `prd.md` (section 10, O-4 note, section 12). `traceability.md` (section 1, section 2, O-4 note). |
| RQ-68 | Named in the O-4 note only. Row text stays. | `prd.md` (section 9, section 10, O-4 note, section 12, section 13). `traceability.md` (section 1, section 2, section 3, section 4, O-4 note). |

### Agreement check

| Claim | Places | What this round did |
|---|---|---|
| 128 character limit | RQ-44, RQ-69, section 11, section 13 N-01, RK-03 | RQ-69 now has PROPOSED and Team-Force, same as RQ-44, section 11 and N-01. RK-03 points at RQ-69 and stays. |
| 300 second answer store | RQ-31, section 11, RK-14, section 13 | Meaning stays. RQ-31 gained an Open question pointer only. |
| Breaker numbers | RQ-54, section 11, N-05 | All three now state 5 failures, 30 seconds open, 10 calls at once, PROPOSED (N-05), owner Team-Force. |
| Open question count | `prd.md` header, `traceability.md` header, section 15 | Both headers now say fifteen. Section 15 has the fifteen lines. |
| claimed role | RQ-65, RK-01, section 13 D-07 | The words stay. RQ-65 and section 15 point to the Open question. RK-01 and D-07 keep the same words. |

### Version check

| Place | Version | Label |
|---|---|---|
| `semantic-layer/README.md` line 6 and line 69 | `1.1.1` | **Verified Fact** |
| `prd.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `traceability.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `docs/02-baseline/semantic-layer-revision.md` line 6 | `1.1.1` | **Verified Fact** |
| `prd-review.md` header | `1.1.1` | **Verified Fact** |
| ADR 0002 (newest ADR that changed the YAML) | `1.1.1`. One sentence in `metric.recommendation_latency`. No id added. | **Verified Fact** |

All six strings are equal. The status is not BLOCKED on versions.

### Checks 8a to 8g

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
unique prd ids: 73
unique trace ids: 73
duplicate prd ids: none
duplicate trace ids: none
counts equal: True
id set difference: none
```

**Verified Fact** (script, 2026-10-12). Matches the locked fact: RQ-01 to RQ-73, 73 rows.

#### 8b. YAML id lookup

```
YAML ids collected from seven files: 757
YAML ids cited in requirement rows: 462
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 173
audit action words resolved via value: [('policy.deny', 'status.code.audit_action.policy_deny'), ('policy.hold', 'status.code.audit_action.policy_hold')]
unresolved backticked id-shaped tokens: ['policy.py']
```

**Verified Fact** (script, 2026-10-12). 757 ids match the locked fact. `policy.deny` and `policy.hold` resolve through `status.code.audit_action.*`. `record.read` is the `value:` of `status.code.audit_action.record_read`. `policy.py` is a file name, not a YAML id.

#### 8c. Row-by-row compare

```
mismatches: none
```

**Verified Fact** (script, 2026-10-12). YAML ids, test name, existing-or-planned status and design file match on all 73 rows.

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 44
```

**Verified Fact** (script, 2026-10-12). Matches the locked fact: 29 exist, 44 planned for S07.

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
.........................................                                [100%]
41 passed in 2.84s
```

**Verified Fact** (`python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`, 2026-10-12). Matches the locked fact.

#### 8f. Existing PRD tests

`logs/audit.log` had 240 lines before the run. After the run it had 241 lines. After restore it had 240 lines.

```
40 passed, 1 skipped, 61 warnings in 5.54s
```

The skip is `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination` (RQ-59). **Verified Fact.** Matches the locked fact: 40 passed, 1 skipped, 240 audit lines before and after.

#### 8g. git status

Before:

```
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md
 D "Archive/Project Intent segments fed to stages/Project_Intent - Appendix B.md"
 M Project_Acronyms.md
 M playbook/README.md
 M playbook/S06-prd.md
 M playbook/S06R-prd-review.md
 M playbook/STATUS.md
 M transcript/chat_transcript.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md
?? 06-telecom-service-network-incident-ops/docs/prd/
?? "Project_Intent - Appendix B.md"
?? playbook/S06F-prd-fixes.md
```

After:

```
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md
 D "Archive/Project Intent segments fed to stages/Project_Intent - Appendix B.md"
 M Project_Acronyms.md
 M playbook/README.md
 M playbook/S06-prd.md
 M playbook/S06R-prd-review.md
 M playbook/STATUS.md
 M transcript/chat_transcript.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md
?? 06-telecom-service-network-incident-ops/docs/prd/
?? "Project_Intent - Appendix B.md"
?? playbook/S06F-prd-fixes.md
```

**Verified Fact.** The folder `docs/prd/` was already untracked. This stage wrote `prd.md`, `traceability.md` and `prd-fixes.md` inside it. No other file gained a new difference. The other rows were already present before this stage started.

### Done test

In `prd.md` RQ-01 the YAML id `status.code.health.ok` was changed to `status.code.health.does_not_exist`. Check 8b then printed:

```
unresolved cited ids: [('RQ-01', 'status.code.health.does_not_exist')]
```

The id was restored. Check 8b then printed:

```
unresolved cited ids: none
```

**Verified Fact** (script, 2026-10-12).

### Map from FAIL rows to fixes

No row is marked PASS. The next S06R does that.

| FAIL row in the review | Fix numbers | Edits that address it |
|---|---|---|
| P2 | F-1, F-2, F-3 | Four Open question lines for the missing words (section 15 lines 571 to 577). Three Open question lines for the planned fields (lines 579 to 583). Section 2 line 40 and the gate row at line 607 now name that list. |
| P7 | F-4 | Section 8 label table line 213. The `cannot_prove` counts now have a REAL row. |
| P8 | F-5 | RQ-69 line 397 now has PROPOSED and Team-Force. |
| P11 | F-6, F-7 | RQ-40 line 334 rewritten. RQ-54 line 366 rewritten. RQ-72 was already PASS in the review and was not changed. |
| P12.6 (observation on the gate row; the row itself was PASS) | F-3 | Gate row at line 607 no longer says "No term is defined here" as if that closed P2. |
| P12.8 | F-1, F-2 | Same Open question lines as P2. |


## Round 2, 2026-10-12

### Fix source

| Field | Value |
|---|---|
| Path | `docs/prd/prd-review.md` |
| Header date and version | 2026-10-12, v2.0 of this review. It replaces v1.0 (round 1, BLOCKED). Semantic layer version read from `semantic-layer/README.md`: `1.1.1`. |
| Stage status | **BLOCKED.** P2 is FAIL. P11 and P12.4 are also FAIL, and P12.8 repeats P2. P1, P3, P4, P5, P6, P7, P8, P9, P10 and P13 are PASS. |

### Fixes required (copied word for word)

| # | For | Fix needed |
|---|---|---|
| F-1 | P2, P12.8 | At `prd.md` lines 316 (RQ-31) and 466 (RK-14), replace "the output policy" with words the YAML has. Example: "the same checks as a fresh answer: the answer shape (`policy.output_schema`), the forbidden-value check (RQ-70) and the command phrases (RQ-30)". Or write an "Open question for S03:" line that names "output policy" and what RQ-31 needs it for, and do not define it. Either choice clears P2. ADR 0003 line 46 and `Risk Management.md` lines 219 and 221 keep the phrase. S06F may not edit them, and the PRD stays consistent with them in meaning. |
| F-2 | P11, RQ-54 | Rewrite the last sentence of RQ-54 (line 366) so the 10 is a separate limit. Example: "The app also lets at most 10 model calls run at the same time. The numbers (5 failures, 30 seconds open, 10 calls at the same time) are PROPOSED (N-05). Owner: Team-Force." Change section 11 line 426 and N-05 (line 535) to the same words. The test name and YAML ids in `traceability.md` stay. |
| F-3 | P12.4 | At `prd.md` line 74, add the files that show the claim: `apps/api/main.py`, `apps/api/services/policy.py`, `tests/ai/test_guardrails.py`, `apps/api/services/audit_query.py`. At lines 245 and 257, label the sentence about the change tool and the validated change. Use **Verified Fact** with `field.policy_input.change_plan_ok` and `apps/api/main.py` (no change route), or use **Inference**. |
| F-4 | P3 (observation, optional) | Carried from round 1 as F-8. Quote the approval point for the six uses that section 7 skips, or state that section 3 is the whole list for them. `S06-prd.md` step 3 asks for a quote for every AI use. |
| F-5 | Section 7, R2-2 | Add RQ-70 and RQ-71 to the requirement list of `POST /ai/recommend/{id}` in `prd.md` line 232, in the step 3 row at line 124, and in `traceability.md` section 3 (line 158). |

### Other findings named by a fix (copied word for word)

F-5 names R2-2. No other fix names a row of "Other findings".

| # | Finding | Evidence | Impact | Label |
|---|---|---|---|---|
| R2-2 | The route tables leave RQ-70 and RQ-71 out of the recommend route. Both rows are about the answer from `POST /ai/recommend/{id}`. The same tables also list no route for RQ-69 and RQ-72. | `prd.md` line 232 and line 124 say "RQ-18 to RQ-31". `traceability.md` line 158 says the same. RQ-70 is at line 398 and RQ-71 at line 399. | A builder who lists the recommend route requirements from the route table misses the answer check and the near-miss check. | **Verified Fact** for the ranges. **Inference** for the impact. |

The review lists no FAIL row without a fix. P2 and P12.8 are covered by F-1. P11 is covered by F-2. P12.4 is covered by F-3.

### Decisions for this round

Pasted in the prompt (the exact block):

```
F-1: use the YAML words. Do not write an Open question line. In RQ-31 (prd.md section 10), replace the second sentence with: "The second answer comes from the stored answer. It goes through the same checks as a fresh answer: the answer shape (`policy.output_schema`, RQ-25), the check for a forbidden field name or value (RQ-70) and the command phrase checks (RQ-30, RQ-71). It returns HOLD_FOR_REVIEW with the same sentence, and its audit row says no model ran." In RQ-31, replace "The store never holds a BLOCK or HOLD answer." with "The store holds an answer only when it has text and passed those checks. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence)." In RK-14 write: "The store stays. It never holds an answer that stopped with no text. A stored answer goes through the same checks again (RQ-31, ADR 0003)." In the section 13 ADR 0003 table, row RQ-31, write: "The 300 second answer store stays. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). The cap is PROPOSED and has no number." Owner decision: ADR 0003's words "BLOCK or HOLD" mean an answer that stopped with no text. A healthy recommend answer is HOLD_FOR_REVIEW with a sentence (RQ-18), and the RQ-31 test needs the store to hold it. This keeps the meaning of ADR 0003. Do not use the words near-miss phrase or near-miss list in the new text. Afterwards, search prd.md and traceability.md for "output policy" and "BLOCK or HOLD". No hit may stay, except the quoted ADR 0003 row if it keeps that wording.
F-2: apply, with these exact words. Replace the whole text of RQ-54 with: "The app stops calling the model in two cases. In the first case the breaker is open. It opens after 5 failed model calls in a row and stays open 30 seconds. Then it lets one test call through. A success closes it. A failure opens it again. In the second case 10 model calls are already running, and a new request is refused. In both cases `POST /ai/recommend/{id}` returns HOLD_FOR_REVIEW with no text at once and does not call the model. The numbers (5 failures in a row, 30 seconds open, 10 calls at the same time) are PROPOSED (N-05). Owner: Team-Force." In section 11, Breaker row, write: "Opens after 5 failures in a row and stays open 30 seconds. At most 10 model calls run at the same time." In section 13, N-05, write: "Breaker: 5 failures in a row, 30 seconds open. In-flight limit: 10 calls at the same time." Keep the RQ-54 YAML ids, the test name and the design file in both files. Do not add tests to the test cell.
F-3: use Verified Fact for the change tool claim, and say what is Unknown. At prd.md line 74 (reason 2), write: "The record route and the summary route (`apps/api/main.py`), the policy tables (`apps/api/services/policy.py`), the guardrail tests (`tests/ai/test_guardrails.py`) and the audit read route (`apps/api/services/audit_query.py` and `apps/api/main.py`) are in the repo." At the two sentences about the change tool and the validated change (the Any EXECUTE route table row and the "Rule for EXECUTE" paragraph), write: "**Verified Fact.** The code that builds the policy input (`apps/api/services/policy.py`) sets `change_plan_ok` to false (`field.policy_input.change_plan_ok`). `apps/api/main.py` has four routes and none of them changes a device. **Unknown.** What "validated" means for a change." Keep the four gates and the rule that no EXECUTE route is built.
F-4: leave alone.
F-5: apply. Add RQ-70 and RQ-71 to the requirement list of `POST /ai/recommend/{id}` in the prd.md routes section, in the step 3 row of section 6, and in traceability.md section 3. Use the same range or list style the file already uses. Do not add or renumber a requirement row.
```

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| F-1 | apply | The Decisions block gives exact words for four places. It picks the YAML words and no Open question line. The block also says what "BLOCK or HOLD" means in ADR 0003. No ADR is edited. |
| F-2 | apply | The Decisions block gives exact words for RQ-54, section 11 and N-05. The numbers stay PROPOSED (N-05). Owner: Team-Force (`operating-contract.md` row 10). No number is new. |
| F-3 | apply | The Decisions block picks Verified Fact and gives the words. I checked the claim first. `apps/api/services/policy.py` line 396 sets `"change_plan_ok": False` in the policy input. `apps/api/main.py` has four route decorators (lines 64, 68, 82, 112). **Verified Fact.** |
| F-4 | left alone | The Decisions block says leave alone. It is optional. Not edited. |
| F-5 | apply | The Decisions block says apply, in the same list style. No requirement row is added or renumbered. |

### Edit list

Line numbers are the lines after the edit. **Verified Fact.**

| Fix | File | Requirement id or section | Line | Old text | New text |
|---|---|---|---|---|---|
| F-1 | `prd.md` | RQ-31 | 316 | The second answer comes from the stored answer, passes the output policy again, and its audit row says no model ran. | The second answer comes from the stored answer. It goes through the same checks as a fresh answer: the answer shape (`policy.output_schema`, RQ-25), the check for a forbidden field name or value (RQ-70) and the command phrase checks (RQ-30, RQ-71). It returns HOLD_FOR_REVIEW with the same sentence, and its audit row says no model ran. |
| F-1 | `prd.md` | RQ-31 | 316 | The store never holds a BLOCK or HOLD answer. | The store holds an answer only when it has text and passed those checks. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). |
| F-1 | `prd.md` | section 12, RK-14 | 466 | The store stays. It never holds BLOCK or HOLD. The output policy runs again (RQ-31, ADR 0003). | The store stays. It never holds an answer that stopped with no text. A stored answer goes through the same checks again (RQ-31, ADR 0003). |
| F-1 | `prd.md` | section 13, ADR 0003 table, row RQ-31 | 498 | The 300 second answer store stays. It never holds BLOCK or HOLD. The cap is PROPOSED and has no number. | The 300 second answer store stays. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). The cap is PROPOSED and has no number. |
| F-2 | `prd.md` | RQ-54 | 366 | After a run of failed model calls, the breaker opens. The app then stops calling the model for a while. `POST /ai/recommend/{id}` returns HOLD_FOR_REVIEW at once and does not call the model. The numbers (opens after 5 failures, stays open 30 seconds, allows 10 calls at once) are PROPOSED (N-05). Owner: Team-Force. | The app stops calling the model in two cases. In the first case the breaker is open. It opens after 5 failed model calls in a row and stays open 30 seconds. Then it lets one test call through. A success closes it. A failure opens it again. In the second case 10 model calls are already running, and a new request is refused. In both cases `POST /ai/recommend/{id}` returns HOLD_FOR_REVIEW with no text at once and does not call the model. The numbers (5 failures in a row, 30 seconds open, 10 calls at the same time) are PROPOSED (N-05). Owner: Team-Force. |
| F-2 | `prd.md` | section 11, Breaker row | 426 | Opens after 5 failures, stays open 30 seconds, allows 10 calls at once | Opens after 5 failures in a row and stays open 30 seconds. At most 10 model calls run at the same time. |
| F-2 | `prd.md` | section 13, N-05 | 535 | Breaker: 5 failures, 30 seconds open, 10 calls at once | Breaker: 5 failures in a row, 30 seconds open. In-flight limit: 10 calls at the same time. |
| F-3 | `prd.md` | section 4, reason 2 | 74 | The record route, the summary route, the policy tables, the guardrail tests and the audit read route are in the repo. | The record route and the summary route (`apps/api/main.py`), the policy tables (`apps/api/services/policy.py`), the guardrail tests (`tests/ai/test_guardrails.py`) and the audit read route (`apps/api/services/audit_query.py` and `apps/api/main.py`) are in the repo. |
| F-3 | `prd.md` | section 9, row "Any EXECUTE route" | 245 | No route sets `change_plan_ok`, and the repo has no change tool and no way to check a change. So no EXECUTE route is built. | **Verified Fact.** The code that builds the policy input (`apps/api/services/policy.py`) sets `change_plan_ok` to false (`field.policy_input.change_plan_ok`). `apps/api/main.py` has four routes and none of them changes a device. **Unknown.** What "validated" means for a change. So no EXECUTE route is built. |
| F-3 | `prd.md` | section 9, "Rule for EXECUTE" | 257 | A reversible validated change does not exist. So the rule keeps the route out. | **Verified Fact.** The code that builds the policy input (`apps/api/services/policy.py`) sets `change_plan_ok` to false (`field.policy_input.change_plan_ok`). `apps/api/main.py` has four routes and none of them changes a device. **Unknown.** What "validated" means for a change. So the rule keeps the route out. |
| F-5 | `prd.md` | section 9, route table, row `POST /ai/recommend/{id}` | 232 | RQ-18 to RQ-31 | RQ-18 to RQ-31, RQ-70 and RQ-71 |
| F-5 | `prd.md` | section 6, step 3 row | 124 | RQ-18 to RQ-31 | RQ-18 to RQ-31, RQ-70 and RQ-71 |
| F-5 | `traceability.md` | section 3, row `POST /ai/recommend/{id}` | 158 | RQ-18 to RQ-31 | RQ-18 to RQ-31, RQ-70 and RQ-71 |
| version | `prd.md` | header, Date / version and Status | 7, 9 | v1.2. S06R fixes applied, round 1. Fixes F-1 to F-7, F-9. F-8 skipped. / CONDITIONAL PASS. S06R fixes applied, round 1. | v1.3. S06R fixes applied, round 2. Fixes F-1, F-2, F-3, F-5. F-4 left alone. / CONDITIONAL PASS. S06R fixes applied, round 2. |
| version | `prd.md` | header, Status and Unresolved issues | 9, 12 | F-8 is optional and was not applied. | F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. |
| version | `traceability.md` | header, Date / version and Status | 6, 8 | v1.2. S06R fixes applied, round 1. Fixes F-1 to F-7, F-9. F-8 skipped. / CONDITIONAL PASS. S06R fixes applied, round 1. | v1.3. S06R fixes applied, round 2. Fixes F-1, F-2, F-3, F-5. F-4 left alone. / CONDITIONAL PASS. S06R fixes applied, round 2. |
| version | `traceability.md` | header, Status and Unresolved issues | 8, 11 | F-8 is optional and was not applied. | F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. |

The `traceability.md` section 1 rows for RQ-31 and RQ-54 did not change. Both rows hold only YAML ids, a test name, a status and a design file. The Decisions block says to keep the RQ-54 ids, test name and design file. The RQ-31 test name still describes the check ("no model call for the second identical request"). The new RQ-31 text adds checks that the same planned test can cover. S07 may add more test checks later.

The PRD completion-gate section (section 15, "Gate check") makes no statement about the output policy, the breaker or the EXECUTE gates. No gate statement needed a change. The gate row for the version stays at `1.1.1`.

### RQ ids touched

No RQ id was added, removed, merged or renumbered.

| RQ id | What changed | Files that cite it |
|---|---|---|
| RQ-31 | Second sentence and store sentence rewritten with the YAML words. The 300 second store, the stale-flag rule and the PROPOSED cap stay. YAML ids, test name and design file stay. | `prd.md` (section 6, section 9, section 10, section 12 RK-14, section 13, header). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-54 | Text replaced. Breaker and in-flight limit are now two cases. YAML ids, test name and design file stay. | `prd.md` (section 10, section 11, section 13 N-05). `traceability.md` (section 1, section 3). |
| RQ-70 | Added to the route lists of `POST /ai/recommend/{id}`. Row text stays. Cited by the new RQ-31 text. | `prd.md` (section 6, section 9, section 10, section 12). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-71 | Added to the route lists of `POST /ai/recommend/{id}`. Row text stays. Cited by the new RQ-31 text. | `prd.md` (section 6, section 9, section 10, section 12 RK-05, section 15). `traceability.md` (section 1, section 2, section 3, section 4). |
| RQ-25, RQ-30 | Cited by the new RQ-31 text only. Row text stays. | `prd.md` (section 10). `traceability.md` (section 1, section 2, section 3). |
| RQ-18 | Cited in the RQ-31 decision note (healthy recommend answer). Row text stays. | `prd.md` (section 10). `traceability.md` (section 1, section 2, section 3). |

### Agreement check

| Claim | Places searched | What this round did |
|---|---|---|
| The answer store never holds an answer that stopped with no text | RQ-31 (316), RK-14 (466), section 13 ADR 0003 row (498), header Unresolved issues (12), `traceability.md` section 4 (OB-01) | The three places that said "BLOCK or HOLD" now say the same new words. The header line and `traceability.md` section 4 hold no BLOCK or HOLD wording and stay. |
| A stored answer goes through the same checks again | RQ-31, RK-14 | Both use the words "same checks". The old phrase "output policy" has no hit left in `prd.md` or `traceability.md`. |
| Breaker numbers and in-flight limit | RQ-54 (366), section 11 (426), N-05 (535) | All three say 5 failures in a row, 30 seconds open, and 10 calls at the same time. All three keep PROPOSED, N-05 and Team-Force. Line 437 (failure table, "Breaker open ... 202 at once, model not called") holds no number and stays. |
| The change tool and the validated change | Section 4 reason 4 (line 76), section 9 EXECUTE row (245), Rule for EXECUTE (257), section 14 (the demo) | Line 245 and line 257 now carry the same Verified Fact and Unknown sentences. The four gates and the rule that no EXECUTE route is built stay. Reason 4 in section 4 says the four gates "are not all present" and holds no claim about a change tool, so it stays. |
| Route requirement lists for `POST /ai/recommend/{id}` | Section 6 step 3 (124), section 9 route table (232), `traceability.md` section 3 (158) | All three now say "RQ-18 to RQ-31, RQ-70 and RQ-71". No other place lists the range for this route. |
| Version and status | `prd.md` header, `traceability.md` header | Both say v1.3, round 2, fixes F-1, F-2, F-3, F-5, F-4 left alone. Both keep the semantic layer version `1.1.1`. |

### Version check

| Place | Version | Label |
|---|---|---|
| `semantic-layer/README.md` (Date / version and "Version" section) | `1.1.1` | **Verified Fact** |
| `prd.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `traceability.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `docs/02-baseline/semantic-layer-revision.md` header (line 6) | `1.1.1` ("The current version is `1.1.1`") | **Verified Fact** |
| `prd-review.md` header (v2.0) | `1.1.1` | **Verified Fact** |
| ADR 0002 (newest ADR that changed the YAML) | `1.1.1`. One sentence in `metric.recommendation_latency`. ADR 0003 added no YAML id. | **Verified Fact** |

All six strings are equal. The status is not BLOCKED on versions. Document versions: `prd.md` v1.2 to v1.3. `traceability.md` v1.2 to v1.3. Both are the same.

### Checks 8a to 8g

All outputs are from 2026-10-12, run after the edits. The script for 8a to 8d is a temporary Python file and is not part of the repo. **Verified Fact.**

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
duplicate prd ids: none
duplicate trace ids: none
counts equal: True
id set difference: none
```

Matches the locked fact (RQ-01 to RQ-73). RQ-31 appears a second time inside the ADR 0003 table of section 13. That row repeats a decision and is outside section 10, so the count does not include it.

#### 8b. YAML id lookup

```
YAML ids collected from seven files: 757
YAML ids cited in requirement rows (distinct): 122
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 174
audit action words resolved via value: [('policy.deny', 'status.code.audit_action.policy_deny'), ('policy.hold', 'status.code.audit_action.policy_hold'), ('record.read', 'status.code.audit_action.record_read')]
unresolved backticked id-shaped tokens: ['events.jsonl']
```

757 ids match the locked fact. `events.jsonl` is a file name, not a YAML id. `policy.py` is excluded by the same rule. The tokens in the text I changed are `policy.output_schema` and `field.policy_input.change_plan_ok`. Both are `id:` lines in `semantic-layer/ai-context-policy.yaml`. The script also found no other new unresolved token. **Verified Fact.**

#### 8c. Row-by-row compare

```
mismatches: none
```

YAML ids, test name, existing-or-planned status and design file match on all 73 rows.

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 44
```

Matches the locked fact: 29 exist, 44 are planned for S07.

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
.........................................                                [100%]
41 passed in 3.24s
```

(`python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`.) Matches the locked fact.

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines. After the test run it had 241 lines. After the restore it had 240 lines. The test command named the 29 existing test ids that `prd.md` section 10 lists.

```
40 passed, 1 skipped, 60 warnings in 8.18s
SKIPPED [1] policy\tests\test_policy_python.py:577: opa binary not on PATH
```

Matches the locked fact: 40 passed, 1 skipped. The skip is the `opa` test (RQ-59). I ran the command a second time to read the skip reason and restored the log again. It had 240 lines at the end.

#### 8g. git status

Before (taken before the first edit):

```
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md
 D "Archive/Project Intent segments fed to stages/Project_Intent - Appendix B.md"
 M Project_Acronyms.md
 M playbook/README.md
 M playbook/S06-prd.md
 M playbook/S06R-prd-review.md
 M playbook/STATUS.md
 M transcript/chat_transcript.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md
?? 06-telecom-service-network-incident-ops/docs/prd/
?? "Project_Intent - Appendix B.md"
?? playbook/S06F-prd-fixes.md
```

After (taken after the last edit): the output is line for line the same (`Compare-Object` found no difference).

`docs/prd/` was already untracked as a whole folder, so the three files this stage edited (`prd.md`, `traceability.md`, `prd-fixes.md`) do not add a line. I confirmed the edit scope another way: the only files I wrote are those three. `logs/audit.log` was restored to its 240 lines. The files that already appear in the status (for example `.pytest_cache` and `__pycache__` files, and `transcript/chat_transcript.md`) were already present. Test runs touch the cache files. I do not count them as a difference. The chat transcript is written by the chat-transcript rule after this reply. It was already marked as modified before this stage began.

#### F-1 search result

```
== "output policy", case-insensitive, prd.md and traceability.md ==
(no hit)
== "BLOCK or HOLD" as a whole phrase (word boundary) ==
(no hit)
== "BLOCK or HOLD" as a plain substring ==
prd.md:124:BLOCK or HOLD_FOR_REVIEW wit
```

The one plain-substring hit is line 124 (section 6, step 3). The text there is "A stop returns BLOCK or HOLD_FOR_REVIEW with no text." That is the full outcome word HOLD_FOR_REVIEW, written as the outcome name. It is not the ADR 0003 short form "BLOCK or HOLD". It also says the same thing as the new text of RQ-31: a stop with no text. So the line stays. The ADR 0003 file itself and `Risk Management.md` keep their old wording. This stage may not edit them. The meaning is the same, as the owner decision says.

The words "near-miss phrase" and "near-miss list" do not appear in any of the new text. They stay only in the old RQ-71 row (line 399), RK-05 (line 457) and the Open question line (line 573).

### Done test

In `prd.md` RQ-01 the YAML id `status.code.health.ok` was changed to `status.code.health.does_not_exist`. Check 8b then printed:

```
unresolved cited ids: [('RQ-01', 'status.code.health.does_not_exist')]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash of the copy (`6AF2FD4E4D5439A5ECA770477665C0F8570D85714BE75ED1E098627247E535B1`). Check 8b then printed:

```
unresolved cited ids: none
```

**Verified Fact.**

### Map from FAIL rows to fixes

No row is marked PASS. The next S06R does that.

| FAIL row in the review | Fix numbers | Edits that address it |
|---|---|---|
| P2 | F-1 | RQ-31 (line 316) and RK-14 (line 466) now use the YAML words: the answer shape `policy.output_schema` (RQ-25), the forbidden-value check (RQ-70) and the command phrase checks (RQ-30, RQ-71). Section 13 row RQ-31 (line 498) uses the new "answer that stopped with no text" words. No hit for "output policy" remains. |
| P11 | F-2 | RQ-54 (line 366) now names two cases: the open breaker, and 10 calls already running. Section 11 (line 426) and N-05 (line 535) use the same words. The numbers stay PROPOSED (N-05). Owner: Team-Force. |
| P12.4 | F-3 | Section 4 reason 2 (line 74) names the files. Section 9 lines 245 and 257 carry a Verified Fact with `field.policy_input.change_plan_ok` and `apps/api/main.py`, and an Unknown for what "validated" means. |
| P12.8 | F-1 | Same edits as P2. |
| R2-2 (other finding, named by F-5) | F-5 | RQ-70 and RQ-71 were added to the route lists at `prd.md` lines 124 and 232 and `traceability.md` line 158. |

## Round 3, 2026-10-13

### Fix source

| Field | Value |
|---|---|
| Path | `docs/prd/prd-review.md` |
| Header date and version | 2026-10-13, v3.0 of this review. It replaces v2.0 (round 2, BLOCKED). Semantic layer version read from `semantic-layer/README.md`: `1.1.1`. |
| Stage status | **PASS.** No row is FAIL. P1 to P13 are PASS. |

### Fixes required (copied word for word)

Fixes required: None

The fixes come from the "Decisions for this round" block below. Each line of that block is one fix. R3-1 to R3-8 are rows of "Other findings" in the review. R3-9 is not in the review. The owner raised R3-9 after the review.

### Other findings named by the Decisions block (copied word for word)

The Decisions block names R3-1 to R3-8. The review lists them in its section 7.

| # | Finding | Evidence | Impact | Label |
|---|---|---|---|---|
| R3-1 | **Needs an owner answer before S07.** The words of RQ-31 differ from ADR 0003 and from the design file RQ-31 cites. ADR 0003 says "S07 never stores a BLOCK or HOLD answer". `docs/12-finops/optimization-backlog.md` line 124 says an answer is stored "only when the outcome is `RECOMMEND_ONLY`" and "a `HOLD_FOR_REVIEW`... [is] never stored". RQ-18 says RECOMMEND_ONLY is not a result of `POST /ai/recommend/{id}`, so under those two files nothing from that route could be stored, and the RQ-31 test could not pass. The PRD (line 316) stores an answer that has text and passed the same checks as a fresh answer. The owner chose that reading in S06F round 2. It is written in `playbook/S06F-prd-fixes.md` line 121 and `prd-fixes.md` round 2. It is not in ADR 0003, in `optimization-backlog.md`, or in the PRD itself. `playbook/S06R-prd-review.md` lines 47 and 66 still carry the old words. | `prd.md` lines 316, 466, 498; `ADR/0003` line 46; `optimization-backlog.md` lines 24 and 124; `S06F-prd-fixes.md` line 121; `S06R-prd-review.md` lines 47, 66 | An S07 builder who opens the cited design file gets the opposite rule. A later review that reads the locked fact word for word marks P13 FAIL. The second model in S08 gets the PRD and the YAML only, so it follows the PRD. | **Verified Fact** for the lines. **Inference** for the impact. |
| R3-2 | RQ-08 and RQ-09 do not say whether a flagged row counts in the deduped count. RQ-09 says a flagged row is listed with its flag word and "is not counted as an incident candidate". The storm route returns no incident, so that sentence gives no rule for the count. RQ-08 says only that a blank-key row is left out. The worked example (`STO-00005`) has no flagged row. In the data, 166 of 354 alarm rows are flagged and 1 more is unreadable. | `prd.md` lines 284, 285, 217 to 219; `alarms.csv`; `metrics.yaml` line 142 (the formula does not mention flags) | Two builders will count differently on a real storm, and the S08 comparison will show a gap that the PRD caused. | **Verified Fact** for the text and the counts. **Inference** for the impact. |
| R3-3 | Stale lines in files this review and S06F may not edit. (a) `docs/prd/Risk Management.md` line 95 says "The storm, recommend and approval routes already refuse a call with no header" and labels it Verified Fact. Those three routes do not exist. `main.py` has four routes. (b) `S05R_Decisions_Taken.md` line 26 counts 14 deferred items and lists D-07, while its line 11 says D-07 is decided in ADR 0003. (c) `semantic-layer-revision.md` line 442 says "S06 writes `1.1.0` into the PRD header. S08 hashes the tree at `1.1.0`", and line 8 says 14 items stay deferred. Its line 6 says the current version is `1.1.1`. (d) `playbook/S07-application-and-demo.md` line 36 lists RECOMMEND_ONLY as a result of `/ai/recommend`, and line 37 says the approval takes "a reason". The PRD says HOLD_FOR_REVIEW (RQ-18) and no reason field (section 15). (e) `Risk Management.md` lines 219 to 223 and ADR 0003 line 46 keep the phrase "output policy". | The files and lines named | S07 and S08 can receive a version note that says `1.1.0` or a route list that disagrees with the PRD. The PRD names (b), (c) and (d) in section 15 ("Stale text found while writing"). | **Verified Fact** for the lines. **Inference** for the risk. |
| R3-4 | Section 7 quotes the approval point for 5 of the 11 AI uses. The other six (order qualification, retry and rollback, alarm dedupe, correlation, topology lookup, remediation validation) have pick and agency in section 3. Two of them have an approval point that names a person: for dedupe and correlation, the `noc_operator` decides whether the group becomes one incident. `playbook/S06-prd.md` line 42 says "for every AI use". The owner left this alone twice (round 1 F-8, round 2 F-4). | `prd.md` lines 136 to 147; `ai-qualification.md` column "Human approval point"; `S06-prd.md` line 42 | None for a builder. The PRD says section 3 is not the whole list only by omission. | **Verified Fact.** |
| R3-5 | Step 5 of the workflow uses the verb "review", which is not one of the four agency verbs (analyse, recommend, decide, execute). Its persona is `role.admin`, which the PRD says is an API role with no persona. Step 6 has the persona "none" because no one takes it. The route table at line 234 repeats "review". | `prd.md` lines 115 to 127 and 234; section 5, row `role.admin` | None for a builder. A strict reader of "each step carries a verb and a persona" finds two steps that do not. The reading of audit rows is `analyse` in the agency list. | **Verified Fact** for the text. **Inference** for the reading. |
| R3-6 | Three design points stay open by owner decision: how the page learns a `device_id` after the storm step, the input and reply of `POST /approvals/{id}` (including what `{id}` is), and the audit action words and the final-action key name. RQ-34 leaves the lookup of the shown recommendation to S07. | `prd.md` lines 326, 585, 587, 589 | The S07 builder and the S08 second model will choose differently, so the S08 comparison will compare two designs. The first one is S07's guess. | **Verified Fact** for the text. **Inference** for the impact. |
| R3-7 | Small plain-speech and consistency items. (a) RQ-06 and RQ-05 name `mgmt_ip` and `credential_profile` and do not say what they hold. (b) The section 8 label table (lines 203 to 216) has no row for `metric.ai_outcome_count` and `metric.audit_completeness`, which section 14 says the demo shows. RQ-63 cites neither id. (c) Gate row 3 at line 607 has no PASS or FAIL word. (d) "Healthy call" is not in the glossary. (e) The section 5 route table says "No header gives 403" for three routes and not for the storm, approval and audit rows. RQ-11 and rule `rule.no_default_role` cover the storm route. | `prd.md` lines 104 to 111, 203 to 216, 273, 541 to 557, 607 | None blocks a build. Each can mislead a reader once. | **Verified Fact** for the text. |
| R3-8 | RQ-54 now says the breaker opens and the in-flight limit refuses at 10. Both return HOLD_FOR_REVIEW. The failure table in section 7 (lines 162 to 172) lists "Model raises an error, or the breaker is open" and has no row for "10 calls already running". The audit reason for the in-flight case is not named. | `prd.md` lines 162 to 172 and 366; `breaker.py` (`REFUSED_IN_FLIGHT`) | S07 must choose which `failmode` id the in-flight refusal writes. `failmode.model_unreachable` is the nearest id. | **Verified Fact** for the text. **Inference** for the nearest id. |

R3-9 has no row in the review. It is a fix that the owner raised after the review.

### Decisions for this round

Pasted in the prompt (the exact block):

```
Round 3. The review says "Fixes required: None". The fixes below close "Other findings" R3-1 to R3-8, and R3-9, which the owner raised after the review. Apply every line. Edit only prd.md, traceability.md and prd-fixes.md. The "Owner edits outside this stage" line lists edits that this stage does not make.

R3-1 (answer store of RQ-31). Apply. Decision: keep the owner reading from round 2. In ADR 0003 the words "BLOCK or HOLD" mean an answer with no text.
  a) RQ-31. Replace the two sentences "The store holds an answer only when it has text and passed those checks. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence)." with: "The store holds an answer only when it has text and passed those checks. A HOLD_FOR_REVIEW answer that has a sentence is stored. A BLOCK, a HOLD_FOR_REVIEW with no sentence, a timeout and a bad answer are never stored. The store belongs to POST /ai/recommend/{id} only. POST /ai/summarize/{id} neither reads it nor writes it. An entry is found by prompt_hash alone. It lives 300 seconds, counted from the moment it was stored. A stored answer that fails a check is treated like a fresh answer that fails the same check (RQ-25, RQ-30, RQ-70, RQ-71) and is removed from the store."
  b) RK-14 and the section 13 row for RQ-31. Add the sentence "It serves POST /ai/recommend/{id} only." Keep the rest.
  c) prd.md header, row "Unresolved issues". Delete the sentence "Whether the answer store of RQ-31 needs the route name in its key is Unknown." Make the same deletion in traceability.md if the sentence is there.
  d) Section 15, list "Stale text found while writing". Add two bullets. Bullet 1: "docs/ADR/0003-s06-risk-recommendations.md line 46 says S07 never stores a BLOCK or HOLD answer. Read it as an answer with no text. The ADR is outside this stage." Bullet 2: "docs/12-finops/optimization-backlog.md line 124 says an answer is stored only when the outcome is RECOMMEND_ONLY. RQ-31 stores a HOLD_FOR_REVIEW recommendation that has a sentence. The file is outside this stage."
  e) Do not edit ADR 0003 or optimization-backlog.md.

R3-2 (flagged rows and the deduped count). Apply. Decision: a flagged row stays in every count and every list. The flag only stops it being an incident candidate.
  a) RQ-08. Replace the whole Requirement cell with: "GET /alarms/storms/{storm_batch_id} returns the raw count, the deduped count, the flagged count and the rows. Raw count: every row with that storm_batch_id. Deduped count: the number of different non-blank dedupe_key values among those rows. Flagged count: the number of rows that carry the flag word last_seen_before_first_seen or times_unreadable. The reply lists each row with alarm_id, device_id, dedupe_key and its flag word (empty when none). A flagged row counts in the raw count. It also counts in the deduped count when its dedupe_key is not blank. A row with a blank dedupe_key is held aside, listed apart from the other rows, counted in the raw count only, and left out of the deduped count. No row is removed from a list because of a flag. The words raw count and flagged count are an Open question for S03."
  b) RQ-09. Replace the whole Requirement cell with: "A row whose last_seen_at is before first_seen_at, or whose time cannot be read, carries its flag word in the reply and counts in the flagged count. It still counts in the raw count and, when its dedupe_key is not blank, in the deduped count (RQ-08). It is not counted as an incident candidate. Example from data/synthetic/alarms.csv: storm STO-00019 has two rows (file lines 20 and 355), both ALA-00019 with dedupe_key DED-00019, both flagged. Its raw count is 2, its deduped count is 1 and its flagged count is 2. Storm STO-00002 has one row, flagged. Its raw count is 1, its deduped count is 1 and its flagged count is 1." Before you write the example, read those rows in alarms.csv. If they differ, the file wins, and you change the numbers to match it.
  c) Section 6, step 1, "What happens" cell. Replace "Flagged rows are listed apart." with "A flagged row keeps its flag word in the list and counts in the flagged count." Search the whole PRD for "listed apart" and "flagged" and make every hit agree with a) and b).
  d) Keep the Open question for S03 line about the words raw count and flagged count. The words still have no YAML id.
  e) Add no row and no test name. The planned tests of RQ-08 and RQ-09 keep their names. Their expected values follow a) and b).

R3-6 (three design points). Apply. Decision: the PRD names every item below. All new names are PROPOSED. Owner: Team-Force. S07 adds the YAML ids under a new ADR.
  a) How the page gets a device id. In RQ-08 the reply rows carry device_id (R3-2 a). RQ-62: replace "look up a device" with "look up a device: the page lists the different device_id values from the storm reply, the operator picks one, and the page uses that value as {id} in the lookup (GET /records/{id}), the recommendation (POST /ai/recommend/{id}) and the decision (POST /approvals/{id}). All steps send the same X-Correlation-Id". In section 6, rows 2 to 4, write "{id} is the device_id picked from the storm reply". Delete the Open question line (O-1) about how the page learns a device_id.
  b) POST /approvals/{id}. RQ-32: replace the whole Requirement cell with: "POST /approvals/{id} lets persona.noc_operator store decision and approver for a recommendation. {id} is the device_id that the recommendation was about. The caller sends a JSON body with one key, decision, whose value is the word yes or the word no. The caller sends no approver and no approval id. The server sets approver to the persona id of the caller's role (always persona.noc_operator, the only allowed role, RQ-35) and makes the approval id. The role check runs before the body check. A body with no decision, or with any other value, returns HTTP 422 and stores nothing. A good call returns HTTP 200 and a JSON body with five keys: approval_id, decision, approver, record_id (the device_id) and correlation_id. A second call for the same device_id and correlation id stores a second record. Nothing is overwritten. The call writes one ai.approval audit row first (RQ-36)."
     RQ-34: replace the last sentence "S07 chooses how the route finds that recommendation and writes the reason." with "The route stores a decision only when the audit log holds, under the same X-Correlation-Id, one row with the action ai.recommendation whose record_id equals {id}. That row exists only when the recommend route returned text, from the model or from the answer store. If no such row exists, the route returns 404 not_found and stores nothing. A call with no X-Correlation-Id gets a new id from the server (RQ-49). That id matches no row, so the call returns 404."
     Delete the Open question line (O-2) about the input and reply of POST /approvals/{id}.
  c) Audit words and the final-action key. RQ-15: replace "writes one audit row" with "writes one record.storm_read audit row". RQ-18: add the sentence "A healthy call writes one ai.recommendation audit row. A stop with no text writes policy.hold or policy.deny, as before." RQ-31: add "A stored answer writes the same ai.recommendation row, and the row says no model ran." RQ-40: replace "The key name is an Open question for S03." with "The key is named final_action and is the 17th key, after record_id." RQ-52: replace "including the storm read, the recommendation and the approval" with "including record.storm_read, ai.recommendation and ai.approval". The three words use the prefixes record., ai. and ai. because the existing test test_audit_action_words_in_main_py_all_have_an_id checks the prefixes audit, policy, record and ai.
     Section 15. Rewrite the Open question line for the final-action key: "the audit key final_action has no YAML id. The existing id status.code.cannot_prove.final_action names a word in the list of things the log cannot prove. It does not name an audit key. Action: S07 adds the key id under a new ADR. This does not block the PRD." Rewrite the Open question line for O-3: "the audit action words record.storm_read, ai.recommendation and ai.approval have no YAML id. They are PROPOSED. Owner: Team-Force. Action: S07 adds the ids under a new ADR before it ships the routes. This does not block the PRD." In the "Planned YAML additions" paragraph, name the three words and the key final_action.
  d) Open question counts. The PRD now has 13 Open question lines, not 15. Change "Fifteen" to "Thirteen" everywhere: prd.md header, the section 15 text, traceability.md header and Unresolved issues. In the prd.md header, "Unresolved issues", delete the sentence "The way POST /approvals/{id} finds the recommendation it decides on is left to S07 (RQ-34)." Do the same in traceability.md.
  e) Add no row and no test name. The planned tests keep their names.

R3-8 (the limit of 10 running calls). Apply. Decision: the cause is failmode.model_unreachable. The code keeps the reason strings it writes today.
  a) Section 7, failure table. Directly under the row "Model raises an error, or the breaker is open", add a row: Cause "10 model calls are already running" | YAML id `failmode.model_unreachable` | Outcome HOLD_FOR_REVIEW | What the caller sees "HTTP 202, both null".
  b) Section 7, directly under the failure table, add: "The failure table names the cause. The reasons list in the response body holds these strings today (policy.py lines 231 to 236, ai_gateway.py lines 296 to 332). A timeout, an open breaker and a full limit of 10 running calls: failmode.schema_failure and failmode.timeout. A model that raises an error: failmode.schema_failure only. The id failmode.model_unreachable names the cause in this table, in RQ-24 and in RQ-54. The code does not write it. The audit row stores no reasons. A refused call has null prompt_hash, tokens and latency_ms in its audit row. A timeout has them set. A breaker refusal and a full limit look the same in the audit row. S07 keeps this behaviour. Verified Fact." Before you write it, read those lines of policy.py and ai_gateway.py. If the code differs, the code wins, and you change the sentence to match.
  c) Section 7, outcome table, row HOLD_FOR_REVIEW, column "Which route in this PRD can return it". Replace "on a timeout, an error, a bad shape, a blank stale flag or a command phrase" with "on a timeout, an error, an open breaker, a full limit of 10 running calls, a bad shape, a blank stale flag or a command phrase".
  d) RQ-54. Add at the end: "The reasons list in the response body holds failmode.schema_failure and failmode.timeout in both cases. The id failmode.model_unreachable names the cause only." Add `failmode.timeout` and `failmode.schema_failure` to the YAML ids cell of RQ-54 in prd.md and in traceability.md.
  e) RQ-24. Add at the end: "The test checks HTTP 202, outcome HOLD_FOR_REVIEW, null text and no model call for an open breaker. It checks no reason string." Section 7, list "Limits of the checks". Add a bullet: "The reasons list cannot tell an open breaker from a full limit of 10 running calls. A later ADR may add a flag for it. This PRD adds none."

R3-5 (workflow verb and persona). Apply. Decision: step 5 uses the verb analyse. Step 6 keeps no persona and says why.
  a) Section 6, step 5. Change the Verb cell from "review" to "analyse". Change the Persona cell to "`role.admin` (`admin`). An API role, not a persona (section 5)".
  b) Section 6, step 6. Change the Persona cell from "none" to "none. No one takes this step".
  c) Section 6, under the table, after the sentence that ends "The model never fills the approval id.", add: "Steps 1 to 5 each have a verb from the four agency verbs and a caller. Step 6 has no caller because it is not built."
  d) Section 9, route table, row `GET /audit/{correlation_id}`. Change the verb cell from "review" to "analyse".
  e) Search prd.md and traceability.md for the word "review" in any table cell that holds a verb. Change each hit to analyse. Leave every other use of the word "review" as it is, for example "HOLD_FOR_REVIEW" and "review and approve".

R3-7 (small consistency items). Apply all five.
  a) RQ-05. Replace "`mgmt_ip` and `credential_profile`" with "`mgmt_ip` (the management address of the device; in this data it holds a word such as alpha or legacy, not an address) and `credential_profile` (a label for which login details the device uses; it is not a password)". RQ-06. Replace "`mgmt_ip` and `credential_profile`" with "the two sensitive fields of RQ-05". Section 8, row "entity.device (sensitive)", Fields cell: add the same two bracketed phrases after the field names. The source is semantic-layer/entities.yaml.
  b) Section 8, honesty label table. Add four rows after the row "Number of rows in the audit chain".
     Row 1: Number "Calls per outcome (RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE)" | REAL | "Counted from `logs/audit.log` at the request. The log mixes test rows and real rows (D-05). EXECUTE shows 0." | `metric.ai_outcome_count`.
     Row 2: Number "Share of audit rows with every key filled" | REAL | "Counted from `logs/audit.log` at the request. The page shows it only after `record_id` exists (D-06). Before that the page shows no number." | `metric.audit_completeness`.
     Row 3: Number "Share of audit rows whose `prompt_hash` was seen before" | REAL | "Counted from `logs/audit.log` at the request." | `metric.repeated_prompt_share`.
     Row 4: Number "Status code of `GET /health`" | REAL | "A live call at the request, not a stored value." | `metric.api_availability`.
     RQ-63. Add `metric.ai_outcome_count`; `metric.audit_completeness`; `metric.repeated_prompt_share`; `metric.api_availability` to the YAML ids cell, in prd.md and in traceability.md.
  c) Section 15, Gate check, row "The PRD and the YAML agree". Start the Result cell with "PASS." and keep the rest of the sentence. If the cell names a count of Open question lines, it must say 13.
  d) Section 7, paragraph "The four outcomes". Directly before the outcome table, add: "In this PRD, a healthy call is a call from a caller with an allow row to which no row of the failure table below applies."
  e) Section 5, route table, column "Everyone else". Add "No header gives 403." to the rows `GET /alarms/storms/{storm_batch_id}`, `POST /approvals/{id}` and `GET /audit/{correlation_id}`. RQ-35. Change "Every other role gets 403 and a `policy.deny` audit row." to "Every other role, and a call with no role header, gets 403 and a `policy.deny` audit row." Add `rule.no_default_role`; `status.code.role_header.absent` to the YAML ids cell of RQ-35, in prd.md and in traceability.md. RQ-43. Change "Any other caller gets 403" to "Any other caller, including a call with no role header, gets 403". RQ-11 and RQ-28 already say this.

R3-4 (approval point for every AI use). Apply. Decision: section 7 lists all 11 AI uses.
  a) Section 7, first table. Add six rows after the row `ai_use.remediation_execution`. Keep the first three rows first, so the sentence "The desk jobs for the first three rows are PROPOSED" stays true. The columns are AI use | Pick | Agency | Outcome | Human approval point (quoted).
     Row 1: `ai_use.order_qualification` (no route in this PRD) | rules | analyse | none | "None at this agency. A provision of a circuit is a live network change. A named human approves that change on the remediation execution row."
     Row 2: `ai_use.provisioning_retry_and_rollback` (no route in this PRD) | deterministic code | analyse | none | "None at this agency. A rollback that changes a live circuit uses the human approval on the remediation execution row."
     Row 3: `ai_use.alarm_dedupe` (`GET /alarms/storms/{storm_batch_id}`) | deterministic code | analyse | none | "None at this agency. The `noc_operator` decides whether the group becomes one incident. That decision sits on the correlation row."
     Row 4: `ai_use.alarm_to_incident_correlation` (the storm route flags rows and opens no incident) | deterministic code | analyse | none | "None at this agency. The `noc_operator` opens or merges the incident. The later read named in the contract is `GET /alarms/storms/{storm_batch_id}` (`operating-contract.md` row 2)."
     Row 5: `ai_use.topology_lookup` (`GET /records/{id}`) | deterministic code | analyse | none | "None at this agency. The lookup returns a row. It leaves the device unchanged."
     Row 6: `ai_use.remediation_validation` (no route in this PRD) | deterministic code | analyse | none | "None at this agency. A person reads the match or the mismatch. A rollback uses the human approval on the remediation execution row. This row leaves the incident open."
  b) Section 7, first line. Replace the sentence "Each cell below is quoted from `docs/02-baseline/ai-qualification.md`." with "Each cell below is quoted from `docs/02-baseline/ai-qualification.md`. This table lists all 11 AI uses. An Outcome of none means that file names no outcome word for that use."
  c) Before you write each row, read the quoted cell in ai-qualification.md and copy it word for word. If a cell differs from the text above, the file wins.

R3-3 (stale lines in other files). Apply in the PRD only. Decision: this stage records every stale line in section 15 and changes no other file.
  a) Section 15, list "Stale text found while writing". Add four bullets.
     Bullet 1: "`docs/prd/Risk Management.md` line 95 says the storm, recommend and approval routes already refuse a call with no header. Those routes are new in this PRD. RQ-11, RQ-28 and RQ-35 require the refusal. The file is outside this stage."
     Bullet 2: "`docs/prd/Risk Management.md` lines 219, 221 and 223 use the phrase 'output policy' and the words 'never store BLOCK or HOLD'. RQ-31 uses 'the same checks as a fresh answer' and says the store never holds an answer that has no text. The file is outside this stage."
     Bullet 3: "`docs/02-baseline/semantic-layer-revision.md` line 8 says 14 items stay deferred. D-07 was decided later in ADR 0003, so 13 stay deferred. The file is outside this stage."
     Bullet 4: "`docs/12-finops/optimization-backlog.md` line 37 says 'Run the output policy on that answer again.' RQ-31 says 'the same checks as a fresh answer'. The file is outside this stage."
  b) Section 15, directly under the list, add: "The lines in this list are stale. S07 does not follow them. For each line in this list, the requirement row of this PRD applies. If the YAML and this PRD disagree, the YAML applies, and the PRD is fixed or an ADR is recorded. For any other disagreement between this PRD and a file outside the YAML, S07 stops and writes an open question for S06. Owner decision, 2026-10-13."
  c) Keep the existing bullets for `semantic-layer-revision.md` line 442, `S05R_Decisions_Taken.md` and the two `playbook/S07` lines. Add to the S07 bullet about "a reason": "The approval body has one key, `decision` (RQ-32)."
  d) Do not edit any file outside prd.md, traceability.md and prd-fixes.md.

R3-9 (S07 gap reporting). Apply. Decision: S07 records every gap in `docs/demo/evidence.md`, in one fixed section.
  a) Section 15, after the "Stale text found while writing" list and the sentence of R3-3 b), add a heading "How S07 reports a gap" and this text: "A gap is any choice that this PRD, the YAML and the ADRs do not fix. Examples: a key name, a status code, a field in a reply, a word on the page. S07 does not fill a gap. S07 stops work on that requirement and builds no guess for it. S07 writes the gap in a section called 'PRD gaps' in `docs/demo/evidence.md`. The section is a table with five columns: requirement id, what the PRD lacks, the sources that disagree (file and line), what S07 did, and the owner answer. The owner answer is empty until the owner fills it. If S07 finds no gap, the section holds one line: 'None. S07 found no gap.' S07 reports the stage as PASS only when the section holds that line or every row has an owner answer. S07 repeats each gap row under item 6, Blocking issues, of its final response."
  b) Section 15, same place, add: "If the owner answers a gap by changing this PRD, the PRD version goes up by one minor step and `traceability.md` gets the same version. S07 then re-checks every requirement row whose text changed, and says so in `docs/demo/evidence.md`. S08 starts only after the PRD version stops changing."
  c) Add no RQ row, no YAML id, no Open question line and no test name. The count of Open question lines stays 13.
  d) Read playbook/S07-application-and-demo.md. It must name `docs/demo/evidence.md` as required artifact 6 and "Blocking issues" as item 6 of the final response. If it does not, stop and mark R3-9 "cannot apply".

Owner edits outside this stage. This stage makes none of them. The owner makes them by hand before S07 starts. Name them in the Residual risks row of the prd-fixes.md header and do not edit the files.
  - docs/ADR/0003-s06-risk-recommendations.md line 46: replace the sentence with "S07 never stores an answer that has no text. That means a BLOCK, or a HOLD_FOR_REVIEW with no sentence. It stores a HOLD_FOR_REVIEW recommendation that has a sentence and passed every output check. The output checks run again on a stored answer."
  - docs/12-finops/optimization-backlog.md line 124: replace the sentence with "An answer is stored only when it has text and passed every output check. A BLOCK, a HOLD_FOR_REVIEW with no text, a timeout and a bad answer are never stored." Then make lines 24 and 121 say the same. Line 37: replace "the output policy" with "the output checks".
  - playbook/S06R-prd-review.md lines 47 and 66: change "never stores or holds BLOCK or HOLD" to "never stores an answer that has no text (BLOCK, or HOLD_FOR_REVIEW with no sentence)".
  - docs/prd/Risk Management.md line 95: replace the sentence with "Those three routes do not exist yet. The PRD requires each one to refuse a call with no header (RQ-11, RQ-28, RQ-35)." Lines 219 and 221: replace "the output policy" with "the same output checks". Lines 221 and 223: replace "Never store BLOCK or HOLD answers" and "never store BLOCK or HOLD" with "never store an answer that has no text (a BLOCK, or a HOLD_FOR_REVIEW with no sentence)".
  - docs/02-baseline/S05R_Decisions_Taken.md line 26: write 13 deferred items without D-07, and add the row "Decided later in ADR 0003 | 1 | D-07". The total stays 20.
  - docs/02-baseline/semantic-layer-revision.md line 8: replace "14 stay deferred" with "13 stay deferred (D-07 was decided later in ADR 0003)". Line 442: replace the text with "Next: S06 writes `1.1.1` into the PRD header. S08 hashes the tree at `1.1.1` for the second model."
  - playbook/S07-application-and-demo.md line 34: the storm route returns the raw count, the deduped count, the flagged count and the rows (alarm_id, device_id, dedupe_key, flag word). Line 36: the recommend route returns HOLD_FOR_REVIEW with the sentence on a healthy call, and HOLD_FOR_REVIEW with no text or BLOCK on a stop, and never RECOMMEND_ONLY or EXECUTE. Line 37: the approvals route takes decision (yes or no) in a JSON body, the server sets approver, makes the approval id, writes the audit row first, and returns approval_id, decision, approver, record_id and correlation_id, with no reason field. Line 53: replace with "Build only what the PRD names. If a route needs something the PRD lacks, stop work on that requirement and write it in the 'PRD gaps' section of docs/demo/evidence.md (see prd.md, section 15, 'How S07 reports a gap')." The "Expected output" row for evidence.md: add "A 'PRD gaps' section."
  - playbook/S08-second-model.md, comparison step 3: add "For each difference between the two apps, say whether S07 listed a related gap in the 'PRD gaps' section of docs/demo/evidence.md. Mark each difference 'listed gap' or 'unlisted'."
  - playbook/README.md line 46: change "Runs only when S06R has a FAIL row" to "Runs when S06R has a FAIL row, or when the owner chooses to fix Other findings before S07".

Version and checks for this round. Raise the version of prd.md and traceability.md from 1.3 to 1.4, once, with the same number in both. Add no RQ row, no YAML id and no test name. Keep 73 RQ rows, 29 existing tests, 44 planned tests, 757 ids and layer version 1.1.1. The count of Open question lines goes from 15 to 13. After the edits, search prd.md and traceability.md for "Fifteen", "fifteen", "output policy", "listed apart", "review" in a verb cell, "healthy call", "No header gives 403", "failmode.timeout", "failmode.model_unreachable", "all 11", "raw count", "deduped count", "flagged", "answer store" and "approval". Every hit must agree with the text above. Every term in the new text must appear in the glossary, in the YAML, or on an Open question for S03 line.
```

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| R3-1 | apply | The Decisions block gives exact words for RQ-31, RK-14, the section 13 row, the header and two stale-text bullets. ADR 0003 and `optimization-backlog.md` are not edited. |
| R3-2 | apply | I read the two storms in `data/synthetic/alarms.csv` before writing the example. `STO-00019` is at file lines 20 and 355, both `ALA-00019`, both `DED-00019`, both with `last_seen_at` before `first_seen_at`. `STO-00002` is at file line 3, `ALA-00002`, `DED-00002`, flagged. The numbers in the Decisions block match the file. **Verified Fact.** |
| R3-3 | apply | Four stale-text bullets and the paragraph under the list are in section 15. I read each cited line first (list in the agreement check). Bullet 2 cites two lines for "output policy" and two other lines for "never store BLOCK or HOLD". The file wins, so the bullet names the lines that way. No file outside the three is edited. |
| R3-4 | apply | Six rows added to section 7. A script compared all 11 quoted cells with `docs/02-baseline/ai-qualification.md`: all equal. **Verified Fact.** |
| R3-5 | apply | Step 5 and the route table use the verb analyse. Step 5 and step 6 have the persona cells that the block gives. |
| R3-6 | apply | The names `record.storm_read`, `ai.recommendation`, `ai.approval` and `final_action` are PROPOSED. Owner: Team-Force (`operating-contract.md` row 10). The first three keep the prefixes that `test_audit_action_words_in_main_py_all_have_an_id` checks (audit, policy, record, ai). |
| R3-7 | apply | All five items applied. The four new label rows use REAL only. |
| R3-8 | apply | I read `policy.py` lines 231 to 236, `ai_gateway.py` lines 296 to 332, `breaker.py` and `audit_query.py` line 128 before writing the paragraph. The code matches the sentence: a timeout and a breaker refusal both set `timeout_hit`, so the reasons list holds `failmode.timeout` and `failmode.schema_failure`. A model that raises an error sets `output_schema_ok` false and holds `failmode.schema_failure` only. The audit row stores no reasons. A refused call has no `prompt_hash`, `tokens` or `latency_ms`. **Verified Fact.** |
| R3-9 | apply | I read `playbook/S07-application-and-demo.md`. It names `docs/demo/evidence.md` as required artifact 6 and "Blocking issues" as item 6 of the final response. So R3-9 can apply. |
| Owner edits outside this stage | not a fix | This stage made none of them. They are named in the Residual risks row of the header. |

Where I used my own words besides the exact text in the block:

- RQ-62. The block says to replace "look up a device" with a long phrase. I wrote that phrase word for word. A plain replacement would leave the sentence "...All steps send the same X-Correlation-Id, ask for a recommendation, decide, and read the audit chain." So I changed only the words after the phrase: "The page then asks for a recommendation, records the decision, and reads the audit chain."
- Section 6, steps 1 and 4. The old sentences said "the alarm ids" and "The person stores yes or no and the approver". They disagree with R3-2 a and R3-6 b. I changed them to match (step 5 of the instructions asks for agreement).
- Section 8, rows "Approval record" and "Audit row". The first now lists the device id (`record_id`), because RQ-32 returns it. The second names the key `final_action`, because RQ-40 now names it.

### Edit list

Line numbers are the lines after the edit, except for a deleted line. A deleted line shows its line number before the edit. **Verified Fact** (a script found each line in the final files).

| Fix | File | Requirement id or section | Line | Old text | New text |
|---|---|---|---|---|---|
| version | `prd.md` | header, Date / version | 7 | 2026-10-12, v1.3. S06R fixes applied, round 2. Fixes F-1, F-2, F-3, F-5. F-4 left alone. | 2026-10-13, v1.4. S06R fixes applied, round 3. Fixes R3-1 to R3-9. The review says Fixes required: None. The owner's Decisions block closes R3-1 to R3-8. The owner raised R3-9 after the review. |
| version | `prd.md` | header, Status | 9 | S06R fixes applied, round 2. All 73 requirements | S06R fixes applied, round 3. All 73 requirements |
| version | `prd.md` | header, Status | 9 | F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. ADR 0003 records the three risk decisions. | Round 3 closed R3-1 to R3-9. R3-4 settled the old F-4 and F-8: section 7 now lists all 11 AI uses. ADR 0003 records the three risk decisions. |
| R3-1 c, R3-6 d, R3-6 b | `prd.md` | header, Unresolved issues | 12 | Fifteen Open questions for S03 stay open: see section 15. The way `POST /approvals/{id}` finds the recommendation it decides on is left to S07 (RQ-34). Whether the answer store of RQ-31 needs the route name in its key is Unknown. The cap on stored answers is PROPOSED and has no number. No real model has been measured. F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. | Thirteen Open questions for S03 stay open: see section 15. The cap on stored answers is PROPOSED and has no number. No real model has been measured. Section 15 lists stale lines in files outside this stage. S07 does not follow them. |
| R3-1 a, R3-6 c | `prd.md` | RQ-31 | 332 | The store holds an answer only when it has text and passed those checks. It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). | The store holds an answer only when it has text and passed those checks. A HOLD_FOR_REVIEW answer that has a sentence is stored. A BLOCK, a HOLD_FOR_REVIEW with no sentence, a timeout and a bad answer are never stored. The store belongs to `POST /ai/recommend/{id}` only. `POST /ai/summarize/{id}` neither reads it nor writes it. An entry is found by `prompt_hash` alone. It lives 300 seconds, counted from the moment it was stored. A stored answer that fails a check is treated like a fresh answer that fails the same check (RQ-25, RQ-30, RQ-70, RQ-71) and is removed from the store. A stored answer writes the same `ai.recommendation` audit row, and the row says no model ran. |
| R3-1 b | `prd.md` | section 12, RK-14 | 482 | A stored answer goes through the same checks again (RQ-31, ADR 0003). | A stored answer goes through the same checks again (RQ-31, ADR 0003). It serves `POST /ai/recommend/{id}` only. |
| R3-1 b | `prd.md` | section 13, ADR 0003 table, row RQ-31 | 514 | It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). The cap is PROPOSED and has no number. | It never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence). The cap is PROPOSED and has no number. It serves `POST /ai/recommend/{id}` only. |
| R3-2 a | `prd.md` | RQ-08 | 300 | `GET /alarms/storms/{storm_batch_id}` returns the raw count (every row with that `storm_batch_id`), the deduped count (each `dedupe_key` once) and the alarm ids. A row with a blank `dedupe_key` is held aside, listed apart, and left out of the deduped count. The words raw count and flagged count are an Open question for S03. | `GET /alarms/storms/{storm_batch_id}` returns the raw count, the deduped count, the flagged count and the rows. Raw count: every row with that `storm_batch_id`. Deduped count: the number of different non-blank `dedupe_key` values among those rows. Flagged count: the number of rows that carry the flag word `last_seen_before_first_seen` or `times_unreadable`. The reply lists each row with `alarm_id`, `device_id`, `dedupe_key` and its flag word (empty when none). A flagged row counts in the raw count. It also counts in the deduped count when its `dedupe_key` is not blank. A row with a blank `dedupe_key` is held aside, listed apart from the other rows, counted in the raw count only, and left out of the deduped count. No row is removed from a list because of a flag. The words raw count and flagged count are an Open question for S03. |
| R3-2 b | `prd.md` | RQ-09 | 301 | A row whose `last_seen_at` is before `first_seen_at`, or whose time cannot be read, is listed with its flag word and is not counted as an incident candidate. | A row whose `last_seen_at` is before `first_seen_at`, or whose time cannot be read, carries its flag word in the reply and counts in the flagged count. It still counts in the raw count and, when its `dedupe_key` is not blank, in the deduped count (RQ-08). It is not counted as an incident candidate. Example from `data/synthetic/alarms.csv`: storm `STO-00019` has two rows (file lines 20 and 355), both `ALA-00019` with `dedupe_key` `DED-00019`, both flagged. Its raw count is 2, its deduped count is 1 and its flagged count is 2. Storm `STO-00002` has one row, flagged. Its raw count is 1, its deduped count is 1 and its flagged count is 1. |
| R3-2 c, R3-6 a | `prd.md` | section 6, step 1, What happens | 122 | Reads the raw count, the deduped count and the alarm ids of one storm. Flagged rows are listed apart. | Reads the raw count, the deduped count, the flagged count and the rows of one storm (alarm id, device id, dedupe key, flag word). A flagged row keeps its flag word in the list and counts in the flagged count. |
| R3-6 a | `prd.md` | RQ-62 | 399 | pick a storm, read the counts, look up a device, ask for a recommendation, decide, and read the audit chain. | pick a storm, read the counts, look up a device: the page lists the different `device_id` values from the storm reply, the operator picks one, and the page uses that value as `{id}` in the lookup (`GET /records/{id}`), the recommendation (`POST /ai/recommend/{id}`) and the decision (`POST /approvals/{id}`). All steps send the same `X-Correlation-Id`. The page then asks for a recommendation, records the decision, and reads the audit chain. |
| R3-6 a | `prd.md` | section 6, step 2, What happens | 123 | Looks up one device. The two sensitive fields are left out for this persona. | Looks up one device. The two sensitive fields are left out for this persona. `{id}` is the `device_id` picked from the storm reply. |
| R3-6 a | `prd.md` | section 6, step 3, What happens | 124 | A stop returns BLOCK or HOLD_FOR_REVIEW with no text. | A stop returns BLOCK or HOLD_FOR_REVIEW with no text. `{id}` is the `device_id` picked from the storm reply. |
| R3-6 a, R3-6 b | `prd.md` | section 6, step 4, What happens | 125 | The person stores yes or no and the approver. The server makes the approval id. Nothing on any device changes. | The person stores yes or no. The server sets the approver and makes the approval id. Nothing on any device changes. `{id}` is the `device_id` picked from the storm reply. |
| R3-6 a | `prd.md` | section 15, Open question O-1 (how the page learns a device_id) | 585 (before the edit) | **Open question for S03:** how the page learns a `device_id` after the storm step (O-1). RQ-08 returns the raw count, the deduped count and the alarm ids. Step 2 of the demo looks up a device and needs a `device_id`. The storm response is not required to carry one. This PRD does not pick a way. Action: S07 chooses how the page gets a `device_id` and writes it in the page test (RQ-62). This does not block the PRD. | (line deleted) |
| R3-6 b | `prd.md` | RQ-32 | 342 | `POST /approvals/{id}` lets `persona.noc_operator` store `decision` (yes or no) and `approver` (a persona id) for a recommendation. The server makes the approval id. The caller does not send one. | `POST /approvals/{id}` lets `persona.noc_operator` store `decision` and `approver` for a recommendation. `{id}` is the `device_id` that the recommendation was about. The caller sends a JSON body with one key, `decision`, whose value is the word `yes` or the word `no`. The caller sends no `approver` and no approval id. The server sets `approver` to the persona id of the caller's role (always `persona.noc_operator`, the only allowed role, RQ-35) and makes the approval id. The role check runs before the body check. A body with no `decision`, or with any other value, returns HTTP 422 and stores nothing. A good call returns HTTP 200 and a JSON body with five keys: `approval_id`, `decision`, `approver`, `record_id` (the `device_id`) and `correlation_id`. A second call for the same `device_id` and correlation id stores a second record. Nothing is overwritten. The call writes one `ai.approval` audit row first (RQ-36). |
| R3-6 b | `prd.md` | RQ-34 | 344 | S07 chooses how the route finds that recommendation and writes the reason. | The route stores a decision only when the audit log holds, under the same `X-Correlation-Id`, one row with the action `ai.recommendation` whose `record_id` equals `{id}`. That row exists only when the recommend route returned text, from the model or from the answer store. If no such row exists, the route returns 404 `not_found` and stores nothing. A call with no `X-Correlation-Id` gets a new id from the server (RQ-49). That id matches no row, so the call returns 404. |
| R3-6 b | `prd.md` | section 15, Open question O-2 (input and reply of POST /approvals/{id}) | 587 (before the edit) | **Open question for S03:** the input and reply of `POST /approvals/{id}` (O-2). `{id}` is not defined as a device id, a recommendation id or an invocation id. The PRD does not say whether the caller sends `approver` or the server sets it from the header. The reply shape is not given. This PRD does not pick those values. Action: S07 chooses them and writes them in the approval tests (RQ-32, RQ-34). This does not block the PRD. | (line deleted) |
| R3-6 c | `prd.md` | RQ-15 | 307 | Every storm read writes one audit row that holds the correlation id | Every storm read writes one `record.storm_read` audit row that holds the correlation id |
| R3-6 c | `prd.md` | RQ-18 | 319 | RECOMMEND_ONLY is not a result of this route (policy row O2). | RECOMMEND_ONLY is not a result of this route (policy row O2). A healthy call writes one `ai.recommendation` audit row. A stop with no text writes `policy.hold` or `policy.deny`, as before. |
| R3-6 c | `prd.md` | RQ-40 | 350 | The key name is an Open question for S03. The value is `none` on every row | The key is named `final_action` and is the 17th key, after `record_id`. The value is `none` on every row |
| R3-6 c | `prd.md` | RQ-52 | 371 | including the storm read, the recommendation and the approval, has a YAML id. | including `record.storm_read`, `ai.recommendation` and `ai.approval`, has a YAML id. |
| R3-6 c | `prd.md` | section 15, Open question for the final-action key | 599 | **Open question for S03:** the final-action key name has no YAML id. RQ-40 needs a name for the audit key that records what last happened to a device. This PRD uses the words final-action key from ADR 0002 D-05 and does not invent an id. Action: S07 adds the id under a new ADR. This does not block the PRD. | **Open question for S03:** the audit key `final_action` has no YAML id. The existing id `status.code.cannot_prove.final_action` names a word in the list of things the log cannot prove. It does not name an audit key. Action: S07 adds the key id under a new ADR. This does not block the PRD. |
| R3-6 c | `prd.md` | section 15, Open question O-3 | 601 | **Open question for S03:** the audit action words for the storm read, the recommendation and the approval, and the name and position of the final-action key (O-3). RQ-52 says S07 adds the ids under a new ADR before it ships the route. This PRD does not invent those words or a key name. Action: S07 adds the ids under a new ADR. This does not block the PRD. | **Open question for S03:** the audit action words `record.storm_read`, `ai.recommendation` and `ai.approval` have no YAML id. They are PROPOSED. Owner: Team-Force. Action: S07 adds the ids under a new ADR before it ships the routes. This does not block the PRD. |
| R3-6 c | `prd.md` | section 15, Planned YAML additions | 603 | The final-action key (D-05). `record_id` (D-06). The command-phrase list (D-08). The cache flag (D-18). The audit action words for the storm read, the recommendation and the approval (RQ-52). | The final-action key `final_action` (D-05). `record_id` (D-06). The command-phrase list (D-08). The cache flag (D-18). The audit action words `record.storm_read`, `ai.recommendation` and `ai.approval` (RQ-52). |
| R3-6 b (agreement) | `prd.md` | section 8, Approval record row | 210 | `decision`, `approver`, the approval id, the correlation id | `decision`, `approver`, the approval id, the device id (`record_id`), the correlation id |
| R3-6 c (agreement) | `prd.md` | section 8, Audit row | 209 | plus `record_id` (D-06) and a final-action key (D-05) from S07 | plus `record_id` (D-06) and the `final_action` key (D-05) from S07 |
| R3-8 a | `prd.md` | section 7, failure table | 174 | (no row) | \| 10 model calls are already running            \| `failmode.model_unreachable`              \| HOLD_FOR_REVIEW \| HTTP 202, both null                           \| |
| R3-8 b | `prd.md` | section 7, under the failure table | 184 | (no paragraph) | The failure table names the cause. The reasons list in the response body holds these strings today (`policy.py` lines 231 to 236, `ai_gateway.py` lines 296 to 332). A timeout, an open breaker and a full limit of 10 running calls: `failmode.schema_failure` and `failmode.timeout`. A model that raises an error: `failmode.schema_failure` only. The id `failmode.model_unreachable` names the cause in this table, in RQ-24 and in RQ-54. The code does not write it. The audit row stores no reasons. A refused call has null `prompt_hash`, `tokens` and `latency_ms` in its audit row. A timeout has them set. A breaker refusal and a full limit look the same in the audit row. S07 keeps this behaviour. **Verified Fact.** |
| R3-8 c | `prd.md` | section 7, outcome table, row HOLD_FOR_REVIEW | 162 | on a timeout, an error, a bad shape, a blank stale flag or a command phrase | on a timeout, an error, an open breaker, a full limit of 10 running calls, a bad shape, a blank stale flag or a command phrase |
| R3-8 d | `prd.md` | RQ-54 | 382 | (5 failures in a row, 30 seconds open, 10 calls at the same time) are PROPOSED (N-05). Owner: Team-Force. | (5 failures in a row, 30 seconds open, 10 calls at the same time) are PROPOSED (N-05). Owner: Team-Force. The reasons list in the response body holds `failmode.schema_failure` and `failmode.timeout` in both cases. The id `failmode.model_unreachable` names the cause only. |
| R3-8 d | `prd.md` | RQ-54, YAML ids cell | 382 | `failmode.model_unreachable`; `status.code.breaker_state.open` | `failmode.model_unreachable`; `status.code.breaker_state.open`; `failmode.timeout`; `failmode.schema_failure` |
| R3-8 e | `prd.md` | RQ-24 | 325 | An open breaker means the model is not called. | An open breaker means the model is not called. The test checks HTTP 202, outcome HOLD_FOR_REVIEW, null text and no model call for an open breaker. It checks no reason string. |
| R3-8 e | `prd.md` | section 7, Limits of the checks | 195 | - The model name and the model version are the same text, `local-sim-v1` (SB-15). | - The model name and the model version are the same text, `local-sim-v1` (SB-15). / - The reasons list cannot tell an open breaker from a full limit of 10 running calls. A later ADR may add a flag for it. This PRD adds none. |
| R3-5 a | `prd.md` | section 6, step 5, Verb and Persona | 126 | \| review    \| `role.admin` (`admin`)              \| | \| analyse   \| `role.admin` (`admin`). An API role, not a persona (section 5) \| |
| R3-5 b | `prd.md` | section 6, step 6, Persona | 127 | \| none                                \| | \| none. No one takes this step        \| |
| R3-5 c | `prd.md` | section 6, under the table | 130 | The model never fills the approval id. | The model never fills the approval id. Steps 1 to 5 each have a verb from the four agency verbs and a caller. Step 6 has no caller because it is not built. |
| R3-5 d | `prd.md` | section 9, route table, row GET /audit/{correlation_id} | 250 | \| review         \| | \| analyse        \| |
| R3-7 a | `prd.md` | RQ-05 | 288 | `GET /records/{id}` leaves `mgmt_ip` and `credential_profile` out of the body for every role except `persona.network_engineer`. | `GET /records/{id}` leaves `mgmt_ip` (the management address of the device; in this data it holds a word such as alpha or legacy, not an address) and `credential_profile` (a label for which login details the device uses; it is not a password) out of the body for every role except `persona.network_engineer`. |
| R3-7 a | `prd.md` | RQ-06 | 289 | `GET /records/{id}` returns `mgmt_ip` and `credential_profile` to `persona.network_engineer` | `GET /records/{id}` returns the two sensitive fields of RQ-05 to `persona.network_engineer` |
| R3-7 a | `prd.md` | section 8, row entity.device (sensitive), Fields cell | 207 | `field.device.mgmt_ip`, `field.device.credential_profile` | `field.device.mgmt_ip` (the management address of the device; in this data it holds a word such as alpha or legacy, not an address), `field.device.credential_profile` (a label for which login details the device uses; it is not a password) |
| R3-7 b | `prd.md` | section 8, honesty label table, after the row Number of rows in the audit chain | 225 to 228 | (no row) | \| Calls per outcome (RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE) \| REAL \| Counted from `logs/audit.log` at the request. The log mixes test rows and real rows (D-05). EXECUTE shows 0. \| `metric.ai_outcome_count` \| / \| Share of audit rows with every key filled \| REAL \| Counted from `logs/audit.log` at the request. The page shows it only after `record_id` exists (D-06). Before that the page shows no number. \| `metric.audit_completeness` \| / \| Share of audit rows whose `prompt_hash` was seen before \| REAL \| Counted from `logs/audit.log` at the request. \| `metric.repeated_prompt_share` \| / \| Status code of `GET /health` \| REAL \| A live call at the request, not a stored value. \| `metric.api_availability` \| |
| R3-7 b | `prd.md` | RQ-63, YAML ids cell | 400 | `status.code.token_estimate_method.word_count_x2_educational` | `status.code.token_estimate_method.word_count_x2_educational`; `metric.ai_outcome_count`; `metric.audit_completeness`; `metric.repeated_prompt_share`; `metric.api_availability` |
| R3-7 c | `prd.md` | section 15, Gate check, row The PRD and the YAML agree | 633 | \| The version is `1.1.1` in all places. | \| PASS. The version is `1.1.1` in all places. |
| R3-7 d | `prd.md` | section 7, paragraph The four outcomes | 157 | (no sentence) | In this PRD, a healthy call is a call from a caller with an allow row to which no row of the failure table below applies. |
| R3-7 e | `prd.md` | section 5, route table, row storm, Everyone else | 106 | \| 403 and a `policy.deny` row | \| 403 and a `policy.deny` row. No header gives 403. |
| R3-7 e | `prd.md` | section 5, route table, row approvals, Everyone else | 109 | \| 403 and a `policy.deny` row | \| 403 and a `policy.deny` row. No header gives 403. |
| R3-7 e | `prd.md` | section 5, route table, row audit, Everyone else | 110 | \| 403 and a `policy.deny` row | \| 403 and a `policy.deny` row. No header gives 403. |
| R3-7 e | `prd.md` | RQ-35 | 345 | Every other role gets 403 and a `policy.deny` audit row. | Every other role, and a call with no role header, gets 403 and a `policy.deny` audit row. |
| R3-7 e | `prd.md` | RQ-35, YAML ids cell | 345 | `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny` | `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny`; `rule.no_default_role`; `status.code.role_header.absent` |
| R3-7 e | `prd.md` | RQ-43 | 362 | Any other caller gets 403 and a `policy.deny` audit row. | Any other caller, including a call with no role header, gets 403 and a `policy.deny` audit row. |
| R3-4 b | `prd.md` | section 7, first line | 134 | Each cell below is quoted from `docs/02-baseline/ai-qualification.md`. | Each cell below is quoted from `docs/02-baseline/ai-qualification.md`. This table lists all 11 AI uses. An Outcome of none means that file names no outcome word for that use. |
| R3-4 a | `prd.md` | section 7, first table, after the row ai_use.remediation_execution | 144 to 149 | (no row) | \| `ai_use.order_qualification` (no route in this PRD) \| rules \| analyse \| none \| "None at this agency. A provision of a circuit is a live network change. A named human approves that change on the remediation execution row." \| / \| `ai_use.provisioning_retry_and_rollback` (no route in this PRD) \| deterministic code \| analyse \| none \| "None at this agency. A rollback that changes a live circuit uses the human approval on the remediation execution row." \| / \| `ai_use.alarm_dedupe` (`GET /alarms/storms/{storm_batch_id}`) \| deterministic code \| analyse \| none \| "None at this agency. The `noc_operator` decides whether the group becomes one incident. That decision sits on the correlation row." \| / \| `ai_use.alarm_to_incident_correlation` (the storm route flags rows and opens no incident) \| deterministic code \| analyse \| none \| "None at this agency. The `noc_operator` opens or merges the incident. The later read named in the contract is `GET /alarms/storms/{storm_batch_id}` (`operating-contract.md` row 2)." \| / \| `ai_use.topology_lookup` (`GET /records/{id}`) \| deterministic code \| analyse \| none \| "None at this agency. The lookup returns a row. It leaves the device unchanged." \| / \| `ai_use.remediation_validation` (no route in this PRD) \| deterministic code \| analyse \| none \| "None at this agency. A person reads the match or the mismatch. A rollback uses the human approval on the remediation execution row. This row leaves the incident open." \| |
| R3-1 d, R3-3 a, R3-3 c, R3-3 b, R3-9 a, R3-9 b | `prd.md` | section 15, list Stale text found while writing, and the text under it | 610 to 624 | This PRD adds no reason field. /  | This PRD adds no reason field. The approval body has one key, `decision` (RQ-32). / - `docs/ADR/0003-s06-risk-recommendations.md` line 46 says S07 never stores a BLOCK or HOLD answer. Read it as an answer with no text. The ADR is outside this stage. / - `docs/12-finops/optimization-backlog.md` line 124 says an answer is stored only when the outcome is RECOMMEND_ONLY. RQ-31 stores a HOLD_FOR_REVIEW recommendation that has a sentence. The file is outside this stage. / - `docs/prd/Risk Management.md` line 95 says the storm, recommend and approval routes already refuse a call with no header. Those routes are new in this PRD. RQ-11, RQ-28 and RQ-35 require the refusal. The file is outside this stage. / - `docs/prd/Risk Management.md` lines 219 and 221 use the phrase 'output policy'. Lines 221 and 223 use the words 'never store BLOCK or HOLD'. RQ-31 uses 'the same checks as a fresh answer' and says the store never holds an answer that has no text. The file is outside this stage. / - `docs/02-baseline/semantic-layer-revision.md` line 8 says 14 items stay deferred. D-07 was decided later in ADR 0003, so 13 stay deferred. The file is outside this stage. / - `docs/12-finops/optimization-backlog.md` line 37 says 'Run the output policy on that answer again.' RQ-31 says 'the same checks as a fresh answer'. The file is outside this stage. /  / The lines in this list are stale. S07 does not follow them. For each line in this list, the requirement row of this PRD applies. If the YAML and this PRD disagree, the YAML applies, and the PRD is fixed or an ADR is recorded. For any other disagreement between this PRD and a file outside the YAML, S07 stops and writes an open question for S06. Owner decision, 2026-10-13. /  / ### How S07 reports a gap /  / A gap is any choice that this PRD, the YAML and the ADRs do not fix. Examples: a key name, a status code, a field in a reply, a word on the page. S07 does not fill a gap. S07 stops work on that requirement and builds no guess for it. S07 writes the gap in a section called 'PRD gaps' in `docs/demo/evidence.md`. The section is a table with five columns: requirement id, what the PRD lacks, the sources that disagree (file and line), what S07 did, and the owner answer. The owner answer is empty until the owner fills it. If S07 finds no gap, the section holds one line: 'None. S07 found no gap.' S07 reports the stage as PASS only when the section holds that line or every row has an owner answer. S07 repeats each gap row under item 6, Blocking issues, of its final response. /  / If the owner answers a gap by changing this PRD, the PRD version goes up by one minor step and `traceability.md` gets the same version. S07 then re-checks every requirement row whose text changed, and says so in `docs/demo/evidence.md`. S08 starts only after the PRD version stops changing. /  |
| version | `traceability.md` | header, Date / version | 6 | 2026-10-12, v1.3. S06R fixes applied, round 2. Fixes F-1, F-2, F-3, F-5. F-4 left alone. | 2026-10-13, v1.4. S06R fixes applied, round 3. Fixes R3-1 to R3-9. The review says Fixes required: None. The owner's Decisions block closes R3-1 to R3-8. The owner raised R3-9 after the review. |
| version | `traceability.md` | header, Status | 8 | S06R fixes applied, round 2. 73 of 73 requirements | S06R fixes applied, round 3. 73 of 73 requirements |
| version | `traceability.md` | header, Status | 8 | F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. | Round 3 closed R3-1 to R3-9. |
| R3-6 d, R3-1 c | `traceability.md` | header, Unresolved issues | 11 | The way `POST /approvals/{id}` finds its recommendation (RQ-34) is left to S07. Fifteen Open questions for S03: see `docs/prd/prd.md` section 15. F-4 of round 2 (optional, the same as F-8 of round 1) was left alone by owner decision. | Thirteen Open questions for S03: see `docs/prd/prd.md` section 15. |
| R3-7 e | `traceability.md` | RQ-35, YAML ids cell | 56 | `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny` | `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny`; `rule.no_default_role`; `status.code.role_header.absent` |
| R3-8 d | `traceability.md` | RQ-54, YAML ids cell | 75 | `failmode.model_unreachable`; `status.code.breaker_state.open` | `failmode.model_unreachable`; `status.code.breaker_state.open`; `failmode.timeout`; `failmode.schema_failure` |
| R3-7 b | `traceability.md` | RQ-63, YAML ids cell | 84 | `status.code.token_estimate_method.word_count_x2_educational` | `status.code.token_estimate_method.word_count_x2_educational`; `metric.ai_outcome_count`; `metric.audit_completeness`; `metric.repeated_prompt_share`; `metric.api_availability` |

The `traceability.md` section 1 rows keep their test names, status words and design files. Only the YAML ids cell changed, for RQ-35, RQ-54 and RQ-63. The planned tests in `traceability.md` section 2 keep their names. The expected values of the RQ-08, RQ-09, RQ-31, RQ-32 and RQ-34 tests follow the new requirement text.

### RQ ids touched

No RQ id was added, removed, merged or renumbered. The count stays 73.

| RQ id | What changed | Files that cite it (by section) |
|---|---|---|
| RQ-05 | Names what `mgmt_ip` and `credential_profile` hold. Behaviour and YAML ids stay. | `prd.md` (sections 6, 8, 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-06 | Names the two sensitive fields of RQ-05. Behaviour stays. | `prd.md` (sections 6, 8, 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-08 | Rewritten. Gives the raw count, the deduped count, the flagged count and the reply rows. Test name, YAML ids and design file stay. | `prd.md` (sections 6, 9, 10, 14, 15). `traceability.md` (sections 1, 2, 3). |
| RQ-09 | Rewritten. A flagged row stays in every count and list. Worked example from `alarms.csv`. Test name, YAML ids and design file stay. | `prd.md` (sections 6, 9, 10, 14). `traceability.md` (sections 1, 2, 3). |
| RQ-15 | Names the audit word `record.storm_read`. | `prd.md` (sections 6, 9, 10, 14). `traceability.md` (sections 1, 2, 3). |
| RQ-18 | Names the audit word `ai.recommendation`, and the words for a stop. | `prd.md` (sections 6, 9, 10, 15). `traceability.md` (sections 1, 2, 3). |
| RQ-24 | Says what the test checks. Test name stays. | `prd.md` (sections 6, 7, 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-31 | Store rules rewritten. Store serves the recommend route only. Entry found by `prompt_hash`. Stores a HOLD_FOR_REVIEW answer that has a sentence. Names `ai.recommendation`. Test name, YAML ids and design file stay. | `prd.md` (sections 6, 9, 10, 12, 13, 15). `traceability.md` (sections 1, 2, 3, 4). |
| RQ-32 | Rewritten. Input, reply, `{id}` and approver are fixed. Test name, YAML ids and design file stay. | `prd.md` (sections 6, 9, 10, 13, 15). `traceability.md` (sections 1, 2, 3, 4). |
| RQ-34 | Last sentence rewritten. The route finds the recommendation in the audit log. | `prd.md` (sections 6, 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-35 | No role header gets 403. Two YAML ids added in both files. | `prd.md` (sections 6, 9, 10, 15). `traceability.md` (sections 1, 2, 3). |
| RQ-40 | Names the key `final_action` and its place (17th key). | `prd.md` (sections 6, 9, 10, 13). `traceability.md` (sections 1, 2, 3, 4). |
| RQ-43 | No role header gets 403. | `prd.md` (sections 6, 9, 10). `traceability.md` (sections 1, 3). |
| RQ-52 | Names the three audit words. | `prd.md` (sections 6, 9, 10, 15). `traceability.md` (sections 1, 3). |
| RQ-54 | Adds the reasons list sentence. Two YAML ids added in both files. | `prd.md` (sections 7, 10, 13). `traceability.md` (section 1). |
| RQ-62 | Says how the page gets a device id. Test name stays. | `prd.md` (sections 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-63 | Four YAML ids added in both files. | `prd.md` (sections 8, 9, 10, 12). `traceability.md` (sections 1, 2, 3). |

Cited by new text, or checked, with no change to the row:

| RQ id | Why | Files that cite it (by section) |
|---|---|---|
| RQ-25, RQ-30, RQ-70, RQ-71 | Cited by the new RQ-31 text. Row text stays. | `prd.md` (sections 6, 9, 10). `traceability.md` (sections 1, 2, 3). |
| RQ-35, RQ-36, RQ-49 | Cited by the new RQ-32 and RQ-34 text. RQ-35 is also listed above. RQ-36 and RQ-49 row text stays. | `prd.md` (sections 6, 9, 10, 15). `traceability.md` (sections 1, 2, 3). |
| RQ-11, RQ-28 | Cited by a new stale-text bullet in section 15. Row text stays. | `prd.md` (sections 6, 9, 10, 14, 15). `traceability.md` (sections 1, 2, 3). |
| RQ-41 | Named in the new RQ-40 text (`record_id`). Row text stays. | `prd.md` (sections 6, 9, 10, 13, 15). `traceability.md` (sections 1, 2, 3, 4). |
| RQ-23, RQ-53 | Checked only. They use `failmode.timeout`. Row text stays. | `prd.md` (sections 6, 9, 10). `traceability.md` (sections 1, 2, 3). |

### Agreement check

| Claim | Places searched | What this round did |
|---|---|---|
| A flagged row stays in every count and every list | RQ-08, RQ-09, section 6 step 1, section 8 label row and example (`STO-00005`), section 14 (`metric.alarm_storm_size`), section 15 Open question for raw count and flagged count, `traceability.md` RQ-08 and RQ-09 rows | RQ-08, RQ-09 and step 1 now say the same. The search for "listed apart" has one hit, in RQ-08, where the block's own words say a blank-key row is listed apart from the other rows. The "flagged" hits agree. The word list for the Open question stays (R3-2 d). |
| The device id comes from the storm reply | RQ-08, RQ-62, section 6 steps 2 to 4, RQ-32 | All five say the page picks a `device_id` from the storm reply and uses it as `{id}`. The Open question line O-1 is deleted. |
| What the caller sends to `POST /approvals/{id}` | RQ-32, RQ-34, RQ-35, section 6 step 4, section 8 approval row, section 13 D-03, section 15 Open question for `decision` and `approver` | The caller sends `decision` only. The server sets the approver. Step 4 and section 8 match. D-03 and the Open question line say the record holds `decision` and `approver`, which stays true. The Open question line O-2 is deleted. |
| Audit action words and the final-action key | RQ-15, RQ-18, RQ-31, RQ-32, RQ-40, RQ-52, section 8 audit row, section 15 Open question lines and Planned YAML additions | `record.storm_read`, `ai.recommendation`, `ai.approval` and `final_action` are named the same way in every place. RQ-23 already says `policy.hold`, which agrees with the new RQ-18 sentence. |
| Open question count | `prd.md` header, `prd.md` section 15, `traceability.md` header | All say thirteen. Section 15 has 13 lines (check 8h). The 13 deferred items in section 13 are a different count and stay. |
| The answer store | RQ-31, RK-14, section 13 ADR 0003 row, section 11 row (lifetime 300 seconds), section 15 stale bullets, `traceability.md` section 4 | RQ-31, RK-14 and the section 13 row say it serves the recommend route only. Section 11 and `traceability.md` section 4 hold no store rule and stay. |
| The reasons list and the cause names | Section 7 failure table, the paragraph under it, outcome table, RQ-24, RQ-54, Limits bullet, section 11 degraded-mode table | The cause is `failmode.model_unreachable` in the table, RQ-24 and RQ-54. The paragraph says what the code writes. The section 11 table holds no cause name and stays. |
| The four agency verbs | Section 6, section 9 route table, `traceability.md` | No table cell holds the verb "review" now. The heading "10.E. Audit read (step: review the chain)" is a heading, not a verb cell, and stays (R3-5 e). |
| All 11 AI uses | Section 3 table, section 7 table | Both tables give the same pick and agency for each use. |
| Cited file lines of the new stale-text bullets | ADR 0003 line 46; `optimization-backlog.md` lines 37 and 124; `Risk Management.md` lines 95, 219, 221, 223; `semantic-layer-revision.md` lines 8 and 442 | I read each line. All say what the bullets say. **Verified Fact.** |
| Version and status | `prd.md` header, `traceability.md` header | Both say v1.4, round 3, fixes R3-1 to R3-9. Both keep semantic layer `1.1.1`. |

The PRD completion-gate section (section 15, "Gate check") holds one changed statement: the row "The PRD and the YAML agree" now starts with "PASS." as R3-7 c asks. The row names no count of Open question lines. No other gate statement changed.

### Version check

| Place | Version | Label |
|---|---|---|
| `semantic-layer/README.md` (lines 6 and 69) | `1.1.1` | **Verified Fact** |
| `prd.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `traceability.md` Evidence sources | `1.1.1` | **Verified Fact** |
| `docs/02-baseline/semantic-layer-revision.md` line 6 | `1.1.1` ("The current version is `1.1.1`") | **Verified Fact** |
| `prd-review.md` header (v3.0) | `1.1.1` | **Verified Fact** |
| ADR 0002 (newest ADR that changed the YAML) | `1.1.1`. ADR 0003 added no YAML id. | **Verified Fact** |

All six strings are equal. The status is not BLOCKED on versions. Document versions: `prd.md` v1.3 to v1.4. `traceability.md` v1.3 to v1.4. Both are the same, and the raise happened once.

### Checks 8a to 8h

All outputs are from 2026-10-13, run after the edits. The scripts for 8a to 8d and 8h are temporary Python files. They are not part of the repo. **Verified Fact.**

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
duplicate prd ids: none
duplicate trace ids: none
counts equal: True
id set difference: none
ids are RQ-01 to RQ-73: True
```

Matches the locked fact: RQ-01 to RQ-73, 73 rows.

#### 8b. YAML id lookup

```
YAML ids collected from seven files: 757
YAML ids cited in requirement rows (distinct): 123
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 188
audit action words resolved via value: [('policy.deny', 'status.code.audit_action.policy_deny'), ('policy.hold', 'status.code.audit_action.policy_hold'), ('record.read', 'status.code.audit_action.record_read')]
expected misses (PROPOSED words on the Open question for S03 line):
    ai.approval first seen ('prd.md', 342) ; named on the Open question line [601]
    ai.recommendation first seen ('prd.md', 319) ; named on the Open question line [601]
    record.storm_read first seen ('prd.md', 307) ; named on the Open question line [601]
unresolved backticked id-shaped tokens (other than file names): none
```

757 ids match the locked fact. The three expected misses are the PROPOSED words that sit on the Open question for S03 line at `prd.md` line 601: `record.storm_read`, `ai.recommendation`, `ai.approval`. `final_action` is not dotted, so the id-shaped search does not pick it up. It is on the Open question line at `prd.md` line 599. `policy.py`, `ai_gateway.py`, `events.jsonl` and similar file names are not YAML ids. The script skips them. `record.read`, `policy.deny` and `policy.hold` resolve through the `value:` of `status.code.audit_action.*`. **Verified Fact.**

#### 8c. Row-by-row compare

```
mismatches: none
```

YAML ids, test name, existing-or-planned status and design file match on all 73 rows.

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 44
```

Matches the locked fact: 29 exist, 44 are planned for S07.

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
.........................................                                [100%]
41 passed in 3.07s
```

(`python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`.) Matches the locked fact.

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines (SHA-256 `BC2D23CDA9734222576DE51B7EC2917FE90C0C326DDC7DBD1FCB74B6ED482FAD`). After the test run it had 241 lines. After the restore it had 240 lines and the same SHA-256. The command named the 29 existing test ids that `prd.md` section 10 lists.

```
SKIPPED [1] policy\tests\test_policy_python.py:577: opa binary not on PATH
40 passed, 1 skipped, 60 warnings in 6.00s
```

Matches the locked fact: 40 passed, 1 skipped. The skip is the `opa` test (RQ-59).

#### 8g. git status

Before (taken before the first edit) and after (taken after the last edit):

```
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md
 D "Archive/Project Intent segments fed to stages/Project_Intent - Appendix B.md"
 M Project_Acronyms.md
 M playbook/README.md
 M playbook/S06-prd.md
 M playbook/S06R-prd-review.md
 M playbook/S07-application-and-demo.md
 M playbook/S08-second-model.md
 M playbook/STATUS.md
 M transcript/chat_transcript.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md
?? 06-telecom-service-network-incident-ops/docs/prd/
?? "Project_Intent - Appendix B.md"
?? playbook/S06F-prd-fixes.md
```

`Compare-Object` found no difference between the two outputs. The folder `docs/prd/` was already untracked as a whole, so the three files this stage edited (`prd.md`, `traceability.md`, `prd-fixes.md`) add no line. `playbook/S07-application-and-demo.md`, `playbook/S08-second-model.md` and `playbook/README.md` already showed as modified before this stage began. The owner made those edits. This stage did not touch them. `logs/audit.log` was restored. **Verified Fact.**

File hashes after the last edit (SHA-256), so the next stage can see whether the PRD changed:

- `prd.md`: `476C5E30AB17EA05A8F9922DD0A18AC5B724B2326C05202A6F5A21333A2A35AF`
- `traceability.md`: `165207C3F2B2A4B21FBB42AEEFA03E50C086012347D3D2D7C46093642734C710`

#### 8h. Open question lines

```
Open question for S03 lines in prd.md section 15: 13
  count statement: prd.md line 12 -> Thirteen Open question
  count statement: traceability.md line 11 -> Thirteen Open question
count equals 13: True
```

The two files that state the count in words are the `prd.md` header and the `traceability.md` header. Both say thirteen. Section 15 holds 13 lines. **Verified Fact.**

#### Searches the block asks for

The block lists terms to search in `prd.md` and `traceability.md`. Each hit agrees with the block's text.

| Term | Result |
|---|---|
| "Fifteen", "fifteen" | No hit. |
| "output policy" | Two hits in `prd.md` section 15. Both sit inside the new stale-text bullets and quote other files (`Risk Management.md`, `optimization-backlog.md`). RQ-31 and RK-14 do not use the phrase. |
| "listed apart" | One hit, in RQ-08. It reads "listed apart from the other rows", the block's own words for a blank-key row. |
| "review" in a verb cell | No hit in either file. |
| "healthy call" | Section 7 definition (R3-7 d), outcome table, RQ-16, RQ-18. |
| "No header gives 403" | Six rows of the section 5 route table. |
| "failmode.timeout", "failmode.model_unreachable" | Section 7 table and paragraph, RQ-23, RQ-24, RQ-53, RQ-54, and the RQ-23, RQ-24, RQ-53 and RQ-54 rows of `traceability.md`. |
| "all 11" | Header Status and section 7 first line. The table has 11 rows (script). |
| "raw count", "deduped count", "flagged" | RQ-08, RQ-09, section 6 step 1, section 8 label row and example, section 14, section 15 Open question. All agree with R3-2. |
| "answer store" | RQ-31, RQ-34, section 13, section 11 text, section 15 Open question line, `traceability.md` section 4. |
| "approval" | Checked in the agreement check above. |

Terms in the new text that the glossary and the YAML lack (a script looked each one up). "deduped count" (the review accepted it in round 3 because `metrics.yaml` line 142 says the same thing in other words), "healthy call" (section 7 now states its meaning, R3-7 d) and "failure table" (a table in this PRD). The words answer store, stored answer, raw count and flagged count sit on Open question for S03 lines. **Inference.**

### Done test

In `prd.md` RQ-01 the YAML id `status.code.health.ok` was changed to `status.code.health.does_not_exist`. Check 8b then printed:

```
unresolved cited ids: [('RQ-01', 'status.code.health.does_not_exist')]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash before the change (`476C5E30AB17EA05A8F9922DD0A18AC5B724B2326C05202A6F5A21333A2A35AF`). Check 8b then printed:

```
unresolved cited ids: none
unresolved backticked id-shaped tokens (other than file names): none
```

**Verified Fact.**

### Map from the Decisions lines to the "Other findings" rows

The review has no FAIL row. No row is marked PASS. The next S06R does that.

| Decisions line | Row it closes | Edits that address it |
|---|---|---|
| R3-1 | R3-1 | RQ-31 store sentences. RK-14 and the section 13 row. Header Unresolved issues. Two stale-text bullets in section 15. |
| R3-2 | R3-2 | RQ-08, RQ-09 and section 6 step 1. |
| R3-3 | R3-3 | Four stale-text bullets, the S07 bullet addition, and the paragraph under the list in section 15. |
| R3-4 | R3-4 (also the old F-4 of round 2 and F-8 of round 1) | Six rows and the first line of section 7. |
| R3-5 | R3-5 | Section 6 steps 5 and 6, the sentence under the table, and the section 9 route table. |
| R3-6 | R3-6 | RQ-62, section 6 steps 2 to 4, RQ-32, RQ-34, RQ-15, RQ-18, RQ-31, RQ-40, RQ-52, section 15 lines and the count of Open question lines. |
| R3-7 | R3-7 | RQ-05, RQ-06, RQ-35, RQ-43, RQ-63, section 5 route table, section 7 sentence, section 8 label rows and the gate row. |
| R3-8 | R3-8 | Section 7 failure table row, the paragraph under it, the outcome table row, RQ-24, RQ-54 and the Limits bullet. |
| R3-9 | none (the owner raised it after the review) | Section 15 heading "How S07 reports a gap" and its two paragraphs. |

### Items for the next S06R

These are not fixes and this stage did not act on them. **Inference.**

- RQ-30 says the route "writes the reason in the audit row". RQ-70 says the audit row uses `failmode.forbidden_field_in_prompt`. The new section 7 paragraph says the audit row stores no reasons (`audit_query.py` line 128) and "S07 keeps this behaviour". The two statements pull in different directions. The audit row has no key for a reason today. The decisions do not say which one wins, so I changed neither.
- The two "output policy" hits in section 15 are quotes of stale text in other files. A search for the phrase will find them. They are the only hits.
- The owner edits outside this stage are still to do (see Residual risks in the header). Several of them change the files that S07 and S08 read.

## Round 4, 2026-10-13

### Fix source

| Field | Value |
|---|---|
| Path | The owner's request in chat on 2026-10-13: "Do the fixes for Risk 1 and Risk 2 to all the required files and provide steps that I need to execute to resolve these issues." There is no new review file. |
| Where the two risks come from | Item 3 (Major risks) of the round 3 final response, and the "Items for the next S06R" section of round 3 in this file. |
| Newest review | `docs/prd/prd-review.md` (2026-10-13, review v3.0, PASS, "Fixes required: None"). It is unchanged. |
| Semantic layer version | `1.1.1`. Round 4 adds no YAML id. |

### Fix list

| # | Fix |
|---|---|
| R4-1 | RQ-30 and RQ-70 said the route writes the reason in the audit row. The audit row has no key for a reason (`audit_query.py` line 128), and the section 7 paragraph says so. Settle it with option A: the reasons list in the response body holds the reason. The audit row holds the action word `policy.hold` and the outcome only. |
| R4-2 | The owner edits that round 3 listed but did not make. Make them in the files outside the PRD. |

### Decisions for this round

The owner read three options in chat (A: reason in the response body, B: a new reason key in the audit row, C: S07 reports the gap). The owner confirmed option A in chat on 2026-10-13, after the fixes were made. Option B stays a later ADR. For R4-2 the words are the "Owner edits outside this stage" lines of the round 3 Decisions block, above in this file.

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| R4-1 | apply, option A | It matches the code. `audit_query.py` line 128 says "The reasons and the policy version are not stored on any row." RQ-64 already has the page show the reason from the response body. The section 7 paragraph says the audit row stores no reasons. Option B needs a new YAML id, a new ADR, a layer version change and S07 code, so it is a design change and not a fix. **Verified Fact** for the code lines. **Inference** for the choice. |
| R4-2 | apply | Nine files outside the PRD are edited. Four lines are not on the round 3 list and say the same thing: `optimization-backlog.md` line 129, `Risk Management.md` lines 263 and 279, and `playbook/S06-prd.md` line 58. They are edited too, because they carry the old rule. `optimization-backlog.md` lines 24 and 121 were on the list, and they hold no stale text, so they are not edited. |

Where I used my own words besides the exact text in the block:

- `Risk Management.md` line 95. The block gives "Those three routes do not exist yet." In that place no sentence names the three routes, so I wrote "The storm, recommend and approval routes do not exist yet. The PRD requires each one to refuse a call with no header (RQ-11, RQ-28, RQ-35)."
- `playbook/S07-application-and-demo.md` lines 34, 36 and 37. The block gives the content, not full sentences. I wrote each as a short sentence in the style of the line.
- `Risk Management.md` line 219 reads "the same output checks" with "to run again on a stored answer", so the sentence still reads.
- `S05R_Decisions_Taken.md` line 26. The count is 13, and the new row "Decided later in ADR 0003" has count 1. The total stays 20 (5 + 1 + 13 + 1).
- `docs/prd/prd.md` section 15. The list "Stale text found while writing" is replaced by one paragraph that says round 4 closed it. I checked each stale line first (see "Searches" below).

### Edit list

Line numbers are the physical lines after the edits. Files changed in this round: `prd.md`, `traceability.md`, `prd-fixes.md`, and nine files outside the PRD, as listed.

1. **R4-1.** `docs/prd/prd.md`, header, Date / version, line 7.
   - Old: v1.4. S06R fixes applied, round 3. Fixes R3-1 to R3-9. The review says Fixes required: None. The owner's Decisions block closes R3-1 to R3-8. The owner raised R3-9 after the review.
   - New: v1.5. S06R fixes applied, round 4. Round 4 closes R4-1 (the reason of a held answer is in the response body, not in the audit row) and R4-2 (the owner edits in files outside the PRD). Round 3 closed R3-1 to R3-9.
2. **R4-1.** `docs/prd/traceability.md`, header, Date / version, line 6.
   - Old: v1.4. S06R fixes applied, round 3. Fixes R3-1 to R3-9. The review says Fixes required: None. The owner's Decisions block closes R3-1 to R3-8. The owner raised R3-9 after the review.
   - New: v1.5. S06R fixes applied, round 4. Round 4 closes R4-1 (the reason of a held answer is in the response body, not in the audit row) and R4-2 (the owner edits in files outside the PRD). Round 3 closed R3-1 to R3-9.
3. **R4-1.** `docs/prd/prd.md`, header, Status, line 9.
   - Old: CONDITIONAL PASS. S06R fixes applied, round 3. All 73 requirements
   - New: CONDITIONAL PASS. S06R fixes applied, round 4. All 73 requirements
4. **R4-1.** `docs/prd/prd.md`, header, Status, line 9.
   - Old: ADR 0003 records the three risk decisions.
   - New: ADR 0003 records the three risk decisions. Round 4 closed R4-1 and R4-2.
5. **R4-1.** `docs/prd/traceability.md`, header, Status, line 8.
   - Old: CONDITIONAL PASS. S06R fixes applied, round 3. 73 of 73 requirements have a YAML id and a named test. 44 tests are planned for stage S07. Round 3 closed R3-1 to R3-9.
   - New: CONDITIONAL PASS. S06R fixes applied, round 4. 73 of 73 requirements have a YAML id and a named test. 44 tests are planned for stage S07. Round 3 closed R3-1 to R3-9. Round 4 closed R4-1 and R4-2.
6. **R4-2.** `docs/prd/prd.md`, header, Unresolved issues, line 12.
   - Old: Section 15 lists stale lines in files outside this stage. S07 does not follow them.
   - New: Round 4 corrected the stale lines that earlier rounds found in files outside the PRD (section 15).
7. **R4-1.** `docs/prd/prd.md`, RQ-30, line 331.
   - Old: and writes the reason in the audit row. The list is short
   - New: The reasons list in the response body holds `failmode.command_text_in_recommendation`. The audit row holds the action word `policy.hold` and the outcome. It stores no reason (section 7). The list is short
8. **R4-1.** `docs/prd/prd.md`, RQ-70, line 414.
   - Old: Until that id exists, the audit row uses `failmode.forbidden_field_in_prompt`.
   - New: Until that id exists, the reasons list in the response body uses `failmode.forbidden_field_in_prompt`. The audit row holds the action word `policy.hold` and the outcome, and no reason.
9. **R4-1.** `docs/prd/prd.md`, section 15, Open question for RQ-70, line 583.
   - Old: Until it exists, the audit row uses `failmode.forbidden_field_in_prompt`.
   - New: Until it exists, the reasons list in the response body uses `failmode.forbidden_field_in_prompt`. The audit row stores no reason.
10. **R4-1.** `docs/prd/prd.md`, section 7, paragraph under the failure table, line 184.
   - Old: The audit row stores no reasons. A refused call has
   - New: The audit row stores no reasons. This includes the reasons of RQ-30 and RQ-70: they appear in the response body only. A refused call has
11. **R4-2.** `docs/prd/prd.md`, section 15, list 'Stale text found while writing', line 605.
   - Old: the whole list of nine stale-text bullets, and the first two sentences of the paragraph under it (see the round 3 edit list for the bullets)
   - New: **Stale text found while writing (Verified Fact).** Round 4 closed this list on 2026-10-13. The owner edits recorded in `docs/prd/prd-fixes.md` (round 4) corrected every line that the list named. The files are `docs/02-baseline/semantic-layer-revision.md`, `docs/02-baseline/S05R_Decisions_Taken.md`, `docs/ADR/0003-s06-risk-recommendations.md`, `docs/12-finops/optimization-backlog.md`, `docs/prd/Risk Management.md`, ` ... (cut)
12. **R4-2.** `playbook/S07-application-and-demo.md`, line 34 (storm route).
   - Old: returns raw count, deduped count, and the alarm ids.
   - New: returns the raw count, the deduped count, the flagged count and the rows (alarm_id, device_id, dedupe_key, flag word).
13. **R4-2.** `playbook/S07-application-and-demo.md`, line 36 (recommend route).
   - Old: returns one of RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK; never EXECUTE from this route;
   - New: returns HOLD_FOR_REVIEW with the sentence on a healthy call, and HOLD_FOR_REVIEW with no text or BLOCK on a stop; never RECOMMEND_ONLY or EXECUTE from this route;
14. **R4-2.** `playbook/S07-application-and-demo.md`, line 37 (approvals route).
   - Old: a named human persona records approve or reject with a reason; writes an audit row with approval_id; returns the decision. It does not execute anything.
   - New: a named human persona sends decision (yes or no) in a JSON body; the server sets approver and makes the approval id; it writes the audit row first; it returns approval_id, decision, approver, record_id and correlation_id. There is no reason field. It does not execute anything.
15. **R4-2.** `docs/ADR/0003-s06-risk-recommendations.md`, line 46.
   - Old: S07 never stores a BLOCK or HOLD answer. The output policy runs again on a stored answer.
   - New: S07 never stores an answer that has no text. That means a BLOCK, or a HOLD_FOR_REVIEW with no sentence. It stores a HOLD_FOR_REVIEW recommendation that has a sentence and passed every output check. The output checks run again on a stored answer.
16. **R4-2.** `docs/12-finops/optimization-backlog.md`, line 37.
   - Old: Run the output policy on that answer again.
   - New: Run the output checks on that answer again.
17. **R4-2.** `docs/12-finops/optimization-backlog.md`, line 124.
   - Old: An answer is stored only when the outcome is `RECOMMEND_ONLY`. A `BLOCK`, a `HOLD_FOR_REVIEW`, a timeout, and a bad answer are never stored.
   - New: An answer is stored only when it has text and passed every output check. A BLOCK, a HOLD_FOR_REVIEW with no text, a timeout and a bad answer are never stored.
18. **R4-2.** `docs/12-finops/optimization-backlog.md`, line 129 (not on the owner list, same rule).
   - Old: and `outcome` `RECOMMEND_ONLY`. The row must say a stored answer was used.
   - New: and `outcome` `HOLD_FOR_REVIEW`. The row must say a stored answer was used.
19. **R4-2.** `docs/prd/Risk Management.md`, line 95.
   - Old: The storm, recommend and approval routes already refuse a call with no header.
   - New: The storm, recommend and approval routes do not exist yet. The PRD requires each one to refuse a call with no header (RQ-11, RQ-28, RQ-35).
20. **R4-2.** `docs/prd/Risk Management.md`, line 219.
   - Old: RQ-31 already requires the output policy to run again on a stored answer
   - New: RQ-31 already requires the same output checks to run again on a stored answer
21. **R4-2.** `docs/prd/Risk Management.md`, line 221.
   - Old: Never store BLOCK or HOLD answers. Run the output policy again on a stored answer.
   - New: Never store an answer that has no text (a BLOCK, or a HOLD_FOR_REVIEW with no sentence). Run the same output checks again on a stored answer.
22. **R4-2.** `docs/prd/Risk Management.md`, line 223.
   - Old: add the "never store BLOCK or HOLD" rule as extra text on RQ-31.
   - New: add the "never store an answer that has no text (a BLOCK, or a HOLD_FOR_REVIEW with no sentence)" rule as extra text on RQ-31.
23. **R4-2.** `docs/prd/Risk Management.md`, line 263 (not on the owner list, same rule).
   - Old: Keep it if S07 has time. Never store BLOCK or HOLD. Cap the store.
   - New: Keep it if S07 has time. Never store an answer that has no text (a BLOCK, or a HOLD_FOR_REVIEW with no sentence). Cap the store.
24. **R4-2.** `docs/prd/Risk Management.md`, line 279 (not on the owner list, same rule).
   - Old: RQ-31 extra text. Never store a BLOCK or HOLD answer.
   - New: RQ-31 extra text. Never store an answer that has no text (a BLOCK, or a HOLD_FOR_REVIEW with no sentence).
25. **R4-2.** `docs/02-baseline/S05R_Decisions_Taken.md`, line 26.
   - Old: | Kept deferred, each with a named trigger | 14 | D-01, D-02, D-04, D-05, D-07, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20 |
   - New: | Kept deferred, each with a named trigger | 13 | D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20 | then a new row: | Decided later in ADR 0003 | 1 | D-07 |
26. **R4-2.** `docs/02-baseline/semantic-layer-revision.md`, line 8.
   - Old: and 14 stay deferred.
   - New: and 13 stay deferred (D-07 was decided later in ADR 0003).
27. **R4-2.** `docs/02-baseline/semantic-layer-revision.md`, line 442.
   - Old: - Next: S06 writes `1.1.0` into the PRD header. S08 hashes the tree at `1.1.0` for the second model.
   - New: - Next: S06 writes `1.1.1` into the PRD header. S08 hashes the tree at `1.1.1` for the second model.
28. **R4-2.** `playbook/S06R-prd-review.md`, line 47.
   - Old: the 300 second answer store stays and never stores BLOCK or HOLD.
   - New: the 300 second answer store stays and never stores an answer that has no text (BLOCK, or HOLD_FOR_REVIEW with no sentence).
29. **R4-2.** `playbook/S06R-prd-review.md`, line 66.
   - Old: It never holds BLOCK or HOLD.
   - New: It never holds an answer that has no text (BLOCK, or HOLD_FOR_REVIEW with no sentence).
30. **R4-2.** `playbook/README.md`, line 46.
   - Old: Runs only when S06R has a FAIL row.
   - New: Runs when S06R has a FAIL row, or when the owner chooses to fix Other findings before S07.
31. **R4-2.** `playbook/S06-prd.md`, line 58 (not on the owner list, same D-07 fact).
   - Old: The 14 deferred items (D-01, D-02, D-04, D-05, D-07, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20) listed as open items, each with its trigger.
   - New: The 13 deferred items (D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20) listed as open items, each with its trigger. D-07 is decided in ADR 0003 and is not on this list.

### RQ ids touched

| Row | File | What changed |
|---|---|---|
| RQ-30 | `prd.md` line 331 | The reason sentence. The test name and the YAML ids stay. |
| RQ-70 | `prd.md` line 414 | The reason sentence. The test name and the YAML ids stay. |

`traceability.md` has no row change. Its RQ-30 and RQ-70 rows cite the same ids and the same tests. Only its header changed (version, Status).

### Agreement check

Every sentence below now says the same thing: the reason is in the response body, and the audit row stores the action word and the outcome only.

| Where | What it says now |
|---|---|
| `prd.md` line 331 (RQ-30) | The reasons list in the response body holds `failmode.command_text_in_recommendation`. The audit row holds `policy.hold` and the outcome. It stores no reason. |
| `prd.md` line 414 (RQ-70) | The reasons list in the response body uses `failmode.forbidden_field_in_prompt` until a better id exists. The audit row holds `policy.hold` and the outcome, and no reason. |
| `prd.md` line 583 (Open question for S03) | The reasons list in the response body uses `failmode.forbidden_field_in_prompt`. The audit row stores no reason. |
| `prd.md` line 184 (section 7, paragraph) | The audit row stores no reasons. This includes RQ-30 and RQ-70. They appear in the response body only. |
| `prd.md` line 401 (RQ-64) | The page shows the reason. It reads it from the response body. No change needed. |
| `prd.md` line 325 (RQ-24) | The test checks no reason string. No change needed. |
| `audit_query.py` line 128 | "The reasons and the policy version are not stored on any row." The code matches the PRD. |

### Version check

| Item | Result |
|---|---|
| `prd.md` header | v1.5, round 4. |
| `traceability.md` header | v1.5, round 4. |
| Raise count | Once, from v1.4 to v1.5, with the same number in both. |
| Semantic layer version | `1.1.1`. |

### Checks 8a to 8h

All outputs are from 2026-10-13, run after the edits. The scripts for 8a to 8d and 8h are temporary Python files. They are not part of the repo. **Verified Fact.**

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
duplicate prd ids: none
duplicate trace ids: none
counts equal: True
id set difference: none
ids are RQ-01 to RQ-73: True
```

Matches the locked fact: 73 rows.

#### 8b. YAML id lookup

```
YAML ids collected from seven files: 757
YAML ids cited in requirement rows (distinct): 123
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 188
audit action words resolved via value: [('policy.deny', 'status.code.audit_action.policy_deny'), ('policy.hold', 'status.code.audit_action.policy_hold'), ('record.read', 'status.code.audit_action.record_read')]
expected misses (PROPOSED words on the Open question for S03 line):
    ai.approval first seen ('prd.md', 342) ; named on the Open question line [601]
    ai.recommendation first seen ('prd.md', 319) ; named on the Open question line [601]
    record.storm_read first seen ('prd.md', 307) ; named on the Open question line [601]
unresolved backticked id-shaped tokens (other than file names): none
```

757 ids match the locked fact. The three expected misses are the PROPOSED words on the Open question for S03 line. **Verified Fact.**

#### 8c. Row-by-row compare

```
mismatches: none
```

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 44
```

Matches the locked fact: 29 exist, 44 are planned for S07.

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
.........................................                                [100%]
41 passed in 2.26s
```

(`python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`.) Matches the locked fact.

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines (SHA-256 `BC2D23CDA9734222576DE51B7EC2917FE90C0C326DDC7DBD1FCB74B6ED482FAD`). After the test run it had 241 lines. After the restore it had 240 lines and the same SHA-256. The command named the 29 existing test ids that `prd.md` section 10 lists.

```
SKIPPED [1] policy\tests\test_policy_python.py:577: opa binary not on PATH
40 passed, 1 skipped, 60 warnings in 5.02s
```

Matches the locked fact: 40 passed, 1 skipped. The skip is the `opa` test (RQ-59).

#### 8g. git status

After the last edit, the files that `git status` shows as changed or new, other than caches and `logs/audit.log`: `docs/02-baseline/S05R_Decisions_Taken.md`, `docs/02-baseline/semantic-layer-revision.md`, `docs/12-finops/optimization-backlog.md`, `playbook/README.md`, `playbook/S06-prd.md`, `playbook/S06R-prd-review.md`, `playbook/S07-application-and-demo.md` and the untracked `docs/prd/` and `docs/ADR/0003-s06-risk-recommendations.md`. `playbook/S08-second-model.md`, `playbook/STATUS.md`, `Project_Acronyms.md` and `transcript/chat_transcript.md` were already modified before this round. This round did not touch them, except that the chat transcript gets its new turn. The semantic layer, `apps/`, `tests/` and `data/` show no change. `logs/audit.log` was restored. **Verified Fact.**

File hashes after the last edit (SHA-256), so the next stage can see whether the PRD changed:

- `prd.md`: `3A13E19C56BFC8F7BFAA9B94228492FD776BB6432B6E0397C4A136F0AF7A9E91`
- `traceability.md`: `4E811E86922EF9965BC59636D104DDF411B596BC7E6F29EBA9CAE77A45C9FA84`

#### 8h. Open question lines

```
Open question for S03 lines in prd.md section 15: 13
  count statement: prd.md line 12 -> Thirteen Open question
  count statement: traceability.md line 11 -> Thirteen Open question
count equals 13: True
```

The Open question for S03 line about RQ-70 stays, because the failmode id for a forbidden value in an answer still does not exist. Only its words changed. **Verified Fact.**

#### Searches

I searched the nine outside files, `prd.md` and `traceability.md` for the old words.

| Term | Result |
|---|---|
| "output policy" | No hit in any of the 11 files. |
| "BLOCK or HOLD" | One hit in `prd.md` line 124 (step 3). It reads "A stop returns BLOCK or HOLD_FOR_REVIEW with no text", which is correct. No other hit. |
| "stores or holds" | No hit. |
| "14 stay deferred" | No hit. |
| "writes the reason in the audit row", "audit row uses" | No hit. |
| "outside this stage" | One hit in `semantic-layer-revision.md` line 60 (CSV files). It is old text about a different subject. |
| "Fifteen", "fifteen" | No hit. |
| "RECOMMEND_ONLY" in `optimization-backlog.md` | No hit. In `playbook/S07-application-and-demo.md` it appears only in the line that says the recommend route never returns it, and in the list of four outcomes. |
| "Next: S06 writes" in `semantic-layer-revision.md` | Line 442 names `1.1.1` twice. |

### Done test

In `prd.md` RQ-01 the YAML id `status.code.health.ok` was changed to `status.code.health.does_not_exist`. Check 8b then printed:

```
unresolved cited ids: [('RQ-01', 'status.code.health.does_not_exist')]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash before the change (`3A13E19C56BFC8F7BFAA9B94228492FD776BB6432B6E0397C4A136F0AF7A9E91`). Check 8b then printed:

```
unresolved cited ids: none
unresolved backticked id-shaped tokens (other than file names): none
```

**Verified Fact.**

### Map from the fixes to the risks

| Fix | Risk it closes | Edits that address it |
|---|---|---|
| R4-1 | RQ-30 and RQ-70 against the section 7 paragraph | RQ-30, RQ-70, the section 7 paragraph, the Open question for S03 line about RQ-70, and the headers of `prd.md` and `traceability.md`. |
| R4-2 | The owner edits outside this stage | Edits 12 to 31 in the edit list, and the paragraph that replaces the stale-text list in `prd.md` section 15. |

### Items for the next S06R

These are not fixes and this round did not act on them. **Inference.**

- The audit row has no key for a reason. If the team wants a person to see why a case was held by reading `logs/audit.log`, it needs option B: a new key, a YAML id under a new ADR, a layer version change and S07 code. Until then the response body holds the reason.
- `playbook/S07-application-and-demo.md` item 3 says the page lets a person "approve or reject". The route takes `yes` or `no`. The page words and the route words differ. This is a page label and not a rule, so it is left alone.
- Four older records still say 14 deferred items or ask for the D-07 decision: `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` line 94, `docs/02-baseline/S05R_Decisions.md` line 649, `playbook/STATUS.md` lines 63 and 64, and `playbook/S06-prd.md` line 51. They record what was true on the day they were written. The owner may choose to add a note.
- The round 3 section of this file keeps its own text, including the open item that round 4 closed. It is the record of what round 3 found.

## Round 5, 2026-10-13

### Fix source

| Field | Value |
|---|---|
| Path | `docs/prd/prd-review.md` |
| Header date and version | 2026-10-13, v4.0 of this review (S06R round 4, the review of PRD v1.5). Semantic layer version read from `semantic-layer/README.md`: `1.1.1`. |
| Stage status | **BLOCKED.** One row is FAIL: P2, and the same finding in P12.8. P1, P3, P4, P9 and P13 are PASS. |

### Fixes required (copied word for word)

The review has one numbered fix.

| Fix | Closes | File and line | What to change |
|---|---|---|---|
| **F-1** | P2, P12.8 | `prd.md` lines 157, 162, 317, 319; section 15 | **Recommended option.** Remove the defining sentence at line 157. At lines 162, 317 and 319, replace "a healthy call" with the plain condition: "a call with an allow row to which no row of the failure table applies". Leave the planned test name `test_healthy_recommend_is_hold_for_review_with_the_sentence` as it is, because it is an identifier and not a PRD term. No count changes, and `traceability.md` needs no edit. **Other option.** Keep "healthy call" and add one "Open question for S03:" line in section 15 that says the word has no YAML id and no glossary row and that the PRD does not explain it. Then also delete the defining sentence at line 157, because an Open question word must be "listed and not defined". This option raises the Open question count from 13 to 14 in the PRD header (line 12), `traceability.md` (header), line 620 and the S06F count checks. |

### Other findings named by the Decisions block (copied word for word)

The Decisions block closes X-1 to X-7. It leaves X-8 as it is. All eight rows are copied.

| # | Finding | Evidence | Impact | Label |
|---|---|---|---|---|
| X-1 | **Needs an owner answer before S07.** RQ-31 names `docs/12-finops/optimization-backlog.md` as its source design. That file disagrees with RQ-31 on three points. (a) Key: the file says the key holds `prompt_hash`, `model_version` and the policy version (line 125). RQ-31 says an entry is found by `prompt_hash` alone. (b) Clearing: the file empties the store when the policy or model version changes (line 127). RQ-31 says nothing about it. (c) Size: the file says "500 stored answers in memory, oldest removed first" (line 128), with no PROPOSED label. RQ-31, ADR 0003 and the locked fact say the cap is PROPOSED and has no number. | `prd.md` line 332, line 514; `optimization-backlog.md` lines 125, 127, 128; ADR 0003 line 46 | An S07 builder who opens the cited design file finds a cap number and a different key. Line 605 tells S07 to stop and report a gap. The 500 is a cutoff with no PROPOSED label, which is a P8 problem in a file outside this review's scope. | **Verified Fact** for the lines. **Inference** for the impact. |
| X-2 | RQ-69 says a correlation id over 128 characters "is refused when the audit row is written". It does not say what the caller gets (status code, body), whether the call still returns data, or whether a refusal row is written. The open question at line 581 covers only the word stored for an unknown role. | `prd.md` lines 413, 581 | Two builders will choose different replies. The planned test `test_unknown_role_word_is_not_stored_as_sent` checks the role word and not the long id. | **Verified Fact** for the text. **Inference** for the impact. |
| X-3 | The real data has two alarm rows that the PRD does not mention. `alarms.csv` line 2 (`REC-0001`, storm `STO-00001`) has `device_id` `DEV-00001`, and `devices.csv` has no such device (its first id is `REC-0001`). Line 353 (`ALA-BAD1`) has a blank `storm_batch_id`, a blank `device_id` and a blank `dedupe_key`. So (a) the page lists `DEV-00001` for `STO-00001`, and the lookup then gives 404 and the recommend call gives BLOCK. (b) The one blank-key row can never appear in a storm reply, because its storm id is blank. The RQ-08 "held aside" rule needs a test fixture, not the real file. (c) RQ-62 does not say what the page does with a blank `device_id`. | `alarms.csv` lines 2 and 353; `devices.csv` line 2; `prd.md` lines 300, 399 | None blocks a build. A demo that picks `STO-00001` meets the 404 path. S07 must know the held-aside test needs a fixture. | **Verified Fact** (script on the CSV files). **Inference** for the impact. |
| X-4 | Section 7 says each cell is "quoted from `ai-qualification.md`" and that an Outcome of none means that file names no outcome word. The Outcome cell for `ai_use.remediation_execution` says EXECUTE (line 143). The S2Q row names no outcome word. The word comes from the YAML (`ai-context-policy.yaml` line 680). | `prd.md` lines 134, 143; `ai-qualification.md` row "Remediation execution" | None for a builder. The sentence at line 134 is wrong for one row. | **Verified Fact.** |
| X-5 | The PROPOSED limit of 10 running model calls appears at lines 162, 174, 184 and 195 with no PROPOSED word or pointer to N-05. It is labelled in RQ-54, section 11 and N-05. | `prd.md` lines 162, 174, 184, 195, 382, 442, 551 | A reader of section 7 alone sees an unlabelled cutoff. | **Verified Fact** for the text. |
| X-6 | D-18 is listed as deferred (line 532), and the section 15 list "Planned YAML additions (decided, built in S07...)" names the cache flag under D-18 (line 603). RQ-31 says "the row says no model ran" but names no key. The key is the D-18 cache flag. The two statements fit once read together (the trigger fires when the cache is built). The PRD does not say so. | `prd.md` lines 332, 532, 603; `S05R_Decisions_Taken.md` row D-18 | The locked fact says D-18 stays deferred. A strict reader sees a deferred item that is also planned. | **Verified Fact** for the text. **Inference** for the reading. |
| X-7 | Small plain-speech items. (a) RQ-44 says "case id" and the route says `correlation_id`. (b) RQ-52 uses "audit action word" with no explanation. (c) RQ-33 and its test name use "execute check" and "approval check", which are not in the YAML. | `prd.md` lines 343, 363, 371 | None blocks a build. Each can mislead a reader once. | **Verified Fact** for the text. |
| X-8 | Workflow step 5 carries `role.admin` (an API role, not a persona) and step 6 carries "none". Line 130 says why. A strict reader of "each step carries a verb and a persona" finds two steps that do not. | `prd.md` lines 126, 127, 130 | None for a builder. | **Verified Fact** for the text. **Inference** for the reading. |

### Decisions for this round

Pasted in the prompt:

```text
Round 5. The review (`docs/prd/prd-review.md`, v4.0, BLOCKED) lists one fix under "Fixes required": F-1. It closes the one FAIL row, P2, and the same finding in failure-list item 8 (P12.8). The lines below also close "Other findings" X-1 to X-7 from that review. X-8 is left as it is. Apply every line except X-8. Edit only prd.md, traceability.md and prd-fixes.md. The "Owner edits outside this stage" line lists edits that this stage does not make.

F-1 (the words "healthy call"). Apply option A. Decision: the PRD does not define "healthy call". It writes the condition in plain words. No Open question line is added. The Open question count stays 13.
  a) Section 7, paragraph "The four outcomes". Delete the sentence "In this PRD, a healthy call is a call from a caller with an allow row to which no row of the failure table below applies." Keep every other sentence of the paragraph.
  b) Section 7, outcome table, row HOLD_FOR_REVIEW. In the column "Which route in this PRD can return it", replace "on a healthy call (policy row O2)" with "on a call that no row of the failure table applies to (policy row O2)". In the column "Text shown", replace "The sentence on a healthy call. No text on a failure." with "The sentence when no failure row applies. No text on a failure."
  c) RQ-16. Replace "A healthy call returns the policy outcome RECOMMEND_ONLY" with "A call with an allow row, to which no row of the failure table applies, returns the policy outcome RECOMMEND_ONLY". Keep the rest of the cell.
  d) RQ-18. Replace "A healthy call returns HTTP 202" with "A call with an allow row, to which no row of the failure table applies, returns HTTP 202". Replace "A healthy call writes one `ai.recommendation` audit row." with "A call that returns the sentence writes one `ai.recommendation` audit row." Keep the rest of the cell.
  e) Do not rename the planned test `test_healthy_recommend_is_hold_for_review_with_the_sentence`. It is an identifier and not a PRD term. `traceability.md` keeps it as it is.
  f) Do not write a new sentence that defines any word. After the edits, search prd.md and traceability.md for "healthy". The only hits left are the test name in RQ-18 of prd.md and the two rows of traceability.md that hold that test name. Section 2 ("Terms come from the glossary and the YAML. This PRD does not define a term.") and the gate row "The PRD and the YAML agree" stay as they are. They are true again.

X-1 (RQ-31 and the design file it cites). Apply. Decision: RQ-31 stays as it is. The owner decided the store rule in round 3 (R3-1 a) and ADR 0003 decision 3 fixes it: an entry is found by `prompt_hash` alone, and the cap is PROPOSED with no number. The design file is the one that changes. Reason for the key (Inference): one stub model and one policy version exist in this packet, and a restart empties the store, so a key with a model version and a policy version adds nothing here.
  a) Section 15, paragraph "Stale text found while writing". After the sentence "If a stale line turns up later, the requirement row of this PRD applies." add: "Round 5 found one more case. `docs/12-finops/optimization-backlog.md` lines 125, 127 and 128 give a key of `prompt_hash`, model version and policy version, a clear when either version changes, and a cap of 500 stored answers. RQ-31 says an entry is found by `prompt_hash` alone and the cap is PROPOSED with no number. RQ-31 applies. The file is outside this stage." Before you write it, read those three lines of optimization-backlog.md. If they differ from the sentence, the file wins, and you change the sentence to match.
  b) Add no new RQ row, no YAML id, no Open question line and no number. Do not edit optimization-backlog.md.

X-2 (a correlation id over 128 characters on a write). Apply. Decision: the call is not refused. The server swaps the long id for a new UUID, as it does for a missing header (RQ-49). The long text is never stored. The audit route keeps its own 400 for a long id in the path (RQ-44). This adds no status code and no YAML id.
  a) RQ-69. Replace the whole Requirement cell with: "An unknown role word is not stored as sent. A correlation id sent in `X-Correlation-Id` that is longer than 128 characters is not stored either. The server makes a new UUID and uses it, as it does for a missing header (RQ-49). The call is not refused, and the long text appears nowhere in the audit log or the response header. The audit route keeps its own HTTP 400 for a long id in the path (RQ-44). The test sends an `X-Correlation-Id` of 129 characters and checks that the audit row and the response header hold a new UUID. The 128 limit is PROPOSED. Owner: Team-Force. The word to store for an unknown role is an Open question for S03."
  b) Section 12, RK-03, column "What the app does". Replace "applies the 128 limit at write time (RQ-69)" with "swaps a header id over the 128 limit for a new UUID at write time (RQ-69)".
  c) Search the whole PRD for "128" and "write time" and "written, not only when it is read". Make every hit agree with a) and b). The planned test name `test_unknown_role_word_is_not_stored_as_sent` stays. Its expected values now include the 129 character case. `traceability.md` section 1 holds no requirement text, so only its header changes.

X-3 (alarm rows that have no usable device or storm). Apply. Decision: the PRD states the facts and the page behaviour. Before you write any of it, read alarms.csv line 2 and line 353, and check whether devices.csv holds a device_id DEV-00001 (the check on 2026-10-13 found none, and found that line 353 is blank except for its alarm id). If the files differ from the text below, the files win, and you change the text to match.
  a) RQ-08. At the end of the Requirement cell add: "In `data/synthetic/alarms.csv`, the only row with a blank `dedupe_key` is `ALA-BAD1` at file line 353. That row has a blank `storm_batch_id` too, so no storm reply lists it. The held-aside rule is tested with a small fixture and not with that file."
  b) RQ-62. At the end of the Requirement cell add: "The page does not list a blank `device_id`. A `device_id` with no device row is listed. Example: storm `STO-00001` has one row (file line 2 of `alarms.csv`), and its `device_id` is `DEV-00001`. `devices.csv` has no `DEV-00001`. The lookup then returns 404 (RQ-03), the recommendation returns BLOCK (RQ-20), and the page shows each reply."
  c) Section 12, RK-17. At the end of the "Risk" cell add: "Two alarm rows have no usable device: file line 2 (`REC-0001`) names `DEV-00001`, which `devices.csv` lacks, and file line 353 (`ALA-BAD1`) is blank except for its `alarm_id`." In the "Label" cell, add `data/synthetic/alarms.csv` lines 2 and 353 to the Verified Fact pointer.
  d) Add no RQ row and no test name. The planned tests keep their names.

X-4 (the Outcome cell for remediation execution). Apply. Decision: say where the Outcome column comes from.
  a) Section 7, first paragraph, "Pick, agency and approval point." Replace the sentence "Each cell below is quoted from `docs/02-baseline/ai-qualification.md`. This table lists all 11 AI uses. An Outcome of none means that file names no outcome word for that use." with "The Pick, Agency and Human approval point cells below are quoted from `docs/02-baseline/ai-qualification.md`. The Outcome cell is the outcome word that file names. Only `ai_use.remediation_execution` takes its outcome from the YAML (`outcome.execute`), because the file names none for it. This table lists all 11 AI uses. An Outcome of none means neither source names an outcome word for that use." Before you write it, read the Outcome of every ai_use in ai-context-policy.yaml. If another use has an outcome that ai-qualification.md lacks, name it in the sentence too.

X-5 (the limit of 10 running calls). Apply. Decision: label every mention in section 7.
  a) Section 7, outcome table, row HOLD_FOR_REVIEW. Replace "a full limit of 10 running calls" with "a full limit of 10 running calls (PROPOSED, N-05. Owner: Team-Force)".
  b) Section 7, failure table, row "10 model calls are already running". Change the Cause cell to "10 model calls are already running (PROPOSED limit, N-05. Owner: Team-Force)".
  c) Section 7, the paragraph that holds the sentence "The failure table names the cause" (line 184 of v1.5), and the other place in section 7 that says "a full limit of 10 running calls" (line 195 of v1.5). After "10 running calls" add " (N-05)" in each place.
  d) Search the whole PRD for "10 running calls", "10 model calls" and "10 calls". Every hit outside RQ-54, section 11 and section 13 carries PROPOSED with N-05, or "(N-05)".

X-6 (D-18 and the cache flag). Apply. Decision: say once why D-18 is on the deferred list and also planned.
  a) Section 13, directly under the table "The 13 items that stay deferred", add: "D-18 stays on this list for every audit field whose feature is not built yet. The trigger of D-18 names the cache flag: 'If the cache is built in S07, the cache flag comes first.' RQ-31 builds the stored-answer store, so S07 adds the cache flag under a new ADR before the route ships. The fields of D-18 whose feature is not built stay deferred."
  b) RQ-31. Replace "A stored answer writes the same `ai.recommendation` audit row, and the row says no model ran." with "A stored answer writes the same `ai.recommendation` audit row, and the row says no model ran. The row says it through the cache flag of D-18. The flag has no YAML id yet. S07 adds it under a new ADR before the route ships." If that sentence is not in the cell in that form, find the sentence that says "no model ran" and add the two new sentences after it.
  c) The Open question count stays 13. Do not add an Open question line for the cache flag. The word "cache" is already on the Open question line about the answer store.

X-7 (small plain-speech items). Apply all three.
  a) RQ-44. Replace "A case id longer than 128 characters" with "A case id (the `correlation_id` in the route path) longer than 128 characters".
  b) RQ-52. At the end of the Requirement cell add: "An audit action word (`status.code.audit_action.*`) is the word in the audit row that names what happened. Example: `record.read`."
  c) RQ-33. Replace "It never fills the approval id input of the execute check." with "It never fills the approval id that the policy checks before an EXECUTE (`provenance.approval_id`, `outcome.execute`)." Search prd.md for "execute check" and "approval check". Change each hit in prose in the same way. Leave test names as they are.

X-8 (steps 5 and 6 of the workflow). Do not apply. Decision: no edit. Round 3 settled both steps (R3-5), and section 6 says why step 5 has an API role and step 6 has no caller. Record X-8 in the edit list as "left as it is" with that reason.

Owner edits outside this stage. This stage makes none of them. The owner makes them by hand before S07 starts. Name them in the Residual risks row of the prd-fixes.md header and do not edit the files. If the owner has not made them when S06R runs again, S06R lists them again as other findings.
  - docs/12-finops/optimization-backlog.md line 125: replace the row with "What the key holds | `prompt_hash` alone (RQ-31 in the PRD). One stub model and one policy version exist, so no other key part is needed in this packet." Line 127: replace the row with "Clear at once | No rule empties the store before its 300 seconds are up. A restart empties it." Line 128: replace the row with "Size limit | The cap on stored answers is PROPOSED. Owner: Team-Force. No number is set (ADR 0003 decision 3). One process only, like the dedupe memory and the audit lock (`recovery-evidence.md`). A restart empties it."
  - playbook/S07-application-and-demo.md line 36: replace "on a healthy call" with "when no failure row applies".

Version and checks for this round. Raise the version of prd.md and traceability.md from 1.5 to 1.6, once, with the same number in both. Add no RQ row, no YAML id and no test name. Keep 73 RQ rows, 29 existing tests, 44 planned tests, 757 ids, 13 Open question lines and layer version 1.1.1. After the edits, search prd.md and traceability.md for "healthy", "healthy call", "execute check", "approval check", "case id", "audit action word", "10 running calls", "10 model calls", "10 calls", "128", "write time", "refused when the audit row is written", "optimization-backlog", "cache flag", "Thirteen" and "13". Every hit must agree with the text above. Every term in the new text must appear in the glossary, in the YAML, or on an Open question for S03 line. No new sentence may define a word.
```

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| F-1 | apply, option A | The Decisions block says so. The PRD stops giving the words "healthy call" a meaning. It writes the condition in plain words. No Open question line is added. The count stays 13. Closes P2 and P12.8. |
| X-1 | apply | RQ-31 stays. The block asks for one sentence in section 15. I read the three lines of `optimization-backlog.md` first, as the block requires. They differ from the sentence in the block, so the file wins and I changed the sentence to match (see "Reads before writing"). |
| X-2 | apply | The call is not refused. The server swaps a header id over 128 characters for a new UUID. No new status code and no YAML id. |
| X-3 | apply | The block says to read `alarms.csv` lines 2 and 353 and `devices.csv` first. I did. The files match the block, so the text is written as given. |
| X-4 | apply | I read the Outcome of every `ai_use` in `ai-context-policy.yaml` first. No other use differs, so the sentence names only `ai_use.remediation_execution`. |
| X-5 | apply | Every mention of the limit of 10 in section 7 now carries PROPOSED with N-05, or "(N-05)". |
| X-6 | apply | One paragraph under the deferred table in section 13 and two sentences in RQ-31. The sentence in RQ-31 was in the form the block names. |
| X-7 | apply | Three small edits (RQ-44, RQ-52, RQ-33). |
| X-8 | left as it is | Round 3 settled both steps (R3-5). Section 6 (line 130) says why step 5 has an API role and why step 6 has no caller. |

**Reads before writing.** Where the block asks me to read a file first, this is what I found. **Verified Fact.**

| Fix | What I read | Result |
|---|---|---|
| X-1 | `docs/12-finops/optimization-backlog.md` lines 125, 127, 128 | Line 125: "`prompt_hash` alone (RQ-31 in the PRD). One stub model and one policy version exist in this packet, so no other key part is needed." Line 127: "No rule empties the store before its 300 seconds are up. A restart empties it." Line 128: "The cap on stored answers is PROPOSED. Owner: Team-Force. No number is set (ADR 0003 decision 3). One process only ... A restart empties it." These are not the lines that review v4.0 read (a key with model and policy version, a clear on a version change, a cap of 500). The file was changed at 08:47 on 2026-10-13, before this round started. So the sentence in the block does not match the file. The file wins. The new text in `prd.md` section 15 says what review v4.0 read, says what the lines read now, and says they agree with RQ-31. |
| X-3 | `data/synthetic/alarms.csv` lines 1, 2 and 353; `data/synthetic/devices.csv` | Line 2: `REC-0001,DEV-00001,...,DED-00001,degraded,STO-00001`. Line 353: `ALA-BAD1,,,,,,,,,` (blank except the alarm id). A script found one row with a blank `dedupe_key` (line 353) and one row with a blank `device_id` (line 353). `STO-00001` has one row (line 2). `devices.csv` has no `device_id` `DEV-00001` (its first id is `REC-0001`). All match the block. |
| X-4 | `ai_use` outcomes in `ai-context-policy.yaml` (lines 574 to 693) and the S2Q rows in `ai-qualification.md` (lines 38 to 48) | YAML outcomes: `incident_summary` RECOMMEND_ONLY, `next_action_recommendation` HOLD_FOR_REVIEW, `configuration_suggestion` HOLD_FOR_REVIEW, `remediation_execution` EXECUTE, and the other seven null. `ai-qualification.md` names an outcome word for the first three and for no other use. So only `remediation_execution` takes its outcome from the YAML. |
| Owner edits | `playbook/S07-application-and-demo.md` line 36; `docs/12-finops/optimization-backlog.md` lines 125, 127, 128 | Line 36 of the playbook already reads "when no failure row applies". The three backlog lines already carry the new rules. Both files changed on 2026-10-13 at 08:44 and 08:47, before this round. See "Owner edits outside this stage" below. |

### Edit list

Line numbers are the physical lines of `prd.md` and `traceability.md` after the edits. Files changed in this round: `prd.md`, `traceability.md`, `prd-fixes.md`. No other file changed.

1. **F-1 a.** `prd.md`, section 7, paragraph before the outcome table, old line 157 (removed).
   - Old: In this PRD, a healthy call is a call from a caller with an allow row to which no row of the failure table below applies.
   - New: (the sentence and its blank line are removed). The rest of the paragraph "The four outcomes" is unchanged.
2. **F-1 b and X-5 a.** `prd.md`, section 7, outcome table, row HOLD_FOR_REVIEW, column "Which route in this PRD can return it", line 160.
   - Old: `POST /ai/recommend/{id}` on a healthy call (policy row O2), and on a timeout, an error, an open breaker, a full limit of 10 running calls, a bad shape,
   - New: `POST /ai/recommend/{id}` on a call that no row of the failure table applies to (policy row O2), and on a timeout, an error, an open breaker, a full limit of 10 running calls (PROPOSED, N-05. Owner: Team-Force), a bad shape,
3. **F-1 b.** `prd.md`, section 7, same row, column "Text shown", line 160.
   - Old: The sentence on a healthy call. No text on a failure.
   - New: The sentence when no failure row applies. No text on a failure.
4. **F-1 c.** `prd.md`, RQ-16, line 315.
   - Old: A healthy call returns the policy outcome RECOMMEND_ONLY
   - New: A call with an allow row, to which no row of the failure table applies, returns the policy outcome RECOMMEND_ONLY
5. **F-1 d.** `prd.md`, RQ-18, line 317.
   - Old: A healthy call returns HTTP 202 with outcome
   - New: A call with an allow row, to which no row of the failure table applies, returns HTTP 202 with outcome
6. **F-1 d.** `prd.md`, RQ-18, line 317.
   - Old: A healthy call writes one `ai.recommendation` audit row.
   - New: A call that returns the sentence writes one `ai.recommendation` audit row.
7. **F-1 e.** No edit. The planned test `test_healthy_recommend_is_hold_for_review_with_the_sentence` keeps its name in `prd.md` RQ-18 and in `traceability.md` (lines 39 and 115).
8. **X-1 a.** `prd.md`, section 15, paragraph "Stale text found while writing", line 604. The text in the block was changed to match the file (see "Reads before writing").
   - Old: ... If a stale line turns up later, the requirement row of this PRD applies. If the YAML and this PRD disagree ...
   - New (inserted after "applies."): Round 5 checked one more case. `docs/12-finops/optimization-backlog.md` is the source design of RQ-31. Review v4.0 read its lines 125, 127 and 128 as a key of `prompt_hash`, model version and policy version, a clear when either version changes, and a cap of 500 stored answers. On 2026-10-13 those three lines read differently. Line 125 gives `prompt_hash` alone as the key. Line 127 says no rule empties the store before its 300 seconds are up. Line 128 says the cap is PROPOSED, with owner Team-Force and no number. They agree with RQ-31. RQ-31 applies.
9. **X-2 a.** `prd.md`, RQ-69, Requirement cell, line 411.
   - Old: An unknown role word is not stored as sent. A correlation id longer than 128 characters is refused when the audit row is written, not only when it is read. The 128 limit is PROPOSED. Owner: Team-Force. The word to store for an unknown role is an Open question for S03.
   - New: The text given in the Decisions block, word for word (the 129 character case, the new UUID, no refusal, the 400 kept for the path in RQ-44, the limit PROPOSED, the Open question kept).
10. **X-2 b.** `prd.md`, section 12, RK-03, column "What the app does", line 469.
    - Old: applies the 128 limit at write time (RQ-69)
    - New: swaps a header id over the 128 limit for a new UUID at write time (RQ-69)
11. **X-2 c.** Search for "128", "write time" and "written, not only when it is read". No further edit. See "Agreement check".
12. **X-3 a.** `prd.md`, RQ-08, end of the Requirement cell, line 298.
    - Old: ... The words raw count and flagged count are an Open question for S03.
    - New: (same, then) In `data/synthetic/alarms.csv`, the only row with a blank `dedupe_key` is `ALA-BAD1` at file line 353. That row has a blank `storm_batch_id` too, so no storm reply lists it. The held-aside rule is tested with a small fixture and not with that file.
13. **X-3 b.** `prd.md`, RQ-62, end of the Requirement cell, line 397.
    - Old: ... The page then asks for a recommendation, records the decision, and reads the audit chain.
    - New: (same, then) The page does not list a blank `device_id`. A `device_id` with no device row is listed. Example: storm `STO-00001` has one row (file line 2 of `alarms.csv`), and its `device_id` is `DEV-00001`. `devices.csv` has no `DEV-00001`. The lookup then returns 404 (RQ-03), the recommendation returns BLOCK (RQ-20), and the page shows each reply.
14. **X-3 c.** `prd.md`, section 12, RK-17, cell "Risk", line 483.
    - Old: ... 192 `true` and 1 blank stale flags in 354 device rows.
    - New: (same, then) Two alarm rows have no usable device: file line 2 (`REC-0001`) names `DEV-00001`, which `devices.csv` lacks, and file line 353 (`ALA-BAD1`) is blank except for its `alarm_id`.
15. **X-3 c.** `prd.md`, section 12, RK-17, cell "Label", line 483.
    - Old: **Verified Fact** (counts from `ai-qualification.md` and `semantic-layer/business-rules.yaml`)
    - New: **Verified Fact** (counts from `ai-qualification.md` and `semantic-layer/business-rules.yaml`; the two alarm rows from `data/synthetic/alarms.csv` lines 2 and 353)
16. **X-4 a.** `prd.md`, section 7, first paragraph "Pick, agency and approval point.", line 134.
    - Old: Each cell below is quoted from `docs/02-baseline/ai-qualification.md`. This table lists all 11 AI uses. An Outcome of none means that file names no outcome word for that use.
    - New: The Pick, Agency and Human approval point cells below are quoted from `docs/02-baseline/ai-qualification.md`. The Outcome cell is the outcome word that file names. Only `ai_use.remediation_execution` takes its outcome from the YAML (`outcome.execute`), because the file names none for it. This table lists all 11 AI uses. An Outcome of none means neither source names an outcome word for that use.
17. **X-5 b.** `prd.md`, section 7, failure table, row "10 model calls are already running", column Cause, line 172.
    - Old: 10 model calls are already running
    - New: 10 model calls are already running (PROPOSED limit, N-05. Owner: Team-Force)
18. **X-5 c.** `prd.md`, section 7, paragraph "The failure table names the cause", line 182.
    - Old: A timeout, an open breaker and a full limit of 10 running calls: `failmode.schema_failure`
    - New: A timeout, an open breaker and a full limit of 10 running calls (N-05): `failmode.schema_failure`
19. **X-5 c.** `prd.md`, section 7, bullet in "Limits of the checks", line 193.
    - Old: The reasons list cannot tell an open breaker from a full limit of 10 running calls.
    - New: The reasons list cannot tell an open breaker from a full limit of 10 running calls (N-05).
20. **X-5 d.** Search for "10 running calls", "10 model calls" and "10 calls". No further edit. See "Agreement check".
21. **X-6 a.** `prd.md`, section 13, directly under the table "The 13 items that stay deferred", line 534 (new paragraph).
    - Old: (nothing between the table and "Limits from the PROPOSED bundles.")
    - New: D-18 stays on this list for every audit field whose feature is not built yet. The trigger of D-18 names the cache flag: "If the cache is built in S07, the cache flag comes first." RQ-31 builds the stored-answer store, so S07 adds the cache flag under a new ADR before the route ships. The fields of D-18 whose feature is not built stay deferred.
22. **X-6 b.** `prd.md`, RQ-31, line 330.
    - Old: A stored answer writes the same `ai.recommendation` audit row, and the row says no model ran. The cap
    - New: A stored answer writes the same `ai.recommendation` audit row, and the row says no model ran. The row says it through the cache flag of D-18. The flag has no YAML id yet. S07 adds it under a new ADR before the route ships. The cap
23. **X-7 a.** `prd.md`, RQ-44, line 361.
    - Old: A case id longer than 128 characters is refused
    - New: A case id (the `correlation_id` in the route path) longer than 128 characters is refused
24. **X-7 b.** `prd.md`, RQ-52, end of the Requirement cell, line 369.
    - Old: ... S07 adds the ids under a new ADR before it ships the route.
    - New: (same, then) An audit action word (`status.code.audit_action.*`) is the word in the audit row that names what happened. Example: `record.read`.
25. **X-7 c.** `prd.md`, RQ-33, line 341.
    - Old: It never fills the approval id input of the execute check.
    - New: It never fills the approval id that the policy checks before an EXECUTE (`provenance.approval_id`, `outcome.execute`).
26. **X-7 c.** Search for "execute check" and "approval check". No prose hit is left. The test name `test_a_no_never_unlocks_the_approval_check` stays in RQ-33 of `prd.md` and in `traceability.md`.
27. **Version.** `prd.md`, header, Date / version, line 7, and `traceability.md`, header, Date / version, line 6.
    - Old: 2026-10-13, v1.5. S06R fixes applied, round 4. Round 4 closes R4-1 (the reason of a held answer is in the response body, not in the audit row) and R4-2 (the owner edits in files outside the PRD). Round 3 closed R3-1 to R3-9.
    - New: 2026-10-13, v1.6. S06R fixes applied, round 5. Round 5 closes F-1 (the PRD gives no word a meaning of its own where the call has no failure) and the other findings X-1 to X-7 of review v4.0. X-8 is left as it is. Round 4 closed R4-1 and R4-2. Round 3 closed R3-1 to R3-9.
28. **Status.** `prd.md`, header, Status, line 9: "round 4" becomes "round 5", and "Round 4 closed R4-1 and R4-2." gets "Round 5 closed F-1 and X-1 to X-7." added. `traceability.md`, header, Status, line 8: the same two changes.
29. **X-8.** No edit. Left as it is, with the reason in "Decision per fix".

`traceability.md` section 1 holds no requirement text, so it has no row change. Its RQ-18 row keeps the planned test name. Only its header changed.

### RQ ids touched

For each id, the files that cite it. The count of citing files comes from a search of the whole project on 2026-10-13, without the chat transcript.

| Row | File | What changed | Other files that cite the id |
|---|---|---|---|
| RQ-08 | `prd.md` line 298 | One added fact about `ALA-BAD1`. YAML ids and test name stay. | `traceability.md`, `prd-review.md`, `prd-fixes.md`, `Project_Acronyms.md` (lines 386, 407) |
| RQ-16 | `prd.md` line 315 | The words "a healthy call". | `traceability.md`, `prd-review.md`, `prd-fixes.md` |
| RQ-18 | `prd.md` line 317 | The words "a healthy call", twice. The test name stays. | `traceability.md`, `prd-review.md`, `prd-fixes.md`, `Project_Acronyms.md` (line 387) |
| RQ-31 | `prd.md` line 330 | Two added sentences on the cache flag. | `traceability.md`, `optimization-backlog.md` (line 125), `ADR 0003`, `Risk Management.md`, `S06R-prd-review.md` (playbook), `Project_Acronyms.md` (lines 93, 394, 404), `prd-review.md`, `prd-fixes.md` |
| RQ-33 | `prd.md` line 341 | One sentence on the approval id. The test name stays. | `traceability.md`, `prd-review.md`, `prd-fixes.md` |
| RQ-44 | `prd.md` line 361 | Three words explain "case id". | `traceability.md`, `prd-review.md`, `prd-fixes.md` |
| RQ-52 | `prd.md` line 369 | One sentence that says what an audit action word is. | `traceability.md`, `prd-review.md`, `prd-fixes.md` |
| RQ-62 | `prd.md` line 397 | One example with `STO-00001`. | `traceability.md`, `prd-review.md`, `prd-fixes.md`, `Project_Acronyms.md` (line 389) |
| RQ-69 | `prd.md` line 411 | The whole Requirement cell. The test name and YAML ids stay. | `traceability.md`, `ADR 0003` (line 57), `Risk Management.md` (line 274), `prd-review.md`, `prd-fixes.md` |

The RQ-69 test `test_unknown_role_word_is_not_stored_as_sent` now also checks the 129 character case. `traceability.md` section 1 holds no requirement text, so it needs no row change.

### Agreement check

| Claim | Where it appears | Result |
|---|---|---|
| "healthy" | `prd.md` line 317 (the test name in RQ-18), `traceability.md` lines 39 and 115 (the same test name). | No other hit in either file. This is the result the block names. Section 2 ("This PRD does not define a term") and the gate row "The PRD and the YAML agree" are true again. |
| 128 characters | RQ-44 (line 361), RQ-69 (line 411), RK-03 (line 469), section 11 "Longest audit case id" (line 441), N-01 (line 546). | RQ-69 and RK-03 say the same new thing. RQ-44 keeps the 400 for a path id. Section 11 and N-01 state the number, the label and the owner. Neither says the call is refused, so both stay as they are. `ADR 0003` line 57 says "The 128 character limit applies when the row is written." The swap for a new UUID happens at that moment, so the line is still true. The ADR is not edited. |
| "write time" and "written, not only when it is read" | "write time" only in RK-03 (line 469). The phrase "refused when the audit row is written" has no hit. | Agrees with RQ-69. |
| 10 running calls, 10 model calls, 10 calls | Section 7: outcome table row (line 160, PROPOSED, N-05, Team-Force), failure table row (line 172, PROPOSED, N-05, Team-Force), paragraph (line 182, N-05), bullet (line 193, N-05). Outside section 7: RQ-54 (line 380), section 11 (line 440), N-05 (line 550). | Every hit in section 7 has PROPOSED with N-05 or "(N-05)". The three hits outside section 7 are the places the block excludes. All three already carry PROPOSED and N-05. |
| Cache flag and D-18 | RQ-31 (line 330), section 13 D-18 row (line 530), the new paragraph (line 534), section 15 "Planned YAML additions" (line 602). | All four say the same: the flag has no YAML id, S07 adds it under a new ADR before the route ships, D-18 stays deferred for the fields whose feature is not built. The Open question line about the answer store (line 586) holds the word "cache". No new Open question line. |
| "execute check", "approval check" | RQ-33 only. | The prose now names `provenance.approval_id` and `outcome.execute`. The test name keeps `approval_check`. |
| The count 13 | `prd.md` line 12 ("Thirteen"), line 515 ("The 13 items"), `traceability.md` line 11 ("Thirteen"). 13 Open question lines. | All agree. |
| `optimization-backlog` | RQ-31 (source design column) and section 15 (line 604). | Both name the same file. |
| "Verified Fact" for the alarm rows | RQ-08 and RQ-62 give the facts. RK-17 gives the two rows and the file pointer. | Same two rows, same line numbers (2 and 353). |

### Version check

| Item | Result |
|---|---|
| `semantic-layer/README.md` | `1.1.1` |
| `prd.md` header, Evidence sources | `1.1.1` |
| `traceability.md` header, Evidence sources | `1.1.1` |
| `semantic-layer-revision.md` header (line 6) | "The current version is `1.1.1`." |
| `generated/manifest.json` | `"version": "1.1.1"` |
| Review v4.0 | `1.1.1` |
| Newest ADR that changed the YAML | ADR 0002 (`1.1.0` to `1.1.1`). ADR 0003 added no id. |
| `prd.md` document version | v1.6 |
| `traceability.md` document version | v1.6 |
| Raise count | Once, from v1.5 to v1.6, with the same number in both. |

```
README: ['1.1.1']
prd.md header: ['1.1.1']
traceability.md header: ['1.1.1']
semantic-layer-revision.md header: ['1.0.0', '1.1.0', '1.1.1']
prd.md doc version: ['v1.6.']
traceability.md doc version: ['v1.6.']
```

(The `semantic-layer-revision.md` line lists the three versions that its text mentions.)

### Checks 8a to 8h

All outputs are from 2026-10-13, run after the last edit. The scripts are temporary Python files. They are not part of the repo. **Verified Fact.**

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
duplicate prd ids: none
duplicate trace ids: none
counts equal: True
id set difference: none
ids are RQ-01 to RQ-73: True
```

Matches the locked fact: 73 rows.

#### 8b. YAML id lookup

```
YAML files: 7
YAML ids collected from seven files: 757
YAML ids cited in requirement rows (distinct): 123
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 178
audit action words resolved via value: [('policy.deny', 'status.code.audit_action.policy_deny'), ('policy.hold', 'status.code.audit_action.policy_hold'), ('record.read', 'status.code.audit_action.record_read')]
wildcard prefixes (ids that start with the prefix): [('field.audit_row.*', 15, ('prd.md', 207)), ('status.code.audit_action.*', 7, ('prd.md', 369))]
expected misses (PROPOSED words on the Open question for S03 line):
    ai.approval first seen ('prd.md', 340)
    ai.recommendation first seen ('prd.md', 317)
    record.storm_read first seen ('prd.md', 305)
unresolved backticked id-shaped tokens (other than file names): none
```

757 ids match the locked fact. The three expected misses are the PROPOSED words that the Open question for S03 line names (section 15, the line that starts "the audit action words"). The wildcard `status.code.audit_action.*` is the new text in RQ-52. It is a prefix, and 7 ids start with it. `field.audit_row.*` was already in section 8. **Verified Fact.**

#### 8c. Row-by-row compare

```
mismatches: none
```

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 44
```

Matches the locked fact: 29 exist, 44 are planned for S07.

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
.........................................                                [100%]
41 passed in 2.46s
```

(`python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q`.) Matches the locked fact.

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines (SHA-256 `BC2D23CDA9734222576DE51B7EC2917FE90C0C326DDC7DBD1FCB74B6ED482FAD`). After the test run it had 241 lines. After the restore it had 240 lines and the same SHA-256. The command named the 29 existing test ids that `prd.md` section 10 lists.

```
SKIPPED [1] policy\tests\test_policy_python.py:577: opa binary not on PATH
40 passed, 1 skipped, 60 warnings in 4.78s
```

Matches the locked fact: 40 passed, 1 skipped. The skip is the `opa` test (RQ-59).

#### 8g. git status

I ran `git status --short` before the first edit and after the last one. Both outputs have 18 lines and are the same line for line. The reason: `docs/prd/` is a whole untracked folder, so git shows the folder and not the files inside it. So I also compared file times. Files that changed on disk during this round: `docs/prd/prd.md`, `docs/prd/traceability.md` and `docs/prd/prd-fixes.md`, and `transcript/chat_transcript.md` (the chat log gets its new turn). `docs/12-finops/optimization-backlog.md` (08:47) and `playbook/S07-application-and-demo.md` (08:44) changed before the round started. They are the owner edits, already made. The output of `git status` for `apps/`, `semantic-layer/`, `policy/` and `data/` shows no change except cache files. `logs/audit.log` was restored. **Verified Fact.**

Files already present in the first output and left as they were: the modified files, the deleted Archive file, and the untracked `ADR/0003`, `Project_Intent - Appendix B.md` and `playbook/S06F-prd-fixes.md`. Cache files (`__pycache__`, `.pytest_cache`) are not counted.

File hashes after the last edit (SHA-256), so the next stage can see whether the PRD changed:

- `prd.md`: `483BCFC03B7DDDE2C8CD9AA7848DF9DAA1F44402DBBE5A1118B04F909BD4377D`
- `traceability.md`: `B8B993DC6AC492F6E8E537B27FA33AA25D014317A78092BF909496059044FA2F`

#### 8h. Open question lines

```
Open question for S03 lines in prd.md section 15: 13
  prd.md line 12: Thirteen Open questions for S03 stay o
  prd.md line 515: The 13 items that stay deferred, eac
  traceability.md line 11: Thirteen Open questions for S03: see `
count equals 13: True
```

No Open question line was added or removed. **Verified Fact.**

#### Searches

I searched `prd.md` and `traceability.md` for each term the block names.

| Term | Result |
|---|---|
| "healthy", "healthy call" | `prd.md` line 317 (test name). `traceability.md` lines 39 and 115 (the same test name). Nothing else. |
| "execute check", "approval check" | No prose hit. The test name keeps `approval_check` (with an underscore). |
| "case id" | `prd.md` RQ-44 (explained), RQ-45 (the audit route path id), section 11 and N-01 (the 128 limit, unchanged). None in `traceability.md`. |
| "audit action word" | RQ-52 (defined by example), and the Open question line about the audit action words. |
| "10 running calls", "10 model calls", "10 calls" | See the agreement check. |
| "128" | See the agreement check. `traceability.md` has two hits (RQ-44 test name, N-01). |
| "write time" | One hit, RK-03. |
| "refused when the audit row is written" | No hit. |
| "optimization-backlog" | RQ-31 source design column, and section 15. `traceability.md` has the RQ-31 design file. |
| "cache flag" | RQ-31, the D-18 row, the new paragraph, and the planned YAML additions paragraph. |
| "Thirteen", "13" | See 8h and the agreement check. |

### Done test

In `prd.md` RQ-01 the YAML id `status.code.health.ok` was changed to `status.code.health.does_not_exist`. Check 8b then printed:

```
unresolved cited ids: [('RQ-01', 'status.code.health.does_not_exist')]
unresolved backticked id-shaped tokens (other than file names): [('status.code.health.does_not_exist', ('prd.md', 282))]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash before the change (`483BCFC03B7DDDE2C8CD9AA7848DF9DAA1F44402DBBE5A1118B04F909BD4377D`). Check 8b then printed:

```
unresolved cited ids: none
unresolved backticked id-shaped tokens (other than file names): none
```

**Verified Fact.**

### Map from the FAIL rows to fixes

| Row in review v4.0 | Fix | Edits that address it |
|---|---|---|
| P2 (FAIL) | F-1 | Edits 1 to 6 remove the defining sentence and replace "a healthy call" in the outcome table, RQ-16 and RQ-18. Edit 7 keeps the test name. |
| P12.8 (FAIL, same finding) | F-1 | The same edits 1 to 6. |

Other findings and the Decisions lines that close them. I mark no row PASS. The next S06R does that.

| Finding | Decisions line | Edits |
|---|---|---|
| X-1 | X-1 | 8 |
| X-2 | X-2 | 9 to 11 |
| X-3 | X-3 | 12 to 15 |
| X-4 | X-4 | 16 |
| X-5 | X-5 | 2, 17 to 20 |
| X-6 | X-6 | 21, 22 |
| X-7 | X-7 | 23 to 26 |
| X-8 | X-8 (do not apply) | 29. Left as it is. |

Decisions lines that close no finding: none. The block's "Owner edits outside this stage" line closes none either, because it is not a fix.

### Owner edits outside this stage

The block lists two owner edits. This stage does not make them. I read the places at the start of the round, and both were already made.

| File and line | The block's text | What the file holds now |
|---|---|---|
| `docs/12-finops/optimization-backlog.md` lines 125, 127, 128 | Line 125: "`prompt_hash` alone (RQ-31 in the PRD). One stub model and one policy version exist, so no other key part is needed in this packet." Line 127: "No rule empties the store before its 300 seconds are up. A restart empties it." Line 128: "The cap on stored answers is PROPOSED. Owner: Team-Force. No number is set ... A restart empties it." | Lines 127 and 128 are the same as the block. Line 125 ends "so no other key part is needed." and lacks the last two words "in this packet". The meaning is the same. |
| `playbook/S07-application-and-demo.md` line 36 | Replace "on a healthy call" with "when no failure row applies". | The line reads "returns HOLD_FOR_REVIEW with the sentence when no failure row applies". Done. |

### Items for the next S06R

These are not fixes and this round did not act on them. **Inference** unless a line says Verified Fact.

- **Verified Fact.** `Project_Acronyms.md` is outside the fix list. It still holds two stale lines. Line 387 says "A healthy call returns HOLD_FOR_REVIEW with one recommendation sentence." Lines 93 and 394 say the store "never holds a BLOCK or HOLD answer". The PRD says the store never holds an answer that has no text, and it holds a HOLD_FOR_REVIEW that has a sentence. The owner may change the three lines.
- The audit row still has no key for a reason (round 4 item). The response body holds the reason.
- Line 125 of `optimization-backlog.md` lacks the last two words of the block's text. The meaning is the same. No action needed.
- The four older records that say 14 deferred items or ask for the D-07 decision (round 4 item) are unchanged.
- `playbook/S07-application-and-demo.md` item 3 says "approve or reject". The route takes `yes` or `no` (round 4 item).
- The round 4 section of this file keeps its own text, including the S07 line 36 edit that used "a healthy call". It is the record of what round 4 did.


## Round 6, 2026-10-13

### Fix source

| Field | Value |
|---|---|
| Path | No review file. The fix comes from the owner's request in chat on 2026-10-13: "1. Fix the four Project_Acronyms.md lines now. 2. Defer RQ-31." |
| Header date and version | Not applicable. `docs/prd/prd-review.md` v4.0 (review of PRD v1.5) is the last review. It is not re-run in this round. |
| Stage status | Not applicable. The next S06R scores the round 6 edits. |

The request has two parts.

- Part 1 is the four `Project_Acronyms.md` lines named in the round 5 "Items for the next S06R". It was done before this section. The four lines now agree with the PRD.
- Part 2 is a decision, R6-1: RQ-31 (the 300 second answer store) is deferred. The decision is written in `docs/ADR/0004-defer-rq-31-answer-store.md`. This round applies it to `prd.md` and `traceability.md`.

### Fix list

| Id | Fix | Source |
|---|---|---|
| R6-1 | Mark RQ-31 as deferred. S07 does not build the answer store. Keep the RQ-31 row, its test name and its YAML ids. | The owner's request, ADR 0004. |

### Decision per fix

R6-1. Apply. Decision: the RQ-31 row stays in both files, so the 73 rows and the RQ ids do not change. The row gets the status "deferred (ADR 0004)". A deferred test is not counted as planned. The counts become 29 existing, 43 planned and 1 deferred (29 + 43 + 1 = 73). The 300 second lifetime (`OB-01`) stays DECIDED. The rules of ADR 0003 decision 3 stay as the rules for a later build. The cache flag (D-18) is not needed in S07, so S07 adds no YAML id for it and the layer stays `1.1.1`. The 13 Open question lines stay as they are, because none of them is about RQ-31.

### Edit list

`prd.md`:

1. Header: version v1.6 to v1.7. Round 6 added to the Date / version and Status rows. The planned count 44 became 43, with "1 test (RQ-31) is deferred and no stage writes it yet". ADR 0004 added to the Evidence sources.
2. Section 1 (how to read): one sentence defines a test marked **deferred**.
3. Section 6 (the recommend workflow row) and section 9 (the `POST /ai/recommend/{id}` route row): RQ-31 removed from the range. The text "(RQ-31 is deferred)" added.
4. Section 10, RQ-31: the cell starts with "Deferred (ADR 0004). S07 does not build this requirement." The rules stay. The words "before the route ships" became "before the store is built". The test status "planned S07" became "deferred (ADR 0004)".
5. Section 10, RQ-34: the sentence about the `ai.recommendation` audit row now says that, in S07, the text always comes from the model, because RQ-31 is deferred. If RQ-31 is built later, a stored answer writes the same row.
6. Section 10, the Count paragraph: 44 became 43, and "1 is deferred (RQ-31, ADR 0004)" was added. Section 11, the `OB-01` row: it says the store is not built in S07.
7. Section 12, RK-14: "The store stays" became "S07 builds no store (RQ-31 deferred, ADR 0004), so the risk does not apply in S07."
8. Section 13: a short table, "Decision this PRD recorded in ADR 0004", added under the ADR 0003 table. The D-18 row and the paragraph under it say the cache flag is added by a later stage, under a new ADR, before the store is built.
9. Section 15: the planned YAML additions paragraph says the cache flag is not on the list. The two gate rows say 43 planned and 1 deferred, and that RQ-31 has no stage.

`traceability.md`:

10. Header: version v1.7. Round 6 added. Counts changed as in edit 1.
11. Assumptions (1): defines "deferred".
12. Section 1, RQ-31: the status became "deferred (ADR 0004)".
13. Section 2 (the list of planned tests): the RQ-31 row was removed. A sentence says the list has 43 tests and gives the name of the deferred test.
14. Section 3: the route range for `POST /ai/recommend/{id}` says "(RQ-31 is deferred)".
15. Section 4: the `OB-01` row says "RQ-31 (deferred, ADR 0004)".

Files outside the three PRD files that the request asked for, or that held text the deferral made stale. Each is a small edit.

| File | Edit |
|---|---|
| `docs/ADR/0004-defer-rq-31-answer-store.md` | Created. It holds the decision, the consequences, how the store comes back, and the open items. |
| `docs/ADR/0003-s06-risk-recommendations.md` | One line under decision 3: ADR 0004 moves the build out of S07. The decision text stays. |
| `docs/12-finops/optimization-backlog.md` | OB-01 status, the decision 2 status, the "waits for S07" line, the review trigger and the closing sentence say the build is deferred. |
| `docs/prd/Risk Management.md` | Line 8: 43 planned tests and "RQ-31 is deferred". RK-14 has a "Decision (2026-10-13)" paragraph. |
| `playbook/S06R-prd-review.md` | P13 and the locked facts say RQ-31 is deferred. A locked fact gives the counts 29, 43 and 1. |
| `playbook/S06F-prd-fixes.md` | The locked facts hold the version before round 6 and the counts from round 6. The store row mentions ADR 0004. |
| `Project_Acronyms.md` | The ADR row adds ADR 0004. The rows `RQ-nn`, `planned S07`, `OB-xx`, `DECIDED` and the answer store row say the build is deferred. The count is 43 planned. |
| `playbook/STATUS.md` | Rows added for round 5 and round 6. |

### RQ ids touched

RQ-31 and RQ-34. RQ-31: the status and the first sentence of the requirement changed. The YAML ids, the test name and the design file did not change. RQ-34: one sentence says the text comes from the model in S07.

### Agreement check

I searched `prd.md` and `traceability.md` for "44", "RQ-31", "answer store", "stored answer", "cache flag", "before the route ships" and "S07 builds".

- "44" appears only inside `RQ-44` and "N-01 id limit 128" lines. No planned-test count of 44 remains.
- Every "RQ-31" hit says deferred, except the ADR 0003 table in section 13 (line 512). That table records what ADR 0003 decided, and the line right after it states that ADR 0004 moved the build out of S07.
- No sentence says S07 builds the answer store or adds the cache flag.

**Verified Fact.**

### Version check

| Place | Value |
|---|---|
| `semantic-layer/README.md` | `1.1.1` |
| `prd.md` header (Semantic layer version) | `1.1.1` |
| `traceability.md` header | `1.1.1` |
| `semantic-layer-revision.md` header | newest entry `1.1.1` |
| `prd.md` Date / version | v1.7 |
| `traceability.md` Date / version | v1.7 |

ADR 0004 added no YAML id. **Verified Fact.**

### Checks 8a to 8h

Checks 8a to 8d and 8h come from one script. It prints these lines for the files after the last edit.

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
counts equal: True
id set difference: none
ids are RQ-01 to RQ-73: True
```

#### 8b. YAML id lookup

```
YAML ids collected from seven files: 757
YAML ids cited in requirement rows (distinct): 123
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 178
expected misses: record.storm_read, ai.recommendation, ai.approval
unresolved backticked id-shaped tokens (other than file names): none
```

The three expected misses are the PROPOSED audit action words on the Open question for S03 line.

#### 8c. Row-by-row compare

```
mismatches: none
```

The compare now reads the status "deferred" as a third value next to "existing" and "planned". RQ-31 reads "deferred" in both files.

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 43
deferred tests: RQ-31 (test file not present, as required)
```

29 + 43 + 1 = 73.

#### 8e. Semantic layer unchanged

`git status --short` for `semantic-layer/` lists nothing. The seven YAML files are unchanged.

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines (SHA-256 `BC2D23CDA9734222576DE51B7EC2917FE90C0C326DDC7DBD1FCB74B6ED482FAD`). After the run it had 241 lines. After the restore it had 240 lines and the same SHA-256. The command named the 29 existing test ids that `prd.md` section 10 lists.

```
40 passed, 1 skipped, 60 warnings in 5.59s
```

This matches the locked fact: 40 passed, 1 skipped. The skip is the `opa` test (RQ-59). I also ran the whole suite (`semantic-layer/tests`, `policy/tests`, `tests`): 331 passed, 2 skipped. I restored `logs/audit.log` after that run too.

#### 8g. git status

`docs/prd/` is a whole untracked folder, so git shows the folder and not the files inside it. I compared file times and hashes as well. Files that changed on disk during this round: `docs/prd/prd.md`, `docs/prd/traceability.md`, `docs/prd/prd-fixes.md`, `docs/ADR/0004-defer-rq-31-answer-store.md` (new), the files in the "outside" table above, and `transcript/chat_transcript.md`. The semantic layer files are unchanged. Cache files (`__pycache__`, `.pytest_cache`) are not counted.

File hashes after the last edit (SHA-256), so the next stage can see whether the PRD changed:

- `prd.md`: `0BA9E7896268CFA0E27FF3F9510EFA10A54D022F5728C6B4257FE955DA6B1D6F`
- `traceability.md`: `770EBE737CA4383DEEBC577E2D91409272B4D58BACD8F5A9C0DAA70D3121BAA9`

#### 8h. Open question lines

```
Open question for S03 lines in prd.md section 15: 13
count equals 13: True
```

No Open question line was added or removed. **Verified Fact.**

### Done test

I changed the id `metric.repeated_prompt_share` in `semantic-layer/metrics.yaml` to `metric.repeated_prompt_shareX`, a name no row cites. RQ-31 and RQ-63 cite the real id. Check 8b then printed:

```
unresolved cited ids: [('RQ-31', 'metric.repeated_prompt_share'), ('RQ-63', 'metric.repeated_prompt_share')]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash before the change. Check 8b then printed:

```
unresolved cited ids: none
```

**Verified Fact.**

### Items for the next S06R

These are not fixes and this round did not act on them. **Inference** unless a line says Verified Fact.

- **Verified Fact.** `docs/12-finops/evidence.md` line 265 still says "Only RECOMMEND_ONLY ... 500 answers. Built in S07". It was already out of date before this round, and the deferral makes it more so. This round did not edit it.
- `docs/12-finops/optimization-backlog.md` lines 24, 122, 131, 141 and 170 now say the build is deferred. The next S06R should read them once.
- `prd.md` line 512 (the ADR 0003 table) keeps the words "The 300 second answer store stays". They record what ADR 0003 decided. The next line points to ADR 0004.
- Check 8c and 8d in `playbook/S06F-prd-fixes.md` assume two statuses (existing and planned). A third status, deferred, now exists. The locked facts say how to count it. The check text itself is unchanged.
- If a later stage builds RQ-31, it must run S05R, add the cache flag as a YAML id under a new ADR, raise the layer version, and change the RQ-31 status back to planned. ADR 0004 lists these steps.
- The audit row still has no key for a reason (round 4 item).

## Round 7, 2026-10-13

### Fix source

| Field | Value |
|---|---|
| Path | `docs/prd/prd-review.md` |
| Header date and version | 2026-10-13, v5.0 of this review (S06R round 5, the review of PRD v1.7). Semantic layer version read from `semantic-layer/README.md`: `1.1.1`. |
| Stage status | **PASS.** No row is FAIL. P1 to P13 are PASS. Nine other findings, X-1 to X-9, are in section 6 of the review. |

### Fixes required (copied word for word)

Section 9 of the review says:

> None. No row is FAIL.

The review lists three optional fixes (O-1, O-2, O-3). It does not number them as "Fixes required". So the fixes of this round are the lines of the Decisions block, as the stage rules say. Each line closes one row of "Other findings": X-3, X-4 and X-7. The owner closed X-1 and X-2 by hand on 2026-10-13, in files outside this stage. X-5, X-6, X-8 and X-9 are left as they are.

### Other findings named by the Decisions block (copied word for word)

X-3, X-4 and X-7 are the rows to close. X-5, X-6, X-8 and X-9 are copied too, because a Decisions line names them as "left as it is".

| # | Finding | Label |
|---|---|---|
| X-3 | **RQ-08 gives no key names for the three counts.** RQ-08 (line 298) names the row keys `alarm_id`, `device_id` and `dedupe_key`. It does not name the keys for the raw count, the deduped count, the flagged count, the flag word, or the list of held-aside rows. It says only "listed apart". The planned test `test_storm_returns_raw_count_deduped_count_and_alarm_ids` has to read those keys. RQ-62 (line 397) reads the `device_id` values from the same reply. Two builders, or the S08 second model, would choose different key names. The PRD's gap rule (line 614) tells S07 to stop and write a gap, so S07 will not guess. **Fix:** add the five key names to RQ-08 before S07. This changes the PRD version by one minor step. | **Verified Fact** for the missing names. **Inference** for the impact. |
| X-4 | **RQ-32 and RQ-33 read two ways on a "no".** RQ-32 (line 340) says a good call returns an `approval_id`, for a yes or a no. RQ-33 (line 341) says a stored no "never fills the approval id that the policy checks before an EXECUTE". The PRD does not say whether the `ai.approval` audit row of a no holds an `approval_id`. Test `test_cannot_prove_lists_approval_id_when_a_row_holds_an_approval` (RQ-47) depends on that. No EXECUTE route exists, so no live effect. **Fix:** add one sentence to RQ-33: for a no, the audit row holds `approval_id` null (or holds the id, with `decision` no). The owner picks. | **Verified Fact** for the text. **Inference** for the confusion. |
| X-5 | **Open question lines say "does not explain" while RQ rows describe the words.** Lines 592 to 598 say "This PRD uses those words and does not explain them". RQ-08, RQ-31, RQ-65 and RQ-71 do describe what the words do. See section 4. **Fix:** change the sentence on those four lines to "This PRD describes what the word does in RQ-nn and gives it no YAML id." | **Verified Fact** for the text. |
| X-6 | **Workflow steps 5 and 6 have no persona (carried over from v4.0 X-8).** Step 5 carries `role.admin`, which is an API role and not a persona. Step 6 carries "none". Line 130 and section 5 say why. P5 asks for a persona on each step. I scored PASS because the PRD states the reason and the owner kept it in round 5. A strict reader could score it FAIL. | **Verified Fact** for the text. **Inference** for the reading. |
| X-7 | **The page shows status numbers that the label table does not list.** RQ-62 (line 397) says "the page shows each reply". A reply has an HTTP status number (404, 202, 403). Section 8 (lines 212 to 230) labels only the `/health` status. RQ-63 says "every number on the page". **Fix:** add one row to the section 8 label table: "HTTP status of each reply: REAL, a live call at the request." | **Inference** for the reading. |
| X-8 | **The limit of 10 running calls has no PROPOSED word at lines 182 and 193.** Both lines cite N-05 and nothing else. Lines 160, 172, 380 and 440 label it. Round 5 closed the old X-5 by adding the pointer. A reader of section 7 alone still sees a bare number. Optional fix: write "(PROPOSED, N-05)" on both lines. | **Verified Fact** for the text. |
| X-9 | **Smaller items.** RQ-30 (line 329) is missing a full stop after "with no text", before "The reasons list". `playbook/S07-application-and-demo.md` "Required work" item 1 (lines 32 to 38) lists seven routes and omits `GET /ready` (RQ-73) and the no-header 403 (RQ-68). Its Scope says "the routes the PRD lists", so the PRD wins. RQ-62 uses `STO-00001` as its example of a `device_id` with no device row (`DEV-00001`). Round 4 verified that against `alarms.csv` line 2. | **Verified Fact** for the first two. |

X-1 and X-2 of the review list stale lines in other files. The owner closed both by hand on 2026-10-13. This stage does not touch them and does not copy them here.

### Decisions for this round

Pasted in the prompt (the block in `playbook/S06F-prd-fixes.md`):

```text
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
```

### Decision per fix

| # | Decision | Reason |
|---|---|---|
| X-3 | apply | The Decisions block gives the exact words. I read the RQ-08 cell and the section 8 storm example first (see "Reads before writing"). Nothing in them conflicts with the new sentence, so the words are written as given. |
| X-4 | apply | I read `approval-workflow.md` line 76 first. It says "A rejection writes no approval id." That equals the decision, so the words are written as given. |
| X-7 | apply | One row in the section 8 label table, in the words of the block. It uses the label REAL, which is one of the four allowed labels. |
| X-5 | left as it is | The owner chose to close only X-3, X-4 and X-7 in this round. |
| X-6 | left as it is | Same reason. Round 5 kept steps 5 and 6 as they are, and section 6 line 130 says why. |
| X-8 | left as it is | Same reason. It is an optional fix in the review. |
| X-9 | left as it is | Same reason. The three small items stay. |

Naming the owner next to PROPOSED does not approve anything. The owner is Team-Force (`operating-contract.md` row 10), as the block says.

**Reads before writing.** **Verified Fact.**

| Fix | What I read | Result |
|---|---|---|
| X-3 | `prd.md` RQ-08 cell (old line 298) and the section 8 storm example (the `STO-00005` paragraph under the label table) | The cell has one sentence that lists the row keys, and the replacement covers it. The cell says a row with a blank `dedupe_key` is "held aside, listed apart from the other rows, counted in the raw count only, and left out of the deduped count". It says a flagged row counts in the raw count, and in the deduped count when its `dedupe_key` is not blank. No sentence says a row is flagged and also held aside. The storm example has no held-aside row and no flagged row, so it does not conflict. One tension stays and is not mine to change. See "Items for the next S06R". |
| X-4 | `docs/09-ai-guardrails/approval-workflow.md` line 76 | "The noc_operator rejects the next-action sentence. The network_engineer rejects a configuration suggestion. A rejection writes no approval id. No ticket is opened. The device row stays as stored." It matches the decision. The file does not win over the block here, because they agree. |
| X-4 e | `prd.md` search for "approval id" and "approval_id" | See the "Searches" table. No hit says the server makes the id on every call after the edits. |
| Owner edits | `playbook/S07-application-and-demo.md` lines 35, 38, 106 and `Project_Acronyms.md` lines 312, 386, 388 | Read after the PRD edits. See "Owner edits outside this stage". |

### Edit list

Line numbers are the physical lines of `prd.md` and `traceability.md` after the edits. Old line numbers are in brackets where an earlier edit moved the line. Files changed in this round: `prd.md`, `traceability.md`, `prd-fixes.md`, and one new row in `playbook/STATUS.md`.

1. **X-3 a.** `prd.md`, section 10, RQ-08, line 299 (old line 298).
   - Old: "The reply lists each row with `alarm_id`, `device_id`, `dedupe_key` and its flag word (empty when none)."
   - New: "The reply is a JSON body with five keys: `raw_count`, `deduped_count` and `flagged_count` (each a whole number), and `rows` and `held_aside` (each a list). Each entry of `rows` and of `held_aside` has four keys: `alarm_id`, `device_id`, `dedupe_key` and `flag`. `flag` holds the flag word, or an empty string when the row has none. A row with a blank `dedupe_key` goes in `held_aside` and not in `rows`. Every other row goes in `rows`, flagged or not. These key names are PROPOSED. Owner: Team-Force."
   - Every other sentence of the cell is unchanged. The test name, the YAML ids and the design file are unchanged.
2. **X-3 b.** `prd.md`, section 10, RQ-62, line 398 (old line 397).
   - Old: "the page lists the different `device_id` values from the storm reply, the operator picks one"
   - New: "the page lists the different `device_id` values from the storm reply (read from `rows` and `held_aside`), the operator picks one"
3. **X-3 c.** `prd.md`, section 15, the Open question line about "raw count and flagged count", line 599 (old line 598).
   - Added, before "Action: rerun S05R": "The reply key names are in RQ-08. They are PROPOSED. Owner: Team-Force. They are not YAML ids."
   - The count of Open question lines stays 13.
4. **X-3 d.** No edit. `prd.md` section 6, step 1 names no key and stays as it is. `traceability.md` needs no row change, because the test name stays.
5. **X-4 a.** `prd.md`, section 10, RQ-32, line 341 (old line 340). Three changes.
   - Old: "(always `persona.noc_operator`, the only allowed role, RQ-35) and makes the approval id."
   - New: "(always `persona.noc_operator`, the only allowed role, RQ-35). When `decision` is `yes`, the server makes the approval id. When `decision` is `no`, the server makes no approval id and `approval_id` is null."
   - After the sentence that lists the five keys of the reply, added: "The key `approval_id` is null for a no."
   - Old: "The call writes one `ai.approval` audit row first (RQ-36)."
   - New: "The call writes one `ai.approval` audit row first (RQ-36). For a yes, the server makes the approval id before it writes the row, and the row holds the id. For a no, the row holds `approval_id` null."
6. **X-4 b.** `prd.md`, section 10, RQ-33, line 342 (old line 341).
   - Added after the first sentence: "A no has `approval_id` null in the reply, in the stored record and in the audit row."
7. **X-4 c.** `prd.md`, section 6, step 4, line 125.
   - Old: "The server sets the approver and makes the approval id."
   - New: "The server sets the approver. For a yes it makes the approval id. For a no it makes none."
8. **X-4 d.** `prd.md`, section 8, table row "Approval record", line 208.
   - Old: "the approval id"
   - New: "the approval id (a yes only, null for a no)"
9. **X-4 e.** Search of `prd.md`. No further edit was needed. See "Searches".
10. **X-7.** `prd.md`, section 8, the label table, new line 227, directly after the row "Status code of `GET /health`" (line 226).
    - Added the row: "HTTP status of each other reply the page shows (for example 200, 202, 403, 404) | REAL | A live call at the request, not a stored value. | not applicable".
    - RQ-63 is unchanged.
11. **Header.** `prd.md` lines 7 and 9, `traceability.md` lines 6 and 8. Version v1.7 became v1.8, in both files. The Date / version row now starts "2026-10-13, v1.8. S06R fixes applied, round 7. Round 7 closes X-3, X-4 and X-7 of review v5.0." The older round sentences follow it. The Status row of both files says "round 7". The `prd.md` Status row adds a sentence about round 7 and about X-5, X-6, X-8 and X-9 left as they are. The `traceability.md` Status row adds "Round 7 closed X-3, X-4 and X-7."

I changed no RQ row count, no YAML id, no test name, no design file and no test status. No row of `traceability.md` section 1 changed, so its test names and statuses still match `prd.md`.

**X-5, X-6, X-8 and X-9: left as it is.** The owner chose to close only X-3, X-4 and X-7 in this round. No edit was made for these four findings.

### RQ ids touched

RQ-08, RQ-32, RQ-33 and RQ-62. Files that cite each one:

| RQ | Files that cite it |
|---|---|
| RQ-08 | `prd.md` lines 9, 122 (section 6 step 1), 245 (section 9 route row), 299 (the row), 300 (RQ-09), 570 (section 14) and 599 (section 15); `traceability.md` section 1, section 2 (the test `test_storm_returns_raw_count_deduped_count_and_alarm_ids`) and section 3; `Project_Acronyms.md` (the storm route row, line 386); `playbook/S07-application-and-demo.md` (the storm route, line 35). |
| RQ-32 | `prd.md` lines 9, 125 (section 6 step 4), 248 (section 9 route row), 272 (section 9 EXECUTE rule), 341 (the row), 498 (section 13 decision table) and 601 (section 15); `traceability.md` section 1, section 2, section 3 (`POST /approvals/{id}`) and section 4 (D-03); `Project_Acronyms.md` (lines 312 and 388). `playbook/S07-application-and-demo.md` line 38 describes the same route and does not cite the id. |
| RQ-33 | `prd.md` lines 9, 342 (the row) and 498; `traceability.md` section 1, section 2 and section 4 (D-03). |
| RQ-62 | `prd.md` lines 250 (section 9 route row) and 398 (the row); `traceability.md` section 1, section 2 and section 3; `Project_Acronyms.md` (the page row). |

The YAML ids, the test names and the design files of these four rows did not change.

### Agreement check

For each edit I searched `prd.md` and `traceability.md` for the same claim stated somewhere else.

- **Storm reply keys (X-3).** Section 6 step 1 says "the raw count, the deduped count, the flagged count and the rows of one storm (alarm id, device id, dedupe key, flag word)". It names no JSON key and stays by the decision. RQ-09 (flagged rows keep the flag word in the reply) and RQ-13 (counts only, no size flag) name no key either, and they do not conflict. RQ-62 now reads the device ids from `rows` and `held_aside`. The label table row "Number of alarm ids listed" needs no change.
- **Approval id (X-4).** After the edits, every hit agrees. RQ-32, RQ-33, step 4 of section 6 and the "Approval record" row of section 8 say a yes gets an id and a no gets none. Line 130 ("The model never fills the approval id"), RQ-38 (no route reads an id from the caller), RQ-47 (the `cannot_prove` list, for example the approval id) and RQ-58 (EXECUTE needs an approval id) are true for both a yes and a no. Line 143 quotes `ai-qualification.md` word for word and stays. Lines 94, 260 and 272 speak of the gate that EXECUTE needs and of the id that exists after S07 for a yes. They stay.
- **Counts.** The edits change no count. Seventy-three rows, 29 existing, 43 planned, 1 deferred and 13 Open question lines hold.

### Version check

| Place | Value |
|---|---|
| `semantic-layer/README.md` line 69 | `1.1.1` |
| `prd.md` header (Semantic layer version) | `1.1.1` |
| `traceability.md` header | `1.1.1` |
| `docs/02-baseline/semantic-layer-revision.md` line 6 | "The current version is `1.1.1`." |
| Review v5.0 | `1.1.1` |
| Newest ADR that changed the YAML | ADR 0002 (one sentence, `1.1.0` to `1.1.1`). ADR 0003 and ADR 0004 added no YAML id. |
| `prd.md` Date / version | v1.8 |
| `traceability.md` Date / version | v1.8 |

All equal. **Verified Fact.** The check script (`build.py --check`) printed "Version 1.1.1."

### Checks 8a to 8h

Checks 8a to 8d and 8h come from one script. It prints these lines for the files after the last edit.

#### 8a. RQ count

```
prd.md section 10 RQ rows: 73
traceability.md section 1 RQ rows: 73
each id appears once in prd.md section 10: True
counts equal: True
id set difference: none
ids are RQ-01 to RQ-73: True
```

#### 8b. YAML id lookup

```
YAML ids collected from 7 files: 757
YAML ids cited in requirement rows (distinct): 123
unresolved cited ids: none
backticked id-shaped tokens in prd.md + traceability.md: 176
expected misses: ai.approval, ai.recommendation, record.storm_read
unresolved backticked id-shaped tokens (other than file names): none
```

The three expected misses are the PROPOSED audit action words on the last Open question line of section 15 (`record.storm_read`, `ai.recommendation`, `ai.approval`). Audit action words such as `record.read` and `policy.deny` resolve through `status.code.audit_action.*`.

Reply keys, not ids: `raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside`, `alarm_id`, `device_id`, `dedupe_key`, `flag` and `approval_id`. RQ-08 and RQ-32 name them. They have no dot, so the script does not look them up as ids. They are PROPOSED. Owner: Team-Force.

#### 8c. Row-by-row compare

```
mismatches: none
```

#### 8d. Design files and tests

```
missing design files: none
existing tests found: 29
existing tests missing: none
planned tests that already exist: none
planned tests absent as required: 43
deferred tests: [('RQ-31', 'test file not present, as required')]
29 + 43 + 1 = 73
```

#### 8e. Semantic layer unchanged

```
generated/ matches the YAML. 7 files validated. Version 1.1.1.
41 passed in 3.26s     (pytest semantic-layer/tests -q)
```

The layer is unchanged. `git status` for `semantic-layer/` lists nothing, in the output before the first edit and in the output after the last one (see 8g).

#### 8f. Existing PRD tests

I copied `logs/audit.log` first. It had 240 lines (SHA-256 `BC2D23CDA9734222576DE51B7EC2917FE90C0C326DDC7DBD1FCB74B6ED482FAD`). The command named the 29 existing test ids that `prd.md` section 10 lists.

```
40 passed, 1 skipped, 60 warnings in 5.05s
```

After the run the log had 241 lines. After the restore it had 240 lines and the same SHA-256. This equals the S06R baseline (40 passed, 1 skipped). The skip is the `opa` test (RQ-59). No test file changed in this round.

One earlier command in this round passed no test ids by mistake (a quoting error in my shell line), so pytest ran its default set: 290 passed, 2 skipped. It appended 8 lines to the log. I restored the log from the copy. That run is not the check. The check is the run above.

#### 8g. git status

I ran `git status --short -uall` from the repository root before the first edit and after the last one (the second run came after the STATUS.md row was added). `-uall` is needed because `docs/prd/` is untracked, so plain `git status --short` shows it as one folder. Before the first edit I also took a SHA-256 hash of every file the first list names (23 files). I ran the same command after the last edit. **Verified Fact.**

The first output and the second output. Both have 24 lines, and they are the same line for line:

```
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions.md
 M 06-telecom-service-network-incident-ops/docs/02-baseline/S05R_Decisions_Taken.md
 M 06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md
 M 06-telecom-service-network-incident-ops/docs/12-finops/evidence.md
 M 06-telecom-service-network-incident-ops/docs/12-finops/optimization-backlog.md
 M 06-telecom-service-network-incident-ops/docs/ADR/0002-s05r-deferred-and-proposed-decisions.md
 D "Archive/Project Intent segments fed to stages/Project_Intent - Appendix B.md"
 M Project_Acronyms.md
 M playbook/README.md
 M playbook/S06-prd.md
 M playbook/S06R-prd-review.md
 M playbook/S07-application-and-demo.md
 M playbook/S08-second-model.md
 M playbook/STATUS.md
 M transcript/chat_transcript.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0003-s06-risk-recommendations.md
?? 06-telecom-service-network-incident-ops/docs/ADR/0004-defer-rq-31-answer-store.md
?? "06-telecom-service-network-incident-ops/docs/prd/Risk Management.md"
?? 06-telecom-service-network-incident-ops/docs/prd/prd-fixes.md
?? 06-telecom-service-network-incident-ops/docs/prd/prd-review.md
?? 06-telecom-service-network-incident-ops/docs/prd/prd.md
?? 06-telecom-service-network-incident-ops/docs/prd/traceability.md
?? "Project_Intent - Appendix B.md"
?? playbook/S06F-prd-fixes.md
```

The hash comparison (23 files before and after) found exactly four files with a different hash. Nothing else changed:

| File | Change |
|---|---|
| `docs/prd/prd.md` | The round 7 edits (edits 1 to 3, 5 to 8, 10 and 11). |
| `docs/prd/traceability.md` | The header edit (edit 11). |
| `docs/prd/prd-fixes.md` | This round section and the header. |
| `playbook/STATUS.md` | One new row at the end of the table (73 lines now, 72 before). The new row is the round 7 row ("S06F round 7"). No other row changed. |

No new file appeared. Every other file in the first list has the same hash after: `S05R_Decisions.md`, `S05R_Decisions_Taken.md`, `semantic-layer-revision.md`, `docs/12-finops/evidence.md`, `docs/12-finops/optimization-backlog.md`, ADR 0002, ADR 0003, ADR 0004, `Project_Acronyms.md`, `Project_Intent - Appendix B.md`, `docs/prd/Risk Management.md`, `docs/prd/prd-review.md`, `playbook/README.md`, `playbook/S06-prd.md`, `playbook/S06R-prd-review.md`, `playbook/S06F-prd-fixes.md`, `playbook/S07-application-and-demo.md` and `playbook/S08-second-model.md`. The deleted Archive file stays deleted. `transcript/chat_transcript.md` is in the first list and is appended after the final response, so it is outside this check. `logs/audit.log` is in neither list. It has the same content as the committed copy, because I restored it after each test run (240 lines, the same SHA-256 as before). Nothing under `semantic-layer/`, `apps/`, `policy/`, `tests/` or `data/` appears in either list. The test runs wrote `.pytest_cache` and `__pycache__` files. Git does not list them (the first list holds none), so they are not a difference.

The hash of `prd.md` before the round equals the one that round 6 recorded (`0BA9E7896268CFA0E27FF3F9510EFA10A54D022F5728C6B4257FE955DA6B1D6F`). So nothing touched the PRD between the two rounds. The same holds for `traceability.md` (`770EBE737CA4383DEEBC577E2D91409272B4D58BACD8F5A9C0DAA70D3121BAA9`).

File hashes after the last edit to the PRD (SHA-256), so the next stage can see whether the PRD changed:

- `prd.md`: `DC66A7234150D49E2868073B7CD72FC0346A200FFD405649C6E5AF0062FB6F45`
- `traceability.md`: `096200AB2CF1A05AF6FBC3FB0FCCC9DB680DCB280C621EFB643563856BEB4503`

#### 8h. Open question lines

```
Open question for S03 lines in prd.md section 15: 13
count equals 13: True
```

Places that state the count: `prd.md` line 12 ("Thirteen Open questions for S03 stay open") and `traceability.md` line 11 ("Thirteen Open questions for S03"). `prd.md` line 522 ("The 13 items that stay deferred") and line 565 ("All 13 have `target: null`") use 13 for other things (deferred items and metrics). All agree. No Open question line was added or removed. Line 599 gained one sentence. **Verified Fact.**

#### Searches

I searched `prd.md` and `traceability.md` for each term the block names, after the last edit.

| Term | Result |
|---|---|
| "approval id" | `prd.md`: line 9 (header, round 7 text), 94, 125, 130, 143, 208, 260, 272, 341 (RQ-32), 342 (RQ-33), 347 (RQ-38), 365 (RQ-47), 385 (RQ-58). All agree with the decision. None says the server makes the id on every call. Line 143 is a word-for-word quote. |
| "approval_id" | `prd.md`: RQ-29, RQ-32, RQ-33, RQ-38, RQ-47 (YAML id and test name), RQ-58 (test name). `traceability.md`: rows RQ-29, RQ-32, RQ-33, RQ-38, RQ-47, RQ-58, as YAML ids and test names only. The new text only says `approval_id` is null for a no. |
| "raw_count", "deduped_count", "flagged_count" | `prd.md` RQ-08 (the new sentence and the test name). `traceability.md` rows RQ-08 and section 2 (the test name only). |
| "held_aside" | `prd.md` RQ-08 (the new sentence and the id `status.code.dedupe_result.held_aside`) and RQ-62. `traceability.md` RQ-08 (the YAML id and a test name). |
| "five keys" | `prd.md` RQ-08 (the storm reply) and RQ-32 (the approval reply). Both are true for their own reply. |
| "flag word" | `prd.md` section 6 step 1, RQ-08, RQ-09. All agree: a flagged row stays in a list with its flag word. |
| "13" and "Thirteen" | See 8h. |

Every term in the new text is in the glossary or the YAML, or is a reply key (not an id), or is on an Open question line. The reply keys are PROPOSED with the owner named in RQ-08 and in the section 15 line. No new sentence defines a word.

### Done test

In `prd.md` RQ-13 the YAML id `metric.alarm_storm_size` was changed to `metric.alarm_storm_sizeX`. Check 8b then printed:

```
unresolved cited ids: [('RQ-13', 'metric.alarm_storm_sizeX')]
```

I restored the file from a copy taken before the change. The SHA-256 hash of the restored file equals the hash before the change (`DC66A7234150D49E2868073B7CD72FC0346A200FFD405649C6E5AF0062FB6F45`). Check 8b then printed:

```
unresolved cited ids: none
unresolved backticked id-shaped tokens (other than file names): none
```

**Verified Fact.**

### Map from the Decisions lines to the "Other findings" rows

The review has no FAIL row. I mark no row PASS. The next S06R does that.

| Finding in review v5.0 | Decisions line | Edits |
|---|---|---|
| X-3 | X-3 (a to d) | 1 to 4, and 11 |
| X-4 | X-4 (a to e) | 5 to 9, and 11 |
| X-7 | X-7 | 10, and 11 |
| X-5 | X-5, X-6, X-8 and X-9 (do not apply) | None. Left as it is. |
| X-6 | same line | None. Left as it is. |
| X-8 | same line | None. Left as it is. |
| X-9 | same line | None. Left as it is. |
| X-1, X-2 | The "Owner edits outside this stage" line | None. The owner closed both by hand on 2026-10-13. |

Decisions lines that close no finding: none.

### Owner edits outside this stage

I read each line after the PRD edits and compared it with the new RQ-08 and RQ-32 text. **Verified Fact.**

| File and line | What it says | Agrees with the PRD? |
|---|---|---|
| `playbook/S07-application-and-demo.md` line 35 | The storm reply has five keys (`raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside`). Each entry has four keys (`alarm_id`, `device_id`, `dedupe_key`, `flag`). `flag` is the flag word or an empty string. A blank `dedupe_key` goes in `held_aside`. Every other row goes in `rows`, flagged or not. The names are PROPOSED (owner Team-Force, RQ-08). | Yes. Same keys, same rule. |
| `playbook/S07-application-and-demo.md` line 38 | The server sets `approver`. For a yes it makes the approval id, and for a no it makes none. The audit row is written first, and for a no `approval_id` is null. The reply has `approval_id` (null for a no), `decision`, `approver`, `record_id` and `correlation_id`. | Yes. Same five keys. Same rule. |
| `playbook/S07-application-and-demo.md` line 106 | The demo approves, so it is a yes. | Yes. A yes has an approval id. |
| `Project_Acronyms.md` line 312 (`APR-`) | The server makes the approval id for a yes. A no gets no id. The caller never sends one (RQ-38). | Yes. |
| `Project_Acronyms.md` line 386 (storm route) | Five reply keys. A blank `dedupe_key` row is in `held_aside`. Every other row is in `rows`. A flagged row stays in `rows` with a flag word. The names are PROPOSED. | Yes. |
| `Project_Acronyms.md` line 388 (`POST /approvals/{id}`) | The server makes the approval id for a yes only. A no has no id. | Yes. |

Owner edits agree with the PRD. This stage did not edit any of these files.

### Items for the next S06R

These are not fixes and this round did not act on them. **Inference** unless a line says Verified Fact.

- **Verified Fact.** RQ-08 now says a held-aside row has a `flag` key, which can hold a flag word. An older sentence of the same cell says a held-aside row is "counted in the raw count only". The flagged count is "the number of rows that carry the flag word". A row with a blank `dedupe_key` that also carries a flag word is therefore counted by one sentence and not counted by the other. No sentence says such a row exists, and the one blank-key row in `alarms.csv` (`ALA-BAD1`, file line 353) has no times at all. This round kept every other sentence of the cell, as the block says. The owner may settle it in a later round.
- The RQ-32 test name `test_yes_is_stored_with_decision_approver_and_a_server_made_id` names the yes case. The block says S07 may add checks for the no case (`approval_id` null in the reply, the stored record and the audit row) and for the storm key names. No row was added.
- X-5, X-6, X-8 and X-9 of review v5.0 are open by owner decision.
- The review file keeps its original text. It still says the PRD is v1.7. The next S06R replaces it.
- Section 6 step 1 says "flag word" and names no key. The block keeps it so. RQ-08 holds the key names.
