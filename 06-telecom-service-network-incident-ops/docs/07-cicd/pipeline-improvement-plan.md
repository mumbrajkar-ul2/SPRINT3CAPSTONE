# Pipeline improvement plan

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half A and Half B |
| Date / version | 2026-10-11, v1.2. v1.1 was the Half A update after S04-05 Half B and S04-06 Half B. v1.2 is the Half B update. It records what the pipeline did when it ran. See "Revision note" at the end. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Half B ran the pipeline on Windows (Python 3.13.5) and on Linux (Python 3.11.17). Every stage wrote its file. Three stages exit 1 because the scans found real issues: ruff, pip-audit, and bandit. Each has a backlog row (BL-10 to BL-12). Owner: Team-Force. |
| Evidence sources | `.github/workflows/ci.yml`; `requirements.txt`; `pyproject.toml`; `Makefile`; `scripts/bootstrap.ps1`; `scripts/bootstrap.sh`; `Dockerfile`; `.gitignore`; `apps/web/package.json`; `tests/` (6 files); `tests/security/test_secret_patterns.py`; `semantic-layer/tests/test_semantic_layer.py`; `policy/opa/*`; `policy/tests/` (83 Python tests, 30 Rego tests, 23 fixtures); `docs/05-iac/iac-gap-report.md`; `docs/05-iac/reproducible-setup-guide.md`; `docs/05-iac/evidence.md`; `docs/06-policy/evidence.md`; `docs/06-policy/policy-catalogue.md`; `docs/00-setup/tool-versions.md`; `pytest --collect-only` and `pytest policy/tests -q -rs` run in the repo `.venv` on 2026-10-11; `pip index versions` for the four new tools on 2026-10-11; Half B: `scripts/evidence.sh`, `scripts/evidence.ps1`, `requirements-dev.txt`, `evidence/` (both runs), `docs/07-cicd/evidence.md` |
| Assumptions | The target repo for CI is the GitHub remote `https://github.com/mumbrajkar-ul2/SPRINT3CAPSTONE.git` (`git remote -v`). Python 3.11 stays the CI version. The Team-Force team owns every PROPOSED item (`docs/00-contract/operating-contract.md` row 10). |
| Unresolved issues | Whether the workflow runs on GitHub is Unknown until the first push. The lint tool is `ruff` by assumption (decided 2026-10-11, PROPOSED, owner Team-Force). The ruff default rule set in version 0.17.0 is wider than the plan assumed, and it finds 12 issues (BL-10). The workflow is at the repo root (decided and done 2026-10-11). The `opa` binary is absent on this machine, so the Windows run skipped 2 policy tests. The workflow installs OPA 1.21.1 and the Linux run used it (CI-12). **Resolved in Half B:** the 98 original tests pass on Python 3.11.17 (20 + 1 security + 83 in the Linux run, 0 skipped). |
| Residual risks | The files in `evidence/` show one run on one day. The workflow has not run on GitHub, so the Linux evidence comes from a Docker container on this machine. The `opa` download step and the artifact upload have not run in GitHub Actions. |

## What this file is

This file says what the CI pipeline does today and what it should do after Half B. It lists each target stage with its tool, its command, what the stage proves, and the file it writes under `evidence/`.

Half A changed no program file, test, workflow, or Makefile. Half B added `scripts/evidence.sh`, `scripts/evidence.ps1`, `requirements-dev.txt`, a Makefile target, one test file (`tests/ci/test_evidence_contract.py`), the workflow at the repo root, and the `evidence/` folder. Where a section below changed in Half B, it says "v1.2".

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file path or a command output.

All paths are under `06-telecom-service-network-incident-ops/` unless a path starts with the project root.

## CI today

**Verified Fact.** `.github/workflows/ci.yml` has 11 lines and one job named `test`.

| Line | What it does |
|---|---|
| 1 to 2 | Workflow named `workshop-ci`. Runs on `push` and `pull_request`. |
| 5 | Runs on `ubuntu-latest`. |
| 7 | `actions/checkout@v4` |
| 8 to 9 | `actions/setup-python@v5` with Python `3.11` |
| 10 | `pip install -r requirements.txt` |
| 11 | `pytest -q` |

The file has no `permissions` block, no `working-directory`, no cache, no timeout, no artifact upload, and no step that writes a file.

**Verified Fact.** `pytest -q` now collects 98 tests, because `pyproject.toml` line 3 sets `testpaths = ["tests", "policy/tests"]` (S04-06 Half B added the second path). The split is 15 under `tests/` (14 without the `security` marker, 1 with it) and 83 under `policy/tests/`. `python -m pytest policy/tests -q -rs` on 2026-10-11 in the repo `.venv` (Python 3.13.5): `81 passed, 2 skipped`. Both skips say `opa binary not on PATH` (`policy/tests/test_policy_python.py` lines 520 and 530).

**Verified Fact.** `docs/06-policy/evidence.md` records that with a Docker-backed `opa` (OPA 1.21.1) the same suite gave `98 passed` and `opa test` gave `PASS: 30/30`.

**Verified Fact.** `python -m pytest semantic-layer/tests -q` collects 35 tests. Run on 2026-10-11: `35 passed in 0.88s`. CI never runs them.

**Verified Fact.** `python -m pytest -m security --collect-only -q` collects 1 test, `tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns`. The marker is registered in `pyproject.toml` lines 4 to 6.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| CI-01 | The workflow file sits in a folder GitHub does not read for this repo. | **Verified Fact.** `git rev-parse --show-toplevel` prints `C:/MangeshStudy/FDE/Labs/SPRINT3CAPSTONE`. The workflow path is `06-telecom-service-network-incident-ops/.github/workflows/ci.yml`. The folder `SPRINT3CAPSTONE/.github` does not exist. Same finding as IG-09 in `docs/05-iac/iac-gap-report.md`. **Inference.** GitHub runs workflows only from `.github/workflows` at the repo root. | CI gives no signal today. No stage in this plan produces evidence on GitHub until the file moves. | Every later claim "CI passed" would rest on a run that never happened. | High for the path. Medium for the GitHub behaviour (Inference). | **Decided 2026-10-11 by Mangesh (FDE):** the repo is the whole `SPRINT3CAPSTONE/` folder. Half B writes `SPRINT3CAPSTONE/.github/workflows/ci.yml` with `git mv` from the old path, so one copy exists. Every step runs in `06-telecom-service-network-incident-ops` through `defaults.run.working-directory`. The artifact path is `06-telecom-service-network-incident-ops/evidence/`. Whether GitHub runs the file stays Unknown until the first push. |
| CI-02 | CI writes no evidence. | **Verified Fact.** `ci.yml` lines 10 and 11 run `pip install` and `pytest -q`. Neither writes a file. No `upload-artifact` step exists. `evidence/` does not exist (`Test-Path evidence` printed `False`). | A reviewer cannot see what CI checked after the run ends. | A pass in the log is the only proof, and logs expire. | High | None. |
| CI-03 | **Revised in v1.1.** The 35 semantic-layer tests need `jsonschema`, which no requirements file lists. `httpx` is fixed. | **Verified Fact.** `requirements.txt` line 7 is `httpx==0.28.1` (added by S04-05 Half B, `docs/05-iac/evidence.md` "Decision on `requirements.txt`"). `jsonschema` is imported by `semantic-layer/build.py` and `semantic-layer/tests/test_semantic_layer.py` and is in no requirements file. The working `.venv` holds `jsonschema` 4.26.0, installed by hand. **Verified Fact.** The `ci.yml` install line is still `pip install -r requirements.txt`, which now covers the tests under `testpaths`. | Stage 4 (semantic-layer tests) fails at import on a clean runner until `jsonschema` is pinned. The v1.0 failure for `tests/` (3 collection errors) no longer applies. | Low for stages 3 and 5. High for stage 4. | High | `jsonschema` goes in `requirements-dev.txt`, pinned (PROPOSED, owner Team-Force). S04-05 left this pin to S04-07 (`evidence.md` residual risks). |
| CI-04 | **Revised in v1.1.** CI skips the 35 semantic-layer tests. The policy tests now exist and the default run includes them, but 2 of them skip without `opa`. | **Verified Fact.** `pyproject.toml` line 3 now lists `tests` and `policy/tests`. `semantic-layer/tests/test_semantic_layer.py` is still outside it. `policy/tests/` holds `test_policy_python.py`, `access_test.rego`, `ai_action_test.rego`, and 23 fixtures. `python -m pytest policy/tests -q -rs` gave `81 passed, 2 skipped`. | A change to the YAML or to `generated/` can break the build and CI stays green. Policy tests run in a plain `pytest -q`, but the Rego tests do not run at all without `opa`. | Drift between the YAML and its generated JSON goes unseen. The Rego files can drift from the Python copy unseen (CI-12). | High | None for the semantic layer. See CI-12 for `opa`. |
| CI-05 | There is no lint tool and no lint config. | **Verified Fact.** The repo has no `ruff.toml`, `.flake8`, `setup.cfg`, or `[tool.ruff]` table (`pyproject.toml` has only `[tool.pytest.ini_options]` and `[project]`). `apps/web/package.json` sets `"lint": "echo scaffold"`, which checks nothing. | A syntax slip or an unused import reaches `main` unseen. | Low alone. It also means the web folder has no check at all. | High | **Decided 2026-10-11 by Mangesh (FDE):** assume `ruff` is the lint tool for now. It stays PROPOSED with owner Team-Force, and Half B uses the default rules. **v1.2:** ruff 0.17.0 has no config in this repo, so its own default rule set applies. That set is wider than the "unused import or undefined name" checks the plan assumed. It also checks import order (I001), type-hint style (UP045), date and time calls (DTZ003), and style rules (C401, SIM103, PIE810). Half B did not narrow the set, because that would hide findings (BL-10). |
| CI-06 | The secret-pattern test runs inside the general test run and skips the `docs` folder. | **Verified Fact.** `tests/security/test_secret_patterns.py` lines 9 to 16 set `SKIP_DIR_NAMES` to `.git`, `.venv`, `venv`, `docs`, `__pycache__`, `.pytest_cache`. A secret written in a Markdown file under `docs/` is not found. **Verified Fact.** The same file has no skip for `evidence/` or `logs/`, so it will read every file written to `evidence/`. | A secret in `docs/` passes the test. A scanner output file that holds a matching line makes the test fail on its own output. | Medium. The second case is Inference until Half B runs the stages in order. | High for the skip list. Medium for the evidence-folder case. | None. Half B handles the second case by running the security stage before any scan output is written, and by clearing old files from `evidence/` at the start of each run. |
| CI-07 | **Revised in v1.1.** A test run still changes a tracked file, although an ignore file now exists. | **Verified Fact.** `apps/api/services/audit.py` appends to `logs/audit.log`. `.gitignore` (added by S04-05) lists `logs/`, but its own header says a line there affects only files git does not track yet. `git ls-files logs` still prints `logs/audit.log`. **Verified Fact.** The policy route tests use a fixture named `audit_log` that points the log at a temporary file (`policy/tests/test_policy_python.py` lines 59 to 60), so they do not touch `logs/audit.log`. The tests under `tests/` still do. | `make evidence` run on a laptop leaves `logs/audit.log` modified. | A later diff mixes test output with real edits. | High | Whether to run `git rm --cached logs/audit.log` is a Team-Force decision. Half B notes it in `evidence/README.md`. |
| CI-08 | The workflow uses tag versions for actions and has no permission limit. | **Verified Fact.** `ci.yml` lines 7 and 8 use `actions/checkout@v4` and `actions/setup-python@v5`. A tag can move to new code. The file has no `permissions:` key. **Inference.** A workflow with no `permissions:` key gets the default token permission of the repository. | A moved tag changes what runs in CI without a change in this repo. | Medium. | Medium | The default token permission of this repository is Unknown. Half B sets `permissions: contents: read`. |
| CI-09 | **Revised in v1.1.** The Makefile still defaults to `python3` and still has a name with no rule. It gained a `setup` target. | **Verified Fact.** `Makefile` line 1 is `PYTHON ?= python3`. The `.PHONY` line still lists `package`, and no rule has that name. `setup` runs `bash scripts/bootstrap.sh`. `make` is not installed in this Windows shell (`docs/05-iac/evidence.md` H5: `make setup` ran only in a Linux container). | `make evidence` does not run on this machine. The PowerShell script must do the same job. | A script and a Makefile can drift apart. | High | None. Half B adds a test that both write the same file names. `scripts/evidence.ps1` follows the `bootstrap.ps1` pattern (`-Python`, `-SkipTests`, exit code per step). |
| CI-10 | Python 3.11 in CI and 3.13.5 locally can give different results. | **Verified Fact.** `ci.yml` line 9 sets `3.11`. `docs/00-setup/tool-versions.md` lists Python 3.13.5 on this machine. `reproducible-setup-guide.md` runs R2, R3, R4: 15 passed on 3.13.5, 3.12.10, and 3.11.17. Warnings differ: 7 versus 1. | Evidence from a local run says "3.13.5". Evidence from CI says "3.11". | A reader can treat the two as the same run. | High | Half B writes the Python version into `evidence/run-info.txt`. |
| CI-11 | No Node check exists, and none can run. | **Verified Fact.** `apps/web/package.json` has `@playwright/test` `^1.46.0` and `"dependencies": {}`. `apps/web/package-lock.json` does not exist (`iac-gap-report.md` IG-12). `tests/playwright/operations.spec.ts` calls `page.goto('/')` with no base URL, so it cannot pass. | The web folder gets no scan and no test in CI. | A range version pulls a new Playwright on each install. | High | None. This plan leaves the Node stage out of Half B and records it in the backlog below. |
| CI-12 | **New in v1.1.** The `opa` binary is absent here and on the default CI runner, so the Rego tests and two agreement tests do not run. | **Verified Fact.** `docs/06-policy/evidence.md`: normal run `96 passed, 2 skipped`; with Docker-backed OPA 1.21.1, `98 passed`, `opa test` `PASS: 30/30`, and Rego and Python agree on 82,959 AI inputs. The 2 skips are `test_opa_and_python_agree_on_every_ai_action_combination` and `test_opa_and_python_agree_on_access`. **Verified Fact.** The agreement run took about 39 seconds, and the whole suite about 65 seconds through Docker. Same finding as S04-06 status CONDITIONAL PASS ("install the `opa` binary … and rerun"). | A green CI run without `opa` says only that the Python copy of the policy is right. The Rego files, which are the policy of record, go unchecked. | The Rego and the Python copy can drift. The first `opa test` run in S04-06 failed 1 of 30 while the Python run was green. | High | How the runner gets `opa` is Unknown. PROPOSED: install version 1.21.1 in CI, the version the passing run used (BL-07). |
| CI-13 | **New in v1.1.** The new Dockerfile pulls a base image by a tag that moves. | **Verified Fact.** `Dockerfile` line `FROM python:3.11-slim`. Its header comment records the digest seen on 2026-10-11. `.dockerignore` excludes `logs` and `.venv`. The image runs `python -m pytest -q`, which writes no `evidence/` file. | A rebuild next month can pull a different Python 3.11 patch release. | Low for Half B. CI does not build the image in this plan. | High | Whether CI should build the image is Unknown. PROPOSED: not in Half B (BL-08). |

## Target pipeline

One job, `evidence`, on `ubuntu-latest`, Python 3.11. Each stage writes a file under `evidence/`. **Changed in v1.2.** A failed stage does not stop the later stages. Every step after stage 0 has `if: ${{ !cancelled() }}`, so it runs after an earlier failure, and the job still ends red. The upload step has the same condition. This keeps `evidence/` as full as it can be. The v1.1 text said `if: always()` on the upload only, which would have hidden the files from the stages after a failure. No step uses `continue-on-error`, and no scan is switched off. A contract test (`tests/ci/test_evidence_contract.py`) checks the second point.

Commands run from `06-telecom-service-network-incident-ops/`. `$PY` means the Python of the job's virtual environment.

| # | Stage | Tool | Command | What it proves | File it writes |
|---|---|---|---|---|---|
| 0 | Prepare | shell | Remove every file in `evidence/` except `README.md`. Write the commit id, UTC time, Python version, and runner name. | The run starts with no old output. The reader knows which run wrote the files. | `evidence/run-info.txt` |
| 1 | Install | `scripts/bootstrap.sh` (CI), then pip | `SKIP_TESTS=1 bash scripts/bootstrap.sh`, then `$PY -m pip install -r requirements-dev.txt`, then `$PY -m pip freeze`. On Windows, `scripts/bootstrap.ps1 -SkipTests` replaces the first command. | The venv is built the same way as the S04-05 setup guide. The exact package versions on the runner. Bootstrap without the skip flag would also run all 98 tests, so the flag keeps the tests in their own stages. | `evidence/pip-freeze.txt` |
| 2 | Lint | `ruff` (PROPOSED) | `$PY -m ruff check apps etl legacy scripts tests semantic-layer policy --output-format json --output-file evidence/ruff.json` | Python files pass ruff's default rules. On 2026-10-11 the run found 12 issues, so the stage exits 1 (BL-10). | `evidence/ruff.json` |
| 3 | Unit and characterization tests | `pytest` | `$PY -m pytest tests -m "not security" -q --junitxml=evidence/junit-tests.xml` | The 20 non-security tests under `tests/` pass: 14 for the API contract, characterization, and negative access, plus 6 contract tests that check the evidence scripts (v1.2). | `evidence/junit-tests.xml` |
| 4 | Semantic-layer tests | `pytest` | `$PY -m pytest semantic-layer/tests -q --junitxml=evidence/junit-semantic-layer.xml` | The 35 YAML, schema, glossary, and generated-JSON checks pass. | `evidence/junit-semantic-layer.xml` |
| 5 | Policy tests | `pytest`, then `opa test` | `$PY -m pytest policy/tests -q --junitxml=evidence/junit-policy.xml`, then `opa test policy/opa policy/tests --format json > evidence/opa-test.json`. The `opa` binary must be on the PATH first (CI-12, BL-07). | The 83 Python tests pass, including the allow test, the deny test, and the "EXECUTE needs an approval id" tests for "an AI remediation recommendation becomes a change". The 30 Rego tests pass. With `opa` present, the two Rego-versus-Python agreement tests run and the XML shows 0 skipped. | `evidence/junit-policy.xml`, `evidence/opa-test.json` |
| 6 | Security tests | `pytest` | `$PY -m pytest -m security -q --junitxml=evidence/junit-security.xml` | No committed file outside the skip list holds a secret pattern. Stage S05-13 adds more tests under this marker. | `evidence/junit-security.xml` |
| 7 | SBOM | `cyclonedx-py` (package `cyclonedx-bom`) | Create a second venv, install `requirements.txt` into it, then `cyclonedx-py environment --of JSON -o evidence/sbom.cdx.json <second venv python>` | The list of packages the app needs, with versions, in CycloneDX JSON. | `evidence/sbom.cdx.json` |
| 8 | Dependency scan | `pip-audit` | `$PY -m pip_audit -r requirements.txt -r requirements-dev.txt -f json -o evidence/pip-audit.json` | Each package, including packages pulled in by pip, was checked against the public advisory database on the run date. | `evidence/pip-audit.json` |
| 9 | Static scan | `bandit` | `$PY -m bandit -r apps etl legacy scripts semantic-layer/build.py -f json -o evidence/bandit.json` | Python source under the folders was checked for known risky code patterns. v1.2: the command is wider than the three folders in v1.1, and `scripts/` and `semantic-layer/build.py` are included. On 2026-10-11 it found 2 LOW results, so the stage exits 1 (BL-12). | `evidence/bandit.json` |
| 10 | Source checksums | `sha256sum` (CI) or `Get-FileHash` (PowerShell) | Hash `legacy/*.py`, `etl/*.py`, `policy/opa/*.rego`, and `policy/opa/policy_data.json`. | The legacy scripts have a recorded fingerprint for this run (dependency risk register row DR-12). | `evidence/source-checksums.txt` |
| 11 | Stage results | shell | Each stage appends `<stage name>=<exit code>` to the file. | Which stage passed and which failed, in one place. | `evidence/exit-codes.txt` |
| 12 | Evidence upload | `actions/upload-artifact@v4` | Upload the whole `evidence/` folder as `evidence-<commit id>`. Runs with `if: ${{ !cancelled() }}`. | The files outlive the run, including when a stage failed. | The workflow artifact |

Stage 11 is not a step of its own. Every stage from 1 to 10 writes its line, so the file exists even when a stage fails.

**Worked example.** A pull request adds a line `API_TOKEN = "abc123"` to `legacy/reconcile_legacy.py`. Stage 3 passes. Stage 6 fails, because the secret-pattern test finds `API_TOKEN holds a non-placeholder` (`test_secret_patterns.py` lines 70 to 76). Stage 9 still runs and writes `bandit.json` with the same line. The upload step runs. The reviewer opens `evidence-<commit id>` and sees `junit-security.xml` with one failure and `exit-codes.txt` with `security=1`.

### Order rules

1. Stage 0 clears old files first. The secret-pattern test reads every file under `evidence/` (CI-06), so a committed `bandit.json` from an earlier run must not be there when stage 6 runs.
2. Stage 6 runs before stages 7, 8, and 9. Their output files then do not exist when the secret test reads the folder. The files from stages 1 to 5 (`pip-freeze.txt`, `ruff.json`, the three JUnit files, and `opa-test.json`) do exist at that point. **v1.2:** Half B checked it. The secret test passed in the run, with the files from stages 1 to 5 present. It passed again with all 13 files present (`pytest -m security`: 1 passed). Stage 6 did not need to move.
3. Stage 7 uses a second venv. The SBOM then lists what `requirements.txt` needs and does not list `ruff`, `bandit`, `pip-audit`, or `cyclonedx-bom`.
4. Stage 8 audits both requirements files. The audit is wider than the SBOM on purpose: a vulnerable test tool still runs in CI.

### Local equivalents (Half B)

`make evidence` and `scripts/evidence.ps1` run stages 0 to 10 in the same order and write the same 14 file names (see `release-evidence-checklist.md`). Neither can run stage 12. `make evidence` calls `scripts/evidence.sh`, the same file the workflow calls step by step, so one implementation serves both. `scripts/evidence.ps1` is a PowerShell copy for Windows.

On this Windows machine `make` and `opa` are both absent. Docker is present (`docs/05-iac/evidence.md` H7, H8). `scripts/evidence.ps1` therefore runs `opa test` through the Docker image `openpolicyagent/opa` when no binary is on the PATH, and records the image tag in `evidence/run-info.txt`. If neither exists, it writes no `opa-test.json`, and `exit-codes.txt` says `opa=not_run`. **v1.2:** the Docker image worked, so `opa-test.json` exists. The Windows run still skipped 2 policy tests, because the pytest agreement tests look for an `opa` binary on the PATH and do not use Docker.

## Dependencies on other stages

| Needs | From | State today | Effect on Half B |
|---|---|---|---|
| `httpx` pinned | S04-05 Half B | Done. `requirements.txt` line 7. **Verified Fact.** | Stages 3 and 5 can import `fastapi.testclient`. |
| `jsonschema` pinned | This stage | Done in v1.2. `requirements-dev.txt` pins `jsonschema==4.26.0`. **Verified Fact.** | Stage 4 passed on a clean Linux venv (35 passed). |
| `policy/tests/` | S04-06 Half B | Done. 83 Python tests, 30 Rego tests, 23 fixtures. **Verified Fact.** | Stage 5 can run. |
| The `opa` binary | S04-06 evidence ("install the `opa` binary … and rerun") | Absent on this machine. Docker image available. **Verified Fact.** | Windows run: Docker wrote `opa-test.json`, and 2 tests skipped. Linux run: the real binary ran, and 0 tests skipped. |
| `scripts/bootstrap.ps1` and `scripts/bootstrap.sh` | S04-05 Half B | Done. H1 ran `bootstrap.ps1` on Windows. H5 ran `make setup` on Linux. **Verified Fact.** | Stage 1 calls them with the skip flag. |
| A decision on `logs/audit.log` | Team-Force | Open | None for Half B. Recorded in the evidence README. |
| Workflow file location (CI-01) | Mangesh (FDE), 2026-10-11 | Decided: repo root. Done. | `SPRINT3CAPSTONE/.github/workflows/ci.yml` exists (moved with `git mv`, staged, not committed). |
| A fixed lint rule set | Mangesh (FDE), 2026-10-11 | Decided: `ruff`, default rules, for now | Recorded. The default set found 12 issues (BL-10). |

## Backlog (owner Team-Force)

The playbook says a failing scan is recorded in the remediation backlog and not switched off. These items exist before any scan has run. Half B added one row for each scan that returned findings (BL-10 to BL-12) and one row for a test problem it found (BL-13).

| id | Item | Source | State |
|---|---|---|---|
| BL-01 | Move the workflow to `SPRINT3CAPSTONE/.github/workflows/ci.yml` and set the working directory. | CI-01 | Decided 2026-10-11. Done in Half B (`git mv`, staged, not committed). |
| BL-02 | Add `jsonschema` to a pinned `requirements-dev.txt`. (`httpx` is done.) | CI-03 | Done in Half B (`jsonschema==4.26.0`) |
| BL-03 | Make `docs/` readable to the secret-pattern test, or add a second check for Markdown. | CI-06 | Open. Stage S05-13 owns the test. |
| BL-04 | Add `package-lock.json` for `apps/web`, then `npm ci` and `npm audit` as a stage. | CI-11 | Open. Waits on the web scaffold. |
| BL-05 | Pin the two GitHub actions to a commit id. | CI-08 | Open. PROPOSED. |
| BL-06 | Replace `"lint": "echo scaffold"` in `apps/web/package.json` with a real check, or remove the script. | CI-05 | Open |
| BL-07 | Get the `opa` binary onto the CI runner (PROPOSED version 1.21.1) and onto developer machines, so the 30 Rego tests and the 2 agreement tests run. | CI-12 | Done for CI in Half B (the workflow installs 1.21.1 and checks a `sha256`). Open for developer machines. |
| BL-08 | Pin the Dockerfile base image by digest, or record that CI does not build it. | CI-13 | Open. PROPOSED. |
| BL-09 | Decide whether to run `git rm --cached logs/audit.log` so `.gitignore` takes effect. | CI-07 | Open decision. Half B's own runs added 8 lines to `logs/audit.log`. |
| BL-10 | Fix or rule on the 12 ruff findings. 8 have a safe automatic fix in ruff: 6 `I001` (import order) in `apps/api/main.py`, `apps/api/services/ai_gateway.py`, `etl/run_daily_batch.py`, `scripts/sanity_check.py`, `tests/test_api_contract.py`, `tests/test_characterization.py`; `UP045` at `apps/api/main.py:36`; `F401` (unused `os`) at `apps/api/services/ai_gateway.py:1`. 4 need a person: `DTZ003` (`datetime.utcnow()`, no automatic fix) at `apps/api/services/audit.py:9`; `C401` (unsafe fix) at `semantic-layer/tests/test_semantic_layer.py:344`; `SIM103` and `PIE810` (unsafe fixes) at `tests/security/test_secret_patterns.py:51`. Decide the rule set in a `[tool.ruff]` table. | `evidence/ruff.json`, CI-05 | Open. The scan stays on. |
| BL-11 | Upgrade the 3 packages with advisories: `pytest` 8.3.2 (1 advisory, fix 9.0.3), `python-dotenv` 1.0.1 (1, fix 1.2.2), `starlette` 0.38.6 (7, fixes 0.40.0 to 1.3.1). `starlette` is held below 0.39 by FastAPI 0.115.0 (DR-F4), so the fix needs a FastAPI upgrade. | `evidence/pip-audit.json`, `dependency-risk-register.md` | Open. The scan stays on. |
| BL-12 | Rule on the 2 bandit results in `apps/api/services/policy.py`: `B404` (line 24, `import subprocess`) and `B603` (line 66, `subprocess.run` of a fixed list, no shell, input on stdin). Both LOW severity, HIGH confidence. Fix, or record a reviewed exception with a reason. Do not add `# nosec` without a recorded review. | `evidence/bandit.json`, `security-scan-plan.md` | Open. The scan stays on. |
| BL-13 | Make the semantic-layer test `test_every_item_has_a_source_list_of_existing_paths` work without the repo root. It needs `../Project_Intent.md` one folder above the project. A copy of the project folder alone fails 1 of 35. | Linux run, 2026-10-11 | Open. Does not affect CI, which checks out the whole repo. |

Open question for S03: none. This design uses no term, id, status word, persona, resource, scope value, metric, or field that the YAML lacks.

## Link to the production-readiness policy

S04-06 defines a production-readiness policy that reads four inputs (`policy/tests/fixtures/pr-01-allow-release-with-all-evidence.json`). This pipeline writes the source for three of them.

| Policy input | Source file in `evidence/` |
|---|---|
| `policy_tests_result` | `junit-policy.xml` (and `opa-test.json`) |
| `secret_pattern_test_result` | `junit-security.xml` |
| `ci_run_seen` | The workflow artifact `evidence-<commit id>` (stage 12) |
| `evidence_sections_missing` | Not written here. Stage S09 fills it from the evidence pack. |

**Verified Fact.** `docs/06-policy/policy-catalogue.md` row 5 says the readiness area has no running CI today and no YAML rule. That open question belongs to S03. This design adds no term.

## Revision note (v1.1)

v1.0 was written when `policy/tests/`, the bootstrap scripts, `httpx` in `requirements.txt`, `.gitignore`, the Dockerfile, and the corrected `main.tf` did not exist. They exist now. Changes in this version:

- CI-03, CI-04, CI-07, and CI-09 are revised. CI-12 and CI-13 are new.
- Stage 1 calls the bootstrap script. Stage 5 adds `opa test` and one output file, `opa-test.json`. Stage 10 adds `policy_data.json`.
- The dependency table is updated. BL-02 shrinks. BL-07, BL-08, and BL-09 are new.
- The file list grows from 14 to 15 rows (14 files plus the artifact).
- CI-01, CI-02, CI-05, CI-06, CI-08, CI-10, and CI-11 are unchanged. A re-check on 2026-10-11 shows `SPRINT3CAPSTONE/.github` is still absent and `apps/web/package-lock.json` is still absent.

## Revision note (v1.2)

v1.2 is the Half B update. It records what happened when the pipeline ran on 2026-10-11.

- The workflow moved to the repo root and now has one step per stage. Stages after stage 0 run after a failure (`if: ${{ !cancelled() }}`).
- The 14 evidence files exist. Three stages exit 1 for real findings (BL-10 to BL-12).
- The stage 3 test count is 20, because 6 contract tests were added.
- Stage 9 scans `scripts/` and `semantic-layer/build.py` as well.
- Unknown to Resolved: the 98 original tests pass on Python 3.11.17. The `opa` Docker path works.
- One Linux-only note: a Windows mount makes every file executable, and ruff then reports 23 extra `EXE002` findings. Git stores these files as mode 644, so CI does not see them. The run in `evidence/linux-py311/` used mode 644.

## Lifecycle

This plan cites `docs/05-iac/` for the bootstrap scripts and the `httpx` pin, `docs/06-policy/` for the policy tests and the `opa` gap, and `docs/04-secrets/` for the secret-pattern test. Stage S05-13 adds `pytest -m security` tests to stage 6. Stage S09 copies `evidence/` into `PRODUCTION_EVIDENCE_PACK.md`.
