"""POST /ai/recommend/{id}. Stage S07. PRD RQ-18 to RQ-28, RQ-70.

The model is the stub `local-sim-v1`, or a stand-in from the `fake_model` fixture. Every test
checks the route body and the audit row. A stand-in counts its calls, so a test can prove that
the model was not called.
"""

import json
import time

import pytest

from apps.api.services import ai_gateway, domain_service
from tests.app.helpers import ADMIN, BLANK_FLAG_ID, ENGINEER, GOOD_ID, MISSING_ID, OPERATOR, STALE_ID

SENTENCE = "Review and approve before action"
SENTINEL_IP = "SENTINEL-MGMT-9X"


def recommend(client, record_id=GOOD_ID, headers=OPERATOR):
    return client.post(f"/ai/recommend/{record_id}", headers=headers)


def assert_no_text(body):
    assert body["summary"] is None
    assert body["recommendation"] is None


def test_healthy_recommend_is_hold_for_review_with_the_sentence(client, audit_log):
    response = recommend(client)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["recommendation"] == SENTENCE
    assert body["summary"] == "Synthetic summary for " + GOOD_ID
    assert body["reasons"] == ["ai_use.next_action_recommendation"]
    for key in ("model", "model_version", "prompt_hash", "tokens", "latency_ms", "correlation_id"):
        assert body[key] not in (None, "")
    rows = audit_log()
    assert [row["action"] for row in rows] == ["ai.recommendation"]
    row = rows[0]
    assert row["outcome"] == "HOLD_FOR_REVIEW"
    assert row["record_id"] == GOOD_ID
    assert row["prompt_hash"] == body["prompt_hash"]
    assert row["token_estimate_method"] == "word_count_x2_EDUCATIONAL"
    # The audit row holds no prompt text and no reason (PRD section 7).
    assert "device_id:" not in json.dumps(row)
    assert "reasons" not in row


def test_recommend_never_returns_execute(client, fake_model, audit_log):
    # RQ-19. The model says EXECUTE. The route returns BLOCK with no text.
    model = fake_model(outcome="EXECUTE")
    response = recommend(client)
    assert response.status_code == 403
    body = response.json()
    assert body["outcome"] == "BLOCK"
    assert_no_text(body)
    assert "rule.ai_output_cannot_execute" in body["reasons"]
    assert model.calls == 1
    assert [row["action"] for row in audit_log()] == ["policy.deny"]
    # No other call returns EXECUTE either.
    for record_id in (GOOD_ID, STALE_ID, BLANK_FLAG_ID, MISSING_ID, "nonsense"):
        assert recommend(client, record_id).json()["outcome"] != "EXECUTE"
    assert all(row["outcome"] != "EXECUTE" for row in audit_log())


def test_recommend_has_no_recommend_only_outcome(client):
    # RQ-18. Policy row O2 gives HOLD_FOR_REVIEW. RECOMMEND_ONLY is the outcome of the summarize route only.
    assert recommend(client).json()["outcome"] == "HOLD_FOR_REVIEW"
    summary = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    assert summary.json()["outcome"] == "RECOMMEND_ONLY"


def test_missing_id_is_blocked_and_the_model_is_not_called(client, fake_model, audit_log):
    model = fake_model()
    response = recommend(client, MISSING_ID)
    assert response.status_code == 403
    body = response.json()
    assert body["outcome"] == "BLOCK"
    assert_no_text(body)
    assert "failmode.missing_id" in body["reasons"]
    assert model.calls == 0
    assert [row["action"] for row in audit_log()] == ["policy.deny"]
    assert audit_log()[0]["prompt_hash"] is None


def test_stale_true_is_blocked_and_the_model_is_not_called(client, fake_model):
    model = fake_model()
    response = recommend(client, STALE_ID)
    assert response.status_code == 403
    body = response.json()
    assert body["outcome"] == "BLOCK"
    assert_no_text(body)
    assert "failmode.stale_topology_true" in body["reasons"]
    assert model.calls == 0


def test_blank_stale_flag_is_held_and_the_model_is_not_called(client, fake_model, audit_log):
    model = fake_model()
    response = recommend(client, BLANK_FLAG_ID)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(body)
    assert "failmode.stale_topology_blank" in body["reasons"]
    assert model.calls == 0
    assert [row["action"] for row in audit_log()] == ["policy.hold"]


def test_timeout_returns_hold_for_review_with_no_summary(client, monkeypatch, audit_log):
    # The test sets a short deadline. It is not the production default (10 seconds).
    monkeypatch.setenv(ai_gateway.TIMEOUT_ENV, "0.05")

    def slow(prompt):
        time.sleep(0.4)
        raise AssertionError("the answer arrives after the deadline and is not used")

    monkeypatch.setattr(ai_gateway, "call_model", slow)
    response = recommend(client)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(body)
    assert "failmode.timeout" in body["reasons"]
    assert SENTENCE not in response.text
    assert "Synthetic summary" not in response.text
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.hold"]
    assert rows[0]["outcome"] == "HOLD_FOR_REVIEW"
    # The routes that do not call the model keep working (RQ-53).
    assert client.get("/health").status_code == 200
    assert client.get(f"/records/{GOOD_ID}", headers=OPERATOR).status_code == 200


def test_model_error_and_open_breaker_return_hold_for_review(client, fake_model):
    model = fake_model(error=ConnectionRefusedError("refused"))
    first = recommend(client)
    assert first.status_code == 202
    assert first.json()["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(first.json())
    # Four more failures in a row open the breaker (default threshold 5, PROPOSED N-05).
    for _ in range(4):
        recommend(client)
    assert model.calls == 5
    refused = recommend(client)
    assert refused.status_code == 202
    assert refused.json()["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(refused.json())
    assert model.calls == 5  # the open breaker did not call the model


@pytest.mark.parametrize(
    "raw",
    [
        "this is not json",
        json.dumps({"record_id": GOOD_ID, "summary": "x"}),
        json.dumps({"record_id": GOOD_ID, "summary": "", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1}),
        json.dumps({"record_id": GOOD_ID, "summary": "x", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1, "extra": 1}),
        json.dumps({"record_id": "DEV-OTHER", "summary": "x", "recommendation": "y", "outcome": "RECOMMEND_ONLY", "source_count": 1}),
    ],
)
def test_schema_failure_returns_hold_for_review_with_no_text(client, fake_model, raw):
    fake_model(raw=raw)
    response = recommend(client)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(body)
    assert "failmode.schema_failure" in body["reasons"]


def _with_sentinel_ip(monkeypatch):
    real = domain_service.load_record(GOOD_ID)
    row = {**real, "mgmt_ip": SENTINEL_IP}
    monkeypatch.setattr(domain_service, "load_record", lambda record_id: dict(row))
    return row


def test_forbidden_value_in_prompt_is_blocked_and_not_logged(client, fake_model, monkeypatch, audit_log):
    _with_sentinel_ip(monkeypatch)
    real_build = ai_gateway.build_prompt
    monkeypatch.setattr(ai_gateway, "build_prompt", lambda record: real_build(record) + "\nnote: " + SENTINEL_IP)
    model = fake_model()
    response = recommend(client)
    assert response.status_code == 403
    body = response.json()
    assert body["outcome"] == "BLOCK"
    assert_no_text(body)
    assert "failmode.forbidden_field_in_prompt" in body["reasons"]
    assert model.calls == 0
    assert SENTINEL_IP not in response.text
    assert SENTINEL_IP not in audit_log.path.read_text(encoding="utf-8")


def test_forbidden_value_in_the_answer_is_held_with_no_text(client, fake_model, monkeypatch, audit_log):
    _with_sentinel_ip(monkeypatch)
    model = fake_model(summary=f"The management address is {SENTINEL_IP}.")
    response = recommend(client)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(body)
    assert body["reasons"] == ["failmode.forbidden_field_in_prompt"]
    assert model.calls == 1
    assert SENTINEL_IP not in response.text
    text = audit_log.path.read_text(encoding="utf-8")
    assert SENTINEL_IP not in text
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.hold"]
    assert rows[0]["outcome"] == "HOLD_FOR_REVIEW"
    assert "failmode" not in text


def test_a_forbidden_field_name_in_the_answer_is_held_with_no_text(client, fake_model):
    fake_model(recommendation="Check the credential_profile first")
    body = recommend(client).json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert_no_text(body)
    assert body["reasons"] == ["failmode.forbidden_field_in_prompt"]


def test_roles_without_a_recommend_row_get_403(client, fake_model, audit_log):
    model = fake_model()
    for headers in (ADMIN, {"X-User-Role": "clinician"}, {"X-User-Role": "customer_support"}, {}):
        response = recommend(client, headers=headers)
        assert response.status_code == 403
        assert response.json() == {"error": "forbidden"}
    assert model.calls == 0
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.deny"] * 4
    assert rows[-1]["role"] is None


@pytest.mark.parametrize("headers", [OPERATOR, ENGINEER, {"X-User-Role": "ai_agent"}])
def test_roles_with_a_recommend_row_reach_the_model(client, headers):
    response = recommend(client, headers=headers)
    assert response.status_code == 202
    assert response.json()["recommendation"] == SENTENCE
