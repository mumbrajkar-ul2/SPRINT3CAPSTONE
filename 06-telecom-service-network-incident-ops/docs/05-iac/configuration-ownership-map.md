# Configuration ownership map

| Field | Value |
|---|---|
| Stage | S04-05 — Infrastructure as code (Challenge 5), Half A |
| Date / version | 2026-10-11, v1.1. v1.1 (S04-05 Half B): added the section "Rows added or changed in Half B". The 33 rows above it keep their Half A text. The 33-of-33 Unknown count is the Half A count. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every config value has a file and a line. Owner is Unknown on 33 of 33 rows. That is more than half. The repo names no owner for any config value. Owner: Team-Force. |
| Evidence sources | `.env.example`; `apps/api/settings.py`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `legacy/reconcile_legacy.py`; `infra/terraform/main.tf`; `Makefile`; `requirements.txt`; `pyproject.toml`; `.github/workflows/ci.yml`; `apps/web/package.json`; `api-examples/http-requests.http`; `data/manifest.json`; `policy/opa/access.rego`; `docs/04-secrets/secrets-inventory.md`; `docs/04-secrets/cleaned-configuration-model.md`; `docs/01-discovery/component-inventory.md`; `docs/00-contract/operating-contract.md` |
| Assumptions | A config value is any named setting, version, path, port, or constant that changes how the program, the tests, or the setup behaves. Owner means the person or team the repo names for that value. |
| Unresolved issues | Owner is Unknown on every row. `docs/01-discovery/component-inventory.md` also lists Unknown on all 55 of its rows. The repo names no team for any file. |
| Residual risks | A later stage can treat Unknown as a team name. Unknown means the repo does not say. The Team-Force name in this file applies to proposed Half B files only (`operating-contract.md` row 10). It does not mean Team-Force owns the old values. |

## What this file is

This file lists every config value in the scoped files. For each value it gives the file, the line, who owns it, and whether it is a secret.

Secret means a password, an API key, a token, or a shared account. The column links to the id in `docs/04-secrets/secrets-inventory.md`. Every secret value in this file is written `<redacted>` or `CHANGE_ME`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Code reads it means a `.py` file reads the value when the program, the test, or the script runs.

## Map

| id | value or name | file and line | what it controls | code reads it | owner | secret |
|---|---|---|---|---|---|---|
| CO-01 | `DATABASE_URL` | `.env.example` line 1 | Database address with the shared user `app_shared` and a password. Placeholder `CHANGE_ME`. | No. **Verified Fact.** | Unknown | Yes. SI-03. |
| CO-02 | `AI_GATEWAY_KEY` | `.env.example` line 2 | A key for a hosted AI call. Placeholder `CHANGE_ME`. | No. `ai_gateway.py` never reads it. | Unknown | Yes. SI-04. |
| CO-03 | `LEGACY_BATCH_PASSWORD` | `.env.example` line 3 | A batch password. Placeholder `CHANGE_ME`. | No. | Unknown | Yes. SI-05. |
| CO-04 | `OT_VENDOR_TOKEN` | `.env.example` line 4 | A shared vendor token. Placeholder `CHANGE_ME`. | No. | Unknown | Yes. SI-06. |
| CO-05 | `LOG_LEVEL=DEBUG` | `.env.example` line 5 | A log level. | No. A search finds no read in any `.py` file. | Unknown | No. |
| CO-06 | `SHARED_DB_PASSWORD` | Read in `legacy/reconcile_legacy.py` through `require(...)`. Not named in `.env.example`. | The password the legacy script needs. The script stops when it is absent or `CHANGE_ME`. | Yes. `reconcile_legacy.py` and the tests. | Unknown | Yes. SI-01. Value `<redacted>`. |
| CO-07 | `SHARED_DB_USER = "app_shared"` | `legacy/reconcile_legacy.py` line 12 | The shared database user name. | The name is assigned. No function uses it. | Unknown | Shared account. SI-02. |
| CO-08 | `PLACEHOLDER = "CHANGE_ME"` | `apps/api/settings.py` line 10 | The text that counts as "not set". | Yes. `settings.require`. | Unknown | No. |
| CO-09 | `filename = "generated-env.txt"` | `infra/terraform/main.tf` line 3 | The text file Terraform would write. | No program reads it. | Unknown | No. |
| CO-10 | `content = "shared_user=app_shared"` | `infra/terraform/main.tf` line 4 | The text Terraform would write. | No program reads it. | Unknown | Shared account. SI-07. |
| CO-11 | `PYTHON ?= python3` | `Makefile` line 1 | The Python name `make` calls. | `make` only. | Unknown | No. |
| CO-12 | Six pinned packages | `requirements.txt` lines 1 to 6 | `fastapi==0.115.0`, `uvicorn==0.30.6`, `pydantic==2.8.2`, `pytest==8.3.2`, `python-dotenv==1.0.1`, `PyYAML==6.0.2`. | `pip` only. | Unknown | No. |
| CO-13 | `httpx` (no pin, not listed) | Absent from `requirements.txt` | Needed by `fastapi.testclient`. Installed by hand at 0.28.1. | Yes, through Starlette. | Unknown | No. |
| CO-14 | `jsonschema` (no pin, not listed) | Absent from `requirements.txt` | Needed by `semantic-layer/build.py` and its tests. Installed by hand at 4.26.0. | Yes, in `build.py`. | Unknown | No. |
| CO-15 | `pythonpath = ["."]` | `pyproject.toml` line 2 | Puts the project folder on the import path for the tests. | `pytest` only. | Unknown | No. |
| CO-16 | `testpaths = ["tests"]` | `pyproject.toml` line 3 | Which folder `pytest -q` collects. `semantic-layer/tests` is outside it. | `pytest` only. | Unknown | No. |
| CO-17 | `markers` entry `security` | `pyproject.toml` lines 4 to 6 | Names the marker for the secret-pattern tests. | `pytest` only. | Unknown | No. |
| CO-18 | `requires-python = ">=3.10"` | `pyproject.toml` line 12 | The lowest Python the project claims. Not tested on 3.10. | Package tools only. | Unknown | No. |
| CO-19 | `python-version: '3.11'` | `.github/workflows/ci.yml` line 9 | The Python CI installs. | `actions/setup-python`. | Unknown | No. |
| CO-20 | `runs-on: ubuntu-latest` | `.github/workflows/ci.yml` line 5 | The CI operating system. | GitHub. | Unknown | No. |
| CO-21 | `actions/checkout@v4`, `actions/setup-python@v5` | `.github/workflows/ci.yml` lines 7 and 8 | The versions of two CI actions. A tag, not a fixed commit. | GitHub. | Unknown | No. |
| CO-22 | Role list `admin`, `operator`, `engineer`, `ai_agent` and default `operator` | `apps/api/main.py` lines 11 and 13 | Which role header values may read a record. | Yes. | Unknown | No. |
| CO-23 | `MODEL_VERSION = "local-sim-v1"` | `apps/api/services/ai_gateway.py` line 3 | The model name in the summary body and the audit row. | Yes. | Unknown | No. |
| CO-24 | `time.sleep(0.01)` | `apps/api/services/ai_gateway.py` line 9 | The fixed wait that stands in for a model call. | Yes. | Unknown | No. |
| CO-25 | `DATA_DIR` | `apps/api/services/domain_service.py` line 4 | The data folder, built from the file's own path. | Yes. | Unknown | No. |
| CO-26 | `LOG` path | `apps/api/services/audit.py` line 5 | The audit log file, `logs/audit.log` in the project folder. | Yes. | Unknown | No. |
| CO-27 | `csv_files` counts and `jsonl_events` | `data/manifest.json` | Expected row counts. `scripts/sanity_check.py` compares against them. | Yes. | Unknown | No. |
| CO-28 | `@playwright/test` `^1.46.0` | `apps/web/package.json` | The browser-test package range. | `npm` only. | Unknown | No. |
| CO-29 | Port 8000 | `api-examples/http-requests.http` lines 2, 5, and 9 | The port in the sample requests. | No. | Unknown | No. |
| CO-30 | Port 8011 | `docs/00-setup/tool-versions.md`, "Commands used" | The port the S00 replay used. | A command line, not a file in the repo. | Unknown | No. |
| CO-31 | Rego rules | `policy/opa/access.rego` lines 3 to 11 | Admin allowed. Operator allowed to read. Default deny. | No test calls OPA. | Unknown | No. |
| CO-32 | `SHARED_DB_PASSWORD=local-test-only` | `tests/characterization/test_current_behaviour.py` line 115 | A test word set for one child process. | Yes, in the test. | Unknown | No. A test word. |
| CO-33 | `PYTHONDONTWRITEBYTECODE=1` | `tests/characterization/test_current_behaviour.py` lines 68 and 114 | Stops child processes writing `.pyc` files. | Yes, in the test. | Unknown | No. |

## Rows added or changed in Half B (v1.1)

Every row here is PROPOSED. Owner: Team-Force (`operating-contract.md` row 10). Naming the owner does not approve the item.

| id | value or name | file and line | what it controls | code reads it | owner | secret |
|---|---|---|---|---|---|---|
| CO-13 (changed) | `httpx==0.28.1` | `requirements.txt` line 7 | Needed by `fastapi.testclient`. Now pinned. | Yes, through Starlette. | PROPOSED. Owner: Team-Force. | No. |
| CO-34 | `PYTHON` variable and `-Python` option | `scripts/bootstrap.sh`, `scripts/bootstrap.ps1` | The Python the bootstrap uses to create `.venv`. Default `python3` on Linux and `python` on Windows. | The scripts. | PROPOSED. Owner: Team-Force. | No. |
| CO-35 | Minimum Python 3.10 check | `scripts/bootstrap.sh`, `scripts/bootstrap.ps1`, step 1 | Stops the setup on a Python older than `requires-python` in `pyproject.toml`. | The scripts. | PROPOSED. Owner: Team-Force. | No. |
| CO-36 | `FROM python:3.11-slim` | `Dockerfile` | The Python and Linux the container uses. | Docker. | PROPOSED. Owner: Team-Force. | No. |
| CO-37 | `variable "log_level"` default `DEBUG`, `variable "api_port"` default `8000`, `variable "output_file"` | `infra/terraform/main.tf` | The two settings written to `generated-env.txt`, and where the file goes. No code reads them. | No. | PROPOSED. Owner: Team-Force. | No. |
| CO-38 | Provider `hashicorp/local` `~> 2.5`, locked at 2.9.1; `required_version >= 1.5.0` | `infra/terraform/main.tf`, `infra/terraform/.terraform.lock.hcl` | The Terraform and provider versions. | Terraform. | PROPOSED. Owner: Team-Force. | No. |
| CO-09, CO-10 (changed) | The old `filename` and `content` rows | `infra/terraform/main.tf` | The file now writes `LOG_LEVEL` and `API_PORT` only. The shared user (SI-07) is gone from the file. | No program reads the file. | Unknown | No longer holds a shared account. |

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| CM-01 | The example file does not list the name the legacy script reads. | **Verified Fact.** `.env.example` holds `LEGACY_BATCH_PASSWORD` on line 3 and no `SHARED_DB_PASSWORD`. `legacy/reconcile_legacy.py` calls `require("SHARED_DB_PASSWORD")`. | A person who copies the names from `.env.example` still gets an error from the script. | A person can set `LEGACY_BATCH_PASSWORD` and expect the script to run. It still stops. | High | Whether `LEGACY_BATCH_PASSWORD` and `SHARED_DB_PASSWORD` mean the same login is Unknown (`secrets-inventory.md` SI-05). |
| CM-02 | No code loads `.env`. | **Verified Fact.** `settings.py` reads `os.environ`. No `.py` file imports `dotenv`. `python-dotenv` is pinned on line 5 of `requirements.txt`. | A file named `.env` has no effect. Values must be exported in the shell. | A reader can think the file is read. | High | None. |
| CM-03 | Five of the six names in the example file are read by no code. | **Verified Fact.** CO-01 to CO-05. A search of the `.py`, `.ts`, `.tf`, `.yml`, and `Makefile` files finds no read. | The file documents names the program does not use. | A later change can start to read a name with no owner for the value. | High | Which names a later stage wires is Unknown. |
| CM-04 | Owner is Unknown on all 33 rows. | **Verified Fact.** No file in the repo names an owner for a config value. `component-inventory.md` has the same result for 55 of 55 files. | No one is named who can approve a change to a pin, a port, or a Python version. | A change to a pin can land without a reviewer who knows the value. | High | `operating-contract.md` row 7 says Mangesh (FDE) accepts each code change. That is a reviewer, not an owner of the value. |
| CM-05 | Three values that affect the result sit outside every config file. | **Verified Fact.** CO-13 and CO-14 are installed by hand. CO-30 is a command line. | A fresh install does not get them. | The result changes between machines (IG-05, IG-06). | High | None. |

## Worked example

Row CO-06. The script `legacy/reconcile_legacy.py` calls `require("SHARED_DB_PASSWORD")` on its first line of work. The function reads the process environment. When the name is set to `local-test-only`, the script prints `legacy reconciled 354`. When the name is absent or equals `CHANGE_ME`, the script stops with an error that names the variable. The repo names no owner for the value, so the owner cell says Unknown. The value is a secret, so the last cell links to SI-01.

## Owner count

33 rows. 33 owner cells say Unknown. 33 divided by 33 is more than one half. This is why the stage status is CONDITIONAL PASS.

Open question for S03: this map needs an owner role for the environment settings (the setup, the Python version, and the pins). The YAML names none. Stage S05R decides whether to add one.

## Lifecycle

This file cites `docs/04-secrets/secrets-inventory.md` for the secret column and `docs/04-secrets/cleaned-configuration-model.md` for the placeholder rule and the loader. Half B adds new config files (`scripts/bootstrap.*`, `Dockerfile`). Each new row will say `Owner: Team-Force` next to the word PROPOSED. Stage S04-07 changes rows CO-19 to CO-21.
