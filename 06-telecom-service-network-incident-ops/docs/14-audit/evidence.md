# Audit route evidence

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half B |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. `GET /audit/{correlation_id}` rebuilds the Half A case from stored rows, in time order, and lists what the rows cannot prove. Seven calls were tried and each gave the expected status. 32 new tests pass. All 327 tests pass with no skip. The status is conditional because `approval_id` is null on every row and the route lists it under `cannot_prove`. The route also does not close the gaps in the log itself (see "What the route cannot fix"). |
| Evidence sources | `apps/api/main.py`; `apps/api/services/audit_query.py`; `apps/api/services/policy.py`; `policy/opa/policy_data.json`; `policy/tests/`; `tests/audit/test_audit_rebuild.py`; a scratch run on 2026-10-12 (script at the end); `docs/14-audit/audit-read-access-design.md`; `docs/14-audit/evidence-chain-one-case.md` |
| Assumptions | The Python copy of the policy ran in the scratch run and in every test under `tests/` (see "Which policy engine ran"). The rows in the scratch run are REAL: the app wrote them. The model is the stub `local-sim-v1`. Its summary text is SIMULATED and is not stored. Token counts are EDUCATIONAL estimates. |
| Unresolved issues | Four new words have no id in the YAML (see "Open questions for S03"). Rows for admin reads have no actor. The log can still be edited by hand. |
| Residual risks | A person with the `admin` header word can read every case, and the header is a word the caller types (`SB-09`). The route proves what the log holds. It cannot prove the log is complete (`SB-12`). The files in `evidence/` were rewritten by `scripts\evidence.ps1` after Half B (see "Test counts"). `evidence/linux-py311/` is still the S04-07 Linux run. |

## What this file is

This file records what Half B built, the tests, and one run of the route on the Half A case. All output below came from real commands on 2026-10-12. None was typed by hand.

Commands ran from `06-telecom-service-network-incident-ops/` with the repo `.venv` Python. Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## What Half B built

| File | What changed |
|---|---|
| `policy/opa/policy_data.json` | New row TA-35: `role.admin` may do `action.read` on `resource.audit_log`, for `purpose.audit_review`, scope `scope.all_records`, risk `risk.read_only`. The Rego file and the Python file both read this JSON, so both now hold the row. |
| `policy/opa/access.rego` | Two comments updated. The matching code did not change. |
| `apps/api/services/policy.py` | New function `check_audit_read(role_id)`. It builds the TA-35 input and calls the existing `evaluate_access`. The matching code did not change. |
| `policy/tests/fixtures/` | Two new access fixtures. `ac-06` is admin reading the audit log (allow, row TA-35). `ac-07` is operator reading the audit log (deny, no row). |
| `policy/tests/test_policy_python.py` | Counts moved: 23 to 25 fixtures, 5 to 7 access fixtures, 34 to 35 rows. Two new tests. The Python-versus-Rego agreement test now also sends the audit-read call for five roles. |
| `policy/tests/access_test.rego` | Counts moved: 34 to 35 rows, 5 to 7 access fixtures. Two new Rego tests for TA-35. |
| `apps/api/services/audit_query.py` | New. Reads `audit.LOG`, picks the rows for one id, sorts them by `ts`, and builds the `cannot_prove` list. It never writes. |
| `apps/api/main.py` | New route `GET /audit/{correlation_id}`. The helper `_audit` takes a `resource` argument. It still defaults to `resource.device`. |
| `tests/audit/test_audit_rebuild.py` | New. 32 tests. All are marked `security`. None is skipped. |
| `docs/03-identity/target-access-matrix.md` | A note under the table adds TA-35. The 34 rows are unchanged. |

## How the route answers

Checks run in this order.

| Step | Check | Result if it fails | Own audit row |
|---|---|---|---|
| 1 | Policy. Only `role.admin` matches TA-35. A missing header has no role and is denied. | 403 `{"error": "forbidden"}` | `policy.deny` on `resource.audit_log` |
| 2 | The id in the path is 128 characters or fewer. | 400 `{"error": "id_too_long", "max_length": 128}` | `audit.id_refused` |
| 3 | At least one row has this id. | 404 `{"error": "not_found"}` | `audit.not_found` |
| 4 | None failed. | 200 with `correlation_id`, `row_count`, `rows`, and `cannot_prove` | `audit.read` |

Policy runs first. A caller without permission gets the same 403 body for an id that exists and an id that does not. The id length is checked only after policy, so a caller without permission cannot learn anything from the 400.

The route writes its own row after it has read the log. The answer therefore does not list the request that asked for it.

## Which policy engine ran

**Verified Fact.** These checks used the Python copy of the policy.

| Where | Engine | Why |
|---|---|---|
| Every test under `tests/`, including `tests/audit/` | Python copy | `tests/conftest.py` sets `POLICY_ENGINE=python` for each test (backlog row `SB-20`). With `opa` on the PATH each decision starts a new `opa` program and is about 15 times slower. |
| The scratch run below | Python copy | The script sets `POLICY_ENGINE=python`. |
| `policy/tests/test_policy_python.py` | Python copy, plus a test that runs `opa eval` | The two agreement tests give the Python copy and the Rego copy the same inputs and compare the answers. With `opa` on the PATH they ran and passed. |
| `opa test policy/opa policy/tests` | Rego copy | 32 of 32 Rego tests passed. |
| The app with `POLICY_ENGINE` unset | `opa` when it is on the PATH, otherwise the Python copy | This is the setting a real server would use. Whether production runs `opa` as a long-lived server is Unknown (`SB-20`). |

This shell did not have `opa` on the PATH at the start of the stage. The binary is at `C:\Users\mange\tools\opa\opa.exe`. Without it, the two agreement tests skip, and the security stage fails on the skip guard (`SB-10`). That is the guard working. The run below used `opa` 1.21.1 on the PATH.

## Test counts

**Verified Fact.** Output of these commands on 2026-10-12 on Windows, Python 3.13.5, `opa` 1.21.1 on the PATH. The first runs wrote junit files to a temporary folder. Then `scripts\evidence.ps1` ran all stages at 07:51 UTC with `opa` on the PATH and rewrote the files in `evidence/`. It gave the same counts as the table. Exit codes: lint, pip_audit, and bandit exit 1 on real findings (ruff 11, pip-audit 18 entries of which 9 are unique, bandit 2 LOW). The other eight stages exit 0. The script deletes `evidence/linux-py311/` in its first step, so that folder was restored from git.

| Stage | Command | At S05-13 Half B | Now | Change |
|---|---|---|---|---|
| tests | `pytest tests -m "not security"` | 97 passed | **97 passed, 0 skipped** | None |
| semantic_layer | `pytest semantic-layer/tests` | 35 passed | **35 passed** | None |
| policy | `pytest policy/tests` | 83 passed | **87 passed, 0 skipped** | +4: 2 new tests and 2 new fixtures |
| opa | `opa test policy/opa policy/tests` | 30 of 30 | **32 of 32** | +2 Rego tests for TA-35 |
| security | `pytest -m security`, then `scripts/check_junit_no_skips.py` | 159 passed | **195 passed, 0 skipped.** Guard exit 0. | +36: 32 in `tests/audit` and 4 in `policy/tests` |
| lint | `ruff check` | 11 findings | **11 findings** | None. The new code added none. |
| bandit | `bandit -r apps` | 2 LOW | **2 LOW** | None |

The full script also ran `pip_audit` (18 entries, 9 unique, same as S05-13), the SBOM, and the checksums stage. `requirements.txt` did not change.

Worked example of the security count. The marker covers 159 tests from S05-13. This stage adds 32 audit tests, 2 new policy tests, and 2 new fixture tests. 159 + 32 + 2 + 2 = 195.

**Real log.** `git status --short logs` was clean after the tests in `tests/audit`. `logs/audit.log` still has 240 lines. The full test run does add 8 rows to the tracked log (backlog row `BL-09`). Those 8 rows were removed with `git checkout -- logs/audit.log` so the Half A numbers stay true.

## The Half A case, run through the route

The scratch run made the same three calls as Half A, with `X-Correlation-Id: s0514-case-0001`. It pointed `audit.LOG` at a temporary file. Then it called the new route.

### R1: admin reads the case

`GET /audit/s0514-case-0001` with `X-User-Role: admin` and `X-Correlation-Id: s0514-read-1`. Status 200. `row_count` 3. The rows came back in time order.

```text
ROW {"ts": "2026-10-12T07:41:34.584554", "correlation_id": "s0514-case-0001", "actor": "noc_operator", "role": "operator", "action": "record.read", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
ROW {"ts": "2026-10-12T07:41:34.608602", "correlation_id": "s0514-case-0001", "actor": "noc_operator", "role": "operator", "action": "ai.summary", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": "local-sim-v1", "model_version": "local-sim-v1", "prompt_hash": "e17907200e7e3bae144dba21da6f6056952d8382a5fdc24cb8744125dd5ab61d", "tokens": 90, "latency_ms": 14, "outcome": "RECOMMEND_ONLY", "token_estimate_method": "word_count_x2_EDUCATIONAL"}
ROW {"ts": "2026-10-12T07:41:34.628695", "correlation_id": "s0514-case-0001", "actor": null, "role": "clinician", "action": "policy.deny", "resource": "resource.device", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

**Verified Fact.** The three rows hold the same action words, roles, and prompt hash (`e17907…ab61d`) as the rows in `evidence-chain-one-case.md`. Only `ts` and `latency_ms` differ, because the calls ran again.

The `cannot_prove` list in the response had these ten items:

| Item | Reason the route gave |
|---|---|
| `approval_id` | `approval_id` is null on every row. No approval route exists until S07. |
| `policy_decision` | `policy_decision` is null on every row. The action word and outcome are the only trace of the policy result. |
| `actor` | At least one row has no actor. The role has no persona, or the header was missing. |
| `final_action` | No column holds the final action. By the code no route changes a device. |
| `record_asked_for` | No column holds the record id the caller asked for. |
| `policy_reasons_and_version` | The reasons and the policy version are not stored on any row. |
| `caller_identity` | The role is a header word the caller typed. Nothing proves who the caller was. |
| `case_membership` | The caller chose the correlation_id. A second caller can reuse it and add a row to this case. |
| `log_integrity` | The log is a plain file. A line can be changed or deleted. This route cannot prove the case is complete or unchanged. |
| `rows_before_correlation_id` | 0 line(s) in the log have no correlation_id and can never be returned here. |

The `model` item is not on the list for this case, because row 2 holds a model. **Verified Fact.**

The route wrote one row of its own. The log grew by exactly one line:

```text
{"ts": "2026-10-12T07:41:34.649804", "correlation_id": "s0514-read-1", "actor": null, "role": "admin", "action": "audit.read", "resource": "resource.audit_log", "policy_decision": null, "approval_id": null, "model": null, "model_version": null, "prompt_hash": null, "tokens": null, "latency_ms": null, "outcome": null, "token_estimate_method": null}
```

### R2: another caller reuses the id, then admin reads again

Call E from Half A ran: `GET /records/REC-0001` as `ai_agent` with the same id. Then admin read the case again. Status 200. `row_count` 4. The fourth row has `actor` `ai_agent`. **Verified Fact.** This shows the gap `case_membership` names. The caller picks the id, so a second caller can add a row to the case. The `actor` column is the only sign that the row came from someone else.

### R3 to R7: other callers and inputs

| Call | Request | Status | Body | Own row `action` | Own row `resource` |
|---|---|---|---|---|---|
| R3 | `operator` asks for `s0514-case-0001` (exists) | 403 | `{"error": "forbidden"}` | `policy.deny` | `resource.audit_log` |
| R4 | `operator` asks for `s0514-no-such-case` (does not exist) | 403 | `{"error": "forbidden"}` | `policy.deny` | `resource.audit_log` |
| R5 | No `X-User-Role` header | 403 | `{"error": "forbidden"}` | `policy.deny` (role null) | `resource.audit_log` |
| R6 | `admin` asks for `s0514-no-such-case` | 404 | `{"error": "not_found"}` | `audit.not_found` | `resource.audit_log` |
| R7 | `admin` sends an id of 129 characters | 400 | `{"error": "id_too_long", "max_length": 128}` | `audit.id_refused` | `resource.audit_log` |

**Verified Fact.** The R3 and R4 response bodies were byte for byte the same. A caller without permission cannot tell an id that exists from one that does not.

After all seven calls the temporary log had 11 lines: 4 case rows and 7 route rows. The real `logs/audit.log` had the same SHA-256 and the same 240 lines before and after. **Verified Fact.**

The R2 response held neither `mgmt_ip` nor `credential_profile`. **Verified Fact.**

**GitHub run.** **Verified Fact.** The workflow ran for commit `78c79b3` on 2026-10-12: run [38221204638](https://github.com/mumbrajkar-ul2/SPRINT3CAPSTONE/actions/runs/38221204638). In the uploaded artifact, `junit-security.xml` has 195 tests with 0 failures, 0 errors, and 0 skipped. Stage 6 (security tests, no skips allowed) passed. `opa-test.json` has 32 of 32 passed. The job is red because lint, pip_audit, and bandit exit 1 on the known findings.

## What the 32 tests check

| Group | What a test proves |
|---|---|
| Chain | Rows come back in time order. Rows written out of order still come back sorted. Two cases do not mix. Old lines with no id are never returned and are counted. A line that is not JSON is counted and skipped. |
| No rows | An unknown id gives 404 and the route's own row. A missing log file gives 404, not an error. |
| No permission | Six callers (operator, engineer, ai_agent, an unknown word, `ADMIN` in capitals, no header) each get 403 and a `policy.deny` row on `resource.audit_log`. The 403 body is the same for an id that exists and one that does not. A 500-character id from a caller without permission gets 403, not 400. |
| Read only | The log is the same except for one new line. The real log is not touched. The source of `audit_query.py` holds no write call. |
| What leaves the route | A normal chain holds no `mgmt_ip`, no `credential_profile`, and no credential name. A forbidden name stored in a row is replaced in the answer, and the stored line stays as it was. An id that is a forbidden name is not echoed. |
| Id limit | 129 characters gives 400 and the id is not stored. Exactly 128 is looked up. The limit constant is 128. |
| Cannot prove | `approval_id` and `log_integrity` are always listed for these rows. The five fixed items are listed. `actor` and `policy_decision` follow the null fields. `model` is not listed when a row holds a model. `approval_id` is not listed when a row holds an approval id. |

## What changed from the Half A design

| Change | Why |
|---|---|
| The route uses three new action words on its own row: `audit.read`, `audit.not_found`, `audit.id_refused`. The 403 case reuses `policy.deny`. | The `outcome` column holds AI words only. A reviewer needs to tell a served read from a miss and from a refusal. The action word is the only other column. |
| The answer replaces any text value that holds a forbidden field name or credential name with `<withheld: forbidden name>`. The `cannot_prove` list then gains an item `withheld_text`. | Backlog row `SB-03` stores header text as typed. Without this step the route could return a name that a caller wrote into the log. The stored line is not changed. |
| The `cannot_prove` list gains `unreadable_lines` when a line cannot be parsed. | A skipped line would otherwise be silent. |

## What the route cannot fix

| Gap | Why the route cannot close it |
|---|---|
| The admin's own row has `actor` null. | `role.admin` has no persona, so `actor_for_role` returns null. A reviewer reading the log cannot see which admin read a case. This follows the `SB-09` gap. |
| The log can be edited. | The route reads a plain file (`SB-12`). It cannot prove no line was removed. |
| The id belongs to the caller. | Another caller can reuse it (R2). |
| A 500 has no id and no row. | `RF-04` is outside this stage. |
| The record id and the policy reasons are not in any row. | These are columns the log does not have (findings `AG-02` and `AG-03`). Changing the row shape is outside Half B. |

## Open questions for S03

- Open question for S03: the YAML has no id for the actions `audit.read`, `audit.not_found`, and `audit.id_refused`.
- Open question for S03: the YAML has no id for `resource.audit_log` or `purpose.audit_review`.
- Open question for S03: the YAML has no id for the items on the `cannot_prove` list (`approval_id`, `log_integrity`, and the rest).
- Open question for S03: the YAML has no id for the rule "an id longer than 128 characters is refused".

## How to repeat

Run the tests:

```text
powershell -Command "$env:Path = 'C:\Users\mange\tools\opa;' + $env:Path; .venv\Scripts\python.exe -m pytest tests/audit policy/tests -q -p no:cacheprovider"
```

Run the Half A case through the route. The script is the three calls in `evidence-chain-one-case.md`, followed by:

```python
admin = {"X-User-Role": "admin", "X-Correlation-Id": "s0514-read-1"}
response = client.get(f"/audit/{cid}", headers=admin)
print(response.status_code, response.json()["row_count"])
for row in response.json()["rows"]:
    print(row["ts"], row["action"], row["role"])
```

Expected output: `200 3`, then three lines with the actions `record.read`, `ai.summary`, `policy.deny`. The `ts` values differ on each run. The `prompt_hash` stays `e17907…ab61d` while the `REC-0001` row stays the same.
