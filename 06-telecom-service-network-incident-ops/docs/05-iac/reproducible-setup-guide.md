# Reproducible setup guide

| Field | Value |
|---|---|
| Stage | S04-05 — Infrastructure as code (Challenge 5), Half A |
| Date / version | 2026-10-11, v1.1. v1.1 (S04-05 Half B): added the one-command section, removed the hand-installed `httpx` line because `requirements.txt` now pins it, and added the container route. Runs R1 to R6 are unchanged. Runs H1 to H8 are in `evidence.md`. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The Windows commands ran on Python 3.13.5 and 3.12.10 and gave `15 passed`. The Linux commands ran inside a `python:3.11-slim` container and gave `15 passed`. macOS was not run. Native Ubuntu with Python 3.10 could not create a venv. Owner: Team-Force. |
| Evidence sources | Runs R1 to R6 below; `requirements.txt`; `pyproject.toml`; `README.md`; `Makefile`; `scripts/sanity_check.py`; `etl/run_daily_batch.py`; `docs/00-setup/tool-versions.md`; `docs/00-setup/replay-log.md` |
| Assumptions | Every run used a copy of the working tree made with `robocopy` (Windows) or `cp -r` (container). The copy left out `.venv`, `.pytest_cache`, `__pycache__`, and `logs/audit.log`. The runs did not use `git clone`. The last commit does not hold the S04 work (finding IG-14 in `iac-gap-report.md`), so a clone gives a different tree. |
| Unresolved issues | macOS is Unknown. Python 3.10 is Unknown. The commit that holds the S04 work does not exist yet. |
| Residual risks | Half B added `httpx==0.28.1` to `requirements.txt`. A copy of the repo from before that change, or a `git clone` of the last commit, still lacks the line and shows three collection errors until `httpx` is installed. The last commit also lacks the bootstrap scripts, the `Dockerfile`, and the S04 files until the work is committed. |

## What this file is

This file lists the exact commands from a fresh copy of the repo to a passing `pytest -q`. It has one set for Windows PowerShell and one set for Linux and macOS.

Tool versions come from `docs/00-setup/tool-versions.md`: Python 3.13.5, pip 25.1.1, `httpx` 0.28.1, git 2.35.1.windows.2. CI uses Python 3.11 (`.github/workflows/ci.yml` line 9).

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## What you need before you start

| Need | Version | Needed to run `pytest -q` | Source |
|---|---|---|---|
| Python | 3.11, 3.12, or 3.13. Use 3.11 to match CI. | Yes | Runs R2, R3, R4 |
| `venv` module | Part of Python. On Ubuntu and Debian, install `python3.X-venv` first. | Yes | Run R5 |
| Internet access to PyPI | n/a | Yes, for the install | Runs R1 to R4 |
| git | 2.35.1 or newer | Only to get the files | `tool-versions.md` |
| Docker, Node, OPA, make | any | No | `deployment-dependency-list.md` |

## One-command setup (added in Half B)

Each command creates `.venv`, installs `requirements.txt`, and runs `pytest -q`. It stops with a non-zero exit code and a message when a step fails. Output of each run is in `evidence.md`.

| Where | Command | Verified in |
|---|---|---|
| Windows PowerShell | `powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1` | H1, `15 passed` on Python 3.13.5 |
| Windows, other Python | `powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Python "py -3.11"` | H3 ran `py -3.12` with `-SkipTests` |
| Linux or macOS | `bash scripts/bootstrap.sh`, or `PYTHON=python3.11 bash scripts/bootstrap.sh` | H5 through `make setup`, `15 passed` on Python 3.11.17 |
| Linux or macOS with `make` | `make setup` | H5 |
| Any machine with Docker | `docker build -t telecom-ops-tests .` then `docker run --rm telecom-ops-tests` | H7, `15 passed` on Python 3.11 |

Use `-SkipTests` (PowerShell) or `SKIP_TESTS=1` (bash) to set up without running the tests. Run the script from any folder. It moves to the project folder on its own.

The steps below are the same work by hand.

## Windows (PowerShell)

Verified Fact. This set ran as runs R1, R2, and R3. Since Half B, `requirements.txt` holds `httpx`, so the separate `httpx` line from those runs is no longer needed.

```powershell
git clone https://github.com/mumbrajkar-ul2/SPRINT3CAPSTONE.git
cd SPRINT3CAPSTONE\06-telecom-service-network-incident-ops

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

If your copy is older than 2026-10-11, add `.\.venv\Scripts\python.exe -m pip install httpx==0.28.1` before the last line.

If more than one Python is installed, use `py -3.11 -m venv .venv` in place of `python -m venv .venv`. The runs used `py -3.13` and `py -3.12`.

Expected last line on Python 3.13.5 or 3.12.10: `15 passed, 7 warnings`.

Run the two optional checks from the same folder.

```powershell
.\.venv\Scripts\python.exe scripts\sanity_check.py
.\.venv\Scripts\python.exe etl\run_daily_batch.py --sample
```

Expected output, in order:

```text
{'status': 'ok', 'repo': '06-telecom-service-network-incident-ops', 'csv_files': 6, 'events': 3000, 'clean_repo_contract': True}
{'processed': 354, 'malformed': 1, 'sample': True}
```

## Linux and macOS (bash or zsh)

Verified Fact for Linux on Python 3.11.17 (run R4). Assumption for macOS. The commands carry no Linux-only step, but no Mac was available.

```bash
git clone https://github.com/mumbrajkar-ul2/SPRINT3CAPSTONE.git
cd SPRINT3CAPSTONE/06-telecom-service-network-incident-ops

python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

If your copy is older than 2026-10-11, add `python -m pip install httpx==0.28.1` before the last line.

On Ubuntu and Debian, run `sudo apt install python3.11-venv` first when `python3.11 -m venv .venv` stops with the text `ensurepip is not available`. Run R5 shows that text on Ubuntu 22.04.5 with Python 3.10.12. This stage did not run `sudo`.

Expected last line on Python 3.11.17: `15 passed, 1 warning`.

## Start the API by hand (optional)

Verified Fact in S00 (`tool-versions.md`, "Commands used").

```powershell
.\.venv\Scripts\python.exe -m uvicorn apps.api.main:app --port 8011
```

Open `http://127.0.0.1:8011/health`. The body is `{"status":"ok","repo":"06-telecom-service-network-incident-ops"}` (`replay-log.md` section 2.1).

Do not copy the `README.md` line `uvicorn apps/api.main:app --reload`. It has a slash where a dot belongs.

## Secrets and settings during setup

`pytest -q` needs no secret. The test `test_legacy_script_reads_password_from_environment` sets `SHARED_DB_PASSWORD` to `local-test-only` for its own child process (`tests/characterization/test_current_behaviour.py` lines 113 to 115). The value is a test word, not a secret.

To run `legacy/reconcile_legacy.py` by hand, set that name first.

```powershell
$env:SHARED_DB_PASSWORD = "local-test-only"
.\.venv\Scripts\python.exe legacy\reconcile_legacy.py
```

Expected output: `legacy reconciled 354`. The value `CHANGE_ME` in `.env.example` makes the script stop with an error that names the variable, by design (`apps/api/settings.py` lines 17 to 21). Copying `.env.example` to `.env` changes nothing, because no code reads a `.env` file (IG-08).

## What a test run changes

Every `pytest -q` appends lines to `logs/audit.log`. Git tracks that file, so `git status` shows it as modified after a run (IG-11). The new lines are test output. Run `git checkout -- logs/audit.log` before you commit if you do not want them.

## Things that go wrong

| What you see | Cause | Fix |
|---|---|---|
| `RuntimeError: The starlette.testclient module requires the httpx package to be installed.` and `3 errors` | Your copy of `requirements.txt` has no `httpx` line. Copies from before 2026-10-11 lack it (IG-05). | `python -m pip install httpx==0.28.1`, then run `pytest -q` again. |
| `bootstrap FAILED: Python command '...' did not run` (exit code 1) | The Python name does not exist on this machine. | Pass `-Python "py -3.11"` or set `PYTHON=python3.11`. |
| `bootstrap FAILED: could not create .venv` (exit code 2) | Ubuntu or Debian without the `venv` package (H6). | `sudo apt install python3.X-venv`, then run the script again. |
| `bootstrap FAILED: pip install failed` (exit code 3) | No network, or a package version is not on the index. | Read the pip lines above the message. |
| `bootstrap FAILED: pytest reported a failure` (exit code 4) | A test failed. | Read the pytest lines above the message. |
| `The virtual environment was not created successfully because ensurepip is not available.` | Ubuntu or Debian without the `venv` package (R5). | `sudo apt install python3.X-venv`, where X is your minor version. Delete `.venv`. Create it again. |
| `make: command not found` (Windows) | `make` is not installed on Windows. | Skip `make`. Call the Python commands above. Half B adds a bootstrap script. |
| `make test` runs but cannot find `pytest` | `Makefile` line 1 uses `python3`, which is not the venv Python (IG-04). | Activate the venv first, or call `make PYTHON=.venv/bin/python test`. This was not run in this stage. **Assumption.** |
| `python3` opens the Microsoft Store (Windows) | The `WindowsApps\python3.exe` alias (IG-04). | Use `python` or `py -3.11`. |
| `ModuleNotFoundError: No module named 'apps'` | The command ran from another folder. `pyproject.toml` line 2 sets `pythonpath` to `.`, which is the folder that holds the file. | `cd` into `06-telecom-service-network-incident-ops` first. |
| `legacy` script prints an error that names `SHARED_DB_PASSWORD` | The name is unset or equals `CHANGE_ME`. | Set a local value as shown above. |

## Run records

All six runs were made on 2026-10-11 on this machine (Windows 10.0.26200, Docker 28.3.2). The output lines below were copied from the terminal.

| Run | Where | Python | Commands | Result |
|---|---|---|---|---|
| R1 | Windows copy in `%TEMP%\s0405-win313` | 3.13.5, pip 25.1.1 | `python -m venv .venv`, `pip install -r requirements.txt`, `pytest -q` | `3 errors in 1.03s`. Exit code 2. Every error is the `httpx` `RuntimeError`. |
| R2 | Same venv as R1 | 3.13.5 | `pip install httpx==0.28.1`, `pytest -q`, `scripts\sanity_check.py`, `etl\run_daily_batch.py --sample` | `15 passed, 7 warnings in 3.06s`. The two scripts printed the lines shown above. |
| R3 | Windows copy in `%TEMP%\s0405-win312` | 3.12.10 | `py -3.12 -m venv .venv`, `pip install -r requirements.txt httpx==0.28.1`, `pytest -q` | `15 passed, 7 warnings in 2.89s`. |
| R4 | Container `python:3.11-slim`, folder mounted read-only and copied to `/work` | 3.11.17, pip 24.0 | `python -m venv .venv`, `. .venv/bin/activate`, `pip install -r requirements.txt`, `pytest -q`, then `pip install httpx==0.28.1`, `pytest -q`, then the two scripts | First `pytest -q`: `3 errors in 0.68s`. Second: `15 passed, 1 warning in 1.04s`. The two scripts printed the same lines as R2. The image has no `make`. |
| R5 | WSL, Ubuntu 22.04.5, copy in the WSL home folder | 3.10.12 | `python3 -m venv .venv` | Stopped with `ensurepip is not available`. `python3 -m pip` also fails: `No module named pip`. No install was tried. |
| R6 | Same venv as R2 | 3.13.5 | `pip uninstall -y uvicorn PyYAML python-dotenv click colorama h11`, `pytest -q` | `15 passed, 7 warnings in 1.64s`. |

The same suite in the existing `.venv` of the working tree also gave `15 passed, 7 warnings in 2.42s` on 2026-10-11. That `.venv` already holds `httpx` and `jsonschema`, which S00 and S03 installed by hand.

## Why 7 warnings on 3.13 and 1 on 3.11

**Verified Fact.** `apps/api/services/audit.py` line 9 calls `datetime.utcnow()`. Python 3.12 and later print a deprecation warning for it. Python 3.11 does not. The run counts match that: 7 warnings on 3.12 and 3.13, 1 warning on 3.11. **Inference.** The one remaining warning on 3.11 is the Starlette `anyio` alias warning that `replay-log.md` section 1.3 names.

## Lifecycle

This guide cites `docs/00-setup/tool-versions.md` for tool versions and `docs/04-secrets/cleaned-configuration-model.md` for the secret rule. Half B turns the Windows and Linux commands into `scripts/bootstrap.ps1` and `scripts/bootstrap.sh`. Stage S04-07 calls the bootstrap from CI. Stage S09 uses this guide in the readiness checklist.
