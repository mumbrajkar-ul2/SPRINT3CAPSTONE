# Production Evidence Pack

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenges 15 and 16, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. Every path in this pack exists (`docs/16-evidence-pack/path-check.md`). 41 of 63 open risks have a PROPOSED owner and no written acceptance. |
| Evidence sources | `docs/15-readiness/` (six files); `docs/16-evidence-pack/` (four files); `evidence/` (final run); `docs/` evidence file of each stage; `../playbook/STATUS.md`; `docs/00-contract/operating-contract.md` v1.4; `docs/00-contract/challenge-to-spine-crosswalk.md`; `docs/model-comparison/app-comparison.md` version 2; `docs/model-comparison/second-model-load-fix.md`; `docs/model-comparison/yaml-hashes-after.md`; `docs/demo/evidence.md`. |
| Assumptions | "The lab demo" means the governed app in `apps/api/`, on one machine, with synthetic data, the stand-in model `local-sim-v1`, one server process, and a person who types the role word. "Production" means a live service with real users, a real model and more than one server process. |
| Unresolved issues | Seven PRD gaps are open (G-1 to G-4, G-6, G-8, G-9). The refreshed `evidence/` folder has no commit. `../playbook/STATUS.md` has no row for S05-14, S06 or S06R. |
| Residual risks | 63 open rows in `docs/15-readiness/residual-risk-register.md`. |

Paths are relative to the project folder (06-telecom-service-network-incident-ops) unless they start with `../`.

**Claim labels.** Verified Fact names a file or a test. Inference is a conclusion drawn from facts. Assumption is a stated starting point. Unknown means the packet has no evidence.

**Number labels.** REAL is a measured value. PRECOMPUTED is a value worked out before the run. SIMULATED is a value that a stand-in produces. EDUCATIONAL is a teaching figure, and it is not money.

## Executive summary

**Decision.** No-go for production. Go for the lab demo and the S10 defence, under seven conditions (`docs/15-readiness/go-no-go-decision.md`).

**What exists.**
- A governed app in `apps/api/` with 9 routes. No route can reach the outcome EXECUTE.
- A policy in OPA (Rego) and in Python. The two copies agree in a test.
- An audit log with 17 keys per row. One route rebuilds a case from one correlation id.
- A second app, built by another model from the same semantic layer, for comparison.
- 469 tests pass with 0 skipped in the final run (REAL).

**Biggest risks.**
1. The caller's role is a word the caller types. Nothing proves who the caller is (`SB-09`).
2. The model is the stand-in `local-sim-v1`. No test ran against a real model (`AIR-01`).
3. The audit log is a plain file. Anyone with file access can edit it (`SB-12`).
4. The GitHub run on the last commit ended red. Lint (30 findings), the dependency scan (9 advisory ids) and the static scan (40 findings) exit 1.
5. The policy checks that an approval id is not blank. It does not look the id up (`SB-08`).

**Second model.** The 36 hashes of the semantic layer and the PRD match, so neither changed. The two apps differ in 16 places: 3 are listed gaps and 13 are unlisted. The second app loses audit rows when 8 threads write at once (1927 of 2000 kept).

**What stays unknown.** Behaviour with real users, a real model or two server processes. Encryption at rest and in transit. Who owns 41 of the 63 open risks.

**Gate.** CONDITIONAL PASS, because 41 owners are PROPOSED (contract row 10). The stage results are in `docs/15-readiness/go-no-go-decision.md` section 4.

## Release Summary

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The release is the governed app in `apps/api/`. It has 9 routes: `GET /`, `GET /health`, `GET /ready`, `GET /records/{id}`, `GET /alarms/storms/{storm_batch_id}`, `POST /ai/summarize/{id}`, `POST /ai/recommend/{id}`, `POST /approvals/{id}`, `GET /audit/{correlation_id}`. | Verified Fact | `apps/api/main.py`; `data/contracts/openapi-fragment.yaml`; `tests/app/test_openapi_fragment.py` | REAL (9 routes) | Behaviour with real users. |
| No route can reach the outcome EXECUTE. | Verified Fact | `policy/tests/test_policy_python.py::test_no_route_can_execute` | none | A future route. The contract says an execute route waits for four gates (row 2). |
| 469 tests pass and 0 skip in the final run on this machine. | Verified Fact | `evidence/junit-tests.xml` (233); `evidence/junit-semantic-layer.xml` (41); `evidence/junit-policy.xml` (87); `evidence/junit-security.xml` (195, which holds the 87 policy tests and 108 security-marked tests); `evidence/exit-codes.txt` | REAL | The same run on another machine. |
| The semantic layer is version 1.2.1 (765 ids). The PRD is v1.9. `docs/prd/traceability.md` is v1.10. | Verified Fact | `semantic-layer/README.md`; `docs/prd/prd.md`; `docs/prd/traceability.md`; `docs/model-comparison/yaml-hashes-after.md` | REAL | A full S06R review of PRD v1.9. The last full review was against v1.8 (`S09-2`). |
| The GitHub run on commit `ec56a34` ended red. The failing steps are lint, pip-audit and bandit. | Verified Fact | `docs/16-evidence-pack/ci-run-38521594275.txt` | REAL | A run on the final tree. The refreshed `evidence/` has no commit (`S09-1`). |
| `make evidence` did not run. `make` is not installed on this machine. `scripts/evidence.ps1` ran instead. | Verified Fact | `evidence/run-info.txt`; `Makefile` (target `evidence`) | none | The make target on this machine (`S09-4`). |
| The decision is no-go for production and go for the lab demo under seven conditions. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` | none | Written acceptance of 41 risks by Team-Force (`docs/15-readiness/risk-owner-table.md`). |

### Run id of the final evidence run

| Item | Value | Source |
|---|---|---|
| Commit | `ec56a3411f963e80b3f23e262801d22ef1cb121c` | `evidence/run-info.txt` |
| Time (UTC) | 2026-10-14T06:32:03Z | `evidence/run-info.txt` |
| Runner | local (Windows 10.0.26200.0, Python 3.13.5, OPA 1.21.2) | `evidence/run-info.txt` |
| Command | `scripts/evidence.ps1` | `evidence/README.md` |
| GitHub run for the same commit | 38521594275. It ended in failure. | `docs/16-evidence-pack/ci-run-38521594275.txt` |

The run id of the local run is "local, commit `ec56a34`, 2026-10-14T06:32:03Z", because the script writes no other id.

## Behavioural Baseline Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The tests recorded today's behaviour before any change. | Verified Fact | `tests/characterization/test_current_behaviour.py`; `docs/02-baseline/behaviour-snapshot.md`; `docs/02-baseline/baseline-test-report.md` | REAL | Behaviour that no test reaches. |
| The Keep list and the Fix list share no row. | Verified Fact | `docs/02-baseline/defect-list.md` | none | Who fixes each defect (Unknown). |
| The data profile confirmed 19 of the 24 seeded quality labels. It did not find 5 labels. | Verified Fact | `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/profile-output.json`; `data/quality_issues.json` | REAL (19 of 24) | Why 5 labels are not found (Unknown). |
| `data/synthetic/` and `apps/web/` match the first commit `e61ba2e`. | Verified Fact | `git diff e61ba2e HEAD -- data/synthetic apps/web` prints nothing. `docs/15-readiness/operating-contract-check.md` rows 5 and 6. | none | None. |
| Each changed behaviour has a reason. | Verified Fact | `docs/demo/evidence.md` section 5 | none | Tests that nobody updated. The older tests that expected the old behaviour are listed in that section. |

## IAM and Least Privilege Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| A call with no role header gets 403 and a `policy.deny` row. | Verified Fact | `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` | none | None for the lab demo. |
| 18 roles times 6 routes give 108 access cells. Both apps give the same answer in all 108. | Verified Fact | `docs/model-comparison/app-comparison.md` section 1; `docs/03-identity/target-access-matrix.md` | REAL (108) | A role that nobody listed. |
| No route reads an approval id from the caller. | Verified Fact | `tests/security/test_client_flags_ignored.py::test_no_route_reads_an_approval_id_from_the_caller` | none | None. |
| The role `clinician` was removed from `apps/api/main.py`. | Verified Fact | `docs/03-identity/evidence.md`; `../playbook/STATUS.md` row S04-03 Half B | none | None. |
| The role is a word the caller types. Nothing proves who the caller is. | Verified Fact | `apps/api/main.py` reads `X-User-Role`; `docs/ADR/0003-s06-risk-recommendations.md` decision 1 | none | Sign-in. ADR 0003 puts it out of scope (`SB-09`, `RK-01`). |
| `apps/api/services/policy.py` still falls back to the `operator` fields for a role id with no entry. | Verified Fact | `apps/api/services/policy.py`; `docs/15-readiness/residual-risk-register.md` row `SB-02` | none | Whether the fallback goes. |

## Secrets and Encryption Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The old shared database password left `legacy/reconcile_legacy.py`. The script reads it from the environment. | Verified Fact | `legacy/reconcile_legacy.py`; `tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment` | none | The old value is still in git history (commit `e61ba2e`). |
| `.env.example` holds `CHANGE_ME` for every secret. | Verified Fact | `.env.example` | none | A real secret store (none exists). |
| The repo has no secret pattern. | Verified Fact | `tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns` | none | The test scans the project folder only (`REPO` is two levels above the test file). `../transcript/` is outside it. It matches real key formats only (`BL-03`). |
| Nobody recorded a secret rotation. | Verified Fact | `docs/04-secrets/rotation-log.md` (no entries) | none | Where a rotation record would live (`SB-17`). |
| Encryption at rest and in transit. | Unknown | A search of `docs/04-secrets/`, `docs/05-iac/` and `docs/13-security-validation/` finds no mention of encryption, TLS or HTTPS. | none | All of it. The app serves plain HTTP on one machine. |
| The old password text sits in `../transcript/chat_transcript.md`. | Verified Fact | `docs/15-readiness/operating-contract-check.md` section 3.3 | none | A decision to redact or accept it (`S09-5`). |

## IaC Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| `scripts/bootstrap.ps1` ran from a fresh folder copy and 15 tests passed on Python 3.13.5. | Verified Fact | `docs/05-iac/evidence.md` | REAL (15, at S04-05 Half B) | The count today is 469. The bootstrap was not rerun in S09. |
| The same steps passed in a Linux Python 3.11 container, and the Docker build and container run passed. | Verified Fact | `docs/05-iac/evidence.md`; `Dockerfile` | REAL | The same on a cloud host. |
| `infra/terraform/main.tf` writes one local settings file. It builds no cloud resource. It passed `terraform validate` in a container (Terraform 1.9.8). | Verified Fact | `infra/terraform/main.tf`; `docs/05-iac/evidence.md` | none | `terraform apply` never ran. The packet has no cloud account. Production infrastructure is Unknown. |

## Policy-as-Code Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| 87 Python policy tests pass with 0 skipped. | Verified Fact | `evidence/junit-policy.xml`; `policy/tests/test_policy_python.py` | REAL (87) | None for the lab demo. |
| 32 of 32 Rego tests pass. | Verified Fact | `evidence/opa-test.json`; `evidence/exit-codes.txt` (`opa=0`) | REAL (32) | Rego under real load. With `opa` on the PATH each decision is slow, so tests use the Python copy (`SB-20`). |
| The Rego copy and the Python copy agree on access. | Verified Fact | `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access` | none | Inputs that no test names. |
| EXECUTE needs an approval id. No route can reach EXECUTE. | Verified Fact | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id`; `policy/tests/test_policy_python.py::test_no_route_can_execute` | none | None. |
| The policy checks that the approval id is not blank. It does not look the id up in the approval store. | Verified Fact | `docs/demo/evidence.md` section 8 (limits 1 and 2) | none | A lookup inside the policy (`SB-08`). |
| A check over 73,728 input combinations found one that reaches EXECUTE. That one has an approval id and an audit row. | Verified Fact | `docs/06-policy/evidence.md` (S04-06 Half A) | REAL (73,728 combinations checked) | The check ran at S04-06 Half A, before S07. It was not rerun in S09. |

## CI/CD and Supply Chain Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The pipeline script runs 10 stages and writes the files in `evidence/`. Tests, semantic-layer, `opa`, policy, security, sbom and checksums exit 0. | Verified Fact | `scripts/evidence.ps1`; `evidence/exit-codes.txt` | REAL | The `make evidence` target on this machine (`S09-4`). |
| Lint, `pip-audit` and `bandit` exit 1 on real findings. | Verified Fact | `evidence/exit-codes.txt`; `evidence/ruff.json`; `evidence/pip-audit.json`; `evidence/bandit.json` | REAL (ruff 30; pip-audit 9 advisory ids on 3 packages, printed as 18 findings; bandit 40, all LOW) | Fixes. Each has a backlog row (`BL-10`, `BL-11`, `BL-12`). |
| The workflow `workshop-ci` runs on `ubuntu-24.04`. The run on commit `ec56a34` ended in failure at the same three steps. | Verified Fact | `../.github/workflows/ci.yml`; `docs/16-evidence-pack/ci-run-38521594275.txt` | REAL | A run that proves the final tree. |
| A skip guard fails the security stage when any security test skips. | Verified Fact | `scripts/check_junit_no_skips.py`; `tests/ci/test_skip_guard.py` | none | None. |
| A software bill of materials is written on each run. | Verified Fact | `evidence/sbom.cdx.json`; `evidence/pip-freeze.txt`; `evidence/source-checksums.txt` | none | Signing and provenance of builds are Unknown. |
| 5 development tools are pinned in `requirements-dev.txt`. | Verified Fact | `requirements-dev.txt`; `docs/07-cicd/evidence.md` | REAL (5) | Pins of every transitive package. |
| The dependency scan lists advisories on `starlette` (7), `pytest` (1) and `python-dotenv` (1). | Verified Fact | `evidence/pip-audit.json`; `supply-chain/dependency-risk-register.md` | REAL | The effect of each advisory on this app. |

## Observability and Traceability Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| Every new audit row has 17 keys and a `correlation_id`. | Verified Fact | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field`; `tests/app/test_audit_row_keys.py` | REAL (17 keys) | Rows written before the change. 96 old lines have 3 keys and no `correlation_id`. |
| Before the change, 1992 of 3000 event lines had a null or blank correlation id. | Verified Fact | `docs/08-observability/evidence.md`; `../playbook/STATUS.md` row S04-08 Half A | REAL (1992 of 3000, measured at S04-08 Half A) | The share today. The pack did not recount it. |
| `GET /ready` returns 503 when a dependency is down. | Verified Fact | `tests/app/test_readiness_route.py` | none | A health check from outside the machine. |
| Dashboards, service level targets and a trace design are written. Nobody built them. | Verified Fact | `docs/08-observability/dashboard-sketch.md`; `docs/08-observability/slo-proposal.md`; `docs/08-observability/trace-design.md` | none (targets are PROPOSED) | A metric pipeline and a trace collector. |
| One case can be rebuilt after the fact from one correlation id. | Verified Fact | `docs/08-observability/incident-reconstruction.md`; `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` | none | A case that crosses two processes. |

## AI Security and Guardrails Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| 51 guardrail tests pass. | Verified Fact | `tests/ai/test_guardrails.py`; `docs/09-ai-guardrails/evidence.md` | REAL (51) | A real model. |
| A model timeout returns HOLD_FOR_REVIEW with no summary. | Verified Fact | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` | none | The timeout of 10 seconds is PROPOSED. Nobody measured it against a real model. |
| A bad answer shape returns HOLD_FOR_REVIEW with no text. | Verified Fact | `tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text` | none | None. |
| The recommend route holds a model answer that carries one of 29 command phrases. | Verified Fact | `tests/app/test_command_phrases.py` | REAL (29 phrases, 40 tests) | A phrase outside the list. The PRD says the list is short. |
| The summarize route holds only one injection sentence. A model text with another command phrase comes back as RECOMMEND_ONLY. | Verified Fact | `docs/model-comparison/app-comparison.md` finding F-3 (D-09) | none | A decision on whether the summarize route holds all 29 phrases (`Q-3`). |
| The prompt carries 10 device fields. `mgmt_ip`, `credential_profile` and secret names stay out. | Verified Fact | `tests/ai/test_guardrails.py`; `docs/model-comparison/app-comparison.md` section 7 | REAL (10 fields) | Instruction text typed into `hostname` or `vendor` travels with the prompt (`AIR-01`). |
| The model is the stand-in `local-sim-v1`. | Verified Fact | `apps/api/services/ai_gateway.py` | none | All behaviour of a real model. |

## Performance and Scalability Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| `load_record` fell from 2.170 and 2.352 ms to 0.0005 ms per call after the data file is read once. | Verified Fact | `docs/10-performance/evidence.md`; `docs/10-performance/measure-before.json`; `docs/10-performance/measure-after.json`; `tests/performance/test_load_once.py` | REAL (one Windows machine, 2026-10-11) | Another machine. |
| The median time of `GET /records/{id}` fell from 16.031 ms to 5.805 ms after both steps. | Verified Fact | `docs/10-performance/evidence.md` | REAL (one Windows machine) | Part of that time is the test client (about 3.6 to 4.2 ms on `GET /health`). |
| The measurements are single-caller medians from `measure.py --rounds 5`. The evidence lists no test with many callers at once. Traffic in production is Unknown. | Inference | `docs/10-performance/evidence.md`; `docs/10-performance/load-scenarios.md` | none | Throughput and latency under many callers. |
| The stand-in model waits 0.01 seconds, so the latency in the audit rows is the wait of the stand-in. | Verified Fact | `docs/12-finops/evidence.md` (residual risks); `apps/api/services/ai_gateway.py` | SIMULATED | Real model latency. |

## Reliability and Failure Engineering Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The reliability drills pass, including the impossible-timestamp drill and the AI-timeout drill. | Verified Fact | `docs/11-reliability/recovery-evidence.md`; `tests/reliability/test_drills.py` | REAL (46 tests at S04-11) | The drills ran with one process. |
| The audit write lock keeps all rows when 8 threads write 2000 rows. Before the lock, 71 to 109 rows were lost. | Verified Fact | `tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row`; `docs/11-reliability/failure-mode-catalogue.md` | REAL (2000 of 2000; 71 to 109 lost before) | Linux and two server processes (`SB-12`, `FM-13`). |
| A circuit breaker and an in-flight limit cover the model call. | Verified Fact | `tests/reliability/test_breaker.py`; `.env.example` (`BREAKER_FAILURE_THRESHOLD`, `BREAKER_OPEN_SECONDS`, `MODEL_MAX_IN_FLIGHT`) | none (the three values are PROPOSED) | Values tested against a real model. |
| The duplicate memory for alarms, orders and events lives in one process. | Verified Fact | `docs/11-reliability/recovery-evidence.md` ("Open items") | none | Two processes (`FM-06`). |
| A held case has no inbox. A person must know where to look. | Verified Fact | `docs/prd/Risk Management.md` (`RK-10`) | none | A queue or an inbox. |
| The model error and the model timeout give other reason ids than the PRD failure table asks for. | Verified Fact | `docs/model-comparison/app-comparison.md` finding F-4 (D-06) | none | A decision on the right id (`Q-4`). |

## AI FinOps Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| `docs/12-finops/metrics_from_audit.py` computes 5 of the 7 metrics from real audit rows. | Verified Fact | `docs/12-finops/metrics_from_audit.py`; `docs/12-finops/metrics_from_audit_output.txt`; `tests/finops/test_metrics_from_audit.py` | REAL (rows). EDUCATIONAL (tokens). | `metric.quarantine_rate` and `metric.retry_count` have no audit source (`docs/12-finops/evidence.md`). |
| Every token and cost figure is a teaching figure. In the S04-12 run the 17 model-call rows gave a mean of 90.0 tokens and 1.53 educational units in total. | Verified Fact | `docs/12-finops/evidence.md`; `docs/12-finops/cost_baseline_output_halfB.txt` | EDUCATIONAL (rate 1.0 unit per 1000 tokens, PROPOSED) | A price. The packet has no price list. |
| Eight capabilities have hosted-model cost 0 because they use no model. Three keep an Unknown price. | Verified Fact | `docs/00-contract/cost-envelope.md`; `../playbook/STATUS.md` row S2Q | none (price Unknown) | The price of a hosted model call. |
| The 300 second answer store (RQ-31) is deferred. | Verified Fact | `docs/ADR/0004-defer-rq-31-answer-store.md` | none | The saving the store would give. |

## Automated Security Validation Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| 195 security tests pass with 0 skipped. | Verified Fact | `evidence/junit-security.xml`; `docs/13-security-validation/evidence.md` | REAL (195) | Tests for threats that nobody listed. |
| The threat model lists open threats. The STRIDE list had 21 open threats at S05-13 Half A. Nobody recounted it. | Verified Fact | `security/threat-model.md` | REAL (21, at S05-13 Half A) | The count today. |
| The remediation backlog has 21 open rows after S05-13 Half B. Each has an owner and a stage. | Verified Fact | `docs/13-security-validation/remediation-backlog.md` | REAL (21, at S05-13 Half B) | The count today. Some rows closed after that stage. |
| Three scans exit 1 on real findings. None is switched off. | Verified Fact | `evidence/exit-codes.txt`; `docs/13-security-validation/evidence.md` | REAL | Fixes. |
| No outside penetration test appears in the packet. | Unknown | A search of `docs/13-security-validation/` finds no mention of one. | none | An outside test, if one exists. |

## Auditability and Compliance Evidence

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| `GET /audit/{correlation_id}` rebuilds a case in time order and lists what the log cannot prove. | Verified Fact | `tests/audit/test_audit_rebuild.py`; `docs/14-audit/evidence.md` | REAL (32 new tests at S05-14) | The list says the log cannot prove caller identity, log integrity and case membership. |
| The audit row is written before any execute-like state change. | Verified Fact | `tests/app/test_audit_before_state_change.py` | none | A route that changes a live network (none exists). |
| 34 compliance duties each name a stored evidence file. 2 duties fail today (`SB-01`, `SB-06`). | Verified Fact | `docs/14-audit/compliance-evidence-mapping.md` | REAL (34; 2 fail) | Duties outside the five mapped control areas. |
| The audit log is a plain file that anyone with file access can edit. | Verified Fact | `docs/prd/Risk Management.md` (`RK-08`) | none | Tamper evidence. |
| Tests outside `tests/app/` write to the real audit log. | Verified Fact | `docs/demo/evidence.md` section 8 (limit 7); `docs/16-evidence-pack/audit-log-record.md` | none | A change so that no test writes the real file (`BL-09`). |

### Audit log before and after the final evidence run

Source: `docs/16-evidence-pack/audit-log-record.md`. All numbers are REAL.

| Moment | Time (UTC) | Lines | SHA-256 |
|---|---|---|---|
| Before the run | 2026-10-14 06:31:53 | 308 | `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` |
| After the run, before the restore | 2026-10-14 06:37:27 | 314 | `A117EA326FE4AA4D3E87ABF9D292D60D89F82DF9FD6C0BAF1BD5ABF47A7A8B55` |
| After the restore | 2026-10-14 (after 06:37:27) | 308 | `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` |

**The run added 6 rows** (lines 309 to 314). Nothing was restored by the run. After the run, the agent copied the saved pre-run file back over `logs/audit.log`, so the file is back to 308 lines and the same SHA-256 as before the run.

**Worked example.** Before the run the file had 308 lines. The run wrote 6 more, so the file had 314. The restore put back the saved copy, so the file has 308 again. The six rows are listed in the record file by line number, action and role.

### Hash re-check

Source: `docs/16-evidence-pack/hash-recheck.md`. **36 of 36 hashes match** the values in `docs/model-comparison/yaml-hashes-after.md`. These cover 20 files in `semantic-layer/`, `docs/prd/prd.md` and 15 other files. The semantic layer and the PRD did not change after S08.

## Second-Model Comparison Evidence

This section covers stage S08. The second model (GPT-5.6 Sol) built `apps/api_model_b/` from the same YAML and the same brief. Both apps ran the same test files through the alias plugin `docs/model-comparison/harness/alias_model_b.py`, with `APP_UNDER_TEST=b` for the second app.

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The 36 hashes match. The YAML and the PRD did not change between S08 Part 1 and now. | Verified Fact | `docs/model-comparison/yaml-hashes-before.md`; `docs/model-comparison/yaml-hashes-after.md`; `docs/16-evidence-pack/hash-recheck.md` | REAL (36 of 36) | None. |
| The first app passes all 469 tests with 0 skipped in the final run. In S08 it passed 467 and skipped 2, because no `opa` program was installed. | Verified Fact | `evidence/junit-tests.xml`; `evidence/junit-policy.xml`; `docs/model-comparison/app-comparison.md` section 3.1 | REAL | None. |
| The second app passes 378 of 469 tests. It fails 89: 35 are differences a user can see (D) and 54 are internal names that the first app's tests patch (H). It skips 2 and 0 failed to load. | Verified Fact | `docs/model-comparison/app-comparison.md` sections 3.1 and 3.3; `docs/model-comparison/second-model-load-fix.md` | REAL (378 / 89 / 2 / 0; 35 D plus 54 H) | The second app was not rerun with `opa` installed. Whether its 2 skips pass is Unknown. |
| 24 of the second app's passing drill tests run a copy of the first app's `apps/api/services/dedupe.py`. They say nothing about the second model. | Verified Fact | `docs/model-comparison/second-model-load-fix.md`; `docs/model-comparison/app-comparison.md` section 3.1 | REAL (24) | A second-model dedupe. |
| The second model was asked to pass 22 named tests. The first app passed 22. The second app passed 21. | Verified Fact | `docs/model-comparison/second-model-test-split.md`; `docs/model-comparison/second-model-run-log.md`; `docs/model-comparison/app-comparison.md` section 3.2 | REAL (22; 21) | The other 47 tests the PRD names were not asked of the second model. |
| Both apps return identical bodies for 351 device reads and 352 storm reads, and agree on 108 role and route cells. Neither app returns EXECUTE. Neither app writes a data file. | Verified Fact | `docs/model-comparison/app-comparison.md` section 1 | REAL (351; 352; 108) | Inputs that no probe sent. |
| No status word falls outside the YAML in either app. | Verified Fact | `docs/model-comparison/app-comparison.md` section 4.1 | REAL (0 words) | None. |

### The 16 differences

Source: `docs/model-comparison/app-comparison.md` section 5. 3 are listed in the PRD gaps. 13 are unlisted.

| Id | What differs | Listed? |
|---|---|---|
| D-01 | `/ready` body keys. First app: the key status and the check name devices_csv. Second app: the key runbook_level and the check name devices.csv. | Listed. G-4. |
| D-02 | The 422 and 500 body text. | Listed. G-6. |
| D-03 | `approval_required` in the recommend body. First app `false`. Second app `true`. | Unlisted. |
| D-04 | `policy_version` key in the AI body. Present in the first app only. | Unlisted. |
| D-05 | Reasons list. The first app adds a `rule.*` id after the `failmode.*` id. | Unlisted. |
| D-06 | Failure id when the model raises, times out or the breaker is open. Neither app follows the PRD table fully. | Unlisted. |
| D-07 | Stale flag check. The first app blocks `true` in any letter case. The second app blocks exact `true` only. | Unlisted. |
| D-08 | Model answer check. The first app holds a bad outcome word or a blank summary. The second app returns the text. | Unlisted. |
| D-09 | Summarize route. The first app holds one injection sentence. The second app holds all 29 command phrases. | Unlisted. |
| D-10 | Command phrase matching. 7 of 29 texts get another result. | Listed. G-8. |
| D-11 | Audit `cannot_prove`. After an approval the second app still says it cannot prove `approval_id`. | Unlisted. |
| D-12 | Audit file writes. The first app has a lock and keeps 2000 of 2000 rows. The second app keeps 1927 of 2000. | Unlisted. |
| D-13 | Approvals file path and the `ts` key. | Unlisted. |
| D-14 | Policy copy. The second app's `evaluate_ai_action` fails 9 policy tests. No route calls it. | Unlisted. |
| D-15 | The page. 20,062 bytes against 2,703 bytes. | Unlisted. |
| D-16 | Prompt text lines. This changes `prompt_hash`. | Unlisted. |

### Findings of the comparison

Each finding has the finding, the evidence, the impact, the risk, the confidence and the open questions. The full text is in `docs/model-comparison/app-comparison.md` section 6.

| Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|
| F-7. The second app loses audit rows when 8 threads write at once. | D-12. `tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row` fails for the second app. | An audit chain with missing rows. | High for a service that serves two requests at once. | High. Unknown on another operating system. | Q-7 |
| F-2. The second app lets some bad model answers through. | D-08, D-10. Two guardrail tests fail for the second app. | The caller sees model text that the first app holds. | Medium. The second app never returns EXECUTE. | High for the facts. Medium for the impact. | Q-1, Q-2 |
| F-3. The first app lets most command texts through on the summarize route. | D-09. `docs/model-comparison/harness/probe_battery2.py`. | The `recommendation` field can carry command text. | Medium. No code turns the text into a change. | High. | Q-3 |
| F-4. Neither app follows the PRD failure table. | D-06. PRD lines 170 and 171. | An audit reader sees a timeout when the model failed. | Medium. | High. | Q-4 |
| F-5. The two apps give different `approval_required` values. | D-03. | A client may skip or force the approval step. | Medium. | High for the facts. Low on which value is right. | Q-5 |
| F-6. The second app's audit answer says it cannot prove `approval_id` after an approval. | D-11. `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` fails for the second app. | An auditor reads that the approval id is unprovable when the log holds it. | Medium. No row is hidden. | High. | Q-6 |
| F-8. The second app has a policy copy that disagrees with the policy tests. | D-14. 9 policy tests fail for the second app. | None today. | Medium later. | High. | Q-8 |

### Verdict

**Did the meanings drift?** Yes in rare inputs and list contents. No in outcome words, failure ids, audit keys, role grants and data rows. 6 of the 16 differences change which model text a caller receives, which reason an audit shows, or whether an audit row survives (D-06, D-08, D-09, D-10, D-11, D-12).

**What the YAML prevented.** It prevented invented words (0 outside the YAML), invented fields, a different prompt allow list, a different command phrase list, a different access matrix and a different audit row shape.

**What the YAML did not prevent.** A rule for what counts as a word break (G-8). The meaning of `approval_required` (D-03). The meaning of "any row" for `cannot_prove` (D-11). The failure id after a raise or an open breaker (D-06). Locking of the audit file (D-12).

**Stage status.** CONDITIONAL PASS (`../playbook/STATUS.md` rows S08 Part 1, Part 2 and Part 3). The ranking of risk is F-7, F-2, F-3, F-4, F-5, F-6, F-8.

## Production Readiness Decision

| Claim | Label | Evidence (path or test) | Number label | Still unproven |
|---|---|---|---|---|
| The decision is no-go for production. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` section 1 | none | None. |
| The decision is go for the lab demo and the S10 defence under seven conditions (C1 to C7). | Verified Fact | `docs/15-readiness/go-no-go-decision.md` section 2 | none | Whether Team-Force accepts the 41 PROPOSED owners. |
| 63 risks are open. 22 have a named acceptor. 41 have a PROPOSED owner (38 Team-Force, 3 Mangesh). | Verified Fact | `docs/15-readiness/residual-risk-register.md` section 4; `docs/15-readiness/risk-owner-table.md` | REAL (63; 22; 41) | Written acceptance for the 41. |
| 39 items of work are deferred. | Verified Fact | `docs/15-readiness/deferred-work-list.md` | REAL (39) | An owner decision for each item. |
| No change crossed a Prohibited or PROVISIONAL row of the operating contract. No row is PROVISIONAL at v1.4. | Verified Fact | `docs/15-readiness/operating-contract-check.md` | none | An exception for 3 routes and 4 files that no row or playbook names (`S09-5`). |
| Ten of 11 items in `../Project_Intent.md` section 6.3 are ticked. One is marked not ready. | Verified Fact | `docs/15-readiness/readiness-checklist.md` section 3 | REAL (10 of 11) | Item 11 needs the S10 defence answers. |
| The gate result of this stage is CONDITIONAL PASS. | Verified Fact | `docs/15-readiness/go-no-go-decision.md` section 5 | none | None. |

### Readiness by control area

Source: `docs/15-readiness/readiness-checklist.md` section 1. "Partial" means the control works for part of the claim and the file names the missing part.

| Control area | For the lab demo | For production |
|---|---|---|
| Identity | partial | not ready |
| Secrets | partial | not ready |
| IaC | partial | not ready |
| Policy | ready | partial |
| CI/CD | partial | partial |
| Observability | partial | not ready |
| AI guardrails | partial | not ready |
| Performance | partial | not ready |
| Reliability | partial | not ready |
| FinOps | partial | not ready |
| Security validation | partial | not ready |
| Audit | ready | not ready |

### The 11 items of `../Project_Intent.md` section 6.3

| # | Item | Result |
|---|---|---|
| 1 | D1 exists. Inherited-repo meaning is unchanged unless a later ADR says why. | Ticked |
| 2 | D2 exists. Intended behaviour and defects are in different lists. | Ticked |
| 3 | D3 exists and passed schema tests. | Ticked |
| 4 | D4 exists. A high-risk decision has allow and deny policy tests. AI cannot silently execute. | Ticked |
| 5 | D5 exists. The PRD traces to YAML ids. | Ticked |
| 6 | D6 exists. The demo completes one flow to a human decision. The audit row is written first. | Ticked |
| 7 | An AI timeout or schema failure sends the case to a person. | Ticked |
| 8 | D7 exists. The second model consumed the same YAML. Differences are written. | Ticked |
| 9 | D8 exists. Ready, not ready and accepted risk have owners. | Ticked, with PROPOSED owners |
| 10 | Demo numbers carry an honesty label. | Ticked |
| 11 | You can answer the section 3.3 questions. | Not ready. S10 writes the answers. |

Proof for each item is in `docs/15-readiness/readiness-checklist.md` section 3.

### Top findings

| Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|
| The GitHub run on the last commit ended red. | `docs/16-evidence-pack/ci-run-38521594275.txt`; `evidence/exit-codes.txt` | The pipeline cannot be shown as green. | Low for the demo. Medium for the dependency scan. | High. | Whether to fix the three scans before the defence. |
| The refreshed `evidence/` folder has no commit. | `git status` (S09-1) | The next CI run does not prove the final tree. | Low. | High. | Who commits and when. |
| The role is a typed word. | `apps/api/main.py`; ADR 0003 | Anyone can claim any role. | High if more than the team can reach the app. | Medium. | Whether login enters scope. |
| The policy does not look up the approval id. | `docs/demo/evidence.md` section 8 | A route that took an id from a caller would accept any text. | Medium. | High. | Whether to add a lookup. |
| The audit log is a plain file. | `RK-08`; `docs/14-audit/evidence.md` | Log rows can be edited or lost with two processes. | Medium. | High on this machine. | Tamper evidence. |
| The old password text sits in the chat transcript. | `docs/15-readiness/operating-contract-check.md` section 3.3 | A copy of a lab password exists in a new file. | Low. | High. | Redact or accept. |

## Stage gate results

Source: `docs/15-readiness/go-no-go-decision.md` section 4. The list below keeps the final result of each stage.

| Stage | Result |
|---|---|
| S00, S01, S02 | CONDITIONAL PASS |
| S0B, S2Q, S03 | PASS |
| S03R | PASS in round 3 (rounds 1 and 2 BLOCKED) |
| S04-03 to S04-12 | Each half is PASS or CONDITIONAL PASS. No half is BLOCKED. |
| S05-13 | CONDITIONAL PASS. The CI proof is PASS. |
| S05-14 | CONDITIONAL PASS (no STATUS row) |
| S05R | CONDITIONAL PASS |
| S06 | No stage result recorded. S06F rounds 3 to 7 are CONDITIONAL PASS. |
| S06R | PASS against PRD v1.8 (no STATUS row) |
| S07 | CONDITIONAL PASS |
| S08 | CONDITIONAL PASS |
| S09 | CONDITIONAL PASS |

## Challenge-to-spine crosswalk

Source: `docs/00-contract/challenge-to-spine-crosswalk.md` (v1.0, 2026-10-09). The 16 challenges map to the 16 sections of this pack as follows.

| Pack section | Challenge | Packet folder |
|---|---|---|
| Release Summary | Summary of all 16 | `docs/00-contract/`, `docs/15-readiness/`, `docs/16-evidence-pack/` |
| Behavioural Baseline Evidence | 2 | `docs/02-baseline/` |
| IAM and Least Privilege Evidence | 3 | `docs/03-identity/` |
| Secrets and Encryption Evidence | 4 | `docs/04-secrets/` |
| IaC Evidence | 5 | `docs/05-iac/` |
| Policy-as-Code Evidence | 6 | `docs/06-policy/` |
| CI/CD and Supply Chain Evidence | 7 | `docs/07-cicd/` |
| Observability and Traceability Evidence | 8 | `docs/08-observability/` |
| AI Security and Guardrails Evidence | 9 | `docs/09-ai-guardrails/` |
| Performance and Scalability Evidence | 10 | `docs/10-performance/` |
| Reliability and Failure Engineering Evidence | 11 | `docs/11-reliability/` |
| AI FinOps Evidence | 12 | `docs/12-finops/` |
| Automated Security Validation Evidence | 13 | `docs/13-security-validation/` |
| Auditability and Compliance Evidence | 14 | `docs/14-audit/` |
| Second-Model Comparison Evidence | Stage S08 (D7) | `docs/model-comparison/` |
| Production Readiness Decision | 15 | `docs/15-readiness/` |

Challenge 1 (`docs/01-discovery/`) and challenge 16 (this pack) have no section of their own. Challenge 1 feeds the Release Summary. This pack is challenge 16.

**Worked example.** Take the row for `docs/06-policy/`. The spine has no stage that requires an executable allow-and-deny policy, so the verdict is None. This packet still did the work in stage S04-06, and the section "Policy-as-Code Evidence" above shows it.

### The eighteen rows of the crosswalk

Each row maps one packet folder to the stages of the 42-stage production spine that cover the same ground. The verdict Match means the spine requires the same work. Partial means the spine covers part of it. None means no spine stage requires it. This copy gives the spine stage ids. The spine folder names are in `docs/00-contract/challenge-to-spine-crosswalk.md`, because they name folders of the spine, not folders of this repo.

| Packet folder | Challenge | Spine stage ids that cover the same ground | Verdict |
|---|---|---|---|
| `docs/00-setup/` | Setup and first replay. This packet's Phase 0, beside the 16 challenges. | 0A. Stage 0A is the read-only orientation before any change. | Partial |
| `docs/00-contract/` | Operating contract, cost envelope, and this crosswalk. Spine stages 0B and 0C. | 0B; 0C. | Partial |
| `docs/01-discovery/` | 1. Understand Existing Repo | 0A; 5; 7. Related, smaller files: 0B and 2. | Match |
| `docs/02-baseline/` | 2. Establish Behavioural Baseline | 7; 16. | Partial |
| `docs/03-identity/` | 3. Identity and Least Privilege | 10; 12; 20. Later: 24; 27. | Partial |
| `docs/04-secrets/` | 4. Secrets and Encryption | 7; 11; 12; 15. Later: 24; 27. | Partial |
| `docs/05-iac/` | 5. Infrastructure as Code | 0B; 10; 14. Later: 30; 37. | Partial |
| `docs/06-policy/` | 6. Policy as Code | No spine stage requires an executable allow-and-deny policy. The nearest file is stage 12. The plain-speak note counts that file as a written rule for people, and counts it as different work. Stages 23 and 25 test approval gates and map obligations. They are also counted as different work. | None |
| `docs/07-cicd/` | 7. CI/CD and Supply Chain | 7; 16; 18. Later: 27; 30. | Partial |
| `docs/08-observability/` | 8. Observability and Traceability | 10; 12; 20. Later: 31. | Partial |
| `docs/09-ai-guardrails/` | 9. AI Security and Guardrails | Same-work files: 8; 19 (structured output); 20. Related files: 0B; 2; 9; 10; 11. Later: 23; 24; 26. | Partial |
| `docs/10-performance/` | 10. Performance and Scalability | 0C; 10; 19. Later: 28; 31. | Partial |
| `docs/11-reliability/` | 11. Reliability and Failure Engineering | 20 (the build must implement idempotency). Later: 21; 28. | Partial |
| `docs/12-finops/` | 12. Cost and AI FinOps | 0C; 8; 19. Later: 32. | Partial |
| `docs/13-security-validation/` | 13. Automated Security Validation | 7; 16. Later: 24; 26; 27. | Partial |
| `docs/14-audit/` | 14. Auditability and Compliance Evidence | 20 (audit hooks). Later: 25; 42. | Partial |
| `docs/15-readiness/` | 15. Production Readiness Gate | 0A; 2; 7; 9; 10; 14; 16; 18; 19; 20. Later: 27; 30. | Partial |
| `docs/16-evidence-pack/` | 16. Production Evidence Pack | Pieces in 7; 16; 19. Later: 42 is the pack the note names. | Partial |

