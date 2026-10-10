# Semantic layer review

| Field | Value |
|---|---|
| Stage | S03R — Semantic layer review (Execution Plan Phase 3 review), round 2 |
| Date / version | 2026-10-10, review v2.0 of semantic layer `1.0.0`. This file replaces the round 1 review (v1.0). Round 1's fix list is copied word for word in `docs/02-baseline/semantic-layer-fixes.md`. |
| Author | Independent reviewer (fresh Cursor chat, Claude Opus 5.5) for Mangesh (FDE) |
| Status | BLOCKED for S04. Every check on the `semantic-layer/` tree passes, including all seven hard-block rows (R1, R5, R7, R8, R10, R11, R13). One row fails: R14.7. `data-quality-baseline.md` line 11 still says the owner of the two PROPOSED bounds is Unknown, while line 12 of the same file says Team-Force. R14.7 falls outside the CONDITIONAL PASS allowance. Fix 1 is two sentence swaps. |
| Evidence sources | `Semantic_Layer_capture.pdf`; `Project_Intent (section 6.2).md`; every file under `semantic-layer/`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/semantic-layer-fixes.md`; `docs/00-contract/operating-contract.md` row 10; `playbook/README.md` failure list; `playbook/STATUS.md`; `git diff`, `git status`, and `git ls-files` on 2026-10-10; runs of `build.py --check`, `pytest semantic-layer/tests`, and a clean rebuild in a temp copy on 2026-10-10 |
| Assumptions | R8 reads "AI use" as "a step where a model acts", the same reading as round 1. R14.7 treats a bound that a file marks "owner is Unknown" as a bound with no owner, the same reading as round 1. A Python byte-code cache under `tests/__pycache__/` is not part of the layer (Inference). |
| Unresolved issues | The completion gate names no status for a FAIL in R14 alone. This review calls it BLOCKED because `playbook/README.md` says a FAIL row blocks the next stage. Round 1 used the same reading. Fix 3 needs a choice from Team-Force. |
| Residual risks | The tree tests cannot see the baseline docs. A baseline file can contradict the tree and every test still passes. That is how the R14.7 gap got through S03F round 1. |

Claim labels: **Verified Fact** (I ran it or read it), **Inference**.

Paths below are relative to `06-telecom-service-network-incident-ops/`. "SL" means `semantic-layer/`.

## Points for the S03R reviewer, from S03F round 1

S03F round 1 listed three edits that went past the literal fix text. Team-Force accepted all three on 2026-10-10. This review checked that each edit matches its description.

| Point | Verdict | Evidence |
|---|---|---|
| 1. The comment on `SL/access-semantics.yaml` line 294 | Accept. The edit matches. | **Verified Fact.** Line 294 now reads `# All grants are PROPOSED. Owner Team-Force. Stage S04-03 confirms them.` The file has 19 `owner: Team-Force` keys and no other owner text. `git diff` shows the comment as the only non-key change in the file. A YAML comment does not reach the JSON. No file under `SL/generated/` contains "Mangesh". The S03R playbook now asks for this kind of edit: a fix that changes an owner also covers every comment in the same file that states it. |
| 2. Quotes on `SL/metrics.yaml` lines 69 and 107 | Accept. The edit matches. | **Verified Fact.** Both `proposed_bound_note` values are now in double quotes. `git diff` shows that the only other change on each line is "Owner Unknown" to "Owner: Team-Force", as fix 4 says. `SL/generated/metrics.json` holds both strings with no quote marks around them. The build and the tests pass. |
| 3. README counts and the new test | Accept. The edit matches. | **Verified Fact.** `test_every_agency_and_pick_word_is_defined` is at `SL/tests/test_semantic_layer.py` lines 278–294. It runs and passes. `SL/README.md` says 35 tests on lines 8, 88, and 182. It lists the new check on line 189. It has `agency.` and `pick.` rows in the id table on lines 118–119. It says 181 glossary rows on line 213. `glossary_rows()` returns 181. Two older texts still give the old picture. See advisory A7. |

## Review table

### Checks R1 to R13 and R15

| Check | Result | Citation | Reason |
|---|---|---|---|
| R1 | PASS | `SL/README.md` lines 31–63; `Semantic_Layer_capture.pdf` page 1; test `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` | **Verified Fact.** The disk holds the eleven entries in the PDF, plus `build.py` and `generated/` (8 files). README lines 59–65 say why those two were added. The only other file is `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc`. Python wrote it. **Inference:** a byte-code cache is not part of the layer. See advisory A1. |
| R2 | PASS | Tests `test_every_item_has_a_source_list_of_existing_paths` (test file line 400) and `test_every_proposed_item_names_an_owner` (line 413) | **Verified Fact.** Every item with an id carries a `source:` list of paths that exist. All 28 `owner:` keys say `Team-Force`: 19 in `access-semantics.yaml`, 7 in `ai-context-policy.yaml`, 2 in `metrics.yaml`. Both tests pass. |
| R3 | PASS | `docs/02-baseline/data-quality-baseline.md` lines 200–210; `SL/status-taxonomy.yaml`; test `test_every_word_in_every_word_column_is_in_the_taxonomy` (line 520) | **Verified Fact.** The baseline names seven severity words, `legacy` in `hostname`, and `requires_review` in `vendor`. Each one is a `status.word.*` item. The test checks every cell of every CSV status column against the taxonomy and passes. `status-taxonomy.yaml` did not change in S03F (`git status`). |
| R4 | PASS | `SL/status-taxonomy.yaml` lines 3387–3478: `collision.gold_bronze_as_severity` (3388), `collision.status_words_in_hostname_and_vendor` (3410), `collision.rec_0001_first_key_in_six_tables` (3445), `collision.clinician_role_in_telecom_api` (3464) | **Verified Fact.** The `collisions` block holds exactly the four named entries. Test `test_collisions_block_has_the_four_named_entries` passes. Five more overlaps sit under `other_overlaps` from line 3479. |
| R5 | PASS | `SL/business-rules.yaml` lines 33, 60, 75, 87, 104, 118 | **Verified Fact.** The six required rules are present, each with an id: `rule.missing_id_not_other_device`, `rule.ai_output_cannot_execute`, `rule.alarm_last_seen_not_before_first_seen`, `rule.shared_admin_not_least_privilege`, `rule.duplicate_dedupe_key_in_storm_is_one_alarm`, `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. The file holds 13 rules in all. S03F changed only the owner name in the line 132 `stage_note`. |
| R6 | PASS | `SL/access-semantics.yaml` lines 297, 336, 366, 382, 398, 424, 441 (seven `persona.*` items); lines 283–284 (`removed_roles`, `role: role.clinician`) | **Verified Fact.** All seven personas are present. Each grant uses ids from the five value lists. `clinician` is under `removed_roles`. Tests `test_required_personas_present` and `test_api_roles_today_and_clinician_removed` pass. |
| R7 | PASS | `SL/ai-context-policy.yaml` lines 78–82 (forbidden), 224–257 (`policy.outcomes`), 262–307 (`policy.fail_to_person`), 362–483 (`ai_uses`); `docs/02-baseline/ai-qualification.md` lines 36–48 | **Verified Fact.** `mgmt_ip` and `credential_profile` are forbidden. The four outcomes and fail-to-person are present. I compared all eleven uses with the S2Q table. Each has the same pick, agency, outcome, and approval point. The only change on both sides since round 1 is the owner name, Mangesh (FDE) to Team-Force. Example: S2Q line 43 says "Desk job: PROPOSED. Owner: Team-Force. Stage S04-09 confirms the job title". YAML line 418 says "Desk job PROPOSED. Owner Team-Force. Stage S04-09 confirms." The meaning is the same. |
| R8 | PASS | `SL/ai-context-policy.yaml` line 464 (`ai_use.remediation_execution`); schema `SL/schemas/semantic-layer.schema.json` lines 513–514; tests `test_four_outcomes_present_and_model_never_executes` and `test_every_agency_and_pick_word_is_defined` | **Verified Fact.** The only AI use with `agency: execute` is remediation execution. Its pick is `workflow_automation`, and its executor is `persona.automation_service`. No model runs that step. The schema limits a `genai` pick to analyse or recommend. **Inference:** this matches S2Q line 8, "No row gives execute agency to a model". See advisories A2 and A6. |
| R9 | PASS | `SL/glossary.md` lines 322–377 (agency, pick, AI use, provenance rows), line 231 (`resource.sensitive_device_fields`); `SL/ai-context-policy.yaml` lines 313–357 (`agency_levels`, `picks`); test file lines 58–62 (`GLOSSARY_PREFIXES`) | **Verified Fact.** The glossary now has rows for the 4 agency words, the 4 pick words, the 11 `ai_use.*` ids, and the 9 `provenance.*` fields. Row 231 says what `mgmt_ip` and `credential_profile` are. The glossary meanings agree with the YAML `description` text. For example, `agency.analyse` reads "Read stored fields and show them. Nothing changes." in both files. Test `test_glossary_and_yaml_agree_on_every_term` covers 19 prefixes and passes. Every `agency` and `pick` value in the seven files has a matching item. |
| R10 | PASS | `SL/build.py --check`; `pytest SL/tests`; test `test_schema_validates_every_yaml_file` | **Verified Fact.** The schema validated all seven YAML files. 35 of 35 tests passed. The output is pasted below. |
| R11 | PASS | `SL/build.py`; `SL/generated/` (8 files) | **Verified Fact.** I copied the repo to a temp folder, deleted `generated/`, and ran `build.py`. All 8 rebuilt files have the same SHA-256 as the files in the real tree. The output is pasted below. The real tree was not touched. |
| R12 | PASS | `SL/metrics.yaml` lines 69 and 107; `SL/entities.yaml` lines 416 and 485; `SL/glossary.md` line 201; `SL/README.md` lines 127, 229, 230 | **Verified Fact.** I searched the tree for threshold, cutoff, maximum, minimum, bound, limit, target, and timeout. Two numbers are bounds: the retry bound of 1000 and the `sla_breach_risk` range of 0 to 1. Each one says PROPOSED and "Owner: Team-Force" wherever it appears. Every `target:` is `null`. `timeout_seconds` is `null`. The other numbers are counts from the data, such as "Minimum 32. Maximum 4995." |
| R13 | PASS | Test `test_no_secret_value_anywhere_in_the_tree` (test file line 599); `SL/ai-context-policy.yaml` line 89 | **Verified Fact.** The test reads the secret values from `.env.example` and `legacy/reconcile_legacy.py` and finds none of them in the tree. I also scanned for password, secret, token, and key assignments, for `sk-`, `AKIA`, and `Bearer` strings, and for a password inside a URL. Nothing matched. Line 89 lists six secret names and no values. |
| R15 | PASS | `SL/glossary.md` rows `scope.own_vendor_devices` (line 258), `metric.tokens_per_invocation` (line 195), `scope.none` (line 259) | **Verified Fact** for the pick: Python `random.sample` with seed 20261011 over the 181 glossary rows. `own vendor devices` is clear: "Only devices made by the caller's company." `none` is clear: "No records. Used for an action a persona may never take." `tokens per invocation` is clear on "one model call". The row does not say what a token is. Row `provenance.tokens` (line 371) does: "A token is a small piece of text that a model counts and charges by." **Inference:** a new reader can picture all three, with one look-up for "token". See advisory A8. |

### R14: failure list from `playbook/README.md`

| Check | Result | Citation | Reason |
|---|---|---|---|
| R14.1 Code before its analysis gate | PASS | `playbook/STATUS.md` S2Q and S03F rows; `git status` on `apps/`, `policy/`, `data/`, `etl/`, `legacy/` | **Verified Fact.** The only code changed in S03F is `SL/tests/test_semantic_layer.py` and `SL/schemas/semantic-layer.schema.json`. Round 1's fixes 1 and 2 asked for both. `git status` shows no change under the app, policy, data, ETL, or legacy folders. |
| R14.2 Design before the S2Q table | PASS | `docs/02-baseline/ai-qualification.md` status row; `SL/ai-context-policy.yaml` lines 310–311 and 333 | **Verified Fact.** The eleven AI uses still come from S2Q. The new agency and pick meanings cite `ai-qualification.md` lines 18–20 as their source. |
| R14.3 AI picked with no stated need | PASS | `SL/ai-context-policy.yaml` lines 413–450; `ai-qualification.md` lines 43–45 and 67–84 | **Verified Fact.** Three uses are `genai`: incident summary, next-action recommendation, and configuration suggestion. S2Q states the need for each one: writing new text, or reasoning over varied inputs. The other eight uses call no model. |
| R14.4 Claim with no label, or a Verified Fact with no pointer | PASS | `SL/glossary.md` line 18 | **Verified Fact.** Line 18 now says status-word meanings are Inference, because the repo defines none of them. That clears the round 1 finding. The new rows that add an example, such as `pick.rules`, cite `ai-qualification.md` in the YAML `source`. |
| R14.5 Artifact missing or at the wrong path | PASS | `SL/` tree; `docs/02-baseline/semantic-layer-fixes.md`; `playbook/S03F-semantic-layer-fixes.md` Expected output | **Verified Fact.** Every file S03 requires exists at its stated path. The S03F record exists at its stated path. |
| R14.6 Completion gate skipped or not stated | PASS | `SL/README.md` header Status and lines 210–218; `docs/02-baseline/semantic-layer-fixes.md` header Status; `playbook/STATUS.md` S03F row | **Verified Fact.** The README states the S03 and S03F results and ticks all seven 6.2 items. The S03F record states its gate and its done test output. |
| R14.7 Number invented without PROPOSED and an owner | FAIL | `docs/02-baseline/data-quality-baseline.md` line 11 (Unresolved issues) and line 214 (Lifecycle), compared with lines 12, 85, 192, and 193 of the same file | **Verified Fact.** Line 11 says "The owner of the retry bound is Unknown. The owner of the `sla_breach_risk` range is Unknown." Line 12 says "Owner: Team-Force." Lines 85, 192, and 193 also say "Owner: Team-Force." Line 214 says "The PROPOSED bounds stay proposals until an owner is named." A reader of this file gets two answers to "who owns the 1000 bound". Round 1's fix 4 named lines 12, 85, 192, and 193. It did not name lines 11 and 214. The tree itself is clean (see R12). |
| R14.8 Term or status word used with a meaning that is not in the YAML | PASS | `SL/ai-context-policy.yaml` lines 313–357; test `test_every_agency_and_pick_word_is_defined` | **Verified Fact.** Each agency word and pick word used as a value now has a YAML item with a meaning. The S03F record shows that the test fails when an access action uses the made-up agency word `observe`. |

## Test and build output

Run on 2026-10-10 from `06-telecom-service-network-incident-ops` with `.venv\Scripts\python.exe`. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
...................................                                      [100%]
35 passed in 0.93s
exit=0
```

Clean rebuild for R11. This ran in a copy of the repo under `%TEMP%\s03r2-rebuild`, so the real tree stayed as it was. The copy was deleted afterwards.

```text
> (copy) Remove-Item semantic-layer/generated; python semantic-layer/build.py
Validated 7 YAML files against semantic-layer.schema.json. Version 1.0.0.
  wrote generated/entities.json
  wrote generated/relationships.json
  wrote generated/status-taxonomy.json
  wrote generated/business-rules.json
  wrote generated/metrics.json
  wrote generated/access-semantics.json
  wrote generated/ai-context-policy.json
  wrote generated/manifest.json
exit=0

SHA-256 compare, real tree vs rebuilt:
access-semantics.json    1271DEFD2BC632D3 IDENTICAL
ai-context-policy.json   3218FD6A47491116 IDENTICAL
business-rules.json      9482A702AAC7C219 IDENTICAL
entities.json            FA305EA8E76FCA1B IDENTICAL
manifest.json            308047A6F633F6E7 IDENTICAL
metrics.json             CE001E64388A6616 IDENTICAL
relationships.json       8A030AD09B9B280F IDENTICAL
status-taxonomy.json     C533A8D13E75DC37 IDENTICAL
files original=8 rebuilt=8
```

R15 random pick:

```text
glossary id rows: 181
| `own vendor devices` | `scope.own_vendor_devices` | Only devices made by the caller's company. The `vendor` column holds status words today, so this cannot run yet. PROPOSED. |
| `tokens per invocation` | `metric.tokens_per_invocation` | How many tokens one model call used. From `token_count` in the CSV, or `token_estimate` on the live body. |
| `none` | `scope.none` | No records. Used for an action a persona may never take. |
```

## Gate result

All seven hard-block rows pass: R1, R5, R7, R8, R10, R11, R13. Every other check on the `semantic-layer/` tree also passes. Five rows that failed in round 1 now pass: R9, R12, R14.4, R14.8, and R15. The round 1 R14.7 finding is cleared inside the tree.

One row fails: R14.7. The cause is a new place, `data-quality-baseline.md` lines 11 and 214. CONDITIONAL PASS allows a FAIL only in R12 or R15. R14.7 is outside that allowance. `playbook/README.md` says a FAIL row blocks the next stage. So S04 may not start until S03F applies fix 1 and S03R runs again.

Fixes 2 and 3 clear no failed row. They bring five more texts in line with `operating-contract.md` row 10. Round 1 handled its fixes 8 and 9 the same way.

## Fixes required

Stage S03F (`playbook/S03F-semantic-layer-fixes.md`) applies these fixes and keeps version `1.0.0`. It runs `build.py` and the tests after fix 2, because fix 2 changes one YAML file. Then S03R runs again in a fresh chat. Fix 3 needs a choice.

1. **R14.7. Make the data-quality baseline name one owner for the two bounds.** In `docs/02-baseline/data-quality-baseline.md`:
   - Line 11, Unresolved issues. Replace "The owner of the retry bound is Unknown. The owner of the `sla_breach_risk` range is Unknown." with "The retry bound and the `sla_breach_risk` range are PROPOSED. Owner: Team-Force. Neither is approved." Keep the rest of the cell.
   - Line 214, Lifecycle. Replace "The PROPOSED bounds stay proposals until an owner is named." with "The PROPOSED bounds stay proposals until Team-Force approves them."
   - Lines 12, 85, 192, and 193 already say "Owner: Team-Force". No other text in this file states the owner of either bound. **Verified Fact:** search for "owner" in the file on 2026-10-10.
   - No test, id, or README count changes. This fix adds no required item.
2. **Owner decision of 2026-10-10 (`operating-contract.md` row 10, v1.1). Name Team-Force in four more places.** This fix comes from the owner decision, not from a failed row. Row 10 names "the order of the severity words" and "a legal value" as decisions Team-Force owns. The edits are:
   - `SL/status-taxonomy.yaml` line 3404, `collision.gold_bronze_as_severity` `resolution`. Replace "Open. The owner of the severity list is Unknown." with "Open. The severity list and its order are not set. Owner: Team-Force." Keep "This file records the words. It does not pick a cutoff." The value is a folded block (`>-`), so the colon needs no quotes. `SL/README.md` line 226 already gives this owner. No other text in `status-taxonomy.yaml` states an owner. Rebuild `generated/`. `status-taxonomy.json` and `manifest.json` will change.
   - `docs/02-baseline/ai-qualification.md` line 110, Open questions cell of the provisioning retry row. Replace "Who sets the legal maximum is Unknown." with "The legal maximum is not set. Owner: Team-Force." The same row already says "Owner: Team-Force" for the 1000 bound. R7 is not affected, because this cell is not an approval point.
   - `docs/02-baseline/defect-list.md` line 58, F18 Open questions cell. Replace "Who sets the legal maximum is Unknown." with "The legal maximum is not set. Owner: Team-Force." The same row already says "Owner: Team-Force".
   - `docs/02-baseline/defect-list.md` line 59, F19 Open questions cell. Replace "Who sets the legal range is Unknown." with "The legal range is not set. Owner: Team-Force." The same row already says "Owner: Team-Force".
3. **Choice needed. `docs/02-baseline/defect-list.md` line 11, Unresolved issues, "Owners are Unknown."** This line is in the same file as the fix 2 edit and states an owner, so fix 2 must cover it. The line does not say which owners it means. Options:
   - (a) It means the owner of each PROPOSED item. Replace it with "The owner of every PROPOSED item, including the bounds in F18 and F19, is Team-Force (`docs/00-contract/operating-contract.md` row 10)."
   - (b) It means who will fix each defect. Replace it with "Who fixes each defect is Unknown. The owner of the PROPOSED bounds in F18 and F19 is Team-Force."
   - (c) Leave it as it is. Record in the S03F file why it stays.

## Advisories (not FAIL, no gate effect)

- **A1, corrected from round 1.** Round 1 called `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc` untracked. It is tracked. **Verified Fact:** `git ls-files` lists it. No `.gitignore` in the repo names `__pycache__`. So the committed tree holds one file that the PDF does not list. Run `git rm --cached` on it and add `__pycache__/` to a `.gitignore` before S05R reruns R1.
- **A2, still open.** The key `ai_uses` holds eleven capabilities, and eight of them call no model. One of the eight has `agency: execute`. A literal reader can take that as an AI use with execute agency. No item carries `uses_model`. The new `pick.*` meanings now say "No model is called" on each of the three non-model picks, which helps.
- **A3, still open.** `ai_use.alarm_dedupe` and `ai_use.alarm_to_incident_correlation` set `approver: persona.noc_operator`, and their `approval_point` says "None at this agency" (`SL/ai-context-policy.yaml` lines 388–389 and 398–399).
- **A4, still open.** `jsonschema` is not in `requirements.txt`. **Verified Fact:** search on 2026-10-10. CI cannot run the tree tests until it is added.
- **A5, still open.** `docs/02-baseline/profile_data.py` and `profile-output.json` are the recorded S02 run. S03F did not change them (`git status`).
- **A6, new.** The schema allows the pick words `classical_ml` and `agentic_ai` (`SL/schemas/semantic-layer.schema.json` line 504). No item defines them. The schema also lets `agentic_ai` carry `agency: execute`, because the only pick it limits is `genai` (lines 513–514). No YAML value uses either word today. `test_every_agency_and_pick_word_is_defined` would fail if one did. At S05R, either cut the enum to the four defined picks or add the two items.
- **A7, new.** Two texts still give the S03 picture. The test module's opening comment (`SL/tests/test_semantic_layer.py` lines 6–18) lists what the tests fail on and leaves out the agency and pick check. `SL/README.md` lines 203–208 ("Done test") report "34 passed" with no stage name. That run was the S03 done test. Name it as the S03 run, or point to the S03F done test in `semantic-layer-fixes.md`.
- **A8, new.** The `metric.tokens_per_invocation` glossary row (line 195) uses "token" and does not say what it is. Row `provenance.tokens` (line 371) does. Repeating that one sentence in the metric row would let the row stand alone.

## Lifecycle

This review cites `semantic-layer/` files by path and id. Stage S03F reads the "Fixes required" list above and records round 2 in `docs/02-baseline/semantic-layer-fixes.md`. S04 waits until S03R reads PASS, or CONDITIONAL PASS with the fixes applied. Stage S05R folds in the Phase 4 and 5 open questions and runs rows R1 to R15 again. Stage S08 gives the second model the tree at the S05R version.
