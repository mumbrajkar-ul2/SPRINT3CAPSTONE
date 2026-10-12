# Dependency and Supply Chain Risk Register

The full register is now in `docs/07-cicd/dependency-risk-register.md` (stage S04-07). That file lists every pinned and unpinned package, the lockfile state, and the risk if a version changes. The three rows below stay as the original starting point.

| Package | Current Concern | Transformation Target | Now in |
|---|---|---|---|
| fastapi | version pinned but no SBOM | Generate SBOM and vulnerability evidence | DR-01; plan in `docs/07-cicd/sbom-recommendation.md` |
| legacy scripts | no provenance | checksum and ownership metadata | DR-12 |
| frontend dependencies | scaffold only | add lockfile discipline when expanded | DR-11 |
