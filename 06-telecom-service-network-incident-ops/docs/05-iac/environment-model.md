# Environment model

| Field | Value |
|---|---|
| Stage | S04-05 — Infrastructure as code (Challenge 5), Half A |
| Date / version | 2026-10-11, v1.1. v1.1 (S04-05 Half B): replaced the closing section with a container table. The local and CI columns are unchanged. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The local column rests on runs. The CI column rests on `ci.yml` alone, because no CI run has been seen. Owner: Team-Force. |
| Evidence sources | `.github/workflows/ci.yml`; `pyproject.toml`; `Makefile`; `requirements.txt`; `.env.example`; `apps/api/settings.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `tests/characterization/test_current_behaviour.py`; `docs/00-setup/tool-versions.md`; runs R1 to R6 in `reproducible-setup-guide.md`; `iac-gap-report.md` |
| Assumptions | A GitHub-hosted `ubuntu-latest` runner has no `httpx` unless a step installs it. The workflow has no such step. |
| Unresolved issues | What the CI runner holds before the first step is Unknown. Whether the workflow runs at all is Unknown (IG-09). |
| Residual risks | Local and CI differ in operating system, Python version, install steps, and where the command runs. The first CI run may show a result that no local run has shown. |

## What this file is

This file lists the two places the tests run today: this machine and CI. For each setting it says what the value is and where the value comes from.

The environment is the machine, the tool versions, and the named values a process starts with.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Model

| Setting | Local (this machine) | Where the local value comes from | CI (`ci.yml`) | Where the CI value comes from |
|---|---|---|---|---|
| Operating system | Windows 10.0.26200, PowerShell | **Verified Fact.** `tool-versions.md` "Machine". | Ubuntu, latest image | **Verified Fact.** `ci.yml` line 5, `runs-on: ubuntu-latest`. |
| Python version | 3.13.5 in `.venv` | **Verified Fact.** `tool-versions.md`. Runs R1 and R2. | 3.11 | **Verified Fact.** `ci.yml` line 9. |
| How Python is chosen | Whatever `python` or `py` finds on the PATH | **Verified Fact.** S00 commands; `Makefile` line 1 (`python3`). | `actions/setup-python@v5` installs it | **Verified Fact.** `ci.yml` lines 8 and 9. |
| Lowest Python the repo allows | 3.10 or newer | **Verified Fact.** `pyproject.toml` line 12. | Same file | Same file. Not tested on 3.10 (R5). |
| Virtual environment | `.venv` made by hand | **Verified Fact.** `tool-versions.md` "Commands used". | None. Packages go into the runner's Python. | **Verified Fact.** `ci.yml` has no `venv` step. |
| Install command | `python -m pip install -r requirements.txt`, then by hand `httpx` | **Verified Fact.** `tool-versions.md` "Installed by hand". | `pip install -r requirements.txt` | **Verified Fact.** `ci.yml` line 10. |
| `httpx` | 0.28.1, installed by hand | **Verified Fact.** `tool-versions.md`. | Not installed by any step | **Verified Fact.** `ci.yml` lines 7 to 11. **Inference:** the CI test run stops at collection like R1 and R4 did. |
| `jsonschema` | 4.26.0, installed by hand (S03) | **Verified Fact.** `.venv` package list on 2026-10-11. | Not installed | **Verified Fact.** `ci.yml`. Not needed by `pytest -q`. |
| Test command | `python -m pytest -q` from the project folder | **Verified Fact.** `tool-versions.md`; `Makefile` line 6 does the same through `make test`. | `pytest -q` | **Verified Fact.** `ci.yml` line 11. |
| Folder the command runs in | `06-telecom-service-network-incident-ops/` | **Verified Fact.** `pyproject.toml` line 2 (`pythonpath = ["."]`) needs the folder that holds that file. | The repo root `SPRINT3CAPSTONE/`, because `ci.yml` sets no `working-directory` | **Inference.** `actions/checkout@v4` puts the root there. The tests would not find `requirements.txt` there. |
| Where the workflow file sits | n/a | n/a | `06-telecom-service-network-incident-ops/.github/workflows/` | **Verified Fact.** `git ls-files`. See IG-09. |
| When it runs | When a person types it | n/a | On push and pull request | **Verified Fact.** `ci.yml` line 2. Applies only if GitHub reads the file (IG-09). |
| Environment variables set | None by hand. The tests set `SHARED_DB_PASSWORD` and `PYTHONDONTWRITEBYTECODE` for child processes. | **Verified Fact.** `test_current_behaviour.py` lines 67 to 68 and 113 to 115. | None | **Verified Fact.** `ci.yml` has no `env:` key. |
| Files that hold settings | `.env.example` (names only). No `.env` is loaded. | **Verified Fact.** `.env.example`; `settings.py` reads `os.environ` only. | Same files, plus the workflow | Same. |
| Data path | `data/synthetic/` next to `apps/` | **Verified Fact.** `domain_service.py` line 4, built from the file's own location. | Same relative path | Same code. |
| Log path | `logs/audit.log` next to `apps/`, created if missing | **Verified Fact.** `audit.py` lines 5 and 8. | Same relative path, inside the runner's checkout | Same code. |
| Warnings per run | 7 on 3.13.5 and 3.12.10, 1 on 3.11.17 | **Verified Fact.** R2, R3, R4. | Unknown | Unknown. No run seen. |
| git | 2.35.1.windows.2 | **Verified Fact.** `git --version` on 2026-10-11. | Preinstalled on the runner | **Assumption.** `actions/checkout` needs it. |
| Docker | 28.3.2, daemon answers | **Verified Fact.** `docker --version`; R4. | Not used | **Verified Fact.** `ci.yml`. |
| Node, OPA, Terraform | Node v22.18.0. OPA and Terraform absent. | **Verified Fact.** `tool-versions.md`; `opa version` and `terraform --version` on 2026-10-11. | Not used | **Verified Fact.** `ci.yml`. |

## What differs

1. **Operating system.** Windows locally, Linux in CI. Path separators change. `Scripts\python.exe` becomes `bin/python`. The code builds paths with `pathlib`, so the tests passed on both (R2, R4).
2. **Python version.** 3.13.5 locally and 3.11 in CI. Both pass 15 tests (R2, R4). The warning count differs: 7 against 1.
3. **Install steps.** Local has two extra packages that CI does not install: `httpx` and `jsonschema`. This is the difference most likely to change the result. See IG-05 and IG-06.
4. **Folder.** Local runs inside the project folder. CI would start in the repo root.
5. **Isolation.** Local uses a venv. CI installs into the runner's own Python.
6. **Trigger.** Local runs when a person types. CI runs when GitHub starts the workflow, which may not happen (IG-09).

## Worked example

The test file `tests/test_api_contract.py` imports `fastapi.testclient`. On this machine `httpx` 0.28.1 sits in the `.venv`, so the import works and 15 tests pass. On a CI runner, `pip install -r requirements.txt` installs six packages and their dependencies. `httpx` is not among them. The import raises `RuntimeError`, the same error R1 and R4 printed. The same command gives two results because the install steps differ.

## The container environment (added in Half B, v1.1)

A container is a third environment. `Dockerfile` builds it. The values below come from the file and from run H7 in `evidence.md`.

| Setting | Container | Where the value comes from |
|---|---|---|
| Operating system | Debian-based Linux, from the `python:3.11-slim` image | **Verified Fact.** `Dockerfile` line `FROM python:3.11-slim`. |
| Python version | 3.11.17 | **Verified Fact.** Run H5 printed it. Same minor version as CI. |
| Virtual environment | None. Packages go into the image's Python. | **Verified Fact.** `Dockerfile` runs `pip install -r requirements.txt` directly. |
| Install command | `pip install -r requirements.txt`, which now includes `httpx==0.28.1` | **Verified Fact.** `Dockerfile`; `requirements.txt` line 7. |
| Test command | `python -m pytest -q`, run in `/app` | **Verified Fact.** `Dockerfile` `CMD` and `WORKDIR`. |
| Run user | `app`, not root | **Verified Fact.** `docker image inspect` printed `user=app`. |
| Environment variables set | `PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`, `PIP_DISABLE_PIP_VERSION_CHECK`, `PIP_NO_CACHE_DIR`. No secret. | **Verified Fact.** `Dockerfile`. |
| Files left out of the image | `.venv`, `.git`, `logs`, caches, `.env`, `node_modules` | **Verified Fact.** `.dockerignore`. |
| Result | `15 passed, 1 warning` | **Verified Fact.** Run H7. |

The setup scripts give the same result on a host: `scripts/bootstrap.ps1` on Windows (run H1) and `scripts/bootstrap.sh` on Linux (run H5). The base image tag `3.11-slim` moves. The `Dockerfile` comment records the digest seen on 2026-10-11. **Assumption.** The choice of Python 3.11 as the standard is Team-Force's to confirm. Owner: Team-Force.

## Lifecycle

This file cites `docs/00-setup/tool-versions.md` and `docs/04-secrets/cleaned-configuration-model.md` (the environment holds the secret names). Stage S04-07 changes the CI column. Stage S09 uses this model in the readiness checklist.
