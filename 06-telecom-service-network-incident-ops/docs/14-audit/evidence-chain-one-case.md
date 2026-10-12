# Evidence chain for one case

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. One case, `s0514-case-0001`, has 3 stored rows in time order. The rows show who asked, which kind of call it was, which model answered, and the trace id. Five facts are missing or unproven: which record, why the policy decided, the policy decision value, the approval, and the final action. |
| Evidence sources | A scratch run of the real app on 2026-10-12 (script below), with the audit log pointed at a temporary file; `apps/api/main.py`; `apps/api/services/audit.py`; `apps/api/services/policy.py`; `apps/api/services/ai_gateway.py`; `docs/14-audit/decision-provenance-model.md`; `docs/03-identity/target-access-matrix.md` (rows TA-01 and TA-06); `policy/opa/policy_data.json` |
| Assumptions | The Python copy of the policy ran (`POLICY_ENGINE=python`). `opa` was not on the PATH in this shell. The rows are REAL: the app wrote them. The model is the stub `local-sim-v1`, so its summary text is SIMULATED. The text is not stored in any row. |
| Unresolved issues | See "What is still missing". The "Open question for S03:" lines for these items are in `audit-gap-report.md` and `decision-provenance-model.md`. This file adds none. |
| Residual risks | A different caller can reuse the id and add a row to this case (call E below). The rows live in a temporary file that this stage did not keep. The doc holds the copy. |

## What this file is

This file rebuilds one case from stored rows, the way Half B's route will. It answers the nine parts of defence question 5 for one case, and marks what the rows cannot answer.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Why this id was made and not taken from the real log

`logs/audit.log` has 144 rows with a `correlation_id`, and every id appears once. **Verified Fact. REAL.** The real log holds no case with more than one row. Test runs also add rows to it (`docs/13-security-validation/evidence.md`, EV-07). So this stage chose an id, `s0514-case-0001`, and made three calls with it.

The calls wrote to a temporary file. `logs/audit.log` was not changed. **Verified Fact:** `git status --short logs` printed nothing after the run, and the file still has 240 lines.

## The three calls

All three used `X-Correlation-Id: s0514-case-0001`. Each response echoed that id in its `X-Correlation-Id` header. **Verified Fact.**

| Step | Request | `X-User-Role` | HTTP status | What the body held |
|---|---|---|---|---|
| 1 | `GET /records/REC-0001` | `operator` | 200 | The `REC-0001` device row. It includes `mgmt_ip` and `credential_profile`. Both values are redacted here. |
| 2 | `POST /ai/summarize/REC-0001` | `operator` | 200 | `outcome` `RECOMMEND_ONLY`, `policy_result` `allow`, `approval_id` null, `reasons` `["ai_use.incident_summary"]`, `policy_version` `0.1.0-proposed`. The summary is SIMULATED. |
| 3 | `GET /records/REC-0001` | `clinician` | 403 | `{"error": "forbidden"}` |

Step 1 returned both sensitive cells to the operator. That is backlog row `SB-06`. The audit row for step 1 does not say so.

## The stored rows, in time order

These are the three rows that share the id, in full. Every key is shown. Nothing was removed, because no row holds a secret. **Verified Fact.** A search of the temporary log for `mgmt_ip` and `credential_profile` found neither.

Row 1, `record.read`:

```json
{"ts": "2026-10-12T07:23:27.829397", "correlation_id": "s0514-case-0001", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

Row 2, `ai.summary`:

```json
{"ts": "2026-10-12T07:23:27.850004", "correlation_id": "s0514-case-0001", "actor": "noc_operator", "role": "operator", "action": "ai.summary", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": "local-sim-v1", "model_version": "local-sim-v1", "prompt_hash": "e17907200e7e3bae144dba21da6f6056952d8382a5fdc24cb8744125dd5ab61d", "tokens": 90, "latency_ms": 13, "outcome": "RECOMMEND_ONLY", "token_estimate_method": "word_count_x2_EDUCATIONAL"}
```

Row 3, `policy.deny`:

```json
{"ts": "2026-10-12T07:23:27.866817", "correlation_id": "s0514-case-0001", "actor": null, "role": "clinician", "action": "policy.deny", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

## The chain

| Order | `ts` (UTC, 2026-10-12) | `action` | Who | What the row proves | What the row does not say |
|---|---|---|---|---|---|
| 1 | 07:23:27.829 | `record.read` | `noc_operator`, role `operator` | A device read was allowed and served for this id. | Which device. That the policy said allow (the column is null). |
| 2 | 07:23:27.850 (21 ms later) | `ai.summary` | `noc_operator`, role `operator` | The model `local-sim-v1` ran once. The prompt hash, a token estimate of 90, and latency of 13 ms are stored. The AI outcome was `RECOMMEND_ONLY`. | Which device. The reasons. The policy version. |
| 3 | 07:23:27.867 (17 ms later) | `policy.deny` | role `clinician`, no actor | A read was refused. | Which device. Why (no matrix row for the role). |

**Verified Fact.** The three rows are in the order the calls were made. Order here is file order and `ts` order. They agree.

## Defence question 5, answered from the rows

| Part | Answer for this case | Read from | Label |
|---|---|---|---|
| Actor | Steps 1 and 2: a caller who sent `operator`, stored as actor `noc_operator`. Step 3: a caller who sent `clinician`, with no actor. | Rows 1 to 3, `actor` and `role` | Verified Fact for the stored values. The `operator` to `noc_operator` map is an Inference (`access-semantics.yaml`). Nothing proves the caller held either role (`SB-09`). |
| Request | A device read, a summary request, and a refused device read. | Rows 1 to 3, `action` | Verified Fact. The record is not on any row. It is known only because this stage made the calls. Unknown from the rows alone. |
| Data used | The prompt for step 2 has the hash `e17907…ab61d`. This stage rebuilt the prompt from the current `REC-0001` row and got the same hash. The prompt holds 10 allowed fields and holds no `mgmt_ip` and no `credential_profile`. | Row 2, `prompt_hash`. `ai_gateway.build_prompt`. | Verified Fact for the match. The prompt text is not stored. The match holds only while the device row is unchanged. |
| Model and version | `local-sim-v1` and `local-sim-v1`. 90 tokens, estimated by `word_count_x2_EDUCATIONAL`. 13 ms. | Row 2 | Verified Fact. The tokens are an estimate. The version is the name again (`SB-15`). The summary text is SIMULATED and is not stored. |
| Policy result | Step 1: allowed (matrix row TA-01). Step 2: allowed (TA-06), then `RECOMMEND_ONLY`. Step 3: refused, because no row grants `clinician` a read. | Row 2 `outcome`. Rows 1 and 3 `action`. Step 2 body `reasons` and `policy_version`. | The word `RECOMMEND_ONLY` is stored. The allow on step 1 is an Inference from the word `record.read`. The reasons and the version are in the HTTP body only. They are not stored. |
| Approval | None. No approval was needed for a read or a summary. | Rows 1 to 3, `approval_id` null | Verified Fact that the column is null. No approval route exists until S07. |
| Final action | None. No device changed. | No column. `test_no_route_can_execute`. | Inference from the code and the test. No row says it. |
| Trace id | `s0514-case-0001` | Rows 1 to 3, `correlation_id`. The three response headers. | Verified Fact. The caller chose the id. |
| What cannot be proven | See the next section. | | |

## What is still missing

| Item | Status | Why |
|---|---|---|
| `approval_id` | Null on 3 of 3 rows | S07 builds the approval route. |
| Final action | No field | The row has no column for it. By the code the answer is "none". |
| Which record | Not stored | The row has no record id (finding AG-03). |
| `policy_decision` | Null on 3 of 3 rows | The code never writes it (finding AG-02). |
| Reasons and policy version | Not stored | They are in the HTTP body only. |
| Which sensitive cells the operator received | Not stored | Step 1 returned `mgmt_ip` and `credential_profile`. No row says so. |
| That the caller held the role | Not proven | The role is a header the caller typed (`SB-09`). |
| That these are all the rows | Not proven | The log is a plain file. A line can be changed or deleted (`SB-12`). A write failure gives HTTP 500, with no id and no row (`RF-04`). |
| That the three calls came from one person | Not proven | The id is chosen by the caller. Call E shows another caller can reuse it. |

## Probes behind the findings

These probes ran in the same scratch run. They wrote to the same temporary file.

### Calls C and D: two refusals with the same stored row

| Call | Request | Status | Body `reasons` |
|---|---|---|---|
| C | `POST /ai/summarize/DEV-00001` as `operator`, id `s0514-other-record` | 403 | `failmode.missing_id` |
| D | `POST /ai/summarize/DEV-00003` as `operator`, id `s0514-stale-record` | 403 | `failmode.stale_topology_true`, `rule.stale_topology_blocks_recommendation` |

Both calls stopped before the model. The two stored rows differ only in `ts` and `correlation_id`. Both read: `action` `policy.deny`, `actor` `noc_operator`, `role` `operator`, `outcome` `BLOCK`, `policy_decision` null, and all model fields null. **Verified Fact.**

### Call E: another caller reuses the id

Call E was `GET /records/REC-0001` with `X-User-Role: ai_agent` and `X-Correlation-Id: s0514-case-0001`. Status 200. It wrote this row:

```json
{"ts": "2026-10-12T07:23:27.907690", "correlation_id": "s0514-case-0001", "actor": "ai_agent", "role": "ai_agent", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

A lookup of `s0514-case-0001` now returns 4 rows, not 3. The fourth row has a different actor. **Verified Fact.** The `actor` column is the only sign that the row came from another caller. The case in this file is the first three rows.

## How to repeat the run

Run from `06-telecom-service-network-incident-ops/` with the repo `.venv` Python. The script points `audit.LOG` at a temporary file, so the tracked log is not changed.

```python
import os, sys, tempfile, json
from pathlib import Path
os.environ["POLICY_ENGINE"] = "python"
sys.path.insert(0, os.getcwd())
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.services import audit, policy

audit.LOG = Path(tempfile.mkdtemp()) / "audit.log"
policy.reset_engine_cache()
client = TestClient(app)
cid = "s0514-case-0001"
client.get("/records/REC-0001", headers={"X-User-Role": "operator", "X-Correlation-Id": cid})
client.post("/ai/summarize/REC-0001", headers={"X-User-Role": "operator", "X-Correlation-Id": cid})
client.get("/records/REC-0001", headers={"X-User-Role": "clinician", "X-Correlation-Id": cid})
for line in audit.LOG.read_text(encoding="utf-8").splitlines():
    print(line)
```

Expected output: three lines with the same `correlation_id` and the `action` words `record.read`, `ai.summary`, `policy.deny`. The `ts`, `latency_ms`, and the response ids differ on each run. The `prompt_hash` stays `e17907…ab61d` while the `REC-0001` row stays the same.

## Findings

### EC-01

| | |
|---|---|
| Finding | One case can be listed from stored rows by one id, in time order. The rows show actor, kind of call, model, version, hash, and trace id. |
| Evidence | **Verified Fact.** Rows 1 to 3 above, from the scratch run. `tests/observability/test_audit_schema.py::test_request_with_header_keeps_the_id`. |
| Impact | Half B has a real chain to test the route against. |
| Risk | Low. |
| Confidence | High |
| Open questions | None. |

### EC-02

| | |
|---|---|
| Finding | Five answers are missing from the rows: which record, the policy decision, the reasons, the approval, and the final action. |
| Evidence | **Verified Fact.** "What is still missing" above. Calls C and D. |
| Impact | The chain shows what happened. It does not fully show why. |
| Risk | High for the policy decision, the record, and the reasons. Medium for the approval and the final action, because nothing changes today. |
| Confidence | High |
| Open questions | Open question for S03 lines in `audit-gap-report.md` (AG-02, AG-03, AG-04). |

### EC-03

| | |
|---|---|
| Finding | The `correlation_id` is not proof that the rows belong to one case. A second caller can add a row. |
| Evidence | **Verified Fact.** Call E. |
| Impact | The Half B route must return `actor` and `role` for each row, so a reader can see a mixed case. |
| Risk | Medium. |
| Confidence | High |
| Open questions | The correlation id form rule (AG-05). |

## Lifecycle

Half B builds `GET /audit/{correlation_id}`. For `s0514-case-0001` it must return rows 1 to 3 in this order and list approval, final action, and log integrity under `cannot_prove`. Stage S07 fills `approval_id` and the final action. Stage S10 answers defence question 5 from the route output.
