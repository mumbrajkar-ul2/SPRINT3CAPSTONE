"""Locks current behaviour. These tests do not fix the code they call."""

import ast
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit, domain_service

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


@pytest.mark.security
def test_clinician_role_is_denied_on_record_read():
    """Replaces test_clinician_role_is_accepted_on_record_read.

    That test locked HTTP 200 and device_id REC-0001 for header clinician.
    This test locks the forbidden body. Since S04-06 the status is 403.
    Before S04-06 it was 200 with the same body.
    role: role.clinician
    action: action.read
    resource: resource.device
    purpose: purpose.incident_triage
    scope: scope.all_records
    risk: risk.read_only
    """
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "clinician"},
    )
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}


@pytest.mark.security
def test_ai_summarize_refuses_request_with_no_role_header(tmp_path, monkeypatch):
    """Replaces test_ai_summarize_accepts_request_with_no_role_header.

    That test locked HTTP 200 and a summary for a call with no role header.
    Since S04-06 a call with no role has no caller. The policy denies it,
    the route returns 403, and an audit row is written.
    """
    monkeypatch.setattr(audit, "LOG", tmp_path / "audit.log")
    response = client.post("/ai/summarize/REC-0001")
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    rows = [json.loads(line) for line in (tmp_path / "audit.log").read_text().splitlines()]
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["role"] is None
    assert rows[0]["correlation_id"]


def test_etl_counts_blank_fields_and_keeps_its_old_count_meaning():
    """Replaces test_etl_counts_blank_fields_and_does_not_quarantine (S04-11 Half B).

    The ETL now also reports `quarantined`. The old keys `processed`, `malformed` and `sample`
    keep their meaning, and this test still locks that. The new key is tested in
    tests/reliability/test_drills.py (drill DR-5).
    """
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


@pytest.mark.security
def test_legacy_script_reads_password_from_environment():
    """Replaces test_legacy_script_holds_password_constant.

    That test locked a string constant for SHARED_DB_PASSWORD.
    This test locks an environment read and the device-row count.
    """
    source_path = REPO / "legacy" / "reconcile_legacy.py"
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "SHARED_DB_PASSWORD":
                is_literal = (
                    isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and node.value.value != ""
                )
                assert not is_literal, "SHARED_DB_PASSWORD string constant is present"

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["SHARED_DB_PASSWORD"] = "local-test-only"
    proc = subprocess.run(
        [sys.executable, str(REPO / "legacy" / "reconcile_legacy.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "legacy reconciled 354"

    env.pop("SHARED_DB_PASSWORD", None)
    missing = subprocess.run(
        [sys.executable, str(REPO / "legacy" / "reconcile_legacy.py")],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert missing.returncode != 0
    assert "SHARED_DB_PASSWORD" in missing.stderr
    assert "legacy reconciled" not in missing.stdout
