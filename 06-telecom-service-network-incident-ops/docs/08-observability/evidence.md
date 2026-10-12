# Observability evidence

| Field | Value |
|---|---|
| Stage | S04-08 — Observability and traceability (Challenge 8), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Every new audit row has the fourteen fields and a `correlation_id`. `pytest tests policy/tests -q` on 2026-10-11: 105 passed, 2 skipped. |
| Evidence sources | `apps/api/services/audit.py`; `apps/api/main.py`; `tests/observability/test_audit_schema.py`; `logs/audit.log` lines 105 to 108; `docs/00-setup/replay-log.md` sections 2.1, 2.2, 2.3, 2.7, and 3; `pytest tests policy/tests -q -rs` on 2026-10-11 |
| Assumptions | The four S00 calls are the four named in `playbook/S00-setup-and-replay.md`: health, the operator read of `REC-0001`, the operator read of `DOES-NOT-EXIST`, and `POST /ai/summarize/REC-0001` with no role header. The replay used `TestClient` against the app. That client runs the same routes a server runs. |
| Unresolved issues | `record_id` and the reason list are off the new row. Open question LS-Q7 in `log-schema.md`. `policy_decision` and `approval_id` are null, as this half's playbook requires. `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` stay null until S04-09. The 2 skipped tests need the `opa` binary. |
| Residual risks | Lines 1 to 96 of `logs/audit.log` keep the old three-key shape. The log is append-only, so those lines stay. A reader who groups the whole file will find 96 lines with no `correlation_id`. Two pytest runs during this half also appended 16 lines to the same file, because some tests still write the real log. |

## What this file is

This file places the S00 audit lines next to the lines the same calls wrote on 2026-10-11, after the fourteen-field row landed.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Tests

Command, from `06-telecom-service-network-incident-ops`, with the repo `.venv` Python:

```text
python -m pytest tests policy/tests -q -rs
```

Result: 105 passed, 2 skipped, in 4.21 seconds on the second run (4.89 seconds on the first). **Verified Fact.**

The skipped tests are `test_opa_and_python_agree_on_access` and `test_opa_and_python_agree_on_every_ai_action_combination`. The skip reason is `opa binary not on PATH`. **Verified Fact:** `policy/tests/test_policy_python.py` lines 524 and 534.

`tests/observability/test_audit_schema.py` checks three things. Every audit row has the fourteen keys. A request that sends `X-Correlation-Id: demo-123` stores `demo-123`. A request that sends no such header stores a UUID, and a header of spaces stores a different UUID.

## The four S00 calls, old line and new line

The old lines are copied from `docs/00-setup/replay-log.md` section 3 and from `logs/audit.log` as it stood after S00. The new lines are `logs/audit.log` lines 105 to 108, written by the replay on 2026-10-11 at 22:20 UTC. **Verified Fact.**

`GET /health` wrote no audit line in S00 and wrote no audit line in this replay. The response status was 200. The response header `X-Correlation-Id` was `1b8e6236-f214-4dc7-9606-6ad496030643`. **Verified Fact.**

### `GET /records/REC-0001` with `X-User-Role: operator`

Status in this replay: 200. The response header was `740ea063-5386-4111-a0de-66c7e1383ee6`.

Old line, S00:

```json
{"ts": "2026-10-08T18:58:49.394239", "action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}
```

New line, `logs/audit.log` line 105:

```json
{"ts": "2026-10-11T22:20:07.535264", "correlation_id": "740ea063-5386-4111-a0de-66c7e1383ee6", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null}
```

The new line has all fourteen keys. `correlation_id` is the UUID the API created. `actor` is `noc_operator` because the role word `operator` maps to that persona. That mapping is an Inference in `access-semantics.yaml`.

### `GET /records/DOES-NOT-EXIST` with `X-User-Role: operator`

Status in this replay: 200. The body is still the `REC-0001` device row. The response header was `6f98208d-2c3c-47b7-8f26-f0a00c1ebc21`.

Old line, S00:

```json
{"ts": "2026-10-08T18:58:49.423408", "action": "record.read", "details": {"record_id": "DOES-NOT-EXIST", "role": "operator"}}
```

New line, `logs/audit.log` line 106:

```json
{"ts": "2026-10-11T22:20:07.551077", "correlation_id": "6f98208d-2c3c-47b7-8f26-f0a00c1ebc21", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null}
```

The old line stored the id the caller asked for, `DOES-NOT-EXIST`. The new line has no `record_id` column. A reader of the new line sees a device read and the chain id. The reader does not see which id was asked for. That gap is open question LS-Q7.

### `POST /ai/summarize/REC-0001` with no role header

Status in this replay: 403. Body `{"error":"forbidden"}`. The response header was `8897dd18-91e5-4861-b7f8-d5979fed67c6`.

Old line, S00:

```json
{"ts": "2026-10-08T18:58:49.478925", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
```

New line, `logs/audit.log` line 107:

```json
{"ts": "2026-10-11T22:20:07.563117", "correlation_id": "8897dd18-91e5-4861-b7f8-d5979fed67c6", "actor": null, "role": null, "action": "policy.deny", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null}
```

S00 returned 200 and wrote `ai.summary`. The same request on 2026-10-11 returns 403 and writes `policy.deny`. S04-06 denies a summarize call that sends no role. `role` and `actor` are null because the header was absent. The action word `policy.deny` is the deny. The column `policy_decision` is null on this row, because this half leaves that column null.

## Done test

`GET /records/REC-0001` with `X-User-Role: operator` and `X-Correlation-Id: demo-123`. Status 200. The response header was `demo-123`.

New line, `logs/audit.log` line 108:

```json
{"ts": "2026-10-11T22:20:07.578844", "correlation_id": "demo-123", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null}
```

`"correlation_id": "demo-123"` is on the line. The other thirteen keys are on the line. **Verified Fact.**

## What the file holds after this half

| Lines | Shape | Count |
|---|---|---|
| 1 to 96 | `ts`, `action`, `details` | 96 |
| 97 to 104 | fourteen fields, written by the first `pytest` run | 8 |
| 105 to 108 | fourteen fields, the replay and the done test | 4 |
| 109 to 116 | fourteen fields, written by the second `pytest` run | 8 |

**Verified Fact. REAL.** Counted from `logs/audit.log` on 2026-10-11. Every line from 97 onward has a non-empty `correlation_id`.

The route tests that used to read `details.reasons` now read `role`, `action`, `outcome`, and `correlation_id`. The reason words `policy.opa.default_deny`, `failmode.stale_topology_true`, and `failmode.missing_id` stay on the policy function result. They are no longer copied onto the audit row. The HTTP 202 body for a hold still returns its reason list.

## Lifecycle

Stage S04-09 fills `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms`. Stage S04-12 computes cost from those rows. Stage S05-14 rebuilds a case from rows that share one `correlation_id`. The 96 older lines have no chain id, so a rebuild of those calls stays a single line each.
