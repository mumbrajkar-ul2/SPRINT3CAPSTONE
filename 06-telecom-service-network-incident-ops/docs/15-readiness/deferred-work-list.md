# Deferred work list

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 15, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. 26 items were named in the plan, a decision file or a backlog and were not finished. 13 more items are on the S05R deferred list. Each row names the stage and the reason. Owners are PROPOSED. |
| Evidence sources | `Execution Plan.md` (phases 7, 9, 10, 11); `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/ADR/0003-s06-risk-recommendations.md`; `docs/ADR/0004-defer-rq-31-answer-store.md`; `docs/02-baseline/S05R_Decisions.md`; `docs/demo/evidence.md` sections 7 and 8; `docs/model-comparison/app-comparison.md` section 8; `docs/13-security-validation/remediation-backlog.md`; `docs/11-reliability/recovery-evidence.md`; `docs/12-finops/evidence.md`; `docs/prd/Risk Management.md`; `../playbook/STATUS.md`. |
| Assumptions | (1) "Deferred" means a source file says the work is planned and no later file shows it done. (2) S09 may not add a control, a test or a fix, and may not change code or YAML. So any item that needs one waits. (3) Team-Force is the PROPOSED owner of each row (`docs/00-contract/operating-contract.md` row 10). |
| Unresolved issues | Nobody set a date for any row. The packet gives no deadline. |
| Residual risks | A deferred item that sits in the residual risk register keeps its risk. The last column of section 1 gives the register id. |

Paths are relative to the project folder (06-telecom-service-network-incident-ops) unless they start with `../`.

## 1. Work the plan named and did not finish

| Id | Item | Where the plan named it | Stage | Why it is not finished | Register id |
|---|---|---|---|---|---|
| DW-01 | The 300 second answer store (RQ-31). | `docs/prd/prd.md` RQ-31; `docs/ADR/0004-defer-rq-31-answer-store.md`. | S07 | Mangesh (FDE) deferred it on 2026-10-13. The row and its test name stay in the PRD, marked deferred. | FM-05 |
| DW-02 | Owner answers for PRD gaps G-1, G-2, G-3, G-4, G-6, G-8 and G-9. | `docs/demo/evidence.md` section 7. | S07 | The "Owner answer" cell is blank for all seven. The PRD says S07 reports PASS only when every row has an answer. This is why S07 is CONDITIONAL PASS. | G-1 to G-9 rows |
| DW-03 | Remove the two `operator` fallbacks in `apps/api/services/policy.py`. | `docs/ADR/0003-s06-risk-recommendations.md` decision 2. | S07 | S07 removed the header default in `apps/api/main.py`. The two fallbacks on lines 290 and 297 remain. No file records why. | SB-02 |
| DW-04 | Wire the Angular scaffold in `apps/web/` to the API. | `Execution Plan.md` Phase 7 ("unless time allows"); `docs/00-contract/operating-contract.md` row 5. | S07 | The four conditions of row 5 are not all met. The served page is the demo. | G-9 |
| DW-05 | Turn the six remaining `enforced_today: false` rules on, or correct them. | `docs/prd/Risk Management.md` RK-13 ("After S07, then S09"). | S09 | A change to `semantic-layer/` needs an ADR and a new version. S09 may not change YAML. | SB-16 |
| DW-06 | Answers to Q-1 to Q-13 and a later ADR for each. | `docs/model-comparison/app-comparison.md` section 8. | After S08 | Each question needs an owner answer first. S08 changed no YAML and no PRD. | S08 D-03 to D-16 |
| DW-07 | A ruling on each of the 30 lint findings, the 9 advisory ids and the 40 static scan findings. | `docs/13-security-validation/remediation-backlog.md` rows BL-10, BL-11 and BL-12. | Unknown | Nobody named a stage. Fixing `starlette` needs a FastAPI upgrade. The scans stay on and the pipeline ends red. | BL-10, BL-11, BL-12 |
| DW-08 | Raise the versions of the three GitHub actions off Node 20. | `docs/13-security-validation/remediation-backlog.md` row SB-21 ("Action versions: S09"). | S09 | The change is an edit of `../.github/workflows/ci.yml`. A version bump needs its own proof run. S09 may not change YAML. | SB-21 |
| DW-09 | Decide the default policy engine (`auto`, `python` or `opa`). | `docs/13-security-validation/remediation-backlog.md` row SB-20. | S07 or a performance follow-up | The decision by Mangesh (FDE) is pending. | SB-20 |
| DW-10 | Limits on request rate, prompt size and answer size, and a load test. | `docs/13-security-validation/remediation-backlog.md` row SB-13. | S04-10 follow-up or S07 | Team-Force has not named the numbers. Production traffic is Unknown. `Risk Management.md` RK-09 says accept. | SB-13 |
| DW-11 | Tamper evidence for the audit log. | `docs/13-security-validation/remediation-backlog.md` row SB-12; `docs/14-audit/evidence.md` ("What the route cannot fix"). | Production | Outside the lab scope. `Risk Management.md` RK-08 says accept the file store. | SB-12 |
| DW-12 | A sign-in system and a server-set role. | `docs/ADR/0003-s06-risk-recommendations.md` decision 1. | Production | ADR 0003 puts login out of scope for this packet. | SB-09 |
| DW-13 | Entries in the rotation log and a place to store rotations. | `docs/04-secrets/rotation-log.md` (no entries); `docs/13-security-validation/remediation-backlog.md` row SB-17. | S04-04 follow-up | The rotation store is Unknown. | BF-R02 |
| DW-14 | A full S06R review of PRD v1.9. | `../playbook/STATUS.md` (row "S07 gaps G-5 G-7"). | S06R | Mangesh (FDE) chose not to rerun it. Checks 8a to 8h held at v1.9. | S09-2 |
| DW-15 | Rows in `../playbook/STATUS.md` for S05-14, S06 and S06R. | `../playbook/STATUS.md` ("One line per stage run"). | S05-14, S06, S06R | Nobody logged a row when the stage ran. | S09-3 |
| DW-16 | A test of a real model: timeout, answer shape, cost and latency. | `docs/09-ai-guardrails/ai-risk-register.md` AIR-05; `docs/prd/Risk Management.md` RK-15. | After a real model is chosen | The packet uses the stand-in `local-sim-v1`. Contract row 8 stops a hosted-model call that S2Q has not named. | AIR-05, RK-15 |
| DW-17 | Three FinOps metrics: `metric.cost_per_correlated_incident`, `metric.quarantine_rate` and `metric.retry_count`. | `docs/12-finops/evidence.md`. | S04-12 | The join from an alarm to an incident is Unknown. `quarantine_rate` and `retry_count` have no audit field. | none |
| DW-18 | A list or inbox page for held cases. | `docs/prd/Risk Management.md` RK-10 ("optional Build"). | S07 | Optional. Team-Force accepted the risk. | RF-08 |
| DW-19 | Dashboards, a trace collector and measured service levels. | `docs/08-observability/dashboard-sketch.md`; `docs/08-observability/trace-design.md`; `docs/08-observability/slo-proposal.md`. | S04-08 | These files are designs. No metric pipeline exists in the lab. The levels are PROPOSED. | none |
| DW-20 | A store that several server processes share for duplicate memory and the audit write lock. | `docs/11-reliability/recovery-evidence.md` ("Open items"). | S07 build decides storage | The app runs as one process. | FM-06 |
| DW-21 | A run of `make` on this machine, including `make security` and `make evidence`. | `Makefile`; `docs/13-security-validation/evidence.md` (Make not installed). | S05-13 Half B, S09 | `make` is not installed. `scripts/evidence.ps1` ran instead. The Linux script ran through `make evidence` in a container at S04-07 and in GitHub at S05-13. | S09-4 |
| DW-22 | `terraform apply`, and runs on macOS and Python 3.10. | `docs/05-iac/evidence.md`. | S04-05 | The packet has no cloud account (contract "Production access"). macOS and Python 3.10 were not run. | none |
| DW-23 | A commit and a push of the refreshed `evidence/` folder and the S09 files. | This stage. | S09 | The agent does not commit. Mangesh (FDE) commits. | S09-1 |
| DW-24 | Written defence answers and a slide outline. | `Execution Plan.md` Phase 10; `../Project_Intent.md` section 3.3. | S10 | S10 has not run. `docs/defence/` does not exist. | none |
| DW-25 | Optional moonshots: Decision Provenance Engine, AI Governance Gateway, Self-Generating Evidence Pack, Continuous Red-Team Harness. | `Execution Plan.md` Phase 11. | After S10 | Optional. Not started. | none |
| DW-26 | A written exception for the three routes outside the list in contract row 2. | `docs/15-readiness/operating-contract-check.md`. | S09 | The owner has not written one. | S09-5 |

## 2. The 13 items kept deferred by ADR 0002 and ADR 0003

The list comes from `docs/02-baseline/S05R_Decisions.md`. These ids are the S05R decision numbers. They are a different list from the D numbers in the second-model comparison.

| S05R id | Item | Revisit when |
|---|---|---|
| D-01 | Names for the checks a release must pass. | Stage S09. S09 may not add a control, so it waits. |
| D-02 | Audit entries for granting and using a waiver. | Only if a waiver feature is built. |
| D-04 | A narrower permission to read one audit case. | More people than the admin need audit access. |
| D-05 | Four more facts on the audit row. | The final action was built in S07. The other three wait. |
| D-09 | Catching instructions hidden inside an allowed field. | Real data or a real model arrives. |
| D-10 | A version number for the prompt wording. | The wording changes. |
| D-11 | How many seconds the model may take. | A real model is measured. |
| D-14 | A measure of how often the model path is shut off. | A dashboard exists. |
| D-15 | Lists of model names and risk levels. | A real model is chosen. |
| D-17 | Extra alarm fields allowed in a prompt. | A batch summary is designed. |
| D-18 | Four more fields on the audit row for cost grouping. | The feature that needs each one is built. |
| D-19 | A saved place for the count of damaged rows. | A dashboard exists (S05R names the S09 dashboard). |
| D-20 | The MAESTRO list. | The course gives the definition. |

## 3. Count check

| Group | Rows |
|---|---|
| Section 1 | 26 |
| Section 2 | 13 |
| Total | 39 |

