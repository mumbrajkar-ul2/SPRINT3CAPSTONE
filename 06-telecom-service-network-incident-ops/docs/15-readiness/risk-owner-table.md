# Risk owner table

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 15, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. 22 accepted risks have a named owner role and a file that records the acceptance. 41 more risks have no recorded acceptance. For those 41 the owner is Unknown and the table PROPOSES one. |
| Evidence sources | `docs/15-readiness/residual-risk-register.md`; `docs/prd/Risk Management.md` section 7; `docs/00-contract/operating-contract.md` rows 5, 7, 9 and 10; `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/ADR/0003-s06-risk-recommendations.md`; `docs/ADR/0004-defer-rq-31-answer-store.md`; `docs/02-baseline/S05R_Decisions.md`; `../playbook/STATUS.md`. |
| Assumptions | (1) Team-Force owns every PROPOSED item (`docs/00-contract/operating-contract.md` row 10). Team-Force is the FDE team that Mangesh belongs to. Its other members are Unknown. (2) Mangesh (FDE) acts for Team-Force. (3) The instruction "proceed with the recommendations for the Risks" in the status line of ADR 0003 covers the accept and defer stances in `Risk Management.md` section 7. That reading is an Inference. The ADR writes out only three decisions. |
| Unresolved issues | A business owner outside the FDE team is Unknown. A second code reviewer is Unknown. The sign-in system and its owner do not exist, because ADR 0003 puts login out of scope. |
| Residual risks | The same team proposes, owns and accepts. The packet names no person outside it to check the business numbers (`CR-10` in the register). |

Paths are relative to the project folder (06-telecom-service-network-incident-ops).

## 1. Owner roles in this packet

| Role | Who it is | What it may do | Source |
|---|---|---|---|
| Team-Force | The FDE team. Mangesh belongs to it. Other members are Unknown. | Owns every PROPOSED item and every row of the remediation backlog. | `docs/00-contract/operating-contract.md` row 10 |
| Mangesh (FDE) | One named person. | Acts for Team-Force. Reviews each code change. Accepts each stage. Confirms rows 1 to 9 of the contract. | `docs/00-contract/operating-contract.md` rows 7 and 10 |
| `network_engineer` | A desk job, not a named person. | Approves a live network change by writing a stored approval id. No route in this packet changes a live network. | `docs/00-contract/operating-contract.md` row 9 (v1.4) |
| Business owner | Unknown. | Would replace Team-Force for business decisions such as numbers and cutoffs. | `docs/00-contract/operating-contract.md` row 10 |

## 2. Accepted risks (22)

Each row names the owner role, who accepted the risk, and the file that records it. The review trigger says when to look at the risk again.

| Risk id (register) | Risk in plain words | Owner role | Accepted by | Where it is recorded | Review trigger |
|---|---|---|---|---|---|
| SB-09 (`RK-01`) | The role is a word the caller types. Nothing proves who the caller is. | Team-Force | Mangesh (FDE) for Team-Force, 2026-10-12 | `docs/ADR/0003-s06-risk-recommendations.md` decision 1; `docs/prd/Risk Management.md` section 7 | The app is reachable by more than the team. |
| AIR-08 (`RK-05`) | The command phrase list is short. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference) | `docs/prd/Risk Management.md` section 7; `docs/ADR/0005-s07-yaml-additions.md` | A test shows a missed phrase. |
| S08 D-09 (`RK-05`) | The summarize route holds one command sentence and lets other command text through. | Team-Force | Unknown whether `RK-05` covers the summarize route. Mangesh (FDE) accepted the short list (Inference). | `docs/prd/Risk Management.md` section 7; `docs/model-comparison/app-comparison.md` F-3 | A test shows a missed phrase on the summarize route. |
| AIR-01 (`RK-06`) | Instruction text typed into an allowed field is not found. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). S05R D-09 is "keep deferred". | `docs/prd/Risk Management.md` section 7; `docs/02-baseline/S05R_Decisions.md` | A real model arrives. |
| SB-14 (`RK-06`) | A secret value typed into an allowed field is not found. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | A real model arrives. |
| SB-15 (`RK-07`) | The model name and the model version are the same text. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | S08 or a hosted model. Inference: the risk stays open after S08, because `docs/model-comparison/app-comparison.md` names no model identity test. |
| SB-12 (`RK-08`) | The audit log is a plain file with no tamper evidence. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | A second server process, or a reviewer asks for tamper evidence. |
| BF-R12 (`RK-08`) | 96 old audit lines have no correlation id. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | A reviewer asks to rebuild a case from the old lines. |
| SB-13 (`RK-09`) | No limit on request rate, prompt size or answer size. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | Team-Force names the two lengths, or a flood is seen. |
| RF-08 (`RK-10`) | A held case has no inbox. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | Operators cannot find a held case. |
| RK-12 | Four scopes need data the CSV files lack. There is no row-level filter. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | An assignment table is added. |
| RK-15 | Time, token and cost numbers come from the stand-in model. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | A real model is measured. |
| BF-R05 and BF-R09 (`RK-17`) | The data files hold known faults. Three incident ids repeat. | Team-Force | Mangesh (FDE), by the instruction in ADR 0003 (Inference). | `docs/prd/Risk Management.md` section 7 | The data owner replaces the files. |
| FM-05 | Each repeat of a summary request costs one model call. | Team-Force | Mangesh (FDE), 2026-10-13 | `docs/ADR/0004-defer-rq-31-answer-store.md` | A real model is in use and cost matters. |
| AIR-05 | The 10 second model timeout was not measured against a real model. | Team-Force | Mangesh (FDE), who accepted all 120 PROPOSED items | `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/02-baseline/S05R_Decisions.md` D-11 | A real model is measured. |
| FM-14 | The breaker numbers (5 failures, 30 seconds) and the in-flight limit of 10 are PROPOSED. | Team-Force | Mangesh (FDE), who accepted all 120 PROPOSED items | `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/11-reliability/recovery-evidence.md` | Production request rate and model wait are known. |
| AIR-06 | The prompt wording version and the hash method have no YAML id. | Team-Force | Mangesh (FDE), 2026-10-12 | `docs/02-baseline/S05R_Decisions.md` D-10 ("keep deferred") | The prompt wording changes. |
| BL-09 | `logs/audit.log` stays tracked by git and changes on each run. | Team-Force | Mangesh (FDE), 2026-10-11 | `../playbook/STATUS.md` (S05-13 Half A owner decision, choice 4) | A reviewer asks for a clean log in git. |
| G-9 and BF-R23 | The Angular scaffold stays unwired. The served page is the demo. | Team-Force | Mangesh (FDE), 2026-10-10 (v1.3) | `docs/00-contract/operating-contract.md` row 5 | The PRD names a screen the served page cannot meet. |
| S09-2 | PRD v1.9 had no full S06R review. | Team-Force | Mangesh (FDE), 2026-10-13 | `../playbook/STATUS.md` (row "S07 gaps G-5 G-7") | Any later PRD change. |
| CR-7 | One person reviews every code change. | Team-Force | Mangesh (FDE), 2026-10-10 (v1.2) | `docs/00-contract/operating-contract.md` row 7 | A second reviewer joins. |
| CR-10 | The team that proposes an item also owns it. | Team-Force | Mangesh (FDE), 2026-10-10 (v1.2) | `docs/00-contract/operating-contract.md` row 10 | A business owner is named. |

**Worked example (`SB-12`).** The audit log is a text file. A person with file access can change a line and no check shows it. The owner role is Team-Force. Mangesh (FDE) accepted the file store for the lab. The trigger to look again is a second server process or a reviewer who asks for tamper evidence. The audit route says in every reply that it cannot prove `log_integrity`.

## 3. Risks with no recorded acceptance (41)

Nobody in the packet accepted these risks. The owner is Unknown. The table PROPOSES an owner under `docs/00-contract/operating-contract.md` row 10. A PROPOSED owner has not agreed. `docs/15-readiness/go-no-go-decision.md` asks Team-Force to accept the 38 rows that name Team-Force for the lab demo only, or to name a different owner. It asks Mangesh (FDE) to close the 3 rows that name him (S09-1, S09-3 and S09-5).

| Risk id (register) | PROPOSED owner | Risk in plain words |
|---|---|---|
| BF-R01 | Team-Force | The storm route exists. |
| BF-R02 and SB-17 | Team-Force | The shared database password left the source file. |
| BF-R03 | Team-Force | A device with a `true` stale flag blocks a recommendation. |
| BF-R06 | Team-Force | The shared database user and the persona `automation_service` may be one account. |
| BF-R22, FM-08 and RF-05 | Team-Force | The daily batch counts a bad row in `quarantined` and writes no file. |
| AIR-07 | Team-Force | A program that imports `summarize_record` directly skips the role check. |
| FM-01 and RF-04 | Team-Force | A 500 reply may carry no correlation id and write no audit row. |
| FM-02 | Team-Force | 1992 of 3000 event lines have no usable correlation id. |
| FM-03, FM-04 and RF-03 | Team-Force | A timeout and a model error give failure reasons that do not match the PRD table. |
| FM-06 | Team-Force | Duplicate memory for alarms, orders and events lives in one process. |
| FM-11 and RF-06 | Team-Force | A policy engine failure returns 403 `forbidden`. |
| SB-02 | Team-Force | `apps/api/services/policy.py` still falls back to the `operator` fields for a role id with no entry. |
| SB-08 | Team-Force | The policy checks that an approval id is not blank. |
| SB-16 | Team-Force | Six rules in `semantic-layer/business-rules.yaml` still say `enforced_today: false`. |
| SB-20 | Team-Force | `POLICY_ENGINE` defaults to `auto`. |
| SB-21 | Team-Force | The workflow uses actions that run on Node 20. |
| BL-10 | Team-Force | `ruff` reports 30 findings. |
| BL-11 | Team-Force | `pip-audit` reports 9 advisory ids on 3 packages. |
| BL-12 | Team-Force | `bandit` reports 40 findings, all LOW. |
| G-1 and SB-03 | Team-Force | The PRD does not say what word to store for an unknown role header. |
| G-2 | Team-Force | A 404, a 422, a call of `GET /` or a call of `GET /ready` writes no audit row. |
| G-3 | Team-Force | `record_id` is null on a storm read and on an audit read. |
| G-4 and S08 D-01 | Team-Force | The `/ready` body uses the key `status` in the first app and `runbook_level` in the second. |
| G-6 and S08 D-02 | Team-Force | The 422 body and the 500 body of the approvals route use PROPOSED wording. |
| G-8, S08 D-10 and Q-10 | Team-Force | The PRD says "whole words" and does not say what ends a word. |
| S08 D-03 (Q-5) | Team-Force | `approval_required` is `false` in the first app and `true` in the second. |
| S08 D-04 (Q-9) | Team-Force | The first app adds `policy_version` to the body. |
| S08 D-05 (Q-9) | Team-Force | The first app adds a `rule.*` id after the `failmode.*` id. |
| S08 D-06 (Q-4) | Team-Force | A model that raises, times out or trips the breaker gives different reasons in each app. |
| S08 D-07 (Q-11) | Team-Force | The stale flag check differs for a capital `True` and for an odd word. |
| S08 D-08 (Q-1, Q-2) | Team-Force | The second app lets through a bad model answer. |
| S08 D-11 (Q-6) | Team-Force | After an approval the second app still lists `approval_id` as unprovable. |
| S08 D-12 (Q-7) | Team-Force | The second app has no write lock and loses audit rows. |
| S08 D-13 (Q-12) | Team-Force | The approvals file path and row shape differ. |
| S08 D-14 (Q-8) | Team-Force | The second app types its grants by hand and one function returns EXECUTE for an invalid resource. |
| S08 D-15 | Team-Force | The second app's page has fewer honesty labels. |
| S08 D-16 (Q-13) | Team-Force | The two apps build the prompt text in a different layout. |
| S09-4 | Team-Force | `make` is not installed on this machine, so `make evidence` did not run. |
| S09-1 | Mangesh (FDE) | The refreshed `evidence/` folder is not committed. |
| S09-3 | Mangesh (FDE) | `../playbook/STATUS.md` has no row for S05-14, S06 or S06R. |
| S09-5 | Mangesh (FDE) for Team-Force | Three live routes are outside the list that contract row 2 allows. Four files have no stage as author. The old shared password sits in the chat transcript. |

## 4. Count check

| Group | Rows |
|---|---|
| Accepted risks in section 2 | 22 |
| Risks with no recorded acceptance in section 3 | 41 |
| Total (equals the register) | 63 |

**Gate effect.** Section 3 holds 41 rows with a PROPOSED owner. The S09 gate therefore reads CONDITIONAL PASS and cannot read PASS.

