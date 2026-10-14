# Pack path check

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 16, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | PASS. All 150 paths and test ids in `PRODUCTION_EVIDENCE_PACK.md` exist. 0 are missing. |
| Evidence sources | `PRODUCTION_EVIDENCE_PACK.md`; the file system of this repo; the script in section 2. |
| Assumptions | A path counts when it sits in backticks in the pack and holds a slash or a file extension. A path that starts with `../` is read from the project folder (06-telecom-service-network-incident-ops). Every other path is read from that folder. |
| Unresolved issues | None for the pack. Section 4 lists paths in other S09 files that do not exist on purpose. |
| Residual risks | The check proves that a file or test exists. It does not prove that the file says what the pack claims. A reader checks the claim against the file. |

## 1. Result

| Measure | Value |
|---|---|
| Distinct paths and test ids in the pack | 150 |
| Files | 109 |
| Folders | 29 |
| Test ids (file plus `def` name) | 12 |
| Missing | 0 |

The gate rule says BLOCKED when any pack path is missing. No pack path is missing, so this check does not block the stage.

## 2. How the check ran

The script below ran from the project folder with the command `python pathcheck.py PRODUCTION_EVIDENCE_PACK.md`. It reads each backticked text in the pack and keeps the ones that look like a path. It skips routes, shell commands and texts with brackets or equals signs. For a test id of the form `file::name` it checks that the file exists and that the file holds `def name`.

```python
import re,sys,json
from pathlib import Path
ROOT=Path(".").resolve()
EXT=re.compile(r"\.(md|py|json|xml|txt|yaml|yml|ps1|sh|tf|hcl|csv|jsonl|html|rego|toml|log|bak|pdf)$")
NAMES={"Makefile","Dockerfile",".env.example",".gitignore",".dockerignore",".gitattributes"}
SKIP_START=("GET ","POST ","git ","make ","pytest","python","opa ","gh ","terraform","$","http","X-","pip","ruff","bandit")
def candidates(text):
    for m in re.finditer(r"`([^`\n]+)`",text):
        t=m.group(1).strip()
        if t.startswith(SKIP_START) or "(" in t or "{" in t or "*" in t or "=" in t: continue
        if " " in t and not EXT.search(t.split("::")[0]): continue
        base=t.split("::")[0]
        if base in NAMES or ("/" in base and (EXT.search(base) or base.endswith("/"))) or (EXT.search(base) and " " not in base):
            yield t
def check(t):
    parts=t.split("::")
    base=parts[0]
    p=(ROOT/base)
    ok=p.exists()
    detail=""
    if ok and len(parts)>1:
        name=parts[-1].split("[")[0]
        src=p.read_text(encoding="utf-8",errors="replace")
        ok=bool(re.search(r"def\s+"+re.escape(name)+r"\b",src))
        detail="test defined" if ok else "test name not found in file"
    return ok,detail
files=sys.argv[1:]
total=0;missing=[]
for f in files:
    txt=Path(f).read_text(encoding="utf-8")
    seen=[]
    for t in candidates(txt):
        if t not in seen: seen.append(t)
    print(f"## {f}: {len(seen)} distinct paths or test ids")
    for t in seen:
        ok,d=check(t); total+=1
        print(("OK      " if ok else "MISSING ")+t+(("  ["+d+"]") if d else ""))
        if not ok: missing.append((f,t))
print("TOTAL",total,"MISSING",len(missing))
for f,t in missing: print("MISSING_IN",f,t)
```

## 3. Every path and test id in the pack

| # | Path or test id | Kind | Exists |
|---|---|---|---|
| 1 | `docs/16-evidence-pack/path-check.md` | file | Yes |
| 2 | `docs/15-readiness/` | folder | Yes |
| 3 | `docs/16-evidence-pack/` | folder | Yes |
| 4 | `evidence/` | folder | Yes |
| 5 | `docs/` | folder | Yes |
| 6 | `../playbook/STATUS.md` | file | Yes |
| 7 | `docs/00-contract/operating-contract.md` | file | Yes |
| 8 | `docs/00-contract/challenge-to-spine-crosswalk.md` | file | Yes |
| 9 | `docs/model-comparison/app-comparison.md` | file | Yes |
| 10 | `docs/model-comparison/second-model-load-fix.md` | file | Yes |
| 11 | `docs/model-comparison/yaml-hashes-after.md` | file | Yes |
| 12 | `docs/demo/evidence.md` | file | Yes |
| 13 | `apps/api/` | folder | Yes |
| 14 | `docs/15-readiness/residual-risk-register.md` | file | Yes |
| 15 | `../` | folder | Yes |
| 16 | `docs/15-readiness/go-no-go-decision.md` | file | Yes |
| 17 | `apps/api/main.py` | file | Yes |
| 18 | `data/contracts/openapi-fragment.yaml` | file | Yes |
| 19 | `tests/app/test_openapi_fragment.py` | file | Yes |
| 20 | `policy/tests/test_policy_python.py::test_no_route_can_execute` | test | Yes |
| 21 | `evidence/junit-tests.xml` | file | Yes |
| 22 | `evidence/junit-semantic-layer.xml` | file | Yes |
| 23 | `evidence/junit-policy.xml` | file | Yes |
| 24 | `evidence/junit-security.xml` | file | Yes |
| 25 | `evidence/exit-codes.txt` | file | Yes |
| 26 | `docs/prd/traceability.md` | file | Yes |
| 27 | `semantic-layer/README.md` | file | Yes |
| 28 | `docs/prd/prd.md` | file | Yes |
| 29 | `docs/16-evidence-pack/ci-run-38521594275.txt` | file | Yes |
| 30 | `scripts/evidence.ps1` | file | Yes |
| 31 | `evidence/run-info.txt` | file | Yes |
| 32 | `Makefile` | file | Yes |
| 33 | `docs/15-readiness/risk-owner-table.md` | file | Yes |
| 34 | `evidence/README.md` | file | Yes |
| 35 | `tests/characterization/test_current_behaviour.py` | file | Yes |
| 36 | `docs/02-baseline/behaviour-snapshot.md` | file | Yes |
| 37 | `docs/02-baseline/baseline-test-report.md` | file | Yes |
| 38 | `docs/02-baseline/defect-list.md` | file | Yes |
| 39 | `docs/02-baseline/data-quality-baseline.md` | file | Yes |
| 40 | `docs/02-baseline/profile-output.json` | file | Yes |
| 41 | `data/quality_issues.json` | file | Yes |
| 42 | `data/synthetic/` | folder | Yes |
| 43 | `apps/web/` | folder | Yes |
| 44 | `docs/15-readiness/operating-contract-check.md` | file | Yes |
| 45 | `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` | test | Yes |
| 46 | `docs/03-identity/target-access-matrix.md` | file | Yes |
| 47 | `tests/security/test_client_flags_ignored.py::test_no_route_reads_an_approval_id_from_the_caller` | test | Yes |
| 48 | `docs/03-identity/evidence.md` | file | Yes |
| 49 | `docs/ADR/0003-s06-risk-recommendations.md` | file | Yes |
| 50 | `apps/api/services/policy.py` | file | Yes |
| 51 | `legacy/reconcile_legacy.py` | file | Yes |
| 52 | `tests/characterization/test_current_behaviour.py::test_legacy_script_reads_password_from_environment` | test | Yes |
| 53 | `.env.example` | file | Yes |
| 54 | `tests/security/test_secret_patterns.py::test_repo_has_no_secret_patterns` | test | Yes |
| 55 | `../transcript/` | folder | Yes |
| 56 | `docs/04-secrets/rotation-log.md` | file | Yes |
| 57 | `docs/04-secrets/` | folder | Yes |
| 58 | `docs/05-iac/` | folder | Yes |
| 59 | `docs/13-security-validation/` | folder | Yes |
| 60 | `../transcript/chat_transcript.md` | file | Yes |
| 61 | `scripts/bootstrap.ps1` | file | Yes |
| 62 | `docs/05-iac/evidence.md` | file | Yes |
| 63 | `Dockerfile` | file | Yes |
| 64 | `infra/terraform/main.tf` | file | Yes |
| 65 | `policy/tests/test_policy_python.py` | file | Yes |
| 66 | `evidence/opa-test.json` | file | Yes |
| 67 | `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access` | test | Yes |
| 68 | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` | test | Yes |
| 69 | `docs/06-policy/evidence.md` | file | Yes |
| 70 | `evidence/ruff.json` | file | Yes |
| 71 | `evidence/pip-audit.json` | file | Yes |
| 72 | `evidence/bandit.json` | file | Yes |
| 73 | `../.github/workflows/ci.yml` | file | Yes |
| 74 | `scripts/check_junit_no_skips.py` | file | Yes |
| 75 | `tests/ci/test_skip_guard.py` | file | Yes |
| 76 | `evidence/sbom.cdx.json` | file | Yes |
| 77 | `evidence/pip-freeze.txt` | file | Yes |
| 78 | `evidence/source-checksums.txt` | file | Yes |
| 79 | `requirements-dev.txt` | file | Yes |
| 80 | `docs/07-cicd/evidence.md` | file | Yes |
| 81 | `supply-chain/dependency-risk-register.md` | file | Yes |
| 82 | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | test | Yes |
| 83 | `tests/app/test_audit_row_keys.py` | file | Yes |
| 84 | `docs/08-observability/evidence.md` | file | Yes |
| 85 | `tests/app/test_readiness_route.py` | file | Yes |
| 86 | `docs/08-observability/dashboard-sketch.md` | file | Yes |
| 87 | `docs/08-observability/slo-proposal.md` | file | Yes |
| 88 | `docs/08-observability/trace-design.md` | file | Yes |
| 89 | `docs/08-observability/incident-reconstruction.md` | file | Yes |
| 90 | `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` | test | Yes |
| 91 | `tests/ai/test_guardrails.py` | file | Yes |
| 92 | `docs/09-ai-guardrails/evidence.md` | file | Yes |
| 93 | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` | test | Yes |
| 94 | `tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text` | test | Yes |
| 95 | `tests/app/test_command_phrases.py` | file | Yes |
| 96 | `apps/api/services/ai_gateway.py` | file | Yes |
| 97 | `docs/10-performance/evidence.md` | file | Yes |
| 98 | `docs/10-performance/measure-before.json` | file | Yes |
| 99 | `docs/10-performance/measure-after.json` | file | Yes |
| 100 | `tests/performance/test_load_once.py` | file | Yes |
| 101 | `docs/10-performance/load-scenarios.md` | file | Yes |
| 102 | `docs/12-finops/evidence.md` | file | Yes |
| 103 | `docs/11-reliability/recovery-evidence.md` | file | Yes |
| 104 | `tests/reliability/test_drills.py` | file | Yes |
| 105 | `tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row` | test | Yes |
| 106 | `docs/11-reliability/failure-mode-catalogue.md` | file | Yes |
| 107 | `tests/reliability/test_breaker.py` | file | Yes |
| 108 | `docs/prd/Risk Management.md` | file | Yes |
| 109 | `docs/12-finops/metrics_from_audit.py` | file | Yes |
| 110 | `docs/12-finops/metrics_from_audit_output.txt` | file | Yes |
| 111 | `tests/finops/test_metrics_from_audit.py` | file | Yes |
| 112 | `docs/12-finops/cost_baseline_output_halfB.txt` | file | Yes |
| 113 | `docs/00-contract/cost-envelope.md` | file | Yes |
| 114 | `docs/ADR/0004-defer-rq-31-answer-store.md` | file | Yes |
| 115 | `docs/13-security-validation/evidence.md` | file | Yes |
| 116 | `security/threat-model.md` | file | Yes |
| 117 | `docs/13-security-validation/remediation-backlog.md` | file | Yes |
| 118 | `tests/audit/test_audit_rebuild.py` | file | Yes |
| 119 | `docs/14-audit/evidence.md` | file | Yes |
| 120 | `tests/app/test_audit_before_state_change.py` | file | Yes |
| 121 | `docs/14-audit/compliance-evidence-mapping.md` | file | Yes |
| 122 | `tests/app/` | folder | Yes |
| 123 | `docs/16-evidence-pack/audit-log-record.md` | file | Yes |
| 124 | `logs/audit.log` | file | Yes |
| 125 | `docs/16-evidence-pack/hash-recheck.md` | file | Yes |
| 126 | `semantic-layer/` | folder | Yes |
| 127 | `apps/api_model_b/` | folder | Yes |
| 128 | `docs/model-comparison/harness/alias_model_b.py` | file | Yes |
| 129 | `docs/model-comparison/yaml-hashes-before.md` | file | Yes |
| 130 | `apps/api/services/dedupe.py` | file | Yes |
| 131 | `docs/model-comparison/second-model-test-split.md` | file | Yes |
| 132 | `docs/model-comparison/second-model-run-log.md` | file | Yes |
| 133 | `docs/model-comparison/harness/probe_battery2.py` | file | Yes |
| 134 | `docs/15-readiness/deferred-work-list.md` | file | Yes |
| 135 | `../Project_Intent.md` | file | Yes |
| 136 | `docs/15-readiness/readiness-checklist.md` | file | Yes |
| 137 | `docs/00-contract/` | folder | Yes |
| 138 | `docs/02-baseline/` | folder | Yes |
| 139 | `docs/03-identity/` | folder | Yes |
| 140 | `docs/06-policy/` | folder | Yes |
| 141 | `docs/07-cicd/` | folder | Yes |
| 142 | `docs/08-observability/` | folder | Yes |
| 143 | `docs/09-ai-guardrails/` | folder | Yes |
| 144 | `docs/10-performance/` | folder | Yes |
| 145 | `docs/11-reliability/` | folder | Yes |
| 146 | `docs/12-finops/` | folder | Yes |
| 147 | `docs/14-audit/` | folder | Yes |
| 148 | `docs/model-comparison/` | folder | Yes |
| 149 | `docs/01-discovery/` | folder | Yes |
| 150 | `docs/00-setup/` | folder | Yes |

## 4. Paths in other S09 files that do not exist on purpose

The same script ran over the six files in `docs/15-readiness/` and the two record files in `docs/16-evidence-pack/`. It found three paths that do not exist. None is in the pack.

| Path | Where it appears | Why it does not exist |
|---|---|---|
| `docs/defence/` and `docs/defence/defence-answers.md` | `docs/15-readiness/deferred-work-list.md`; `docs/15-readiness/readiness-checklist.md` | Stage S10 writes these. The checklist marks item 11 as not ready for this reason. |
| `logs/approvals.jsonl` | `docs/15-readiness/operating-contract-check.md` | The app creates this file at the first yes decision. No yes decision has run against the real file. |

## 5. Lifecycle

`docs/15-readiness/go-no-go-decision.md` section 5 cites this file for the gate rule "every pack path exists".
