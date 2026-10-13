# PRD review (S06R), round 6

| Field | Value |
|---|---|
| Stage | S06R. Independent review of `docs/prd/prd.md` v1.8 and `docs/prd/traceability.md` v1.8. This is the sixth run. It follows S06F round 7 (`docs/prd/prd-fixes.md`). The review edits no PRD, ADR, `Risk Management.md` or semantic-layer file. |
| Date / version | 2026-10-13, v6.0 of this review. It replaces v5.0 (round 5, PASS against PRD v1.7). The PRD version is read from the Date / version row of the `prd.md` header (line 7): v1.8. `traceability.md` line 6 carries v1.8 too. Semantic layer version read from `semantic-layer/README.md` line 6: `1.1.1`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | **PASS.** No row is FAIL. All three version strings read `1.1.1`. `prd.md` and `traceability.md` agree on 29 existing, 43 planned and 1 deferred test. The storm reply key names and the approval id rule are the same in every place that states them. The stale "S07 builds the answer store" lines that v5.0 listed are fixed. Twelve other findings are in section 6. None changes the stage result. |
| Evidence sources | `docs/prd/prd.md`; `docs/prd/traceability.md`; `docs/prd/Risk Management.md`; `docs/prd/prd-fixes.md` (round history only); the seven YAML files, `glossary.md`, `README.md`, `generated/manifest.json` and `schemas/semantic-layer.schema.json` in `semantic-layer/`; `docs/02-baseline/ai-qualification.md` (the S2Q table); `docs/02-baseline/semantic-layer-revision.md`; `docs/02-baseline/semantic-layer-review.md`; `docs/02-baseline/S05R_Decisions_Taken.md`; `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/ADR/0003-s06-risk-recommendations.md`; `docs/ADR/0004-defer-rq-31-answer-store.md`; `docs/12-finops/optimization-backlog.md`; `docs/12-finops/evidence.md`; `docs/09-ai-guardrails/approval-workflow.md`; `Project_Acronyms.md`; `Project_Intent.md`; `Project_Intent - Appendix B.md`; `playbook/README.md`; `playbook/S06-prd.md`; `playbook/S07-application-and-demo.md`; `docs/03-identity/target-access-matrix.md`; `docs/06-policy/ai-action-policy-design.md`; `apps/api/main.py`; `apps/api/services/policy.py`; `apps/api/services/dedupe.py`; `data/synthetic/alarms.csv`; `data/synthetic/devices.csv`; `logs/audit.log` |
| Assumptions | (1) "PRD line" means the physical line in `prd.md` on 2026-10-13. (2) "A term" means a domain word or a status word. Labels such as `existing`, `planned S07`, `deferred` and `DECIDED` are not terms. (3) P4 says "no AI use has execute agency". I read "AI use" as "a use where a model acts". `ai_use.remediation_execution` has agency execute, but its pick is workflow automation and the PRD builds no route for it. This is the same reading as v5.0 and as `semantic-layer-review.md` (R8). (4) The three random picks for P11 came from `random.SystemRandom().sample(range(1, 74), 3)` and gave RQ-15, RQ-42 and RQ-62. (5) The 10 random picks for P12.4 came from the same source. (6) `docs/02-baseline/S05R_Decisions.md` and `playbook/STATUS.md` are not inputs of this run. I list lines from them in Z-9 only because the PRD cites the first one and the playbook cites the second. |
| Unresolved issues | None blocks S07. Z-5 and Z-7 are worth an owner answer before S07 starts, because two builders could build them two ways. Thirteen Open questions for S03 stay open (`prd.md` lines 583 to 607). |
| Residual risks | A planned test is not evidence until it exists and passes. 43 of 73 tests are planned and 1 is deferred. S07 adds YAML ids under a new ADR, so the layer version will move. Then the PRD header, `traceability.md` and the S08 hash step must follow. The RQ-59 test skips on this machine because `opa` is not on the PATH. The PRD, `traceability.md`, both ADRs and `Risk Management.md` are not committed to git (Z-11). |

Claim labels: **Verified Fact** (I read it, ran it or resolved it), **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/` unless they start with `playbook/` or `Project_`.

## 1. Gate result

| Gate rule | Result |
|---|---|
| PASS when no row is FAIL | **Met.** No row is FAIL. |
| CONDITIONAL PASS when every FAIL is in P8 or P11 only | Not needed. |
| BLOCKED when any of P1, P2, P3, P4, P9, P13 is FAIL | Not met. All six are PASS. |
| Stage result | **PASS.** S07 may start. Section 6 lists optional clean-up. |

Four judgement calls sit behind this result. They are P2 (section 4 and Z-1), P4 (Assumption 3 in the header), P5 (Z-2) and P8 (Z-3). Read them before you start S07.

## 2. How the checks were run

| What I did | Result | Label |
|---|---|---|
| Parsed every `RQ-nn` row of `prd.md` section 10 (lines 283 to 416) | 73 rows. RQ-01 to RQ-73 once each in section 10. RQ-31 shows again in the section 13 decision tables (lines 513 and 519) as a decision row. RQ-68 to RQ-73 are at lines 411 to 416. | **Verified Fact** (script) |
| Collected every `id:` in the seven YAML files | 757 ids. That is 665 at `1.0.0` plus 92 added in S05R (`semantic-layer-revision.md` line 20). So ADR 0002, ADR 0003 and ADR 0004 added none. | **Verified Fact** (script) |
| Looked up every YAML id cited in the 73 requirement rows | All resolve. No row lacks a YAML id. | **Verified Fact** (script) |
| Compared `traceability.md` section 1 with `prd.md` section 10 row by row | YAML ids, test name and status match on all 73 rows. Section 2 of `traceability.md` lists the same 43 planned names as the planned rows of `prd.md`. | **Verified Fact** (script) |
| Counted the status of each test | 29 existing, 43 planned S07, 1 deferred (ADR 0004). | **Verified Fact** (script) |
| Checked that each `existing` test is a function in the named file, and that no `planned` test exists yet | All 29 existing found. None of the 43 planned names exists. `tests/app/` does not exist. The deferred file `tests/app/test_recommend_cache.py` does not exist. | **Verified Fact** (script) |
| Looked up every id-shaped token in `prd.md` and `traceability.md` | `prd.md`: 173 tokens. All resolve, except `policy.deny` and `policy.hold`. Those two are audit action values (`status.code.audit_action.policy_deny`, `status.code.audit_action.policy_hold`). `policy.py` is a file name. `traceability.md`: 123 tokens. All resolve. | **Verified Fact** (script) |
| Ran `pytest` for `tests` and `policy/tests` | 290 passed, 2 skipped. Both skips need `opa` (`policy/tests/test_policy_python.py` lines 567 and 577). One of them is the RQ-59 test. | **Verified Fact** (`pytest`, 2026-10-13) |
| Ran `python semantic-layer/build.py --check` and `pytest semantic-layer/tests -q` | "generated/ matches the YAML. 7 files validated. Version 1.1.1." 41 passed. Together with the line above: 331 passed, 2 skipped. That equals the S06F round 6 record in `playbook/STATUS.md` line 71. | **Verified Fact** |
| Saved `logs/audit.log` before the runs and restored it after | 240 lines and SHA-256 `BC2D23CD...` before and after. The test run appended 8 lines while it ran. The copy is back as it was. | **Verified Fact** |
| Compared the 11 rows of PRD section 7 with the S2Q table in `ai-qualification.md` (lines 38 to 48) | Pick, agency and approval-point text are equal on all 11 rows. | **Verified Fact** (script) |
| Compared the deferred list in `prd.md` section 13 (lines 523 to 539) with the locked list | Thirteen ids: D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20. D-07 is not in it. | **Verified Fact** (script) |
| Read the version in every place | `semantic-layer/README.md` line 6, all seven YAML files, `generated/manifest.json`, `semantic-layer-revision.md` line 6, `prd.md` line 10 and `traceability.md` line 9 all say `1.1.1`. | **Verified Fact** (script) |
| Counted the Open question lines | 13 lines, at `prd.md` lines 583, 585, 587, 589, 591, 593, 595, 597, 599, 601, 603, 605, 607. | **Verified Fact** (script) |
| Searched `prd.md`, `traceability.md`, `Project_Acronyms.md`, `approval-workflow.md` and `playbook/S07-application-and-demo.md` for the storm reply key names and the approval id rule | The five keys and the four row keys are the same wherever they are named. The approval id rule is the same wherever it is stated. See P13. | **Verified Fact** (search) |
| Re-read the data facts in `data/synthetic/alarms.csv` and `devices.csv` | 354 alarm rows and 354 device rows. 166 alarm rows have `last_seen_at` before `first_seen_at`, and one more (`ALA-BAD1`) has no times. Three `dedupe_key` values appear twice (`DED-00005`, `DED-00013`, `DED-00019`). 192 `true`, 161 `false` and 1 blank stale flags. File line 2 is `REC-0001` for `DEV-00001`, which `devices.csv` lacks. File line 353 is `ALA-BAD1`, blank except for its id. The worked examples of RQ-08, RQ-09, RQ-62 and section 8 hold. | **Verified Fact** (script) |
| Counted `enforced_today: false` rules and metric targets | 11 rules (the list in `prd.md` section 12 names the same 11). 13 metrics, none with a target. | **Verified Fact** (script) |
| Checked every access matrix row the PRD cites (TA-01, 02, 06, 08, 09, 11, 13, 15, 16, 17, 18 to 27, 28, 32, 34, 35) | Each row exists in `docs/03-identity/target-access-matrix.md` with the persona, action and resource the PRD names. | **Verified Fact** |
| Looked for source changes | `git status` shows no change under `apps/`, `policy/`, `tests/`, `semantic-layer/`, `data/` or `etl/`, other than byte-code and test-cache files. The last commit that touched them is `173d754` (2026-10-12). | **Verified Fact** |
| Searched every input file for "answer store", "stored answer", "cache", `RQ-31` and `OB-01` next to "S07" | No input file now says S07 builds the store. Four files keep an older recommendation line next to an update note. See Z-9. | **Verified Fact** |

## 3. Review table

Each row: check, result, where, one-sentence reason with its label.

| Check | Result | File and line or id | Reason |
|---|---|---|---|
| P1 | PASS | `prd.md` line 7 (v1.8) and lines 283 to 416; `traceability.md` line 6 (v1.8) and section 1; RQ-31 line 331; RQ-68 to RQ-73 lines 411 to 416 | **Verified Fact.** All 73 requirements have an id, YAML ids that resolve in `semantic-layer/`, and a test name. RQ-68 to RQ-73 are present. 29 tests exist, 43 are planned for S07 by name, and the RQ-31 name is kept and marked deferred (ADR 0004). `traceability.md` carries the same v1.8 and the same test statuses. PRD version recorded: v1.8. |
| P2 | PASS | `prd.md` lines 583 to 607 (13 Open question lines); section 4 of this file | **Verified Fact.** Every domain word is in the glossary or the YAML, or is on an Open question line, or is one of the four honesty labels. The new round 7 words (`raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside`, `flag`, `approval_id`) are either YAML ids, YAML values, or reply keys that line 599 names as PROPOSED and not YAML ids. One judgement call is in section 4. |
| P3 | PASS | `prd.md` section 7 (lines 132 to 148); `ai-qualification.md` lines 38 to 48 | **Verified Fact.** A script found pick, agency and approval-point text equal to the S2Q table on all 11 rows. The Outcome of `ai_use.remediation_execution` comes from the YAML (`outcome.execute`), and the section 7 intro says so. |
| P4 | PASS | `prd.md` section 3 (Highest agency column); lines 156 to 161 (EXECUTE row: no route); lines 260 and 272; RQ-19 line 319; RQ-57 and RQ-58 lines 384 and 385; `apps/api/main.py` | **Verified Fact.** The two AI uses the app builds have agency recommend. The only agency execute is `ai_use.remediation_execution`, and it has no route. The PRD lists the four gates, says the fourth does not exist, and lists no EXECUTE route. `main.py` has four routes (`/health`, `/records/{record_id}`, `/ai/summarize/{record_id}`, `/audit/{correlation_id}`) and none changes a device. |
| P5 | PASS | `prd.md` section 4 (lines 67 to 78); section 6 (lines 115 to 130, rows 122 to 127) | **Verified Fact.** Section 4 names the flow and gives five reasons. All six steps carry a verb. Steps 1 to 4 carry `persona.noc_operator`. Step 5 carries `role.admin`, which the PRD says is an API role with no persona. Step 6 carries "none" because no one takes it. See Z-2. |
| P6 | PASS | `prd.md` lines 239 to 251 (implement list); lines 253 to 269 (not-built list) | **Verified Fact.** Every not-built row has a reason. Line 258 holds "order provisioning stays unimplemented because no route reads service_orders.csv or circuits.csv". Line 259 holds "remediation validation stays unimplemented because this packet does not apply a live change". `GET /ready` is on the implement list (line 244, RQ-73). `GET /records/{id}` names the no-header 403 (line 243, RQ-68). A login or token route is on the not-built list (line 266, D-07, ADR 0003). |
| P7 | PASS | `prd.md` lines 213 to 233 (label table, including the new row at line 227); RQ-63 line 399; section 14 (lines 563 to 579) | **Verified Fact.** Every number the page shows has a label that matches `Project_Intent - Appendix B.md` lines 8 to 11: storm counts (REAL), `tokens` (EDUCATIONAL), `latency_ms` (SIMULATED), audit chain rows (REAL), outcome counts (REAL), completeness (REAL), repeated-prompt share (REAL), the `/health` status code (REAL), the HTTP status of each other reply (REAL), the counts inside `cannot_prove` (REAL), cost units (EDUCATIONAL). The v5.0 gap about status numbers (X-7) is closed. |
| P8 | PASS | RQ-44 (362), RQ-54 (381), RQ-69 (412), RQ-30 (330), RQ-71 (414); lines 160, 172, 437 to 443; lines 548 to 561 | **Verified Fact.** Every cutoff or target carries PROPOSED and Team-Force where it is introduced: 128 characters, the breaker numbers, the limit of 10 running calls, 10 seconds, the three service levels, the command-phrase list, the near-miss list and the cap on stored answers (no number). The 300 second lifetime is DECIDED (`OB-01`, line 443). The cost rate of 1.0 unit is EDUCATIONAL and decided (line 561). Lines 182 and 193 repeat "10 running calls" with a pointer to N-05 and no PROPOSED word. See Z-3. |
| P9 | PASS | RQ-03 (285), RQ-04 (286), RQ-23 (323), RQ-36 and RQ-37 (345, 346), RQ-48 (366) | **Verified Fact.** All five required checks are present: 404 on a missing id, clinician denied, HOLD_FOR_REVIEW on timeout with null summary, audit row before state change, one case rebuilt by correlation id. Only the clinician test exists today. The other four are planned by name. |
| P10 | PASS | `prd.md` lines 239 to 251; lines 253 to 269; section 12 (lines 461 to 487) | **Verified Fact.** `POST /ai/summarize/{id}` is kept (line 246). `POST /ai/recommend/{id}` is new and "the demo page calls it" (line 247). `GET /ready` and the no-header 403 are on the implement list. A login route is on the not-built list. No qualify, provision, retry, rollback or fix-validation route is required. 17 inherited gaps (RK-01 to RK-17) are listed with what the app does. |
| P11 | PASS | RQ-15 (306), RQ-42 (360), RQ-62 (398) | **Inference.** A reader new to telecom can picture the behaviour in all three. Detail in section 5. |
| P12.1 | PASS | `git status` for `apps/`, `policy/`, `tests/`, `semantic-layer/`; commit `173d754` | **Verified Fact.** No source file changed since the S05R commit. S06, S06F and the ADRs wrote documents only. |
| P12.2 | PASS | `ai-qualification.md` line 6 (2026-10-10); `prd.md` section 3 | **Verified Fact.** The S2Q table is dated before the PRD (v1.0 on 2026-10-12, v1.8 on 2026-10-13). PRD section 3 builds on it. |
| P12.3 | PASS | `prd.md` lines 44 to 65 and section 7; `ai-qualification.md` column "Why this pick needs no more intelligence than stated" | **Inference.** The PRD adds no AI pick. The two GenAI uses it builds come from the S2Q table, which states the need a rule cannot meet. The PRD does not repeat that need. |
| P12.4 | PASS | `prd.md` lines 16, 73, 76, 260, 471, 472, 473, 474, 478, 479 (10 of the 30 "Verified Fact" lines, picked at random) | **Verified Fact.** Line 16 is the label legend and makes no claim. The other nine each name a file, a test, a section, a source id or a command. The section 12 rows give the source id in the Source column. In those rows the label covers the risk (the gap that exists today). The "What the app does" column is a plan for S07, so a reader could read the label as covering the plan. See Z-10. |
| P12.5 | PASS | `docs/prd/prd.md`, `docs/prd/traceability.md` | **Verified Fact.** Both required S06 artifacts exist at the right path. |
| P12.6 | PASS | `prd.md` lines 619 to 631; `traceability.md` header | **Verified Fact.** The gate is stated in both files. Row 3 of the gate table says "This PRD does not define a term". See section 4 for how I read that sentence. |
| P12.7 | PASS | `prd.md` lines 437 to 443, 548 to 561 | **Verified Fact.** Every number traces to N-01 to N-06, `OB-01` or a dated decision. None is invented. |
| P12.8 | PASS | Same as P2 | **Verified Fact.** No term has a meaning that the YAML lacks, apart from the words on Open question lines. |
| P13 | PASS | `semantic-layer/README.md` line 6; `prd.md` line 10; `traceability.md` line 9; `semantic-layer-revision.md` line 6; `generated/manifest.json`; `prd.md` lines 243, 266, 299, 331, 341 to 343, 398, 411, 481, 504 to 541; `approval-workflow.md` line 76 | **Verified Fact.** All three version strings read `1.1.1`. The id count is 757, so ADR 0003 and ADR 0004 added none. The PRD states login out of scope (lines 266, 504, 511), the no-header 403 (RQ-68, RK-02), the answer store rule (RQ-31, RK-14, line 513: "never holds an answer that stopped with no text (BLOCK, or HOLD_FOR_REVIEW with no sentence)") and ADR 0004 (RQ-31 marked deferred at line 331, lines 519 and 541). `prd.md` and `traceability.md` agree on 29, 43 and 1. The 13 deferred items match. D-07 is not among them. **Storm reply keys:** `raw_count`, `deduped_count`, `flagged_count`, `rows`, `held_aside` and the four row keys appear in RQ-08 (line 299) and RQ-62 (line 398, `rows` and `held_aside`). Line 599 says the names are in RQ-08 and are PROPOSED. `Project_Acronyms.md` line 386 and `playbook/S07-application-and-demo.md` line 35 use the same names. None differs. **Approval id:** RQ-32 (line 341), RQ-33 (line 342), section 6 step 4 (line 125) and the section 8 Approval record row (line 208) all say a yes gets an id and a no gets none, with `approval_id` null in the reply, the stored record and the audit row. `approval-workflow.md` line 76, `Project_Acronyms.md` lines 312 and 388 and the S07 playbook line 38 say the same. No other input file says S07 builds the answer store (Z-9 lists the older lines that remain, each with an update note). |

## 4. P2 detail: words the PRD uses and the semantic layer lacks

I listed every word in `prd.md` (outside backticks) that is absent from the glossary, the seven YAML files, the README and Appendix B. That gave 209 words out of 930. Most are everyday words ("alone", "already", "apart"). I looked up each domain phrase. I also looked up every backticked token that is not an id. Only 16 are absent from the layer, and each is a file name, an example id, a code name, or a word on an Open question line.

| Phrase in the PRD | Where | What the semantic layer has | Result |
|---|---|---|---|
| answer store, stored answer, cache, cap, lifetime | RQ-31 (331), RK-14 (481), lines 443, 513, 519 | None. Open question line 593. No id invented. | PASS under exception 1. |
| near-miss phrase, near-miss list | RQ-71 (414) | None. Open question line 595. | PASS under exception 1. |
| claimed role | RQ-65 (401), RK-01 | None. Open question line 597. | PASS under exception 1. |
| raw count, flagged count; keys `raw_count`, `flagged_count`, `deduped_count` | RQ-08 (299), section 6 step 1 (122) | None. Open question line 599. The line says the key names are PROPOSED and are not YAML ids. | PASS under exception 1. See Z-1. |
| deduped count | RQ-08 (299) | `metric.alarm_storm_size` (`metrics.yaml` line 142): "after rows with the same dedupe_key are counted once". | PASS. Same meaning. RQ-08 adds that a blank key is left out. |
| held aside; key `held_aside` | RQ-08 (299) | `status.code.dedupe_result.held_aside` (`status-taxonomy.yaml` line 3609): "The row has no usable key... The row is held aside and counted." | PASS. RQ-08 says which count: the raw count only. The YAML says "counted" and does not say in which count. |
| flag, flag word; key `flag` | RQ-08, RQ-09 | `status.code.alarm_flag.last_seen_before_first_seen` and `status.code.alarm_flag.times_unreadable`. | PASS. |
| `decision`, `approver`, `record_id` (16th key), `final_action`, `record.storm_read`, `ai.recommendation`, `ai.approval` | RQ-32, RQ-40, RQ-41, RQ-52 | None. Open question lines 601 to 607. | PASS under exception 1. |
| a word for an unknown role; a failmode for a forbidden value in the answer; a status id for the readiness body; degraded mode as a design mode | RQ-69, RQ-70, RQ-73 | None. Open question lines 585 to 591. RQ-70 uses the existing `failmode.forbidden_field_in_prompt`. | PASS under exception 1. |
| REAL, PRECOMPUTED, SIMULATED, EDUCATIONAL; honesty label | RQ-63, section 8 | `Project_Intent - Appendix B.md`. Open question line 583. | PASS under exception 2. |
| reasons list | lines 160 to 195, RQ-30, RQ-54, RQ-70 | `entities.yaml` line 894: the policy "returns allow, deny, and the reasons". | PASS. Same meaning. |
| command-phrase list | RQ-30 (330) | `glossary.md` line 339, "the command list". | PASS. Same meaning. |
| held case, inbox, queue | line 267, RK-10 | `resource.model_call_queue` (`access-semantics.yaml` line 121). | PASS. |
| in-flight limit, 10 calls at the same time | RQ-54 (381) | "the in-flight limit" in `ai-context-policy.yaml`. | PASS. |
| incident candidate | RQ-09 (300) | `status-taxonomy.yaml`: "The row does not become an incident candidate." | PASS. |
| approval record | lines 208, 601 | `concept.approval` (`entities.yaml` line 721): "A named person's recorded yes or no". | PASS. Same meaning. |
| case id, audit action word | RQ-44 (362), RQ-52 (370) | `rule.audit_case_id_limit`; `status.code.audit_action.*`. Each row explains the word with the same ids. | PASS. |

**Judgement call (see Z-1).** Exception 1 says a word on an Open question line is PASS "when listed and not defined". RQ-08, RQ-31, RQ-65 and RQ-71 each say what the behaviour behind the word is, because a requirement has to. Each Open question line also says "This PRD uses those words and does not explain them". Both cannot be fully true. I scored PASS. The exception ends with "if the PRD does not invent the missing id". The PRD invents no id. A strict reader could score this FAIL. Z-1 gives a one-line fix. The owner kept this text in round 7 (`prd.md` line 9).

## 5. P11 detail: three random requirements

| Requirement | What a reader new to telecom pictures | Result |
|---|---|---|
| RQ-15 (line 306): "Every storm read writes one `record.storm_read` audit row that holds the correlation id, the role and the resource `resource.alarm`." | The reader pictures one log line saved each time someone reads a storm. The line names the case, the caller's role and what was read. "Storm" is explained by RQ-08 (a group of alarm rows with one `storm_batch_id`) and by the section 8 example. "Correlation id" is explained in section 6 (the page sends one `X-Correlation-Id` for the whole walk). | PASS |
| RQ-42 (line 360): "`GET /audit/{correlation_id}` returns the rows of one case in time order." | The reader pictures one request that brings back every log row of one case, oldest first. "Case" is explained in section 6. | PASS |
| RQ-62 (line 398): the page walks the demo flow. | The reader pictures one page with six steps: pick a storm, read the counts, pick a device, ask for a recommendation, say yes or no, read the audit chain. The worked example (`STO-00001`, `DEV-00001`, no device row) says what the page shows when the device is missing. The row is one long paragraph, so a reader must go slowly. Each word is plain. | PASS |

## 6. Other findings (outside P1 to P13)

These come from the objective: could a builder build the app from the PRD and the semantic layer with no other source? None changes the stage result. Each has a label. Z-1 to Z-4 carry over from review v5.0. The owner kept them as they are (`prd.md` line 9). Z-5 to Z-11 are new.

### Z-1. Open question lines say "does not explain" while RQ rows describe the words (was X-5)

`prd.md` lines 593, 595, 597 and 599 say "This PRD uses those words and does not explain them". RQ-08 (299), RQ-31 (331), RQ-65 (401) and RQ-71 (414) do say what the behaviour behind each word is. **Verified Fact** for the text. **Fix (optional):** change the sentence on those four lines to "This PRD says what the word does in RQ-nn and gives it no YAML id."

### Z-2. Workflow steps 5 and 6 have no persona (was X-6)

Step 5 carries `role.admin`, which is an API role and not a persona. Step 6 carries "none" (`prd.md` lines 126 and 127). Line 130 and section 5 say why. P5 asks for a persona on each step. I scored PASS because the PRD states the reason, and the owner kept it in rounds 5 and 7. A strict reader could score it FAIL. **Verified Fact** for the text. **Inference** for the reading.

### Z-3. The limit of 10 running calls has no PROPOSED word at lines 182 and 193 (was X-8)

Both lines cite N-05 and nothing else. Lines 160, 172, 381 and 441 label it. A reader of section 7 alone sees a bare number. I scored P8 PASS because "N-05" is the id of a PROPOSED row, one step away (line 557, under the heading at line 548). A strict reader could score it FAIL, and the fix is one line. **Verified Fact** for the text. **Fix (optional):** write "(PROPOSED, N-05)" on both lines.

### Z-4. Smaller items (was X-9)

- RQ-30 (line 330) is missing a full stop after "with no text", before "The reasons list". **Verified Fact.**
- `playbook/S07-application-and-demo.md` "Required work" item 1 (lines 31 to 40) lists seven routes. It omits `GET /ready` (RQ-73) and the no-header 403 on `GET /records/{id}` (RQ-68). Its Scope says "the routes the PRD lists", so the PRD wins. This file is not an input of this review. **Verified Fact** for the omission. **Inference** for the impact.

### Z-5. The storm counts cannot come from `alarm_intake` as it is written (new)

`prd.md` line 77 says the storm step "uses `dedupe.py`". Line 245 says "`dedupe.py` exists and has no caller". RQ-08 and RQ-09 define the counts in their own way: a flagged row stays in `rows` and still counts in the deduped count when its `dedupe_key` is not blank.

`alarm_intake` in `apps/api/services/dedupe.py` (lines 142 to 171) does the opposite. A flagged row goes into `flagged` and "goes no further". It is not entered in the repeat memory. I ran it on three storms with the real file:

| Storm | Raw rows | `alarm_intake` result | RQ-08 and RQ-09 say |
|---|---|---|---|
| `STO-00019` | 2 | candidates 0, flagged 2, repeats 0, held aside 0 | raw 2, deduped 1, flagged 2 |
| `STO-00005` | 2 | candidates 1, flagged 0, repeats 1, held aside 0 | raw 2, deduped 1, flagged 0 |
| `STO-00002` | 1 | candidates 0, flagged 1, repeats 0, held aside 0 | raw 1, deduped 1, flagged 1 |

**Verified Fact** for both sets of numbers. **Inference** for the impact: a builder who reads "uses `dedupe.py`" literally and adds up the lists of `alarm_intake` gets a deduped count of 0 for `STO-00019`. RQ-09 says 1. The planned test `test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` would catch it, but only after S07 has built the wrong thing. **Fix (optional):** say in RQ-08 that the route counts the rows itself, and that `check_alarm_row` (not `alarm_intake`) supplies the flag word. Change lines 77 and 245 to match.

### Z-6. The degraded-mode table says "200" for model routes when `alarms.csv` is missing (new)

`prd.md` line 455, column "Model routes", says 200. `POST /ai/recommend/{id}` returns 202 on a call with no failure row (RQ-18). `POST /ai/summarize/{id}` returns 200 (RQ-16). The cell means "no change from the healthy state", but it shows one number for two routes. **Verified Fact** for the text. **Inference** for the confusion. **Fix (optional):** write "unchanged (200 summarize, 202 recommend)" in that cell.

### Z-7. The order of the 422 and the 404 on `POST /approvals/{id}` is not fixed (new)

RQ-32 (line 341) says the role check runs before the body check, and a bad body returns 422. RQ-34 (line 343) says a call with no shown recommendation returns 404. The PRD does not say which one wins when both are true. Two builders could choose differently. The PRD's gap rule (line 613) tells S07 to stop and write a gap, so S07 will not guess. **Verified Fact** for the text. **Inference** for the impact. **Fix (optional):** add one sentence to RQ-34, for example "The body check runs before the recommendation check." The owner picks.

### Z-8. A blank-key row that also carries a flag word is read two ways (carried from `prd-fixes.md` round 7)

RQ-08 (line 299) says a held-aside row is "counted in the raw count only". The same cell counts every row that carries a flag word in the flagged count, and gives held-aside rows a `flag` key. A blank-key row with a flag word would be counted in the flagged count by one sentence and left out by the other. **Verified Fact:** `data/synthetic/alarms.csv` has no such row. `ALA-BAD1` has a blank storm id too, so no storm reply lists it. The owner knows this (`prd-fixes.md` residual risks, round 7 item a). It does not make P13 FAIL, because P13 covers key names and the approval id rule. **Fix (optional):** change "counted in the raw count only" to "counted in the raw count, and in the flagged count when it carries a flag word".

### Z-9. Older lines in input files that still read as "S07 builds the answer store" (P13 finding)

P13 asks me to list each input file that says S07 builds the answer store, with file and line. The lines that v5.0 listed (X-1, X-2) are fixed. `evidence.md` line 265, `S05R_Decisions_Taken.md` line 94, `S05R_Decisions.md` lines 354 and 621, ADR 0003 lines 12 and 69, `Risk Management.md` line 11, `Project_Acronyms.md` lines 387 and 400 and ADR 0002 line 11 now read correctly. **Verified Fact.**

These older lines remain. Each sits next to an update note, or is conditional. None says S07 does build it today.

| File and line | What it says | What sits next to it |
|---|---|---|
| `docs/ADR/0003-s06-risk-recommendations.md` line 44 | "The 300 second answer store stays in S07." | Line 46: "Update, 2026-10-13. ADR 0004 moves the build of the store out of S07." |
| `docs/prd/Risk Management.md` lines 51, 221, 223 and 265 | "S07 if kept." "Keep the 300 second lifetime if S07 has time." "Keep the 300 second answer store in S07?" | Line 225: "Decision (2026-10-13). Team-Force deferred RQ-31 in ADR 0004. S07 builds no answer store." Lines 51, 223 and 265 have no note of their own. |
| `docs/02-baseline/S05R_Decisions_Taken.md` line 53 and `S05R_Decisions.md` line 360 | "If the cache is built in S07, add the cache flag first." | It is conditional. The PRD quotes the same words at lines 537 and 541 and says S07 does not add the flag. |
| `playbook/STATUS.md` line 51 (not an input of this run) | "The cache itself is built in S07." | It is a dated row of 2026-10-11. Rows 70 and 71 record the deferral. No fix needed. |

**Inference** for the impact: an S07 builder who reads only `Risk Management.md` line 265 could think the store is still an open question for S07. The PRD tells S07 to stop and write a gap when a file disagrees (`prd.md` line 613), so the cost is a stop and not a wrong build. **Fix (optional):** add "(deferred, ADR 0004)" to `Risk Management.md` lines 51 and 265.

### Z-10. The section 12 label covers the risk, and a reader may read it as covering the plan (new)

In the risk table (lines 468 to 484), the Label column says **Verified Fact**. It backs the risk and its source id (for example RK-04 and SB-04). The "What the app does" column is a plan for S07 and is not yet true. P12.4 passes because each row names its source. **Inference** for the reading. **Fix (optional):** rename the column "Label (the risk)".

### Z-11. The PRD files are not committed to git (new)

`git status` on 2026-10-13 shows `docs/prd/prd.md`, `traceability.md`, `prd-fixes.md`, `prd-review.md`, `Risk Management.md`, ADR 0003 and ADR 0004 as untracked files. The last commit is `173d754` (2026-10-12). **Verified Fact.** **Inference** for the impact: stage S07 builds from files that no commit holds, and the S08 hash step needs a fixed version of the PRD. **Fix (optional):** commit the PRD set after this review and before S07.

### Z-12. The demo case is not named

Section 6 says "the demo walks one case" and does not name a storm. The storm decides what the page shows. `STO-00002` leads to `DEV-00002` (stale flag `false`), so the recommendation returns a sentence. `STO-00001` leads to a device that does not exist (404, then BLOCK). `STO-00005` leads to `DEV-00005` (stale flag `true`), so the recommendation is BLOCK. Of the 350 storms in `alarms.csv`, 158 reach a device with stale flag `false`. **Verified Fact** (script). **Inference:** the S07 demo script must pick one storm that reaches a sentence, or the demo ends at BLOCK and no approval can be stored (RQ-34). The section 3 worked example already uses `DEV-00002`. **Fix (optional):** name `STO-00002` as the demo storm in the S07 demo script, and write that in the "PRD gaps" table of `docs/demo/evidence.md` as a choice S07 made.

## 7. What closed since v5.0

| v5.0 item | Now | Evidence |
|---|---|---|
| X-1 (input files that say S07 builds the answer store) | Closed for the lines v5.0 named. Older lines with update notes are in Z-9. | `evidence.md` line 265; `S05R_Decisions_Taken.md` line 94; `S05R_Decisions.md` lines 354 and 621; ADR 0003 lines 12 and 69 |
| X-2 (other stale lines) | Closed. | `Risk Management.md` line 11 ("Thirteen"); `Project_Acronyms.md` lines 387 and 400; ADR 0002 line 11 |
| X-3 (RQ-08 had no key names) | Closed. RQ-08 names five keys and four row keys. RQ-62 and line 599 agree. | `prd.md` lines 299, 398, 599 |
| X-4 (RQ-32 and RQ-33 read two ways on a no) | Closed. Only a yes gets an id. `approval_id` is null for a no in the reply, the record and the audit row. | `prd.md` lines 125, 208, 341, 342 |
| X-5 (Open question wording) | Left as it is by owner decision. Same as Z-1. | `prd.md` line 9 |
| X-6 (steps 5 and 6 have no persona) | Left as it is. Same as Z-2. | `prd.md` lines 126, 127 |
| X-7 (HTTP status numbers have no label) | Closed. A label row covers the status of each reply. | `prd.md` line 227 |
| X-8 (10 running calls with no PROPOSED word) | Left as it is. Same as Z-3. | `prd.md` lines 182, 193 |
| X-9 (RQ-30 full stop; S07 playbook route list) | Left as it is. Same as Z-4. | `prd.md` line 330 |

## 8. Verdict on the objective

A builder can build the governed application from the PRD and the semantic layer. The route list, the roles per route, the four outcomes, the failure rows, the honesty labels, the not-built list and the 73 tests agree with each other. Every YAML id resolves. All version strings match. The counts of 29, 43 and 1 agree in both PRD files. The answer store is deferred in the PRD, ADR 0004 and the tracked counts. The storm reply keys and the approval id rule are the same in every place.

Two things can still make two builders differ: how the storm counts are computed (Z-5) and which error comes first on the approval route (Z-7). **Inference** for the verdict. The facts behind it are in sections 2, 3 and 6.

## 9. Fixes required

None. No row is FAIL.

Optional fixes, in the order I suggest:

| Fix | Closes | Where | Change |
|---|---|---|---|
| O-1 | Z-5, Z-7, Z-6, Z-8 | `prd.md` RQ-08, RQ-34, section 4 reason 5 (line 77), section 9 (line 245), section 11 degraded table (line 455) | Four short edits. PRD and `traceability.md` go from v1.8 to v1.9 together. Stage S06F applies them. Run S06R again after. |
| O-2 | Z-1, Z-3, Z-4, Z-10 | `prd.md` lines 182, 193, 330, 593 to 599, section 12 | Wording only. Same version bump as O-1. |
| O-3 | Z-9 | `Risk Management.md` lines 51 and 265 | Add "(deferred, ADR 0004)". No PRD version change. |
| O-4 | Z-11, Z-12 | Git; S07 demo script | Commit the PRD set before S07. Name the demo storm in the S07 demo script. |

## 10. Lifecycle linkage

- Requirement ids cited: RQ-03, RQ-04, RQ-08, RQ-09, RQ-15, RQ-16, RQ-18, RQ-19, RQ-23, RQ-30, RQ-31, RQ-32, RQ-33, RQ-34, RQ-36, RQ-37, RQ-42, RQ-44, RQ-48, RQ-52, RQ-54, RQ-57, RQ-58, RQ-59, RQ-62, RQ-63, RQ-65, RQ-68, RQ-69, RQ-70, RQ-71, RQ-73 and the full set RQ-01 to RQ-73.
- Semantic-layer ids cited: `metric.alarm_storm_size`, `status.code.dedupe_result.held_aside`, `status.code.alarm_flag.last_seen_before_first_seen`, `status.code.alarm_flag.times_unreadable`, `status.code.audit_action.policy_deny`, `status.code.audit_action.policy_hold`, `concept.approval`, `resource.model_call_queue`, `ai_use.remediation_execution`, `outcome.execute`, `provenance.approval_id`, `rule.audit_case_id_limit`, `failmode.forbidden_field_in_prompt`.
- ADR 0002 changed one YAML sentence (the p95 choice) and raised the layer to `1.1.1`. ADR 0003 and ADR 0004 added no YAML id. Both facts hold (757 ids, `build.py --check` passes).
- The version in `semantic-layer/README.md` is `1.1.1`. The PRD header, the header of `semantic-layer-revision.md`, all seven YAML files and `generated/manifest.json` carry the same string. The PRD and `traceability.md` are both v1.8.
- Next: S07 may start. Apply O-1 through S06F if you want the storm count rule and the approval error order fixed before S07. If you do, run S06R again in a fresh chat. Commit the PRD set first (O-4). S08 gives the second model the PRD that passed this review.
