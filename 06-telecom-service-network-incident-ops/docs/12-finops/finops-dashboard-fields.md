# FinOps dashboard fields

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Each of the seven metrics has its source fields named. Four metrics can be computed from the audit log in Half B. Two metrics have no source in the audit log. One metric cannot be computed as defined. |
| Evidence sources | `docs/08-observability/log-schema.md` (the 14 fields); `semantic-layer/metrics.yaml`; `logs/audit.log` (211 lines, counted 2026-10-11); `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `docs/11-reliability/recovery-evidence.md`; `docs/12-finops/cost_baseline.py` section 6; `docs/00-contract/cost-envelope.md` |
| Assumptions | A model call has a non-null `model`. A held call has `model`, `tokens`, and `latency_ms` null (**Verified Fact:** `recovery-evidence.md`). The EDUCATIONAL rate will come from settings in Half B. PROPOSED. Owner: Team-Force. |
| Unresolved issues | The audit row has no `record_id`, no capability, no flow name, and no `token_estimate_method`. `metric.quarantine_rate` and `metric.retry_count` have no audit field. |
| Residual risks | Rows written before stage S04-09 have `tokens` null and still look like model calls. A reader who treats null as held will count them wrongly. |

## What this file is

This file names the audit fields that feed each metric in `metrics.yaml`. A dashboard reads these fields. Half B turns them into a table in `metrics_from_audit.py`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Number labels: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## The six fields the playbook names

**Verified Fact.** All six are among the 14 fields in `log-schema.md`. Counts below are over the 115 audit rows written in the new shape. The other 96 rows have three keys only. All counts REAL, from `logs/audit.log`, written by test runs and demo calls on this machine.

| Field | Meaning | Written by | Rows with a value today | Feeds |
|---|---|---|---|---|
| `tokens` | Tokens used by one model call. Null when no model ran. | `ai_gateway.py` line 312 | 11 of 115 | `metric.tokens_per_invocation`, `metric.cost_per_correlated_incident` |
| `latency_ms` | Milliseconds from request to answer. Null when no model ran. | `ai_gateway.py` line 329 | 11 of 115 | `metric.recommendation_latency` |
| `model` | Model name. The live value is `local-sim-v1`. | `ai_gateway.py` `provenance()` | 11 of 115 | Grouping for the three metrics above |
| `model_version` | Version text. The live value is `local-sim-v1`, the same as the name. | `ai_gateway.py` `provenance()` | 11 of 115 | Grouping, so a model change does not mix figures |
| `outcome` | `RECOMMEND_ONLY`, `HOLD_FOR_REVIEW`, `BLOCK`, or `EXECUTE`. | `main.py` | 13 of 115 (all `RECOMMEND_ONLY`) | `metric.ai_outcome_count`, and the filter for latency |
| `correlation_id` | The request chain id. | `main.py` | 115 of 115 | Grouping for `metric.cost_per_correlated_incident` |

Two more fields support the dashboard. `ts` is the window for every metric. `prompt_hash` is the key for the cache saving in `optimization-backlog.md` (OB-01). `prompt_hash` has a value on 11 of 115 rows.

Worked example. One live call on 2026-10-12 UTC wrote `tokens` 90, `latency_ms` 11, `model` `local-sim-v1`, `outcome` `RECOMMEND_ONLY`, and a `correlation_id`. Those six fields give one point on the tokens chart and one point on the latency chart. The 90 is EDUCATIONAL. The 11 is REAL, and it is the time the 0.01 second stub took.

## Metric by metric

| Metric | Source fields in the audit log | How to read them | Today (REAL) | Gap |
|---|---|---|---|---|
| `metric.tokens_per_invocation` | `tokens`, `model`, `model_version`, `ts` | Sum of `tokens` over rows where `model` is not null, divided by the count of those rows. Group by `model` and `model_version`. | 11 rows, mean 90.0. EDUCATIONAL. | Rows from before S04-09 have `tokens` null with no way to tell them from held rows (see below). |
| `metric.cost_per_correlated_incident` | `tokens`, `correlation_id`, `model`, plus a rate from settings | Sum of `tokens` per `correlation_id`, times the EDUCATIONAL rate. | Computable per chain for 11 rows. EDUCATIONAL. | No incident id on the row. As defined, the metric stays Unknown. |
| `metric.quarantine_rate` | None | The ETL prints `quarantined` to its output. It is not in the audit log. | Not in the log. | A gap. The number comes from `etl/run_daily_batch.py` output (S04-11). |
| `metric.retry_count` | None | The value is `retry_count` in `service_orders.csv`. No audit row records a retry. | Not in the log. | A gap. No code reads orders (`idempotency-plan.md`). |
| `metric.audit_completeness` | All 14 fields. `correlation_id` and `actor` are in the required list. | Filled required fields divided by required fields, per row. | `actor` filled on 72 of 115. `approval_id` 0 of 115. `policy_decision` 0 of 115. | The required list names `record_id`, which has no column (LS-Q7). |
| `metric.recommendation_latency` | `latency_ms`, `outcome`, `model` | Median and 95th percentile of `latency_ms` over rows where `model` is not null. | 11 rows, 11 to 14 ms, mean 11.3. REAL, stub. | The stub is 0.01 s. A real model's value is Unknown. No percentile rule in the YAML. |
| `metric.ai_outcome_count` | `outcome` | Count of rows per outcome word. | 13 rows, all `RECOMMEND_ONLY`. | The 43 `policy.deny` rows have `outcome` null. Whether any of them is a `BLOCK` outcome is Unknown. The `BLOCK` count in the log is 0 today. |

### Held calls

A held call makes no model call. Its `model`, `tokens`, and `latency_ms` are null. The count of held rows is its own number. It must not enter the mean of `tokens` or `latency_ms`, because that would lower both.

**Verified Fact.** The log has 0 rows with action `policy.hold` today (script section 6). Two `ai.summary` rows in the new shape have `outcome` `RECOMMEND_ONLY` and `tokens` null. **Inference:** they were written after S04-08 and before S04-09, when `tokens` was always null. They are not held calls. Half B reports them as "rows with no token value" and keeps them out of the held count.

### Fields that no metric can read yet

| Missing item | What the dashboard needs it for | Where it would come from |
|---|---|---|
| Incident id on the audit row | `metric.cost_per_correlated_incident` | `record_id` is not one of the 14 fields (LS-Q7) |
| Flow name on the audit row | Cost per flow from the log | `event_type` is on events only |
| Capability name on the audit row | Calls per model capability (OB-03) | None |
| `token_estimate_method` | Carry the EDUCATIONAL label on every row | Added by Half B |
| ETL `quarantined` count | `metric.quarantine_rate` | ETL output, not the log |
| Retry events | `metric.retry_count` | `service_orders.csv`, not the log |

Open question for S03: `log-schema.md` has no field for the incident id, the flow name, or the model capability on an audit row. This design needs those fields so cost can be grouped by incident, by flow, and by capability.

Open question for S03: the YAML has no field id for `token_estimate_method`. This design needs one so each `tokens` value says whether it is a word-count estimate or a real tokenizer count.

Open question for S03: `metric.quarantine_rate` names `field.device.device_id` as its only source field and no audit field. This design needs a stored place for the ETL `quarantined` count, so the dashboard can read it.

## Findings

### FD-01

| | |
|---|---|
| Finding | The six fields the playbook names are in the audit row and filled on every model call. |
| Evidence | **Verified Fact. REAL.** 11 of 11 model-call rows hold `tokens`, `latency_ms`, `model`, `model_version`, and `prompt_hash`. |
| Impact | Tokens and latency per call can be computed from the log in Half B. |
| Risk | Low |
| Confidence | High |
| Open questions | None. |

### FD-02

| | |
|---|---|
| Finding | Two of the seven metrics have no audit field: `metric.quarantine_rate` and `metric.retry_count`. |
| Evidence | **Verified Fact.** `metrics.yaml` source fields. `log-schema.md` field list. |
| Impact | A FinOps table built from the audit log cannot show those two metrics. |
| Risk | Low. Neither metric is a model-cost metric. |
| Confidence | High |
| Open questions | The open question about the ETL count is above. |

### FD-03

| | |
|---|---|
| Finding | Cost per incident, per flow, and per capability cannot be read from the audit row. |
| Evidence | **Verified Fact.** The 14 fields have no incident, flow, or capability field. |
| Impact | Half B can group cost by `correlation_id` only. |
| Risk | Medium. A chain is not an incident (`cost-per-workflow.md`). |
| Confidence | High |
| Open questions | Three fields for S03, above. |

### FD-04

| | |
|---|---|
| Finding | Null `tokens` does not always mean a held call. |
| Evidence | **Verified Fact. REAL.** 2 of 13 `ai.summary` rows in the new shape have `tokens` null and `outcome` `RECOMMEND_ONLY`. 0 rows are `policy.hold`. |
| Impact | A mean taken over all `ai.summary` rows would be too low, and a held count taken from null tokens would be too high. |
| Risk | Medium |
| Confidence | Medium. The explanation for the two rows is an Inference. |
| Open questions | None. Half B reads `model` not null as the test for a model call. |

## Lifecycle

`ai-cost-baseline.md` states the figures these fields will reproduce. Half B adds `metrics_from_audit.py`, which reads the fields in the second table. Stage S05-14 rebuilds a case from rows that share one `correlation_id`. Stage S07 shows one labelled number from these fields.

## Update after Half B (2026-10-11)

Half B ran a `BLOCK` case through the real route (stale flag true, `DEV-00003`). The route wrote a `policy.deny` row with `outcome` `BLOCK`. So a `policy.deny` row can hold the `BLOCK` word, and `metric.ai_outcome_count` counts it. The Half A line "whether any of them is a BLOCK outcome is Unknown" is now answered: the route does write it. The 43 older `policy.deny` rows in the Half A count are role denials with no outcome word. Details are in `evidence.md`.
