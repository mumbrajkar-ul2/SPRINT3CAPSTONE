"""Read one case back from the audit log. Stage S05-14 Half B.

A case is every row that shares one `correlation_id`. This module reads
`audit.LOG`, picks the rows for one id, and puts them in time order.

Read only. Nothing here opens the log for writing, and nothing changes a row.

Rules
- A row with no `correlation_id` is never returned. The 96 old three-key lines
  are in that group (docs/14-audit/audit-gap-report.md, AG-01).
- Order is by `ts`. Two rows with the same `ts` keep their order in the file.
- A line that is not a JSON object is counted and skipped. It is never returned.
- The text of a row is checked before it leaves. A value that holds a forbidden
  field name or a credential name is replaced. The log file is not changed.

`cannot_prove` is computed from the rows. Some items come from a null field.
Some are always listed, because the log cannot prove them
(docs/14-audit/decision-provenance-model.md, group 9). The item names are
PROPOSED plain names. Open question for S03: the YAML has no id for an item on
the "cannot be proven" list.
"""

import json
import re
from dataclasses import dataclass, field

from apps.api.services import ai_gateway, audit

# PROPOSED. Owner: Team-Force. Accepted for S05-14 Half B on 2026-10-12.
# The limit applies to the id in the path of GET /audit/{correlation_id}.
MAX_ID_LENGTH = audit.MAX_CORRELATION_ID_LENGTH

# S07 (PRD RQ-34). The action word of the row that proves a recommendation was shown with text.
RECOMMENDATION_SHOWN_ACTION = "ai.recommendation"

WITHHELD = "<withheld: forbidden name>"

# The same names the prompt check uses: mgmt_ip, credential_profile, customer_id,
# and the six credential names in ai-context-policy.yaml.
_FORBIDDEN = [
    re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])", re.IGNORECASE)
    for name in ai_gateway.FORBIDDEN_LABELS
]


@dataclass
class CaseRead:
    """What one read of the log found."""

    rows: list = field(default_factory=list)
    lines_read: int = 0
    lines_without_id: int = 0
    unreadable_lines: int = 0
    withheld_values: int = 0


def _holds_forbidden_name(text: str) -> bool:
    return any(pattern.search(text) for pattern in _FORBIDDEN)


def withhold_forbidden(value):
    """Return (value, count). A string with a forbidden name becomes WITHHELD."""
    if isinstance(value, str) and _holds_forbidden_name(value):
        return WITHHELD, 1
    return value, 0


def read_case(correlation_id: str) -> CaseRead:
    """Every row for `correlation_id`, in time order. An empty id matches nothing."""
    result = CaseRead()
    if not isinstance(correlation_id, str) or correlation_id == "":
        return result
    found = []
    path = audit.LOG
    if not path.exists():
        return result
    with path.open("r", encoding="utf-8") as handle:
        for position, line in enumerate(handle):
            if not line.strip():
                continue
            result.lines_read += 1
            try:
                row = json.loads(line)
            except ValueError:
                result.unreadable_lines += 1
                continue
            if not isinstance(row, dict):
                result.unreadable_lines += 1
                continue
            row_id = row.get("correlation_id")
            if not isinstance(row_id, str) or row_id == "":
                result.lines_without_id += 1
                continue
            if row_id == correlation_id:
                found.append((str(row.get("ts", "")), position, row))
    found.sort(key=lambda item: (item[0], item[1]))
    for _, _, row in found:
        clean = {}
        for key, value in row.items():
            clean[key], count = withhold_forbidden(value)
            result.withheld_values += count
        result.rows.append(clean)
    return result


def recommendation_was_shown(correlation_id: str, record_id: str) -> bool:
    """True when the log holds, under this correlation id, one row with the action
    `ai.recommendation` whose `record_id` equals `record_id` (PRD RQ-34).

    That row is written only when the recommend route returned text. Read only.
    """
    if not isinstance(correlation_id, str) or not correlation_id:
        return False
    if not isinstance(record_id, str) or not record_id:
        return False
    path = audit.LOG
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if (
                isinstance(row, dict)
                and row.get("correlation_id") == correlation_id
                and row.get("action") == RECOMMENDATION_SHOWN_ACTION
                and row.get("record_id") == record_id
            ):
                return True
    return False


def _item(name: str, reason: str) -> dict:
    return {"item": name, "reason": reason}


def cannot_prove(case: CaseRead) -> list:
    """What these rows cannot prove. Computed from null fields and fixed facts."""
    rows = case.rows
    items = []
    if rows and all(row.get("approval_id") is None for row in rows):
        items.append(
            _item(
                "approval_id",
                "approval_id is null on every row. No yes was stored in this case. A no also leaves it null.",
            )
        )
    if rows and all(row.get("policy_decision") is None for row in rows):
        items.append(
            _item(
                "policy_decision",
                "policy_decision is null on every row. The action word and outcome are the only trace of the policy result.",
            )
        )
    if rows and all(row.get("model") is None for row in rows):
        items.append(_item("model", "No row shows a model call. A call that stopped before the model has no hash."))
    if any(row.get("actor") is None for row in rows):
        items.append(_item("actor", "At least one row has no actor. The role has no persona, or the header was missing."))
    items.extend(
        [
            _item(
                "final_action",
                "final_action is none on every row, because no route in this app changes a device. The log cannot show a change made outside this app.",
            ),
            _item(
                "record_asked_for",
                "record_id is null on a row that names no device, such as a storm read or an audit read. For other rows it holds the id as the caller typed it.",
            ),
            _item("policy_reasons_and_version", "The reasons and the policy version are not stored on any row."),
            _item("caller_identity", "The role is a header word the caller typed. Nothing proves who the caller was."),
            _item(
                "case_membership",
                "The caller chose the correlation_id. A second caller can reuse it and add a row to this case.",
            ),
            _item(
                "log_integrity",
                "The log is a plain file. A line can be changed or deleted. This route cannot prove the case is complete or unchanged.",
            ),
            _item(
                "rows_before_correlation_id",
                f"{case.lines_without_id} line(s) in the log have no correlation_id and can never be returned here.",
            ),
        ]
    )
    if case.unreadable_lines:
        items.append(
            _item("unreadable_lines", f"{case.unreadable_lines} line(s) in the log could not be read and were skipped.")
        )
    if case.withheld_values:
        items.append(
            _item(
                "withheld_text",
                f"{case.withheld_values} value(s) held a forbidden field name or credential name and were replaced.",
            )
        )
    return items
