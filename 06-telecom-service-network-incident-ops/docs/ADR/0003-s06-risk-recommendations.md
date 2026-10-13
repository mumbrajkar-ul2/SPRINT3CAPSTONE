# ADR 0003: Decisions on the S06 risk recommendations

| Field | Value |
|---|---|
| Stage | S06 follow-up. This ADR records the owner's decisions on the three open choices in `docs/prd/Risk Management.md` section 5, and the PRD requirements that follow. |
| Date / version | 2026-10-12, v1.0 |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Accepted on 2026-10-12. Mangesh (FDE) decided for Team-Force by the instruction "proceed with the recommendations for the Risks". Each decision below is the recommendation in `docs/prd/Risk Management.md`. |
| Evidence sources | `docs/prd/Risk Management.md`; `docs/prd/prd.md` section 12 and section 13; `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` (D-07 deferred to S06); `docs/02-baseline/S05R_Decisions_Taken.md`; `docs/13-security-validation/remediation-backlog.md` (SB-01, SB-09); `docs/12-finops/optimization-backlog.md` (`OB-01`); `docs/00-contract/operating-contract.md` row 10 |
| Assumptions | (1) Mangesh (FDE) speaks for Team-Force on these choices. (2) "Decided" here means the choice is written down. It does not mean the code or the test exists. Stage S07 builds the code. (3) This ADR adds no YAML id. New ids wait for S07 and a later ADR, or for an S05R rerun when an Open question for S03 is answered. |
| Unresolved issues | The letters of MAESTRO (D-20) are Unknown. Three Open questions for S03 stay open: the word to store for an unknown role, a failmode id for a forbidden value in the model answer, and a status id for the readiness body. A real model is not in use. |
| Residual risks | Six new requirements (RQ-68 to RQ-73) and the extra text on RQ-31 are planned for S07. Until S07 the code does not match them. **Update, 2026-10-13.** ADR 0004 moves the build of RQ-31 (the answer store) out of S07. RQ-68 to RQ-73 stay planned for S07. Authentication stays out of scope, so `approver` and `actor` stay claims. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## Context

ADR 0002 left D-07 deferred: decide the login scope when the PRD is written. The PRD at v1.0 proposed "out of scope" and left it Unknown until S06R. `docs/prd/Risk Management.md` then recommended an action for each of RK-01 to RK-17 and named three choices that only Team-Force can make.

This ADR records those three choices and the PRD rows that follow.

## Decision 1. D-07 login scope

A login system is out of scope for this packet.

The role stays a word the caller types in `X-User-Role`. The page and the audit route show `caller_identity` on the `cannot_prove` list (RQ-65). `approver` and `actor` are shown as claimed role.

Production would issue a token per persona. The server would then set the role. That work is not in S07.

**Verified Fact.** `Project_Intent.md` has no authentication requirement. `apps/api/main.py` reads `X-User-Role` and nothing else. Source: SB-09.

## Decision 2. F15 / SB-01 on `GET /records/{id}`

A call with no role header is refused.

S07 removes `Header(default="operator")` in `apps/api/main.py` and the two fallbacks in `apps/api/services/policy.py` (`_RECORD_READ_DEFAULT`, `_SUMMARIZE_DEFAULT`). The two tests that lock the old behaviour change to expect HTTP 403, a `policy.deny` row and `role` null. The requirement is RQ-68. After the code runs, S07 turns `rule.no_default_role` on under a later ADR.

**Verified Fact.** The summarize route already refuses a missing header (`tests/characterization/test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header`).

## Decision 3. RQ-31 answer store

The 300 second answer store stays in S07.

**Update, 2026-10-13.** ADR 0004 moves the build of the store out of S07. The rules below stay as the rules for a later build.

S07 never stores an answer that has no text. That means a BLOCK, or a HOLD_FOR_REVIEW with no sentence. It stores a HOLD_FOR_REVIEW recommendation that has a sentence and passed every output check. The output checks run again on a stored answer. A `true` or blank `stale_topology_flag` stops the call before the store is read. The cache flag (D-18) is added under a later ADR before the route ships.

The cap on how many answers the store holds is PROPOSED. Owner: Team-Force. S07 does not invent a number. Until Team-Force names a cap, the store holds answers for 300 seconds and no more rule is added.

## Decision 4. The six new PRD requirements

These rows are added to `docs/prd/prd.md` as RQ-68 to RQ-73. Each cites an existing YAML id. Three of them name an Open question for S03 for a missing id. S07 writes the planned tests.

| Requirement | Risk | What S07 builds |
|---|---|---|
| RQ-68 | RK-02 | No-header 403 on `GET /records/{id}` |
| RQ-69 | RK-03 | Unknown role word is not stored as sent. The 128 character limit applies when the row is written. |
| RQ-70 | RK-04 | A forbidden value in the model answer returns HOLD_FOR_REVIEW with no text. |
| RQ-71 | RK-05 | A near-miss command phrase is held. The near-miss list is PROPOSED. Owner: Team-Force. |
| RQ-72 | RK-08 | App tests do not write to `logs/audit.log`. |
| RQ-73 | RK-11 | `GET /ready` returns 503 when `devices.csv` is missing. |

## Consequences

- D-07 is decided. It is no longer deferred. The 13 items that stay deferred are D-01, D-02, D-04, D-05, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20.
- The PRD version goes from v1.0 to v1.1. The semantic layer stays `1.1.1`. This ADR adds no YAML id.
- Stage S07 builds RQ-68 to RQ-73 and the extra text on RQ-31, plus the rows already named in the v1.0 PRD. **Update, 2026-10-13.** ADR 0004 moves the build of RQ-31 out of S07. S07 builds RQ-68 to RQ-73 and the rows named in the v1.0 PRD, and does not build the answer store.
- Authentication is not built. A later packet that needs it writes a new ADR.

## Open items

| Item | Owner |
|---|---|
| The word to store when the role header is not in the known list | Team-Force. Open question for S03. |
| A failmode id for a forbidden value in the model answer | Team-Force. Open question for S03. |
| A status id for the readiness body | Team-Force. Open question for S03. |
| The cap on stored answers | Team-Force. PROPOSED. No number is set. |
