# Project Intent — Telecom Service, Network, and Incident Operations - Section 4.3


### 4.3 Constants found in the inherited repo

These values appear in the files. They are current-state values. They are not a new policy you chose. A later cutoff needs a named owner and an Architecture Decision Record. Until the packet or the trainer names a business owner, that owner is Team-Force, the FDE team Mangesh belongs to (`docs/00-contract/operating-contract.md` row 10).

| Constant | Value in the files | Where it appears |
|---|---|---|
| Primary data file for the API | `devices.csv` | `apps/api/services/domain_service.py` |
| Missing-record behaviour | return first row | `domain_service.py`, `tests/test_characterization.py` |
| Allowed API roles | `admin`, `operator`, `clinician`, `engineer`, `ai_agent` | `apps/api/main.py` |
| Domain personas | `noc_operator`, `network_engineer`, `field_engineer`, `customer_support`, `automation_service`, `vendor_account`, `ai_agent` | `docs/domain-specific-spec.md` |
| OPA allow rules | any `admin`; `operator` + `read` | `policy/opa/access.rego` |
| AI model version | `local-sim-v1` | `ai_gateway.py`, `main.py` audit event |
| AI prompt | `Summarize this operational record and recommend next action: {record}` | `ai_gateway.py` |
| Guardrail status returned | `not_enforced` | `ai_gateway.py` |
| Token estimate formula | `len(prompt.split()) * 2` | `ai_gateway.py` |
| Shared DB user / password | `app_shared` / `Welcome123` | `legacy/reconcile_legacy.py`, `.env.example` |
| Example AI key | `sk-workshop-hardcoded-example` | `.env.example` |
| CSV row counts | 354 each | `data/manifest.json`, `data/README.md` |
| Event count | 3000 | `data/manifest.json` |
| First key reused across tables | `REC-0001` | first row of each CSV |
| ADR 0001 status | Accepted, never revisited | `docs/ADR/0001-partial-modernization.md` |
| OpenAPI coverage | `/health` only | `data/contracts/openapi-fragment.yaml` |
| CI Python version | 3.11 | `.github/workflows/ci.yml` |

