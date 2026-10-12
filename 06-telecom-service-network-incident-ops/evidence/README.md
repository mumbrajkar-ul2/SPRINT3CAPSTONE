# Evidence folder

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Both runs wrote all 13 script files, and `make evidence` was run once in a Linux container with the same result. The Windows run skipped 2 policy tests because `opa` is not on the PATH. The Linux run skipped none, so every tool has run at least once. |
| Evidence sources | `scripts/evidence.ps1` (Windows run); `scripts/evidence.sh` in a `python:3.11-slim` Docker container (Linux run); `docs/07-cicd/release-evidence-checklist.md` |
| Assumptions | The Docker image `openpolicyagent/opa:1.21.1` gives the same `opa test` result as the binary. The S04-06 run supports this (`docs/06-policy/evidence.md`). |
| Unresolved issues | The workflow has not run on GitHub, so no CI artifact exists yet. The commit id in `run-info.txt` is the last commit. The S04 work is not committed (see "What the commit id means"). |
| Residual risks | These files describe one run on one day. Three stages exit 1 because the scans found real issues. A reader must open `exit-codes.txt` before trusting a green test file. |

## Honesty label

**REAL.** Every file below, except this README, was written by a script run on 2026-10-11. No file was typed by hand, and none was copied from another run. The files in `linux-py311/` come from a second, separate run.

## Which run wrote the files

| | Main set (this folder) | Linux copy (`linux-py311/`) |
|---|---|---|
| Command | `powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1` from the project folder | `bash scripts/evidence.sh all` inside `python:3.11-slim` |
| Time (UTC) | 2026-10-11T20:32:21Z | 2026-10-11T20:41:20Z (the third of 3 `evidence.sh` container runs) |
| Machine | This Windows 10 machine (10.0.26200), local | Docker on the same machine, Linux 6.18 under WSL2 |
| Python | 3.13.5 | 3.11.17 |
| Virtual environment | The existing repo `.venv`. The install stage added the pinned scan tools to it. | A new venv, built by `scripts/bootstrap.sh` |
| `opa` | Not on the PATH. `opa test` ran through the Docker image `openpolicyagent/opa:1.21.1`. | Real binary, version 1.21.1, downloaded in the container with a checksum check |
| Policy tests | 83 run, 2 skipped (`test_opa_and_python_agree_on_access`, `test_opa_and_python_agree_on_every_ai_action_combination`) | 83 run, 0 skipped |
| Commit id in `run-info.txt` | `5f4a6185ab0aeaee8c0e7a20fe8ddc6fe68cd395` | `unknown` (the container has no git) |

A further run through `make evidence` (`make` 4.4.1, installed in a fresh `python:3.11-slim` container) wrote the same 13 files and the same exit codes. `make` printed `Error 1` because the script exits 1 when a stage fails, and `make` itself exited 2. Its files are not kept in this folder.

## What the commit id means

`5f4a6185…` is the last commit on this branch, "After successfully completing S03R round 3", dated 2026-10-10. It was made before the S04 stages. Every S04 change (policy files, scripts, tests, these docs) was in the working folder and not committed when the run happened. So the id names the starting point and does not name the code that ran. Commit first, then run again, to get an id that matches.

## Results

`exit-codes.txt` has one line per stage. Both runs gave the same lines.

| Stage | Exit code | Meaning |
|---|---|---|
| install | 0 | Bootstrap and the pinned tools installed. |
| lint (`ruff`) | **1** | 12 findings in `ruff.json`. Backlog BL-10. |
| tests | 0 | 20 passed. |
| semantic_layer | 0 | 35 passed. |
| opa | 0 | 30 of 30 Rego tests passed (`opa-test.json`). |
| policy | 0 | 83 Python tests passed. 2 skipped on Windows. |
| security | 0 | The secret-pattern test passed, with the other evidence files present. |
| sbom | 0 | CycloneDX 1.6, 22 components. |
| pip_audit | **1** | 9 advisories on 3 packages (`pytest`, `python-dotenv`, `starlette`). Backlog BL-11. |
| bandit | **1** | 2 LOW results in `apps/api/services/policy.py`. Backlog BL-12. |
| checksums | 0 | 7 lines. |

No scan was switched off or narrowed to get a pass. The failing stages stay red until someone fixes the code or records a reviewed exception.

## Files in this folder

| File | What it holds |
|---|---|
| `run-info.txt` | Commit id, UTC time, runner, operating system, Python and `opa` versions. |
| `exit-codes.txt` | One line per stage. |
| `pip-freeze.txt` | 69 installed packages in the Windows venv. The venv existed before the run, so this list also holds packages added by hand earlier. The Linux copy, from a new venv, is the clean list. |
| `ruff.json` | Lint findings, one object each. |
| `junit-tests.xml`, `junit-semantic-layer.xml`, `junit-policy.xml`, `junit-security.xml` | Test results. Read `tests`, `failures`, `errors`, and `skipped` on the first line. |
| `opa-test.json` | The 30 Rego test results. |
| `sbom.cdx.json` | The package list in CycloneDX JSON, made from a venv that holds `requirements.txt` only. It also lists `pytest` and `httpx`, because that file lists them. |
| `pip-audit.json` | The advisory result for every package. |
| `bandit.json` | The static scan result. |
| `source-checksums.txt` | SHA-256 of the legacy scripts, the ETL script, and the policy files. Lowercase hashes, forward-slash paths. |
| `linux-py311/` | The same 13 files from the Linux run. |

The next run of `scripts/evidence.*` deletes every file here except this README, then writes a new set. Copy `linux-py311/` elsewhere first if you want to keep it.

## Known limits of these files

- **Checksums across systems.** On Linux, `sha256sum` hashes the bytes in the file. A Windows checkout with line-ending conversion can give other values for the same text file. The two runs gave the same 7 lines here, so the files had matching bytes on both.
- **Executable bit on Windows mounts.** A Windows folder mounted into Docker marks every file executable. Ruff then reports 23 extra `EXE002` findings. The Linux copy was run with mode 644, which matches what git stores (all 18 tracked `.py` files are 100644).
- **`logs/audit.log`.** The `tests` stage appends rows to this tracked file, so a local run leaves it modified (BL-09).
- **Scan results change daily.** `pip-audit` reads the public advisory list on the day it runs.
- **Not covered.** The web folder has no test or scan, because `apps/web` has no lockfile and its Playwright test cannot pass (IG-12).
- **Docker image tag.** `run-info.txt` records the tag `openpolicyagent/opa:1.21.1`. It does not record the image digest.

## How to run it again

```text
make evidence                                                     # Linux, macOS, or Windows with make
powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1     # Windows
```

Add `-Stage <name>` to the PowerShell command, or `bash scripts/evidence.sh <name>`, to run one stage.

Open question for S03: none. This README uses no new term, id, status word, or field.
