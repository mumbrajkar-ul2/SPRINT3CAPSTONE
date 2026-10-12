# Dependency risk register

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half A and Half B |
| Date / version | 2026-10-11, v1.1. Extends the three-row register in `supply-chain/dependency-risk-register.md`. v1.0 was written before S04-05 Half B and S04-06 Half B ran. v1.1 updates DR-08, DR-12, DR-16, DR-F1, and adds DR-21, DR-22, and DR-F7. v1.2 (Half B) adds the `pip-audit` result to DR-01, DR-04, DR-05, DR-07, DR-F4, and the new table "Advisories found on 2026-10-11"; it also records the tool versions that ran (DR-17 to DR-20) and the full checksums (DR-12). |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Every pinned package has a row. Every row says whether a lockfile exists and what happens if the version changes. `pip-audit` ran on 2026-10-11 and found 9 advisories on 3 packages (pytest, python-dotenv, starlette). Each is in the backlog as BL-11. Owner: Team-Force. |
| Evidence sources | `requirements.txt` (7 lines); `apps/web/package.json`; `.github/workflows/ci.yml`; `infra/terraform/main.tf`; `infra/terraform/.terraform.lock.hcl`; `Dockerfile`; `pyproject.toml`; `importlib.metadata` output from the repo `.venv` on 2026-10-11; `pip list --format=freeze` in the same `.venv`; a search of all `.py` files for `import` lines; `Get-FileHash` on two scripts, three Rego or JSON policy files; `docs/05-iac/iac-gap-report.md` IG-05, IG-06, IG-12; `docs/05-iac/evidence.md`; `docs/06-policy/evidence.md`; `docs/00-setup/tool-versions.md`; `pip index versions` on 2026-10-11 |
| Assumptions | The `.venv` versions are what a clean install gives today. Run R4 in `reproducible-setup-guide.md` suggests this for Python 3.11 but did not record transitive versions. |
| Unresolved issues | The advisory list is the public database as of 2026-10-11, so a later scan can differ. Who wrote the legacy scripts and where they came from is Unknown. Which `opa` version a developer or CI runner will use is Unknown (DR-22). |
| Residual risks | `pip-audit` needs the network and reads the public advisory database on the day it runs. A clean result means "no known advisory today". Version numbers for packages that no file pins come from one machine on one day. A clean install on another day can pick another version inside the allowed range. |

## What this file is

This file lists every dependency the repo uses or needs: Python packages, the Node package, the two GitHub actions, the Python version, the legacy scripts, and Terraform. Each row says which file pins it, which version is installed, whether a lockfile exists, and what the risk is if the version changes.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The three original rows

| Original row | Concern then | Where it lives now |
|---|---|---|
| fastapi | Version pinned, no SBOM. | DR-01. The SBOM is planned in `sbom-recommendation.md`. |
| legacy scripts | No provenance. | DR-12. |
| frontend dependencies | Scaffold only. | DR-11. |

## Lockfile state

**Verified Fact.** The repo has no Python lockfile. `Get-ChildItem -Recurse -Include package-lock.json,yarn.lock,pnpm-lock.yaml,requirements*.txt,constraints*.txt,*.lock` finds only `requirements.txt`. That file pins 7 direct packages with `==` (`httpx==0.28.1` was added by S04-05 Half B) and has no `--hash` lines.

**Verified Fact.** `apps/web/package-lock.json` does not exist.

**Verified Fact.** One lockfile exists: `infra/terraform/.terraform.lock.hcl`, written by `terraform init` in S04-05 Half B. It pins the provider `hashicorp/local` at 2.9.1.

**Inference.** A pip install resolves the packages that `requirements.txt` does not pin (rows DR-07 to DR-10) on the day it runs.

## Python packages in `requirements.txt`

| id | Package | Pinned in | Version pinned | Installed (`.venv`, 2026-10-11) | Lockfile? | What uses it | Risk if the version changes |
|---|---|---|---|---|---|---|---|
| DR-01 | `fastapi` | `requirements.txt` line 1 | 0.115.0 | 0.115.0 | No | `apps/api/main.py` (the API). **Verified Fact:** it asks for `starlette<0.39.0,>=0.37.2`. | A new FastAPI changes routing, validation, and the response shape. The tests in `tests/test_api_contract.py` and `tests/access/test_negative_access.py` would catch some of that, not all. A security fix in Starlette 0.39 or later cannot be taken without a new FastAPI. **Verified Fact (v1.2):** `pip-audit` found 7 advisories on the Starlette that FastAPI pulls in (DR-07), so this matters now. |
| DR-02 | `uvicorn` | line 2 | 0.30.6 | 0.30.6 | No | Started from the command line (`uvicorn apps.api.main:app`). **Verified Fact:** no `.py` file imports it. | A new version changes server flags and defaults. No test starts the server, so a break shows up only at run time. |
| DR-03 | `pydantic` | line 3 | 2.8.2 | 2.8.2 | No | Required by FastAPI. **Verified Fact:** no `.py` file imports it directly. It pins `pydantic-core==2.20.1` exactly. | A move to another 2.x changes validation errors. A move to 3 breaks FastAPI 0.115.0 (it asks for `pydantic<3.0.0`). |
| DR-04 | `pytest` | line 4 | 8.3.2 | 8.3.2 | No | The tests. **Verified Fact:** a test tool sits in the file that also lists the app packages. **Verified Fact (v1.2):** `pip-audit` lists 1 advisory, `PYSEC-2026-1845`, fix in 9.0.3. | A new version changes marker and collection rules. The `security` marker is registered in `pyproject.toml` and the run depends on it. |
| DR-05 | `python-dotenv` | line 5 | 1.0.1 | 1.0.1 | No | Nothing. **Verified Fact:** no `.py` file imports `dotenv` (IG-06, run R6). | None for the app. The package adds an unused item to every SBOM and every scan. **Verified Fact (v1.2):** `pip-audit` lists 1 advisory, `PYSEC-2026-2270`, fix in 1.2.2. Nothing imports the package, so the app does not run the affected code. **Inference.** |
| DR-06 | `PyYAML` | line 6 | 6.0.2 | 6.0.2 | No | `semantic-layer/build.py` and `semantic-layer/tests/test_semantic_layer.py`. **Verified Fact:** `apps/`, `etl/`, and `legacy/` do not import it. | A new version can load YAML differently. The 35 semantic-layer tests would show it, but CI does not run them today (CI-04). |

## Python packages that `requirements.txt` does not pin

In v1.1 `httpx` is pinned. Its row stays in this table so its id does not change.

| id | Package | Why it is here | Installed | Lockfile? | Risk if the version changes |
|---|---|---|---|---|---|
| DR-07 | `starlette` | FastAPI needs it. | 0.38.6 | No | **Verified Fact:** FastAPI allows `>=0.37.2,<0.39.0`. A fresh install can pick another version in that range. The `testclient` warning in the test run comes from this package. **Verified Fact (v1.2):** `pip-audit` lists 7 advisories on 0.38.6 (see "Advisories found on 2026-10-11"). |
| DR-08 | `httpx` | `fastapi.testclient.TestClient` needs it. **Verified Fact (v1.1):** pinned at `requirements.txt` line 7 as `httpx==0.28.1`, added by S04-05 Half B. Its own dependencies `certifi`, `httpcore`, `anyio`, and `idna` are not pinned (DR-10). | 0.28.1 | No | A new version can change `TestClient` behaviour. The fix for the old failure (3 collection errors on a clean install) is in place. |
| DR-09 | `jsonschema` | `semantic-layer/build.py` and the semantic-layer tests import it. **Verified Fact:** it is in no requirements file (IG-06). | 4.26.0 | No | Without it, the 35 semantic-layer tests cannot load. Half B pins it. |
| DR-10 | Other packages pulled in by pip | Needed by DR-01 to DR-09. | `annotated-types` 0.8.0, `anyio` 4.15.1, `attrs` 26.1.0, `certifi` 2026.7.22, `click` 8.5.0, `colorama` 0.4.6, `h11` 0.16.0, `httpcore` 1.0.9, `idna` 3.20, `iniconfig` 2.3.1, `jsonschema-specifications` 2025.9.1, `packaging` 26.3, `pluggy` 1.6.0, `pydantic_core` 2.20.1, `referencing` 0.37.0, `rpds-py` 2026.9.1, `typing_extensions` 4.16.0 | No | Each one can change on a new install. Run R1 to R4 in `reproducible-setup-guide.md` passed on three Python versions, so the tests did not show a break. The SBOM records the versions of one run. |

## Other dependencies

| id | Dependency | Pinned in | Version | Lockfile? | Risk if it changes |
|---|---|---|---|---|---|
| DR-11 | `@playwright/test` (the original "frontend dependencies" row) | `apps/web/package.json` `devDependencies` | `^1.46.0`, a range | No. **Verified Fact:** `apps/web/package-lock.json` is absent and `dependencies` is `{}`. | Two installs a week apart can pull two Playwright versions. The test in `tests/playwright/operations.spec.ts` cannot pass today (IG-12), so a change shows no result. No Angular package is listed. |
| DR-12 | Legacy, batch, and policy source files (the original "legacy scripts" row) | Not pinned. Files in the tree. | SHA-256, first 8 characters, on 2026-10-11 (v1.1): `legacy/reconcile_legacy.py` `265A8139`. `etl/run_daily_batch.py` `D004CA45`. `policy/opa/access.rego` `11B0467F` (it was `6094F2C9` in v1.0; S04-06 Half B rewrote it). `policy/opa/ai_action.rego` `9D4170A7`. `policy/opa/policy_data.json` `B0330A92`. **v1.2:** the full values are in `evidence/source-checksums.txt` (lowercase, 7 lines). The Windows run and the Linux run wrote the same 7 lines. | No | **Verified Fact.** `git status` shows `legacy/reconcile_legacy.py` as modified, so the hash is of the working file and not of the commit. **Unknown.** Who wrote the scripts and where they came from. Any edit changes behaviour that the characterization tests cover only in part. |
| DR-13 | GitHub action `actions/checkout` | `.github/workflows/ci.yml` line 7 | `v4`, a tag | No | A tag can move. **Inference.** The code that runs in CI can change with no commit in this repo. |
| DR-14 | GitHub action `actions/setup-python` | `ci.yml` line 8 | `v5`, a tag | No | Same as DR-13. |
| DR-15 | Python itself | `ci.yml` line 9 (`3.11`); `pyproject.toml` line 12 (`requires-python = ">=3.10"`) | CI 3.11. This machine 3.13.5. | No | **Verified Fact.** 3.11.17, 3.12.10, and 3.13.5 each gave 15 passed. Python 3.10 was not run (R5), so `>=3.10` has no run behind it. |
| DR-16 | Terraform and its provider | `infra/terraform/main.tf`; `infra/terraform/.terraform.lock.hcl` | **Verified Fact (v1.1):** `required_version = ">= 1.5.0"`, provider `hashicorp/local` `~> 2.5`, lock file pins 2.9.1. `terraform` is still not installed on this machine. S04-05 H8 validated and applied the file with Terraform v1.9.8 in a container. | Yes, for the provider | The CLI version has a floor and no ceiling. A new major Terraform can change the file's meaning. The provider is locked, so it does not move. |
| DR-21 | Docker base image `python:3.11-slim` | `Dockerfile` line `FROM python:3.11-slim` | Tag `3.11-slim`. The header comment records the digest seen on 2026-10-11: `sha256:e88e9763…f6ce`. | No | **Verified Fact.** The tag moves. A rebuild can pull a new Python 3.11 patch and a new Debian layer. CI does not build this image in this plan (BL-08). |
| DR-22 | `opa` binary (policy engine) | Not pinned. Not installed here. | **Verified Fact.** `docs/06-policy/evidence.md` ran OPA 1.21.1 through the Docker image `openpolicyagent/opa:latest`, a tag that moves. | No | Rego syntax and the `opa test` result can change between OPA versions. Without the binary, 2 tests skip and the 30 Rego tests do not run (CI-12). PROPOSED: pin 1.21.1 in CI. Owner: Team-Force. |

## Tools this stage adds (Half B pins them in `requirements-dev.txt`)

**Verified Fact.** `pip index versions <tool>` on 2026-10-11 listed these as the newest on the index. **v1.2, Verified Fact:** all four are pinned in `requirements-dev.txt` and ran on Windows (Python 3.13.5) and on Linux (Python 3.11.17). `evidence/pip-freeze.txt` records the installed versions.

| id | Tool | Newest on the index | Job |
|---|---|---|---|
| DR-17 | `pip-audit` | 2.10.1 | Dependency scan (stage 8) |
| DR-18 | `bandit` | 1.9.4 | Static scan (stage 9) |
| DR-19 | `cyclonedx-bom` (command `cyclonedx-py`) | 7.5.0 | SBOM (stage 7) |
| DR-20 | `ruff` (PROPOSED lint tool) | 0.17.0 | Lint (stage 2) |

`jsonschema==4.26.0` is pinned in the same file (DR-09). Half B pinned each tool to the version it ran with and recorded that version in `evidence/pip-freeze.txt`.

## Advisories found on 2026-10-11

**Verified Fact.** `evidence/pip-audit.json`: `pip-audit 2.10.1` audited 68 packages from `requirements.txt` and `requirements-dev.txt` in the Windows run (67 in the Linux run, where `colorama` is absent). It found 9 advisories on 3 packages. Both runs found the same 9. No package was skipped.

| Package | Installed | Advisory ids | Fix versions | Backlog |
|---|---|---|---|---|
| `pytest` | 8.3.2 | `PYSEC-2026-1845` | 9.0.3 | BL-11 |
| `python-dotenv` | 1.0.1 | `PYSEC-2026-2270` | 1.2.2 | BL-11 |
| `starlette` | 0.38.6 | `PYSEC-2026-161`, `PYSEC-2026-248`, `PYSEC-2026-249`, `PYSEC-2026-1941`, `PYSEC-2026-1943`, `PYSEC-2026-2280`, `PYSEC-2026-2281` | 1.0.1, 1.3.0, 1.3.1, 0.47.2, 0.40.0, 1.1.0, 1.1.0 (in id order) | BL-11 |

**Worked example.** The advisory `PYSEC-2026-1943` on `starlette` has fix version 0.40.0. `fastapi==0.115.0` allows only `starlette<0.39.0`. So pip cannot install 0.40.0 next to this FastAPI. The team must move FastAPI first.

**Unknown.** What each advisory says and whether the app runs the affected code. `pip-audit` lists the ids and fix versions. Reading the advisory text is a Team-Force task.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| DR-F1 | Only 7 of the 26 Python packages in the `.venv` are pinned. (v1.0 said 6; `httpx` is now pinned.) | **Verified Fact.** `requirements.txt` has 7 lines. `pip list --format=freeze` in the `.venv` shows 26 installed packages besides `pip`. Rows DR-01 to DR-10 cover all 26: 7 pinned, `starlette`, `jsonschema`, and 17 others. | Two clean installs on different days can differ. | A version change that breaks a test looks like a code change. | High | Whether the team wants a full lockfile (`pip-compile` or `pip freeze`) is Unknown. PROPOSED: Half B saves `pip freeze` as evidence and leaves the lockfile decision to Team-Force. |
| DR-F2 | Two pinned packages are not used by the app. | **Verified Fact.** DR-05 is imported nowhere. DR-06 is used only by the semantic layer. | Extra packages widen every scan and every SBOM. | Low. | High | S04-05 Half B left both in `requirements.txt` and handed the question to S04-07 (`docs/05-iac/evidence.md`, "Decision on `requirements.txt`"). PROPOSED for Half B: leave them. `scripts/bootstrap.*` and the `Dockerfile` install `requirements.txt` alone and then run `pytest`, so moving `pytest` would break both. Half B creates `requirements-dev.txt` for new tools only. Owner: Team-Force. |
| DR-F3 | A test tool and the app packages share one file. | **Verified Fact.** `requirements.txt` line 4 lists `pytest`. | The SBOM for `requirements.txt` includes `pytest`. | Low. | High | Same as DR-F2. |
| DR-F4 | FastAPI 0.115.0 caps Starlette below 0.39.0. | **Verified Fact.** `importlib.metadata.requires("fastapi")` prints `starlette<0.39.0,>=0.37.2`. | A fix released in a newer Starlette needs a FastAPI upgrade first. | **Verified Fact (v1.2).** `pip-audit` lists 7 advisories on Starlette 0.38.6. Their fix versions are 0.40.0 to 1.3.1. FastAPI 0.115.0 blocks all of them. | High. | Which FastAPI version allows a fixed Starlette is Unknown here. BL-11 tracks it. Owner: Team-Force. |
| DR-F5 | Legacy scripts have a checksum command but no recorded owner or source. | **Verified Fact.** `Get-FileHash` ran on the two scripts on 2026-10-11. The repo has no file that names an author or source for `legacy/`. | A change to a script cannot be matched to a person or a reason. | Medium. | High | Owner and source are Unknown. PROPOSED owner for the metadata: Team-Force. |
| DR-F6 | Two GitHub actions run from moving tags. | **Verified Fact.** DR-13 and DR-14. | See DR-13. | Medium. | Medium | Pin to a commit id (BL-05). |
| DR-F7 | **New in v1.1.** Two tools that S04-05 and S04-06 used run from moving Docker tags, and one policy tool is not installed. | **Verified Fact.** DR-21 (`python:3.11-slim`), DR-22 (`openpolicyagent/opa:latest`), and `hashicorp/terraform:1.9` in `docs/05-iac/evidence.md` H8. | The evidence that S04-05 and S04-06 recorded came from images that can change. | Low to Medium. | High | PROPOSED: Half B records the digest or version of every image it uses in `evidence/run-info.txt`. |

## Lifecycle

The older file `supply-chain/dependency-risk-register.md` keeps its three rows and gains a pointer to this file. Stage S04-05 Half B pinned `httpx` (DR-08). Stage S04-07 Half B pins `jsonschema` (DR-09). Stage S09 copies this register into the evidence pack.
