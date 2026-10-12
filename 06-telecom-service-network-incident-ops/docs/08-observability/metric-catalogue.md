# Metric catalogue

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. All nine ids in `metrics.yaml` are listed. Each `target` is null. Four of the nine can be computed from the fourteen-field audit row once later stages fill it. Five stay on other files. |
| Evidence sources | `semantic-layer/metrics.yaml` (nine metric ids); `docs/02-baseline/data-quality-baseline.md`; `docs/08-observability/log-schema.md`; `logs/audit.log`; `data/synthetic/events.jsonl`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py` |
| Assumptions | A metric is computed only from the source fields named on its YAML entry. This catalogue adds no metric id and no target. A PROPOSED bound already written in the YAML stays a note. Owner: Team-Force. |
| Unresolved issues | Open question for S03: none in this file. The missing field ids for the log columns are in `log-schema.md`. API availability has no metric id. That question is in `slo-proposal.md`. |
| Residual risks | A reader can treat a `proposed_bound_note` as an approved target. `metrics.yaml` sets `target: null` on every metric. The note stays a proposal. Owner: Team-Force. |

## What this file is

This file lists every metric id in `semantic-layer/metrics.yaml`. For each one it names the source fields, how the number is computed from the log schema, and the target.

The target is null on every metric. **Verified Fact:** `metrics.yaml` lines 3 and 34, and the `target: null` line on each entry. The file says no owner has approved a target.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The nine metrics

### metric.tokens_per_invocation

| | |
|---|---|
| Id | `metric.tokens_per_invocation` |
| Unit | tokens |
| Source fields | `field.ai_invocation.token_count` |
| How the log schema computes it | Sum of `tokens` on audit rows where `tokens` is not null, divided by the count of those rows. One row uses its own `tokens` value. |
| What the log can do today | The audit row has no `tokens` key. The live body returns `token_estimate` as `len(prompt.split()) * 2`. The value for REC-0001 was 64. The gateway does not write the CSV. **Verified Fact:** `metrics.yaml` `live_source` and `today`. |
| Today, from the YAML | The CSV holds 353 numeric `token_count` values. The simulated sum in the cost envelope is 845675. That sum is a lab figure. |
| Target | null |

Stage S04-09 writes `tokens`. Until then this metric stays on the CSV, and the CSV and the live body never meet.

### metric.cost_per_correlated_incident

| | |
|---|---|
| Id | `metric.cost_per_correlated_incident` |
| Unit | cost_units per incident |
| Source fields | `field.ai_invocation.incident_id`, `field.ai_invocation.token_count`, `field.event.cost_units`, `field.incident.incident_id` |
| How the log schema computes it | The YAML sum needs an incident id and `cost_units`. The fourteen fields include neither. `tokens` arrives on the row at S04-09. Stage S04-12 turns tokens into a cost. The join from an alarm to an incident is still Unknown. |
| Today, from the YAML | No incident is correlated yet. `events.jsonl` has `cost_units` with an Unknown money unit. The hosted-model price is Unknown. |
| Target | null |

Worked example from the sample chain. The seven lines of `corr-00273` sum to 16.734 in `cost_units`. **Verified Fact. REAL.** The money unit is Unknown. The seven lines name tables, not one incident id, so the sum is not this metric.

### metric.quarantine_rate

| | |
|---|---|
| Id | `metric.quarantine_rate` |
| Unit | fraction of rows |
| Source fields | `field.device.device_id` |
| How the log schema computes it | The source is the batch run: rows held aside divided by rows processed. The audit row has no batch count, so the number stays on the batch printout. |
| Today, from the YAML | `etl/run_daily_batch.py` printed processed 354 and malformed 1. It held nothing aside. The rate today is 0 of 354, while 1 row is known bad. Where a held-aside row would go is Unknown. |
| Target | null |

### metric.retry_count

| | |
|---|---|
| Id | `metric.retry_count` |
| Unit | retries |
| Source fields | `field.service_order.retry_count` |
| How the log schema computes it | Retry counts live on `service_orders.csv`. The audit row has no retry column, so the number stays on that file. |
| Today, from the YAML and the baseline | 353 numeric values. Minimum 32. Maximum 4995. 294 at or above 1000. **Verified Fact:** `docs/02-baseline/data-quality-baseline.md`. |
| Target | null |
| Note already in the YAML | The baseline uses 1000 as a PROPOSED bound so the odd case is counted. Owner: Team-Force. The metric `target` stays null. |

### metric.audit_completeness

| | |
|---|---|
| Id | `metric.audit_completeness` |
| Unit | fraction of required fields present |
| Source fields | `field.event.correlation_id`, `field.event.actor` |
| How the log schema computes it | For one audit row, count the required fields that are filled and divide by the count of required fields. The metric's required fields are `ts`, `action`, `actor`, `correlation_id`, `record_id`, and, for a model call, `model`, `approval_id`, and `policy_result`. |
| What the log can do today | A `record.read` row fills 3 of 5. An `ai.summary` row fills 4 of 8. The arithmetic is in `log-schema.md`. `record_id` is in this formula and is not one of the fourteen columns. |
| Today, from the YAML | No row has `actor`, `correlation_id`, `approval_id`, or `policy_result`. |
| Target | null |
| Note already in the YAML | The required-field list is PROPOSED. Owner: Team-Force. `proposed: true`. |

### metric.recommendation_latency

| | |
|---|---|
| Id | `metric.recommendation_latency` |
| Unit | milliseconds |
| Source fields | `field.event.latency_ms` |
| How the log schema computes it | The `latency_ms` value on one audit row where the model call ran. For a set of rows, the same subtraction the YAML states: answer time minus request time, stored as that integer. |
| What the log can do today | The audit row has no `latency_ms`. The live gateway waits `time.sleep(0.01)` and records nothing. **Verified Fact:** `ai_gateway.py` line 9. `provenance.latency_ms` has `present_today: false`. |
| Today, from the event file | `events.jsonl` holds `latency_ms` on all 3000 lines. **Verified Fact:** `metrics.yaml`. Recount 2026-10-11: minimum 15, median 776, 95th by nearest rank 13627, maximum 14992. That file is not the live API. |
| Target | null |

### metric.sla_breach_risk

| | |
|---|---|
| Id | `metric.sla_breach_risk` |
| Unit | score |
| Source fields | `field.incident.sla_breach_risk` |
| How the log schema computes it | The score sits on the incident row. The audit row leaves it there. The YAML says the repo states no formula for how the score is made. |
| Today, from the YAML and the baseline | 352 values between 0 and 1. `INC-00019` holds 1.42. One cell is blank. |
| Target | null |
| Note already in the YAML | The baseline uses 0 to 1 inclusive as a PROPOSED range. Owner: Team-Force. The metric `target` stays null. |

### metric.alarm_storm_size

| | |
|---|---|
| Id | `metric.alarm_storm_size` |
| Unit | alarms |
| Source fields | `field.alarm.storm_batch_id`, `field.alarm.dedupe_key` |
| How the log schema computes it | Storm size is a count of alarm rows that share `storm_batch_id`. The audit row has no `storm_batch_id`, so the number stays on `alarms.csv`. |
| Today, from the YAML | 351 distinct `storm_batch_id` values. Three appear twice. The largest batch in the file is 2 rows. How many alarms make a storm is Unknown. |
| Target | null |

### metric.ai_outcome_count

| | |
|---|---|
| Id | `metric.ai_outcome_count` |
| Unit | calls |
| Source fields | `field.ai_invocation.guardrail_status`, `field.ai_invocation.approval_required` |
| How the log schema computes it | For each of the four outcome words, count audit rows whose `outcome` equals that word. |
| What the log can do today | 7 audit lines store `details.outcome`: 5 are `RECOMMEND_ONLY` and 2 are `BLOCK`. The word sits inside `details`. The top-level column `outcome` is still absent. The CSV columns hold the generic status words. The YAML says the metric is 0 for all four outcomes, because no live call recorded an outcome when that sentence was written. **Verified Fact** for the 7 lines counted 2026-10-11. **Inference:** those 7 lines are newer than the YAML sentence. |
| Target | null |
| Note already in the YAML | `proposed: true`. Owner: Team-Force. |

The four words are `outcome.recommend_only` (`RECOMMEND_ONLY`), `outcome.hold_for_review` (`HOLD_FOR_REVIEW`), `outcome.block` (`BLOCK`), and `outcome.execute` (`EXECUTE`).

## Which metrics the audit row can feed

| Metric id | Computed from the fourteen-field audit row |
|---|---|
| `metric.tokens_per_invocation` | Yes, after S04-09 fills `tokens`. |
| `metric.audit_completeness` | Yes, with the gap that `record_id` is outside the fourteen fields. |
| `metric.recommendation_latency` | Yes, after S04-09 fills `latency_ms`. |
| `metric.ai_outcome_count` | Yes, once `outcome` is the top-level field. |
| `metric.cost_per_correlated_incident` | No. Needs an incident id and a cost. S04-12 uses the row. It does not add those source fields by itself. |
| `metric.quarantine_rate` | No. Batch run. |
| `metric.retry_count` | No. `service_orders.csv`. |
| `metric.sla_breach_risk` | No. `incidents.csv`. |
| `metric.alarm_storm_size` | No. `alarms.csv`. |

## Findings

### MC-01

| | |
|---|---|
| Finding | Every metric id has `target: null`. Two entries carry a PROPOSED bound note. One entry carries a PROPOSED required-field list. |
| Evidence | **Verified Fact.** `metrics.yaml` for `metric.retry_count`, `metric.sla_breach_risk`, and `metric.audit_completeness`. Owner on each note: Team-Force. |
| Impact | A dashboard can show the computed number. It cannot draw an approved pass line. |
| Risk | Medium. A later chart that uses 1000 retries or the 0-to-1 score as a red line would present a proposal as a rule. |
| Confidence | High |
| Open questions | Open question for S03: none. |

### MC-02

| | |
|---|---|
| Finding | Four metrics can move onto the audit row. Five cannot. Cost per incident needs fields the fourteen-field row does not have. |
| Evidence | **Verified Fact.** Source fields on each YAML entry, compared with the fourteen names in `log-schema.md`. |
| Impact | A trace screen that only reads `logs/audit.log` can show completeness, latency, tokens, and outcome counts after the later stages fill those columns. Storm size, retry, quarantine, and the SLA score stay on the CSV files and the batch printout. |
| Risk | Medium. Stage S04-12 can compute a cost from tokens and still be unable to divide by one correlated incident, because the alarm-to-incident join is Unknown. |
| Confidence | High |
| Open questions | Open question for S03: none. |

## Lifecycle

The ids are the ids in `metrics.yaml`. The blank-id facts that feed `metric.audit_completeness` are in `docs/02-baseline/data-quality-baseline.md`. Stage S04-09 fills the model fields the token and latency metrics read. Stage S04-12 computes cost from the audit row. Stage S05-14 rebuilds a case from the same row.
