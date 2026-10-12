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
- `.github/workflows/ci.yml` (at the repo root `SPRINT3CAPSTONE/`. S04-07 Half B moved it there.)
- `06-telecom-service-network-incident-ops/pyproject.toml`
- `06-telecom-service-network-incident-ops/Makefile`
- `06-telecom-service-network-incident-ops/scripts/evidence.sh` and `evidence.ps1`
- `06-telecom-service-network-incident-ops/tests/ci/test_evidence_contract.py` (it checks the evidence file names)
- `06-telecom-service-network-incident-ops/tests/observability/test_audit_schema.py`
- `06-telecom-service-network-incident-ops/evidence/` (the scan outputs: `bandit.json`, `pip-audit.json`, `ruff.json`, `junit-security.xml`)
- `06-telecom-service-network-incident-ops/docs/07-cicd/evidence.md` and `release-evidence-checklist.md`
- `06-telecom-service-network-incident-ops/docs/09-ai-guardrails/trust-boundary-diagram.md`, `ai-risk-register.md`, and `unsafe-output-handling-rules.md`
- `06-telecom-service-network-incident-ops/docs/08-observability/log-schema.md`
- `06-telecom-service-network-incident-ops/docs/06-policy/ai-action-policy-design.md` and `evidence.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
- `06-telecom-service-network-incident-ops/semantic-layer/business-rules.yaml`, `access-semantics.yaml`, and `ai-context-policy.yaml`
- `06-telecom-service-network-incident-ops/PRODUCTION_EVIDENCE_PACK_TEMPLATE.md` (section "Automated Security Validation Evidence")

## Prompt

```text
# Stage S05-13 — Automated security validation (Challenge 13)

## Objective
Half A: plan one security test suite that covers unauthorized access, policy bypass, prompt injection, sensitive data in logs and prompts, insecure defaults, and unsafe AI action, and list the abuse cases with evidence. Half B: make `pytest -m security` run that suite locally and in CI, with no skipped test.

## Scope
Include: every test marked security from S04-03, S04-04, S04-06, S04-09; the scan plan from S04-07; the threat-model starter.
Exclude in Half A: any code change. Exclude in Half B: new controls not designed in Phase 4. If a gap needs a new control, write it in the remediation backlog.

## Required analysis (Half A)
1. Security test suite plan: one table. Per row: abuse case, the test that covers it (file and name), the control it proves, the YAML rule id, and whether it exists. Rows for at least: unauthorized role reads a record; removed role (clinician) reads a record; request with no role header; AI route without recommend permission; EXECUTE without approval_id; prompt injection via hostname; mgmt_ip in a prompt; secret pattern in a committed file; insecure default (the old default role header); unsafe AI action (output with an execute verb); audit row missing correlation_id; a caller sends `approval_required` as false (finding `AA-01` in `docs/06-policy/ai-action-policy-design.md`); `mgmt_ip`, `credential_profile`, or a password written into `logs/audit.log`; the Python copy and the Rego copy of the policy give different answers (the two tests that need the `opa` program).
   The "exists" column has three values: yes, no, or backlog. Use backlog when the repo has no control to prove. Two rows are backlog today. A call with no role header still maps to `operator` (owner decision in S04-03, test `test_missing_role_header_keeps_operator_default`). So "request with no role header" and "insecure default" cannot show a deny. Write each as a backlog item with an owner.
2. Negative tests: for every row with "exists: no", write the test design (input, expected status, expected audit row).
3. Scanning checklist: the five scans from S04-07 with what each ran against and where the output lands. Record what each scan returned on its last run. Three of them exit 1 on real findings today: ruff 12 (backlog `BL-10`), pip-audit 9 advisories (`BL-11`), bandit 2 LOW (`BL-12`). Keep those backlog rows. A failing scan with an owner and a backlog row gives CONDITIONAL PASS. A scan that is switched off gives BLOCKED.
4. Abuse-case evidence: for each abuse case that already has a test, paste the passing test name and the assertion that proves the control.
5. Remediation backlog: every gap found, with owner and the stage that should fix it.
6. Extend security/threat-model.md with a STRIDE table per trust boundary `B1` to `B9` from `docs/09-ai-guardrails/trust-boundary-diagram.md`. Mark each threat as covered by test, covered by scan, or open. The file also names MAESTRO. Its letters are Unknown in this repo, so do not expand them. Write "Open question for S03:" for the MAESTRO letters.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. The `security` marker is already registered in pyproject.toml. Update its description so it names every area the suite covers. Make sure every test in the plan carries @pytest.mark.security. Today `tests/access/` (6 tests) and `policy/tests/` (37 tests) have no mark.
2. Write the missing negative tests from Half A under tests/security/.
3. Make `opa` available so the two policy agreement tests run and none skip. Decision by Mangesh (FDE), 2026-10-11: choice 1.
   - The tests skip when `shutil.which("opa")` finds nothing. The `opa` command must be on the PATH of the pytest process. Install the binary, or put a small `opa` command on the PATH that calls the Docker image used in S04-06 (OPA 1.21.1). A Docker command run by hand does not satisfy the test.
   - Add a step to the CI workflow that installs `opa` at a pinned version before the security stage.
   - Record the `opa` version and how it was installed in `docs/13-security-validation/evidence.md`.
4. Stage 6 of the CI workflow already runs `pytest -m security` through `scripts/evidence.sh security` and writes `evidence/junit-security.xml`. Keep that file name. `tests/ci/test_evidence_contract.py` and the S04-07 documents use it, and S09 copies it. Do not add a second stage or a second file. Add a `make security` target that runs the same command. Marking more tests moves them out of the `tests` stage, which runs `-m "not security"`. Update the counts in `docs/07-cicd/evidence.md` and the contract test if they change.
5. Run it. Record in docs/13-security-validation/evidence.md.

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
| Tests marked security so far | from S04-04 (secret patterns), S04-09 (guardrails); S04-03 and S04-06 tests exist and need the marker. At the end of S04-09, `pytest -m security` gave 52 passed. |
| Marker and CI stage today | The `security` marker exists in pyproject.toml. CI stage 6 runs it and writes `evidence/junit-security.xml`. The Makefile has no `security` target. |
| `opa` program | Absent on this machine. Two tests in `policy/tests/test_policy_python.py` skip because of it. Decision (2026-10-11): make `opa` available locally and in CI so they run. |
| Scans planned (S04-07) | pip-audit, bandit, secret-pattern test, policy tests, semantic-layer tests |
| Scan results on the last run | ruff 12, pip-audit 9 advisories, bandit 2 LOW. Each has a backlog row (`BL-10` to `BL-12`). |
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
Half A PASS when every abuse case has a test or a test design, and every threat in the STRIDE table has a status. Half B PASS when pytest -m security passes locally, the CI stage exists and installs `opa`, and every security claim planned for the evidence pack names a test in this suite. CONDITIONAL PASS when a backlog item is open with an owner, including a scan that finds a real issue. BLOCKED when any security test is skipped or xfailed, or a scan is switched off.

## Lifecycle linkage
Cite tests from S04-03, S04-04, S04-06, S04-09 and docs/07-cicd/security-scan-plan.md. Stage S09 copies evidence/junit-security.xml into the pack and cites this suite for every security claim.

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
| `security-test-suite-plan.md` | Header. At least fifteen abuse cases with test, control, rule id, exists (yes, no, or backlog). |
| `negative-tests.md` | Header. Design per missing test. |
| `scanning-checklist.md` | Header. Five scans with target and output path. |
| `abuse-case-evidence.md` | Header. Test name and assertion per case. |
| `remediation-backlog.md` | Header. Gaps with owner and stage. |
| `threat-model.md` | STRIDE table per boundary with status. |
| CI stage, make target | `pytest -m security` runs. CI installs `opa` first. `make security` runs the same command. |
| `evidence.md` | Header. Suite output. The `opa` version and install method. |

## Done test

`pytest -m security -q` passes. `evidence/junit-security.xml` exists after `make security`. No test in the run is skipped, including the two that need `opa`. The `opa` command is on the PATH.
