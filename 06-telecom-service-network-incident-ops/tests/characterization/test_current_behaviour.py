"""Locks current behaviour. These tests do not fix the code they call."""

import ast
import csv
import os
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import domain_service

client = TestClient(app)
REPO = Path(__file__).resolve().parents[2]


def test_missing_id_returns_first_row():
    """characterization: locks current behaviour; replace when the defect is fixed"""
    row = domain_service.load_record("DOES-NOT-EXIST")
    assert row["device_id"] == "REC-0001"
    response = client.get(
        "/records/DOES-NOT-EXIST",
        headers={"X-User-Role": "operator"},
    )
    assert response.status_code == 200
    assert response.json()["device_id"] == "REC-0001"


def test_clinician_role_is_accepted_on_record_read():
    """characterization: locks current behaviour; replace when the defect is fixed"""
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "clinician"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["device_id"] == "REC-0001"
    assert body.get("error") != "forbidden"


def test_ai_summarize_accepts_request_with_no_role_header():
    """characterization: locks current behaviour; replace when the defect is fixed"""
    response = client.post("/ai/summarize/REC-0001")
    assert response.status_code == 200
    body = response.json()
    assert "summary" in body
    assert body.get("error") != "forbidden"


def test_etl_counts_blank_fields_and_does_not_quarantine():
    """characterization: locks current behaviour; replace when the defect is fixed"""
    devices = REPO / "data" / "synthetic" / "devices.csv"
    before = devices.read_bytes()
    data_names_before = sorted(
        path.name for path in (REPO / "data").rglob("*") if path.is_file()
    )
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, str(REPO / "etl" / "run_daily_batch.py"), "--sample"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert proc.returncode == 0
    payload = ast.literal_eval(proc.stdout.strip())
    with devices.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    blank_rows = sum(1 for row in rows if any(value == "" for value in row.values()))
    assert payload["processed"] == len(rows)
    assert payload["malformed"] == blank_rows
    assert payload["sample"] is True
    assert blank_rows > 0
    assert devices.read_bytes() == before
    data_names_after = sorted(
        path.name for path in (REPO / "data").rglob("*") if path.is_file()
    )
    assert data_names_after == data_names_before


def test_legacy_script_holds_password_constant():
    """characterization: locks current behaviour; replace when the defect is fixed"""
    source_path = REPO / "legacy" / "reconcile_legacy.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    present = False
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "SHARED_DB_PASSWORD":
                present = (
                    isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and node.value.value != ""
                )
    assert present, "SHARED_DB_PASSWORD string constant is absent"
