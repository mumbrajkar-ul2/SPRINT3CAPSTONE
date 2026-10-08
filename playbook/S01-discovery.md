# S01 — Discovery dossier (Challenge 1, D1)

Phase 1 in `Execution Plan.md`. Spine stages 0A, 5, 7. This stage maps the inherited system. It does not improve it.

## Inputs

- `Project_Intent.md` (sections 3.1, 4.2, 4.3)
- Every repo file listed in `Project_Intent.md` section 4.2 (attach the `06-telecom-service-network-incident-ops` folder)
- `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md`
- `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md`

## Prompt

```text
# Stage S01 — Discovery dossier (Challenge 1)

## Objective
Understand the inherited system `06-telecom-service-network-incident-ops` as it is. Produce the six Challenge 1 deliverables. Do not improve, refactor, or redesign anything.

## Scope
Include: every file named in `Project_Intent.md` 4.2; the replay log from S00; the operating contract from S0B.
Exclude: refactoring; redesign; target architecture; any file edit inside the repo other than new files under `docs/01-discovery/`.

## Required analysis
1. Architecture: map the three generations named in `docs/architecture/current-state.md` (legacy script, FastAPI, AI gateway). State what each one reads, writes, and calls.
2. Components: inventory every component, route, script, data file, test, policy, workflow, and infra file. One line each: path, job, owner or Unknown.
3. Business flows: reconstruct the four flows in `docs/domain-specific-spec.md`. For each flow list the steps, the data it needs, the routes that exist today, and the steps with no code. Today none of the four runs end to end; show that per flow.
4. Data and integrations: the six CSVs, `events.jsonl`, `manifest.json`, `quality_issues.json`; which table the API reads (`devices.csv` only); UI fetch wrapper to API; API to CSV; API to AI stub; audit to `logs/audit.log`; Terraform to a text file.
5. AI touchpoints: `ai_gateway.py` (prompt, model, guardrail status, token formula), the three AI products named in current-state, `ai_invocations.csv` fields, and the fact that the live gateway does not write that file.
6. Ownership: ownership boundaries and the ADR 0001 split (legacy batch kept, never revisited).
7. Risk: start from `docs/architecture/known-gaps.md`. Add what it misses, at least: `clinician` role in a telecom API; missing id returns the first row; first key `REC-0001` reused across six tables; OpenAPI documents one of three routes; AI summarize has no role check; audit rows have no actor or correlation id.
For each finding: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, or Unknown.
- A Verified Fact names a file path with a line or symbol, a test name, a log line, or a replay result from `docs/00-setup/replay-log.md`.
- Write Unknown for owners and behaviours the repo does not state.

## Constraints and guardrails
- Plain speech. Short sentences. Everyday words.
- No proposal, fix, or target design in any file. If you notice one, write it as an open question.
- No invented severity cutoff or SLA threshold.
- Redact secrets. Write <redacted> for any password, key, or token.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md 4.3; read, do not re-derive)
| Constant | Value | Where |
|---|---|---|
| Primary data file for the API | devices.csv | domain_service.py |
| Missing-record behaviour | return first row | domain_service.py, tests/test_characterization.py |
| Allowed API roles | admin, operator, clinician, engineer, ai_agent | apps/api/main.py |
| Domain personas | noc_operator, network_engineer, field_engineer, customer_support, automation_service, vendor_account, ai_agent | docs/domain-specific-spec.md |
| OPA allow rules | any admin; operator + read | policy/opa/access.rego |
| AI model version | local-sim-v1 | ai_gateway.py |
| AI prompt | "Summarize this operational record and recommend next action: {record}" | ai_gateway.py |
| Guardrail status | not_enforced | ai_gateway.py |
| Shared DB user | app_shared (password <redacted>, in legacy/reconcile_legacy.py and .env.example) | |
| CSV row counts / events | 354 each / 3000 | data/manifest.json |
| First key reused across tables | REC-0001 | first row of each CSV |
| ADR 0001 status | Accepted, never revisited | docs/ADR/0001-partial-modernization.md |
| OpenAPI coverage | /health only | data/contracts/openapi-fragment.yaml |

## Required artifacts
All under `06-telecom-service-network-incident-ops/docs/01-discovery/`:
1. `current-state-architecture.md` — three generations, what each reads, writes, calls; one diagram in Mermaid.
2. `component-inventory.md` — one table; columns: path, type, job, owner, evidence.
3. `business-flow-reconstruction.md` — four flows; steps, data, routes that exist, steps with no code.
4. `data-and-integration-map.md` — files, fields the API uses, integrations, direction of each call.
5. `ai-subsystem-discovery.md` — touchpoints, prompt, model, guardrail status, provenance fields present and absent.
6. `brownfield-risk-register.md` — one table; columns: id, risk, evidence, impact, likelihood (Unknown allowed), confidence, open question.

## Completion gate
PASS when every row in every file cites a file, test, log, or replay result, and no row proposes a change. CONDITIONAL PASS when an owner column has Unknown in more than half the rows and that is stated. BLOCKED when any of the six files is missing.

## Lifecycle linkage
Cite `docs/00-setup/replay-log.md` and `docs/00-contract/operating-contract.md`. Stage S02 cites this dossier for behaviours to snapshot. Stage S03 harvests entities and status words from it. Stage S09 reuses the risk register.

## Required final response
End with exactly these seven items:
1. Stage status: PASS, CONDITIONAL PASS, or BLOCKED, with one sentence why.
2. Key findings.
3. Major risks.
4. Assumptions and unknowns.
5. Artifacts created, with paths.
6. Blocking issues.
7. Recommended next action.
```

## Expected output

| File | Must contain |
|---|---|
| `current-state-architecture.md` | Header. Three generations. Mermaid diagram. Reads / writes / calls per generation. |
| `component-inventory.md` | Header. One row per file or route. Owner or Unknown. Evidence column. |
| `business-flow-reconstruction.md` | Header. Four flows. "Runs end to end today: No" per flow with the missing steps. |
| `data-and-integration-map.md` | Header. Nine data files. `devices.csv` marked as the only table the API reads. Five integrations with direction. |
| `ai-subsystem-discovery.md` | Header. Prompt text, model name, guardrail status, token formula. Provenance fields present and absent. |
| `brownfield-risk-register.md` | Header. Every known-gaps item plus at least six added risks. Each with evidence. |

## Done test

Open the risk register. Pick any row. Its evidence column names a file, test, log, or replay result. No row says "should" or "recommend".
