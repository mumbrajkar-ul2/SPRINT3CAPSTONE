"""COPIED from apps/api/services/dedupe.py in the S08 load fix. The second model did not write this file.
It exists so that tests/reliability/test_drills.py can load. No route of the second app calls it.
Passing tests on this file say nothing about the second model."""

"""Repeat detection and alarm intake checks. Stage S04-11 Half B.

Design: docs/11-reliability/idempotency-plan.md.

Two small helpers. Nothing here reads or writes a data file. A caller passes
rows in.

1. `DedupeSet` says whether a key has been seen. It keeps its memory in this
   process. A restart empties it. A second server process has its own copy.
   Keys the plan names:
   - alarm: (dedupe_key, storm_batch_id)   rule.duplicate_dedupe_key_in_storm_is_one_alarm
   - order: (order_id, retry_count)
   - event: (event_id,)

2. `check_alarm_row` and `alarm_intake` apply the alarm time rule. A row whose
   last_seen_at is before first_seen_at is flagged and does not become an
   incident candidate. The rule id is
   rule.alarm_last_seen_not_before_first_seen. The check compares two
   timestamps. It uses no cutoff.

Open question for S03: the YAML has no rule id for "an event seen twice is one
event" and none for "an order attempt with the same order_id and retry_count is
one attempt". The plan uses the key shapes above until S03 names them.
"""

import threading
from dataclasses import dataclass
from datetime import datetime

NEW = "new"
REPEAT = "repeat"
HELD_ASIDE = "held_aside"

ALARM_TIME_RULE = "rule.alarm_last_seen_not_before_first_seen"

FLAG_LAST_BEFORE_FIRST = "last_seen_before_first_seen"
# Open question for S03: a blank or unreadable timestamp cannot be compared. What
# the YAML wants for it is Unknown. PROPOSED. Owner: Team-Force. Flag it for review.
FLAG_TIMES_UNREADABLE = "times_unreadable"


def _usable(part) -> bool:
    return isinstance(part, str) and part.strip() != ""


class DedupeSet:
    """Remember keys. The first sight of a key is new. Every later sight is a repeat."""

    def __init__(self):
        self._lock = threading.Lock()
        self._repeats: dict[tuple, int] = {}
        self._held_aside = 0
        self._new = 0
        self._repeat_total = 0

    def check(self, key) -> str:
        """Record `key` and return NEW, REPEAT, or HELD_ASIDE.

        `key` is a tuple of strings. A tuple with a blank or missing part is never
        recorded. It is held aside, because it cannot be grouped.
        """
        if not isinstance(key, tuple) or not key or not all(_usable(part) for part in key):
            with self._lock:
                self._held_aside += 1
            return HELD_ASIDE
        normal = tuple(part.strip() for part in key)
        with self._lock:
            if normal in self._repeats:
                self._repeats[normal] += 1
                self._repeat_total += 1
                return REPEAT
            self._repeats[normal] = 0
            self._new += 1
            return NEW

    def repeat_count(self, key) -> int:
        """How many times `key` came back after its first sight. 0 for an unknown key."""
        if not isinstance(key, tuple):
            return 0
        normal = tuple(part.strip() if isinstance(part, str) else part for part in key)
        with self._lock:
            return self._repeats.get(normal, 0)

    def totals(self) -> dict:
        with self._lock:
            return {
                "new": self._new,
                "repeat": self._repeat_total,
                "held_aside": self._held_aside,
            }

    def clear(self) -> None:
        with self._lock:
            self._repeats.clear()
            self._new = 0
            self._repeat_total = 0
            self._held_aside = 0


def alarm_key(row: dict) -> tuple:
    """The alarm key: (dedupe_key, storm_batch_id)."""
    return (row.get("dedupe_key"), row.get("storm_batch_id"))


def order_key(row: dict) -> tuple:
    """The order attempt key: (order_id, retry_count)."""
    return (row.get("order_id"), row.get("retry_count"))


def event_key(event: dict) -> tuple:
    """The event key: (event_id,)."""
    return (event.get("event_id"),)


@dataclass(frozen=True)
class AlarmCheck:
    ok: bool
    flag: str | None
    rule: str | None
    can_become_incident: bool


def check_alarm_row(row: dict) -> AlarmCheck:
    """Compare first_seen_at with last_seen_at on one alarm row.

    Equal times are fine. last_seen_at later than first_seen_at is fine.
    last_seen_at before first_seen_at is flagged. A blank or unreadable time is flagged
    for review. A flagged row does not become an incident on its own.
    """
    try:
        first = datetime.fromisoformat(str(row.get("first_seen_at", "")).strip())
        last = datetime.fromisoformat(str(row.get("last_seen_at", "")).strip())
        before = last < first
    except (ValueError, TypeError):
        # Includes a blank cell and a pair where one time has a zone and the other has none.
        return AlarmCheck(False, FLAG_TIMES_UNREADABLE, None, False)
    if before:
        return AlarmCheck(False, FLAG_LAST_BEFORE_FIRST, ALARM_TIME_RULE, False)
    return AlarmCheck(True, None, None, True)


def alarm_intake(rows, seen: DedupeSet | None = None) -> dict:
    """Sort alarm rows into incident candidates, flagged rows, repeats, and held-aside rows.

    Order of checks for each row:
    1. The time check. A flagged row is listed in `flagged` and goes no further. It is not
       entered in the repeat memory, so a good row with the same key can still be first.
    2. The key check. A repeat is counted. A row with a blank key part is held aside.
    3. Anything left is a candidate. A candidate is not an incident. It is a row that a
       later step may turn into one.
    """
    seen = seen if seen is not None else DedupeSet()
    candidates, flagged, repeats, held_aside = [], [], [], []
    for row in rows:
        verdict = check_alarm_row(row)
        if not verdict.ok:
            flagged.append((row, verdict))
            continue
        outcome = seen.check(alarm_key(row))
        if outcome == NEW:
            candidates.append(row)
        elif outcome == REPEAT:
            repeats.append(row)
        else:
            held_aside.append(row)
    return {
        "candidates": candidates,
        "flagged": flagged,
        "repeats": repeats,
        "held_aside": held_aside,
    }
