"""FastAPI application for the governed telecom incident demo."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .services import (
    ai_gateway,
    alarm_service,
    approvals,
    audit,
    audit_query,
    domain_service,
    policy,
)

app = FastAPI(title="Governed telecom incident application")

ALLOWED = {
    "record": {"operator", "engineer", "ai_agent"},
    "storm": {"operator", "engineer"},
    "summarize": {"operator", "ai_agent"},
    "recommend": {"operator", "engineer", "ai_agent"},
    "approve": {"operator"},
    "audit": {"admin"},
}


def _role(request: Request) -> str | None:
    value = request.headers.get("X-User-Role")
    return value.strip() if value and value.strip() else None


def _correlation(request: Request) -> str:
    return request.state.correlation_id


def _error(text: str, status: int, **extra: Any) -> JSONResponse:
    return JSONResponse({"error": text, **extra}, status_code=status)


def _write_or_error(action: str, request: Request, resource: str, **values: Any) -> JSONResponse | None:
    try:
        audit.write_event(
            action,
            correlation_id=_correlation(request),
            role=_role(request),
            resource=resource,
            **values,
        )
    except OSError:
        return _error("audit log unwritable", 500)
    return None


def _deny(request: Request, resource: str, record_id: str | None = None) -> JSONResponse:
    failed = _write_or_error("policy.deny", request, resource, record_id=record_id)
    return failed or _error("forbidden", 403)


def _allowed(request: Request, route: str) -> bool:
    return _role(request) in ALLOWED[route]


@app.middleware("http")
async def correlation_header(request: Request, call_next):
    sent = request.headers.get("X-Correlation-Id", "").strip()
    request.state.correlation_id = sent if sent and len(sent) <= 128 else str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = request.state.correlation_id
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    checks = {
        "devices.csv": (domain_service.DATA_DIR / domain_service.DEVICES).is_file(),
        "alarms.csv": (alarm_service.DATA_DIR / alarm_service.ALARMS).is_file(),
        "audit log": _audit_writable(),
        "policy": bool(policy.ACCESS.get("grants")),
    }
    status = 200 if all(checks.values()) else 503
    return JSONResponse({"runbook_level": "Degraded" if status == 503 else "ok", "checks": checks}, status_code=status)


def _audit_writable() -> bool:
    path = audit.LOG
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8"):
            pass
        return True
    except OSError:
        return False


@app.get("/records/{record_id}")
def read_record(record_id: str, request: Request):
    if not _allowed(request, "record"):
        return _deny(request, "resource.device", record_id)
    try:
        record = domain_service.load_record(record_id)
    except FileNotFoundError:
        return _error("data file missing", 500)
    if record is None:
        return _error("not_found", 404)
    failed = _write_or_error("record.read", request, "resource.device", record_id=record_id)
    if failed:
        return failed
    if _role(request) != "engineer":
        record.pop("mgmt_ip", None)
        record.pop("credential_profile", None)
    return record


@app.get("/alarms/storms/{storm_batch_id}")
def read_storm(storm_batch_id: str, request: Request):
    if not _allowed(request, "storm"):
        return _deny(request, "resource.alarm")
    try:
        result = alarm_service.read_storm(storm_batch_id)
    except FileNotFoundError:
        return _error("data file missing", 500)
    if result is None:
        return _error("not_found", 404)
    failed = _write_or_error("record.storm_read", request, "resource.alarm")
    return failed or result


def _ai_body(
    record_id: str,
    request: Request,
    outcome: str,
    *,
    summary: str | None = None,
    recommendation: str | None = None,
    reasons: list[str],
    approval_required: bool,
    source_count: int = 0,
    provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    provenance = provenance or {}
    return {
        "record_id": record_id,
        "summary": summary,
        "recommendation": recommendation,
        "outcome": outcome,
        "model": provenance.get("model"),
        "model_version": provenance.get("model_version"),
        "prompt_hash": provenance.get("prompt_hash"),
        "tokens": provenance.get("tokens"),
        "latency_ms": provenance.get("latency_ms"),
        "source_count": source_count,
        "guardrail_status": "enforced",
        "approval_required": approval_required,
        "policy_result": "allow",
        "approval_id": None,
        "correlation_id": _correlation(request),
        "reasons": reasons,
    }


def _audit_ai(body: dict[str, Any], request: Request, action: str) -> JSONResponse | None:
    return _write_or_error(
        action,
        request,
        "resource.device",
        model=body["model"],
        model_version=body["model_version"],
        prompt_hash=body["prompt_hash"],
        tokens=body["tokens"],
        latency_ms=body["latency_ms"],
        outcome=body["outcome"],
        token_estimate_method=ai_gateway.ESTIMATE_METHOD if body["tokens"] is not None else None,
        record_id=body["record_id"],
    )


def _pre_model(record_id: str, request: Request, route: str) -> tuple[dict[str, str] | None, JSONResponse | None]:
    if not _allowed(request, route):
        return None, _deny(request, "resource.device", record_id)
    try:
        record = domain_service.load_record(record_id)
    except FileNotFoundError:
        return None, _error("data file missing", 500)
    if record is None:
        body = _ai_body(
            record_id,
            request,
            "BLOCK",
            reasons=["failmode.missing_id"],
            approval_required=route == "recommend",
        )
        failed = _audit_ai(body, request, "policy.deny")
        return None, failed or JSONResponse(body, status_code=403)
    stale = record.get("stale_topology_flag", "")
    if stale == "true":
        body = _ai_body(
            record_id,
            request,
            "BLOCK",
            reasons=["failmode.stale_topology_true"],
            approval_required=route == "recommend",
        )
        failed = _audit_ai(body, request, "policy.deny")
        return None, failed or JSONResponse(body, status_code=403)
    if not stale.strip():
        body = _ai_body(
            record_id,
            request,
            "HOLD_FOR_REVIEW",
            reasons=["failmode.stale_topology_blank"],
            approval_required=route == "recommend",
        )
        failed = _audit_ai(body, request, "policy.hold")
        return None, failed or JSONResponse(body, status_code=202)
    return record, None


def _model_route(record_id: str, request: Request, route: str):
    record, stopped = _pre_model(record_id, request, route)
    if stopped:
        return stopped
    assert record is not None
    result = ai_gateway.run(record)
    provenance = {name: result.get(name) for name in ("model", "model_version", "prompt_hash", "tokens", "latency_ms")}
    if result["kind"] == "ok":
        answer = result["answer"]
        if answer["outcome"] == "EXECUTE":
            outcome, reasons, status, action = "BLOCK", ["rule.ai_output_cannot_execute"], 403, "policy.deny"
            summary = recommendation = None
        else:
            outcome = "RECOMMEND_ONLY" if route == "summarize" else "HOLD_FOR_REVIEW"
            reasons = ["ai_use.incident_summary" if route == "summarize" else "ai_use.next_action_recommendation"]
            status = 200 if route == "summarize" else 202
            action = "ai.summary" if route == "summarize" else "ai.recommendation"
            summary, recommendation = answer["summary"], answer["recommendation"]
        body = _ai_body(
            record_id,
            request,
            outcome,
            summary=summary,
            recommendation=recommendation,
            reasons=reasons,
            approval_required=route == "recommend",
            source_count=answer["source_count"],
            provenance=provenance,
        )
    else:
        mapping = {
            "prompt_forbidden": ("BLOCK", "failmode.forbidden_field_in_prompt", 403, "policy.deny"),
            "timeout": ("HOLD_FOR_REVIEW", "failmode.timeout", 202, "policy.hold"),
            "unreachable": ("HOLD_FOR_REVIEW", "failmode.model_unreachable", 202, "policy.hold"),
            "schema_failure": ("HOLD_FOR_REVIEW", "failmode.schema_failure", 202, "policy.hold"),
            "answer_forbidden": ("HOLD_FOR_REVIEW", "failmode.forbidden_field_in_prompt", 202, "policy.hold"),
            "command_text": ("HOLD_FOR_REVIEW", "failmode.command_text_in_recommendation", 202, "policy.hold"),
        }
        outcome, reason, status, action = mapping[result["kind"]]
        body = _ai_body(
            record_id,
            request,
            outcome,
            reasons=[reason],
            approval_required=route == "recommend",
            provenance=provenance,
        )
    failed = _audit_ai(body, request, action)
    return failed or JSONResponse(body, status_code=status)


@app.post("/ai/summarize/{record_id}")
def summarize(record_id: str, request: Request):
    return _model_route(record_id, request, "summarize")


@app.post("/ai/recommend/{record_id}")
def recommend(record_id: str, request: Request):
    return _model_route(record_id, request, "recommend")


def _recommendation_was_shown(correlation_id: str, record_id: str) -> bool:
    rows, _ = audit.read_lines()
    return any(
        row.get("correlation_id") == correlation_id
        and row.get("record_id") == record_id
        and row.get("action") == "ai.recommendation"
        for row in rows
    )


@app.post("/approvals/{record_id}")
async def approve(record_id: str, request: Request):
    if not _allowed(request, "approve"):
        return _deny(request, "resource.ai_invocation", record_id)
    correlation_id = _correlation(request)
    if not _recommendation_was_shown(correlation_id, record_id):
        return _error("not_found", 404)
    try:
        payload = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return _error("input_invalid", 422)
    if not isinstance(payload, dict) or type(payload.get("decision")) is not str or payload["decision"] not in {"yes", "no"}:
        return _error("input_invalid", 422)
    decision = payload["decision"]
    approval_id = approvals.make_id() if decision == "yes" else None
    record = {
        "approval_id": approval_id,
        "decision": decision,
        "approver": "persona.noc_operator",
        "record_id": record_id,
        "correlation_id": correlation_id,
    }
    failed = _write_or_error(
        "ai.approval",
        request,
        "resource.ai_invocation",
        approval_id=approval_id,
        record_id=record_id,
    )
    if failed:
        return failed
    try:
        approvals.append(record)
    except OSError:
        return _error("audit log unwritable", 500)
    return record


@app.get("/audit/{correlation_id}")
def read_audit(correlation_id: str, request: Request):
    if not _allowed(request, "audit"):
        return _deny(request, "resource.audit_log")
    if len(correlation_id) > audit_query.MAX_ID_LENGTH:
        failed = _write_or_error("audit.id_refused", request, "resource.audit_log")
        return failed or _error("id_too_long", 400, max_length=audit_query.MAX_ID_LENGTH)
    case = audit_query.read_case(correlation_id)
    if not case.rows:
        failed = _write_or_error("audit.not_found", request, "resource.audit_log")
        return failed or _error("not_found", 404)
    failed = _write_or_error("audit.read", request, "resource.audit_log")
    if failed:
        return failed
    shown_id = audit_query.WITHHELD if any(name in correlation_id for name in audit_query.FORBIDDEN_NAMES) else correlation_id
    return {
        "correlation_id": shown_id,
        "row_count": len(case.rows),
        "rows": case.rows,
        "cannot_prove": audit_query.cannot_prove(case),
    }


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Governed telecom incident application</title></head>
<body>
<h1>Topology lookup to AI recommendation</h1>
<p>Role sent: operator. The role is a claimed role. The audit result lists caller_identity under cannot_prove.</p>
<label>Storm batch id <input id="storm" value="STO-00002"></label>
<label>Device id <select id="device"></select></label>
<label>Decision <select id="decision"><option>yes</option><option>no</option></select></label>
<button id="run">Run the demo flow</button>
<ol>
<li>Pick a storm. Read raw count (REAL), deduped count (REAL), flagged count (REAL), and alarm ids (REAL).</li>
<li>Look up a device from rows and held_aside.</li>
<li>Ask for a recommendation. Tokens are EDUCATIONAL. Latency in milliseconds is SIMULATED.</li>
<li>Record a yes or no decision. A person must review HOLD_FOR_REVIEW or BLOCK. A held reply shows the reason and hides the model text.</li>
<li>Read the audit chain and its cannot_prove list. Row count is REAL.</li>
</ol>
<p>Health HTTP status is REAL. Reply HTTP status is REAL. Calls per outcome are REAL. EXECUTE is 0 (REAL).</p>
<pre id="result"></pre>
<script>
const result = document.getElementById("result");
const device = document.getElementById("device");
async function call(path, options, correlation) {
  const response = await fetch(path, {
    ...options,
    headers: {"X-User-Role": options.role, "X-Correlation-Id": correlation, "Content-Type": "application/json"}
  });
  return {status: response.status, body: await response.json()};
}
document.getElementById("run").onclick = async () => {
  const correlation = crypto.randomUUID();
  const storm = await call("/alarms/storms/" + document.getElementById("storm").value, {role: "operator"}, correlation);
  const ids = [...storm.body.rows, ...storm.body.held_aside].map(row => row.device_id).filter(Boolean);
  device.replaceChildren(...[...new Set(ids)].map(id => new Option(id, id)));
  const id = device.value;
  const lookup = await call("/records/" + id, {role: "operator"}, correlation);
  const recommend = await call("/ai/recommend/" + id, {method: "POST", role: "operator"}, correlation);
  let decide = {status: 404, body: {error: "not_found"}};
  if (recommend.body.summary && recommend.body.recommendation) {
    decide = await call("/approvals/" + id, {
      method: "POST", role: "operator", body: JSON.stringify({decision: document.getElementById("decision").value})
    }, correlation);
  }
  const chain = await call("/audit/" + correlation, {role: "admin"}, crypto.randomUUID());
  result.textContent = JSON.stringify({storm, lookup, recommend, decide, chain}, null, 2);
};
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def page():
    return PAGE
