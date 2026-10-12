# Privilege reduction backlog

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half A |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. Four reductions are listed, each with an owner. The no-header item stays the current default, with a proposed change and owner Team-Force. |
| Evidence sources | `apps/api/main.py`; `legacy/reconcile_legacy.py`; `.env.example`; `infra/terraform/main.tf`; `policy/opa/access.rego`; `semantic-layer/access-semantics.yaml`; `semantic-layer/business-rules.yaml`; `docs/01-discovery/brownfield-risk-register.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/operating-contract.md` |
| Assumptions | Effort in hours is Unknown on every item. The repo states no estimate. PROPOSED items stay PROPOSED until Team-Force accepts them in writing. Operating contract row 10. |
| Unresolved issues | Whether `automation_service` is `app_shared` is Unknown. Whether `role.engineer` stays on the API list is Unknown. The proposed no-header deny has no role id. |
| Residual risks | Half B performs PB-01 only. PB-02, PB-03, and PB-04 stay open after Half B. Until they land, the shared password, the unscoped machine account, and the operator default remain. |

## What this file is

This file lists four cuts to today's access. Each cut has an owner. Least privilege means the caller keeps only the actions on their grant in `target-access-matrix.md`.

Half A writes this list. It does not edit `main.py`.

| id | Change | Owner | Effort | When it can be done |
|---|---|---|---|---|
| PB-01 | Take `clinician` out of the allow list in `apps/api/main.py`. | Team-Force. Half B of this stage does the edit after "Half A accepted". | Unknown. The edit is one name removed from the list on line 13. | S04-03 Half B. |
| PB-02 | Split the shared user `app_shared` into named accounts. The names are the existing persona ids. This item adds no new persona. | Team-Force. The password move is S04-04. | Unknown. | S04-04 moves the password out of the source file. Which persona replaces `app_shared` stays Unknown until that stage. |
| PB-03 | Scope `persona.automation_service` to its grants. Execute only on TA-24 and TA-25, and only with a stored approval id. | Team-Force. | Unknown. | S04-06 writes the rule. S04-09 writes the four gates. No execute route is added here. |
| PB-04 | Stop filling a missing role header with `operator`. The proposed result is a deny. | Team-Force. PROPOSED. | Unknown. | Not in Half B. Half B may not change the header default. |

## PB-01. Remove clinician

| Field | Text |
|---|---|
| Finding | `role.clinician` can read a device row. The telecom persona list does not contain that job. |
| Evidence | Verified Fact. `main.py` line 13. F03. R07. `removed_roles` in `access-semantics.yaml`. `test_clinician_role_is_accepted_on_record_read`. |
| Impact | After the removal, that header takes line 17 and the body is `{"error":"forbidden"}`. The status stays 200. |
| Risk | Until the edit, the caller receives `mgmt_ip` and `credential_profile`. |
| Confidence | High |
| Open questions | Why the word is on the list is Unknown. The removal does not need that answer. |
| Owner | Team-Force |
| Effort | Unknown |

## PB-02. Split app_shared into named accounts

| Field | Text |
|---|---|
| Finding | One user name, `app_shared`, is in the legacy script, the example env file, and Terraform. The password is in the source file. |
| Evidence | Verified Fact. `legacy/reconcile_legacy.py` lines 5 to 6. `.env.example` line 1. `infra/terraform/main.tf` line 4. F05. R06. `rule.shared_admin_not_least_privilege`. Password `<redacted>`. The `reconcile` function counts `devices.csv` and does not use the user or the password. |
| Impact | Each later account would be one existing persona, with that persona's rows in the target matrix. |
| Risk | Anyone with the repo can read the password. The link from this user to `persona.automation_service` is not stated. Treating them as the same account would give the shared password the execute grant. |
| Confidence | High for the three files. Medium for any link to a persona. |
| Open questions | Whether `automation_service` is `app_shared` is Unknown. Stage S04-04. This backlog does not answer it. |
| Owner | Team-Force |
| Effort | Unknown |

The named accounts are the seven persona ids already in the YAML. This item does not create an eighth persona.

## PB-03. Scope automation_service

| Field | Text |
|---|---|
| Finding | `persona.automation_service` is a machine account. Its execute grant is limited to `scope.assigned_incident` on `resource.device` and `resource.circuit`, and it needs a human approval id it does not write. |
| Evidence | Verified Fact. Grants TA-23, TA-24, TA-25. `requires_rule` `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`. Operating contract row 9. AI qualification, remediation execution row. The API allow list does not include the persona. R06. |
| Impact | A later execute call with an empty `provenance.approval_id` is deny. A read of `resource.device` for `purpose.scheduled_automation` stays allow (TA-23). |
| Risk | The gap name `overpowered_automation_account` sits on the shared user and on `policy.opa.admin_any`. No execute route exists, so there is no live push to measure. |
| Confidence | High for the grant text. Medium for the gap name, because the files do not say the persona and `app_shared` are one account. |
| Open questions | Whether this persona is `app_shared` is Unknown. |
| Owner | Team-Force |
| Effort | Unknown |

The persona may not `action.approve`. The approval id is written by `persona.network_engineer` on TA-17.

## PB-04. Remove the default role header

| Field | Text |
|---|---|
| Finding | A call that sends no `X-User-Role` header is treated as `operator`, and the read is allowed. |
| Evidence | Verified Fact. `main.py` line 11 `Header(default="operator")`. F15. R16. `rule.no_default_role`. `status.code.role_header_default.operator`. |
| Impact | The proposed change refuses the call. The server would stop writing `operator` for the caller. |
| Risk | Until that change, a caller who sends no role reads the device row, including `mgmt_ip` and `credential_profile`. |
| Confidence | High |
| Open questions | Open question for S03: there is no id for a call that sends no role header. This design needs that id so a deny rule can name the role field when the header is absent, without first storing `role.operator`. Whether the default is for a local demo is Unknown. |
| Owner | Team-Force. PROPOSED. |
| Effort | Unknown |

This is the CONDITIONAL PASS item. Half B leaves the default in place. The test is NA-06. It asserts the current fill-in.

`rule.no_default_role` names enforcement stage S04-03. The Half B edit list for this stage allows one change: remove `clinician`. The header default stays until a later acceptance widens the edit or S04-06 takes the deny path.

## Also recorded for S04-06

Two neighbouring facts sit here for S04-06. They stay outside the four rows above.

`policy.opa.admin_any` allows any action when the role is `admin`. The target matrix gives `role.admin` no row. `rule.shared_admin_not_least_privilege` says S04-03 and S04-06 replace that rule with the per-persona rows. Owner: Team-Force. Effort: Unknown. Half B does not edit `access.rego`.

`role.engineer` stays on the Python list. The YAML map to `persona.network_engineer` is an Inference. Whether the string `engineer` remains after the persona string is accepted is Unknown. Half B does not remove it. K02 stays in force for that header. The semantic-layer README assigns that question to S04-03. This stage's answer is: keep it for the code half, and leave the permanent name open. Owner: Team-Force.

The summary route still checks no role. F16. That gap is real. It is not one of the four items. S04-06 calls the policy from the AI route. Half B does not add a role check there.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| BL-01 | One of the four items is ready for Half B. The other three stay proposed or scheduled later. | Verified Fact. PB-01 matches `removed_roles` and the Half B scope. PB-04 is PROPOSED because Half B cannot change the default. | After Half B, `clinician` is refused and the other three gaps remain. | The operator default and the shared user still reach data they should not decide. | High | The `app_shared` link and the empty-header role id stay open. |
| BL-02 | Sensitive device fields have one target reader, `persona.network_engineer`, row TA-15. That cut is recorded on TA-15. S04-06 carries it when it writes the policy. | Verified Fact. TA-15. F10. The grant is PROPOSED. Owner: Team-Force. | A later mask would drop `mgmt_ip` and `credential_profile` from every other caller's body. | Until that mask, every allowed header still receives both cells. | High for the exposure. The mask itself is a later stage. | The source YAML still says the reader question is Unknown. This stage copies the single proposed grant. |

## Lifecycle

This file cites `docs/01-discovery/brownfield-risk-register.md` R06, R07, and R16, `docs/02-baseline/defect-list.md` F03, F05, F10, and F15, and `docs/02-baseline/ai-qualification.md` on remediation execution. Stage S04-04 takes PB-02's password move. Stage S04-06 takes PB-03's rule and the admin-any replacement. Stage S06 cites the target matrix these cuts point at.
