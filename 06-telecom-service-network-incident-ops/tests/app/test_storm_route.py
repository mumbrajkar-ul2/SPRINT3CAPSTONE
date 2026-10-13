"""GET /alarms/storms/{storm_batch_id}. Stage S07. PRD RQ-08 to RQ-15."""

import csv

from apps.api.services import alarm_service
from tests.app.helpers import ENGINEER, OPERATOR

ALARMS = alarm_service.DATA_DIR / alarm_service.ALARMS
ROW_KEYS = {"alarm_id", "device_id", "dedupe_key", "flag"}


def test_storm_returns_raw_count_deduped_count_and_alarm_ids(client):
    # STO-00005 has two rows with the same dedupe key DED-00005 (PRD RQ-08).
    response = client.get("/alarms/storms/STO-00005", headers=OPERATOR)
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"raw_count", "deduped_count", "flagged_count", "rows", "held_aside"}
    assert (body["raw_count"], body["deduped_count"], body["flagged_count"]) == (2, 1, 0)
    assert [row["alarm_id"] for row in body["rows"]] == ["ALA-00005", "ALA-00004"]
    assert all(set(row) == ROW_KEYS for row in body["rows"])
    assert body["held_aside"] == []


def test_flagged_alarm_is_listed_and_is_not_an_incident_candidate(client):
    # RQ-09. Both rows of STO-00019 are flagged. They count in raw and flagged. They are listed.
    body = client.get("/alarms/storms/STO-00019", headers=OPERATOR).json()
    assert (body["raw_count"], body["deduped_count"], body["flagged_count"]) == (2, 1, 2)
    assert [row["flag"] for row in body["rows"]] == ["last_seen_before_first_seen"] * 2
    single = client.get("/alarms/storms/STO-00002", headers=OPERATOR).json()
    assert (single["raw_count"], single["deduped_count"], single["flagged_count"]) == (1, 1, 1)
    # The reply makes no incident. It holds no incident key of any kind.
    assert "incident" not in str(body).lower()


def test_a_row_with_a_blank_dedupe_key_goes_to_held_aside(client, tmp_path, monkeypatch):
    # RQ-08. A blank key is held aside. It counts in the raw count and not in the deduped count.
    path = tmp_path / alarm_service.ALARMS
    header = "alarm_id,device_id,interface,severity,alarm_type,first_seen_at,last_seen_at,dedupe_key,maintenance_window,storm_batch_id\n"
    path.write_text(
        header
        + "ALA-T1,DEV-00002,x,low,t,2026-01-01T00:00:00,2026-01-02T00:00:00,DED-T1,none,STO-T\n"
        + "ALA-T2,DEV-00003,x,low,t,2026-01-01T00:00:00,2026-01-02T00:00:00,,none,STO-T\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(alarm_service, "DATA_DIR", tmp_path)
    body = client.get("/alarms/storms/STO-T", headers=OPERATOR).json()
    assert body["raw_count"] == 2
    assert body["deduped_count"] == 1
    assert [row["alarm_id"] for row in body["rows"]] == ["ALA-T1"]
    assert [row["alarm_id"] for row in body["held_aside"]] == ["ALA-T2"]


def test_unknown_storm_returns_404(client):
    response = client.get("/alarms/storms/STO-NOPE", headers=OPERATOR)
    assert response.status_code == 404
    assert response.json() == {"error": "not_found"}


def test_roles_without_an_alarm_read_row_get_403(client, audit_log):
    for headers in ({"X-User-Role": "admin"}, {"X-User-Role": "clinician"}, {"X-User-Role": "ai_agent"}, {}):
        response = client.get("/alarms/storms/STO-00005", headers=headers)
        assert response.status_code == 403
        assert response.json() == {"error": "forbidden"}
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"] * 4
    assert {row["resource"] for row in rows} == {"resource.alarm"}


def test_network_engineer_may_read_a_storm(client):
    # TA-13.
    assert client.get("/alarms/storms/STO-00005", headers=ENGINEER).status_code == 200


def test_storm_read_leaves_alarms_csv_unchanged(client):
    before = ALARMS.read_bytes()
    names_before = sorted(path.name for path in ALARMS.parent.iterdir())
    for storm in ("STO-00005", "STO-00019", "STO-00002", "STO-00001", "STO-NOPE"):
        client.get(f"/alarms/storms/{storm}", headers=OPERATOR)
    assert ALARMS.read_bytes() == before
    assert sorted(path.name for path in ALARMS.parent.iterdir()) == names_before


def test_storm_response_has_no_size_flag(client):
    body = client.get("/alarms/storms/STO-00005", headers=OPERATOR).json()
    text = str(body).lower()
    for word in ("large", "small", "size", "storm_size", "is_storm"):
        assert word not in text


def test_missing_alarms_file_returns_500_and_health_stays_200(client, tmp_path, monkeypatch):
    monkeypatch.setattr(alarm_service, "DATA_DIR", tmp_path)
    response = client.get("/alarms/storms/STO-00005", headers=OPERATOR)
    assert response.status_code == 500
    assert response.json() == {"error": "data file missing"}
    assert client.get("/health").status_code == 200


def test_storm_read_writes_one_audit_row(client, audit_log):
    response = client.get(
        "/alarms/storms/STO-00005", headers={**OPERATOR, "X-Correlation-Id": "storm-case-1"}
    )
    assert response.status_code == 200
    rows = audit_log()
    assert len(rows) == 1
    row = rows[0]
    assert row["action"] == "record.storm_read"
    assert row["correlation_id"] == "storm-case-1"
    assert row["role"] == "operator"
    assert row["resource"] == "resource.alarm"


def test_the_alarm_file_has_the_columns_the_service_reads():
    with ALARMS.open(newline="", encoding="utf-8") as handle:
        columns = csv.DictReader(handle).fieldnames
    assert {"alarm_id", "device_id", "dedupe_key", "storm_batch_id", "first_seen_at", "last_seen_at"} <= set(columns)
