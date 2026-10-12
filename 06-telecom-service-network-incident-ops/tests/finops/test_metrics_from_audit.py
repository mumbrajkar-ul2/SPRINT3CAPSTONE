"""FinOps metrics from the audit log. Stage S04-12 Half B."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import ai_gateway, audit

SCRIPT = Path(__file__).resolve().parents[2] / "docs" / "12-finops" / "metrics_from_audit.py"

client = TestClient(app)


def _load():
    # The folder name has a hyphen, so the script is loaded by path.
    import importlib.util

    spec = importlib.util.spec_from_file_location("metrics_from_audit", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


metrics = _load()


def _row(**values):
    base = {
        "ts": "2026-10-11T00:00:00",
        "correlation_id": "c-1",
        "actor": "noc_operator",
        "role": "operator",
        "action": "ai.summary",
        "resource": "resource.device",
        "policy_decision": None,
        "approval_id": None,
        "model": "local-sim-v1",
        "model_version": "local-sim-v1",
        "prompt_hash": "abc",
        "tokens": 90,
        "latency_ms": 10,
        "outcome": "RECOMMEND_ONLY",
        "token_estimate_method": "word_count_x2_EDUCATIONAL",
    }
    base.update(values)
    return base


def _held(**values):
    return _row(
        action="policy.hold",
        model=None,
        model_version=None,
        prompt_hash=None,
        tokens=None,
        latency_ms=None,
        outcome="HOLD_FOR_REVIEW",
        token_estimate_method=None,
        **values,
    )


def test_the_token_method_word_is_the_one_the_playbook_names():
    assert ai_gateway.ESTIMATE_METHOD == "word_count_x2_EDUCATIONAL"


def test_a_model_call_row_carries_the_method_and_a_held_row_does_not(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)
    ok = client.post("/ai/summarize/REC-0001", headers={"X-User-Role": "operator"})
    held = client.post("/ai/summarize/DEV-BAD1", headers={"X-User-Role": "operator"})
    assert ok.status_code == 200
    assert held.status_code == 202
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    first, second = rows
    assert first["action"] == "ai.summary"
    assert first["token_estimate_method"] == "word_count_x2_EDUCATIONAL"
    assert isinstance(first["tokens"], int) and isinstance(first["latency_ms"], int)
    assert second["action"] == "policy.hold"
    assert second["tokens"] is None and second["latency_ms"] is None
    assert second["token_estimate_method"] is None
    # The response body keeps its old shape. The method is an audit field only.
    assert "token_estimate_method" not in ok.json()


def test_method_is_dropped_when_tokens_is_null(tmp_path, monkeypatch):
    path = tmp_path / "audit.log"
    monkeypatch.setattr(audit, "LOG", path)
    audit.write_event(
        "policy.hold",
        correlation_id="x",
        actor=None,
        role=None,
        resource="resource.device",
        token_estimate_method="word_count_x2_EDUCATIONAL",
    )
    assert json.loads(path.read_text(encoding="utf-8"))["token_estimate_method"] is None


def test_held_rows_are_counted_apart_and_do_not_lower_the_mean():
    rows = [_row(tokens=100, correlation_id="a"), _row(tokens=200, correlation_id="b"), _held(), _held()]
    result = metrics.compute(rows, 1.0)
    assert result["row_counts"]["model_call"] == 2
    assert result["row_counts"]["held_no_call"] == 2
    assert result["tokens_per_invocation"]["mean"] == 150
    assert result["tokens_per_invocation"]["calls"] == 2
    assert result["recommendation_latency"]["calls"] == 2


def test_a_row_with_no_tokens_that_is_not_held_is_its_own_kind():
    legacy = _row(model=None, tokens=None, latency_ms=None, token_estimate_method=None)
    old = {"ts": "t", "action": "ai.summary", "details": {"record_id": "R", "model": "local-sim-v1"}}
    result = metrics.compute([legacy, old, _row()], 1.0)
    counts = result["row_counts"]
    assert counts["no_token_row"] == 1
    assert counts["old_three_key_shape"] == 1
    assert counts["model_call"] == 1
    assert counts["held_no_call"] == 0


def test_cost_per_chain_uses_the_rate_and_groups_by_correlation_id():
    rows = [
        _row(tokens=1000, correlation_id="a"),
        _row(tokens=3000, correlation_id="a"),
        _row(tokens=2000, correlation_id="b"),
    ]
    result = metrics.compute(rows, 2.0)
    chain = result["cost_per_correlation_id"]
    assert chain["chains"] == 2
    assert chain["total"] == pytest.approx(12.0)  # 6000 tokens at 2.0 per 1000
    assert chain["max"] == pytest.approx(8.0)  # chain a: 4000 tokens
    assert chain["mean"] == pytest.approx(6.0)


def test_the_rate_comes_from_settings_and_a_bad_value_gives_the_default(monkeypatch):
    monkeypatch.setenv(metrics.RATE_ENV, "2.5")
    assert metrics.load_rate() == 2.5
    for bad in ("", "abc", "0", "-1", "nan"):
        monkeypatch.setenv(metrics.RATE_ENV, bad)
        assert metrics.load_rate() == metrics.DEFAULT_RATE
    monkeypatch.delenv(metrics.RATE_ENV)
    assert metrics.load_rate() == 1.0


def test_latency_percentiles_and_outcome_split():
    rows = [_row(latency_ms=value, correlation_id=f"c{value}") for value in range(1, 21)]
    rows.append(_row(latency_ms=500, outcome="HOLD_FOR_REVIEW", action="policy.hold", correlation_id="slow"))
    result = metrics.compute(rows, 1.0)
    latency = result["recommendation_latency"]
    assert latency["calls"] == 21
    assert latency["max"] == 500
    assert latency["p95"] == 20  # nearest rank: ceil(21 * 0.95) = 20th value of 1..20 then 500
    assert latency["by_outcome"]["HOLD_FOR_REVIEW"]["calls"] == 1
    assert latency["by_outcome"]["RECOMMEND_ONLY"]["calls"] == 20


def test_outcome_counts_name_all_four_words_and_unknown_words_are_kept_apart():
    rows = [_row(), _held(), _row(outcome="BLOCK", action="policy.deny", model=None, tokens=None), _row(outcome="MAYBE")]
    result = metrics.compute(rows, 1.0)
    assert result["ai_outcome_count"] == {"RECOMMEND_ONLY": 1, "HOLD_FOR_REVIEW": 1, "BLOCK": 1, "EXECUTE": 0}
    assert result["outcome_other_words"] == {"MAYBE": 1}


def test_the_two_metrics_with_no_audit_source_are_named_as_gaps():
    result = metrics.compute([_row()], 1.0)
    assert result["no_audit_source"] == ["metric.quarantine_rate", "metric.retry_count"]


def test_an_empty_log_gives_unknown_and_not_zero(tmp_path, capsys):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    assert metrics.main(["--log", str(path)]) == 0
    text = capsys.readouterr().out
    assert "Unknown" in text
    result = metrics.compute([], 1.0)
    assert result["tokens_per_invocation"] is None
    assert result["recommendation_latency"] is None


def test_every_printed_metric_line_has_a_label(tmp_path, capsys):
    path = tmp_path / "audit.log"
    path.write_text("\n".join(json.dumps(r) for r in [_row(), _held()]) + "\nnot json\n", encoding="utf-8")
    assert metrics.main(["--log", str(path)]) == 0
    text = capsys.readouterr().out
    assert "lines not JSON                 : 1" in text
    table = text.split("metric id", 1)[1].splitlines()[2:]
    for line in table:
        if line.startswith("metric."):
            assert any(label in line for label in ("EDUCATIONAL", "REAL", "Unknown", "gap")), line


def test_json_output_parses(tmp_path, capsys):
    path = tmp_path / "audit.log"
    path.write_text(json.dumps(_row()) + "\n", encoding="utf-8")
    assert metrics.main(["--log", str(path), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["tokens_per_invocation"]["mean"] == 90
    assert data["rate_edu_units_per_1k_tokens"] == 1.0


def test_repeat_prompt_calls_are_counted_from_prompt_hash():
    rows = [
        _row(prompt_hash="h1", tokens=90, correlation_id="a"),
        _row(prompt_hash="h1", tokens=90, correlation_id="b"),
        _row(prompt_hash="h1", tokens=90, correlation_id="c"),
        _row(prompt_hash="h2", tokens=64, correlation_id="d"),
        _held(),
    ]
    repeat = metrics.compute(rows, 1.0)["repeat_prompt_calls"]
    assert repeat["model_calls_with_hash"] == 4
    assert repeat["distinct_hashes"] == 2
    assert repeat["repeat_calls"] == 2
    assert repeat["tokens_in_repeat_calls"] == 180
