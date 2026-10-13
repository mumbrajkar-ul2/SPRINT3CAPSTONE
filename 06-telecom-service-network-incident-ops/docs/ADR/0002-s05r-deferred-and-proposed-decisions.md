# ADR 0002: Decisions on the S05R deferred and PROPOSED items

| Field | Value |
|---|---|
| Stage | S05R follow-up. This ADR records the owner's decisions on the open items that stage S05R left. |
| Date / version | 2026-10-12, v1.0 |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Accepted on 2026-10-12. Mangesh (FDE) decided for Team-Force by the instruction "Proceed with the recommended decisions in S05R_Decisions.md". Each decision below is the recommendation in that file. |
| Evidence sources | `docs/02-baseline/S05R_Decisions.md` (the options and the reasons for each item); `docs/02-baseline/semantic-layer-revision.md` (the deferred list D-01 to D-20); `docs/00-contract/operating-contract.md` row 10 (Team-Force owns open choices) |
| Assumptions | (1) Mangesh (FDE) speaks for Team-Force on these choices. (2) The word "decided" here means the choice is made and written down. It does not mean the code or the test exists. |
| Unresolved issues | The letters of MAESTRO (D-20) are Unknown. Whether a login system is in scope (D-07) is Unknown. **Update, 2026-10-13.** ADR 0003 decided D-07: login is out of scope for this packet. A real model is not in use, so every time and cost number is from a stub. |
| Residual risks | Three decisions (D-03, D-06, D-08) are made here but built in stage S07. Until S07 the code does not match them. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## Context

Stage S05R folded 92 ids into the semantic layer (version `1.1.0`). It left 20 design questions deferred (D-01 to D-20) and 120 items marked `proposed: true` with `owner: Team-Force`. `docs/02-baseline/S05R_Decisions.md` explains each one and gives a recommendation. This ADR records the answer to each.

After S05R, a change to the YAML needs an ADR. This ADR is that record for the one YAML change below.

## Decision 1. What changes now

| Change | Where | Why |
|---|---|---|
| The percentile for model delay is p95 (D-16). | `metric.recommendation_latency`, field `today`, in `semantic-layer/metrics.yaml`. The glossary row has the same sentence. | It names a method. It does not set a target. `target` stays `null`. |
| The semantic layer version goes from `1.1.0` to `1.1.1`. | Seven YAML files, the schema, the glossary, the README, and the test constant. | One text change in the YAML raises the version for the whole tree. `build.py` refuses to write when two files disagree. |
| A rotation log is created (D-12). | `docs/04-secrets/rotation-log.md` | The design asked for a named place. The log has columns and no entries. No rotation has been recorded. |
| The open question on the rotation store is closed (D-12). | This ADR | The store is the markdown log above. Production would use a secret manager. That is stated in the PRD at stage S06. |

Nothing else in the YAML changes. No id is added, removed, or deprecated.

## Decision 2. The 20 deferred items

| Id | Decision | What happens next |
|---|---|---|
| D-01 | Keep deferred | Name the release checks at stage S09, when the evidence pack is written. |
| D-02 | Keep deferred | Add waiver audit entries only if a waiver feature is built. |
| D-03 | Decided | The approval record gets two fields. `decision` holds yes or no. `approver` holds a persona id. Stage S07 builds them and adds the ids to the YAML under a new ADR. |
| D-04 | Keep deferred | `scope.all_records` stays for the admin. A narrower audit scope waits until more than the admin needs audit access. |
| D-05 | Keep deferred, except final action | Final action is built at stage S07. The other three facts wait. |
| D-06 | Decided (option B) | Stage S07 adds `record_id` to the audit row as the 16th key. A reasons list comes later. S07 adds the id to the YAML under a new ADR. |
| D-07 | Keep deferred | Name the person who made a call when a login is in scope. |
| D-08 | Decided, start small | Stage S07 writes a short list of command phrases, marked PROPOSED, owner Team-Force. The starting phrases are: reboot, restart, shut down, delete, clear config, push config, apply. The list grows only when a test shows a gap. |
| D-09 | Keep deferred | Catching text hidden in an allowed field waits for real data or a real model. |
| D-10 | Keep deferred | A version number for the prompt wording waits until the wording changes. |
| D-11 | Keep deferred | The model timeout in the YAML stays `null` until a real model is measured. |
| D-12 | Decided (option A) | `docs/04-secrets/rotation-log.md` is created. It never holds a secret value. |
| D-13 | Closed | No new role id. The owner of environment settings stays the existing Team-Force owner. |
| D-14 | Keep deferred | Waits for a dashboard. |
| D-15 | Keep deferred | Model names and risk levels wait for a real model. |
| D-16 | Decided | Report p95. Written into the YAML under Decision 1. |
| D-17 | Keep deferred | Extra alarm fields wait for the batch summary design. |
| D-18 | Keep deferred | Each cost-grouping field is added when the feature that needs it is built. |
| D-19 | Keep deferred | The count of damaged rows gets a saved place at the S09 dashboard. |
| D-20 | Keep deferred | The MAESTRO list is added when the course material gives the definition. Option A (copy the course list) is the plan. |

Worked example for D-03. A recommendation shows "restart the router". An operator says no. The approval record then holds `decision: no` and `approver: persona.noc_operator` (the persona id is an example). The audit row can then show who refused and what.

## Decision 3. The PROPOSED items

The 120 PROPOSED items are accepted in the 12 bundles of `S05R_Decisions.md` Part 2.

| Bundle | Decision |
|---|---|
| P-01 to P-05 | Accept |
| P-06 (six metrics) | Accept with a note. The metric `metric.audit_completeness` cannot be worked out until `record_id` is on the audit row (D-06, stage S07). No metric `target` is set. |
| P-07 to P-09 | Accept. In P-09, the four runbook levels are accepted if the names read well to an operator. The three model call queue states are accepted and are removed if the queue is never built. |
| P-10 (seven rules) | Accept with a note. Three rules have `enforced_today: false` because nothing runs them in a live flow: `rule.policy_copies_agree`, `rule.repeat_event_is_one_event`, `rule.order_attempt_same_retry_is_one_attempt`. Stage S07 connects `dedupe.py` to the alarm intake, or the PRD says these rules are designs only. |
| P-11 | Accept |
| P-12 (the 35 access matrix rows, TA-01 to TA-35) | Accept. TA-15 stays as written (option A). |

**The flag stays.** The `proposed: true` flag marks an item that is not in the inherited repo (operating contract row 10). It records where the item came from. It does not mean the owner has not accepted it. So the flag stays on all 120 items. This ADR is the written acceptance.

## Decision 4. The PROPOSED numbers

| Id | Value | Decision |
|---|---|---|
| N-01 | 128 (audit id length limit) | Accept. This ADR is its ADR. |
| N-02 | 1000 | Accept with a note. It is a flag level. It is not a legal maximum. |
| N-03 | `sla_breach_risk` runs from 0 to 1 | Accept |
| N-04 | Timeout of 10 seconds | Accept as the stub default. The YAML stays `null` until a real model is measured. |
| N-05 | Breaker: 5 failures, 30 seconds open, 10 in flight | Accept for the lab |
| N-06 | Service levels: 99 of 100 `GET /health` calls return 200 each day, 95 of 100 summaries finish in 2000 ms, audit completeness 1.0 | Accept the first and third levels. Accept the 2000 ms level for a real model only, because the stub waits 10 ms and passes with no real test. |

Each number came from a design or a stub. None was measured with a real model. **Verified Fact** for the source of each number: `S05R_Decisions.md` Part 2.

## Consequences

- Version `1.1.1` is the layer that stage S06 and later stages cite.
- Stage S07 has three decided items to build (D-03, D-06, D-08). Each needs code, a test, and an ADR for its new YAML ids.
- 14 deferred items stay open, each with a named trigger. Update 2026-10-13: ADR 0003 later decided D-07 (login is out of scope for this packet), so 13 items stay deferred.
- No AI use gains execute agency from any decision here.
- No code, Rego, CI file, Terraform, fixture, or `policy_data.json` changes.

## Open items

| Item | Owner |
|---|---|
| The letters of MAESTRO | Team-Force, when the course gives them |
| Whether a login system is in scope | Team-Force |
| A measured model timeout and p95 | Team-Force, after a real model is chosen |
