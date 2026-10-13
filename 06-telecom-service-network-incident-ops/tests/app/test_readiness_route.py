"""GET /ready. Stage S07. PRD RQ-73. /health stays 200 in every case."""

from apps.api.services import alarm_service, audit, domain_service, policy


def test_readiness_is_200_when_all_four_checks_pass(client):
    response = client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["checks"] == {
        "devices_csv": True,
        "alarms_csv": True,
        "audit_log_writable": True,
        "policy_loaded": True,
    }


def test_readiness_returns_503_when_devices_csv_is_missing(client, tmp_path, monkeypatch):
    monkeypatch.setattr(domain_service, "DATA_DIR", tmp_path)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["status"] == "Degraded"
    assert response.json()["checks"]["devices_csv"] is False
    assert client.get("/health").status_code == 200


def test_readiness_returns_503_when_alarms_csv_is_missing(client, tmp_path, monkeypatch):
    monkeypatch.setattr(alarm_service, "DATA_DIR", tmp_path)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["alarms_csv"] is False
    assert client.get("/health").status_code == 200


def test_readiness_returns_503_when_the_audit_log_cannot_be_written(client, tmp_path, monkeypatch):
    blocker = tmp_path / "blocker"
    blocker.write_text("a file where a folder should be", encoding="utf-8")
    monkeypatch.setattr(audit, "LOG", blocker / "audit.log")
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["audit_log_writable"] is False
    assert client.get("/health").status_code == 200


def test_readiness_returns_503_when_the_policy_is_not_loaded(client, monkeypatch):
    monkeypatch.setattr(policy, "POLICY_VERSION", "")
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["policy_loaded"] is False


def test_when_the_policy_engine_fails_readiness_is_503_and_every_role_route_is_403(client, monkeypatch):
    # PRD section 11, degraded mode row "Policy engine fails". The engine is set to opa with no
    # opa program on the path. The policy then denies. It never allows a call because the engine failed.
    monkeypatch.setenv("POLICY_ENGINE", "opa")
    monkeypatch.setenv("PATH", "")
    policy.reset_engine_cache()
    operator = {"X-User-Role": "operator"}
    assert client.get("/health").status_code == 200
    assert client.get("/ready").status_code == 503
    assert client.get("/records/DEV-00002", headers=operator).status_code == 403
    assert client.get("/alarms/storms/STO-00002", headers=operator).status_code == 403
    assert client.post("/ai/recommend/DEV-00002", headers=operator).status_code == 403
    assert client.post("/approvals/DEV-00002", headers=operator, json={"decision": "yes"}).status_code == 403
    assert client.get("/audit/anything", headers={"X-User-Role": "admin"}).status_code == 403
