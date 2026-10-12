from typing import Optional

from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from apps.api.services import domain_service, ai_gateway, audit, policy

app = FastAPI(title="Telecommunications: Service Provisioning, Network & Incident Operations")

RESOURCE_DEVICE = "resource.device"


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # First running hop. Keep X-Correlation-Id when it has text. Otherwise create a UUID.
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


def _audit(action, request: Request, role, outcome=None, provenance=None):
    """Write one audit row. `provenance` holds model, model_version, prompt_hash,
    tokens, latency_ms, and token_estimate_method when a model call ran.
    Otherwise those stay null."""
    word = _role_word(role)
    audit.write_event(
        action,
        correlation_id=request.state.correlation_id,
        actor=audit.actor_for_role(word),
        role=word,
        resource=RESOURCE_DEVICE,
        outcome=outcome,
        **(provenance or {}),
    )


# S04-09. The audit action and the HTTP status for each outcome the AI route can
# return. EXECUTE has no entry. The route never returns it.
AI_ROUTE_RESULT = {
    "RECOMMEND_ONLY": ("ai.summary", 200),
    "HOLD_FOR_REVIEW": ("policy.hold", 202),
    "BLOCK": ("policy.deny", 403),
}


@app.get("/health")
def health():
    return {"status":"ok","repo":"06-telecom-service-network-incident-ops"}

@app.get("/records/{record_id}")
def get_record(record_id: str, request: Request, x_user_role: str = Header(default="operator")):
    # S04-06: the policy decides. Role words not in the matrix get 403 and an audit row.
    # Still open for S07: facility and tenant context are ignored.
    # Still open for S04-03: a missing header still means "operator".
    role_id = policy.role_id_from_header(x_user_role)
    decision = policy.check_record_read(role_id)
    if not decision["allow"]:
        _audit("policy.deny", request, x_user_role)
        return JSONResponse(status_code=403, content={"error": "forbidden"})
    result = domain_service.load_record(record_id)
    _audit("record.read", request, x_user_role)
    return result

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
        _audit("policy.deny", request, x_user_role)
        return JSONResponse(status_code=403, content={"error": "forbidden"})
    record = domain_service.load_record(record_id)
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
    )
    return JSONResponse(
        status_code=status_code, content=result.to_body(request.state.correlation_id)
    )
