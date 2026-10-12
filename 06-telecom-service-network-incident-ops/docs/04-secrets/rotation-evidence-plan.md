# Rotation evidence plan

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The record fields are named. Where the record is stored is Unknown. Owner: Team-Force. |
| Evidence sources | `docs/04-secrets/secrets-inventory.md`; `docs/04-secrets/remediation-plan.md`; `legacy/reconcile_legacy.py`; `.env.example`; `semantic-layer/business-rules.yaml`; `semantic-layer/ai-context-policy.yaml`; `docs/00-contract/operating-contract.md`; `docs/03-identity/current-role-matrix.md` |
| Assumptions | A rotation record proves a change of secret. It names the variable and the person. It holds no secret value. |
| Unresolved issues | Where a rotation record is stored is Unknown. Owner: Team-Force. Whether `automation_service` is the user `app_shared` is Unknown. |
| Residual risks | The password and the example key are already in git history. A later placeholder in the working files leaves the older copies in history. A rotation record that is never stored cannot prove the change. |

## What this file is

This file says what a rotation record would contain after a secret is changed, and where that record would be stored.

Rotate means change the secret to a new value so the old text no longer works as a login.

Half A writes this plan. No rotation record is written in this half.

Every secret value in this file is written `<redacted>`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## What a rotation record would contain

| Field | What it holds |
|---|---|
| Variable name | The name that was changed. One of `SHARED_DB_PASSWORD`, `DATABASE_URL`, `AI_GATEWAY_KEY`, `LEGACY_BATCH_PASSWORD`, or `OT_VENDOR_TOKEN`. |
| Date | The day the new value was put into the environment. |
| Person | The named person who changed it. |
| Proof the old text is gone | A note that the pattern test passed on the working files, or a path to that test run. The note holds no secret value. |

The record holds the old value as `<redacted>`. It holds the new value as `<redacted>`.

## Where the record would be stored

Unknown. A search of the repo finds no file, table, or log that stores a rotation record. `logs/audit.log` stores `ts`, `action`, and `details` for a record read and a summary. **Verified Fact.** `apps/api/services/audit.py` line 9. Those actions are `record.read` and `ai.summary`. **Verified Fact.** `apps/api/main.py` lines 15 and 23.

Owner of this gap: Team-Force.

Open question for S03: the YAML has no store for a rotation record, and this plan needs a named place for that record.

## Rows that stay Unknown

| Topic | What is known | What stays Unknown | Owner |
|---|---|---|---|
| Storage | The live audit file stores read and summary lines. | Where a rotation record is stored. | Team-Force |
| Shared account | The user `app_shared` is in the legacy script, the example env file, and Terraform. `rule.shared_admin_not_least_privilege`. CR-06. | Whether `automation_service` is `app_shared`. | Team-Force |
| History | The password and the example key sit in the working files today. | How a later reader of git history is told those values are retired. | Team-Force |

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| RE-01 | A rotation record would name the variable, the date, the person, and proof the old text is gone. | Assumption for the field list. The playbook asks for those contents. Verified Fact that no such record exists today: this stage's search of the docs tree and of `audit.py`. | A later reviewer can see that a named person changed a named variable on a named day. | A record that stored the old or new value would copy a secret into a new file. Operating contract stop list item 5 forbids that copy. | High for the forbid. Medium for the field list, which this stage proposes. | Team-Force accepts the field list when the store is named. |
| RE-02 | Where that record is stored is Unknown. | Verified Fact of the silence. `audit.py` line 9. `main.py` lines 15 and 23. No YAML id names a rotation store. | This stage can name the fields and cannot name the file. | A rotation that is never written down cannot be proven later. | High | Open question for S03: the YAML has no store for a rotation record, and this plan needs a named place. |
| RE-03 | Whether `automation_service` is `app_shared` is Unknown. | Verified Fact of the open question. `rule.shared_admin_not_least_privilege`. CR-06. R06. `access-semantics.yaml` `persona.automation_service` `open_question`. | A rotation of the shared password may retire one account or two. | A later reader can treat the persona and the user as the same login. | High for the Unknown. | The files do not say. |

## Lifecycle

This file cites `docs/02-baseline/defect-list.md` F05, `rule.shared_admin_not_least_privilege`, and CR-06. Stage S04-04 Half B removes the working-file secrets. Stage S04-07 adds the pattern test that later proof can cite. Stage S04-08 owns the audit schema and leaves it unchanged in this stage. Stage S05R folds the S03 open question into the YAML.
