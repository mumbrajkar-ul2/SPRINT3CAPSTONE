# Project acronyms

| Field | Value |
|---|---|
| Stage | Reader guide. Written while S04-03 Half A was in progress. Updated on 2026-10-12 after S05-13, S05-14, and S05R. |
| Date / version | 2026-10-12, v1.3. v1.0 (2026-10-10) covered S04-03 Half A. v1.1 added the labels from S04-03 Half B through S04-07 Half B, and corrected five rows that the later stages made out of date (`OPA`, `CI`, `IaC`, `SBOM`, and the comment rows for `main.tf` and `access.rego`). v1.2 added the labels from S04-08 through S04-12 Half B, and updated the rows for `EDUCATIONAL`, `HOLD_FOR_REVIEW`, `BLOCK`, `SLO`, and the comment rows for `ai_gateway.py` and `audit.py`. v1.3 adds the labels from S05-13 (security validation), S05-14 (audit chain), and S05R (semantic layer revision to version `1.1.0`). It also corrects the rows for `CI`, `PATH`, `Rego`, `TA-xx`, `AC-`, `S05R`, the scan codes, and the YAML prefix table. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | Current for the files on disk after S05R. Stage ids S06 and later have not run, so no label from them is listed. A later stage that adds a new short code should add a row here. |
| Evidence sources | Documents under the project root and `06-telecom-service-network-incident-ops/docs/`; `playbook/`; `semantic-layer/README.md`; comments in `apps/`, `etl/`, `legacy/`, `policy/opa/`, `infra/terraform/`, `scripts/`, `Dockerfile`, and `semantic-layer/`. v1.1 also read `docs/04-secrets/`, `docs/05-iac/`, `docs/06-policy/`, `docs/07-cicd/`, `policy/tests/fixtures/`, and `playbook/STATUS.md`. v1.2 also read `docs/08-observability/`, `docs/09-ai-guardrails/`, `docs/10-performance/`, `docs/11-reliability/`, `docs/12-finops/`, `docs/runbooks/`, `apps/api/services/breaker.py`, `apps/api/services/dedupe.py`, and `.env.example`. v1.3 also read `docs/13-security-validation/`, `docs/14-audit/`, `docs/02-baseline/semantic-layer-revision.md`, `apps/api/services/audit_query.py`, `scripts/check_junit_no_skips.py`, `evidence/ruff.json`, `evidence/bandit.json`, `evidence/pip-audit.json`, and the ten fixture files added since v1.2. The synthetic CSV files and the chat transcript were left out of the scan. |
| Assumptions | A sample id such as `DEV-00013` is one row of a prefix. This file lists the prefix once. |
| Unresolved issues | `security/threat-model.md` names STRIDE/MAESTRO and does not spell those letters out. The letters of MAESTRO are Unknown in this repo. |
| Residual risks | Two lists can share a letter. `R07` is a risk. `R7` is a review check. Since v1.1, six more pairs share a label: `BL-01` (identity and CI/CD), `CM-01` (secrets and IaC), `H1` (a Half B run and a HOLD row), `R1` (a setup run and a review check), `AI-01` (a fixture and the words AI), and `OS-01` (a fixture and the letters OS). The tables below say which file each one lives in. Since v1.2, four more labels are shared: `PB-xx` (identity backlog and performance baseline), `HB-xx` (S04-06 Half B and S04-10 Half B), `DR-xx` (dependency register and reliability drills), and `B1` to `B9` (AI outcome rows and trust boundaries). The `D-1` to `D-7` decisions in `docs/11-reliability/` look like `D1` to `D8`, the hand-back ids, but they are a different list. Since v1.3, more labels are shared: `EV-xx` (S04-09 Half B and S05-13), `R3` to `R7` (S05-14 probe runs and review checks), `D-01` to `D-20` (S05R deferred items, with a leading zero) and `D-1` to `D-7` (reliability decisions), `SB-xx` (the S05-13 security backlog) and `BL-xx` (rows of the CI/CD backlog that the security backlog repeats), and `AR-xx` with `AR-Rx` (S05-14 findings and risks). The S05-13 file `docs/13-security-validation/remediation-backlog.md` uses both `SB-xx` and `BL-xx`. |

## What this file is

This file says what each short label means. A short label is a few letters, sometimes with a number, that stands in for a longer name. The words below are the ones already used in the documents and in the code comments.

This file adds no new id. The YAML ids in `semantic-layer/` stay the source for persona, role, action, resource, purpose, scope, and risk.

## Document row ids

These labels number a row in one file. The letters say which list. The number says which row.

| Label | What the row is | Where it lives | Range on disk now |
|---|---|---|---|
| `Fxx` | A defect to change. Example: `F03` is the `clinician` role on the record route. | `docs/02-baseline/defect-list.md` | `F01` to `F23` |
| `Kxx` | Current behaviour to leave in place until a named stage changes it. Example: `K02` is a read of `REC-0001` for an allowed role. | `docs/02-baseline/defect-list.md`, Keep table | `K01` to `K08` |
| `Rxx` | A risk in the discovery register. Example: `R07` is the `clinician` role. `R16` is the missing role header. | `docs/01-discovery/brownfield-risk-register.md` | `R01` to `R24` |
| `TA-xx` | One allow row in the target access matrix. Example: `TA-01` is `persona.noc_operator` reading a device. `TA-35` was added in S05-14 Half B. It lets `role.admin` read `resource.audit_log` for `purpose.audit_review`. Mangesh accepted it on 2026-10-12. | `docs/03-identity/target-access-matrix.md`, `docs/14-audit/audit-read-access-design.md`, `policy/opa/policy_data.json` | `TA-01` to `TA-35` (35 rows in `policy_data.json`) |
| `TA-Fx` | A finding about that matrix. Example: `TA-F5` is the note that the live header for the NOC reader is `operator`. | Same file, Findings table | `TA-F1` to `TA-F5` |
| `CR-xx` | A finding about who can reach the API or the data today. | `docs/03-identity/current-role-matrix.md` | `CR-01` to `CR-07` |
| `PB-xx` | One cut on the privilege-reduction backlog. | `docs/03-identity/privilege-reduction-backlog.md` | `PB-01` to `PB-04` |
| `BL-xx` | A finding about that backlog. | Same file, Findings table | `BL-01`, `BL-02` |
| `NA-xx` | One case in the negative access test plan. | `docs/03-identity/negative-access-test-plan.md` | `NA-01` to `NA-06` |
| `NT-xx` | A finding about that test plan. | Same file, Findings table | `NT-01` to `NT-03` |
| `PI-xx` | A finding about the policy input JSON. | `docs/03-identity/policy-input-model.md` | `PI-01` to `PI-03` |
| `SI-xx` | One secret, or one place that holds none, in the secrets inventory. The finding with the same number sits in the same file. Example: `SI-01` is the shared database password assigned in `legacy/reconcile_legacy.py`. `SI-08` says `apps/` holds no password, key, or token constant. | `docs/04-secrets/secrets-inventory.md` | `SI-01` to `SI-08` |
| `RP-xx` | One step in the plan to remove a secret. It has the same number as its `SI-xx` row. Example: `RP-01` moves the password to the environment. | `docs/04-secrets/remediation-plan.md` | `RP-01` to `RP-08` |
| `RE-xx` | A finding about the rotation evidence plan. Example: `RE-03` says it is Unknown whether `automation_service` is a shared account. | `docs/04-secrets/rotation-evidence-plan.md` | `RE-01` to `RE-03` |
| `CM-xx` (secrets) | A finding about the cleaned configuration model. Example: `CM-01` says the example file will hold names and the placeholder `CHANGE_ME`. | `docs/04-secrets/cleaned-configuration-model.md` | `CM-01` to `CM-03` |
| `SF-xx` | A finding about how sensitive fields are handled. Example: `SF-01` says the two device fields `mgmt_ip` and `credential_profile` are marked sensitive and stay out of a prompt. | `docs/04-secrets/sensitive-field-handling-checklist.md` | `SF-01` to `SF-04` |
| `CO-xx` | One setting in the configuration ownership map. Example: `CO-01` is `DATABASE_URL` in `.env.example`. | `docs/05-iac/configuration-ownership-map.md` | `CO-01` to `CO-38` |
| `CM-xx` (IaC) | A finding about that map. Example: `CM-02` says no code loads a `.env` file. This is a different list from the secrets `CM-xx`. | Same file, Findings table | `CM-01` to `CM-05` |
| `DD-xx` | A finding about the deployment dependency list. Example: `DD-01` says the test run needs one package that no file pinned (`httpx`, now pinned). | `docs/05-iac/deployment-dependency-list.md` | `DD-01` to `DD-04` |
| `IG-xx` | One gap in the infrastructure-as-code report. Example: `IG-01` is that `main.tf` wrote the shared user name into a text file. `IG-09` is the workflow file sitting below the git root. | `docs/05-iac/iac-gap-report.md` | `IG-01` to `IG-14` |
| `Hx` | One check that S04-05 Half B ran. Example: `H1` ran `bootstrap.ps1` from a fresh folder copy and got `15 passed`. | `docs/05-iac/evidence.md` | `H1` to `H8` |
| `Rx` (setup run) | One run of the setup steps on a fresh copy. Example: `R1` is a Windows copy that failed with 3 collection errors, because `httpx` was not pinned. | `docs/05-iac/reproducible-setup-guide.md` | `R1` to `R6` |
| `PC-xx` | A finding in the policy catalogue. Example: `PC-01` says only the access area had policy code when S04-06 Half A was written. | `docs/06-policy/policy-catalogue.md` | `PC-01` to `PC-07` |
| `B1` to `B10`, `H1` to `H4`, `O1` to `O3` | A row of the AI action outcome table. `B` rows give BLOCK. `H` rows give HOLD_FOR_REVIEW. `O` rows say what the action decides when no `B` or `H` row matched. `H1` is the row "`timeout_hit` is true". The `H` here is a different list from the `Hx` runs above. | `docs/06-policy/ai-action-policy-design.md`, comments in `policy/opa/ai_action.rego` | `B1` to `B10`, `H1` to `H4`, `O1` to `O3` |
| `Wxx` | One worked combination of AI inputs, with the outcome row it reaches. Example: `W1` is `action.summarize` by `persona.noc_operator`, which gives RECOMMEND_ONLY through row `O1`. | `docs/06-policy/ai-action-policy-design.md` | `W1` to `W17` |
| `AA-xx` | A finding about the AI action policy design. Example: `AA-01` says the playbook wording lets a caller skip approval by sending `approval_required` as false. | Same file, Findings table | `AA-01` to `AA-09` |
| `EX-xx` | A finding about the exception handling model. Example: `EX-01` says every business rule is set aside today without a record. | `docs/06-policy/exception-handling-model.md` | `EX-01` to `EX-06` |
| `AC-`, `AI-`, `DU-`, `OS-`, `PR-` plus a number | One example input (a fixture). `AC` is access, `AI` is AI approval, `DU` is data use, `OS` is operational safety, `PR` is production readiness. Each id names a JSON file. Example: `AC-01` is `ac-01-allow-noc-operator-reads-device.json`. | `docs/06-policy/example-inputs.md`; files in `policy/tests/fixtures/` | `AC-01` to `AC-07`, `AI-01` to `AI-10`, `DU-01` to `DU-04`, `OS-01`, `OS-02`, `PR-01`, `PR-02` (25 files). `AC-06` is `ac-06-allow-admin-reads-audit-log.json`. `AC-07` is `ac-07-deny-operator-reads-audit-log.json`. |
| `EI-xx` | A finding about those example inputs. Example: `EI-01` says every policy area has at least one allow fixture and one deny fixture. | `docs/06-policy/example-inputs.md`, Findings table | `EI-01` to `EI-04` |
| `HB-xx` | A finding that S04-06 Half B recorded. Example: `HB-01` says the three gateway flags are placeholders, so the policy reports `forbidden_field_in_prompt` as false. | `docs/06-policy/evidence.md` | `HB-01` to `HB-09` |
| `DR-xx` | One dependency in the dependency risk register. Example: `DR-01` is `fastapi` 0.115.0. | `docs/07-cicd/dependency-risk-register.md` | `DR-01` to `DR-22` |
| `DR-Fx` | A finding about that register. Example: `DR-F4` says FastAPI 0.115.0 caps `starlette` below 0.39.0. | Same file, Findings table | `DR-F1` to `DR-F7` |
| `CI-xx` | A finding about the CI workflow. Example: `CI-01` says the workflow file sat in a folder GitHub does not read. Half B moved it to the repo root. | `docs/07-cicd/pipeline-improvement-plan.md` | `CI-01` to `CI-13` |
| `BL-xx` (CI/CD) | One item on the pipeline backlog. Example: `BL-10` is the 12 ruff findings. This is a different list from the identity `BL-xx` above. | Same file, Backlog table | `BL-01` to `BL-13` |
| `LS-xx` | A finding about the audit log schema. | `docs/08-observability/log-schema.md`, Findings table | `LS-01` to `LS-02` |
| `LS-Qx` | An open question for S03 that the log schema raised. Example: `LS-Q7` says `record_id` and the reason list are not on the new audit row. | Same file | `LS-Q1` to `LS-Q7` |
| `TD-xx` | A finding about the trace design. | `docs/08-observability/trace-design.md` | `TD-01` to `TD-04` |
| `MC-xx` | A finding about the metric catalogue. | `docs/08-observability/metric-catalogue.md` | `MC-01` to `MC-02` |
| `SL-xx` | A finding about the SLO proposal. This is a different list from the word `SL` in the capitals table. | `docs/08-observability/slo-proposal.md` | `SL-01` to `SL-02` |
| `DS-xx` | A finding about the dashboard sketch. | `docs/08-observability/dashboard-sketch.md` | `DS-01` to `DS-02` |
| `IR-xx` | A finding about the rebuild of one incident from stored rows. | `docs/08-observability/incident-reconstruction.md` | `IR-01` to `IR-03` |
| `AIR-xx` | One AI risk, with its control and its YAML id. Example: `AIR-01` is instruction text inside `hostname` or `vendor`, which are on the prompt allow list. | `docs/09-ai-guardrails/ai-risk-register.md` | `AIR-01` to `AIR-09` |
| `GR-xx` | One guardrail case. Each control from the risk register has one. The test names carry the number, such as `test_gr05_...`. Example: `GR-01` is instruction text in `hostname`. `GR-02` is `mgmt_ip` in the prompt. `GR-03` is a true stale topology flag. `GR-04` is malformed JSON from the model. `GR-05` is a timeout. `GR-06` is a caller with no recommend permission. `GR-07` is an execute verb in the output. | `docs/09-ai-guardrails/guardrail-test-pack.md`, `tests/ai/test_guardrails.py` | `GR-01` to `GR-11` |
| `B1` to `B9` (trust boundary) | One arrow in the trust boundary diagram, where a check sits. `B1` is the caller reaching the route. `B9` is the four gates before any device change. This is a different list from the outcome-table `B` rows. | `docs/09-ai-guardrails/trust-boundary-diagram.md` | `B1` to `B9` |
| `TB-xx` | A finding about the trust boundary diagram. | Same file | `TB-01` to `TB-03` |
| `AW-xx` | A finding about the approval workflow. Example: `AW-01` says three human jobs sit on three different rows, and only the live-change job is confirmed. | `docs/09-ai-guardrails/approval-workflow.md` | `AW-01` to `AW-03` |
| `UO-xx` | A finding about unsafe output handling. Example: `UO-01` says a failure body has a null summary. `UO-02` chose BLOCK for a true stale flag. | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` | `UO-01` to `UO-03` |
| `MP-xx` | A finding about model provenance, the fields that record which model answered. | `docs/09-ai-guardrails/model-provenance-design.md` | `MP-01` to `MP-03` |
| `GT-xx` | A finding about the guardrail test pack. | `docs/09-ai-guardrails/guardrail-test-pack.md` | `GT-01` to `GT-02` |
| `EV-xx` | A finding that S04-09 Half B recorded. Example: `EV-08` says the 10-second timeout was never run against a real model. | `docs/09-ai-guardrails/evidence.md` | `EV-01` to `EV-08` |
| `BN-xx` | One bottleneck, with a measured cost. Example: `BN-01` is the policy check searching the PATH for `opa` on every call. | `docs/10-performance/bottleneck-list.md` | `BN-01` to `BN-07` |
| `PB-xx` (performance) | A finding about the performance baseline. This is a different list from the identity `PB-xx` above. | `docs/10-performance/performance-baseline.md` | `PB-01` to `PB-06` |
| `DA-xx` | A finding about how the code reads data. | `docs/10-performance/data-access-findings.md` | `DA-01` to `DA-06` |
| `SR-xx` | One scaling recommendation. Example: `SR-01` loads `devices.csv` once and indexes its rows by `device_id`. Half B built `SR-01`. | `docs/10-performance/scaling-recommendations.md` | `SR-01` to `SR-05` |
| `HB-xx` (performance) | A finding that S04-10 Half B recorded. This is a different list from the S04-06 `HB-xx` above. | `docs/10-performance/evidence.md` | `HB-01` to `HB-04` |
| `FM-xx` | One failure mode. Example: `FM-03` is an AI call that times out. `FM-13` is several threads writing the audit log at once. | `docs/11-reliability/failure-mode-catalogue.md` | `FM-01` to `FM-15` |
| `RF-xx` | A finding in the failure mode catalogue. Example: `RF-01` says the audit log loses rows when threads write at once. | Same file, Findings table | `RF-01` to `RF-09` |
| `OQ-xx` | An open question for S03 from the reliability documents. | `docs/11-reliability/` | `OQ-1` to `OQ-7` |
| `D-x` | A decision taken before S04-11 Half B. Example: `D-1` says a true stale flag gives BLOCK and a blank flag stays HOLD_FOR_REVIEW. | `docs/11-reliability/failure-mode-catalogue.md` | `D-1` to `D-7` |
| `Px` | One read-only probe in the S04-11 Half A script. It calls the app in memory with one thing broken. Example: `P9` is the audit write test that lost 109, 71, and 85 of 2000 rows. | `docs/11-reliability/probe_half_a.py` | `P1` to `P11` |
| `DM-xx` | A finding about the degraded-mode design. Example: `DM-01` says `/health` and `/records/{id}` continue when the AI path is down. | `docs/11-reliability/degraded-mode-design.md` | `DM-01` to `DM-06` |
| `ID-xx` | A finding about the idempotency plan. Example: `ID-01` says a retried summary call repeats one model call and one audit row, and repeats no business row. | `docs/11-reliability/idempotency-plan.md` | `ID-01` to `ID-06` |
| `RB-xx` | A finding about the retry and circuit breaker strategy. | `docs/11-reliability/retry-and-circuit-breaker-strategy.md` | `RB-01` to `RB-05` |
| `DR-x` (drill) | One recovery drill that S04-11 Half B ran. Example: `DR-1` is a request with no correlation id. This is a different list from the dependency `DR-xx` above. | `docs/11-reliability/recovery-evidence.md` | `DR-1` to `DR-6` |
| `AB-xx` | A finding about the AI cost baseline. | `docs/12-finops/ai-cost-baseline.md` | `AB-01` to `AB-06` |
| `CW-xx` | A finding about cost per workflow. | `docs/12-finops/cost-per-workflow.md` | `CW-01` to `CW-05` |
| `RC-xx` | A finding about retry cost. | `docs/12-finops/retry-cost-analysis.md` | `RC-01` to `RC-04` |
| `OB-xx` | One item in the cost optimization backlog. Example: `OB-01` caches repeated prompts by `prompt_hash`. Its cache lifetime is decided at 300 seconds, to be built in S07. `OB-05` is the stop before the model, already built. | `docs/12-finops/optimization-backlog.md` | `OB-01` to `OB-05` |
| `OB-Fx` | A finding about that backlog. | Same file | `OB-F1` to `OB-F2` |
| `FD-xx` | A finding about the FinOps dashboard fields. | `docs/12-finops/finops-dashboard-fields.md` | `FD-01` to `FD-04` |
| `FB-xx` | A finding that S04-12 Half B recorded. | `docs/12-finops/evidence.md` | `FB-01` to `FB-06` |
| `SV-xx` | One security test requirement: a threat, the test that covers it, and what the test must show. Example: `SV-01` is a role with no matrix row reading a device record. `SV-27` is a security test that skips while the stage still exits 0. | `docs/13-security-validation/security-test-suite-plan.md`, `docs/13-security-validation/abuse-case-evidence.md` | `SV-01` to `SV-27` |
| `SVF-xx` | A finding about that test plan. Example: `SVF-09` says the secret scan reads no file when the repo sits in a folder named `docs`, `venv`, `.venv`, or `.git`. | `docs/13-security-validation/security-test-suite-plan.md` | `SVF-01` to `SVF-09` |
| `AE-xx` | A finding from the abuse case run. Example: `AE-01` says 19 of 20 rows with a test passed and the 20th skipped. | `docs/13-security-validation/abuse-case-evidence.md` | `AE-01` to `AE-04` |
| `NG-xx` | One negative test design. Example: `NG-01` is `write_event` refusing an empty correlation id. `NG-04` is the secret scan finding a planted secret. | `docs/13-security-validation/negative-tests.md` | `NG-01` to `NG-04` |
| `NG-Fx` | A finding about those designs. | Same file | `NG-F1`, `NG-F2` |
| `SC-xx` | A finding about the scanning checklist. Example: `SC-05` says the secret scan has three blind spots. | `docs/13-security-validation/scanning-checklist.md` | `SC-01` to `SC-05` |
| `SB-xx` | One row of the security remediation backlog. Example: `SB-01` is a call with no role header being treated as `operator`. `SB-10` is a security test that skips without failing the build. `SB-21` is the workflow runner image, pinned to `ubuntu-24.04` on 2026-10-12. | `docs/13-security-validation/remediation-backlog.md` | `SB-01` to `SB-21` |
| `EV-xx` (security) | A finding that S05-13 Half B recorded. Example: `EV-01` says a record read takes a median 150 ms when the app starts `opa` for each decision, and 10 ms with the Python copy. This is a different list from the S04-09 `EV-xx` above. | `docs/13-security-validation/evidence.md` | `EV-01` to `EV-09` |
| `AG-xx` | A finding in the audit gap report. Example: `AG-01` says 96 of 240 lines had 3 keys and no `correlation_id`. `AG-08` says `role` and `actor` hold a claim and not a proven fact. | `docs/14-audit/audit-gap-report.md` | `AG-01` to `AG-08` |
| `DP-xx` | A finding about the decision provenance model. Example: `DP-01` says 15 of 24 facts have a column on the row and 9 do not. | `docs/14-audit/decision-provenance-model.md` | `DP-01` to `DP-02` |
| `AR-xx` | A finding about audit read access. Example: `AR-01` says no role could read the audit log before `TA-35`. | `docs/14-audit/audit-read-access-design.md` | `AR-01` to `AR-03` |
| `AR-Rx` | A risk of the audit read route. Example: `AR-R1` says any caller can type `admin`, so the row is only as strong as the header. | Same file | `AR-R1` to `AR-R4` |
| `BA-xx` | A finding about the before-and-after audit row. Example: `BA-01` says the row grew from 3 keys to 15. | `docs/14-audit/before-and-after-audit-example.md` | `BA-01` to `BA-03` |
| `EC-xx` | A finding about the one-case evidence chain. | `docs/14-audit/evidence-chain-one-case.md` | `EC-01` to `EC-03` |
| `CE-xx` | A finding about the compliance evidence mapping. Example: `CE-01` says all five control areas have stored evidence with a test name. | `docs/14-audit/compliance-evidence-mapping.md` | `CE-01` to `CE-03` |
| `Rx` (audit probe) | One call in the S05-14 Half B run against the audit route. Example: `R3` is `operator` asking for an existing case and getting 403. `R7` is `admin` sending an id of 129 characters and getting 400. | `docs/14-audit/evidence.md` | `R3` to `R7` |
| `C-xx` | One row of the S05R collection table. It names a place where a design, policy, test, or comment asked for a term the YAML lacked, and the decision taken. | `docs/02-baseline/semantic-layer-revision.md` | `C-01` to `C-65` |
| `D-xx` (deferred) | One question that S05R left open with owner Team-Force. It has a leading zero. This is a different list from the reliability `D-x` decisions and from the hand-back ids `D0` to `D8`. | `docs/02-baseline/semantic-layer-revision.md` | `D-01` to `D-20` |

Worked example. `F03`, `R07`, and `CR-01` all talk about the header word `clinician`. `F03` is the defect row. `R07` is the risk row. `CR-01` is the current-access finding. `TA-01` is a different fact: the target allow for `persona.noc_operator` to read a device. `NA-02` is the test that will check the `clinician` deny after Half B.

Worked example for the shared labels. `BL-01` in `docs/03-identity/privilege-reduction-backlog.md` is a finding about the privilege backlog. `BL-01` in `docs/07-cicd/pipeline-improvement-plan.md` is "move the workflow to the repo root". `CM-01` in `docs/04-secrets/` is about the example file. `CM-01` in `docs/05-iac/configuration-ownership-map.md` says the example file does not list the name the legacy script reads. Always read the file name next to the label.

The review file uses the letter R for a different list. `R1`, `R7`, and `R14.7` in `docs/02-baseline/semantic-layer-review.md` are review checks. `R07` in the risk register is a risk. The review number has no leading zero. The risk number has two digits.

`A1`, `A5`, and the other `A` numbers in that same review are advisories. An advisory is a note. It does not by itself fail the review.

`Fix 1` in `docs/02-baseline/semantic-layer-fixes.md` is a repair step from a failed review. It is a different list from `F01`.

## Hand-back ids

`playbook/README.md` names the packets you hand back. `Project_Intent.md` names `D0`.

| Label | What it is |
|---|---|
| `D0` | This assignment's locked brief: `Project_Intent.md`. |
| `D1` | The six discovery files under `docs/01-discovery/`. |
| `D2` | The baseline, the defect list, and the characterization tests. |
| `D3` | The semantic layer, after review, including the later revision. |
| `D4` | The Phase 4 control folders, `docs/03-identity/` through `docs/12-finops/`, each with a design half and a code half. |
| `D5` | The PRD and its traceability file. |
| `D6` | The running demo of one flow that ends in a human decision. |
| `D7` | The second-model comparison. |
| `D8` | The filled production evidence pack and the readiness note. |

## Stage ids

A stage id starts with `S`. The playbook file of the same name holds the prompt.

| Id | What that stage writes or decides |
|---|---|
| `S00` | Setup and replay. |
| `S0B` | The operating contract, the cost envelope, and the crosswalk. The `B` marks the contract phase before discovery. |
| `S01` | The discovery dossier. |
| `S02` | The behavioural baseline and the defect list. |
| `S2Q` | AI versus no AI, one row per capability. The `Q` marks that qualification. |
| `S03` | The semantic-layer YAML. |
| `S03R` | The review of that YAML. The `R` marks a review. |
| `S03F` | The fix pass after a failed review. The `F` marks the fixes. |
| `S04-03` to `S04-12` | Phase 4. The number after the hyphen is the challenge number, 3 through 12. |
| `S05-13` | Phase 5, challenge 13. Security validation: a security test suite plan, abuse cases, negative tests, a scanning checklist, and a remediation backlog. Half B added the skip guard `scripts/check_junit_no_skips.py` and the `security` test marker. |
| `S05-14` | Phase 5, challenge 14. The audit chain: gaps in the audit row, the decision provenance model, compliance evidence mapping, and the read route `GET /audit/{correlation_id}`. Half B added `TA-35`. |
| `S05R` | The revision that folds open questions into the YAML and raises the version. It ran on 2026-10-12 and raised the layer from `1.0.0` to `1.1.0`: 92 ids added, 0 removed, 2 deprecated. The result is CONDITIONAL PASS, with 20 deferred questions. The record is `docs/02-baseline/semantic-layer-revision.md`. |
| `S06` | The PRD. |
| `S06R` | The review of the PRD. |
| `S07` | The application and the demo. |
| `S08` | The second model and the comparison. |
| `S09` | Readiness and the evidence pack. |
| `S10` | The defence. |

`Half A` is the design half of a Phase 4 or Phase 5 stage. It writes documents and leaves the code as it is. `Half B` is the code half. It starts after you reply `Half A accepted` in that stage's chat.

## Codes from the scan tools

S04-07 Half B ran three scan tools. Each prints its own code for a finding. These codes are the tools' codes, not ids of this project. They appear in `evidence/ruff.json`, `evidence/bandit.json`, and `evidence/pip-audit.json`, and in `docs/07-cicd/`.

| Code | What it means | Where it shows up |
|---|---|---|
| `I001` | `ruff`: imports are not in sorted order. 5 files in the 2026-10-12 run. | `ruff.json`, backlog `BL-10` |
| `UP045` | `ruff`: `Optional[X]` is written the old way. `apps/api/main.py:83`. | Same |
| `F401` | `ruff`: an import is never used. The two findings in `apps/api/services/ai_gateway.py` were in the S04-07 run. They are gone from `ruff.json` now. | `docs/07-cicd/`, `docs/13-security-validation/evidence.md` `EV-06` |
| `DTZ003` | `ruff`: `datetime.utcnow()` returns a time with no time zone. `apps/api/services/audit.py:87`. | `ruff.json` |
| `SIM114` | `ruff`: two `if` branches can be one branch with `or`. `apps/api/services/breaker.py:165`. New since S04-11. | Same |
| `C401` | `ruff`: a generator is turned into a set in a longer way than needed. `semantic-layer/tests/test_semantic_layer.py:344`. | Same |
| `SIM103` | `ruff`: an `if` that returns True or False can return the test itself. | Same |
| `PIE810` | `ruff`: several `startswith` calls can be one call with a tuple. | Same |
| `EXE002` | `ruff`: a file is marked executable and has no `#!` first line. It appeared only when a Windows folder was mounted into Docker, which marks every file executable. Git stores these files as mode 644, so CI does not see it. | `evidence/` run record, `docs/07-cicd/evidence.md` |
| `B404` | `bandit`: the code imports `subprocess`. `apps/api/services/policy.py:25`. | `bandit.json`, backlog `BL-12` |
| `B603` | `bandit`: the code calls `subprocess.run` with a list. `apps/api/services/policy.py:86`. | Same |
| `PYSEC-yyyy-nnn` | `pip-audit`: an advisory id from the Python package advisory database. 9 unique ids on 3 packages (`pytest`, `python-dotenv`, `starlette`), listed 18 times in `pip-audit.json`. Example: `PYSEC-2026-1845`. | `pip-audit.json`, backlog `BL-11` |

`LOW` and `HIGH` in `bandit.json` are severity and confidence words. Both bandit results are LOW severity with HIGH confidence.

The 2026-10-12 run of `scripts\evidence.ps1` found 11 `ruff` findings, 2 `bandit` results, and 9 unique `pip-audit` advisories. `evidence/exit-codes.txt` shows `lint=1`, `pip_audit=1`, and `bandit=1`. The other eight stages exit 0.

## Words written in capitals

Each row says what the letters stand for in this project, then where they show up.

| Letters | What they mean here | Where they show up |
|---|---|---|
| `AI` | A model that writes a summary or a recommendation. | The summary route, `ai_gateway.py`, and the qualification file. |
| `GenAI` | A language model that writes new text from a prompt. | `docs/02-baseline/ai-qualification.md`. |
| `ML` | A model trained on past examples to predict a number or a class. The qualification file calls this classical ML. | `ai-qualification.md`. |
| `API` | The service other programs call. In this repo that service is `apps/api/`. | `main.py` and the docs that describe the three routes. |
| `HTTP` | The web call and its status number. A refused role today still returns HTTP 200. | Replay log, defect list. |
| `GET` | A read call. `GET /records/{id}` reads a device row. | `main.py`. |
| `POST` | A call that asks the service to do a step. `POST /ai/summarize/{id}` asks for a summary. | `main.py`. |
| `JSON` | A text shape for an object. Audit lines and the policy input use it. | `audit.py`, `docs/03-identity/policy-input-model.md`. |
| `JSONL` | A file with one JSON object on each line. The event log is `data/synthetic/events.jsonl`. | Cost envelope, discovery notes. |
| `YAML` | The text format of the files under `semantic-layer/`. | `semantic-layer/`. |
| `CSV` | A table stored as text with commas. The six files under `data/synthetic/` are CSV files. | Domain spec, baseline. |
| `URL` | A web address. `.env.example` holds `DATABASE_URL`. The value is a secret and is not copied here. | `.env.example`, component inventory. A test comment in `semantic-layer/tests/test_semantic_layer.py` says a URL may embed a password. |
| `DB` | Database. The legacy script assigns `SHARED_DB_USER` and `SHARED_DB_PASSWORD`. The reconcile function counts a CSV file. | `legacy/reconcile_legacy.py`. |
| `OPA` | Open Policy Agent. In this repo it is the policy files `policy/opa/access.rego` and `policy/opa/ai_action.rego`, with one shared data file, `policy/opa/policy_data.json`. Since S04-06 Half B the API calls the policy. `apps/api/services/policy.py` runs `opa eval` when the `opa` binary is on the PATH. Otherwise it applies the same table in Python. The setting `POLICY_ENGINE` can force `python` or `opa`. The tests under `tests/` set the Python copy by default (`tests/conftest.py`). `opa test` passes 32 of 32 on 2026-10-12. | `access.rego`, `ai_action.rego`, `policy.py`, `docs/06-policy/`, `docs/13-security-validation/evidence.md`. |
| `CI` | The automated check on a change. Since S04-07 Half B, `.github/workflows/ci.yml` sits at the repo root and runs one step per stage: install, lint, three test groups, the secret-pattern test, SBOM, `pip-audit`, `bandit`, checksums, and an upload of `evidence/`. It has run on GitHub on the image `ubuntu-24.04`, pinned on 2026-10-12 (backlog `SB-21`). The job is red because `lint`, `pip_audit`, and `bandit` exit 1 on the findings listed above. The skip guard `scripts/check_junit_no_skips.py` fails the security stage when any security test is skipped. | Project Intent section 4.3, the workflow file, `docs/07-cicd/`. |
| `CI/CD` | The path that builds, tests, and releases the software. Challenge 7. `CD` is the release half of that path. | `How the product spine addresses the 16 challenges - plain speak.md`, `playbook/S04-07-cicd.md`. |
| `ETL` | The batch job that reads a file, counts rows, and writes a count. The guide's words are: extract data, change it, and load it. The comment in `etl/run_daily_batch.py` says malformed rows are counted and left in the file. | `etl/run_daily_batch.py`, the spine note. |
| `IaC` | Infrastructure as code. The Terraform file `infra/terraform/main.tf` builds no cloud resource. S04-05 Half B corrected it to write one local settings file with no secret. The first comment of the file no longer uses these letters. | `infra/terraform/main.tf`, `docs/05-iac/`, `playbook/S04-05-iac.md`. |
| `ADR` | Architecture decision record. `docs/ADR/0001-partial-modernization.md` is ADR 0001. `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` is ADR 0002. It records the owner's decisions on the S05R open items and raised the semantic layer to `1.1.1`. | That file. Project Intent uses the full words "Architecture Decision Record". |
| `PRD` | The product requirements document. Stage S06 writes it. | `playbook/S06-prd.md`. |
| `FDE` | Forward Deployed Engineer. `Project_Intent.md` says a Forward Deployed Engineer works at the customer site, uses AI under written rules, and leaves a system people can run and explain. Team-Force is the FDE team Mangesh belongs to. | `Project_Intent.md`, operating contract row 10. |
| `SLA` | The service promise on a circuit. The files use it in `sla_tier` and `sla_breach_risk`. | Domain spec, defect `F19`. |
| `SLO` | A stated target for the running service, such as how often a request finishes in time. The spine note calls this a service level objective. S04-08 Half A proposes three of them. Each number is PROPOSED, owner Team-Force, and none is a target in `metrics.yaml` yet. | `playbook/S04-08-observability.md`, `docs/08-observability/slo-proposal.md`. |
| `SBOM` | The list of libraries inside a build. The spine note calls this a software bill of materials. In this repo the file is `evidence/sbom.cdx.json`. It lists 22 packages in the CycloneDX format. | `playbook/S04-07-cicd.md`, `docs/07-cicd/sbom-recommendation.md`. |
| `UI` | The page a person opens. | `playbook/S07-application-and-demo.md`. |
| `HTML` | The text format of that page. | `playbook/S07-application-and-demo.md`. |
| `PDF` | The capture document for the semantic-layer file tree. | `semantic-layer/README.md`, the review. |
| `RBAC` | Access granted from a job role. | The spine note, in the identity challenge. |
| `ABAC` | Access granted from extra facts, such as purpose and risk. | The same spine note. |
| `NOC` | The network operations centre. `persona.noc_operator` is a person who works there. | `access-semantics.yaml`, Project Intent. |
| `SSH` | A remote login method named in the gap `static_ssh_credentials`. The discovery register found no `ssh` string in the Python files or in `devices.csv`. | Risk `R02`. |
| `OS` | The operating system of the machine that ran the replay. | `docs/00-setup/tool-versions.md`. |
| `SHA-256` | The hash function the semantic-layer build uses to show a generated file was not edited by hand. | `semantic-layer/README.md`. |
| `UUID` | An id that is unique without a central counter. The observability and reliability stages name it as one way to make a correlation id. | `playbook/S04-08-observability.md`, `playbook/S04-11-reliability.md`. |
| `IAM` | The login and permission system a production pack would name. The evidence-pack template uses the letters. This repo has no such system wired up. | `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md`. |
| `KPI` | A number the business watches. The spine note uses the letters for a measure tied to an outcome. | `How the product spine addresses the 16 challenges - plain speak.md`. |
| `STRIDE` | The threat-model file names STRIDE/MAESTRO and does not spell the letters. STRIDE is the usual six-part list: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. | `security/threat-model.md`. |
| `MAESTRO` | Named beside STRIDE in that same file. The file does not spell the letters. The expansion is Unknown here. | `security/threat-model.md`. |
| `SL` | A short name the review notes use for the folder `semantic-layer/`. | `docs/02-baseline/semantic-layer-review.md`. |
| `Rego` | The language of Open Policy Agent policy files. The two `.rego` files and the two `*_test.rego` files are written in it. 32 Rego tests pass (`opa test`, 2026-10-12). Two were added in S05-14 for `TA-35`. | `policy/opa/`, `policy/tests/`, `docs/06-policy/`. |
| `CycloneDX` | The file format of the SBOM. The tool `cyclonedx-py` writes version 1.6 here. | `evidence/sbom.cdx.json`, `docs/07-cicd/sbom-recommendation.md`. |
| `JUnit` | The XML test-result format that `pytest --junitxml` writes. Four files in `evidence/` use it: `junit-tests.xml`, `junit-semantic-layer.xml`, `junit-policy.xml`, and `junit-security.xml`. | `evidence/`, `docs/07-cicd/release-evidence-checklist.md`. |
| `XML` | A text format with nested tags. The JUnit result files are XML. | Same. |
| `PATH` | The list of folders the shell searches for a program. Before 2026-10-12, `opa` was not on the PATH on this Windows machine, so 2 policy tests skipped and `evidence.ps1` fell back to a Docker image. Now `opa` 1.21.1 is in `C:\Users\mange\tools\opa` on the user PATH, and no policy test skips. | `docs/06-policy/evidence.md`, `docs/07-cicd/evidence.md`, `docs/13-security-validation/evidence.md`. |
| `WSL` | Windows Subsystem for Linux. The S04-05 runs used a WSL Ubuntu 22.04 install for a Python 3.10 check. It had no `venv` module, so no virtual environment was made there. | `docs/05-iac/deployment-dependency-list.md`, `docs/05-iac/evidence.md`. |
| `UTC` | The time zone of the times in `evidence/run-info.txt`, such as `2026-10-11T20:32:21Z`. The audit `ts` field is also UTC. | `evidence/run-info.txt`, `docs/08-observability/log-schema.md`. |
| `FinOps` | Cost management for the AI calls. S04-12 counts tokens and cost units for each flow, each correlation chain, and each incident. The cost units are EDUCATIONAL. They are not money. | `playbook/S04-12-finops.md`, `docs/12-finops/`. |
| `p95` | The value that 95 of every 100 calls stay under. S04-12 Half B reports a p95 latency of 14 ms on the 17 model calls in the audit log. | `docs/12-finops/metrics_from_audit_output.txt`, `docs/12-finops/evidence.md`. |
| `KiB` | 1024 bytes. The performance documents give file sizes in KiB. | `docs/10-performance/`. |
| `UTF-8` | A way to store text as bytes. Before S04-11 Half B, one line that was not valid UTF-8 stopped the ETL run and lost the counts for every good row. Drill `DR-5` now holds that row aside and names it. | `docs/11-reliability/failure-mode-catalogue.md`, `docs/11-reliability/recovery-evidence.md`. |

## Outcome words and honesty labels

These are written in capitals. They are status words, not file-row ids.

| Word | What it means here |
|---|---|
| `RECOMMEND_ONLY` | Show the model text. Leave the stored row unchanged. |
| `HOLD_FOR_REVIEW` | Stop for a person. A timeout, a bad output shape, or a blank stale topology flag uses this outcome. A held call that never reached the model has `model`, `tokens`, and `latency_ms` empty in its audit row. |
| `BLOCK` | Stop the call before the model runs. A missing id or a true stale topology flag is a block. S04-09 Half B follows the YAML on this, and the playbook sentence that says HOLD_FOR_REVIEW was set aside. The audit log writes a block as a `policy.deny` row with `outcome` BLOCK. |
| `EXECUTE` | Carry out a live change. The model never has this outcome. The summary route never returns it. |
| `PASS` | The stage or the review check met its gate. |
| `CONDITIONAL PASS` | The stage met the gate with a named condition still open. |
| `BLOCKED` | A required piece is missing. The next stage waits. |
| `FAIL` | A review check did not pass. |
| `NOT APPLICABLE` | That review check does not apply to this packet. |
| `DONE` | A playbook or owner-decision row in `playbook/STATUS.md` that is finished. |
| `PROPOSED` | A design or a number the owner has not accepted in writing. Owner: Team-Force. |
| `PROVISIONAL` | A contract row the packet left open until the owner confirmed it. Operating contract v1.4 has no remaining provisional row. |
| `REAL` | A number or a file measured from a run on this machine. Every file in `evidence/`, except its `README.md`, carries this label. |
| `PRECOMPUTED` | A number calculated ahead of the demo and stored. |
| `SIMULATED` | A lab figure, such as the token sum in the cost file. It is not a bill. |
| `EDUCATIONAL` | A teaching formula or rate. The token estimate `len(prompt.split()) * 2` stays educational until a real tokenizer is used. The audit field `token_estimate_method` holds the value `word_count_x2_EDUCATIONAL` to say so. The cost rate is 1.0 unit per 1000 tokens. It is a teaching number, not a price. |
| `DECIDED` | A backlog item whose open choice the owner has settled, with a build stage named. Example: `OB-01` is DECIDED with a cache lifetime of 300 seconds, built in S07. |
| `REVISED-S2Q` | The status of `docs/00-contract/cost-envelope.md` after the qualification stage rewrote the hosted-model rows. |
| `Verified Fact` | A claim that names a file and line, a YAML id, a test name, or a command output the writer ran. The reviews and `semantic-layer-revision.md` use this label. |
| `Inference` | A claim drawn from facts, with no direct proof. |
| `Assumption` | Something taken as true so the work can go on. It is listed in the Assumptions row of the file. |
| `Unknown` | The repo or the owner has not said. Example: the letters of MAESTRO. |

## Record id prefixes

These letters start an id in the synthetic data. The form is in `semantic-layer/entities.yaml`.

| Prefix | What the id points at | Example |
|---|---|---|
| `DEV-` | A device, after the first row. | `DEV-00002` |
| `REC-` | The first key of each of the six CSV files. On the device file that row is also the device the API returns for `REC-0001`. | `REC-0001` |
| `CIR-` | A circuit. | `CIR-00002` |
| `ALA-` | An alarm. | `ALA-00002` |
| `INC-` | An incident. | `INC-00002` |
| `ORD-` | A service order. | `ORD-00002` |
| `SER-` | The blank service-order row. Normal order ids use `ORD-`. | `SER-BAD1` |
| `AI_-` | An AI invocation row. The underscore is part of the prefix in the file. | `AI_-00002` |
| `SIT-` | A site id on a device. | `SIT-00001` |
| `CUS-` | A customer id. | `CUS-00001` |
| `DED-` | An alarm dedupe key. | `DED-00002` |
| `STO-` | An alarm storm batch. | `STO-00002` |
| `TOP-` | A topology snapshot id on an AI invocation row. | `TOP-00001` |
| `EVT-` | An event id in `events.jsonl`. | `EVT-0000000` |
| `APR-` | An approval id. It appears only in the policy fixtures and tests, as a made-up value. No approval store exists, so no real id is checked against a stored yes. | `APR-EXAMPLE-0001` |
| `corr-` | A correlation id, when the event has one. The letters are lower case in the data. | `corr-00273` |
| `-BAD1` | The blank row in a CSV file. The letters in front say which file. | `DEV-BAD1`, `CIR-BAD1`, `ALA-BAD1`, `INC-BAD1`, `SER-BAD1` |

## YAML id prefixes

Every item in `semantic-layer/` has an id in dot form. The first word is the kind. The full table is in `semantic-layer/README.md` under "Id conventions". The kinds used in the identity documents are these.

| Prefix | What it names | Example |
|---|---|---|
| `persona.` | One of the seven telecom personas. | `persona.network_engineer` |
| `role.` | One of the five API role strings today. | `role.engineer` |
| `action.` | What the caller asks to do. | `action.read` |
| `resource.` | What the action is done to. | `resource.device` |
| `purpose.` | Why the caller is doing it. | `purpose.incident_triage` |
| `scope.` | Which records the caller may touch. | `scope.all_records` |
| `risk.` | How much harm a wrong action can do. | `risk.read_only` |
| `rule.` | A rule the system must keep. | `rule.no_default_role` |
| `policy.` | A named policy block. The ids `policy.opa.admin_any` and `policy.opa.operator_read` are deprecated since 1.1.0. Both name `policy.opa.access_matrix` as the replacement. | `policy.opa.access_matrix` |
| `status.word.` | A word that appears in a status column of the data. | `status.word.gold` |
| `status.code.` | A word the code writes, such as an audit action, an error, or a reason. S05R added 47. | `status.code.audit_action.audit_read` |
| `collision.` | A word used with two meanings. | `collision.gold_bronze_as_severity` |
| `metric.` | A number the system can report. No metric has a target. | `metric.api_availability` |
| `field.audit_row.` | One of the 15 keys of the audit row, added in S05R. | `field.audit_row.correlation_id` |
| `field.policy_input.` | One of the 8 inputs of the AI action policy, added in S05R. | `field.policy_input.record_found` |
| `provenance.` | A field that says where an answer came from. | `provenance.approval_id` |
| `outcome.` | One of the four AI outcomes. | `outcome.hold_for_review` |
| `entity.` | A table or the event log. | `entity.device` |
| `field.` | One column. | `field.device.mgmt_ip` |
| `ai_use.` | One of the eleven capabilities. | `ai_use.incident_summary` |
| `failmode.` | A trigger that sends a call to a person. The AI action policy rows `H1` to `H4` use these. | `failmode.timeout` |
| `concept.` | A term with no table. | `concept.policy_decision` |

## Names written in code

These names come from S04-08 to S04-12. They are field names, setting names, and file names. Each row says what the name does.

| Name | What it is | Where it lives |
|---|---|---|
| `correlation_id` | The id that ties one request to its audit row. The header `X-Correlation-Id` carries it. A sent value is kept. A blank or missing value is replaced by a new UUID. | `apps/api/main.py`, `docs/08-observability/log-schema.md`. |
| `prompt_hash` | The SHA-256 hash of the prompt text. The same prompt gives the same hash. The audit row stores it so a reviewer can tell two calls used the same prompt. | `apps/api/services/ai_gateway.py`, `audit.py`. |
| `token_estimate_method` | The last of the 15 audit fields. It holds `word_count_x2_EDUCATIONAL` when `tokens` is filled. It is empty when no model was called. | `apps/api/services/audit.py`, `docs/08-observability/log-schema.md`. |
| `ESTIMATE_METHOD` | The Python constant that holds the text `word_count_x2_EDUCATIONAL`. | `apps/api/services/ai_gateway.py`. |
| `FINOPS_EDU_RATE_PER_1K` | The setting for the cost rate. The default is 1.0 unit per 1000 tokens. Decided on 2026-10-11 by Mangesh (FDE). EDUCATIONAL. Owner: Team-Force. | `.env.example`, `docs/12-finops/metrics_from_audit.py`. |
| `AI_MODEL_TIMEOUT_SECONDS` | The setting for how long the model call may take. The default is 10 seconds. An empty, non-number, zero, or negative value gives 10. PROPOSED. Owner: Team-Force. | `.env.example`, `ai_gateway.py`. |
| `breaker` | The circuit breaker in `apps/api/services/breaker.py`. It opens after 5 failures, stays open for 30 seconds, and allows 10 calls in flight at once. All three numbers are PROPOSED. Owner: Team-Force. | `breaker.py`, `docs/11-reliability/retry-and-circuit-breaker-strategy.md`. |
| `in-flight limit` | The most model calls that may run at the same moment. It is 10. When the limit is reached, the next call is refused before the model runs. | `breaker.py`. |
| `held row` | An audit row for a call that stopped before the model. Its `model`, `tokens`, and `latency_ms` are empty. The FinOps script leaves held rows out of the token and latency means. | `docs/12-finops/metrics_from_audit.py`. |
| `quarantined` | An ETL count of rows held aside because they are damaged. The three older counts are unchanged. | `etl/run_daily_batch.py`, `docs/11-reliability/recovery-evidence.md`. |
| `dedupe.py` | A small helper that treats two alarms with the same `dedupe_key` and `storm_batch_id` as one. | `apps/api/services/dedupe.py`, `docs/11-reliability/idempotency-plan.md`. |
| `POLICY_ENGINE` | The setting that picks which copy of the policy runs. Values are `auto`, `python`, and `opa`. `auto` is the default. With `auto` the app starts `opa eval` for each decision when `opa` is on the PATH. | `apps/api/services/policy.py`, `tests/conftest.py`, `docs/13-security-validation/evidence.md` `EV-01`. |
| `security` marker | The pytest mark `@pytest.mark.security`. `pytest -m security` runs 195 tests. A skipped test in that run fails the stage. | `tests/`, `scripts/check_junit_no_skips.py`. |
| `check_junit_no_skips.py` | A script that reads a JUnit file and exits 1 when any test is skipped or no test ran. Added in S05-13 Half B. | `scripts/check_junit_no_skips.py`. |
| `GET /audit/{correlation_id}` | The route that returns every audit row for one case, in time order. Only `role.admin` may read it (`TA-35`). An id over 128 characters gets HTTP 400. | `apps/api/main.py`, `apps/api/services/audit_query.py`. |
| `audit.read`, `audit.not_found`, `audit.id_refused` | The three audit action words the audit route writes on its own row. They are new in S05-14. The route reuses `policy.deny` for a refused caller. S05R gave each one a `status.code.audit_action.*` id. | `apps/api/main.py`. |
| `policy.deny`, `policy.hold` | Audit action words for a denied call and a held call. | `apps/api/main.py`, `status.code.audit_action.policy_deny` and `policy_hold` in `status-taxonomy.yaml`. |
| `MAX_ID_LENGTH` | The most characters a case id may have on the audit route. It is 128. PROPOSED. Mangesh accepted it on 2026-10-12. | `apps/api/services/audit_query.py`, `rule.audit_case_id_limit`. |
| `cannot_prove` | A list the audit route returns with each case. It names facts the log cannot show, such as `approval_id`, `log_integrity`, and `final_action`. It has 13 item names. | `apps/api/services/audit_query.py`, `status.code.cannot_prove.*`. |
| `enforced_today` | A flag on each rule in `business-rules.yaml`. It is true when code in `apps/` or `etl/` runs the rule on a live route or in the batch. At `1.1.0` it is true on 9 of 20 rules. | `semantic-layer/business-rules.yaml`. |
| `deprecated`, `replaced_by` | Two YAML keys added to the schema in S05R. An id marked `deprecated: true` keeps its meaning and names the id that replaces it. | `semantic-layer/schemas/semantic-layer.schema.json`. |
| `local-sim-v1` | The stub model. Its text is SIMULATED. The repo has no second model version, so `model` and `model_version` hold the same string. | `ai_gateway.py`, `docs/09-ai-guardrails/evidence.md`. |

## Code comments

The Python comments name few initials. They describe the current behaviour in sentences. The initials that do appear in comments are already in the tables above.

| File | Comment | Label it uses |
|---|---|---|
| `infra/terraform/main.tf` | The first line calls the file a local settings file. It builds no cloud resource, writes one text file, and holds no user name, password, key, or token. Stage S04-05 Half B, PROPOSED, owner Team-Force. | `PROPOSED` |
| `etl/run_daily_batch.py` | Malformed records are counted and left in the file. | The batch is the `ETL` job. The comment does not use the letters. |
| `semantic-layer/build.py` | The seven YAML files, in the order the README lists them. | `YAML` |
| `semantic-layer/tests/test_semantic_layer.py` | A URL may embed a password. | `URL` |
| `policy/opa/access.rego` | The file replaces the two brownfield rules. It answers whether a caller may take an action on a resource, for a purpose, over a scope, at a risk. The allow rows `TA-01` to `TA-35` live in `policy_data.json`. Every grant is PROPOSED. | `TA-xx`, `PROPOSED` |
| `policy/opa/ai_action.rego` | It returns one of RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE. Any BLOCK row wins. Otherwise any HOLD row wins. Otherwise the action decides. No row compares a number. | `B1` to `B10`, `H1` to `H4`, `O1` to `O3`, the four outcome words |
| `apps/api/services/policy.py` | Policy evaluation for the API. Stage S04-06 Half B. | The `OPA` policy; no other initials. |
| `apps/api/settings.py` | Load required settings from the process environment. A setting that is absent, empty, or still the placeholder raises an error. | No initials. |
| `scripts/evidence.sh`, `scripts/evidence.ps1` | Run the CI pipeline stages and write every output file into `evidence/`. Each stage appends its name and exit code to `exit-codes.txt`. No stage switches a scan off. | No initials. |
| `Dockerfile` | Runs the test suite in a clean Linux container with the same Python as CI. The tag `3.11-slim` moves, so the comment records the image digest seen on 2026-10-11. | `PROPOSED` |
| `apps/api/main.py` | The role check is broad and facility or tenant context is ignored. | No initials. |
| `apps/api/services/ai_gateway.py` | Since S04-09 Half B the prompt comes from the YAML allow list, the model call has a timeout, and the answer must match a schema. The token formula is marked EDUCATIONAL. | `EDUCATIONAL`, `PROPOSED` |
| `apps/api/services/audit.py` | Since S04-08 Half B the row carries an actor, a correlation id, and the five provenance values. Since S04-12 Half B it has a 15th field, `token_estimate_method`. No retention class. | `EDUCATIONAL` |
| `apps/api/services/domain_service.py` | A missing id returns the first row. | No initials. |
| `apps/api/services/audit_query.py` | Reads one case back from the audit log. Read only. A row with no `correlation_id` is never returned. The item names on the cannot-prove list are PROPOSED plain names. | `PROPOSED`, `S05-14` |
| `apps/api/main.py` (audit route) | The three audit action words are PROPOSED. The comment says the YAML had no id for them. S05R answered that comment with `status.code.audit_action.*` ids. | `PROPOSED` |
| `scripts/check_junit_no_skips.py` | Fails when a JUnit file shows a skipped test or no test. Stage S05-13 Half B, backlog row `SB-10`. PROPOSED. Owner: Team-Force. | `SB-xx`, `PROPOSED` |

Many comments in `apps/`, `policy/opa/`, and `etl/` end with "Open question for S03". S05R read each one and did not edit any of them. `docs/02-baseline/semantic-layer-revision.md` section 8 says how each one was answered.
