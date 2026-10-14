"""In-memory limits for the local model path."""

from __future__ import annotations

import threading
import time

FAILURE_LIMIT = 5
OPEN_SECONDS = 30.0
IN_FLIGHT_LIMIT = 10

_lock = threading.Lock()
_failures = 0
_opened_at: float | None = None
_half_open_running = False
_slots = threading.BoundedSemaphore(IN_FLIGHT_LIMIT)


def reset() -> None:
    global _failures, _opened_at, _half_open_running, _slots
    with _lock:
        _failures = 0
        _opened_at = None
        _half_open_running = False
        _slots = threading.BoundedSemaphore(IN_FLIGHT_LIMIT)


def begin() -> bool:
    global _opened_at, _half_open_running
    with _lock:
        if _opened_at is not None:
            if time.monotonic() - _opened_at < OPEN_SECONDS:
                return False
            if _half_open_running:
                return False
            _half_open_running = True
    if not _slots.acquire(blocking=False):
        with _lock:
            _half_open_running = False
        return False
    return True


def finish(success: bool) -> None:
    global _failures, _opened_at, _half_open_running
    _slots.release()
    with _lock:
        _half_open_running = False
        if success:
            _failures = 0
            _opened_at = None
            return
        _failures += 1
        if _failures >= FAILURE_LIMIT:
            _opened_at = time.monotonic()
