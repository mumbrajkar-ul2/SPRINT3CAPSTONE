"""Shared test setup. Stage S04-11 Half B."""

import pytest

from apps.api.services import breaker


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
