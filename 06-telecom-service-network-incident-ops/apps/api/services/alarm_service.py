"""Read one alarm storm. Stage S07 (PRD RQ-08 to RQ-15).

A storm is every row of `alarms.csv` that holds one `storm_batch_id`. This module
reads the file, groups the rows with `dedupe.py`, and returns counts and lists.
It writes nothing. It opens no incident and drops no row (RQ-12).

Counts (all REAL, computed at the request from the file, whose rows are synthetic):
- raw_count      every row with that storm_batch_id.
- deduped_count  the number of different non-blank dedupe_key values among those rows.
- flagged_count  the number of rows that carry a flag word.

A flagged row stays in its list and keeps its flag word. A row with a blank
dedupe_key goes in `held_aside`. Every other row goes in `rows`.

The reply key names are PROPOSED. Owner: Team-Force (RQ-08). The module sets no storm
size and calls no storm large or small (RQ-13).
"""

import csv
from pathlib import Path

from apps.api.services import dedupe

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "synthetic"
ALARMS = "alarms.csv"


def _entry(row: dict, flag: str | None) -> dict:
    return {
        "alarm_id": row.get("alarm_id") or "",
        "device_id": row.get("device_id") or "",
        "dedupe_key": row.get("dedupe_key") or "",
        "flag": flag or "",
    }


def read_storm(storm_batch_id: str) -> dict | None:
    """The storm reply, or None when no alarm row has this storm_batch_id.

    A missing file raises FileNotFoundError. The route turns that into HTTP 500 (RQ-14).
    """
    with (DATA_DIR / ALARMS).open(newline="", encoding="utf-8") as handle:
        matching = [
            row for row in csv.DictReader(handle) if row.get("storm_batch_id") == storm_batch_id
        ]
    if not matching:
        return None

    memory = dedupe.DedupeSet()
    rows, held_aside = [], []
    flagged = 0
    for row in matching:
        # The time check flags a row. It does not remove it from any list.
        flag = dedupe.check_alarm_row(row).flag
        if flag:
            flagged += 1
        # Every row goes through the memory, flagged or not, so a flagged row with a
        # key still counts in deduped_count (RQ-08 and RQ-09).
        verdict = memory.check(dedupe.alarm_key(row))
        if verdict == dedupe.HELD_ASIDE:
            held_aside.append(_entry(row, flag))
        else:
            rows.append(_entry(row, flag))
    totals = memory.totals()
    return {
        "raw_count": len(matching),
        "deduped_count": totals["new"],
        "flagged_count": flagged,
        "rows": rows,
        "held_aside": held_aside,
    }
