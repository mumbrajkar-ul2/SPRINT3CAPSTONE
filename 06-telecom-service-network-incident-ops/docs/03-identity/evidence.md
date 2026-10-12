# Identity evidence

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The negative tests pass. Header `clinician` is denied. The other live results stay as they were. A call with no role header still uses `operator`. The proposed change is to refuse that call. Owner: Team-Force. |
| Evidence sources | `python -m pytest -q` before the edit; `python -m pytest -q` after the edit; `apps/api/main.py`; `tests/characterization/test_current_behaviour.py`; `tests/access/test_negative_access.py` |
| Assumptions | The suite collected is the one in `pyproject.toml` `testpaths = ["tests"]`. Semantic-layer tests sit outside that path and were not part of this command. |
| Unresolved issues | The playbook done-test line says `clinician` returns 403. Half B does not change the status code. The deny stays HTTP 200 with body `{"error":"forbidden"}`. S04-06 is the stage that returns 403. The missing-header deny stays PROPOSED. Owner: Team-Force. |
| Residual risks | A caller who sends no role can still read the device row, including `mgmt_ip` and `credential_profile`. A client that checks only the status code still sees 200 on a denied call. |

## What this file is

This file records the pytest run before the Half B edit and the pytest run after it. Both outputs below are the real command output. They were not typed by hand.

The command each time was `python -m pytest -q`, run with the repo `.venv` Python from `06-telecom-service-network-incident-ops/`, with `PYTHONDONTWRITEBYTECODE` set so the run wrote no bytecode files. Exit code was 0 both times.

## Before

This run is the tree before `clinician` left the allow list. `test_clinician_role_is_accepted_on_record_read` is one of the eight tests. It passed, which locked the allow.

```text
........                                                                 [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\starlette\testclient.py:40
  C:\MangeshStudy\FDE\Labs\SPRINT3CAPSTONE\06-telecom-service-network-incident-ops\.venv\Lib\site-packages\starlette\testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row
tests/characterization/test_current_behaviour.py::test_clinician_role_is_accepted_on_record_read
tests/characterization/test_current_behaviour.py::test_ai_summarize_accepts_request_with_no_role_header
tests/test_api_contract.py::test_ai_summary_has_minimum_contract
  C:\MangeshStudy\FDE\Labs\SPRINT3CAPSTONE\06-telecom-service-network-incident-ops\apps\api\services\audit.py:9: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    event = {"ts": datetime.utcnow().isoformat(), "action": action, "details": details}

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
8 passed, 5 warnings in 1.66s
```

**Verified Fact.** 8 passed, 5 warnings, exit code 0.

## The one change in main.py

`apps/api/main.py` line 13 lost the word `clinician`. Nothing else in that file changed.

```text
-    if x_user_role in ["admin", "operator", "clinician", "engineer", "ai_agent"]:
+    if x_user_role in ["admin", "operator", "engineer", "ai_agent"]:
```

The header default on line 11 is still `operator`. A role outside the list still returns `{"error":"forbidden"}` on line 17, with HTTP 200.

`tests/characterization/test_current_behaviour.py` replaced `test_clinician_role_is_accepted_on_record_read` with `test_clinician_role_is_denied_on_record_read`. The new docstring says it replaces the old test.

## After

This run is the tree after that edit, the replaced characterization test, and `tests/access/test_negative_access.py`.

```text
..............                                                           [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\starlette\testclient.py:40
  C:\MangeshStudy\FDE\Labs\SPRINT3CAPSTONE\06-telecom-service-network-incident-ops\.venv\Lib\site-packages\starlette\testclient.py:40: DeprecationWarning: The anyio.abc.BlockingPortal alias is deprecated, use anyio.from_thread.BlockingPortal instead.
    _PortalFactoryType = typing.Callable[[], typing.ContextManager[anyio.abc.BlockingPortal]]

tests/access/test_negative_access.py::test_noc_operator_mapped_role_may_read_record
tests/access/test_negative_access.py::test_ai_agent_may_recommend
tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default
tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row
tests/characterization/test_current_behaviour.py::test_ai_summarize_accepts_request_with_no_role_header
tests/test_api_contract.py::test_ai_summary_has_minimum_contract
  C:\MangeshStudy\FDE\Labs\SPRINT3CAPSTONE\06-telecom-service-network-incident-ops\apps\api\services\audit.py:9: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    event = {"ts": datetime.utcnow().isoformat(), "action": action, "details": details}

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
14 passed, 7 warnings in 1.03s
```

**Verified Fact.** 14 passed, 7 warnings, exit code 0.

The count moves from 8 to 14 because one characterization test was replaced and six access tests were added. 8 − 1 + 1 + 6 = 14.

## What the two runs show

| Check | Before | After |
|---|---|---|
| Header `operator` on `GET /records/REC-0001` | Allowed. The missing-id test still passed. | Allowed. `test_noc_operator_mapped_role_may_read_record` passed. |
| Header `clinician` | Allowed. `test_clinician_role_is_accepted_on_record_read` passed and wrote an audit line. | Denied. The warning list no longer names a clinician test, so that call wrote no audit line. The body asserted is `{"error":"forbidden"}`. Status 200. |
| Header `ai_agent` | Still on the list. No access test yet. | `test_ai_agent_may_recommend` passed and returned `REC-0001`. |
| No role header on the record route | The default was `operator`. No test named that call. | `test_missing_role_header_keeps_operator_default` passed and returned `REC-0001`. |
| Summary with no role header | `test_ai_summarize_accepts_request_with_no_role_header` passed. | The same test passed. |
| Health, summary contract, missing id, ETL count, legacy password | Passed inside the 8. | Passed inside the 14. |

Worked example. Before the edit, `GET /records/REC-0001` with header `clinician` returned the `REC-0001` row. After the edit, the same call returns `{"error":"forbidden"}` and the status stays 200. `GET /records/REC-0001` with header `operator` still returns the `REC-0001` row.

The recommend and execute cases in `tests/access/test_negative_access.py` record the target decision. `persona.ai_agent` recommend is allow (`TA-33`). `persona.ai_agent` execute is deny. `persona.automation_service` execute with an empty approval id is deny. The live app still has no execute route. Those three checks do not call a policy engine. S04-06 is the stage that does.

## Lifecycle

Stage S04-06 consumes `policy-input-model.md` and is the stage that returns 403. Stage S05-13 collects `tests/access/test_negative_access.py` into the security suite. The no-header proposal stays PB-04. Owner: Team-Force.
