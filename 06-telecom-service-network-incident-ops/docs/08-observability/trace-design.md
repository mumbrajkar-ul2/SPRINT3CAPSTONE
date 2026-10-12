# Trace design

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. One id is designed from the first running hop through policy, the model, approval, and the audit row. The sample chain `corr-00273` has seven stored lines. The UI, the API route, the policy answer, the model call, the approval, and the audit row have no line for that id. |
| Evidence sources | `apps/api/services/audit.py`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `observability/otel-notes.md`; `logs/audit.log` (96 lines, counted 2026-10-11); `data/synthetic/events.jsonl` (3000 lines, counted 2026-10-11); `docs/02-baseline/data-quality-baseline.md`; `docs/01-discovery/business-flow-reconstruction.md`; `semantic-layer/entities.yaml` (`field.event.correlation_id`); `semantic-layer/ai-context-policy.yaml` (`provenance.correlation_id`); `semantic-layer/relationships.yaml` (`relationship.event_refers_to_entity`); `docs/00-contract/operating-contract.md` row 5 |
| Assumptions | The first hop that runs today is the API. The web scaffold does not call the API. A non-empty `X-Correlation-Id` value is kept as sent, including a value such as `demo-123`. An empty header is treated as missing. File order is the reading order for `events.jsonl` because that file has no clock time. |
| Unresolved issues | Open question for S03: there is no field id for the named person on an API call. `field.event.actor` is a persona word on the event file. This design needs an id for the person who called, separate from the role. |
| Residual risks | 1992 event lines have no chain id. Those lines stay as they are because writes under `data/synthetic/` are prohibited. 96 audit lines have no chain id. A reader who groups on a blank id will join unrelated steps. |

## What this file is

This file says where the request chain id is created, where each hop reads it, and what happens when it is missing.

Half A writes this design. No code changes in this half.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file, a line, or a YAML id.

## The id

The chain id is one string named `correlation_id`.

YAML ids for that string: `field.event.correlation_id` and `provenance.correlation_id`.

The running API does not read or write that string today. **Verified Fact:** `apps/api/main.py` reads `X-User-Role` and does not mention `X-Correlation-Id`. `apps/api/services/audit.py` lines 7 to 9 write `ts`, `action`, and `details`.

## Create rule

The API is the create point in the running system.

When a request arrives, the API reads the header `X-Correlation-Id`.

When that header holds a non-empty string, the API keeps that string for the whole request. The later done test sends `demo-123`. The API stores `demo-123`.

When the header is absent, or the value is empty, or the value is only spaces, the API creates a new UUID and uses that string. A created id is a UUID. A caller-supplied id can be any non-empty string.

The same string is the only chain id for that request. The API does not create a second id at policy, at the model, or at the audit write.

The web scaffold does not send the header today. Operating contract row 5 says the portal stays unwired until four conditions are true. **Verified Fact:** `docs/00-contract/operating-contract.md` row 5. **Inference:** no screen is the create point until that wiring exists.

`GET /health` gets an id by the same rule. That route writes no audit row today. **Verified Fact:** `status.code.health.ok` in `semantic-layer/status-taxonomy.yaml`. The id still exists on the request so a later row can use it.

## Read rule

Each hop reads the id. No hop replaces it.

| Hop | What it does with the id | What the code does today |
|---|---|---|
| UI | Sends `X-Correlation-Id` when the portal is wired. | The portal does not call the API. **Verified Fact:** operating contract row 5. |
| API | Creates the id or keeps the header. Puts the same value on the response header `X-Correlation-Id` so the caller can read it. Hands it to every handler. | `main.py` has three routes. None reads the chain header. |
| Policy | The access check and the AI-action check receive the id. A deny row and an allow row both keep it. | `policy.check_record_read`, `policy.check_summarize`, and `policy.decide_summarize` are called with a role and a record. **Verified Fact:** `main.py` lines 18 to 55. The id is not an argument. |
| Model | `summarize_record` receives the id with the device row. | `ai_gateway.summarize_record(record)` receives the device dict only. **Verified Fact:** `ai_gateway.py` line 6 and `main.py` line 83. |
| Approval | The later approval route receives the id and stores it with `approval_id`. That route is S07. | No approval route exists. **Verified Fact:** `business-flow-reconstruction.md` flow 4. `provenance.approval_id` has `present_today: false`. |
| Audit | Every `write_event` call stores the id on the row. | `write_event(action, details)` stores `ts`, `action`, and `details`. **Verified Fact:** `audit.py` lines 7 to 12. |

## Missing rule

A stored row never keeps a blank chain id.

When the header is missing, the API creates a UUID before any hop runs. The audit row then holds that UUID. A route that writes an audit row with an empty `correlation_id` fails the stage gate.

The old files already contain blanks. This design does not rewrite them.

| Store | What is missing | Count | Label |
|---|---|---|---|
| `data/synthetic/events.jsonl` | JSON `null` | 982 | **Verified Fact. REAL.** Same count as `docs/02-baseline/data-quality-baseline.md`. Recounted 2026-10-11. |
| `data/synthetic/events.jsonl` | Empty string | 1010 | **Verified Fact. REAL.** |
| `data/synthetic/events.jsonl` | Null or blank together | 1992 | **Verified Fact. REAL.** 982 + 1010 = 1992. |
| `data/synthetic/events.jsonl` | Filled id | 1008 | **Verified Fact. REAL.** 1992 + 1008 = 3000. |
| `logs/audit.log` | No `correlation_id` key on the row | 96 of 96 | **Verified Fact. REAL.** Counted 2026-10-11. |

A null and an empty string both leave the line with no chain id. Those 1992 event lines cannot be grouped with any other line. **Verified Fact:** `relationship.event_refers_to_entity` says `correlation_id` is filled on 1008 of 3000 lines.

The 1008 filled values are 525 distinct ids. **Verified Fact. REAL.** Counted 2026-10-11.

| Events with the same filled id | How many ids |
|---|---|
| 1 | 237 |
| 2 | 151 |
| 3 | 89 |
| 4 | 40 |
| 5 | 7 |
| 7 | 1 (`corr-00273`) |

288 ids have more than one event. Those 288 ids cover 771 lines. The other 237 filled ids are a single line each. **Verified Fact. REAL.**

`entities.yaml` uses `corr-00273` as the example shape of `field.event.correlation_id`. That id is the one chain with seven lines. The reconstruction of that chain is `incident-reconstruction.md`.

## What a missing id does to a business event

`events.jsonl` records a flow name. It does not run the flow. **Verified Fact:** `business-flow-reconstruction.md` and `field.event.event_type`.

A line with a filled id can be placed next to the other lines that share that id. A line with a null or a blank id stands alone. The four flows in the reconstruction doc still have the same step gaps they had in S01. The chain id does not fill a missing route.

## Findings

### TD-01

| | |
|---|---|
| Finding | 1992 of 3000 event lines have no chain id. 982 are JSON null. 1010 are an empty string. |
| Evidence | **Verified Fact. REAL.** Recount on 2026-10-11 matches `docs/02-baseline/data-quality-baseline.md` lines 142 to 149. YAML: `field.event.correlation_id`. |
| Impact | Those lines cannot be placed in a request chain. A count of "events in this incident" that treats blank as one shared id will merge 1992 unrelated lines. |
| Risk | High. A later cost or latency figure built on a blank id describes a mix of flows. |
| Confidence | High |
| Open questions | None on this count. |

### TD-02

| | |
|---|---|
| Finding | Every live audit row is written with no chain id. |
| Evidence | **Verified Fact.** `audit.py` lines 7 to 12. `logs/audit.log`: 96 lines, 0 lines contain `correlation_id`. `observability/otel-notes.md` lines 4 to 7. `provenance.correlation_id` has `present_today: false`. |
| Impact | A caller cannot take an audit line and find the policy check or the model call that belonged to the same request. |
| Risk | High. Stage S05-14 rebuilds a case from this log. With no id, the case is one line. |
| Confidence | High |
| Open questions | None. |

### TD-03

| | |
|---|---|
| Finding | The running API has no create point and no read point for the chain id. |
| Evidence | **Verified Fact.** `main.py` header parameters are `x_user_role` only. Policy calls and `summarize_record` do not take a chain id. |
| Impact | Half B adds the header read, the UUID create, and the pass-through. Until that lands, new audit rows stay without an id. |
| Risk | High. The Half B gate is BLOCKED when any route writes an audit row without a `correlation_id`. Today's three write sites do that: `record.read`, `policy.deny`, and `ai.summary`. |
| Confidence | High |
| Open questions | Open question for S03: there is no field id for the named person on an API call. `field.event.actor` is a persona word on the event file. This design needs an id for the person who called, separate from the role. |

### TD-04

| | |
|---|---|
| Finding | One filled id can hold several flows and several personas. |
| Evidence | **Verified Fact. REAL.** `corr-00273` has 7 lines, 3 flow names, and 4 actor words. It is the only id with 7 lines. Full chain: `incident-reconstruction.md`. |
| Impact | Grouping by `correlation_id` produces a list of lines. The list can hold more than one flow name. |
| Risk | Medium. A dashboard that titles the group "one incident" will show orders, alarms, and a remediation line under one heading. |
| Confidence | High |
| Open questions | None. |

## Lifecycle

`docs/02-baseline/data-quality-baseline.md` is the source for the blank-id counts. This stage recounted them. Stage S04-09 writes `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` on the audit row that carries this id. Stage S04-12 computes cost from that row. Stage S05-14 rebuilds a case from the rows that share one id.
