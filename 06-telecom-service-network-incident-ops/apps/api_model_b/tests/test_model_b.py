"""Checks owned by the Model B implementation."""

from __future__ import annotations

import json
import uuid

import pytest
from fastapi.testclient import TestClient

from apps.api_model_b.main import app
from apps.api_model_b.services import ai_gateway, approvals, audit


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "LOG", tmp_path / "audit.log")
    monkeypatch.setattr(approvals, "STORE", tmp_path / "approvals.jsonl")
    ai_gateway.reset_runtime_state()
    return TestClient(app)


def _rows(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_health_and_route_set(client):
    assert client.get("/health").json() == {"status": "ok"}
    paths = {route.path for route in app.routes}
    assert {
        "/",
        "/health",
        "/ready",
        "/records/{record_id}",
        "/alarms/storms/{storm_batch_id}",
        "/ai/summarize/{record_id}",
        "/ai/recommend/{record_id}",
        "/approvals/{record_id}",
        "/audit/{correlation_id}",
    } <= paths
    assert all("execute" not in path for path in paths)


def test_record_access_and_field_filter(client):
    assert client.get("/records/DEV-00002").status_code == 403
    operator = client.get("/records/DEV-00002", headers={"X-User-Role": "operator"})
    engineer = client.get("/records/DEV-00002", headers={"X-User-Role": "engineer"})
    assert operator.status_code == engineer.status_code == 200
    assert "mgmt_ip" not in operator.json()
    assert engineer.json()["mgmt_ip"] == "alpha"
    assert client.get("/records/DOES-NOT-EXIST", headers={"X-User-Role": "operator"}).status_code == 404


def test_storm_contract(client):
    response = client.get("/alarms/storms/STO-00005", headers={"X-User-Role": "operator"})
    assert response.status_code == 200
    assert response.json() == {
        "raw_count": 2,
        "deduped_count": 1,
        "flagged_count": 0,
        "rows": [
            {"alarm_id": "ALA-00005", "device_id": "DEV-00005", "dedupe_key": "DED-00005", "flag": ""},
            {"alarm_id": "ALA-00004", "device_id": "DEV-00005", "dedupe_key": "DED-00005", "flag": ""},
        ],
        "held_aside": [],
    }


def test_recommend_approval_and_audit_chain(client):
    headers = {"X-User-Role": "operator", "X-Correlation-Id": "model-b-case"}
    assert client.get("/alarms/storms/STO-00002", headers=headers).status_code == 200
    assert client.get("/records/DEV-00002", headers=headers).status_code == 200
    recommendation = client.post("/ai/recommend/DEV-00002", headers=headers)
    assert recommendation.status_code == 202
    assert recommendation.json()["outcome"] == "HOLD_FOR_REVIEW"
    approval = client.post("/approvals/DEV-00002", headers=headers, json={"decision": "yes"})
    assert approval.status_code == 200
    chain = client.get(
        "/audit/model-b-case",
        headers={"X-User-Role": "admin", "X-Correlation-Id": "model-b-reader"},
    )
    assert chain.status_code == 200
    assert [row["action"] for row in chain.json()["rows"]] == [
        "record.storm_read",
        "record.read",
        "ai.recommendation",
        "ai.approval",
    ]


def test_client_approval_id_is_ignored(client):
    headers = {"X-User-Role": "operator", "X-Correlation-Id": "forged-case"}
    client.post("/ai/recommend/DEV-00002", headers=headers)
    response = client.post(
        "/approvals/DEV-00002",
        headers=headers,
        json={"decision": "yes", "approval_id": "caller-value"},
    )
    assert response.status_code == 200
    assert response.json()["approval_id"] != "caller-value"
    assert "caller-value" not in approvals.STORE.read_text(encoding="utf-8")


def test_every_audit_row_has_the_17_semantic_keys(client):
    client.get("/records/DEV-00002", headers={"X-User-Role": "operator"})
    rows = _rows(audit.LOG)
    assert len(rows) == 1
    assert tuple(rows[0]) == audit.SCHEMA_KEYS
    assert rows[0]["record_id"] == "DEV-00002"
    assert rows[0]["final_action"] == "none"


def test_flagged_storm_and_denied_role(client):
    body = client.get("/alarms/storms/STO-00019", headers={"X-User-Role": "operator"}).json()
    assert (body["raw_count"], body["deduped_count"], body["flagged_count"]) == (2, 1, 2)
    assert {row["flag"] for row in body["rows"]} == {"last_seen_before_first_seen"}
    denied = client.get("/records/REC-0001", headers={"X-User-Role": "clinician"})
    assert denied.status_code == 403
    assert denied.json() == {"error": "forbidden"}


def test_summary_chain_and_cannot_prove(client):
    headers = {"X-User-Role": "operator", "X-Correlation-Id": "summary-case"}
    assert client.get("/records/REC-0001", headers=headers).status_code == 200
    assert client.post("/ai/summarize/REC-0001", headers=headers).status_code == 200
    client.get("/records/REC-0001", headers={**headers, "X-User-Role": "visitor"})
    response = client.get("/audit/summary-case", headers={"X-User-Role": "admin"})
    assert response.status_code == 200
    body = response.json()
    assert [row["action"] for row in body["rows"]] == ["record.read", "ai.summary", "policy.deny"]
    assert [row["role"] for row in body["rows"]] == ["operator", "operator", "visitor"]
    items = {entry["item"] for entry in body["cannot_prove"]}
    assert {"approval_id", "caller_identity", "log_integrity"} <= items


def test_long_header_correlation_id_is_replaced(client):
    sent = "x" * 129
    response = client.get(
        "/records/DEV-00002",
        headers={"X-User-Role": "operator", "X-Correlation-Id": sent},
    )
    assert response.status_code == 200
    replacement = response.headers["x-correlation-id"]
    assert uuid.UUID(replacement).version == 4
    assert sent not in audit.LOG.read_text(encoding="utf-8")
