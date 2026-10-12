# CI/CD evidence

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half B |
| Date / version | 2026-10-11, v1.0. v1.1 (S05-13 Half B): the section "Update from S05-13 Half B" below gives the current counts. The counts in the sections after it are as of S04-07 Half B and are kept as the record of that run. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The pipeline wrote all 13 script files and the checklist points at each one. It ran on Windows (`scripts/evidence.ps1`) and on Linux (`scripts/evidence.sh`, and through `make evidence`). Three stages exit 1 because the scans found real issues (ruff 12, pip-audit 9 advisories, bandit 2). Each issue has a backlog row. Whether the workflow runs on GitHub is Unknown. Owner: Team-Force. |
| Evidence sources | `scripts/evidence.sh`; `scripts/evidence.ps1`; `Makefile`; `requirements-dev.txt`; `.github/workflows/ci.yml` (repo root); `tests/ci/test_evidence_contract.py`; `evidence/` (13 files plus `README.md`); `evidence/linux-py311/` (13 files); `docs/07-cicd/release-evidence-checklist.md`; `docs/07-cicd/pipeline-improvement-plan.md` |
| Assumptions | The Docker image `openpolicyagent/opa:1.21.1` gives the same result as the `opa` binary (S04-06 supports this). A Docker container on this machine is a fair stand-in for the `ubuntu-latest` runner, with two differences: Python 3.11.17 versus the runner's 3.11.x, and a Windows folder mount (see run 4 under "Runs, in order"). |
| Unresolved issues | The workflow has not run on GitHub: the `opa` download step, the `sha256sum` check, and `upload-artifact` are unproven there (CI-01). The ruff rule set is the tool default, not a team decision (BL-10). The 9 advisories are not read yet, so whether the app runs the affected code is Unknown (BL-11). |
| Residual risks | Three red stages mean the job fails on every push until the findings are fixed or ruled on. That is intended: no scan was switched off. The S04 work is not committed, so the commit id in `run-info.txt` does not name the code that ran. |

## What this file is

This file records what Half B built, every run, what each stage returned, and what the gate result is. The outputs come from real command runs on 2026-10-11. None was typed by hand.

Commands ran from `06-telecom-service-network-incident-ops/`. Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Update from S05-13 Half B

**Verified Fact.** These numbers come from `scripts\evidence.ps1` (all stages) run on 2026-10-11 on Windows, Python 3.13.5, with `opa` 1.21.1 on the PATH. The files are in `evidence/`. The output is in `docs/13-security-validation/evidence.md`.

| Stage | At S04-07 Half B | Now (S05-13 Half B) | Why it changed |
|---|---|---|---|
| tests (`pytest tests -m "not security"`) | 20 passed | **97 passed, 0 skipped** (`junit-tests.xml`) | S04-08 to S04-12 added tests. S05-13 marks 12 more tests `security`, which moves them to stage 6. S05-13 adds 8 tests to `tests/ci`. |
| semantic_layer | 35 passed | 35 passed | No change. |
| policy (`pytest policy/tests`, `opa test`) | 83 passed, 2 skipped on Windows | **83 passed, 0 skipped.** `opa test`: 30 of 30 | `opa` 1.21.1 is on the PATH. |
| security (`pytest -m security`) | 1 passed | **159 passed, 0 skipped** (`junit-security.xml`) | The marker covers 6 access tests, 83 policy tests, 3 audit-row tests, 3 characterization tests, 51 guardrail tests, 1 secret-pattern test, and 12 new tests. The stage now also fails when any test is skipped (`scripts/check_junit_no_skips.py`). |
| lint (ruff) | 12 findings | **11 findings** (BL-10) | Exit 1. The 2 `ai_gateway.py` findings are no longer in `ruff.json`. `breaker.py` has 1 new finding (`SIM114`). S05-13 added none. |
| pip_audit | 9 advisories | 9 advisories (BL-11) | Exit 1. The file lists 18 entries. 9 are unique. |
| bandit | 2 LOW | 2 LOW (BL-12) | Exit 1. |

Three stages exit 1 (lint, pip_audit, bandit) because the scans found real issues. None is switched off.

**CI.** The workflow already installed `opa` 1.21.1 with a sha256 check. S05-13 Half B leaves that step as it is and renames stage 6 in `ci.yml`. Stage 6 runs `scripts/evidence.sh security`, which now fails on a skipped test. The workflow has not run on GitHub (CI-01 stays open).

**`make security`.** The Makefile has a target `security` that runs `bash scripts/evidence.sh security`. Make is not installed on this Windows machine, so the target was not run here. The Windows command with the same effect is `powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1 -Stage security`. `tests/ci/test_skip_guard.py::test_makefile_has_a_security_target_that_runs_the_security_stage` checks the target text.

## What Half B built

| File | What it does |
|---|---|
| `scripts/evidence.sh` | Runs the 10 stages in order and writes every file under `evidence/`. Each stage appends `<name>=<exit code>` to `exit-codes.txt`. With `all` it keeps going after a failure and exits 1 at the end. With a stage name it runs that stage and exits with its code. |
| `scripts/evidence.ps1` | The same stages and file names for Windows. If `opa` is not on the PATH it runs `opa test` through the Docker image. |
| `Makefile` | New target `evidence`. It runs `bash scripts/evidence.sh all`. |
| `requirements-dev.txt` | Pins `jsonschema==4.26.0`, `ruff==0.17.0`, `bandit==1.9.4`, `pip-audit==2.10.1`, and `cyclonedx-bom==7.5.0`. It stands alone. `requirements.txt` is unchanged, because the bootstrap scripts and the `Dockerfile` install that file alone and then run `pytest`. |
| `.github/workflows/ci.yml` (repo root) | Moved with `git mv` from `06-telecom-service-network-incident-ops/.github/workflows/ci.yml`. The move is staged, not committed. One job, 15 steps: checkout, Python 3.11, install `opa` 1.21.1 with a checksum check, stage 0 to stage 10, upload. Every step after stage 0 has `if: ${{ !cancelled() }}`. `permissions: contents: read`. `defaults.run.working-directory` is the project folder. |
| `tests/ci/test_evidence_contract.py` | 6 tests. Both scripts name the same 13 files and the same stages. The checklist lists every file. The Makefile has the target. `requirements-dev.txt` pins every tool with `==`. The workflow calls every stage, uploads the artifact, and no step sets `continue-on-error`. |
| `evidence/` | 13 files from the Windows run, `README.md`, and `linux-py311/` with 13 files from the Linux run. |

## Decisions made in Half B

| Decision | Reason |
|---|---|
| One shell script (`evidence.sh`) serves both the Makefile and the workflow. | One implementation cannot drift from itself. The PowerShell copy is checked against it by the contract test. |
| Stages after a failure still run (`if: ${{ !cancelled() }}`). | A red stage must not hide the scan files that come after it. The job still ends red. This changes the Half A text (`if: always()` on the upload only). The plan is updated. |
| `prepare` deletes old files in `evidence/`, and the security stage runs after stages 1 to 5. | `tests/security/test_secret_patterns.py` reads every file outside its skip list, and `evidence/` is not on that list. It passed with all 13 files present. |
| The SBOM comes from a second venv that holds `requirements.txt` only. | The SBOM then omits the scan tools. |
| Bandit scans `apps etl legacy scripts semantic-layer/build.py`. | Wider than the playbook's three folders. PROPOSED in Half A. |
| The new findings go to the backlog. No scan is disabled. | Playbook rule. |
| The evidence files are not committed by this stage. | A commit is the user's call. See "What is not done". |

## Commands and real output

### The Windows run (main set)

```text
powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1
```

`evidence/exit-codes.txt` after the run:

```text
install=0
lint=1
tests=0
semantic_layer=0
opa=0
policy=0
security=0
sbom=0
pip_audit=1
bandit=1
checksums=0
```

`evidence/run-info.txt`:

```text
commit=5f4a6185ab0aeaee8c0e7a20fe8ddc6fe68cd395
date_utc=2026-10-11T20:32:21Z
runner=local
os=Microsoft Windows NT 10.0.26200.0
python_for_venv=Python 3.13.5
python_in_venv=Python 3.13.5
opa=not on PATH
opa_image=openpolicyagent/opa:1.21.1
```

### The Linux run

The project folder, `.github/`, and `Project_Intent.md` were copied into a fresh `python:3.11-slim` container. `opa` 1.21.1 was downloaded, and its `sha256` file was checked with `sha256sum -c`, the same two steps as the workflow. Then `bash scripts/evidence.sh all` ran. Run 5 (the one kept) printed:

```text
20 passed, 1 deselected, 1 warning in 1.57s
35 passed in 2.65s
83 passed, 1 warning in 40.17s
1 passed, 103 deselected, 1 warning in 1.81s
== evidence done. Failed stages: 3. See evidence/exit-codes.txt
evidence.sh exit code: 1
```

The `exit-codes.txt` from that run has the same 11 lines as the Windows run. `run-info.txt` has `python_for_venv=Python 3.11.17` and `opa=Version: 1.21.1`.

### The Makefile target

```text
make evidence      (GNU Make 4.4.1, in a python:3.11-slim container)
```

It wrote the same 13 files and the same exit codes. It printed `make: *** [Makefile:22: evidence] Error 1`, because the script exits 1 when a stage fails. `make` itself exited 2.

### Final test counts in the repo `.venv` (Python 3.13.5)

| Command | Result |
|---|---|
| `python -m pytest -q` | `102 passed, 2 skipped` (104 tests: 98 from before, plus the 6 contract tests). The 2 skips say `opa binary not on PATH`. |
| `python -m pytest semantic-layer/tests -q` | `35 passed` |
| `python -m pytest -m security -q` | `1 passed`, with all 13 evidence files and the README present |
| `python -m pytest tests/ci -q` | `6 passed` |

## Runs, in order

| Run | Where | Result | Cause |
|---|---|---|---|
| 1 | Windows | 7 stages failed with pytest exit 4 ("file or directory not found:"). | A bug in my `evidence.ps1`: `--junitxml=(Join-Path ...)` is not expanded in PowerShell. It is not a product finding. The fix is `"--junitxml=$(Join-Path $EV 'name.xml')"`. |
| 2 | Windows | 11 lines. `lint`, `pip_audit`, and `bandit` exit 1. The rest exit 0. | Real scan findings. This is the main set in `evidence/`. |
| 3 | Linux, `evidence.sh` | `semantic_layer` failed 1 of 35 tests. | The test `test_every_item_has_a_source_list_of_existing_paths` needs `../Project_Intent.md`, one folder above the project. My copy left it out. Git tracks the file, so CI has it. Not a product finding. BL-13 records the dependency. |
| 4 | Linux, `evidence.sh` | `semantic_layer` passed. `lint` found 35 issues, not 12. | 23 extra `EXE002` findings ("executable file with no shebang"). A Windows folder mounted into Docker marks every file executable. Git stores all 18 tracked `.py` files as mode 100644, so CI does not see this. Not a product finding. |
| 5 | Linux, `evidence.sh` | 12 findings, same as Windows. Kept as `evidence/linux-py311/`. | Files set to mode 644 before the run. |
| 6 | Linux, `make evidence` | Same 13 files and exit codes. | Proves the Makefile target. |

Runs 3, 4, and 5 are the three `evidence.sh` container runs. Run 6 is the `make` run. The Windows run 2 and the Linux run 5 are the two sets of files kept in `evidence/`.

**Cross-check of Windows and Linux.** Same 12 ruff findings (rule codes and files). Same 9 `pip-audit` advisories. Same 2 bandit results. Same 22 SBOM components. Same 30 Rego results. Same 7 checksum lines. Differences: `pip-audit` audited 68 packages on Windows and 67 on Linux (`colorama` is a Windows-only package), and `junit-policy.xml` shows `skipped="2"` on Windows and `skipped="0"` on Linux.

## What each stage returned

| Stage | Result |
|---|---|
| install | 0. Bootstrap and the pinned tools installed. |
| lint | **1.** 12 `ruff` findings. See below. |
| tests | 0. 20 passed. |
| semantic_layer | 0. 35 passed. |
| policy | 0. 83 Python tests passed (2 skipped on Windows). `opa test`: 30 of 30. |
| security | 0. 1 passed. |
| sbom | 0. CycloneDX 1.6, 22 components. The 7 pinned packages are at their pinned versions. `starlette` 0.38.6 is listed. The scan tools are absent. |
| pip_audit | **1.** 9 advisories on 3 packages. See below. |
| bandit | **1.** 2 LOW results. See below. |
| checksums | 0. 7 lines. |

### ruff: 12 findings (backlog BL-10)

**Verified Fact.** `evidence/ruff.json`.

| Rule | What it checks | Count | Where | Fix state in ruff |
|---|---|---|---|---|
| `I001` | Import order | 6 | `apps/api/main.py`, `apps/api/services/ai_gateway.py`, `etl/run_daily_batch.py`, `scripts/sanity_check.py`, `tests/test_api_contract.py`, `tests/test_characterization.py` | Safe |
| `UP045` | `Optional[X]` written the old way | 1 | `apps/api/main.py:36` | Safe |
| `F401` | Unused import `os` | 1 | `apps/api/services/ai_gateway.py:1` | Safe |
| `DTZ003` | `datetime.utcnow()` has no time zone | 1 | `apps/api/services/audit.py:9` | None |
| `C401` | A generator turned into a set | 1 | `semantic-layer/tests/test_semantic_layer.py:344` | Unsafe |
| `SIM103` | An `if` that returns True or False | 1 | `tests/security/test_secret_patterns.py:51` | Unsafe |
| `PIE810` | Several `startswith` calls that can merge | 1 | `tests/security/test_secret_patterns.py:51` | Unsafe |

The repo has no ruff config (`pyproject.toml` has no `[tool.ruff]` table). Ruff 0.17.0 therefore applies its own default rule set. That set is wider than the "unused import or undefined name" checks that Half A assumed. Half B did not narrow it.

### pip-audit: 9 advisories on 3 packages (backlog BL-11)

**Verified Fact.** `evidence/pip-audit.json`.

| Package | Installed | Advisories | Fix versions |
|---|---|---|---|
| `pytest` | 8.3.2 | 1 (`PYSEC-2026-1845`) | 9.0.3 |
| `python-dotenv` | 1.0.1 | 1 (`PYSEC-2026-2270`) | 1.2.2 |
| `starlette` | 0.38.6 | 7 (`PYSEC-2026-161`, `248`, `249`, `1941`, `1943`, `2280`, `2281`) | 0.40.0 to 1.3.1 |

FastAPI 0.115.0 requires `starlette<0.39.0`, so none of the 7 Starlette fixes can be installed beside it. Risk register row DR-F4 expected this and the scan confirms it. The ids and fix versions come from the tool. Nobody has read the advisory text yet (Unknown).

### bandit: 2 results (backlog BL-12)

**Verified Fact.** `evidence/bandit.json`: both are in `apps/api/services/policy.py`, severity LOW, confidence HIGH.

| Test | Line | What it says |
|---|---|---|
| `B404` | 24 | `import subprocess` |
| `B603` | 66 | `subprocess.run` called with a list command |

The command is `opa eval` with fixed arguments. The query is one of two fixed strings (lines 125 and 237). The user-supplied part goes in on stdin. **Inference.** The risk is low. A person must rule on it, and Half B added no `# nosec`.

## Checklist result

`docs/07-cicd/release-evidence-checklist.md` v1.2 lists 15 rows. Rows 1 to 14 each have a file and a "State today" entry that matches the file. Row 15 (the workflow artifact) is Unknown.

## Gate result

| Gate line | Result |
|---|---|
| PASS: `make evidence` (or the script) wrote every file in the checklist, and the checklist points at them | **Met.** 13 script files, plus the README. The Windows script, `evidence.sh`, and `make evidence` each wrote them. |
| CONDITIONAL PASS: one tool could not run and the reason is recorded | Applied to the Windows run only. `opa` is not on its PATH, so 2 tests skipped. Docker ran `opa test`. The Linux run used the real binary and skipped none. |
| BLOCKED: the pipeline writes no evidence file | Not met. |

**Stage status: PASS.** The gate asks whether the pipeline writes the evidence. It does. Three red scans are findings about the code, and the gate does not ask for them to be green.

## What is not done

- **No commit.** The playbook says "commit". Half B did not run `git commit`. The files are in the working folder. The rename of `ci.yml` is staged with `git mv`. Nothing else is staged.
- **The workflow has not run on GitHub.** Whether GitHub finds `.github/workflows/ci.yml` at the repo root, downloads `opa`, and uploads the artifact is Unknown until the first push.
- **The 12, 9, and 2 findings are not fixed.** They are in the backlog (BL-10 to BL-12). The scans stay on.
- **Actions are not pinned to a commit id** (BL-05). They use tags `@v4` and `@v5`.
- **Node and the web folder have no scan or test** (BL-04, CI-11).
- **No container image scan** (BL-08).

## Unknowns

| Unknown | Why | Who |
|---|---|---|
| Does the workflow run on GitHub, and does the artifact upload? | No push yet. | Team-Force, at the first push |
| Do the `opa` download URL and `sha256` file name still work on the runner? | The URL was tested from a container on this machine, not from GitHub Actions. | Team-Force |
| Does the app run the code the 9 advisories describe? | The advisory text was not read. | Team-Force |
| Which ruff rules does the team want? | The default set was used by assumption. | Team-Force |
| Should `evidence/` be committed, or only uploaded by CI? | A team policy question. | Team-Force |

Open question for S03: none. This stage adds no term, id, status word, persona, resource, scope value, metric, or field to the YAML.

## Lifecycle

Stage S09 copies `evidence/` into `PRODUCTION_EVIDENCE_PACK.md` and `docs/16-evidence-pack/`, and fills the readiness policy inputs from these files (`release-evidence-checklist.md`, "How these files feed the readiness policy").
