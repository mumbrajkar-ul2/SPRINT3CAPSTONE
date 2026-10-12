# Evidence — S04-12 Half B

| Field | Value |
|---|---|
| Stage | S04-12 — Cost and AI FinOps (Challenge 12), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), built with Cursor |
| Status | CONDITIONAL PASS. `metrics_from_audit.py` computes five of the seven `metrics.yaml` metrics from real audit rows. `metric.cost_per_correlated_incident` is a proxy only. `metric.quarantine_rate` and `metric.retry_count` have no audit source. Every token number is EDUCATIONAL. |
| Evidence sources | `docs/12-finops/metrics_from_audit.py` and `metrics_from_audit_output.txt`; `docs/12-finops/cost_baseline.py` and `cost_baseline_output_halfB.txt`; `logs/audit.log`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/main.py`; `tests/finops/test_metrics_from_audit.py`; `tests/observability/test_audit_schema.py`; `semantic-layer/metrics.yaml`; `docs/08-observability/log-schema.md`; `docs/11-reliability/recovery-evidence.md` |
| Assumptions | The audit rows come from test runs and demo calls on this machine. They are not production traffic. The EDUCATIONAL rate is 1.0 educational unit per 1000 tokens, read from the setting `FINOPS_EDU_RATE_PER_1K`. PROPOSED. Owner: Team-Force. It is not a price. |
| Unresolved issues | The model name, the price per token, and the money unit are Unknown. The ETL `quarantined` count has no stored place. A chain is not an incident, so cost per incident stays Unknown as defined. 11 older model-call rows have no `token_estimate_method`. |
| Residual risks | A reader can take 1.53 educational units as money. It is a teaching figure from a word-count formula. The latency of 11 ms is the time the 0.01 second stub takes. It says nothing about a real model. |

## How to repeat every run

From `06-telecom-service-network-incident-ops/`:

```text
.venv\Scripts\python.exe -m pytest tests policy/tests semantic-layer/tests -q -p no:cacheprovider
.venv\Scripts\python.exe docs/12-finops/cost_baseline.py
.venv\Scripts\python.exe docs/12-finops/metrics_from_audit.py
.venv\Scripts\python.exe docs/12-finops/metrics_from_audit.py --json
```

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. Number labels: **REAL**, **PRECOMPUTED**, **SIMULATED**, **EDUCATIONAL**.

## Step 1. Does the gateway write tokens and latency into the audit row?

**Verified Fact: yes.** Stage S04-09 added both. No field was missing.

| Field | Where it is computed | Where it reaches the audit row |
|---|---|---|
| `tokens` | `ai_gateway.py` line 319: `len(prompt.split()) * 2`, set when the model is about to be called | `GatewayResult.provenance()` (line 373) returns it. `main.py` passes it to `audit.write_event`. |
| `latency_ms` | `ai_gateway.py` line 336: `round((time.perf_counter() - started) * 1000)`, set in a `finally`, so a timeout also gets a value | Same path |
| `model`, `model_version`, `prompt_hash` | `provenance()` | Same path |
| All five | Null when no model call ran, such as a policy stop or a held call from the breaker | Same path |

Proof from real rows. The log has 17 model-call rows, and every one holds an integer `tokens` and an integer `latency_ms` (script output, REAL). The held row has all five null.

The one field that was missing is `token_estimate_method`. Step 3 adds it.

## Step 2. `metrics_from_audit.py`

It reads `logs/audit.log` and prints one table. It keeps four kinds of row apart so that no kind lowers the mean of another.

| Row kind | How the script recognises it | Used in the means |
|---|---|---|
| Model call | `model` is not null | Yes |
| Held, no call | `outcome` is `HOLD_FOR_REVIEW` and `model` is null | No. Counted on its own line. |
| No token row | New shape, action `ai.summary`, `model` null, not held | No |
| Old three-key row | No `tokens` key | No |

A timeout is a model call. Its row has a `model`, `tokens`, and a `latency_ms` equal to the wait. The breaker and the in-flight limit make no call, so those rows are held rows with nulls (**Verified Fact:** `recovery-evidence.md`).

### Output of the run

The run exited with code 0. The full text is in `metrics_from_audit_output.txt`. Rows REAL. Tokens EDUCATIONAL.

| Row count | Value |
|---|---|
| All rows | 240 |
| Old three-key rows | 96 |
| New-shape rows | 144 |
| Model-call rows | 17 |
| Held rows, no model call | 1 |
| `ai.summary` rows with no tokens | 2 |
| Other new-shape rows (read, deny) | 124 |
| `token_estimate_method` on the 17 model-call rows | `word_count_x2_EDUCATIONAL` on 6, missing on 11 |

| Metric id | Value | Label |
|---|---|---|
| `metric.tokens_per_invocation` | Mean 90.0 tokens over 17 calls. Sum 1,530. Smallest 90. Largest 90. | EDUCATIONAL |
| `metric.cost_per_correlated_incident` | Proxy. Mean 0.0900 educational units per `correlation_id`. 17 chains. Total 1.5300. | EDUCATIONAL. The metric stays Unknown as defined. |
| `metric.recommendation_latency` | Median 11.0 ms. 95th percentile 14 ms. Smallest 10, mean 11.3, largest 14. 17 calls. | REAL, stub model |
| `metric.ai_outcome_count` | `RECOMMEND_ONLY` 19, `HOLD_FOR_REVIEW` 1, `BLOCK` 1, `EXECUTE` 0 | REAL |
| `metric.audit_completeness` | Mean 0.707 over 144 new-shape rows | REAL. Required list PROPOSED. Owner: Team-Force. |
| `metric.quarantine_rate` | Not from the audit log | Gap |
| `metric.retry_count` | Not from the audit log | Gap |

Supplement, not in `metrics.yaml`: all 17 model calls share one `prompt_hash`, so 16 of them repeat the first. Those 16 repeats hold 1,440 tokens (EDUCATIONAL). One prompt means one device row, which the tests and demo calls ask about again and again. This is not a traffic rate.

### The held row, worked example

The log has 1 held row and 17 model calls. The mean over model calls is 90.0 tokens. If the held row were counted as 0 tokens, the mean would be 1,530 over 18 rows, which is 85.0 tokens. That is 5.6% lower and wrong, because no model ran. The script keeps the held row out of the mean. (EDUCATIONAL arithmetic.)

### `metric.quarantine_rate`: where the number comes from

**Verified Fact.** The ETL count `quarantined` prints to the output of `etl/run_daily_batch.py` (stage S04-11: real file gives processed 354, malformed 1, quarantined 1). It is not written to `logs/audit.log`. The script does not read it from the audit log and prints "not from the audit log".

Open question for S03: `metric.quarantine_rate` has no stored source. This design needs a place that keeps the ETL `quarantined` count and `processed` count for each run, so a dashboard can read the rate.

### `metric.retry_count`

**Verified Fact.** The value is `retry_count` in `service_orders.csv`. No audit row records a retry. The Half A script `cost_baseline.py` section 4 reads it (sum 943,094, SIMULATED). The audit script prints a gap line and names that source.

## Step 3. The EDUCATIONAL mark on the token formula

| Place | Change |
|---|---|
| `ai_gateway.py` line 56 | New constant `ESTIMATE_METHOD = "word_count_x2_EDUCATIONAL"`, with a comment that the formula is a word count doubled and is EDUCATIONAL |
| `ai_gateway.py` near line 319 | The comment on `tokens=len(prompt.split()) * 2` changed from SIMULATED to EDUCATIONAL, and names the audit field |
| `ai_gateway.py` line 391 | New method `GatewayResult.audit_provenance()`. It adds `token_estimate_method`, and it is null when `tokens` is null. |
| `audit.py` | New keyword `token_estimate_method`. The row has a fifteenth key at the end. The key is stored only when `tokens` has a value. |
| `main.py` | The AI route passes `audit_provenance()`. The response body still uses `provenance()`. |
| `docs/12-finops/metrics_from_audit.py` | Module text names the formula as EDUCATIONAL |

The method is an audit field only. The response body model forbids extra keys, so the API body is unchanged (test `test_a_model_call_row_carries_the_method_and_a_held_row_does_not` checks this).

A live row after the change, from `logs/audit.log` (shortened):

```json
{"correlation_id": "s04-12-demo-0", "action": "ai.summary", "model": "local-sim-v1", "tokens": 90, "latency_ms": 14, "outcome": "RECOMMEND_ONLY", "token_estimate_method": "word_count_x2_EDUCATIONAL"}
{"correlation_id": "s04-12-demo-held", "action": "policy.hold", "model": null, "tokens": null, "latency_ms": null, "outcome": "HOLD_FOR_REVIEW", "token_estimate_method": null}
{"correlation_id": "s04-12-demo-block", "action": "policy.deny", "model": null, "tokens": null, "latency_ms": null, "outcome": "BLOCK", "token_estimate_method": null}
```

Open question for S03: the YAML and `log-schema.md` have no field id for `token_estimate_method`. This design needs one. `log-schema.md` now carries a note about the fifteenth key.

### The rate comes from settings

`metrics_from_audit.py` reads `FINOPS_EDU_RATE_PER_1K` through `apps/api/settings.py` (`positive_number`). The default is 1.0. An empty, non-numeric, zero, negative, or non-finite value gives the default (test `test_the_rate_comes_from_settings_and_a_bad_value_gives_the_default`). `.env.example` has the name with a PROPOSED comment. Owner: Team-Force.

The name avoids the word TOKEN. `tests/security/test_secret_patterns.py` flags any upper-case setting name that contains it and holds a value. The first draft of the name failed that test and was renamed.

## Step 4. Runs

### Demo calls written to the real log

To get a held row and a blocked row in the real log, five calls went through the real routes with `TestClient` on 2026-10-11. They added 5 rows to `logs/audit.log`.

```text
POST /ai/summarize/REC-0001  x3  (X-Correlation-Id s04-12-demo-0, -1, -2)  200 RECOMMEND_ONLY, tokens 90
POST /ai/summarize/DEV-BAD1       (s04-12-demo-held)                       202 HOLD_FOR_REVIEW, tokens null
POST /ai/summarize/DEV-00003      (s04-12-demo-block)                      403 BLOCK, tokens null
```

All five used the header `X-User-Role: operator`. `DEV-BAD1` has a blank stale flag. `DEV-00003` has a true stale flag. Both cases match drill DR-4 in `recovery-evidence.md`.

The audit log is append-only. The full suite also writes to it, so the row counts above change on every suite run.

### Tests

| Run | Result | Label |
|---|---|---|
| `pytest tests/finops tests/observability` | 16 passed on the first run (13 finops, 3 observability). One more finops test was added after, so `tests/finops` now has 14. | REAL |
| Full suite: `pytest tests policy/tests semantic-layer/tests` | 269 passed, 2 skipped | REAL |
| Before this half (S04-11) | 255 passed, 2 skipped | REAL |
| Difference | 14 new tests, all in `tests/finops/test_metrics_from_audit.py` | REAL |

The 2 skipped tests need the `opa` binary, which this machine does not have.

One earlier test changed: `tests/observability/test_audit_schema.py` now expects the fifteenth key, with the method on a model call and null elsewhere. The first full run after the change failed once, in `tests/security/test_secret_patterns.py`, because of the setting name. After the rename the suite passed.

What the new tests check:

| Test group | Checks |
|---|---|
| Method field | The word is `word_count_x2_EDUCATIONAL`. A model-call row has it. A held row has null. Null `tokens` drops the method. The response body is unchanged. |
| Row kinds | Held rows, no-token rows, and old rows are counted apart and stay out of the mean. |
| Cost | Cost per `correlation_id` uses the rate. The rate comes from settings and bad values give the default. |
| Latency | The 95th percentile uses nearest rank. Outcomes are split. |
| Outcomes | All four words are named. Unknown words are kept apart. |
| Gaps | `metric.quarantine_rate` and `metric.retry_count` are named as gaps. |
| Output | An empty log gives Unknown, not 0. Every metric line has a label. JSON output parses. Repeated prompt hashes are counted. |

### Both scripts

| Script | Exit code | Output file |
|---|---|---|
| `cost_baseline.py` | 0 | `cost_baseline_output_halfB.txt`. The Half A file `cost_baseline_output.txt` is left as it was, because the Half A documents quote it. Sections 1 to 5 are identical. Section 6 shows the larger log. |
| `metrics_from_audit.py` | 0 | `metrics_from_audit_output.txt` |

Section 6 of the Half B baseline run (REAL): 240 rows. 29 rows have the `token_estimate_method` key. 1 `policy.hold` row. Actions: `record.read` 125, `policy.deny` 73, `ai.summary` 41, `policy.hold` 1. Half A showed 211 rows and 0 rows with the key.

## Findings

### FB-01

| | |
|---|---|
| Finding | The gateway already wrote `tokens` and `latency_ms` into the audit row. The only missing field was `token_estimate_method`, and it is now added. |
| Evidence | **Verified Fact. REAL.** Step 1. 17 of 17 model-call rows hold both. The new rows carry the method. |
| Impact | The audit row says how each token number was worked out. |
| Risk | Low. The 11 older model-call rows have no method. |
| Confidence | High |
| Open questions | Open question for S03: a field id for `token_estimate_method` (above). |

### FB-02

| | |
|---|---|
| Finding | Five of the seven metrics can be computed from the audit log. Two cannot. |
| Evidence | **Verified Fact. REAL.** Script output. `metrics.yaml` source fields. |
| Impact | The FinOps table covers tokens, cost proxy, latency, outcomes, and completeness. It does not cover quarantine rate or retry count. |
| Risk | Low |
| Confidence | High |
| Open questions | The stored place for the ETL count (above). |

### FB-03

| | |
|---|---|
| Finding | Held rows have null tokens and null latency. The script counts them on their own line and keeps them out of every mean. |
| Evidence | **Verified Fact. REAL.** 1 held row. Mean 90.0 over 17 calls. With the held row counted as 0, the mean would be 85.0 (EDUCATIONAL arithmetic). |
| Impact | The mean tokens per invocation is not lowered by calls that never ran. |
| Risk | Low |
| Confidence | High |
| Open questions | None. |

### FB-04

| | |
|---|---|
| Finding | Cost per correlated incident is still a proxy. The script groups by `correlation_id`, and a chain is not an incident. |
| Evidence | **Verified Fact.** The audit row has no incident id (Half A, `finops-dashboard-fields.md`). The script prints "the metric stays Unknown as defined". |
| Impact | Stage S07 can show one labelled number: the mean cost per chain, 0.0900 educational units. It must carry the word EDUCATIONAL and the word "chain". |
| Risk | High if the number is shown as cost per incident. |
| Confidence | High |
| Open questions | Open question for S03 (Half A): fields for incident id, flow name, and capability on the audit row. |

### FB-05

| | |
|---|---|
| Finding | A `BLOCK` outcome is written as a `policy.deny` row with `outcome` `BLOCK`. This answers an Unknown from Half A. |
| Evidence | **Verified Fact. REAL.** Row `s04-12-demo-block`. `metric.ai_outcome_count` shows `BLOCK` 1. |
| Impact | The outcome metric counts BLOCK correctly when the route writes the word. Older `policy.deny` rows from role denials have no outcome word. |
| Risk | Low |
| Confidence | High |
| Open questions | None. |

### FB-06

| | |
|---|---|
| Finding | Every number from the audit log is a test or demo number. No figure here describes production cost. |
| Evidence | **Verified Fact.** All 17 model calls share one `prompt_hash`, so they ask about one prompt, and the model is the stub. |
| Impact | The 90 tokens, 11 ms, and 0.0900 units describe a stub and one device row. |
| Risk | Medium. Stage S09 must not cite them as a measured operating cost. |
| Confidence | High |
| Open questions | The live model, price, and traffic are Unknown until S07 and a hosted model exist. |

## Changes to earlier files

- `apps/api/services/audit.py`: a fifteenth key and one keyword.
- `apps/api/services/ai_gateway.py`: one constant, one method, two comments.
- `apps/api/main.py`: the AI route passes `audit_provenance()`.
- `tests/observability/test_audit_schema.py`: expects the fifteenth key.
- `.env.example`: one new name, `FINOPS_EDU_RATE_PER_1K`, with a PROPOSED comment.
- `docs/08-observability/log-schema.md`: a note about the fifteenth key.
- `docs/12-finops/finops-dashboard-fields.md`: an update note about the `BLOCK` row.
- `logs/audit.log`: grew by the rows the runs wrote. Five rows are the demo calls above.

## Completion gate

Half B PASS needs `metrics_from_audit.py` to compute the `metrics.yaml` metrics from real audit rows. It does so for five metrics. Two have no audit source, and the script says so. Cost per incident is a proxy. The status is CONDITIONAL PASS for those reasons.

## Decisions after Half B (2026-10-11)

Mangesh (FDE) asked for final values for the two PROPOSED items. Owner: Team-Force. Neither is measured.

| Item | Decision | Label |
|---|---|---|
| Educational rate | Keep 1.0 educational unit per 1000 tokens. Not money. | EDUCATIONAL |
| Cache lifetime for OB-01 | 300 seconds. Only `RECOMMEND_ONLY` answers are stored. The cache is emptied when the policy version or the model version changes. At most 500 answers. Built in S07. | DECIDED, not measured |

The reasons and the review triggers are in `optimization-backlog.md`, section "Decisions". No code changed for these decisions. The rate was already 1.0. The cache is not built.

## Open questions for S03 (all from this stage)

- A metric for cost per flow.
- A metric for repeated prompts.
- A link from a call row to an event.
- Incident id, flow name, and capability fields on the audit row.
- A field id for `token_estimate_method`.
- A stored place for the ETL `quarantined` count.
- A list of real model names, and a list of risk levels.
- A percentile rule for `metric.recommendation_latency`.
- A timestamp field on service orders.
- Allowed alarm fields for a batch prompt.
- A field on the audit row that says an answer came from the cache.

## Lifecycle

Stage S05-14 rebuilds a case from rows that share one `correlation_id`. It can read `tokens` and `token_estimate_method` from those rows. Stage S07 shows one labelled cost number, taken from `metrics_from_audit.py`. Stage S09 cites the per-flow cost from Half A and the guard in `optimization-backlog.md` OB-05. Stage S05R folds the open questions into the YAML.
