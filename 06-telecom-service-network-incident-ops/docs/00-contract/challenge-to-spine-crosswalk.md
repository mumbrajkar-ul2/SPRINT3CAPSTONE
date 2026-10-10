# Challenge-to-spine crosswalk

| Field | Value |
|---|---|
| Stage | S0B — Crosswalk (Execution Plan Phase 0B; spine stages 0B and 0C) |
| Date / version | 2026-10-09, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | ACTIVE |
| Evidence sources | `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf` (the 16 challenge names); `How the product spine addresses the 16 challenges - plain speak.md`; `Assignment Material/AI_FDE_End-to-End_Production_Delivery_Spine.pdf` (folder tree on pages 31 and 32); `Execution Plan.md` section 3 |
| Assumptions | The plain-speak note is the comparison this table follows. Its window for a full match test is spine stages 0A, 0B, 0C, and 1 through 20. Later stages are listed when that note names them. |
| Unresolved issues | The spine and this packet both use a `docs/` tree, and the folder numbers mean different jobs. The table uses both trees. A reader still has to keep them apart. |
| Residual risks | A Match row means the spine requires the same work. The files can still be missing from this repo. |

## What this file is

This file maps each challenge folder in this packet to the spine stages that cover the same ground. The spine is the 42-stage production plan in `AI_FDE_End-to-End_Production_Delivery_Spine.pdf`. The challenge folders are the ones this packet will fill, from `docs/00-setup/` through `docs/16-evidence-pack/`.

The two trees use the same word `docs/` and different numbers. This packet's `docs/01-discovery/` is challenge 1, Understand Existing Repo. Spine stage 1 is `docs/01-engagement/`, the engagement qualification. Use the table to pick the folder you mean.

## How to read the verdict

| Verdict | What it means on one row |
|---|---|
| Match | The plain-speak note says the pass test is met and the named outputs are required in the spine. |
| Partial | A spine stage covers part of the same ground. The pass test is still open, one named output is missing, or only a related file exists. |
| None | No spine stage from 0A through 42 requires that work. |

The verdict records what the spine requires. Where `Execution Plan.md` still asks for the work, the row says so.

## Stage folders cited below

Paths are the spine's own `docs/` tree.

| Spine id | Folder |
|---|---|
| 0A | `docs/00-preflight/discovery/` |
| 0B | `docs/00-preflight/operating-contract/` |
| 0C | `docs/00-preflight/ai-economics/` |
| 2 | `docs/02-stakeholders/` |
| 5 | `docs/05-current-state/` |
| 7 | `docs/07-repo-assessment/` |
| 8 | `docs/08-ai-qualification/` |
| 9 | `docs/09-initial-prd/` |
| 10 | `docs/10-architecture/` |
| 11 | `docs/11-data-context/` |
| 12 | `docs/12-specs/` |
| 14 | `docs/14-transformation/` |
| 15 | `docs/15-modernization/` |
| 16 | `docs/16-repo-validation/` |
| 18 | `docs/18-delivery/` |
| 19 | `docs/19-intelligence/` |
| 20 | `docs/20-application/` |
| 21 | `docs/21-integration/` |
| 23 | `docs/23-human-control/` |
| 24 | `docs/24-security-privacy/` |
| 25 | `docs/25-governance/` |
| 26 | `docs/26-tevv/` |
| 27 | `docs/27-hardening/` |
| 28 | `docs/28-resilience/` |
| 30 | `docs/30-release/` |
| 31 | `docs/31-observability/` |
| 32 | `docs/32-finops/` |
| 37 | `docs/37-operating-model/` |
| 42 | `docs/42-executive/` |

## The eighteen rows

| Packet folder | Challenge | Spine stages that cover the same ground | Verdict |
|---|---|---|---|
| `docs/00-setup/` | Setup and first replay. This packet's Phase 0, beside the 16 challenges. | 0A `docs/00-preflight/discovery/`. Stage 0A is the read-only orientation before any change. | Partial |
| `docs/00-contract/` | Operating contract, cost envelope, and this crosswalk. Spine stages 0B and 0C. | 0B `docs/00-preflight/operating-contract/`; 0C `docs/00-preflight/ai-economics/`. | Partial |
| `docs/01-discovery/` | 1. Understand Existing Repo | 0A `docs/00-preflight/discovery/`; 5 `docs/05-current-state/`; 7 `docs/07-repo-assessment/`. Related, smaller files: 0B `docs/00-preflight/operating-contract/` and 2 `docs/02-stakeholders/`. | Match |
| `docs/02-baseline/` | 2. Establish Behavioural Baseline | 7 `docs/07-repo-assessment/`; 16 `docs/16-repo-validation/`. | Partial |
| `docs/03-identity/` | 3. Identity and Least Privilege | 10 `docs/10-architecture/`; 12 `docs/12-specs/`; 20 `docs/20-application/`. Later: 24 `docs/24-security-privacy/`; 27 `docs/27-hardening/`. | Partial |
| `docs/04-secrets/` | 4. Secrets and Encryption | 7 `docs/07-repo-assessment/`; 11 `docs/11-data-context/`; 12 `docs/12-specs/`; 15 `docs/15-modernization/`. Later: 24 `docs/24-security-privacy/`; 27 `docs/27-hardening/`. | Partial |
| `docs/05-iac/` | 5. Infrastructure as Code | 0B `docs/00-preflight/operating-contract/`; 10 `docs/10-architecture/`; 14 `docs/14-transformation/`. Later: 30 `docs/30-release/`; 37 `docs/37-operating-model/`. | Partial |
| `docs/06-policy/` | 6. Policy as Code | No spine stage requires an executable allow-and-deny policy. The nearest file is stage 12 `docs/12-specs/` `business-rules.md`. The plain-speak note counts that file as a written rule for people, and counts it as different work. Stages 23 and 25 test approval gates and map obligations. They are also counted as different work. | None |
| `docs/07-cicd/` | 7. CI/CD and Supply Chain | 7 `docs/07-repo-assessment/`; 16 `docs/16-repo-validation/`; 18 `docs/18-delivery/`. Later: 27 `docs/27-hardening/`; 30 `docs/30-release/`. | Partial |
| `docs/08-observability/` | 8. Observability and Traceability | 10 `docs/10-architecture/`; 12 `docs/12-specs/`; 20 `docs/20-application/`. Later: 31 `docs/31-observability/`. | Partial |
| `docs/09-ai-guardrails/` | 9. AI Security and Guardrails | Same-work files: 8 `docs/08-ai-qualification/`; 19 `docs/19-intelligence/` (structured output); 20 `docs/20-application/`. Related files: 0B `docs/00-preflight/operating-contract/`; 2 `docs/02-stakeholders/`; 9 `docs/09-initial-prd/`; 10 `docs/10-architecture/`; 11 `docs/11-data-context/`. Later: 23 `docs/23-human-control/`; 24 `docs/24-security-privacy/`; 26 `docs/26-tevv/`. | Partial |
| `docs/10-performance/` | 10. Performance and Scalability | 0C `docs/00-preflight/ai-economics/`; 10 `docs/10-architecture/`; 19 `docs/19-intelligence/`. Later: 28 `docs/28-resilience/`; 31 `docs/31-observability/`. | Partial |
| `docs/11-reliability/` | 11. Reliability and Failure Engineering | 20 `docs/20-application/` (the build must implement idempotency). Later: 21 `docs/21-integration/`; 28 `docs/28-resilience/`. | Partial |
| `docs/12-finops/` | 12. Cost and AI FinOps | 0C `docs/00-preflight/ai-economics/`; 8 `docs/08-ai-qualification/`; 19 `docs/19-intelligence/`. Later: 32 `docs/32-finops/`. | Partial |
| `docs/13-security-validation/` | 13. Automated Security Validation | 7 `docs/07-repo-assessment/`; 16 `docs/16-repo-validation/`. Later: 24 `docs/24-security-privacy/`; 26 `docs/26-tevv/`; 27 `docs/27-hardening/`. | Partial |
| `docs/14-audit/` | 14. Auditability and Compliance Evidence | 20 `docs/20-application/` (audit hooks). Later: 25 `docs/25-governance/`; 42 `docs/42-executive/`. | Partial |
| `docs/15-readiness/` | 15. Production Readiness Gate | 0A `docs/00-preflight/discovery/`; 2 `docs/02-stakeholders/`; 7 `docs/07-repo-assessment/`; 9 `docs/09-initial-prd/`; 10 `docs/10-architecture/`; 14 `docs/14-transformation/`; 16 `docs/16-repo-validation/`; 18 `docs/18-delivery/`; 19 `docs/19-intelligence/`; 20 `docs/20-application/`. Later: 27 `docs/27-hardening/`; 30 `docs/30-release/`. | Partial |
| `docs/16-evidence-pack/` | 16. Production Evidence Pack | Pieces in 7 `docs/07-repo-assessment/`; 16 `docs/16-repo-validation/`; 19 `docs/19-intelligence/`. Later: 42 `docs/42-executive/` is the pack the note names. | Partial |

## Worked examples

`docs/00-contract/` is Partial. This folder writes the operating contract and the first cost view. Spine stage 0B requires that contract and also requires separate files for scope, write rules, environment access, data use, tool permissions, human approval, evidence, change control, and stop conditions. Spine stage 0C requires the cost scenarios and also requires token budgets, loop budgets, and a draft total cost. The decisions are the same kind of work. The spine's file list is longer, so the verdict is Partial.

`docs/01-discovery/` is Match. The plain-speak note says the pass test is met and the named outputs are required. Stages 0A, 5, and 7 must save the architecture maps, the component lists, the workflow maps, the data and integration maps, the risk list, and the rule that each claim cites the repo. Two items stay thinner: a file whose only job is the AI subsystem, and a list of who owns each component. Both are named in the row above.

`docs/02-baseline/` is Partial. Stages 7 and 16 cover the test snapshot, the behaviour record, and the pass test that separates old behaviour from a defect. The missing output in that window is a data-quality profile of the synthetic files. Stage 11 writes target data rules for the future design. The current-file profile is a separate output. This packet's `Execution Plan.md` still asks stage S02 to write that profile. The spine verdict stays Partial.

`docs/06-policy/` is None. The challenge guide asks for executable policy, with one allow case and one deny case. The plain-speak note says that file is absent from stages 0A through 42. This packet's `Execution Plan.md` still requires that allow-and-deny pair in Phase 4, under `docs/06-policy/`. The None verdict records the spine gap. This packet still does that work in Phase 4.

## Lifecycle

Stage S09 copies this crosswalk into the evidence pack. A reviewer who thinks in spine stage numbers uses the middle column to find the matching spine folder. A reviewer who thinks in the 16 challenges uses the packet folder column.
