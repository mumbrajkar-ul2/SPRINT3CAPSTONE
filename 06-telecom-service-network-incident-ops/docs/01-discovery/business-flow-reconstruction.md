# Business flow reconstruction

| Field | Value |
|---|---|
| Stage | S01 — Discovery dossier (Execution Plan Phase 1; spine stages 0A, 5, 7) |
| Date / version | 2026-10-09, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The inventory owner column is Unknown on every row. That is more than half the rows. This file cites files and the replay. It proposes no change. |
| Evidence sources | `docs/domain-specific-spec.md`; `apps/api/main.py`; `data/synthetic/events.jsonl`; `data/synthetic/*.csv`; `docs/00-setup/replay-log.md`; `docs/00-contract/operating-contract.md`; `docs/runbooks/incident-response.md` |
| Assumptions | The four names in the domain card are the four flows. The card does not list steps. Steps below are reconstructed from column names and from routes that exist. Each step is labelled. |
| Unresolved issues | The repo does not define the step order. The repo does not define how many alarms make a storm. The repo does not define a ticket as a named object. |
| Residual risks | A step list can be read as a design. It is a reading of columns and of missing routes. |

## What this file is

`docs/domain-specific-spec.md` lines 12 to 16 names four flows. This note reconstructs each one. For each flow it lists steps, the data the step needs, the routes that exist today, and the steps with no code.

The live API exposes three routes (`apps/api/main.py`; replay section 2.9): `GET /health`, `GET /records/{record_id}`, and `POST /ai/summarize/{record_id}`. Health is a process check. It is not one of the four flows.

**Verified Fact.** `events.jsonl` has 3000 lines. Counted in this stage: Customer order to provisioning 741, Alarm storm to incident correlation 706, Topology lookup to AI recommendation 782, Approved remediation to validation 771. `scripts/sanity_check.py` counts those lines. No other Python file opens `events.jsonl`. The event file records the flow name. It does not run the flow.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Flow 1 — Customer order to provisioning

**Runs end to end today: No.**

No route reads `service_orders.csv` or `circuits.csv`. **Verified Fact:** `domain_service.py` line 5 sets `PRIMARY = "devices.csv"`. A search of `*.py` finds no `service_orders.csv` or `circuits.csv` filename.

| Step | Data it needs | Route that exists today | Code |
|---|---|---|---|
| An order row is on disk | `service_orders.csv` columns `order_id`, `customer_id`, `service_type`, `requested_bandwidth` | None | File only. **Verified Fact:** header row. **Inference:** this is the start of the named flow. |
| Qualification is recorded | `qualification_status` | None | No code reads the column. **Verified Fact:** column exists. Values counted in this stage include `approved`, `manual_hold`, `queued`, `exception`, `in_progress`, `failed`, `closed`, `new`, and one blank. |
| Provisioning is recorded | `provisioning_status` | None | No code reads the column. **Verified Fact:** column exists. |
| A retry count is stored | `retry_count` | None | No code reads the column. **Verified Fact:** counted in this stage, max `4995` on a numeric cell, 294 rows at or above 1000. The domain card does not define a retry limit. |
| A rollback word is stored | `rollback_status` | None | No code reads the column. **Verified Fact:** column exists. |
| A circuit row is on disk | `circuits.csv` columns `circuit_id`, `customer_id`, `bandwidth_mbps`, `status`, `provisioned_at`, `sla_tier`, `orphan_flag` | None | File only. **Verified Fact:** header and 354 rows. |

Steps with no code: qualification, provisioning, retry, rollback, and any write of a circuit. The order file and the circuit file are present. Nothing in `apps/api/main.py` moves an order from one status word to another.

`docs/00-contract/operating-contract.md` row 2 says a later stage does not add a route for qualify, provision, retry, or rollback. That row is a contract rule. It matches the absence in `main.py`. This note does not add those routes.

## Flow 2 — Alarm storm to incident correlation

**Runs end to end today: No.**

No route reads `alarms.csv` or `incidents.csv`. **Verified Fact:** those filenames are absent from `*.py`.

| Step | Data it needs | Route that exists today | Code |
|---|---|---|---|
| Alarm rows are on disk | `alarms.csv` columns `alarm_id`, `device_id`, `severity`, `alarm_type`, `first_seen_at`, `last_seen_at`, `dedupe_key`, `maintenance_window`, `storm_batch_id` | None | File only. **Verified Fact:** header and 354 rows. |
| Alarms share a storm id | `storm_batch_id` | None | No code groups the column. **Verified Fact:** counted in this stage, 351 distinct values, 3 values appear twice (`STO-00005`, `STO-00013`, `STO-00019`), 1 blank. The repo does not say how many alarms make a storm. |
| Alarms share a dedupe key | `dedupe_key` | None | No code collapses duplicates. **Verified Fact:** 3 keys appear twice. |
| An incident row is on disk | `incidents.csv` columns `incident_id`, `customer_id`, `circuit_id`, `severity`, `status`, `opened_at`, `root_cause`, `automation_used`, `sla_breach_risk` | None | File only. **Verified Fact:** header and 354 rows. |
| An alarm is tied to an incident | a shared id between the two files | None | No code joins the files. **Unknown:** which columns are the join. `alarms.device_id` and `incidents.circuit_id` are different names. |

Steps with no code: group a storm, collapse a dedupe key, open an incident, link an alarm to an incident.

**Verified Fact from the alarm file, counted in this stage.** 166 rows have `last_seen_at` earlier than `first_seen_at` when both cells are filled. One row is blank. The API never sees these rows.

## Flow 3 — Topology lookup to AI recommendation

**Runs end to end today: No.**

Two routes cover a lookup and a local summary. The rest of the flow has no code. The summary of a missing id is a summary of the first device row (replay section 2.8). That is a different device from the id in the request.

| Step | Data it needs | Route that exists today | Code |
|---|---|---|---|
| Look up a device row | `devices.csv`, including `stale_topology_flag`, `mgmt_ip`, `credential_profile` | `GET /records/{record_id}` | **Verified Fact:** `main.py` lines 10 to 16. Replay section 2.2 returned the `REC-0001` row. |
| A missing id is rejected | the requested id | The same route | The route returns the first row. **Verified Fact:** `domain_service.py` lines 14 to 15. Replay section 2.3. |
| The stale flag changes the answer | `stale_topology_flag` | None | The flag is inside the returned row. No branch reads it. **Verified Fact:** `ai_gateway.py` does not mention the flag. Counted in this stage: `true` 192, `false` 161, blank 1. |
| A summary is produced | the device dict | `POST /ai/summarize/{record_id}` | **Verified Fact:** `main.py` lines 19 to 24. `ai_gateway.py` lines 6 to 18. Replay section 2.7. The route checks no role. |
| One of the three named products runs | names in `current-state.md` lines 11 to 13 | None | No function uses those names. **Verified Fact.** |
| A call row is stored | `ai_invocations.csv` | None | The gateway does not write the file. **Verified Fact:** `ai_gateway.py` has no file write. |
| A person approves the text | an approval id | None | Replay section 2.7: the audit line stores `record_id` and `model` only. `docs/00-contract/operating-contract.md` row 9 says no route writes an approval id today. |

Steps with no code: a decision on the stale flag, any of the three named products, a write to `ai_invocations.csv`, a role check on the summary route, and a stored approval id.

`GET /records/{record_id}` and `POST /ai/summarize/{record_id}` exist. They do not carry this flow from a topology lookup through a governed next action to a stored human approval.

## Flow 4 — Approved remediation to validation

**Runs end to end today: No.**

| Step | Data it needs | Route that exists today | Code |
|---|---|---|---|
| A human approval is stored | an approval id on an audit line or a call row | None | **Verified Fact:** `audit.py` lines 8 to 9 store `ts`, `action`, and `details`. Replay section 3. `ai_invocations.csv` has `approval_required`. The gateway does not write that file. |
| A change is applied on a device | a device config or a command channel | None | **Verified Fact:** `main.py` has no route that pushes a config. `Project_Intent.md` section 3.1 row 3 says the current code does not push to a device. `docs/00-contract/operating-contract.md` row 9 says the same action is prohibited until a stored approval id exists. |
| The change is checked | a validation result | None | **Verified Fact:** `docs/runbooks/incident-response.md` says rollback, degraded mode, and evidence capture are missing from the runbook. No test in `tests/` checks a remediation result. |
| The incident records that automation ran | `incidents.automation_used` | None | File only. **Verified Fact:** counted in this stage, `false` 187, `true` 166, blank 1. No code reads the column. |

Steps with no code: store an approval, apply a remediation, validate the result, and update `automation_used`.

The summarize body contains the sentence "Review and approve before action" (`ai_gateway.py` line 14). Replay section 2.7 returned that sentence with `guardrail_status` `not_enforced`. The audit line for that call has no approval id. The sentence is text in a JSON body. No route records an approval after it.

## Routes that exist, by flow

| Flow | Routes that exist today | Steps with no code |
|---|---|---|
| Customer order to provisioning | None | Qualification, provisioning, retry, rollback, circuit write |
| Alarm storm to incident correlation | None | Group storm, collapse dedupe key, open or link an incident |
| Topology lookup to AI recommendation | `GET /records/{record_id}`, `POST /ai/summarize/{record_id}` | Stale-flag branch, three named products, write `ai_invocations.csv`, role check on summarize, stored approval id |
| Approved remediation to validation | None | Stored approval, device change, validation, update `automation_used` |

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and `docs/00-contract/operating-contract.md`. Stage S02 cites this dossier for behaviours to snapshot. Stage S03 harvests entities and status words from these flows. Stage S09 reuses the risk register.
