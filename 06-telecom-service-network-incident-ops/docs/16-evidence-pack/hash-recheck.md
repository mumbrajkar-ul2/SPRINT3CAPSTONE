# Hash re-check of the 36 files

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenges 15 and 16). |
| Date / version | 2026-10-13 local time (2026-10-14 UTC), v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | 36 of 36 match. |
| Evidence sources | `docs/model-comparison/yaml-hashes-after.md` (the table of 36 rows). The 36 files on disk. A Python script that reads each row, hashes the file with SHA-256, and compares the result with the "before" column, the "after" column and the byte count. |
| Assumptions | The table in `docs/model-comparison/yaml-hashes-after.md` lists the files in the first column and the SHA-256 in the second and third columns. |
| Unresolved issues | None. |
| Residual risks | A hash match proves the bytes are the same as at S08 Part 3. It does not prove the content is right. |

Paths are relative to the project folder (06-telecom-service-network-incident-ops).

## Result

| Measure | Value |
|---|---|
| Rows read from `docs/model-comparison/yaml-hashes-after.md` | 36 |
| Rows where the file hash equals the "before" hash, equals the "after" hash, and the byte count matches | 36 |
| Rows with a mismatch or a missing file | 0 |

Label: REAL.

**Verified Fact.** The result means that none of the 20 files in `semantic-layer/`, `docs/prd/prd.md` and the 15 other files named in `docs/model-comparison/yaml-hashes-after.md` changed between the S08 Part 3 check and this check. S09 changed none of them.

## How to repeat

From the project folder (06-telecom-service-network-incident-ops), read the rows of `docs/model-comparison/yaml-hashes-after.md` whose third column holds 64 hexadecimal characters. For each row, compute `Get-FileHash <file> -Algorithm SHA256` and compare it with the second and third columns.
