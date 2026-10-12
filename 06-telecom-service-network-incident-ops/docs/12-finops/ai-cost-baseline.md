# AI cost baseline

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Tokens and cost are counted from the repo files and every number has a label. No price exists in the repo, so every price here is EDUCATIONAL. The real model name is Unknown. |
| Evidence sources | `docs/12-finops/cost_baseline.py` and its saved output `cost_baseline_output.txt`; `data/synthetic/ai_invocations.csv`; `data/synthetic/events.jsonl`; `data/manifest.json` (through `cost-envelope.md`); `semantic-layer/entities.yaml`; `semantic-layer/metrics.yaml`; `docs/00-contract/cost-envelope.md` (v1.1); `docs/02-baseline/ai-qualification.md`; `apps/api/services/ai_gateway.py`; `logs/audit.log`; `docs/11-reliability/recovery-evidence.md`; `Project_Intent.md` Appendix B |
| Assumptions | The CSV and the JSONL file are synthetic stand-ins, so every figure taken from them is SIMULATED. The EDUCATIONAL rate is 1.0 educational unit per 1000 tokens. That rate is PROPOSED. Owner: Team-Force. It is a teaching number and not a price. |
| Unresolved issues | The money unit of `cost_units` is Unknown. The price per token is Unknown. The real model name behind the CSV `model` column is Unknown. The CSV has no outcome column, so held calls cannot be found in it. |
| Residual risks | A reader can take 845,675 tokens or 845.675 educational units as a bill. Neither is a bill. The CSV mean of 2,395.7 tokens per call is far above the live estimate of 90 tokens per call, so a forecast built on the CSV overstates the live gateway. |

## What this file is

This file counts tokens and cost from the data that is in the repo today. It uses one script, `cost_baseline.py`. The script reads three data files and one log. It writes nothing and calls no model.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file, a column, a metric id, or a script output.

Number labels from `Project_Intent.md` Appendix B: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## How to repeat the run

From `06-telecom-service-network-incident-ops/`:

```text
.venv\Scripts\python.exe docs/12-finops/cost_baseline.py
```

The run on 2026-10-11 exited with code 0. The saved output is `docs/12-finops/cost_baseline_output.txt`.

## What the two data files hold

| Item | Value | Label | Source |
|---|---|---|---|
| Data rows in `ai_invocations.csv` | 354 | PRECOMPUTED | `data/manifest.json`. The script counts 354. |
| Rows with an integer `token_count` | 353 | SIMULATED | Script section 1. |
| Rows with a blank `token_count` | 1 (`AI_-BAD1`) | SIMULATED | Script section 1. |
| Sum of `token_count` | 845,675 | SIMULATED | Script section 1. Same as `cost-envelope.md`. |
| Mean `token_count` per row | 2,395.7 | SIMULATED | Script section 1. |
| Smallest, middle, largest `token_count` | 23, 2336, 4946 | SIMULATED | Script section 1. |
| Cost column in `ai_invocations.csv` | None | Verified Fact | The ten columns are `ai_call_id`, `incident_id`, `use_case`, `model`, `topology_snapshot_id`, `alarm_count`, `token_count`, `recommendation_risk`, `approval_required`, `guardrail_status`. |
| Lines in `events.jsonl` | 3000 | PRECOMPUTED | `data/manifest.json`. The script counts 3000. |
| Token field in `events.jsonl` | None | Verified Fact | The nine fields are `event_id`, `business_entity`, `event_type`, `severity`, `correlation_id`, `actor`, `latency_ms`, `cost_units`, `payload_hash`. |
| Sum of `cost_units` | 6,736.4198 | SIMULATED | Script section 2. Same as `cost-envelope.md`. The money unit is Unknown. |

Tokens exist only in the CSV. Cost exists only in the JSONL file. No row joins the two. A cost per token cannot be read from the repo.

## Check of the `model` column before grouping

**Verified Fact.** The `model` column has 15 distinct values, counting the blank cell. None is a model name. The 14 words are `approved`, `requires_review`, `vendor`, `standard`, `degraded`, `pending`, `legacy`, `ai_assisted`, `not_enforced`, `rejected`, `high_risk`, `manual`, `internal`, `normal`. The count of rows that hold `local-sim-v1` is 0 (SIMULATED, script section 1a).

The same 14 words fill `use_case`, `recommendation_risk`, `approval_required`, and `guardrail_status`. **Inference:** the generator drew every word column from one shared list. No column holds a real model name, a real risk level, or a real approval answer.

So the grouping below is by status word. The real model name is **Unknown**. The table says "status word" and not "model" on purpose.

## Tokens by the `model` column (a status word, real model name Unknown)

All numbers: SIMULATED.

| `model` word | Rows | Sum of `token_count` | Share |
|---|---|---|---|
| requires_review | 33 | 96,153 | 11.4% |
| standard | 28 | 79,133 | 9.4% |
| vendor | 30 | 75,243 | 8.9% |
| approved | 35 | 69,857 | 8.3% |
| pending | 24 | 67,570 | 8.0% |
| degraded | 27 | 63,935 | 7.6% |
| ai_assisted | 24 | 62,791 | 7.4% |
| internal | 21 | 54,690 | 6.5% |
| not_enforced | 22 | 52,059 | 6.2% |
| high_risk | 22 | 49,836 | 5.9% |
| normal | 20 | 49,832 | 5.9% |
| manual | 21 | 49,230 | 5.8% |
| legacy | 24 | 43,655 | 5.2% |
| rejected | 22 | 31,691 | 3.7% |
| Total | 353 | 845,675 | 100.0% |

Worked example. The word `requires_review` has 33 rows. Their `token_count` values add to 96,153. That is 11.4% of 845,675. The spread across words is wide only because the row counts differ. The mean per row runs from 1,440 (`rejected`: 31,691 over 22 rows) to 2,914 (`requires_review`: 96,153 over 33 rows). Both are SIMULATED.

## Which column holds the risk level

Two columns hold risk-like words: `recommendation_risk` and `use_case`. **Verified Fact:** `entities.yaml` describes `recommendation_risk` as "how risky the model's advice was judged" and `use_case` as "what the call was for".

This file uses `recommendation_risk`. The reason is its definition. The reason is not its values, because both columns hold the same word list. A risk level from this column is therefore Unknown for most rows.

One cell is a number. `AI_-00019` holds 1.42 in `recommendation_risk` (**Verified Fact:** `entities.yaml`). The script puts that row in its own line.

All numbers: SIMULATED.

| `recommendation_risk` word | Rows | Sum of `token_count` | Share |
|---|---|---|---|
| internal | 35 | 96,623 | 11.4% |
| manual | 27 | 74,245 | 8.8% |
| high_risk | 28 | 73,060 | 8.6% |
| standard | 25 | 65,074 | 7.7% |
| requires_review | 28 | 64,200 | 7.6% |
| approved | 25 | 62,240 | 7.4% |
| degraded | 27 | 62,196 | 7.4% |
| legacy | 23 | 59,315 | 7.0% |
| not_enforced | 25 | 55,719 | 6.6% |
| ai_assisted | 20 | 52,359 | 6.2% |
| pending | 25 | 51,517 | 6.1% |
| rejected | 26 | 49,680 | 5.9% |
| normal | 25 | 47,013 | 5.6% |
| vendor | 13 | 32,380 | 3.8% |
| numeric cell 1.42 | 1 | 54 | 0.0% |
| Total | 353 | 845,675 | 100.0% |

Roll-up for the one word that reads as a risk level. `high_risk` has 28 rows and 73,060 tokens (8.6%). The other 325 rows and 772,615 tokens carry a word whose risk meaning is Unknown. All SIMULATED. The `use_case` view is in `cost_baseline_output.txt` section 1d.

## An EDUCATIONAL price on the SIMULATED tokens

The script applies 1.0 educational unit per 1000 tokens. PROPOSED. Owner: Team-Force. The unit is not money.

| Item | Value | Label |
|---|---|---|
| Whole CSV at that rate | 845.675 educational units | EDUCATIONAL, on SIMULATED tokens |
| One call at the mean `token_count` (2,395.7) | 2.3957 educational units | EDUCATIONAL |
| Real price per token | Unknown | No rate card in the repo |

## Cost and latency from `events.jsonl`

Every number: SIMULATED. The money unit of `cost_units` is Unknown.

| `event_type` (one business flow) | Events | Sum of `cost_units` | Mean per event | Median `latency_ms` | Mean `latency_ms` |
|---|---|---|---|---|---|
| Topology lookup to AI recommendation | 782 | 1,783.4217 | 2.2806 | 761.5 | 4,092.3 |
| Approved remediation to validation | 771 | 1,740.6596 | 2.2577 | 1,521 | 4,337.6 |
| Customer order to provisioning | 741 | 1,676.6506 | 2.2627 | 765 | 4,270.0 |
| Alarm storm to incident correlation | 706 | 1,535.6879 | 2.1752 | 1,638.5 | 4,320.6 |
| All four | 3000 | 6,736.4198 | 2.2455 | 776.5 | 4,252.9 |

| `actor` (one of seven personas) | Events | Sum of `cost_units` | Mean per event |
|---|---|---|---|
| automation_service | 444 | 1,028.6606 | 2.3168 |
| noc_operator | 435 | 996.2683 | 2.2903 |
| network_engineer | 440 | 990.9971 | 2.2523 |
| field_engineer | 422 | 950.5192 | 2.2524 |
| vendor_account | 424 | 948.4768 | 2.2370 |
| customer_support | 420 | 930.7537 | 2.2161 |
| ai_agent | 415 | 890.7441 | 2.1464 |
| All seven | 3000 | 6,736.4198 | 2.2455 |

All numbers: SIMULATED.

Latency across all 3000 events (SIMULATED): smallest 15 ms, median 776.5 ms, mean 4,252.9 ms, 95th percentile 13,627 ms, largest 14,992 ms. 1,403 events took more than 2000 ms. 540 took more than 10,000 ms. The 2000 ms level is PROPOSED in `slo-proposal.md`. The 10-second model timeout is PROPOSED in `ai_gateway.py`. Both are owned by Team-Force and neither is approved.

## What the live gateway records today

`logs/audit.log` is written by the running code, so these counts are REAL. The rows come from test runs and demo calls on this machine. They are not production traffic.

| Item | Value | Label |
|---|---|---|
| Rows in the log | 211 | REAL |
| Rows by action | `record.read` 113, `policy.deny` 63, `ai.summary` 35 | REAL |
| Rows with an integer `tokens` value | 11 | REAL |
| `tokens` on those 11 rows | 90 on every row (word count times 2) | EDUCATIONAL |
| `latency_ms` on those rows | 11 to 14 ms, mean 11.3 ms | REAL |
| Rows with `policy.hold` | 0 | REAL |
| Rows with the key `token_estimate_method` | 0 | REAL |

**Verified Fact.** `ai_gateway.py` line 312 computes `tokens` and line 329 computes `latency_ms` on every model call. `provenance()` in the same file (line 366) returns null for both when no model was called. The gateway therefore already writes the two fields. Half B confirms this against the audit row writer and adds `token_estimate_method`.

## Comparing the CSV with the live gateway

| Measure | CSV (SIMULATED) | Live gateway, first device row (EDUCATIONAL) |
|---|---|---|
| Tokens per call | 2,395.7 mean | 90 |
| 353 calls at that size | 845,675 tokens | 31,770 tokens |
| Ratio | 26.6 times larger | 1 |

The 31,770 figure is 353 times 90. It is a what-if sum (EDUCATIONAL). The live 90 tokens is one prompt for one device row. It is the word count of the allow-list prompt built in stage S04-09. A different record can give a different count.

## Reconciliation with `docs/00-contract/cost-envelope.md`

The envelope is REVISED-S2Q at v1.1. This stage added a v1.2 row to its change log and left the earlier rows as they were.

| Point | Envelope says | This baseline says | Result |
|---|---|---|---|
| CSV rows and integer `token_count` rows | 354 and 353 | 354 and 353 | Agree |
| Sum of `token_count` | 845675 (SIMULATED) | 845,675 (SIMULATED) | Agree |
| Blank `token_count` row | `AI_-BAD1` | `AI_-BAD1` | Agree |
| Event lines and sum of `cost_units` | 3000 and 6736.4198 (SIMULATED) | 3000 and 6,736.4198 (SIMULATED) | Agree |
| Four `event_type` sums | 1535.6879, 1740.6596, 1676.6506, 1783.4217 | Same four values | Agree |
| `model` column | Status words. `local-sim-v1` is absent. | 14 status words and a blank. 0 rows hold `local-sim-v1`. | Agree. This baseline names all 14 words. |
| Hosted-model cost of the eight rule capabilities | 0, by assignment | 0, by assignment. Not re-measured. | Agree |
| Hosted-model price for the three GenAI capabilities | Unknown | Unknown. An EDUCATIONAL rate is used for teaching only. | Agree |
| Money unit of `cost_units` | Unknown | Unknown | Agree |
| Tokens split across the three GenAI capabilities | Cannot be split | Cannot be split. This baseline groups by status word and places all tokens in one flow by Inference. | Agree on the limit. This baseline adds an Inference the envelope does not make. |
| Live token estimate | 64, from the S00 replay | 90 for the first device row, from the S04-09 allow-list prompt | Differ. The prompt changed. The 64 is still the S00 figure. |
| Retry cost | Money cost Unknown. `retry_count` not summed. | Sum is 943,094 (SIMULATED). What-if is EDUCATIONAL. Money still Unknown. | Extended |
| Latency | Stub wait 0.01 s (EDUCATIONAL) | Live rows show 11 to 14 ms (REAL). Event file median 776.5 ms (SIMULATED). | Agree for the stub. The event file adds a tail the envelope did not report. |
| Gap between CSV and live | Not stated | CSV mean is 2,395.7 tokens per call. Live is 90. Ratio 26.6. | New |

**Verified Fact.** No figure in the envelope is contradicted. One figure (64) is superseded for the current prompt. The envelope's "Unknown rows" table stays as it is.

## Findings

### AB-01

| | |
|---|---|
| Finding | The `model` column holds status words. The real model name is Unknown. |
| Evidence | **Verified Fact.** 14 words and a blank cell. 0 rows hold `local-sim-v1`. Script section 1a. `entities.yaml` `field.ai_invocation.model`. |
| Impact | A cost per model cannot be stated. The grouping above is a grouping by status word. |
| Risk | Medium. A reader may treat `high_risk` or `vendor` in the `model` column as a model name. |
| Confidence | High |
| Open questions | Open question for S03: `field.ai_invocation.model` needs a value list of real model names, so the column can be grouped by model. |

### AB-02

| | |
|---|---|
| Finding | `recommendation_risk` is the best available risk column, and it still holds mixed words. Only `high_risk` reads as a risk level. |
| Evidence | **Verified Fact.** Script section 1c. 28 rows hold `high_risk` (SIMULATED). One cell holds 1.42. |
| Impact | Cost per risk level is stated for `high_risk` only: 73,060 tokens (SIMULATED). The other 772,615 tokens have no usable risk level. |
| Risk | Medium |
| Confidence | Medium. The choice of column follows its definition in `entities.yaml`. |
| Open questions | Open question for S03: the YAML has no list of the risk levels the model advice can have. This design needs that list to group cost by risk level. |

### AB-03

| | |
|---|---|
| Finding | The CSV mean of 2,395.7 tokens per call is 26.6 times the live estimate of 90 tokens per call. |
| Evidence | **Verified Fact.** CSV mean from script section 1 (SIMULATED). The 90 comes from `logs/audit.log` (11 rows, all 90) and from the script's call to `build_prompt` on the first device row (EDUCATIONAL). |
| Impact | A volume forecast taken from the CSV overstates tokens for the live gateway. The prompt in `ai_gateway.py` now holds only the allow-list fields. |
| Risk | Medium. A budget built on 845,675 tokens would be wrong by an unknown factor. This stage sets no budget. |
| Confidence | Medium. The live figure is one device row. A tokenizer would change both sides. |
| Open questions | How many tokens a real summary of an incident, with alarms, needs is Unknown. The live prompt reads a device row only. |

### AB-04

| | |
|---|---|
| Finding | `cost_units` is one number per event. It does not split into model, compute, and labour. It also varies little. The mean per event ranges from 2.1464 to 2.3168 across actors and from 2.1752 to 2.2806 across flows. |
| Evidence | **Verified Fact.** Script section 2. `entities.yaml` `field.event.cost_units`. |
| Impact | No flow or actor stands out as the cost driver. A cost driver cannot be found in this file. |
| Risk | Low for the baseline. Medium if a reader draws a ranking from differences of under 8%. |
| Confidence | High |
| Open questions | The money unit of `cost_units`. Unknown. |

### AB-05

| | |
|---|---|
| Finding | Latency has a long tail. The median is 776.5 ms. The mean is 4,252.9 ms. 540 of 3000 events took more than 10,000 ms. |
| Evidence | **Verified Fact.** Script section 2 (SIMULATED). |
| Impact | A mean latency hides the tail. `metric.recommendation_latency` should be read as a median and a 95th percentile. |
| Risk | Medium. A held call at the 10 second timeout is also a tail event. |
| Confidence | High for the file. Unknown for the live model. The stub answers in about 11 ms. |
| Open questions | Open question for S03: `metrics.yaml` has no percentile rule for `metric.recommendation_latency`. This design needs one to report the tail. |

### AB-06

| | |
|---|---|
| Finding | The live audit log already holds tokens and latency for 11 model calls. It holds no held call and no `token_estimate_method`. |
| Evidence | **Verified Fact. REAL.** Script section 6. |
| Impact | `metric.tokens_per_invocation` and `metric.recommendation_latency` can be computed from the log in Half B. Held calls cannot be shown yet, because the log has 0 `policy.hold` rows. |
| Risk | Low |
| Confidence | High |
| Open questions | None. |

## Lifecycle

`cost-per-workflow.md` turns these totals into cost per flow and per incident. `retry-cost-analysis.md` prices the retries. `optimization-backlog.md` lists the savings. `finops-dashboard-fields.md` names the audit fields that feed each metric. `docs/00-contract/cost-envelope.md` carries the reconciliation row. Half B adds `metrics_from_audit.py`.
