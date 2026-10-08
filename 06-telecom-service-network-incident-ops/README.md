# Telecommunications: Service Provisioning, Network & Incident Operations

This is an independent brownfield enterprise system repository. It combines modern code, legacy scripts, data-quality issues, security weaknesses, incomplete tests, operational gaps, and AI governance debt.

## Centre of Gravity

Scale + observability + automation safety + reliability

## Quick Start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
python etl/run_daily_batch.py --sample
uvicorn apps/api.main:app --reload
```

The Angular portal is represented as a lightweight scaffold under `apps/web/` with components, services, route definitions, forms, and Playwright tests. It is deliberately not fully wired, so participants can modernize it without fighting framework setup.

## Synthetic Data

All data is local and synthetic under `data/`. No external services are required.

## Transformation Spine

1. Understand Existing Repo
2. Establish Behavioural Baseline
3. Identity & Least Privilege
4. Secrets & Encryption
5. Infrastructure as Code
6. Policy as Code
7. CI/CD & Supply Chain
8. Observability & Traceability
9. AI Security & Guardrails
10. Performance & Scalability
11. Reliability & Failure Engineering
12. Cost & AI FinOps
13. Automated Security Validation
14. Auditability & Compliance Evidence
15. Production Readiness Gate
16. Production Evidence Pack

