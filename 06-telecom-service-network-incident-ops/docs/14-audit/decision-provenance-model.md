# Decision provenance model

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The model has 9 groups and 24 facts. 15 facts have a column on the row today, and one of those columns (`policy_decision`) is null on every row. 9 facts have no column. 7 items are always on the "cannot be proven" list. The 15 keys have no field named `trace_id`. `correlation_id` answers that question. |
| Evidence sources | `apps/api/services/audit.py` (`SCHEMA_KEYS`, 15 keys); `docs/08-observability/log-schema.md`; `docs/08-observability/trace-design.md`; `docs/09-ai-guardrails/model-provenance-design.md`; `semantic-layer/ai-context-policy.yaml` (`provenance.*`, `output_schema`); `semantic-layer/access-semantics.yaml`; `semantic-layer/business-rules.yaml` (`rule.audit_row_names_actor_and_correlation`); `docs/14-audit/audit-gap-report.md`; `Project_Intent - section 3.3 question 5.md` |
| Assumptions | A complete record is one set of rows that share a `correlation_id`. The model does not add a column. It names the columns a reviewer needs and marks which ones exist. |
| Unresolved issues | Nine facts have no column. Each has an "Open question for S03:" line in the section "Facts with no column". |
| Residual risks | A field on this list that the row holds is still a claim in three cases: `role`, `actor`, and `correlation_id`. The caller supplies all three. |

## What this file is

This file lists what one decision needs on record so a reviewer can answer defence question 5: actor, request, data used, model and version, policy result, approval, final action, trace id, and what cannot be proven.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

A decision here means one request and everything the system did for it. In the live app, one request is one call to `GET /records/{record_id}` or `POST /ai/summarize/{record_id}`.

## The 15 keys on a row today

**Verified Fact.** `audit.py` `SCHEMA_KEYS`:

`ts`, `correlation_id`, `actor`, `role`, `action`, `resource`, `policy_decision`, `approval_id`, `model`, `model_version`, `prompt_hash`, `tokens`, `latency_ms`, `outcome`, `token_estimate_method`.

## The model

Each row of the table is one fact a reviewer needs. "Column" is the key on the audit row. "YAML id" is the id in the semantic layer. "Today" says whether a row holds a value for that fact.

### Group 1: actor (who)

| Fact | Column | YAML id | Today |
|---|---|---|---|
| The persona that acted | `actor` | `field.event.actor`, `provenance.actor` | In part. A persona word for `operator`, `engineer`, `ai_agent`. Null for other roles and for a missing header. |
| The role word the caller sent | `role` | None for the column (LS-Q3). Values are `role.*` ids. | Yes, as typed. Null when the header was missing. |
| The named person | None | None (LS-Q2) | No. |

### Group 2: request (what was asked)

| Fact | Column | YAML id | Today |
|---|---|---|---|
| The kind of call | `action` | `status.code.audit_action.record_read`, `status.code.audit_action.ai_summary`. `policy.deny` and `policy.hold` have none (LS-Q4). | Yes. Four words: `record.read`, `ai.summary`, `policy.deny`, `policy.hold`. |
| The thing acted on | `resource` | None for the column (LS-Q5). Value is `resource.device`. | Yes, but always the same value. |
| The time | `ts` | None (LS-Q1) | Yes. UTC, no zone marker (`replay-log.md` section 5, item 9). |
| The record the caller asked for | None | None (LS-Q7) | No. |
| The route and method | None | None | No. |

### Group 3: data used

| Fact | Column | YAML id | Today |
|---|---|---|---|
| A fingerprint of the prompt | `prompt_hash` | `provenance.prompt_hash` | Yes, when the model ran. SHA-256 of the prompt text. |
| Which prompt wording was used | None | None (`model-provenance-design.md` open question) | No. |
| Which device cells the caller received | None | None | No. A record read returns `mgmt_ip` and `credential_profile` to every allowed role (`SB-06`). The row does not say so. |

### Group 4: model

| Fact | Column | YAML id | Today |
|---|---|---|---|
| Model name | `model` | `provenance.model`, `field.ai_invocation.model`, `status.code.model.local_sim_v1` | Yes, when the model ran. |
| Model version | `model_version` | `provenance.model_version` | Yes, but it holds the same string as the name (`SB-15`). |
| Tokens used | `tokens` | `provenance.tokens`, `field.ai_invocation.token_count` | Yes, as an estimate. |
| How the token number was made | `token_estimate_method` | None (open question in `log-schema.md`) | Yes, on rows with tokens. Holds `word_count_x2_EDUCATIONAL`. |
| Time the model took | `latency_ms` | `provenance.latency_ms`, `field.event.latency_ms` | Yes, when the model ran. |

### Group 5: policy

| Fact | Column | YAML id | Today |
|---|---|---|---|
| Allow or deny | `policy_decision` | `concept.policy_decision`, `provenance.policy_result` (LS-Q6) | No. Null on every row. The `action` word carries it. |
| The AI outcome word | `outcome` | `policy.outcomes`, `outcome.*` | Yes on summary rows and on AI blocks. Null on a record read and on an access deny. |
| The reasons | None | None (LS-Q7) | No. |
| The policy version | None | None | No. |

### Group 6: approval

| Fact | Column | YAML id | Today |
|---|---|---|---|
| The stored approval | `approval_id` | `provenance.approval_id`, `concept.approval`, `resource.approval` | Null until S07. |
| Who approved, and yes or no | None | None | No. `SB-08`. |

### Group 7: final action

| Fact | Column | YAML id | Today |
|---|---|---|---|
| What changed in the world, or none | None | None | No. By the code, no route changes anything. |

### Group 8: trace

| Fact | Column | YAML id | Today |
|---|---|---|---|
| The id that ties the rows of one request together | `correlation_id` | `field.event.correlation_id`, `provenance.correlation_id` | Yes. 144 of 144 new rows. |

The 15 keys have no key named `trace_id`. Defence question 5 asks for a trace id. This model names `correlation_id` as the answer. **Verified Fact:** `trace-design.md` says "The chain id is one string named `correlation_id`." The same string is on the response header `X-Correlation-Id`. **Inference:** the repo has no second id and no span id, so no other field can be the trace id.

Open question for S03: the YAML has no `trace_id` and no span id. Defence question 5 asks for a trace id. This design uses `correlation_id` for it and needs S03 to confirm that, or to add a separate id.

### Group 9: cannot be proven

This group is not a column. It is a list the route computes. Each item has a rule: the value of a field, or a fixed fact about the log.

| Item | Rule that puts it on the list | Why it cannot be proven today |
|---|---|---|
| Approval | `approval_id` is null on every row of the case | No approval route exists (S07). |
| Policy decision | `policy_decision` is null on every row of the case | The code never writes it. The `action` word is the only trace. |
| Model call | `model` is null on every row of the case | No row shows a model call. A call that stopped before the model has no hash. |
| Actor | `actor` is null on at least one row | The role has no persona, or the header was missing. |
| Final action | Always listed | No column holds it. |
| Record asked for | Always listed | No column holds it. |
| Reasons and policy version | Always listed | No column holds them. |
| Who the caller really was | Always listed | The role is a typed word (`SB-09`). |
| Which rows belong to the case | Always listed | The caller chose the id, and another caller can reuse it (finding AG-05). |
| Log integrity | Always listed | The log is a plain file. A line can be changed or deleted (`SB-12`). The route cannot prove a case is complete or unchanged. |
| Rows from before the id | Always listed | 96 old lines have no `correlation_id` (`AG-01`). |

Worked example. A case has three rows. All three have `approval_id` null and `policy_decision` null. Two have `model` null. The first rule puts "Approval" on the list. The second puts "Policy decision" on the list. The third rule does not fire, because one row has a model. The "Always listed" items appear on every case.

Open question for S03: the YAML has no id for an item on the "cannot be proven" list. This design needs ids so the route can return stable names and S09 can count them.

## Facts with no column

| Fact | Open question for S03 |
|---|---|
| Record asked for | Already LS-Q7 in `log-schema.md`. This design needs a field id for the record id. |
| Route and method | Open question for S03: there is no field id for the route a call used. This design needs one if the record id alone is not enough. |
| Prompt wording version | Already in `model-provenance-design.md`. This design needs an id for `prompt_template_version`. |
| Device cells returned to the caller | Open question for S03: there is no field that says which sensitive cells a response held. This design needs one so a reviewer can see who received `mgmt_ip`. |
| Reasons | Already LS-Q7. This design needs an id for the reason list. |
| Policy version | Already in `model-provenance-design.md`. This design needs an id and a value format. |
| Approver and decision | Already filed in S04-06 (`SB-08`). This design needs both on the approval record. |
| Final action | Open question for S03: there is no id for the final action of a decision. This design needs one with a value for "none". |
| Named person | Already LS-Q2. |

## How the model maps to the completeness metric

`metric.audit_completeness` counts the required fields on one row. Its list (`ts`, `action`, `actor`, `correlation_id`, `record_id`, and for a model call `model`, `approval_id`, `policy_result`) is PROPOSED. Owner: Team-Force. Against this model, `record_id` and `policy_result` have no filled column. Every row scores below 1.0 on a model call until those two are written. **Inference:** the metric formula applies to the key counts. This stage did not recompute the metric.

## Findings

### DP-01

| | |
|---|---|
| Finding | Of 24 facts, 15 have a column on the row today. 9 have no column. 7 items are always on the "cannot be proven" list. |
| Evidence | **Verified Fact.** The tables above in groups 1 to 8, counted against `SCHEMA_KEYS` and the YAML ids in `log-schema.md`. |
| Impact | A reviewer can rebuild who, which model, and which trace from the row. A reviewer cannot rebuild which record, why the policy decided, or what changed. |
| Risk | High. Those three are the core of defence question 5. |
| Confidence | High |
| Open questions | The nine lines in "Facts with no column". |

### DP-02

| | |
|---|---|
| Finding | `correlation_id` answers "trace id". It is a request id and has no order of steps inside it. |
| Evidence | **Verified Fact.** `trace-design.md` ("The id"). **Inference:** step order comes from `ts` and file order only. |
| Impact | A reviewer orders rows by time. Two rows in one millisecond have no tie-break except file order. |
| Risk | Low. |
| Confidence | Medium |
| Open questions | The trace id question above. |

## Lifecycle

`evidence-chain-one-case.md` applies this model to one case. Half B computes the "cannot be proven" list from the rules in group 9. Stage S07 fills `approval_id` and the final action. Stage S05R folds the open questions into the YAML.
