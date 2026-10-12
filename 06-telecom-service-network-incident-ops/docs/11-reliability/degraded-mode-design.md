# Degraded-mode design

| Field | Value |
|---|---|
| Stage | S04-11 — Reliability and failure engineering (Challenge 11), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every dependency has a row that says what continues, what returns HOLD_FOR_REVIEW, and what stops. Each row is checked against a probe run. Some target changes are PROPOSED for a later stage. |
| Evidence sources | `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `apps/api/services/policy.py`; `docs/11-reliability/probe_half_a.py` and `probe-output.json` (checks P2, P3, P5, P6, P7, P7b, P8, P10); `docs/09-ai-guardrails/unsafe-output-handling-rules.md`; `docs/10-performance/evidence.md`; `semantic-layer/ai-context-policy.yaml` (`policy.fail_to_person`); `Project_Intent - Section 3.1 Row 8.md` |
| Assumptions | A route "continues" when it returns its normal success status. A route "stops" when it returns an error status to every caller. The probe ran on Windows with the Python policy engine, except check P6, which forced the `opa` path with `opa` absent. |
| Unresolved issues | No inbox or person receives a held case (RF-08 in `failure-mode-catalogue.md`). The 500 error has no correlation id (RF-04). Open questions OQ-1, OQ-5, and OQ-6 ask S03 for failure ids and state words. |
| Residual risks | `/health` returns 200 in every row below. A monitor that calls only `/health` cannot see an outage. A readiness route would fix that. It is a new route, so it belongs to S07. |

## What this file is

This file says what the system does when one thing it depends on stops working. It states what still works, what goes to a person, and what stops.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file with a line or a probe check id.

No code changes in Half A.

## The answer to "what still works if the AI path is down?"

This answers `Project_Intent - Section 3.1 Row 8.md` and defence question 8.

At the baseline the answer was Unknown as a designed mode. Today:

- `GET /health` returns 200. It never calls the model.
- `GET /records/{id}` returns the record. It never calls the model.
- `POST /ai/summarize/{id}` returns HTTP 202 with `outcome` HOLD_FOR_REVIEW. `summary` and `recommendation` are null. An audit row says `policy.hold`. **Verified Fact:** probe P2 and P3.
- No route returns a made-up summary on a failure.

Two limits apply:

1. A person receives the held case only as the HTTP 202 body and one audit row. No inbox exists.
2. While many summaries wait on a hung model, `/health` and `/records/{id}` slow from about 10 ms to about 830 ms. They still return 200 (probe P5). The in-flight limit in `retry-and-circuit-breaker-strategy.md` removes most of this delay.

## What continues, for every dependency

Read each row as: "when this dependency is down, this is what each route returns."

| Dependency state | `GET /health` | `GET /records/{id}` | `POST /ai/summarize/{id}` | Evidence |
|---|---|---|---|---|
| Model times out | 200 | 200 | 202 HOLD_FOR_REVIEW, summary null | **Verified Fact.** Probe P2. |
| Model raises an error | 200 | 200 | 202 HOLD_FOR_REVIEW, summary null | **Verified Fact.** Probe P3. |
| Model hangs for many callers, no in-flight limit | 200 | 200, but about 830 ms | 202 after the deadline | **Verified Fact. REAL.** Probe P5. |
| Breaker open (after Half B) | 200 | 200 | 202 HOLD_FOR_REVIEW at once, summary null | **Assumption.** Half B tests it. |
| Policy engine fails | 200 | 403 `forbidden` | 403 `forbidden` | **Verified Fact.** Probe P6. |
| `devices.csv` missing | 200 | 500 | 500 | **Verified Fact.** Probe P7. |
| `devices.csv` has a header and no rows | 200 | 200 with body `{"error": "missing"}` | 403 BLOCK, `failmode.missing_id` | **Verified Fact.** Probe P7b. |
| Audit log cannot be written | 200 | 500, no device data | 500, no summary. The model ran once. | **Verified Fact.** Probe P8. |
| Another data file is missing (`alarms.csv`, `service_orders.csv`, `events.jsonl`, `circuits.csv`, `incidents.csv`, `ai_invocations.csv`) | 200 | 200 | 200 | **Verified Fact.** No route reads them (`data-access-findings.md` DA-03; probe P4). |
| `policy_data.json` or `ai-context-policy.yaml` missing or invalid at start-up | The app does not start | The app does not start | The app does not start | **Verified Fact** by reading the code. `policy.py` line 29 and `ai_gateway.py` line 108 read these files when the module loads. A missing file stops the start. Not probed. |

A stale or blank `stale_topology_flag` is a data fault and not a dependency failure. It is in `failure-mode-catalogue.md` FM-07.

## Dependency 1 — The model (AI gateway)

| | |
|---|---|
| What continues | `/health`. `/records/{id}`. Audit rows for every call. |
| What returns HOLD_FOR_REVIEW | `/ai/summarize/{id}` on a timeout, an error, or an open breaker. HTTP 202. `summary` null. `recommendation` null. |
| What stops | Nothing else. |
| Who receives the held case | The YAML names `persona.noc_operator`. The desk job is PROPOSED. Owner: Team-Force. No route, queue, or screen delivers it today. |
| What is written | One audit row: `policy.hold`, `outcome` HOLD_FOR_REVIEW. With a timeout the row holds `prompt_hash` and `latency_ms`. With an open breaker those fields are null. |
| What is never done | No default summary. No retry into an action. No EXECUTE. |
| Target change after Half B | The breaker and the in-flight limit. `/records/{id}` stays near 10 ms during a hang. |
| Label | **Verified Fact** for today. Half B proves the breaker. |

## Dependency 2 — The policy engine

| | |
|---|---|
| What continues | `/health`. |
| What returns HOLD_FOR_REVIEW | Nothing. A policy failure is a refusal, not a case for review. |
| What stops | `/records/{id}` and `/ai/summarize/{id}`. Both return 403 with body `{"error": "forbidden"}`. |
| Why it stops and does not continue | The code never allows a call because the engine failed. **Verified Fact:** `policy.py` lines 147 to 148 and 259 to 264. This is the fail-closed rule from S04-06. This design keeps it. |
| What is written | An audit row with action `policy.deny`. The reason `policy_engine_error` is not in the row. |
| Which engines can fail | Only the `opa` run can fail. The Python copy of the same table does not shell out. `opa` is not installed on the measuring machine (`docs/10-performance/evidence.md`). Whether the `opa` path and the Python path give the same answer on every input is checked by two Rego tests that are skipped when `opa` is absent. That is **Unknown** here. |
| Target change (PROPOSED, later stage) | Return 503 with a body that says the policy service is unavailable, so a person can tell an outage from a wrong role. Write the reason in the audit row. This changes route bodies and the audit shape. It needs OQ-5. It belongs to S07. |
| Label | **Verified Fact** for today. |

## Dependency 3 — `devices.csv`

| | |
|---|---|
| What continues | `/health`. |
| What returns HOLD_FOR_REVIEW | Nothing. The summary route stops before the model runs, so no model call is made (probe P7, `model_calls` 0). |
| What stops | `/records/{id}` and `/ai/summarize/{id}` with HTTP 500. |
| What is written | Nothing. No audit row exists for the failure. |
| Recovery | The failed first load is not kept. Once the file is back, the next request reads it (test `test_a_missing_file_raises_and_is_not_cached`). A load that succeeded earlier is kept until the app restarts (`domain_service.py` lines 8 to 13). |
| A header and no rows | The record read returns HTTP 200 with an error body. The summary route blocks. This is a different case from a missing file. It is listed so a reader does not treat it as healthy. |
| Target change (PROPOSED, later stage) | Return 503 JSON with the correlation id and write an audit row for the failure. Needs OQ-5. S07. |
| Label | **Verified Fact** for today. |

## Dependency 4 — The audit log

| | |
|---|---|
| What continues | `/health`. |
| What returns HOLD_FOR_REVIEW | Nothing. |
| What stops | `/records/{id}` and `/ai/summarize/{id}` with HTTP 500. The body holds no device data and no summary (probe P8). |
| Why it stops | No audit row means no answer. This keeps the rule that evidence exists before a change of state. **Verified Fact:** `main.py` lines 69 and 90 call `_audit` before the route returns its result. |
| Cost | On a summary the model has already run when the write fails (probe P8, `model_calls_before_the_failure` 1). The result is thrown away. The cost of one call is Unknown until S04-12. |
| Rule for future routes | A route that changes stored state (S07 approvals) writes the audit row first. If the write fails, the state is not changed. This follows `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. |
| A different failure | Rows can be lost without an error when threads write at once (FM-13). That failure is silent. Decision D-3 proposes a lock. |
| Label | **Verified Fact** for today. |

## Dependency 5 — The route thread pool

This is a shared resource and not an outside service. It decides whether the rows above stay true under load.

| | |
|---|---|
| What it is | 40 threads run the `def` routes. A summary holds one thread for the whole model wait. **Verified Fact:** `main.py` line 73; `load-scenarios.md`. |
| What continues while the model hangs | `/health` and `/records/{id}` return 200 after a delay (probe P5). |
| What stops | With a 10 second deadline, 4 summaries a second would fill all 40 threads (`load-scenarios.md` 1b). Other routes would then wait up to the deadline. This is an **Inference** for production rates, which are Unknown. |
| Design | The in-flight limit of 10 model calls (PROPOSED. Owner: Team-Force). |
| Label | **Verified Fact. REAL** for the measured delay. **Inference** for the higher rate. |

## Order of events on a summary request

The route does these steps in this order. **Verified Fact:** `main.py` lines 73 to 99.

1. Create or keep the correlation id.
2. Read the role. Check access. A refusal returns 403 and writes `policy.deny`.
3. Load the record.
4. Run the policy before the model. A true stale flag, a blank flag, or a missing id stops here. The model is not called.
5. Call the model under the deadline (and, after Half B, under the breaker and the in-flight limit).
6. Run the policy again on what the call measured.
7. Write the audit row.
8. Return the body.

A failure at step 3 or step 7 returns HTTP 500. A failure at step 5 returns HTTP 202. A failure at step 4 returns 403 or 202.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| DM-01 | When the AI path is down, `/health` and `/records/{id}` continue and the summary route holds with no summary. | **Verified Fact.** Probe P2, P3. | The baseline answer "Unknown" can be replaced by a measured answer. | Low | High | None. |
| DM-02 | A held case has no receiver. | **Verified Fact.** `main.py` has three routes. | Fail-to-person ends at a response body and an audit row. | High | High | The inbox is Unknown. S07. |
| DM-03 | `/health` stays 200 in every failure row. | **Verified Fact.** Probe P6, P7, P8. `main.py` lines 54 to 56. | A monitor sees no outage while both business routes fail. | High | High | A readiness route. S07. |
| DM-04 | Policy, file, and audit failures return 403 or 500 with no id for the cause. | **Verified Fact.** Probe P6, P7, P8. | A person cannot tell an outage from a refusal without logs. | Medium | High | OQ-5. |
| DM-05 | Under a hang, other routes slow down about 80 times. | **Verified Fact. REAL.** Probe P5. | The statement "other routes continue" needs the in-flight limit to stay fast. | High | High | Decision D-4. |
| DM-06 | The summary route runs the model before it writes the audit row. | **Verified Fact.** `main.py` lines 86 to 98. Probe P8. | An audit failure wastes one model call. | Low | High | None. |

## Lifecycle

`failure-mode-catalogue.md` holds the failures this design answers. `retry-and-circuit-breaker-strategy.md` holds the breaker and the limit. `docs/runbooks/incident-response.md` turns each row into triage and rollback steps. Stage S09 cites this file. Stage S10 uses it for defence question 8.
