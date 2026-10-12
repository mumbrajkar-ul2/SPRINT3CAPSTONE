# Retry and circuit-breaker strategy

| Field | Value |
|---|---|
| Stage | S04-11 — Reliability and failure engineering (Challenge 11), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Every number in this file is PROPOSED. Owner: Team-Force. The repo gives no measured model wait, request rate, or failure rate to base a number on. |
| Evidence sources | `apps/api/services/ai_gateway.py` (lines 53, 282 to 311); `apps/api/main.py`; `apps/api/services/policy.py`; `semantic-layer/ai-context-policy.yaml` (`policy.fail_to_person`); `docs/09-ai-guardrails/unsafe-output-handling-rules.md`; `docs/08-observability/slo-proposal.md`; `docs/10-performance/load-scenarios.md` scenario 1b; `docs/10-performance/evidence.md` HB-04; `docs/11-reliability/probe-output.json` (checks P2, P3, P5); `docs/02-baseline/defect-list.md` F18 |
| Assumptions | The model is a stub today (`local-sim-v1`). A real model's wait and failure rate are Unknown. The route runs on 40 threads (`load-scenarios.md`). Team-Force owns every PROPOSED item (operating contract row 10). |
| Unresolved issues | The model timeout default of 10 seconds is already PROPOSED by S04-09. The service-level proposal says 95 of 100 summaries finish in 2000 ms. The two numbers describe different things and nobody has accepted either. Open question OQ-1 and OQ-6 in `failure-mode-catalogue.md` (no failure id and no state words for the breaker). |
| Residual risks | A PROPOSED number copied into code as a fixed value looks approved. Half B reads each number from the environment, with the default written next to the word PROPOSED. |

## What this file is

This file says which calls retry, how often, and how long they wait. It says when the circuit breaker opens and what the route returns while it is open.

A circuit breaker stops calls to a failing service for a short time. It then lets one test call through. If that call works, normal calls resume.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A number marked PROPOSED is a proposal and not a measurement.

No code changes in Half A.

## Rules that do not change

These come from the YAML and the operating contract. They hold whatever numbers are chosen.

1. A retry never turns a failed call into an action. `policy.fail_to_person` says the system "never retries into an action" and "never fills in a default answer".
2. A failure stores the outcome and the reason. It does not store a made-up summary (`unsafe-output-handling-rules.md`).
3. A retry or an open breaker cannot change an outcome to RECOMMEND_ONLY. Only the model answer plus the policy can.
4. No path returns EXECUTE.

## Which calls retry

| Call | Retry? | Attempts | Wait between attempts | Why | Label |
|---|---|---|---|---|---|
| Model call that hits the deadline | No | 1 | Not applicable | A retry would double the wait the person sees. The case goes to a person. | PROPOSED. Owner: Team-Force. |
| Model call that fails before the prompt is accepted, for example a refused connection | Yes | 2 (the first try and 1 retry) | 0.5 seconds | The failure is fast and the prompt was not processed, so a repeat costs nothing extra. | PROPOSED. Owner: Team-Force. |
| Model answer that fails the schema | No | 1 | Not applicable | The model answered. Asking again hides a model that is drifting. The case goes to a person. | PROPOSED. Owner: Team-Force. |
| Policy engine (`opa` run fails) | No | 1 | Not applicable | The answer is deny or BLOCK. The code never allows a call because the engine failed (`policy.py` lines 141 to 148). | **Verified Fact** for the fail-closed rule. |
| Audit write | No | 1 | Not applicable | If the row cannot be written the request fails. A retry inside the request would delay the failure and add no evidence. | PROPOSED. Owner: Team-Force. |
| First load of `devices.csv` | Next request tries again | 1 per request | Not applicable | A failed load is not kept (test `test_a_missing_file_raises_and_is_not_cached`). No retry loop is needed for a local file. | **Verified Fact.** |
| Daily batch (`etl/run_daily_batch.py`) | A person runs it again | 1 per run | Not applicable | The batch writes no file, so a second run is safe. | **Verified Fact:** `run_daily_batch.py` has no write call. |
| Reader of events, alarms, or orders (built in S07) | Yes | 3 (the first try and 2 retries) | 1 second, then 2 seconds | A row that still fails after 3 tries is held aside and counted. It does not block the rows behind it. | PROPOSED. Owner: Team-Force. |
| A person sends the same summary request again | Allowed | No limit | Not applicable | The route changes no business row. A repeat costs one model call and one audit row (`idempotency-plan.md`). | **Verified Fact.** Probe P4. |

**What Half B builds from this table.** Half B builds the breaker only. It does not change the retry on a refused connection, because the gateway catches every error the same way (`ai_gateway.py` line 303) and cannot tell a refused connection from a bad answer. The first-try-plus-one-retry row waits for a change in `ai_gateway.py` that separates the error kinds. That change needs the failure id in OQ-1.

**Do not read the retry count for events as the data bound.** The PROPOSED bound of 1000 in defect F18 is a data check on `retry_count` values already in the file. It is not a retry policy. Both are PROPOSED. Neither is approved.

## The circuit breaker

### What it watches

One breaker watches the model call and nothing else. The policy engine, the file load, and the audit write each fail closed already.

| Result of one model call | Counts as a failure? | Why |
|---|---|---|
| The call hits the deadline | Yes | The model is slow or gone. |
| The call raises an error | Yes | The model is not reachable. |
| The answer fails the schema | No | The model answered. This is a content problem. |
| The policy returns BLOCK or HOLD before the model runs | No | The model was not called. |
| A schema-valid answer | Success | Resets the count. |

### When it opens

| Setting | PROPOSED value | Environment name | Owner |
|---|---|---|---|
| Consecutive failures that open it | 5 | `BREAKER_FAILURE_THRESHOLD` | Team-Force |
| Seconds it stays open | 30 | `BREAKER_OPEN_SECONDS` | Team-Force |
| Test calls allowed when it half opens | 1 | Fixed in code | Team-Force |

Why 5. It is half of the in-flight limit below (10), so the breaker opens before the limit is full. This is a design choice and not a measurement.

Why 30 seconds. It is three times the 10 second deadline. A test call that hangs finishes before the next test. This is a design choice and not a measurement.

States:

| State | What happens |
|---|---|
| Closed | Every call goes to the model. Failures are counted. A success sets the count to 0. |
| Open | No call goes to the model. Every request returns the held answer at once. After 30 seconds the state becomes half open. |
| Half open | One call goes to the model. Other requests get the held answer. If the call succeeds, the state is closed. If it fails, the state is open for another 30 seconds. |

### What it returns while open

| Part | Value |
|---|---|
| HTTP status | 202 |
| `outcome` | HOLD_FOR_REVIEW |
| `summary` and `recommendation` | null. The body never carries a made-up summary. |
| `reasons` | `failmode.timeout` as the nearest existing id. The policy also adds `failmode.schema_failure`, as it does for any timeout today (`policy.py` line 233). |
| Audit row | Action `policy.hold`, `outcome` HOLD_FOR_REVIEW. `model`, `model_version`, `prompt_hash`, `tokens`, and `latency_ms` are null. The nulls show that no call ran. |
| Model called | No |

Honest limit. `failmode.timeout` says the model did not answer in time. When the breaker is open, no call was made. Open question OQ-1 asks for an id that says "the model path is closed". Until S03 adds it, the reason id is the nearest one, and the null model fields in the audit row show the difference.

### Where its state lives

| Item | Rule |
|---|---|
| Storage | In the process. A restart closes the breaker. Two server processes have two breakers. |
| Clock | A monotonic clock, so a change of the system time does not open or close it. |
| Thread safety | One lock around the state. |
| Reset | A function that tests call. |

## The in-flight limit

The breaker alone does not protect `/health` and `/records`. It opens only after the failures come back, which takes one full deadline. During that time every arriving summary holds a route thread.

**Measured.** While 50 summaries waited on a hung model, `/health` took about 825 ms instead of about 10 ms (probe P5). The route has 40 threads.

**Proposed fix.** Limit how many model calls run at the same time.

| Setting | PROPOSED value | Environment name | Owner |
|---|---|---|---|
| Model calls in flight at once | 10 | `MODEL_MAX_IN_FLIGHT` | Team-Force |

When 10 calls are in flight, the 11th does not wait. It returns the held answer at once, with the same body as the open breaker. Route threads stay free for other routes.

Worked example. 50 summaries arrive at the same moment and the model hangs, with a 10 second deadline. Without a limit, 40 route threads wait 10 seconds, and 10 summaries queue. With the limit of 10, 10 calls wait. The other 40 return in milliseconds. At most 10 of the 40 threads are held for the 10 seconds. At least 30 stay free for `/health` and `/records`. This is an **Inference** from the thread counts. Half B measures it in the breaker test.

This limit is not in the playbook's Half B list. It is decision D-4 in `failure-mode-catalogue.md`. The recommended answer is yes.

## Leftover worker threads

Each model call starts a one-thread pool and does not wait for it when the deadline passes (`ai_gateway.py` lines 295 and 310). Probe P5 counted 3 threads before, 138 during, 76 right after the last answer, and 1 three seconds later. The thread of a late call ends when the model finishes.

A model that never returns would keep the thread. The in-flight limit also bounds this: at most 10 calls start, and with the breaker open no new call starts. This is an **Inference**.

## How settings reach the code

`apps/api/settings.py` has one function, `require(name)`. It raises when a name is absent, so it cannot supply a default. Half B adds a small reader for a number with a default. It reads the environment name, falls back to the PROPOSED default, and ignores a value that is empty, not a number, zero, or negative. That is the rule `configured_timeout_seconds` already follows (`ai_gateway.py` lines 249 to 260).

Each PROPOSED default sits in the code next to the words "PROPOSED. Owner: Team-Force." The YAML slot `fail_to_person.timeout_seconds` stays null until S05R.

## What this design does not do

- It does not set a service level. `docs/08-observability/slo-proposal.md` holds those numbers, all PROPOSED.
- It does not add a queue or a background worker. Both are PROPOSED only (SR-04 in `scaling-recommendations.md`).
- It does not use an outside breaker library. The playbook excludes one.
- It does not add a route. A readiness route is S07 scope.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| RB-01 | The model call has a deadline and no breaker. | **Verified Fact.** `ai_gateway.py` lines 53 and 295 to 301. No file in `apps/` holds breaker state. | Each request waits one full deadline during an outage. | High | High | None. |
| RB-02 | The deadline default of 10 seconds is 5 times the proposed 2000 ms service level. | **Verified Fact.** `ai_gateway.py` line 53. `slo-proposal.md` section 2. | A timeout is outside the proposed level. The two numbers have not been compared by an owner. | Medium | High | Team-Force decides both. |
| RB-03 | The breaker does not protect other routes in the first seconds of a hang. | **Verified Fact. REAL.** Probe P5. | `/health` and `/records` slow down by about 80 times. | High | High | Decision D-4. |
| RB-04 | The gateway cannot tell a refused connection from a bad answer. | **Verified Fact.** `ai_gateway.py` line 303. Probe P3. | A retry on a refused connection cannot be built until the kinds are separated. | Medium | High | OQ-1. |
| RB-05 | Every threshold is PROPOSED. | **Verified Fact.** This file. | The stage is CONDITIONAL PASS until Team-Force accepts them. | Medium | High | Owner: Team-Force. |

## Lifecycle

`failure-mode-catalogue.md` FM-03, FM-04, and FM-14 name the failures this file answers. Half B writes `apps/api/services/breaker.py` and reads the three environment names above. Stage S09 cites the breaker and the in-flight limit. Stage S10 uses this file for defence question 8.
