# Semantic layer review

| Field | Value |
|---|---|
| Stage | S03R — Semantic layer review (Execution Plan Phase 3 review), round 3 |
| Date / version | 2026-10-10, review v3.0 of semantic layer `1.0.0`. This file replaces the round 2 review. Round 1 and round 2 fix lists stay in `docs/02-baseline/semantic-layer-fixes.md`. |
| Author | Independent reviewer (fresh Cursor chat, Grok 4.7) for Mangesh (FDE) |
| Status | PASS. No row is FAIL. The seven hard-block rows pass. `build.py --check` passes. 35 tests pass. A clean rebuild writes the same eight JSON files. S04 may start. |
| Evidence sources | `Semantic_Layer_capture.pdf`; `Project_Intent (section 6.2).md`; every file under `semantic-layer/`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/semantic-layer-fixes.md`; `docs/00-contract/operating-contract.md` row 10; `playbook/README.md` failure list; `playbook/STATUS.md`; `git status` and `git log` on 2026-10-10; runs of `build.py --check`, `pytest semantic-layer/tests`, and a clean rebuild in a temp copy on 2026-10-10 |
| Assumptions | R8 reads "AI use" as a step where a model acts. The remediation row is workflow automation. A model does not take that step. A Python byte-code file under `tests/__pycache__/` is not part of the layer. R14.7 is checked on the semantic layer, the S2Q table, and `data-quality-baseline.md`, which this stage names as inputs. |
| Unresolved issues | None that fail a row. Advisories A1 to A6 and A8 to A10 stay open. They do not change the gate. |
| Residual risks | The tests cannot see `profile-output.json`. That file still says the two bounds have owner Unknown. A reader of that file and a reader of `data-quality-baseline.md` get two owners. See advisory A5. |

Claim labels: **Verified Fact** (I ran it or read it) or **Inference**.

Paths below are relative to `06-telecom-service-network-incident-ops/` unless they start with `playbook/` or `Semantic_Layer_capture.pdf`. "SL" means `semantic-layer/`.

## Round 2 fixes still in place

S03F round 2 applied three fixes. This review checked that the text is still the text those fixes named.

| Fix | Verdict | Evidence |
|---|---|---|
| 1. One owner for the two bounds in the data-quality baseline | Still in place | **Verified Fact.** `docs/02-baseline/data-quality-baseline.md` line 11 says the retry bound and the `sla_breach_risk` range are PROPOSED, owner Team-Force, and neither is approved. Line 214 says the bounds stay proposals until Team-Force approves them. Lines 12, 85, 192, and 193 also say Owner: Team-Force. |
| 2. Team-Force on the severity list and the legal maximum | Still in place | **Verified Fact.** `SL/status-taxonomy.yaml` lines 3403–3404, `collision.gold_bronze_as_severity`, say the severity list and its order are not set, owner Team-Force. `docs/02-baseline/ai-qualification.md` line 110 says the legal maximum is not set, owner Team-Force. `docs/02-baseline/defect-list.md` lines 58 and 59 say the same for F18 and F19. |
| 3. Option B on who fixes each defect | Still in place | **Verified Fact.** `docs/02-baseline/defect-list.md` line 11 says who fixes each defect is Unknown, and that Team-Force owns the PROPOSED bounds in F18 and F19. |

The live-change approver desk job was confirmed after that round. **Verified Fact.** `docs/00-contract/operating-contract.md` row 9, version note v1.4, names the desk job `network_engineer`. The same title is in `SL/ai-context-policy.yaml` line 466, `SL/access-semantics.yaml` lines 340 and 362, `SL/business-rules.yaml` line 132, `SL/glossary.md` line 291, and `SL/README.md` lines 80 and 235. `docs/02-baseline/ai-qualification.md` line 47 says the same desk job.

## Review table

### Checks R1 to R13 and R15

| Check | Result | Citation | Reason |
|---|---|---|---|
| R1 | PASS | `Semantic_Layer_capture.pdf` page 1; `SL/README.md` lines 31–65; test `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` | **Verified Fact.** The PDF lists eleven entries: `README.md`, `glossary.md`, seven YAML files, `schemas/semantic-layer.schema.json`, and `tests/test_semantic_layer.py`. The disk holds those eleven, plus `build.py` and `generated/` (eight JSON files). README lines 61–65 say why those two were added: one script writes the JSON, and the JSON is what a service loads. The only other file is `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc`. Python wrote it. **Inference:** a byte-code cache is not part of the layer. The test skips it and passes. See advisory A1. |
| R2 | PASS | Tests `test_every_item_has_a_source_list_of_existing_paths` (test file line 401) and `test_every_proposed_item_names_an_owner` (line 414) | **Verified Fact.** I walked every YAML object that has an `id`. There are 665. Each has a `source:` list, and each path exists on disk. No object has `proposed: true` without `owner:`. Every `owner:` value is `Team-Force`. Both tests pass. |
| R3 | PASS | `docs/02-baseline/data-quality-baseline.md` lines 109–120, 194, and 204–210; `SL/status-taxonomy.yaml` `status.word.*` items; test `test_every_word_in_every_word_column_is_in_the_taxonomy` (test file line 521) | **Verified Fact.** The baseline names seven severity words (`silver`, `high`, `low`, `bronze`, `medium`, `gold`, `critical`), `legacy` in `hostname`, `requires_review` in `vendor`, and `high_risk` in `recommendation_risk`. Each word is a `status.word.*` item. The test checks every cell of every CSV status column against the taxonomy and passes. |
| R4 | PASS | `SL/status-taxonomy.yaml` lines 3387–3478 | **Verified Fact.** The `collisions` block holds exactly four entries: `collision.gold_bronze_as_severity` (line 3388), `collision.status_words_in_hostname_and_vendor` (line 3410), `collision.rec_0001_first_key_in_six_tables` (line 3445), and `collision.clinician_role_in_telecom_api` (line 3464). Test `test_collisions_block_has_the_four_named_entries` passes. Five more overlaps sit under `other_overlaps` from line 3479. |
| R5 | PASS | `SL/business-rules.yaml` lines 33, 60, 75, 87, 104, and 118 | **Verified Fact.** The six required rules are present, each with an id: `rule.missing_id_not_other_device`, `rule.ai_output_cannot_execute`, `rule.alarm_last_seen_not_before_first_seen`, `rule.shared_admin_not_least_privilege`, `rule.duplicate_dedupe_key_in_storm_is_one_alarm`, and `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. The file holds 13 rules in all. |
| R6 | PASS | `SL/access-semantics.yaml` lines 297, 336, 366, 382, 398, 424, and 441; lines 283–284 | **Verified Fact.** The seven personas are `persona.noc_operator`, `persona.network_engineer`, `persona.field_engineer`, `persona.customer_support`, `persona.automation_service`, `persona.vendor_account`, and `persona.ai_agent`. `removed_roles` lists `role.clinician`. Tests `test_required_personas_present` and `test_api_roles_today_and_clinician_removed` pass. |
| R7 | PASS | `SL/ai-context-policy.yaml` lines 78–82, 224–257, 262–307, and 362–483; `docs/02-baseline/ai-qualification.md` lines 36–48 | **Verified Fact.** `field.device.mgmt_ip` and `field.device.credential_profile` are forbidden. The four outcomes are `RECOMMEND_ONLY`, `HOLD_FOR_REVIEW`, `BLOCK`, and `EXECUTE`. `policy.fail_to_person` names the hand-off to a person, including timeout and schema failure. I compared all eleven AI uses with the S2Q table. Each has the same pick, the same agency, and the same approval point. Example: S2Q line 47 says the remediation desk job is `network_engineer`, confirmed on 2026-10-10. YAML line 466 says the same. The header assumption on S2Q line 10 is older than that row. See advisory A9. The copied row matches. |
| R8 | PASS | `SL/ai-context-policy.yaml` lines 413–466; `SL/schemas/semantic-layer.schema.json` lines 513–514; `SL/glossary.md` line 331; test `test_four_outcomes_present_and_model_never_executes` | **Verified Fact.** The three uses with pick `genai` have agency `recommend`. The schema limits a `genai` pick to agency `analyse` or `recommend`. The only use with `agency: execute` is `ai_use.remediation_execution`. Its pick is `workflow_automation`. Its executor is `persona.automation_service`. Its description says the model stops at the recommendation rows. The glossary says a model never has the execute word. **Inference:** this matches S2Q line 8, "No row gives execute agency to a model." See advisory A2. |
| R9 | PASS | `SL/glossary.md` line 328 and lines 322–377; `SL/ai-context-policy.yaml` line 316; test `test_glossary_and_yaml_agree_on_every_term` (test file line 442) | **Verified Fact.** The glossary has 181 id rows. The test checks that every id with a glossary prefix has one row, that the Term matches the YAML `name` or `word`, and that no row is empty. The test passes. The meanings I compared agree. Example: `agency.analyse` is "Read stored fields and show them. Nothing changes." in the glossary (line 328) and in the YAML (line 316). The retry-count row omits the proposed counting bound. The legal maximum is still unset in both files. See advisory A10. |
| R10 | PASS | `SL/build.py --check`; `pytest SL/tests`; test `test_schema_validates_every_yaml_file` | **Verified Fact.** The schema validated all seven YAML files. 35 of 35 tests passed. The output is pasted below. |
| R11 | PASS | Temp copy of `SL/`, then `build.py`; the eight files under `SL/generated/` | **Verified Fact.** I copied the folder to a temp directory, deleted `generated/`, and ran `build.py`. All eight rebuilt files have the same SHA-256 as the files in the real tree. The real tree was not edited. The output is pasted below. |
| R12 | PASS | `SL/metrics.yaml` lines 67–69 and 105–107; `SL/entities.yaml` lines 416 and 484–485; `SL/glossary.md` line 201; `docs/02-baseline/data-quality-baseline.md` lines 11, 85, and 192 | **Verified Fact.** Two bounds appear. The retry bound is 1000. The `sla_breach_risk` range is 0 to 1 inclusive. Each one says PROPOSED and Owner: Team-Force on the metric note, on the entity field, and in the data-quality baseline. Every metric `target:` is `null`. `timeout_seconds` is `null` (`SL/ai-context-policy.yaml` line 272). The other numbers are counts from the files, such as minimum 32 and maximum 4995 on `metric.retry_count`. |
| R13 | PASS | Test `test_no_secret_value_anywhere_in_the_tree` (test file line 600); `SL/ai-context-policy.yaml` line 89 | **Verified Fact.** The test reads secret values from `.env.example` and `legacy/reconcile_legacy.py` at run time and finds none of them in the tree. It passes. I also scanned the tree for `sk-` keys, `AKIA` keys, and `Bearer` tokens. The only `sk-` hits are the letters inside the filename `brownfield-risk-register.md`. Line 89 lists six secret names and no values. |
| R15 | PASS | `SL/glossary.md` lines 131, 138, 196, and 358 | **Verified Fact** for the pick. Python `random.sample` with seed 20261010 over the 181 glossary id rows. The three rows are below. **Inference:** a reader new to telecom can picture each one. |

### R14: failure list from `playbook/README.md`

| Check | Result | Citation | Reason |
|---|---|---|---|
| R14.1 Code before its analysis gate | PASS | `playbook/STATUS.md` rows for S2Q, S03, and S03F; `git status` on 2026-10-10 | **Verified Fact.** STATUS records S2Q as PASS before S03 wrote the layer. `git status` shows no change under `apps/`, `policy/`, `data/`, `etl/`, or `legacy/`. The only dirty path is `transcript/chat_transcript.md`. |
| R14.2 Design before the S2Q table | PASS | `docs/02-baseline/ai-qualification.md` status row; `SL/ai-context-policy.yaml` lines 360–361 | **Verified Fact.** The eleven AI uses cite `ai-qualification.md`. STATUS places that file before the semantic layer. |
| R14.3 AI picked with no stated need | PASS | `SL/ai-context-policy.yaml` lines 413–450; `docs/02-baseline/ai-qualification.md` lines 43–45 | **Verified Fact.** Three uses have pick `genai`: incident summary, next-action recommendation, and configuration suggestion. S2Q states the need for each one. Incident summary must write a new account when the case changes. Next-action and configuration suggestion must write a sentence that follows fields that differ by row. The other eight uses call no model. |
| R14.4 Claim with no label, or a Verified Fact with no pointer | PASS | `SL/glossary.md` line 18; `SL/README.md` line 243; `SL/ai-context-policy.yaml` line 473 | **Verified Fact.** Glossary line 18 says status-word meanings are Inference, because the repo defines none of them, and that other meanings are a Verified Fact from the named files. The desk-job confirmation in the YAML cites `docs/00-contract/operating-contract.md`. The README "Last build" block marks that run as a Verified Fact. |
| R14.5 Artifact missing or at the wrong path | PASS | `SL/` tree; `docs/02-baseline/semantic-layer-fixes.md`; `playbook/S03-semantic-layer.md` Expected output | **Verified Fact.** Every file S03 requires is at the path the capture PDF and the S03 prompt name. The S03F record is at its stated path. |
| R14.6 Completion gate skipped or not stated | PASS | `SL/README.md` lines 6 and 212–220; `docs/02-baseline/semantic-layer-fixes.md` header Status; `playbook/STATUS.md` S03 and S03F rows | **Verified Fact.** The README states S03 PASS, states that S03F round 2 applied its fixes, and ticks all seven items from `Project_Intent.md` 6.2. The S03F record states its gate. |
| R14.7 Number invented without PROPOSED and an owner | PASS | `docs/02-baseline/data-quality-baseline.md` lines 11, 85, 192, and 214; `SL/metrics.yaml` lines 69 and 107; `docs/02-baseline/defect-list.md` lines 58–59; `docs/02-baseline/ai-qualification.md` line 110 | **Verified Fact.** The retry bound of 1000 and the `sla_breach_risk` range of 0 to 1 are PROPOSED with owner Team-Force in the baseline, in the S2Q findings row, in the defect list, and in the YAML. Line 214 says Team-Force must approve them. The round 2 contradiction (owner Unknown on lines 11 and 214) is gone. `profile-output.json` still says Owner: Unknown. That file is the S02 run record and is outside this stage's named inputs. See advisory A5. |
| R14.8 Term or status word used with a meaning that is not in the YAML | PASS | `SL/ai-context-policy.yaml` lines 313–357; `SL/glossary.md` lines 322–342; test `test_every_agency_and_pick_word_is_defined` | **Verified Fact.** Each agency word and each pick word used as a value has a YAML item and a glossary row. The test passes. `network_engineer` is `persona.network_engineer`. |

## R15 plain speech

Seed `20261010`. Population: 181 glossary id rows.

| Term | Id | Line | Can a new reader picture it? |
|---|---|---|---|
| `cost per correlated incident` | `metric.cost_per_correlated_incident` | 196 | Yes. The row says to add up the cost of the model calls for one incident, that the price is unknown, and that the alarms are not tied to the incident yet. |
| `east-4` | `status.word.east_4` | 138 | Yes. The sentence above the table (line 131) says a network zone is a named part of the network that a device belongs to. The row says `east-4` is one of those names, and it is the one on the most devices: 70 rows. The picture is that name on 70 device rows. Line 131 also says the repo does not describe whether the name follows a place or a function. |
| `capacity forecast` | `ai_use.capacity_forecast` | 358 | Yes. The row says to show the stored bandwidth numbers for circuits and orders, and that nothing is forecast because no file holds a history of use. Bandwidth here is the size number already stored on the connection. |

## Test and build output

Run on 2026-10-10 from `06-telecom-service-network-incident-ops` with `.venv\Scripts\python.exe`. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
...................................                                      [100%]
35 passed in 1.11s
exit=0
```

Clean rebuild for R11. This ran in a copy of `semantic-layer/` under `%TEMP%\s03r3-rebuild`. The real tree was not edited. The copy was deleted afterwards.

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
```

SHA-256 compare, real tree vs rebuilt. First 16 hex characters. All eight match.

```text
access-semantics.json    7F1A0A85248D0CF1 IDENTICAL
ai-context-policy.json   0DB345F01DC563D8 IDENTICAL
business-rules.json      8AB302F735D28B4E IDENTICAL
entities.json            FA305EA8E76FCA1B IDENTICAL
manifest.json            C9FDFFB026D6233C IDENTICAL
metrics.json             CE001E64388A6616 IDENTICAL
relationships.json       8A030AD09B9B280F IDENTICAL
status-taxonomy.json     911ADFDA57B5C723 IDENTICAL
files original=8 rebuilt=8 mismatches=0
```

## Gate result

No row is FAIL. The seven hard-block rows pass: R1, R5, R7, R8, R10, R11, and R13. R12 and R15 pass. R14.1 through R14.8 pass. The round 2 failure, R14.7, is cleared in the files this stage reviews.

S04 may start. S03F does not run on this review.

## Fixes required

None. No row is FAIL. There is no choice for an owner to make.

## Advisories (not FAIL, no gate effect)

- **A1.** `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc` is on disk. The capture PDF does not list it. The tree test skips `__pycache__`. It is a Python cache file.
- **A2.** The key `ai_uses` holds eleven capabilities. Eight call no model. One of those eight, `ai_use.remediation_execution`, has `agency: execute`. A reader who treats every entry under that key as a model step can misread it. The pick is `workflow_automation`, and the glossary says a model never has that agency word.
- **A3.** `ai_use.alarm_dedupe` and `ai_use.alarm_to_incident_correlation` set `approver: persona.noc_operator`, and their `approval_point` says "None at this agency" (`SL/ai-context-policy.yaml` lines 388–389 and 398–399). The S2Q sentences do the same: no approval at this agency, and the `noc_operator` makes a later decision. The YAML copies that.
- **A4.** `jsonschema` is not in `requirements.txt`. **Verified Fact:** `SL/README.md` lines 92–93. A new machine that installs only that file cannot run the schema tests until `jsonschema` is installed.
- **A5.** `docs/02-baseline/profile_data.py` lines 18 and 24, and `docs/02-baseline/profile-output.json` lines 851 and 875, still say `Owner: Unknown` on the retry bound of 1000 and the `sla_breach_risk` range of 0 to 1. Those files are the recorded S02 profile run. They are not in this stage's named inputs. `data-quality-baseline.md` now says Owner: Team-Force. A reader of both files sees two owners.
- **A6.** The schema allows the pick words `classical_ml` and `agentic_ai` (`SL/schemas/semantic-layer.schema.json` line 504). No YAML item defines them. The schema also lets a pick other than `genai` carry `agency: execute` (lines 513–514). No YAML value uses those two pick words today. The test `test_every_agency_and_pick_word_is_defined` fails if one appears without a matching item.
- **A8.** The glossary row `metric.tokens_per_invocation` (line 195) uses the word "token" and does not say what a token is. Row `provenance.tokens` (line 371) does: a token is a small piece of text that a model counts and charges by.
- **A9.** `docs/02-baseline/ai-qualification.md` line 10 still says the desk job on a human approval line is PROPOSED until stage S04-09. Line 47 says the remediation desk job is `network_engineer`, confirmed on 2026-10-10. The YAML copied line 47. The other human-approval desk jobs in that table are still PROPOSED.
- **A10.** `SL/glossary.md` line 198, `metric.retry_count`, says the maximum is Unknown. `SL/metrics.yaml` lines 67–69 also record a PROPOSED counting bound of 1000 with owner Team-Force, and say it is not an approved maximum. The legal maximum is unset in both places. The glossary row does not mention the counting bound.

A7 from round 2 is closed. **Verified Fact.** The test file's opening comment now lists the agency and pick check (lines 11–12). `SL/README.md` line 207 names the "34 passed" run as the S03 done test.

## Lifecycle

This review cites `semantic-layer/` files by path and id. No row is FAIL, so stage S03F does not run. Stage S04 may start. A Phase 4 or Phase 5 design that needs a term this tree lacks writes one line that starts with "Open question for S03:". Stage S05R folds those lines into the tree, raises the version, and runs rows R1 to R15 again. Stage S08 gives the second model the tree at the S05R version.
