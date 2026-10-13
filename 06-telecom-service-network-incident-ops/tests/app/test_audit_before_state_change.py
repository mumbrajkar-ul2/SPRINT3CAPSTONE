"""The audit row comes before any state change. Stage S07. PRD RQ-36, RQ-37, RQ-56.

`POST /approvals/{id}` is the only route that stores new state. These tests make the audit
write fail, or make the approval write fail, and check what is left.
"""

import json

import pytest

from apps.api.services import approvals, audit
from tests.app.helpers import GOOD_ID, OPERATOR

CASE = "order-case-1"


def show_recommendation(client):
    response = client.post(
        f"/ai/recommend/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": CASE}
    )
    assert response.status_code == 202


def approve(client):
    return client.post(
        f"/approvals/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": CASE}, json={"decision": "yes"}
    )


def break_audit_writes(monkeypatch):
    def cannot_write(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(audit, "write_event", cannot_write)


def test_the_audit_row_is_on_disk_when_the_approval_is_stored(client, audit_log, monkeypatch):
    seen = {}
    real_store = approvals.store

    def store_after_checking(record):
        # Called at the moment the approval is stored. The audit row must already be in the log.
        seen["rows"] = [r for r in audit_log() if r["action"] == "ai.approval"]
        real_store(record)

    monkeypatch.setattr(approvals, "store", store_after_checking)
    show_recommendation(client)
    response = approve(client)
    assert response.status_code == 200
    assert len(seen["rows"]) == 1
    assert seen["rows"][0]["approval_id"] == response.json()["approval_id"]


def test_audit_row_exists_when_the_approval_write_fails(client, audit_log, approvals_file, monkeypatch):
    show_recommendation(client)

    def cannot_store(record):
        raise OSError("approvals file is read-only")

    monkeypatch.setattr(approvals, "store", cannot_store)
    response = approve(client)
    assert response.status_code == 500
    assert response.json() == {"error": "approval not stored"}
    rows = [r for r in audit_log() if r["action"] == "ai.approval"]
    assert len(rows) == 1
    assert rows[0]["correlation_id"] == CASE
    assert rows[0]["record_id"] == GOOD_ID
    assert not approvals_file.exists() or approvals_file.read_text(encoding="utf-8") == ""


def test_no_approval_is_stored_when_the_audit_row_cannot_be_written(client, audit_log, approvals_file, monkeypatch):
    show_recommendation(client)
    break_audit_writes(monkeypatch)
    response = approve(client)
    assert response.status_code == 500
    assert response.json() == {"error": "audit log unwritable"}
    assert not approvals_file.exists() or approvals_file.read_text(encoding="utf-8") == ""
    assert approvals.read_all() == []
    assert not [r for r in audit_log() if r["action"] == "ai.approval"]


@pytest.mark.parametrize(
    "method, path, headers, secret",
    [
        ("get", f"/records/{GOOD_ID}", OPERATOR, GOOD_ID),
        ("get", "/alarms/storms/STO-00005", OPERATOR, "ALA-00005"),
        ("post", f"/ai/summarize/{GOOD_ID}", OPERATOR, "Synthetic summary"),
        ("post", f"/ai/recommend/{GOOD_ID}", OPERATOR, "Review and approve before action"),
    ],
)
def test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written(
    client, monkeypatch, method, path, headers, secret
):
    break_audit_writes(monkeypatch)
    response = getattr(client, method)(path, headers=headers)
    assert response.status_code == 500
    assert response.json() == {"error": "audit log unwritable"}
    assert secret not in response.text


def test_the_audit_route_returns_500_when_its_own_row_cannot_be_written(client, audit_log, monkeypatch):
    client.get(f"/records/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": "chain-1"})
    break_audit_writes(monkeypatch)
    response = client.get("/audit/chain-1", headers={"X-User-Role": "admin"})
    assert response.status_code == 500
    assert "rows" not in response.json()


def test_a_denied_call_also_returns_500_when_the_deny_row_cannot_be_written(client, monkeypatch):
    break_audit_writes(monkeypatch)
    response = client.get(f"/records/{GOOD_ID}")
    assert response.status_code == 500
    assert json.loads(response.text) == {"error": "audit log unwritable"}
