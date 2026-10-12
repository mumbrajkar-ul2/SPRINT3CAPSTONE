# Current role matrix

| Field | Value |
|---|---|
| Stage | S04-03 — Identity and least privilege (Challenge 3), Half A |
| Date / version | 2026-10-10, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. This file records who can reach the API and the data today. A call with no role header stays the current default `operator`. The proposed change is to refuse that call. Owner: Team-Force. |
| Evidence sources | `apps/api/main.py`; `policy/opa/access.rego`; `semantic-layer/access-semantics.yaml`; `semantic-layer/business-rules.yaml`; `legacy/reconcile_legacy.py`; `.env.example`; `infra/terraform/main.tf`; `docs/domain-specific-spec.md`; `docs/01-discovery/brownfield-risk-register.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/ai-qualification.md`; `Project_Intent Section 4.3.md`; `tests/characterization/test_current_behaviour.py` |
| Assumptions | Likelihood stays Unknown. The repo states no frequency. A header word outside the five-name list takes the same code path. This stage replayed that path only for the headers named in the defect list. |
| Unresolved issues | Why `clinician` is on the list is Unknown. Whether `engineer` stays on the list is Unknown. Whether `automation_service` is the user `app_shared` is Unknown. Whether the missing-header default is for a local demo is Unknown. |
| Residual risks | Until Half B, `clinician` can still read a device row. A call with no role header can still read that row, including `mgmt_ip` and `credential_profile`. The summary route still checks no role. The shared password stays in the legacy file until S04-04. |

## What this file is

This file lists every role and account that can reach the API or the data today, what that caller can do, and the file that proves it. Least privilege means each caller gets only the actions on their grant. This file is the picture before that grant list is applied.

Half A writes this document. The Python files stay as they are.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Routes the process exposes

The live app has three routes. **Verified Fact:** `apps/api/main.py` lines 6, 10, and 19. Defect K08.

| Route | Who it checks | What a successful call returns |
|---|---|---|
| `GET /health` | No role header. Any caller who can reach the process. | `status` `ok` and the repo name. No audit line. K01. |
| `GET /records/{record_id}` | Header `X-User-Role`. If the header is absent, the value is `operator`. | The device row when the header is one of five words. Otherwise the body `{"error":"forbidden"}`. |
| `POST /ai/summarize/{record_id}` | No role header. The function takes `record_id` only. | A summary object. The audit line stores `record_id` and `model`. F16. |

Worked example. `GET /records/REC-0001` with header `clinician` returns the row whose `device_id` is `REC-0001`, with HTTP 200. The same URL with header `vendor` returns HTTP 200 and the body `{"error":"forbidden"}`, and writes no audit line. Both results are current behaviour. Replay sections 2.5 and 2.6. Defects F03 and F14.

## API roles on the record route

The allow list is `admin`, `operator`, `clinician`, `engineer`, `ai_agent`. **Verified Fact:** `main.py` line 13. The same five words are `role.admin`, `role.operator`, `role.clinician`, `role.engineer`, and `role.ai_agent` in `access-semantics.yaml` `api_roles_today`. Project Intent section 4.3 locks the same list.

A word on that list loads a device row and writes an audit line `record.read` with `record_id` and `role`. **Verified Fact:** `main.py` lines 14 to 16. The row includes `mgmt_ip` and `credential_profile`. Defect F10. Risk R14.

| Role id | Header word | What it can do on the live API | What the OPA file would do | Proof |
|---|---|---|---|---|
| `role.admin` | `admin` | Read a device row on `GET /records/{id}`. | Allow every action. `policy.opa.admin_any`. | `main.py` line 13. `access.rego` lines 6 to 8. K02 for this header. `maps_to_persona` is null. |
| `role.operator` | `operator` | Read a device row. This is also the value used when the header is absent. | Allow only when the action is `read`. `policy.opa.operator_read`. | `main.py` lines 11 and 13. `access.rego` lines 9 to 11. K02. F15. `status.code.role_header_default.operator`. |
| `role.clinician` | `clinician` | Read a device row, including `mgmt_ip` and `credential_profile`. | Refuse. The OPA file has no clinician rule. `policy.opa.default_deny`. | `main.py` line 13. `test_clinician_role_is_accepted_on_record_read`. F03. R07. `removed_roles`. |
| `role.engineer` | `engineer` | Read a device row. | Refuse. No engineer rule. | `main.py` line 13. K02. `maps_to_persona` `persona.network_engineer`, label Inference. |
| `role.ai_agent` | `ai_agent` | Read a device row. The summary route does not look at this header. | Refuse. No `ai_agent` rule. | `main.py` lines 13 and 19 to 24. K02. `maps_to_persona` `persona.ai_agent`, label Verified Fact. |

The record route checks that Python list. The OPA file sits in `policy/opa/access.rego`. No Python file imports it. **Verified Fact:** R19. `docs/01-discovery/current-state-architecture.md` records the same split. The HTTP call follows the five-name list. Admin-any and operator-read stay in the OPA file.

`default allow = false` is line 3 of `access.rego`. That line refuses every input the two allow rules miss. The API does not consult that result.

## Personas

The domain list is `noc_operator`, `network_engineer`, `field_engineer`, `customer_support`, `automation_service`, `vendor_account`, `ai_agent`. **Verified Fact:** `docs/domain-specific-spec.md` lines 20 to 26. The YAML ids are `persona.noc_operator`, `persona.network_engineer`, `persona.field_engineer`, `persona.customer_support`, `persona.automation_service`, `persona.vendor_account`, `persona.ai_agent`.

Only `ai_agent` is both a header word and a persona name. **Verified Fact:** R20. `role.ai_agent` `mapping_label` Verified Fact.

| Persona id | Header if someone sends the persona name | Live result on `GET /records/{id}` | API role the YAML records | Label |
|---|---|---|---|---|
| `persona.noc_operator` | `noc_operator` | HTTP 200, body `{"error":"forbidden"}`, no audit line. | `role.operator` | The forbidden result is Verified Fact for this header: F14. The map to `role.operator` is Inference. |
| `persona.network_engineer` | `network_engineer` | The word is outside the five-name list, so the path is `main.py` line 17. This header was not in the cited replay. | `role.engineer` | Code path Verified Fact. This header's HTTP call was not replayed. Map is Inference. |
| `persona.field_engineer` | `field_engineer` | Same line 17 path. This header was not replayed. | null | `api_role_today: null`. Verified Fact in the YAML. |
| `persona.customer_support` | `customer_support` | Same line 17 path. This header was not replayed. | null | Verified Fact in the YAML. |
| `persona.automation_service` | `automation_service` | Same line 17 path. This header was not replayed. The allow list does not include it. R06. | null | Verified Fact in the YAML. |
| `persona.vendor_account` | `vendor_account` | Same line 17 path. This exact header was not replayed. | null | Verified Fact in the YAML. |
| `persona.ai_agent` | `ai_agent` | Read is allowed. K02. | `role.ai_agent` | Verified Fact. |

The replay sent `X-User-Role: vendor`, and the body was `{"error":"forbidden"}` with HTTP 200 and no audit line. **Verified Fact:** replay section 2.6. F14. `persona.vendor_account` `note_today`. The header word was `vendor`. The persona name is `vendor_account`. Those are two strings.

## Accounts and tokens that are not API roles

| Account | Where it is stored | What it can do today | Proof |
|---|---|---|---|
| `app_shared` | User name in `legacy/reconcile_legacy.py` line 5. User name in `.env.example` line 1. Terraform content `shared_user=app_shared` in `infra/terraform/main.tf` line 4. | The legacy script counts rows in `devices.csv` and prints that count. The user name and the password are assigned on lines 5 to 6. The `reconcile` function does not use them. No database connect call is in that file. The API allow list does not contain `app_shared`. | Verified Fact: the three files above. F05. R02. R06. K04. Password value is `<redacted>`. |
| `OT_VENDOR_TOKEN` | Name only, `.env.example` line 4. Value `<redacted>`. Also listed under `forbidden_credential_names` in `semantic-layer/ai-context-policy.yaml`. | A search of this repo finds the name in `.env.example`, in that YAML list, and in the generated JSON copy. No Python file reads the name. The token does not select `persona.vendor_account`. | Verified Fact: this stage's search. The token value is not copied here. |

`generated-env.txt` is the file Terraform declares. It is not in the repo tree. Whether that declaration was ever applied is Unknown. **Verified Fact** of the absence in the tree: `docs/01-discovery/data-and-integration-map.md`.

## What no caller can do today

No route pushes a device config, provisions a circuit, or writes an approval id. **Verified Fact:** `main.py` has the three routes above. AI qualification, remediation execution row. Operating contract row 9. `action.execute` and `action.approve` have no route.

The summary function returns the sentence `Review and approve before action` and `guardrail_status` `not_enforced`. **Verified Fact:** K07. F12. That sentence is text. The route does not change a device.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| CR-01 | Five header words can read a device row. One of them is `clinician`, which is outside the seven personas. | Verified Fact. `main.py` line 13. F03. R07. `test_clinician_role_is_accepted_on_record_read` expects HTTP 200 and `device_id` `REC-0001`. `removed_roles` names `role.clinician`. | A caller with that header receives the row, including `mgmt_ip` and `credential_profile`. | Those cells are readable under a job word the telecom persona list does not name. | High | Why `clinician` is on the list is Unknown. |
| CR-02 | A missing role header is stored as `operator`, and the read is allowed. | Verified Fact. `main.py` line 11. F15. R16. `rule.no_default_role` `current_behaviour`. `status.code.role_header_default.operator`. | A caller who sends no role can read the device row. | The same row includes the two sensitive cells. F10. | High | Whether the default is for a local demo or for a deployed caller is Unknown. |
| CR-03 | The summary route accepts a call that sends no role. | Verified Fact. `main.py` lines 19 to 24. F16. R11. `test_ai_summarize_accepts_request_with_no_role_header`. | Any caller who can reach the route gets a summary of a device row. | The prompt text contains the whole row, including the two sensitive cells. F12. | High | Whether the missing check is intended for this stub is Unknown. |
| CR-04 | A header outside the five names gets HTTP 200, the body `{"error":"forbidden"}`, and no audit line. | Verified Fact. `main.py` line 17. F14. R13. Observed for `vendor` and `noc_operator`. | A client that checks the status code sees success. The log has no denied-access line. | Denied access is invisible in the log. `rule.denied_access_is_audited` is unenforced. Stage S04-08. | High | Which HTTP status a real client already expects is Unknown. |
| CR-05 | The OPA file and the Python list allow different callers. The API follows the Python list. | Verified Fact. `access.rego` lines 3 to 11. `main.py` line 13. R19. `policy.opa.admin_any`, `policy.opa.operator_read`, `policy.opa.default_deny`. | `engineer`, `clinician`, and `ai_agent` can read a row on the HTTP call. The OPA file would refuse those three. | A reviewer who reads only the OPA file will miss the live allow. | High | The file a reviewer reads for a live allow is `main.py` for today. S04-06 is the stage that makes the API call the policy. |
| CR-06 | The shared user name `app_shared` appears in the legacy script, the example env file, and Terraform. The password sits in source. | Verified Fact. `reconcile_legacy.py` lines 5 to 6. `.env.example` line 1. `main.tf` line 4. F05. R06. `rule.shared_admin_not_least_privilege`. Password `<redacted>`. | Anyone with the repo can read the password. The script's printed result is still the device-row count. | The password and the persona `automation_service` may be one account or two. The files do not say. | High for the three files. Medium for any link to the persona. | Whether `automation_service` is `app_shared` is Unknown. Stage S04-04. |
| CR-07 | The vendor token name is in the example env file. No Python file reads it. It does not log anyone in. | Verified Fact. `.env.example` line 4. `ai-context-policy.yaml` `forbidden_credential_names`. This stage's search. Value `<redacted>`. | The token is a shared secret in an example file. It grants no API role. | A later reader can treat the token as the vendor login. The live vendor check is the header word, and `vendor` is refused. | High | Which supplier login the token was meant to be is Unknown. |

## Lifecycle

This file cites `docs/01-discovery/brownfield-risk-register.md` rows R02, R06, R07, R11, R13, R14, R16, R19, and R20, and `docs/02-baseline/defect-list.md` rows K01, K02, K04, F03, F05, F10, F12, F14, F15, and F16. Stage S04-06 reads the target matrix and the policy input model when it extends `access.rego`. This file stays the picture of today's callers. Stage S06 cites the target matrix.
