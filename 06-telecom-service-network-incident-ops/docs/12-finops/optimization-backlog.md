# Optimization backlog

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Four items are listed, each with a saving mechanism, a metric, and an owner. One item that saves cost is already built. No saving figure is measured on live traffic, so every saving figure is EDUCATIONAL. |
| Evidence sources | `docs/12-finops/cost_baseline.py` section 5 and `cost_baseline_output.txt`; `docs/11-reliability/recovery-evidence.md` (DR-3, DR-4); `docs/11-reliability/idempotency-plan.md`; `docs/11-reliability/retry-and-circuit-breaker-strategy.md`; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/cost-envelope.md`; `docs/08-observability/log-schema.md`; `semantic-layer/metrics.yaml`; `apps/api/services/ai_gateway.py`; `data/synthetic/alarms.csv`; `data/synthetic/events.jsonl` |
| Assumptions | Team-Force owns every PROPOSED item (operating contract row 10). A model call costs about 90 tokens on the live prompt (EDUCATIONAL, one device row). The EDUCATIONAL rate is 1.0 educational unit per 1000 tokens. PROPOSED. Owner: Team-Force. |
| Unresolved issues | The live repeat rate of prompts is Unknown. The number of alarms that make a storm is Unknown. The price per token is Unknown. The cache lifetime is decided at 300 seconds, with no measured basis (see "Decisions"). |
| Residual risks | A saving figure can be read as a target. None here is a target. A cache can return an answer for a record that changed, if the key does not cover the record fields. |

## What this file is

This file lists ways to cut model cost, from the baseline in `ai-cost-baseline.md`. Each item has a saving mechanism, a metric from `metrics.yaml` that will show the effect, and an owner. No saving figure is stated without a label.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Number labels: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## Summary

| Id | Item | Saving mechanism | Metric that shows it | Saving figure | Owner | Status |
|---|---|---|---|---|---|---|
| OB-01 | Cache repeated prompts by `prompt_hash` | Same prompt text gets the stored answer. No second model call. | `metric.tokens_per_invocation` (sum over a window) | 4 of 5 calls saved in the DR-3 case. EDUCATIONAL. | Team-Force | DECIDED lifetime 300 s. Build in S07. |
| OB-02 | Batch alarm summaries per `storm_batch_id` | One call for the whole batch, not one per alarm. | `metric.alarm_storm_size`, `metric.tokens_per_invocation` | 3 of 353 calls in the file. EDUCATIONAL. | Team-Force | PROPOSED |
| OB-03 | No model call for the eight capabilities S2Q gave to rules | A guard allows a model call only for the three GenAI capabilities. | `metric.ai_outcome_count`, `metric.retry_count` | Avoids the retry what-if of 84,878.46 educational units. EDUCATIONAL. | Team-Force | PROPOSED |
| OB-04 | Replace the word-count formula and the teaching rate | A real tokenizer and a real price turn EDUCATIONAL numbers into REAL ones. | `metric.tokens_per_invocation`, `metric.cost_per_correlated_incident` | None. This item makes the others measurable. | Team-Force | PROPOSED only |
| OB-05 | Stop before the model (already built) | The policy check and the breaker refuse a call before any model call. | `metric.ai_outcome_count` | Model called 0 times in the stale-flag drill. Test run, REAL. | Team-Force | Built in S04-09 and S04-11 |

Every saving figure above is explained in its own section.

## OB-01. Cache repeated prompts by `prompt_hash`

| | |
|---|---|
| What happens today | **Verified Fact.** The summary route has no idempotency key. Five identical calls make five model calls and five audit rows (`recovery-evidence.md` DR-3, test `test_dr3_the_summary_route_has_no_key_so_five_calls_cost_five_model_calls_and_five_rows`, REAL). |
| Proposed change | Before a model call, look up the `prompt_hash` of the prompt. If a stored answer exists for that hash, return it. Run the output policy on that answer again. Write an audit row that says no model ran. |
| Saving mechanism | A repeat of the same prompt costs 0 tokens. The first call pays. In the DR-3 case, 1 call instead of 5. That saves 4 calls and, at 90 tokens a call, 360 tokens. Both figures EDUCATIONAL. |
| Metric | `metric.tokens_per_invocation`, read as the sum of `tokens` over a window. The sum falls when repeats are served from the cache. |
| Measured repeat rate in stored data | 0 repeated `payload_hash` values in `events.jsonl` (SIMULATED). `payload_hash` is the hash of an event, not of a prompt, so this says nothing about prompts. `ai_invocations.csv` has no `prompt_hash` column. The live repeat rate is **Unknown**. |
| Owner | Team-Force |
| Conditions | The prompt holds the allow-list field values, so a changed record gives a new hash (**Inference** from `build_prompt`). A stale or blank `stale_topology_flag` still stops the call before the cache is read. The lifetime is 300 seconds. See "Decisions". A lifetime of "until the record changes" needs a record version, which does not exist. |
| Relation to idempotency | `idempotency-plan.md` leaves the summary route without a key. A cache lowers cost and does not make the route idempotent. The two stay separate. |
| Risk | Medium. A wrong cached answer repeats. The policy check after the cache limits this. |

Open question for S03: `metrics.yaml` has no metric for repeated prompts. This design needs a metric for the share of audit rows that carry a `prompt_hash` seen before, so the saving can be shown.

## OB-02. Batch alarm summaries per `storm_batch_id`

| | |
|---|---|
| What happens today | **Verified Fact.** No code reads `alarms.csv` (`idempotency-plan.md`). The live prompt holds device fields only. There is no alarm summary call to batch. This item is a design rule for stage S07. |
| Proposed change | When a summary of alarms is built, make one call per `storm_batch_id`. Do not make one call per alarm. |
| Saving mechanism | The model is called once for the batch. The fixed instruction text is sent once. |
| Size in the data | 353 alarm rows have both keys. They form 350 `storm_batch_id` values. The largest batch has 2 rows. One call per alarm would be 353 calls. One call per batch is 350. That saves 3 calls (SIMULATED data, EDUCATIONAL what-if). |
| Worked example | A storm of 100 alarms. One call per alarm is 100 calls. One call per storm is 1 call. That saves 99 calls. EDUCATIONAL. |
| Limit on the saving | The batch prompt grows with each alarm line. The token saving is smaller than the call saving. Only the repeated instruction text is saved. The size of that saving is Unknown. |
| Metric | `metric.alarm_storm_size` shows how many alarms share a batch. `metric.tokens_per_invocation` shows calls fall while tokens per call rise. |
| Owner | Team-Force |
| Conditions | How many alarms make a storm is Unknown (`metric.alarm_storm_size`). The batch size limit for one prompt is Unknown. The prompt allow list names device fields, so an alarm prompt needs new allowed fields from S03. |
| Risk | Low for cost. Medium for quality. A long batch may hide one important alarm. |

Open question for S03: `ai-context-policy.yaml` allows device fields only in the prompt. This design needs allowed alarm fields, such as `storm_batch_id` and `alarm_type`, before a batch summary can be built.

## OB-03. Do not call the model for capabilities S2Q gave to rules

| | |
|---|---|
| What happens today | **Verified Fact.** `ai-qualification.md` assigns eight capabilities to rules, deterministic code, or workflow automation. `cost-envelope.md` sets their hosted-model cost to 0 by Assignment. No route calls the gateway for them. |
| Proposed change | Keep it that way with a guard. The gateway accepts a call only for incident summary, next-action recommendation, and configuration suggestion. A test fails if a route for one of the other eight calls the gateway. |
| Saving mechanism | The cost of any model call in those eight capabilities stays 0. The most expensive mistake would be a model call inside the order retry loop. The what-if from `retry-cost-analysis.md` is 84,878.46 educational units on the live estimate and 2,259,351.33 on the CSV mean. EDUCATIONAL. |
| Metric | `metric.ai_outcome_count` (calls per outcome) and `metric.retry_count`. Both should show no model call from those capabilities. |
| Owner | Team-Force |
| Conditions | The audit row has no field for which capability made the call. The guard can be a test on routes, and the metric cannot split calls by capability. |
| Risk | Low |

Open question for S03: the 14-field audit row in `log-schema.md` has no `capability` field. This design needs one field to count model calls for each of the three model capabilities.

## OB-04. Replace the word-count formula and the teaching rate

| | |
|---|---|
| What happens today | **Verified Fact.** `tokens` uses `len(prompt.split()) * 2`. `Project_Intent.md` Appendix B calls that EDUCATIONAL "unless you replace the formula with a real tokenizer and a real model bill". No price exists in the repo. |
| Proposed change | PROPOSED only. Use the tokenizer of the chosen model. Take the price from the provider's invoice. Move the EDUCATIONAL rate into settings with a name. Half B reads the rate from settings and does not add a billing integration. |
| Saving mechanism | None directly. The change lets every figure in this folder move from EDUCATIONAL to REAL. |
| Metric | `metric.tokens_per_invocation` and `metric.cost_per_correlated_incident` change label from EDUCATIONAL to REAL. |
| Owner | Team-Force |
| Conditions | A hosted model must be chosen. The model name, the provider, and the price are Unknown. |
| Risk | Low |

## OB-05. Stop before the model (already built)

| | |
|---|---|
| What happens today | **Verified Fact.** Stage S04-09 stops a call before the model when the id is missing, the stale flag is true, or the stale flag is blank. Stage S04-11 refuses a call when the breaker is open or 10 calls are already running. |
| Evidence | `recovery-evidence.md` DR-4: with a true stale flag the model is called 0 times (REAL, test run). With a blank flag it is called 0 times. With the breaker open, 0 new calls. |
| Saving mechanism | A blocked or held call makes no model call and uses 0 tokens. |
| Metric | `metric.ai_outcome_count`. The `BLOCK` and `HOLD_FOR_REVIEW` counts are the calls avoided. Half B counts held rows, where `tokens` is null, apart from the average. |
| Size in the data | 192 device rows have a true stale flag and 1 is blank (`recovery-evidence.md` DR-4, REAL). If every one were summarized, that is 193 calls. The live traffic mix is Unknown. |
| Owner | Team-Force |
| Limit | The three breaker numbers (5 failures, 30 seconds, 10 calls at once) are PROPOSED. Owner: Team-Force. |

## Decisions (2026-10-11)

Mangesh (FDE) asked for final values. Owner of both: Team-Force. Neither value is measured. Both are judgment calls from the facts below, and each has a trigger to review it.

### Decision 1. Educational rate: keep 1.0 educational unit per 1000 tokens

| | |
|---|---|
| Value | 1.0 educational unit per 1000 tokens. Setting `FINOPS_EDU_RATE_PER_1K`. Unchanged. |
| Label | EDUCATIONAL. The unit is not money and not a currency. |
| Why this value | The repo has no price, no provider, and no model name. Any rate that looks like a real price in dollars would be read as a bill. A plain 1.0 makes the arithmetic easy to check by hand: 90 tokens is 0.09 units. The numbers still show which flow or call costs more than another. |
| What it cannot do | It cannot say what a call costs in money. The money cost stays Unknown. |
| Review trigger | A hosted model is chosen. Then OB-04 replaces the word-count formula with a real tokenizer and the rate with the provider's price, and the label moves from EDUCATIONAL to REAL. |

### Decision 2. Cache lifetime for OB-01: 300 seconds

| | |
|---|---|
| Value | A stored answer may be reused for 300 seconds (5 minutes) from the moment it was stored. |
| Status | DECIDED. Not measured. Built in stage S07. Owner: Team-Force. |
| Why 300 seconds | The cache exists to stop the same person or system asking the same question again and again in a short time. The S04-11 drill DR-3 shows that case: five identical calls in a row. In a network operations centre a person watches one incident for a few minutes, refreshes, and asks again. Five minutes covers that. It is also short against the life of an alarm storm, so an answer about a changing situation does not stay long. It is 30 times the 10 second model timeout and 10 times the 30 second breaker window, so one outage does not outlive the cache by much. |
| What goes in the cache | An answer is stored only when the outcome is `RECOMMEND_ONLY`. A `BLOCK`, a `HOLD_FOR_REVIEW`, a timeout, and a bad answer are never stored. |
| What the key holds | `prompt_hash`, `model_version`, and the policy version. A change in any one gives a new key. |
| What runs before the cache | The access check and the stale-flag check run first, every time. A true or blank stale flag stops the call before the cache is read. The output check runs again on a stored answer before it is shown. |
| Clear at once | The cache is emptied when the policy version or the model version changes. |
| Size limit | 500 stored answers in memory, oldest removed first. One process only, like the dedupe memory and the audit lock (`recovery-evidence.md`). A restart empties it. |
| Audit | A cache hit writes an audit row with `model` null, `tokens` null, `latency_ms` null, and `outcome` `RECOMMEND_ONLY`. The row must say a stored answer was used. Open question for S03: the audit row has no field for "served from cache". This design needs one, so a cache hit is not counted as a held row or a model call. |
| What it saves | In the DR-3 case, 4 of 5 calls and 360 tokens. EDUCATIONAL. The live repeat rate is Unknown. |
| Review trigger | Stage S07 traffic shows the real gap between repeat calls. `metrics_from_audit.py` already prints the share of calls that repeat a `prompt_hash`. If most repeats come after more than 300 seconds, lengthen it. If the policy or the device data changes more often than every 5 minutes, shorten it. |

Telecom reason for the short lifetime. A device summary describes alarms and topology that can change within minutes during a fault. A stale recommendation is worse than a repeated model call, because a person may act on it. The cost of the extra call is small (0.09 educational units on the live prompt).

## Order of work

PROPOSED order. Owner: Team-Force. The order is by effort and risk, and it is not a measured ranking.

1. OB-03. A guard and a test. It stops the worst cost mistake.
2. OB-04. It makes every later saving measurable. It needs a chosen model.
3. OB-01. The lifetime is decided. The build waits for stage S07.
4. OB-02. It waits for stage S07 and for allowed alarm fields.

## Findings

### OB-F1

| | |
|---|---|
| Finding | No saving here is measured on live traffic. All saving figures are EDUCATIONAL. |
| Evidence | **Verified Fact.** The live audit log holds 11 model-call rows from tests (REAL, script section 6). The repeat rate in stored data is 0 and does not describe prompts. |
| Impact | The backlog says where cost can fall. It does not say by how much. |
| Risk | Medium. A reader may read the DR-3 figure as a rate. |
| Confidence | High |
| Open questions | The live volume and repeat rate. Unknown until S07 runs. |

### OB-F2

| | |
|---|---|
| Finding | The largest saving that is already in place is the refusal before the model. The largest saving still open depends on traffic that does not exist yet. |
| Evidence | **Verified Fact.** OB-05 and DR-4. Stored alarm data shows batches of 1 to 2 rows. |
| Impact | Batching saves little in this data. Caching saves nothing that the data can show. |
| Risk | Low |
| Confidence | Medium |
| Open questions | The number of alarms in a real storm. Unknown. |

## Lifecycle

`finops-dashboard-fields.md` lists the audit fields behind each metric named above. Half B computes `metric.tokens_per_invocation` and counts held rows. Stage S07 builds the route that would use OB-01 and OB-02. Stage S09 cites OB-05 as a cost guard.
