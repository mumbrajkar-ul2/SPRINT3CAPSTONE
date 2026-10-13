from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, Request
from fastapi.responses import FileResponse, JSONResponse
from apps.api.services import (
    ai_gateway,
    alarm_service,
    approvals,
    audit,
    audit_query,
    domain_service,
    policy,
)

app = FastAPI(title="Telecommunications: Service Provisioning, Network & Incident Operations")

RESOURCE_DEVICE = "resource.device"
RESOURCE_AUDIT_LOG = "resource.audit_log"
# Stage S07. The resources of the new routes (PRD RQ-15 and RQ-32).
RESOURCE_ALARM = "resource.alarm"
RESOURCE_AI_INVOCATION = "resource.ai_invocation"

# S05-14 Half B. The action words the audit route writes on its own row.
# policy.deny already exists. The other three are PROPOSED.
# Open question for S03: the YAML has no id for audit.read, audit.not_found, or audit.id_refused.
AUDIT_READ = "audit.read"
AUDIT_NOT_FOUND = "audit.not_found"
AUDIT_ID_REFUSED = "audit.id_refused"

# Stage S07. The action words of the three new rows. ADR 0005 gives each an id.
STORM_READ = "record.storm_read"
AI_RECOMMENDATION = "ai.recommendation"
AI_APPROVAL = "ai.approval"

STATIC_DIR = Path(__file__).resolve().parent / "static"


class AuditUnwritable(Exception):
    """The audit row could not be written. The route returns HTTP 500 with no data (RQ-37, RQ-56)."""


@app.exception_handler(AuditUnwritable)
async def audit_unwritable_handler(request: Request, exc: AuditUnwritable):
    # The words are the value of status.code.fault.audit_log_unwritable.
    return JSONResponse(status_code=500, content={"error": "audit log unwritable"})


@app.exception_handler(FileNotFoundError)
async def data_file_missing_handler(request: Request, exc: FileNotFoundError):
    # The words are the value of status.code.fault.data_file_missing. /health stays 200 (RQ-14).
    return JSONResponse(status_code=500, content={"error": "data file missing"})


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # First running hop. Keep X-Correlation-Id when it has text and is at most 128 characters.
    # Otherwise create a UUID (RQ-49 and RQ-69).
    correlation_id = audit.correlation_id_from_header(request.headers.get("x-correlation-id"))
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-Id"] = correlation_id
    return response


def _role_word(value):
    """The role string the route used. None when the header was missing or blank."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _audit(
    action,
    request: Request,
    role,
    outcome=None,
    provenance=None,
    resource=RESOURCE_DEVICE,
    record_id=None,
    approval_id=None,
):
    """Write one audit row. `provenance` holds model, model_version, prompt_hash,
    tokens, latency_ms, and token_estimate_method when a model call ran.
    Otherwise those stay null. `resource` is resource.device unless the caller
    names another one. `record_id` is the device id the caller asked for, or None.

    If the row cannot be written, this raises AuditUnwritable. Every caller writes
    its row before it changes state or returns data (RQ-36, RQ-37, RQ-56).
    """
    word = _role_word(role)
    try:
        audit.write_event(
            action,
            correlation_id=request.state.correlation_id,
            actor=audit.actor_for_role(word),
            role=word,
            resource=resource,
            outcome=outcome,
            record_id=record_id,
            approval_id=approval_id,
            **(provenance or {}),
        )
    except Exception as err:  # noqa: BLE001  any failure to write means the case is not on record
        raise AuditUnwritable() from err


def _forbidden():
    return JSONResponse(status_code=403, content={"error": "forbidden"})


def _not_found():
    return JSONResponse(status_code=404, content={"error": "not_found"})


# S04-09. The audit action and the HTTP status for each outcome the summarize route can
# return. EXECUTE has no entry. The route never returns it.
AI_ROUTE_RESULT = {
    "RECOMMEND_ONLY": ("ai.summary", 200),
    "HOLD_FOR_REVIEW": ("policy.hold", 202),
    "BLOCK": ("policy.deny", 403),
}


@app.get("/", include_in_schema=False)
def page():
    # S07 (RQ-62). One served page that walks the demo flow. It sends the role header the person picks.
    return FileResponse(STATIC_DIR / "index.html", media_type="text/html")


@app.get("/health")
def health():
    return {"status":"ok","repo":"06-telecom-service-network-incident-ops"}


def _audit_log_writable() -> bool:
    try:
        audit.LOG.parent.mkdir(exist_ok=True)
        with audit.LOG.open("a", encoding="utf-8"):
            pass
        return True
    except OSError:
        return False


@app.get("/ready")
def ready():
    # S07 (RQ-73). Four checks. One failure gives 503. /health stays 200 in every case.
    # The status words are existing ones: status.code.health.ok and
    # status.code.runbook_level.degraded. Open question for S03: a status id for this body.
    checks = {
        "devices_csv": (domain_service.DATA_DIR / domain_service.PRIMARY).is_file(),
        "alarms_csv": (alarm_service.DATA_DIR / alarm_service.ALARMS).is_file(),
        "audit_log_writable": _audit_log_writable(),
        "policy_loaded": bool(policy.POLICY_VERSION) and policy.check_record_read("role.operator")["allow"],
    }
    healthy = all(checks.values())
    return JSONResponse(
        status_code=200 if healthy else 503,
        content={"status": "ok" if healthy else "Degraded", "checks": checks},
    )


@app.get("/records/{record_id}")
def get_record(record_id: str, request: Request, x_user_role: Optional[str] = Header(default=None)):
    # S04-06: the policy decides. A role word not in the matrix gets 403 and an audit row.
    # S07 (RQ-68): a missing header has no role and gets 403 too. The server no longer fills in "operator".
    # S07 (RQ-03): an id with no device row gets 404. The route never returns another row.
    # S07 (RQ-05, RQ-06): mgmt_ip and credential_profile go only to the role with row TA-15.
    # Still open for S07 PRD gap: facility and tenant context are ignored (RK-12).
    role_id = policy.role_id_from_header(x_user_role)
    decision = policy.check_record_read(role_id)
    if not decision["allow"]:
        _audit("policy.deny", request, x_user_role, record_id=record_id)
        return _forbidden()
    result = domain_service.load_record(record_id)
    if result is None:
        return _not_found()
    if not policy.check_sensitive_read(role_id)["allow"]:
        result.pop("mgmt_ip", None)
        result.pop("credential_profile", None)
    _audit("record.read", request, x_user_role, record_id=record_id)
    return result


@app.get("/alarms/storms/{storm_batch_id}")
def get_storm(storm_batch_id: str, request: Request, x_user_role: Optional[str] = Header(default=None)):
    # S07 (RQ-08 to RQ-15). The route only reads. It opens no incident and changes no file.
    role_id = policy.role_id_from_header(x_user_role)
    access = policy.check_storm_read(role_id)
    if not access["allow"]:
        _audit("policy.deny", request, x_user_role, resource=RESOURCE_ALARM)
        return _forbidden()
    storm = alarm_service.read_storm(storm_batch_id)
    if storm is None:
        return _not_found()
    _audit(STORM_READ, request, x_user_role, resource=RESOURCE_ALARM)
    return storm


@app.post("/ai/summarize/{record_id}")
def ai_summary(record_id: str, request: Request, x_user_role: Optional[str] = Header(default=None)):
    # S04-06: the access check comes first. A missing header has no role and is denied.
    #    A denied caller gets 403 and an audit row. The record is not loaded.
    # S04-09: the gateway then runs the ai_action policy before the model and again
    #    before it returns. Every body past this point carries the policy outcome.
    #    BLOCK gives 403, HOLD_FOR_REVIEW gives 202, RECOMMEND_ONLY gives 200.
    #    A failed call has summary null. The route never returns EXECUTE.
    role_id = policy.role_id_from_header(x_user_role)
    access = policy.check_summarize(role_id)
    if not access["allow"]:
        _audit("policy.deny", request, x_user_role, record_id=record_id)
        return _forbidden()
    # S07: a missing id loads as None. An empty record makes the policy input record_found false,
    # so the call is BLOCK with failmode.missing_id and the model is not called.
    record = domain_service.load_record(record_id) or {}
    result = ai_gateway.summarize_record(
        record, record_id=record_id, role_id=role_id, access=access
    )
    audit_action, status_code = AI_ROUTE_RESULT[result.outcome]
    _audit(
        audit_action,
        request,
        x_user_role,
        outcome=result.outcome,
        provenance=result.audit_provenance(),
        record_id=record_id,
    )
    return JSONResponse(
        status_code=status_code, content=result.to_body(request.state.correlation_id)
    )


@app.post("/ai/recommend/{record_id}")
def ai_recommend(record_id: str, request: Request, x_user_role: Optional[str] = Header(default=None)):
    # S07 (RQ-18 to RQ-30, RQ-70, RQ-71). The same gateway as the summarize route.
    # Order: access policy, policy pre-flight, prompt allow list, model under the timeout and
    # the breaker, answer shape, answer content checks, policy again, audit row, reply.
    # This route never returns RECOMMEND_ONLY and never returns EXECUTE.
    #   HOLD_FOR_REVIEW with the sentence  202  audit action ai.recommendation
    #   HOLD_FOR_REVIEW with no text       202  audit action policy.hold
    #   BLOCK                              403  audit action policy.deny
    role_id = policy.role_id_from_header(x_user_role)
    access = policy.check_recommend(role_id)
    if not access["allow"]:
        _audit("policy.deny", request, x_user_role, record_id=record_id)
        return _forbidden()
    record = domain_service.load_record(record_id) or {}
    result = ai_gateway.recommend_record(
        record, record_id=record_id, role_id=role_id, access=access
    )
    if result.outcome == "HOLD_FOR_REVIEW":
        audit_action = AI_RECOMMENDATION if result.recommendation is not None else "policy.hold"
        status_code = 202
    else:
        # BLOCK. The gateway returns no other outcome. If it ever did, the route would still
        # refuse, and it would write no text (the body below is built from a BLOCK result).
        audit_action, status_code = "policy.deny", 403
        result.outcome, result.summary, result.recommendation = "BLOCK", None, None
    _audit(
        audit_action,
        request,
        x_user_role,
        outcome=result.outcome,
        provenance=result.audit_provenance(),
        record_id=record_id,
    )
    return JSONResponse(
        status_code=status_code, content=result.to_body(request.state.correlation_id)
    )


@app.post("/approvals/{record_id}")
async def post_approval(record_id: str, request: Request, x_user_role: Optional[str] = Header(default=None)):
    # S07 (RQ-32 to RQ-39). The only route that stores new state. Order of checks:
    #   1. Policy. Only role.operator (persona.noc_operator, TA-09) passes. 403 and a policy.deny row.
    #      The role check runs before the body check, so the body is read here and not by FastAPI.
    #   2. Body. One key, decision, with the word yes or no. Anything else is HTTP 422. Nothing is stored.
    #   3. A recommendation was shown with text under this correlation id (RQ-34). If not, HTTP 404.
    #   4. The audit row, written first. If it cannot be written, nothing is stored and the route gives 500.
    #   5. The approval record. If this fails, the audit row stays and no approval exists.
    # The caller sends no approver and no approval id. The server makes both (RQ-32, RQ-38).
    # The route runs no command and changes no device (RQ-39).
    role_id = policy.role_id_from_header(x_user_role)
    access = policy.check_approve(role_id)
    if not access["allow"]:
        _audit(
            "policy.deny", request, x_user_role, resource=RESOURCE_AI_INVOCATION, record_id=record_id
        )
        return _forbidden()

    try:
        payload = await request.json()
    except ValueError:
        payload = None
    decision = payload.get("decision") if isinstance(payload, dict) else None
    if not (isinstance(decision, str) and decision in approvals.DECISIONS):
        return JSONResponse(status_code=422, content={"detail": "decision must be the word yes or the word no"})

    correlation_id = request.state.correlation_id
    if not audit_query.recommendation_was_shown(correlation_id, record_id):
        return _not_found()

    approver = policy.persona_of(role_id)
    approval_id = approvals.new_approval_id() if decision == "yes" else None
    # The audit row comes first. For a yes it holds the id. For a no approval_id is null.
    _audit(
        AI_APPROVAL,
        request,
        x_user_role,
        resource=RESOURCE_AI_INVOCATION,
        record_id=record_id,
        approval_id=approval_id,
    )
    record = approvals.build_record(
        decision=decision,
        approver=approver,
        record_id=record_id,
        correlation_id=correlation_id,
        approval_id=approval_id,
    )
    try:
        approvals.store(record)
    except Exception:  # noqa: BLE001  any failure means no approval exists; the audit row stays (RQ-36)
        # The PRD names no body for this case. PROPOSED wording. Owner: Team-Force.
        return JSONResponse(status_code=500, content={"error": "approval not stored"})
    return {
        "approval_id": record["approval_id"],
        "decision": record["decision"],
        "approver": record["approver"],
        "record_id": record["record_id"],
        "correlation_id": correlation_id,
    }


@app.get("/audit/{correlation_id}")
def audit_case(correlation_id: str, request: Request, x_user_role: str | None = Header(default=None)):
    # S05-14. Read one case back from the audit log. This route only reads.
    # Order of checks:
    #   1. Policy (TA-35). Only role.admin passes. A missing header has no role and is denied.
    #      The 403 body is the same for an id that exists and an id that does not.
    #   2. Id length. An id over 128 characters is refused with 400 and is not looked up.
    #   3. Lookup. No rows for the id gives 404.
    # Every path writes its own audit row on resource.audit_log. The row is written
    # after the read, so the chain in the response does not include this request.
    role_id = policy.role_id_from_header(x_user_role)
    access = policy.check_audit_read(role_id)
    if not access["allow"]:
        _audit("policy.deny", request, x_user_role, resource=RESOURCE_AUDIT_LOG)
        return _forbidden()
    if len(correlation_id) > audit_query.MAX_ID_LENGTH:
        _audit(AUDIT_ID_REFUSED, request, x_user_role, resource=RESOURCE_AUDIT_LOG)
        return JSONResponse(
            status_code=400,
            content={"error": "id_too_long", "max_length": audit_query.MAX_ID_LENGTH},
        )
    case = audit_query.read_case(correlation_id)
    if not case.rows:
        _audit(AUDIT_NOT_FOUND, request, x_user_role, resource=RESOURCE_AUDIT_LOG)
        return _not_found()
    body = {
        "correlation_id": audit_query.withhold_forbidden(correlation_id)[0],
        "row_count": len(case.rows),
        "rows": case.rows,
        "cannot_prove": audit_query.cannot_prove(case),
    }
    _audit(AUDIT_READ, request, x_user_role, resource=RESOURCE_AUDIT_LOG)
    return body
