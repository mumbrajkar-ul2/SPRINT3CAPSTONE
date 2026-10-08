from fastapi import FastAPI, Header
from apps.api.services import domain_service, ai_gateway, audit

app = FastAPI(title="Telecommunications: Service Provisioning, Network & Incident Operations")

@app.get("/health")
def health():
    return {"status":"ok","repo":"06-telecom-service-network-incident-ops"}

@app.get("/records/{record_id}")
def get_record(record_id: str, x_user_role: str = Header(default="operator")):
    # Brownfield issue: role check is broad and facility/tenant context is ignored.
    if x_user_role in ["admin", "operator", "clinician", "engineer", "ai_agent"]:
        result = domain_service.load_record(record_id)
        audit.write_event("record.read", {"record_id": record_id, "role": x_user_role})
        return result
    return {"error":"forbidden"}

@app.post("/ai/summarize/{record_id}")
def ai_summary(record_id: str):
    record = domain_service.load_record(record_id)
    summary = ai_gateway.summarize_record(record)
    audit.write_event("ai.summary", {"record_id": record_id, "model":"local-sim-v1"})
    return summary
