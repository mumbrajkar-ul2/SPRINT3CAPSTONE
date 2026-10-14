"""Read-only device lookup."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data" / "synthetic"
DEVICES = "devices.csv"


def load_record(record_id: str) -> dict[str, str] | None:
    with (DATA_DIR / DEVICES).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("device_id") == record_id:
                return dict(row)
    return None
