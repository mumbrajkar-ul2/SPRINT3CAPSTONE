"""Read and analyse one alarm storm without changing the source file."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "synthetic"
ALARMS = "alarms.csv"


def _flag(row: dict[str, str]) -> str:
    try:
        first = datetime.fromisoformat(row.get("first_seen_at", ""))
        last = datetime.fromisoformat(row.get("last_seen_at", ""))
    except (TypeError, ValueError):
        return "times_unreadable"
    return "last_seen_before_first_seen" if last < first else ""


def read_storm(storm_batch_id: str) -> dict | None:
    with (DATA_DIR / ALARMS).open(newline="", encoding="utf-8") as handle:
        matches = [
            dict(row)
            for row in csv.DictReader(handle)
            if row.get("storm_batch_id") == storm_batch_id
        ]
    if not matches:
        return None

    rows: list[dict[str, str]] = []
    held_aside: list[dict[str, str]] = []
    dedupe_keys: set[str] = set()
    flagged_count = 0
    for source in matches:
        flag = _flag(source)
        if flag:
            flagged_count += 1
        item = {
            "alarm_id": source.get("alarm_id", ""),
            "device_id": source.get("device_id", ""),
            "dedupe_key": source.get("dedupe_key", ""),
            "flag": flag,
        }
        key = item["dedupe_key"].strip()
        if key:
            rows.append(item)
            dedupe_keys.add(key)
        else:
            held_aside.append(item)
    return {
        "raw_count": len(matches),
        "deduped_count": len(dedupe_keys),
        "flagged_count": flagged_count,
        "rows": rows,
        "held_aside": held_aside,
    }
