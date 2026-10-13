# ADR 0004: Defer RQ-31, the answer store

| Field | Value |
|---|---|
| Stage | Between S06F and S07. This ADR records the owner's decision to move the answer store (RQ-31) out of S07. |
| Date / version | 2026-10-13, v1.0 |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Accepted on 2026-10-13. Mangesh (FDE) decided for Team-Force in chat: "Defer RQ-31." The recommendation came from the same chat. It changes the part of ADR 0003 decision 3 that says the store is built in S07. |
| Evidence sources | `docs/ADR/0003-s06-risk-recommendations.md` (decision 3); `docs/prd/prd.md` (RQ-31, RK-14, section 13, section 15); `docs/prd/Risk Management.md` (RK-14); `docs/12-finops/optimization-backlog.md` (OB-01, "What it saves"); `docs/02-baseline/S05R_Decisions_Taken.md` (D-18); `tests/finops/test_metrics_from_audit.py::test_repeat_prompt_calls_are_counted_from_prompt_hash`; `docs/00-contract/operating-contract.md` row 10 |
| Assumptions | (1) Mangesh (FDE) speaks for Team-Force (`operating-contract.md` row 10). (2) "Deferred" means the requirement row stays in the PRD, S07 does not build it, and no id or test name is removed. (3) This ADR adds no YAML id. The semantic layer stays `1.1.1`. |
| Unresolved issues | The cap on stored answers stays PROPOSED with no number (ADR 0003). The name and place of the cache flag (D-18) are not decided. Both wait until someone builds the store. |
| Residual risks | The saving that OB-01 describes (4 of 5 calls in the DR-3 case, EDUCATIONAL) is not realised. `metric.repeated_prompt_share` still shows how often a prompt repeats, so the size of the missed saving stays visible. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## Context

ADR 0003 decision 3 said the 300 second answer store stays in S07. It fixed the rules for what the store may hold. The PRD turned those rules into RQ-31.

Before S07 starts, the owner asked whether S07 should still build the store. Two facts decided it.

1. **Verified Fact.** The store adds a lot to S07. It needs a 300 second lifetime, a cap with no number, four output checks that run again on a stored answer, a stale-flag check before the store is read, and a new audit key (the cache flag, D-18). The cache flag has no name and no place in the audit row yet. A new ADR and a new layer version must settle it before any code.
2. **Verified Fact.** The demo shows no saving from it. The page walks one case once, so no call repeats. The model is the stub `local-sim-v1`, which waits 10 ms. The saving in `optimization-backlog.md` is labelled EDUCATIONAL, and the real repeat rate is Unknown.

**Inference.** The FinOps idea can still be shown without the store. `metric.repeated_prompt_share` counts how many audit rows hold a `prompt_hash` seen before, and its test already exists.

## Decision

S07 does not build the answer store.

- RQ-31 stays in the PRD as row 31. Its text is kept for the stage that builds it later. The row is marked **deferred (ADR 0004)**.
- The acceptance test `test_second_identical_request_within_300_seconds_makes_no_model_call` is not planned for S07. Its status is **deferred**. The name stays, so a later stage can write it.
- The rules of ADR 0003 decision 3 stay as the rules for that later build: the store never holds an answer that has no text, an entry is found by `prompt_hash` alone, and the cap is PROPOSED with no number.
- The 300 second lifetime (`OB-01`) stays DECIDED. The decision says how long an answer may be reused, once a store exists. It does not say that S07 builds one.
- D-18 stays deferred. S07 does not add the cache flag.
- `POST /approvals/{id}` (RQ-34) needs a recommendation row that was shown with text. In S07 that row always comes from a model call.
- The route ranges in the PRD change from "RQ-18 to RQ-31, RQ-70 and RQ-71" to "RQ-18 to RQ-30, RQ-70 and RQ-71 (RQ-31 is deferred)". A builder then does not read RQ-31 as part of S07.

## Consequences

- The PRD goes from v1.6 to v1.7, in `prd.md` and `traceability.md`. The semantic layer stays `1.1.1`.
- The PRD counts change. It still has 73 requirements and 29 existing tests. It has 43 tests planned for S07 and 1 deferred.
- S07 builds 43 planned tests, not 44.
- ADR 0003 decision 3 is changed in one part: the store is no longer built in S07. Its other rules are not changed.
- The risk RK-14 (a wrong stored answer repeats) does not apply to S07, because no store exists. It comes back when the store is built.
- Counts of Open questions for S03 and deferred items do not change. 13 Open question lines stay. 13 items stay deferred.

## How the store comes back

Build it only when one of these is true.

- A real model is in use and the cost of repeat calls is measured.
- `metric.repeated_prompt_share` shows a repeat rate high enough to matter, and Team-Force names the cap.
- Team-Force wants one running FinOps saving in a later demo.

Then run these steps in order.

1. S05R names the cache flag and its place in the audit row, and adds the YAML id.
2. A new ADR records the flag and raises the layer version.
3. S06F changes RQ-31 from deferred to planned and raises the PRD version.
4. S07 (or a later build stage) writes the store and its test.

## Open items

| Item | Owner |
|---|---|
| The name and place of the cache flag (D-18) | Team-Force. Deferred. |
| The cap on stored answers | Team-Force. PROPOSED. No number is set. |
| The condition that brings the store back | Team-Force. See "How the store comes back". |
