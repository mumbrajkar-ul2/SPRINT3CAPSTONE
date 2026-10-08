# Replay log

| Field | Value |
|---|---|
| Stage | S00 — Setup and first replay (Execution Plan Phase 0) |
| Date / version | 2026-10-08, v1.0 |
| Author | Mangesh (FDE), run with Cursor |
| Status | CONDITIONAL PASS |
| Evidence sources | Commands run in `.venv` on this machine; `logs/audit.log`; `Project_Intent.md` Appendix D |
| Assumptions | The repo as copied into this workspace is the inherited baseline. No file under `apps/`, `tests/`, `data/`, `etl/`, `legacy/`, or `policy/` was changed in this stage. |
| Unresolved issues | `requirements.txt` does not include `httpx`, so the test suite cannot collect on a clean install (see item 1). The repo folder is not a git repository, so there is no commit history to cite. |
| Residual risks | The CI workflow installs `requirements.txt` and runs `pytest -q`. On a clean runner it would fail at collection for the same `httpx` reason, unless the runner image already has `httpx`. Unknown until CI is run. |

## What this file is

This file records what the inherited repo does today. Every result below came from a command or an HTTP call run on 2026-10-08. Nothing in the repo was edited. One package (`httpx`) was installed into the local `.venv` only, so the tests could run. That package is not in `requirements.txt`.

## 1. Commands

### 1.1 Create venv and install

Commands:

```text
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Result: install succeeded. Packages installed are listed in `tool-versions.md`.

### 1.2 `pytest -q` on a clean install

Result: **collection error**. Exit code 2.

```text
ERROR collecting tests/test_api_contract.py
RuntimeError: The starlette.testclient module requires the httpx package to be installed.
1 error in 1.49s
```

Finding (Verified Fact): `tests/test_api_contract.py` imports `fastapi.testclient.TestClient`. Starlette 0.38.6 needs `httpx` for that class. `requirements.txt` does not list `httpx`. So the test suite does not run on the pinned requirements alone.

- Evidence: the error above; `requirements.txt` (six pins, no `httpx`).
- Impact: a new team following `README.md` Quick Start sees a broken test run before any real test runs.
- Risk: CI may be green only because the runner image carries `httpx`. Unknown.
- Confidence: high for the local result; Unknown for CI.
- Open question: should `httpx` be added to `requirements.txt` (a Phase 4, Challenge 5 or 7 change)?

Action taken in this stage: `pip install httpx` into `.venv` only. `requirements.txt` was not edited.

### 1.3 `pytest -q -v` after installing `httpx` locally

Result: **3 passed**, 2 warnings. Exit code 0.

```text
tests\test_api_contract.py::test_health_contract PASSED
tests\test_api_contract.py::test_ai_summary_has_minimum_contract PASSED
tests\test_characterization.py::test_missing_record_returns_first_row PASSED
3 passed, 2 warnings in 1.09s
```

Warnings (Verified Fact):

- `apps/api/services/audit.py:9`: `datetime.utcnow()` is deprecated. The audit timestamp has no timezone.
- `starlette/testclient.py:40`: an anyio alias deprecation inside the library. Not the repo's code.

Side effect (Verified Fact): the AI contract test called the summarize route, which wrote the first line of `logs/audit.log`. The `logs/` folder did not exist before this run.

Match with Appendix D: match. Appendix D says three tests lock health, the AI minimum shape, and the first-row fallback.

### 1.4 `python scripts/sanity_check.py`

Result: exit code 0.

```text
{'status': 'ok', 'repo': '06-telecom-service-network-incident-ops', 'csv_files': 6, 'events': 3000, 'clean_repo_contract': True}
```

Match with Appendix D and `data/manifest.json`: match. Six CSVs, 3000 events, no forbidden workshop path present.

### 1.5 `python etl/run_daily_batch.py --sample`

Result: exit code 0.

```text
{'processed': 354, 'malformed': 1, 'sample': True}
```

Match with Appendix D: match. The ETL counts rows in `devices.csv` and increments `malformed` when any field is blank. It prints counts. It writes no quarantine file. One row in `devices.csv` has a blank field.

## 2. HTTP replay

Server: `uvicorn apps.api.main:app --port 8011`. Started and stopped by a temporary script. Each call below shows the request, the status, and the body.

### 2.1 `GET /health` (no header)

Status 200.

```json
{"status":"ok","repo":"06-telecom-service-network-incident-ops"}
```

Match with Appendix D: match. No audit row was written for this call.

### 2.2 `GET /records/REC-0001` with `X-User-Role: operator`

Status 200.

```json
{"device_id":"REC-0001","hostname":"legacy","vendor":"requires_review","device_type":"manual","site_id":"SIT-00001","network_zone":"remote-6","mgmt_ip":"gamma","firmware":"vendor","owner_team":"normal","credential_profile":"vendor","last_seen_at":"2026-05-28T13:24:00","stale_topology_flag":"false"}
```

Match with Appendix D: match. `hostname` is `legacy` and `vendor` is `requires_review`. Those are status words in the wrong columns. The response also returns `mgmt_ip` and `credential_profile` to the caller. Appendix D does not say that; it is an added observation (Verified Fact).

Audit row written: `{"action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}`.

### 2.3 `GET /records/DOES-NOT-EXIST` with `X-User-Role: operator`

Status **200**, not 404.

Body: identical to 2.2. `device_id` is `REC-0001`.

Match with Appendix D: match. A missing id returns the first device row.

Audit row written: `{"action": "record.read", "details": {"record_id": "DOES-NOT-EXIST", "role": "operator"}}`. The audit row names the id the caller asked for. The response holds a different device. The audit row and the response disagree about which device was read (Verified Fact; this is an added observation).

### 2.4 `GET /records/REC-0001` with no role header

Status 200. Body identical to 2.2.

Audit row written: `{"action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}`.

Finding (Verified Fact): with no header, the API treats the caller as `operator`. `main.py` sets that default.

### 2.5 `GET /records/REC-0001` with `X-User-Role: clinician`

Status 200. Body identical to 2.2.

Audit row written with `"role": "clinician"`.

Match with Appendix D: match. `clinician` is in the allow list although it is not a telecom persona.

### 2.6 `GET /records/REC-0001` with `X-User-Role: vendor`

Status **200** with body `{"error":"forbidden"}`.

Findings (Verified Fact):

- The role is refused, but the HTTP status is 200, not 403. A client that checks status codes sees success.
- **No audit row was written for this refused call.** The audit log has no record of denied access.

Appendix D does not cover this call. These are added observations.

### 2.7 `POST /ai/summarize/REC-0001` (no header)

Status 200.

```json
{"model":"local-sim-v1","summary":"Synthetic summary for REC-0001","recommendation":"Review and approve before action","token_estimate":64,"source_count":1,"guardrail_status":"not_enforced"}
```

Match with Appendix D: match. No role check. `guardrail_status` is `not_enforced`. `token_estimate` 64 is `len(prompt.split()) * 2` (EDUCATIONAL).

Audit row written: `{"action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}`. No actor, no role, no correlation id, no prompt hash, no outcome.

### 2.8 `POST /ai/summarize/DOES-NOT-EXIST` (no header)

Status 200.

```json
{"model":"local-sim-v1","summary":"Synthetic summary for REC-0001", ...same as 2.7}
```

Finding (Verified Fact): the AI route inherits the first-row fallback. A summary for a device that does not exist is a summary of `REC-0001`. The audit row says `record_id: DOES-NOT-EXIST`. Appendix D does not cover this call. Added observation.

### 2.9 `GET /openapi.json` (generated by FastAPI)

Paths: `/ai/summarize/{record_id}`, `/health`, `/records/{record_id}`.

Match with Appendix D: match. The live app has three routes. `data/contracts/openapi-fragment.yaml` documents one (`/health`).

## 3. `logs/audit.log` after the replay

Seven lines. Line 1 came from pytest (1.3). Lines 2 to 7 came from the replay. The refused `vendor` call (2.6) and the `/health` call (2.1) wrote nothing.

```json
{"ts": "2026-10-08T18:58:26.259133", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
{"ts": "2026-10-08T18:58:49.394239", "action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}
{"ts": "2026-10-08T18:58:49.423408", "action": "record.read", "details": {"record_id": "DOES-NOT-EXIST", "role": "operator"}}
{"ts": "2026-10-08T18:58:49.428949", "action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}
{"ts": "2026-10-08T18:58:49.434307", "action": "record.read", "details": {"record_id": "REC-0001", "role": "clinician"}}
{"ts": "2026-10-08T18:58:49.478925", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
{"ts": "2026-10-08T18:58:49.524986", "action": "ai.summary", "details": {"record_id": "DOES-NOT-EXIST", "model": "local-sim-v1"}}
```

Row shape (Verified Fact): `ts`, `action`, `details`. No actor, no correlation id, no approval id, no policy decision, no outcome.

## 4. Match table against Appendix D

| Appendix D line | Replayed | Result |
|---|---|---|
| Health returns status ok and repo name | 2.1 | Match |
| REC-0001 read is allowed for operator; hostname `legacy`, vendor `requires_review` | 2.2 | Match |
| Missing id returns first row, not 404 | 2.3 | Match |
| `clinician` is allowed | 2.5 | Match |
| AI summarize has no role header; returns model, summary, recommendation, token estimate, source_count 1, `not_enforced`; audit stores record id and model only | 2.7, section 3 | Match |
| ETL counts rows and increments malformed on a blank field; no quarantine file | 1.5 | Match |
| Live app has three routes; fragment documents one | 2.9 | Match |
| Three tests exist | 1.3 | Match |

## 5. Observations Appendix D did not list

These are Verified Facts from this replay. They feed Phase 1 (risk register) and Phase 2 (defect list).

1. `requirements.txt` lacks `httpx`; the test suite does not collect on a clean install.
2. The record response returns `mgmt_ip` and `credential_profile` to any allowed role.
3. The audit row for a missing id names the requested id while the response holds `REC-0001`.
4. No role header is treated as `operator`.
5. A refused role gets HTTP 200 with `{"error":"forbidden"}`, and no audit row is written.
6. The AI route inherits the first-row fallback: a summary for a missing id is a summary of `REC-0001`.
7. `/health` writes no audit row (expected for a health check; recorded for completeness).
8. The repo folder is not a git repository. There is no commit history.
9. `audit.py` uses `datetime.utcnow()`; timestamps carry no timezone.

## 6. Stage result

- Stage status: **CONDITIONAL PASS**. All three commands and all four required calls ran. Every Appendix D line matched. The condition: `pytest` needed `httpx` installed outside `requirements.txt` to run at all. That gap is recorded here and is not fixed in this stage.
- Key findings: items 1 to 9 above.
- Major risks: CI may not run the tests on a clean runner; denied access is not audited; sensitive fields are returned and could enter prompts.
- Assumptions and unknowns: CI behaviour is Unknown until a run is seen. Owners are Unknown.
- Artifacts created: `docs/00-setup/replay-log.md`, `docs/00-setup/tool-versions.md`, `logs/audit.log` (7 lines, written by the app).
- Blocking issues: none.
- Recommended next action: Stage S0B, the operating contract. Decide there whether the repo folder should become a git repository so later changes can be diffed.
