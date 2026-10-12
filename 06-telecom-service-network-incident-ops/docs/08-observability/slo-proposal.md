# SLO proposal

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Three service levels are proposed. Each number is PROPOSED. Owner: Team-Force. None is a target in `metrics.yaml`. |
| Evidence sources | `observability/otel-notes.md`; `semantic-layer/metrics.yaml` (`metric.recommendation_latency`, `metric.audit_completeness`); `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `logs/audit.log`; `data/synthetic/events.jsonl`; `docs/02-baseline/data-quality-baseline.md`; `docs/00-contract/operating-contract.md` row 10 |
| Assumptions | Team-Force owns every PROPOSED number. Operating contract row 10. The owner name records who must confirm the number. The live path and `events.jsonl` are different stores. A bound taken from the event file describes that file. The live service level is the PROPOSED number in this file. |
| Unresolved issues | Open question for S03: there is no metric id for API availability. This design needs that id so the availability service level maps to `metrics.yaml` the way recommendation latency maps to `metric.recommendation_latency`. |
| Residual risks | A reader can copy 99 of 100, or 2000 milliseconds, or 1.0, into a dashboard as an approved line. They are proposals. `target` stays null until Team-Force accepts one in writing. |

## What this file is

This file proposes three service levels. Each one says what the repo can show today, then states a PROPOSED number and the owner who must confirm it.

`observability/otel-notes.md` line 6 says there are no SLOs. **Verified Fact.**

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## 1. API availability

**What the repo gives today.** Unknown.

`GET /health` returns a body with `status` `ok` and the repo name when the process handles the call. **Verified Fact:** `main.py` lines 9 to 11. `status.code.health.ok`. The route writes no audit row.

The repo stores no count of health calls, no count of failed calls, and no uptime series. **Verified Fact:** `otel-notes.md` has no availability figure. `metrics.yaml` has no availability id.

**PROPOSED number.** In one calendar day, 99 of every 100 calls to `GET /health` return HTTP 200 and body `status` `ok`.

**Owner who must confirm.** Team-Force.

The repo stores no health-call count, so today's availability stays Unknown. The PROPOSED number waits for Team-Force. `metrics.yaml` has no availability target and no availability id. See the open question below.

## 2. Recommendation latency

**What the repo gives today.** Unknown for the live API as a service level.

The live gateway waits `time.sleep(0.01)` and returns. That wait is 10 milliseconds. It writes no `latency_ms` on the body or the audit row. **Verified Fact:** `ai_gateway.py` line 9. `provenance.latency_ms` has `present_today: false`. `metric.recommendation_latency` `target` is null.

`events.jsonl` stores `latency_ms` on all 3000 lines. That file is not the live API. **Verified Fact. REAL.** Recount 2026-10-11:

| Item | Milliseconds |
|---|---|
| Minimum | 15 |
| Median | 776 |
| 95th, nearest rank | 13627 |
| Maximum | 14992 |

540 of 3000 lines are at or above 10000 milliseconds. **Verified Fact. REAL.**

**PROPOSED number.** 95 of every 100 live recommendation calls finish in 2000 milliseconds or less. The stored field is `latency_ms` on the audit row.

**Owner who must confirm.** Team-Force.

The proposal applies to the live call after S04-09 records `latency_ms`. The 13627 millisecond figure stays a fact about the event file. `metric.recommendation_latency` keeps `target: null` until Team-Force accepts a target.

## 3. Audit completeness

**What the repo gives today.** A number can be computed for the current log. It is not an approved service level.

`metric.audit_completeness` defines the fraction. The required-field list is already PROPOSED. Owner: Team-Force. `target` is null. **Verified Fact:** `metrics.yaml`.

Applied to `logs/audit.log` (96 lines, counted 2026-10-11):

| Row kind | Filled required fields | Fraction |
|---|---|---|
| `record.read` | `ts`, `action`, `record_id` | 3 of 5 |
| `ai.summary` | `ts`, `action`, `record_id`, `model` | 4 of 8 |
| `policy.deny` | `ts`, `action`, `record_id` | 3 of 5 |

The key counts are **Verified Fact. REAL.** The fraction is the metric formula. Treating `policy.deny` as a non-model row is an **Inference**. The metric text does not name that action.

No row fills `actor`, `correlation_id`, `approval_id`, or `policy_result`. **Verified Fact.**

**PROPOSED number.** Completeness is 1.0 on the metric's required fields. Every required field on the row is filled. A model-call row includes `model`, `approval_id`, and `policy_result` in that set.

**Owner who must confirm.** Team-Force.

The fourteen-field log and this metric do not list the same required names. `record_id` is in the metric and outside the fourteen fields. That gap is open question LS-Q7 in `log-schema.md`. This proposal uses the metric's list, which is the list already marked PROPOSED in the YAML.

## The other seven metrics

`metric.retry_count`, `metric.sla_breach_risk`, `metric.quarantine_rate`, `metric.alarm_storm_size`, `metric.tokens_per_invocation`, `metric.cost_per_correlated_incident`, and `metric.ai_outcome_count` keep `target: null`. The bound notes already on retry and on the SLA score stay notes. This stage adds the three service levels above and leaves the other targets null.

## Findings

### SL-01

| | |
|---|---|
| Finding | The repo states no service level. Three numbers are proposed here, each with owner Team-Force. |
| Evidence | **Verified Fact.** `otel-notes.md` line 6. `metrics.yaml` `target: null` on every metric. Operating contract row 10 for the owner. |
| Impact | A later stage can test against these numbers only after Team-Force accepts them in writing. Until then the dashboard shows the measured figure and no pass line. |
| Risk | Medium. The numbers 99 of 100, 2000 milliseconds, and 1.0 are easy to copy into a report as if they were measured. |
| Confidence | High |
| Open questions | Open question for S03: there is no metric id for API availability. This design needs that id so the availability service level maps to `metrics.yaml` the way recommendation latency maps to `metric.recommendation_latency`. |

### SL-02

| | |
|---|---|
| Finding | Live recommendation latency is not stored. The event file's 95th value is 13627 milliseconds. |
| Evidence | **Verified Fact.** `ai_gateway.py` line 9. Recount of `events.jsonl` on 2026-10-11. |
| Impact | The PROPOSED 2000 millisecond bound cannot be checked on today's audit row. It also does not describe the event file, where 13627 milliseconds is the 95th value. |
| Risk | Medium. Using the event-file 95th as the live target would set the service level from synthetic lines that no API wrote. |
| Confidence | High |
| Open questions | None beyond SL-01. |

## Lifecycle

`metric.recommendation_latency` and `metric.audit_completeness` are the YAML ids for levels 2 and 3. Level 1 has no YAML id yet. Stage S04-09 writes `latency_ms`, which is the field level 2 reads. Stage S05-14 needs completeness at the proposed 1.0 before a rebuilt case can show actor, chain id, and approval id from the row.
