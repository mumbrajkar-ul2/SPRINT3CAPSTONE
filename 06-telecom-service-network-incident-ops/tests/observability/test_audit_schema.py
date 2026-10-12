"""Audit row shape. Stage S04-08 Half B."""

import json
import uuid

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit

# Stage S05-13 Half B: every test in this file is part of the security suite.
pytestmark = pytest.mark.security

client = TestClient(app)

REQUIRED_KEYS = (
    "ts",
    "correlation_id",
    "actor",
    "role",
    "action",
    "resource",
    "policy_decision",
    "approval_id",
    "model",
    "model_version",
    "prompt_hash",
    "tokens",
    "latency_ms",
    "outcome",
    # S04-12 Half B. The fifteenth key. Names the formula behind `tokens`.
    "token_estimate_method",
)


def _rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _use_log(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)
    return path


def test_every_audit_row_has_every_required_field(tmp_path, monkeypatch):
    path = _use_log(tmp_path, monkeypatch)
    client.get("/health")
    client.get("/records/REC-0001", headers={"X-User-Role": "operator"})
    client.post("/ai/summarize/REC-0001", headers={"X-User-Role": "operator"})
    client.post("/ai/summarize/REC-0001")
    client.get("/records/REC-0001", headers={"X-User-Role": "clinician"})
    rows = _rows(path)
    assert len(rows) == 4
    for row in rows:
        assert tuple(row) == REQUIRED_KEYS
        assert row["ts"]
        assert row["correlation_id"]
        assert row["action"]
        assert row["resource"] == "resource.device"
        assert row["policy_decision"] is None
        assert row["approval_id"] is None
        # S04-09: a row that ran the model carries the five provenance values.
        # Every other row leaves them null. This test used to expect null on all four.
        provenance = [row[key] for key in ("model", "model_version", "prompt_hash", "tokens", "latency_ms")]
        if row["action"] == "ai.summary":
            assert row["model"] == "local-sim-v1"
            assert row["model_version"] == "local-sim-v1"
            assert row["prompt_hash"]
            assert isinstance(row["tokens"], int)
            assert isinstance(row["latency_ms"], int)
            # S04-12 Half B. The word-count formula is EDUCATIONAL, and the row says so.
            assert row["token_estimate_method"] == "word_count_x2_EDUCATIONAL"
        else:
            assert provenance == [None] * 5
            assert row["token_estimate_method"] is None
        text = json.dumps(row)
        assert "mgmt_ip" not in text
        assert "credential_profile" not in text


def test_request_with_header_keeps_the_id(tmp_path, monkeypatch):
    path = _use_log(tmp_path, monkeypatch)
    response = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "operator", "X-Correlation-Id": "demo-123"},
    )
    assert response.status_code == 200
    assert response.headers["x-correlation-id"] == "demo-123"
    row = _rows(path)[0]
    assert row["correlation_id"] == "demo-123"
    assert row["actor"] == "noc_operator"
    assert row["role"] == "operator"
    assert row["action"] == "record.read"
    assert row["outcome"] is None


def test_request_without_header_gets_a_uuid(tmp_path, monkeypatch):
    path = _use_log(tmp_path, monkeypatch)
    response = client.get("/records/REC-0001", headers={"X-User-Role": "operator"})
    assert response.status_code == 200
    correlation_id = response.headers["x-correlation-id"]
    parsed = uuid.UUID(correlation_id)
    assert parsed.version == 4
    assert _rows(path)[0]["correlation_id"] == correlation_id

    blank = client.get(
        "/records/REC-0001",
        headers={"X-User-Role": "operator", "X-Correlation-Id": "   "},
    )
    blank_id = blank.headers["x-correlation-id"]
    assert uuid.UUID(blank_id).version == 4
    assert blank_id != correlation_id
    assert _rows(path)[1]["correlation_id"] == blank_id
