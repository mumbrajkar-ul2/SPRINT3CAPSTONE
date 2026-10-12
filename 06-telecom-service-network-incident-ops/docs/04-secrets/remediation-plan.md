# Remediation plan

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every inventory row has an action and an owner. The actions wait for Half B. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Evidence sources | `docs/04-secrets/secrets-inventory.md`; `legacy/reconcile_legacy.py`; `.env.example`; `infra/terraform/main.tf`; `docs/00-contract/operating-contract.md`; `docs/02-baseline/defect-list.md`; `docs/03-identity/current-role-matrix.md`; `semantic-layer/business-rules.yaml`; `tests/characterization/test_current_behaviour.py` |
| Assumptions | Half B is the first edit that may change `legacy/reconcile_legacy.py` and `.env.example`. A later pattern test is the proof that a known string is gone. |
| Unresolved issues | Whether `automation_service` is the user `app_shared` is Unknown. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Residual risks | The password and the example key are already in git history. Replacing the working-file text leaves the older copies in history. `test_legacy_script_holds_password_constant` still expects the password constant in the source file. Removing the constant will fail `pytest -q` until that assertion is updated. |

## What this file is

This file says what to do with each inventory row, who owns the action, and what later proof will show the action is done. Half A writes the plan. The program files stay as they are.

Rotate means change the secret to a new value so the old text no longer works as a login. The old text is already in this repo, so the new value must be different.

Every secret value in this file is written `<redacted>`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Actions

| id | inventory row | action | owner | later proof |
|---|---|---|---|---|
| RP-01 | SI-01. Password constant `SHARED_DB_PASSWORD` in `legacy/reconcile_legacy.py` line 6. | Move the password to the environment. The script reads the name from the process start values. Rotate the password, because the old text is already in the repo. Do not copy the old text into a new file. | Mangesh (FDE). Operating contract row 4 names this edit. | The constant is gone from `legacy/reconcile_legacy.py`. The pattern test fails when the old text is put back. The script still prints the device-row count when the name is set. |
| RP-02 | SI-02. Shared user `app_shared` in `legacy/reconcile_legacy.py` line 5. | Leave the user name in the script. Operating contract row 4 names the password move only. | Team-Force | The user name `app_shared` remains. The password constant is gone. |
| RP-03 | SI-03. Password inside `DATABASE_URL` on `.env.example` line 1. | Replace the password text with the placeholder `CHANGE_ME`. The user name `app_shared` may stay. Rotate, because the old text is already in the repo. | Team-Force | `.env.example` line 1 holds `CHANGE_ME` in the password place. The pattern test finds no old password text outside `docs/`. |
| RP-04 | SI-04. Example AI key on `.env.example` line 2. | Replace the value with `CHANGE_ME`. The letters `sk-` leave the value. Rotate, because the old text is already in the repo. | Team-Force | `.env.example` line 2 is `AI_GATEWAY_KEY=CHANGE_ME`. The pattern test finds no `sk-` key in committed code or `.env.example`. |
| RP-05 | SI-05. Batch password on `.env.example` line 3. | Replace the value with `CHANGE_ME`. Rotate, because the old text is already in the repo. | Team-Force | `.env.example` line 3 is `LEGACY_BATCH_PASSWORD=CHANGE_ME`. The pattern test finds no old batch password text. |
| RP-06 | SI-06. Shared vendor token on `.env.example` line 4. | Replace the value with `CHANGE_ME`. Rotate, because the old text is already in the repo. | Team-Force | `.env.example` line 4 is `OT_VENDOR_TOKEN=CHANGE_ME`. The pattern test finds no old token text. |
| RP-07 | SI-07. Terraform writes `shared_user=app_shared` in `infra/terraform/main.tf` line 4. | Leave the user name. Do not add a password to `generated-env.txt`. | Team-Force | `main.tf` line 4 still writes the user name only. |
| RP-08 | SI-08. No password, key, or token constant in `apps/`. | No code change in `apps/` in this stage. | Team-Force | A later search of `apps/` still finds no secret constant. |

`.env.example` line 5 (`LOG_LEVEL=DEBUG`) stays as it is. It is a log setting.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| RP-01 | The password constant leaves the legacy script in Half B and is read from the environment. | Verified Fact of today's assignment: `legacy/reconcile_legacy.py` line 6. F05. Operating contract row 4. | The script keeps the device-row count once the name is set. K04. | `test_legacy_script_holds_password_constant` in `tests/characterization/test_current_behaviour.py` line 93 asserts the constant is still in the source file. That test will fail when the constant is removed, until the assertion is updated. | High | None for the named edit. |
| RP-03 | The four secret values in `.env.example` become the placeholder `CHANGE_ME`. | Verified Fact of today's values: `.env.example` lines 1 to 4. Playbook Half B item 3 names the placeholder. | The committed example file then holds stand-in text. | The old text remains in git history. | High | None for the placeholder rule. |
| RP-07 | Terraform keeps the user name and gains no password. | Verified Fact. `infra/terraform/main.tf` line 4 writes `shared_user=app_shared`. | Applying the file still writes the user name only. | A later edit that adds a password would write a secret to `generated-env.txt`. | High | Whether the declaration was ever applied is Unknown. |
| RP-08 | `apps/` needs no secret-constant change in this stage. | Verified Fact. SI-08. | Half B can add `apps/api/settings.py` as a loader without first deleting a key from `apps/`. | The summary still places the whole device row in the prompt. F12. Stage S04-09 owns that prompt change. | High | None for a missing key. |

## Half B note, not done in this half

`test_legacy_script_holds_password_constant` walks `legacy/reconcile_legacy.py` and asserts that `SHARED_DB_PASSWORD` is assigned a non-empty string. **Verified Fact.** `tests/characterization/test_current_behaviour.py` lines 93 to 100. Removing the constant will fail `pytest -q` until that assertion is updated. This half leaves the test as it is.

## Lifecycle

This file cites `docs/02-baseline/defect-list.md` F05 and `docs/00-contract/operating-contract.md` row 4. Stage S04-04 Half B applies RP-01 and RP-03 through RP-06. Stage S04-07 adds the pattern test to CI. Stage S05-13 collects the test into the security suite.
