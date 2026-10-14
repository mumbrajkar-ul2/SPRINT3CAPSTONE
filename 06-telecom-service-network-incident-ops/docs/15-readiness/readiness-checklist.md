# Readiness checklist

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 15, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. Two of 12 control areas are ready for the lab demo and 10 are partial. No area is ready for production. Ten of 11 items in `../Project_Intent.md` section 6.3 are ticked. One is marked not ready (the defence answers, written in S10). |
| Evidence sources | `../playbook/STATUS.md`; `evidence/run-info.txt`; `evidence/exit-codes.txt`; `evidence/junit-tests.xml`; `evidence/junit-policy.xml`; `evidence/junit-security.xml`; `evidence/junit-semantic-layer.xml`; `docs/16-evidence-pack/ci-run-38521594275.txt`; the evidence file of each stage named in the table; `docs/demo/evidence.md`; `docs/model-comparison/app-comparison.md`; `docs/prd/Risk Management.md`; `docs/00-contract/operating-contract.md`; `../Project_Intent.md` section 6.3. |
| Assumptions | (1) "The lab demo" means the governed app in `apps/api/` run on this machine with synthetic data, the stand-in model `local-sim-v1`, one server process, and a person who types the role word. (2) "Production" means a live service with real users, a real model and more than one server process. (3) The stage status in column 5 is copied from `../playbook/STATUS.md`. A stage with no row there is named in the table. |
| Unresolved issues | `../playbook/STATUS.md` has no row for S05-14, S06 or S06R. The stage evidence files give those results. Owners of accepted risks are PROPOSED where the packet names none (`docs/15-readiness/risk-owner-table.md`). |
| Residual risks | A "ready" verdict means a passing test or a recorded run proves the control for the inputs the test uses. It does not prove that no other input gets through. All test counts below are REAL and come from one Windows machine, plus one GitHub run. |

Claim labels: **Verified Fact** (names a file or a test), **Inference**, **Assumption**, **Unknown**. Paths are relative to the project folder (06-telecom-service-network-incident-ops) unless they start with `../`.

## How to read the verdicts

| Word | What it means in this file |
|---|---|
| ready | A test or a recorded run proves the control for what this packet claims. The open limits are listed in the last column and each has an owner row in `docs/15-readiness/residual-risk-register.md`. |
| partial | The control works for part of what the packet claims. The last column says which part is missing. |
| not ready | The control is absent, or no evidence shows it works. |

Two columns give a verdict. "For the lab demo" judges the claims in the Assumptions row. "For production" judges a live service.

## 1. Control areas

| Control area | For the lab demo | For production | Proof (file or test) | Stage status from `../playbook/STATUS.md` | What is still unproven |
|---|---|---|---|---|---|
| Identity | partial | not ready | `policy/tests/test_policy_python.py` (87 tests, 0 skipped, `evidence/junit-policy.xml`); `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row`; `docs/03-identity/target-access-matrix.md`; `docs/ADR/0003-s06-risk-recommendations.md` (decision 1) | S04-03 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | The role is a word the caller types. Nothing proves who the caller is (`SB-09`, `RK-01`). ADR 0003 puts login out of scope. |
| Secrets | partial | not ready | `tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns` (in `evidence/junit-security.xml`); `legacy/reconcile_legacy.py` reads the password from the environment; `.env.example`; `docs/04-secrets/evidence.md`; `docs/04-secrets/rotation-log.md` (no entries) | S04-04 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | The old password stays in git history (commit `e61ba2e`). Nobody recorded a rotation (`SB-17`). No secret store exists. |
| IaC | partial | not ready | `infra/terraform/main.tf`; `docs/05-iac/evidence.md`; `Dockerfile`; `scripts/bootstrap.ps1` | S04-05 Half A CONDITIONAL PASS. Half B PASS. | `infra/terraform/main.tf` was checked with `terraform validate` in a container. Nobody ran `apply`, because the packet has no cloud account. Production infrastructure is Unknown. |
| Policy | ready | partial | `policy/opa/access.rego`; `policy/opa/ai_action.rego`; `evidence/opa-test.json` (32 results, `opa=0` in `evidence/exit-codes.txt`); `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access`; `policy/tests/test_policy_python.py::test_no_route_can_execute` | S04-06 Half A PASS. Half B CONDITIONAL PASS. | The policy checks that an approval id is not blank. It does not look the id up (`docs/demo/evidence.md` section 8). With `opa` on the PATH each decision is slow, so tests use the Python copy (`SB-20`). |
| CI/CD | partial | partial | `../.github/workflows/ci.yml`; `docs/16-evidence-pack/ci-run-38521594275.txt`; `evidence/exit-codes.txt`; `scripts/check_junit_no_skips.py`; `tests/ci/test_skip_guard.py` | S04-07 Half A PASS. Half B PASS. S05-13 CI proof PASS (runs 38212456142 and 38214470465). | The GitHub run on the current commit ended red. Tests, policy and security stages passed. The lint, dependency scan and static scan stages exit 1 (`BL-10`, `BL-11`, `BL-12`). |
| Observability | partial | not ready | `docs/08-observability/log-schema.md`; `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field`; `tests/app/test_audit_row_keys.py`; `tests/app/test_readiness_route.py`; `docs/08-observability/slo-proposal.md` | S04-08 Half A CONDITIONAL PASS. Half B PASS. | Dashboards and service level targets are written designs only. The targets are PROPOSED. Nobody built a metric pipeline or a trace collector. |
| AI guardrails | partial | not ready | `tests/ai/test_guardrails.py` (51 tests); `tests/app/test_recommend_route.py`; `tests/app/test_command_phrases.py`; `docs/09-ai-guardrails/ai-risk-register.md` | S2Q PASS. S04-09 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | The model is the stand-in `local-sim-v1`. No test ran against a real model. The summarize route holds one command sentence and lets other command text through (`D-09` in `docs/model-comparison/app-comparison.md`). The timeout of 10 seconds is PROPOSED. |
| Performance | partial | not ready | `docs/10-performance/evidence.md`; `docs/10-performance/measure-after.json`; `tests/performance/test_load_once.py` | S04-10 Half A CONDITIONAL PASS. Half B PASS. | Timings come from one Windows machine. No load test ran. Production traffic is Unknown. |
| Reliability | partial | not ready | `docs/11-reliability/recovery-evidence.md`; `tests/reliability/test_drills.py`; `tests/reliability/test_breaker.py` | S04-11 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | The audit write lock and the duplicate memory cover one process. A held case has no inbox (`RK-10`). A model error and a timeout give different reasons than the PRD table asks (`Q-4`). The breaker numbers are PROPOSED. |
| FinOps | partial | not ready | `docs/12-finops/evidence.md`; `docs/12-finops/metrics_from_audit_output.txt`; `docs/12-finops/cost_baseline_output_halfB.txt`; `tests/finops/` | S04-12 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | Every token and cost number is EDUCATIONAL. It is not money. The 300 second answer store (RQ-31) is not built (ADR 0004). |
| Security validation | partial | not ready | `evidence/junit-security.xml` (195 tests, 0 skipped); `docs/13-security-validation/evidence.md`; `docs/13-security-validation/remediation-backlog.md`; `security/threat-model.md` | S05-13 Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. CI proof PASS. | Three scans exit 1 on real findings. No outside penetration test ran. The STRIDE list had 21 open threats at Half A and nobody recounted it. |
| Audit | ready | not ready | `tests/audit/test_audit_rebuild.py`; `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id`; `docs/14-audit/evidence.md`; `docs/14-audit/compliance-evidence-mapping.md` | S05-14 has no row in `../playbook/STATUS.md`. `docs/14-audit/audit-gap-report.md` (Half A) and `docs/14-audit/evidence.md` (Half B) each say CONDITIONAL PASS. S07 CONDITIONAL PASS added 17-key rows. | The log is a plain file. Anyone with file access can edit it (`RK-08`). The audit route lists what the log cannot prove: caller identity, log integrity and case membership. |

**Worked example (Policy).** The row says "ready" for the lab demo because `evidence/junit-policy.xml` records 87 tests with 0 failures and 0 skipped, and `policy/tests/test_policy_python.py::test_no_route_can_execute` shows that no route can reach EXECUTE. The same row says "partial" for production because the policy only checks that an approval id is not blank. If a route took an approval id from a caller, any text would pass. No route does (`tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check`).

## 2. Counts behind the verdicts

| Measure | Value | Label | Source |
|---|---|---|---|
| Tests collected in the whole repo | 469 | REAL | `pytest tests policy/tests semantic-layer/tests --collect-only`, 2026-10-13 |
| `tests` stage (security-marked tests left out) | 233 passed, 0 failed, 0 skipped | REAL | `evidence/junit-tests.xml` |
| Semantic-layer stage | 41 passed | REAL | `evidence/junit-semantic-layer.xml` |
| Policy stage | 87 passed, 0 skipped | REAL | `evidence/junit-policy.xml` |
| Security stage | 195 passed, 0 skipped | REAL | `evidence/junit-security.xml` |
| Lint findings (`ruff`) | 30 | REAL | `evidence/ruff.json` |
| Dependency advisories (`pip-audit`) | 9 advisory ids on 3 packages, printed as 18 findings | REAL | `evidence/pip-audit.json` |
| Static scan findings (`bandit`) | 40, all LOW severity | REAL | `evidence/bandit.json` |

Check: 233 + 108 security-marked tests in `tests/` + 87 policy tests + 41 semantic-layer tests = 469. The security stage runs the 108 plus the 87, which is 195.

## 3. The 11 items of `../Project_Intent.md` section 6.3

| # | Item | Result | Proof |
|---|---|---|---|
| 1 | D1 exists. Inherited-repo meaning is unchanged unless a later ADR says why. | Ticked | `docs/01-discovery/brownfield-risk-register.md`. `data/synthetic/` and `apps/web/` match the first commit (`git diff e61ba2e HEAD -- data/synthetic apps/web` is empty). Each changed behaviour is listed with its reason in `docs/demo/evidence.md` section 5. |
| 2 | D2 exists. Intended behaviour and defects are in different lists. | Ticked | `docs/02-baseline/behaviour-snapshot.md`; `docs/02-baseline/defect-list.md`. |
| 3 | D3 exists and passed schema tests. Stage S05R folded in the terms D4 introduced, raised the version, and the PRD header cites that version. | Ticked | `evidence/junit-semantic-layer.xml` (41 passed); `docs/02-baseline/semantic-layer-revision.md`; `docs/model-comparison/yaml-hashes-after.md` (version `1.2.1` in 36 hashed files and the PRD). |
| 4 | D4 exists. At least one high-risk decision has allow and deny policy tests. AI cannot silently execute. | Ticked | `policy/tests/test_policy_python.py::test_no_route_can_execute`; `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id`; `evidence/opa-test.json`. |
| 5 | D5 exists. The PRD traces to YAML ids. | Ticked | `docs/prd/prd.md`; `docs/prd/traceability.md`; `docs/prd/prd-review.md` (PASS against v1.8). The PRD is now v1.9 and the last full review was v1.8. |
| 6 | D6 exists. The demo completes one flow to a human decision. The audit row is written before any execute-like state change. | Ticked | `docs/demo/evidence.md` section 2; `tests/app/test_audit_before_state_change.py`; `tests/app/test_demo_flow.py`. |
| 7 | An AI timeout or schema failure sends the case to a person and stores no fake safe recommendation. | Ticked | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary`; `tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text`. |
| 8 | D7 exists. The second model consumed the same YAML. Differences are written. | Ticked | `docs/model-comparison/app-comparison.md` (16 differences); `docs/model-comparison/yaml-hashes-after.md`; `docs/16-evidence-pack/hash-recheck.md` (36 of 36 match). |
| 9 | D8 exists. Ready, not ready, and accepted risk have owners. | Ticked, with PROPOSED owners | `docs/15-readiness/go-no-go-decision.md`; `docs/15-readiness/risk-owner-table.md`. The owner of some rows is Unknown, with Team-Force PROPOSED under `docs/00-contract/operating-contract.md` row 10. |
| 10 | Demo numbers carry an honesty label: REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. | Ticked | `tests/app/test_page.py::test_every_number_on_the_page_has_a_label`. The second app's page has fewer labels (`D-15`). |
| 11 | You can answer the section 3.3 questions. | Not ready | S10 writes the answers in `docs/defence/defence-answers.md`. That folder does not exist yet. The pack holds the evidence for each answer. |

## 4. Lifecycle

This file cites the stage results in `../playbook/STATUS.md` and the operating contract (`docs/15-readiness/operating-contract-check.md`). `docs/15-readiness/go-no-go-decision.md` uses the verdicts above. Stage S10 presents from `PRODUCTION_EVIDENCE_PACK.md`.
