# Scanning checklist

| Field | Value |
|---|---|
| Stage | S05-13 — Automated security validation (Challenge 13), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Five scans from `docs/07-cicd/security-scan-plan.md` are on and write a file each. Two of them exit 1 on real findings (`pip-audit` 9 advisories, `bandit` 2 LOW). Ruff is a sixth stage, not one of the five, and exits 1 on 12 findings. Each red scan has a backlog row with an owner. No scan is switched off. |
| Evidence sources | `docs/07-cicd/security-scan-plan.md`; `docs/07-cicd/evidence.md`; `.github/workflows/ci.yml`; `scripts/evidence.sh`; `scripts/evidence.ps1`; `evidence/exit-codes.txt`; `evidence/run-info.txt`; `evidence/bandit.json`; `evidence/pip-audit.json`; `evidence/ruff.json`; `evidence/junit-security.xml`; `evidence/junit-policy.xml`; `evidence/junit-semantic-layer.xml`; `evidence/opa-test.json`; `pytest -m security -q` and `pytest policy/tests -rs -q` run on 2026-10-11 |
| Assumptions | The scan files in `evidence/` are the last full run of the pipeline: Windows, Python 3.13.5, 2026-10-11, 13:32 to 13:33 local time (`run-info.txt`: `date_utc=2026-10-11T20:32:21Z`). Half A did not rerun `pip-audit`, `bandit`, or `ruff`, because a rerun rewrites the files in `evidence/`. |
| Unresolved issues | The workflow has not run on GitHub (`CI-01`). Whether the 9 advisories reach code the app runs is Unknown. Which ruff rules the team wants is Unknown. |
| Residual risks | A clean scan is true on the day it ran. The advisory database changes daily. `evidence/` was last written before the guardrail tests existed (`SVF-02`), so the security and tests files are out of date. |

## What this file is

This file lists the scans, what each one reads, where its output goes, and what it returned on its last run.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The five scans, plus ruff

| # | Scan | Runs against | Command | Output file | CI stage | Last run |
|---|---|---|---|---|---|---|
| 1 | Secret-pattern test | Every text file under the project folder, except `.git`, `.venv`, `venv`, `docs`, `__pycache__`, `.pytest_cache`, and the test file itself. 164 files today. It reads `logs/audit.log` and `evidence/`. | `pytest -m security -q -p no:cacheprovider --junitxml=evidence/junit-security.xml` (`scripts/evidence.sh security`) | `evidence/junit-security.xml` | 6 | `evidence/junit-security.xml`: 1 test, 0 failures, 0 errors, 0 skipped. Exit 0. Today's run of `pytest -m security`: 52 passed. |
| 2 | Dependency scan (`pip-audit` 2.10.1) | `requirements.txt` and `requirements-dev.txt`. It resolves the packages those files pull in. | `python -m pip_audit -r requirements.txt -r requirements-dev.txt -f json -o evidence/pip-audit.json` | `evidence/pip-audit.json` | 8 | 68 packages audited. 9 advisories on 3 packages. Exit 1. Backlog `BL-11`. |
| 3 | Static scan (`bandit` 1.9.4) | `apps`, `etl`, `legacy`, `scripts`, and `semantic-layer/build.py`. 595 lines of code. | `python -m bandit -r apps etl legacy scripts semantic-layer/build.py -f json -o evidence/bandit.json` | `evidence/bandit.json` | 9 | 2 results, both LOW severity and HIGH confidence. 0 `nosec` marks. 0 skipped tests. Exit 1. Backlog `BL-12`. |
| 4 | Policy tests | `policy/tests/test_policy_python.py` (83 tests), and `policy/tests/access_test.rego` plus `ai_action_test.rego` (30 Rego tests) against `policy/opa/*.rego` and `policy_data.json`. | `python -m pytest policy/tests -q -p no:cacheprovider --junitxml=evidence/junit-policy.xml`, then `opa test policy/opa policy/tests --format json > evidence/opa-test.json` (through the Docker image `openpolicyagent/opa:1.21.1` when `opa` is not on the PATH) | `evidence/junit-policy.xml`, `evidence/opa-test.json` | 5 | Windows: 83 tests, 0 failures, 2 skipped (`opa` missing). `opa test`: 30 tests, 0 failed. Exit 0. Today's run of `pytest policy/tests -rs`: 81 passed, 2 skipped. |
| 5 | Semantic-layer tests | `semantic-layer/tests/test_semantic_layer.py` against the seven YAML files and `generated/`. The test also searches the tree for the two known secret values. | `python -m pytest semantic-layer/tests -q -p no:cacheprovider --junitxml=evidence/junit-semantic-layer.xml` | `evidence/junit-semantic-layer.xml` | 4 | 35 tests, 0 failures, 0 errors, 0 skipped. Exit 0. |
| 6 | Lint (`ruff` 0.17.0). Not one of the five. | `apps etl legacy scripts tests semantic-layer policy` | `python -m ruff check apps etl legacy scripts tests semantic-layer policy --output-format json --output-file evidence/ruff.json` | `evidence/ruff.json` | 2 | 12 findings. Exit 1. Backlog `BL-10`. |

**Verified Fact.** Every "Last run" value comes from the named file in `evidence/` or from the command output on 2026-10-11. `evidence/exit-codes.txt` reads: `install=0`, `lint=1`, `tests=0`, `semantic_layer=0`, `opa=0`, `policy=0`, `security=0`, `sbom=0`, `pip_audit=1`, `bandit=1`, `checksums=0`.

**Why ruff has its own row.** The playbook lists ruff with the five. `security-scan-plan.md` lists five checks and ruff is not among them (finding `SVF-07`). Ruff is pipeline stage 2. Treating it as a sixth row keeps both documents true.

**Worked example.** The `security` stage exits 0, because the 1 test it ran passed. The `bandit` stage exits 1 because `bandit.json` holds 2 results. The job ends red. The reviewer opens `bandit.json`, reads the 2 results, and finds backlog row `BL-12` with an owner.

## What each red scan returned

### `pip-audit`: 9 advisories on 3 packages (`BL-11`)

**Verified Fact.** `evidence/pip-audit.json`.

| Package | Installed | Advisories | Fix versions |
|---|---|---|---|
| `pytest` | 8.3.2 | 1 (`PYSEC-2026-1845`) | 9.0.3 |
| `python-dotenv` | 1.0.1 | 1 (`PYSEC-2026-2270`) | 1.2.2 |
| `starlette` | 0.38.6 | 7 (`PYSEC-2026-161`, `248`, `249`, `1941`, `1943`, `2280`, `2281`) | 0.40.0 up to 1.3.1 |

FastAPI 0.115.0 asks for `starlette<0.39.0`. None of the 7 Starlette fixes can be installed beside it. The file lists some advisories twice. The unique count is 9. **Unknown:** whether the app runs the affected code, because nobody has read the advisory text.

### `bandit`: 2 results (`BL-12`)

**Verified Fact.** `evidence/bandit.json`. Both are in `apps/api/services/policy.py`.

| Test | Line | What it says |
|---|---|---|
| `B404` | 24 | `import subprocess` |
| `B603` | 66 | `subprocess.run` is called with a list command |

**Inference.** The command is `opa eval` with fixed arguments and the input goes in on stdin, so the risk is low. A person must rule on it. Nobody has added `# nosec`.

### `ruff`: 12 findings (`BL-10`)

**Verified Fact.** `evidence/ruff.json`. 6 are `I001` (import order). The other six are `UP045` (`apps/api/main.py`, line 36), `F401` (`apps/api/services/ai_gateway.py`, line 1, unused `os`), `DTZ003` (`apps/api/services/audit.py`, line 9, `datetime.utcnow()`), `C401` (`semantic-layer/tests/test_semantic_layer.py`, line 344), and `SIM103` plus `PIE810` (both in `tests/security/test_secret_patterns.py`, line 51). The last two are in a security test file. `BL-10` already lists them.

## Is any scan switched off?

No. **Verified Fact.**

| Way to switch a scan off | Check | Result |
|---|---|---|
| `continue-on-error` in the workflow | `ci.yml` has none. `tests/ci/test_evidence_contract.py::test_workflow_calls_every_stage_when_it_exists` fails if a step sets it. | None found. |
| `--ignore-vuln` on `pip-audit` | `scripts/evidence.sh` and `evidence.ps1` do not pass it. | None found. |
| `# nosec` or a skip list for `bandit` | `bandit.json` metrics: `nosec` 0, `skipped_tests` 0. | None found. |
| A stage that does not run | Every stage after `prepare` has `if: ${{ !cancelled() }}`. `exit-codes.txt` has a line for every stage. | All 10 stages ran. |
| A test that skips | `junit-policy.xml` shows `skipped="2"` on Windows. See the next section. | Not switched off. 2 tests skip for a missing program. |

The workflow has not run on GitHub. That is Unknown until the first push (`CI-01`).

## The two skipped tests

**Verified Fact.** `test_policy_python.py` line 477 sets `needs_opa = pytest.mark.skipif(shutil.which("opa") is None, ...)`. The two tests that use it are `test_opa_and_python_agree_on_access` and `test_opa_and_python_agree_on_every_ai_action_combination`. Both skip on this machine.

The playbook says BLOCKED when any security test is skipped. Half A does not run the suite as a gate, so the stage status stays CONDITIONAL PASS. Half B must show `skipped="0"` in `evidence/junit-security.xml`.

| Step | Detail |
|---|---|
| Local | Make an `opa` command available on the PATH of the pytest process. Install the binary, or put a small `opa.cmd` on the PATH that calls `openpolicyagent/opa:1.21.1`. The test looks for the name with `shutil.which`. A Docker command typed by hand does not count. |
| CI | `ci.yml` already installs `opa` 1.21.1 with a checksum check. The step has not run on GitHub. |
| Gate | Nothing fails the build when a security test skips (`SB-10`). |

## What the scans leave out

| Gap | Where it goes |
|---|---|
| Secrets in Markdown under `docs/` (the scan skips the folder). A trial run of the same patterns on `docs/` finds 4 hits that are not secrets. | `BL-03` |
| The secret scan reads no file when the repo path holds a folder named `docs`, `venv`, `.venv`, or `.git`. | `SB-18` |
| Node packages and Playwright. | `BL-04` |
| GitHub actions pinned by tag. | `BL-05` |
| The container image and the `Dockerfile` base image. | `BL-08` |
| A model answer that repeats a forbidden value. No scan reads model output. | `SB-04` |

**The `docs/` trial.** **Verified Fact (read-only probe).** The three patterns of `test_secret_patterns.py` run over `docs/` give 4 hits. Three are in `docs/04-secrets/evidence.md` (lines 18, 71, and 130). They name the stand-in text `sk-temp-should-fail`, which the page says is not a live key. The fourth is `docs/12-finops/cost_baseline.py` line 35: a constant named `EDU_UNITS_PER_1K_TOKENS` holds a number, and the name ends in `TOKENS`. None is a secret. A `docs/` scan with the same patterns would fail on these four lines. The fix needs a decision from the owner (see `BL-03`). The fix is not a skip.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| SC-01 | Five scans are on, each with a command, an output file, and a CI stage. | **Verified Fact.** `security-scan-plan.md`; `ci.yml`; `scripts/evidence.sh`. | S09 can cite five output files. | None. | High | None. |
| SC-02 | Two of the five exit 1 on real findings, and ruff is a third red stage. | **Verified Fact.** `evidence/exit-codes.txt`. | The job is red on every push until the findings are fixed or ruled on. | The red job trains people to ignore it. | High | Who rules on `BL-10`, `BL-11`, `BL-12` is Unknown. The owner is Team-Force. |
| SC-03 | `evidence/` was last written before the guardrail tests existed. `junit-security.xml` shows 1 test. The suite has 52 today. | **Verified Fact.** The file timestamp is 13:32 on 2026-10-11. `pytest -m security`: 52 passed. | A reviewer reading the file sees a 1-test suite. | S09 copies a stale file. | High | None. Half B reruns. |
| SC-04 | Two security tests skip on this machine and the stage exits 0. | **Verified Fact.** `junit-policy.xml`: `skipped="2"`. | The Rego copy is not compared with the Python copy here. | Drift goes unseen on a laptop. | High | None. |
| SC-05 | The secret scan has three blind spots: the `docs/` folder, the path-name rule, and no self-test. | **Verified Fact.** `SVF-09`; `docs/` trial above; `NG-04` design. | A secret in Markdown, or a checkout under a folder named `docs`, passes the scan. | Medium for `docs/`. Low for the path rule. | High | The `docs/` fix needs an owner decision. |

## Lifecycle

Half B reruns all stages with `opa` available, then records the real counts. Stage S09 copies the files in `evidence/` into the pack and cites this suite for each security claim.

Open question for S03: none.
