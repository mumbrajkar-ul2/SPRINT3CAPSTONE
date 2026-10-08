# Observability Baseline

Current state:
- health endpoint exists
- audit log exists but lacks actor, tenant, correlation id, model input hash, approval id
- no distributed tracing
- no SLOs
- no dashboard as code

Transformation target:
- correlation from user request to data access to AI invocation to human approval to final action
- RED/USE metrics for services
- AI metrics: token count, latency, model version, fallback reason, guardrail result
