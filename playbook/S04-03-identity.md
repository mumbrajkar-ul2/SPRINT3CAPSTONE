# S04-03 — Identity and least privilege (Challenge 3)

Phase 4 in `Execution Plan.md`. Two halves. Half A is analysis and design. Half B is code and tests. Half B starts only after you reply "Half A accepted" in the same chat.

## Inputs

- `Project_Intent.md` (section 4.3)
- `06-telecom-service-network-incident-ops/semantic-layer/access-semantics.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/business-rules.yaml`
- `06-telecom-service-network-incident-ops/apps/api/main.py`
- `06-telecom-service-network-incident-ops/policy/opa/access.rego`
- `06-telecom-service-network-incident-ops/docs/01-discovery/brownfield-risk-register.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/tests/characterization/test_current_behaviour.py`

## Prompt

```text
# Stage S04-03 — Identity and least privilege (Challenge 3)

## Objective
Half A: design least-privilege access for the API using the personas and ids in `semantic-layer/access-semantics.yaml`. Half B: prove it with negative tests and remove the `clinician` role from `apps/api/main.py`.

## Scope
Include: API role header handling in `main.py`; OPA roles in `access.rego`; the seven personas; `app_shared`; the vendor token; `ai_agent`; `automation_service`.
Exclude in Half A: any code change. Exclude in Half B: any change beyond removing `clinician`, adding tests under `tests/access/`, and updating the one characterization test that locked `clinician`. Policy engine changes belong to S04-06.

## Required analysis (Half A)
1. Current role matrix: every role and account that can reach the API or the data, what it can do today, and the file that proves it.
2. Target access matrix: persona by resource by action by purpose by risk, copied from `access-semantics.yaml` ids. No new persona.
3. Policy input model: role, resource, purpose, scope, risk. Write it as the JSON input shape OPA will receive. Name the YAML id for each value set.
4. Negative access test plan: at least these cases. noc_operator may read a record. clinician is denied. ai_agent may recommend and may not execute. automation_service may not execute without an approval id. A request with no role header is denied or gets the lowest role, and the choice is stated.
5. Privilege reduction backlog: remove clinician; split app_shared into named accounts; scope automation_service; remove the default role header; each with owner and effort Unknown if not stated.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response for Half A. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Write `tests/access/test_negative_access.py` with the cases from the test plan. Each test names role, resource, purpose, scope, and risk in its docstring or parameters.
2. Remove `clinician` from the allowed roles in `main.py`. Make no other change to `main.py`.
3. Replace the characterization test that locked `clinician` with a test that asserts it is denied. Note the swap in the test docstring.
4. Run `pytest -q`. Record before and after in `docs/03-identity/evidence.md`.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line or symbol, a YAML id, or a test name.
- Before-and-after test output is REAL. Say so.

## Constraints and guardrails
- Plain speech.
- Use YAML ids from access-semantics.yaml. Do not invent a persona or a resource name. If one is missing, write it as an open question for S03, not in this design.
- Redact secrets.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Constant | Value |
|---|---|
| API roles today | admin, operator, clinician, engineer, ai_agent (main.py) |
| Default when header absent | operator (main.py) |
| OPA rules today | any admin; operator + read (access.rego) |
| Personas | noc_operator, network_engineer, field_engineer, customer_support, automation_service, vendor_account, ai_agent |
| Shared account | app_shared (legacy script, .env.example, Terraform) |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/03-identity/`:
1. `current-role-matrix.md`
2. `target-access-matrix.md`
3. `policy-input-model.md` (with the JSON shape)
4. `negative-access-test-plan.md`
5. `privilege-reduction-backlog.md`
Half B:
6. `06-telecom-service-network-incident-ops/tests/access/test_negative_access.py`
7. `06-telecom-service-network-incident-ops/docs/03-identity/evidence.md` (before and after pytest output, diff summary of main.py)

## Completion gate
Half A PASS when all five documents exist and every allow decision in the target matrix names role, resource, purpose, scope, and risk with a YAML id. Half B PASS when the negative tests pass, clinician is denied, and no other behaviour changed. CONDITIONAL PASS when the no-header case is left as the current default with a PROPOSED change and owner. BLOCKED when any test case cannot name all five input fields.

## Lifecycle linkage
Cite docs/01-discovery/brownfield-risk-register.md, docs/02-baseline/defect-list.md, docs/02-baseline/ai-qualification.md, and semantic-layer ids. Stage S04-06 consumes the policy input model. Stage S05-13 collects the negative tests into the security suite. Stage S06 cites the target matrix.

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
| `current-role-matrix.md` | Header. Every role and account with current rights and evidence. |
| `target-access-matrix.md` | Header. Persona × resource × action × purpose × risk. YAML id per cell set. |
| `policy-input-model.md` | Header. JSON input shape. Id per value set. |
| `negative-access-test-plan.md` | Header. At least five cases with the five input fields each. |
| `privilege-reduction-backlog.md` | Header. Four items with owner. |
| `tests/access/test_negative_access.py` | Passing tests. Five fields named per test. |
| `evidence.md` | Header. Before and after pytest output. The one-line change in main.py. |

## Done test

`clinician` with `GET /records/REC-0001` returns 403. `noc_operator` (or the mapped API role) returns 200. Half A files have no code.
