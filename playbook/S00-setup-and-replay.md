# S00 — Setup and first replay

Phase 0 in `Execution Plan.md`. This stage runs the inherited repo and records what it does. It changes nothing.

## Inputs

- `Project_Intent.md` (sections 4.2, 4.4, Appendix D)
- `06-telecom-service-network-incident-ops/README.md`
- `06-telecom-service-network-incident-ops/Makefile`
- `06-telecom-service-network-incident-ops/requirements.txt`
- `06-telecom-service-network-incident-ops/api-examples/http-requests.http`

## Prompt

```text
# Stage S00 — Setup and first replay

## Objective
Establish the running baseline of the inherited repo `06-telecom-service-network-incident-ops` and record exactly what it does today. Make no change to the repo other than the two new files named under Required Artifacts.

## Scope
Include:
- Create a Python venv and install `requirements.txt`.
- Run `pytest -q`, `python scripts/sanity_check.py`, `python etl/run_daily_batch.py --sample`.
- Start the API with uvicorn (`apps.api.main:app`).
- Replay four calls and save request and response bodies:
  1. GET /health
  2. GET /records/REC-0001 with header X-User-Role: operator
  3. GET /records/DOES-NOT-EXIST with header X-User-Role: operator
  4. POST /ai/summarize/REC-0001
- Save the lines that `logs/audit.log` gained during those calls.
- Record tool versions: Python, pytest, fastapi, uvicorn, pydantic, PyYAML, OS.
Exclude:
- Any edit to application code, tests, data, configuration, or `.env.example`.
- Any opinion about what should change. That is Phase 1 and later.

## Required analysis
For each command and each call, record: what ran, exit code or HTTP status, output or body, side effect (files written, log lines added). Compare each result with `Project_Intent.md` Appendix D and state match or difference.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, or Unknown.
- A Verified Fact names a command, a file path, a test name, a log line, or a replay result.
- Write Unknown where something did not run or could not be observed. Do not fill a gap with a guess.

## Constraints and guardrails
- Plain speech. Short sentences. Everyday words.
- Redact secrets in every artifact. Write <redacted> for any password, key, or token that appears in output.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- Stop the uvicorn process when done.

## Locked facts (from Project_Intent.md 4.3; read, do not re-derive)
| Constant | Value |
|---|---|
| Primary data file for the API | `devices.csv` |
| Missing-record behaviour | return first row |
| Allowed API roles | admin, operator, clinician, engineer, ai_agent |
| AI model version | local-sim-v1 |
| Guardrail status returned | not_enforced |
| CSV row counts | 354 each |
| Event count | 3000 |
| CI Python version | 3.11 |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md` — one section per command and per call: what ran, result, side effect, match with Appendix D.
2. `06-telecom-service-network-incident-ops/docs/00-setup/tool-versions.md` — a table of tool and version, plus the exact commands used to create the venv.

## Completion gate
PASS when the three commands and four calls all ran and the saved outputs match Appendix D. CONDITIONAL PASS when a command ran but one result differs from Appendix D and the difference is written down. BLOCKED when a command or the server did not run.

## Lifecycle linkage
Cite `Project_Intent.md` Appendix D in the replay log. Phase 1 (S01) and Phase 2 (S02) will cite these two files as their runtime evidence.

## Required final response
End with exactly these seven items:
1. Stage status: PASS, CONDITIONAL PASS, or BLOCKED, with one sentence why.
2. Key findings.
3. Major risks.
4. Assumptions and unknowns.
5. Artifacts created, with paths.
6. Blocking issues.
7. Recommended next action.
```

## Expected output

| File | Must contain |
|---|---|
| `docs/00-setup/replay-log.md` | Header table. pytest result (count passed). sanity_check output. ETL sample output with blank-field counts. Four calls with status code, body, and the audit lines each added. A match/difference line per item against Appendix D. |
| `docs/00-setup/tool-versions.md` | Header table. Python, pytest, fastapi, uvicorn, pydantic, PyYAML, OS versions. The venv commands. |

## Done test

`GET /records/DOES-NOT-EXIST` returned HTTP 200 with `device_id: REC-0001`, and the replay log says so as a Verified Fact. No file under `apps/`, `tests/`, `data/`, or `etl/` changed.
