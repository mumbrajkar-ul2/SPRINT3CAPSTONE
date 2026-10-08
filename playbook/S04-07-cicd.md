# S04-07 — CI/CD and supply chain (Challenge 7)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `06-telecom-service-network-incident-ops/.github/workflows/ci.yml`
- `06-telecom-service-network-incident-ops/supply-chain/dependency-risk-register.md`
- `06-telecom-service-network-incident-ops/requirements.txt`
- `06-telecom-service-network-incident-ops/apps/web/package.json`
- `06-telecom-service-network-incident-ops/Makefile`
- `06-telecom-service-network-incident-ops/scripts/` (bootstrap from S04-05)
- `06-telecom-service-network-incident-ops/tests/security/test_secret_patterns.py`
- `06-telecom-service-network-incident-ops/policy/tests/`
- `06-telecom-service-network-incident-ops/semantic-layer/tests/`

## Prompt

```text
# Stage S04-07 — CI/CD and supply chain (Challenge 7)

## Objective
Half A: plan a pipeline that checks the code, scans dependencies, produces an SBOM, and saves evidence of what it checked. Half B: change `.github/workflows/ci.yml` and the Makefile so the pipeline does that and writes files into `evidence/`.

## Scope
Include: the CI workflow; dependency pins; the three-row risk register; SBOM; scans; the evidence folder.
Exclude in Half A: any code change. Exclude in Half B: deployment steps to any environment; signing infrastructure beyond a PROPOSED note.

## Required analysis (Half A)
1. Pipeline improvement plan: current stages (install, pytest) versus target stages (install, lint, unit and characterization tests, semantic-layer tests, policy tests, security tests, SBOM, dependency scan, static scan, evidence upload). Per stage: tool, command, what it proves, what file it writes.
2. Dependency risk register: extend the three rows. Add every pinned package, its version, whether a lockfile exists, and the risk if it changes.
3. SBOM recommendation: CycloneDX via `cyclonedx-py` (or `pip-audit --format cyclonedx-json`). Output path. How often.
4. Security scan plan: `pip-audit`, `bandit -r apps etl legacy`, the secret-pattern test, policy tests, semantic-layer tests. What each catches and what it misses.
5. Release evidence checklist: the list of files a release must carry, with the path each will have under `evidence/`.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Rewrite `.github/workflows/ci.yml` with the target stages. Each stage writes its output into `evidence/` (test report as JUnit XML, SBOM JSON, pip-audit JSON, bandit JSON, secret-pattern result, policy test result, semantic-layer test result). Upload `evidence/` as a workflow artifact.
2. Add a `make evidence` target (and a PowerShell equivalent in `scripts/`) that runs the same stages locally and writes the same files.
3. Add the scan tools to a `requirements-dev.txt`. Pin them.
4. Run `make evidence` (or the script) locally. Commit the generated files under `evidence/` with a `README.md` that says which run produced them and the honesty label REAL.
5. Record the run in `docs/07-cicd/evidence.md`.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path or a command output.
- Scan output is REAL. If a tool could not run, write Unknown with the reason.

## Constraints and guardrails
- Plain speech.
- Do not disable a failing scan to make the pipeline green. Record the finding in the remediation backlog with an owner.
- Redact secrets in any pasted output.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| CI today | install deps, pytest -q (Python 3.11) |
| Risk register today | three rows: FastAPI no SBOM; legacy no provenance; frontend no lockfile discipline |
| Web package | Playwright only, no Angular runtime deps |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/07-cicd/`:
1. `pipeline-improvement-plan.md`
2. `dependency-risk-register.md` (extended; also update `supply-chain/dependency-risk-register.md` to point here)
3. `sbom-recommendation.md`
4. `security-scan-plan.md`
5. `release-evidence-checklist.md`
Half B:
6. `.github/workflows/ci.yml`, Makefile `evidence` target, `scripts/evidence.ps1`, `requirements-dev.txt`
7. `evidence/` with generated files and `evidence/README.md`
8. `docs/07-cicd/evidence.md`

## Completion gate
Half A PASS when every target stage names a tool, a command, and an output file, and the checklist lists every evidence file with its path. Half B PASS when `make evidence` wrote every file in the checklist and the checklist points at them. CONDITIONAL PASS when one tool could not run on this machine and the reason is recorded. BLOCKED when the pipeline writes no evidence file.

## Lifecycle linkage
Cite docs/05-iac/ for bootstrap and docs/04-secrets/ for the pattern test. Stage S05-13 adds `pytest -m security` as a stage here. Stage S09 copies `evidence/` into the pack.

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
| `pipeline-improvement-plan.md` | Header. Current vs target stages. Tool, command, proof, output per stage. |
| `dependency-risk-register.md` | Header. Every pinned package. Lockfile column. |
| `sbom-recommendation.md` | Header. Tool, format, path, cadence. |
| `security-scan-plan.md` | Header. Five scans. Catches and misses. |
| `release-evidence-checklist.md` | Header. File list with paths under `evidence/`. |
| `ci.yml`, Makefile, scripts | Run. |
| `evidence/` | Generated files plus README with the run id and REAL label. |
| `evidence.md` | Header. Local run output. |

## Done test

Open `release-evidence-checklist.md`. Every path it lists exists under `evidence/` after `make evidence`.
