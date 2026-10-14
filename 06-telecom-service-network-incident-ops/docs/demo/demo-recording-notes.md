# Demo recording notes

| Field | Value |
|---|---|
| Stage | S07. Application and demo. These notes tell the person who records the demo what to show, which file proves each point, and what not to claim. |
| Date / version | 2026-10-13, v1.1. Semantic layer 1.2.1. PRD v1.9. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Ready to record. The agent ran the page in a browser on 2026-10-13 and read each result. The agent made no video. |
| Evidence sources | `docs/demo/demo-script.md`. `docs/demo/evidence.md`. `apps/api/static/index.html`. `apps/api/main.py`. `tests/app/`. `docs/prd/prd.md` sections 7, 8 and 12. |
| Assumptions | (1) The recorder runs the app on one machine with the commands in `docs/demo/demo-script.md`, section 1. (2) The recorder shows the page, one editor window and one terminal. |
| Unresolved issues | The PRD gaps in `docs/demo/evidence.md`, section 7, have no owner answer yet. The recording can say so. |
| Residual risks | A viewer can read the stub text as real model output. The notes below say what to say to prevent that. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Before you record

| Check | How |
|---|---|
| The app runs on the Python copy of the policy. | `$env:POLICY_ENGINE = "python"` before `uvicorn`. |
| The files of an earlier run are out of the way. | Move `logs/audit.log` and `logs/approvals.jsonl` to a folder named for the earlier run. The audit read then shows only this recording. |
| The test suite passes. | `.\.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q`. On 2026-10-13: 469 passed, 0 skipped (REAL), with `opa` 1.21.2 on the path. Without `opa`, the result is 467 passed and 2 skipped. |
| The browser window is wide enough to show the audit table. | The table has 11 columns. |

## 2. What to show at each step

| Step | Show on screen | Say | File that proves it | Do not claim |
|---|---|---|---|---|
| Open the page | The top of the page, with the four label words and the case id. | "Every number has a label. Real means the app counted it in this run. Simulated means the stub made it up." | `apps/api/static/index.html`; `tests/app/test_page.py::test_every_number_on_the_page_has_a_label` | Do not say the labels are checked by a browser test. The test reads the page source. It does not run the page. |
| 1. Read storm | Counts and the one row. Point at the flag word. | "These counts come from the alarm file at the moment of the call. They are real. The rows in the file are synthetic." | `apps/api/services/alarm_service.py`; `tests/app/test_storm_route.py` | Do not call the storm large or small. The route sets no size (RQ-13). Do not say an incident was opened. The route opens none. |
| 2. Look up device | The device table and the line "Left out for this role". | "The operator role does not get the management address or the credential profile. In this data the address field holds a word such as alpha." | `tests/app/test_records_route.py` | Do not say the data is a real network. All rows are synthetic. |
| 3. Recommendation | The outcome `HOLD_FOR_REVIEW`, the sentence, the provenance table. | "The policy holds every healthy recommendation for a person. The sentence is simulated. Tokens are an educational estimate: a word count times two. The delay is the stub's." | `apps/api/services/ai_gateway.py`; `tests/app/test_recommend_route.py` | Do not say the model is accurate or safe. It is a stub. Do not quote the tokens or the delay as a cost or a speed. |
| 4. Decision | Click yes. Show the approver and the approval id. | "A person stored a decision. The server set the approver and the approval id. Nothing in the network changed." | `apps/api/services/approvals.py`; `tests/app/test_approvals_route.py` | Do not say the approver is a verified person. The role is a word the caller typed. Say "claimed role". |
| 5. Audit chain | The table of four rows and the "cannot prove" list. | "One case id gives the whole case back. The log still cannot say who the caller was." | `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id`; `docs/14-audit/` | Do not say the log is tamper-proof. It is a plain file (`log_integrity`). |
| Timeout variant | Restart with the short deadline. Show `HOLD_FOR_REVIEW`, the notice "A person must review this case", and the empty summary. Then show the decision returning "Nothing was stored". | "When the model is late, the system shows no text. It does not make up a safe-looking summary." | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary`; `tests/app/test_demo_flow.py::test_ai_timeout_variant_holds_with_no_summary_and_no_approval_is_possible` | Do not say 0.001 seconds is the product's deadline. It is a test setting. The code default is 10 seconds and is PROPOSED. |
| Missing device and stale device | `STO-00001` and `STO-00005`. Show `BLOCK` and the reason. | "Two stops. One device has no row. One device is flagged stale. The model does not run in either case." | `tests/app/test_demo_flow.py` | Do not say the system fixes stale data. It refuses to recommend from it. |
| Audit before change | The terminal with the test run. Show `tests/app/test_audit_before_state_change.py`. | "The test makes the approval store fail. The audit row is still there. A second test makes the audit write fail. No approval is stored." | `tests/app/test_audit_before_state_change.py` | Do not say every possible failure is covered. The tests cover the write failures named in the PRD. |

## 3. What not to claim

These limits are real. Say them if a viewer asks. Each one has a source.

| Limit | Source |
|---|---|
| The role header is a word the caller types. Nothing proves who the caller is. `actor` and `approver` are claims. | PRD D-07 and RQ-65; `cannot_prove` item `caller_identity` |
| The command-phrase lists are short. A sentence that means the same as a listed phrase, in other words, passes the check. | PRD RQ-30; `tests/app/test_command_phrases.py::test_a_phrase_that_is_not_on_either_list_gets_through` |
| The near-miss list is a draft that S07 wrote. It needs Team-Force review. | `docs/ADR/0005-s07-yaml-additions.md` |
| The check for a forbidden value in the model answer uses plain words such as `alpha` as values. A harmless sentence that holds such a word is held for review. | `apps/api/services/ai_gateway.py`, `answer_check_reasons` |
| The policy checks that an approval id is not blank. It does not look the id up in the approvals file. | `docs/demo/evidence.md`, section 8 |
| The audit log is a plain file. A line can be changed or deleted. | `cannot_prove` item `log_integrity` |
| The answer store (RQ-31) is not built. Two identical requests call the model twice. | `docs/ADR/0004-defer-rq-31-answer-store.md` |
| No EXECUTE route exists. The system does not change a device, so the demo shows no network change. | PRD RQ-57, RQ-58 |
| The Angular scaffold in `apps/web` is not wired. It sends no role header, so its calls get 403. | `docs/demo/evidence.md`, section 7 |

## 4. Order for a short recording

A short recording shows the page opening, steps 1 to 5 for `STO-00002`, the timeout variant, and the passing test run. Leave out the other variants unless a viewer asks.
