# Data and integration map

| Field | Value |
|---|---|
| Stage | S01 — Discovery dossier (Execution Plan Phase 1; spine stages 0A, 5, 7) |
| Date / version | 2026-10-09, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The inventory owner column is Unknown on every row. That is more than half the rows. This file cites files and the replay. It proposes no change. |
| Evidence sources | `data/manifest.json`; `data/quality_issues.json`; `data/synthetic/`; `apps/api/services/domain_service.py`; `apps/api/main.py`; `apps/api/services/audit.py`; `apps/web/src/app/api.service.ts`; `infra/terraform/main.tf`; `logs/audit.log`; `docs/00-setup/replay-log.md`; `docs/00-contract/operating-contract.md` |
| Assumptions | Row counts in this file come from a read-only Python read on 2026-10-09. That read did not write the CSV files. `docs/00-contract/operating-contract.md` row 6 says writes under `data/synthetic/` are prohibited. |
| Unresolved issues | Owners of each file are Unknown. Whether `alarm_count` may be larger than the alarm file is Unknown. The money unit of `cost_units` is Unknown (`docs/00-contract/cost-envelope.md`). |
| Residual risks | Secret values from `.env.example` and `legacy/reconcile_legacy.py` are written here as `<redacted>`. |

## What this file is

This file lists the nine data files, the fields the API uses, and five integrations with the direction of each call.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Nine data files

`devices.csv` is the only table the API reads. **Verified Fact:** `apps/api/services/domain_service.py` line 5, `PRIMARY = "devices.csv"`. `load_record` and `list_recent` both open that file. No route calls `list_recent`.

| File | Rows | What it holds | Who reads it | Who writes it in this repo |
|---|---|---|---|---|
| `data/synthetic/devices.csv` | 354 | Device rows. Columns: `device_id`, `hostname`, `vendor`, `device_type`, `site_id`, `network_zone`, `mgmt_ip`, `firmware`, `owner_team`, `credential_profile`, `last_seen_at`, `stale_topology_flag`. | The API (`domain_service.py`), `etl/run_daily_batch.py`, `legacy/reconcile_legacy.py`, and `scripts/sanity_check.py` (count only). | No writer in the repo. The file is already on disk. |
| `data/synthetic/circuits.csv` | 354 | Circuit rows. Columns: `circuit_id`, `customer_id`, `a_end`, `z_end`, `bandwidth_mbps`, `service_class`, `status`, `provisioned_at`, `sla_tier`, `orphan_flag`. | `scripts/sanity_check.py` counts rows. | No writer in the repo. |
| `data/synthetic/alarms.csv` | 354 | Alarm rows. Columns: `alarm_id`, `device_id`, `interface`, `severity`, `alarm_type`, `first_seen_at`, `last_seen_at`, `dedupe_key`, `maintenance_window`, `storm_batch_id`. | `scripts/sanity_check.py` counts rows. | No writer in the repo. |
| `data/synthetic/incidents.csv` | 354 | Incident rows. Columns: `incident_id`, `customer_id`, `circuit_id`, `severity`, `status`, `opened_at`, `root_cause`, `automation_used`, `sla_breach_risk`. | `scripts/sanity_check.py` counts rows. | No writer in the repo. |
| `data/synthetic/service_orders.csv` | 354 | Order rows. Columns: `order_id`, `customer_id`, `service_type`, `requested_bandwidth`, `qualification_status`, `provisioning_status`, `retry_count`, `rollback_status`. | `scripts/sanity_check.py` counts rows. | No writer in the repo. |
| `data/synthetic/ai_invocations.csv` | 354 | Stored AI-call rows. Columns listed in the AI note. | `scripts/sanity_check.py` counts rows. | The live gateway does not write it. **Verified Fact:** `ai_gateway.py` returns a dict and opens no CSV. |
| `data/synthetic/events.jsonl` | 3000 | One JSON object per line. Fields: `event_id`, `business_entity`, `event_type`, `severity`, `correlation_id`, `actor`, `latency_ms`, `cost_units`, `payload_hash`. | `scripts/sanity_check.py` counts lines. | No writer in the repo. |
| `data/manifest.json` | one object | Expected counts: 354 per CSV and 3000 events. Also repeats four defect labels per table. | `scripts/sanity_check.py`. | No writer in the repo. |
| `data/quality_issues.json` | one object | The same four defect labels per table, plus two notes that the data is synthetic. | No Python file opens this path. **Verified Fact:** repo search. | No writer in the repo. |

The 354 and 3000 figures match `data/manifest.json` and replay section 1.4. **Verified Fact.**

## Fields the API uses

`load_record` returns the whole matching row, or the first row (`domain_service.py` lines 11 to 15). Replay section 2.2 shows every column of the first device row in the HTTP body:

`device_id`, `hostname`, `vendor`, `device_type`, `site_id`, `network_zone`, `mgmt_ip`, `firmware`, `owner_team`, `credential_profile`, `last_seen_at`, `stale_topology_flag`.

The match is `record_id in row.values()` (line 12). The id is compared to every cell, not only to `device_id`.

The first data row is `REC-0001` with `hostname` `legacy` and `vendor` `requires_review` (`devices.csv` line 2). Replay section 2.2 returned that row. Those two cells hold status words in the hostname and vendor columns.

`list_recent` would return the first 20 rows of the same file (`domain_service.py` lines 17 to 19). Nothing calls it.

## First key reused across six tables

**Verified Fact.** The first data row of each CSV uses `REC-0001` as its first column:

| File | First column | First value |
|---|---|---|
| `devices.csv` | `device_id` | `REC-0001` |
| `circuits.csv` | `circuit_id` | `REC-0001` |
| `alarms.csv` | `alarm_id` | `REC-0001` |
| `incidents.csv` | `incident_id` | `REC-0001` |
| `service_orders.csv` | `order_id` | `REC-0001` |
| `ai_invocations.csv` | `ai_call_id` | `REC-0001` |

Inside `devices.csv`, `REC-0001` appears once. The same string is the first key of the other five files. The API reads only the device file, so an API call for `REC-0001` returns the device row. It does not return the circuit, alarm, incident, order, or AI-call row that uses the same text.

## Counts taken in this stage

These are **Verified Fact** from a read-only count. They sit here so S02 can snapshot them. This note does not set a cutoff.

| Item | Count |
|---|---|
| Duplicate first-column keys in each CSV | 3 extra rows. Device ids `DEV-00004`, `DEV-00013`, `DEV-00019`. The other files repeat the same pattern: `CIR-`, `ALA-`, `INC-`, `ORD-`, and `AI_-` with `00004`, `00013`, and `00019`. |
| Blank device row | 1. `devices.csv` line 353, `device_id` `DEV-BAD1`, other cells empty. Replay section 1.5 `malformed` 1 matches this shape. |
| `stale_topology_flag` | `true` 192, `false` 161, blank 1 |
| `orphan_flag` on circuits | `true` 186, `false` 167, blank 1 |
| Alarms with `last_seen_at` before `first_seen_at` | 166 |
| Storm ids that appear twice | 3 (`STO-00005`, `STO-00013`, `STO-00019`). 351 distinct `storm_batch_id` values. |
| `events.jsonl` `correlation_id` | null 982, empty string 1010, filled 1008 |
| `ai_invocations.csv` `model` equal to `local-sim-v1` | 0 |
| `ai_call_id` values that start with `AI_-` | 353. Line 2 is `AI_-00002`. The first id is `REC-0001`. |

One impossible timestamp example: `devices.csv` line 354, `device_id` `DEV-00013`, `last_seen_at` `1900-01-01T00:00:00`. `data/quality_issues.json` lists "impossible timestamp" for devices. This stage did not count every such cell.

`ai_invocations.csv` row `AI_-00019` has `recommendation_risk` `1.42`. Other values in that column are words. `data/quality_issues.json` lists "out-of-range score or risk marker" for that table.

## Five integrations

| Integration | From | To | Direction | Evidence |
|---|---|---|---|---|
| UI fetch wrapper to API | `apps/web/src/app/api.service.ts` | paths `/api/records/{id}` and `/api/ai/summarize/{id}` | The web file calls those URLs. The live routes are `/records/{record_id}` and `/ai/summarize/{record_id}` with no `/api` prefix (`main.py`). | Verified Fact: `api.service.ts` lines 2 to 4; `main.py` lines 6, 10, and 19. `docs/00-contract/operating-contract.md` row 5: `apps/web` does not open in a browser today. |
| API to CSV | `domain_service.load_record` | `data/synthetic/devices.csv` | The API reads the file. The API does not write it. | Verified Fact: `domain_service.py` lines 4 to 15. Replay section 2.2. |
| API to AI stub | `main.ai_summary` | `ai_gateway.summarize_record` | The route calls the function in the same process. The function does not call a network model. | Verified Fact: `main.py` lines 21 to 22; `ai_gateway.py` lines 6 to 18. Replay section 2.7. |
| Audit to `logs/audit.log` | `audit.write_event` | `logs/audit.log` | The API appends a line. | Verified Fact: `audit.py` lines 5 to 12. Replay section 3. The file now has 13 lines. The replay quotes 7. Lines 8 to 13 are later `record.read` and `ai.summary` rows. Who ran those calls is Unknown. |
| Terraform to a text file | `infra/terraform/main.tf` | `generated-env.txt` | The file declares a write. Content is the line `shared_user=app_shared`. | Verified Fact: `main.tf` lines 2 to 4. `generated-env.txt` is not in the repo tree. Whether the declaration was ever applied is Unknown. |

`policy/opa/access.rego` is a rule file on disk. It is not one of the five running integrations. No Python file imports it. **Verified Fact.**

## Secrets on the data path

The database password and the example AI key are `<redacted>`. They appear in `legacy/reconcile_legacy.py` lines 5 to 6 and in `.env.example` lines 1 to 4. `docs/00-contract/operating-contract.md` row 6 and the stop list forbid copying those values into a new file.

`mgmt_ip` and `credential_profile` are on the device row the API returns. Replay section 2.2. The operating contract records that fact and does not design a field list in this stage.

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and `docs/00-contract/operating-contract.md`. Stage S02 cites this dossier for behaviours to snapshot, including the counts above. Stage S03 harvests entities and status words from these columns. Stage S09 reuses the risk register.
