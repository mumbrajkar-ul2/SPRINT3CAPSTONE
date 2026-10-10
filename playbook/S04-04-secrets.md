# S04-04 — Secrets and encryption (Challenge 4)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted".

## Inputs

- `Project_Intent.md` (section 4.3)
- `06-telecom-service-network-incident-ops/.env.example`
- `06-telecom-service-network-incident-ops/legacy/reconcile_legacy.py`
- `06-telecom-service-network-incident-ops/infra/terraform/main.tf`
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py`
- `06-telecom-service-network-incident-ops/apps/api/services/audit.py`
- `06-telecom-service-network-incident-ops/semantic-layer/ai-context-policy.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/entities.yaml`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`

## Prompt

```text
# Stage S04-04 — Secrets and encryption (Challenge 4)

## Objective
Half A: inventory every secret and sensitive field in the repo and design how configuration is loaded without a real secret in any committed file. Half B: add a secret-pattern test that runs in CI and a settings loader that replaces the constants.

## Scope
Include: `.env.example`; `legacy/reconcile_legacy.py`; `infra/terraform/main.tf`; any hardcoded key in `apps/`; sensitive fields named in `entities.yaml` and `ai-context-policy.yaml` (`mgmt_ip`, `credential_profile`, `customer_id`); what reaches logs and prompts.
Exclude in Half A: any code change. Exclude in Half B: changes to the AI prompt itself (S04-09) and to the audit schema (S04-08).

## Required analysis (Half A)
1. Secrets inventory: every secret-like value, its file and line, its kind (password, API key, token, shared account), and whether code reads it. Write <redacted> for the value.
2. Remediation plan: per item, the action (remove, move to environment, rotate, replace with placeholder), owner, and evidence that will prove it.
3. Cleaned configuration model: `.env.example` holds placeholders only; a settings loader reads the environment; no real default for any secret; the app fails clearly when a required value is absent.
4. Sensitive-field handling checklist: for `mgmt_ip`, `credential_profile`, `customer_id`, and any field marked sensitive in entities.yaml: may it be logged, may it enter a prompt, may it appear in an API response, and who may see it. Cite the ai-context-policy.yaml id.
5. Rotation evidence plan: what a rotation record would contain and where it would be stored. Unknown where the repo is silent.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. `tests/security/test_secret_patterns.py`: scans the repo (excluding `.git`, venv, `docs/`) for the known strings and common patterns (password=, sk-, token=). Fails when one is found in committed code or `.env.example`. Mark the test with `@pytest.mark.security`.
2. `apps/api/settings.py`: loads values from the environment; raises a clear error when a required value is absent; no secret default.
3. Replace the password constant in `legacy/reconcile_legacy.py` with a read from the environment. Replace real-looking values in `.env.example` with placeholders like `CHANGE_ME`.
4. Run the pattern test and `pytest -q`. Record before and after in `docs/04-secrets/evidence.md`.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line.
- Never write a secret value into any artifact. Write <redacted>.

## Constraints and guardrails
- Plain speech.
- Do not add a secrets manager or cloud service. Name one as PROPOSED with an owner if the design needs it.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Where |
|---|---|
| Shared DB user app_shared with a password constant | legacy/reconcile_legacy.py, .env.example |
| Example AI key (a sample value that looks real) | .env.example |
| Shared vendor token | .env.example |
| shared_user=app_shared written to generated-env.txt | infra/terraform/main.tf |
| Fields never in a prompt | mgmt_ip, credential_profile (ai-context-policy.yaml) |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/04-secrets/`:
1. `secrets-inventory.md`
2. `remediation-plan.md`
3. `cleaned-configuration-model.md`
4. `sensitive-field-handling-checklist.md`
5. `rotation-evidence-plan.md`
Half B:
6. `06-telecom-service-network-incident-ops/tests/security/test_secret_patterns.py`
7. `06-telecom-service-network-incident-ops/apps/api/settings.py`
8. edits to `legacy/reconcile_legacy.py` and `.env.example`
9. `06-telecom-service-network-incident-ops/docs/04-secrets/evidence.md`

## Completion gate
Half A PASS when every inventory row has a file, a kind, a remediation action, and an owner, and the checklist covers every sensitive field. Half B PASS when the pattern test passes on the cleaned repo and fails when a known string is re-added (show both runs), and no sensitive value is needed in committed code or `.env.example`. CONDITIONAL PASS when rotation evidence is Unknown with an owner. BLOCKED when any real-looking value remains in a committed file.

## Lifecycle linkage
Cite docs/02-baseline/defect-list.md and ai-context-policy.yaml ids. Stage S04-07 adds the pattern test to CI. Stage S04-09 uses the sensitive-field checklist for the prompt allow-list. Stage S05-13 collects the test into the security suite.

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
| `secrets-inventory.md` | Header. Every item, file, line, kind, read-by-code, value `<redacted>`. |
| `remediation-plan.md` | Header. Action and owner per item. |
| `cleaned-configuration-model.md` | Header. Loader design. Fail-clear rule. Placeholder rule. |
| `sensitive-field-handling-checklist.md` | Header. Per field: log, prompt, response, viewer. YAML id. |
| `rotation-evidence-plan.md` | Header. Record fields. Storage. Unknown rows. |
| `test_secret_patterns.py` | Passes on clean repo. Fails when a known string is added. Marked `security`. |
| `settings.py` | Environment reads. Clear error on missing value. No secret default. |
| `evidence.md` | Header. Two runs of the pattern test. pytest before and after. |

## Done test

Grep the repo for the password constant and the sample key. No hits outside `docs/` evidence files that say `<redacted>`.
