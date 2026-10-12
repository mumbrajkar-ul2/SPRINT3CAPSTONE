"""Circuit breaker, in-flight limit, and audit write lock. Stage S04-11 Half B.

Design: docs/11-reliability/retry-and-circuit-breaker-strategy.md. Every number
the breaker uses is PROPOSED. Owner: Team-Force. The tests set their own small
numbers. One test checks the defaults.
"""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import ai_gateway, audit, breaker

OPERATOR = {"X-User-Role": "operator"}
GOOD_ID = "DEV-00002"


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def make(threshold=3, open_seconds=30.0, in_flight=10):
    clock = FakeClock()
    return breaker.CircuitBreaker(threshold, open_seconds, in_flight, clock=clock), clock


# ---------------------------------------------------------------------------
# The breaker on its own
# ---------------------------------------------------------------------------


def test_it_opens_after_the_threshold_of_failures_in_a_row():
    b, _ = make(threshold=3)
    for _ in range(2):
        b.admit().failed()
    assert b.snapshot()["state"] == breaker.CLOSED
    b.admit().failed()
    assert b.snapshot()["state"] == breaker.OPEN
    with pytest.raises(breaker.BreakerRefused) as refused:
        b.admit()
    assert refused.value.reason == breaker.REFUSED_OPEN


def test_a_success_resets_the_count():
    b, _ = make(threshold=3)
    b.admit().failed()
    b.admit().failed()
    b.admit().ok()
    assert b.snapshot()["failures_in_a_row"] == 0
    b.admit().failed()
    b.admit().failed()
    assert b.snapshot()["state"] == breaker.CLOSED


def test_a_refused_answer_is_neutral_it_neither_counts_nor_resets():
    b, _ = make(threshold=2)
    b.admit().failed()
    b.admit().neutral()
    assert b.snapshot()["failures_in_a_row"] == 1
    b.admit().failed()
    assert b.snapshot()["state"] == breaker.OPEN


def test_it_half_opens_after_the_open_time_and_lets_one_test_call_through():
    b, clock = make(threshold=1, open_seconds=30)
    b.admit().failed()
    clock.advance(29.9)
    with pytest.raises(breaker.BreakerRefused):
        b.admit()
    clock.advance(0.2)
    assert b.snapshot()["state"] == breaker.HALF_OPEN
    probe = b.admit()
    with pytest.raises(breaker.BreakerRefused):
        b.admit()
    probe.ok()
    assert b.snapshot()["state"] == breaker.CLOSED
    b.admit().ok()


def test_a_failed_test_call_opens_it_again_for_the_full_time():
    b, clock = make(threshold=1, open_seconds=30)
    b.admit().failed()
    clock.advance(31)
    b.admit().failed()
    assert b.snapshot()["state"] == breaker.OPEN
    clock.advance(29)
    with pytest.raises(breaker.BreakerRefused):
        b.admit()
    clock.advance(2)
    assert b.snapshot()["state"] == breaker.HALF_OPEN


def test_a_neutral_test_call_frees_the_probe_slot_and_stays_half_open():
    b, clock = make(threshold=1, open_seconds=30)
    b.admit().failed()
    clock.advance(31)
    b.admit().neutral()
    assert b.snapshot()["state"] == breaker.HALF_OPEN
    b.admit()  # another test call may go


def test_the_in_flight_limit_refuses_without_waiting_and_frees_on_finish():
    b, _ = make(in_flight=2)
    one, two = b.admit(), b.admit()
    with pytest.raises(breaker.BreakerRefused) as refused:
        b.admit()
    assert refused.value.reason == breaker.REFUSED_IN_FLIGHT
    one.ok()
    b.admit()
    two.neutral()


def test_a_ticket_reports_once():
    b, _ = make(threshold=2)
    ticket = b.admit()
    ticket.failed()
    ticket.failed()
    ticket.ok()
    assert b.snapshot() == {"state": breaker.CLOSED, "failures_in_a_row": 1, "in_flight": 0}


def test_many_threads_never_go_past_the_in_flight_limit():
    b, _ = make(in_flight=3)
    peak = {"now": 0, "max": 0}
    lock = threading.Lock()

    def worker(_):
        try:
            ticket = b.admit()
        except breaker.BreakerRefused:
            return
        with lock:
            peak["now"] += 1
            peak["max"] = max(peak["max"], peak["now"])
        time.sleep(0.02)
        with lock:
            peak["now"] -= 1
        ticket.ok()

    with ThreadPoolExecutor(max_workers=20) as pool:
        list(pool.map(worker, range(200)))
    assert 1 <= peak["max"] <= 3
    assert b.snapshot()["in_flight"] == 0


def test_the_proposed_defaults_and_the_environment_names(monkeypatch):
    # PROPOSED. Owner: Team-Force.
    assert (
        breaker.DEFAULT_FAILURE_THRESHOLD,
        breaker.DEFAULT_OPEN_SECONDS,
        breaker.DEFAULT_MAX_IN_FLIGHT,
    ) == (5, 30.0, 10)
    built = breaker.CircuitBreaker()
    assert (built.failure_threshold, built.open_seconds, built.max_in_flight) == (5, 30.0, 10)
    monkeypatch.setenv(breaker.THRESHOLD_ENV, "2")
    monkeypatch.setenv(breaker.OPEN_SECONDS_ENV, "1.5")
    monkeypatch.setenv(breaker.MAX_IN_FLIGHT_ENV, "4")
    built = breaker.CircuitBreaker()
    assert (built.failure_threshold, built.open_seconds, built.max_in_flight) == (2, 1.5, 4)


@pytest.mark.parametrize("bad", ["", "abc", "0", "-3", "nan", "inf", "2.5"])
def test_a_bad_setting_gives_the_default(monkeypatch, bad):
    for name in (breaker.THRESHOLD_ENV, breaker.OPEN_SECONDS_ENV, breaker.MAX_IN_FLIGHT_ENV):
        monkeypatch.setenv(name, bad)
    built = breaker.CircuitBreaker()
    # "2.5" is a fine number of seconds. It is not a whole number for the two counts.
    expected_seconds = 2.5 if bad == "2.5" else 30.0
    assert (built.failure_threshold, built.open_seconds, built.max_in_flight) == (
        5,
        expected_seconds,
        10,
    )


# ---------------------------------------------------------------------------
# The breaker on the summary route
# ---------------------------------------------------------------------------


@pytest.fixture
def audit_rows(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)

    def read():
        if not path.exists():
            return []
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

    return read


class Model:
    def __init__(self, sleep=0.0, error=None):
        self.calls = 0
        self.sleep = sleep
        self.error = error
        self._lock = threading.Lock()

    def __call__(self, prompt):
        with self._lock:
            self.calls += 1
        if self.sleep:
            time.sleep(self.sleep)
        if self.error is not None:
            raise self.error
        return json.dumps(
            {
                "record_id": GOOD_ID,
                "summary": "SIMULATED breaker summary",
                "recommendation": "Review and approve before action",
                "outcome": "RECOMMEND_ONLY",
                "source_count": 1,
            }
        )


def test_route_the_model_is_not_called_once_the_breaker_is_open(monkeypatch, audit_rows):
    monkeypatch.setenv(breaker.THRESHOLD_ENV, "2")
    monkeypatch.setenv(ai_gateway.TIMEOUT_ENV, "0.05")
    model = Model(sleep=0.3)
    monkeypatch.setattr(ai_gateway, "call_model", model)
    client = TestClient(app)
    for _ in range(2):
        assert client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR).status_code == 202
    assert model.calls == 2
    assert breaker.get_breaker().snapshot()["state"] == breaker.OPEN

    started = time.perf_counter()
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    elapsed = time.perf_counter() - started
    body = response.json()
    assert model.calls == 2  # no new call
    assert elapsed < 0.2  # answered at once, not after the deadline
    assert response.status_code == 202
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["summary"] is None and body["recommendation"] is None
    assert body["model"] is None and body["prompt_hash"] is None and body["latency_ms"] is None
    assert client.get("/health").status_code == 200
    assert client.get(f"/records/{GOOD_ID}", headers=OPERATOR).status_code == 200
    last_hold = [row for row in audit_rows() if row["action"] == "policy.hold"][-1]
    assert last_hold["outcome"] == "HOLD_FOR_REVIEW"
    assert last_hold["model"] is None and last_hold["latency_ms"] is None


def test_route_a_test_call_after_the_open_time_closes_the_breaker(monkeypatch, audit_rows):
    monkeypatch.setenv(breaker.THRESHOLD_ENV, "1")
    monkeypatch.setenv(breaker.OPEN_SECONDS_ENV, "0.2")
    client = TestClient(app)

    def broken(prompt):
        raise ConnectionRefusedError("refused")

    monkeypatch.setattr(ai_gateway, "call_model", broken)
    assert client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR).status_code == 202
    assert breaker.get_breaker().snapshot()["state"] == breaker.OPEN

    time.sleep(0.3)
    model = Model()
    monkeypatch.setattr(ai_gateway, "call_model", model)
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 200
    assert response.json()["outcome"] == "RECOMMEND_ONLY"
    assert model.calls == 1
    assert breaker.get_breaker().snapshot()["state"] == breaker.CLOSED


def test_route_a_bad_answer_does_not_open_the_breaker(monkeypatch, audit_rows):
    monkeypatch.setenv(breaker.THRESHOLD_ENV, "2")
    monkeypatch.setattr(ai_gateway, "call_model", lambda prompt: "not json")
    client = TestClient(app)
    for _ in range(4):
        assert client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR).status_code == 202
    assert breaker.get_breaker().snapshot()["state"] == breaker.CLOSED


def test_route_a_hung_model_does_not_hold_every_route_thread(monkeypatch, audit_rows):
    """The in-flight limit. 50 summaries arrive at once and the model hangs for 2 seconds.

    The route has 40 threads. With the limit of 10, only 10 calls reach the model. The other
    40 are held at once. /health and /records answer fast. Without the limit the same
    request pattern made /health wait about 0.8 seconds (docs/11-reliability/probe-output.json,
    check P5, 1.5 second deadline). The numbers here are the test's own.
    """
    monkeypatch.setenv(breaker.THRESHOLD_ENV, "1000")  # keep the breaker out of this test
    monkeypatch.setenv(breaker.MAX_IN_FLIGHT_ENV, "10")
    monkeypatch.setenv(ai_gateway.TIMEOUT_ENV, "5")
    model = Model(sleep=2.0)
    monkeypatch.setattr(ai_gateway, "call_model", model)

    results = []
    with TestClient(app) as shared:
        pool = ThreadPoolExecutor(max_workers=60)
        futures = [
            pool.submit(lambda: shared.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR))
            for _ in range(50)
        ]
        time.sleep(0.5)  # the 40 refused calls have returned. The 10 admitted calls still wait.
        timings = []
        for path, headers in (("/health", {}), (f"/records/{GOOD_ID}", OPERATOR)):
            started = time.perf_counter()
            status = shared.get(path, headers=headers).status_code
            timings.append((status, time.perf_counter() - started))
        results = [future.result() for future in futures]
        pool.shutdown()

    assert all(status == 200 for status, _ in timings)
    assert all(elapsed < 0.5 for _, elapsed in timings), timings
    assert model.calls == 10
    codes = sorted(response.status_code for response in results)
    assert codes == [200] * 10 + [202] * 40
    refused = [r.json() for r in results if r.status_code == 202]
    assert all(body["summary"] is None for body in refused)


# ---------------------------------------------------------------------------
# The audit write lock (decision D-3)
# ---------------------------------------------------------------------------


def test_eight_threads_writing_the_audit_log_lose_no_row(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)

    def writer(n):
        for i in range(250):
            audit.write_event(
                "probe.write",
                correlation_id=f"c-{n}-{i}",
                actor=None,
                role="operator",
                resource="resource.device",
            )

    for _ in range(3):
        path.write_text("", encoding="utf-8")
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(writer, range(8)))
        lines = path.read_text(encoding="utf-8").splitlines()
        ids = {json.loads(line)["correlation_id"] for line in lines}  # every line must parse
        assert len(lines) == 2000
        assert len(ids) == 2000
