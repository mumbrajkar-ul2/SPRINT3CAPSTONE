"""Shared setup for tests/app. Stage S07.

Every test here writes its audit rows to a temporary file and its approvals to a temporary
file (PRD RQ-72). No test in this folder appends to logs/audit.log or logs/approvals.jsonl.
The tests/conftest.py file above this one already resets the breaker and picks the Python
copy of the policy for every test.
"""

import json
import re
import threading

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import ai_gateway, approvals, audit



@pytest.fixture(autouse=True)
def audit_log(tmp_path, monkeypatch):
    """Point the audit log at a temporary file. Returns a function that reads its rows."""
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)

    def rows():
        if not path.exists():
            return []
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

    rows.path = path
    return rows


@pytest.fixture(autouse=True)
def approvals_file(tmp_path, monkeypatch):
    """Point the approvals store at a temporary file."""
    path = tmp_path / "approvals.jsonl"
    monkeypatch.setattr(approvals, "STORE", path)
    return path


@pytest.fixture
def client():
    # A 500 is a result these tests check. The client returns it and does not raise.
    return TestClient(app, raise_server_exceptions=False)


class FakeModel:
    """Stands in for ai_gateway.call_model. Counts calls and returns the answer it was given."""

    def __init__(self, summary="SIMULATED test summary", recommendation="Review and approve before action",
                 outcome="RECOMMEND_ONLY", raw=None, error=None):
        self.summary = summary
        self.recommendation = recommendation
        self.outcome = outcome
        self.raw = raw
        self.error = error
        self.calls = 0
        self._lock = threading.Lock()

    def __call__(self, prompt):
        with self._lock:
            self.calls += 1
        if self.error is not None:
            raise self.error
        if self.raw is not None:
            return self.raw
        match = re.search(r"^device_id: (.+)$", prompt, re.MULTILINE)
        return json.dumps(
            {
                "record_id": match.group(1).strip() if match else "unknown",
                "summary": self.summary,
                "recommendation": self.recommendation,
                "outcome": self.outcome,
                "source_count": 1,
            }
        )


@pytest.fixture
def fake_model(monkeypatch):
    """Returns a function. Call it with the answer to give. It installs the stand-in and returns it."""

    def install(**kwargs):
        model = FakeModel(**kwargs)
        monkeypatch.setattr(ai_gateway, "call_model", model)
        return model

    return install
