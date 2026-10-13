"""The approvals record. Stage S07 (PRD RQ-32 to RQ-39).

`POST /approvals/{id}` is the only route that stores new state. It stores one
record for each decision, in an append-only JSON Lines file. The file is not a CSV
and it is not a data file the app reads (PRD section 8). The route writes its
audit row first and calls `store` second (RQ-36).

One record holds five keys: `approval_id`, `decision`, `approver`, `record_id` and
`correlation_id`. `approval_id` is null for a no. A second call for the same device
and correlation id stores a second record. Nothing is overwritten.

The approval id is made here, on the server. No caller sends one (RQ-38).
No code here changes a device, a circuit, an incident or an alarm (RQ-39).
"""

import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

STORE = Path(__file__).resolve().parents[3] / "logs" / "approvals.jsonl"

_LOCK = threading.Lock()

DECISIONS = ("yes", "no")

# The text that starts every server-made approval id. PROPOSED. Owner: Team-Force.
APPROVAL_ID_PREFIX = "APR-"


def new_approval_id() -> str:
    """A server-made id for a yes. A no gets none."""
    return APPROVAL_ID_PREFIX + str(uuid.uuid4())


def build_record(*, decision: str, approver: str, record_id: str, correlation_id: str, approval_id) -> dict:
    return {
        "approval_id": approval_id if decision == "yes" else None,
        "decision": decision,
        "approver": approver,
        "record_id": record_id,
        "correlation_id": correlation_id,
    }


def store(record: dict) -> None:
    """Append one record. A failure raises and the route returns HTTP 500."""
    line = json.dumps({"ts": datetime.utcnow().isoformat(), **record}) + "\n"
    with _LOCK:
        STORE.parent.mkdir(exist_ok=True)
        with STORE.open("a", encoding="utf-8") as handle:
            handle.write(line)


def read_all() -> list[dict]:
    """Every stored record, in file order. Used by tests and by the demo evidence."""
    if not STORE.exists():
        return []
    with STORE.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
