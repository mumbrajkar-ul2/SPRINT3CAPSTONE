# Release evidence checklist

| Field | Value |
|---|---|
| Stage | S04-07 — CI/CD and supply chain (Challenge 7), Half A and Half B |
| Date / version | 2026-10-11, v1.2. v1.0 had 14 rows. v1.1 added `opa-test.json`, so it has 15 rows. v1.2 is the Half B update: the "State today" column is filled from the local run, the junit-tests count is 20, and the two skipped test names are corrected. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS for rows 1 to 14: every file exists under `evidence/`. Row 15 (the workflow artifact) is Unknown until the workflow runs on GitHub. Owner: Team-Force. |
| Evidence sources | `docs/07-cicd/pipeline-improvement-plan.md`; `docs/07-cicd/sbom-recommendation.md`; `docs/07-cicd/security-scan-plan.md`; `docs/06-policy/evidence.md`; `policy/tests/fixtures/pr-01-allow-release-with-all-evidence.json`; `Execution Plan.md` section 3 ("Pipeline evidence" row); `evidence/` (13 files from `scripts/evidence.ps1` on Windows, plus a Linux copy in `evidence/linux-py311/`); `evidence/README.md`; `docs/07-cicd/evidence.md` |
| Assumptions | Every path is under `06-telecom-service-network-incident-ops/`. A file written by a run on one machine gets the honesty label REAL. A file that no run wrote does not exist; the checklist does not accept a hand-written stand-in. Row 1 (`README.md`) is the one file written by hand. |
| Unresolved issues | Whether the workflow runs on GitHub is Unknown until the first push (row 15). No web test report is on the list, because the Playwright test cannot pass today (IG-12). The local Windows run skipped 2 policy tests because `opa` is not on the PATH. The Linux run in `evidence/linux-py311/` skipped none. |
| Residual risks | A release that carries these files shows what the checks said on one day. It does not show that the code is safe. Three of the ten stages exit 1 because the scans found real issues (ruff 12, pip-audit 9 advisories, bandit 2). Each has a backlog row (BL-10 to BL-12). |

## What this file is

This file lists the files a release must carry as proof. A reviewer can open each file and check one thing. Half B writes the files with `make evidence` or `scripts/evidence.ps1`. CI writes the same files and uploads them as the artifact `evidence-<commit id>`.

Honesty label for every file below: REAL when a run wrote it. If a tool could not run, the file is absent, `exit-codes.txt` says so, and `evidence/README.md` writes Unknown with the reason.

## The 15 rows

| # | Path | Written by (stage in `pipeline-improvement-plan.md`) | What a reviewer checks | State today |
|---|---|---|---|---|
| 1 | `evidence/README.md` | By hand in Half B, after the first run | It names the run that wrote the files: commit id, date, machine, Python version, command. It carries the label REAL. | Written by hand. Names the run, the label REAL, and the Linux copy. |
| 2 | `evidence/run-info.txt` | Stage 0 | Commit id, UTC time, Python version, runner name, and the `opa` version or image tag used. These match the README. | Written. Commit `5f4a6185`, 2026-10-11T20:32:21Z, Windows, Python 3.13.5, `opa=not on PATH`, `opa_image=openpolicyagent/opa:1.21.1`. |
| 3 | `evidence/pip-freeze.txt` | Stage 1 | Every package and version on the runner. The seven pinned packages match `requirements.txt`. | Written. 69 lines. The seven pinned packages match `requirements.txt`. |
| 4 | `evidence/ruff.json` | Stage 2 | An empty list, or findings that each have a backlog row. | Written. 12 findings, so `lint=1`. Backlog row BL-10. |
| 5 | `evidence/junit-tests.xml` | Stage 3 | `failures="0"` and `errors="0"`. The test count is 20: the 14 from Half A plus the 6 contract tests in `tests/ci/test_evidence_contract.py`. | Written. 20 tests, 0 failures, 0 errors. |
| 6 | `evidence/junit-semantic-layer.xml` | Stage 4 | `failures="0"` and `errors="0"`. The test count is 35. | Written. 35 tests, 0 failures, 0 errors. |
| 7 | `evidence/junit-policy.xml` | Stage 5 | `failures="0"`. The test count is 83. `skipped="0"` when `opa` was present. If `skipped="2"`, the README says why (CI-12). The two skipped tests are `test_opa_and_python_agree_on_access` and `test_opa_and_python_agree_on_every_ai_action_combination` (`pytest -rs` says `opa binary not on PATH`). The allow, deny, and "EXECUTE needs an approval id" tests run without `opa` and pass. | Written. 83 tests, 0 failures, 2 skipped (Windows, no `opa`). The Linux copy shows `skipped="0"`. |
| 8 | `evidence/opa-test.json` | Stage 5 | Every one of the 30 Rego tests has a pass result. | Written through the Docker image `openpolicyagent/opa:1.21.1`. 30 tests, none failed. |
| 9 | `evidence/junit-security.xml` | Stage 6 | `failures="0"`. Contains `test_repo_has_no_secret_patterns`. This is the secret-pattern result. | Written. 1 test, 0 failures. |
| 10 | `evidence/sbom.cdx.json` | Stage 7 | Parses as JSON. `bomFormat` is `CycloneDX`. Lists `fastapi` 0.115.0, `httpx` 0.28.1, and `starlette`. | Written. CycloneDX 1.6, 22 components. |
| 11 | `evidence/pip-audit.json` | Stage 8 | Every package has `"vulns": []`, or each vulnerability has a backlog row. | Written. 68 packages audited, 9 advisories on 3 packages, so `pip_audit=1`. Backlog row BL-11. |
| 12 | `evidence/bandit.json` | Stage 9 | `"results": []`, or each result has a backlog row. | Written. 2 results (B404, B603, both LOW), so `bandit=1`. Backlog row BL-12. |
| 13 | `evidence/source-checksums.txt` | Stage 10 | Holds SHA-256 values for `legacy/reconcile_legacy.py`, `etl/run_daily_batch.py`, `policy/opa/access.rego`, `policy/opa/ai_action.rego`, and `policy/opa/policy_data.json`. | Written. 7 lines (the two empty `__init__.py` files share one hash). |
| 14 | `evidence/exit-codes.txt` | Each stage appends one line | One line per stage 1 to 10. Every value is 0, or the failure has a backlog row. `opa=not_run` is allowed only with a reason in the README. | Written. 11 lines: `lint=1`, `pip_audit=1`, `bandit=1`, all others 0, and `opa=0`. |
| 15 | `evidence/` as one workflow artifact | Stage 12 (CI only) | The artifact `evidence-<commit id>` opens and holds rows 1 to 14. | Unknown. The workflow is at `.github/workflows/ci.yml` and has not run on GitHub (CI-01). |

## How these files feed the readiness policy

S04-06 wrote a production-readiness policy. Its two fixtures read four inputs (`pr-01-allow-release-with-all-evidence.json` and `pr-02-deny-release-with-missing-evidence.json`). Stage S09 is the stage that evaluates it. This table says which row above is the source of each input.

| Policy input | Source row |
|---|---|
| `policy_tests_result` | Rows 7 and 8 |
| `secret_pattern_test_result` | Row 9 |
| `ci_run_seen` | Row 15 |
| `evidence_sections_missing` | Not an `evidence/` file. Stage S09 fills it from `PRODUCTION_EVIDENCE_PACK.md`. |

**Verified Fact.** In `pr-02`, the deny case, `policy_tests_result` is `not_run` and `ci_run_seen` is `false`. A release that skips stage 5 or never runs CI would look like that fixture.

## Files that are not on the list, and why

| File | Why it is absent |
|---|---|
| A Playwright report | `apps/web` has no lockfile and the test has no base URL (IG-12). The scaffold is not wired (`docs/00-contract/operating-contract.md`). |
| An npm audit report | `package-lock.json` does not exist (BL-04). |
| A container image scan | The `Dockerfile` exists, and CI does not build it in this plan (BL-08). |
| A signed artifact or signed SBOM | Signing is outside this stage. PROPOSED: a later stage signs the artifact. Owner: Team-Force. |

## How a reviewer reads the folder

1. Open `evidence/README.md`. Read the commit id and the label.
2. Open `exit-codes.txt`. Any line that is not `0` points to a backlog row.
3. Open the four `junit-*.xml` files. Read `tests`, `failures`, `errors`, and `skipped` on the first line of each.
4. Open `opa-test.json`. Check that no test failed.
5. Open `pip-audit.json` and `bandit.json`. Search for `"vulns": [` with content, and for `"results": [` with content.
6. Open `sbom.cdx.json`. Look for the seven pinned packages.

**Worked example.** The README says commit `abc1234`, Python 3.11, label REAL. `exit-codes.txt` reads `security=0`, `pip_audit=1`. The reviewer opens `pip-audit.json` and finds one advisory on `starlette`. The backlog has row "starlette advisory" with owner Team-Force. The release carries a known, recorded finding. Without that backlog row, the checklist fails.

## Pass rule for Half B

Half B is PASS when `make evidence` (or `scripts/evidence.ps1`) wrote rows 1 to 14 and this list points at them. It is CONDITIONAL PASS when one tool could not run and the reason is recorded. For example, `opa` is absent on this machine, so row 8 can be missing and row 7 can show `skipped="2"`. Half B tried the Docker image first, and it worked, so row 8 exists. It is BLOCKED when the pipeline writes no evidence file.

## Lifecycle

Stage S04-07 Half B filled the "State today" column on 2026-10-11. Stage S09 copies `evidence/` into `PRODUCTION_EVIDENCE_PACK.md` and into `docs/16-evidence-pack/`, and evaluates the readiness policy.

Open question for S03: none. `docs/06-policy/policy-catalogue.md` already holds the open question about ids for the release checks (PC-06).
