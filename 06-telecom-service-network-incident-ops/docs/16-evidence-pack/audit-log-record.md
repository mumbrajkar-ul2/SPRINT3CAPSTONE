# Audit log record around the final evidence run

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenges 15 and 16). |
| Date / version | 2026-10-13 local time (2026-10-14 UTC), v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | Record of one measurement. Not a gate by itself. |
| Evidence sources | `logs/audit.log` read with `Get-Content` and `Get-FileHash` before the run, right after the run, and after the restore. `evidence/run-info.txt`. |
| Assumptions | The file `logs/audit.log` is tracked by git (decision on `BL-09`, `docs/13-security-validation/remediation-backlog.md`). Older tests outside `tests/app/` write to it. |
| Unresolved issues | None for this record. |
| Residual risks | The restore replaced the file with the saved copy. The 6 rows the run wrote are no longer in the file. This file names them. |

Paths are relative to the project folder (06-telecom-service-network-incident-ops).

## What was measured

| Moment | Time (UTC) | Lines | Bytes | SHA-256 |
|---|---|---|---|---|
| Before the run | 2026-10-14 06:31:53 | 308 | 97099 | `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` |
| After the run, before the restore | 2026-10-14 06:37:27 | 314 | 99799 | `A117EA326FE4AA4D3E87ABF9D292D60D89F82DF9FD6C0BAF1BD5ABF47A7A8B55` |
| After the restore | 2026-10-14 (after 06:37:27) | 308 | 97099 | `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` |

All three numbers are REAL.

## Were the rows added by the run, or restored?

**Verified Fact.** The run added 6 rows. The first 308 lines after the run were identical to the 308 lines before it. Lines 309 to 314 are new. The run wrote them. Nothing was restored by the run.

The 6 new rows came from tests that call the real routes without a temporary log. The row `action`, `role` and time of day are below. No row holds a prompt text, `mgmt_ip`, `credential_profile` or a secret.

| Line | Time (UTC) | action | role |
|---|---|---|---|
| 309 | 2026-10-14 06:32:32 | `ai.summary` | operator |
| 310 | 2026-10-14 06:33:29 | `record.read` | operator |
| 311 | 2026-10-14 06:33:29 | `policy.deny` | clinician |
| 312 | 2026-10-14 06:33:29 | `record.read` | ai_agent |
| 313 | 2026-10-14 06:33:29 | `policy.deny` | automation_service |
| 314 | 2026-10-14 06:33:33 | `policy.deny` | clinician |

**Verified Fact.** After the run, the agent copied the saved pre-run file back over `logs/audit.log`. The file now has 308 lines and the same SHA-256 as before the run. It is also the same SHA-256 that `docs/model-comparison/app-comparison.md` section 10 records for the S08 restore.

So the answer is: the run added 6 rows, and the agent then restored the file to its earlier 308-line state.

## Why the log changes during a run

**Verified Fact.** Tests outside `tests/app/` write to the real log (`docs/demo/evidence.md` section 8, limit 7; `tests/app/test_audit_row_keys.py::test_app_tests_do_not_write_to_the_real_audit_log` covers only `tests/app/`). This is gap `BL-09` and risk `RK-08` in `docs/prd/Risk Management.md`.

## What this record does not prove

- **Unknown.** Whether the 6 rows would have caused any later test or report to differ. No later check was run with them in place.
- **Unknown.** Whether two runs at the same time would have lost rows. That is `RK-08`.
