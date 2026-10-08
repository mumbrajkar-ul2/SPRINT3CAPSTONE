# Tool versions

| Field | Value |
|---|---|
| Stage | S00 — Setup and first replay (Execution Plan Phase 0) |
| Date / version | 2026-10-08, v1.0 |
| Author | Mangesh (FDE), run with Cursor |
| Status | PASS |
| Evidence sources | `python --version`, `pip freeze`, `git --version`, `Get-Command` on this machine |
| Assumptions | The versions below are the ones every later stage runs with, unless a stage records a change. |
| Unresolved issues | Python here is 3.13.5. CI pins 3.11. Behaviour may differ between the two. Unknown until CI runs. |
| Residual risks | `opa` is absent. Policy tests in Phase 4 will need the binary or a Python evaluator. |

## Machine

| Tool | Version | Note |
|---|---|---|
| OS | Microsoft Windows NT 10.0.26200.0 | PowerShell shell |
| Python (venv) | 3.13.5 | CI uses 3.11 (`.github/workflows/ci.yml`) |
| pip | 25.1.1 | |
| git | 2.35.1.windows.2 | The repo folder is not a git repository |
| opa | absent | Needed for `opa test`; Phase 4 Challenge 6 falls back to a Python evaluator |
| docker | present | Available for the Phase 4 Challenge 5 container file |
| node | v22.18.0 | Only needed if the Playwright smoke test is run |

## Python packages in `.venv` after `pip install -r requirements.txt`

Pinned in `requirements.txt`:

| Package | Version |
|---|---|
| fastapi | 0.115.0 |
| uvicorn | 0.30.6 |
| pydantic | 2.8.2 |
| pytest | 8.3.2 |
| python-dotenv | 1.0.1 |
| PyYAML | 6.0.2 |

Pulled in as dependencies: annotated-types 0.8.0, anyio 4.15.1, click 8.5.0, colorama 0.4.6, h11 0.16.0, idna 3.20, iniconfig 2.3.1, packaging 26.3, pluggy 1.6.0, pydantic_core 2.20.1, starlette 0.38.6, typing_extensions 4.16.0.

Installed by hand in this stage, not in `requirements.txt`:

| Package | Version | Why |
|---|---|---|
| httpx | 0.28.1 | `fastapi.testclient.TestClient` needs it. Without it `pytest` fails at collection. See `replay-log.md` item 1.2. |
| certifi, httpcore | 2026.7.22, 1.0.9 | Dependencies of httpx |

## Commands used

```text
cd 06-telecom-service-network-incident-ops
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install httpx        # local only; gap recorded
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\sanity_check.py
.\.venv\Scripts\python.exe etl\run_daily_batch.py --sample
.\.venv\Scripts\python.exe -m uvicorn apps.api.main:app --port 8011
```
