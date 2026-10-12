# Audit-read access design

| Field | Value |
|---|---|
| Stage | S05-14 — Auditability and compliance evidence (Challenge 14), Half A |
| Date / version | 2026-10-12, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. One new matrix row is proposed: row TA-35 lets `role.admin` read `resource.audit_log` for `purpose.audit_review`. Every other caller stays denied. The row is PROPOSED. Owner: Team-Force. Who may read the audit log is a business decision for Team-Force. |
| Evidence sources | `semantic-layer/access-semantics.yaml` (`resource.audit_log`, `purpose.audit_review`, `scope.all_records`, `risk.read_only`, `api_roles_today`, `personas`); `policy/opa/policy_data.json`; `policy/opa/access.rego`; `apps/api/services/policy.py` (`HEADER_ROLE_IDS`); `apps/api/main.py`; `docs/03-identity/target-access-matrix.md`; `docs/03-identity/policy-input-model.md`; `docs/13-security-validation/remediation-backlog.md` (`SB-03`, `SB-09`); `semantic-layer/business-rules.yaml` (`rule.shared_admin_not_least_privilege`); `policy/tests/test_policy_python.py` |
| Assumptions | A new row follows the existing match rule: an exact match on role, action, resource, purpose, scope, and risk. The route sets purpose and scope itself, as the other two routes do. The Rego file needs no change, because it reads the grants from `policy_data.json`. |
| Unresolved issues | No persona names an audit reviewer. The row uses the API role `role.admin` as a stand-in. Whether the packet will have authentication is Unknown (`SB-09`). |
| Residual risks | The role is a word the caller types. Until authentication exists, any caller who sends `admin` can read any case by id. |

## What this file is

This file proposes who may read the audit log. Half B needs this row so `GET /audit/{correlation_id}` can call the policy before it looks anything up.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Where things stand today

| Fact | Evidence | Label |
|---|---|---|
| The YAML defines `resource.audit_log`. Its description is "The file `logs/audit.log` and its rows." | `access-semantics.yaml` | Verified Fact |
| The YAML defines `purpose.audit_review`. It is `proposed: true` and its owner is Team-Force. | `access-semantics.yaml` | Verified Fact |
| None of the seven personas has a grant on `resource.audit_log`. | `access-semantics.yaml` `personas` | Verified Fact |
| The access matrix has no row for `resource.audit_log`. It has 34 rows, TA-01 to TA-34. | `target-access-matrix.md` | Verified Fact |
| `policy_data.json` has no grant for `resource.audit_log` and no `purpose.audit_review`. | A text search of the file on 2026-10-12 | Verified Fact |
| The app has three routes. None reads the audit log. | `main.py` | Verified Fact |
| `role.admin` has no persona and no row. The old rule that allowed any admin is gone. | `policy_data.json` `persona_of`; `access.rego` | Verified Fact |

So no role may read the audit log today. The policy would answer deny for any caller who asked.

## The proposed row

| Row | Role | Action | Resource | Purpose | Scope | Risk | Decision |
|---|---|---|---|---|---|---|---|
| TA-35 | `role.admin` | `action.read` | `resource.audit_log` | `purpose.audit_review` | `scope.all_records` | `risk.read_only` | allow |

Every id above exists in `access-semantics.yaml`. This design adds no id.

The policy input for an allowed call is:

```json
{
  "role": "role.admin",
  "action": "action.read",
  "resource": "resource.audit_log",
  "purpose": "purpose.audit_review",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

Expected answer: allow, matrix row `TA-35`.

The same call from `role.operator` has no matching row. Expected answer: deny, reason `policy.opa.default_deny`.

```json
{
  "role": "role.operator",
  "action": "action.read",
  "resource": "resource.audit_log",
  "purpose": "purpose.audit_review",
  "scope": "scope.all_records",
  "risk": "risk.read_only"
}
```

The header word `admin` already maps to `role.admin` in `policy.py` `HEADER_ROLE_IDS`. **Verified Fact.**

## Why `role.admin`

| Caller | What it can do in the matrix today | For or against | Verdict |
|---|---|---|---|
| `role.admin` | Nothing. It has no row. | For: it has no duty that the log records. A reader of the log is not also an actor in it. Against: it is a shared role, not a person. `rule.shared_admin_not_least_privilege` says an admin allowed every action breaks least privilege. One read row on one resource does not give admin every action. | **Proposed.** |
| `persona.noc_operator` | Reads alarms, devices, incidents, circuits. Summarizes. Recommends. Approves AI text (TA-09). Writes incidents (TA-10). | Against: the operator would read the log of the operator's own actions. | Not proposed. |
| `persona.network_engineer` | Approves a live network change (TA-17). The only reader of `mgmt_ip` (TA-15). | Against: the approver would read the record of the approver's own approvals. The persona already holds the one sensitive-field grant. | Not proposed. |
| `persona.ai_agent` | Reads allowed fields and writes text. | Against: the model must not read the log that records the model. | Rejected. |
| No role | Deny for everyone. | For: the safest choice while the role is a typed word (`SB-09`). Against: the route returns only 403, and no reviewer can use it. | The fallback if Team-Force declines TA-35. |

**Inference:** the arguments about the operator and the engineer rest on the rows TA-09, TA-10, and TA-17, and on the idea that a reviewer should not review their own work. The argument about the AI agent rests on the same idea. The YAML does not state that idea as a rule.

## Conditions on the row

| Condition | Why |
|---|---|
| The row stays PROPOSED until Team-Force accepts it in writing. | Operating contract row 10. Every grant in the matrix is PROPOSED. |
| The route calls the policy first, then looks up the id. | A caller with no permission gets 403 for an id that exists and for one that does not. A 404 before the policy check would show which ids exist. |
| The route writes its own audit row for every call, including 403 and 404. | Reading the audit log is itself an event the log must hold. |
| The route returns rows for one id only. | The grant says `scope.all_records`, but the route does not return the whole file. |
| The route is read only. | The route never changes the log. |
| The route's own row names `resource.audit_log`. | `main.py` `_audit` today always writes `resource.device`. Half B passes the resource in. |

## Risks

| Id | Risk | Evidence | Level |
|---|---|---|---|
| AR-R1 | Any caller can type `admin`. The row is only as strong as the header. | **Verified Fact.** `main.py` reads `X-User-Role` and nothing else. `SB-09`. | High if more than the team can reach the app. |
| AR-R2 | The rows hold text the caller typed: the role word and the correlation id. A caller can plant a secret-looking string or a very long string. The route would return it. | **Verified Fact.** `SB-03`: a 5000-character id and a role of `mgmt_ip=… password=…` were stored whole. | Medium. The route must refuse an id over a set length. Half B sets the limit. |
| AR-R3 | A reader who knows an id can read that case. Ids are UUIDs or caller-chosen strings. | **Verified Fact.** `audit.correlation_id_from_header`. | Low to medium. |
| AR-R4 | The Python and the Rego copy must agree on the new row. | **Verified Fact.** `test_opa_and_python_agree_on_access` covers every row. | Low. The same test covers TA-35 after Half B. |

## Proposed limit on the id in the path

The Half B test for a long id needs a number. This design proposes **128 characters**. PROPOSED. Owner: Team-Force. Accept or change it when you accept Half A.

| Id | Length | Result under the proposal |
|---|---|---|
| A UUID, for example `a06fc772-953f-4730-85df-b90b0d57ba59` | 36 | Accepted |
| A chosen id, for example `s0514-case-0001` | 15 | Accepted |
| An id from the event file, for example `corr-00273` | 10 | Accepted |
| An id of 5000 characters (the probe in `SB-03`) | 5000 | Refused after the policy check. The route does not store the id or echo it. |

Why 128. Every id this stage saw (the UUIDs in `logs/audit.log`, `corr-00273`, `demo-123`) is 36 characters or fewer. 128 leaves room for a caller-chosen id and stops a very long string. **Assumption:** no real caller needs a longer id. The number comes from this design and not from the repo.

The limit applies to the id in the path of `GET /audit/{correlation_id}`. It does not change what `write_event` stores. `SB-03` stays open for the header written on every other route.

The order of checks stays: policy first, then the length check, then the lookup. A caller with no permission gets 403 for a long id as well, so the length check does not show a caller with no permission anything.

## What Half B changes

This list is for planning. Half A changes nothing.

| File | Change |
|---|---|
| `policy/opa/policy_data.json` | Add one grant, `TA-35`. |
| `policy/opa/access.rego` | No change expected. The rules read the grants from the data file. |
| `apps/api/services/policy.py` | Add one helper that sends the six fields above. The matching code does not change. |
| `policy/tests/fixtures/` | Add one access fixture for the allow, and one for the operator deny. |
| `policy/tests/test_policy_python.py` | Update two counts. `test_every_matrix_row_is_allowed_with_its_own_fields` asserts 34 rows. `test_fixture_counts` asserts 23 fixtures and 5 access fixtures. **Verified Fact:** lines 91 to 94 and line 122. |
| `policy/tests/access_test.rego` | Add a case for the allow and the deny, if the file lists rows. |

Half B changes nothing else in policy. `test_admin_has_no_blanket_access` keeps passing: it asks `role.admin` for `resource.device`, and TA-35 is on `resource.audit_log`. **Inference:** the test reads the base fixture `ac-01-allow-noc-operator-reads-device` and changes only the role and the action.

## Open questions for S03

Open question for S03: no persona names the person who reviews the audit log. This design needs one, for example an audit reviewer, so the row can name a persona and not the API role `role.admin`.

Open question for S03: no scope names one case. `scope.all_records` is the closest id. This design needs a scope for one correlation chain if the grant should be narrower than every record.

Open question for S03: the audit action word for the route's own row has no status id. This design needs one for a read of the audit log, next to `status.code.audit_action.record_read` and `status.code.audit_action.ai_summary`.

Open question for S03: no rule id gives the allowed form of a correlation id (length and characters). This design needs one number so the route can refuse a very long id.

## Findings

### AR-01

| | |
|---|---|
| Finding | No role may read the audit log today. The matrix and `policy_data.json` have no row for it. |
| Evidence | **Verified Fact.** "Where things stand today". |
| Impact | Half B's route would deny every caller until a row is added. |
| Risk | Low. The default is deny. |
| Confidence | High |
| Open questions | None. |

### AR-02

| | |
|---|---|
| Finding | One row is proposed: TA-35, `role.admin` reads `resource.audit_log` for `purpose.audit_review`. |
| Evidence | **Verified Fact** for the ids. **Inference** for the choice of role. |
| Impact | Half B can build the route and the tests. |
| Risk | High while the role is a typed word (`AR-R1`). |
| Confidence | Medium. The choice of role is a Team-Force decision. |
| Open questions | The persona question above. |

### AR-03

| | |
|---|---|
| Finding | The route must check the policy before it looks up the id. |
| Evidence | The playbook gate: BLOCKED when the route answers 404 before it checks policy. |
| Impact | A 403 for an id that exists looks the same as a 403 for one that does not. |
| Risk | Medium if the order is wrong. |
| Confidence | High |
| Open questions | None. |

## Lifecycle

Half B adds TA-35 to the policy copies, builds `GET /audit/{correlation_id}`, and tests the three outcomes: 200 for `admin`, 403 for a caller with no row, and 404 for an unknown id after the policy allows. Stage S07 may replace the stand-in role with an audit reviewer persona.
