# Model provenance design

| Field | Value |
|---|---|
| Stage | S04-09 — AI security and guardrails (Challenge 9), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Seven fields are listed. One of them has no YAML id. The timeout is a separate unset number and is not one of these seven. |
| Evidence sources | `semantic-layer/ai-context-policy.yaml` (`provenance`, `model_today`, `output_schema`); `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/main.py`; `docs/08-observability/log-schema.md`; `data/synthetic/ai_invocations.csv`; `docs/06-policy/ai-action-policy-design.md` |
| Assumptions | Half B writes `local-sim-v1` in both `model` and `model_version`. They are the same string. A distinct version does not exist in the repo. |
| Unresolved issues | `prompt_template_version` has no YAML id. The hash algorithm has no YAML id. `policy_version` has no YAML id. The production timeout number is null. |
| Residual risks | Older lines in `logs/audit.log` keep the shape they were written with. New rows use the fourteen keys. This design does not rewrite old lines. |

## What this file is

This file says which facts about a model call are stored on the audit row, which of those facts exist today, and where the value comes from. The stored stand-in for the prompt text is `prompt_hash`. The prompt text stays off the row.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The seven fields

| Field | Exists today | Where it is today | Where Half B writes it | YAML id |
|---|---|---|---|---|
| `model` | Yes, on the response body. The value is `local-sim-v1`. The audit column exists and the value written now is null. | `ai_gateway.py` line 12. `audit.py` lines 69 to 74 set null. The playbook locked fact says model only, which matches the response body. | Audit column `model`, and the response field `model`. | `provenance.model`. `present_today: true`. |
| `model_version` | No. The string `local-sim-v1` is the model name. There is no second version field. | `provenance.model_version` says `present_today: false`. `log-schema.md` says the column stays null until a separate version exists. | Audit column `model_version` set to `local-sim-v1`, the same string as `model`. | `provenance.model_version` |
| `prompt_hash` | No. | Absent from the body and from the values `write_event` stores. | Audit column `prompt_hash` when a prompt was built. Null when the model was not called. The prompt text is not stored. | `provenance.prompt_hash` |
| `prompt_template_version` | No. | The template string exists as `PROMPT_TEMPLATE` and as `model_today.prompt_template`. There is no version id. | Not written in Half B, until an id exists. | None. Open question below. |
| `tokens` | The response has `token_estimate`, computed as `len(prompt.split()) * 2`. The audit column `tokens` is null. The CSV column is `token_count`. | `ai_gateway.py` line 10. `provenance.tokens` says the body name is `token_estimate` and the value is not on the audit row. | Audit column `tokens`. The response field name becomes `tokens`. The stub number stays a word-count estimate and is labeled SIMULATED. | `provenance.tokens`; `field.ai_invocation.token_count` |
| `latency_ms` | No, on the live call. `events.jsonl` has the key on event lines. The gateway records nothing. | `provenance.latency_ms`: `present_today: false`. `ai_gateway.py` line 9 sleeps 0.01 seconds and does not store the elapsed time. | Audit column `latency_ms`, measured around the model call. | `provenance.latency_ms`; `field.event.latency_ms` |
| `policy_version` | The policy return value includes it. The audit row has no column for it. | `evaluate_ai_action` returns `policy_version` (`policy.py` lines 226 to 229). `audit.py` `SCHEMA_KEYS` has no `policy_version`. | The HTTP body already can carry the policy's `policy_version`. This design does not add an eighth audit column. | None. S04-06 open question. The code value is `POLICY_VERSION`, read from the policy data file. |

Worked example. A successful summarize of `REC-0001` after Half B writes one audit line. `model` is `local-sim-v1`. `model_version` is `local-sim-v1`. `prompt_hash` is a hash of the allow-list prompt for that row. `tokens` is the SIMULATED estimate. `latency_ms` is the measured wait, which today is about the 0.01 second sleep plus the work around it. `prompt_template_version` is absent. `policy_version` is on the HTTP body and not on the audit line.

A BLOCK before the model, such as `DEV-00003` with a true stale flag, writes the same fourteen keys. `outcome` is BLOCK. The five model fields are null. There is no hash, because no prompt was sent.

## What the CSV is

`data/synthetic/ai_invocations.csv` line 1 names `model`, `token_count`, `approval_required`, and `guardrail_status`. It does not name `prompt_hash`, `model_version`, `latency_ms`, or `policy_version`. Line 2 puts `not_enforced` in the `model` column and `requires_review` in `guardrail_status`. **Verified Fact.** That file is not a provenance record for the live call. The live call's model name is `local-sim-v1` in `ai_gateway.py`.

## What is not stored

The audit row does not store the prompt text, `mgmt_ip`, `credential_profile`, or a secret. **Verified Fact:** `audit.py` lines 52 to 56. `log-schema.md` says the same. `prompt_hash` is how a reviewer proves what was sent without keeping the text (`provenance.prompt_hash`).

The summary sentence is not an audit field. On HOLD or BLOCK from a failed call, `summary` in the HTTP body is null, so a failure does not add a sentence to the log either.

## Hash and template version

Open question for S03: `prompt_template_version` has no id. This design needs it so the audit row can name which prompt wording was used. The wording today is `Summarize this operational record and recommend next action: {record}` (`ai_gateway.py` line 4 and `model_today.prompt_template`). Half B changes the wording to the allow list. Until the id exists, the hash of the built prompt is the record of what was sent.

Open question for S03: the hash algorithm for `prompt_hash` has no id. This design needs the algorithm name so two runs of the same prompt can be compared. This file does not name an algorithm.

Open question for S03: `policy_version` has no id and no value format. This design needs it on the audit row only if a reviewer must see the policy version beside the model hash. S04-06 already returns it on the policy object. This stage leaves the audit schema at fourteen fields.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| MP-01 | Of the seven fields, only `model` is filled today, and only on the response body. | **Verified Fact.** `ai_gateway.py` lines 11 to 17. `audit.py` lines 69 to 74. | A reviewer of the log cannot reconstruct the call. | Every new audit row. | High | Template version, hash algorithm, policy version id. |
| MP-02 | The response field is `token_estimate`. The audit column is `tokens`. They are different names. | **Verified Fact.** `ai_gateway.py` line 15. `provenance.tokens`. | A reader can think the audit column is already filled. | The column is null. | High | None. |
| MP-03 | `model_version` will copy the model name. | **Assumption.** `provenance.model_version` says the string doubles as the version. `log-schema.md` says stay null until a separate version exists. | The column is filled with a string the repo already has. | A reader can think a second release was deployed. The evidence file must say the strings match. | Medium | A real version string is Unknown. |

## Lifecycle

`docs/08-observability/log-schema.md` owns the fourteen columns. This stage fills five of them when the model runs. Stage S04-12 reads `tokens` for cost. Stage S07 writes `approval_id`, which stays null here.
