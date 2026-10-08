# S02 — Behavioural baseline (Challenge 2, D2)

Phase 2 in `Execution Plan.md`. Spine stage 7. This stage records current behaviour and locks it with tests. It fixes nothing.

## Inputs

- `Project_Intent.md` (sections 4.2, 4.3, Appendix D)
- `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/` (all six files)
- `06-telecom-service-network-incident-ops/tests/`
- `06-telecom-service-network-incident-ops/data/` (manifest, quality_issues, synthetic files)
- `06-telecom-service-network-incident-ops/etl/run_daily_batch.py`
- `06-telecom-service-network-incident-ops/legacy/reconcile_legacy.py`
- `06-telecom-service-network-incident-ops/apps/api/`

## Prompt

```text
# Stage S02 — Behavioural baseline (Challenge 2)

## Objective
Capture the current behaviour of the inherited repo before anything changes it. Produce the Challenge 2 deliverables: baseline test report, behaviour snapshot, characterization tests, data-quality baseline, and a defect list that is separate from the list of behaviour to keep.

## Scope
Include: the S00 replay; `tests/`; `data/synthetic/`; `etl/`; `legacy/`; `apps/api/`.
Exclude: fixing any defect; changing any existing test; changing any application file. New files are allowed only under `docs/02-baseline/` and `tests/characterization/`.

## Required analysis
1. Baseline test report: run `pytest -q`. Record each test name and result. Three tests exist today.
2. Behaviour snapshot: for each route (`/health`, `/records/{id}`, `/ai/summarize/{id}`) and each script (`etl/run_daily_batch.py --sample`, `legacy/reconcile_legacy.py`, `scripts/sanity_check.py`): input, output, side effect.
3. Characterization tests: write new tests under `tests/characterization/` that pass against the current code and lock these behaviours: a missing id returns the first row (`REC-0001`); `clinician` is an accepted role on `/records/{id}`; `/ai/summarize/{id}` accepts a request with no role header; the ETL counts blank fields and does not quarantine rows; the legacy script holds a password constant (assert on the variable's presence, not its value). Each test docstring says "characterization: locks current behaviour; replace when the defect is fixed".
4. Data-quality baseline: write `docs/02-baseline/profile_data.py` and run it. It must report per file: row count against `manifest.json`; blanks per column; duplicate keys; alarms where `last_seen_at` is before `first_seen_at`; `service_orders.retry_count` out of range; distinct severity values in `incidents.csv` (expect `gold` and `bronze`); malformed `ai_call_id` values; `events.jsonl` rows with null or blank `correlation_id`. Confirm each item in `quality_issues.json` against the files and mark Confirmed or Not found.
5. Split findings into two lists: intended legacy behaviour to keep, and defects to fix. The missing-record fallback goes in the defect list. The two lists must not share a row.
For each finding: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, or Unknown.
- A Verified Fact names a test name, a command and its output, a file path with line, or a replay result.
- Numbers from `profile_data.py` are REAL. Say so.

## Constraints and guardrails
- Plain speech. Short sentences. Everyday words.
- Do not fix anything. Do not edit `tests/test_characterization.py` or `tests/test_api_contract.py`.
- No invented severity cutoff or SLA threshold. If `retry_count` "out of range" needs a bound, state the bound you used as PROPOSED and name the owner.
- Redact secrets. Never print the password value in any file or test.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md 4.3; read, do not re-derive)
| Constant | Value |
|---|---|
| Missing-record behaviour | return first row (REC-0001) |
| Allowed API roles | admin, operator, clinician, engineer, ai_agent |
| Default role when header absent | operator (see main.py) |
| CSV row counts / events | 354 each / 3000 |
| Seeded defects | duplicate keys, blanks, impossible timestamps, out-of-range scores (data/quality_issues.json) |
| Known odd values | severity gold and bronze; ai_call_id like AI_-00002; retry_count in the thousands |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/02-baseline/baseline-test-report.md`
2. `06-telecom-service-network-incident-ops/docs/02-baseline/behaviour-snapshot.md`
3. `06-telecom-service-network-incident-ops/tests/characterization/test_current_behaviour.py` (and `__init__.py` if pytest needs it)
4. `06-telecom-service-network-incident-ops/docs/02-baseline/profile_data.py`
5. `06-telecom-service-network-incident-ops/docs/02-baseline/data-quality-baseline.md`
6. `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md` — two tables: "Keep" and "Fix".

## Completion gate
PASS when all new characterization tests pass against unchanged code, `profile_data.py` runs, and a reader can point to one behaviour kept and one defect to fix with no row in both lists. CONDITIONAL PASS when one seeded defect from `quality_issues.json` could not be confirmed and that is written. BLOCKED when any existing test was edited or any application file changed.

## Lifecycle linkage
Cite `docs/00-setup/replay-log.md` and `docs/01-discovery/`. Stage S03 harvests status words from `data-quality-baseline.md`. Stage S04 Half A cites `defect-list.md` for what to fix. Stage S05-14 uses `behaviour-snapshot.md` as the "before" picture.

## Required final response
End with exactly these seven items:
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
| `baseline-test-report.md` | Header. Test names and results. Count: 3 existing plus the new characterization tests. |
| `behaviour-snapshot.md` | Header. One section per route and per script: input, output, side effect. |
| `tests/characterization/test_current_behaviour.py` | Five tests, all passing, each with the characterization docstring. |
| `profile_data.py` | Runs with `python docs/02-baseline/profile_data.py`. Prints or writes the profile. |
| `data-quality-baseline.md` | Header. Per-file table. Each `quality_issues.json` item marked Confirmed or Not found. Numbers labelled REAL. |
| `defect-list.md` | Header. "Keep" table and "Fix" table. Missing-record fallback is in "Fix". No row in both. |

## Done test

`pytest -q` passes with the new tests. `git status` shows no modified files, only new files under `docs/02-baseline/` and `tests/characterization/`.
