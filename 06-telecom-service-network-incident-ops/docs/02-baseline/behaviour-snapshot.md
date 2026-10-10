# Behaviour snapshot

| Field | Value |
|---|---|
| Stage | S02 — Behavioural baseline (Execution Plan Phase 2; spine stage 7) |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The calls below ran. Five labels in `data/quality_issues.json` were not found in the files. That condition is written in `data-quality-baseline.md`. |
| Evidence sources | TestClient calls on 2026-10-10; `python etl/run_daily_batch.py --sample`; `python legacy/reconcile_legacy.py`; `python scripts/sanity_check.py`; `apps/api/main.py`; `apps/api/services/domain_service.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `docs/00-setup/replay-log.md`; `docs/01-discovery/` |
| Assumptions | The TestClient call uses the same app object as `uvicorn apps.api.main:app`. The replay on 2026-10-08 used uvicorn. The bodies match. |
| Unresolved issues | `engineer` and `ai_agent` were not in the 2026-10-08 replay. They were called in this stage. Whether a deployed caller sends those strings is Unknown. |
| Residual risks | The route calls append to `logs/audit.log`. This stage restored the log to the 13-line file from the start of the stage. Four of those lines are timestamped `2026-10-10T05:51` and were already there. The quoted lines below are from the command output of this stage. |

## What this file is

This file is the before picture. Each section is one route or one script. It records the input, the output, and the side effect on 2026-10-10. Nothing in the application was changed to produce these results.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

The route calls used `fastapi.testclient.TestClient` on `apps.api.main:app`. **Verified Fact.**

## GET /health

**Input.** `GET /health`. No body. No role header.

**Output.** HTTP 200.

```json
{"status": "ok", "repo": "06-telecom-service-network-incident-ops"}
```

**Verified Fact.** This stage's TestClient call. `apps/api/main.py` lines 6 to 8. `test_health_contract` PASSED. Replay section 2.1 matches this body.

**Side effect.** The call writes no audit line. **Verified Fact:** the audit lines captured in this stage's route session have no health action. Replay section 2.1 records the same.

## GET /records/{record_id}

**Input.** `GET /records/{record_id}` with optional header `X-User-Role`. When the header is absent, `main.py` line 11 sets the role to `operator`.

The allow list on line 13 is `admin`, `operator`, `clinician`, `engineer`, `ai_agent`. A role in that list loads a row and writes an audit line (lines 14 to 16). Any other role returns `{"error":"forbidden"}` and writes no audit line (line 17).

`load_record` compares the id to every cell in the row (`domain_service.py` line 12). When no cell matches, it returns the first row (lines 14 to 15). The first row's `device_id` is `REC-0001` (`devices.csv` line 2).

**Output and side effect, this stage.** Every call below returned HTTP 200. **Verified Fact.**

| Input | Output | Side effect |
|---|---|---|
| `/records/REC-0001`, header `operator` | The device row below | Audit line `record.read`, `record_id` `REC-0001`, `role` `operator` |
| `/records/DOES-NOT-EXIST`, header `operator` | The same device row. `device_id` is `REC-0001` | Audit line `record.read`, `record_id` `DOES-NOT-EXIST`, `role` `operator` |
| `/records/REC-0001`, no role header | The same device row | Audit line `record.read`, `role` `operator` |
| `/records/REC-0001`, header `clinician` | The same device row | Audit line `record.read`, `role` `clinician` |
| `/records/REC-0001`, header `admin` | The same device row | Audit line `record.read`, `role` `admin` |
| `/records/REC-0001`, header `engineer` | The same device row | Audit line `record.read`, `role` `engineer` |
| `/records/REC-0001`, header `ai_agent` | The same device row | Audit line `record.read`, `role` `ai_agent` |
| `/records/REC-0001`, header `vendor` | `{"error":"forbidden"}` | No audit line |
| `/records/REC-0001`, header `noc_operator` | `{"error":"forbidden"}` | No audit line |

The device row returned for the allowed calls:

```json
{"device_id":"REC-0001","hostname":"legacy","vendor":"requires_review","device_type":"manual","site_id":"SIT-00001","network_zone":"remote-6","mgmt_ip":"gamma","firmware":"vendor","owner_team":"normal","credential_profile":"vendor","last_seen_at":"2026-05-28T13:24:00","stale_topology_flag":"false"}
```

**Verified Fact.** This stage's TestClient output. Replay sections 2.2, 2.3, 2.4, 2.5, and 2.6 match the operator, missing-id, no-header, clinician, and vendor rows. `admin`, `engineer`, `ai_agent`, and `noc_operator` are added observations from this stage.

Worked example. The caller asks for `DOES-NOT-EXIST`. The response body says `device_id` `REC-0001`. The audit line says `record_id` `DOES-NOT-EXIST`. The body and the log name different devices.

`hostname` is `legacy`. `vendor` is `requires_review`. Those are status words in the hostname and vendor columns. `mgmt_ip` and `credential_profile` are in the body. **Verified Fact:** `devices.csv` line 2 and the JSON above.

`test_missing_id_returns_first_row` and `test_clinician_role_is_accepted_on_record_read` PASSED against this behaviour.

## POST /ai/summarize/{record_id}

**Input.** `POST /ai/summarize/{record_id}`. The function takes `record_id` only (`main.py` lines 19 to 24). It does not read a role header.

The route loads the device row, calls `ai_gateway.summarize_record`, and writes an audit line with `record_id` and model `local-sim-v1`.

The gateway builds the prompt `Summarize this operational record and recommend next action: {record}`, waits 0.01 seconds, and returns a dict (`ai_gateway.py` lines 3 to 17). `guardrail_status` is `not_enforced`.

**Output.** Both calls returned HTTP 200. **Verified Fact.**

| Input | Output |
|---|---|
| `POST /ai/summarize/REC-0001`, no role header | The summary JSON below |
| `POST /ai/summarize/DOES-NOT-EXIST`, no role header | The same summary JSON. The summary text says `REC-0001` |

```json
{"model":"local-sim-v1","summary":"Synthetic summary for REC-0001","recommendation":"Review and approve before action","token_estimate":64,"source_count":1,"guardrail_status":"not_enforced"}
```

**Verified Fact.** This stage's TestClient output. Replay sections 2.7 and 2.8 match. `test_ai_summarize_accepts_request_with_no_role_header` and `test_ai_summary_has_minimum_contract` PASSED.

**Side effect.** Each call appends one `ai.summary` line. The line stores `record_id` and `model`. For `DOES-NOT-EXIST`, the audit `record_id` is `DOES-NOT-EXIST` and the summary text is for `REC-0001`. **Verified Fact:** the captured lines below, and `main.py` line 23.

The gateway waits 0.01 seconds on the path that returns this body. **Verified Fact:** `ai_gateway.py` line 9. This stage did not time the wait.

Captured audit lines from this stage's route session (timestamps are the run clock):

```json
{"ts": "2026-10-10T07:38:35.369571", "action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}
{"ts": "2026-10-10T07:38:35.376058", "action": "record.read", "details": {"record_id": "DOES-NOT-EXIST", "role": "operator"}}
{"ts": "2026-10-10T07:38:35.382621", "action": "record.read", "details": {"record_id": "REC-0001", "role": "operator"}}
{"ts": "2026-10-10T07:38:35.388500", "action": "record.read", "details": {"record_id": "REC-0001", "role": "clinician"}}
{"ts": "2026-10-10T07:38:35.394377", "action": "record.read", "details": {"record_id": "REC-0001", "role": "engineer"}}
{"ts": "2026-10-10T07:38:35.400003", "action": "record.read", "details": {"record_id": "REC-0001", "role": "admin"}}
{"ts": "2026-10-10T07:38:35.406608", "action": "record.read", "details": {"record_id": "REC-0001", "role": "ai_agent"}}
{"ts": "2026-10-10T07:38:35.430012", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
{"ts": "2026-10-10T07:38:35.448048", "action": "ai.summary", "details": {"record_id": "DOES-NOT-EXIST", "model": "local-sim-v1"}}
```

The pytest run just before that session also wrote one `ai.summary` line for `REC-0001` at `2026-10-10T07:38:21.780028`. **Verified Fact:** the log comparison in this stage. `vendor` and `noc_operator` do not appear. `/health` does not appear.

Row shape: `ts`, `action`, `details`. No actor. No correlation id. No approval id. **Verified Fact:** `audit.py` line 9 and the lines above. Replay section 3 shows the same shape.

## etl/run_daily_batch.py --sample

**Input.** Command, from the repo root:

```text
python etl/run_daily_batch.py --sample
```

The script reads `data/synthetic/devices.csv`. For each row it adds 1 to `processed`. When any cell is an empty string it adds 1 to `malformed` and continues (`etl/run_daily_batch.py` lines 8 to 17).

**Output.** Exit code 0.

```text
{'processed': 354, 'malformed': 1, 'sample': True}
```

**Verified Fact.** This stage's command. Replay section 1.5 matches. The one blank row is `devices.csv` line 353, key `DEV-BAD1`. **Verified Fact:** `profile-output.json`, and the characterization test, which set `malformed` equal to the blank-row count.

**Side effect.** The script prints the counts. It does not write a second file of bad rows. `devices.csv` stayed byte-for-byte the same during `test_etl_counts_blank_fields_and_does_not_quarantine`, and the set of file names under `data/` stayed the same. **Verified Fact:** that test PASSED. The source has a `print` and no file write (`etl/run_daily_batch.py` lines 10 to 17).

## legacy/reconcile_legacy.py

**Input.** Command, from the repo root:

```text
python legacy/reconcile_legacy.py
```

The script counts rows in `data/synthetic/devices.csv` (`legacy/reconcile_legacy.py` lines 8 to 14).

The file also assigns `SHARED_DB_USER` and `SHARED_DB_PASSWORD` (lines 5 to 6). The password value is redacted in this note. `test_legacy_script_holds_password_constant` PASSED. It checks that the name is assigned a non-empty string. It does not put the string in the assertion message.

**Output.** Exit code 0.

```text
legacy reconciled 354
```

**Verified Fact.** This stage's command. The stdout is the count. The password value is not in the stdout.

**Side effect.** The script reads the CSV and prints the count. It does not write the CSV. **Verified Fact:** the function body at lines 8 to 14 returns a count, and line 14 prints that count.

## scripts/sanity_check.py

**Input.** Command, from the repo root:

```text
python scripts/sanity_check.py
```

The script checks six required paths, four forbidden workshop paths, the CSV row counts in `data/manifest.json`, and the line count of `events.jsonl` (`scripts/sanity_check.py` lines 4 to 33).

**Output.** Exit code 0.

```text
{'status': 'ok', 'repo': '06-telecom-service-network-incident-ops', 'csv_files': 6, 'events': 3000, 'clean_repo_contract': True}
```

**Verified Fact.** This stage's command. Replay section 1.4 matches. `data/manifest.json` expects 354 rows in each of six CSV files and 3000 events.

**Side effect.** The script prints the dict and exits. It does not write the data files. **Verified Fact:** the source reads files and either prints a failure dict and exits 1, or prints the ok dict (lines 19 to 33). This run took the ok path.

The check counts rows. It does not open `quality_issues.json`. The blank cells and the duplicate keys are still in the CSV files after this command exits 0. **Verified Fact:** `profile-output.json` row counts match the manifest, and the same file records the duplicate keys and the blank rows.

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and `docs/01-discovery/`. It is the before picture for stages S05 to S14. Stage S04 Half A cites `defect-list.md` for what to fix. Stage S03 harvests status words from `data-quality-baseline.md`.
