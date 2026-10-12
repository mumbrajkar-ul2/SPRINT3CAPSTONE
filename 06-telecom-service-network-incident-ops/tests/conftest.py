"""Shared test setup. Stage S04-11 Half B. Extended in S05-13 Half B."""

import pytest

from apps.api.services import breaker, policy


@pytest.fixture(autouse=True)
def fresh_breaker(monkeypatch):
    """Every test starts with a closed breaker and the default settings.

    The breaker lives in the process. Without this, failures from one test (a model that
    raises, a timeout) would count toward the threshold of a later test.
    """
    for name in (breaker.THRESHOLD_ENV, breaker.OPEN_SECONDS_ENV, breaker.MAX_IN_FLIGHT_ENV):
        monkeypatch.delenv(name, raising=False)
    breaker.reset()
    yield
    breaker.reset()


@pytest.fixture(autouse=True)
def python_policy_engine(monkeypatch):
    """Run the Python copy of the policy for every test under tests/.

    S05-13 Half B (backlog row SB-20). With `opa` on the PATH, the default setting
    (`POLICY_ENGINE` unset, meaning auto) starts one `opa eval` program for every decision.
    Measured on 2026-10-11 on this Windows machine: a record read took a median 150 ms with
    `opa` and 10 ms with the Python copy, and a summary took 401 ms and 26 ms. The timing
    tests under tests/reliability and tests/performance then fail for a reason that is not the
    code they test. These tests check the app, not the engine.

    The Rego copy is still tested. policy/tests runs `opa test` and the two tests that give the
    Python copy and the Rego copy the same inputs. A test that needs another engine sets
    `POLICY_ENGINE` itself, which overrides this fixture.
    """
    monkeypatch.setenv("POLICY_ENGINE", "python")
    policy.reset_engine_cache()
    yield
    policy.reset_engine_cache()
