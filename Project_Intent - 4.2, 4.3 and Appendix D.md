# Project Intent — Telecom Service, Network, and Incident Operations


### 4.2 Inherited repo files

Every path below sits under `06-telecom-service-network-incident-ops`. You read these files. You do not treat them as the finished policy.

| File | What it is | What job it does | Why you need it | What you do with it |
|---|---|---|---|---|
| `README.md` | Cover note. | Names the centre of gravity, quick start, synthetic-data rule, and 16-step spine. | It is the first map of the estate. | Read first. Keep. |
| `docs/domain-specific-spec.md` | Domain card. | Names flows, personas, and the six data entities. | It is the business language the semantic layer must use. | Read. Quote in D1 and D3. |
| `docs/architecture/current-state.md` | Three-generation sketch. | Names legacy, FastAPI, and AI gateway. Names three AI products. | It is the architecture you must map, not the target. | Read. Keep. |
| `docs/architecture/target-state-principles.md` | Target principles. | Says preserve continuity, govern AI, use policy-as-code, emit evidence, make failure explicit, and tie cost to outcomes. | These are design rules, not implemented controls. | Read. Use in D4 and D5. |
| `docs/architecture/known-gaps.md` | Short gap list. | Names alarm storms, static SSH credentials, stale topology, risky AI config, duplicate tickets, overpowered automation. | It is a search list, not a complete defect list. | Review. Look for items it does not name. |
| `docs/ADR/0001-partial-modernization.md` | One accepted ADR. | Keeps legacy batch jobs while adding FastAPI. Status says it was never revisited. | It explains why rules differ across paths. | Read. Record the split in D1. |
| `docs/transformation-roadmap.md` | Modernization notes. | Lists themes and engineering concerns. | It names audit and AI metadata gaps. | Read. Keep. |
| `docs/discovery/README.md` | Empty reserved folder note. | Says discovery notes belong here. | D1 notes can go here or in a sibling pack. | Do not treat it as finished discovery. |
| `docs/runbooks/incident-response.md` | Incomplete runbook. | Says severity, triage, rollback, comms, and evidence are missing. | Spine step 11 and 15 need a real runbook. | Read. Treat missing as missing. |
| `docs/runbooks/failure-injection-drills.md` | Drill list. | Names missing correlation ids, AI timeout, duplicate replay, stale master data, partial batch failure. | These are the reliability tests you must design. | Review. Keep. |
| `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md` | Empty section list. | Mirrors the 16 spine headings. | D8 fills this. It is not evidence yet. | Keep. Fill later. |
| `apps/api/main.py` | FastAPI app. | Serves `/health`, `/records/{record_id}`, `/ai/summarize/{record_id}`. | This is the live API surface. | Read. Replay. Keep. |
| `apps/api/services/domain_service.py` | CSV loader. | Reads `devices.csv`. Missing id returns the first row. | This is the current record contract. | Replay. Characterize. Do not keep the silent fallback. |
| `apps/api/services/ai_gateway.py` | Local AI stub. | Builds a hardcoded prompt, sleeps 0.01s, returns a synthetic summary. | This is the AI trust boundary. Guardrails are `not_enforced`. | Read. Add tests later. |
| `apps/api/services/audit.py` | Append-only JSONL writer. | Writes `logs/audit.log` with timestamp, action, and details. | This is the current audit trail. No actor, no correlation id, no approval id. | Read. Use in audit-gap notes. |
| `apps/web/src/app/operations.component.ts` | Angular scaffold. | Sets a title and column names. | The portal is not wired. It trusts the backend and does not mask fields. | Read. Do not treat it as a working UI. |
| `apps/web/src/app/api.service.ts` | Fetch wrapper. | Calls `/api/records/{id}` and `/api/ai/summarize/{id}`. | It shows the intended UI-to-API path. | Read. Keep. |
| `apps/web/package.json` | Web package file. | Playwright only. No Angular runtime dependencies. | The README says the portal is a scaffold. | Read. Keep. |
| `legacy/reconcile_legacy.py` | Legacy batch script. | Counts device rows. Embeds `app_shared` / `Welcome123`. | This is the secrets and shared-account evidence. | Read. Do not copy the password into new code. |
| `etl/run_daily_batch.py` | Daily batch job. | Counts blank fields. Does not quarantine them. | This is the data-quality baseline. | Run with `--sample`. Keep the counts. |
| `policy/opa/access.rego` | Starter OPA policy. | Allows any `admin`. Allows `operator` only for `read`. | Policy-as-code exists but is coarse. It ignores resource, purpose, and risk. | Read. Extend later. |
| `infra/terraform/main.tf` | Incomplete IaC. | Writes `generated-env.txt` with `shared_user=app_shared`. | Environment assumptions are not reproducible. | Read. Treat as a gap. |
| `.github/workflows/ci.yml` | CI workflow. | Installs Python deps and runs `pytest -q`. | The pipeline runs tests. It does not emit SBOM, scan, or evidence. | Read. Keep. |
| `.env.example` | Example environment file. | Contains database URL with password, `AI_GATEWAY_KEY`, batch password, and a shared vendor token. | Challenge step 4 forbids unsafe example secrets. | Inventory. Do not treat as safe sample config. |
| `data/README.md` | Synthetic-data note. | Lists file sizes and deliberate defects. | It tells you the data is local and dirty on purpose. | Read. Profile anyway. |
| `data/manifest.json` | Row-count contract. | Expects 354 rows per CSV and 3000 events. | `scripts/sanity_check.py` uses this. | Keep. |
| `data/quality_issues.json` | Seeded-defect list. | Repeats duplicate keys, blanks, impossible timestamps, out-of-range scores. | It is a hint list. Defects must still be found in the files. | Review. Confirm in the CSVs. |
| `data/synthetic/devices.csv` | 354 device rows. | First key is `REC-0001`, not `DEV-00001`. Values leak status words into hostname and vendor. | This is the only table the API reads. | Profile. Replay `REC-0001` and a missing id. |
| `data/synthetic/circuits.csv` | 354 circuit rows. | Has SLA tier and `orphan_flag`. First key is also `REC-0001`. | Needed for order-to-provisioning and SLA evidence. | Profile. The API does not load it. |
| `data/synthetic/alarms.csv` | 354 alarm rows. | Has `storm_batch_id` and `dedupe_key`. Some `last_seen_at` values are before `first_seen_at`. | Needed for alarm-storm correlation. | Profile. |
| `data/synthetic/incidents.csv` | 354 incident rows. | Has `automation_used` and `sla_breach_risk`. Severity values include `gold` and `bronze`. | Needed for incident routing. | Profile. |
| `data/synthetic/service_orders.csv` | 354 order rows. | Has retry and rollback fields. `retry_count` values in the thousands appear. | Needed for provisioning reliability. | Profile. |
| `data/synthetic/ai_invocations.csv` | 354 AI-call rows. | Has model, tokens, risk, approval, guardrail. Some ids look malformed (`AI_-00002`). | Needed for AI FinOps and provenance. | Profile. The live gateway does not write this file. |
| `data/synthetic/events.jsonl` | 3000 events. | Mixes the four business flows, actors, latency, cost, and missing correlation ids. | Needed for observability and FinOps design. | Sample. Count null or blank `correlation_id`. |
| `data/contracts/openapi-fragment.yaml` | Partial OpenAPI file. | Documents `/health` only. | The contract is behind the code. | Read. Do not treat as the full API. |
| `tests/test_api_contract.py` | Two API tests. | Checks `/health` and a minimum AI JSON shape. | This is the current contract net. | Run. Keep. |
| `tests/test_characterization.py` | One characterization test. | Asserts a missing id still returns a dict with content. | This captures the silent fallback. Transformation should replace it with 404. | Run. Keep until you change the behaviour. |
| `tests/playwright/operations.spec.ts` | UI smoke test. | Opens `/` and checks the body is visible. | It does not prove operations behaviour. | Run if the portal is served. |
| `scripts/sanity_check.py` | Repo self-check. | Confirms required files, forbids workshop briefs inside the repo, and checks row counts. | It proves packaging, not production readiness. | Run. |
| `api-examples/http-requests.http` | Manual HTTP samples. | Shows health, record read with `X-User-Role: operator`, and AI summarize. | Useful for replay. | Use in D2. |
| `observability/otel-notes.md` | Observability note. | Says health exists, audit is thin, tracing and SLOs are absent. | Spine step 8 starts here. | Read. Keep. |
| `security/threat-model.md` | Threat-model starter. | Repeats the known-gap list and asks for STRIDE/MAESTRO. | It is not a completed model. | Read. Extend later. |
| `supply-chain/dependency-risk-register.md` | Three-row register. | Names FastAPI with no SBOM, legacy with no provenance, frontend with no lockfile discipline. | Spine step 7 starts here. | Read. Keep. |
| `requirements.txt` | Python pins. | FastAPI, uvicorn, pydantic, pytest, python-dotenv, PyYAML. | Needed to run tests and the API. | Install in a venv. |
| `pyproject.toml` | Pytest config. | Sets `pythonpath` and project name. | Needed so tests import `apps.api`. | Keep. |
| `Makefile` | Local shortcuts. | `test`, `smoke`, `etl`. | Useful for baseline commands. | Use. |

Worked example for `domain_service.py` plus `devices.csv`: `load_record("DOES-NOT-EXIST")` walks every cell in `devices.csv`. No cell matches. The function returns the first row. That row’s `device_id` is `REC-0001`. The characterization test locks this behaviour. A caller can believe a missing device exists.

### 4.3 Constants found in the inherited repo

These values appear in the files. They are current-state values. They are not a new policy you chose. A later cutoff needs a named owner and an Architecture Decision Record. Until the packet or the trainer names a business owner, that owner is Team-Force, the FDE team Mangesh belongs to (`docs/00-contract/operating-contract.md` row 10).

| Constant | Value in the files | Where it appears |
|---|---|---|
| Primary data file for the API | `devices.csv` | `apps/api/services/domain_service.py` |
| Missing-record behaviour | return first row | `domain_service.py`, `tests/test_characterization.py` |
| Allowed API roles | `admin`, `operator`, `clinician`, `engineer`, `ai_agent` | `apps/api/main.py` |
| Domain personas | `noc_operator`, `network_engineer`, `field_engineer`, `customer_support`, `automation_service`, `vendor_account`, `ai_agent` | `docs/domain-specific-spec.md` |
| OPA allow rules | any `admin`; `operator` + `read` | `policy/opa/access.rego` |
| AI model version | `local-sim-v1` | `ai_gateway.py`, `main.py` audit event |
| AI prompt | `Summarize this operational record and recommend next action: {record}` | `ai_gateway.py` |
| Guardrail status returned | `not_enforced` | `ai_gateway.py` |
| Token estimate formula | `len(prompt.split()) * 2` | `ai_gateway.py` |
| Shared DB user / password | `app_shared` / `Welcome123` | `legacy/reconcile_legacy.py`, `.env.example` |
| Example AI key | `sk-workshop-hardcoded-example` | `.env.example` |
| CSV row counts | 354 each | `data/manifest.json`, `data/README.md` |
| Event count | 3000 | `data/manifest.json` |
| First key reused across tables | `REC-0001` | first row of each CSV |
| ADR 0001 status | Accepted, never revisited | `docs/ADR/0001-partial-modernization.md` |
| OpenAPI coverage | `/health` only | `data/contracts/openapi-fragment.yaml` |
| CI Python version | 3.11 | `.github/workflows/ci.yml` |


## Appendix D — Worked replay of current runtime behaviour

Use this replay when a table cell in this file would otherwise need a lecture. Confirm each line against the source file or a live call before you treat it as locked.

**Health.** `GET /health` returns `{"status":"ok","repo":"06-telecom-service-network-incident-ops"}`. `tests/test_api_contract.py` locks this.

**Record read, known first row.** `GET /records/REC-0001` with `X-User-Role: operator` is allowed because `operator` is in the broad list. `domain_service.load_record` finds `REC-0001` in `devices.csv` and returns that row. The row’s hostname is `legacy`. Vendor is `requires_review`. Those are status words stored in the wrong columns.

**Record read, missing id.** `GET /records/DOES-NOT-EXIST` with a permitted role does not return 404. It returns the first device row. `tests/test_characterization.py` locks this. The comment in that test says transformation should replace it with 404 semantics.

**Role mismatch.** The API allow list includes `clinician`. That word belongs to another industry pack, not this telecom spec. Domain personas such as `noc_operator` and `field_engineer` are not in the API allow list. A header `X-User-Role: noc_operator` would be forbidden even though the spec names that job.

**AI summarize.** `POST /ai/summarize/REC-0001` has no role header. It loads the same device row, interpolates it into the prompt, and returns `model: local-sim-v1`, a synthetic summary, `recommendation: Review and approve before action`, a token estimate, `source_count: 1`, and `guardrail_status: not_enforced`. The audit event stores `record_id` and model name only.

**Legacy secrets.** `legacy/reconcile_legacy.py` counts device rows and contains `SHARED_DB_PASSWORD = "Welcome123"`. `.env.example` repeats that password on a PostgreSQL URL. Terraform writes `shared_user=app_shared` into `generated-env.txt`. The overpowered shared account is visible in three files.

**ETL.** `python etl/run_daily_batch.py --sample` counts rows in `devices.csv` and increments `malformed` when any field is blank. It prints counts. It does not write a quarantine file.

**Alarm timestamp defect.** `ALA-00002` has `first_seen_at` `2026-07-31T23:45:00` and `last_seen_at` `2026-02-23T09:35:00`. Last seen is before first seen. `data/quality_issues.json` said to look for impossible timestamps.

**Incident vocabulary leak.** `INC-00002` has `severity: gold`. `gold` is an SLA-tier word on circuits, not a severity word. A later metric that groups by severity will mix SLA class into incident severity.

**Events.** `data/synthetic/events.jsonl` includes the four business-flow names as `event_type`. Many rows have `correlation_id` null or `""`. `observability/otel-notes.md` already says correlation is missing.

**OpenAPI drift.** The live app has three routes. The OpenAPI fragment documents one.

---
