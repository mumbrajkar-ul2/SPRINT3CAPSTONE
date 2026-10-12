# Incident reconstruction

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. `corr-00273` has seven stored lines, listed from the first to the last. The UI, the API route, the policy answer, the model call, the approval, and the audit row have no stored row for this id. Those gaps cannot be filled from the files on disk. |
| Evidence sources | `data/synthetic/events.jsonl` lines 1140, 1279, 1447, 1583, 2386, 2842, and 2904; `logs/audit.log` (96 lines); `docs/02-baseline/data-quality-baseline.md`; `docs/01-discovery/business-flow-reconstruction.md`; `semantic-layer/entities.yaml` (`field.event.correlation_id`, `entity.event`); `semantic-layer/relationships.yaml` (`relationship.event_refers_to_entity`, `relationship.event_belongs_to_flow`) |
| Assumptions | The seven lines are read in file order. The event file has no clock column, so a true time order is Unknown. File order is the order of `event_id`. |
| Unresolved issues | Open question for S03: `entity.event` has no timestamp field. This reconstruction needs a clock time so the seven lines can be ordered by when they happened. This file uses line order and does not add a field. |
| Residual risks | The seven lines use three flow names and four personas. A reader who calls the group one incident will merge an alarm step, a topology step, and a remediation step. The sum of `cost_units` is 16.734 in an Unknown money unit. |

## What this file is

This file rebuilds one chain from stored rows. The chain id is `corr-00273`. It is the only id in `events.jsonl` with seven lines. **Verified Fact. REAL.** Counted 2026-10-11. `entities.yaml` uses `corr-00273` as the example shape of `field.event.correlation_id`.

The business event, as far as the file can say it, is: seven recorded steps share this id. The steps name three flows. They do not name one device, one alarm, or one incident.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Why this id

525 distinct filled ids exist. 288 of them have more than one line. One of them has seven lines. **Verified Fact. REAL.** The size counts are in `trace-design.md`.

`logs/audit.log` cannot supply a second chain. All 96 lines lack `correlation_id`. **Verified Fact. REAL.**

## The seven stored lines

Read from the top of the file to the bottom. Each line is one JSON object. The columns below are the fields on that object. No other fields are present. **Verified Fact:** the key list on each line is `event_id`, `business_entity`, `event_type`, `severity`, `correlation_id`, `actor`, `latency_ms`, `cost_units`, `payload_hash`.

| Order | File line | event_id | business_entity | event_type | severity | actor | latency_ms | cost_units | payload_hash |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1140 | EVT-0001139 | alarms | Alarm storm to incident correlation | info | customer_support | 11595 | 3.3139 | 5219a084f55578b4 |
| 2 | 1279 | EVT-0001278 | devices | Topology lookup to AI recommendation | error | customer_support | 4343 | 1.9684 | 08283f780bb48e42 |
| 3 | 1447 | EVT-0001446 | incidents | Topology lookup to AI recommendation | critical | customer_support | 392 | 2.3474 | 8b872d6fc38d529e |
| 4 | 1583 | EVT-0001582 | ai_invocations | Alarm storm to incident correlation | debug | customer_support | 6692 | 1.6619 | 78fb4d1159c3018e |
| 5 | 2386 | EVT-0002385 | devices | Alarm storm to incident correlation | debug | network_engineer | 671 | 2.7753 | 2d0308a3f10c37ed |
| 6 | 2842 | EVT-0002841 | incidents | Approved remediation to validation | warn | noc_operator | 545 | 2.3396 | 852171539e54b841 |
| 7 | 2904 | EVT-0002903 | service_orders | Alarm storm to incident correlation | error | ai_agent | 3083 | 2.3275 | a535c94a53058435 |

Worked reading of row 1. Line 1140 says an alarm-table event happened inside the flow "Alarm storm to incident correlation". The persona word is `customer_support`. The step took 11595 milliseconds. The cost figure is 3.3139. The line does not say which alarm.

Sums across the seven lines: `latency_ms` 27321, `cost_units` 16.734. **Verified Fact. REAL.** The money unit of `cost_units` is Unknown. **Verified Fact:** `field.event.cost_units`.

Personas on the chain: `customer_support` on lines 1 to 4, then `network_engineer`, `noc_operator`, and `ai_agent`. **Verified Fact.**

Flow names on the chain:

| Flow name | YAML id | Lines in this chain |
|---|---|---|
| Alarm storm to incident correlation | `concept.flow_alarm_storm_to_incident_correlation` | 1, 4, 5, 7 |
| Topology lookup to AI recommendation | `concept.flow_topology_lookup_to_ai_recommendation` | 2, 3 |
| Approved remediation to validation | `concept.flow_approved_remediation_to_validation` | 6 |

Customer order to provisioning does not appear. **Verified Fact.**

## What the seven lines explain

The stored chain is a list of seven steps in file order.

Step 1 names the alarms table and the alarm-storm flow. Steps 2 and 3 name the topology-to-recommendation flow, first on the devices table, then on the incidents table. Step 4 names the ai_invocations table and returns to the alarm-storm flow. Step 5 names the devices table again, with a different persona. Step 6 names the incidents table and the remediation flow. Step 7 names the service_orders table and the alarm-storm flow, with persona `ai_agent`.

`relationship.event_belongs_to_flow` says each event belongs to one of the four flows. **Verified Fact.** This id belongs to three of them.

`relationship.event_refers_to_entity` says each event names a table and has no row id, so it cannot be joined to one device or one incident. **Verified Fact.** That is true of all seven lines. `business_entity` is `alarms`, `devices`, `incidents`, `ai_invocations`, `devices`, `incidents`, and `service_orders`. None of those values is a row key such as `ALA-00002` or `DEV-00004`.

## Gaps

A hop with no stored row is marked GAP. The gap stays open. No file in the repo fills it for this id.

| Hop | What a full chain would show | What is stored for `corr-00273` |
|---|---|---|
| UI | A screen sent the id. | GAP. No line names a screen. The portal does not call the API. **Verified Fact:** operating contract row 5, cited in `business-flow-reconstruction.md`. |
| API | A route name and an HTTP result. | GAP. No line names `GET /records/{record_id}` or `POST /ai/summarize/{record_id}`. |
| Policy | Allow or deny, and the reason. | GAP. No line holds allow, deny, or a policy id. |
| Model | Model name, version, prompt hash, tokens, and the outcome word. | GAP for the call itself. Line 4 names the table `ai_invocations`. It stores no `ai_call_id`, no model name, and no token count. `event_type` on that line is the alarm-storm flow. |
| Approval | An `approval_id` written by a named person. | GAP. No line has an approval id. `provenance.approval_id` is absent on the live call as well. |
| Audit row | One `logs/audit.log` line with this `correlation_id`. | GAP. 96 audit lines. 0 contain `corr-00273`. 0 contain any `correlation_id`. |
| Clock time | A timestamp on each step. | GAP. `entity.event` has no timestamp field. Order above is file order. |
| Row identity | The device, alarm, or incident the step is about. | GAP. The line names the table only. |

The live routes that do exist (`GET /records/{record_id}` and `POST /ai/summarize/{record_id}`) write audit lines with `record_id` and, for a summary, `model`. Those lines have no chain id, so they cannot be attached to `corr-00273`. **Verified Fact:** `audit.py` and the 96-line count.

Flow 3 in `business-flow-reconstruction.md` says the lookup and the local summary exist, and a stored approval id does not. Flow 4 says the approval, the device change, and the validation have no code. **Verified Fact:** that file. This chain's step 6 names the remediation flow. The repo has no row that shows a change or a validation result for this id. That matches the flow-4 gap. It does not fill it.

## What remains Unknown

Which alarm, device, incident, or order these seven lines point at. Unknown. The file does not store those ids.

Whether the file order is the order the steps happened. Unknown. There is no timestamp.

Whether one person walked this chain. The actor words change across the seven lines. **Inference:** the id groups lines. The file leaves the question of one person as Unknown.

Whether 16.734 is the cost of one incident. Unknown. The money unit is Unknown, and no incident id is on the lines. `metric.cost_per_correlated_incident` says this metric cannot be computed today.

## Findings

### IR-01

| | |
|---|---|
| Finding | `corr-00273` is seven event lines in file order. It is the longest chain in the file. |
| Evidence | **Verified Fact. REAL.** Lines 1140, 1279, 1447, 1583, 2386, 2842, 2904 of `data/synthetic/events.jsonl`. Size histogram in `trace-design.md`. |
| Impact | A reviewer can list every stored step for this id. The list is the whole stored business event. |
| Risk | Medium. Three flow names sit under one id, so the list is not one flow from start to finish. |
| Confidence | High |
| Open questions | Open question for S03: `entity.event` has no timestamp field. This reconstruction needs a clock time so the seven lines can be ordered by when they happened. This file uses line order and does not add a field. |

### IR-02

| | |
|---|---|
| Finding | Six hops have no row: UI, API, policy, model call, approval, and audit. The event line that names `ai_invocations` does not identify a model call. |
| Evidence | **Verified Fact.** Key list on the seven lines. `logs/audit.log` has 0 matching ids. `business-flow-reconstruction.md` flows 3 and 4. `provenance.approval_id` `present_today: false`. |
| Impact | The chain cannot be walked from a screen click to a stored approval. The gaps are written here because no stored row can fill them. |
| Risk | High. Stage S05-14 cannot rebuild this case from the audit log. The audit log does not contain the id. |
| Confidence | High |
| Open questions | The field-id questions in `log-schema.md` are the columns a future audit row would need. This file does not define them. |

### IR-03

| | |
|---|---|
| Finding | Each line names a table and no row inside that table. |
| Evidence | **Verified Fact.** `field.event.business_entity`. `relationship.event_refers_to_entity`. The seven `business_entity` values in the table above. |
| Impact | The chain names tables. It leaves the row key empty, so the seven lines stay unbound to one alarm or one device. A latency sum of 27321 milliseconds is the sum of the seven steps. No incident id is on those lines. |
| Risk | High. A cost or SLA figure built from this id has no incident key to hang on. |
| Confidence | High |
| Open questions | None beyond IR-01. The join from an alarm to an incident is already Unknown in `business-flow-reconstruction.md` flow 2. |

## Lifecycle

Blank ids for the rest of the file are counted in `docs/02-baseline/data-quality-baseline.md` (982 null, 1010 blank, 1008 filled). This chain is one of the 1008 filled lines, grouped into one of 525 ids. Stage S04-09 adds model fields to the audit schema. Stage S04-12 computes cost from that schema. Stage S05-14 is the stage that rebuilds a case. For this id, S05-14 still has the gaps in the table above.
