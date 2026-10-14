# Go / no-go decision

| Field | Value |
|---|---|
| Stage | S09. Production readiness gate and evidence pack (Challenge 15, D8). |
| Date / version | 2026-10-13, v1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE). |
| Status | CONDITIONAL PASS. The decision states what is ready, what is not ready and which risks are accepted. 41 of the 63 open risks have a PROPOSED owner and no written acceptance. |
| Evidence sources | `docs/15-readiness/readiness-checklist.md`; `docs/15-readiness/residual-risk-register.md`; `docs/15-readiness/risk-owner-table.md`; `docs/15-readiness/deferred-work-list.md`; `docs/15-readiness/operating-contract-check.md`; `docs/16-evidence-pack/audit-log-record.md`; `docs/16-evidence-pack/hash-recheck.md`; `docs/16-evidence-pack/ci-run-38521594275.txt`; `evidence/run-info.txt`; `../playbook/STATUS.md`; `docs/00-contract/operating-contract.md` v1.4. |
| Assumptions | "The lab demo" means the governed app in `apps/api/`, run on one machine, with synthetic data, the stand-in model `local-sim-v1`, one server process, and a person who types the role word. "Production" means a live service with real users, a real model and more than one server process. |
| Unresolved issues | 41 risks have no written owner. Seven PRD gaps are open (G-1 to G-4, G-6, G-8, G-9). The refreshed `evidence/` folder has no commit. |
| Residual risks | The 63 rows in `docs/15-readiness/residual-risk-register.md`. |

## 1. Decision

**NO-GO for production. GO for the lab demo and the S10 defence, under the seven conditions in section 2.** The governed app in `apps/api/` is ready for the lab demo because 469 tests pass with 0 skipped, `GET /audit/{correlation_id}` rebuilds a demo case from one correlation id, and no route can reach the outcome EXECUTE (`policy/tests/test_policy_python.py::test_no_route_can_execute`). It is not ready for production because the caller's role is a word the caller types, the model is the stand-in `local-sim-v1` and no test ran against a real model, the audit log is a plain file that anyone with file access can edit, nobody built metrics, a secret store or a way to find a held case, the pipeline on GitHub ends red on three scans (lint 30 findings, dependency scan 9 advisory ids, static scan 40 findings), and one reviewer accepts every code change. The lab demo carries these gaps. 22 of the 63 open risks have a named acceptor in the packet. The other 41 have a PROPOSED owner: Team-Force for 38 rows and Mangesh (FDE) for 3 rows (contract row 10). No acceptance exists for those 41 until Team-Force writes it. The no-go for production stays until a named owner accepts or closes each row in `docs/15-readiness/risk-owner-table.md` section 3, and each production gap in `docs/15-readiness/readiness-checklist.md` has a built control and a test.

## 2. Conditions for the lab demo

| # | Condition | Why | Who keeps it | Row |
|---|---|---|---|---|
| C1 | Say "stand-in model" whenever the demo shows a model answer. Latency is SIMULATED. Tokens and cost are EDUCATIONAL. | No real model call exists in the repo. | Mangesh (FDE) | `AIR-01` |
| C2 | Say "synthetic data" and "one process". Do not claim it handles real alarms or several servers. | The audit lock and the duplicate memory cover one process. | Mangesh (FDE) | `FM-06`, `SB-12` |
| C3 | Say the role is a typed word. Do not claim the app knows who the caller is. | ADR 0003 puts login out of scope. | Mangesh (FDE) | `SB-09` |
| C4 | Say the GitHub run on the last commit ended red because of lint, the dependency scan and the static scan. The tests, policy and security stages passed. | Run 38521594275 on commit `ec56a34` (`docs/16-evidence-pack/ci-run-38521594275.txt`). | Mangesh (FDE) | `BL-10`, `BL-11`, `BL-12` |
| C5 | Commit and push the refreshed `evidence/` folder so that the next CI run proves the final tree. | The run in `evidence/` has no commit. | Mangesh (FDE) (PROPOSED) | `S09-1` |
| C6 | Team-Force accepts the 38 risks that name it as PROPOSED owner for the lab demo only, or names another owner. Mangesh (FDE) closes the 3 risks that name him. | 41 risks have no written acceptance. | Team-Force; Mangesh (FDE) | `docs/15-readiness/risk-owner-table.md` section 3 |
| C7 | Decide whether to keep or redact the old shared password in `../transcript/chat_transcript.md`. Decide the exception for the three extra routes and the four files with no named stage. | Contract row 4 and stop condition 5. | Mangesh (FDE) (PROPOSED) | `S09-5` |

The word "PROPOSED" in the column "Who keeps it" means nobody has accepted the item in writing (contract row 10).

## 3. What is ready, what is not ready

| Area | Ready for | Not ready for |
|---|---|---|
| Policy | The lab demo. 87 policy tests pass, and 32 of 32 `opa test` results pass. | Production. The policy checks that an approval id is not blank. It does not look the id up. |
| Audit | The lab demo. One correlation id rebuilds one case. | Production. The log is a plain file, and the route lists what the log cannot prove. |
| Identity, secrets, IaC, CI/CD, observability, AI guardrails, performance, reliability, FinOps, security validation | Part of the lab demo (partial). The last column of `docs/15-readiness/readiness-checklist.md` names the missing part of each. | Production. |
| Live network change | Nothing. No route changes a device, and none is planned. | Any use. Contract rows 8 and 9 stop it. |
| Real model calls | Nothing. | Any use. No test ran against a real model. |

## 4. Gate result of each stage

Source: `../playbook/STATUS.md` unless the row says otherwise. The contract rule that gives each result its meaning is `docs/00-contract/operating-contract.md` v1.4.

| Stage | Result | Source |
|---|---|---|
| S00 | CONDITIONAL PASS | STATUS 2026-10-08 |
| S0B | PASS | STATUS 2026-10-09 |
| S01 | CONDITIONAL PASS | STATUS 2026-10-09 |
| S02 | CONDITIONAL PASS | STATUS 2026-10-10 |
| S2Q | PASS | STATUS 2026-10-10 |
| S03 | PASS | STATUS 2026-10-10 |
| S03R | PASS in round 3. Rounds 1 and 2 were BLOCKED. | STATUS 2026-10-10 |
| S04-03 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | STATUS |
| S04-04 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | STATUS |
| S04-05 | Half A CONDITIONAL PASS. Half B PASS. | STATUS |
| S04-06 | Half A PASS. Half B CONDITIONAL PASS. | STATUS |
| S04-07 | Half A PASS (two runs). Half B PASS. | STATUS |
| S04-08 | Half A CONDITIONAL PASS. Half B PASS. | STATUS |
| S04-09 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | STATUS |
| S04-10 | Half A CONDITIONAL PASS. Half B PASS. | STATUS |
| S04-11 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | STATUS |
| S04-12 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. | STATUS |
| S05-13 | Half A CONDITIONAL PASS. Half B CONDITIONAL PASS. CI proof PASS (two runs). | STATUS |
| S05-14 | CONDITIONAL PASS | No STATUS row. `docs/14-audit/evidence.md` line 8. |
| S05R | CONDITIONAL PASS | STATUS 2026-10-12 |
| S06 | No stage result recorded. S06F rounds 3 to 7 each CONDITIONAL PASS. | No STATUS row for S06. STATUS rows for S06F. |
| S06R | PASS against PRD v1.8 | No STATUS row. `docs/prd/prd-review.md` line 8. |
| S07 | CONDITIONAL PASS. Gaps G-5 and G-7 closed, also CONDITIONAL PASS. | STATUS 2026-10-13 |
| S08 | Parts 1, 2 and 3 CONDITIONAL PASS. Load fix DONE. | STATUS 2026-10-13 |
| S09 | CONDITIONAL PASS | This stage. See section 5. |

## 5. Gate of this stage

| Gate rule from `../playbook/S09-readiness-and-evidence-pack.md` | Met? | Proof |
|---|---|---|
| PASS: the decision states ready, not ready and accepted risk with owners. | Met for ready and not ready. Met for accepted risk on 22 rows. Not met for 41 rows, whose owner is PROPOSED. | Section 1 and `docs/15-readiness/risk-owner-table.md`. |
| PASS: every path in the pack exists. | Met. | `docs/16-evidence-pack/path-check.md`. |
| PASS: every 6.3 item is ticked or marked not ready. | Met. 10 ticked, 1 not ready. | `docs/15-readiness/readiness-checklist.md` section 3. |
| CONDITIONAL PASS: an owner is PROPOSED. | Applies. 41 owners are PROPOSED. | `docs/15-readiness/risk-owner-table.md` section 3. |
| BLOCKED: a pack path is missing or a claim has no evidence. | Does not apply. | `docs/16-evidence-pack/path-check.md`. |

**Result: CONDITIONAL PASS.** Stage S10 presents from `PRODUCTION_EVIDENCE_PACK.md`.
