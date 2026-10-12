"""Stage S04-10 Half B (SR-02). The PATH is searched for `opa` once per process.

The tests count calls to shutil.which. They do not time anything. Only the
search is cached. A decision is never cached, and POLICY_ENGINE is read on every
call. If the cached program is gone, the answer fails closed.
"""

import pytest

from apps.api.services import policy


@pytest.fixture(autouse=True)
def clean_engine(monkeypatch):
    monkeypatch.delenv("POLICY_ENGINE", raising=False)
    policy.reset_engine_cache()
    yield
    policy.reset_engine_cache()


class FakeWhich:
    """Stands in for shutil.which. Counts calls. `answer` is the path it returns."""

    def __init__(self, answer):
        self.answer = answer
        self.calls = 0

    def __call__(self, name, *args, **kwargs):
        assert name == "opa"
        self.calls += 1
        return self.answer


def install(monkeypatch, answer):
    fake = FakeWhich(answer)
    monkeypatch.setattr(policy.shutil, "which", fake)
    return fake


def test_many_access_decisions_search_the_path_once(monkeypatch):
    fake = install(monkeypatch, None)
    for _ in range(100):
        assert policy.check_record_read("role.operator")["allow"] is True
        assert policy.check_summarize("role.operator")["allow"] is True
    assert policy.engine_name() == "python"
    assert fake.calls == 1


def test_many_ai_decisions_search_the_path_once(monkeypatch):
    fake = install(monkeypatch, None)
    access = policy.check_summarize("role.operator")
    record = {"device_id": "DEV-00002", "stale_topology_flag": "false"}
    for _ in range(100):
        policy.decide_summarize("role.operator", "DEV-00002", record, access)
    assert fake.calls == 1


def test_the_setting_is_still_read_on_every_call(monkeypatch):
    fake = install(monkeypatch, None)
    assert policy.engine_name() == "python"
    monkeypatch.setenv("POLICY_ENGINE", "opa")
    assert policy.engine_name() == "opa"
    monkeypatch.setenv("POLICY_ENGINE", "python")
    assert policy.engine_name() == "python"
    monkeypatch.setenv("POLICY_ENGINE", "auto")
    assert policy.engine_name() == "python"
    # The forced settings did not search at all. The auto setting searched once.
    assert fake.calls == 1


def test_a_program_found_on_the_path_chooses_opa(monkeypatch):
    fake = install(monkeypatch, "C:/tools/opa.exe")
    assert policy.engine_name() == "opa"
    assert policy.engine_name() == "opa"
    assert fake.calls == 1


def test_reset_searches_again(monkeypatch):
    fake = install(monkeypatch, "C:/tools/opa.exe")
    assert policy.engine_name() == "opa"
    fake.answer = None
    # Still the old answer until a restart or a reset. This is the stated limit.
    assert policy.engine_name() == "opa"
    policy.reset_engine_cache()
    assert policy.engine_name() == "python"
    assert fake.calls == 2


def test_a_cached_program_that_is_gone_fails_closed(monkeypatch):
    install(monkeypatch, "C:/no/such/folder/opa.exe")
    payload = {
        "role": "role.operator",
        "action": "action.read",
        "resource": "resource.device",
        "purpose": "purpose.incident_triage",
        "scope": "scope.all_records",
        "risk": "risk.read_only",
    }
    answer = policy.evaluate_access(payload)
    assert answer["allow"] is False
    assert answer["reasons"] == ["policy_engine_error"]
