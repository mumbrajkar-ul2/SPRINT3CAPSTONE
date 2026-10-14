"""Append-only approval records."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

STORE = Path(__file__).resolve().parents[1] / "runtime" / "approvals.jsonl"
APPROVAL_ID_PREFIX = "APR-"


def make_id() -> str:
    return APPROVAL_ID_PREFIX + str(uuid.uuid4())


def append(record: dict[str, Any]) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    with STORE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, separators=(",", ":")) + "\n")


def read_all() -> list[dict[str, Any]]:
    if not STORE.exists():
        return []
    rows = []
    with STORE.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows
