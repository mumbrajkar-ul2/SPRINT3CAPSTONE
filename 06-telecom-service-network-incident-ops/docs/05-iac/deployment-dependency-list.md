# Deployment dependency list

| Field | Value |
|---|---|
| Stage | S04-05 — Infrastructure as code (Challenge 5), Half A |
| Date / version | 2026-10-11, v1.1. v1.1 (S04-05 Half B): `httpx==0.28.1` is now pinned in `requirements.txt` line 7. The rows and findings below are the Half A text. DD-01 is fixed. DD-02 to DD-04 are unchanged. Docker is now used by the `Dockerfile` and its run is in `evidence.md` (H7). |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every row has an observed version and a yes or no for `pytest -q`. The yes and no answers for the three optional packages come from run R6. Python 3.10 and the CI runner packages are Unknown. Owner: Team-Force. |
| Evidence sources | `requirements.txt`; `pyproject.toml`; `.github/workflows/ci.yml`; `apps/web/package.json`; `semantic-layer/README.md`; `docs/00-setup/tool-versions.md`; `pip freeze` of a fresh 3.12.10 venv and of the working `.venv`; `python --version`, `docker --version`, `git --version`, `node --version`, `opa version`, `terraform --version`, `make --version` on 2026-10-11; runs R1 to R6 in `reproducible-setup-guide.md` |
| Assumptions | "Required for tests" means required for `pytest -q` from the project folder, which collects `tests/` only (`pyproject.toml` line 3). Two commands use more: the semantic-layer tests and the Playwright test. |
| Unresolved issues | What the CI runner holds before step one is Unknown. Python 3.10 was not tested. No lock file exists, so the versions of indirect packages come from whatever PyPI serves on the day. |
| Residual risks | A new PyPI release of an indirect package can change a result with no change in the repo. A fresh install today picked the same indirect versions as S00 (see below), so the risk is not seen yet. |

## What this file is

This file lists everything a machine needs to run or test this repo. For each item it gives the version seen, where the pin lives, and whether `pytest -q` needs it.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Python and pip

| Dependency | Version observed | Pin | Required for tests | Evidence |
|---|---|---|---|---|
| Python | 3.13.5 (working `.venv`). 3.12.10 and 3.11.17 (runs R3 and R4). 3.10.12 on WSL, no venv created. | CI: 3.11 (`ci.yml` line 9). `pyproject.toml` line 12: `>=3.10`. No `.python-version`. | Yes | **Verified Fact.** R2, R3, R4, R5. 3.10 is Unknown. |
| `venv` module | Part of Python. Missing on the WSL Ubuntu 22.04.5 install (`python3.10-venv` absent). | None | Yes, to follow the guide | **Verified Fact.** R5. |
| pip | 25.1.1 in the working `.venv`. 24.0 in the 3.11 container. | None | Yes | **Verified Fact.** `tool-versions.md`; R4. |
| PyPI access | Reached on 2026-10-11 from this machine. | None | Yes, for the install | **Verified Fact.** R1 to R4. |

## Packages the repo pins (`requirements.txt`)

| Package | Pin | Observed in fresh install | Required for tests | Needed for | Evidence |
|---|---|---|---|---|---|
| fastapi | `==0.115.0` (line 1) | 0.115.0 | Yes | The app and `TestClient` | **Verified Fact.** `tests/test_api_contract.py` line 1 imports it. |
| uvicorn | `==0.30.6` (line 2) | 0.30.6 | No | Serving the API by hand | **Verified Fact.** R6: `pytest -q` passed with it removed. |
| pydantic | `==2.8.2` (line 3) | 2.8.2 | Yes | FastAPI | **Verified Fact.** Installed with fastapi; imported by it. |
| pytest | `==8.3.2` (line 4) | 8.3.2 | Yes | The test run | **Verified Fact.** |
| python-dotenv | `==1.0.1` (line 5) | 1.0.1 | No | Nothing. No `.py` file imports it. | **Verified Fact.** R6; a search of the `.py` files. |
| PyYAML | `==6.0.2` (line 6) | 6.0.2 | No | `semantic-layer/build.py` | **Verified Fact.** R6; `build.py` imports `yaml`. |

## Packages the repo needs and does not pin

| Package | Version observed | Where it sits today | Required for tests | Needed for | Evidence |
|---|---|---|---|---|---|
| httpx | 0.28.1 | Installed by hand (S00). Absent from `requirements.txt`. | Yes. Without it, 3 files fail to load. | `fastapi.testclient` | **Verified Fact.** R1, R2, R4. |
| jsonschema | 4.26.0 | Installed by hand (S03). Absent from `requirements.txt`. | No | `semantic-layer/build.py` and its 35 tests | **Verified Fact.** `semantic-layer/README.md` line 92. Not run again in this stage. |

## Indirect packages (no pin, no lock file)

**Verified Fact.** `pip freeze` of a fresh Python 3.12.10 venv, after installing `requirements.txt` and `httpx==0.28.1`, gives these indirect versions: starlette 0.38.6, pydantic_core 2.20.1, anyio 4.15.1, annotated-types 0.8.0, typing_extensions 4.16.0, idna 3.20, click 8.5.0, colorama 0.4.6, h11 0.16.0, iniconfig 2.3.1, packaging 26.3, pluggy 1.6.0, certifi 2026.7.22, httpcore 1.0.9.

The working `.venv` holds the same versions. It also holds `jsonschema` 4.26.0, `attrs` 26.1.0, `jsonschema-specifications` 2025.9.1, `referencing` 0.37.0, and `rpds-py` 2026.9.1. Those five came in with `jsonschema`.

**Inference.** The same install a month from now can pick newer indirect versions, because no file fixes them. The cause is `requirements.txt` listing six top-level names and nothing else.

## Tools outside Python

| Dependency | Version observed | Pin | Required for tests | Needed for | Evidence |
|---|---|---|---|---|---|
| git | 2.35.1.windows.2 | None | No | Getting the files | **Verified Fact.** `git --version`. |
| Docker | 28.3.2, build 578ccf6. The daemon answers. | None | No | The Half B container, and run R4 | **Verified Fact.** `docker --version`; R4. |
| make | Absent on Windows. GNU Make 4.3 in WSL. | None | No | `make test`, `make smoke`, `make etl` | **Verified Fact.** `make` not recognised in PowerShell. `make --version` in WSL. |
| OPA | Absent | None | No | `opa test` on `policy/opa/access.rego`. No test calls it today. | **Verified Fact.** `opa version` not recognised; `tool-versions.md`. |
| Node | v22.18.0 | None. `apps/web/package.json` names no `engines` key. | No | The Playwright test | **Verified Fact.** `node --version`. |
| `@playwright/test` | Not installed. `apps/web/node_modules` is absent. | `^1.46.0` in `apps/web/package.json`. No lock file. | No | `tests/playwright/operations.spec.ts` | **Verified Fact.** The file lists. The test has no base URL and no config, so it cannot pass today (IG-12). |
| Terraform | Absent | None. `main.tf` has no `required_version`. | No | Applying `infra/terraform/main.tf` | **Verified Fact.** `terraform --version` not recognised. |
| A GitHub runner | `ubuntu-latest`, Python 3.11 | `ci.yml` lines 5 and 9 | Not applicable | CI | **Verified Fact.** The file. Whether it runs is Unknown (IG-09). |

## What `pytest -q` needs, in one list

Python 3.11, 3.12, or 3.13, with `venv` and `pip`. The packages fastapi, pydantic, pytest, and httpx, plus what they pull in. Internet access to PyPI for the first install. Nothing else.

That list is shorter than `requirements.txt` in one way and longer in another. It leaves out uvicorn, python-dotenv, and PyYAML. It adds httpx.

## Worked example

Take uvicorn. `requirements.txt` line 2 pins it at 0.30.6. A person who only runs tests never starts a server, so run R6 removed it and `pytest -q` still gave `15 passed`. The person who wants to open `/health` in a browser needs it. So uvicorn is needed for serving and not needed for tests. The file does not say that, which is why this column exists.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| DD-01 | The test run needs one package that no file pins. | **Verified Fact.** httpx, in the table above. R1, R2, R4. | A new install fails at collection. | Same as IG-05. | High | None. |
| DD-02 | Indirect packages have no pin and no lock file. | **Verified Fact.** `requirements.txt` has six lines. The `pip freeze` above shows 14 indirect packages. | The tested versions are not recorded in the repo. | A new release of starlette or pydantic_core can change a test result with no repo change. | High for the missing lock. Medium for the risk, which has not happened yet. | Whether the team wants a lock file or a constraints file is Unknown. |
| DD-03 | Three pinned packages are not needed by the tests. | **Verified Fact.** R6. | A reader cannot tell which package each job needs. | Removing a package without checking can break the app run or the semantic-layer build. | High | None. |
| DD-04 | The optional tools are all absent or unused on this machine, and the tests pass without them. | **Verified Fact.** OPA, Terraform, and `@playwright/test` are absent. 15 tests pass. | A passing `pytest -q` says nothing about the Rego file, the Terraform file, or the browser test. | A defect in those three goes unseen until a later stage adds a check. | High | None. |

## Lifecycle

This file cites `docs/00-setup/tool-versions.md` for the machine versions and `docs/04-secrets/cleaned-configuration-model.md` for the rule that setup holds names and not secret values. Half B adds a `Dockerfile` that will use Python 3.11 and the same pins. Stage S04-07 calls the bootstrap from CI. Stage S09 uses this list in the readiness checklist.
