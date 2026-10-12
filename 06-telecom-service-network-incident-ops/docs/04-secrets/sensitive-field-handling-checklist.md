# Sensitive-field handling checklist

| Field | Value |
|---|---|
| Stage | S04-04 — Secrets and encryption (Challenge 4), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The checklist covers `mgmt_ip`, `credential_profile`, and the three `customer_id` fields. Who may read the two device fields is Unknown. Owner: Team-Force. The service-order `customer_id` prompt rule is an open question for S03. |
| Evidence sources | `semantic-layer/entities.yaml`; `semantic-layer/ai-context-policy.yaml`; `semantic-layer/access-semantics.yaml`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py`; `apps/api/services/domain_service.py`; `docs/02-baseline/defect-list.md`; `docs/03-identity/current-role-matrix.md` |
| Assumptions | A field marked `sensitive: true` in `entities.yaml` is treated as sensitive whatever the cell holds. A PROPOSED grant is a proposal. It is not an approved viewer list. |
| Unresolved issues | Who may read `mgmt_ip` and `credential_profile` is Unknown. Owner: Team-Force. Whether `field.service_order.customer_id` may enter a prompt is an open question for S03. |
| Residual risks | Today every allowed role receives the two device fields on a record read. The summary prompt receives the whole device row. Stage S04-09 owns the prompt change. Stage S04-08 owns the audit schema. This stage leaves both as they are. |

## What this file is

This file says, for each sensitive or named private field, whether it may be written to a log, placed in a prompt sent to the model, returned in an API response, and who may see it.

Half A writes this checklist. The prompt file and the audit file stay as they are.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## Field `field.device.mgmt_ip`

YAML marks: `sensitive: true`, `never_in_prompt: true`. **Verified Fact.** `semantic-layer/entities.yaml` lines 104 to 114.

Policy ids: `policy.prompt_fields` (forbidden list). `failmode.forbidden_field_in_prompt`.

| Question | Rule | Today |
|---|---|---|
| May it be logged | No. A log line stores `record_id` and `role` or `model`. It leaves this cell out. | The audit lines in `main.py` lines 15 and 23 store `record_id`, `role`, and `model`. **Verified Fact.** `audit.py` line 9. |
| May it enter a prompt | No. `policy.prompt_fields` forbids `field.device.mgmt_ip`. A later builder that finds it stops the call (`failmode.forbidden_field_in_prompt`). | `ai_gateway.py` line 7 places the whole device row in the prompt string. F12. |
| May it appear in an API response | Today yes. The proposed later rule is that only the approved viewer receives it. Who that viewer is stays Unknown. | `GET /records/{record_id}` returns the whole row. F10. `domain_service.py` returns every cell. |
| Who may see it | Unknown today. A PROPOSED grant on `persona.network_engineer` is the only proposed reader (`access-semantics.yaml` `resource.sensitive_device_fields` and the network_engineer read grant). `persona.ai_agent` is written to stay off this field. | Every allowed role on `main.py` line 13 receives the cell: `admin`, `operator`, `engineer`, `ai_agent`. K02. F10. Header `clinician` is denied after S04-03 Half B. |

## Field `field.device.credential_profile`

YAML marks: `sensitive: true`, `never_in_prompt: true`. **Verified Fact.** `semantic-layer/entities.yaml` lines 130 to 140. The cell is a label for a login set. It is still treated as sensitive.

Policy ids: `policy.prompt_fields` (forbidden list). `failmode.forbidden_field_in_prompt`.

| Question | Rule | Today |
|---|---|---|
| May it be logged | No. Same audit fields as `mgmt_ip`. | `main.py` lines 15 and 23. `audit.py` line 9. |
| May it enter a prompt | No. `policy.prompt_fields` forbids `field.device.credential_profile`. `failmode.forbidden_field_in_prompt` stops a later builder that finds it. | `ai_gateway.py` line 7 places the whole device row in the prompt string. F12. |
| May it appear in an API response | Today yes. The proposed later rule is that only the approved viewer receives it. Who that viewer is stays Unknown. | `GET /records/{record_id}` returns the whole row. F10. |
| Who may see it | Unknown today. The same PROPOSED grant on `persona.network_engineer` is the only proposed reader. `persona.ai_agent` is written to stay off this field. | Every allowed role on `main.py` line 13 receives the cell: `admin`, `operator`, `engineer`, `ai_agent`. K02. F10. Header `clinician` is denied after S04-03 Half B. |

## Field `field.circuit.customer_id`

YAML marks: identifier. The field has no `sensitive: true` key. **Verified Fact.** `semantic-layer/entities.yaml` lines 182 to 189.

Policy ids: `policy.prompt_fields` forbids this field. The forbid reason is PROPOSED. Owner: Team-Force.

| Question | Rule | Today |
|---|---|---|
| May it be logged | The live audit lines store `record_id`, `role`, and `model`. They leave this cell out. | No live route reads `circuits.csv`. **Verified Fact.** `domain_service.py` reads `devices.csv` only. |
| May it enter a prompt | No, as a PROPOSED rule. `policy.prompt_fields` lists `field.circuit.customer_id` on the forbidden list. | The live prompt is built from a device row. A circuit `customer_id` is absent from that row. |
| May it appear in an API response | No live route returns a circuit row. | The three live routes read a device row or return health. |
| Who may see it | A PROPOSED grant on `persona.customer_support` reads circuits for one customer (`scope.one_customer`). That grant is a proposal. Inference from `access-semantics.yaml`. | No caller receives a circuit row from the API today. |

## Field `field.incident.customer_id`

YAML marks: identifier. The field has no `sensitive: true` key. **Verified Fact.** `semantic-layer/entities.yaml` lines 360 to 367.

Policy ids: `policy.prompt_fields` forbids this field. The forbid reason is PROPOSED. Owner: Team-Force.

| Question | Rule | Today |
|---|---|---|
| May it be logged | The live audit lines store `record_id`, `role`, and `model`. They leave this cell out. | No live route reads `incidents.csv`. **Verified Fact.** `domain_service.py` reads `devices.csv` only. |
| May it enter a prompt | No, as a PROPOSED rule. `policy.prompt_fields` lists `field.incident.customer_id` on the forbidden list. | The live prompt is built from a device row. An incident `customer_id` is absent from that row. |
| May it appear in an API response | No live route returns an incident row. | The three live routes read a device row or return health. |
| Who may see it | A PROPOSED grant on `persona.customer_support` reads incidents for one customer (`scope.one_customer`). That grant is a proposal. Inference from `access-semantics.yaml`. | No caller receives an incident row from the API today. |

## Field `field.service_order.customer_id`

YAML marks: identifier. The field has no `sensitive: true` key. **Verified Fact.** `semantic-layer/entities.yaml` lines 445 to 452.

Open question for S03: `field.service_order.customer_id` is in `entities.yaml` and is absent from the `policy.prompt_fields` forbidden list. This checklist needs a yes or no on whether that field may enter a prompt.

| Question | Rule | Today |
|---|---|---|
| May it be logged | The live audit lines store `record_id`, `role`, and `model`. They leave this cell out. | No live route reads `service_orders.csv`. **Verified Fact.** `domain_service.py` reads `devices.csv` only. |
| May it enter a prompt | Unknown. The YAML has the field and is silent on the prompt. | The live prompt is built from a device row. A service-order `customer_id` is absent from that row. |
| May it appear in an API response | No live route returns a service-order row. | The three live routes read a device row or return health. |
| Who may see it | A PROPOSED grant on `persona.customer_support` reads service orders for one customer (`scope.one_customer`). That grant is a proposal. Inference from `access-semantics.yaml`. | No caller receives a service-order row from the API today. |

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| SF-01 | The two device fields are marked sensitive and must stay out of a prompt. | Verified Fact. `entities.yaml` lines 108, 109, 134, and 135. `policy.prompt_fields` forbidden list. `failmode.forbidden_field_in_prompt`. Locked in `Project_Intent Section 4.3.md`. | A later prompt builder that finds either field stops the call. | Today `ai_gateway.py` line 7 still places both cells in the prompt. F12. | High | Which fields may enter the prompt is confirmed at S04-09. The allow list is PROPOSED. |
| SF-02 | Every allowed role receives `mgmt_ip` and `credential_profile` on a record read. | Verified Fact. `main.py` lines 13 and 16. F10. K02. `resource.sensitive_device_fields` says who may read them is Unknown. | Those two cells leave the API for `admin`, `operator`, `engineer`, and `ai_agent`. | A caller who can reach the record route sees both cells. Header `clinician` is denied after S04-03 Half B. | High | Who may read the two cells is Unknown. Owner: Team-Force. |
| SF-03 | Circuit and incident `customer_id` stay out of a prompt under a PROPOSED rule. | Verified Fact of the YAML lines. `policy.prompt_fields` forbidden list, reasons marked PROPOSED. Owner: Team-Force. | A later prompt builder that follows the list leaves those two ids out. | The rule is a proposal until Team-Force accepts it. | High for the YAML text. Medium for the rule, because it is PROPOSED. | Team-Force confirmation waits for S04-09. |
| SF-04 | Service-order `customer_id` has no prompt rule in the YAML. | Verified Fact. `entities.yaml` lines 445 to 452. The forbidden list names circuit and incident `customer_id` and is silent on the service-order field. | This checklist cannot mark a yes or no for a prompt. | A later builder that copies only the forbidden list can place the service-order id in a prompt. | High | Open question for S03: whether `field.service_order.customer_id` may enter a prompt. |

## Lifecycle

This file cites `docs/02-baseline/defect-list.md` F10 and F12, `policy.prompt_fields`, and `failmode.forbidden_field_in_prompt`. Stage S04-09 uses this checklist for the prompt allow-list. Stage S04-08 owns the audit schema and leaves it unchanged in this stage. Stage S05R folds the S03 open question into the YAML.
