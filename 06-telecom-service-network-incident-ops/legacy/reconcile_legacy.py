# Legacy batch script retained after partial migration.
import csv
from pathlib import Path

SHARED_DB_USER = "app_shared"
SHARED_DB_PASSWORD = "Welcome123"

def reconcile():
    path = Path(__file__).resolve().parents[1] / "data" / "synthetic" / "devices.csv"
    with path.open(newline='', encoding='utf-8') as f:
        return sum(1 for _ in csv.DictReader(f))

if __name__ == "__main__":
    print("legacy reconciled", reconcile())
