# Secret rotation log

| Field | Value |
|---|---|
| Stage | S05R follow-up, decision D-12 (option A). Names the place for rotation records. |
| Date / version | 2026-10-12, v1.0 |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Created. The log has no entries. No rotation has been recorded. Owner: Team-Force. |
| Evidence sources | `docs/04-secrets/rotation-evidence-plan.md` (the record fields); `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` (the decision to keep this log) |
| Assumptions | (1) A markdown log is enough for this lab. (2) A real system would keep rotation records in a secret manager. The PRD (stage S06) says so. |
| Unresolved issues | Whether `automation_service` is the database user `app_shared` is Unknown. The password and the example key are still in git history. A rotation of the live values is not recorded here, because none has been made. |
| Residual risks | A log that nobody fills in proves nothing. An entry that holds a secret value copies the secret into a new file. |

Paths are relative to `06-telecom-service-network-incident-ops/`.

## What this log is for

When a secret is replaced, one row goes in the table below. A reviewer can then see which variable changed, on which day, and who changed it.

## Rules for every row

1. Never write a secret value in this file. Not the old value, not the new value.
2. Write the old value and the new value only as `<redacted>` if the column asks for them.
3. Name the variable. The names are `SHARED_DB_PASSWORD`, `DATABASE_URL`, `AI_GATEWAY_KEY`, `LEGACY_BATCH_PASSWORD`, `OT_VENDOR_TOKEN`.
4. Name a person, not a team.
5. In "Proof the old text is gone", write the path of a test run, or a short note. The pattern test for committed secrets is the usual proof.

## Log

| Date | Variable name | Person | Where it was replaced | Proof the old text is gone |
|---|---|---|---|---|
| (no entries) | | | | |

## Example row (not a real rotation)

| Date | Variable name | Person | Where it was replaced | Proof the old text is gone |
|---|---|---|---|---|
| 2026-01-01 | `AI_GATEWAY_KEY` | A. Example | The local `.env` file | `evidence/junit-security.xml`, secret pattern test passed |

The example row is invented to show the shape. It is not a record.
