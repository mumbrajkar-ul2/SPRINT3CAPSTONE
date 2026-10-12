# Dashboard sketch

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The screen is a text layout. Each panel names one metric id from `metrics.yaml`. No drawing tool is chosen. |
| Evidence sources | `semantic-layer/metrics.yaml`; `docs/08-observability/metric-catalogue.md`; `docs/08-observability/log-schema.md`; `observability/otel-notes.md` |
| Assumptions | One screen is enough for this stage. The nine panels are the nine metric ids. A tenth block lists the audit rows for one `correlation_id`. That block is a trace list of log columns. |
| Unresolved issues | Open question for S03: none. This sketch adds no metric id, no field, and no status word. |
| Residual risks | A later tool can be treated as decided. The tool is PROPOSED only. Owner: Team-Force. No product is named here. |

## What this file is

This file is a text layout of the screen a person would open to explain one business event from stored rows.

`observability/otel-notes.md` lines 7 to 8 say there is no dashboard as code. **Verified Fact.** This stage does not add a dashboard tool. A tool that draws this layout is PROPOSED. Owner: Team-Force.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Screen

The screen has a filter, a trace list, and nine panels. The filter is one `correlation_id` string. Empty means all rows.

```text
Operations trace
Filter: correlation_id = ________

Trace list
  One row per audit line that carries this id, in ts order.
  Columns: ts, correlation_id, actor, role, action, resource, outcome.
  This list is the log. It has no metric id.

Row 1
  [ Panel A  metric.audit_completeness ]
  [ Panel B  metric.recommendation_latency ]
  [ Panel C  metric.ai_outcome_count ]

Row 2
  [ Panel D  metric.tokens_per_invocation ]
  [ Panel E  metric.cost_per_correlated_incident ]

Row 3
  [ Panel F  metric.retry_count ]
  [ Panel G  metric.quarantine_rate ]

Row 4
  [ Panel H  metric.sla_breach_risk ]
  [ Panel I  metric.alarm_storm_size ]
```

## What each panel shows

| Panel | Metric id | What the number is | Where the number is read | Filled from the audit row today |
|---|---|---|---|---|
| A | `metric.audit_completeness` | Filled required fields divided by required fields, for the rows in the filter. | The audit row. Formula in `metric-catalogue.md`. | The current 96 lines can be scored. A read is 3 of 5. A summary is 4 of 8. |
| B | `metric.recommendation_latency` | `latency_ms` for each model call in the filter. | Audit column `latency_ms` after S04-09. Until then, `events.jsonl` field `field.event.latency_ms`. | No. The audit file has no `latency_ms`. |
| C | `metric.ai_outcome_count` | Count of rows for each of the four outcome words. | Audit column `outcome`. | Partly. 7 lines store the word inside `details.outcome`. The column `outcome` does not exist yet. |
| D | `metric.tokens_per_invocation` | Average `tokens` on model rows in the filter. | Audit column `tokens` after S04-09. Until then, `token_count` on the CSV. | No. |
| E | `metric.cost_per_correlated_incident` | Cost of the model calls for one incident. | Not on the fourteen-field row. Source fields are on the YAML entry. | No. The metric cannot be computed today. The YAML says so. |
| F | `metric.retry_count` | Minimum, maximum, and the count at or above the PROPOSED bound of 1000. | `service_orders.csv` column `retry_count`. | No. |
| G | `metric.quarantine_rate` | Rows held aside divided by rows processed. | The batch printout. Today 0 of 354. | No. |
| H | `metric.sla_breach_risk` | The score on one incident, or the count outside the PROPOSED range 0 to 1. | `incidents.csv`. | No. |
| I | `metric.alarm_storm_size` | Alarms in one storm batch after `dedupe_key` is counted once. | `alarms.csv`. | No. |

How to read a row. Panel A is the only panel the current audit file can fill without waiting for S04-09. Panel B's number for the live API is absent. The event file can fill a latency panel, and that panel is then about `events.jsonl`, not about a live call.

The PROPOSED bound of 1000 on panel F and the PROPOSED range 0 to 1 on panel H are notes. Owner: Team-Force. `target` on both metrics is null.

## The trace list and the sample chain

When the filter is `corr-00273`, the trace list is empty. **Verified Fact:** `logs/audit.log` has no `correlation_id` on any of its 96 lines.

The seven event lines for that id can be shown beside the empty list as a second table, with a gap mark on every hop that has no audit row. That table is `incident-reconstruction.md`. The nine metric ids stay the nine panels.

## Findings

### DS-01

| | |
|---|---|
| Finding | The repo has no dashboard. This file is the layout. |
| Evidence | **Verified Fact.** `observability/otel-notes.md` lines 7 to 8: "no dashboard as code". |
| Impact | A person can read the layout and know which metric id sits in which panel. Nothing draws the panels. |
| Risk | Low for this stage. The risk rises if a later stage picks a tool and treats this sketch as an approved build. |
| Confidence | High |
| Open questions | Open question for S03: none. |

### DS-02

| | |
|---|---|
| Finding | Five panels read files other than the audit log. One panel, cost, has no number today. |
| Evidence | **Verified Fact.** Source fields in `metrics.yaml`, matched in `metric-catalogue.md`. |
| Impact | Opening this screen after Half B still leaves panels E through I dependent on CSV files and the batch run. |
| Risk | Medium. A single "operations" number that averages all nine panels would mix a log fraction with a storm count. |
| Confidence | High |
| Open questions | Open question for S03: none. |

## Lifecycle

Stage S04-09 fills the columns panels B and D read. Stage S04-12 is the cost step panel E is waiting on. The panel still needs a correlated incident, which the YAML marks Unknown. Stage S05-14 uses the trace list to rebuild one case.
