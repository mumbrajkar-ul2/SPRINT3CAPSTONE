# Incident response runbook

| Field | Value |
|---|---|
| Stage | S04-11 — Reliability and failure engineering (Challenge 11), Half A |
| Date / version | 2026-10-11, v1.0. Replaces the draft that said "This runbook is intentionally incomplete." |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. All five sections are written. The severity names and every number are PROPOSED. Owner: Team-Force. No message channel is named, because the packet names none. |
| Evidence sources | `docs/11-reliability/failure-mode-catalogue.md`; `docs/11-reliability/degraded-mode-design.md`; `docs/11-reliability/retry-and-circuit-breaker-strategy.md`; `docs/11-reliability/idempotency-plan.md`; `docs/11-reliability/probe-output.json`; `apps/api/main.py`; `apps/api/services/policy.py`; `apps/api/services/audit.py`; `docs/09-ai-guardrails/approval-workflow.md`; `docs/00-contract/operating-contract.md` |
| Assumptions | The system under change is this workspace. It runs locally on synthetic data. No production system, live device, or network change exists (operating contract rows 6, 8, and 9). Commands are PowerShell, run from `06-telecom-service-network-incident-ops`. |
| Unresolved issues | Response-time targets for each level are Unknown. Team-Force sets them. The channel for notices is Unknown. The inbox that should receive held cases does not exist (RF-08). The running app has no setting that turns the AI path off (see Rollback). |
| Residual risks | `/health` returns 200 in every failure the catalogue lists, so a green health check does not show that the service is working. A 500 error carries no correlation id. Triage then starts from the time and the route. |

## How to use this runbook

1. Read "Severity levels" and pick a level.
2. Follow "Triage steps" in order.
3. Use "Rollback steps" for the cause you found.
4. Send the notices in "Communications".
5. Collect everything in "Evidence to collect" before you close the incident.

Repo text before this stage, kept for the record: "This runbook is intentionally incomplete. Participants should add severity model, triage steps, rollback/degraded-mode procedures, communication templates, and evidence capture."

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file, a probe check id, or a test name.

---

## 1. Severity levels (written in S04-11)

The level names are PROPOSED. Owner: Team-Force. The levels use what a person can observe. They use no numeric cutoff.

Open question for S03: the YAML has no names for incident severity levels. Alarm severity (`gold`, `bronze`, and others) and event severity (`debug` to `critical`) are separate scales and are not used here.

| Level | What a person observes | Examples from the catalogue | What it means |
|---|---|---|---|
| Stopped | A business route gives no useful answer to any caller. Or audit rows cannot be written or are being lost. | FM-10 (`devices.csv` missing), FM-11 (policy engine fails), FM-12 (audit log unwritable), FM-13 (audit rows lost) | Act now. Do not wait for more reports. |
| Degraded | One dependency is down. The degraded-mode design says what still works. People still get answers or a held case. | FM-03, FM-04 (AI timeout or error), FM-14 (model hangs and other routes slow down) | Work on it now. Tell the desk that receives held cases. |
| Data fault | A data defect is found. Routes still answer. | FM-07 (stale topology), FM-08 (bad batch rows), FM-09 (impossible alarm times), FM-15 (device id not found) | Record it. Fix it in the next planned change. |
| Watch | A failure happened once and cleared by itself. No user saw a wrong answer. | FM-01 (a request with no correlation id) | Note it. Look again if it repeats. |

Rules for choosing a level:

- If two levels fit, choose the higher one.
- A held case (HTTP 202, HOLD_FOR_REVIEW) is a designed result. It is Degraded when many callers get it and Watch when one caller gets it once.
- A wrong answer shown to a person is at least Data fault, even when no outage exists. FM-15 is the example: the record read returns the first row for an unknown id.

Response-time targets for each level are **Unknown**. Team-Force sets them. This runbook states none.

---

## 2. Triage steps (written in S04-11)

### Step 1. Write down the facts

Write the time, the route, and the status code. If the response has an `X-Correlation-Id` header, write it. A 500 response has no such header (probe P7, P8). In that case write the time only.

### Step 2. Check that the process answers

```powershell
curl.exe -s http://127.0.0.1:8000/health
```

The commands use `curl.exe` because Windows PowerShell 5.1 stops on an HTTP error status with `Invoke-WebRequest`. The port 8000 is the `uvicorn` default. Change it if the app runs on another port.

The body `status` `ok` means the process answers. It does not mean the routes work. Go on to step 3 either way. If there is no answer, the process is down or did not start. Check that `policy/opa/policy_data.json` and `semantic-layer/ai-context-policy.yaml` exist, because the app reads both when it starts (`policy.py` line 29, `ai_gateway.py` line 108).

### Step 3. Find which routes fail

Call a record read and a summary with a known good id. `DEV-00002` has `stale_topology_flag` false.

```powershell
curl.exe -s -o NUL -w "%{http_code}`n" -H "X-User-Role: operator" http://127.0.0.1:8000/records/DEV-00002
curl.exe -s -w "`n%{http_code}`n" -X POST -H "X-User-Role: operator" http://127.0.0.1:8000/ai/summarize/DEV-00002
```

The first command prints only the status code. It does not print the record body, because the body holds `mgmt_ip` and `credential_profile`. The second prints the summary body and then the status code. The summary body holds neither field.

### Step 4. Match the result to a row

| What you see | What it points to | First check | Level | Catalogue id |
|---|---|---|---|---|
| Record read 200. Summary 202 with `HOLD_FOR_REVIEW` and `failmode.timeout` in `reasons`. | The model is slow or gone. | Is the model service up? Is `AI_MODEL_TIMEOUT_SECONDS` set to a very short number? | Degraded | FM-03 |
| Summary 202 with only `failmode.schema_failure`. | A bad answer, or a model that raised an error. The reason cannot tell them apart. | Does the model service answer? Run one call by hand. | Degraded | FM-04 |
| Record read 403 and summary 403 for a role that worked before. Body `{"error": "forbidden"}`. | The policy engine failed. A wrong role gives the same body. | Is `POLICY_ENGINE` set to `opa`? Run `where.exe opa`. Check the `policy.deny` rows (see Step 5). | Stopped | FM-11 |
| Record read 500 and summary 500. Body text `Internal Server Error`. | `devices.csv` is missing, or the audit log cannot be written. | Run the two checks under "Telling the two 500 causes apart". | Stopped | FM-10, FM-12 |
| Record read 200 and `/health` fast, but everything feels slow while summaries wait. | The model hangs and holds route threads. | Time `/health`. Count summaries in flight. | Degraded | FM-14 |
| A record read for an unknown id returns `REC-0001` with 200. | The first-row fallback. | Not an outage. Check the id the caller sent. | Data fault | FM-15 |
| Summary 403 with `failmode.stale_topology_true`. | The device row is stale. | Count true flags in `devices.csv`. | Data fault | FM-07 |
| Summary 202 with `failmode.stale_topology_blank`. | The flag is blank on this row. | Look at the row in `devices.csv`. | Data fault | FM-07 |
| Audit rows are missing for calls you know happened. | Rows were lost when threads wrote at once. | Run the line-count check in Step 5. | Stopped | FM-13 |
| `python etl/run_daily_batch.py --sample` prints nothing and exits with code 1. | The batch stopped on a missing file or a line that is not valid UTF-8. | Read the last line of the error text. | Data fault | FM-08 |
| The batch prints `malformed` 0 but a person sees a short row. | A short or long row passes as good. | Open the file at that row. | Data fault | FM-08 |

### Telling the two 500 causes apart

```powershell
Test-Path data\synthetic\devices.csv
(Get-Item logs\audit.log).IsReadOnly
(Get-Item logs).PSDrive.Free
```

- `Test-Path` returns `False`: the data file is missing. See "Rollback steps", item C.
- `IsReadOnly` returns `True`, or the free space is 0: the audit log cannot be written. See item D.
- All three look fine: read the web server output for the error text.

### Step 5. Read the audit rows

Find all rows for one correlation id:

```powershell
Select-String -Path logs\audit.log -Pattern '"correlation_id": "PUT-THE-ID-HERE"'
```

Count refusals:

```powershell
(Select-String -Path logs\audit.log -Pattern '"action": "policy.deny"' | Measure-Object).Count
```

A sudden rise of `policy.deny` rows for the role `operator` points to FM-11. A wrong role gives the same row.

Count lines that do not parse:

```powershell
$bad = 0; Get-Content logs\audit.log | ForEach-Object { $line = $_; try { $null = $line | ConvertFrom-Json -ErrorAction Stop } catch { $bad++ } }; $bad
```

A result above 0 means a cut line. A line that is missing leaves no mark, so a count of 0 does not prove that no row is lost (FM-13).

### Step 6. Pick the level and go to Rollback

Use "Severity levels". Write the level next to the facts from Step 1.

---

## 3. Rollback steps (written in S04-11)

This system has no live device change and no execute path (operating contract rows 8 and 9). Rollback means returning code, configuration, or a data file to a known good state.

**What does not exist.** The running app has no setting that turns the AI path off. The only ways to stop calls to the model are to restart the app with a very short `AI_MODEL_TIMEOUT_SECONDS` or to return to an earlier code version. Half B adds the breaker, which opens on its own. A manual switch is not designed. That is an open item for Team-Force.

Do not delete or edit `logs/audit.log` in any step. It is append-only evidence.

### A. The model path fails or hangs (Degraded)

1. Confirm the summary route returns 202 with `summary` null. The app is behaving as designed.
2. Tell the desk (see Communications, notice 2).
3. To stop callers waiting the full deadline, restart the app with a short deadline, for example 2 seconds. The default is 10 seconds. Both numbers are PROPOSED.

```powershell
$env:AI_MODEL_TIMEOUT_SECONDS = "2"
```

   Then restart the app. The number is read when each call starts, and a running process cannot see the change.
4. After Half B: read the breaker state. An open breaker is working as designed. It closes after a test call succeeds.
5. When the model is back, restart the app with the variable removed:

```powershell
Remove-Item Env:AI_MODEL_TIMEOUT_SECONDS
```

### B. The policy engine fails (Stopped)

1. Confirm that `POLICY_ENGINE` is `opa` or that `opa` is on the PATH (`where.exe opa`).
2. Run the engine by hand to read its error.
3. To restore service, set the engine to the Python copy and restart the app:

```powershell
$env:POLICY_ENGINE = "python"
```

   The Python copy reads the same `policy_data.json` and follows the same decision table (`policy.py` lines 1 to 17). Whether it gives the same answer as `opa` on every input is **Unknown** here, because the two Rego tests are skipped when `opa` is absent. The Python copy denies on any input it does not recognise. Tell Team-Force before you use this setting in any shared setting.
4. The app finds `opa` once per process (`policy.py` lines 49 to 66). Restart after you change anything about `opa`.

### C. `devices.csv` is missing or wrong (Stopped, or Data fault)

1. Check what changed: `git status --short data/synthetic/devices.csv`.
2. Restore only that file from version control:

```powershell
git checkout -- data/synthetic/devices.csv
```

3. A failed first load is not kept, so the next request reads the file. If a bad file loaded earlier, restart the app. The app keeps the rows it loaded until it restarts (`domain_service.py` lines 8 to 13).
4. Check with Step 3.

### D. The audit log cannot be written (Stopped)

1. Check the three items under "Telling the two 500 causes apart".
2. Free disk space or fix the folder permission for `logs/`.
3. Do not delete `logs/audit.log` to make room. Move old copies elsewhere only after Team-Force agrees. A rotation rule is **Unknown**.
4. After the write works, call Step 3. Every business route returns to normal on the next request.

### E. Audit rows are lost (Stopped)

1. Record the lost rows in the evidence folder (see item 7 of "Evidence to collect").
2. The probe lost rows only when several threads wrote at the same moment (probe P9). Ask callers to send one request at a time until the cause is fixed. Decision D-3 proposes a lock in `audit.py`. The lock is not in place yet.
3. Rows already lost cannot be rebuilt from this log. Say so in the notice.

### F. The daily batch fails (Data fault)

1. Read the last line of the error text.
2. Fix or restore the file (item C). The batch writes nothing, so a second run is safe.
3. Run it again:

```powershell
.venv\Scripts\python.exe etl\run_daily_batch.py --sample
```

### G. A code change caused it

1. Find the change: `git log --oneline -n 5`.
2. Revert that one commit: `git revert <commit>`.
3. Run the whole suite and read the result:

```powershell
.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q
```

   The S04-10 run passed 209 tests and skipped 2 (`docs/10-performance/evidence.md`). A later stage may have changed that number. The suite must pass as before the revert.
4. Mangesh (FDE) reviews the revert before it is kept (operating contract row 7).

### What cannot be rolled back here

A live network change cannot be rolled back by this runbook because none exists. If a later stage adds one, the change must be reversible and validated before it runs (gate 4 of `outcome.execute`). Its own reverse plan is the rollback.

---

## 4. Communications (written in S04-11)

### Who is told

| Person or desk | Why | When |
|---|---|---|
| The desk that triages (`persona.noc_operator`, PROPOSED desk job. Owner: Team-Force) | Receives held cases and wrong-looking answers. | At level Degraded and Stopped. |
| The live-change approver (`persona.network_engineer`) | Must know when summaries are held, because no approval relies on a held case. | At level Degraded and Stopped. |
| The owner of PROPOSED items (Team-Force, acted for by Mangesh (FDE)) | Owns every number and every decision in this runbook. | At every level except Watch. |

The channel (chat, email, ticket) is **Unknown**. The packet names none. Team-Force names it.

### Notice 1. Start

> **Incident: <short name>.** Level: <Stopped | Degraded | Data fault>.
> Started at <time>. Seen by <who>.
> What people see: <for example, "summaries come back as held with no text" or "record reads return an error">.
> What still works: <for example, "record reads and the health check">.
> What to do now: <for example, "triage by hand from the record. Do not act on a held case.">
> Next update at <time>.

### Notice 2. Held cases (the model path is down)

> Summaries are on hold. A call to the summary route returns "HOLD_FOR_REVIEW" with no text. This is the designed result. No summary exists for the case.
> Please read the record and decide by hand. Do not treat a held case as a recommendation.
> Record reads still work. They may be slower than usual.

### Notice 3. Update

> **Incident: <short name>.** Update at <time>.
> What changed: <one sentence>.
> What we know: <one sentence>. What we do not know: <one sentence>.
> Next update at <time>.

### Notice 4. All clear

> **Incident: <short name>.** Closed at <time>.
> Cause: <one sentence, or "not yet known">.
> What was lost: <for example, "no data", or "<n> audit rows">.
> What we changed: <one sentence>.
> Evidence is in <folder>.

Rules for every notice:

- Write the facts in short sentences. Do not guess a cause.
- Do not paste `mgmt_ip`, `credential_profile`, a password, a key, or a token.
- Do not paste a record body or a prompt. The audit row holds `prompt_hash` for that reason.
- If a number is not known, write "Unknown".

---

## 5. Evidence to collect (written in S04-11)

Collect these before the incident is closed. Each item answers a question a reviewer will ask.

| # | Item | How to collect it | What it shows |
|---|---|---|---|
| 1 | Times: first seen, level chosen, fixed, closed | Write them in the notes. | How long each step took. |
| 2 | The correlation ids of failing calls | The `X-Correlation-Id` response header. A 500 has none, so write the time. | Which audit rows belong to the failure. |
| 3 | The audit rows for the window | `Select-String` on `logs/audit.log`, saved to a file. | Who called, what was decided, and whether a row is missing. |
| 4 | The count of refusals and cut lines | The two counts in Step 5. | Whether a policy outage or lost rows are involved. |
| 5 | The code version | `git rev-parse HEAD` and `git status --short`. | Which code ran. |
| 6 | The settings in force, names only | `Get-ChildItem Env:AI_MODEL_TIMEOUT_SECONDS, Env:POLICY_ENGINE`. After Half B also `BREAKER_FAILURE_THRESHOLD`, `BREAKER_OPEN_SECONDS`, and `MODEL_MAX_IN_FLIGHT`. | Which PROPOSED numbers were live. Never copy a secret value. |
| 7 | What was lost, if anything | For lost audit rows, the count of calls you know happened against the rows found. | What the evidence cannot prove. |
| 8 | The test result after the fix | The `pytest` line from item G. | That the fix did not break other behaviour. |
| 9 | The decision and who made it | A line in the notes naming the person. | Accountability. A team name is not an approver (operating contract row 10). |
| 10 | What you still cannot prove | One sentence per gap. | Defence question 5. |

**Where to keep it.** PROPOSED. Owner: Team-Force. A folder `evidence/incidents/YYYY-MM-DD-short-name/` holds the saved files and a notes file. The folder does not exist yet.

**Half B adds** the drill runs to `docs/11-reliability/recovery-evidence.md`. A real incident uses the same layout.

---

## Open items

| Item | Owner |
|---|---|
| Response-time target for each level. | Team-Force |
| The channel for notices. | Team-Force |
| An inbox that receives held cases. | Team-Force. Stage S07. |
| A manual switch for the AI path. | Team-Force |
| A readiness route so a monitor can see more than `/health`. | Team-Force. Stage S07. |
| A rotation rule for `logs/audit.log`. | Team-Force |
| Names for incident severity levels in the YAML. | Stage S03 (OQ-7 in `failure-mode-catalogue.md`). |

## Lifecycle

`failure-mode-catalogue.md` names each failure. `degraded-mode-design.md` says what continues. Stage S09 cites this runbook. Stage S10 uses it for defence questions 4, 5, and 8. Half B tests the AI timeout, duplicate, stale data, batch, and alarm drills that this runbook refers to.
