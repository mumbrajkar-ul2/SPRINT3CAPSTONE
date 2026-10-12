"""Circuit breaker and in-flight limit for the model call. Stage S04-11 Half B.

Design: docs/11-reliability/retry-and-circuit-breaker-strategy.md.

A circuit breaker stops calls to a failing service for a short time. It then
lets one test call through. This one also limits how many model calls run at
the same time, so a hung model cannot hold every route thread.

States.
- closed: calls go to the model. Failures in a row are counted.
- open: no call goes to the model. After `open_seconds` the state is half open.
- half open: one test call goes to the model. Other requests are refused. A
  success closes the breaker. A failure opens it again.

What counts. The caller reports one result for each admitted call:
- `ticket.failed()`  the call hit the deadline or raised an error.
- `ticket.ok()`      the model gave a schema-valid answer.
- `ticket.neutral()` the model answered but the answer was refused. No count.

Every number is PROPOSED. Owner: Team-Force. Each one is read from the
environment through `apps/api/settings.py`:

    BREAKER_FAILURE_THRESHOLD  failures in a row that open the breaker. Default 5.
    BREAKER_OPEN_SECONDS       seconds the breaker stays open. Default 30.
    MODEL_MAX_IN_FLIGHT        model calls running at once. Default 10.

State lives in this process. A restart closes the breaker. Two server
processes have two breakers.
"""

import threading
import time

from apps.api import settings

# PROPOSED. Owner: Team-Force. Design choices, not measurements.
DEFAULT_FAILURE_THRESHOLD = 5
DEFAULT_OPEN_SECONDS = 30.0
DEFAULT_MAX_IN_FLIGHT = 10

THRESHOLD_ENV = "BREAKER_FAILURE_THRESHOLD"
OPEN_SECONDS_ENV = "BREAKER_OPEN_SECONDS"
MAX_IN_FLIGHT_ENV = "MODEL_MAX_IN_FLIGHT"

CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half_open"

# Why a request was refused.
REFUSED_OPEN = "breaker_open"
REFUSED_IN_FLIGHT = "in_flight_limit"


class BreakerRefused(Exception):
    """The model call must not start. `reason` is one of the two words above."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class Ticket:
    """One admitted call. Report one result. A second report is ignored."""

    def __init__(self, breaker: "CircuitBreaker", probe: bool):
        self._breaker = breaker
        self._probe = probe
        self._done = False

    def _finish(self, result: str) -> None:
        if self._done:
            return
        self._done = True
        self._breaker._finish(result, self._probe)

    def ok(self) -> None:
        self._finish("ok")

    def failed(self) -> None:
        self._finish("failed")

    def neutral(self) -> None:
        self._finish("neutral")


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int | None = None,
        open_seconds: float | None = None,
        max_in_flight: int | None = None,
        clock=time.monotonic,
    ):
        self.failure_threshold = (
            settings.positive_int(THRESHOLD_ENV, DEFAULT_FAILURE_THRESHOLD)
            if failure_threshold is None
            else failure_threshold
        )
        self.open_seconds = (
            settings.positive_number(OPEN_SECONDS_ENV, DEFAULT_OPEN_SECONDS)
            if open_seconds is None
            else open_seconds
        )
        self.max_in_flight = (
            settings.positive_int(MAX_IN_FLIGHT_ENV, DEFAULT_MAX_IN_FLIGHT)
            if max_in_flight is None
            else max_in_flight
        )
        self._clock = clock
        self._lock = threading.Lock()
        self._state = CLOSED
        self._failures = 0
        self._opened_at = 0.0
        self._in_flight = 0
        self._probe_running = False

    # -- reading --------------------------------------------------------

    def snapshot(self) -> dict:
        with self._lock:
            self._maybe_half_open()
            return {
                "state": self._state,
                "failures_in_a_row": self._failures,
                "in_flight": self._in_flight,
            }

    # -- admitting a call -----------------------------------------------

    def admit(self) -> Ticket:
        """Return a ticket, or raise BreakerRefused. The caller never waits."""
        with self._lock:
            self._maybe_half_open()
            if self._state == OPEN:
                raise BreakerRefused(REFUSED_OPEN)
            if self._state == HALF_OPEN and self._probe_running:
                raise BreakerRefused(REFUSED_OPEN)
            if self._in_flight >= self.max_in_flight:
                raise BreakerRefused(REFUSED_IN_FLIGHT)
            probe = self._state == HALF_OPEN
            if probe:
                self._probe_running = True
            self._in_flight += 1
            return Ticket(self, probe)

    # -- inside the lock ------------------------------------------------

    def _maybe_half_open(self) -> None:
        if self._state == OPEN and self._clock() - self._opened_at >= self.open_seconds:
            self._state = HALF_OPEN
            self._probe_running = False

    def _open(self) -> None:
        self._state = OPEN
        self._opened_at = self._clock()
        self._probe_running = False

    def _finish(self, result: str, probe: bool) -> None:
        with self._lock:
            self._in_flight = max(0, self._in_flight - 1)
            if probe:
                self._probe_running = False
            if result == "failed":
                self._failures += 1
                if self._state == HALF_OPEN and probe:
                    self._open()
                elif self._state == CLOSED and self._failures >= self.failure_threshold:
                    self._open()
            elif result == "ok":
                self._failures = 0
                if self._state == HALF_OPEN and probe:
                    self._state = CLOSED
            # "neutral": no count, no reset. A half-open probe slot is freed above.


_breaker: CircuitBreaker | None = None
_breaker_lock = threading.Lock()


def get_breaker() -> CircuitBreaker:
    """The one breaker for this process. Built on first use from the environment."""
    global _breaker
    with _breaker_lock:
        if _breaker is None:
            _breaker = CircuitBreaker()
        return _breaker


def reset() -> None:
    """Forget the breaker. The next call builds a new one and reads the environment again."""
    global _breaker
    with _breaker_lock:
        _breaker = None
