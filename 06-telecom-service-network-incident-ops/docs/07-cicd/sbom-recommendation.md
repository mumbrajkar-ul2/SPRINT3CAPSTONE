# SBOM recommendation

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half A and Half B |
| Date / version | 2026-10-11, v1.2. v1.1 was updated after S04-05 Half B (`httpx` pinned, Dockerfile added). v1.2 is the Half B update: the command ran and the checks below passed. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The tool, the command, the output path, and the run rate are named. The command ran on Windows and on Linux on 2026-10-11 and wrote `evidence/sbom.cdx.json`. Owner: Team-Force. |
| Evidence sources | `requirements.txt` (7 lines); `Dockerfile`; `docs/05-iac/evidence.md`; `docs/07-cicd/dependency-risk-register.md`; `docs/07-cicd/pipeline-improvement-plan.md`; `pip index versions cyclonedx-bom pip-audit` on 2026-10-11; the pip-audit usage text from its own README, read through the documentation lookup on 2026-10-11 |
| Assumptions | An SBOM in CycloneDX JSON meets the "SBOM" line in the playbook. The exact flag names of `cyclonedx-py` match the version Half B pins. |
| Unresolved issues | **Resolved in v1.2:** `cyclonedx-py environment --of JSON -o <file> <python>` is the working command in `cyclonedx-bom` 7.5.0. It writes CycloneDX 1.6 by default. Which CycloneDX schema version the team wants is still Unknown. |
| Residual risks | An SBOM lists packages. It does not say whether any package is vulnerable (that is `pip-audit`, stage 8). An SBOM made from a requirements file alone misses the packages pip pulls in. |

## What an SBOM is here

An SBOM (software bill of materials) is a file that lists every package the app needs, with its version. This repo has none today (original register row 1, `supply-chain/dependency-risk-register.md`).

A reviewer uses it to answer two questions: which package versions did this release contain, and does a newly announced advisory name any of them.

## Recommendation

| Item | Recommendation | Label |
|---|---|---|
| Format | CycloneDX, JSON. | Playbook requirement. |
| Tool | `cyclonedx-py`, installed from the package `cyclonedx-bom`. Newest on the index on 2026-10-11: 7.5.0. | **Verified Fact** for the version number. **Unknown** for the flags. |
| Source | The packages installed in a venv built from `requirements.txt` only. | Recommendation. |
| Command | `cyclonedx-py environment --of JSON -o evidence/sbom.cdx.json <path to the venv python>` | **Assumption.** The tool's own `--help` decides the final spelling. |
| Output path | `evidence/sbom.cdx.json` | Recommendation. Matches `Execution Plan.md` section 3, "Pipeline evidence". |
| Fallback | `pip-audit -r requirements.txt -f cyclonedx-json -o evidence/sbom.cdx.json` | **Verified Fact** that `pip-audit` lists `cyclonedx-json` as an output format (its usage text). This output also carries vulnerability data, so it is not the same file. |

### Why read the environment and not the file

`requirements.txt` has 7 lines. The working `.venv` holds 26 packages besides `pip` (`dependency-risk-register.md`, DR-F1). `cyclonedx-py requirements requirements.txt` lists what the file names. The environment run lists what pip installed, including packages the file does not name, such as `starlette` and `pydantic_core`. The second list is the one a vulnerability advisory is matched against.

### Why a second venv

The job installs the scan tools and test tools into its main venv. An SBOM taken from that venv would list `ruff`, `bandit`, `pip-audit`, and `cyclonedx-bom`, which the app does not use. Stage 7 builds a second venv from `requirements.txt` alone and reads that one.

`requirements.txt` still lists `pytest` (DR-04), `httpx` (DR-08), `python-dotenv`, and `PyYAML`, so they all appear in the SBOM. **Verified Fact.** The bootstrap scripts and the `Dockerfile` install `requirements.txt` alone and then run the tests, so `pytest` and `httpx` must stay in that file. The SBOM therefore describes "what the repo needs to build and test", and the README in `evidence/` says so. **Inference.**

## How often

PROPOSED, owner Team-Force. No number here is a requirement.

| When | Why |
|---|---|
| Every CI run on `push` and `pull_request` | The file is small and the run is fast. Each run's artifact then pairs a commit with its package list. **Inference** for "fast", until Half B times it. |
| Every release, kept in the evidence pack | S09 copies `evidence/` into `PRODUCTION_EVIDENCE_PACK.md`. |
| Once a week from a scheduled workflow | A new advisory can name a package that did not change. A weekly run of stages 7 and 8 finds it without a commit. |

## What the SBOM leaves out

| Gap | State |
|---|---|
| Node packages in `apps/web` | `package-lock.json` does not exist, so no npm SBOM can be made. Backlog BL-04. |
| Python itself and the operating system image | The CI runner image is not in the file. The new `Dockerfile` (`python:3.11-slim`) is a container image, and `cyclonedx-py environment` does not list its operating system layer. Register row DR-21. |
| The legacy scripts | They are files, not packages. Their SHA-256 values go to `evidence/source-checksums.txt` (register row DR-12). |
| GitHub actions | Not in a Python SBOM. They are rows DR-13 and DR-14 in the register. |
| Vulnerabilities | Stage 8 (`pip-audit`). |

## How Half B checks the file

1. The file exists at `evidence/sbom.cdx.json` and parses as JSON.
2. `bomFormat` equals `CycloneDX`, and `specVersion` is recorded in `evidence/README.md`.
3. The component list holds each of the seven pinned packages at the pinned version (for example `fastapi` 0.115.0 and `httpx` 0.28.1).
4. The component list holds `starlette`, which `requirements.txt` does not name. This proves the tool read the environment.

If the tool cannot run on this machine, Half B writes Unknown with the reason and the stage result is CONDITIONAL PASS.

## Result of the first run (v1.2)

**Verified Fact.** Run on 2026-10-11, on Windows (Python 3.13.5) and in a Linux container (Python 3.11.17). Both runs wrote the same 22 components.

| Check | Result |
|---|---|
| File parses as JSON, `bomFormat` is `CycloneDX` | Yes. `specVersion` is 1.6. |
| Each of the seven pinned packages is at its pinned version | Yes: `fastapi` 0.115.0, `uvicorn` 0.30.6, `pydantic` 2.8.2, `pytest` 8.3.2, `python-dotenv` 1.0.1, `PyYAML` 6.0.2, `httpx` 0.28.1. |
| `starlette` is listed although `requirements.txt` does not name it | Yes, version 0.38.6. |
| `ruff`, `bandit`, `pip-audit`, `cyclonedx-bom` are absent | Yes. The second venv worked. |

The "Fallback" row above was not needed.

## Lifecycle

Stage S04-07 Half B wrote `evidence/sbom.cdx.json`. Stage S09 cites it as supply-chain evidence. Row DR-01 of the dependency risk register points here.
