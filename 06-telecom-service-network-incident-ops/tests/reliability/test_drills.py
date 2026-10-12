"""Failure drills. Stage S04-11 Half B.

One test for each drill in docs/runbooks/failure-injection-drills.md, plus the
impossible alarm timestamp. Design: docs/11-reliability/. Each test checks what
the person sees and what is stored. No test writes under data/synthetic.

Drill ids used in the evidence file:

  DR-1  missing correlation id
  DR-2  AI timeout
  DR-3  duplicate replay
  DR-4  stale master data
  DR-5  partial batch failure
  DR-6  impossible alarm timestamp
"""

import ast
import csv
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import ai_gateway, audit, dedupe

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data" / "synthetic"
OPERATOR = {"X-User-Role": "operator"}
GOOD_ID = "DEV-00002"  # stale_topology_flag false
STALE_ID = "DEV-00003"  # stale_topology_flag true
BLANK_FLAG_ID = "DEV-BAD1"  # stale_topology_flag blank

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def audit_rows(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)

    def read():
        if not path.exists():
            return []
        return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]

    return read


class CountingModel:
    """Stands in for call_model. Counts calls. Can sleep first."""

    def __init__(self, sleep=0.0):
        self.calls = 0
        self.sleep = sleep
        self._lock = threading.Lock()

    def __call__(self, prompt):
        with self._lock:
            self.calls += 1
        if self.sleep:
            time.sleep(self.sleep)
        return json.dumps(
            {
                "record_id": GOOD_ID,
                "summary": "SIMULATED drill summary",
                "recommendation": "Review and approve before action",
                "outcome": "RECOMMEND_ONLY",
                "source_count": 1,
            }
        )


def csv_rows(name):
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# DR-1  Missing correlation id
# ---------------------------------------------------------------------------


def test_dr1_missing_correlation_id_creates_a_uuid_and_logs_it(audit_rows):
    response = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 200
    created = response.headers["X-Correlation-Id"]
    assert str(uuid.UUID(created)) == created
    rows = audit_rows()
    assert len(rows) == 1
    assert rows[0]["correlation_id"] == created


def test_dr1_a_blank_correlation_id_is_replaced_and_a_sent_one_is_kept(audit_rows):
    blank = client.get(f"/records/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": "   "})
    kept = client.get(f"/records/{GOOD_ID}", headers={**OPERATOR, "X-Correlation-Id": "demo-123"})
    replaced = blank.headers["X-Correlation-Id"]
    assert str(uuid.UUID(replaced)) == replaced
    assert kept.headers["X-Correlation-Id"] == "demo-123"
    assert [row["correlation_id"] for row in audit_rows()] == [replaced, "demo-123"]


def test_dr1_the_event_stream_has_blank_ids_and_the_dedupe_key_does_not_use_them():
    """The 1992 blank ids in events.jsonl are a fact of the data. The event key is event_id."""
    events = [
        json.loads(line)
        for line in (DATA / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    blank = [e for e in events if not (e.get("correlation_id") or "").strip()]
    assert (len(events), len(blank)) == (3000, 1992)
    assert all(dedupe.event_key(e)[0] for e in events)


# ---------------------------------------------------------------------------
# DR-2  AI timeout
# ---------------------------------------------------------------------------


def test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up(
    monkeypatch, audit_rows
):
    """The test sets a short deadline. It is not the production default."""
    monkeypatch.setenv(ai_gateway.TIMEOUT_ENV, "0.05")
    monkeypatch.setattr(ai_gateway, "call_model", CountingModel(sleep=0.4))
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["summary"] is None
    assert body["recommendation"] is None
    assert "failmode.timeout" in body["reasons"]
    assert "Synthetic summary for" not in response.text
    assert "Review and approve before action" not in response.text
    assert "SIMULATED" not in response.text
    # The routes that do not call the model keep working.
    assert client.get("/health").status_code == 200
    assert client.get(f"/records/{GOOD_ID}", headers=OPERATOR).status_code == 200
    held = audit_rows()[0]
    assert held["action"] == "policy.hold"
    assert held["outcome"] == "HOLD_FOR_REVIEW"


def test_dr2_a_model_error_is_held_and_health_stays_up(monkeypatch, audit_rows):
    def broken(prompt):
        raise ConnectionRefusedError("refused")

    monkeypatch.setattr(ai_gateway, "call_model", broken)
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 202
    assert response.json()["summary"] is None
    assert client.get("/health").status_code == 200


# ---------------------------------------------------------------------------
# DR-3  Duplicate replay
# ---------------------------------------------------------------------------


def test_dr3_the_same_alarm_sent_twice_is_one_alarm_by_dedupe_key():
    seen = dedupe.DedupeSet()
    alarm = {"alarm_id": "ALA-X", "dedupe_key": "DED-X", "storm_batch_id": "STO-X"}
    assert seen.check(dedupe.alarm_key(alarm)) == dedupe.NEW
    assert seen.check(dedupe.alarm_key(alarm)) == dedupe.REPEAT
    assert seen.repeat_count(dedupe.alarm_key(alarm)) == 1
    assert seen.totals() == {"new": 1, "repeat": 1, "held_aside": 0}


def test_dr3_same_dedupe_key_in_another_storm_is_a_different_alarm():
    seen = dedupe.DedupeSet()
    one = {"dedupe_key": "DED-X", "storm_batch_id": "STO-1"}
    two = {"dedupe_key": "DED-X", "storm_batch_id": "STO-2"}
    assert seen.check(dedupe.alarm_key(one)) == dedupe.NEW
    assert seen.check(dedupe.alarm_key(two)) == dedupe.NEW


def test_dr3_a_blank_key_part_is_held_aside_and_never_recorded():
    seen = dedupe.DedupeSet()
    row = {"dedupe_key": "", "storm_batch_id": "STO-1"}
    assert seen.check(dedupe.alarm_key(row)) == dedupe.HELD_ASIDE
    assert seen.check(dedupe.alarm_key(row)) == dedupe.HELD_ASIDE
    assert seen.totals() == {"new": 0, "repeat": 0, "held_aside": 2}
    assert seen.check((None, "STO-1")) == dedupe.HELD_ASIDE


def test_dr3_all_354_alarm_rows_give_350_new_3_repeats_1_held_aside():
    seen = dedupe.DedupeSet()
    for row in csv_rows("alarms.csv"):
        seen.check(dedupe.alarm_key(row))
    assert seen.totals() == {"new": 350, "repeat": 3, "held_aside": 1}


def test_dr3_all_354_order_rows_give_351_new_2_repeats_1_held_aside():
    seen = dedupe.DedupeSet()
    for row in csv_rows("service_orders.csv"):
        seen.check(dedupe.order_key(row))
    assert seen.totals() == {"new": 351, "repeat": 2, "held_aside": 1}


def test_dr3_replaying_the_event_file_twice_gives_3000_new_and_3000_repeats():
    events = [
        json.loads(line)
        for line in (DATA / "events.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    seen = dedupe.DedupeSet()
    for _ in range(2):
        for event in events:
            seen.check(dedupe.event_key(event))
    assert seen.totals() == {"new": 3000, "repeat": 3000, "held_aside": 0}


def test_dr3_the_summary_route_has_no_key_so_five_calls_cost_five_model_calls_and_five_rows(
    monkeypatch, audit_rows
):
    """Defence question 4: what a retry duplicates today. The route changes no stored row."""
    model = CountingModel()
    monkeypatch.setattr(ai_gateway, "call_model", model)
    headers = {**OPERATOR, "X-Correlation-Id": "dr3-retry"}
    codes = [client.post(f"/ai/summarize/{GOOD_ID}", headers=headers).status_code for _ in range(5)]
    assert codes == [200] * 5
    assert model.calls == 5
    rows = audit_rows()
    assert len(rows) == 5
    assert {row["correlation_id"] for row in rows} == {"dr3-retry"}


# ---------------------------------------------------------------------------
# DR-4  Stale master data
# ---------------------------------------------------------------------------


def test_dr4_a_true_stale_flag_is_blocked_and_the_model_is_not_called(monkeypatch, audit_rows):
    """Decision D-1. The YAML id failmode.stale_topology_true says BLOCK, not HOLD_FOR_REVIEW."""
    model = CountingModel()
    monkeypatch.setattr(ai_gateway, "call_model", model)
    response = client.post(f"/ai/summarize/{STALE_ID}", headers=OPERATOR)
    body = response.json()
    assert response.status_code == 403
    assert body["outcome"] == "BLOCK"
    assert body["summary"] is None
    assert "failmode.stale_topology_true" in body["reasons"]
    assert model.calls == 0
    assert audit_rows()[0]["outcome"] == "BLOCK"


def test_dr4_a_blank_stale_flag_is_held_for_review_and_the_model_is_not_called(
    monkeypatch, audit_rows
):
    model = CountingModel()
    monkeypatch.setattr(ai_gateway, "call_model", model)
    response = client.post(f"/ai/summarize/{BLANK_FLAG_ID}", headers=OPERATOR)
    body = response.json()
    assert response.status_code == 202
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["summary"] is None
    assert "failmode.stale_topology_blank" in body["reasons"]
    assert model.calls == 0


def test_dr4_a_false_flag_still_gets_a_summary(monkeypatch, audit_rows):
    monkeypatch.setattr(ai_gateway, "call_model", CountingModel())
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 200
    assert response.json()["outcome"] == "RECOMMEND_ONLY"


def test_dr4_192_rows_are_true_and_1_is_blank():
    flags = [row["stale_topology_flag"].strip().lower() for row in csv_rows("devices.csv")]
    assert flags.count("true") == 192
    assert flags.count("") == 1


# ---------------------------------------------------------------------------
# DR-5  Partial batch failure
# ---------------------------------------------------------------------------


def run_etl(tree):
    return subprocess.run(
        [sys.executable, str(tree / "etl" / "run_daily_batch.py"), "--sample"],
        cwd=tree,
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def etl_tree(tmp_path, rows):
    """A copy of the batch script with its own devices.csv. `rows` is a list of byte lines."""
    (tmp_path / "etl").mkdir()
    (tmp_path / "data" / "synthetic").mkdir(parents=True)
    shutil.copy(REPO / "etl" / "run_daily_batch.py", tmp_path / "etl" / "run_daily_batch.py")
    (tmp_path / "data" / "synthetic" / "devices.csv").write_bytes(b"\n".join(rows) + b"\n")
    return tmp_path


def test_dr5_one_bad_row_is_reported_and_the_rest_are_processed(tmp_path):
    lines = (DATA / "devices.csv").read_bytes().splitlines()
    header, good = lines[0], lines[1:4]
    cells = good[0].split(b",")
    blank_cell = b",".join(cells[:3] + [b""] + cells[4:])
    tree = etl_tree(tmp_path, [header, good[0], blank_cell, good[1], good[2]])
    proc = run_etl(tree)
    assert proc.returncode == 0
    payload = ast.literal_eval(proc.stdout.strip())
    assert payload == {"processed": 4, "malformed": 1, "sample": True, "quarantined": 1}
    assert "file line 3: blank cell" in proc.stderr


def test_dr5_short_long_and_undecodable_rows_are_held_aside_and_the_run_goes_on(tmp_path):
    lines = (DATA / "devices.csv").read_bytes().splitlines()
    header, good = lines[0], lines[1:4]
    cells = good[0].split(b",")
    short_row = b",".join(cells[:-2])
    long_row = good[0] + b",extra,extra"
    bad_bytes = b",".join([b"DEV-9", b"\xff\xfe"] + cells[2:])
    tree = etl_tree(tmp_path, [header, good[0], short_row, long_row, bad_bytes, good[1], good[2]])
    proc = run_etl(tree)
    assert proc.returncode == 0
    payload = ast.literal_eval(proc.stdout.strip())
    assert payload["processed"] == 6
    assert payload["quarantined"] == 3
    assert "short row" in proc.stderr
    assert "long row" in proc.stderr
    assert "not valid UTF-8" in proc.stderr


def test_dr5_the_real_file_keeps_its_old_counts_and_adds_one_quarantined_row(tmp_path):
    before = (DATA / "devices.csv").read_bytes()
    names_before = sorted(p.name for p in (REPO / "data").rglob("*") if p.is_file())
    proc = run_etl(REPO)
    assert proc.returncode == 0
    payload = ast.literal_eval(proc.stdout.strip())
    assert payload["processed"] == 354
    assert payload["malformed"] == 1
    assert payload["sample"] is True
    assert payload["quarantined"] == 1
    assert "file line 353: blank cell" in proc.stderr
    # Nothing is written.
    assert (DATA / "devices.csv").read_bytes() == before
    assert sorted(p.name for p in (REPO / "data").rglob("*") if p.is_file()) == names_before


# ---------------------------------------------------------------------------
# DR-6  Impossible alarm timestamp (separate from the stale flag drill)
# ---------------------------------------------------------------------------


def test_dr6_ala_00002_is_flagged_and_does_not_become_an_incident():
    rows = csv_rows("alarms.csv")
    row = next(r for r in rows if r["alarm_id"] == "ALA-00002")
    # File line 3: the header is line 1 and REC-0001 is line 2.
    assert rows.index(row) + 2 == 3
    assert row["last_seen_at"] < row["first_seen_at"]

    verdict = dedupe.check_alarm_row(row)
    assert verdict.ok is False
    assert verdict.flag == dedupe.FLAG_LAST_BEFORE_FIRST
    assert verdict.rule == "rule.alarm_last_seen_not_before_first_seen"
    assert verdict.can_become_incident is False

    outcome = dedupe.alarm_intake([row])
    assert outcome["candidates"] == []
    assert [r["alarm_id"] for r, _ in outcome["flagged"]] == ["ALA-00002"]


def test_dr6_the_rule_id_exists_in_business_rules_yaml():
    document = yaml.safe_load((REPO / "semantic-layer" / "business-rules.yaml").read_text(encoding="utf-8"))
    ids = {rule["id"] for rule in document["rules"]}
    assert dedupe.ALARM_TIME_RULE in ids


def test_dr6_equal_times_are_fine_and_later_last_seen_is_fine():
    same = {"first_seen_at": "2026-01-01T10:00:00", "last_seen_at": "2026-01-01T10:00:00"}
    later = {"first_seen_at": "2026-01-01T10:00:00", "last_seen_at": "2026-01-01T10:00:01"}
    assert dedupe.check_alarm_row(same).can_become_incident is True
    assert dedupe.check_alarm_row(later).can_become_incident is True


def test_dr6_blank_or_unreadable_times_are_flagged_for_review():
    blank = {"first_seen_at": "", "last_seen_at": ""}
    mixed = {"first_seen_at": "2026-01-01T10:00:00+00:00", "last_seen_at": "2026-01-01T10:00:00"}
    for row in (blank, mixed):
        verdict = dedupe.check_alarm_row(row)
        assert verdict.flag == dedupe.FLAG_TIMES_UNREADABLE
        assert verdict.can_become_incident is False


def test_dr6_the_real_file_has_166_rows_before_and_1_unreadable_and_none_become_incidents():
    rows = csv_rows("alarms.csv")
    outcome = dedupe.alarm_intake(rows)
    flags = [verdict.flag for _, verdict in outcome["flagged"]]
    assert flags.count(dedupe.FLAG_LAST_BEFORE_FIRST) == 166
    assert flags.count(dedupe.FLAG_TIMES_UNREADABLE) == 1
    flagged_ids = {id(r) for r, _ in outcome["flagged"]}
    assert all(id(r) not in flagged_ids for r in outcome["candidates"])
    # Every row lands in exactly one list.
    total = sum(len(outcome[name]) for name in ("candidates", "repeats", "held_aside")) + len(
        outcome["flagged"]
    )
    assert total == len(rows) == 354
