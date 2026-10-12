# Retry cost analysis

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The retries in the data are counted and every figure has a label. The model cost of a retry is a what-if, because no code retries a model call and no code retries an order. Money cost is Unknown. |
| Evidence sources | `docs/12-finops/cost_baseline.py` section 4 and `cost_baseline_output.txt`; `data/synthetic/service_orders.csv`; `semantic-layer/metrics.yaml` (`metric.retry_count`); `semantic-layer/entities.yaml` (`field.service_order.retry_count`); `docs/11-reliability/retry-and-circuit-breaker-strategy.md`; `docs/11-reliability/idempotency-plan.md`; `docs/11-reliability/recovery-evidence.md`; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/cost-envelope.md` |
| Assumptions | A "retry" is the count stored in `retry_count`. The what-if lets each stored retry call the model once. The EDUCATIONAL rate is 1.0 educational unit per 1000 tokens. PROPOSED. Owner: Team-Force. The 1000 bound comes from defect F18 and is PROPOSED. Owner: Team-Force. It is not a maximum. |
| Unresolved issues | The legal maximum for `retry_count` is Unknown. The meaning of the number (retries in total, or retries for one attempt) is Unknown. `service_orders.csv` has no date-time column, so retries per hour are Unknown. The money cost of a retry is Unknown. |
| Residual risks | A reader can take the what-if as a forecast of model spend. It is a stress picture. S2Q assigns this capability to deterministic code, so the real hosted-model cost of an order retry is 0 by assignment. |

## What this file is

This file counts the retries in `service_orders.csv`. It then asks one question: what would these retries cost if each one called the model? It also states the business effect of a stuck order.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Number labels: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## How many retries the data shows

| Item | Value | Label |
|---|---|---|
| Rows in `service_orders.csv` | 354 | PRECOMPUTED |
| Rows with a numeric `retry_count` | 353 | SIMULATED |
| Rows with a blank `retry_count` | 1 (`SER-BAD1`) | SIMULATED |
| Sum of `retry_count` | 943,094 | SIMULATED |
| Smallest, median, mean, largest | 32, 2,763, 2,671.7, 4,995 | SIMULATED |
| Rows at or above 1000 (PROPOSED bound, Owner: Team-Force) | 294 | SIMULATED |
| Retries held in those 294 rows | 912,359 | SIMULATED |
| Distinct `order_id` among the 353 numeric rows | 350 | SIMULATED |
| Sum if each `order_id` counts once, first row | 935,183 | SIMULATED |

**Verified Fact.** The sum 943,094 matches `idempotency-plan.md`. The values match `metrics.yaml` (`metric.retry_count`: 353 values, smallest 32, largest 4995, 294 at or above 1000).

Worked example. `ORD-00002` has `retry_count` 4052 (SIMULATED). That one order holds 0.43% of the 943,094 retries. The data has no timestamp, so the 4052 retries have no length of time.

Every row is already above 30. No order shows 0 retries. A rule that flags orders with retries would flag all 353. **Inference:** the synthetic generator drew the numbers from a wide range, so the data does not describe a healthy order flow.

## What each retry would cost if it called the model

**Verified Fact.** No order retry calls a model today. `ai-qualification.md` picks deterministic code for "Provisioning retry and rollback". The hosted-model cost of that capability is 0 by **Assignment** in `cost-envelope.md`. `retry-and-circuit-breaker-strategy.md` says a timed-out model call is not retried, and a call with a bad answer is not retried.

The numbers below answer a different question. They show the size of the cost if every stored retry were a model call. All EDUCATIONAL.

| Case | Tokens per call | Tokens for 943,094 retries | Educational units | One retry |
|---|---|---|---|---|
| A. CSV mean `token_count` | 2,395.7 | 2,259,351,327 | 2,259,351.33 | 2.3957 |
| B. Live prompt, word count times 2 | 90 | 84,878,460 | 84,878.46 | 0.0900 |

Case A uses the SIMULATED CSV mean. Case B uses the live estimate for one device row. Both pass through the EDUCATIONAL rate of 1.0 unit per 1000 tokens. The unit is not money.

Worked example. Case A multiplies 943,094 by 2,395.7 tokens. The result is 2,259,351,327 tokens. At 1.0 unit per 1000 tokens that is 2,259,351.33 units. The whole CSV of 353 calls costs 845.675 units at the same rate. So the what-if is 2,672 times the CSV total. That ratio equals the mean retry count, 2,671.7. Each retry repeats the same cost, so the total grows in step with the retry count.

What this shows. If a model call were ever placed inside an order retry loop, the retry count would decide the cost, and the token size would matter much less. A model call in that loop is the wrong design. The retry path stays deterministic code, as S2Q assigns.

## The retries that can reach a model

Only one retry path can reach the model, and it is a PROPOSED path.

| Path | Retries the model? | Cost of one retry | Label |
|---|---|---|---|
| Model call that hits the deadline | No. One attempt. | 0 extra. The case goes to a person. | Verified Fact. PROPOSED rule. Owner: Team-Force. |
| Model answer that fails the schema | No. One attempt. | 0 extra. | Verified Fact. PROPOSED rule. |
| Model call that fails before the prompt is accepted (refused connection) | Yes, 1 retry after 0.5 s. Not built. | Near 0 tokens, because the prompt was not processed. | PROPOSED. Owner: Team-Force. The gateway cannot tell this failure from a bad answer yet (`RB-04`). |
| A person sends the same summary request again | Allowed. No limit. | 1 model call. About 90 tokens, so 0.09 educational units. | EDUCATIONAL, on the live estimate. |
| Open breaker or full in-flight limit | No call at all | 0 tokens | Verified Fact. `recovery-evidence.md`. |

**Verified Fact.** `idempotency-plan.md` finding ID-01: a repeat of the summary route costs one model call and one audit row, and changes no business row. Probe P4 showed 5 identical calls gave 5 model calls (REAL, test run).

## Business effect

The business effect of a stuck order is that the customer circuit is not delivered. A stuck order delays the circuit the customer bought.

| `provisioning_status` | Orders | Retries | Label |
|---|---|---|---|
| manual_hold | 50 | 144,378 | SIMULATED |
| queued | 51 | 142,754 | SIMULATED |
| in_progress | 48 | 137,472 | SIMULATED |
| failed | 42 | 116,530 | SIMULATED |
| closed | 37 | 103,522 | SIMULATED |
| approved | 39 | 103,124 | SIMULATED |
| exception | 44 | 101,421 | SIMULATED |
| new | 42 | 93,893 | SIMULATED |
| Total | 353 | 943,094 | SIMULATED |

Five statuses read as "not finished": `manual_hold`, `queued`, `in_progress`, `failed`, and `exception`. They hold 235 of the 353 orders (SIMULATED). That reading of the words is an **Inference**, because the status word list has no definition in the repo. 37 orders are `closed` and still show 103,522 retries (SIMULATED). The retries are not tied to the status.

Worked example. 51 orders are `queued`. Together they show 142,754 retries (SIMULATED). If those orders each wait on a circuit for a customer, the customer circuits wait. How long they wait is Unknown, because the table has no date-time column.

The cost of delay to the customer is not in the repo. `circuits.csv` has `sla_tier` and the incident table has `sla_breach_risk`. Neither links an order to a penalty. The money cost of a late circuit is **Unknown**.

## Findings

### RC-01

| | |
|---|---|
| Finding | The data shows 943,094 retries across 353 orders. Every order has at least 32. |
| Evidence | **Verified Fact.** Script section 4 (SIMULATED). `metric.retry_count`. |
| Impact | The retry count cannot separate healthy orders from stuck orders. 294 rows are at or above the PROPOSED bound of 1000. |
| Risk | Medium. A report built on the raw number will flag every order. |
| Confidence | High for the counts. Low for the meaning of the number. |
| Open questions | What `retry_count` counts, and the legal maximum, are Unknown. Owner: Team-Force. |

### RC-02

| | |
|---|---|
| Finding | The real hosted-model cost of order retries is 0 by assignment. If each retry called the model, the cost would be 84,878.46 educational units on the live estimate, or 2,259,351.33 on the CSV mean. |
| Evidence | **Verified Fact** for the assignment (`cost-envelope.md`, `ai-qualification.md`). EDUCATIONAL for the what-if (script section 4). |
| Impact | The what-if is a design guard. A model call in a retry loop multiplies cost by the retry count. |
| Risk | High if a later stage adds a model call to the order flow. |
| Confidence | High for the arithmetic. The tokens per call are Unknown for a real model. |
| Open questions | The hosted-model price. Unknown. |

### RC-03

| | |
|---|---|
| Finding | The only retry that can reach the model is a PROPOSED retry on a refused connection. It is not built. |
| Evidence | **Verified Fact.** `retry-and-circuit-breaker-strategy.md`; RB-04. |
| Impact | The model path has no retry cost today. A person who repeats a summary request pays one model call each time. |
| Risk | Low |
| Confidence | High |
| Open questions | The failure id that separates a refused connection from a bad answer is OQ-1 from S04-11. It is still open. |

### RC-04

| | |
|---|---|
| Finding | The business effect of the retries cannot be put in money or in time. |
| Evidence | **Verified Fact.** `service_orders.csv` has no date-time column (`entities.yaml`, `entity.service_order`). No file stores a late-circuit cost. |
| Impact | The cost of a stuck order is a delay of an unknown length for 235 orders in a not-finished status (Inference on the status words). |
| Risk | Medium |
| Confidence | Medium |
| Open questions | Open question for S03: `field.service_order` has no timestamp field. This design needs one to turn retry count into delay. |

## Lifecycle

`optimization-backlog.md` lists the guard against a model call inside a retry loop. `cost-envelope.md` carries the reconciliation. The envelope's Unknown row "Money cost of retries" stays Unknown for money. This file replaces it with a labelled count and an EDUCATIONAL what-if.
