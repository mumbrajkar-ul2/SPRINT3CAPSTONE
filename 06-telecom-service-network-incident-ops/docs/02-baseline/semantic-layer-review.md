# Semantic layer review

| Field | Value |
|---|---|
| Stage | S03R — Semantic layer review (Execution Plan Phase 3 review) |
| Date / version | 2026-10-10, review v1.0 of semantic layer `1.0.0` |
| Author | Independent reviewer (fresh Cursor chat, Claude Opus 5.5) for Mangesh (FDE) |
| Status | BLOCKED for S04. Every hard-block row (R1, R5, R7, R8, R10, R11, R13) passes. Rows R9, R12, R14.4, R14.7, R14.8, and R15 fail. R9 and three R14 rows fall outside the CONDITIONAL PASS allowance, so S04 may not start. Each failure has a short fix below. |
| Evidence sources | `Semantic_Layer_capture.pdf`; `Project_Intent.md` 6.2 and Appendix E; every file under `semantic-layer/`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/data-quality-baseline.md`; `playbook/README.md` failure list; `playbook/S03-semantic-layer.md`; `playbook/STATUS.md`; runs of `build.py --check`, `pytest semantic-layer/tests`, and a clean rebuild in a temp copy on 2026-10-10 |
| Assumptions | R8 reads "AI use" as "a step where a model acts". The one `agency: execute` item is workflow automation with no model. R14.7 treats a number marked "Owner Unknown" as a number with no owner. |
| Unresolved issues | The completion gate names no status for a FAIL in R9 or R14 alone. This review calls it BLOCKED because `playbook/README.md` says a FAIL row blocks the next stage. The S02 baseline also gives the two bounds "Owner: Unknown". On 2026-10-10 the owner decided that Team-Force owns every PROPOSED item (`docs/00-contract/operating-contract.md` row 10). Team-Force is the FDE team Mangesh belongs to. Fixes 4, 8, and 9 apply that decision. |
| Residual risks | The tests did not catch the R9 gap. The glossary test covers 15 id prefixes. It skips `ai_use.` and `provenance.`, and no test checks the agency or pick words. A second model given this tree must guess what "analyse" and "deterministic_code" mean. |

Claim labels: **Verified Fact** (I ran it or read it), **Inference**.

Paths below are relative to `06-telecom-service-network-incident-ops/`. "SL" means `semantic-layer/`.

## Review table

### Checks R1 to R13 and R15

| Check | Result | Citation | Reason |
|---|---|---|---|
| R1 | PASS | `SL/README.md` lines 31–63; `Semantic_Layer_capture.pdf` page 1; test `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` | **Verified Fact.** The disk holds the eleven entries in the PDF, plus `build.py` and `generated/` (8 files), and README lines 61–63 say why those two were added. The only other item on disk is one untracked cache file, `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc`. Python wrote it when the tests ran. See advisory A1. |
| R2 | PASS | Tests `test_every_item_has_a_source_list_of_existing_paths` (test file line 380) and `test_every_proposed_item_names_an_owner` (line 393) | **Verified Fact.** All 657 items with an id carry a `source:` list of paths that exist. All 28 `proposed: true` items carry `owner: Mangesh (FDE)`. Sub-items with no id, such as persona grants, sit under a parent that has both. |
| R3 | PASS | `docs/02-baseline/data-quality-baseline.md` lines 199–210; `SL/status-taxonomy.yaml`; test `test_every_word_in_every_word_column_is_in_the_taxonomy` (line 500) | **Verified Fact.** The baseline names the seven severity words, `legacy` in `hostname`, and `requires_review` in `vendor`. All of them are defined as `status.word.*` items. The test checks every cell of every CSV status column against the taxonomy and passes. |
| R4 | PASS | `SL/status-taxonomy.yaml` lines 3387–3478: `collision.gold_bronze_as_severity`, `collision.status_words_in_hostname_and_vendor`, `collision.rec_0001_first_key_in_six_tables`, `collision.clinician_role_in_telecom_api` | **Verified Fact.** The `collisions` block holds exactly the four named entries. Each one lists its words or fields, a defect id, and its sources. |
| R5 | PASS | `SL/business-rules.yaml` lines 34, 60, 76, 87, 104, 118 | **Verified Fact.** These six required rules are present, each with an id. `rule.missing_id_not_other_device`. `rule.ai_output_cannot_execute`. `rule.alarm_last_seen_not_before_first_seen`. `rule.shared_admin_not_least_privilege`. `rule.duplicate_dedupe_key_in_storm_is_one_alarm`. `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. Seven more rules bring the total to 13. |
| R6 | PASS | `SL/access-semantics.yaml` lines 297–468 (seven `persona.*` items); lines 283–290 (`removed_roles`, `role: role.clinician`) | **Verified Fact.** All seven personas have grants built from the five value lists (actions, resources, purposes, scopes, risks). `clinician` is under `removed_roles` with the reason and defect F03. |
| R7 | PASS | `SL/ai-context-policy.yaml` lines 78–82 (forbidden), 225–257 (`policy.outcomes`), 262–307 (`policy.fail_to_person`), 313–434 (`ai_uses`); `docs/02-baseline/ai-qualification.md` lines 36–48 | **Verified Fact.** `mgmt_ip` and `credential_profile` are forbidden, and the four outcomes and fail-to-person are present. I compared all eleven uses against S2Q. Each has the same pick, agency, outcome, and approval-point wording. One sentence is dropped on `ai_use.alarm_dedupe`, and the meaning does not change. See advisory A3 about the `approver` field. |
| R8 | PASS | `SL/ai-context-policy.yaml` lines 411–424 (`ai_use.remediation_execution`); schema `SL/schemas/semantic-layer.schema.json` lines 491–492; test `test_four_outcomes_present_and_model_never_executes` | **Verified Fact.** The only item with `agency: execute` is remediation execution. Its pick is `workflow_automation` and its executor is `persona.automation_service`, so no model runs that step. The schema rejects a `genai` pick with any agency other than analyse or recommend. **Inference:** this matches S2Q, which says "No row gives execute agency to a model". See advisory A2. |
| R9 | FAIL | `SL/glossary.md` line 261; `SL/ai-context-policy.yaml` lines 313–434 (`agency:`, `pick:`), 160–219 (`provenance.*`); schema lines 460, 482–483; test file line 58 (`GLOSSARY_PREFIXES`) | **Verified Fact.** The YAML uses words the glossary never defines. The four agency words (analyse, recommend, decide, execute) appear only as a list on glossary line 261. The four pick words (rules, deterministic_code, workflow_automation, genai) have no row. The eleven `ai_use.*` ids and the nine `provenance.*` fields have no rows. `mgmt_ip` and `credential_profile` are named in many rows, and no row says what they are. The meanings that do exist agree with the YAML, because the test checks that. |
| R10 | PASS | `SL/build.py --check`; `pytest SL/tests`; test `test_schema_validates_every_yaml_file` | **Verified Fact.** The schema validated all seven YAML files, and 34 of 34 tests passed. The output is pasted below. |
| R11 | PASS | `SL/build.py`; `SL/generated/` (8 files) | **Verified Fact.** I copied the tree to a temp folder, deleted `generated/`, and ran `build.py`. All 8 rebuilt files have the same SHA-256 as the originals. The output is pasted below. The real tree was not touched. |
| R12 | FAIL | `SL/metrics.yaml` lines 69 and 107; `SL/entities.yaml` lines 416 and 485; `SL/glossary.md` line 199 | **Verified Fact.** Two numbers carry PROPOSED but give "Owner Unknown". One is the retry bound of 1000. The other is the `sla_breach_risk` range of 0 to 1. Both came from `data-quality-baseline.md` lines 84 and 192, which also say "Owner: Unknown". The rule asks for PROPOSED and a named owner. Every `target:` is `null`, and `timeout_seconds` is `null`. |
| R13 | PASS | Test `test_no_secret_value_anywhere_in_the_tree` (test file line 579); `SL/ai-context-policy.yaml` line 89 | **Verified Fact.** The test reads the secret values from `.env.example` and `legacy/reconcile_legacy.py` and finds none of them in the tree. I also ran a pattern scan for password, token, and key assignments, for `sk-`, `AKIA`, and `Bearer` strings, and for passwords inside URLs. It found nothing. Line 89 lists six secret names and no values. |
| R15 | FAIL | `SL/glossary.md` rows `metric.cost_per_correlated_incident` (line 193), `status.word.east_4` (line 136), `concept.guardrail` (line 43) | **Verified Fact** for the pick: Python `random.sample` with seed 20261010 over the 153 glossary rows. `guardrail` is clear: "a check that runs around a model call and can stop the result." `east-4` fails. "A network zone name on devices" does not say what a network zone is, and no row explains it. `cost per correlated incident` fails. "What the model calls for one incident cost" reads like "what the model asks for", and "correlated" is never explained. **Inference:** a new reader can picture one of the three. |

### R14: failure list from `playbook/README.md`

| Check | Result | Citation | Reason |
|---|---|---|---|
| R14.1 Code before its analysis gate | PASS | `playbook/STATUS.md` S2Q row; `git status` on `apps/`, `policy/`, `data/`, `etl/`, `legacy/` | **Verified Fact.** The only new code is `SL/build.py` and `SL/tests/test_semantic_layer.py`. S03 asks for both. S2Q passed before S03. `git status` shows no change under the app, policy, data, ETL, or legacy folders. |
| R14.2 Design before the S2Q table | PASS | `docs/02-baseline/ai-qualification.md` status row; `SL/README.md` line 147 | **Verified Fact.** The AI policy takes its eleven rows from S2Q. The README harvest table cites S2Q as the source of the picks. |
| R14.3 AI picked with no stated need | PASS | `SL/ai-context-policy.yaml` lines 364–400; `ai-qualification.md` lines 41–43 and 67–84 | **Verified Fact.** Three uses are `genai`: incident summary, next-action recommendation, and configuration suggestion. S2Q states the need for each one: writing new text, or reasoning over varied inputs. The other eight uses do not call a model. |
| R14.4 Claim with no label, or a Verified Fact with no pointer | FAIL | `SL/glossary.md` line 18 compared with line 11; rows on lines 80–87, 95–107, 112–113, 146–149 | **Verified Fact.** Line 18 says each meaning is a Verified Fact from the named files unless the row says otherwise. Line 11 says the repo defines none of the 44 status words. So rows such as `new` ("The row was created. Nothing has happened to it yet.") and `debug` ("The lowest log level.") are labelled Verified Fact with no source. They are Inference. |
| R14.5 Artifact missing or at the wrong path | PASS | `SL/` tree; `playbook/S03-semantic-layer.md` Expected output | **Verified Fact.** Every file S03 requires exists at its stated path. |
| R14.6 Completion gate skipped or not stated | PASS | `SL/README.md` header Status and lines 206–214; `playbook/STATUS.md` S03 row | **Verified Fact.** The README states the S03 gate result, ticks all seven 6.2 items with evidence, and records the done test. |
| R14.7 Number invented without PROPOSED and an owner | FAIL | Same lines as R12 | **Verified Fact.** This is the same finding as R12. The 1000 retry bound and the 0-to-1 range are marked PROPOSED, but "Owner Unknown" names no owner. |
| R14.8 Term or status word used with a meaning that is not in the YAML | FAIL | `SL/ai-context-policy.yaml` `agency:` and `pick:` keys; `SL/access-semantics.yaml` `actions[].agency`; schema lines 460, 482–483 | **Verified Fact.** The YAML uses the four agency words and the four pick words as values in 32 places. The schema fixes the allowed set of words. No YAML item says what any of the words means. The meanings live only in `ai-qualification.md` lines 18–20. |

## Test and build output

Run on 2026-10-10 from `06-telecom-service-network-incident-ops` with `.venv\Scripts\python.exe`. **Verified Fact.**

```text
> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
..................................                                       [100%]
34 passed in 1.08s
exit=0
```

Clean rebuild for R11. This ran in a copy under `%TEMP%\s03r-rebuild`, so the real tree stayed as it was.

```text
> (copy) Remove-Item generated/; python build.py
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

SHA-256 compare, original vs rebuilt:
access-semantics.json    9D03460EA3A3F286 IDENTICAL
ai-context-policy.json   17A0F7B4AD519B89 IDENTICAL
business-rules.json      7B8EFD456CBCDBEF IDENTICAL
entities.json            5CFDBE82BE5C6A07 IDENTICAL
manifest.json            39522E135EF3B58F IDENTICAL
metrics.json             ABF7797A48F051A6 IDENTICAL
relationships.json       8A030AD09B9B280F IDENTICAL
status-taxonomy.json     C533A8D13E75DC37 IDENTICAL
files original=8 rebuilt=8
```

R15 random pick:

```text
glossary id rows: 153
| `cost per correlated incident` | `metric.cost_per_correlated_incident` | What the model calls for one incident cost. ... |
| `east-4` | `status.word.east_4` | A network zone name on devices. The largest zone, 70 rows. |
| `guardrail` | `concept.guardrail` | A check that runs around a model call and can stop the result. ... |
```

## Gate result

All seven hard-block rows pass: R1, R5, R7, R8, R10, R11, R13. So the tree is sound as a structure. It validates, it rebuilds byte for byte, it holds no secret, and it never gives a model execute agency.

Six rows fail: R9, R12, R14.4, R14.7, R14.8, R15. CONDITIONAL PASS allows a FAIL only in R12 or R15. R9, R14.4, and R14.8 are outside that allowance, so this review does not reach CONDITIONAL PASS. R14.7 is the same finding as R12. `playbook/README.md` says a FAIL row blocks the next stage. So S04 may not start until S03F applies these fixes and S03R is run again.

## Fixes required

Stage S03F (`playbook/S03F-semantic-layer-fixes.md`) applies these fixes and keeps version `1.0.0`. It also runs `build.py` and the tests. Then S03R runs again in a fresh chat. No fix needs a choice now. Fix 4 was decided on 2026-10-10. Fixes 8 and 9 were added the same day, after the owner decisions.

1. **R9 and R14.8. Define the agency and pick words in the YAML.** Add a value list to `ai-context-policy.yaml` with ids. The ids are `agency.analyse`, `agency.recommend`, `agency.decide`, `agency.execute`, `pick.rules`, `pick.deterministic_code`, `pick.workflow_automation`, and `pick.genai`. Take each meaning from `ai-qualification.md` lines 18–20. Add `agency.` and `pick.` to the schema and to `ID_PREFIXES`.
2. **R9. Fill the glossary gaps.** Add glossary rows for those eight words, the eleven `ai_use.*` ids, and the nine `provenance.*` fields. Add `agency.`, `pick.`, `ai_use.`, and `provenance.` to `GLOSSARY_PREFIXES` in the test file (line 58), so the test fails if a row goes missing.
3. **R9. Say what the two sensitive fields are.** Add one sentence to the `resource.sensitive_device_fields` glossary row (line 229). `mgmt_ip` is the column meant to hold the address used to log in to and manage a device. `credential_profile` names the login details the device uses.
4. **R12 and R14.7. Give the two bounds an owner.** Decided on 2026-10-10: the owner is Team-Force, the business owner in `docs/00-contract/operating-contract.md` row 10. Replace "Owner Unknown" or "Owner: Unknown" with "Owner: Team-Force" for the retry bound of 1000 and the `sla_breach_risk` range of 0 to 1. The numbers stay PROPOSED. The places are:
   - in the semantic layer: `metrics.yaml` lines 9, 69, and 107; `entities.yaml` lines 416 and 485; `glossary.md` line 199; `README.md` lines 124, 225, and 226
   - in the baseline docs: `data-quality-baseline.md` lines 12, 85, 192, and 193; `defect-list.md` rows F18 and F19 (lines 58 and 59); `ai-qualification.md` lines 39, 54, and 110
5. **R14.4. Fix the blanket evidence label.** Change `glossary.md` line 18 to say "Status-word meanings are Inference, because the repo defines none of them. Other meanings are a Verified Fact from the named files unless the row says otherwise."
6. **R15. Explain network zones.** Add one sentence above the network zone table (line 130): "A network zone is a named part of the network that a device belongs to. The repo does not say whether zones follow place or function."
7. **R15. Rewrite the cost row.** Change `metric.cost_per_correlated_incident` (line 193) to "The total cost of the model calls made for one incident. This works only after the alarms are tied to that incident. The repo does not say how to tie them, and the price is Unknown."
8. **Owner decision of 2026-10-10. Name the owner of the other open business decisions.** This fix comes from the owner decision, not from a failed row. In `SL/README.md` lines 222, 224, and 233, replace "owner Unknown" with "owner Team-Force". Those rows are the severity word order, the storm size, and which order built which circuit. Keep the stage named in each row.
9. **Owner decision of 2026-10-10. Make Team-Force the owner of the design proposals.** This fix comes from the owner decision, not from a failed row. Team-Force is the FDE team Mangesh belongs to (`docs/00-contract/operating-contract.md` row 10). The edits are:
   - Change every `owner: Mangesh (FDE)` key to `owner: Team-Force`. There are 28 keys: 19 in `access-semantics.yaml`, 7 in `ai-context-policy.yaml`, and 2 in `metrics.yaml`.
   - Change "Owner Mangesh (FDE)" and "owner Mangesh (FDE)" in YAML text to Team-Force. The places are `ai-context-policy.yaml` (`hand_to_label` and the `approval_point` text of the four GenAI and remediation rows), `metrics.yaml` line 83, `business-rules.yaml` line 132, and `SL/README.md` line 10.
   - Change "Owner: Mangesh (FDE)" to "Owner: Team-Force" in `ai-qualification.md` lines 43, 44, 45, 47, 70, 76, 84, and 118. The `approval_point` text in `ai-context-policy.yaml` is copied from those lines, so both files must change together. R7 then still finds the same meaning.
   - Leave every "Author: Mangesh (FDE)" line as it is. Mangesh wrote the files.

## Advisories (not FAIL, no gate effect)

- **A1.** `SL/tests/__pycache__/` holds an untracked `.pyc` file. Add `__pycache__/` to `.gitignore` before the tree is committed, or the committed tree will not match the PDF.
- **A2.** The key `ai_uses` holds eleven capabilities, and eight of them call no model. One of the eight has `agency: execute`. A literal reader can take that as "an AI use with execute agency". Add `uses_model: false` to the eight non-model rows, or rename the key to `capabilities`.
- **A3.** `ai_use.alarm_dedupe` and `ai_use.alarm_to_incident_correlation` set `approver: persona.noc_operator`. Their `approval_point` says "None at this agency". A reader can take the field to mean an approval is needed. Rename the field to `next_decision_by` on rows that need no approval, or set it to `null`.
- **A4.** `jsonschema` is in `.venv` only. `requirements.txt` does not list it. The README already records this. CI will fail to run the tests until it is added.
- **A5.** `docs/02-baseline/profile_data.py` and `profile-output.json` still print "Owner: Unknown" for the two bounds. They are the recorded S02 run, so fix 4 leaves them as they are. The next S02 rerun can change the script text.

## Lifecycle

This review cites `semantic-layer/` files by path and id. Stage S03F reads the "Fixes required" list above. S04 waits until S03R reads PASS, or CONDITIONAL PASS with the fixes applied. Stage S05R folds in the Phase 4 and 5 open questions and runs rows R1 to R15 again. Stage S08 gives the second model the tree at the S05R version.
