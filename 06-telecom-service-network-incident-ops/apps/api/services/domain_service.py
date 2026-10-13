import csv
import threading
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "synthetic"
PRIMARY = "devices.csv"

# Stage S04-10 Half B (SR-01). The file is read once, at the first call, and the
# rows are indexed by device_id. The cache lasts until the app restarts or
# reset_cache() is called. Owner of the refresh rule for production: Team-Force.
# The repo has no writer for devices.csv, so nothing changes it while the app runs.
_lock = threading.Lock()
_state = None  # (rows, index) once loaded


def _load():
    """Read devices.csv once. Return (rows, index). The index keeps the first row of a repeated id."""
    global _state
    state = _state
    if state is not None:
        return state
    with _lock:
        if _state is None:
            with (DATA_DIR / PRIMARY).open(newline='', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            index = {}
            for row in rows:
                index.setdefault(row.get("device_id"), row)
            _state = (rows, index)
        return _state


def reset_cache():
    """Forget the loaded rows. The next call reads the file again. Tests use this."""
    global _state
    with _lock:
        _state = None


def load_record(record_id: str):
    """The device row whose device_id equals `record_id`, or None when there is none.

    S07 (PRD RQ-03). The old behaviour returned the first row for a missing id. That
    masked data defects (defect F01). The routes now turn None into HTTP 404 or BLOCK.
    """
    _rows, index = _load()
    row = index.get(record_id)
    if row is not None:
        # A copy, so a caller that edits the result cannot change the stored row.
        return dict(row)
    return None

def list_recent(limit=20):
    with (DATA_DIR / PRIMARY).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))[:limit]
