# Cleaned configuration model

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The loader design names placeholders, an environment read, and a clear error when a required value is absent. The loader is written in Half B. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Evidence sources | `.env.example`; `legacy/reconcile_legacy.py`; `apps/api/services/ai_gateway.py`; `apps/api/main.py`; `docs/04-secrets/secrets-inventory.md`; `docs/04-secrets/remediation-plan.md`; `docs/00-contract/operating-contract.md`; `playbook/S04-04-secrets.md` |
| Assumptions | The live routes in `main.py` do not read these secret names today. A loader that fails when the process starts would stop `/health` on a machine that has no secret set. |
| Unresolved issues | Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Residual risks | A placeholder in `.env.example` still leaves the old text in git history. A caller who copies `.env.example` and leaves `CHANGE_ME` in place will hit the missing-value error only after a function asks for that name. |

## What this file is

This file is the design for how settings load after Half B. It names the placeholder rule, the loader, and the error when a required secret is absent. Half A writes the design. The program files stay as they are.

The environment is the set of named values the process is started with. The loader reads those names. It does not store a real secret in a committed file.

Every secret value in this file is written `<redacted>`.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Placeholder rule

`.env.example` keeps the names that are already there: `DATABASE_URL`, `AI_GATEWAY_KEY`, `LEGACY_BATCH_PASSWORD`, `OT_VENDOR_TOKEN`, and `LOG_LEVEL`.

Each secret value becomes the placeholder `CHANGE_ME`.

The user name `app_shared` may stay in `DATABASE_URL`.

The example AI key must be `CHANGE_ME`. The letters `sk-` leave that value.

`LOG_LEVEL=DEBUG` stays. It is a log setting.

## Loader

A later file `apps/api/settings.py` reads a required name from `os.environ`.

The loader holds no default for a secret.

When a caller asks for a required name and the name is absent, or the value is empty, or the value is `CHANGE_ME`, the loader raises an error. The error names the variable. The error prints no secret value.

The file loads when a caller asks. It stays quiet at import. The live routes `/health`, `/records/{record_id}`, and `/ai/summarize/{record_id}` do not use these secrets today. **Verified Fact.** `apps/api/main.py` lines 6 to 24. `ai_gateway.py` line 1 imports `os` and never reads a key. A raise at import would stop `/health` on a machine that has no secret set.

## Legacy script

In Half B, `legacy/reconcile_legacy.py` reads `SHARED_DB_PASSWORD` from the environment through the same fail-clear rule.

When the name is missing, the script stops with that error before it prints the device-row count.

When the name is set to a real value, the script still prints the device-row count. That count is K04. Operating contract row 4 keeps it.

The user name `SHARED_DB_USER` may stay as `app_shared` in the script.

## What this design uses

The design uses the process environment and the example file of names.

This repo can load those names from the environment. A later live system may want a managed store. That store is out of scope here. This file does not name one.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| CM-01 | The example file will hold names and the placeholder `CHANGE_ME` for every secret. | Verified Fact of today's file: `.env.example` lines 1 to 4 hold real-looking values. Playbook Half B item 3 names `CHANGE_ME`. | A new machine can copy the names without copying a secret. | A person who leaves `CHANGE_ME` in place will hit the fail-clear error when a function asks for the name. | High | None for the placeholder. |
| CM-02 | The loader reads the environment and raises a named error when a required secret is absent. | Inference from the playbook Half B item 2 and from SI-08: `apps/` has no settings file today. | A missing secret fails in one place with a message that names the variable. | Raising at import would stop `/health`. The design loads on demand for that reason. | High for the on-demand rule. Medium for the exact error class, which Half B will pick. | The exact exception class is left to Half B. |
| CM-03 | The legacy script will read `SHARED_DB_PASSWORD` from the environment and keep the row count when the name is set. | Verified Fact of today's script: `legacy/reconcile_legacy.py` lines 5 to 14. F05. K04. Operating contract row 4. | The password leaves the source file. The printed count stays. | `test_legacy_script_holds_password_constant` will fail until that assertion is updated. | High | None for the named edit. |

## Lifecycle

This file is the design Half B implements in `apps/api/settings.py`, `legacy/reconcile_legacy.py`, and `.env.example`. Stage S04-07 adds the pattern test to CI. Stage S05-13 collects the test into the security suite.
