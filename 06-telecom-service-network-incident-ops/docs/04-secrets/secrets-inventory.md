# Secrets inventory

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every inventory row names a file, a line, a kind, and whether code reads the value. Real-looking values stay in the committed files. Half B removes them. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Evidence sources | `legacy/reconcile_legacy.py`; `.env.example`; `infra/terraform/main.tf`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/main.py`; `semantic-layer/ai-context-policy.yaml`; `semantic-layer/entities.yaml`; `docs/02-baseline/defect-list.md`; `docs/03-identity/current-role-matrix.md`; `docs/00-contract/operating-contract.md`; `Project_Intent Section 4.3.md` |
| Assumptions | Likelihood stays Unknown. The repo states no frequency. A name listed under `forbidden_credential_names` is a secret name even when no running function reads it. |
| Unresolved issues | Whether `automation_service` is the user `app_shared` is Unknown. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Residual risks | Anyone with the repo can read the password and the example key. Those values are already in git history. A later placeholder in the working files leaves the older copies in history. |

## What this file is

This file lists every secret-like value in the scoped files, the kind of secret, and whether running code reads it. A secret-like value is a password, an API key, a token, or a shared account name.

Half A writes this document. The program files stay as they are.

Every secret value in this file is written `<redacted>`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Inventory

| id | file | line | kind | code reads it | value |
|---|---|---|---|---|---|
| SI-01 | `legacy/reconcile_legacy.py` | 6 | password | The name `SHARED_DB_PASSWORD` is assigned. The function `reconcile` does not use the name. | `<redacted>` |
| SI-02 | `legacy/reconcile_legacy.py` | 5 | shared account | The name `SHARED_DB_USER` is assigned the user `app_shared`. The function `reconcile` does not use the name. | `app_shared` |
| SI-03 | `.env.example` | 1 | password | A search of the Python files finds no read of `DATABASE_URL`. The URL holds user `app_shared` and the same password as SI-01. | `<redacted>` |
| SI-04 | `.env.example` | 2 | API key | `ai_gateway.py` line 1 imports `os`. The function `summarize_record` never calls `os`. A search of the Python files finds no read of `AI_GATEWAY_KEY`. | `<redacted>` |
| SI-05 | `.env.example` | 3 | password | A search of the Python files finds no read of `LEGACY_BATCH_PASSWORD`. | `<redacted>` |
| SI-06 | `.env.example` | 4 | token (shared) | A search of the Python files finds no read of `OT_VENDOR_TOKEN`. The token does not select `persona.vendor_account`. | `<redacted>` |
| SI-07 | `infra/terraform/main.tf` | 4 | shared account | Terraform writes `shared_user=app_shared` into `generated-env.txt`. That generated file is absent from the repo tree. | `app_shared` |
| SI-08 | `apps/` | n/a | none found | A search of `apps/` for a password, a key, or a token constant found none. | n/a |

Worked example for SI-01. The file assigns `SHARED_DB_PASSWORD` on line 6. The next function opens `data/synthetic/devices.csv` and counts the rows. It never opens a database. The password sits in the source file and is unused by that count.

`.env.example` line 5 holds `LOG_LEVEL=DEBUG`. That line is a log setting. It is not a secret. It is left out of the table.

The prompt string in `ai_gateway.py` line 4 is a sentence template. It is not a secret.

`semantic-layer/ai-context-policy.yaml` `policy.prompt_fields` `forbidden_credential_names` lists the six names `SHARED_DB_PASSWORD`, `SHARED_DB_USER`, `DATABASE_URL`, `AI_GATEWAY_KEY`, `LEGACY_BATCH_PASSWORD`, and `OT_VENDOR_TOKEN`. The list holds names only.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| SI-01 | The legacy script assigns a shared database password in the source file. | Verified Fact. `legacy/reconcile_legacy.py` line 6. F05. CR-06. `rule.shared_admin_not_least_privilege`. Operating contract row 4. Value `<redacted>`. | Anyone with the repo can read the password. | The same password text is also in `.env.example` line 1. | High | Operating contract row 4 names Half B as the move to the environment. |
| SI-02 | The legacy script assigns the shared user `app_shared`. | Verified Fact. `legacy/reconcile_legacy.py` line 5. CR-06. The user name is a name, not a password. | A reader of the file learns the shared user. | The user and the persona `automation_service` may be one account or two. | High for the assignment. Medium for any link to the persona. | Whether `automation_service` is `app_shared` is Unknown. |
| SI-03 | The example settings file holds a database URL that embeds the same shared password. | Verified Fact. `.env.example` line 1. F05. `forbidden_credential_names`. Value `<redacted>`. | The password is readable in a second committed file. | A later copy of this file can spread the same password. | High | None for the file and line. |
| SI-04 | The example settings file holds an AI key that looks like a live key. | Verified Fact. `.env.example` line 2. `Project_Intent Section 4.3.md` row "Example AI key". `docs/01-discovery/ai-subsystem-discovery.md` line 30. Value `<redacted>`. | Anyone with the repo can read the sample key. | A later reader can treat the sample as a live key. The live gateway never reads it. | High | None for the unread name. |
| SI-05 | The example settings file holds a batch password. | Verified Fact. `.env.example` line 3. `forbidden_credential_names`. Value `<redacted>`. | The name sits in a committed file. | A later reader can treat it as a live batch login. No function reads it. | High | Which batch job the name was meant for is Unknown. |
| SI-06 | The example settings file holds a shared vendor token. | Verified Fact. `.env.example` line 4. CR-07. `forbidden_credential_names`. Value `<redacted>`. | The token is a shared secret in an example file. It grants no API role. | A later reader can treat the token as the vendor login. The live vendor check is the header word. | High | Which supplier login the token was meant to be is Unknown. |
| SI-07 | Terraform writes the shared user name into `generated-env.txt`. | Verified Fact. `infra/terraform/main.tf` line 4. The content string is `shared_user=app_shared`. The generated file is absent from the repo tree (`docs/01-discovery/data-and-integration-map.md`). | Applying the file would write the user name to disk. | The Terraform file holds no password. A later edit that adds one would write a secret to `generated-env.txt`. | High for the user name. Unknown for whether the declaration was ever applied. | Whether that declaration was ever applied is Unknown. |
| SI-08 | `apps/` holds no password, key, or token constant. | Verified Fact. This stage's search of `apps/` for `password`, `sk-`, `token`, `API_KEY`, and `SECRET` in Python files. `ai_gateway.py` line 4 holds a prompt template. | The live routes do not load a secret from a constant. | The summary still places the whole device row in the prompt string. That case is F12. | High | None for a missing key in `apps/`. |

## What reaches logs and prompts today

`GET /records/{record_id}` returns the whole device row. **Verified Fact.** `apps/api/main.py` line 16. `domain_service.py` returns the row. F10. The body includes `mgmt_ip` and `credential_profile`.

`POST /ai/summarize/{record_id}` builds a prompt from the whole device row. **Verified Fact.** `apps/api/services/ai_gateway.py` line 7. F12. The prompt text includes `mgmt_ip` and `credential_profile`.

A successful record read writes `record_id` and `role` to `logs/audit.log`. A successful summary writes `record_id` and `model`. **Verified Fact.** `apps/api/main.py` lines 15 and 23. `apps/api/services/audit.py` line 9. Those two lines leave out the device row and every secret name in the table above.

## Lifecycle

This file cites `docs/02-baseline/defect-list.md` F05, F10, and F12, `docs/03-identity/current-role-matrix.md` CR-06 and CR-07, and `semantic-layer/ai-context-policy.yaml` `policy.prompt_fields`. Stage S04-04 Half B moves the password and replaces the example values. Stage S04-07 adds the pattern test to CI. Stage S04-09 uses the sensitive-field checklist for the prompt allow-list. Stage S05-13 collects the test into the security suite.
