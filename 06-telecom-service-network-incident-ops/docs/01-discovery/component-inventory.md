# Component inventory

| Field | Value |
|---|---|
| Stage | S01 — Discovery dossier (Execution Plan Phase 1; spine stages 0A, 5, 7) |
| Date / version | 2026-10-09, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Owner is Unknown on 55 of 55 rows. That is more than half. The repo names no component owner. Five notes name an author. That person stays out of the owner column, because the file calls them the author. Every row cites a file, a test, a log, or a replay result. No row proposes a change. |
| Evidence sources | Every path in `Project_Intent.md` section 4.2; `docs/00-setup/replay-log.md`; `docs/00-setup/tool-versions.md`; `docs/00-contract/operating-contract.md`; `docs/00-contract/cost-envelope.md`; `docs/00-contract/challenge-to-spine-crosswalk.md`; `logs/audit.log` |
| Assumptions | A route is listed as its own row because the stage asks for one row per file or route. The job cell says what the file does today. |
| Unresolved issues | Owner is Unknown on every row. `docs/domain-specific-spec.md` line 39 says multiple teams appear to own overlapping capabilities and names no team. |
| Residual risks | A later stage can treat Unknown as a team name. Unknown means the repo does not say. |

## What this file is

One row per inherited file, per live route, per audit log, and per note added in S00 or S0B. The job is one sentence. The owner is Unknown when the repo does not name an owner.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. The evidence column carries the label.

## Inventory

| path | type | job | owner | evidence |
|---|---|---|---|---|
| `README.md` | doc | Names the system, the quick start, the local synthetic data, and a 16-step list. | Unknown | Verified Fact: `README.md` lines 1 to 43. |
| `docs/domain-specific-spec.md` | doc | Names four business flows, seven personas, and six data entities. | Unknown | Verified Fact: `docs/domain-specific-spec.md` lines 12 to 35. |
| `docs/architecture/current-state.md` | doc | Names the legacy scripts, the FastAPI app, the AI gateway, and three AI product names. | Unknown | Verified Fact: `docs/architecture/current-state.md` lines 3 to 13. |
| `docs/architecture/target-state-principles.md` | doc | Lists six design rules and a domain focus line. No rule in this file is executed. | Unknown | Verified Fact: `docs/architecture/target-state-principles.md` lines 3 to 12. |
| `docs/architecture/known-gaps.md` | doc | Lists six gap names and says not every issue is labelled in code. | Unknown | Verified Fact: `docs/architecture/known-gaps.md` lines 3 to 10. |
| `docs/ADR/0001-partial-modernization.md` | decision | Keeps legacy batch jobs while adding FastAPI. Status is Accepted, but never revisited. | Unknown | Verified Fact: `docs/ADR/0001-partial-modernization.md` lines 3 to 5. |
| `docs/transformation-roadmap.md` | doc | Lists modernization themes and says audit records cannot reconstruct a full decision. | Unknown | Verified Fact: `docs/transformation-roadmap.md` lines 7 to 24. |
| `docs/discovery/README.md` | doc | Says this folder is reserved for discovery notes. | Unknown | Verified Fact: `docs/discovery/README.md` lines 1 to 3. |
| `docs/runbooks/incident-response.md` | runbook | Says the runbook is incomplete and names severity, triage, rollback, comms, and evidence as missing. | Unknown | Verified Fact: `docs/runbooks/incident-response.md` lines 1 to 3. |
| `docs/runbooks/failure-injection-drills.md` | runbook | Names five drills: missing correlation ids, AI timeout, duplicate replay, stale master data, and partial batch failure. | Unknown | Verified Fact: `docs/runbooks/failure-injection-drills.md` lines 3 to 7. |
| `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md` | template | Lists empty headings for a later evidence pack. | Unknown | Verified Fact: `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md` lines 1 to 17. |
| `apps/api/main.py` | api app | Creates the FastAPI app and the three routes below. | Unknown | Verified Fact: `apps/api/main.py` lines 4 to 24. Replay section 2.9 lists the same three paths. |
| `GET /health` | route | Returns `status` ok and the repo name. Writes no audit line. | Unknown | Verified Fact: `apps/api/main.py` lines 6 to 8. Replay section 2.1. Test `test_health_contract`. |
| `GET /records/{record_id}` | route | Returns a device row when the role is in the allow list, then writes an audit line. Other roles get a forbidden body. | Unknown | Verified Fact: `apps/api/main.py` lines 10 to 17. Replay sections 2.2, 2.5, and 2.6. |
| `POST /ai/summarize/{record_id}` | route | Loads a device row, calls the local summary, writes an audit line, and returns the summary. The function takes no role. | Unknown | Verified Fact: `apps/api/main.py` lines 19 to 24. Replay section 2.7. Test `test_ai_summary_has_minimum_contract`. |
| `apps/api/services/domain_service.py` | service | Reads `devices.csv`. Returns the first row when no cell matches the id. Defines `list_recent`, which no other file calls. | Unknown | Verified Fact: `domain_service.py` lines 4 to 19. Replay section 2.3. |
| `apps/api/services/ai_gateway.py` | service | Builds a prompt, waits 0.01 seconds, and returns a local summary dict. | Unknown | Verified Fact: `ai_gateway.py` lines 3 to 18. Replay section 2.7. |
| `apps/api/services/audit.py` | service | Appends one JSON object with `ts`, `action`, and `details` to `logs/audit.log`. | Unknown | Verified Fact: `audit.py` lines 5 to 12. `logs/audit.log`. |
| `apps/web/src/app/operations.component.ts` | web | Sets a page title and the column names `id`, `status`, `risk_score`, `owner`, `last_updated`. | Unknown | Verified Fact: `operations.component.ts` lines 1 to 4. |
| `apps/web/src/app/api.service.ts` | web | Calls `fetch` on `/api/records/{id}` and `/api/ai/summarize/{id}`. | Unknown | Verified Fact: `api.service.ts` lines 1 to 4. |
| `apps/web/package.json` | web package | Runs Playwright for `test`. The dependencies object is empty. Lint prints the word scaffold. | Unknown | Verified Fact: `apps/web/package.json` lines 2 to 9. |
| `legacy/reconcile_legacy.py` | script | Counts rows in `devices.csv` and holds user `app_shared` with password `<redacted>`. | Unknown | Verified Fact: `legacy/reconcile_legacy.py` lines 5 to 14. |
| `etl/run_daily_batch.py` | script | Counts device rows and rows with a blank field, then prints the counts. | Unknown | Verified Fact: `etl/run_daily_batch.py` lines 4 to 17. Replay section 1.5. |
| `policy/opa/access.rego` | policy | Allows any `admin`. Allows `operator` when the action is `read`. Default is deny. | Unknown | Verified Fact: `policy/opa/access.rego` lines 3 to 11. |
| `infra/terraform/main.tf` | infra | Declares a local file `generated-env.txt` whose content is `shared_user=app_shared`. | Unknown | Verified Fact: `infra/terraform/main.tf` lines 1 to 4. |
| `.github/workflows/ci.yml` | workflow | On push or pull request, installs `requirements.txt` and runs `pytest -q` on Python 3.11. | Unknown | Verified Fact: `.github/workflows/ci.yml` lines 1 to 11. Replay section 1.2. |
| `.env.example` | config | Holds a database URL for user `app_shared`, an AI key, a batch password, and a vendor token. Secret values are `<redacted>`. | Unknown | Verified Fact: `.env.example` lines 1 to 5. |
| `data/README.md` | doc | Says the data is synthetic and lists six CSVs of 354 rows and 3000 events. | Unknown | Verified Fact: `data/README.md` lines 1 to 15. |
| `data/manifest.json` | data | States 354 rows for each of six CSV names and 3000 JSONL events. | Unknown | Verified Fact: `data/manifest.json` keys `csv_files` and `jsonl_events`. Replay section 1.4. |
| `data/quality_issues.json` | data | Repeats four defect labels on each of six tables. | Unknown | Verified Fact: `data/quality_issues.json` key `seeded_issues`. |
| `data/synthetic/devices.csv` | data | 354 device rows. This is the only table the API reads. | Unknown | Verified Fact: `domain_service.py` line 5. Counted 354 rows in this stage. `data/manifest.json`. |
| `data/synthetic/circuits.csv` | data | 354 circuit rows. The API reads `devices.csv` only. | Unknown | Verified Fact: header and 354 rows counted in this stage. `scripts/sanity_check.py` counts every CSV named in `data/manifest.json`. |
| `data/synthetic/alarms.csv` | data | 354 alarm rows, including `storm_batch_id`. The API reads `devices.csv` only. | Unknown | Verified Fact: header and 354 rows counted in this stage. `scripts/sanity_check.py` counts every CSV named in the manifest. |
| `data/synthetic/incidents.csv` | data | 354 incident rows. The API reads `devices.csv` only. | Unknown | Verified Fact: header and 354 rows counted in this stage. `scripts/sanity_check.py` counts every CSV named in the manifest. |
| `data/synthetic/service_orders.csv` | data | 354 service-order rows. The API reads `devices.csv` only. | Unknown | Verified Fact: header and 354 rows counted in this stage. `scripts/sanity_check.py` counts every CSV named in the manifest. |
| `data/synthetic/ai_invocations.csv` | data | 354 stored AI-call rows. The live gateway leaves this file unchanged. | Unknown | Verified Fact: `ai_gateway.py` has no file write. Header counted in this stage. `scripts/sanity_check.py` counts the rows. |
| `data/synthetic/events.jsonl` | data | 3000 events. The four flow names and seven personas appear as field values. | Unknown | Verified Fact: `data/manifest.json` key `jsonl_events`. Replay section 1.4. Counted in this stage. |
| `data/contracts/openapi-fragment.yaml` | contract | Documents `GET /health` only. | Unknown | Verified Fact: `data/contracts/openapi-fragment.yaml` lines 5 to 9. Replay section 2.9. |
| `tests/test_api_contract.py` | test | Checks health status 200 and that a summary body has `summary`, `model`, and `guardrail_status`. | Unknown | Verified Fact: tests `test_health_contract` and `test_ai_summary_has_minimum_contract`. Replay section 1.3. |
| `tests/test_characterization.py` | test | Calls `load_record('DOES-NOT-EXIST')` and checks the result is a non-empty dict. | Unknown | Verified Fact: `test_legacy_missing_record_behavior_is_characterized`. Replay section 1.3 names a different test function. |
| `tests/playwright/operations.spec.ts` | test | Opens `/` and checks that the body is visible. | Unknown | Verified Fact: test `operations page shell loads`. |
| `scripts/sanity_check.py` | script | Checks required files, rejects four workshop paths, and checks CSV and event counts against the manifest. | Unknown | Verified Fact: `scripts/sanity_check.py` lines 5 to 33. Replay section 1.4. |
| `api-examples/http-requests.http` | sample | Shows health, a record read with role `operator`, and a summarize call, all on port 8000. | Unknown | Verified Fact: `api-examples/http-requests.http` lines 1 to 9. |
| `observability/otel-notes.md` | doc | Says health exists, the audit log lacks actor and correlation id, and tracing and SLOs are absent. | Unknown | Verified Fact: `observability/otel-notes.md` lines 3 to 8. |
| `security/threat-model.md` | doc | Repeats the six gap names and says to map them later. | Unknown | Verified Fact: `security/threat-model.md` lines 5 to 14. |
| `supply-chain/dependency-risk-register.md` | doc | Three rows: FastAPI with no SBOM, legacy scripts with no provenance, frontend with no lockfile. | Unknown | Verified Fact: `supply-chain/dependency-risk-register.md` lines 3 to 6. |
| `requirements.txt` | config | Pins fastapi, uvicorn, pydantic, pytest, python-dotenv, and PyYAML. It does not pin httpx. | Unknown | Verified Fact: `requirements.txt` lines 1 to 6. Replay section 1.2. |
| `pyproject.toml` | config | Sets pytest `pythonpath` to the repo root and test path `tests`. | Unknown | Verified Fact: `pyproject.toml` lines 1 to 9. |
| `Makefile` | config | Defines `test`, `smoke`, and `etl`. The name `package` is phony and has no recipe. | Unknown | Verified Fact: `Makefile` lines 3 to 12. |
| `logs/audit.log` | log | Holds JSON lines written by the API. This reading has 13 lines. | Unknown | Verified Fact: `logs/audit.log`. Replay section 3 quotes the first 7 lines. |
| `docs/00-setup/replay-log.md` | prior note | Records the S00 command and HTTP replay. | Unknown | Verified Fact: header Author is Mangesh (FDE). The file does not name a system owner. |
| `docs/00-setup/tool-versions.md` | prior note | Records tool versions from the S00 machine. | Unknown | Verified Fact: header Author is Mangesh (FDE). The file does not name a system owner. |
| `docs/00-contract/operating-contract.md` | prior note | Records what a later stage may change and what stops the work. | Unknown | Verified Fact: header Author is Mangesh (FDE). Status PROVISIONAL. |
| `docs/00-contract/cost-envelope.md` | prior note | Records a first cost view from the synthetic files. | Unknown | Verified Fact: header Author is Mangesh (FDE). Status PROVISIONAL. |
| `docs/00-contract/challenge-to-spine-crosswalk.md` | prior note | Maps challenge names to spine stages. | Unknown | Verified Fact: header Author is Mangesh (FDE). |

## Worked example

Row `GET /records/{record_id}`. The path is the route. The type is route. The job is the behaviour in `main.py`: an allowed role gets a device row and an audit line. Owner is Unknown because no file says who owns the route. The evidence is the function `get_record` and replay sections 2.2, 2.5, and 2.6.

## Owner count

55 rows. 55 owner cells say Unknown. 55 divided by 55 is more than one half. This is why the stage status is CONDITIONAL PASS.

## Lifecycle

This inventory cites `docs/00-setup/replay-log.md` and `docs/00-contract/operating-contract.md`. Stage S02 cites this dossier for behaviours to snapshot. Stage S03 harvests entities and status words from it. Stage S09 reuses the risk register.
