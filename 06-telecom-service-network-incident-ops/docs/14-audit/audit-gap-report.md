# Audit gap report

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The old row answered none of the 8 provenance questions in full and 3 in part. The row today answers 2 in full (model and version, trace id), 4 in part, and 2 not at all (approval, final action). Two answers got worse: the row no longer names the record, and it no longer names the reason for a refusal. |
| Evidence sources | `docs/00-setup/replay-log.md` (sections 2.7, 3, and 5, items 3 and 5); `docs/02-baseline/behaviour-snapshot.md` (section on `POST /ai/summarize/REC-0001`); `docs/08-observability/log-schema.md`; `docs/08-observability/trace-design.md`; `docs/09-ai-guardrails/model-provenance-design.md`; `docs/13-security-validation/remediation-backlog.md` (`SB-03`, `SB-09`, `SB-12`, `BL-09`); `docs/11-reliability/failure-mode-catalogue.md` (`FM-01`, `FM-12`, `RF-04`); `apps/api/services/audit.py`; `apps/api/main.py`; `logs/audit.log` (240 lines, counted 2026-10-12); `evidence/junit-security.xml` |
| Assumptions | The rows in `logs/audit.log` come from test runs and demo calls on this machine. They are not production traffic. A row is called REAL because the app wrote it. The model text behind an `ai.summary` row is SIMULATED. |
| Unresolved issues | The findings below carry lines that start with "Open question for S03:". S05R folds them into the YAML. |
| Residual risks | The audit log is one plain file. Anyone with file access can change or delete a line. This report cannot prove that the 240 lines are all the lines that were ever written. |

## What this file is

This file says what the audit log could not prove before, and what it still cannot prove today. It answers the eight questions in defence question 5 of `Project_Intent.md` section 3.3, except "what cannot be proven", which is the last section.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a log line, a test, or a file.

## The three row shapes in `logs/audit.log`

The file has 240 lines. **Verified Fact. REAL.** Counted 2026-10-12 with a read-only script. `git status` shows the file unchanged.

| Lines | Keys per line | Count | What they are |
|---|---|---|---|
| 1 to 96 | 3: `ts`, `action`, `details` | 96 | The old row. No `correlation_id`. |
| 97 to 240, written before S04-12 Half B | 14 | 115 | The S04-08 row. Has `correlation_id`. |
| 97 to 240, written after S04-12 Half B | 15 | 29 | The row today. Adds `token_estimate_method`. |

Two facts about the 144 newer rows. **Verified Fact. REAL.**

- Every row has a `correlation_id`. No two rows share one. The log holds no case with more than one row.
- `policy_decision` is null on all 144 rows. `approval_id` is null on all 144 rows.

The old row, from `replay-log.md` section 3, for `POST /ai/summarize/REC-0001` with no role header:

```json
{"ts": "2026-10-08T18:58:49.478925", "action": "ai.summary", "details": {"record_id": "REC-0001", "model": "local-sim-v1"}}
```

What `details` held across the 96 old lines. **Verified Fact. REAL.**

| `action` | Lines | Keys inside `details` |
|---|---|---|
| `record.read` | 54 | `record_id` (54), `role` (54) |
| `ai.summary` | 22 | `record_id` (22), `model` (22), `outcome` (5) |
| `policy.deny` | 20 | `record_id` (20), `role` (20), `route` (20), `reasons` (20), `outcome` (2) |

## The eight questions

The table answers each question twice: for the old row, and for the row today. "Yes" means one row answers it. "In part" means one row gives some of the answer. "No" means the row has no value for it.

| # | Question | Old row | Why (old row) | Row today | Why (row today) |
|---|---|---|---|---|---|
| 1 | Who acted? | No | 0 of 96 lines have an actor. 74 lines have a `role` word inside `details` (54 `record.read`, 20 `policy.deny`). The 22 `ai.summary` lines have none, because the summary route checked no role. | In part | `actor` is a persona word for `operator`, `engineer`, and `ai_agent`. It is null for `admin`, `clinician`, and a missing header. The role is a word the caller typed. Nothing proves the caller holds it (`SB-09`). |
| 2 | What was the request? | In part | `action` plus `record_id` on 96 of 96 lines. `policy.deny` lines also have `route`. The S00 line for `DOES-NOT-EXIST` names the asked id, while the response held `REC-0001` (`replay-log.md` section 5, item 3). | In part, and worse | `action` names the kind of call. `resource` is always `resource.device`. The row has no record id and no route. Two refused summaries of different records give rows that differ only in time and id (calls C and D in `evidence-chain-one-case.md`). See finding AG-03. |
| 3 | What data was used? | No | The line holds the asked id only. The prompt held the whole device row, including `mgmt_ip` and `credential_profile` (defect F12). Nothing about that was stored. | In part | `prompt_hash` is the SHA-256 of the prompt text. It exists only on rows where the model ran. A reviewer proves it by rebuilding the prompt from the same device row. This stage did that for `REC-0001` and the hash matched (see `evidence-chain-one-case.md`). |
| 4 | Which model and version? | In part | `details.model` holds `local-sim-v1` on 22 lines. There is no version. | Yes | `model` and `model_version` are on every row where the model ran. Both hold `local-sim-v1`, the same text (`SB-15`). Both are null when the call stopped before the model. |
| 5 | Which policy result? | In part | 20 `policy.deny` lines hold `reasons`. 7 lines hold an `outcome` word. The 22 `ai.summary` lines from S00 have no policy result, because the route called no policy. | In part, and worse | `policy_decision` is null on 144 of 144 rows. The result shows only in the `action` word (`policy.deny` or `policy.hold`) and in `outcome`. The reason list and `policy_version` are no longer on the row. See finding AG-02. |
| 6 | Which approval? | No | No `approval_id` on any line. No route writes one. | No | `approval_id` is null on 144 of 144 rows. The approval route is S07. |
| 7 | What was the final action? | No | No field. | No | No field. By the code, no route changes a device, so the final action is none. That is shown by `test_no_route_can_execute`, not by a stored value. |
| 8 | Which trace id? | No | 0 of 96 lines have a `correlation_id`. A caller cannot find these lines by id. | Yes, with a limit | `correlation_id` is on 144 of 144 rows. The caller may choose it. Another caller may reuse it. See finding AG-05. |

Count. The old row answers 0 questions in full, 3 in part (questions 2, 4, 5), and 5 not at all. The row today answers 2 in full (questions 4 and 8), 4 in part (questions 1, 2, 3, 5), and 2 not at all (questions 6 and 7).

**Worked example for question 5.** Two summary calls by `operator` on 2026-10-12. One asked for `DEV-00001`, which the data file has no row for. One asked for `DEV-00003`, which has a true stale flag. Both stopped before the model. Both wrote this row, with only `ts` and `correlation_id` different:

```json
{"action": "policy.deny", "actor": "noc_operator", "role": "operator", "outcome": "BLOCK", "policy_decision": null, "model": null, "prompt_hash": null}
```

The HTTP bodies held different reasons (`failmode.missing_id` and `failmode.stale_topology_true`). The stored rows do not. **Verified Fact.** Probe in `evidence-chain-one-case.md`, calls C and D.

## Old lines have no correlation id

96 of 240 lines have no `correlation_id`. That is 40 percent of the file. **Verified Fact. REAL.**

`GET /audit/{correlation_id}` in Half B looks rows up by that id. It cannot return any of these 96 lines. A reviewer who wants one of them must read the file by hand. Each of the 96 lines is its own case of one line, with no link to a policy check or a model call for the same request.

## Findings

### AG-01

| | |
|---|---|
| Finding | 96 of 240 lines have 3 keys and no `correlation_id`. The route in Half B cannot return them. |
| Evidence | **Verified Fact. REAL.** Key counts above. `audit.py` `SCHEMA_KEYS`. `docs/08-observability/log-schema.md` ("The row today"). `SB-12`. |
| Impact | Every call made before 2026-10-11 22:19 UTC (the first new row) is outside any rebuilt case. |
| Risk | Medium. The calls are test and replay calls on this machine. In production the same gap would hide real decisions. |
| Confidence | High |
| Open questions | None. The old lines stay, because the log is append-only. |

### AG-02

| | |
|---|---|
| Finding | `policy_decision` is null on all 144 new rows. The reason list and the policy version are also off the row. The only trace of the policy result is the `action` word and `outcome`. |
| Evidence | **Verified Fact. REAL.** `audit.py` line 93 sets `"policy_decision": None` and `write_event` has no argument for it. `docs/08-observability/evidence.md` says the S04-08 half left it null on purpose. Rows C and D in `evidence-chain-one-case.md`. |
| Impact | A reviewer who asks "why was this call refused?" reads the row and cannot tell. A refusal for a missing id and a refusal for a stale topology flag look the same. |
| Risk | High. The route already computes the answer and the reasons, and does not store them. |
| Confidence | High |
| Open questions | Open question for S03: `policy_decision` has two names, `concept.policy_decision` and `provenance.policy_result` (already LS-Q6 in `log-schema.md`). This design needs one id, and needs an id for the reason list and for the policy version, so a row can say why. |

### AG-03

| | |
|---|---|
| Finding | The new row dropped the record id. It says what kind of call happened and does not say which record. |
| Evidence | **Verified Fact. REAL.** `audit.py` writes 15 keys and none is a record id. `docs/08-observability/log-schema.md` open question LS-Q7. The old row had `details.record_id` on 96 of 96 lines. |
| Impact | A reviewer cannot tell a read of `REC-0001` from a read of any other device. For a summary, `prompt_hash` is the only link, and only on a call that reached the model. |
| Risk | High. This is the "what request" and "what data" part of defence question 5. |
| Confidence | High |
| Open questions | Open question for S03: there is no field id for the record id on an audit row (LS-Q7). This design needs one so the row names the record. |

### AG-04

| | |
|---|---|
| Finding | The row has no field for the final action, and `approval_id` is null on every row. |
| Evidence | **Verified Fact. REAL.** Row key list. `approval_id` non-null count is 0 of 144. `test_no_route_can_execute` in `policy/tests/test_policy_python.py`. `docs/00-setup/replay-log.md` section 5 and `business-flow-reconstruction.md` flow 4: no approval route exists. |
| Impact | "No change happened" is true by code review and is not stored on any row. A reviewer cannot read it from the log. |
| Risk | Medium today, because no route changes anything. High once S07 adds the approval and execute path. |
| Confidence | High |
| Open questions | Open question for S03: there is no id for the final action of a decision (what changed, or none). This design needs one so S07 can fill it. |

### AG-05

| | |
|---|---|
| Finding | The caller chooses the `correlation_id`, and the API stores it unchanged. A second call that sends the same id adds a row to the first call's case. |
| Evidence | **Verified Fact.** `audit.correlation_id_from_header` keeps any non-empty header. Call E in `evidence-chain-one-case.md`: an `ai_agent` read sent `s0514-case-0001` and its row joined the operator's case. `SB-03` (no length limit). `docs/11-reliability/idempotency-plan.md` line 87: five calls with one id gave five rows. |
| Impact | A rebuilt case can hold rows from a different caller. The rows keep their own `actor` and `role`, so a careful reader can see the mix. |
| Risk | Medium. A caller can add rows to a case. A caller cannot remove rows. |
| Confidence | High |
| Open questions | Open question for S03: there is no rule id for the allowed form of a correlation id (length and characters). Half B needs one number to refuse a very long id. |

### AG-06

| | |
|---|---|
| Finding | The log cannot prove it is complete or unchanged. |
| Evidence | **Verified Fact.** `audit.py` opens the file in append mode. The write lock covers one process (decision D-3, `recovery-evidence.md`). `SB-12`. `T-B8-06` in `security/threat-model.md`. A write failure returns HTTP 500 with no `X-Correlation-Id` header, and a summary has already called the model by then (`FM-12`, `RF-04`). `BL-09`: the file is tracked by git and each test run adds rows (`docs/13-security-validation/evidence.md`, EV-07). |
| Impact | Four things can be missing without a trace: an edited line, a deleted line, a row from a second server process, and a row for a call that ended in 500. |
| Risk | Medium. **Inference:** the git history of the tracked file shows a change to a committed line, so it works as a partial check. It covers only lines that were committed. |
| Confidence | High |
| Open questions | None. A database or an external store is PROPOSED only, and is out of scope for this stage. |

### AG-07

| | |
|---|---|
| Finding | A reader cannot tell a test row from a real call. |
| Evidence | **Verified Fact. REAL.** The 144 new rows hold roles `operator` (75), `clinician` (34), `ai_agent` (17), `automation_service` (17), and null (1). **Inference:** the 34 `clinician` and 17 `automation_service` rows come from test runs, because the policy tests send those roles. No field marks a row as a test row. |
| Impact | A count of "denied calls" in the real log mixes tests with traffic. |
| Risk | Low today. Medium when the log serves a real reviewer. |
| Confidence | Medium |
| Open questions | Open question for S03: no field says whether a row came from a test run or from real traffic. This design needs one if a reviewer is to count only real calls. |

### AG-08

| | |
|---|---|
| Finding | Two columns hold a claim, not a proven fact: `role` and `actor`. |
| Evidence | **Verified Fact.** `main.py` reads `X-User-Role` and nothing else. `SB-09`. `actor` comes from a fixed map of three role words (`audit.py` `_ACTOR_FOR_ROLE`). The map is an Inference in `access-semantics.yaml`. |
| Impact | The row says who the caller said they were. |
| Risk | High if the app is reachable by more than the team. |
| Confidence | Medium. Whether authentication is in scope for this packet is Unknown. |
| Open questions | Open question for S03: there is no field id for the named person on an API call (LS-Q2). |

## Lifecycle

`decision-provenance-model.md` turns these gaps into a field list. `evidence-chain-one-case.md` shows one case end to end. `audit-read-access-design.md` proposes who may read the log. Half B builds the route and lists the unproven items in `cannot_prove`.
