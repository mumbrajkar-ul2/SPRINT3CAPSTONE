# Secrets evidence

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The pattern test passes on the cleaned repo and fails when a `sk-` value is put back. No real-looking secret remains in committed code or `.env.example`. Where a rotation record is stored is Unknown. Owner: Team-Force. |
| Evidence sources | `python -m pytest -q` before the edit; `python -m pytest -q tests/security/test_secret_patterns.py` on the cleaned repo; the same pattern test after a temporary `sk-` value; `python -m pytest -q` after the edit; `legacy/reconcile_legacy.py`; `.env.example`; `apps/api/settings.py` |
| Assumptions | The suite collected is the one in `pyproject.toml` `testpaths = ["tests"]`. Semantic-layer tests sit outside that path and were not part of this command. |
| Unresolved issues | Where a rotation record is stored is Unknown. Owner: Team-Force. Whether `automation_service` is `app_shared` is Unknown. |
| Residual risks | The old password and the old example key remain in git history. A placeholder in the working files leaves those older copies in history. |

## What this file is

This file records the pytest run before the Half B edit, the two pattern-test runs, and the pytest run after the edit. The outputs below are the real command output. They were not typed by hand.

Every secret value in this file is written `<redacted>`. The temporary fail run used the stand-in `sk-temp-should-fail`. That stand-in is not a live key.

The commands ran with the repo `.venv` Python from `06-telecom-service-network-incident-ops/`, with `PYTHONDONTWRITEBYTECODE` set.

## Before

This run is the tree while the password constant and the example key were still in the committed files. `test_legacy_script_holds_password_constant` is one of the fourteen tests. It passed, which locked the constant.

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
14 passed, 7 warnings in 0.84s
```

**Verified Fact.** 14 passed, 7 warnings, exit code 0.

## The Half B edits

`legacy/reconcile_legacy.py` no longer assigns `SHARED_DB_PASSWORD` a string. `reconcile()` calls `require("SHARED_DB_PASSWORD")` before it counts the device rows. The user name `app_shared` stays.

`apps/api/settings.py` reads a required name from the environment. A missing, empty, or `CHANGE_ME` value raises `SettingsError` and names the variable. The module stays quiet at import.

`.env.example` keeps the same names. Each secret value is `CHANGE_ME`. The user name `app_shared` stays in `DATABASE_URL`. The example AI key has no `sk-` prefix.

`tests/characterization/test_current_behaviour.py` replaced `test_legacy_script_holds_password_constant` with `test_legacy_script_reads_password_from_environment`. The new docstring says it replaces the old test.

`tests/security/test_secret_patterns.py` scans the repo, skips `.git`, venv, and `docs/`, and is marked `@pytest.mark.security`.

## Pattern test on the cleaned repo

```text
.                                                                        [100%]
1 passed in 0.81s
```

**Verified Fact.** 1 passed, exit code 0.

## Pattern test after a known string is put back

`.env.example` line 2 was set to `AI_GATEWAY_KEY=sk-temp-should-fail` for one run, then restored to `AI_GATEWAY_KEY=CHANGE_ME`.

```text
F                                                                        [100%]
================================== FAILURES ===================================
______________________ test_repo_has_no_secret_patterns _______________________

    @pytest.mark.security
    def test_repo_has_no_secret_patterns():
        hits = find_secret_pattern_hits()
>       assert hits == [], hits
E       AssertionError: ['.env.example:2: sk- key pattern', '.env.example:2: AI_GATEWAY_KEY holds a non-placeholder']
E       assert ['.env.exampl...-placeholder'] == []
E
E         Left contains 2 more items, first extra item: '.env.example:2: sk- key pattern'
E         Use -v to get more diff

tests\security\test_secret_patterns.py:83: AssertionError
=========================== short test summary info ===========================
FAILED tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns
1 failed in 0.88s
```

**Verified Fact.** 1 failed, exit code 1. The file was restored to `CHANGE_ME` after this run.

## After

This run is the tree after the loader, the legacy edit, the placeholder file, the replaced characterization test, and the pattern test.

```text
...............                                                          [100%]
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
15 passed, 7 warnings in 1.96s
```

**Verified Fact.** 15 passed, 7 warnings, exit code 0.

The count moves from 14 to 15 because one characterization test was replaced and one security test was added. 14 − 1 + 1 + 1 = 15.

## What the runs show

| Check | Before | After |
|---|---|---|
| Password constant in `legacy/reconcile_legacy.py` | Present. `test_legacy_script_holds_password_constant` passed. Value `<redacted>`. | Gone. `test_legacy_script_reads_password_from_environment` passed. The script prints `legacy reconciled 354` when `SHARED_DB_PASSWORD` is set. It stops with `SettingsError` when the name is absent, and it prints no count. |
| `.env.example` secret values | Real-looking values. Value `<redacted>`. | All four secret values are `CHANGE_ME`. |
| Pattern test | The file did not exist. | Passes on the cleaned repo. Fails when line 2 is `sk-temp-should-fail`. |
| Record read, summary, health, ETL, access tests | Passed inside the 14. | Passed inside the 15. |

Worked example. Before the edit, `legacy/reconcile_legacy.py` line 6 assigned `SHARED_DB_PASSWORD` a string. After the edit, that name is read from the environment. With `SHARED_DB_PASSWORD=local-test-only`, the script still prints `legacy reconciled 354`. With the name unset, the process exits non-zero and the count is absent from stdout.

A search of `06-telecom-service-network-incident-ops/` for the old password text and the old example key found no hits.

## Lifecycle

Stage S04-07 adds `tests/security/test_secret_patterns.py` to CI. Stage S04-09 uses `docs/04-secrets/sensitive-field-handling-checklist.md` for the prompt allow-list. Stage S05-13 collects the pattern test into the security suite. Stage S05R folds the two open questions for S03.
