# AI subsystem discovery

| Field | Value |
|---|---|
| Stage | S01 — Discovery dossier (Execution Plan Phase 1; spine stages 0A, 5, 7) |
| Date / version | 2026-10-09, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The inventory owner column is Unknown on every row. That is more than half the rows. This file cites files and the replay. It proposes no change. |
| Evidence sources | `apps/api/services/ai_gateway.py`; `apps/api/main.py`; `apps/api/services/audit.py`; `data/synthetic/ai_invocations.csv`; `docs/architecture/current-state.md`; `tests/test_api_contract.py`; `logs/audit.log`; `docs/00-setup/replay-log.md`; `docs/00-contract/operating-contract.md` |
| Assumptions | The live AI path is the function `summarize_record` and the route that calls it. The CSV is a stored table. The gateway and the CSV are separate. |
| Unresolved issues | The three product names have no owner and no code. Whether any later worker treats the summary JSON as a work order is Unknown. The operating contract forbids that step and this note does not design a replacement. |
| Residual risks | The prompt text below is a quote of the source. It is not an instruction to run it. |

## What this file is

This file records the AI touchpoints that exist today: the prompt, the model name, the guardrail status, the token formula, the three product names, the CSV fields, and the fields that show where an answer came from.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Touchpoints

| Touchpoint | What it does today | Evidence |
|---|---|---|
| `apps/api/services/ai_gateway.py` | Builds a prompt, waits 0.01 seconds, returns a dict. | Verified Fact: lines 3 to 18. |
| `POST /ai/summarize/{record_id}` | Loads a device row, calls the gateway, writes an audit line, returns the dict. No role argument. | Verified Fact: `main.py` lines 19 to 24. Replay section 2.7. |
| `tests/test_api_contract.py` | `test_ai_summary_has_minimum_contract` posts `/ai/summarize/REC-0001` and checks that `summary`, `model`, and `guardrail_status` are present. | Verified Fact: the test. Replay section 1.3 passed it. |
| `logs/audit.log` | Stores `action` `ai.summary` with `record_id` and `model`. | Verified Fact: `main.py` line 23. Replay section 2.7 and section 3. |
| `data/synthetic/ai_invocations.csv` | 354 stored rows. The gateway does not write this file. | Verified Fact: `ai_gateway.py` has no open of this path. `docs/00-contract/operating-contract.md` row 6 states the same fact. |
| `docs/architecture/current-state.md` | Names three products. | Verified Fact: lines 11 to 13. No function in `ai_gateway.py` uses those names. |
| `.env.example` | Holds `AI_GATEWAY_KEY=<redacted>`. | Verified Fact: line 2. `ai_gateway.py` imports `os` and never reads the key. |
| `apps/web/src/app/api.service.ts` | `summarize` calls `fetch` `POST /api/ai/summarize/{id}`. | Verified Fact: line 4. The live route has no `/api` prefix. |
| `data/synthetic/events.jsonl` | 782 lines use event type "Topology lookup to AI recommendation". | Verified Fact: counted in this stage. No Python business code reads the lines. |

## Prompt, model, guardrail, token formula

**Verified Fact.** `ai_gateway.py`:

| Item | Value in the file |
|---|---|
| Model | `local-sim-v1` (`MODEL_VERSION`, line 3). The audit call in `main.py` line 23 repeats the same string. |
| Prompt | `Summarize this operational record and recommend next action: {record}` (`PROMPT_TEMPLATE`, line 4). Line 7 fills `{record}` with the whole device dict. |
| Wait | `time.sleep(0.01)` on line 9. |
| Token formula | `len(prompt.split()) * 2` on line 10. The result is returned as `token_estimate`. |
| Summary text | `"Synthetic summary for "` plus the first value in the dict (line 13). For a device row that first value is `device_id`. |
| Fixed sentence | `Review and approve before action` (line 14). |
| `source_count` | The number `1` (line 16). |
| Guardrail status | `not_enforced` (line 17). The function returns that word. It does not check the prompt text before the return. |

Replay section 2.7, `POST /ai/summarize/REC-0001` with no role header, returned:

`model` `local-sim-v1`, `summary` `Synthetic summary for REC-0001`, `recommendation` `Review and approve before action`, `token_estimate` 64, `source_count` 1, `guardrail_status` `not_enforced`.

The replay says 64 matches the word-count formula. This note cites that result. It does not recompute it.

Replay section 2.8: `POST /ai/summarize/DOES-NOT-EXIST` returned `Synthetic summary for REC-0001`. The gateway summarized the first device row. The audit line says `record_id` `DOES-NOT-EXIST`.

## Three product names

**Verified Fact.** `docs/architecture/current-state.md` lines 11 to 13:

- Network Incident Copilot
- Configuration Assistant
- Capacity Intelligence

The file gives the names only. `ai_gateway.py` has one function, `summarize_record`. `ai_invocations.csv` column `use_case` holds words such as `high_risk`, `internal`, and `normal` (counted in this stage). It does not hold the three product names. **Unknown:** which product, if any, a row belongs to.

## `ai_invocations.csv` fields

**Verified Fact.** Header line of `data/synthetic/ai_invocations.csv`:

`ai_call_id`, `incident_id`, `use_case`, `model`, `topology_snapshot_id`, `alarm_count`, `token_count`, `recommendation_risk`, `approval_required`, `guardrail_status`.

354 data rows. First `ai_call_id` is `REC-0001`. Line 2 is `AI_-00002`. 353 ids start with `AI_-`. Counted in this stage: zero rows have `model` `local-sim-v1`. The live gateway always returns `local-sim-v1`.

The live gateway does not write this file. **Verified Fact:** `ai_gateway.py` lines 6 to 18 return a dict and do not open a path. Operating contract row 6 records that fact.

## Provenance fields

Provenance here means the fields that show where an answer came from: who asked, which model, which input, which policy, and which approval.

### Present on the live call

| Field | Where |
|---|---|
| `model` `local-sim-v1` | Response body. `ai_gateway.py` line 12. Replay section 2.7. |
| `guardrail_status` `not_enforced` | Response body. Line 17. Replay section 2.7. |
| `token_estimate` | Response body. Line 10. Replay section 2.7 value 64 for `REC-0001`. |
| `source_count` `1` | Response body. Line 16. Hardcoded. |
| `summary` text that includes the first cell | Response body. Line 13. Replay section 2.7. |
| `ts`, `action` `ai.summary`, `details.record_id`, `details.model` | Audit line. `main.py` line 23. `audit.py` lines 8 to 9. Replay section 3. |

### Absent on the live call

| Field | What the files show |
|---|---|
| Actor | The summarize function takes no role. The audit details for `ai.summary` are `record_id` and `model` only. Replay section 2.7. |
| Correlation id | `audit.py` line 9 writes `ts`, `action`, and `details`. No correlation field. `observability/otel-notes.md` lines 4 to 5 say the same. |
| Approval id | No field on the response or the audit line. Operating contract row 9. Replay section 3. |
| Prompt hash or input hash | Not in the response. Not in the audit line. |
| Policy result | The route does not call `policy/opa/access.rego`. |
| `topology_snapshot_id` | Column on the CSV. Absent from the live response. |
| `incident_id`, `use_case`, `alarm_count`, `approval_required`, `recommendation_risk` | Columns on the CSV. Absent from the live response. |
| A new row in `ai_invocations.csv` | The gateway does not write one. |

### Name differences between the CSV and the live body

| CSV column | Live response field |
|---|---|
| `token_count` | `token_estimate` |
| `model` (words such as `approved`, `vendor`; zero `local-sim-v1`) | `model` `local-sim-v1` |
| `guardrail_status` (many words, including `not_enforced` on 27 rows) | always `not_enforced` |
| no `summary` column | `summary` |
| no column for the fixed sentence | `recommendation` |
| no `source_count` column | `source_count` |

**Verified Fact** for the live names: `ai_gateway.py` lines 11 to 18 and replay section 2.7. **Verified Fact** for the CSV mix: header plus the count in this stage.

## Lifecycle

This file cites `docs/00-setup/replay-log.md` and `docs/00-contract/operating-contract.md`. Operating contract row 3 says `ai_gateway.py` may change in a later stage. This stage does not edit it. Stage S02 cites this dossier for behaviours to snapshot. Stage S03 harvests entities and status words from it. Stage S09 reuses the risk register.
