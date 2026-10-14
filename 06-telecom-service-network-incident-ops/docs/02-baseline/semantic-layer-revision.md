# Semantic layer revision (S05R)

| Field | Value |
|---|---|
| Stage | S05R, Semantic layer revision. It folds the Phase 4 and Phase 5 designs into `semantic-layer/` and reruns the S03R rows. |
| Date / version | 2026-10-12. The semantic layer moves from `1.0.0` to `1.1.0`. ADR 0002 later raised it to `1.1.1` by changing one sentence. ADR 0005 (stage S07, 2026-10-13) raised it to `1.2.0` by adding 8 ids. ADR 0006 (2026-10-13) raised it to `1.2.1` by changing one formula word (`policy_result` to `outcome`). **The current version is `1.2.1`.** The rest of this file records the S05R run at `1.1.0`. One version value is used in all seven YAML files, in the schema, in `generated/manifest.json`, and in `semantic-layer/README.md`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | CONDITIONAL PASS. Build, `--check`, and all test runs pass. Security stage passes with 0 skipped tests. S03R rows R1 to R15 and failure-list rows 1 to 8 all pass. Twenty design questions are deferred, each with an owner. Gate rule: a deferred row that names an owner gives CONDITIONAL PASS. Later on 2026-10-12, the owner decided the open items in `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`. Of the 20, five are decided (D-03, D-06, D-08, D-12, D-16), one is closed (D-13), and 13 stay deferred (D-07 was decided later in ADR 0003). The layer is now `1.1.1`. This file keeps the S05R record as it was run. |
| Evidence sources | `semantic-layer/` (all files); `docs/03-identity` to `docs/14-audit` design files and Half B `evidence.md` files; `docs/runbooks/`; `security/`; `docs/02-baseline/semantic-layer-review.md`; `docs/02-baseline/semantic-layer-fixes.md`; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/operating-contract.md`; ids and "Open question for S03" lines in `policy/`, `tests/`, `apps/`, `etl/`, and `docs/12-finops/metrics_from_audit.py`; `Semantic_Layer_capture.pdf`; `Project_Intent - sections 6.2, 6.3, Appendix E.md`; `playbook/S03R-semantic-layer-review - 15 check rows.md`; `playbook/README.md`; command output from 2026-10-12 pasted below |
| Assumptions | (1) "Never edit a test" in the stage rules means the repo tests under `tests/` and `policy/tests/`. This stage did edit `semantic-layer/tests/test_semantic_layer.py`, which is part of the semantic layer tree. The edits are listed in "Test edits". (2) Changing `enforced_today` from false to true on six rules is a change of state. It is not a change of meaning of the id. Each flip has a sentence in the rule that names the code. (3) Every item this stage added is PROPOSED with owner Team-Force, because Team-Force owns open choices (`docs/00-contract/operating-contract.md` row 10). (4) The access matrix row TA-35 and the 128-character id limit were accepted by Mangesh on 2026-10-12. The YAML still marks them PROPOSED, because the operating contract does not list them. |
| Unresolved issues | Twenty deferred items, D-01 to D-20, each with owner Team-Force. |
| Residual risks | See the end of this file. The main one: a deferred field (record id, named person, final action) means the audit row still cannot answer some defence questions. |

Claim labels: **Verified Fact** (read in a file, or run), **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file and line, a YAML id, or a test name.

Paths are relative to `06-telecom-service-network-incident-ops/`. "SL" means `semantic-layer/`.

## 1. What changed in one paragraph

**Verified Fact.** The YAML held 665 ids at `1.0.0`. It holds 757 at `1.1.0`. Ninety-two ids were added. No id was removed. Two ids were marked `deprecated: true` with `replaced_by`. Sixty-two existing ids had text corrected or extended. Each of those keeps its id and its meaning. Command: `python C:\Users\mange\AppData\Local\Temp\s05r\newids.py` printed `added 92 lost 0 old 665 new 757`. The per-file split is in section 6.

## 2. Collection table

Each row is one place where a design, a policy file, a test, or a code comment asked for a term the YAML lacked. Some rows group several lines that ask for the same term. The "Source file and line" column lists every line in the group. Line numbers are from 2026-10-12.

Decision words: **add** (new id), **alias** (a second name that points at an id that exists), **reject** (no change, with reason), **defer** (no change now, with an owner).

| Row | Source file and line | Term as the design wrote it | Needed for | YAML file | Decision and reason |
|---|---|---|---|---|---|
| C-01 | `docs/06-policy/policy-catalogue.md:94`; `docs/03-identity/negative-access-test-plan.md:138`, `:159`; `docs/03-identity/privilege-reduction-backlog.md:79`; `docs/03-identity/policy-input-model.md:179`; `docs/13-security-validation/remediation-backlog.md:26` | a call that sends no role header | A deny rule must name an empty role | `status-taxonomy.yaml` | **Add** `status.code.role_header.absent`. Five designs ask. The record route in `apps/api/main.py` still gives such a call the role `operator`. The id names the state. It does not name a role. |
| C-02 | `docs/06-policy/policy-catalogue.md:87`, `:96` | destination of a field: prompt, API response, log line | The data-use policy says where a field may go | `status-taxonomy.yaml` | **Add** `status.code.field_destination.prompt`, `.api_response`, `.log_line`. |
| C-03 | `docs/06-policy/policy-catalogue.md:89`, `:98` | the checks a release must show | The production-readiness policy | none | **Defer** (D-01). Owner Team-Force. No policy file and no test reads these checks. An id with no reader would be a term that nothing uses. |
| C-04 | `policy/opa/access.rego:93`; `docs/06-policy/evidence.md:192` | `action_on_denied_list` | The reason text for a denied-list refusal | `status-taxonomy.yaml` | **Add** `status.code.policy_reason.action_on_denied_list`. |
| C-05 | `docs/06-policy/evidence.md:193` | should the two routes send `purpose` and `scope` from the caller | Route behaviour | none | **Reject.** No term is missing. The question is about route behaviour, and this stage does not change routes. |
| C-06 | `docs/06-policy/exception-handling-model.md:62` | `waiver` | The register and the audit row | `entities.yaml` | **Add** `concept.waiver`. The text says no register, route, or audit action for a waiver exists in the code. |
| C-07 | `docs/06-policy/exception-handling-model.md:64` | audit actions for a waiver granted and a waiver used | Two audit rows | none | **Defer** (D-02). Owner Team-Force. No code writes a waiver row. Two ids would describe a behaviour that does not exist. |
| C-08 | `docs/06-policy/exception-handling-model.md:66` | a persona that may waive a rule | A persona id | none | **Reject.** Team-Force is a team, not a persona (`docs/00-contract/operating-contract.md` row 10). The personas stay at the locked seven. |
| C-09 | `docs/06-policy/ai-action-policy-design.md:50`; `docs/09-ai-guardrails/model-provenance-design.md:52`; `docs/09-ai-guardrails/ai-risk-register.md:124`; `policy/opa/ai_action.rego:21` | `policy_version` | Send a call made under an old policy to a person | `ai-context-policy.yaml` | **Add** `field.policy_input.policy_version`. The four lines share one id. |
| C-10 | `docs/06-policy/ai-action-policy-design.md:52`, `:54`, `:56`, `:58`, `:60`; `docs/09-ai-guardrails/ai-risk-register.md:96`, `:111` | `output_schema_ok`, `timeout_hit`, `forbidden_field_in_prompt`, `record_found`, `audit_row_written` | Inputs of the AI action policy | `ai-context-policy.yaml` | **Add** five ids `field.policy_input.*`. |
| C-11 | `docs/06-policy/ai-action-policy-design.md:62`; `policy/opa/ai_action.rego:156` | `change_plan_ok`, "validated" | The fourth gate of EXECUTE | `ai-context-policy.yaml` | **Add** `field.policy_input.change_plan_ok`. The text says what counts as validated is Unknown, and that no route sets the input. |
| C-12 | `docs/06-policy/ai-action-policy-design.md:64` | `approval_required` as a yes or no input | An input that does not share a name with the CSV column | `ai-context-policy.yaml`, `status-taxonomy.yaml` | **Add** `field.policy_input.approval_required` and `collision.approval_required_column_and_policy_input`. |
| C-13 | `docs/06-policy/ai-action-policy-design.md:66`, `:220`; `docs/09-ai-guardrails/approval-workflow.md:80`; `docs/13-security-validation/remediation-backlog.md:39` | approval `decision` and `approver` fields | A rejected approval id must not unlock EXECUTE | none | **Defer** (D-03). Owner Team-Force. No approval store and no approval route exist. Stage S07 adds them. |
| C-14 | `docs/06-policy/ai-action-policy-design.md:68`; `policy/opa/ai_action.rego:78`; `docs/09-ai-guardrails/unsafe-output-handling-rules.md:56` | a failmode for invalid or incomplete input | Row B1 | `ai-context-policy.yaml`, `status-taxonomy.yaml` | **Add** `failmode.input_invalid` and `status.code.policy_reason.input_invalid`. |
| C-15 | `docs/06-policy/ai-action-policy-design.md:70`, `:223` | does stale topology also block a summary | Policy row B5 | `ai-context-policy.yaml` | **Add** `block_conditions` on `ai_use.incident_summary`, PROPOSED. `outcome.block` lists the use. The design applies B5 to all three AI actions. |
| C-16 | `docs/06-policy/ai-action-policy-design.md:72`, `:227` | `ai_use` as a policy input | Pick the reviewer | none | **Reject.** The design says the decision does not read it. |
| C-17 | `policy/opa/ai_action.rego:191` | a policy version mismatch | A failmode and a reason | `ai-context-policy.yaml`, `status-taxonomy.yaml` | **Add** `failmode.policy_version_differs` and `status.code.policy_reason.policy_version_differs`. |
| C-18 | `docs/03-identity/target-access-matrix.md:96`; `docs/14-audit/evidence.md:178` | `resource.audit_log`, `purpose.audit_review` | Access row TA-35 | none | **Reject.** Both ids exist in `access-semantics.yaml` already. |
| C-19 | `docs/14-audit/audit-read-access-design.md:138` | a persona for the audit reviewer | Name a persona in the row | none | **Reject.** The personas are locked at seven. TA-35 uses `role.admin`, accepted by Mangesh on 2026-10-12. |
| C-20 | `docs/14-audit/audit-read-access-design.md:140` | a scope for one case | A grant narrower than `scope.all_records` | none | **Defer** (D-04). Owner Team-Force. TA-35 uses `scope.all_records`. |
| C-21 | `docs/14-audit/audit-read-access-design.md:142`; `docs/14-audit/evidence.md:177`; `apps/api/main.py:14`; `docs/08-observability/log-schema.md:138` | `audit.read`, `audit.not_found`, `audit.id_refused`, `policy.deny`, `policy.hold` | Audit action words | `status-taxonomy.yaml` | **Add** five `status.code.audit_action.*` ids. |
| C-22 | `docs/14-audit/audit-read-access-design.md:144`; `docs/14-audit/audit-gap-report.md:135`; `docs/14-audit/evidence.md:180` | the allowed form of a case id | Refuse a long id | `business-rules.yaml`, `status-taxonomy.yaml` | **Add** `rule.audit_case_id_limit` (128 characters, PROPOSED, accepted by Mangesh on 2026-10-12), `status.code.error.id_too_long`, and `status.code.error.not_found`. |
| C-23 | `docs/14-audit/decision-provenance-model.md:120`; `docs/14-audit/evidence.md:179`; `apps/api/services/audit_query.py:19` | items on the "cannot prove" list | Stable names for the route and the dashboard | `status-taxonomy.yaml` | **Add** 13 `status.code.cannot_prove.*` ids. A test compares them with the 13 item names in `audit_query.py`. |
| C-24 | `docs/14-audit/decision-provenance-model.md:98`; `docs/08-observability/trace-design.md:11` | `trace_id` | Defence question 5 | `ai-context-policy.yaml` | **Alias** to `provenance.correlation_id`. The description and the glossary row say the two names are one value. |
| C-25 | `docs/14-audit/decision-provenance-model.md:124`, `:127`, `:129`, `:133`; `docs/14-audit/audit-gap-report.md:124`, `:157` | final action; route and method; cells returned to the caller; test-versus-real flag | Audit row fields | none | **Defer** (D-05). Owner Team-Force. `SCHEMA_KEYS` in `apps/api/services/audit.py` has 15 keys and none of these. A YAML field would name a column that does not exist. `status.code.cannot_prove.final_action` records that the fact cannot be proven today. |
| C-26 | `docs/14-audit/audit-gap-report.md:102`; `docs/08-observability/log-schema.md:142` | `policy_decision` has two YAML names | One id for the audit column | `entities.yaml` | **Alias.** `field.audit_row.policy_decision` names the column. Its text lists the two older names, `concept.policy_decision` and `provenance.policy_result`. |
| C-27 | `docs/14-audit/audit-gap-report.md:113`; `docs/14-audit/before-and-after-audit-example.md:121`; `docs/08-observability/log-schema.md:144` | `record_id` and `reasons` on the audit row (LS-Q7) | Metric `audit_completeness` | none | **Defer** (D-06). Owner Team-Force. The row has no such keys. The text of `metric.audit_completeness` now says so. |
| C-28 | `docs/14-audit/audit-gap-report.md:168`; `docs/08-observability/log-schema.md:134`; `docs/08-observability/trace-design.md:11`, `:131` | the named person on an API call (LS-Q2) | Say who called | none | **Defer** (D-07). Owner Team-Force. `field.event.actor` is a persona word on the event file. It is not a person. |
| C-29 | `docs/08-observability/log-schema.md:132`, `:136`, `:140`, `:176`; `apps/api/services/audit.py:37`; `docs/12-finops/finops-dashboard-fields.md:68`; `docs/12-finops/evidence.md:117` | ids for the audit columns `ts`, `role`, `resource`, `token_estimate_method`, and the rest | The 15-key audit row | `entities.yaml`, `status-taxonomy.yaml` | **Add** 15 `field.audit_row.*` ids in the order of `SCHEMA_KEYS`, and `status.code.token_estimate_method.word_count_x2_educational`. |
| C-30 | `docs/08-observability/slo-proposal.md:11`, `:98`; `docs/08-observability/metric-catalogue.md:11` | API availability | A metric id | `metrics.yaml` | **Add** `metric.api_availability`. Target null. |
| C-31 | `docs/08-observability/incident-reconstruction.md:11`, `:108`; `docs/12-finops/retry-cost-analysis.md:137`; `docs/12-finops/cost-per-workflow.md:132`; `docs/11-reliability/failure-mode-catalogue.md:266` | an event time, an event sequence number, an order timestamp, a link from a model call to an event | New columns on `entities.yaml` fields | none | **Reject.** The test `test_entity_fields_match_csv_headers` ties each entity field to a CSV column. No CSV has these columns, and CSV files are outside this stage. |
| C-32 | `docs/09-ai-guardrails/guardrail-test-pack.md:104`; `docs/09-ai-guardrails/evidence.md:256`; `docs/09-ai-guardrails/ai-risk-register.md:154`; `docs/13-security-validation/remediation-backlog.md:36`; `apps/api/services/ai_gateway.py:72` | a command list and a failmode for an execute verb in recommendation text | Name the reason when a recommendation reads like a command | `ai-context-policy.yaml` | **Add** `failmode.command_text_in_recommendation`. **Defer** the full command list (D-08). Owner Team-Force. The code holds one sentence. |
| C-33 | `docs/09-ai-guardrails/ai-risk-register.md:53`; `docs/13-security-validation/remediation-backlog.md:43` | a failmode for instruction text inside an allowed field | A test reason for `hostname` holding a sentence | none | **Defer** (D-09). Owner Team-Force. `find_forbidden` in `ai_gateway.py` cannot detect it today. |
| C-34 | `docs/09-ai-guardrails/evidence.md:250`; `apps/api/services/ai_gateway.py:64` | `guardrail_status` value `enforced` | The checks ran | `status-taxonomy.yaml` | **Add** `status.code.guardrail_status.enforced`. The `not_enforced` text now says it was the state before S04-09. |
| C-35 | `docs/09-ai-guardrails/evidence.md:252`; `docs/09-ai-guardrails/model-provenance-design.md:48`; `docs/09-ai-guardrails/ai-risk-register.md:124` | `prompt_template_version` | Name the prompt wording used | none | **Defer** (D-10). Owner Team-Force. The audit row has no such key. The prompt hash is the record. |
| C-36 | `docs/09-ai-guardrails/evidence.md:254`; `docs/09-ai-guardrails/model-provenance-design.md:50` | the algorithm of `prompt_hash` | Let a second system recompute it | `ai-context-policy.yaml` | **Alias.** `provenance.prompt_hash` says SHA-256 in hexadecimal. |
| C-37 | `docs/09-ai-guardrails/evidence.md:258`; `docs/09-ai-guardrails/ai-risk-register.md:111`; `apps/api/services/ai_gateway.py:301`; `docs/06-policy/ai-action-policy-design.md:54` | the model timeout in seconds | `fail_to_person.timeout_seconds` | none | **Defer** (D-11). Owner Team-Force. The slot stays `null` (`SL/ai-context-policy.yaml:438`). The test `test_gr05_yaml_timeout_slot_stays_null_in_this_stage` requires `null`. |
| C-38 | `docs/09-ai-guardrails/evidence.md:260` | `summary` and `recommendation` may be null on a failure body | The output schema | `ai-context-policy.yaml` | **Add** `nullable: true` on seven output fields: `summary`, `recommendation`, `model`, `model_version`, `prompt_hash`, `tokens`, `latency_ms`. Required lists are unchanged. |
| C-39 | `docs/09-ai-guardrails/evidence.md:262` | the `model_today` block describes the old gateway | A true description of the live gateway | `ai-context-policy.yaml` | **Add** `policy.model_now`. `model_today` stays as the state before S04-09. The test `test_model_today_matches_code` reads its values. |
| C-40 | `docs/04-secrets/sensitive-field-handling-checklist.md:78`, `:94`; `docs/13-security-validation/remediation-backlog.md:43` | may `field.service_order.customer_id` enter a prompt | Prompt rules | `ai-context-policy.yaml` | **Add** the field to the `forbidden` list (`SL/ai-context-policy.yaml:212`), PROPOSED. The other two `customer_id` fields on that list are forbidden. |
| C-41 | `docs/04-secrets/rotation-evidence-plan.md:43`, `:58` | a store for the rotation record | Name where the record lives | none | **Defer** (D-12). Owner Team-Force. No file or table holds a rotation record. |
| C-42 | `docs/05-iac/configuration-ownership-map.md:92` | an owner role for the environment settings | A role id | none | **Defer** (D-13). Owner Team-Force. No persona matches. |
| C-43 | `docs/10-performance/scaling-recommendations.md:108`, `:110`; `docs/10-performance/evidence.md:199`; `docs/10-performance/performance-baseline.md:11` | a metric for record read latency; a resource for the model-call queue; queue states | Name the queue in access, audit, and policy rows | `metrics.yaml`, `access-semantics.yaml`, `status-taxonomy.yaml` | **Add** `metric.record_read_latency` (target null), `resource.model_call_queue`, and three `status.code.model_call_queue_state.*` ids. |
| C-44 | `docs/11-reliability/failure-mode-catalogue.md:264` (OQ-1) | the model is not reachable, or the breaker is open | A failmode | `ai-context-policy.yaml` | **Add** `failmode.model_unreachable`. |
| C-45 | `docs/11-reliability/failure-mode-catalogue.md:268` (OQ-3); `apps/api/services/dedupe.py:21` | an event seen twice is one event; an order attempt with the same `order_id` and `retry_count` is one attempt | Replay rules | `business-rules.yaml`, `status-taxonomy.yaml` | **Add** `rule.repeat_event_is_one_event`, `rule.order_attempt_same_retry_is_one_attempt`, and three `status.code.dedupe_result.*` ids. Both rules have `enforced_today: false`, because no route calls `dedupe.py`. |
| C-46 | `docs/11-reliability/failure-mode-catalogue.md:270` (OQ-4); `etl/run_daily_batch.py:9` | a bad row is held aside and the batch goes on | A rule for `metric.quarantine_rate` | `business-rules.yaml` | **Add** `rule.bad_row_held_aside_batch_goes_on`. `enforced_today: true`, because the batch counts and prints each such row. |
| C-47 | `docs/11-reliability/failure-mode-catalogue.md:272` (OQ-5) | a data file is missing; the policy engine failed; the audit log cannot be written | Fault names | `status-taxonomy.yaml` | **Add** three `status.code.fault.*` ids. |
| C-48 | `docs/11-reliability/failure-mode-catalogue.md:274` (OQ-6) | dependency states closed, open, half open; a metric for how often the model path was held open | Breaker states | `status-taxonomy.yaml` | **Add** three `status.code.breaker_state.*` ids. **Defer** the metric (D-14). Owner Team-Force. |
| C-49 | `docs/11-reliability/failure-mode-catalogue.md:276` (OQ-7); `docs/runbooks/incident-response.md:32` | names for incident severity levels | The runbook levels | `status-taxonomy.yaml` | **Add** four `status.code.runbook_level.*` ids (`stopped`, `degraded`, `data_fault`, `watch`) and `collision.degraded_as_runbook_level_and_status_word`. The alarm severity order stays open (see the README open questions table). |
| C-50 | `apps/api/services/dedupe.py:37` | a blank or unreadable timestamp | Alarm flags | `status-taxonomy.yaml` | **Add** two `status.code.alarm_flag.*` ids. |
| C-51 | `docs/12-finops/ai-cost-baseline.md:209`, `:220` | a list of real model names; a list of risk levels | Group cost by model and by risk | none | **Defer** (D-15). Owner Team-Force. No file lists either. |
| C-52 | `docs/12-finops/ai-cost-baseline.md:253` | a percentile rule for `metric.recommendation_latency` | Report the tail | none | **Defer** (D-16). Owner Team-Force. The metric text names the deferral. |
| C-53 | `docs/12-finops/optimization-backlog.md:46` | a metric for repeated prompts | Show the saving from a cache | `metrics.yaml` | **Add** `metric.repeated_prompt_share`. Target null. |
| C-54 | `docs/12-finops/optimization-backlog.md:63` | allowed alarm fields such as `storm_batch_id` and `alarm_type` | A batch summary | none | **Defer** (D-17). Owner Team-Force. Allowing more fields widens the prompt. No batch summary design exists to justify it. |
| C-55 | `docs/12-finops/optimization-backlog.md:77`, `:129`; `docs/12-finops/finops-dashboard-fields.md:66`; `docs/12-finops/evidence.md:219` | audit row fields for capability, incident id, flow, and "served from cache" | Group cost and count cache hits | none | **Defer** (D-18). Owner Team-Force. The audit row has 15 keys and none of these. |
| C-56 | `docs/12-finops/cost-per-workflow.md:121`, `:154` | a metric for cost per flow; the alarm-to-incident join | Cost per flow | `metrics.yaml` | **Add** `metric.cost_per_flow`. Target null. The join stays open, owned by the existing `relationship.alarm_to_incident` row in the README open questions. |
| C-57 | `docs/12-finops/finops-dashboard-fields.md:70`; `docs/12-finops/metrics_from_audit.py:316`; `docs/12-finops/evidence.md:90` | a stored place for the ETL `quarantined` count | `metric.quarantine_rate` | none | **Defer** (D-19). Owner Team-Force. The batch prints the count and stores it nowhere. The text of `metric.quarantine_rate` says so. |
| C-58 | `docs/13-security-validation/security-test-suite-plan.md:56`, `:170` | no secret value is committed | A rule for SV-09 and SV-26 | `business-rules.yaml` | **Add** `rule.no_secret_value_committed`. `enforced_today: false`. A test holds it. No code in `apps/` or `etl/` does. |
| C-59 | `docs/13-security-validation/security-test-suite-plan.md:61`, `:172` | the audit log holds no forbidden field | A rule for SV-14 and SV-25 | `business-rules.yaml` | **Add** `rule.audit_log_holds_no_forbidden_field`. `enforced_today: true`. |
| C-60 | `docs/13-security-validation/security-test-suite-plan.md:62`, `:174` | both copies of the policy agree | A rule for SV-15 | `business-rules.yaml` | **Add** `rule.policy_copies_agree`. `enforced_today: false`. Tests check it. No route does. |
| C-61 | `security/threat-model.md:194` | MAESTRO letters and layers | A map of threats to a list | none | **Defer** (D-20). Owner Team-Force. No file defines the list. This file does not invent one. |
| C-62 | `policy/opa/policy_data.json`; `policy/opa/access.rego`; `docs/03-identity/target-access-matrix.md` | the 35-row access matrix | Replace two ids that describe rules the policy no longer has | `access-semantics.yaml` | **Add** `policy.opa.access_matrix`. **Deprecate** `policy.opa.admin_any` and `policy.opa.operator_read` with `replaced_by: policy.opa.access_matrix`. |
| C-63 | `docs/14-audit/decision-provenance-model.md` (nine groups) | decision provenance | A name for the nine groups | `entities.yaml` | **Add** `concept.decision_provenance`. |
| C-64 | `docs/07-cicd/security-scan-plan.md:129`; `docs/07-cicd/release-evidence-checklist.md:81`; `docs/07-cicd/pipeline-improvement-plan.md:137`; `docs/07-cicd/evidence.md:252`; `evidence/README.md:93`; `docs/13-security-validation/scanning-checklist.md:119`; `docs/13-security-validation/remediation-backlog.md:107`; `docs/13-security-validation/negative-tests.md:107`; `docs/13-security-validation/evidence.md:153`; `docs/13-security-validation/abuse-case-evidence.md:74`; `docs/08-observability/dashboard-sketch.md:11`, `:88`, `:99`; `docs/08-observability/metric-catalogue.md:161`, `:172` | "Open question for S03: none" | Nothing | none | **Reject.** These lines ask for no term. |
| C-65 | `docs/14-audit/evidence-chain-one-case.md:11`, `:169`; `docs/14-audit/audit-gap-report.md:11` | pointers to other open questions | Nothing new | none | **Reject.** The questions they point to are rows C-21 to C-29. |

**Count of decisions.**

- Add: 36 rows (C-01, C-02, C-04, C-06, C-09 to C-12, C-14, C-15, C-17, C-21 to C-23, C-29, C-30, C-32, C-34, C-38 to C-40, C-43 to C-50, C-53, C-56, C-58 to C-60, C-62, C-63). C-32 and C-48 also hold a deferred part.
- Alias: 3 rows (C-24, C-26, C-36).
- Reject: 8 rows (C-05, C-08, C-16, C-18, C-19, C-31, C-64, C-65).
- Defer: 20 items, D-01 to D-20. Eighteen rows are fully deferred, and C-32 and C-48 add one deferred part each.

Two deferred items were not named in earlier notes for this stage: the release checks (C-03, D-01) and the allowed alarm fields for a batch summary (C-54, D-17). Both are in the table with an owner.

### Deferred items in one list

| Id | What is deferred | Owner | Why it waits |
|---|---|---|---|
| D-01 | Release check ids | Team-Force | No reader exists. |
| D-02 | Audit actions for a waiver granted and used | Team-Force | No code writes them. |
| D-03 | Approval `decision` and `approver` fields | Team-Force | No approval store until S07. |
| D-04 | A scope for one audit case | Team-Force | TA-35 uses `scope.all_records`. |
| D-05 | Final action, route and method, cells returned, test-versus-real flag | Team-Force | The audit row has no such key. |
| D-06 | `record_id` and `reasons` on the audit row | Team-Force | The row has no such key. |
| D-07 | The named person on an API call | Team-Force | No identity source exists. |
| D-08 | The full list of command phrases | Team-Force | The code holds one phrase. |
| D-09 | A failmode for instruction text inside an allowed field | Team-Force | No code detects it. |
| D-10 | `prompt_template_version` | Team-Force | The audit row has no such key. |
| D-11 | The model timeout in seconds | Team-Force | A test requires `null`. |
| D-12 | A store for the rotation record | Team-Force | No store exists. |
| D-13 | An owner role for environment settings | Team-Force | No persona matches. |
| D-14 | A metric for how often the model path is held open | Team-Force | No design sets the formula. |
| D-15 | A list of model names and a list of risk levels | Team-Force | No file lists them. |
| D-16 | A percentile rule for `metric.recommendation_latency` | Team-Force | No design sets it. |
| D-17 | Allowed alarm fields for a batch summary | Team-Force | Widens the prompt without a design. |
| D-18 | Audit row fields for capability, incident id, flow, cache flag | Team-Force | The audit row has no such key. |
| D-19 | A stored place for the quarantined count | Team-Force | The batch only prints it. |
| D-20 | The MAESTRO list | Team-Force | No file defines it. |

## 3. How each addition was folded

**Verified Fact.** Every added id has a plain-speech `description:`, a `source:` list of paths that exist, `proposed: true`, `owner: Team-Force`, and a glossary row. The tests `test_every_item_has_a_source_list_of_existing_paths`, `test_every_proposed_item_names_an_owner`, and `test_glossary_and_yaml_agree_on_every_term` check this and pass.

New schema rules in `SL/schemas/semantic-layer.schema.json` (version 1.1.0):

| Rule | What it does |
|---|---|
| `deprecated` and `replaced_by` on every item | An item with `deprecated: true` must name `replaced_by`. An item with `replaced_by` must have `deprecated: true`. |
| `audit_row_field` | One audit row key. It needs `type`, `position`, and `nullable`. |
| `concept` | A concept may hold `row_fields`. |
| `policy_input` | One input of the AI action policy. It has a `type` of boolean or text, and a `set_by`. |
| `model_now` and `policy_inputs` in `ai_context_policy` | The live gateway state, and the eight inputs. |

## 4. Protecting existing ids

**Verified Fact.** Script `cites.py` compared each id in the `1.0.0` YAML (from `git show HEAD:`) with the `1.1.0` YAML. It found 665 old ids, 757 new ids, and 0 lost ids. It found 62 old ids with changed content. No changed id changed its meaning. Each change is one of: a sentence about an old state rewritten with "Now (S05R, 1.1.0)", a `source:` list extended, a flag `enforced_today` set, `nullable: true` added, `deprecated` and `replaced_by` added, or a list entry added.

### Ids marked deprecated

| Old id | `replaced_by` | Files that cite the old id |
|---|---|---|
| `policy.opa.admin_any` | `policy.opa.access_matrix` | `docs/03-identity/current-role-matrix.md`, `docs/03-identity/policy-input-model.md`, `docs/03-identity/privilege-reduction-backlog.md`, `docs/03-identity/target-access-matrix.md`, `docs/06-policy/policy-catalogue.md`, `policy/opa/access.rego`, `policy/tests/access_test.rego`, `policy/tests/test_policy_python.py` |
| `policy.opa.operator_read` | `policy.opa.access_matrix` | `docs/03-identity/current-role-matrix.md`, `docs/03-identity/policy-input-model.md`, `docs/06-policy/policy-catalogue.md`, `policy/opa/access.rego` |

The old ids keep their text. The test `test_every_id_the_code_policy_and_tests_name_is_still_defined` passes, so the cited ids are still defined.

### Changed ids that code, policy, or tests cite

Command: `python C:\Users\mange\AppData\Local\Temp\s05r\cites.py`. It listed 24 changed ids cited by `apps/`, `policy/`, `tests/`, or `etl/`. Each row shows only those files. Docs that cite the id are many and are in the script output.

| Id | Files under `apps/`, `policy/`, `tests/`, `etl/` that cite it |
|---|---|
| `field.device.stale_topology_flag` | `policy/tests/fixtures/du-01-allow-prompt-allow-list-only.json` |
| `rule.ai_output_cannot_execute` | `apps/api/services/ai_gateway.py`, `apps/api/services/policy.py`, `policy/opa/access.rego`, `policy/opa/ai_action.rego`, `policy/tests/ai_action_test.rego`, `policy/tests/fixtures/ai-07-block-ai-agent-execute.json`, `tests/ai/test_guardrails.py` |
| `rule.alarm_last_seen_not_before_first_seen` | `apps/api/services/dedupe.py`, `tests/reliability/test_drills.py` |
| `rule.shared_admin_not_least_privilege` | `policy/opa/access.rego` |
| `rule.duplicate_dedupe_key_in_storm_is_one_alarm` | `apps/api/services/dedupe.py` |
| `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `apps/api/services/policy.py`, `policy/opa/access.rego`, `policy/opa/ai_action.rego`, three fixtures `ai-02`, `ai-09`, `ai-10`, `policy/tests/test_policy_python.py` |
| `rule.forbidden_fields_never_enter_prompt` | `apps/api/services/policy.py`, `policy/opa/ai_action.rego`, fixtures `ai-08` and `du-02`, `tests/ai/test_guardrails.py` |
| `rule.stale_topology_blocks_recommendation` | `apps/api/services/policy.py`, `policy/opa/ai_action.rego`, fixture `ai-06`, `tests/ai/test_guardrails.py` |
| `rule.denied_access_is_audited` | `policy/opa/access.rego` |
| `rule.no_default_role` | `policy/opa/access.rego`, `tests/access/test_negative_access.py` |
| `metric.quarantine_rate` | `etl/run_daily_batch.py`, `tests/finops/test_metrics_from_audit.py` |
| `resource.sensitive_device_fields` | `policy/opa/policy_data.json` |
| `role.admin` | `apps/api/main.py`, `apps/api/services/policy.py`, `policy/opa/access.rego`, `policy/opa/policy_data.json`, `policy/tests/access_test.rego`, `policy/tests/test_policy_python.py`, two fixtures, `tests/audit/test_audit_rebuild.py` |
| `role.operator` | `apps/api/services/policy.py`, `policy/opa/policy_data.json`, `policy/tests/access_test.rego`, `policy/tests/test_policy_python.py`, a fixture, `tests/access/test_negative_access.py`, `tests/ai/test_guardrails.py`, `tests/performance/test_engine_lookup_once.py` |
| `role.clinician` | `apps/api/services/policy.py`, `policy/opa/access.rego`, `policy/opa/policy_data.json`, `policy/tests/access_test.rego`, `policy/tests/test_policy_python.py`, a fixture, `tests/access/test_negative_access.py`, `tests/characterization/test_current_behaviour.py` |
| `policy.opa.default_deny` | `apps/api/services/policy.py`, `policy/opa/access.rego` |
| `persona.vendor_account` | `policy/opa/policy_data.json` |
| `policy.prompt_fields` | `apps/api/services/ai_gateway.py` |
| `policy.output_schema` | `apps/api/services/ai_gateway.py`, `policy/opa/ai_action.rego` |
| `provenance.policy_result` | `apps/api/services/policy.py`, `policy/opa/ai_action.rego`, fixture `ai-07`, `tests/ai/test_guardrails.py` |
| `provenance.approval_id` | `policy/opa/ai_action.rego`, `tests/access/test_negative_access.py` |
| `ai_use.incident_summary` | `policy/opa/ai_action.rego`, `policy/opa/policy_data.json`, fixture `ai-03`, `tests/ai/test_guardrails.py` |
| `field.alarm.dedupe_key`, `field.ai_invocation.guardrail_status` | docs only |
| `concept.audit_row`, `concept.policy_decision` | docs only |

The other 38 changed ids are cited only by docs or by no file outside `semantic-layer/`.

### Stale-state sentences

The stage rule names three ids. Each one was corrected and keeps its meaning.

| Id | File and line | What was stale | What is true now and which stage changed it |
|---|---|---|---|
| `role.admin` | `SL/access-semantics.yaml:252`, `:257`–`:260`; `SL/glossary.md:294` | "Before stage S04-06, the OPA file allowed admin every action." | `role.admin` has exactly one allow row, TA-35 (read of `resource.audit_log`). Stage S04-06 removed the any-admin rule. Stage S05-14 added TA-35. |
| `rule.shared_admin_not_least_privilege` | `SL/business-rules.yaml:116`–`:134`; `SL/glossary.md:183` | "access.rego allowed any admin for any action." | `access.rego` has no any-admin rule. Stages S04-06 and S05-14 made the change. The password statement is kept. |
| `policy.opa.admin_any` | `SL/access-semantics.yaml:298` | The text described a live rule. | The rule is gone. The id is `deprecated: true` and `replaced_by: policy.opa.access_matrix`. |

Command for the other cases: Grep tool for `admin|brownfield|allows any` over `semantic-layer/*.yaml` and `*.md` (case-insensitive). Result, one row per hit group:

| Hits | File and line | Decision |
|---|---|---|
| `brownfield-risk-register.md` in `source:` lists | `SL/status-taxonomy.yaml:3767`, `:3782`; `SL/entities.yaml:896`; `SL/metrics.yaml:73`; `SL/business-rules.yaml:29`, `:134`, `:203`; `SL/access-semantics.yaml:21`, `:475` | Not stale. These are the real name of an existing file. |
| `stage_note` on the shared-admin rule | `SL/business-rules.yaml:133` | Left as written. It says stages S04-03 and S04-06 "replace admin-any with per-persona rules". Stage S04-06 did that. The sentence reads as a plan and is not wrong in substance. Fix is optional. Owner Team-Force. |
| `role.admin` rows | `SL/access-semantics.yaml:252`–`:260`; `SL/glossary.md:294` | Corrected, see the table above. |
| `agency: execute` | `SL/access-semantics.yaml:60` | Not stale. It is the agency word of `action.execute`, and the text says no route does this today. |

## 5. Version and change log

**Verified Fact.** `version: "1.1.0"` is in all seven YAML files. The schema `$id` and title say 1.1.0. `generated/manifest.json` has `"version": "1.1.0"`. `SL/README.md` repeats `1.1.0`. The test `test_every_yaml_carries_version_and_readme_repeats_it` passes.

README change-log row (`SL/README.md`, Change log table): `1.1.0 | 2026-10-12 | S05R | 92 ids added, 0 removed (665 to 757) | 92 glossary rows (181 to 273) | six tests added (35 to 41)`. The row names the design stages that caused the ids: S04-03, S04-06, S04-08, S04-09, S04-10, S04-11, S04-12, S05-13, S05-14.

## 6. Diff

### Per file

| File | Ids added | Aliases added | Ids deprecated | Glossary rows added | Schema rules added | Tests added |
|---|---|---|---|---|---|---|
| `entities.yaml` | 17 (15 audit row fields, `concept.waiver`, `concept.decision_provenance`) | 1 (`policy_decision`, in the text of `field.audit_row.policy_decision`) | 0 | 17 | 0 | 0 |
| `relationships.yaml` | 0 | 0 | 0 | 0 | 0 | 0 |
| `status-taxonomy.yaml` | 49 (47 `status.code.*`, 2 collisions) | 0 | 0 | 49 | 0 | 0 |
| `business-rules.yaml` | 7 | 0 | 0 | 7 | 0 | 0 |
| `metrics.yaml` | 4 | 0 | 0 | 4 | 0 | 0 |
| `access-semantics.yaml` | 2 (`resource.model_call_queue`, `policy.opa.access_matrix`) | 0 | 2 | 2 | 0 | 0 |
| `ai-context-policy.yaml` | 13 (`policy.model_now`, 8 policy inputs, 4 failmodes) | 2 (`trace_id` in `provenance.correlation_id`; hash algorithm in `provenance.prompt_hash`) | 0 | 13 | 0 | 0 |
| `schemas/semantic-layer.schema.json` | 0 | 0 | 0 | 0 | 5 (see section 3) | 0 |
| `tests/test_semantic_layer.py` | 0 | 0 | 0 | 0 | 0 | 6 |
| `glossary.md` | 0 | 0 | 0 | 92 new rows, about 32 rows rewritten | 0 | 0 |
| **Total** | **92** | **3** | **2** | **92** | **5** | **6** |

Note on counts: the `ai-context-policy.yaml` split of 13 is `policy.model_now` (1), `field.policy_input.*` (8), and `failmode.*` (4). The script `newids.py` reports 13 ids for that file. The `entities.yaml` split of 17 is 15 `field.audit_row.*` plus 2 concepts.

### `git diff --stat -- semantic-layer/`

**Verified Fact.** Run on 2026-10-12 from `06-telecom-service-network-incident-ops`.

```text
 .../semantic-layer/README.md                       |  64 ++-
 .../semantic-layer/access-semantics.yaml           |  90 +++-
 .../semantic-layer/ai-context-policy.yaml          | 283 ++++++++--
 .../semantic-layer/business-rules.yaml             | 236 ++++++++-
 .../semantic-layer/entities.yaml                   | 217 +++++++-
 .../semantic-layer/generated/access-semantics.json |  72 ++-
 .../generated/ai-context-policy.json               | 276 ++++++++--
 .../semantic-layer/generated/business-rules.json   | 210 +++++++-
 .../semantic-layer/generated/entities.json         | 274 +++++++++-
 .../semantic-layer/generated/manifest.json         |  30 +-
 .../semantic-layer/generated/metrics.json          | 101 +++-
 .../semantic-layer/generated/relationships.json    |   2 +-
 .../semantic-layer/generated/status-taxonomy.json  | 576 ++++++++++++++++++++-
 .../semantic-layer/glossary.md                     | 179 +++++--
 .../semantic-layer/metrics.yaml                    | 117 ++++-
 .../semantic-layer/relationships.yaml              |   4 +-
 .../schemas/semantic-layer.schema.json             |  65 ++-
 .../semantic-layer/status-taxonomy.yaml            | 352 ++++++++++++-
 .../semantic-layer/tests/test_semantic_layer.py    |  81 ++-
 19 files changed, 2939 insertions(+), 290 deletions(-)
```

The tree is the capture-PDF tree plus `generated/` and `build.py`. No file was added under `semantic-layer/`.

## 7. Test edits

**Verified Fact.** `semantic-layer/tests/test_semantic_layer.py` changed in three ways.

1. `VERSION` is `"1.1.0"`.
2. The reference test `test_every_referenced_id_is_defined` skips the `value` key of a code value. A code value is the exact text the code writes, such as `policy.deny`. The text starts with the prefix `policy.` and would otherwise count as a reference to an id that does not exist.
3. Six tests were added:
   - `test_a_deprecated_item_names_a_defined_replacement`
   - `test_schema_rejects_deprecated_without_replacement`
   - `test_audit_row_fields_are_the_keys_the_code_writes`
   - `test_cannot_prove_ids_match_the_item_names_in_the_code`
   - `test_audit_action_words_in_main_py_all_have_an_id`
   - `test_every_id_the_code_policy_and_tests_name_is_still_defined`

No file under `tests/` or `policy/tests/` changed. The `ruff` run found two style findings in the new test lines on the first pass (`UP031`, `PIE810`). Both were fixed. The one remaining `ruff` finding in this file (`C401`, line 344) was in the `1.0.0` file already.

## 8. Resolutions for code and Rego comments

A code or Rego comment was read and never changed. This table records the resolution of each "Open question for S03" comment in those files.

| File and line | Question | Resolution |
|---|---|---|
| `apps/api/main.py:14` | ids for `audit.read`, `audit.not_found`, `audit.id_refused` | Row C-21. |
| `apps/api/services/audit.py:37` | id for `token_estimate_method` | Row C-29. |
| `apps/api/services/audit_query.py:19` | ids for the cannot-prove items | Row C-23. |
| `apps/api/services/ai_gateway.py:64` | status word for `guardrail_status` after the checks | Row C-34. |
| `apps/api/services/ai_gateway.py:72` | command list and failmode | Row C-32. |
| `apps/api/services/ai_gateway.py:301` | timeout | Row C-37, deferred. |
| `apps/api/services/dedupe.py:21` | rule for an event seen twice | Row C-45. |
| `apps/api/services/dedupe.py:37` | blank or unreadable timestamp | Row C-50. |
| `etl/run_daily_batch.py:9` | rule for a bad row held aside | Row C-46. |
| `policy/opa/ai_action.rego:21`, `:78`, `:156`, `:191` | `policy_version`, invalid input failmode, `change_plan_ok`, version mismatch | Rows C-09, C-14, C-11, C-17. |
| `policy/opa/access.rego:93` | `action_on_denied_list` | Row C-04. |
| `docs/12-finops/metrics_from_audit.py:316` | stored place for the quarantined count | Row C-57, deferred. |

No design file received a line "Resolved in S05R as <id>." This file holds the mapping instead. The rule allows that line. It does not require it.

## 9. Build and test output

Run on 2026-10-12 on Windows, Python 3.13.5, `opa` 1.21.1 on the PATH, from `06-telecom-service-network-incident-ops`. `PYTHONDONTWRITEBYTECODE=1` was set. **Verified Fact.**

```text
> Remove-Item -Recurse semantic-layer\generated
> python semantic-layer\build.py
Validated 7 YAML files against semantic-layer.schema.json. Version 1.1.0.
  wrote generated/entities.json
  wrote generated/relationships.json
  wrote generated/status-taxonomy.json
  wrote generated/business-rules.json
  wrote generated/metrics.json
  wrote generated/access-semantics.json
  wrote generated/ai-context-policy.json
  wrote generated/manifest.json

> python semantic-layer\build.py --check
generated/ matches the YAML. 7 files validated. Version 1.1.0.

> pytest semantic-layer/tests -q -p no:cacheprovider
.........................................                                [100%]
41 passed in 2.75s

> pytest tests policy/tests semantic-layer/tests -q -p no:cacheprovider
333 passed, 6286 warnings in 78.11s (0:01:18)

> powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1
(security stage)
195 passed, 97 deselected
security gate ok: evidence\junit-security.xml has no skipped test
```

`evidence/exit-codes.txt`: `install=0`, `lint=1`, `tests=0`, `semantic_layer=0`, `opa=0`, `policy=0`, `security=0`, `sbom=0`, `pip_audit=1`, `bandit=1`, `checksums=0`. The three non-zero values are the same real findings as at S05-14 (ruff, pip-audit, bandit). The script exits 1 for that reason, as the earlier stages' evidence says.

### Count changes against the S05-14 reference

| Count | S05-14 reference | S05R run | Why |
|---|---|---|---|
| `tests` (junit-tests.xml) | 97 | 97 | No change. |
| `semantic_layer` | 35 | 41 | Six tests were added (section 7). |
| `policy` | 87 | 87 | No change. |
| `opa test` | 32 of 32 | 32 of 32 | No change. |
| `security` | 195, 0 skipped | 195, 0 skipped | No change. |
| full run `pytest tests policy/tests semantic-layer/tests` | 327 (before this stage) | 333 | 327 plus the six new tests. |
| ruff findings | 11 | 11 | Two new findings from the first draft of the new tests were fixed. |
| bandit results | 2 LOW | 2 LOW | No change. |

After the run, `git checkout -- evidence/linux-py311` restored the Linux evidence folder that `evidence.ps1` deletes. `git checkout -- logs/audit.log` restored the audit log that test runs append to (BL-09).

## 10. S03R rerun

Paths are relative to `06-telecom-service-network-incident-ops/` unless they start with `playbook/`. Claim labels follow the header.

### Checks R1 to R13 and R15

| Check | Result | Citation | Reason |
|---|---|---|---|
| R1 | PASS | `Semantic_Layer_capture.pdf`; `SL/README.md:47`–`:48`, `:59`–`:65`; test `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` | **Verified Fact.** The folder holds `README.md`, `glossary.md`, seven YAML files, `schemas/semantic-layer.schema.json`, and `tests/test_semantic_layer.py` (the eleven capture entries), plus `build.py` and `generated/` with eight JSON files. A script listed the tree and found no other file. README line 59 and lines 61–65 say why `build.py` and `generated/` exist. |
| R2 | PASS | Tests `test_every_item_has_a_source_list_of_existing_paths` and `test_every_proposed_item_names_an_owner` | **Verified Fact.** A script walked every YAML object with an `id`. There are 757. Zero lack a `source:` list. Zero source paths are missing on disk. There are 120 items with `proposed: true`. Each has `owner: Team-Force`. Every `owner:` value in the tree is `Team-Force`. |
| R3 | PASS | `docs/02-baseline/data-quality-baseline.md` (unchanged this stage); `SL/status-taxonomy.yaml` `status.word.*` items; test `test_every_word_in_every_word_column_is_in_the_taxonomy` | **Verified Fact.** The test checks every cell of every CSV status column against the taxonomy and passes. This stage added no `status.word.*` item and removed none. The S03R round 3 cites for the baseline lines still hold, because the baseline file did not change. |
| R4 | PASS | `SL/status-taxonomy.yaml:3692`, `:3714`, `:3749`, `:3768`; `other_overlaps` at `:3783` | **Verified Fact.** The `collisions` block holds four entries: `collision.gold_bronze_as_severity`, `collision.status_words_in_hostname_and_vendor`, `collision.rec_0001_first_key_in_six_tables`, `collision.clinician_role_in_telecom_api`. Test `test_collisions_block_has_the_four_named_entries` passes. Seven overlaps sit under `other_overlaps` (`:3784`–`:3851`). Two of those are new in S05R. |
| R5 | PASS | `SL/business-rules.yaml:47`, `:81`, `:99`, `:116`, `:136`, `:153` | **Verified Fact.** The six required rules are present, each with an id. The file holds 20 rules in all. |
| R6 | PASS | `SL/access-semantics.yaml:350`, `:389`, `:419`, `:435`, `:451`, `:477`, `:497`; `removed_roles` at `:335`; `role.clinician` at `:273` | **Verified Fact.** All seven personas are present. `removed_roles` lists `role.clinician`. Tests `test_required_personas_present` and `test_api_roles_today_and_clinician_removed` pass. |
| R7 | PASS | `SL/ai-context-policy.yaml:203`–`:218` (forbidden list), `:391`–`:413` (outcomes), `:429` (fail to person), `:572`–`:687` (eleven AI uses); `docs/02-baseline/ai-qualification.md` | **Verified Fact.** `field.device.mgmt_ip` and `field.device.credential_profile` are on the forbidden list. The four outcomes are `outcome.recommend_only`, `outcome.hold_for_review`, `outcome.block`, `outcome.execute`. `policy.fail_to_person` is present. A script compared each of the eleven `ai_use.*` items at `HEAD` and now on `pick`, `agency`, `approver`, and `approval_point`. All eleven are equal. `ai-qualification.md` did not change. S03R round 3 already matched `HEAD` to that table, so the copy still matches. |
| R8 | PASS | `SL/ai-context-policy.yaml:622`, `:638`, `:651` (the three `genai` uses, agency `recommend`); `:674`–`:677` (`ai_use.remediation_execution`, pick `workflow_automation`, agency `execute`); `:413`–`:415` (`outcome.execute`); test `test_four_outcomes_present_and_model_never_executes` | **Verified Fact.** The script printed the pick and agency of each use. The three model uses have agency `recommend`. The only use with agency `execute` has pick `workflow_automation`. This stage gave `ai_use.incident_summary` a `block_conditions` entry and changed no agency. **Inference:** no AI use gained execute agency. |
| R9 | PASS | `SL/glossary.md` (273 id rows); test `test_glossary_and_yaml_agree_on_every_term` | **Verified Fact.** The glossary has 273 id rows (181 at 1.0.0 and 92 added). The test checks that every id with a glossary prefix has a row and that the Term matches the YAML name. It passes. The three sampled rows in R15 agree with the YAML. |
| R10 | PASS | `build.py --check`; `pytest semantic-layer/tests`; test `test_schema_validates_every_yaml_file` | **Verified Fact.** The schema validated all seven files. 41 of 41 tests passed. Output is in section 9. |
| R11 | PASS | Temp copy of `semantic-layer/`, then `build.py` | **Verified Fact.** A script copied the folder, deleted `generated/`, ran `build.py`, and compared SHA-256 of the eight JSON files with the real tree. Output below. |
| R12 | PASS | `SL/metrics.yaml` (every `target:` is `null`, 14 lines); `SL/ai-context-policy.yaml:438` (`timeout_seconds: null`); `SL/business-rules.yaml:268`–`:278` (the number 128); `SL/metrics.yaml:83`; `SL/entities.yaml:494` | **Verified Fact.** No metric has a target. The timeout is null. The number 128 is PROPOSED with owner Team-Force, and the text says Mangesh accepted it on 2026-10-12. The retry bound 1000 is PROPOSED with owner Team-Force, as before. The new runbook level names carry no cutoff. |
| R13 | PASS | Test `test_no_secret_value_anywhere_in_the_tree`; `SL/ai-context-policy.yaml:221` | **Verified Fact.** The test reads secret values from `.env.example` and `legacy/reconcile_legacy.py` at run time and finds none in the tree. It passes. Line 221 lists six secret names and no values. A Grep for `sk-`, `AKIA`, and `Bearer` over `semantic-layer/` and this file found no key or token value. |
| R15 | PASS | `SL/glossary.md:411`, `:30`, `:69` | **Verified Fact** for the pick: Python `random.sample` with seed `20261012` over the 273 id rows. **Inference** for the judgment: the rows are below. |

R11 hashes. First 16 hex characters. **Verified Fact.**

```text
access-semantics.json    25fa3de5ff282d81 IDENTICAL
ai-context-policy.json   8b56577a88cab14e IDENTICAL
business-rules.json      221b7d8f80c6d5c4 IDENTICAL
entities.json            521292cc6bdbbf3f IDENTICAL
manifest.json            176fcb4c846bae5c IDENTICAL
metrics.json             f01668c43382eec7 IDENTICAL
relationships.json       79de139af39a92a6 IDENTICAL
status-taxonomy.json     0e99a9b86be31a49 IDENTICAL
files 8 mismatches 0
```

The comparison ran after the last YAML edit (the `trace_id` alias in `provenance.correlation_id`).

### R15 plain speech

Seed `20261012`. Population: 273 glossary id rows.

| Term | Id | Line | Can a new reader picture it? |
|---|---|---|---|
| `approval_id` | `field.audit_row.approval_id` | 411 | Yes. The row says it is the stored approval id, and that it is null on every row because no route writes one. The reader pictures an empty column. The term "approval" is defined in a separate row. |
| `service_order` | `entity.service_order` | 30 | Yes. The row says it is a customer request to set up or change a service, and that one row exists per order in `service_orders.csv`. |
| `high` | `status.word.high` | 69 | Partly. The row says it is a severity word and that where it ranks is Unknown. A reader sees a label with no order. That is the true state of the repo. The row does not say that this is a severity on alarms and incidents. Row `status.word.gold` and the collision text explain the two scales. This is not a FAIL, because the row names the fact and the open question. |

### R14 failure list from `playbook/README.md`

| Row | Result | Citation | Reason |
|---|---|---|---|
| R14.1 Code written before its analysis gate | PASS | `git status --short -- apps policy tests etl data legacy scripts docs security .github` | **Verified Fact.** The command printed nothing for those paths before this file was written, so S05R changed no code. The only changes in the repo are under `semantic-layer/`, the evidence files that `evidence.ps1` rewrites, and the transcript. |
| R14.2 Design decided before the S2Q table | PASS | `SL/ai-context-policy.yaml:572`–`:687`; `docs/02-baseline/ai-qualification.md` | **Verified Fact.** The eleven AI uses are unchanged against `HEAD`. This stage added no AI use. |
| R14.3 AI chosen with no stated need | PASS | `SL/ai-context-policy.yaml:622`, `:638`, `:651` | **Verified Fact.** Three uses have pick `genai`, and the pick fields are unchanged. No AI use was added. |
| R14.4 Claim with no label, or a Verified Fact with no pointer | PASS | This file; `SL/README.md` "Last build" | **Verified Fact.** Each added item cites source files. This file labels each claim. The README block is marked Verified Fact and names the run. |
| R14.5 Artifact missing or at the wrong path | PASS | `semantic-layer/`; `docs/02-baseline/semantic-layer-revision.md` | **Verified Fact.** Both required artifacts exist at the paths the stage names. |
| R14.6 Completion gate skipped or not stated | PASS | Header Status of this file; `SL/README.md:8` | **Verified Fact.** Both state the gate result and why. |
| R14.7 Number invented without PROPOSED and an owner | PASS | `SL/business-rules.yaml:268`–`:278`; `SL/metrics.yaml` targets; `SL/ai-context-policy.yaml:438` | **Verified Fact.** The only new number is 128. It comes from `apps/api/services/audit_query.py` (`MAX_ID_LENGTH`), is PROPOSED with owner Team-Force, and was accepted by Mangesh on 2026-10-12. |
| R14.8 Term used with a meaning not in the YAML | PASS | Tests `test_every_agency_and_pick_word_is_defined`, `test_every_referenced_id_is_defined`, `test_every_id_the_code_policy_and_tests_name_is_still_defined` | **Verified Fact.** All three pass. Each term in the collection table that this stage accepted has an id and a glossary row. |

## 11. Gate result

**CONDITIONAL PASS.**

- Every collection row has a decision and a reason. Defer rows name an owner.
- Every add and alias is in the YAML with a `source:` list and a glossary row.
- Build, `--check`, semantic-layer tests (41), the full run (333), and the security stage (195, 0 skipped) pass.
- Stale-state sentences are corrected or listed (section 4).
- Every S03R row passes. R12 and R15 pass.
- No cited id lost its definition. The new version is in every file.
- Why not a plain PASS: the stage rule gives CONDITIONAL PASS when a deferred row names an owner. Twenty rows are deferred.

### Fixes required

None. No row is FAIL. There is no choice for an owner to make for the gate. The following are choices the owner may make later, and none blocks S06:

| Choice | Files | Options |
|---|---|---|
| Release check ids (D-01) | `SL/business-rules.yaml` | A. Add ids when the production-readiness policy is written. B. Leave until S09. |
| Model timeout number (D-11) | `SL/ai-context-policy.yaml:438`, `tests/ai/test_guardrails.py` | A. Team-Force states the number, and the test changes under an ADR. B. Keep `null`. |
| Audit row gaps (D-05, D-06, D-07, D-18) | `apps/api/services/audit.py`, `SL/entities.yaml` | A. Add the keys to the audit row first, then add field ids. B. Leave them out of the audit row. |

## 12. Residual risks and next step

- **Verified Fact.** The audit row still lacks `record_id`, a named caller, and a final action. A reviewer cannot answer those defence questions from the row alone. `status.code.cannot_prove.*` names them.
- **Verified Fact.** Two rules (`rule.repeat_event_is_one_event`, `rule.order_attempt_same_retry_is_one_attempt`) have `enforced_today: false`, because no route calls `dedupe.py`.
- **Inference.** Six `enforced_today` flags changed from false to true. A reader who knew only `1.0.0` could read this as a change of rule. Each rule now says which code runs it.
- **Unknown.** Whether Team-Force accepts the PROPOSED items. They carry `owner: Team-Force` until it does.
- A change to the YAML after this stage needs an ADR under `docs/ADR/`.
- Next: S06 writes `1.1.1` into the PRD header. S08 hashes the tree at `1.1.1` for the second model.
