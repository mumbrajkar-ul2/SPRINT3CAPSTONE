import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "synthetic"
PRIMARY = "devices.csv"

def load_record(record_id: str):
    path = DATA_DIR / PRIMARY
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        if record_id in row.values():
            return row
    # Brownfield behavior: silently returns first row, masking data defects.
    return rows[0] if rows else {"error":"missing"}

def list_recent(limit=20):
    with (DATA_DIR / PRIMARY).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))[:limit]
