# Legacy batch script retained after partial migration.
import csv
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from apps.api.settings import require

SHARED_DB_USER = "app_shared"


def reconcile():
    require("SHARED_DB_PASSWORD")
    path = Path(__file__).resolve().parents[1] / "data" / "synthetic" / "devices.csv"
    with path.open(newline='', encoding='utf-8') as f:
        return sum(1 for _ in csv.DictReader(f))

if __name__ == "__main__":
    print("legacy reconciled", reconcile())
