# Data-quality baseline

| Field | Value |
|---|---|
| Stage | S02 — Behavioural baseline (Execution Plan Phase 2; spine stage 7) |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The profile ran. Five labels in `data/quality_issues.json` are marked Not found. The other 19 labels are marked Confirmed. |
| Evidence sources | `python docs/02-baseline/profile_data.py` on 2026-10-10; `docs/02-baseline/profile-output.json`; `data/manifest.json`; `data/quality_issues.json`; `data/synthetic/`; `docs/00-setup/replay-log.md`; `docs/01-discovery/data-and-integration-map.md` |
| Assumptions | A blank cell is the seeded "blank mandatory fields" item. The repo does not name which columns are mandatory. A timestamp whose year is 1900 is impossible in these files because the other parsed values in that column are year 2026. |
| Unresolved issues | The owner of the retry bound is Unknown. The owner of the `sla_breach_risk` range is Unknown. `service_orders.csv` and `ai_invocations.csv` have no date-time column. `devices.csv`, `circuits.csv`, and `alarms.csv` have no score column that this profile flagged. |
| Residual risks | A later reader can treat the PROPOSED bounds as an approved rule. They are not approved. Owner: Team-Force. |

## What this file is

This file records the shape of the synthetic data before any fix. The counts below are **REAL**. They come from one run of `docs/02-baseline/profile_data.py`. That run wrote `docs/02-baseline/profile-output.json`. The script reads the files. It does not change files under `data/`.

Command, from `06-telecom-service-network-incident-ops`:

```text
python docs/02-baseline/profile_data.py
```

Exit code 0. The script printed `quality_issues Confirmed 19 Not found 5`. **Verified Fact.**

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

`docs/01-discovery/data-and-integration-map.md` already counted 166 alarms with last-before-first, 353 ids starting with `AI_-`, and event correlation counts of 982 null, 1010 blank, and 1008 filled. This run produced the same counts. **Verified Fact:** both files.

## Per file

`data/manifest.json` expects 354 data rows in each CSV and 3000 lines in `events.jsonl`. Every file matched. **Verified Fact. REAL.**

| File | Rows | Manifest | Match | Key column | Distinct keys | Duplicate keys (each appears twice) | Blank row |
|---|---|---|---|---|---|---|---|
| `devices.csv` | 354 | 354 | yes | `device_id` | 351 | `DEV-00004`, `DEV-00013`, `DEV-00019` | line 353, `DEV-BAD1` |
| `circuits.csv` | 354 | 354 | yes | `circuit_id` | 351 | `CIR-00004`, `CIR-00013`, `CIR-00019` | line 353, `CIR-BAD1` |
| `alarms.csv` | 354 | 354 | yes | `alarm_id` | 351 | `ALA-00004`, `ALA-00013`, `ALA-00019` | line 353, `ALA-BAD1` |
| `incidents.csv` | 354 | 354 | yes | `incident_id` | 351 | `INC-00004`, `INC-00013`, `INC-00019` | line 353, `INC-BAD1` |
| `service_orders.csv` | 354 | 354 | yes | `order_id` | 351 | `ORD-00004`, `ORD-00013`, `ORD-00019` | line 353, `SER-BAD1` |
| `ai_invocations.csv` | 354 | 354 | yes | `ai_call_id` | 351 | `AI_-00004`, `AI_-00013`, `AI_-00019` | line 353, `AI_-BAD1` |
| `events.jsonl` | 3000 | 3000 | yes | `event_id` on each JSON line |  |  |  |

Line numbers count the header as line 1. The first data row is line 2. **Verified Fact:** `profile_data.py` uses `enumerate(..., start=2)`.

Worked example for a duplicate. `devices.csv` key `DEV-00004` is on lines 5 and 352. Those two rows differ in hostname, vendor, device type, site, management address, owner team, credential profile, last seen, and the stale-topology flag. `DEV-00019` is on lines 20 and 355, and those two rows are identical. The same line pattern (5 with 352, 14 with 354, 20 with 355) is in every CSV. **Verified Fact. REAL.** `profile-output.json` key `duplicate_pairs`.

### Blanks per column

On every CSV, the key column has **0** blank cells. Every other column has **1** blank cell. All of those blank cells sit on the line 353 row named above. The key on that row is filled. **Verified Fact. REAL.**

| File | Columns with 1 blank cell |
|---|---|
| `devices.csv` | `hostname`, `vendor`, `device_type`, `site_id`, `network_zone`, `mgmt_ip`, `firmware`, `owner_team`, `credential_profile`, `last_seen_at`, `stale_topology_flag` |
| `circuits.csv` | `customer_id`, `a_end`, `z_end`, `bandwidth_mbps`, `service_class`, `status`, `provisioned_at`, `sla_tier`, `orphan_flag` |
| `alarms.csv` | `device_id`, `interface`, `severity`, `alarm_type`, `first_seen_at`, `last_seen_at`, `dedupe_key`, `maintenance_window`, `storm_batch_id` |
| `incidents.csv` | `customer_id`, `circuit_id`, `severity`, `status`, `opened_at`, `root_cause`, `automation_used`, `sla_breach_risk` |
| `service_orders.csv` | `customer_id`, `service_type`, `requested_bandwidth`, `qualification_status`, `provisioning_status`, `retry_count`, `rollback_status` |
| `ai_invocations.csv` | `incident_id`, `use_case`, `model`, `topology_snapshot_id`, `alarm_count`, `token_count`, `recommendation_risk`, `approval_required`, `guardrail_status` |

`device_id` has 0 blanks. The key cell `DEV-BAD1` is filled, and the other 11 cells on that row are empty. The ETL `malformed` count of 1 matches this one device row. **Verified Fact:** replay section 1.5 and this profile.

## Alarms where last seen is before first seen

**166** alarms have `last_seen_at` before `first_seen_at`. **Verified Fact. REAL.**

Worked example. `ALA-00002` is file line 3. `first_seen_at` is `2026-07-31T23:45:00`. `last_seen_at` is `2026-02-23T09:35:00`. Last seen is the earlier time. Appendix D in `Project_Intent.md` names this alarm. Two more examples from the same run: `ALA-00003` line 4, and `ALA-00008` line 9.

## Timestamps whose year is 1900

The script flags a parsed timestamp whose year is not 2026. In these files that year is 1900. The other parsed values in the same column are year 2026. **Verified Fact. REAL.**

| File | Column | Year 1900 | Year 2026 | The 1900 row |
|---|---|---|---|---|
| `devices.csv` | `last_seen_at` | 1 | 352 | line 354, `DEV-00013`, `1900-01-01T00:00:00` |
| `circuits.csv` | `provisioned_at` | 1 | 352 | line 354, `CIR-00013`, `1900-01-01T00:00:00` |
| `alarms.csv` | `first_seen_at` | 1 | 352 | line 354, `ALA-00013`, `1900-01-01T00:00:00` |
| `alarms.csv` | `last_seen_at` | 0 | 353 | none |
| `incidents.csv` | `opened_at` | 1 | 352 | line 354, `INC-00013`, `1900-01-01T00:00:00` |

`service_orders.csv` has no column whose values are all date-times. `ai_invocations.csv` has no such column. **Verified Fact. REAL.** `timestamp_columns` is an empty list for both files.

## service_orders.retry_count

**PROPOSED bound: `retry_count` >= 1000. Owner: Team-Force.**

The repo states no legal maximum. `Project_Intent.md` section 4.3 names values in the thousands as the known odd case. This baseline uses 1000 so that case is counted. The bound is not an approved business rule.

| Item | Count |
|---|---|
| Numeric `retry_count` values | 353 |
| Blank | 1 (line 353, `SER-BAD1`) |
| Non-numeric | 0 |
| Minimum | 32 |
| Maximum | 4995 |
| At or above 1000 | 294 |
| Below 1000 | 59 |

**Verified Fact. REAL.**

Worked example. The smallest value under the bound is 32, order `ORD-00072`, file line 73. The next small values in the profile examples are 54, 58, 68, and 121. The confirmed defect under this bound is the 294 values at or above 1000. A later owner can set a different maximum.

## Distinct severity in incidents.csv

**Verified Fact. REAL.** `gold` and `bronze` are both present.

| Severity | Rows |
|---|---|
| `silver` | 65 |
| `high` | 57 |
| `low` | 54 |
| `bronze` | 50 |
| `medium` | 47 |
| `gold` | 41 |
| `critical` | 39 |
| blank | 1 |

The distinct values are blank, `bronze`, `critical`, `gold`, `high`, `low`, `medium`, and `silver`.

`alarms.csv` `severity` uses the same words. **Verified Fact. REAL.** `gold` 48, `bronze` 52, `silver` 57, `medium` 53, `low` 50, `high` 48, `critical` 45, blank 1.

Worked example. `incidents.csv` line 3 is `INC-00002` with `severity` `gold`. Appendix D names that row. A count grouped by severity will place `gold` next to `high` and `critical`. This file does not set an allowed list. The repo does not state one.

## Malformed ai_call_id

Rule used by the script: a value is malformed when it starts with `AI_-`. That is the shape `Project_Intent.md` section 4.3 names (`AI_-00002`).

| Item | Count |
|---|---|
| Starts with `AI_-` | 353 |
| Includes `AI_-00002` | yes (line 3) |
| Includes `AI_-BAD1` | yes (line 353, the blank row) |
| Other id | 1: line 2, `REC-0001` |
| Starts with `AI-` and not `AI_-` | 0 |

**Verified Fact. REAL.**

## events.jsonl correlation_id

The file has **3000** JSON lines. **0** lines failed to parse. **Verified Fact. REAL.** The line count matches `manifest.json` key `jsonl_events`.

| `correlation_id` | Rows |
|---|---|
| JSON `null` | 982 |
| Empty string | 1010 |
| Null or blank, combined | 1992 |
| Filled | 1008 |

**Verified Fact. REAL.** 982 + 1010 + 1008 = 3000.

## quality_issues.json

`data/quality_issues.json` lists the same four labels on six entities. That is 24 items. The script marked each one Confirmed or Not found.

| Entity | Item | Mark |
|---|---|---|
| devices | duplicate business key | Confirmed |
| devices | blank mandatory fields | Confirmed |
| devices | impossible timestamp | Confirmed |
| devices | out-of-range score or risk marker | Not found |
| circuits | duplicate business key | Confirmed |
| circuits | blank mandatory fields | Confirmed |
| circuits | impossible timestamp | Confirmed |
| circuits | out-of-range score or risk marker | Not found |
| alarms | duplicate business key | Confirmed |
| alarms | blank mandatory fields | Confirmed |
| alarms | impossible timestamp | Confirmed |
| alarms | out-of-range score or risk marker | Not found |
| incidents | duplicate business key | Confirmed |
| incidents | blank mandatory fields | Confirmed |
| incidents | impossible timestamp | Confirmed |
| incidents | out-of-range score or risk marker | Confirmed |
| service_orders | duplicate business key | Confirmed |
| service_orders | blank mandatory fields | Confirmed |
| service_orders | impossible timestamp | Not found |
| service_orders | out-of-range score or risk marker | Confirmed |
| ai_invocations | duplicate business key | Confirmed |
| ai_invocations | blank mandatory fields | Confirmed |
| ai_invocations | impossible timestamp | Not found |
| ai_invocations | out-of-range score or risk marker | Confirmed |

**19 Confirmed. 5 Not found.** **Verified Fact. REAL.**

Why each Not found mark is Not found:

- **devices, circuits, and alarms / out-of-range score or risk marker.** Those files have no `sla_breach_risk`, `retry_count`, or `recommendation_risk` column. This profile did not apply a numeric cutoff to bandwidth, alarm counts, or status words. **Verified Fact:** the column lists in `profile-output.json`.
- **service_orders / impossible timestamp.** The file has no date-time column. **Verified Fact. REAL.**
- **ai_invocations / impossible timestamp.** The file has no date-time column. **Verified Fact. REAL.**

Why the Confirmed score marks are Confirmed:

- **incidents.** **PROPOSED range: `sla_breach_risk` from 0 to 1 inclusive. Owner: Team-Force.** 352 numeric values sit in that range. 1 value is outside it: file line 355, `INC-00019`, `sla_breach_risk` `1.42`. 1 cell is blank. **Verified Fact. REAL.**
- **service_orders.** 294 values of `retry_count` are at or above the PROPOSED bound of 1000. Owner: Team-Force. See the retry section above.
- **ai_invocations.** `recommendation_risk` is a word on the other rows. One cell is numeric: file line 355, `AI_-00019`, `recommendation_risk` `1.42`. **Verified Fact. REAL.** The word counts are in `profile-output.json` under `ai_recommendation_risk.word_counts`. One of those words is `high_risk` (28 rows). That word is a label in the column. The Confirmed mark is the numeric cell `1.42`.

**Assumption:** the blank cells on the `*BAD1` rows are the seeded "blank mandatory fields" item. The phrase in `quality_issues.json` does not list the columns.

## Status words

Stage S03 harvests the words in this section.

Marks used above, and only these two marks: **Confirmed**, **Not found**.

Severity words observed in `incidents.csv`, with REAL row counts: `silver` 65, `high` 57, `low` 54, `bronze` 50, `medium` 47, `gold` 41, `critical` 39, and one blank.

Severity words observed in `alarms.csv`, with REAL row counts: `silver` 57, `medium` 53, `bronze` 52, `low` 50, `high` 48, `gold` 48, `critical` 45, and one blank.

`gold` and `bronze` are in both severity columns.

The first device row stores status words in other columns: `hostname` `legacy`, `vendor` `requires_review`. **Verified Fact:** `devices.csv` line 2, and the `GET /records/REC-0001` body in `behaviour-snapshot.md`.

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and `docs/01-discovery/data-and-integration-map.md`. Stage S03 harvests the status words in the section above. Stage S04 Half A cites `defect-list.md` for what to fix. The PROPOSED bounds stay proposals until an owner is named.
