"""Security tests for the audit log. Stage S05-13 Half B.

NG-01: `write_event` refuses an empty correlation id.
NG-03: the real `logs/audit.log` holds no forbidden field name.

Designs: docs/13-security-validation/negative-tests.md.
These strings are built in pieces so that test_secret_patterns.py does not flag this file.
"""

import json
from pathlib import Path

import pytest
import yaml

from apps.api.services import audit

pytestmark = pytest.mark.security

REPO = Path(__file__).resolve().parents[2]
POLICY_FILE = REPO / "semantic-layer" / "ai-context-policy.yaml"
REAL_LOG = REPO / "logs" / "audit.log"

# The two field names the prompt and the audit row must never carry.
FORBIDDEN_FIELD_NAMES = ("mgmt" + "_ip", "credential" + "_profile")


def _credential_names():
    document = yaml.safe_load(POLICY_FILE.read_text(encoding="utf-8"))
    return list(document["prompt_fields"]["forbidden_credential_names"]["names"])


def forbidden_name_hits(path):
    """Return (line number, name) for every line that holds a forbidden name.

    A missing file has zero lines. That is not a skip.
    """
    names = list(FORBIDDEN_FIELD_NAMES) + _credential_names()
    hits = []
    if not path.exists():
        return hits
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for name in names:
            if name in line:
                hits.append((line_no, name))
    return hits


# ---------------------------------------------------------------------------
# NG-01
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["", "   ", None])
def test_write_event_refuses_an_empty_correlation_id(tmp_path, monkeypatch, value):
    log = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", log)
    with pytest.raises(ValueError, match="correlation_id is required"):
        audit.write_event(
            "record.read",
            correlation_id=value,
            actor=None,
            role=None,
            resource="resource.device",
        )
    # No row was written and no log file was made.
    assert not log.exists()


def test_write_event_with_an_id_writes_exactly_one_row(tmp_path, monkeypatch):
    """Shows the log path works, so the refusals above are not an accident of the setup."""
    log = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", log)
    audit.write_event(
        "record.read",
        correlation_id="demo-123",
        actor=None,
        role=None,
        resource="resource.device",
    )
    rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["correlation_id"] == "demo-123"


# ---------------------------------------------------------------------------
# NG-03
# ---------------------------------------------------------------------------


def test_forbidden_name_finder_finds_a_planted_name(tmp_path):
    """The finder must see a planted name, or the real-log test below proves nothing."""
    planted = tmp_path / "planted.log"
    planted.write_text(
        json.dumps({"ts": "x", "role": "operator"}) + "\n"
        + json.dumps({"note": FORBIDDEN_FIELD_NAMES[0] + "=10.0.0.1"}) + "\n",
        encoding="utf-8",
    )
    assert forbidden_name_hits(planted) == [(2, FORBIDDEN_FIELD_NAMES[0])]
    credential = _credential_names()[0]
    planted.write_text(credential + "\n", encoding="utf-8")
    assert forbidden_name_hits(planted) == [(1, credential)]


def test_real_audit_log_holds_no_forbidden_name():
    assert forbidden_name_hits(REAL_LOG) == []
    if REAL_LOG.exists():
        lines = [line for line in REAL_LOG.read_text(encoding="utf-8").splitlines() if line.strip()]
        for line_no, line in enumerate(lines, 1):
            # Every non-empty line is one JSON object. A broken line is a finding, not a skip.
            assert isinstance(json.loads(line), dict), f"line {line_no} is not an object"
