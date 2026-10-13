# Log schema

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The audit row is specified as fourteen fields, one JSON object per line. Several columns have no field id in the YAML. The sample chain still cannot be joined to an audit row. |
| Evidence sources | `apps/api/services/audit.py`; `apps/api/main.py`; `logs/audit.log` (96 lines, counted 2026-10-11); `semantic-layer/metrics.yaml` (`metric.audit_completeness`); `semantic-layer/ai-context-policy.yaml` (`provenance.*`, `policy.outcomes`, `policy.prompt_fields`); `semantic-layer/entities.yaml` (`concept.audit_row`, `field.event.*`); `semantic-layer/access-semantics.yaml` (`action.*`, `resource.*`, `role.*`); `semantic-layer/status-taxonomy.yaml` (`status.code.audit_action.record_read`, `status.code.audit_action.ai_summary`); `semantic-layer/business-rules.yaml` (`rule.audit_row_names_actor_and_correlation`) |
| Assumptions | Half B writes all fourteen keys on every new row. Half B fills `policy_decision` and `approval_id` with null, as the playbook says, even though the route already computes an allow or deny. Stage S04-09 fills the five model fields. A required key means the key is present. A required value means the value is not null. |
| Unresolved issues | Seven open questions for S03 are listed under "Open questions for S03". This file leaves those ids for stage S03. |
| Residual risks | A row that copies the whole device into `details` would store `mgmt_ip` and `credential_profile`. The new shape has no place for those two fields. The old 96 lines stay in `logs/audit.log` in the old shape, because the log is append-only. |

## What this file is

This file defines the fourteen fields on one audit row. Half B makes `audit.py` write this shape. This half writes the definition only.

The file path stays `logs/audit.log`. The write stays append-only. Each line is one JSON object.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The row today

`audit.write_event` stores three keys. **Verified Fact:** `audit.py` lines 7 to 9.

```text
{"ts": "<UTC timestamp>", "action": "<action>", "details": { ... }}
```

`logs/audit.log` has 96 lines. Every line has `ts`, `action`, and `details`. **Verified Fact. REAL.** Counted 2026-10-11.

| Key inside `details` | Lines that have it |
|---|---|
| `record_id` | 96 |
| `role` | 74 |
| `model` | 22 |
| `route` | 20 |
| `reasons` | 20 |
| `outcome` | 7 |

| `action` | Lines |
|---|---|
| `record.read` | 54 |
| `ai.summary` | 22 |
| `policy.deny` | 20 |

Zero lines have `actor`, `correlation_id`, `approval_id`, `policy_decision`, `model_version`, `prompt_hash`, `tokens`, or `latency_ms`. **Verified Fact. REAL.**

The 7 lines with `details.outcome` hold two words: `BLOCK` on 2 lines and `RECOMMEND_ONLY` on 5 lines. Zero lines hold `HOLD_FOR_REVIEW` or `EXECUTE`. Zero lines have action `policy.hold`. **Verified Fact. REAL.** `main.py` lines 68 to 78 can write `policy.hold`. The current file has no such line.

`concept.audit_row` says the row holds `ts`, `action`, and `details`, and has no actor, no correlation id, and no approval id. **Verified Fact:** `entities.yaml`.

`rule.audit_row_names_actor_and_correlation` says the row should name who acted and which request chain it belongs to. `enforced_today` is false. **Verified Fact:** `business-rules.yaml`.

## The fourteen fields

Every new row has these fourteen keys. The order below is the order in the playbook.

| Field | JSON type | Source | Required key | Required value | YAML id |
|---|---|---|---|---|---|
| `ts` | string, UTC, from `datetime.utcnow().isoformat()` | The clock at the moment `write_event` runs | Yes | Yes | No field id. `concept.audit_row` describes the row. See open question LS-Q1. |
| `correlation_id` | string | Header `X-Correlation-Id`, or a new UUID when that header is missing or blank | Yes | Yes. Never an empty string. | `field.event.correlation_id`. `provenance.correlation_id`. |
| `actor` | string or null | The persona id when the role maps to one persona. Null when the role is `admin`, `clinician`, or absent. | Yes | No | `field.event.actor`. `provenance.actor`. See open question LS-Q2. |
| `role` | string or null | The `X-User-Role` value the route used. On `GET /records/{record_id}` a missing header is still `operator`. On `POST /ai/summarize/{record_id}` a missing header stays null and the call is denied. | Yes | No. Null only when the summarize header was absent. | Value list `role.admin`, `role.operator`, `role.clinician`, `role.engineer`, `role.ai_agent`. No field id for the column. See open question LS-Q3. |
| `action` | string | The audit action the route writes | Yes | Yes | `status.code.audit_action.record_read` is the string `record.read`. `status.code.audit_action.ai_summary` is the string `ai.summary`. `policy.deny` and `policy.hold` have no status id. See open question LS-Q4. The access names for the same two live calls are `action.read` and `action.summarize`. |
| `resource` | string | The resource the route is about. Both live data routes load a device row, so the value is `resource.device`. | Yes | Yes | `resource.device`. No field id for the column. See open question LS-Q5. |
| `policy_decision` | string or null | The access answer, allow or deny. Half B writes null. The route already computes the answer and stores pieces of it under `details.reasons`. | Yes | No | `concept.policy_decision`. `provenance.policy_result`. Two names for one column. See open question LS-Q6. |
| `approval_id` | string or null | The stored human approval. No route writes one. S07 fills it. The model never fills it. | Yes | No. Null until S07. | `provenance.approval_id`. `concept.approval`. |
| `model` | string or null | The model name when a model call ran. The live value is `local-sim-v1`. Null on a record read and on a deny that happens before the gateway. S04-09 writes this column. Today the name sits in `details.model` on the 22 `ai.summary` lines. | Yes | No | `field.ai_invocation.model`. `provenance.model`. `status.code.model.local_sim_v1`. |
| `model_version` | string or null | A version separate from the model name. S04-09 writes it. Today `local-sim-v1` is the name. `provenance.model_version` says that string doubles as the version and the field is absent. This column stays null until a separate version exists. | Yes | No | `provenance.model_version`. |
| `prompt_hash` | string or null | A hash of the exact prompt text. S04-09 writes it. The prompt text stays out of the log. | Yes | No | `provenance.prompt_hash`. This is a different hash from `field.event.payload_hash`, which is the hash on an event line. |
| `tokens` | integer or null | Tokens used by one model call. S04-09 writes it. The live body returns `token_estimate`, computed as `len(prompt.split()) * 2`. The CSV column is `field.ai_invocation.token_count`. | Yes | No | `provenance.tokens`. `field.ai_invocation.token_count`. |
| `latency_ms` | integer or null | Milliseconds from request to answer for one model call. S04-09 writes it on the live row. `events.jsonl` already stores `latency_ms` on every line. The live gateway waits 0.01 seconds and records no latency. | Yes | No | `field.event.latency_ms`. `provenance.latency_ms`. Read by `metric.recommendation_latency`. |
| `outcome` | string or null | One of the four outcome words when the AI check ran: `RECOMMEND_ONLY`, `HOLD_FOR_REVIEW`, `BLOCK`, `EXECUTE`. Null on a record read. | Yes | No | `policy.outcomes`. `outcome.recommend_only`. `outcome.hold_for_review`. `outcome.block`. `outcome.execute`. |

How to read one cell. Take `tokens`. The key is on every new row. The value is null until S04-09. The YAML ids are `provenance.tokens` and `field.ai_invocation.token_count`. The live formula `len(prompt.split()) * 2` is how `token_estimate` is computed today. The audit column that will hold the number is `tokens`.

## What Half B fills, and what stays null

Half B passes `actor`, `role`, `action`, `resource`, and `correlation_id` into the audit write.

Half B leaves `policy_decision` and `approval_id` as null. The playbook says those two wait for S04-06 and S07. The access check already runs in `main.py`. The copy from that check into `policy_decision` is a later edit. This schema still names the column so the key exists.

S04-09 writes `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms`.

`outcome` is null on `record.read`. When the summarize route already has an outcome word, the row stores that word. The current file does this inside `details` on 7 lines.

## Worked example of a new row

This object shows the shape Half B will write. The 96 lines in `logs/audit.log` still use the three-key shape.

A `GET /records/REC-0001` with headers `X-Correlation-Id: demo-123` and `X-User-Role: operator` looks like this after Half B, before S04-09 and S07:

```json
{"ts": "2026-10-11T00:00:00.000000", "correlation_id": "demo-123", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null}
```

`actor` is `noc_operator` because `role.operator` maps to `persona.noc_operator`. That mapping is an Inference in `access-semantics.yaml`. The timestamp above is a placeholder for the shape. A real row uses the clock at write time.

`record_id` is not one of the fourteen fields. The metric `metric.audit_completeness` still counts `record_id` as required. See open question LS-Q7.

## Fields the log must not hold

The audit row does not store `mgmt_ip`, `credential_profile`, or a secret.

**Verified Fact:** `semantic-layer/ai-context-policy.yaml` `policy.prompt_fields` forbids `field.device.mgmt_ip` and `field.device.credential_profile`. The same file lists secret names and says the values must never be written: `SHARED_DB_PASSWORD`, `SHARED_DB_USER`, `DATABASE_URL`, `AI_GATEWAY_KEY`, `LEGACY_BATCH_PASSWORD`, `OT_VENDOR_TOKEN`.

The prompt text stays out of the row. `prompt_hash` is the stand-in. **Verified Fact:** `provenance.prompt_hash` says a reviewer can prove what was sent without storing the text.

The current 96 lines do not contain those field names. Their `details` keys are `record_id`, `role`, `model`, `route`, `reasons`, and `outcome` only. **Verified Fact. REAL.**

## How this schema meets the completeness metric

`metric.audit_completeness` counts, for one row, how many required fields are filled, divided by how many required fields that row has.

The metric's required fields are `ts`, `action`, `actor`, `correlation_id`, `record_id`, and, for a model call, `model`, `approval_id`, and `policy_result`. **Verified Fact:** `metrics.yaml` `metric.audit_completeness`. The required-field list is PROPOSED. Owner: Team-Force.

Applied to the current file:

| Action | Filled | Required by the metric | Fraction |
|---|---|---|---|
| `record.read` (54 lines) | `ts`, `action`, `record_id` | those three, plus `actor` and `correlation_id` | 3 of 5 |
| `ai.summary` (22 lines) | `ts`, `action`, `record_id`, `model` | those four, plus `actor`, `correlation_id`, `approval_id`, and `policy_result` | 4 of 8 |
| `policy.deny` (20 lines) | `ts`, `action`, `record_id` | treated here as a non-model row: 5 fields | 3 of 5 |

The fractions are the metric formula applied to the key counts. **Verified Fact** for the key counts. **Inference** for treating `policy.deny` as a non-model row. The metric text does not name `policy.deny`.

`role` is on 74 lines and is outside that required list.

## Open questions for S03

LS-Q1. Open question for S03: there is no field id for the audit timestamp. `concept.audit_row` describes the row. This design needs a field id for the column `ts`.

LS-Q2. Open question for S03: there is no field id for the named person on an API call. `field.event.actor` is a persona word on the event file. This design needs an id for the person who called, separate from the role. Until that id exists, `actor` stores the persona id when `access-semantics.yaml` maps the role to one, and null when it does not.

LS-Q3. Open question for S03: there is no field id for the role stored on an audit row. The value list `role.*` exists. This design needs a field id for the column `role`.

LS-Q4. Open question for S03: `policy.deny` and `policy.hold` have no status id. `status.code.audit_action.record_read` and `status.code.audit_action.ai_summary` exist. This design needs a status id for the deny row and a status id for the hold row.

LS-Q5. Open question for S03: there is no field id for the resource stored on an audit row. The value list `resource.*` exists. This design needs a field id for the column `resource`.

LS-Q6. Open question for S03: the allow-or-deny word has two YAML names, `concept.policy_decision` and `provenance.policy_result`. This design needs one field id for the column `policy_decision`.

LS-Q7. Open question for S03: `metric.audit_completeness` requires `record_id`. The fourteen-field log has no `record_id` column. The current `details` object also stores `reasons`. This design needs a field id for the record id, and a field id for the reason list, if those two values must stay on the audit row.

## Findings

### LS-01

| | |
|---|---|
| Finding | The live audit row is three keys. The target row is fourteen keys. Actor, chain id, and approval id are absent on all 96 lines. |
| Evidence | **Verified Fact.** `audit.py` lines 7 to 9. Key counts above. `concept.audit_row`. |
| Impact | A reader of the current file can see the time, the action, and a record id. The reader cannot see who asked, which request it was, or which approval applied. |
| Risk | High. Completeness stays at 3 of 5 on a read and 4 of 8 on a summary until Half B and the later stages fill the columns. |
| Confidence | High |
| Open questions | LS-Q1 through LS-Q7 above. |

### LS-02

| | |
|---|---|
| Finding | The current details object does not store `mgmt_ip` or `credential_profile`. The new schema has no column for them. |
| Evidence | **Verified Fact.** Key list on the 96 lines. Forbidden fields in `ai-context-policy.yaml` `policy.prompt_fields`. |
| Impact | A later change that logs the device dict would break this rule. The fourteen columns do not include those names, so the normal write path has nowhere to put them. |
| Risk | Medium. The prompt builder still places the whole device row in the prompt (defect F12). That is a prompt defect. This log schema does not copy that prompt. |
| Confidence | High |
| Open questions | None. |

## Lifecycle

Stage S04-09 fills `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms`. Stage S04-12 computes cost from those rows. Stage S05-14 rebuilds a case from rows that share one `correlation_id`. `metric.audit_completeness` is the measure of how full a row is.

## Change from stage S04-12 Half B

The audit row now has a fifteenth key, `token_estimate_method`. It holds `word_count_x2_EDUCATIONAL` on a row where `tokens` has a value, and null on every other row. It sits after `outcome`. The first fourteen keys and their order are unchanged. Open question for S03: this design needs a field id for `token_estimate_method`, so each token number says how it was worked out.

## Change from stage S07

The audit row now has 17 keys. Two keys are new and sit after `token_estimate_method`.

- The 16th key is `record_id`. It holds the device id the caller asked for. It is null on a row that names no device, such as a storm read or an audit read. The id is stored as the caller typed it.
- The 17th key is `final_action`. It holds the word `none` on every row, because no route in this app changes a device.

`approval_id` is no longer always null. The route `POST /approvals/{id}` writes the id it made on the row `ai.approval` for a yes. A no leaves it null.

Three new action words appear in `action`: `record.storm_read`, `ai.recommendation` and `ai.approval`. Each has a YAML id (`docs/ADR/0005-s07-yaml-additions.md`). A correlation id sent in `X-Correlation-Id` that is longer than 128 characters is not stored. The server makes a new UUID.

Open question for S03: the word to store for a role header that is not in the known list. S07 stores the role as the caller sent it.
