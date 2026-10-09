# Project Intent — Telecom Service, Network, and Incident Operations

---

## 1. Purpose of this document

This file says what this assignment is. It names the decision you must support. It names the files you start with. It names what you must hand back. It names the order of work.

After you finish this file, write [Execution Plan.md](Execution Plan.md). That file is the step list for a Forward Deployed Engineer. A Forward Deployed Engineer works at the customer site, uses AI under written rules, and leaves a system people can run and explain.

If a sentence here would still make you ask “of what?”, “why?”, or “what do I do with this?”, that sentence failed.

---

## 2. What this assignment is

### 2.1 The system, in one sentence

This assignment is about a brownfield telecom operations system. Network and service teams must decide whether an alarm, incident, order, or AI recommendation can safely become a live network action.

### 2.2 The case the trainer assigned

The challenge guide is separate from the repository. Treat the repository as a real inherited system. Discover issues from code, data, configuration, tests, logs, and docs. Do not wait for a trainer note inside the repo.

- **Domain:** Telecommunications. Service provisioning, network operations, and incident operations.
- **Repo:** `06-telecom-service-network-incident-ops`
- **Centre of gravity (README and current-state):** scale, observability, automation safety, and reliability.
- **Domain north star (`docs/domain-specific-spec.md`):** high-volume telemetry, topology truth, automation safety, change governance, and SLA evidence.
- **Business flows named in the spec:**
  1. Customer order to provisioning
  2. Alarm storm to incident correlation
  3. Topology lookup to AI recommendation
  4. Approved remediation to validation
- **AI capabilities named in current-state:** Network Incident Copilot, Configuration Assistant, Capacity Intelligence.
- **What you must keep:** business continuity, human approval on high-risk change, and an evidence trail a reviewer can rebuild.

### 2.3 What you must leave with

The challenge guide names a 16-step transformation spine, then a product path, then a final evidence pack.

1. A discovery reading of the inherited repo. You understand the current files, the gaps, the conflicts, the risks, and the technical debt. Evidence must come from code, data, configuration, tests, or repository documentation.
2. A behavioural baseline. You can tell intended legacy behaviour from defects that must be fixed.
3. Controlled improvements across identity, secrets, IaC, policy, CI/CD, observability, AI guardrails, performance, reliability, FinOps, security tests, and audit evidence.
4. A semantic layer. Markdown explains it. YAML defines it. JSON Schema validates it. Tests protect it. Generated JSON serves it.
5. A Product Requirements Document (PRD) written from the semantic layer and the improved design. A PRD is the written list of what the product must do.
6. A working application and an end-to-end demo.
7. A second-model test of the same semantic layer, then a comparison of the two apps.
8. A production evidence pack and a go/no-go decision.

Moonshot items in the challenge guide are stretch. Do not treat them as the minimum hand-back.

### 2.4 What skill is assessed

The assessed skill is this chain. You read a messy inherited estate without treating the files as the finished design. You name the operational decision, the people and objects it touches, and the action that cannot be undone. You extract a semantic layer that later models can reuse. You write a PRD from that layer. You build a working application from the PRD. You can prove what changed. You can defend whether the system is production-ready.

The final claim the challenge guide wants is:

> We understand this system, we know its risks, we improved it safely, we can prove what changed, and we can defend whether it is production-ready.

### 2.5 Teaching method

The repo is an As-Is brownfield baseline. It is runnable. It is not a clean reference. The validation report for this family of repos says mixed-generation patterns, weak authorization, partial migration, data defects, incomplete release practices, and thin observability are transformation targets, not packaging defects.

The README transformation spine is:

Understand Existing Repo → Establish Behavioural Baseline → Identity & Least Privilege → Secrets & Encryption → Infrastructure as Code → Policy as Code → CI/CD & Supply Chain → Observability & Traceability → AI Security & Guardrails → Performance & Scalability → Reliability & Failure Engineering → Cost & AI FinOps → Automated Security Validation → Auditability & Compliance Evidence → Production Readiness Gate → Production Evidence Pack

The challenge guide then adds this product path:

Develop & Extract Semantic Layer → Develop PRD → Develop APP → Demo → Test Semantic Layer with new model → Compare and contrast APPs - Both Models

The work path for this packet is:

Inherited repo → Discovery and baseline → Semantic layer → Governed design → PRD → Working application → Second-model test → Evidence pack.

### 2.6 Why the main tools and files exist

Each heading names one thing used in this assignment. The next sentences say what it is, what job it does, why you need it, and what you do with it.

#### Challenge guide (`AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf`)

This file is the assignment contract. It names the 16 spine steps, the moonshot list, the semantic-layer-to-app path, and the final submission standard. You need it so you build what the trainer asked for. You read it. You keep it. You do not replace it with repo README wording when the two differ. If they differ, write both sides.

#### Semantic layer capture (`Semantic_Layer_capture.pdf`)

This two-page file is the format contract for the semantic layer. It says Markdown is for people, YAML is the source of truth, JSON Schema validates structure, tests protect behaviour, and generated JSON serves apps. You need it so later models read the same meanings. You follow the folder list it names. You do not store the only definitions in a long essay.

#### Inherited repo (`06-telecom-service-network-incident-ops`)

This folder is the brownfield estate. It holds FastAPI code, a thin Angular scaffold, legacy scripts, ETL, synthetic data, a starter OPA policy, incomplete Terraform, CI, tests, and short docs. You need it as the evidence for discovery and as the input to the semantic layer. You read it. You run the checks. You do not tidy it on day one to look finished.

#### Cursor

Cursor is an AI-powered code editor. It reads the project files and can write or edit files when you give a prompt. You need it to inspect the repo, draft the semantic layer, draft the PRD, and keep a chat transcript. You review every output before you accept it.

#### A language model of your choice, then a second model

A language model is the program that writes text from a prompt. The challenge guide requires you to test the semantic layer with a new model and to compare two apps. You need two models so you can show the YAML meanings travel. You attach the semantic layer. You do not paste a new private glossary into the second prompt.

#### Execution Plan (`Execution Plan.md`)

This file is the ordered work method. You need it after you finish this Project Intent. You follow it. You do not skip discovery or the semantic layer.

### 2.7 What the program does today, and what this packet leaves out

The domain spec names four desk jobs. The running program does three small things, plus two scripts. The build in this packet completes one job to a human decision and writes the other limits down.

**What you can call today.** `GET /health` answers that the program is up. `GET /records/{id}` reads `data/synthetic/devices.csv` only. A missing id returns the first row, `REC-0001`. The response includes `mgmt_ip` and `credential_profile`. `POST /ai/summarize/{id}` has no role check. It puts the whole device row into a fixed prompt, waits 0.01 seconds, and returns a synthetic summary, the line "Review and approve before action", and `guardrail_status: not_enforced`. The model name is `local-sim-v1`. Nothing is sent to a hosted model. Nothing is changed on a device. `data/synthetic/ai_invocations.csv` has token and approval columns. The live gateway does not write that file. `apps/web` names a title and two API paths. It does not open in a browser. `GET /` returns 404.

**What the files describe and the API does not run.**

| Desk job | Where the words and rows are | What is missing in the running program |
|---|---|---|
| Take a customer order for a circuit | `docs/domain-specific-spec.md`. `service_orders.csv` (354 rows; `ORD-00002` is `failed` / `in_progress` with `retry_count` 4052). `circuits.csv` holds the circuit, the SLA tier, and `orphan_flag`. | No route reads an order or a circuit. |
| Group a flood of alarms into one incident | `alarms.csv` has `storm_batch_id` and `dedupe_key`. Alarm `ALA-00002` has last seen on 23 February 2026 and first seen on 31 July 2026. `incidents.csv` uses `gold` and `bronze` as severity (`INC-00002`, `INC-00005`). `known-gaps.md` lists `alarm_storms` and `duplicate_tickets`. | The API does not open `alarms.csv` or `incidents.csv`. |
| Look up a device and ask for a next step | `current-state.md` names Network Incident Copilot, Configuration Assistant, and Capacity Intelligence. The live summarize route is the only AI call. `known-gaps.md` lists `stale_topology` and `risky_ai_config_suggestion`. | The suggestion can describe `REC-0001` when the caller asked for an id that is not in the file. There is no approval id. |
| Check that an approved fix worked | `incident-response.md` says severity, triage, rollback, communication, and evidence are missing. `failure-injection-drills.md` names five drills. They are a list, not tests. `known-gaps.md` lists `overpowered_automation_account`. | No route applies a change. No route reads the device again and records whether the fix worked. |

**What this packet will build, and what it will leave written as not built.** The demo flow is topology lookup, a human decision, and alarm-storm dedupe. Later stages add `GET /alarms/storms/{storm_batch_id}`, `POST /ai/recommend/{id}`, and `POST /approvals/{id}`. `POST /ai/summarize/{id}` stays. The guardrail stage hardens it. The recommend route is new. The demo page calls the recommend route.

Order provisioning stays unimplemented because no route reads `service_orders.csv` or `circuits.csv`. Remediation validation stays unimplemented because this packet does not apply a live change, so there is no result to check. The PRD states both sentences. Qualify, provision, retry, rollback, and a "did the fix work" route are not added.

One data defect does get a test. Alarm `last_seen_at` cannot precede `first_seen_at`. A row shaped like `ALA-00002` is flagged and does not become an incident. That test is separate from the check on `stale_topology_flag`.

---

## 3. What is expected

### 3.1 Decisions you must write down first

Use the trainer’s words and the repo files. If a row is missing from the packet, write Unknown. Do not guess a business cutoff.

| # | Question | Answer from this packet |
|---|---|---|
| 1 | What event arrives? | One of four named flows: a customer service order, an alarm storm that may become an incident, a topology lookup that asks AI for a next action, or an approved remediation that still needs validation. The running API today only exposes record read and AI summarize. |
| 2 | Which people or objects does it touch? | People named in the domain spec: `noc_operator`, `network_engineer`, `field_engineer`, `customer_support`, `automation_service`, `vendor_account`, `ai_agent`. Objects named in the data model: devices, circuits, alarms, incidents, service orders, AI invocations, and operational events. |
| 3 | What action cannot be undone? | A live network change. That means a config push, an automated remediation, a provisioning change, or a close of an incident that hides a real outage. The current code does not push to a device. The current AI path can still recommend an action with `guardrail_status: not_enforced`. |
| 4 | What did they give you? | A brownfield repo, a challenge guide, and a semantic-layer format PDF. There is no finished PRD and no finished semantic layer in the packet. |
| 5 | What must you hand back? | Discovery and baseline, controlled improvements with evidence, a semantic layer in the capture-PDF format, a PRD, a working app and demo, a second-model semantic-layer test, an app comparison, and a production evidence pack with a go/no-go. |
| 6 | Who is harmed if the score or route is wrong? | A customer, if an SLA on a circuit is missed. The network, if a risky config is applied. Field and NOC staff, if duplicate tickets or stale topology hide the real fault. The company, if an overpowered automation account or an ungoverned AI agent changes production. |
| 7 | Which facts exist at decision time? | The domain spec lists fields on devices, circuits, alarms, incidents, service orders, and AI invocations. The running API does not use those tables. It reads `data/synthetic/devices.csv` only. A missing id returns the first row. The AI prompt interpolates the whole row. |
| 8 | What still works if the AI path is down? | Unknown as a designed degraded mode. `/health` and `/records/{id}` do not call the model. `/ai/summarize/{id}` has no timeout, no circuit breaker, and no fail-to-person path. The failure-injection runbook names an AI timeout drill. The runbook is a draft. |

Worked example for row 3: `POST /ai/summarize/REC-0001` returns `recommendation: Review and approve before action` and `guardrail_status: not_enforced`. There is no approval id, no policy decision, and no role check on that route. If a later worker treats that JSON as a change ticket, the recommendation has become an operational decision.

### 3.2 Deliverables

| Deliverable | What it is | What proves it is done |
|---|---|---|
| D0. Project Intent | This file. The locked brief. | Event, entities, irreversible action, hand-back list, and Unknown rows are written. |
| D1. Repo discovery dossier | Current-state map, component inventory, flow reconstruction, data map, AI touchpoints, risk register. | Every claim cites a file, a test, a log, or a runtime result. |
| D2. Behavioural baseline | Test report, behaviour snapshot, characterization tests, data-quality baseline, defect list. | You can point to a behaviour you must keep and a defect you must fix. Missing-record fallback is one of those defects. |
| D3. Semantic layer | The `semantic-layer/` tree from `Semantic_Layer_capture.pdf`. | `entities.yaml`, `relationships.yaml`, `status-taxonomy.yaml`, `business-rules.yaml`, `metrics.yaml`, `access-semantics.yaml`, and `ai-context-policy.yaml` exist. Schema tests pass. Glossary matches YAML. |
| D4. Spine controls | Identity, secrets, IaC, policy-as-code, CI/CD, observability, AI guardrails, performance, reliability, FinOps, security tests, audit chain. | At least one high-risk decision is governed by executable policy with allow and deny cases. AI output cannot silently become an action. |
| D5. PRD | Product Requirements Document written from the semantic layer and D4. | It names users, workflows, AI limits, data, risk, non-functional needs, acceptance checks, and success metrics. It names the demo flow. It states that order provisioning and remediation validation are not built, each with the reason in section 2.7. |
| D6. Working application and demo | A running system built from the PRD. | The demo walks one of the four business flows to a human decision. One case can be rebuilt from the audit row. |
| D7. Second-model test and app comparison | The same semantic layer is given to a new model. Two apps are compared. | Meanings did not drift. Differences are written. The YAML stayed the source of truth. |
| D8. Production evidence pack | Proof, not only code. | A reviewer can verify the transformation without a verbal tour. The pack states ready, not ready, and accepted risk. |
| Presentation | A walkthrough of D1 to D8. | You can answer the defence questions in section 3.3. |

### 3.3 Defence

Defence means you answer with evidence, not opinion.

1. What event did you route, and which facts existed at decision time?
2. Which of the four business flows did the demo run, and which API routes still do not implement that flow?
3. What action cannot be undone, and where does a human approve it?
4. What would a retry duplicate, and how did you prove the count?
5. Rebuild one case: actor, request, data used, model and version, policy result, approval, final action, trace id, and what you still cannot prove.
6. Which inherited gap did you leave visible until a spec closed it?
7. How does a person contest an AI recommendation?
8. What still runs if the AI gateway times out?
9. How did the second model use the same semantic layer, and what changed in the second app?
10. Is the system production-ready? What risk is accepted, and who owns it?

---

## 4. Inputs

### 4.1 Assignment files outside the inherited repo

| File | What it is | What job it does | Why you need it | What you do with it |
|---|---|---|---|---|
| `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf` | Six-page assignment contract. | Names the 16 spine steps, moonshots, semantic-layer path, and final claim. | It is the source of the hand-back list. | Read. Keep. Present from it. |
| `Semantic_Layer_capture.pdf` | Two-page format contract. | Names file types and the `semantic-layer/` tree. | Later models and the PRD must share one meaning set. | Follow. Do not invent a second folder layout. |
| `Assignment Material/AI_FDE_Brownfield_Repos_v2_Validation_Report.md` | Packaging note for an earlier four-repo set. | Says those repos are runnable baselines with deliberate debt. | It explains the teaching stance. It does not describe repo 06 file counts. | Read. Do not copy its SHA values as this repo’s proof. |
| `Execution Plan.md` | Ordered work method. To be written after this file. | Turns this Project Intent into steps. | You need a sequence after you restate the brief. | Follow once it exists. |
| `.cursor/rules/plain-speak.mdc` | Writing rule for this project. | Requires short sentences and everyday words. | The reader must know what to picture after one pass. | Keep. Use when you write. |
| `.cursor/rules/chat-transcript.mdc` | Logging rule for this project. | Appends each chat turn to `transcript/chat_transcript.md`. | The assignment work stays replayable. | Keep. |

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

These values appear in the files. They are current-state values. They are not a new policy you chose. A later cutoff needs a named owner and an Architecture Decision Record.

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

### 4.4 Accounts and tools

| Tool | What it is | Why you need it |
|---|---|---|
| Cursor | AI-powered editor for this workspace. | Inspect files, write D1 to D5 notes, keep the transcript. |
| Python 3.10+ | Language of the API, ETL, and tests. | Create a venv, install `requirements.txt`, run pytest, ETL, and uvicorn. |
| pytest | Test runner already wired in `pyproject.toml`. | Capture the behavioural baseline. |
| uvicorn | ASGI server pinned in `requirements.txt`. | Run the API for replay. |
| A first language model | Text generator used under a written brief. | Draft semantic layer, PRD, and design from cited files. |
| A second language model | Independent generator for the same YAML. | Challenge-guide step: test the semantic layer with a new model. |
| PDF reader | Program that opens the two assignment PDFs. | Confirm the `.md` extract matches the PDF. |
| Playwright (optional) | Browser test named in the web scaffold. | Only needed when the portal is actually served. |

No cloud account is required to read or run the inherited repo. All data is local and synthetic. If a later build calls a hosted model, label which numbers the app really computed. (See Appendix B.)

---

## 5. Approach

The order of work is [Execution Plan.md](Execution Plan.md). This section only names the path and what each step produces for the next.

### 5.1 How this packet maps to the challenge guide

**Primary method:** inherited brownfield repo. Inspect first. Replay the API and the ETL. Treat a missing control as missing.

**Do not:** tidy Repo files on day one, invent a severity cutoff, or treat `docs/architecture/known-gaps.md` as the full defect list.

**Semantic layer method:** follow `Semantic_Layer_capture.pdf`.

- Markdown explains it.
- YAML defines it.
- JSON Schema validates it.
- Tests protect it.
- Generated JSON serves it.

YAML is the core because people can read it, machines can parse it, Git can diff it, and a second model can consume it.

### 5.2 Use-case split

The repo name is one product. The domain spec names four flows. The current-state note names three AI products. Classify them before you write the PRD.

| Use case | What arrives | What a person or system may do | Irreversible if executed |
|---|---|---|---|
| Order to provisioning | `service_orders` row | Qualify, provision, retry, or roll back a circuit | A wrong circuit or bandwidth in production |
| Alarm storm to incident | `alarms` plus topology | Dedupe, correlate, open or merge an incident | A missed outage or a flood of duplicate tickets |
| Topology to AI recommendation | device / incident / alarm context | Ask the copilot or config assistant | None, if the output stays a recommendation |
| Approved remediation to validation | An approved change | Apply, validate, or roll back | The live device or service change |

The running code implements none of those four flows end to end. It implements health, a device-row read, and a synthetic summary. Section 2.7 names the file evidence for each job, the routes this packet adds, and the two jobs that stay unimplemented when the demo stays topology lookup plus alarm-storm dedupe.

### 5.3 Analyse / recommend / decide / execute

A person can be harmed, so keep these four verbs separate.

| Verb | Who may do it today | What the files show |
|---|---|---|
| Analyse | API `load_record`, ETL blank-field count | Analysis can return the wrong device. ETL does not quarantine. |
| Recommend | `ai_gateway.summarize_record` | Hardcoded prompt. Untrusted fields interpolated. No output schema. |
| Decide | Intended: a named human or executable policy | OPA is not called by the API. AI summarize has no role check. |
| Execute | Intended: automation only after approval | No execute route exists. That absence is safer than a silent execute. Keep it until policy, approval, and audit exist. |

### 5.4 Order

| Step | What you produce | What the next step uses |
|---|---|---|
| Restate the brief | This Project Intent. | Execution Plan and D1 use the locked answers. |
| D1 Discovery | Architecture map, inventory, flows, risks. | Baseline and semantic-layer entities come from this map. |
| D2 Baseline | Test report, data profile, characterization tests. | You change behaviour only after it is named. |
| D3 Semantic layer | `semantic-layer/` in the capture-PDF layout. | PRD, policy, and both models use these meanings. |
| D4 Spine controls | Identity, secrets, policy, observability, AI gates, reliability, evidence. | The PRD can require controls that already have a design. |
| D5 PRD | Requirements and acceptance checks. | The application is built only from this PRD. |
| D6 Application and demo | A running flow with a human decision. | The second model and the evidence pack use this app. |
| D7 Second-model test | Same YAML, new model, written comparison. | Shows the semantic layer is the portable source of truth. |
| D8 Evidence pack | Ready / not ready / accepted risk. | The presentation and defence use this pack. |

What goes wrong if you skip D1 or D3: you generate a tidy app that still summarizes the first CSV row, or you let the second model invent new status words.

---

## 6. How you know the work is complete

Tick a row only if the challenge guide or the semantic-layer PDF asked for it.

### 6.1 Ready to start the semantic layer (after D1 and D2)

- [ ] The 16 spine steps and the semantic-layer-to-app path are copied into your notes.
- [ ] Event, entities, and live-network change as the irreversible action are named.
- [ ] The four business flows are classified. The three AI names are classified.
- [ ] Unknown is written where the repo is silent, including AI-down behaviour.
- [ ] You have run `pytest`, `scripts/sanity_check.py`, and `etl/run_daily_batch.py --sample`.
- [ ] You have replayed `/health`, `/records/REC-0001`, `/records/DOES-NOT-EXIST`, and `/ai/summarize/REC-0001`.
- [ ] You have not invented a severity cutoff or an SLA threshold.

### 6.2 Semantic layer done

- [ ] The folder matches `Semantic_Layer_capture.pdf`.
- [ ] `glossary.md` explains terms in everyday words.
- [ ] YAML defines entities, relationships, statuses, rules, metrics, access, and AI context.
- [ ] Status words used in code, docs, and CSV are listed. Collisions such as `gold` used as incident severity are named.
- [ ] JSON Schema validates the YAML.
- [ ] Tests fail when a required entity, status, or rule is missing.
- [ ] Generated JSON is produced from YAML, not edited by hand.

### 6.3 Done enough to hand back

- [ ] D1 exists. Inherited-repo meaning is unchanged unless a later ADR says why.
- [ ] D2 exists. Intended behaviour and defects are in different lists.
- [ ] D3 exists and passed schema tests.
- [ ] D4 exists. At least one high-risk decision has allow and deny policy tests. AI cannot silently execute.
- [ ] D5 exists. The PRD traces to YAML ids.
- [ ] D6 exists. The demo completes one flow to a human decision. The audit row is written before any execute-like state change.
- [ ] An AI timeout or schema failure sends the case to a person and stores no fake safe recommendation.
- [ ] D7 exists. The second model consumed the same YAML. Differences are written.
- [ ] D8 exists. Ready, not ready, and accepted risk have owners.
- [ ] Demo numbers carry an honesty label: REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL.
- [ ] You can answer the section 3.3 questions.

---

## 7. Words used in this assignment

| Word | What it means here |
|---|---|
| Inherited repo | The brownfield folder `06-telecom-service-network-incident-ops`. |
| Semantic layer | The shared meaning set. YAML is the source of truth. Markdown explains it. Schema and tests protect it. |
| PRD | Product Requirements Document. The written list of what the product must do. |
| Spine | The 16 transformation steps in the challenge guide and the repo README. |
| Brownfield | An inherited running environment with gaps. You improve it in pieces. You do not pretend it is empty. |
| Evidence vs truth | A file shows a claim or a behaviour. Two files can disagree. You write both sides. |
| Characterization test | A test that locks current behaviour so you can see when you change it. |
| Guardrail | A check that stops or holds an AI output before it can become an action. |
| Policy as code | A written rule a machine can allow or deny, with tests. |
| Topology truth | A device and circuit map that matches the live network. `stale_topology_flag` marks rows that may not. |
| Alarm storm | Many alarms in a short window, often one fault. `storm_batch_id` is the current grouping field. |
| Remediation | A change meant to clear a fault. Approval must come before execute. |
| SLA | Service level agreement. The promised repair or provision time for a customer circuit. |
| FinOps | Cost tied to a business outcome, such as tokens per correlated incident, not only total spend. |
| SBOM | Software bill of materials. A list of dependencies used for release evidence. |
| ADR | Architecture Decision Record. What you chose, why, and what follows. |
| FDE / AI FDE | An engineer at the customer site who uses AI under written rules and leaves a system people can run and explain. |
| Moonshot | Stretch work in the challenge guide. Not required for the minimum hand-back. |
| Honesty class | REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. A label on a number the demo shows. |

---

## 8. Glossary of terms, acronyms, and concepts

| Term | Full form | What it means here |
|---|---|---|
| ABAC | Attribute-Based Access Control | Access that also uses purpose, resource, scope, and risk, not only role. |
| API | Application Programming Interface | The FastAPI routes under `apps/api/main.py`. |
| CI | Continuous Integration | The GitHub Actions workflow that today only runs pytest. |
| ETL | Extract, Transform, Load | `etl/run_daily_batch.py`. Today it counts blanks and continues. |
| IaC | Infrastructure as Code | Environment defined in files. Today `infra/terraform/main.tf` only writes a local text file. |
| NOC | Network Operations Centre | The team that watches alarms and incidents. Persona: `noc_operator`. |
| OPA | Open Policy Agent | The policy engine. Starter file is `policy/opa/access.rego`. |
| OTel | OpenTelemetry | The tracing style named in `observability/otel-notes.md`. Not implemented. |
| RBAC | Role-Based Access Control | Access by role only. Current API header `X-User-Role` is this, and it is too broad. |
| SLO | Service Level Objective | A numeric reliability target. None exist in the repo. |
| STRIDE / MAESTRO | Threat-model methods | Named in `security/threat-model.md`. Not yet applied. |

---

## Appendix A — Challenge guide path

The trainer text, shortened to one sentence each.

**Spine**

1. Understand the existing repo and write a discovery dossier from evidence.
2. Capture current behaviour before you change it.
3. Design least-privilege access that uses role, resource, purpose, scope, and risk.
4. Remove unsafe secrets and harden sensitive data.
5. Make the environment reproducible with IaC.
6. Encode at least one high-risk decision as policy with allow and deny cases.
7. Strengthen CI/CD so the pipeline emits evidence, not only commands.
8. Correlate one business event from UI to API to AI to approval to action.
9. Keep AI recommendations from becoming silent operational decisions.
10. Tie performance bottlenecks to business impact.
11. Define what continues safely when a dependency fails.
12. Explain cost per business outcome.
13. Prove security controls with repeatable tests.
14. Reconstruct actor, data, model, policy, approval, and action.
15. Say what is ready, what is not, and what risk is accepted.
16. Package the proof so a reviewer does not need a verbal tour.

**Product path after the spine**

1. Develop and extract the semantic layer.
2. Develop the PRD.
3. Develop the app.
4. Demo.
5. Test the semantic layer with a new model.
6. Compare and contrast both apps.

**Final standard**

A reviewer can verify the transformation without relying on verbal explanation.

---

## Appendix B — Honesty classes

A demo can show a number that the live app computed, a number computed earlier and stored, a number made for teaching, or a number that is only a classroom example.

- **REAL:** the running app computed this value from the case in front of you.
- **PRECOMPUTED:** a script computed this value earlier. The screen reads it back.
- **SIMULATED:** the value stands in for a live service you did not call. `local-sim-v1` summaries are SIMULATED until a real model is called.
- **EDUCATIONAL:** the value exists to teach a point. It is not an operating metric.

Token estimates that use `len(prompt.split()) * 2` are EDUCATIONAL unless you replace the formula with a real tokenizer and a real model bill.

---

## Appendix C — Why AI must not silently act

The challenge guide acceptance line for AI security is:

> AI recommendations must not silently become operational decisions.

The current gateway returns a recommendation and `guardrail_status: not_enforced`. The summarize route has no role check, no policy call, no approval id, and no output schema.

Keep four outcomes for a recommendation:

| Outcome | Meaning |
|---|---|
| RECOMMEND_ONLY | Show the text. Do not create a change. |
| HOLD_FOR_REVIEW | A named person must accept or reject. |
| BLOCK | Policy or guardrail refused the output. |
| EXECUTE | Allowed only after policy allow, human approval when required, an audit row, and a reversible or validated change plan. |

The inherited API has no EXECUTE route. Do not add one until those four gates exist.

---

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

## Appendix E — Semantic layer file map

Copy this layout from `Semantic_Layer_capture.pdf`. Fill it from this telecom packet. Do not add a parallel meaning file outside this tree.

```text
semantic-layer/
├── README.md
├── glossary.md
├── entities.yaml
├── relationships.yaml
├── status-taxonomy.yaml
├── business-rules.yaml
├── metrics.yaml
├── access-semantics.yaml
├── ai-context-policy.yaml
├── schemas/
│   └── semantic-layer.schema.json
└── tests/
    └── test_semantic_layer.py
```

| File | What it must define for this domain |
|---|---|
| `glossary.md` | Everyday meanings for device, circuit, alarm, incident, service order, AI invocation, topology, SLA, remediation, guardrail. |
| `entities.yaml` | The six domain entities and their fields from `docs/domain-specific-spec.md`. Mark which fields the API actually reads today. |
| `relationships.yaml` | Device to alarm. Circuit to customer and incident. Incident to AI invocation. Order to circuit. Event to entity. |
| `status-taxonomy.yaml` | Allowed values for severity, incident status, order status, guardrail status, approval. List collisions found in the CSVs. |
| `business-rules.yaml` | Missing id must not return another device. AI output cannot execute. Alarm last_seen cannot precede first_seen. Shared admin is not least privilege. |
| `metrics.yaml` | SLA breach risk, alarm-storm size, token count per invocation, cost per correlated incident, quarantine rate, retry count. |
| `access-semantics.yaml` | Map domain personas to actions, resources, purpose, and risk. Do not keep `clinician` as a telecom role. |
| `ai-context-policy.yaml` | Which fields may enter a prompt, required output schema, model provenance, approval gate, and fail-to-person behaviour. |

YAML is the source of truth. If the PRD and the YAML disagree, fix the PRD or record an ADR. Do not keep two meanings.