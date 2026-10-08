# AI FDE Brownfield Repositories v2 — Validation Report

## Sanity checks completed

- All four repositories pass the repository self-check.
- All four repositories pass 13 pytest tests each.
- Python source trees compile successfully.
- Local SQLite bootstrap completes successfully.
- Baseline ETL jobs execute successfully.
- JSON assets parse successfully.
- CSV files were checked for rectangular structure.
- Local Angular-to-FastAPI CORS preflight is covered by a test.
- Angular project scaffolding, Playwright smoke-test assets, FastAPI health/readiness/metrics, PostgreSQL-oriented SQL, ETL, legacy adapters, observability starters, and synthetic data are included.
- Transient databases, pytest caches and Python bytecode were removed before packaging.

## Important design intent

The repositories are runnable baselines, not clean reference implementations. Deliberate brownfield debt remains for discovery and transformation: mixed-generation patterns, weak legacy authorization, partial migrations, inconsistent rules, selected data-quality/integrity anomalies, legacy batch assumptions, incomplete release practices, and thin observability. These are transformation targets rather than packaging defects.

## Packages

### 01-bfsi-lending-aml-servicing
- Files: 74
- Synthetic CSV rows: 26,880
- ZIP size: 0.43 MB
- SHA-256: `72da95b0e4198490a3d6b64e582ebe54bde96abbd2f6f375c0980edcf3d99d6f`

### 02-smart-manufacturing-quality-maintenance
- Files: 73
- Synthetic CSV rows: 37,480
- ZIP size: 0.45 MB
- SHA-256: `c04678b7a89514bdc2e6237c62a4045388c08a411aee6d328de5d0b90d6d8898`

### 03-life-sciences-clinical-safety-quality
- Files: 73
- Synthetic CSV rows: 18,880
- ZIP size: 0.18 MB
- SHA-256: `f08b82e44f1310572742ea8ee757e59787b48db385ef5483780a1044e791804b`

### 04-energy-utilities-asset-outage-field
- Files: 73
- Synthetic CSV rows: 30,180
- ZIP size: 0.37 MB
- SHA-256: `a01991876a530b41e553a9285d11c896218356f87bf0b6bd796b1a688d9fb2ca`
