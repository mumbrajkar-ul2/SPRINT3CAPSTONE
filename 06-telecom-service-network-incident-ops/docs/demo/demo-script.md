# Demo script: one alarm storm to one human decision

| Field | Value |
|---|---|
| Stage | S07. Application and demo. This file is the step-by-step script for one case. |
| Date / version | 2026-10-13, v1.1. Semantic layer 1.2.1. PRD v1.9. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Written from a real run on 2026-10-13. Every value in the "You will see" column came from that run (see `docs/demo/evidence.md`, section 4). |
| Evidence sources | `docs/prd/prd.md` (RQ-08 to RQ-30, RQ-32 to RQ-34, RQ-42, RQ-48, RQ-62 to RQ-65). `apps/api/main.py`. `apps/api/static/index.html`. `data/synthetic/alarms.csv` and `devices.csv`. `docs/demo/evidence.md`. |
| Assumptions | (1) The model is the stub `local-sim-v1`, so every summary and recommendation sentence is SIMULATED. (2) The role is a word that the page sends in the `X-User-Role` header. Nothing proves who the caller is, so this script calls it a claimed role. (3) The rows in `alarms.csv` and `devices.csv` are synthetic. |
| Unresolved issues | The PRD gaps in `docs/demo/evidence.md`, section 7, have no owner answer yet. None of them changes a step in this script. |
| Residual risks | The recommendation sentence is fixed text from the stub. A real model would give other text, and the lists of command phrases would meet phrases they do not hold. Timing values come from the stub, so they say nothing about a real model. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Number labels on this page and in this script: **REAL** (the app counted or measured it in this run), **PRECOMPUTED** (copied from a stored report), **SIMULATED** (made by the stub), **EDUCATIONAL** (a rule of thumb, not a bill). This script uses no PRECOMPUTED number.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Start the app

Run these commands from the project folder in PowerShell.

```powershell
$env:POLICY_ENGINE = "python"
.\.venv\Scripts\python.exe -m uvicorn apps.api.main:app --port 8000
```

Open `http://127.0.0.1:8000/`. The page is one HTML file (`apps/api/static/index.html`). It calls the routes of the same app.

The run writes two files. `logs/audit.log` gets one line for each call. `logs/approvals.jsonl` gets one line for each stored decision. Both files only grow. Neither file holds a password, a prompt text or a management address.

**Verified Fact.** `POLICY_ENGINE=python` runs the Python copy of the policy. Without it, the app uses the `opa` program when it is on the path. The two copies give the same answers (`policy/tests/test_policy_python.py`, which skips on a machine with no `opa`).

## 2. The case

| Item | Value |
|---|---|
| The event | Alarm storm `STO-00002`. It has one alarm row, `ALA-00002`, for device `DEV-00002`. The row has a flag, `last_seen_before_first_seen`, because its last seen time is before its first seen time. |
| The question | Should a person act on the next-action sentence for device `DEV-00002`? |
| Who asks | A NOC operator. The page sends the word `operator` as the claimed role. |
| Who reads the audit chain | An admin. The page sends the word `admin` as the claimed role for step 5 only. |
| One case id | The page makes one `X-Correlation-Id` when it loads and sends it with every call. The button "Start a new case" makes another. |

## 3. The steps

Click the buttons in order. Each row says what the page does, what you will see, which data the step uses, and which audit row the step writes.

| Step | What you do | You will see | Data used (fields) | Policy result | Audit row written |
|---|---|---|---|---|---|
| 1 | Keep `STO-00002` in the box. Click **Read storm**. | HTTP status 200 (REAL). Raw count 1 (REAL). Deduped count 1 (REAL). Flagged count 1 (REAL). Alarm ids listed 1 (REAL). One row: `ALA-00002`, device `DEV-00002`, key `DED-00002`, flag `last_seen_before_first_seen`. | `alarms.csv`: `storm_batch_id`, `alarm_id`, `device_id`, `dedupe_key`, `first_seen_at`, `last_seen_at`. | The role `operator` has an allow row for reading alarms (TA-02). | `record.storm_read`, resource `resource.alarm`. |
| 2 | The list under "Device id from the storm" holds `DEV-00002`. Click **Look up device**. | HTTP status 200 (REAL). The device row: `device_id`, `hostname`, `vendor`, `device_type`, `site_id`, `network_zone`, `firmware`, `owner_team`, `last_seen_at`, `stale_topology_flag` (value `false`). The page says `mgmt_ip` and `credential_profile` are left out for this role. | `devices.csv`, matched on `device_id` only. | The role `operator` has an allow row for reading a device. The same role has no row for the two sensitive fields (TA-15 belongs to `engineer`). | `record.read`, `record_id` `DEV-00002`. |
| 3 | Click **Ask for a recommendation**. | HTTP status 202 (REAL). Outcome `HOLD_FOR_REVIEW`. The sentence "Review and approve before action" (SIMULATED). The summary "Synthetic summary for DEV-00002" (SIMULATED). Policy reason `ai_use.next_action_recommendation`. Model `local-sim-v1`, version `local-sim-v1`. Tokens 90 (EDUCATIONAL). Latency about 10 to 25 ms (SIMULATED). The page says a person must accept or reject the sentence. | The ten allow-listed fields of the device row go into the prompt (the same ten the page shows in step 2). `mgmt_ip` and `credential_profile` stay out. The prompt hash identifies the prompt. The audit row does not hold the prompt text. | The policy answers `HOLD_FOR_REVIEW` for every healthy recommendation (policy row O2). The model never decides the outcome. | `ai.recommendation`, with the five model values and `token_estimate_method` `word_count_x2_EDUCATIONAL`. |
| 4 | Click **Approve (yes)**. | HTTP status 200 (REAL). Decision `yes`. Approver `persona.noc_operator` (claimed role, set by the server). An approval id that starts with `APR-`. Device id `DEV-00002`. The page says no device, circuit, incident or alarm was changed. | The device id from the list, the case id, and the word `yes`. The page sends no approver and no approval id. | Only the role `operator` may store a decision (TA-09). The route found an `ai.recommendation` row with text under this case id and this device id. | `ai.approval`, resource `resource.ai_invocation`, with the approval id. The row is written first. The approval is stored after it in `logs/approvals.jsonl`. |
| 5 | Click **Read audit chain**. | HTTP status 200 (REAL). Rows in this chain: 4 (REAL). Calls per outcome: `HOLD_FOR_REVIEW` 1 (REAL), the others 0 (REAL). The table lists the four rows in time order. The page then lists what the log cannot prove. | `logs/audit.log`, the rows with this case id. | Only the role `admin` may read the audit log (TA-35). | `audit.read`, written after the read, so the chain on screen does not hold it. A second click shows 5 rows. |

**Verified Fact.** The numbers in the "You will see" column are the values of the run on 2026-10-13 (`docs/demo/evidence.md`, section 4). The latency changes from run to run, because it is the time of the stub call.

**What the "cannot prove" list says (Verified Fact, from the run).** The role is a header word the caller typed, so the log cannot show who the caller was (`caller_identity`). The caller chose the case id, so a second caller can add a row to the same case (`case_membership`). The log is a plain file, so a line can be changed or deleted (`log_integrity`). The log stores no policy reasons and no policy version (`policy_reasons_and_version`). The final action is `none` on every row, because no route changes a device (`final_action`).

## 4. Variants

Run each variant after the main case. Click **Start a new case** between variants.

### 4.1 AI timeout: the recommendation returns HOLD_FOR_REVIEW and no summary

Stop the app. Start it again with a short model deadline:

```powershell
$env:POLICY_ENGINE = "python"
$env:AI_MODEL_TIMEOUT_SECONDS = "0.001"
.\.venv\Scripts\python.exe -m uvicorn apps.api.main:app --port 8000
```

The value 0.001 seconds is a test setting. The stub waits 10 ms, so every call misses the deadline. The default in code is 10 seconds. It is PROPOSED. Owner: Team-Force.

Run steps 1 to 3 with `STO-00002`.

| Step | You will see (Verified Fact, from the run on 2026-10-13) |
|---|---|
| 2 | HTTP status 200 (REAL). The lookup does not use the model, so it still works. |
| 3 | HTTP status 202 (REAL). Outcome `HOLD_FOR_REVIEW`. The page says "A person must review this case. The system shows no summary and no recommendation text." Reason: `failmode.schema_failure`, `failmode.timeout`. The summary is null and the recommendation is null. No substitute text appears. |
| 4 | Click **Approve (yes)**. HTTP status 404 (REAL). Nothing is stored. No sentence was shown, so a decision has nothing to attach to. |
| 5 | Rows in this chain: 3 (REAL). The third row is `policy.hold` with outcome `HOLD_FOR_REVIEW`. |
| Service check | Click **Check health**. HTTP status 200 (REAL). The health route stays up while the model path fails. |

Stop the app and start it again without `AI_MODEL_TIMEOUT_SECONDS` to go on.

### 4.2 A device with no row: STO-00001

Type `STO-00001` and click **Read storm**. The storm lists device `DEV-00001`. The file `devices.csv` has no `DEV-00001`.

| Step | You will see (Verified Fact) |
|---|---|
| 2 | HTTP status 404 (REAL). The page says no device row has this id and the server did not pick another device. |
| 3 | HTTP status 403 (REAL). Outcome `BLOCK`. Reason `failmode.missing_id`. No text. The model did not run, so the page shows no model, hash, tokens or delay. |
| 4 | HTTP status 404 (REAL). Nothing is stored. |
| 5 | Rows in this chain: 2 (REAL). `record.storm_read`, then `policy.deny` with outcome `BLOCK`. |

### 4.3 A stale device: STO-00005

Type `STO-00005` and click **Read storm**. The storm has two alarm rows with the same dedupe key `DED-00005`. Raw count 2 (REAL). Deduped count 1 (REAL). Flagged count 0 (REAL). The device is `DEV-00005`. Its `stale_topology_flag` is `true`.

Click **Look up device** (HTTP status 200, REAL). Click **Ask for a recommendation**. HTTP status 403 (REAL). Outcome `BLOCK`. Reason `failmode.stale_topology_true` and `rule.stale_topology_blocks_recommendation`. No text. The model did not run.

### 4.4 A person says no

In the main case (`STO-00002`), at step 4 click **Reject (no)** instead of yes. HTTP status 200 (REAL). Decision `no`. Approval id `none (a no gets no id)`. The stored record and the audit row hold `approval_id` null. The "cannot prove" list then says the approval id is null on every row. **Verified Fact** (`tests/app/test_demo_flow.py::test_a_no_decision_is_in_the_chain_with_no_approval_id`).

### 4.5 Refused callers (command line)

The page has no way to send a wrong role. Use the command line to show it.

```powershell
# No role header: 403, a policy.deny audit row, role null.
Invoke-WebRequest http://127.0.0.1:8000/records/DEV-00002 -SkipHttpErrorCheck | Select-Object StatusCode

# The engineer role gets the two sensitive fields back (TA-15). In this data mgmt_ip holds a word such as alpha, not an address.
Invoke-RestMethod http://127.0.0.1:8000/records/DEV-00002 -Headers @{ "X-User-Role" = "engineer" }
```

Also: `Invoke-WebRequest` needs PowerShell 7 for `-SkipHttpErrorCheck`. In Windows PowerShell 5.1, wrap the call in `try { } catch { $_.Exception.Response.StatusCode }`.

## 5. What happens behind each step

| Question | Answer | Source |
|---|---|---|
| Which step can change stored data? | Only step 4. It appends one line to `logs/approvals.jsonl`. | `apps/api/services/approvals.py` |
| What comes first in step 4, the audit row or the stored decision? | The audit row. If the row cannot be written, the route returns 500 and stores nothing. If the store fails after the row, the row stays and no approval exists. | `tests/app/test_audit_before_state_change.py` |
| Can the model decide? | No. The policy gives the outcome. A model answer that says `EXECUTE` is turned into `BLOCK` with no text. | `tests/app/test_recommend_route.py::test_recommend_never_returns_execute` |
| Is there a route that runs a command? | No. No route has `execute` in its path. | `policy/tests/test_policy_python.py::test_no_route_can_execute` |
| What happens to command text in the answer? | The route returns `HOLD_FOR_REVIEW` with no text. The reason is `failmode.command_text_in_recommendation`. The list is short and misses phrases that mean the same. | `tests/app/test_command_phrases.py` |

## 6. After the demo

- Stop the app with Ctrl+C.
- The files `logs/audit.log` and `logs/approvals.jsonl` keep the rows of the demo. Do not delete them if you need the evidence. Move them first.
