# Cost per workflow

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Cost is stated for each of the four flows, for each request chain, and for each incident on the AI call rows, all with labels. The metric `metric.cost_per_correlated_incident` cannot be computed as the YAML defines it, because the join from alarms to incidents is Unknown. Two proxies stand in for it. |
| Evidence sources | `docs/12-finops/cost_baseline.py` (sections 2, 3, 3a, 3b) and `cost_baseline_output.txt`; `data/synthetic/events.jsonl`; `data/synthetic/ai_invocations.csv`; `data/synthetic/incidents.csv`; `semantic-layer/entities.yaml` (`concept.flow_*`, `field.event.event_type`, `field.event.correlation_id`); `semantic-layer/metrics.yaml` (`metric.cost_per_correlated_incident`, `metric.tokens_per_invocation`); `docs/08-observability/trace-design.md`; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/cost-envelope.md`; `docs/11-reliability/recovery-evidence.md` |
| Assumptions | One `event_type` value is one business flow. That follows `field.event.event_type` in `entities.yaml`. All CSV tokens belong to the flow "Topology lookup to AI recommendation". That is an Inference. The EDUCATIONAL rate is 1.0 educational unit per 1000 tokens. PROPOSED. Owner: Team-Force. |
| Unresolved issues | The money unit of `cost_units` is Unknown. The link from a request chain to an incident is Unknown. The CSV rows carry no event id and no chain id, so a CSV call cannot be placed on an event. |
| Residual risks | A reader can add `cost_units` and educational units. They have different units and must not be added. A reader can take a chain as an incident. A chain is a request chain. |

## What this file is

This file states cost per business outcome. The four business outcomes are the four flows. A total alone does not answer the question, so each figure below has a flow, a chain, or an incident beside it.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Number labels: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## The four flows and the event types

**Verified Fact.** `events.jsonl` holds four `event_type` values. `entities.yaml` names one concept for each value, and each concept says "N events carry this name". The counts match.

| `event_type` | Flow concept in `entities.yaml` | Events | Mapping status |
|---|---|---|---|
| Customer order to provisioning | `concept.flow_customer_order_to_provisioning` | 741 | Clear. One value, one flow. |
| Alarm storm to incident correlation | `concept.flow_alarm_storm_to_incident_correlation` | 706 | Clear. |
| Topology lookup to AI recommendation | `concept.flow_topology_lookup_to_ai_recommendation` | 782 | Clear. |
| Approved remediation to validation | `concept.flow_approved_remediation_to_validation` | 771 | Clear. |

741 + 706 + 782 + 771 = 3000 (PRECOMPUTED). The script found 0 `event_type` values outside these four. No row in this mapping is Unknown.

The mapping that is not clear is the one from model calls to a flow. That one is in the next section.

## Cost per flow

`cost_units` is SIMULATED. Its money unit is Unknown. Educational units are EDUCATIONAL and come from SIMULATED tokens.

| Flow | Events | Sum of `cost_units` | `cost_units` per event | Model tokens in the flow | Educational units from those tokens |
|---|---|---|---|---|---|
| Customer order to provisioning | 741 | 1,676.6506 | 2.2627 | 0. Assignment from S2Q. | 0 |
| Alarm storm to incident correlation | 706 | 1,535.6879 | 2.1752 | 0. Assignment from S2Q. | 0 |
| Topology lookup to AI recommendation | 782 | 1,783.4217 | 2.2806 | 845,675. Inference. | 845.675 |
| Approved remediation to validation | 771 | 1,740.6596 | 2.2577 | 0. Assignment from S2Q. | 0 |
| All four | 3000 | 6,736.4198 | 2.2455 | 845,675 | 845.675 |

Column labels. `cost_units`: SIMULATED. Tokens: SIMULATED, placed in one flow by Inference. Educational units: EDUCATIONAL. The 0 values: Assignment from `ai-qualification.md`, not a measured bill.

Worked example for the flow "Topology lookup to AI recommendation". 782 events carry `cost_units` that add to 1,783.4217. That is 2.2806 per event (SIMULATED). The 353 CSV calls carry 845,675 tokens, which is 2,395.7 per call (SIMULATED) or 2.3957 educational units per call (EDUCATIONAL). The two per-event figures use different units. They are not added.

### Why the tokens sit in one flow

**Inference.** `ai_invocations.csv` has no `event_type` column. `ai-qualification.md` places the three model capabilities, incident summary, next-action recommendation, and configuration suggestion, in the flow whose name holds a model step: "Topology lookup to AI recommendation". The other three flows use rules, deterministic code, or workflow automation. Their model tokens are 0 by assignment.

**Verified Fact.** `cost-envelope.md` says the hosted-model portion of this flow is Unknown, and that `cost_units` is not split between model and non-model work. This file agrees. The 845,675 tokens are a count of a synthetic column. They are not a bill and they are not a share of the 1,783.4217 `cost_units`.

### Held calls

A held call has no model call, so its tokens are 0. **Verified Fact:** `recovery-evidence.md` says a timeout, an open breaker, or the in-flight limit gives HOLD_FOR_REVIEW with `tokens` and `latency_ms` null.

`ai_invocations.csv` has no outcome column, so no held row can be found in it. The CSV figures count every row as a call that used its `token_count`. The live audit log has 0 `policy.hold` rows today (REAL, script section 6). Half B counts held rows from the log and keeps them out of the average.

## Cost per request chain

A request chain is the set of events that share one filled `correlation_id`. All numbers: SIMULATED.

| Item | Value |
|---|---|
| Events with a null `correlation_id` | 982 |
| Events with an empty-string `correlation_id` | 1010 |
| Events with a filled `correlation_id` | 1008 |
| Distinct chains | 525 |
| `cost_units` inside chains | 2,245.0659 |
| `cost_units` with no chain id | 4,491.3539 (66.7% of 6,736.4198) |
| Cost per chain: smallest, median, mean, largest | 0.0113, 3.6805, 4.2763, 17.6345 |
| Chains with events from two or more flows | 244 of 525 |
| Chains with events from one flow | 281 of 525 |

The blank counts match `trace-design.md` (982, 1010, 1008, and 525 chains). 2,245.0659 + 4,491.3539 = 6,736.4198.

Two thirds of the `cost_units` cannot be placed in any chain. A cost per chain therefore covers one third of the cost. Cost per chain by flow:

| Flow | Chains that touch the flow | `cost_units` of that flow inside chains |
|---|---|---|
| Customer order to provisioning | 217 | 577.9397 |
| Alarm storm to incident correlation | 201 | 552.5526 |
| Topology lookup to AI recommendation | 215 | 593.5920 |
| Approved remediation to validation | 210 | 520.9816 |

All SIMULATED. The four sums add to 2,245.0659. A chain that spans two flows is counted once in each flow row for chain count, and its cost is split by event.

## Cost per correlated incident (`metric.cost_per_correlated_incident`)

**Verified Fact.** `metrics.yaml` defines the metric as the cost of the calls whose `incident_id` is this incident, once alarms are tied to that incident. Its `today` text says the join from alarms to incidents is Unknown, so no incident is correlated yet.

**Verified Fact.** `events.jsonl` has no incident id. `ai_invocations.csv` has `incident_id` and tokens, and has no cost and no chain id.

So the metric as defined cannot be computed from the repo. It is **Unknown**. Two proxies are stated. Neither one is the metric.

| Proxy | What it counts | Value | Label | Limit |
|---|---|---|---|---|
| P1: tokens per `incident_id` on the AI call rows | Tokens of the calls that name one incident | Mean 2,416.2 tokens. Median 2,327.5. Smallest 23. Largest 8,204. | SIMULATED | Tokens only. No cost. No alarm is correlated to the incident. |
| P1 at the EDUCATIONAL rate | Same, in educational units | Mean 2.4162 educational units per incident | EDUCATIONAL | Teaching rate. Not money. |
| P2: `cost_units` per `correlation_id` chain | Event cost for one request chain | Mean 4.2763. Median 3.6805. | SIMULATED | A chain is a request chain. The link from a chain to an incident is Unknown. |

Details for P1 (SIMULATED): 350 distinct `incident_id` values have a token row. 349 of them exist in `incidents.csv`. 3 incident ids have two or more call rows. The one id that is missing from `incidents.csv` is `INC-00001`, on the AI call row `REC-0001`. The first row of `incidents.csv` has the key `REC-0001`, not `INC-00001` (**Verified Fact:** `entities.yaml`, `entity.incident`). So this one call cannot be tied to an incident row.

Worked example for P1. Incident `INC-00002` has the CSV row `AI_-00002` with `token_count` 3264 (SIMULATED). At the EDUCATIONAL rate that is 3.264 educational units. An incident with several alarms and a real summary would use more or fewer tokens. How many is Unknown.

## Findings

### CW-01

| | |
|---|---|
| Finding | Cost per flow is stated for all four flows. The mapping from event type to flow has no Unknown row. |
| Evidence | **Verified Fact.** Table above. Script sections 2 and 3. Counts match `entities.yaml` and `cost-envelope.md`. |
| Impact | Each flow has a labelled cost figure and an event count. The flows cost about the same per event (2.1752 to 2.2806, SIMULATED). |
| Risk | Low. The values are synthetic and near uniform. |
| Confidence | High |
| Open questions | Open question for S03: `metrics.yaml` has no metric for cost per flow. This design needs one metric id so the dashboard can show it. |

### CW-02

| | |
|---|---|
| Finding | All 845,675 CSV tokens are placed in one flow by Inference. The other three flows have 0 model tokens by assignment. |
| Evidence | **Inference.** The CSV has no event type. `ai-qualification.md` puts the three model capabilities in the "Topology lookup to AI recommendation" flow. |
| Impact | The model share of cost can be stated for one flow only. The share is Unknown because `cost_units` has no model split. |
| Risk | Medium. If a model call is added to another flow later, this placement is wrong. |
| Confidence | Medium |
| Open questions | Open question for S03: `ai_invocations.csv` has no field that links a call to an event. This design needs `event_id` or `correlation_id` on the call row to place a call in a flow without Inference. |

### CW-03

| | |
|---|---|
| Finding | 66.7% of event cost has no chain id. |
| Evidence | **Verified Fact.** 4,491.3539 of 6,736.4198 `cost_units` (SIMULATED). Script section 3a. Same blank counts as `trace-design.md` TD-01. |
| Impact | A cost per chain describes one third of the cost. |
| Risk | High for any claim that covers all cost. |
| Confidence | High |
| Open questions | None. The data files stay as they are. |

### CW-04

| | |
|---|---|
| Finding | `metric.cost_per_correlated_incident` cannot be computed today. Two proxies exist and neither is the metric. |
| Evidence | **Verified Fact.** `metrics.yaml` `today` text. `events.jsonl` has no incident id. Script section 3b. |
| Impact | Stage S07 shows one labelled cost number in the demo. That number can be the P1 proxy in educational units, shown with its label, or a live row from the audit log in Half B. |
| Risk | High if the proxy is shown as the metric. |
| Confidence | High |
| Open questions | Open question for S03: the join from an alarm to an incident has no field. This design needs that join to compute the metric. `field.event.correlation_id` has no link to `field.incident.incident_id`. |

### CW-05

| | |
|---|---|
| Finding | 244 of 525 chains hold events from two or more flows. |
| Evidence | **Verified Fact.** Script section 3a (SIMULATED). `trace-design.md` TD-04 says one chain can hold several flows. |
| Impact | A chain cannot be named after one flow. A cost per chain mixes flows. |
| Risk | Medium. A dashboard that titles a chain "one incident" shows several flows under one heading. |
| Confidence | High |
| Open questions | None. |

## Lifecycle

`ai-cost-baseline.md` holds the token and event totals this file uses. `retry-cost-analysis.md` covers the order flow's retries. `finops-dashboard-fields.md` names the audit fields that carry chain id and tokens in Half B. Stage S07 shows one labelled cost number. Stage S09 cites the per-flow figures above.
