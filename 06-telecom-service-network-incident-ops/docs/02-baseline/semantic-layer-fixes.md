# Semantic layer fixes

| Field | Value |
|---|---|
| Stage | S03F — Semantic layer fixes (applies the S03R "Fixes required" list) |
| Date / version | 2026-10-10, round 2. Semantic layer version `1.0.0`, unchanged. Round 1 stays in the section below. |
| Author | Mangesh (FDE), drafted with Cursor. Round 1 used Claude Opus 5.5. Round 2 used Grok 4.7. |
| Status | PASS for round 2. Fixes 1 to 3 and advisory A7 are applied. `build.py`, `build.py --check`, and the 35 tests pass after a clean rebuild. The done test failed and then passed as expected. Every changed file inside the packet is named by a fix, by A7, or by steps 6 and 7. S03R runs again next, in a fresh chat. S04 waits for that review. |
| Evidence sources | `docs/02-baseline/semantic-layer-review.md` (review v2.0, the fix source for round 2); every file under `semantic-layer/`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/00-contract/operating-contract.md` row 10; `playbook/S03-semantic-layer.md`; `playbook/S03F-semantic-layer-fixes.md`; `git diff` and `git status` on 2026-10-10 |
| Assumptions | Round 1's list-shape choice is recorded in the Round 1 section. For advisory A7, this round names the README "Done test" block as the S03 run. The advisory also allows a pointer to this file instead. The Decisions block said to apply A7 and did not pick between those two phrasings. |
| Unresolved issues | Advisories A1, A2, A3, A4, A5, A6, and A8 stay as the review wrote them. The Decisions block applied A7 only. The schema still allows the pick words `classical_ml` and `agentic_ai`, and no item defines them. No AI use has either pick. |
| Residual risks | Naming Team-Force as owner does not approve any number. The retry bound of 1000 and the `sla_breach_risk` range of 0 to 1 stay PROPOSED. Fix 3 option B leaves who will fix each defect as Unknown. The tree tests still cannot see the baseline docs. |

Claim labels: **Verified Fact** (I ran it or read it, with a pointer), **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`. "SL" means `semantic-layer/`.

## Round 1, 2026-10-10

### Fix source

| Item | Value |
|---|---|
| Path | `docs/02-baseline/semantic-layer-review.md` |
| Why this file | `docs/02-baseline/semantic-layer-revision.md` does not exist. **Verified Fact:** `Test-Path` returned False. The review is the only fix source. |
| Header date and version | 2026-10-10, review v1.0 of semantic layer `1.0.0` |
| Stage status | BLOCKED for S04. Rows R9, R12, R14.4, R14.7, R14.8, and R15 fail. |
| Version check | `SL/README.md` states version `1.0.0`. `docs/prd/prd.md` does not exist. **Verified Fact:** `Test-Path` returned False. No later stage cites the version, so this stage may run. |

### Fixes required, copied word for word from the review

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

### Decisions block, as pasted

```text
None
```

### Decision per fix

| Fix | Decision | Reason |
|---|---|---|
| 1 | apply | The fix names the ids, the file, and the source lines. It offers no options. |
| 2 | apply | The fix names every row to add and the test constant to change. |
| 3 | apply | The fix gives the sentence. |
| 4 | apply | The fix names the owner, Team-Force (PROPOSED, Owner: Team-Force, per `operating-contract.md` row 10), and every line. Naming the owner does not approve the 1000 bound or the 0-to-1 range. Both stay PROPOSED. |
| 5 | apply | The fix gives the sentence. |
| 6 | apply | The fix gives the sentence. |
| 7 | apply | The fix gives the sentence. |
| 8 | apply | The fix names the three README rows. |
| 9 | apply | The fix names every key and every text place. |

No fix is waiting for a decision. No fix is marked cannot apply.

### Edit list

Line numbers are the line in the file before the edit. Where an edit added lines, the new line range is also given. **Verified Fact:** `git diff -U0` on 2026-10-10.

#### Fix 1

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/ai-context-policy.yaml` | new lines 309–358, ids `agency.analyse`, `agency.recommend`, `agency.decide`, `agency.execute` | (none) | New top-level list `agency_levels`. Each item has `id`, `name`, `description`, and `source`. Meanings: analyse "Read stored fields and show them. Nothing changes." recommend "Show text a person can accept or reject. Nothing changes until that person acts." decide "Choose the outcome. For example, set a stored status or record an approval." execute "Carry out a change on a live device or circuit." Source: `docs/02-baseline/ai-qualification.md`, `../Project_Intent.md`, and for analyse and decide also `semantic-layer/access-semantics.yaml` (the `risk.read_only` and `risk.decision` wording). |
| `SL/ai-context-policy.yaml` | same block, ids `pick.rules`, `pick.deterministic_code`, `pick.workflow_automation`, `pick.genai` | (none) | New top-level list `picks`. Each item has `id`, `name`, `description`, and `source: [docs/02-baseline/ai-qualification.md]`. Each of the three no-model picks says "The same stored input always gives the same result. No model is called." and gives one example from the eleven AI uses. `genai`: "A language model writes new text from a prompt." |
| `SL/schemas/semantic-layer.schema.json` | new lines 476–497, defs `agency_level` and `pick_word` | (none) | Two item shapes. Each builds on `named_item`. The id must match `^agency\.(analyse|recommend|decide|execute)$` or `^pick\.(rules|deterministic_code|workflow_automation|genai)$`. The name must be one of the matching four words. |
| `SL/schemas/semantic-layer.schema.json` | line 500 (now 522), `ai_context_policy_file.required` | `[..., "fail_to_person", "ai_uses"]` | `[..., "fail_to_person", "agency_levels", "picks", "ai_uses"]` |
| `SL/schemas/semantic-layer.schema.json` | after line 589 (now 612–613), `ai_context_policy_file.properties` | (none) | `agency_levels` and `picks`, each an array of exactly 4 items of the new shape. |
| `SL/tests/test_semantic_layer.py` | line 55, `ID_PREFIXES` | `"provenance.", "ai_use.", "failmode.",` | `"provenance.", "ai_use.", "failmode.", "agency.", "pick.",` |
| `SL/tests/test_semantic_layer.py` | new lines 278–296, test `test_every_agency_and_pick_word_is_defined` | (none) | New test. It fails when an `agency` or `pick` value anywhere in the seven YAML files has no matching item in `agency_levels` or `picks`, or when the ids do not match the names. S03 asks for a test on each required item. |
| `SL/README.md` | after line 116 (now 118–119), id conventions table | (none) | Two rows: `agency.` and `pick.`, defined in `ai-context-policy.yaml`. |
| `SL/README.md` | line 86 (now 87), line 179 (now 182), after line 185 (now 189) | "run the 34 tests"; "has 34 tests" | "run the 35 tests"; "has 35 tests"; new bullet "an `agency` or `pick` value anywhere in the YAML has no matching `agency.*` or `pick.*` item". These keep the README true after the new test. |

#### Fix 2

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/glossary.md` | new lines 322–377, section "Agency words" | (none) | Four rows: `agency.analyse`, `agency.recommend`, `agency.decide`, `agency.execute`. |
| `SL/glossary.md` | same block, section "Pick words" | (none) | Four rows: `pick.rules`, `pick.deterministic_code`, `pick.workflow_automation`, `pick.genai`. |
| `SL/glossary.md` | same block, section "AI uses" | (none) | Eleven rows, one per `ai_use.*` id. Each names the pick and the agency. |
| `SL/glossary.md` | same block, section "Provenance fields" | (none) | Nine rows, one per `provenance.*` id. |
| `SL/tests/test_semantic_layer.py` | line 60 (now 60–61), `GLOSSARY_PREFIXES` | `"purpose.", "scope.", "risk.", "role.", "failmode.", "collision.",` | `"purpose.", "scope.", "risk.", "role.", "failmode.", "collision.", "agency.", "pick.", "ai_use.",` then `"provenance.",` |
| `SL/README.md` | line 209 (now 213), checklist | "153 rows. One row per entity, ... outcome, and fail mode." | "181 rows. One row per entity, ... outcome, fail mode, agency word, pick word, AI use, and provenance field." **Verified Fact:** `glossary_rows()` returns 181. |

#### Fix 3

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/glossary.md` | line 229 (now 231), `resource.sensitive_device_fields` | "`mgmt_ip` and `credential_profile`. Which personas may read them is Unknown. ..." | "`mgmt_ip` and `credential_profile`. `mgmt_ip` is the column meant to hold the address used to log in to and manage a device. `credential_profile` names the login details the device uses. Which personas may read them is Unknown. ..." |

#### Fix 4

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/metrics.yaml` | line 9, file `description` | "recorded as a note with owner Unknown." | "recorded as a note with Owner: Team-Force." |
| `SL/metrics.yaml` | line 69, `metric.retry_count` `proposed_bound_note` | `proposed_bound_note: The baseline uses 1000 ... Owner Unknown. It is not ...` | `proposed_bound_note: "The baseline uses 1000 ... Owner: Team-Force. It is not ..."` |
| `SL/metrics.yaml` | line 107, `metric.sla_breach_risk` `proposed_bound_note` | `proposed_bound_note: The baseline uses 0 to 1 ... Owner Unknown. It is not ...` | `proposed_bound_note: "The baseline uses 0 to 1 ... Owner: Team-Force. It is not ..."` |
| `SL/entities.yaml` | line 416, `field.incident.sla_breach_risk` | "The legal range is PROPOSED 0 to 1. Owner Unknown." | "The legal range is PROPOSED 0 to 1. Owner: Team-Force." |
| `SL/entities.yaml` | line 485, `field.service_order.retry_count` | "The 1000 bound in the baseline is PROPOSED with owner Unknown." | "The 1000 bound in the baseline is PROPOSED. Owner: Team-Force." |
| `SL/glossary.md` | line 199 (now 201), `metric.sla_breach_risk` | "The range is PROPOSED, owner Unknown." | "The range is PROPOSED. Owner: Team-Force." |
| `SL/README.md` | line 124 (now 127) | "the YAML records it as a note with owner Unknown." | "the YAML records it as a note with Owner: Team-Force." |
| `SL/README.md` | lines 225 and 226 (now 229 and 230) | "Owner Unknown" (twice) | "Owner: Team-Force" (twice) |
| `docs/02-baseline/data-quality-baseline.md` | line 12, Residual risks | "The owner is Unknown." | "Owner: Team-Force." |
| `docs/02-baseline/data-quality-baseline.md` | line 85 | "`retry_count` >= 1000. Owner: Unknown." | "`retry_count` >= 1000. Owner: Team-Force." |
| `docs/02-baseline/data-quality-baseline.md` | line 192 | "from 0 to 1 inclusive. Owner: Unknown." | "from 0 to 1 inclusive. Owner: Team-Force." |
| `docs/02-baseline/data-quality-baseline.md` | line 193 | "the PROPOSED bound of 1000. Owner: Unknown." | "the PROPOSED bound of 1000. Owner: Team-Force." |
| `docs/02-baseline/defect-list.md` | line 58, F18 | "The bound is PROPOSED. Owner: Unknown." | "The bound is PROPOSED. Owner: Team-Force." |
| `docs/02-baseline/defect-list.md` | line 59, F19 | "range: 0 to 1 inclusive. Owner: Unknown." | "range: 0 to 1 inclusive. Owner: Team-Force." |
| `docs/02-baseline/ai-qualification.md` | line 39, provisioning retry row | "That bound is PROPOSED. Owner: Unknown." | "That bound is PROPOSED. Owner: Team-Force." |
| `docs/02-baseline/ai-qualification.md` | line 54, retry worked example | "The owner is Unknown." | "Owner: Team-Force." |
| `docs/02-baseline/ai-qualification.md` | line 110, retry findings row | "The bound 1000 is PROPOSED. Owner: Unknown." | "The bound 1000 is PROPOSED. Owner: Team-Force." |

#### Fix 5

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/glossary.md` | line 18 | "Claim labels. A meaning is a **Verified Fact** from the named files unless the row says **Inference**, **Assumption**, or **Unknown**." | "Claim labels. Status-word meanings are **Inference**, because the repo defines none of them. Other meanings are a **Verified Fact** from the named files unless the row says otherwise." The PROPOSED sentence after it is unchanged. |

#### Fix 6

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/glossary.md` | after line 130 (now 131–132), above the network zone table | (none) | "A network zone is a named part of the network that a device belongs to. The repo does not say whether zones follow place or function." |

#### Fix 7

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/glossary.md` | line 194 (now 196), `metric.cost_per_correlated_incident` | "What the model calls for one incident cost. Cannot be computed today. The alarm-to-incident join and the price are Unknown." | "The total cost of the model calls made for one incident. This works only after the alarms are tied to that incident. The repo does not say how to tie them, and the price is Unknown." |

The review cites line 193. The row sits on line 194. The edit hit the row by its id.

#### Fix 8

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/README.md` | line 222 (now 226), severity word order | "S05R, owner Unknown" | "S05R, owner Team-Force" |
| `SL/README.md` | line 224 (now 228), storm size | "S04-11, owner Unknown" | "S04-11, owner Team-Force" |
| `SL/README.md` | line 233 (now 237), order to circuit | "Owner Unknown" | "owner Team-Force". This row names no stage. |

#### Fix 9

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/access-semantics.yaml` | 19 `owner:` keys on lines 122, 128, 134, 140, 146, 152, 158, 164 (`purpose.incident_triage`, `purpose.network_change_planning`, `purpose.field_repair`, `purpose.customer_enquiry`, `purpose.scheduled_automation`, `purpose.vendor_support`, `purpose.ai_assistance`, `purpose.audit_review`); 181, 188, 195, 202 (`scope.one_site`, `scope.one_customer`, `scope.assigned_incident`, `scope.own_vendor_devices`); 305, 344, 372, 388, 406, 430, 449 (the seven `persona.*` items) | `owner: Mangesh (FDE)` | `owner: Team-Force` |
| `SL/access-semantics.yaml` | line 294, YAML comment above `personas` | `# All grants are PROPOSED. Owner Mangesh (FDE). Stage S04-03 confirms them.` | `# All grants are PROPOSED. Owner Team-Force. Stage S04-03 confirms them.` See "Points for the S03R reviewer". |
| `SL/ai-context-policy.yaml` | 7 `owner:` keys on lines 42 (`policy.prompt_fields`), 104 (`policy.output_schema`), 300 (`failmode.stale_topology_blank`), 373 (`ai_use.incident_summary`), 386 (`ai_use.next_action_recommendation`), 399 (`ai_use.configuration_suggestion`), 422 (`ai_use.remediation_execution`) | `owner: Mangesh (FDE)` | `owner: Team-Force` |
| `SL/ai-context-policy.yaml` | line 270, `policy.fail_to_person` `hand_to_label` | "Owner Mangesh (FDE)." | "Owner Team-Force." |
| `SL/ai-context-policy.yaml` | lines 368, 381, 394, 416, `approval_point` of `ai_use.incident_summary`, `ai_use.next_action_recommendation`, `ai_use.configuration_suggestion`, `ai_use.remediation_execution` | "Owner Mangesh (FDE)." | "Owner Team-Force." |
| `SL/metrics.yaml` | line 83, `metric.audit_completeness` `required_fields_note` | "PROPOSED. Owner Mangesh (FDE). Stage S05-14" | "PROPOSED. Owner Team-Force. Stage S05-14" |
| `SL/metrics.yaml` | lines 85 and 129, `owner:` of `metric.audit_completeness` and `metric.ai_outcome_count` | `owner: Mangesh (FDE)` | `owner: Team-Force` |
| `SL/business-rules.yaml` | line 132, `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` `stage_note` | "with owner Mangesh (FDE) until" | "with owner Team-Force until" |
| `SL/README.md` | line 10, Assumptions | "PROPOSED with owner Mangesh (FDE)." | "PROPOSED with owner Team-Force." |
| `docs/02-baseline/ai-qualification.md` | lines 43, 44, 45, 47, 70, 76, 84, 118 | "Owner: Mangesh (FDE)" (8 places) | "Owner: Team-Force" (8 places) |

Every "Author: Mangesh (FDE)" line is unchanged. **Verified Fact:** `rg "Mangesh" semantic-layer --glob "!generated/**"` now finds only the two Author rows.

#### Step 6: change log and header

| File | Line | Old text | New text |
|---|---|---|---|
| `SL/README.md` | line 8, header Status | "PASS. The schema validates all seven YAML files. 34 tests pass. ..." | "S03 PASS. Review S03R round 1 was BLOCKED. Stage S03F round 1 applied its fixes 1 to 9 on 2026-10-10. S03R runs again next. The schema validates all seven YAML files. 35 tests pass. ..." |
| `SL/README.md` | new line 78, change log | (none) | `1.0.0` · 2026-10-10 · S03F · "S03R fixes applied, round 1. Fixes 1 to 9 from `docs/02-baseline/semantic-layer-review.md`. ..." |
| `SL/README.md` | "Last build" block | The S03 output with "34 passed in 0.95s" | The S03F round 1 output pasted below |

Every YAML file still carries `version: "1.0.0"`. **Verified Fact:** test `test_every_yaml_carries_version_and_readme_repeats_it` passes, and `build.py` prints "Version 1.0.0".

### Points for the S03R reviewer

These are the three places where this round went past the literal text of a fix.

**Decision, 2026-10-10:** Team-Force, the owner in `docs/00-contract/operating-contract.md` row 10, accepted all three edits as made. Mangesh (FDE) recorded the decision for Team-Force. S03R does not need to rule on them again. S03R still checks that each edit matches the description below.

1. **The comment on `access-semantics.yaml` line 294.** Fix 9 lists exact places, and this YAML comment is not one of them. It said the grants' owner is Mangesh (FDE). Left as is, it would contradict the 19 `owner: Team-Force` keys in the same file. It is a comment, so no id and no generated JSON changed.
2. **Quotes on two `metrics.yaml` lines.** Lines 69 and 107 were plain YAML strings. The new text "Owner: Team-Force" holds a colon followed by a space. YAML read that as a new key, and `build.py` failed with `mapping values are not allowed here ... line 69, column 102`. Both values are now in double quotes. The text inside is word for word as the fix says. **Verified Fact:** the generated `metrics.json` shows the same string with no quote marks.
3. **README counts and the new test.** S03F step 4 asks for a test when an added item is required. This round added `test_every_agency_and_pick_word_is_defined`. The README test count, the test list, the id table, and the glossary row count were updated so the README stays true.

### Citation check

No id was renamed or removed. Eight ids were added. The other ids below kept their id and changed only an owner or a text field. **Verified Fact:** `rg -l -F <id>` over `semantic-layer/`, `docs/`, `policy/`, `tests/`, and `apps/` on 2026-10-10. `generated/` copies are left out of the list.

| Id | Files that cite it |
|---|---|
| `agency.analyse`, `agency.recommend`, `agency.decide`, `agency.execute` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `docs/02-baseline/semantic-layer-review.md`. `agency.recommend` is also in `SL/README.md`. |
| `pick.rules`, `pick.deterministic_code`, `pick.workflow_automation`, `pick.genai` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `docs/02-baseline/semantic-layer-review.md`. `pick.deterministic_code` is also in `SL/README.md`. |
| `metric.retry_count` | `SL/metrics.yaml`, `SL/glossary.md`, `SL/README.md`, `SL/tests/test_semantic_layer.py` |
| `metric.sla_breach_risk` | `SL/metrics.yaml`, `SL/glossary.md`, `SL/README.md` |
| `metric.audit_completeness` | `SL/metrics.yaml`, `SL/glossary.md`, `SL/business-rules.yaml`, `SL/tests/test_semantic_layer.py` |
| `metric.ai_outcome_count` | `SL/metrics.yaml`, `SL/glossary.md` |
| `metric.cost_per_correlated_incident` | `SL/metrics.yaml`, `SL/glossary.md`, `SL/README.md`, `SL/tests/test_semantic_layer.py`, `docs/02-baseline/semantic-layer-review.md` |
| `field.incident.sla_breach_risk` | `SL/entities.yaml`, `SL/metrics.yaml`, `SL/ai-context-policy.yaml` |
| `field.service_order.retry_count` | `SL/entities.yaml`, `SL/metrics.yaml`, `SL/ai-context-policy.yaml` |
| `policy.prompt_fields` | `SL/ai-context-policy.yaml`, `SL/README.md` |
| `policy.output_schema` | `SL/ai-context-policy.yaml` |
| `policy.fail_to_person` | `SL/ai-context-policy.yaml`, `SL/README.md`, `docs/02-baseline/semantic-layer-review.md` |
| `failmode.stale_topology_blank` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `SL/README.md` |
| `ai_use.incident_summary` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `SL/README.md`, `SL/tests/test_semantic_layer.py` |
| `ai_use.next_action_recommendation`, `ai_use.configuration_suggestion` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `SL/tests/test_semantic_layer.py` |
| `ai_use.remediation_execution` | `SL/ai-context-policy.yaml`, `SL/glossary.md`, `SL/README.md`, `SL/tests/test_semantic_layer.py`, `docs/02-baseline/semantic-layer-review.md` |
| `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `SL/business-rules.yaml`, `SL/ai-context-policy.yaml`, `SL/access-semantics.yaml`, `SL/glossary.md`, `SL/tests/test_semantic_layer.py`, `docs/02-baseline/semantic-layer-review.md` |
| `resource.sensitive_device_fields` | `SL/access-semantics.yaml`, `SL/glossary.md`, `SL/README.md`, `docs/02-baseline/semantic-layer-review.md` |
| 8 `purpose.*`, 4 `scope.*`, and 7 `persona.*` ids with a changed `owner:` | `SL/access-semantics.yaml` and `SL/glossary.md`. Outside the tree, only `persona.noc_operator` and `persona.automation_service` are cited, both in `docs/02-baseline/semantic-layer-review.md`. Nothing in `policy/`, `tests/`, or `apps/` cites any of the 19. |

The pick, agency, outcome, and approval point of each AI use still match `docs/02-baseline/ai-qualification.md`. The only change on both sides is the owner name, Mangesh (FDE) to Team-Force, made together by fix 9. No AI use gained execute agency. `ai_use.remediation_execution` is still the only `agency: execute` item, and its pick is still `workflow_automation`. **Verified Fact:** test `test_four_outcomes_present_and_model_never_executes` passes.

### Build, check, and test output

Run on 2026-10-10 from the repo root with `.venv\Scripts\python.exe`, after `Remove-Item -Recurse semantic-layer\generated`. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
> python semantic-layer/build.py
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

> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
...................................                                      [100%]
35 passed in 1.12s
exit=0
```

`generated/relationships.json` and `generated/status-taxonomy.json` came out byte for byte the same as before. Their YAML did not change. **Verified Fact:** `git status` lists neither file.

The first build attempt failed on the `metrics.yaml` colon described above. That run is not the record. The output above is the clean run after the fix.

### Done test output

Changed the glossary Term `bronze` to `bronzed` on the `status.word.bronze` row, and nothing else. Ran the tests. Restored the word. Ran the tests again. **Verified Fact.**

```text
--- changed bronze to bronzed
E       AssertionError: glossary term differs from YAML name or word: [('bronzed', 'status.word.bronze', 'bronze')]
FAILED semantic-layer/tests/test_semantic_layer.py::test_glossary_and_yaml_agree_on_every_term
1 failed, 34 passed in 1.42s
--- restored
...................................                                      [100%]
35 passed in 0.99s
```

After the restore, `glossary.md` line 72 reads `` | `bronze` | `status.word.bronze` | ... ``.

### Check that the new test catches a bad agency word

Team-Force asked for this check on 2026-10-10, after accepting the three points above. It shows that `test_every_agency_and_pick_word_is_defined` fails when an `agency` value has no `agency.*` item.

The check changed `agency: analyse` to `agency: observe` on `action.read` in `SL/access-semantics.yaml` line 29. The schema does not limit the `agency` key on an action, so `build.py` accepts the change. The build was run after the change so that the generated-file tests stay quiet, and only the new test speaks. Then the word was restored and the build was run again. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
--- changed action.read agency: analyse -> observe
Validated 7 YAML files against semantic-layer.schema.json. Version 1.0.0.

E       AssertionError: [('access-semantics.yaml', 'actions/0', 'agency', 'observe')]
FAILED semantic-layer/tests/test_semantic_layer.py::test_every_agency_and_pick_word_is_defined
1 failed, 34 passed in 1.16s
--- restored
Validated 7 YAML files against semantic-layer.schema.json. Version 1.0.0.
generated/ matches the YAML. 7 files validated. Version 1.0.0.
35 passed in 0.89s
--- before vs after hashes identical: True
```

The build lines show only the first line of output. The last line compares the SHA-256 of `SL/access-semantics.yaml` and all 8 files in `SL/generated/`, taken before the change and after the restore. All 9 are the same. One finding: only the new test caught the made-up word. Without it, an undefined agency word on an access action would pass every other test and the schema.

### Files changed this round

**Verified Fact:** `git status --short` on 2026-10-10.

| File | Named by |
|---|---|
| `SL/README.md` | Fixes 4, 8, 9; steps 6 and 7 |
| `SL/glossary.md` | Fixes 2, 3, 4, 5, 6, 7 |
| `SL/ai-context-policy.yaml` | Fixes 1, 9 |
| `SL/access-semantics.yaml` | Fix 9 |
| `SL/metrics.yaml` | Fixes 4, 9 |
| `SL/entities.yaml` | Fix 4 |
| `SL/business-rules.yaml` | Fix 9 |
| `SL/schemas/semantic-layer.schema.json` | Fix 1 |
| `SL/tests/test_semantic_layer.py` | Fixes 1, 2 |
| `SL/generated/` (6 of 8 files) | Written by `build.py` |
| `docs/02-baseline/data-quality-baseline.md` | Fix 4 |
| `docs/02-baseline/defect-list.md` | Fix 4 |
| `docs/02-baseline/ai-qualification.md` | Fixes 4, 9 |
| `docs/02-baseline/semantic-layer-fixes.md` | This file (S03F required artifact) |
| `../playbook/S03R-semantic-layer-review.md` | Team-Force request on 2026-10-10, after round 1. Two sentences added to "Required artifacts": a fix that changes an owner or a name also covers every comment and text in the same file that states it, and a fix that adds a required item also covers its test and the README counts. This is a playbook file outside the packet. No fix named it. |

No file changed under `apps/`, `policy/`, `data/`, `etl/`, or `legacy/`. The review file is unchanged. No file was added under `semantic-layer/`. The tracked cache file `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc` was rewritten by an early pytest run and then restored with `git checkout`. A stray `.pyc` from a helper command was deleted. Advisory A1 in the review still applies.

### Map from FAIL rows to fixes

This map says which edits address each row. It does not mark any row PASS. The next S03R decides that.

| FAIL row | Fixes | Edits that address it |
|---|---|---|
| R9 | 1, 2, 3 | `agency_levels` and `picks` added to `SL/ai-context-policy.yaml`. 28 glossary rows added: 4 agency, 4 pick, 11 AI use, 9 provenance. `GLOSSARY_PREFIXES` now covers `agency.`, `pick.`, `ai_use.`, and `provenance.`. The `resource.sensitive_device_fields` row says what `mgmt_ip` and `credential_profile` are. |
| R12 | 4 | The retry bound of 1000 and the `sla_breach_risk` range of 0 to 1 now read "PROPOSED" with "Owner: Team-Force" in `SL/metrics.yaml`, `SL/entities.yaml`, `SL/glossary.md`, `SL/README.md`, `data-quality-baseline.md`, `defect-list.md`, and `ai-qualification.md`. |
| R14.4 | 5 | `SL/glossary.md` line 18 now labels status-word meanings Inference. |
| R14.7 | 4 | Same edits as R12. |
| R14.8 | 1 | Each agency word and pick word now has a YAML item with a meaning. The schema checks the shape of both lists. The new test fails when a YAML `agency` or `pick` value has no item. |
| R15 | 6, 7 | A sentence above the network zone table says what a network zone is. The cost row now reads as a total cost of model calls, tied to one incident. |

Fixes 8 and 9 address no FAIL row. They apply the owner decision in `docs/00-contract/operating-contract.md` row 10.

## Round 2, 2026-10-10

### Fix source

| Item | Value |
|---|---|
| Path | `docs/02-baseline/semantic-layer-review.md` |
| Why this file | A file search on 2026-10-10 found no `docs/02-baseline/semantic-layer-revision.md`. The review is the only fix source. **Verified Fact.** |
| Header date and version | 2026-10-10, review v2.0 of semantic layer `1.0.0`. This file replaces the round 1 review (v1.0). |
| Stage status | BLOCKED for S04. Every check on the `semantic-layer/` tree passes. One row fails: R14.7. |
| Version check | `SL/README.md` line 6 states version `1.0.0`. A file search on 2026-10-10 found no `docs/prd/prd.md`. No later stage has written that version into a PRD, so this stage may run. **Verified Fact.** |

### Fixes required, copied word for word from the review

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

The review has one FAIL row, R14.7. Fix 1 matches that row. No FAIL row is missing a fix.

### Advisory A7, copied word for word from the review

The Decisions block says to apply this advisory. The other advisories stay as written.

- **A7, new.** Two texts still give the S03 picture. The test module's opening comment (`SL/tests/test_semantic_layer.py` lines 6–18) lists what the tests fail on and leaves out the agency and pick check. `SL/README.md` lines 203–208 ("Done test") report "34 passed" with no stage name. That run was the S03 done test. Name it as the S03 run, or point to the S03F done test in `semantic-layer-fixes.md`.

### Decisions block, as pasted

```text
Fix 3: Option B.
Apply advisory A7 from semantic-layer-review.md.
```

### Decision per fix

| Fix | Decision | Reason |
|---|---|---|
| 1 | apply | The fix names both sentences and both lines. It offers no options. The owner is Team-Force, PROPOSED, from `docs/00-contract/operating-contract.md` row 10. Naming the owner does not approve the 1000 bound or the 0-to-1 range. |
| 2 | apply | The fix names the four places and the owner, Team-Force. It offers no options. The numbers and the severity list stay unset. |
| 3 | apply, option B | The Decisions block says `Fix 3: Option B.` The new sentence is "Who fixes each defect is Unknown. The owner of the PROPOSED bounds in F18 and F19 is Team-Force." |
| A7 | apply | The Decisions block says to apply it. This round names the README "Done test" block as the S03 run. It leaves the recorded result "34 passed" as the S03 result. It adds the agency and pick check to the test module's opening comment. |

No fix is waiting for a decision. No fix is marked cannot apply.

### Edit list

Line numbers are the line in the file after the edit, except where the note says "before". **Verified Fact:** the files on disk on 2026-10-10, and `git diff --stat`.

#### Fix 1

| File | Line or id | Old text | New text |
|---|---|---|---|
| `docs/02-baseline/data-quality-baseline.md` | line 11, Unresolved issues | "The owner of the retry bound is Unknown. The owner of the `sla_breach_risk` range is Unknown." | "The retry bound and the `sla_breach_risk` range are PROPOSED. Owner: Team-Force. Neither is approved." The rest of the cell is unchanged. |
| `docs/02-baseline/data-quality-baseline.md` | line 214, Lifecycle | "The PROPOSED bounds stay proposals until an owner is named." | "The PROPOSED bounds stay proposals until Team-Force approves them." |

Lines 12, 85, 192, and 193 already said "Owner: Team-Force". This round did not edit them. **Verified Fact:** `git diff --stat` shows 4 changed lines in this file, which is these two replacements.

#### Fix 2

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/status-taxonomy.yaml` | line 3404, `collision.gold_bronze_as_severity` `resolution` | "Open. The owner of the severity list is Unknown. This file records the words. It does not pick a cutoff." | "Open. The severity list and its order are not set. Owner: Team-Force. This file records the words. It does not pick a cutoff." The value stays a folded block (`>-`). The colon has no quotes. `build.py` accepted the file. |
| `docs/02-baseline/ai-qualification.md` | line 110, provisioning retry Open questions cell | "Who sets the legal maximum is Unknown." | "The legal maximum is not set. Owner: Team-Force." The same row still says "Owner: Team-Force" for the 1000 bound. |
| `docs/02-baseline/defect-list.md` | line 58, F18 Open questions cell | "Who sets the legal maximum is Unknown." | "The legal maximum is not set. Owner: Team-Force." |
| `docs/02-baseline/defect-list.md` | line 59, F19 Open questions cell | "Who sets the legal range is Unknown." | "The legal range is not set. Owner: Team-Force." |

`SL/README.md` already said "S05R, owner Team-Force" for the severity-word order. This round did not edit that cell. The new change-log row moved it from line 226 to line 227. **Verified Fact:** line 227.

`build.py` rewrote `SL/generated/status-taxonomy.json` and `SL/generated/manifest.json`. The resolution string in the JSON is the new sentence. **Verified Fact:** `status-taxonomy.json` line 4743. `git status` lists those two generated files and no other file under `generated/`.

#### Fix 3

| File | Line or id | Old text | New text |
|---|---|---|---|
| `docs/02-baseline/defect-list.md` | line 11, Unresolved issues | "Owners are Unknown." | "Who fixes each defect is Unknown. The owner of the PROPOSED bounds in F18 and F19 is Team-Force." The rest of the cell is unchanged. |

#### Advisory A7

| File | Line or id | Old text | New text |
|---|---|---|---|
| `SL/tests/test_semantic_layer.py` | new line 11, opening comment | (none) | "- an agency or pick value anywhere in the YAML has no matching agency or pick item" |
| `SL/README.md` | line 206, Done test (was line 205 before the change-log row) | "Run on 2026-10-10. **Verified Fact.**" | "This is the S03 done test. Run on 2026-10-10. **Verified Fact.**" The two numbered steps below it are unchanged, including "34 passed". |

#### Step 6: change log and header

| File | Line | Old text | New text |
|---|---|---|---|
| `SL/README.md` | line 8, header Status | "S03 PASS. Review S03R round 1 was BLOCKED. Stage S03F round 1 applied its fixes 1 to 9 on 2026-10-10. S03R runs again next. ..." | "S03 PASS. Review S03R round 2 was BLOCKED on R14.7. Stage S03F round 2 applied fixes 1 to 3 and advisory A7 on 2026-10-10. S03R runs again next. ..." The version, the 35 tests, and the 6.2 ticks stay. |
| `SL/README.md` | new line 79, change log | (none) | `1.0.0` · 2026-10-10 · S03F · "S03R fixes applied, round 2. Fixes 1 to 3 and advisory A7 from `docs/02-baseline/semantic-layer-review.md`. ..." |

Every YAML file still carries version `1.0.0`. **Verified Fact:** `build.py` prints "Version 1.0.0", and a search of the seven YAML files shows `version: "1.0.0"` or `version: 1.0.0`.

#### Step 7: Last build

| File | Line | Old text | New text |
|---|---|---|---|
| `SL/README.md` | lines 240–265, Last build | The round 1 output, "35 passed in 1.12s" | The round 2 output pasted below, "35 passed in 1.04s" |

### Citation check

No id was renamed or removed. No id was added. The only id whose text changed is `collision.gold_bronze_as_severity`. The change is the `resolution` sentence. **Verified Fact:** search for that id on 2026-10-10 over `semantic-layer/`, `docs/`, `policy/`, `tests/`, and `apps/`. `generated/` copies are left out of the list.

| Id | Files that cite it |
|---|---|
| `collision.gold_bronze_as_severity` | `SL/status-taxonomy.yaml`, `SL/glossary.md`, `SL/README.md`, `SL/tests/test_semantic_layer.py`, `docs/02-baseline/semantic-layer-review.md` |

`policy/`, `tests/`, and `apps/` do not cite it. The id string is unchanged in every file that cites it.

No AI use changed. `SL/ai-context-policy.yaml` is absent from `git status`. The pick, agency, outcome, and approval point of each AI use still match `docs/02-baseline/ai-qualification.md`. `ai_use.remediation_execution` is still the only `agency: execute` item, and its pick is still `workflow_automation`. **Verified Fact:** `git status` and test `test_four_outcomes_present_and_model_never_executes`, which passed in the 35.

### Build, check, and test output

Run on 2026-10-10 from `06-telecom-service-network-incident-ops` with `.venv\Scripts\python.exe`, after `Remove-Item -Recurse semantic-layer\generated`. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
> python semantic-layer/build.py
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

> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
...................................                                      [100%]
35 passed in 1.04s
exit=0
```

### Done test output

Changed the glossary Term `silver` to `silverd` on the `status.word.silver` row, and nothing else. Ran the tests. Restored the word. Ran the tests again. **Verified Fact.**

```text
--- changed silver to silverd
E       AssertionError: glossary term differs from YAML name or word: [('silverd', 'status.word.silver', 'silver')]
FAILED semantic-layer/tests/test_semantic_layer.py::test_glossary_and_yaml_agree_on_every_term
1 failed, 34 passed in 1.29s
--- restored
...................................                                      [100%]
35 passed in 0.91s
```

After the restore, `glossary.md` line 71 reads `` | `silver` | `status.word.silver` | ... ``. `git status` does not list `glossary.md`.

### Files changed this round

**Verified Fact:** `git status --short` on 2026-10-10.

| File | Named by |
|---|---|
| `docs/02-baseline/data-quality-baseline.md` | Fix 1 |
| `SL/status-taxonomy.yaml` | Fix 2 |
| `SL/generated/status-taxonomy.json` | Written by `build.py` after fix 2 |
| `SL/generated/manifest.json` | Written by `build.py` after fix 2 |
| `docs/02-baseline/ai-qualification.md` | Fix 2 |
| `docs/02-baseline/defect-list.md` | Fixes 2 and 3 |
| `SL/tests/test_semantic_layer.py` | Advisory A7 |
| `SL/README.md` | Advisory A7; steps 6 and 7 |
| `docs/02-baseline/semantic-layer-fixes.md` | This file (S03F required artifact) |

No file changed under `apps/`, `policy/`, `data/`, `etl/`, or `legacy/`. The review file is unchanged. No file was added under `semantic-layer/`. `glossary.md` is unchanged after the done-test restore. The tracked cache file `SL/tests/__pycache__/test_semantic_layer.cpython-313-pytest-8.3.2.pyc` is absent from `git status`.

`transcript/chat_transcript.md` is the project chat log. It sits outside the packet. This round appends one turn there.

### Map from FAIL rows to fixes

This map says which edits address each row. It does not mark any row PASS. The next S03R decides that.

| FAIL row | Fixes | Edits that address it |
|---|---|---|
| R14.7 | 1 | `docs/02-baseline/data-quality-baseline.md` line 11 now says the retry bound and the `sla_breach_risk` range are PROPOSED, with Owner: Team-Force, and that neither is approved. Line 214 now says the bounds stay proposals until Team-Force approves them. Lines 12, 85, 192, and 193 already said Owner: Team-Force. |

Fixes 2 and 3 address no FAIL row. They apply the owner decision in `docs/00-contract/operating-contract.md` row 10 to four more cells, and they apply option B on the defect-list header. Advisory A7 addresses no FAIL row. It names the S03 done test and adds the agency and pick check to the test comment.

## Lifecycle

This file cites `docs/02-baseline/semantic-layer-review.md` as the fix source, the `semantic-layer/` files by path and id, and `docs/02-baseline/ai-qualification.md`. Stage S03R runs next, in a fresh chat, against the fixed tree. It overwrites `semantic-layer-review.md`. Each S03F round adds a new "Round N" section here and keeps the earlier ones. S04 starts only when S03R reads PASS, or CONDITIONAL PASS with fixes applied. When S05R's rerun rows fail, this stage runs again with `semantic-layer-revision.md` as the fix source. After S06 cites the version, this stage does not run. S05R handles the change with an ADR.
