# S05-14 — Auditability and compliance evidence (Challenge 14)

Phase 5 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted". After this stage one case can be rebuilt from stored rows.

Revised after S05-13. The input list now names the evidence files from S04-03 to S05-13. The row has 15 keys. Half B adds the first policy row that lets a role read the audit log.

## Inputs

Question and code:
- `Project_Intent.md` (section 3.3 question 5)
- `Project_Intent - section 3.3 question 5.md`
- `06-telecom-service-network-incident-ops/apps/api/services/audit.py` (after S04-12; the row has 15 keys)
- `06-telecom-service-network-incident-ops/apps/api/main.py`
- `06-telecom-service-network-incident-ops/apps/api/services/policy.py`
- `06-telecom-service-network-incident-ops/logs/audit.log` (tracked by git; 96 old lines have 3 keys and no `correlation_id`)

Before and after:
- `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md` (the S00 row is near line 187)
- `06-telecom-service-network-incident-ops/docs/02-baseline/behaviour-snapshot.md` (the S00 row is near line 107)

Design files:
- `06-telecom-service-network-incident-ops/docs/03-identity/target-access-matrix.md`
- `06-telecom-service-network-incident-ops/docs/03-identity/policy-input-model.md`
- `06-telecom-service-network-incident-ops/docs/06-policy/ai-action-policy-design.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/log-schema.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/trace-design.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/incident-reconstruction.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/model-provenance-design.md`
- `06-telecom-service-network-incident-ops/docs/transformation-roadmap.md`

Evidence files (for the compliance mapping):
- `06-telecom-service-network-incident-ops/docs/04-secrets/evidence.md`
- `06-telecom-service-network-incident-ops/docs/06-policy/evidence.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/evidence.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/evidence.md`
- `06-telecom-service-network-incident-ops/docs/11-reliability/recovery-evidence.md` (audit write lock; 500 responses with no correlation id)
- `06-telecom-service-network-incident-ops/docs/12-finops/evidence.md` (adds `token_estimate_method`, the 15th key)
- `06-telecom-service-network-incident-ops/docs/13-security-validation/evidence.md`
- `06-telecom-service-network-incident-ops/docs/13-security-validation/abuse-case-evidence.md`
- `06-telecom-service-network-incident-ops/docs/13-security-validation/remediation-backlog.md` (`SB-03`, `SB-12`, `BL-09`)
- `06-telecom-service-network-incident-ops/security/threat-model.md` (audit threats on boundary B8)
- `06-telecom-service-network-incident-ops/evidence/junit-security.xml`

Challenge guide (used by Required analysis item 4):
- `How the product spine addresses the 16 challenges - plain speak.md` (section 14)
- `06-telecom-service-network-incident-ops/docs/00-contract/challenge-to-spine-crosswalk.md`

YAML and policy files:
- `06-telecom-service-network-incident-ops/semantic-layer/access-semantics.yaml` (`resource.audit_log`, `purpose.audit_review`)
- `06-telecom-service-network-incident-ops/semantic-layer/business-rules.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/ai-context-policy.yaml` (`forbidden`, `forbidden_credential_names`)
- `06-telecom-service-network-incident-ops/policy/opa/policy_data.json` (has no audit-read grant today)
- `06-telecom-service-network-incident-ops/policy/tests/fixtures/`

Tests to read for the stored row shape:
- `06-telecom-service-network-incident-ops/tests/observability/test_audit_schema.py`
- `06-telecom-service-network-incident-ops/tests/ai/test_guardrails.py`

## Prompt

```text
# Stage S05-14 — Auditability and compliance evidence (Challenge 14)

## Objective
Half A: state what the audit trail could not prove before, design the decision provenance record, and show the evidence chain for one case. Half B: add a route that rebuilds a case from stored rows by correlation_id.

## Scope
Include: the old audit row shape; the S04-08 log schema as extended by S04-12 (15 keys); the S04-09 provenance fields; the S04-06 policy result; the approval id (null until S07); the known audit gaps from S05-13 (SB-03, SB-12, BL-09).
Exclude in Half A: any code change, and any edit to policy/opa/policy_data.json or the Rego files.
Exclude in Half B: the approvals route itself (S07); a database or external store (PROPOSED only). Half B may edit policy_data.json, the Rego files, the Python policy copy, the fixtures, and the agreement tests for the one new audit-read row, and nothing else in policy.

## Required analysis (Half A)
1. Audit gap report: the old row had timestamp, action, record id, model name. For each provenance question (who, what request, what data, which model and version, which policy result, which approval, what final action, which trace id) say whether the old row could answer it. Cite docs/00-setup/replay-log.md. Also say that the 96 old lines with 3 keys have no correlation_id and cannot be found by it.
2. Decision provenance model: the fields a complete record needs, grouped as actor, request, data used, model, policy, approval, final action, trace, and a "cannot be proven" list. Map each field to the log schema field and YAML id. The 15 keys have no trace id field. Name the field that answers "trace id" in defence question 5 (correlation_id is the likely answer) and write one "Open question for S03:" line for it.
3. Evidence chain for one case. Do not take an id from the real log, because test runs add rows to it. Make three calls that share one chosen X-Correlation-Id: a record read, a summary, and a denied call. List every stored row in order. Show the chain. Mark what is still missing (approval_id is null; final action is none).
4. Compliance evidence mapping: for each control area in the challenge guide (identity, secrets, policy, AI, audit) name the stored evidence that proves it and where a reviewer finds it. Use the evidence files listed under Inputs. Name the test file and test name where the evidence is a test.
5. Before-and-after audit example: POST /ai/summarize/REC-0001 from S00 (before) next to the same call now (after, 15 keys). Show both rows in full, secrets redacted.
6. Audit-read access: no role may read the audit log today. The access matrix has no row for resource.audit_log, and policy_data.json has no grant for it. Propose one new matrix row: which role, which purpose (purpose.audit_review exists in access-semantics.yaml), and allow or deny. Who may read the audit log is a business decision for Team-Force. Write one "Open question for S03:" line for any persona, scope, or rule id the YAML lacks.
For each finding: finding, evidence, impact, risk, confidence, open questions.
The "cannot be proven" list must include log integrity. The log is a plain file. Anyone with file access can edit or delete lines (SB-12). The route cannot prove that a chain is complete or unchanged.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Add the audit-read row from Half A to the Python policy copy, the Rego copy and policy_data.json, the fixtures, and the agreement tests. All existing policy tests must still pass.
2. Add apps/api/services/audit_query.py that reads logs/audit.log and returns every row for a correlation_id in time order. Rows with no correlation_id are never returned.
3. Add GET /audit/{correlation_id} in main.py. The order inside the route is: call the policy first, then look up the id. A caller with no permission gets 403 for an id that exists and for one that does not. Otherwise 404 would reveal which ids exist. The route writes its own audit row and returns the chain plus a cannot_prove list. The list is computed from null fields and always includes log integrity.
4. Add tests/audit/test_audit_rebuild.py. Mark every test @pytest.mark.security. Use a temporary log file. Tests:
   - a known chain is returned in order;
   - an unknown id returns 404 and writes its own row;
   - a role without audit permission gets 403 and a policy.deny row, for an id that exists and for one that does not;
   - the log file is unchanged except for the route's own row;
   - the response holds no field.device.mgmt_ip, no field.device.credential_profile, and no name from forbidden_credential_names;
   - an id longer than the limit you set is refused;
   - cannot_prove includes approval_id and log integrity.
5. No test may be skipped or marked to fail. The security stage fails the build on a skipped test. Update the test counts in docs/07-cicd/evidence.md if they change.
6. State which policy engine the tests use. tests/conftest.py forces the Python copy under tests/. The app picks opa when it is on the PATH, which makes each decision slow (SB-20, decision still open).
7. Run the route for the case from Half A. Record in docs/14-audit/evidence.md.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a log line, a route response, or a test name.
- Stored rows are REAL. The model is a stub (local-sim-v1) and its output is SIMULATED. Rows store prompt_hash, model, and tokens. They store no summary text.
- tokens is an estimate. token_estimate_method says how (word_count_x2_EDUCATIONAL). Label it as an estimate.

## Constraints and guardrails
- Plain speech.
- The audit route never alters the log. Read only.
- Redact secrets in every pasted row.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Old audit row | ts, action, details (record id, model name) |
| Current schema (S04-08, extended by S04-12) | ts, correlation_id, actor, role, action, resource, policy_decision, approval_id, model, model_version, prompt_hash, tokens, latency_ms, outcome, token_estimate_method (15 keys) |
| Old lines in logs/audit.log | 96 lines with 3 keys and no correlation_id |
| Audit read access today | none. No matrix row and no policy grant for resource.audit_log |
| Approval route | not built until S07; approval_id is null in this stage |
| Defence question 5 | actor, request, data used, model and version, policy result, approval, final action, trace id, what cannot be proven |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/14-audit/`:
1. `audit-gap-report.md`
2. `decision-provenance-model.md`
3. `evidence-chain-one-case.md`
4. `compliance-evidence-mapping.md`
5. `before-and-after-audit-example.md`
6. `audit-read-access-design.md`
Half B:
7. `apps/api/services/audit_query.py`, GET /audit/{correlation_id} in main.py
8. The audit-read row in the Python policy copy, the Rego copy, policy_data.json, the fixtures, and the agreement tests
9. `tests/audit/test_audit_rebuild.py`
10. `docs/14-audit/evidence.md`

## Completion gate
Half A PASS when the chain for one case shows what happened, who or what influenced it, and the unproven items, and the audit-read row is designed. Half B PASS when the route returns that chain, the tests pass, and no security test is skipped. CONDITIONAL PASS when approval_id is null and that is listed under cannot_prove. BLOCKED when the route can return a chain without a policy check, writes no audit row for itself, or answers 404 before it checks policy.

## Lifecycle linkage
Cite docs/00-setup/replay-log.md, docs/02-baseline/behaviour-snapshot.md, docs/08-observability/log-schema.md, docs/09-ai-guardrails/model-provenance-design.md, docs/13-security-validation/remediation-backlog.md. Stage S07 fills approval_id and final action. Stage S09 uses the compliance mapping as the pack's index. Stage S10 answers defence question 5 from the route output. Stage S05R folds the "Open question for S03:" lines into the YAML.

## Required final response (after each half)
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
| `audit-gap-report.md` | Header. Eight provenance questions, each answered yes/no for the old row. The 96 old lines with no correlation_id. |
| `decision-provenance-model.md` | Header. Grouped fields with log field and YAML id. The field that answers "trace id". "Cannot be proven" list with log integrity. |
| `evidence-chain-one-case.md` | Header. Ordered rows for one correlation_id from three calls (read, summary, denied). Missing items marked. |
| `compliance-evidence-mapping.md` | Header. Control area to stored evidence to location, with test names. |
| `before-and-after-audit-example.md` | Header. Two rows, full, redacted. The after row has 15 keys. |
| `audit-read-access-design.md` | Header. One proposed matrix row (role, purpose, decision) and the open question for S03. |
| `audit_query.py`, route | Read only. Policy checked before the lookup. Own audit row. |
| Policy row | Same row in the Python copy, the Rego copy, policy_data.json, the fixtures. Agreement tests pass. |
| `test_audit_rebuild.py` | Every test marked security. No test skipped. All pass. |
| `evidence.md` | Header. Route output for the case. Test counts. |

## Done test

`GET /audit/<id>` for the case returns the ordered rows and a `cannot_prove` list that includes `approval_id` and log integrity. The route's own row carries the id of the request that made it, unless the caller sends the same id in `X-Correlation-Id`. In that case the call appears as the last row on the next query.
