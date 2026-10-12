# Policy evidence

| Field | Value |
|---|---|
| Stage | S04-06 — Policy as code (Challenge 6), Half B |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The allow test, the deny test, and the "EXECUTE needs an approval id" tests all pass. The `opa` binary is not on the PATH, so the Python copy of the policy ran in the normal test run. The Rego files were run through the Docker image `openpolicyagent/opa:latest` (OPA 1.21.1). That run passed too. The binary on a developer machine or CI runner is still Unknown. |
| Evidence sources | `python -m pytest -q` before and after; `opa check --strict`; `opa test` (Docker); the opa-versus-Python agreement test (Docker); `policy/opa/access.rego`; `policy/opa/ai_action.rego`; `policy/opa/policy_data.json`; `apps/api/services/policy.py`; `apps/api/main.py`; `policy/tests/`; `docs/06-policy/ai-action-policy-design.md`; `docs/03-identity/target-access-matrix.md` |
| Assumptions | Three AI gateway flags are placeholders until S04-09: `forbidden_field_in_prompt` is false, `output_schema_ok` is true, `timeout_hit` is false. The three outcome words 202, 403, and 200 for HOLD_FOR_REVIEW, BLOCK, and RECOMMEND_ONLY are PROPOSED. Owner: Team-Force. The route sets `purpose` and `scope` itself, because the live request has neither. |
| Unresolved issues | No approval store exists, so an approval id string is not checked against a stored yes. No execute route exists. A call with no role header on `GET /records/{id}` still uses `operator`. Eight fixtures (data use, operational safety, production readiness) have no evaluator yet. |
| Residual risks | The live prompt still holds the whole device row, including `mgmt_ip` and `credential_profile` (defect F12). The policy cannot see that, because the flag is a placeholder. A summary of any device with a true stale flag is now refused. That is 192 of 354 rows. |

## What this file is

This file records every test run for Half B. The outputs below are real command output. They were not typed by hand.

Commands ran from `06-telecom-service-network-incident-ops/` with the repo `.venv` Python 3.13.5.

## What Half B built

| File | What it does |
|---|---|
| `policy/opa/access.rego` | Allows a call only when one of the 34 rows matches on role, action, resource, purpose, scope, and risk. Refuses a matching row when the action is on the caller's denied list. Refuses an execute row when the approval id is empty. Each rule has a comment with its YAML rule id. |
| `policy/opa/ai_action.rego` | Returns one of RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE. BLOCK rows B1 to B10 win over HOLD rows H1 to H4. Those win over the action rows O1 to O3. |
| `policy/opa/policy_data.json` | One copy of the 34 rows and the value lists. Rego and Python both read it, so the two cannot differ on a row. |
| `apps/api/services/policy.py` | Runs `opa eval` when `opa` is on the PATH. Otherwise it applies the same table in Python. If the opa run fails, the answer is deny or BLOCK. |
| `apps/api/main.py` | `GET /records/{id}` and `POST /ai/summarize/{id}` call the policy. A denied call returns 403 and writes an audit row. |
| `policy/tests/fixtures/` | 23 JSON files, one per example input. Each file holds one object keyed by the fixture name. |
| `policy/tests/test_policy_python.py` | 83 tests. Two of them need `opa` and are skipped without it. |
| `policy/tests/access_test.rego`, `policy/tests/ai_action_test.rego` | 30 Rego tests. |

## Before

The baseline run at the start of Half B, before any policy code. This is the one summary line recorded from that run.

**Verified Fact.** `python -m pytest -q` gave 15 passed.

## Run with the first wiring and the old tests

After `main.py` called the policy and before the tests were updated, 5 of the 15 old tests failed. Each failure was a behaviour that Half B changes on purpose.

```text
FAILED tests/access/test_negative_access.py::test_clinician_role_is_denied_on_record_read
FAILED tests/access/test_negative_access.py::test_automation_service_may_not_execute_without_approval_id
FAILED tests/characterization/test_current_behaviour.py::test_clinician_role_is_denied_on_record_read
FAILED tests/characterization/test_current_behaviour.py::test_ai_summarize_accepts_request_with_no_role_header
FAILED tests/test_api_contract.py::test_ai_summary_has_minimum_contract - ass...
5 failed, 10 passed, 10 warnings in 2.09s
```

| Test | What changed | Why |
|---|---|---|
| Two `clinician` tests | Status 200 became 403. The body `{"error":"forbidden"}` stayed. | The S04-03 evidence said S04-06 is the stage that returns 403. |
| `automation_service` on the record route | Status 200 became 403. | Same reason. |
| `test_ai_summarize_accepts_request_with_no_role_header` | Replaced by `test_ai_summarize_refuses_request_with_no_role_header`. A call with no role now returns 403 and writes one `policy.deny` audit row. | A call with no role has no caller. The access policy denies it. The new test says it replaces the old one. |
| `test_ai_summary_has_minimum_contract` | The request now sends `X-User-Role: operator`. | The route needs a role the policy allows. |

## After: normal run, no `opa` on the PATH

`Get-Command opa` printed nothing. The Python copy of the policy ran.

```text
........................................................................ [ 73%]
........................ss                                               [100%]
96 passed, 2 skipped in 3.10s
```

**Verified Fact.** 96 passed, 2 skipped. The 2 skipped tests are the opa-versus-Python agreement tests. They skip when `opa` is absent.

## The gate tests

Run with the Python copy and no `opa` on the PATH.

```text
policy/tests/test_policy_python.py::test_remediation_becomes_a_change_with_all_checks_allow PASSED [  7%]
policy/tests/test_policy_python.py::test_remediation_does_not_become_a_change_without_approval_id_deny PASSED [ 15%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[None] PASSED [ 23%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[] PASSED [ 30%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[ ] PASSED [ 38%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[\t\n] PASSED [ 46%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[0] PASSED [ 53%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[False] PASSED [ 61%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[approval_id6] PASSED [ 69%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id[approval_id7] PASSED [ 76%]
policy/tests/test_policy_python.py::test_execute_is_unreachable_when_the_approval_id_key_is_missing PASSED [ 84%]
policy/tests/test_policy_python.py::test_execute_is_reached_by_exactly_the_all_checks_inputs PASSED [ 92%]
policy/tests/test_policy_python.py::test_engine_failure_denies PASSED    [100%]

====================== 13 passed, 70 deselected in 1.23s ======================
```

| Gate | Test | Result |
|---|---|---|
| Allow: an AI remediation recommendation becomes a change | `test_remediation_becomes_a_change_with_all_checks_allow` | PASSED. All checks present gives EXECUTE. |
| Deny: the same change without an approval id | `test_remediation_does_not_become_a_change_without_approval_id_deny` | PASSED. Gives BLOCK. |
| EXECUTE is unreachable without `approval_id` | `test_execute_is_unreachable_without_an_approval_id` (8 empty values) and `..._when_the_approval_id_key_is_missing` | PASSED. `None`, empty string, spaces, tab and newline, `0`, `False`, `[]`, `{}`, and a missing key never give EXECUTE. |
| No fixture reaches EXECUTE without an approval id (BLOCKED gate) | `test_execute_is_reached_by_exactly_the_all_checks_inputs` | PASSED. It runs 82,944 inputs. Exactly 2 give EXECUTE. Both have an approval id, an audit row, `approval_required` true, a validated change plan, persona `persona.automation_service`, and every other check clear. The 2 are the two resources, `resource.device` and `resource.circuit`. |

**Verified Fact.** No fixture reaches EXECUTE without `approval_id`. The BLOCKED gate does not fire.

## Rego checks (Docker, OPA 1.21.1)

`opa` is not installed. The Docker image `openpolicyagent/opa:latest` ran the Rego. The image reported OPA version 1.21.1.

`opa check --strict /policy/opa` printed nothing and exited 0.

`opa test /policy/opa /policy/tests` gave:

```text
PASS: 30/30
```

The first `opa test` run failed 1 of 30. Fixture `ai-04-hold-recommendation-for-review` gave an empty reason list in Rego. The Python copy gave the right list, so the normal run did not show it. The opa-versus-Python test below would also have caught it. The reasons rule in `ai_action.rego` was rewritten to pick the group that decided the outcome. The second run passed 30 of 30.

An earlier `opa test` attempt failed on loading with 22 merge errors. All fixture files used the same top-level keys. Each file now holds one object keyed by its fixture name.

## Rego and Python agree

The test `test_opa_and_python_agree_on_every_ai_action_combination` sends 82,959 inputs to `opa eval` in one call. It checks that the Rego result and the Python result are equal on every input. The inputs are the 82,944 combinations plus 15 inputs that each lack one required key. The test `test_opa_and_python_agree_on_access` does the same for the access policy. It uses every row, every row with one field changed, three approval id values per row, the five access fixtures, and five live role ids.

No real `opa` binary exists here, so a temporary wrapper outside the repo (`opa.cmd` in the user's temp folder) forwarded `opa eval` to the Docker image. The wrapper is not part of the repo.

```text
..                                                                       [100%]
2 passed, 81 deselected in 38.98s
```

The same wrapper ran the whole suite:

```text
........................................................................ [ 73%]
..........................                                               [100%]
98 passed in 64.56s (0:01:04)
```

**Verified Fact.** With the Docker-backed `opa`, 98 passed and 0 skipped. Rego and Python agree on every input tested.

## Routes through the opa engine

With `POLICY_ENGINE=opa` and the wrapper on the PATH, a script called the two routes and sent each audit row to a temporary log.

```text
engine opa
GET operator 200
GET clinician 403
GET admin 403
POST none 403
POST operator 200
POST operator stale 403
POST operator blank 202
7 audit rows
```

| Call | Result | Why |
|---|---|---|
| `GET /records/REC-0001`, `operator` | 200 | Row TA-01. |
| Same, `clinician` or `admin` | 403 | No row for the role. The audit row action is `policy.deny`. |
| `POST /ai/summarize/REC-0001`, no header | 403 | No role means no caller. |
| Same, `operator` | 200 | Row TA-06, then RECOMMEND_ONLY. |
| `POST /ai/summarize/DEV-00003`, `operator` | 403 | The stale flag is true. BLOCK row B5. |
| `POST /ai/summarize/DEV-BAD1`, `operator` | 202 | The stale flag is blank. HOLD row H3. |

## Does the test suite catch a broken policy?

I switched off row B8 (the approval id check) in `policy.py`, ran the policy tests, then restored the line.

```text
9 failed, 74 passed in 40.02s
```

The 9 failures included `test_remediation_does_not_become_a_change_without_approval_id_deny`, all four empty-value cases of `test_execute_is_unreachable_without_an_approval_id`, `test_execute_is_reached_by_exactly_the_all_checks_inputs`, and the opa-versus-Python agreement test. After the line was restored, the normal run passed again (96 passed, 2 skipped).

## Findings

| ID | Finding | Label |
|---|---|---|
| HB-01 | The three gateway flags are placeholders. The live prompt holds the whole device row, including `mgmt_ip` and `credential_profile` (defect F12). The policy reports `forbidden_field_in_prompt` as false because no allow list exists to compute it. S04-09 replaces `gateway_flags_until_s0409()` in `policy.py`. | Verified Fact (placeholder), Assumption (value) |
| HB-02 | `POST /ai/summarize/{id}` now refuses a device whose stale flag is true. In `devices.csv` 192 rows are true, 161 false, and 1 blank. The YAML names the stale block for recommendations. Its use for summaries is PROPOSED. Owner: Team-Force. | Verified Fact (counts), Assumption (rule) |
| HB-03 | A missing role header on `GET /records/{id}` still means `operator`. The summarize route has no default and denies. PB-04 proposes removing the record-route default. | Verified Fact |
| HB-04 | No route can reach EXECUTE. The test `test_no_route_can_execute` checks that no route path contains "execute". EXECUTE is tested in the policy only. | Verified Fact |
| HB-05 | An approval id is checked for presence only. No store holds approvals, so a made-up string passes the check. | Verified Fact |
| HB-06 | Rego `trim_space` and Python `str.strip` treat a few control characters differently (`\x1c` to `\x1f`). The tests use space, tab, and newline only. A string made only of those control characters is untested. | Inference |
| HB-07 | Eight fixtures (DU-01 to DU-04, OS-01, OS-02, PR-01, PR-02) have no evaluator. The tests check their shape and nothing else. S05R decides where each evaluator lives. | Verified Fact |
| HB-08 | `policy_version` mismatch (row H4) holds a call for review. The version string `0.1.0-proposed` has no owner-approved format. | Assumption |
| HB-09 | The one-line comment in `test_negative_access.py` says S04-06 replaces `target_decision` with Rego. That function is still in the file. The new policy tests cover the same cases. Removing it is a clean-up for S05R. | Verified Fact |

New terms the YAML lacks are written as `Open question for S03:` lines in the two Rego files. They are the same terms listed in `ai-action-policy-design.md`.

## Open question for S03

- Open question for S03: `action_on_denied_list` has no YAML id. Reasons for a denied-list refusal carry this plain name.
- Open question for S03: should `GET /records/{id}` and `POST /ai/summarize/{id}` send `purpose` and `scope` from the caller? Today the route sets them from the target row.

## Gate check

| Gate | Outcome |
|---|---|
| PASS needs an allow test, a deny test, and a test that EXECUTE is unreachable without `approval_id` | All three pass. |
| CONDITIONAL PASS applies when `opa` is absent and Python ran | Applies. The binary is not on the PATH. |
| BLOCKED applies if any fixture reaches EXECUTE without `approval_id` | Does not apply. |

**Result: CONDITIONAL PASS.** To reach PASS, install the `opa` binary on the developer machine or CI runner and rerun `python -m pytest -q`. The two skipped tests will run. Until then the binary gap is Unknown.
