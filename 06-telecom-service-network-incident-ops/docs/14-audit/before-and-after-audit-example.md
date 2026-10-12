# Before and after audit example

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The same request, `POST /ai/summarize/REC-0001`, is shown as it was in S00 and as it is now. The row grew from 3 keys to 15. The request with no role header returned 200 then and returns 403 now. The new row answers more questions, and it also dropped the record id and the refusal reasons. |
| Evidence sources | `docs/00-setup/replay-log.md` (sections 2.7 and 3); `docs/02-baseline/behaviour-snapshot.md` (the summary call and its captured audit lines); `docs/09-ai-guardrails/evidence.md` ("Before and after"); `docs/08-observability/evidence.md`; a scratch run of the real app on 2026-10-12 (script in `evidence-chain-one-case.md`, calls A and B); `apps/api/services/audit.py` |
| Assumptions | The "after" rows were written by the app to a temporary file. They are REAL rows from the current code. The summary text in the response is SIMULATED. No row holds a secret, so no value is redacted. |
| Unresolved issues | None new. The record id and the reasons are open in `audit-gap-report.md` (AG-02, AG-03). |
| Residual risks | A reader can think the new row is better on every question. Two questions are answered less well than before. The table in "What changed" shows which. |

## What this file is

This file puts the S00 audit row for one call next to the row the same call writes now. It shows both rows in full.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The call

`POST /ai/summarize/REC-0001`. In S00 the call sent no `X-User-Role` header. That is the call in `replay-log.md` section 2.7 and `behaviour-snapshot.md`.

Since S04-06, the same call with no header is refused. So this file shows two "after" calls:

- **After A.** The exact S00 call: no role header. This is the like-for-like call.
- **After B.** The same call with `X-User-Role: operator`. This is the like-for-like success path. It lets the row be compared with the S00 success.

## Before: S00

Status 200. **Verified Fact:** `replay-log.md` section 2.7.

Response body:

```json
{"model":"local-sim-v1","summary":"Synthetic summary for REC-0001","recommendation":"Review and approve before action","token_estimate":64,"source_count":1,"guardrail_status":"not_enforced"}
```

Audit row, written at 2026-10-08 18:58 UTC. **Verified Fact. REAL.** `replay-log.md` section 3, line 6:

```json
{"ts": "2026-10-08T18:58:49.478925", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
```

3 keys. The row has no actor, no role, no correlation id, no policy result, no approval id, no model version, no prompt hash, and no outcome. The prompt held the whole device row, including `mgmt_ip` and `credential_profile` (defect F12). The row stores none of that and does not say it happened.

## After A: the same call, no role header

Status 403. Response body `{"error":"forbidden"}`. The model did not run. **Verified Fact.** Scratch run, call A, correlation id `s0514-after-noheader`. `test_ai_summarize_refuses_request_with_no_role_header` checks the same behaviour.

Audit row, 15 keys:

```json
{"ts": "2026-10-12T07:23:27.873626", "correlation_id": "s0514-after-noheader", "actor": null, "role": null, "action": "policy.deny", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

The call was a summary request with no role. The row records it as a refusal (`policy.deny`). In S00 the same call was a success and the row said `ai.summary`.

## After B: the same call with `X-User-Role: operator`

Status 200. The model ran. **Verified Fact.** Scratch run, call B, correlation id `s0514-after-operator`.

Response body. The summary text is SIMULATED.

```json
{"record_id": "REC-0001", "summary": "Synthetic summary for REC-0001", "recommendation": "Review and approve before action", "outcome": "RECOMMEND_ONLY", "model": "local-sim-v1", "model_version": "local-sim-v1", "prompt_hash": "e17907200e7e3bae144dba21da6f6056952d8382a5fdc24cb8744125dd5ab61d", "tokens": 90, "latency_ms": 11, "source_count": 1, "guardrail_status": "enforced", "approval_required": false, "policy_result": "allow", "approval_id": null, "correlation_id": "s0514-after-operator", "reasons": ["ai_use.incident_summary"], "policy_version": "0.1.0-proposed"}
```

Audit row, 15 keys:

```json
{"ts": "2026-10-12T07:23:27.891018", "correlation_id": "s0514-after-operator", "actor": "noc_operator", "role": "operator", "action": "ai.summary", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": "local-sim-v1", "model_version": "local-sim-v1", "prompt_hash": "e17907200e7e3bae144dba21da6f6056952d8382a5fdc24cb8744125dd5ab61d", "tokens": 90, "latency_ms": 11, "outcome": "RECOMMEND_ONLY", "token_estimate_method": "word_count_x2_EDUCATIONAL"}
```

The `prompt_hash` is the same as in the chain case for `REC-0001`. The same prompt gives the same hash (`test_gr11_same_prompt_gives_the_same_hash`). The token number changed from 64 to 90 because the prompt text changed, not the record (`docs/09-ai-guardrails/evidence.md`).

## What changed, question by question

| Question | Before (S00 row) | After B (row today) | Change |
|---|---|---|---|
| Who? | Nothing. The summary route checked no role. | `actor` `noc_operator`, `role` `operator`. The role is the caller's claim. | Better |
| What request? | `action` `ai.summary` and `details.record_id` `REC-0001`. | `action` `ai.summary`. No record id. | Worse. The record is gone from the row. |
| What data? | The record id only. Nothing about the prompt. | `prompt_hash`. A reviewer rebuilds the prompt from the device row and compares. | Better |
| Which model and version? | `local-sim-v1` as `details.model`. No version. | `model` and `model_version`, both `local-sim-v1`. | Better, with the limit that both are the same text |
| Which policy result? | None. The route called no policy. | `outcome` `RECOMMEND_ONLY`. `policy_decision` null. Reasons and version are in the body only. | Better than none. Still partial. |
| Which approval? | None. | `approval_id` null. | Same. S07 fills it. |
| Final action? | None. | None. | Same |
| Trace id? | None. | `correlation_id` `s0514-after-operator`. | Better |
| Cost and tokens? | Not stored. | `tokens` 90, `latency_ms` 11, method `word_count_x2_EDUCATIONAL`. | Better. The number is an estimate. |

And for the refused call (After A against the S00 row):

| Question | Before (S00, success) | After A (refusal) |
|---|---|---|
| Was it allowed? | Yes. 200. No policy ran. | No. 403. `action` `policy.deny`. `policy_decision` null. |
| Who? | Nothing. | `actor` null, `role` null. The header was missing. |
| Was the refusal recorded? | Not applicable. | Yes. One row, with an id. |

## Findings

### BA-01

| | |
|---|---|
| Finding | The row grew from 3 keys to 15. Of the 8 provenance questions, 5 are answered better, 1 is answered worse (request), and 2 are unchanged (approval and final action). |
| Evidence | **Verified Fact.** The two rows above. `audit.py` `SCHEMA_KEYS`. |
| Impact | A reviewer can name the model, the hash, and the trace id for a summary. |
| Risk | Low. |
| Confidence | High |
| Open questions | None. |

### BA-02

| | |
|---|---|
| Finding | The new row dropped the record id. The old row had it. |
| Evidence | **Verified Fact.** Before row: `details.record_id`. After row: no such key. `log-schema.md` LS-Q7. |
| Impact | A reviewer cannot tell which record a summary was about, except by trying hashes. |
| Risk | High. |
| Confidence | High |
| Open questions | Open question for S03: a field id for the record id (LS-Q7). |

### BA-03

| | |
|---|---|
| Finding | The same call with no header went from 200 to 403. The audit row for it changed from `ai.summary` to `policy.deny`. |
| Evidence | **Verified Fact.** `replay-log.md` section 2.7 and call A. `test_ai_summarize_refuses_request_with_no_role_header`. |
| Impact | Past `ai.summary` rows from S00 for no-header calls mean "answered". Today the same word means "answered for a caller with a role". A reader who counts `ai.summary` rows over time mixes the two. |
| Risk | Low. |
| Confidence | High |
| Open questions | None. |

## Lifecycle

Stage S09 can cite this file as the before-and-after example for Challenge 14. Half B's route returns row B (After B) as part of a chain.
