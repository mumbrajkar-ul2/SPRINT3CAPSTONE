"""GET /records/{id}. Stage S07. PRD RQ-03, RQ-05, RQ-06, RQ-68.

This file also holds the replacement for the old first-row characterization test
(tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row).
"""

from tests.app.helpers import ADMIN, ENGINEER, GOOD_ID, OPERATOR, MISSING_ID

SENSITIVE = ("mgmt_ip", "credential_profile")


def test_missing_id_returns_404_and_no_row(client, audit_log):
    response = client.get("/records/DOES-NOT-EXIST", headers=OPERATOR)
    assert response.status_code == 404
    assert response.json() == {"error": "not_found"}
    # The body holds no field of the first row of devices.csv or of any other row.
    assert "device_id" not in response.text
    assert "REC-0001" not in response.text
    # The PRD names no audit row for a 404. S07 writes none (see PRD gaps in docs/demo/evidence.md).
    assert audit_log() == []


def test_an_id_that_is_only_in_alarms_csv_returns_404(client):
    # RQ-62 example. DEV-00001 is in alarms.csv (storm STO-00001) and has no device row.
    response = client.get(f"/records/{MISSING_ID}", headers=OPERATOR)
    assert response.status_code == 404


def test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile(client, audit_log):
    response = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    assert response.status_code == 200
    body = response.json()
    assert body["device_id"] == GOOD_ID
    for name in SENSITIVE:
        assert name not in body
    rows = audit_log()
    assert [row["action"] for row in rows] == ["record.read"]
    assert rows[0]["record_id"] == GOOD_ID
    assert rows[0]["resource"] == "resource.device"


def test_network_engineer_read_returns_mgmt_ip_and_credential_profile(client):
    response = client.get(f"/records/{GOOD_ID}", headers=ENGINEER)
    assert response.status_code == 200
    body = response.json()
    assert body["mgmt_ip"] == "alpha"
    assert body["credential_profile"] == "high_risk"


def test_admin_read_does_not_return_the_sensitive_fields(client):
    # role.admin has no allow row for record reads, so the call is refused before any field is chosen.
    response = client.get(f"/records/{GOOD_ID}", headers=ADMIN)
    assert response.status_code == 403
    assert "mgmt_ip" not in response.text


def test_missing_header_returns_403_and_a_deny_row(client, audit_log):
    response = client.get(f"/records/{GOOD_ID}")
    assert response.status_code == 403
    assert response.json() == {"error": "forbidden"}
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"]
    assert rows[0]["role"] is None
    assert rows[0]["actor"] is None
    assert rows[0]["record_id"] == GOOD_ID


def test_a_blank_header_is_treated_as_no_role(client, audit_log):
    response = client.get(f"/records/{GOOD_ID}", headers={"X-User-Role": "   "})
    assert response.status_code == 403
    assert audit_log()[0]["role"] is None
