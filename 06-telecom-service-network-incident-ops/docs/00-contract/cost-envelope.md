# Cost envelope

| Field | Value |
|---|---|
| Stage | S2Q — Cost envelope revised after AI qualification (first issue S0B, Execution Plan Phase 0B; spine stage 0C) |
| Date / version | 2026-10-10, v1.1. First issue 2026-10-09, v1.0. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | REVISED-S2Q. Eight capabilities have hosted-model cost 0 because their pick uses no model. Three GenAI capabilities keep an Unknown price. |
| Evidence sources | `data/synthetic/ai_invocations.csv`; `data/synthetic/events.jsonl`; `data/manifest.json`; `apps/api/services/ai_gateway.py`; `docs/00-setup/replay-log.md` sections 1.4, 1.5, and 2.7; `Project_Intent.md` 4.3 and Appendix B; `docs/02-baseline/ai-qualification.md` |
| Assumptions | The CSV and the JSONL file are the volume evidence that exists today. No price list exists in the repo. The pick for each capability is the one in `docs/02-baseline/ai-qualification.md`. |
| Unresolved issues | The money unit of `cost_units` is Unknown. A price per token is Unknown. A hosted model name is Unknown. The SIMULATED token sum cannot be split across the three GenAI capabilities. The CSV `use_case` column does not name those capabilities. |
| Residual risks | A reader can treat 845675 or 6736.4198 as a bill. Both numbers are synthetic stand-ins. The live summarize call uses `token_estimate` 64 from the word-count formula. The assignment zero below is not a measured bill. |

## What this file is

This file is the cost view for this packet. Version 1.0 recorded the figures already in the repo. Version 1.1 adds the hosted-model assignment from stage S2Q. The measured figures stay in place. The file has three scenarios: deterministic rules, conventional automation, and a hosted model. Every measured number has one of the four honesty labels below. An assignment zero in the S2Q section is marked Assignment. Assignment is the stage decision. It is a separate mark from the four measurement labels. A missing figure stays in the Unknown table. This file sets no budget, no price, and no cutoff.

## Honesty labels

These four words are from `Project_Intent.md` Appendix B.

| Label | What it means in this file |
|---|---|
| REAL | A program in the inherited repo printed the number during the S00 replay. |
| PRECOMPUTED | The number is already stored in a repo file, such as `data/manifest.json`. |
| SIMULATED | The number stands in for a live service this lab did not call. Sums of those stored stand-ins stay SIMULATED. |
| EDUCATIONAL | The number teaches a point. The word-count token formula is the example in this file. |

## What was counted

`data/manifest.json` stores 354 data rows for each of the six CSV files, and 3000 lines for `events.jsonl`. This stage counted `ai_invocations.csv` and `events.jsonl` again. Both counts match the manifest.

| Figure | Value | Honesty | Where it came from |
|---|---|---|---|
| Data rows in `ai_invocations.csv` | 354 | PRECOMPUTED | `data/manifest.json` key `csv_files`. This stage counted 354 data rows in the file. The count matches. |
| Lines in `events.jsonl` | 3000 | PRECOMPUTED | `data/manifest.json` key `jsonl_events`. |
| Lines in `events.jsonl`, as printed by the sanity check | 3000 | REAL | `docs/00-setup/replay-log.md` section 1.4. The command printed `events: 3000`. |
| Device rows the ETL sample counted | 354 | REAL | `docs/00-setup/replay-log.md` section 1.5. The command printed `processed: 354`. |
| Rows in `ai_invocations.csv` with an integer `token_count` | 353 | SIMULATED | This stage counted them. The column is synthetic. One honesty label applies, so the count of that column is SIMULATED with the sum below. |
| Sum of integer `token_count` | 845675 | SIMULATED | This stage added the 353 integer values. The blank cell stays blank. It is left out of the sum. |
| Rows with a blank `token_count` | 1 | EDUCATIONAL | The row id is `AI_-BAD1`. Every other column on that row is blank too. `data/manifest.json` lists blank mandatory fields as a seeded defect for this file. |
| `token_estimate` on the replayed summarize call | 64 | EDUCATIONAL | `docs/00-setup/replay-log.md` section 2.7. The formula in `ai_gateway.py` is `len(prompt.split()) * 2`. |
| `token_count` on CSV row `REC-0001` | 73 | SIMULATED | First data row of `ai_invocations.csv`. |
| Stub wait in `ai_gateway.py` | 0.01 seconds | EDUCATIONAL | `ai_gateway.py` calls `time.sleep(0.01)`. The wait is a fixed stand-in written in the source. |
| Sum of `cost_units` in `events.jsonl` | 6736.4198 | SIMULATED | This stage added the field. The file does not name a currency. |

Worked example. One live summarize call and one CSV row use different token numbers. The replay of `POST /ai/summarize/REC-0001` returned `token_estimate` 64. That 64 is the word-count formula (EDUCATIONAL). The CSV row `REC-0001` stores `token_count` 73 (SIMULATED). The gateway leaves the CSV unchanged. 64 and 73 come from different files. A hosted-model bill for either number is Unknown.

This stage read the `model` column in `ai_invocations.csv`. The values are status words such as `approved`, `vendor`, and `not_enforced`. The string `local-sim-v1` is absent from that column. The live model name is in `ai_gateway.py`: `local-sim-v1`.

## Cost field by event type

The only cost field in `events.jsonl` is `cost_units`. These sums use the four `event_type` values stored in the file. Each sum is SIMULATED. The unit of money is Unknown.

| event_type | Rows | Sum of cost_units | Honesty |
|---|---|---|---|
| Alarm storm to incident correlation | 706 | 1535.6879 | SIMULATED |
| Approved remediation to validation | 771 | 1740.6596 | SIMULATED |
| Customer order to provisioning | 741 | 1676.6506 | SIMULATED |
| Topology lookup to AI recommendation | 782 | 1783.4217 | SIMULATED |
| All four types | 3000 | 6736.4198 | SIMULATED |

706 + 771 + 741 + 782 = 3000. That matches the line count.

## The live model has no bill

`local-sim-v1` is a stub. `ai_gateway.py` waits 0.01 seconds and returns the text "Synthetic summary for " plus the first field of the record. The replay returned that shape for `REC-0001`, with `guardrail_status` `not_enforced`. Nothing in that call is a hosted-model invoice. `Project_Intent.md` 2.7 says nothing is sent to a hosted model.

## Scenario 1 — Deterministic rules

A rules path returns the same result for the same input. It does not call `local-sim-v1`.

Known:

- The repo has a stub model path. This stage measured no separate rules engine.
- Stage S2Q places these capabilities here, because their pick uses no model: order qualification (rules); provisioning retry and rollback (deterministic code); alarm dedupe (deterministic code); alarm-to-incident correlation (deterministic code); topology lookup (deterministic code); capacity forecast (deterministic code); remediation validation (deterministic code). Remediation execution is workflow automation. It also uses no model. The list is in `docs/02-baseline/ai-qualification.md`.

Unknown:

- The money cost of writing rules, running them, or storing their logs. No figure in the repo.

Numbers in this scenario:

| Item | Value | Honesty |
|---|---|---|
| Hosted-model cost for a capability whose pick uses no model | 0 | Assignment from S2Q. Eight capabilities are in the table below. This 0 is not a measured bill. |
| Money cost of a rules run | Unknown | The repo has no figure. |

The token sum 845675 and the `cost_units` sums stay in the tables above as synthetic columns on lab files. Their honesty labels stay SIMULATED. The money cost of writing and running the rules is still Unknown.

## Scenario 2 — Conventional automation

This scenario is scripts, the ETL sample, and the API routes that do not call a model. It includes the daily batch sample and the sanity check. It excludes a hosted model.

Known:

- The ETL sample processed 354 device rows and flagged 1 malformed row (REAL, replay section 1.5).
- The sanity check reported 6 CSV files and 3000 events (REAL, replay section 1.4).
- `events.jsonl` carries `cost_units` on all 3000 lines. Those sums are in the table above (SIMULATED). The file does not say the number is the cost of the ETL.

Unknown:

- The money cost of the ETL, the test run, or a scheduler. No rate and no invoice are in the repo.
- How much of `cost_units` belongs to automation. The field is one number per event. It is not split into labour, compute, and model.

Numbers in this scenario:

| Item | Value | Honesty |
|---|---|---|
| Device rows processed by the ETL sample | 354 | REAL |
| Malformed rows the ETL sample printed | 1 | REAL |
| Event lines the sanity check printed | 3000 | REAL |
| Money cost of one ETL run | Unknown | The repo has no figure. |
| Money cost read from `cost_units` | Unknown | The sums exist and are SIMULATED. The currency is Unknown, so no money figure is stated. |

## Scenario 3 — A hosted model

This scenario is a call to a model hosted outside this machine. The inherited repo does not make that call.

Known:

- The code path that exists is `local-sim-v1`, a stub, with the EDUCATIONAL token formula and the EDUCATIONAL 0.01 second wait.
- If someone treats the CSV `token_count` column as volume, 353 rows add up to 845675 (SIMULATED) and 1 row is blank (EDUCATIONAL, seeded defect).
- One live summarize call in the replay used `token_estimate` 64 (EDUCATIONAL).
- The CSV `model` column holds status words. `local-sim-v1` is absent there. A hosted model name is absent there.

Unknown:

- The provider, the model name, the price per token, and the split between input tokens and output tokens.
- A monthly total, a cost per case closed, and a cost per request in money.
- Whether the three GenAI capabilities will call a host. Stage S2Q allows the call for incident summary, next-action recommendation, and configuration suggestion. It does not name a provider. The price stays Unknown.

Numbers in this scenario:

| Item | Value | Honesty |
|---|---|---|
| Sum of stored `token_count` (353 rows) | 845675 | SIMULATED |
| Blank `token_count` rows | 1 | EDUCATIONAL |
| Replay `token_estimate` for one summarize call | 64 | EDUCATIONAL |
| Stub wait | 0.01 seconds | EDUCATIONAL |
| Price per token | Unknown | No rate card is in the repo. |
| Hosted-model invoice | Unknown | The stub does not call a host. |
| Cost per case closed | Unknown | No such figure is in the repo. |

## Unknown rows

These rows stay visible. This file does not fill them.

| Item | Value | Why it is Unknown |
|---|---|---|
| Currency of `cost_units` | Unknown | The JSONL field is a number. The file does not name dollars or any other unit. |
| Price per token | Unknown | No rate card is in the repo. |
| Hosted model name and provider | Unknown | The code names `local-sim-v1` only. |
| Cost per request in money | Unknown | A request count in money is not stored. |
| Cost per case closed | Unknown | No closed-case cost is stored. |
| Cost of storing logs, metrics, and traces | Unknown | No storage price is stored. |
| Money cost of retries | Unknown | `service_orders.csv` has `retry_count`. This stage did not sum it. No money rate is in the repo. Stage S04-12 is the stage that analyses retry cost. |
| Budget or cutoff | Unknown | This file does not propose one. A later cutoff would be marked PROPOSED and would name an owner. |

## Hosted-model cost after S2Q

`docs/02-baseline/ai-qualification.md` assigns each capability. A capability whose pick is rules, deterministic code, or workflow automation has no hosted-model call. The hosted-model cost for that capability is 0.

The 0 is an **assignment**. It was not counted from a file. It is not REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. Those four labels stay on the measured figures above. The 0 is not a bill and not a budget.

A capability whose pick is GenAI may call a model later. No rate card is in the repo. The hosted-model price for that capability stays Unknown. The SIMULATED sum of `token_count`, 845675, is the whole CSV. It is not split onto these three rows. **Verified Fact:** `docs/01-discovery/ai-subsystem-discovery.md` says the `use_case` column holds words such as `high_risk`, and it does not hold the three product names.

| Capability | Pick | Hosted-model cost | Honesty |
|---|---|---|---|
| Order qualification | rules | 0 | Assignment from S2Q. Not a measured bill. |
| Provisioning retry and rollback | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Alarm dedupe | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Alarm-to-incident correlation | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Topology lookup | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Capacity forecast | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Remediation execution | workflow automation | 0 | Assignment from S2Q. Not a measured bill. The model is not the actor. |
| Remediation validation | deterministic code | 0 | Assignment from S2Q. Not a measured bill. |
| Incident summary | GenAI | Unknown | No rate card is in the repo. The SIMULATED sum 845675 is not this row. |
| Next-action recommendation | GenAI | Unknown | No rate card is in the repo. The SIMULATED sum 845675 is not this row. |
| Configuration suggestion | GenAI | Unknown | No rate card is in the repo. The SIMULATED sum 845675 is not this row. |

Worked example. Alarm dedupe compares `dedupe_key` and `storm_batch_id`. That comparison calls no model. The hosted-model cost on that row is 0 by assignment. The next-action sentence may call a model later. The price of that call is Unknown. The lab figure 845675 stays in the measured table above as a SIMULATED sum of a synthetic column.

The four `event_type` sums stay as they were. They are SIMULATED lab figures. The file does not say they are a model bill. After S2Q, the hosted-model portion of each flow is:

| event_type | Sum of cost_units | Honesty of that sum | Hosted-model portion after S2Q |
|---|---|---|---|
| Alarm storm to incident correlation | 1535.6879 | SIMULATED | 0. Assignment. Dedupe and correlation use no model. |
| Approved remediation to validation | 1740.6596 | SIMULATED | 0. Assignment. Execution and validation use no model. |
| Customer order to provisioning | 1676.6506 | SIMULATED | 0. Assignment. Qualification, retry, and rollback use no model. |
| Topology lookup to AI recommendation | 1783.4217 | SIMULATED | Unknown. The flow mixes a deterministic lookup with the three GenAI capabilities. `cost_units` is one number per event. It is not split. |

706 + 771 + 741 + 782 = 3000. That line count is unchanged. The SIMULATED sums are unchanged.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-10-09 | v1.0 | Provisional envelope. Measured figures from the CSV, the JSONL file, the manifest, and the replay. Status PROVISIONAL. |
| 2026-10-10 | v1.1 | Status REVISED-S2Q. Hosted-model cost set to 0 by assignment for the eight capabilities whose pick uses no model. Hosted-model price left Unknown for incident summary, next-action recommendation, and configuration suggestion. SIMULATED sums 845675 and 6736.4198 kept, with their honesty labels. No price, currency, or cutoff added. |

## Lifecycle

This file cites `Project_Intent.md` 4.3 (the token formula and the row counts) and Appendix B (the four honesty labels). It cites `docs/00-setup/replay-log.md` for the live stub call. It cites `docs/02-baseline/ai-qualification.md` for the pick on each capability. Stage S04-12 reconciles a later FinOps baseline with this file. Stage S2Q is the revision recorded above.
