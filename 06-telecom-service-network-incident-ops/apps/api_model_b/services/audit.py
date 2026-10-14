"""Append-only audit rows defined by semantic-layer/entities.yaml."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
LOG = ROOT / "logs" / "audit.log"

SCHEMA_KEYS = (
    "ts",
    "correlation_id",
    "actor",
    "role",
    "action",
    "resource",
    "policy_decision",
    "approval_id",
    "model",
    "model_version",
    "prompt_hash",
    "tokens",
    "latency_ms",
    "outcome",
    "token_estimate_method",
    "record_id",
    "final_action",
)

ROLE_TO_ACTOR = {
    "operator": "noc_operator",
    "engineer": "network_engineer",
    "ai_agent": "ai_agent",
}


def actor_for(role: str | None) -> str | None:
    return ROLE_TO_ACTOR.get(role)


def write_event(
    action: str,
    *,
    correlation_id: str,
    role: str | None,
    resource: str,
    **values: Any,
) -> dict[str, Any]:
    row: dict[str, Any] = {key: None for key in SCHEMA_KEYS}
    row.update(
        ts=datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        correlation_id=correlation_id,
        actor=actor_for(role),
        role=role,
        action=action,
        resource=resource,
        final_action="none",
    )
    for key, value in values.items():
        if key in row:
            row[key] = value
    # S08 load fix. A row with no token count carries no method word.
    if row["tokens"] is None:
        row["token_estimate_method"] = None
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, separators=(",", ":")) + "\n")
    return row


def read_lines() -> tuple[list[dict[str, Any]], int]:
    if not LOG.exists():
        return [], 0
    rows: list[dict[str, Any]] = []
    unreadable = 0
    with LOG.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                unreadable += 1
                continue
            if isinstance(value, dict):
                rows.append(value)
            else:
                unreadable += 1
    return rows, unreadable
