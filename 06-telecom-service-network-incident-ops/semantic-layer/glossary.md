# Glossary

| Field | Value |
|---|---|
| Stage | S03 — Semantic layer (Execution Plan Phase 3; product path step 1, D3) |
| Date / version | 2026-10-13, semantic layer `1.2.1`. Written in S03 on 2026-10-10 and revised in S05R. One sentence changed in ADR 0002. Eight rows added in S07 (ADR 0005). One formula word changed in ADR 0006 (`policy_result` to `outcome`). |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. Every id with a glossary prefix has one row below. `tests/test_semantic_layer.py` checks that the Term and Id columns match the YAML. |
| Evidence sources | The seven YAML files in this folder; `docs/domain-specific-spec.md`; `docs/01-discovery/`; `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/ai-qualification.md`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `policy/opa/access.rego`; `data/synthetic/` |
| Assumptions | A word's meaning is what the column name and the docs say. Where the repo gives no definition, the row says so. The persona grants and the purposes are PROPOSED. |
| Unresolved issues | The repo defines none of the 44 status words. The allowed severity list, the retry maximum, the sla_breach_risk range, the alarm-to-incident join, and the storm size are Unknown. |
| Residual risks | A reader can treat a PROPOSED row as approved. The YAML marks each one `proposed: true` with an owner. |

## How to read this file

Each row has a term, its id, and its meaning in everyday words. The term is the exact `name` or `word` in the YAML. The id is the exact `id` in the YAML. The test fails when either differs.

Claim labels. Status-word meanings are **Inference**, because the repo defines none of them. Other meanings are a **Verified Fact** from the named files unless the row says otherwise. "PROPOSED" means the YAML item has `proposed: true` and an owner.

## Entities

Seven things the system stores. Six are CSV tables. One is the event log.

| Term | Id | Meaning |
|---|---|---|
| `device` | `entity.device` | A piece of network equipment, such as a router. One row per device in `devices.csv`. The only table the API reads. |
| `circuit` | `entity.circuit` | A connection sold to a customer between two ends of the network. One row per circuit in `circuits.csv`. |
| `alarm` | `entity.alarm` | A warning raised by a device. One row per alarm in `alarms.csv`. |
| `incident` | `entity.incident` | A service problem that someone must handle. One row per incident in `incidents.csv`. |
| `service_order` | `entity.service_order` | A customer request to set up or change a service. One row per order in `service_orders.csv`. |
| `ai_invocation` | `entity.ai_invocation` | A stored record of one call to a model. One row per call in `ai_invocations.csv`. The live gateway does not write this file. |
| `event` | `entity.event` | One line in `events.jsonl`. It names a table, a flow, an actor, a log level, a latency, and a cost. 3000 lines. |

## Concepts

Terms the docs use that have no table of their own.

| Term | Id | Meaning |
|---|---|---|
| `topology` | `concept.topology` | The stored picture of which devices and circuits exist and how they connect. The repo has no topology file. The picture is the device rows plus `stale_topology_flag` and `topology_snapshot_id`. |
| `SLA` | `concept.sla` | A service level agreement. The promise made to a customer about how well a circuit works. The repo stores `sla_tier` and `sla_breach_risk`. It stores no threshold. |
| `remediation` | `concept.remediation` | A change made to a live device or circuit to fix a fault. No route makes such a change today. It is the action that needs a human approval id first. |
| `guardrail` | `concept.guardrail` | A check that runs around a model call and can stop the result. Since stage S04-09 the live gateway checks the prompt before the model and the answer after it, and returns `guardrail_status` `enforced`. |
| `customer` | `concept.customer` | The organisation that buys a circuit or places an order. There is no customer table. `customer_id` sits on circuits, incidents, and orders. |
| `site` | `concept.site` | A physical place where devices sit. There is no site table. `site_id` sits on devices only. |
| `alarm storm` | `concept.storm` | A burst of many alarms in a short time. Alarms that share `storm_batch_id` are one storm batch. How many alarms make a storm is Unknown. |
| `approval` | `concept.approval` | A named person's recorded yes or no to a recommended change. The system stores an approval id. No route writes that id today. |
| `audit row` | `concept.audit_row` | One JSON line in `logs/audit.log`. Since stage S07 it holds 17 keys in this order: ts, correlation_id, actor, role, action, resource, policy_decision, approval_id, model, model_version, prompt_hash, tokens, latency_ms, outcome, token_estimate_method, record_id, final_action. Each key has an id that starts with `field.audit_row`. |
| `prompt` | `concept.prompt` | The text sent to a model. Since stage S04-09 it is a fixed instruction plus one line for each allowed field the record holds. `mgmt_ip` and `credential_profile` stay out. |
| `policy decision` | `concept.policy_decision` | The allow or deny answer from the access policy. Since stage S04-06 `apps/api/services/policy.py` runs `access.rego`, or its Python copy, on every route. |
| `waiver` | `concept.waiver` | A dated exception to one rule id, granted by a named owner. No register, route, or audit action for it exists yet. PROPOSED. |
| `decision provenance` | `concept.decision_provenance` | The record of how one decision was made, in nine groups: actor, request, data used, model, policy, approval, final action, trace, and what cannot be proven. PROPOSED. |
| `Customer order to provisioning` | `concept.flow_customer_order_to_provisioning` | The business flow from a customer order to a working circuit. No route runs any step of it. 741 events carry this name. |
| `Alarm storm to incident correlation` | `concept.flow_alarm_storm_to_incident_correlation` | The business flow from a burst of alarms to one incident. No route runs any step of it. 706 events carry this name. |
| `Topology lookup to AI recommendation` | `concept.flow_topology_lookup_to_ai_recommendation` | The business flow from a device lookup to a model's advice. Two routes cover the lookup and a local summary. 782 events carry this name. |
| `Approved remediation to validation` | `concept.flow_approved_remediation_to_validation` | The business flow from an approved fix to a check that it worked. No route runs any step of it. 771 events carry this name. |

## Status words

Every distinct word found in a status-like column of the CSV files or in `events.jsonl`. The repo defines none of them. Each row says where the word sits.

### Severity words

Seven words. They fill `alarms.severity`, `incidents.severity`, `circuits.service_class`, and `circuits.sla_tier`. The repo sets no rank order.

| Term | Id | Meaning |
|---|---|---|
| `critical` | `status.word.critical` | A severity word. Also an event log level. The two scales share this one word. Where it ranks is Unknown. |
| `high` | `status.word.high` | A severity word. Where it ranks is Unknown. |
| `medium` | `status.word.medium` | A severity word. Where it ranks is Unknown. |
| `low` | `status.word.low` | A severity word. Where it ranks is Unknown. |
| `gold` | `status.word.gold` | A service-class word. In this data it also fills incident severity on 41 rows and alarm severity on 48 rows. That use is a collision. |
| `silver` | `status.word.silver` | A service-class word. In this data it also fills incident severity on 65 rows and alarm severity on 57 rows. |
| `bronze` | `status.word.bronze` | A service-class word. In this data it also fills incident severity on 50 rows and alarm severity on 52 rows. That use is a collision. |

### Workflow words

Eight words. They fill `circuits.status`, `incidents.status`, and the three order status columns. The repo does not define the step order.

| Term | Id | Meaning |
|---|---|---|
| `new` | `status.word.new` | The row was created. Nothing has happened to it yet. |
| `queued` | `status.word.queued` | The row is waiting for the next step. |
| `in_progress` | `status.word.in_progress` | Someone or something is working on the row. |
| `approved` | `status.word.approved` | A step was accepted. The same word also fills 16 other columns, such as `hostname` and `firmware`, where it has no clear meaning. |
| `manual_hold` | `status.word.manual_hold` | A person stopped the row from moving. Who may do that is Unknown. |
| `exception` | `status.word.exception` | The row hit a case the normal path does not handle. The case is not defined. |
| `failed` | `status.word.failed` | The step did not finish. What happens next is Unknown. |
| `closed` | `status.word.closed` | Work on the row ended. Closing an incident while the fault remains is the harm named in `Project_Intent.md` 3.1. |

### Generic status words

Fourteen words. The same pool fills 16 columns across the six files, including `hostname`, `vendor`, `firmware`, `root_cause`, `model`, and `guardrail_status`.

| Term | Id | Meaning |
|---|---|---|
| `ai_assisted` | `status.word.ai_assisted` | A model took part. Also fills columns such as `hostname` where it has no clear meaning. |
| `degraded` | `status.word.degraded` | Something works but not fully. Fills 16 columns. |
| `high_risk` | `status.word.high_risk` | The row is marked risky. Fills 16 columns, including `recommendation_risk`. The risk scale is Unknown. |
| `internal` | `status.word.internal` | Fills 16 columns, including `use_case` and `root_cause`. The repo gives no meaning. |
| `legacy` | `status.word.legacy` | An older generation. Fills 16 word columns and also `mgmt_ip`, `a_end`, and `z_end`. The first device row has `hostname` `legacy`. |
| `manual` | `status.word.manual` | A person did the step. Fills 16 columns, including `root_cause`. |
| `normal` | `status.word.normal` | Nothing unusual. Fills 16 columns. |
| `not_enforced` | `status.word.not_enforced` | A control exists in name and is not applied. Before stage S04-09 the live summary returned `guardrail_status` `not_enforced` on every call. Now the live summary returns `enforced`, and `not_enforced` is a failure value. Also fills 15 other columns. |
| `pending` | `status.word.pending` | Waiting. Fills 16 columns. |
| `rejected` | `status.word.rejected` | A step was turned down. Fills 16 columns. |
| `requires_review` | `status.word.requires_review` | A person must look at the row. The first device row has `vendor` `requires_review`. Fills 16 columns. |
| `standard` | `status.word.standard` | The usual kind. Fills 16 columns. |
| `vendor` | `status.word.vendor` | Points at a supplier. Fills 16 columns, including the `vendor` column itself. No supplier is named anywhere in the repo. |

### Boolean words

| Term | Id | Meaning |
|---|---|---|
| `true` | `status.word.true` | Yes. Stored as text in `stale_topology_flag`, `orphan_flag`, and `automation_used`. |
| `false` | `status.word.false` | No. Stored as text in the same three columns. |

### Endpoint words

Five words. They fill `mgmt_ip` on devices and `a_end` and `z_end` on circuits. `mgmt_ip` holds these words, not addresses.

| Term | Id | Meaning |
|---|---|---|
| `alpha` | `status.word.alpha` | An endpoint word. What place or address it stands for is Unknown. |
| `beta` | `status.word.beta` | An endpoint word. What it stands for is Unknown. |
| `gamma` | `status.word.gamma` | An endpoint word. The first device row has `mgmt_ip` `gamma`. |
| `modernized` | `status.word.modernized` | An endpoint word. What it stands for is Unknown. |

`legacy` is also an endpoint word. Its row is in the generic list above.

### Network zone words

A network zone is a named part of the network that a device belongs to. The repo does not say whether zones follow place or function.

| Term | Id | Meaning |
|---|---|---|
| `north-1` | `status.word.north_1` | A network zone name on devices. The zone is not described. |
| `south-2` | `status.word.south_2` | A network zone name on devices. |
| `west-3` | `status.word.west_3` | A network zone name on devices. |
| `east-4` | `status.word.east_4` | A network zone name on devices. The largest zone, 70 rows. |
| `central-5` | `status.word.central_5` | A network zone name on devices. |
| `remote-6` | `status.word.remote_6` | A network zone name on devices. |

### Event log levels

Five words in `events.jsonl` `severity`. `critical` is listed under severity words above.

| Term | Id | Meaning |
|---|---|---|
| `debug` | `status.word.debug` | The lowest log level. |
| `info` | `status.word.info` | A normal note. |
| `warn` | `status.word.warn` | Something to watch. |
| `error` | `status.word.error` | Something failed. |

## Collisions

Places where one word or one key means two different things.

| Term | Id | Meaning |
|---|---|---|
| `gold and bronze used as incident severity` | `collision.gold_bronze_as_severity` | Service-class words fill the severity column next to `critical` and `high`. A count by severity mixes the two sets. Defect F09. |
| `status words inside hostname and vendor` | `collision.status_words_in_hostname_and_vendor` | The first device row has `hostname` `legacy` and `vendor` `requires_review`. The same 14-word pool fills 16 columns. Defects F17 and F22. |
| `REC-0001 is the first key in six tables` | `collision.rec_0001_first_key_in_six_tables` | Six different objects share one key text. A join on it joins six objects. The API returns the device. Defect F21. |
| `clinician is an API role in a telecom system` | `collision.clinician_role_in_telecom_api` | A health-care job word is on the API allow list. No telecom persona is called that. Defect F03. |
| `token_count in the CSV, token_estimate on the live body` | `collision.token_count_vs_token_estimate` | Two names for the token figure. The CSV column is `token_count`. The live body and the audit row use `tokens`. The gateway does not write the CSV, so they never meet. |
| `model column holds status words, live model is local-sim-v1` | `collision.model_column_vs_live_model` | Zero CSV rows hold the live model name. The column holds the generic words. |
| `critical in the alarm scale and the event log scale` | `collision.critical_in_two_scales` | One word in two scales. A query on `critical` mixes them. |
| `legacy as an endpoint word and a status word` | `collision.legacy_as_endpoint_and_status` | `legacy` sits next to `alpha` in `mgmt_ip` and next to `approved` in `hostname`. |
| `mgmt_ip holds words, not addresses` | `collision.mgmt_ip_holds_words` | Every filled `mgmt_ip` cell is one of five words. The column is still treated as sensitive. |
| `approval_required as a status column and as a yes or no input` | `collision.approval_required_column_and_policy_input` | One spelling, two meanings. The CSV column holds words such as `manual`. The policy input holds true or false. PROPOSED. |
| `Degraded as a runbook level and as a status word` | `collision.degraded_as_runbook_level_and_status_word` | The runbook level Degraded and the status word `degraded` share one spelling and mean different things. PROPOSED. |

## Business rules

Rules the system must keep. Nine of the 20 rules are enforced by code on a live route or in the batch. The YAML key `enforced_today` says which.

| Term | Id | Meaning |
|---|---|---|
| `a missing id must not return another device` | `rule.missing_id_not_other_device` | When no row has the id, the lookup returns no device. The record route still returns `REC-0001` for a missing id. The summary route blocks the call with `failmode.missing_id`. Defect F01. |
| `a record lookup matches the key column only` | `rule.record_lookup_matches_key_only` | The lookup compares the id with `device_id` only. Since stage S04-10 it does. Defect F17. |
| `AI output cannot execute` | `rule.ai_output_cannot_execute` | Model text is a recommendation. No code path turns it into a change. Since stage S04-09 the gateway never returns EXECUTE. |
| `alarm last_seen_at cannot precede first_seen_at` | `rule.alarm_last_seen_not_before_first_seen` | Last seen is the same time as first seen or later. 166 rows break this in the data. `dedupe.py` flags such a row, and no route calls it yet. Defect F08. |
| `a shared admin account is not least privilege` | `rule.shared_admin_not_least_privilege` | Each actor has its own identity with only the actions it needs. A shared user with a password in source, and an admin allowed everything, both break this. Stage S04-06 removed the any-admin rule. The admin role now has one allow row, TA-35, which reads the audit log. Defect F05. |
| `duplicate dedupe_key within a storm_batch_id is one alarm` | `rule.duplicate_dedupe_key_in_storm_is_one_alarm` | Two rows with the same `dedupe_key` and the same `storm_batch_id` count as one alarm. The rows stay on disk. |
| `an AI recommendation needs a policy result, an approval id, and an audit row before any state change` | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | Policy allow, then a human approval id, then an audit row, then a reversible validated change. The AI policy checks these for EXECUTE. No route writes an approval id, and no route reaches EXECUTE. |
| `mgmt_ip, credential_profile, and credentials never enter a prompt` | `rule.forbidden_fields_never_enter_prompt` | Those fields stay out of prompt text. Since stage S04-09 the gateway builds the prompt from the allow list and blocks the call when a forbidden name appears. The record route still returns both cells (defect F10). |
| `a stale topology flag blocks a recommendation` | `rule.stale_topology_blocks_recommendation` | When `stale_topology_flag` is `true`, the call stops before the model runs. A blank flag is Unknown. |
| `a denied access writes an audit row and a deny status` | `rule.denied_access_is_audited` | A refused call is recorded and the status says refused. Since stage S04-06 it is HTTP 403 and an audit row. Defect F14. |
| `a call without a role is not treated as operator` | `rule.no_default_role` | No role header means refused. The summary route and the audit route refuse it. The record route still fills in `operator`. Defects F15 and F16. |
| `an audit row names the actor and the request chain` | `rule.audit_row_names_actor_and_correlation` | Every audit row says who acted and which request it belongs to. Since stage S04-08 it does. Defect F11. |
| `one row per business key` | `rule.one_row_per_key` | Each key appears on one row. Each CSV has three keys that appear twice today. Defect F06. |
| `an audit case id over 128 characters is refused` | `rule.audit_case_id_limit` | The audit route refuses a case id longer than 128 characters, with HTTP 400. The number is PROPOSED. |
| `the audit log holds no forbidden field` | `rule.audit_log_holds_no_forbidden_field` | No audit row holds `mgmt_ip`, `credential_profile`, a secret, or the prompt text. The row has fixed keys. PROPOSED. |
| `no secret value is committed to the repo` | `rule.no_secret_value_committed` | No committed file holds a secret value. A file may name a secret and may not hold its value. A test checks it. PROPOSED. |
| `the Python copy and the Rego copy of the policy agree` | `rule.policy_copies_agree` | The Python copy and the Rego copy of a policy give the same answer for the same input. A test checks it. PROPOSED. |
| `a bad row is held aside and the batch goes on` | `rule.bad_row_held_aside_batch_goes_on` | A bad row is held aside, named by file line, and the batch goes on. The batch writes no file. PROPOSED. |
| `an event seen twice is one event` | `rule.repeat_event_is_one_event` | Two event lines with the same `event_id` are one event. The second is a repeat. PROPOSED. |
| `an order attempt with the same order_id and retry_count is one attempt` | `rule.order_attempt_same_retry_is_one_attempt` | Two order rows with the same `order_id` and `retry_count` are one attempt. PROPOSED. |

## Metrics

Measures computed from stored fields. No metric has a target.

| Term | Id | Meaning |
|---|---|---|
| `tokens per invocation` | `metric.tokens_per_invocation` | How many tokens one model call used. From `token_count` in the CSV, or `tokens` on the live body and the audit row. The live number is a word count times two and is EDUCATIONAL. |
| `cost per correlated incident` | `metric.cost_per_correlated_incident` | The total cost of the model calls made for one incident. This works only after the alarms are tied to that incident. The repo does not say how to tie them, and the price is Unknown. |
| `quarantine rate` | `metric.quarantine_rate` | The share of batch rows held aside as bad. The batch now prints a `quarantined` count. The count is not stored yet. |
| `retry count` | `metric.retry_count` | How many times an order build was tried again. 32 to 4995 in the data. The maximum is Unknown. |
| `audit completeness` | `metric.audit_completeness` | How much of a full decision record an audit row holds. The required-field list is PROPOSED. |
| `recommendation latency` | `metric.recommendation_latency` | How long a model call takes in milliseconds. Since stage S04-09 a live call that reaches the model records it. Report the 95th percentile (p95), decided in ADR 0002 on 2026-10-12. |
| `SLA breach risk` | `metric.sla_breach_risk` | A stored score on each incident. 352 values between 0 and 1. One is 1.42. The range is PROPOSED. Owner: Team-Force. |
| `alarm storm size` | `metric.alarm_storm_size` | How many alarms share one storm batch. The largest in the file is 2. What counts as a storm is Unknown. |
| `AI outcome count` | `metric.ai_outcome_count` | How many calls ended in each of the four outcomes. The audit key `outcome` holds the word on a summary call. EXECUTE never appears. PROPOSED. |
| `API availability` | `metric.api_availability` | How often a call to the API got a useful answer. The repo stores no counts, so it is Unknown today. PROPOSED. |
| `record read latency` | `metric.record_read_latency` | How long one record read takes inside the server, in milliseconds. PROPOSED. |
| `repeated prompt share` | `metric.repeated_prompt_share` | The share of model calls whose prompt hash matches an earlier call. PROPOSED. |
| `cost per flow` | `metric.cost_per_flow` | The cost of the steps of one business flow, for each of the four flows. The money unit is Unknown, so the figures are EDUCATIONAL. PROPOSED. |

## Access

### Actions

| Term | Id | Meaning |
|---|---|---|
| `read` | `action.read` | Look at stored rows. Nothing changes. The one action named in `access.rego`. |
| `summarize` | `action.summarize` | Ask a model for a short account of a record. The live route does this with no role check. |
| `recommend` | `action.recommend` | Ask a model for a next-action sentence. A person can accept or reject it. |
| `approve` | `action.approve` | A named person records yes or no. The system stores an approval id. No route does this today. |
| `write` | `action.write` | Change a stored row that is not a live network element. For example, open an incident. No route does this today. |
| `execute` | `action.execute` | Change a live device or circuit. No route does this today. It waits for four gates. |

### Resources

| Term | Id | Meaning |
|---|---|---|
| `device` | `resource.device` | A device row. The only resource the API serves today. |
| `circuit` | `resource.circuit` | A circuit row. |
| `alarm` | `resource.alarm` | An alarm row, or a storm batch of alarm rows. |
| `incident` | `resource.incident` | An incident row. |
| `service order` | `resource.service_order` | A service order row. |
| `AI invocation` | `resource.ai_invocation` | A stored model-call row, or a live model call. |
| `event` | `resource.event` | An event log line. |
| `audit log` | `resource.audit_log` | The file `logs/audit.log` and its rows. |
| `approval` | `resource.approval` | A stored approval id and its yes or no. |
| `sensitive device fields` | `resource.sensitive_device_fields` | `mgmt_ip` and `credential_profile`. `mgmt_ip` is the column meant to hold the address used to log in to and manage a device. `credential_profile` names the login details the device uses. Which personas may read them is Unknown. Today every allowed role reads them. |
| `model call queue` | `resource.model_call_queue` | A waiting line for model calls, so a slow model does not hold up other routes. It is a proposal (SR-04). No queue exists in the code. PROPOSED. |

### Purposes

All PROPOSED. The repo names no purpose. The comment in `access.rego` says participants should add purpose constraints.

| Term | Id | Meaning |
|---|---|---|
| `incident triage` | `purpose.incident_triage` | Working out what is wrong and what to do next on an open incident. |
| `network change planning` | `purpose.network_change_planning` | Preparing a change to a device or circuit before anyone approves it. |
| `field repair` | `purpose.field_repair` | Fixing or replacing equipment at a site. |
| `customer enquiry` | `purpose.customer_enquiry` | Answering a customer's question about their circuit, order, or incident. |
| `scheduled automation` | `purpose.scheduled_automation` | A machine running a planned step, such as the daily batch. |
| `vendor support` | `purpose.vendor_support` | A supplier helping with the equipment they supplied. |
| `AI assistance` | `purpose.ai_assistance` | A model reading records so it can write a summary or a recommendation. |
| `audit review` | `purpose.audit_review` | Reading the audit log to see who did what. |

### Scopes

Scope is the set of records a persona may touch.

| Term | Id | Meaning |
|---|---|---|
| `all records` | `scope.all_records` | Every row of the resource. No filter. |
| `one site` | `scope.one_site` | Only rows whose `site_id` is the caller's site. PROPOSED. |
| `one customer` | `scope.one_customer` | Only rows whose `customer_id` is the customer in the enquiry. PROPOSED. |
| `assigned incident` | `scope.assigned_incident` | Only the incident the caller is working on, plus its device and alarm rows. The alarm join is Unknown, so today this names the incident row only. PROPOSED. |
| `own vendor devices` | `scope.own_vendor_devices` | Only devices made by the caller's company. The `vendor` column holds status words today, so this cannot run yet. PROPOSED. |
| `none` | `scope.none` | No records. Used for an action a persona may never take. |

### Risks

These follow the four agency words analyse, recommend, decide, execute.

| Term | Id | Meaning |
|---|---|---|
| `read only` | `risk.read_only` | Nothing changes. The harm is that someone sees a row they should not. |
| `recommendation` | `risk.recommendation` | Text is produced. The harm is that a person trusts wrong text or treats it as a work order. |
| `decision` | `risk.decision` | A stored row or an approval changes. The harm is a wrong status or a closed incident that hides a fault. |
| `live network change` | `risk.live_network_change` | A live device or circuit changes. The harm is lost service. Undoing it is another live change. |

### API roles today

The five strings `apps/api/main.py` accepts in `X-User-Role`.

| Term | Id | Meaning |
|---|---|---|
| `admin` | `role.admin` | Accepted by the Python list. No persona is called admin. Before stage S04-06, `access.rego` allowed admin every action. Now admin has one allow row, TA-35, to read the audit log. |
| `operator` | `role.operator` | Accepted by the Python list. Used when no header is sent. Closest persona is `noc_operator`. Inference. |
| `clinician` | `role.clinician` | Accepted by the Python list. A health-care word. Removed in this layer. Defect F03. |
| `engineer` | `role.engineer` | Accepted by the Python list. Closest persona is `network_engineer`. Inference. |
| `ai_agent` | `role.ai_agent` | Accepted by the Python list. The only string that is both an API role and a persona. |

### Personas

The seven telecom personas from `docs/domain-specific-spec.md`. Their grants are PROPOSED.

| Term | Id | Meaning |
|---|---|---|
| `noc_operator` | `persona.noc_operator` | A person in the network operations centre. Watches alarms, handles incidents, reads the model's summary, and accepts or rejects its next-action sentence. 435 events. |
| `network_engineer` | `persona.network_engineer` | A person who designs and changes the network. Reads the configuration suggestion. Confirmed on 2026-10-10 as the human who approves a live network change. The persona grants stay PROPOSED. 440 events. |
| `field_engineer` | `persona.field_engineer` | A person who goes to a site and works on the equipment there. 422 events. |
| `customer_support` | `persona.customer_support` | A person who answers a customer. Sees that customer's circuits, orders, and incidents. 420 events. |
| `automation_service` | `persona.automation_service` | A machine account that runs planned steps. May execute only after a human approval id exists. Whether it is the shared user `app_shared` is Unknown. 444 events. |
| `vendor_account` | `persona.vendor_account` | A supplier's login. Reads the devices that supplier made. The replay's `vendor` header was refused. 424 events. |
| `ai_agent` | `persona.ai_agent` | The model acting as a caller. Reads allowed prompt fields and writes text. Never approves. Never executes. 415 events. |

## AI outcomes

Every model answer carries exactly one of these four words.

| Term | Id | Meaning |
|---|---|---|
| `RECOMMEND_ONLY` | `outcome.recommend_only` | The text is shown to a person. Stored rows stay as they are. Used by the incident summary. |
| `HOLD_FOR_REVIEW` | `outcome.hold_for_review` | The text waits for a named person to accept or reject it. Used by the next-action recommendation and the configuration suggestion. |
| `BLOCK` | `outcome.block` | A rule stopped the call. No text is acted on. The case goes to a person with the reason. |
| `EXECUTE` | `outcome.execute` | A change runs on a live device or circuit. Only workflow automation may reach it, after four gates. The model never sets it. No route reaches it in this packet. |

## Fail modes

What happens when a model call cannot give a safe answer. Each hands the case to a person and writes an audit row.

| Term | Id | Meaning |
|---|---|---|
| `timeout` | `failmode.timeout` | The model did not answer in time. The case goes to the person with no text. The timeout number is not set in this version. |
| `schema failure` | `failmode.schema_failure` | The answer is missing a required field or has a wrong type. The answer is discarded. |
| `missing id` | `failmode.missing_id` | No row has the requested id. The call stops before the model runs. |
| `stale topology flag is true` | `failmode.stale_topology_true` | `stale_topology_flag` is `true`. The call stops before the model runs. |
| `stale topology flag is blank` | `failmode.stale_topology_blank` | The flag is empty. What to do is Unknown. Until an owner decides, the case goes to the person. PROPOSED. |
| `forbidden field in prompt` | `failmode.forbidden_field_in_prompt` | The prompt builder found `mgmt_ip`, `credential_profile`, or a credential name. The call stops. |
| `input invalid or incomplete` | `failmode.input_invalid` | The policy input has a missing key or a value outside its list. The call is BLOCK. PROPOSED. |
| `model unreachable or breaker open` | `failmode.model_unreachable` | The circuit breaker refused the call or the model path was full. The case goes to a person with no text. PROPOSED. |
| `command text in the recommendation` | `failmode.command_text_in_recommendation` | The recommendation holds a sentence from the command list. The answer is discarded and the case goes to a person. PROPOSED. |
| `policy version differs` | `failmode.policy_version_differs` | The policy version in the input differs from the version of the policy that decided. The case goes to a person. PROPOSED. |

## Agency words

An agency word says how far one step may go. The `agency` key on each AI use, each outcome, and each access action holds one of these four words. The four stay separate. From `docs/02-baseline/ai-qualification.md` lines 18 and 19.

| Term | Id | Meaning |
|---|---|---|
| `analyse` | `agency.analyse` | Read stored fields and show them. Nothing changes. |
| `recommend` | `agency.recommend` | Show text that a person can accept or reject. Nothing changes until that person acts. |
| `decide` | `agency.decide` | Choose the outcome. For example, set a stored status or record an approval. |
| `execute` | `agency.execute` | Carry out a change on a live device or circuit. In this layer only workflow automation has this word. A model never has it. |

## Pick words

A pick word says what kind of tool does one step. The `pick` key on each AI use holds one of these four words. From `docs/02-baseline/ai-qualification.md` line 20.

| Term | Id | Meaning |
|---|---|---|
| `rules` | `pick.rules` | A fixed check reads a stored value and gives the answer. The same stored input always gives the same result. No model is called. Example: order qualification reads the word in `qualification_status`. |
| `deterministic_code` | `pick.deterministic_code` | Ordinary program code reads stored fields and works out the answer. The same stored input always gives the same result. No model is called. Example: alarm dedupe groups alarms whose `dedupe_key` text is equal. The repo does not say where a rule ends and code begins. |
| `workflow_automation` | `pick.workflow_automation` | A machine runs a fixed list of steps in order. The same stored input always gives the same result. No model is called. Example: remediation execution runs a policy allow, a human approval id, an audit row, and then the change. |
| `genai` | `pick.genai` | A language model writes new text from a prompt. Three AI uses have this pick. All three stop at text for a person. |

## AI uses

The eleven capabilities from `docs/02-baseline/ai-qualification.md`. Each row names the pick and the agency. Eight of the eleven call no model.

| Term | Id | Meaning |
|---|---|---|
| `order qualification` | `ai_use.order_qualification` | Show the stored word in `qualification_status` for a customer order. Pick `rules`, agency `analyse`. Not built today. |
| `provisioning retry and rollback` | `ai_use.provisioning_retry_and_rollback` | Show how many times an order build was tried again, and the word for whether it was undone. Pick `deterministic_code`, agency `analyse`. Not built today. |
| `alarm dedupe` | `ai_use.alarm_dedupe` | Group alarms that share the same `dedupe_key` and the same `storm_batch_id`, so a person sees one group. The rows stay on disk. Pick `deterministic_code`, agency `analyse`. Not built today. |
| `alarm-to-incident correlation` | `ai_use.alarm_to_incident_correlation` | List the ids that a set of alarms and an incident share, and flag an alarm whose last-seen time is before its first-seen time. The `noc_operator` opens or merges the incident. Pick `deterministic_code`, agency `analyse`. Which columns join the two is Unknown. |
| `topology lookup` | `ai_use.topology_lookup` | Return the one device row whose `device_id` matches the request. A missing id must come back as missing. Pick `deterministic_code`, agency `analyse`. Today a missing id returns `REC-0001` (defect F01). |
| `incident summary` | `ai_use.incident_summary` | A language model writes a short account of a case for the `noc_operator` to read. Stored rows stay as they are. Pick `genai`, agency `recommend`, outcome `RECOMMEND_ONLY`. PROPOSED. |
| `next-action recommendation` | `ai_use.next_action_recommendation` | A language model writes one next-step sentence. The `noc_operator` accepts or rejects it before any change ticket exists. A missing id or a true stale topology flag stops the call first. Pick `genai`, agency `recommend`, outcome `HOLD_FOR_REVIEW`. PROPOSED. |
| `configuration suggestion` | `ai_use.configuration_suggestion` | A language model writes a suggested device change in words. The `network_engineer` accepts or rejects it. The model does not push the change. Pick `genai`, agency `recommend`, outcome `HOLD_FOR_REVIEW`. PROPOSED. |
| `capacity forecast` | `ai_use.capacity_forecast` | Show the stored bandwidth numbers for circuits and orders. No file holds a history of use, so nothing is forecast. Pick `deterministic_code`, agency `analyse`. |
| `remediation execution` | `ai_use.remediation_execution` | A machine account makes a change on a live device or circuit. It runs only after a policy allow, a named human's stored approval id, and an audit row. Pick `workflow_automation`, agency `execute`. No model takes part. No route does this today. PROPOSED. |
| `remediation validation` | `ai_use.remediation_validation` | Compare the state after a change with the state the approval named, and report match or mismatch. Pick `deterministic_code`, agency `analyse`. The expected state is not defined in the repo. |

## Provenance fields

Provenance means where an answer came from. These nine fields travel on each model answer and on its audit row. Since stage S04-09 seven of them have a value on a call that reached the model. `policy_result` is on the answer only, and `approval_id` is always null.

| Term | Id | Meaning |
|---|---|---|
| `model` | `provenance.model` | The name of the model that answered. It is `local-sim-v1` on the answer and the audit row. It is null when the call stopped before the model. |
| `model_version` | `provenance.model_version` | The version of that model. Since stage S04-09 the answer and the audit row hold it. The string `local-sim-v1` serves as both name and version. |
| `prompt_hash` | `provenance.prompt_hash` | A SHA-256 code computed from the exact prompt text. A reviewer can prove which prompt was sent without storing the text. Since stage S04-09 the answer and the audit row hold it. |
| `tokens` | `provenance.tokens` | How many tokens the call used. A token is a small piece of text that a model counts and charges by. Since stage S04-09 the answer and the audit row carry `tokens`. The number is EDUCATIONAL. |
| `latency_ms` | `provenance.latency_ms` | How many milliseconds the call took. Missing from the live call. `events.jsonl` has it on every line. |
| `actor` | `provenance.actor` | Who asked for the answer. Since stage S04-06 the audit row holds a persona word when the role maps to one, and null when it does not. |
| `correlation_id` | `provenance.correlation_id` | One id shared by every step of the same request, so the steps can be found together. Since stage S04-08 every audit row holds it. The audit designs also call it the trace id (`trace_id`). It is the same value. No other trace id exists. |
| `policy_result` | `provenance.policy_result` | What the access policy said for this call: allow or deny. The answer body holds it. The audit key `policy_decision` exists and is null on every row. |
| `approval_id` | `provenance.approval_id` | The stored id of a named person's approval. The answer and the audit row have the key and it is null, because no route writes one. |

## Audit row fields

The 17 keys of one audit row, in the order the code writes them. The first 15 are from 1.1.0. `record_id` and `final_action` are added in 1.2.0 (stage S07). All are PROPOSED. Owner Team-Force.

| Term | Id | Meaning |
|---|---|---|
| `ts` | `field.audit_row.ts` | The time the row was written, as UTC text. |
| `correlation_id` | `field.audit_row.correlation_id` | The id shared by every row of one request. It also serves as the trace id. |
| `actor` | `field.audit_row.actor` | The persona word for the role header. Null when the role has no persona. It is not a named person. |
| `role` | `field.audit_row.role` | The role word the caller sent. Null when the header was missing. |
| `action` | `field.audit_row.action` | What happened. One word from the audit action list. |
| `resource` | `field.audit_row.resource` | What the call touched: `resource.device`, `resource.audit_log`, `resource.alarm` (a storm read) or `resource.ai_invocation` (an approval). |
| `policy_decision` | `field.audit_row.policy_decision` | The policy answer, allow or deny. The key exists and is null on every row today. |
| `approval_id` | `field.audit_row.approval_id` | The stored approval id. Set on the row of a yes from the approvals route. Null on every other row and on the row of a no. |
| `model` | `field.audit_row.model` | The model name. Null when the model did not run. |
| `model_version` | `field.audit_row.model_version` | The model version. Null when the model did not run. |
| `prompt_hash` | `field.audit_row.prompt_hash` | The SHA-256 code of the prompt text. Null when no prompt was sent. |
| `tokens` | `field.audit_row.tokens` | The token count of the model call. A word count times two, so EDUCATIONAL. |
| `latency_ms` | `field.audit_row.latency_ms` | Milliseconds the model call took. Null when the model did not run. |
| `outcome` | `field.audit_row.outcome` | One of the four outcome words on an AI call. Null on a record read and on a refusal. |
| `token_estimate_method` | `field.audit_row.token_estimate_method` | How `tokens` was worked out. Null when `tokens` is null. |
| `record_id` | `field.audit_row.record_id` | The device id the caller asked for, as typed. Null on a row that names no device, such as a storm read. |
| `final_action` | `field.audit_row.final_action` | What last happened to a device. The value is `none` on every row, because no route changes a device. |

## Approval record fields

Added in 1.2.0 (stage S07). Both are PROPOSED. Owner Team-Force.

| Term | Id | Meaning |
|---|---|---|
| `decision` | `field.approval.decision` | The word `yes` or `no` that the person sent to the approvals route. |
| `approver` | `field.approval.approver` | The persona id of the caller's role, set by the server. It is a claim, because the role is a header word the caller typed. |

## Policy inputs and policy items

Names that the policy files read and that no other list had. All are PROPOSED. Owner Team-Force.

| Term | Id | Meaning |
|---|---|---|
| `live model now` | `policy.model_now` | The live gateway as it is after stage S04-09. `policy.model_today` keeps the state before it. |
| `command phrases` | `policy.command_phrases` | The short list of command words, and the list of near-miss forms of them, that make the recommend route hold a model answer. Both lists are PROPOSED. |
| `access matrix rows` | `policy.opa.access_matrix` | The 35 allow rows TA-01 to TA-35 in `policy_data.json`. This replaces the two removed OPA rules. |
| `policy_version` | `field.policy_input.policy_version` | The version text of the policy that decided. A different version sends the call to a person. |
| `output_schema_ok` | `field.policy_input.output_schema_ok` | True when the model answer matched the output schema. |
| `timeout_hit` | `field.policy_input.timeout_hit` | True when the model did not answer in time or the breaker refused the call. |
| `forbidden_field_in_prompt` | `field.policy_input.forbidden_field_in_prompt` | True when the prompt text held a forbidden name or value. |
| `record_found` | `field.policy_input.record_found` | True when a row has the requested id. |
| `audit_row_written` | `field.policy_input.audit_row_written` | True when the audit row for this request exists. |
| `change_plan_ok` | `field.policy_input.change_plan_ok` | True when the change is reversible and validated. What validated means is Unknown. |
| `approval_required` | `field.policy_input.approval_required` | True when a human approval id is needed before any change. A yes or no input. |

## Status codes added in 1.1.0

Exact text that code writes or returns. Each row shows the text in the Term column. All are PROPOSED. Owner Team-Force.

| Term | Id | Meaning |
|---|---|---|
| `policy.deny` | `status.code.audit_action.policy_deny` | The audit action for a refused call, on any route, and for an AI call that ended BLOCK. |
| `policy.hold` | `status.code.audit_action.policy_hold` | The audit action for an AI call that ended HOLD_FOR_REVIEW. The route returns HTTP 202. |
| `audit.read` | `status.code.audit_action.audit_read` | The audit action the audit route writes when it returned a case. |
| `audit.not_found` | `status.code.audit_action.audit_not_found` | The audit action the audit route writes when no row has the id. HTTP 404. |
| `audit.id_refused` | `status.code.audit_action.audit_id_refused` | The audit action the audit route writes when the id is over 128 characters. HTTP 400. |
| `record.storm_read` | `status.code.audit_action.storm_read` | The audit action the storm route writes after an allowed read of one storm. Added in 1.2.0. |
| `ai.recommendation` | `status.code.audit_action.ai_recommendation` | The audit action the recommend route writes when it returned the sentence. It proves a recommendation was shown. Added in 1.2.0. |
| `ai.approval` | `status.code.audit_action.ai_approval` | The audit action the approvals route writes first, before it stores the decision. Added in 1.2.0. |
| `not_found` | `status.code.error.not_found` | The error body of the audit route for an id with no rows. |
| `id_too_long` | `status.code.error.id_too_long` | The error body of the audit route for an id over the limit. It also holds `max_length`. |
| `enforced` | `status.code.guardrail_status.enforced` | The word the live gateway returns when the prompt and answer checks ran. |
| `no X-User-Role header, or a blank one` | `status.code.role_header.absent` | A call with no role header, or a blank one. The policy has no row for it, so the call is refused. |
| `action_on_denied_list` | `status.code.policy_reason.action_on_denied_list` | The reason when a row matched and the action is on the caller's denied list. |
| `input_invalid` | `status.code.policy_reason.input_invalid` | The reason when the AI policy input has a missing key or a bad value. The call is BLOCK. |
| `policy_version_differs` | `status.code.policy_reason.policy_version_differs` | The reason when the policy version in the input is not the bundle's version. The call is HOLD_FOR_REVIEW. |
| `word_count_x2_EDUCATIONAL` | `status.code.token_estimate_method.word_count_x2_educational` | Says `tokens` is the prompt word count times two. It is not a tokenizer and not a bill. |
| `closed` | `status.code.breaker_state.closed` | The circuit breaker lets calls go to the model. The normal state. |
| `open` | `status.code.breaker_state.open` | The circuit breaker refuses every model call for a set time. |
| `half_open` | `status.code.breaker_state.half_open` | The set time has passed. The breaker lets one trial call through. |
| `queued` | `status.code.model_call_queue_state.queued` | A model call is waiting in the proposed queue. |
| `running` | `status.code.model_call_queue_state.running` | A model call left the proposed queue and the model is working on it. |
| `done` | `status.code.model_call_queue_state.done` | A model call finished and left the proposed queue. |
| `Stopped` | `status.code.runbook_level.stopped` | Runbook level: a business route gives no useful answer, or audit rows cannot be written. Act now. |
| `Degraded` | `status.code.runbook_level.degraded` | Runbook level: one dependency is down and people still get answers or a held case. |
| `Data fault` | `status.code.runbook_level.data_fault` | Runbook level: a data defect is found and the routes still answer. |
| `Watch` | `status.code.runbook_level.watch` | Runbook level: a failure happened once and cleared, and no user saw a wrong answer. |
| `prompt` | `status.code.field_destination.prompt` | A place a field value may go: the text sent to a model. |
| `api_response` | `status.code.field_destination.api_response` | A place a field value may go: the body an API route returns. |
| `log_line` | `status.code.field_destination.log_line` | A place a field value may go: a row in `logs/audit.log`. |
| `data file missing` | `status.code.fault.data_file_missing` | A fault: `devices.csv` is missing. The routes return HTTP 500 and write no audit row. |
| `audit log unwritable` | `status.code.fault.audit_log_unwritable` | A fault: `logs/audit.log` cannot be written. Every business route returns HTTP 500. |
| `policy_engine_error` | `status.code.fault.policy_engine_failed` | A fault: the policy engine gave no usable answer. The call is refused. |
| `last_seen_before_first_seen` | `status.code.alarm_flag.last_seen_before_first_seen` | The alarm check flag for last seen earlier than first seen. |
| `times_unreadable` | `status.code.alarm_flag.times_unreadable` | The alarm check flag for a blank or unreadable time. The row goes to review. |
| `new` | `status.code.dedupe_result.new` | The dedupe memory has not seen this key before. |
| `repeat` | `status.code.dedupe_result.repeat` | The dedupe memory has seen this key before. The row stays on disk. |
| `held_aside` | `status.code.dedupe_result.held_aside` | The key has a blank or missing part, so the row cannot be grouped. It is held aside. |
| `approval_id` | `status.code.cannot_prove.approval_id` | Cannot prove: `approval_id` is null on every row. |
| `policy_decision` | `status.code.cannot_prove.policy_decision` | Cannot prove: `policy_decision` is null on every row. |
| `model` | `status.code.cannot_prove.model` | Cannot prove: no row shows a model call. |
| `actor` | `status.code.cannot_prove.actor` | Cannot prove: at least one row has no actor. |
| `final_action` | `status.code.cannot_prove.final_action` | Cannot prove: no column holds the final action. |
| `record_asked_for` | `status.code.cannot_prove.record_asked_for` | Cannot prove: no column holds the record id the caller asked for. |
| `policy_reasons_and_version` | `status.code.cannot_prove.policy_reasons_and_version` | Cannot prove: the policy reasons and version are not stored on any row. |
| `caller_identity` | `status.code.cannot_prove.caller_identity` | Cannot prove: the role is a word the caller typed. |
| `case_membership` | `status.code.cannot_prove.case_membership` | Cannot prove: the caller chose the correlation id, so another caller can reuse it. |
| `log_integrity` | `status.code.cannot_prove.log_integrity` | Cannot prove: the log is a plain file and a line can be changed or deleted. |
| `rows_before_correlation_id` | `status.code.cannot_prove.rows_before_correlation_id` | Cannot prove: some log lines have no correlation id and are never returned. |
| `unreadable_lines` | `status.code.cannot_prove.unreadable_lines` | Cannot prove: some log lines could not be read. Listed only when the count is above zero. |
| `withheld_text` | `status.code.cannot_prove.withheld_text` | Cannot prove: some values were replaced because they held a forbidden name. Listed only when the count is above zero. |

## Lifecycle

This file cites `docs/01-discovery/`, `docs/02-baseline/data-quality-baseline.md`, `docs/02-baseline/defect-list.md`, and `docs/02-baseline/ai-qualification.md`. Stage S03R reviews it. Stage S05R adds rows for terms the control designs introduce and raises the version. After S05R, a change here needs an ADR.
