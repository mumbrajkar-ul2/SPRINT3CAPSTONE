# S05-13 — Automated security validation (Challenge 13)

Phase 5 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted". This stage collects the security tests written in Phase 4 into one suite that CI runs.

## Inputs

- `06-telecom-service-network-incident-ops/tests/access/`
- `06-telecom-service-network-incident-ops/tests/security/`
- `06-telecom-service-network-incident-ops/tests/ai/`
- `06-telecom-service-network-incident-ops/policy/tests/`
- `06-telecom-service-network-incident-ops/docs/07-cicd/security-scan-plan.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/guardrail-test-pack.md`
- `06-telecom-service-network-incident-ops/docs/03-identity/negative-access-test-plan.md`
- `06-telecom-service-network-incident-ops/security/threat-model.md`
- `06-telecom-service-network-incident-ops/.github/workflows/ci.yml`
- `06-telecom-service-network-incident-ops/pyproject.toml`

## Prompt

```text
# Stage S05-13 — Automated security validation (Challenge 13)

## Objective
Half A: plan one security test suite that covers unauthorized access, policy bypass, prompt injection, sensitive data in logs and prompts, insecure defaults, and unsafe AI action, and list the abuse cases with evidence. Half B: make `pytest -m security` run that suite locally and in CI.

## Scope
Include: every test marked security from S04-03, S04-04, S04-06, S04-09; the scan plan from S04-07; the threat-model starter.
Exclude in Half A: any code change. Exclude in Half B: new controls not designed in Phase 4. If a gap needs a new control, write it in the remediation backlog.

## Required analysis (Half A)
1. Security test suite plan: one table. Per row: abuse case, the test that covers it (file and name), the control it proves, the YAML rule id, and whether it exists. Rows for at least: unauthorized role reads a record; removed role (clinician) reads a record; request with no role header; AI route without recommend permission; EXECUTE without approval_id; prompt injection via hostname; mgmt_ip in a prompt; secret pattern in a committed file; insecure default (the old default role header); unsafe AI action (output with an execute verb); audit row missing correlation_id.
2. Negative tests: for every row with "exists: no", write the test design (input, expected status, expected audit row).
3. Scanning checklist: the five scans from S04-07 with what each ran against and where the output lands.
4. Abuse-case evidence: for each abuse case that already has a test, paste the passing test name and the assertion that proves the control.
5. Remediation backlog: every gap found, with owner and the stage that should fix it.
6. Extend security/threat-model.md with a STRIDE table per trust boundary from the S04-09 diagram. Mark each threat as covered by test, covered by scan, or open.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Register the security marker in pyproject.toml. Make sure every test in the plan carries @pytest.mark.security.
2. Write the missing negative tests from Half A under tests/security/.
3. Add a CI stage that runs pytest -m security --junitxml=evidence/security-tests.xml and a make security target.
4. Run it. Record in docs/13-security-validation/evidence.md.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a test file and test name, or a scan output file.
- Test output is REAL.

## Constraints and guardrails
- Plain speech.
- Do not skip or xfail a security test to make the suite green. Record the failure in the backlog.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| Tests marked security so far | from S04-04 (secret patterns), S04-09 (guardrails); S04-03 and S04-06 tests exist and may need the marker |
| Scans planned (S04-07) | pip-audit, bandit, secret-pattern test, policy tests, semantic-layer tests |
| Threat model today | starter only; asks for STRIDE/MAESTRO |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/13-security-validation/`:
1. `security-test-suite-plan.md`
2. `negative-tests.md`
3. `scanning-checklist.md`
4. `abuse-case-evidence.md`
5. `remediation-backlog.md`
6. extended `security/threat-model.md`
Half B:
7. pyproject.toml marker, new tests under tests/security/, CI stage, make target
8. `docs/13-security-validation/evidence.md`

## Completion gate
Half A PASS when every abuse case has a test or a test design, and every threat in the STRIDE table has a status. Half B PASS when pytest -m security passes locally, the CI stage exists, and every security claim planned for the evidence pack names a test in this suite. CONDITIONAL PASS when a backlog item is open with an owner. BLOCKED when any security test is skipped or xfailed.

## Lifecycle linkage
Cite tests from S04-03, S04-04, S04-06, S04-09 and docs/07-cicd/security-scan-plan.md. Stage S09 copies evidence/security-tests.xml into the pack and cites this suite for every security claim.

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
| `security-test-suite-plan.md` | Header. At least eleven abuse cases with test, control, rule id, exists. |
| `negative-tests.md` | Header. Design per missing test. |
| `scanning-checklist.md` | Header. Five scans with target and output path. |
| `abuse-case-evidence.md` | Header. Test name and assertion per case. |
| `remediation-backlog.md` | Header. Gaps with owner and stage. |
| `threat-model.md` | STRIDE table per boundary with status. |
| CI stage, make target | `pytest -m security` runs. |
| `evidence.md` | Header. Suite output. |

## Done test

`pytest -m security -q` passes. `evidence/security-tests.xml` exists after `make security`. No test in the run is skipped.
