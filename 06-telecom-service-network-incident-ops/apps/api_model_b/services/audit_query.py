"""Read one correlation chain from the append-only audit log."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import audit

MAX_ID_LENGTH = 128
WITHHELD = "withheld_text"
FORBIDDEN_NAMES = (
    "mgmt_ip",
    "credential_profile",
    "SHARED_DB_PASSWORD",
    "SHARED_DB_USER",
    "DATABASE_URL",
    "AI_GATEWAY_KEY",
    "LEGACY_BATCH_PASSWORD",
    "OT_VENDOR_TOKEN",
)


@dataclass
class CaseRead:
    rows: list[dict[str, Any]]
    rows_before_correlation_id: int = 0
    unreadable_lines: int = 0
    withheld_text: int = 0


def _unsafe(value: Any) -> bool:
    return isinstance(value, str) and any(name in value for name in FORBIDDEN_NAMES)


def _clean(value: Any) -> tuple[Any, int]:
    if _unsafe(value):
        return WITHHELD, 1
    if isinstance(value, dict):
        output: dict[str, Any] = {}
        count = 0
        for key, item in value.items():
            if _unsafe(key):
                count += 1
                continue
            output[key], added = _clean(item)
            count += added
        return output, count
    if isinstance(value, list):
        output = []
        count = 0
        for item in value:
            cleaned, added = _clean(item)
            output.append(cleaned)
            count += added
        return output, count
    return value, 0


def read_case(correlation_id: str) -> CaseRead:
    stored, unreadable = audit.read_lines()
    old = sum(1 for row in stored if not row.get("correlation_id"))
    selected = [row for row in stored if row.get("correlation_id") == correlation_id]
    selected.sort(key=lambda row: str(row.get("ts") or ""))
    cleaned, withheld = _clean(selected)
    return CaseRead(
        rows=cleaned,
        rows_before_correlation_id=old,
        unreadable_lines=unreadable,
        withheld_text=withheld,
    )


def cannot_prove(case: CaseRead) -> list[dict[str, str]]:
    items: list[tuple[str, str]] = [
        ("final_action", "status.code.cannot_prove.final_action"),
        ("record_asked_for", "status.code.cannot_prove.record_asked_for"),
        ("policy_reasons_and_version", "status.code.cannot_prove.policy_reasons_and_version"),
        ("caller_identity", "status.code.cannot_prove.caller_identity"),
        ("case_membership", "status.code.cannot_prove.case_membership"),
        ("log_integrity", "status.code.cannot_prove.log_integrity"),
    ]
    for field in ("approval_id", "policy_decision", "model", "actor"):
        if not case.rows or any(row.get(field) is None for row in case.rows):
            items.append((field, f"status.code.cannot_prove.{field}"))
    if case.rows_before_correlation_id:
        items.append(
            (
                "rows_before_correlation_id",
                f"{case.rows_before_correlation_id} line(s): status.code.cannot_prove.rows_before_correlation_id",
            )
        )
    if case.unreadable_lines:
        items.append(
            (
                "unreadable_lines",
                f"{case.unreadable_lines} line(s): status.code.cannot_prove.unreadable_lines",
            )
        )
    if case.withheld_text:
        items.append(("withheld_text", "status.code.cannot_prove.withheld_text"))
    return [{"item": item, "reason": reason} for item, reason in items]
