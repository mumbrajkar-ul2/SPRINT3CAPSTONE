# Operating contract check

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 15, D8). |
| Date / version | 2026-10-13, v1.0. Checked against `docs/00-contract/operating-contract.md` v1.4. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. No change crossed a Prohibited row (1, 6, 8, 9). No row is PROVISIONAL at v1.4. Three live routes go beyond the list in the working rule of row 2. Some files that changed (section 3.2) fall under no row of the contract. The owner has not written an exception for either case. |
| Evidence sources | `docs/00-contract/operating-contract.md`; `git diff --name-status e61ba2e HEAD` (the inherited commit against the last commit); `apps/api/main.py`; `apps/api/services/`; `legacy/reconcile_legacy.py`; `etl/run_daily_batch.py`; `data/contracts/openapi-fragment.yaml`; `docs/prd/prd.md`; `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `../playbook/S04-03-identity.md` to `../playbook/S05-14-audit-chain.md`; `../playbook/S07-application-and-demo.md`; `../playbook/STATUS.md`. |
| Assumptions | (1) The inherited commit `e61ba2e` is the baseline. (2) A change counts when `git diff` shows it between that commit and the last commit. The check also ran `git status` for the working tree. (3) The agent compared file lists and read the code that matters for each row. It did not read every line of every diff. |
| Unresolved issues | The owner has not decided whether the three extra routes and the uncovered files need a written exception. Rows 1 to 10 have no row for configuration files, scripts or the ETL. |
| Residual risks | A check by file name can miss a change inside an allowed file that crosses the intent of a row. The tests and the S03R and S06R reviews are the other checks (`CR-7` in `docs/15-readiness/residual-risk-register.md`). |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Paths are relative to the project folder (06-telecom-service-network-incident-ops) unless they start with `../`.

## 1. Row by row

| # | Question | Status in v1.4 | What changed | Evidence | Result |
|---|---|---|---|---|---|
| 1 | May database or CSV schemas change? | Prohibited | No CSV column changed. | `git diff e61ba2e HEAD -- data/synthetic data/manifest.json` is empty. The semantic layer is a new folder (`semantic-layer/`), which row 1 allows. | Held |
| 2 | May API routes be added, changed or removed? | Allowed | Added `GET /alarms/storms/{storm_batch_id}`, `POST /ai/recommend/{id}` and `POST /approvals/{id}` (named in `../Project_Intent.md` 2.7). `GET /records/{id}` now returns 404 for a missing id (row 2 allows it). `POST /ai/summarize/{id}` is kept and hardened. Also added `GET /`, `GET /ready` and `GET /audit/{correlation_id}`. No route for qualify, provision, retry, rollback or fix validation. No EXECUTE route. | `apps/api/main.py` (9 routes); `policy/tests/test_policy_python.py::test_no_route_can_execute`; `tests/app/test_openapi_fragment.py`. | Held for the rules the row states. Boundary case for the 3 extra routes (section 3). |
| 3 | May `apps/api/services/ai_gateway.py` change? | Allowed | Rewritten in S04-09 Half B, after S2Q. Added an allow list of prompt fields, a fixed output shape, a timeout, a stale-topology check and a hold path. S07 added the recommend call on the same file. The file has no execute path. | `docs/09-ai-guardrails/evidence.md`; `tests/ai/test_guardrails.py`; `apps/api/services/ai_gateway.py` ("The module never returns EXECUTE"). | Held |
| 4 | May `legacy/reconcile_legacy.py` change? | Allowed | S04-04 Half B removed the hard-coded password and added `require("SHARED_DB_PASSWORD")`. `.env.example` and `infra/terraform/main.tf` lost the old shared-user values in the same stage. | `git diff e61ba2e HEAD -- legacy/reconcile_legacy.py`; `tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment`. A search of this folder for the old value finds no file. The value stays in git history, in `../Project_Intent.md` (the assignment brief) and in `../transcript/chat_transcript.md` (copied there by earlier chat turns). | Held for the code edit. The transcript copy is an open point (section 3.3). |
| 5 | Is the Angular scaffold under `apps/web/` in scope? | Allowed under four conditions | Nothing changed. The scaffold is read and described only. | `git diff e61ba2e HEAD -- apps/web` is empty. | Held |
| 6 | Are the files under `data/synthetic/` read-only? | Prohibited | No write. The live gateway does not write `data/synthetic/ai_invocations.csv`. The only files the app writes are `logs/audit.log` and `logs/approvals.jsonl`. | `git diff e61ba2e HEAD -- data/synthetic` is empty. `apps/api/services/audit.py` line 134 and `apps/api/services/approvals.py` line 53 are the only file writes in `apps/api/`. `tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged`. | Held |
| 7 | Who approves a code change before it merges? | Allowed | One reviewer, Mangesh (FDE). | `../playbook/STATUS.md` records each stage result. S03R ran 3 rounds (PASS in round 3). S06R reviewed the PRD again after each S06F fix round. The tests ran on each change. | Held. Accepted risk `CR-7`. |
| 8 | What condition stops the work? | Prohibited | No stop condition was hit. No device config was pushed, no circuit was provisioned, and no incident was closed. No production login or live device was used. No hosted model was called. | `apps/api/` holds no URL and no hosted-model client (searched for `openai`, `anthropic`, `requests`, `urllib`, `http://` and `https://`: no match). The model is `local-sim-v1`. | Held |
| 9 | What is the irreversible action, and where must a human approve it? | Prohibited | No route changes a live network. `POST /approvals/{id}` records a yes or a no and changes no data file. The stored approval id is written for a yes only. | `tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id`; `tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check`; `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id`. | Held |
| 10 | Who owns a PROPOSED item? | Allowed | Team-Force owns every PROPOSED item. | `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` records the acceptance of the 120 PROPOSED items of S05R in 12 bundles. It names Team-Force as the owner. | Held. Accepted risk `CR-10`. |

**Worked example (row 6).** Row 6 forbids writes under `data/synthetic/`. `git diff e61ba2e HEAD -- data/synthetic` prints nothing. A search of `apps/api/` for file writes finds two lines: one in `apps/api/services/audit.py` that appends to `logs/audit.log`, and one in `apps/api/services/approvals.py` that appends to `logs/approvals.jsonl` (the file appears at the first yes decision, so none exists in the tree now). Neither path is under `data/synthetic/`. The row is held.

## 2. PROVISIONAL rows

**Verified Fact.** `docs/00-contract/operating-contract.md` v1.4 has no PROVISIONAL row. Mangesh (FDE) confirmed rows 1, 5, 7 and 10 on 2026-10-10 (v1.2), changed row 5 on the same day (v1.3) and named the live-change approver on the same day (v1.4). The first code change (S04-03 Half B) is dated 2026-10-11. So no change in the repo came before a row was confirmed.

No change crossed a PROVISIONAL boundary.

## 3. Changes the contract does not cover

### 3.1 Three routes outside the list in row 2

The working rule of row 2 says "Add only the routes `../Project_Intent.md` 2.7 names", and that list holds three routes. It also says "The PRD must name a route before stage S07 adds it."

| Route | Added in | Named by | Result |
|---|---|---|---|
| `GET /audit/{correlation_id}` | S05-14 Half B (commit `78c79b3`, 2026-10-12) | `../playbook/S05-14-audit-chain.md` Half B ("add a route that rebuilds a case from stored rows by correlation_id"). `docs/prd/prd.md` lines 110, 126 and 249 (RQ-42 to RQ-52) list it later as an existing route. | The route was added before the PRD existed. The playbook asked for it. No written exception from the owner exists in the packet. |
| `GET /ready` | S07 | `docs/prd/prd.md` lines 104 and 244 (RQ-73). `docs/ADR/0003-s06-risk-recommendations.md` line 63 (RQ-73 for risk RK-11). | The PRD named it before S07 added it. The route is not in the list of 2.7. |
| `GET /` (the served page) | S07 | `docs/prd/prd.md` line 250 (RQ-62 to RQ-65). `../Execution Plan.md` lines 425 and 434 ("a small served page"). | The PRD named it before S07 added it. The route is not in the list of 2.7. |

**Inference.** Row 2 is Allowed, and the owner approved the PRD that names all three. The contract text does not say whether a route outside the list in 2.7 needs its own approval, and the check cannot settle that. `S09-5` in `docs/15-readiness/residual-risk-register.md` PROPOSES that Mangesh (FDE) writes the exception.

### 3.2 Files that no row names

The "What may be written" paragraph says a later stage may edit a file only when a row says Allowed. The contract has no row for the files below. Where a playbook file names the file, the table gives that file. Mangesh (FDE) reviewed each stage (row 7). A file that no playbook names is marked "No playbook names it".

| File or folder | Change since `e61ba2e` | Named in |
|---|---|---|
| `Makefile` | Edited. | `../playbook/S04-05-iac.md`, `../playbook/S04-07-cicd.md`, `../playbook/S05-13-security-validation.md` |
| `infra/terraform/main.tf` | Edited. The shared user name was removed from the output. | `../playbook/S04-04-secrets.md`, `../playbook/S04-05-iac.md` |
| `infra/terraform/.terraform.lock.hcl` | Added. | No playbook names it. Inference: the `terraform init` run wrote it. |
| `requirements.txt`, `requirements-dev.txt` | Edited and added. `requirements.txt` gained `httpx==0.28.1`. | `../playbook/S04-05-iac.md`, `../playbook/S04-07-cicd.md` |
| `pyproject.toml` | Edited. | `../playbook/S04-05-iac.md`, `../playbook/S05-13-security-validation.md` |
| `.env.example` | Edited. Each secret value became `CHANGE_ME`. New non-secret settings were added. | `../playbook/S04-03-identity.md`, `../playbook/S04-04-secrets.md` |
| `Dockerfile` | Added. | `../playbook/S04-05-iac.md` |
| `.dockerignore`, `.gitignore`, `.gitattributes` | Added. | No playbook names them. |
| `scripts/` | Added `scripts/bootstrap.ps1`, `scripts/bootstrap.sh`, `scripts/evidence.ps1`, `scripts/evidence.sh`, `scripts/check_junit_no_skips.py`. | `../playbook/S04-05-iac.md` and `../playbook/S04-07-cicd.md` (bootstrap); `../playbook/S04-07-cicd.md` and `../playbook/S05-13-security-validation.md` (evidence). `../playbook/S05R-semantic-layer-revision.md` names `scripts/check_junit_no_skips.py`. The stage that wrote it is Unknown. |
| `../.github/workflows/ci.yml` | Moved with `git mv` from the .github folder inside this project folder to the .github folder at the git root. | `../playbook/S04-05-iac.md`, `../playbook/S04-07-cicd.md`, `../playbook/S05-13-security-validation.md` |
| `etl/run_daily_batch.py` | Edited. A `quarantined` count was added. `processed`, `malformed` and `sample` keep their meaning. No file is written. | `../playbook/S04-11-reliability.md` |
| `apps/api/services/audit.py` | Edited. | `../playbook/S04-08-observability.md`, `../playbook/S04-12-finops.md`, `../playbook/S05-14-audit-chain.md` |
| `apps/api/services/domain_service.py` | Edited. | `../playbook/S04-10-performance.md` |
| `data/contracts/openapi-fragment.yaml` | Edited. | `../playbook/S07-application-and-demo.md` |
| `security/threat-model.md`, `supply-chain/dependency-risk-register.md` | Edited. | `../playbook/S04-09-ai-guardrails.md`, `../playbook/S05-13-security-validation.md`, `../playbook/S05-14-audit-chain.md` (threat model); `../playbook/S04-07-cicd.md` (dependency register). |
| `apps/api/` new modules, `policy/`, `semantic-layer/`, `apps/api_model_b/` | Added. | The stage playbook files. Row 1 allows a new semantic-layer folder. Rows 2 and 3 cover the app. `apps/api_model_b/` is the second-model app of stage S08. |

Row 7 covers the review of each of these changes. The three files with no playbook (`.dockerignore`, `.gitignore`, `.gitattributes`) and the lock file have no stage named as author. The owner has not accepted them in writing. `S09-5` in `docs/15-readiness/residual-risk-register.md` carries this point.

**Result.** None of these files is under a Prohibited row. No change to them touches `data/synthetic/`, `apps/web/` or the CSV columns.

### 3.3 The old shared password in the chat transcript

Row 4 says "Do not copy that password into a new file." Stop condition 5 says the same for any secret.

**Verified Fact.** A search of the workspace for the old value finds it in `../Project_Intent.md`, in the archive copies of the brief under `../Archive/`, and in `../transcript/chat_transcript.md`. It does not appear in any file inside this folder.

**Inference.** The transcript rule appends each turn and never overwrites. Earlier turns carried the value from the brief into the transcript. This is a copy of a secret into a new file.

The packet has no production system (contract section "Production access"). The value belongs to the synthetic lab, and the brief itself prints it. The transcript file is append-only, so the agent did not edit it. The agent did not write the value into any file of this packet. Decision for the owner: redact the old value in the transcript by hand, or accept the copy. `S09-5` carries the point.

## 4. Stop conditions

| # | Stop condition | Hit? | Proof |
|---|---|---|---|
| 1 | The next edit would push a config, provision a circuit, apply an automated fix, or close an incident so that a real outage is hidden. | No | No route or script does it (rows 8 and 9 above). |
| 2 | The next edit needs a production system, a live device, or a secret that is not a placeholder. | No | `.env.example` holds `CHANGE_ME`. No file under `docs/` holds the old password. |
| 3 | The next edit would call a hosted model before S2Q names that call. | No | `apps/api/` holds no hosted-model client. |
| 4 | The next edit would change a CSV column, a row under `data/synthetic/`, or any other Prohibited row. | No | `git diff e61ba2e HEAD -- data/synthetic` is empty. |
| 5 | The next edit would copy the shared database password, or any other secret, into a new file. | No | The S09 files write `<redacted>` and name no value. |

## 5. Lifecycle

This check feeds `docs/15-readiness/go-no-go-decision.md` and the "Production Readiness Decision" section of `PRODUCTION_EVIDENCE_PACK.md`. The rows `S09-5`, `CR-7` and `CR-10` in `docs/15-readiness/residual-risk-register.md` carry its open points.
