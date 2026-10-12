# Security scan plan

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half A and Half B |
| Date / version | 2026-10-11, v1.2. v1.1 was updated after S04-05 Half B and S04-06 Half B. v1.2 is the Half B update: it records what each check returned. See "Results of the first run" at the end. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Five checks are named. Each has a command, an output file, what it catches, and what it misses. Both new scanners ran on 2026-10-11 and found issues, which are in the backlog (BL-11, BL-12). Owner: Team-Force. |
| Evidence sources | `tests/security/test_secret_patterns.py`; `semantic-layer/tests/test_semantic_layer.py` (docstring lines 1 to 20); `pyproject.toml`; `policy/opa/access.rego`; `policy/opa/ai_action.rego`; `policy/tests/test_policy_python.py`; `apps/api/services/policy.py`; `docs/06-policy/evidence.md`; `docs/04-secrets/evidence.md`; `docs/05-iac/iac-gap-report.md` IG-13; `pytest policy/tests -q -rs` on 2026-10-11; `docs/07-cicd/pipeline-improvement-plan.md`; pip-audit usage text and exit codes from its README, read through the documentation lookup on 2026-10-11; `pytest -m security --collect-only` on 2026-10-11 |
| Assumptions | `pip-audit` exits 1 when it finds a vulnerability (its README says so). `bandit` also exits 1 when it finds an issue. The machine that runs `pip-audit` can reach the internet. |
| Unresolved issues | **Resolved in v1.2:** `bandit` returned 2 results, and `pip-audit` returned 9 advisories on 3 packages. **Unknown:** whether the 9 advisories reach code the app runs, and whether `pip-audit` can run offline. |
| Residual risks | A clean scan result is true on the day it ran. The advisory database changes daily. A passing run in October says nothing about November. |

## What this file is

This file says which security checks the pipeline runs, what each one finds, and what each one cannot see.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The five checks

| # | Check | Stage | Command | Output file | Pass means |
|---|---|---|---|---|---|
| 1 | Secret-pattern test | 6 | `$PY -m pytest -m security -q --junitxml=evidence/junit-security.xml` | `evidence/junit-security.xml` | The test reports 0 failures. |
| 2 | Dependency scan | 8 | `$PY -m pip_audit -r requirements.txt -r requirements-dev.txt -f json -o evidence/pip-audit.json` | `evidence/pip-audit.json` | Exit code 0. Every package has an empty `vulns` list. |
| 3 | Static scan | 9 | `$PY -m bandit -r apps etl legacy scripts semantic-layer/build.py -f json -o evidence/bandit.json` | `evidence/bandit.json` | Exit code 0, or every finding has a backlog row with an owner. |
| 4 | Policy tests | 5 | `$PY -m pytest policy/tests -q --junitxml=evidence/junit-policy.xml`, then `opa test policy/opa policy/tests --format json > evidence/opa-test.json` | `evidence/junit-policy.xml`, `evidence/opa-test.json` | 0 failures in both. The EXECUTE-needs-approval tests are in the list. With `opa` present, 0 tests are skipped. |
| 5 | Semantic-layer tests | 4 | `$PY -m pytest semantic-layer/tests -q --junitxml=evidence/junit-semantic-layer.xml` | `evidence/junit-semantic-layer.xml` | 0 failures. |

## Results of the first run (v1.2)

**Verified Fact.** Run on 2026-10-11 by `scripts/evidence.ps1` (Windows, Python 3.13.5) and by `scripts/evidence.sh` in a `python:3.11-slim` container (Python 3.11.17). Both runs gave the same findings. Files: `evidence/` and `evidence/linux-py311/`.

| Check | Result | Exit code | Backlog |
|---|---|---|---|
| 1 Secret-pattern test | 1 passed. It also passed with all 13 evidence files present. | 0 | none |
| 2 `pip-audit` 2.10.1 | 68 packages audited, 9 advisories on 3 packages (`pytest`, `python-dotenv`, `starlette`). See `dependency-risk-register.md`. | 1 | BL-11 |
| 3 `bandit` 1.9.4 | 2 results, both LOW severity and HIGH confidence, both in `apps/api/services/policy.py`: `B404` at line 24 (`import subprocess`) and `B603` at line 66 (`subprocess.run` of a list command). | 1 | BL-12 |
| 4 Policy tests | 83 Python tests passed. `opa test`: 30 of 30. Windows: 2 skipped (no `opa` binary). Linux: 0 skipped. | 0 | none |
| 5 Semantic-layer tests | 35 passed. | 0 | none |

**What the bandit results are.** `policy.py` runs `opa eval` through `subprocess.run`. The command is a Python list, not a string. The program is `shutil.which("opa") or "opa"`. The input goes in on stdin as JSON. `shell` is not set. **Verified Fact.** The query argument is one of two fixed strings, passed at `policy.py` lines 125 and 237. **Inference.** No user text reaches the command line, so the risk is low. A person must still rule on it (BL-12). Half B did not add `# nosec` and did not skip the check.

**Worked example.** The test stage exits 0 and the `bandit` stage exits 1. The job ends red. The artifact still holds all 13 files, so a reviewer can open `bandit.json` and see the two results.

## What each check catches and misses

### 1. Secret-pattern test

**Verified Fact.** `tests/security/test_secret_patterns.py` reads every file under the repo root. It reports three kinds of hit:

- A `sk-` prefix followed by a letter or digit (`SK_RE`, line 23).
- `password` or `token` followed by `=` and a value other than `CHANGE_ME`, empty, `${…}`, or `%…` (`STANDALONE_ASSIGN_RE`, lines 24 to 27).
- A line that begins with an upper-case name that holds `PASSWORD`, `TOKEN`, or ends in `KEY`, set to a value other than the placeholder (`NAMED_ASSIGN_RE`, lines 28 to 30, and lines 70 to 76).

| Catches | Misses |
|---|---|
| The old `sk-` example key and a re-added password constant (`docs/04-secrets/evidence.md` shows the fail run). | **Verified Fact.** Every file under a folder named `docs` (`SKIP_DIR_NAMES`, lines 9 to 16). A secret written in Markdown there is not found. |
| A real value in `.env.example`. | **Verified Fact.** Files that are not UTF-8 text, and the extensions `.pyc`, `.pyo`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.woff`, `.woff2`. |
| | **Inference.** Secret formats that do not match the three patterns, such as a cloud access key with no `sk-` prefix, a private key block, or a connection string in a variable that is not named `…KEY`, `…TOKEN`, or `…PASSWORD`. |
| | Git history. The old password and old example key stay in earlier commits (`docs/04-secrets/evidence.md`, residual risks). |

### 2. `pip-audit`

| Catches | Misses |
|---|---|
| A pinned or pulled-in Python package with an advisory in the database the tool queries (the default service is `pypi`). | Anything that is not a Python package: the two GitHub actions, the Python version, Terraform, and `apps/web`. |
| The same check for packages that `requirements.txt` does not name, because the tool resolves them without `--no-deps`. | A vulnerability that has no advisory yet. |
| | Whether the vulnerable code path is used. A package the app never imports still reports a finding (for example `python-dotenv`, DR-05). |
| | **Unknown.** Whether the scan can run offline. The default needs the network. |

### 3. `bandit`

| Catches | Misses |
|---|---|
| Risky Python patterns under `apps`, `etl`, and `legacy`. The new `apps/api/services/policy.py` sits under `apps`, so the policy call site is scanned. Examples of what it flags: a hard-coded password string, use of `subprocess` with `shell=True`, `assert` in non-test code, or a weak hash. | **Verified Fact.** `scripts/`, `semantic-layer/build.py`, and `policy/` are outside the playbook command. v1.2: Half B added `scripts` and `semantic-layer/build.py` to the command. `policy/` is still outside it. |
| | TypeScript and JavaScript under `apps/web`. |
| | Logic mistakes, such as the missing-id call that returns the first row (`tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row`). |
| | Vulnerable packages (check 2). |

### 4. Policy tests

**Verified Fact (v1.1).** `policy/tests/` exists. It holds `test_policy_python.py` (83 tests), `access_test.rego` and `ai_action_test.rego` (30 Rego tests), and 23 fixtures. `python -m pytest policy/tests -q -rs` gave `81 passed, 2 skipped` on 2026-10-11. Both skips say `opa binary not on PATH`. `opa` is still not installed (`docs/06-policy/evidence.md`).

| Catches | Misses |
|---|---|
| A change that lets an AI recommendation reach EXECUTE without an approval id. The tests are `test_execute_is_unreachable_without_an_approval_id` and `test_execute_is_reached_by_exactly_the_all_checks_inputs` (82,944 inputs; exactly 2 give EXECUTE, both with an approval id and an audit row). | **Verified Fact.** The data use, operational safety, and production readiness areas have 8 fixtures that are recorded and not evaluated (`test_other_areas_are_recorded_but_not_evaluated`; `docs/06-policy/evidence.md` unresolved issues). The tests do not decide those areas. |
| A change that lets a role read what the target access matrix denies (`test_every_matrix_row_is_allowed_with_its_own_fields`, `test_changing_any_one_field_of_a_row_denies`). | **Verified Fact.** Three gateway flags are placeholders until S04-09: `forbidden_field_in_prompt` false, `output_schema_ok` true, `timeout_hit` false. The live prompt still holds the whole device row, including `mgmt_ip` and `credential_profile` (defect F12), and the policy cannot see that. |
| The two routes calling the policy: `test_record_route_denies_with_403_and_audit_row` and `test_summarize_route_allows_roles_with_a_row` run through the API and read the audit row. | Rego drift, when `opa` is absent. The Rego tests and the two agreement tests do not run, so only the Python copy is checked (CI-12). |
| Rego and Python disagreeing on 82,959 AI inputs, when `opa` is present. | Any rule that no fixture names. No approval store exists, so an approval id string is checked only for being non-empty, not against a stored yes. |

### 5. Semantic-layer tests

**Verified Fact.** The test file's opening comment lists what the 35 tests fail on. It includes a missing file, a schema error, a glossary that disagrees with the YAML, a `generated/` file that differs from its YAML, an undefined or doubled id, a metric with a target value, and a secret value from `.env.example` or `legacy/reconcile_legacy.py` anywhere in the tree.

| Catches | Misses |
|---|---|
| Drift between the YAML, the glossary, and the generated JSON. A secret value from the two named files, anywhere in the tree, including under `docs/`. | A secret that is not in `.env.example` or `legacy/reconcile_legacy.py`. Code behaviour. |

The last row of the table is why checks 1 and 5 overlap. Check 5 reads `docs/`, and check 1 does not. Check 5 compares against two known values. Check 1 matches patterns.

## What the five checks leave out together

| Gap | Where it goes |
|---|---|
| Node packages and Playwright | BL-04 in `pipeline-improvement-plan.md`. |
| GitHub actions pinned by tag | BL-05. |
| Secrets in Markdown under `docs/` that do not match a value in the two named files | BL-03. Stage S05-13 owns the test. |
| Container image | A `Dockerfile` now exists (S04-05 Half B). No scan reads it or the image. Backlog BL-08. |
| Licence check | Not in the playbook. Unknown. |

## When a scan fails

1. The job fails. Stage 12 still uploads `evidence/`.
2. The finding is added to the backlog in `pipeline-improvement-plan.md` with an id, the file or package, and the owner. The owner is Team-Force until a person is named.
3. The scan stays on. **Prohibited:** `continue-on-error`, `--ignore-vuln`, `# nosec`, a skip list that grows, and a lowered severity filter. A change of that kind needs an ADR under `docs/ADR/` that names who accepted the risk and until when.
4. A fix is a package bump or a code change in its own commit. The next run's `pip-audit.json` or `bandit.json` shows the result.

**Worked example.** `pip-audit` reports one advisory against `starlette` 0.38.6. FastAPI 0.115.0 asks for `starlette<0.39.0` (DR-F4). The stage fails with exit code 1. The backlog gets a row: "starlette advisory; fix needs a FastAPI upgrade; owner Team-Force". The team tests a FastAPI bump in a branch. Until the bump merges, every run stays red and the artifact keeps the proof.

## How often

PROPOSED, owner Team-Force. Checks 1 to 5 run on every push and pull request. Checks 2 and 3 also run once a week, because the advisory database and the tool rules change with no commit.

## Lifecycle

Stage S05-13 adds more tests under `pytest -m security`, which feed check 1's output file. Stage S04-06 Half B creates the policy tests for check 4. Stage S09 cites the five output files from `evidence/`.

Open question for S03: none.
