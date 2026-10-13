# Traceability: requirement to YAML id to test to design

| Field | Value |
|---|---|
| Stage | S06. Product requirements document (D5). This file maps each requirement in `docs/prd/prd.md` to its YAML ids, its acceptance test and its Phase 4 design file. |
| Date / version | 2026-10-13, v1.9. S07 updated the test status of the 43 planned tests and the semantic layer version (1.2.0). No requirement text changed. v1.8: S06R fixes applied, round 7. Round 7 closes X-3, X-4 and X-7 of review v5.0. Round 6 closed R6-1 (RQ-31, the answer store, is deferred under ADR 0004). Round 5 closed F-1 (the PRD gives no word a meaning of its own where the call has no failure) and the other findings X-1 to X-7 of review v4.0. X-8 is left as it is. Round 4 closed R4-1 and R4-2. Round 3 closed R3-1 to R3-9. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | CONDITIONAL PASS. S07 wrote the 43 planned tests and all 43 pass (2026-10-13, `docs/demo/evidence.md`). S06R fixes applied, round 7. 73 of 73 requirements have a YAML id and a named test. 43 tests were planned for stage S07. 1 test (RQ-31) is deferred (ADR 0004). Round 3 closed R3-1 to R3-9. Round 4 closed R4-1 and R4-2. Round 5 closed F-1 and X-1 to X-7. Round 6 closed R6-1. Round 7 closed X-3, X-4 and X-7. |
| Evidence sources | **Semantic layer version `1.2.0`** (raised from `1.1.1` by S07, `docs/ADR/0005-s07-yaml-additions.md`) (`semantic-layer/README.md`, the same number as in `docs/02-baseline/semantic-layer-revision.md` and ADR 0002). `docs/prd/prd.md` (the requirement table this file is built from). `docs/ADR/0003-s06-risk-recommendations.md`. The seven YAML files in `semantic-layer/`. The test files named in the table. The Phase 4 and Phase 5 design files named in the table. |
| Assumptions | (1) A test marked "planned S07" uses the name written here. S07 updates this file before it renames one. A test marked "deferred" belongs to a requirement that S07 does not build (RQ-31, ADR 0004). Its name stays. (2) "Existing" means the test is in the repo and was run on 2026-10-12. |
| Unresolved issues | Thirteen Open questions for S03: see `docs/prd/prd.md` section 15. |
| Residual risks | The test for RQ-59 skips when `opa` is missing. A planned test is not evidence until it exists and passes. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Requirement to YAML id to test to design

| Requirement | YAML ids | Acceptance test | Status | Also covered by (existing tests) | Phase 4 design file |
|---|---|---|---|---|---|
| RQ-01 | `status.code.health.ok`; `metric.api_availability` | `tests/test_api_contract.py::test_health_contract` | existing | `tests/reliability/test_drills.py::test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up` | `docs/11-reliability/degraded-mode-design.md` |
| RQ-02 | `rule.record_lookup_matches_key_only`; `field.device.device_id`; `ai_use.topology_lookup` | `tests/performance/test_load_once.py::test_only_device_id_is_matched` | existing | `tests/performance/test_load_once.py::test_every_device_id_in_the_real_file_finds_its_first_row` | `docs/10-performance/scaling-recommendations.md` |
| RQ-03 | `rule.missing_id_not_other_device`; `status.code.error.not_found`; `ai_use.topology_lookup` | `tests/app/test_records_route.py::test_missing_id_returns_404_and_no_row` | passed in S07 (2026-10-13) | none | `docs/13-security-validation/remediation-backlog.md` |
| RQ-04 | `role.clinician`; `collision.clinician_role_in_telecom_api`; `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny`; `status.code.error.forbidden` | `tests/access/test_negative_access.py::test_clinician_role_is_denied_on_record_read` | existing | `policy/tests/test_policy_python.py::test_record_route_denies_with_403_and_audit_row` | `docs/03-identity/target-access-matrix.md` |
| RQ-05 | `resource.sensitive_device_fields`; `field.device.mgmt_ip`; `field.device.credential_profile`; `persona.noc_operator` | `tests/app/test_records_route.py::test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile` | passed in S07 (2026-10-13) | none | `docs/04-secrets/sensitive-field-handling-checklist.md` |
| RQ-06 | `resource.sensitive_device_fields`; `persona.network_engineer`; `purpose.network_change_planning` | `tests/app/test_records_route.py::test_network_engineer_read_returns_mgmt_ip_and_credential_profile` | passed in S07 (2026-10-13) | none | `docs/03-identity/target-access-matrix.md` |
| RQ-07 | `status.code.audit_action.record_read`; `concept.audit_row` | `policy/tests/test_policy_python.py::test_record_route_allows_operator_and_writes_read_row` | existing | none | `docs/08-observability/log-schema.md` |
| RQ-08 | `ai_use.alarm_dedupe`; `metric.alarm_storm_size`; `rule.duplicate_dedupe_key_in_storm_is_one_alarm`; `field.alarm.storm_batch_id`; `field.alarm.dedupe_key`; `status.code.dedupe_result.held_aside` | `tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids` | passed in S07 (2026-10-13) | `tests/reliability/test_drills.py::test_dr3_a_blank_key_part_is_held_aside_and_never_recorded`<br>`tests/reliability/test_drills.py::test_dr3_same_dedupe_key_in_another_storm_is_a_different_alarm` | `docs/11-reliability/idempotency-plan.md` |
| RQ-09 | `rule.alarm_last_seen_not_before_first_seen`; `status.code.alarm_flag.last_seen_before_first_seen`; `status.code.alarm_flag.times_unreadable`; `ai_use.alarm_to_incident_correlation` | `tests/app/test_storm_route.py::test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` | passed in S07 (2026-10-13) | `tests/reliability/test_drills.py::test_dr6_ala_00002_is_flagged_and_does_not_become_an_incident` | `docs/11-reliability/idempotency-plan.md` |
| RQ-10 | `resource.alarm`; `field.alarm.storm_batch_id`; `status.code.error.not_found` | `tests/app/test_storm_route.py::test_unknown_storm_returns_404` | passed in S07 (2026-10-13) | none | `docs/11-reliability/idempotency-plan.md` |
| RQ-11 | `resource.alarm`; `persona.noc_operator`; `persona.network_engineer`; `rule.no_default_role`; `rule.denied_access_is_audited`; `status.code.role_header.absent` | `tests/app/test_storm_route.py::test_roles_without_an_alarm_read_row_get_403` | passed in S07 (2026-10-13) | none | `docs/03-identity/target-access-matrix.md` |
| RQ-12 | `ai_use.alarm_dedupe`; `ai_use.alarm_to_incident_correlation`; `action.read`; `risk.read_only` | `tests/app/test_storm_route.py::test_storm_read_leaves_alarms_csv_unchanged` | passed in S07 (2026-10-13) | none | `docs/11-reliability/idempotency-plan.md` |
| RQ-13 | `metric.alarm_storm_size`; `ai_use.alarm_dedupe` | `tests/app/test_storm_route.py::test_storm_response_has_no_size_flag` | passed in S07 (2026-10-13) | none | `docs/11-reliability/idempotency-plan.md` |
| RQ-14 | `status.code.fault.data_file_missing`; `resource.alarm`; `metric.api_availability` | `tests/app/test_storm_route.py::test_missing_alarms_file_returns_500_and_health_stays_200` | passed in S07 (2026-10-13) | none | `docs/11-reliability/degraded-mode-design.md` |
| RQ-15 | `concept.audit_row`; `rule.audit_row_names_actor_and_correlation`; `resource.alarm` | `tests/app/test_storm_route.py::test_storm_read_writes_one_audit_row` | passed in S07 (2026-10-13) | none | `docs/08-observability/log-schema.md` |
| RQ-16 | `ai_use.incident_summary`; `outcome.recommend_only`; `status.code.guardrail_status.enforced`; `policy.model_now` | `tests/ai/test_guardrails.py::test_gr10_success_body_has_the_policy_outcome_and_no_not_enforced` | existing | `tests/ai/test_guardrails.py::test_gr10_every_path_has_a_policy_outcome_and_only_success_has_text`<br>`policy/tests/test_policy_python.py::test_summarize_is_recommend_only` | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-17 | `rule.no_default_role`; `status.code.role_header.absent`; `action.summarize` | `tests/characterization/test_current_behaviour.py::test_ai_summarize_refuses_request_with_no_role_header` | existing | `tests/ai/test_guardrails.py::test_gr06_denied_caller_gets_403_and_the_model_is_not_called` | `docs/03-identity/target-access-matrix.md` |
| RQ-18 | `ai_use.next_action_recommendation`; `outcome.hold_for_review`; `action.recommend`; `status.code.recommendation.review_and_approve_before_action`; `policy.output_schema` | `tests/app/test_recommend_route.py::test_healthy_recommend_is_hold_for_review_with_the_sentence` | passed in S07 (2026-10-13) | `policy/tests/test_policy_python.py::test_recommend_is_held_for_review` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-19 | `rule.ai_output_cannot_execute`; `outcome.execute`; `outcome.block` | `tests/app/test_recommend_route.py::test_recommend_never_returns_execute` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr07_response_type_and_routes_cannot_express_execute`<br>`policy/tests/test_policy_python.py::test_the_model_cannot_set_its_own_outcome` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-20 | `failmode.missing_id`; `rule.missing_id_not_other_device`; `field.policy_input.record_found` | `tests/app/test_recommend_route.py::test_missing_id_is_blocked_and_the_model_is_not_called` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr09_missing_id_is_blocked_and_is_not_a_summary_of_the_first_row` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-21 | `failmode.stale_topology_true`; `rule.stale_topology_blocks_recommendation`; `field.device.stale_topology_flag` | `tests/app/test_recommend_route.py::test_stale_true_is_blocked_and_the_model_is_not_called` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr03_stale_flag_true_is_blocked_before_the_model` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-22 | `failmode.stale_topology_blank`; `field.device.stale_topology_flag`; `outcome.hold_for_review` | `tests/app/test_recommend_route.py::test_blank_stale_flag_is_held_and_the_model_is_not_called` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr08_blank_or_missing_stale_flag_is_held_before_the_model` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-23 | `failmode.timeout`; `policy.fail_to_person`; `status.code.audit_action.policy_hold` | `tests/app/test_recommend_route.py::test_timeout_returns_hold_for_review_with_no_summary` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr05_timeout_is_held_with_no_summary` | `docs/11-reliability/degraded-mode-design.md` |
| RQ-24 | `failmode.model_unreachable`; `status.code.breaker_state.open`; `policy.fail_to_person` | `tests/app/test_recommend_route.py::test_model_error_and_open_breaker_return_hold_for_review` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr04_a_model_that_raises_is_held` | `docs/11-reliability/retry-and-circuit-breaker-strategy.md` |
| RQ-25 | `failmode.schema_failure`; `policy.output_schema`; `field.policy_input.output_schema_ok` | `tests/app/test_recommend_route.py::test_schema_failure_returns_hold_for_review_with_no_text` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr04_malformed_model_output_is_held_with_no_summary` | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-26 | `policy.prompt_fields`; `failmode.forbidden_field_in_prompt`; `rule.forbidden_fields_never_enter_prompt` | `tests/app/test_recommend_route.py::test_forbidden_value_in_prompt_is_blocked_and_not_logged` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr02_every_device_row_builds_a_clean_prompt`<br>`tests/ai/test_guardrails.py::test_gr02_a_builder_that_adds_a_forbidden_value_is_blocked` | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-27 | `policy.provenance`; `provenance.model`; `provenance.model_version`; `provenance.prompt_hash`; `provenance.tokens`; `provenance.latency_ms`; `provenance.correlation_id` | `tests/ai/test_guardrails.py::test_gr11_audit_row_has_provenance_and_no_prompt_text` | existing | `tests/ai/test_guardrails.py::test_gr11_same_prompt_gives_the_same_hash` | `docs/09-ai-guardrails/model-provenance-design.md` |
| RQ-28 | `action.recommend`; `persona.noc_operator`; `persona.network_engineer`; `persona.ai_agent`; `persona.customer_support`; `rule.no_default_role` | `tests/app/test_recommend_route.py::test_roles_without_a_recommend_row_get_403` | passed in S07 (2026-10-13) | `tests/access/test_negative_access.py::test_ai_agent_may_recommend`<br>`tests/ai/test_guardrails.py::test_gr06_caller_without_recommend_permission_is_blocked` | `docs/03-identity/target-access-matrix.md` |
| RQ-29 | `field.policy_input.audit_row_written`; `field.policy_input.change_plan_ok`; `provenance.approval_id`; `collision.approval_required_column_and_policy_input` | `tests/security/test_client_flags_ignored.py::test_client_sent_policy_fields_change_nothing` | existing | none | `docs/06-policy/ai-action-policy-design.md` |
| RQ-30 | `failmode.command_text_in_recommendation`; `rule.ai_output_cannot_execute`; `outcome.hold_for_review` | `tests/app/test_command_phrases.py::test_each_listed_phrase_is_held_with_no_text` | passed in S07 (2026-10-13) | `tests/ai/test_guardrails.py::test_gr01_a_model_that_obeys_the_injection_is_held` | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-31 | `metric.tokens_per_invocation`; `metric.repeated_prompt_share`; `field.audit_row.prompt_hash`; `failmode.stale_topology_true`; `failmode.stale_topology_blank` | `tests/app/test_recommend_cache.py::test_second_identical_request_within_300_seconds_makes_no_model_call` | deferred (ADR 0004) | `tests/finops/test_metrics_from_audit.py::test_repeat_prompt_calls_are_counted_from_prompt_hash` | `docs/12-finops/optimization-backlog.md` |
| RQ-32 | `concept.approval`; `action.approve`; `resource.ai_invocation`; `provenance.approval_id`; `persona.noc_operator` | `tests/app/test_approvals_route.py::test_yes_is_stored_with_decision_approver_and_a_server_made_id` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/approval-workflow.md` |
| RQ-33 | `provenance.approval_id`; `outcome.execute`; `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `tests/app/test_approvals_route.py::test_a_no_never_unlocks_the_approval_check` | passed in S07 (2026-10-13) | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-34 | `concept.approval`; `provenance.correlation_id`; `status.code.error.not_found` | `tests/app/test_approvals_route.py::test_decision_without_a_shown_recommendation_returns_404` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/approval-workflow.md` |
| RQ-35 | `action.approve`; `persona.ai_agent`; `persona.automation_service`; `rule.denied_access_is_audited`; `status.code.audit_action.policy_deny`; `rule.no_default_role`; `status.code.role_header.absent` | `tests/app/test_approvals_route.py::test_other_roles_get_403_and_a_deny_row` | passed in S07 (2026-10-13) | none | `docs/03-identity/target-access-matrix.md` |
| RQ-36 | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `field.policy_input.audit_row_written`; `concept.audit_row` | `tests/app/test_audit_before_state_change.py::test_audit_row_exists_when_the_approval_write_fails` | passed in S07 (2026-10-13) | none | `docs/11-reliability/degraded-mode-design.md` |
| RQ-37 | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `status.code.fault.audit_log_unwritable` | `tests/app/test_audit_before_state_change.py::test_no_approval_is_stored_when_the_audit_row_cannot_be_written` | passed in S07 (2026-10-13) | none | `docs/11-reliability/degraded-mode-design.md` |
| RQ-38 | `provenance.approval_id`; `field.audit_row.approval_id`; `collision.approval_required_column_and_policy_input` | `tests/security/test_client_flags_ignored.py::test_no_route_reads_an_approval_id_from_the_caller` | existing | none | `docs/06-policy/ai-action-policy-design.md` |
| RQ-39 | `rule.ai_output_cannot_execute`; `risk.decision`; `action.approve` | `tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/approval-workflow.md` |
| RQ-40 | `status.code.cannot_prove.final_action`; `concept.decision_provenance`; `concept.audit_row` | `tests/app/test_audit_row_keys.py::test_every_row_has_final_action_none` | passed in S07 (2026-10-13) | none | `docs/14-audit/decision-provenance-model.md` |
| RQ-41 | `concept.audit_row`; `metric.audit_completeness`; `status.code.cannot_prove.record_asked_for` | `tests/app/test_audit_row_keys.py::test_every_row_has_record_id_as_the_16th_key` | passed in S07 (2026-10-13) | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | `docs/14-audit/decision-provenance-model.md` |
| RQ-42 | `concept.audit_row`; `concept.decision_provenance`; `status.code.audit_action.audit_read` | `tests/audit/test_audit_rebuild.py::test_the_chain_comes_back_in_time_order` | existing | `tests/audit/test_audit_rebuild.py::test_two_cases_do_not_mix` | `docs/14-audit/decision-provenance-model.md` |
| RQ-43 | `resource.audit_log`; `purpose.audit_review`; `role.admin`; `rule.denied_access_is_audited` | `tests/audit/test_audit_rebuild.py::test_a_caller_without_permission_gets_403_and_a_policy_deny_row` | existing | `tests/audit/test_audit_rebuild.py::test_the_403_is_the_same_for_an_id_that_exists_and_one_that_does_not`<br>`policy/tests/test_policy_python.py::test_audit_read_is_allowed_for_admin_only` | `docs/14-audit/audit-read-access-design.md` |
| RQ-44 | `rule.audit_case_id_limit`; `status.code.audit_action.audit_id_refused`; `status.code.error.id_too_long` | `tests/audit/test_audit_rebuild.py::test_an_id_of_129_characters_is_refused_and_not_looked_up` | existing | `tests/audit/test_audit_rebuild.py::test_an_id_of_exactly_128_characters_is_looked_up` | `docs/14-audit/audit-read-access-design.md` |
| RQ-45 | `status.code.audit_action.audit_not_found`; `status.code.error.not_found` | `tests/audit/test_audit_rebuild.py::test_an_unknown_id_gives_404_and_writes_its_own_row` | existing | none | `docs/14-audit/audit-read-access-design.md` |
| RQ-46 | `rule.audit_log_holds_no_forbidden_field`; `policy.prompt_fields` | `tests/audit/test_audit_rebuild.py::test_the_response_holds_no_forbidden_field_or_credential_name` | existing | `tests/audit/test_audit_rebuild.py::test_a_forbidden_name_stored_in_a_row_is_replaced_in_the_response_only` | `docs/14-audit/audit-read-access-design.md` |
| RQ-47 | `status.code.cannot_prove.caller_identity`; `status.code.cannot_prove.approval_id`; `status.code.cannot_prove.log_integrity` | `tests/audit/test_audit_rebuild.py::test_cannot_prove_names_approval_id_and_log_integrity` | existing | `tests/audit/test_audit_rebuild.py::test_cannot_prove_lists_approval_id_when_a_row_holds_an_approval` | `docs/14-audit/decision-provenance-model.md` |
| RQ-48 | `provenance.correlation_id`; `field.audit_row.correlation_id`; `rule.audit_row_names_actor_and_correlation` | `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` | passed in S07 (2026-10-13) | none | `docs/14-audit/decision-provenance-model.md` |
| RQ-49 | `provenance.correlation_id`; `field.audit_row.correlation_id` | `tests/observability/test_audit_schema.py::test_request_with_header_keeps_the_id` | existing | `tests/observability/test_audit_schema.py::test_request_without_header_gets_a_uuid` | `docs/08-observability/log-schema.md` |
| RQ-50 | `concept.audit_row`; `metric.audit_completeness` | `tests/observability/test_audit_schema.py::test_every_audit_row_has_every_required_field` | existing | none | `docs/08-observability/log-schema.md` |
| RQ-51 | `rule.audit_log_holds_no_forbidden_field`; `policy.prompt_fields` | `tests/security/test_audit_log_security.py::test_real_audit_log_holds_no_forbidden_name` | existing | none | `docs/08-observability/log-schema.md` |
| RQ-52 | `status.code.audit_action.record_read`; `status.code.audit_action.ai_summary`; `status.code.audit_action.policy_hold`; `status.code.audit_action.audit_read` | `semantic-layer/tests/test_semantic_layer.py::test_audit_action_words_in_main_py_all_have_an_id` | existing | `semantic-layer/tests/test_semantic_layer.py::test_audit_row_fields_are_the_keys_the_code_writes` | `docs/08-observability/log-schema.md` |
| RQ-53 | `policy.fail_to_person`; `failmode.timeout`; `metric.api_availability` | `tests/reliability/test_drills.py::test_dr2_ai_timeout_holds_the_case_with_no_summary_and_health_stays_up` | existing | `tests/reliability/test_drills.py::test_dr2_a_model_error_is_held_and_health_stays_up` | `docs/11-reliability/degraded-mode-design.md` |
| RQ-54 | `failmode.model_unreachable`; `status.code.breaker_state.open`; `failmode.timeout`; `failmode.schema_failure` | `tests/reliability/test_breaker.py::test_route_the_model_is_not_called_once_the_breaker_is_open` | existing | `tests/reliability/test_breaker.py::test_route_a_test_call_after_the_open_time_closes_the_breaker` | `docs/11-reliability/retry-and-circuit-breaker-strategy.md` |
| RQ-55 | `status.code.fault.policy_engine_failed`; `policy.opa.default_deny`; `concept.policy_decision` | `policy/tests/test_policy_python.py::test_engine_failure_denies` | existing | none | `docs/11-reliability/degraded-mode-design.md` |
| RQ-56 | `status.code.fault.audit_log_unwritable`; `concept.audit_row` | `tests/app/test_audit_before_state_change.py::test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written` | passed in S07 (2026-10-13) | none | `docs/11-reliability/degraded-mode-design.md` |
| RQ-57 | `outcome.execute`; `rule.ai_output_cannot_execute`; `agency.execute` | `policy/tests/test_policy_python.py::test_no_route_can_execute` | existing | `tests/ai/test_guardrails.py::test_gr07_route_returns_block_if_the_policy_ever_said_execute` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-58 | `outcome.execute`; `provenance.approval_id`; `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `policy/tests/test_policy_python.py::test_execute_is_unreachable_without_an_approval_id` | existing | `policy/tests/test_policy_python.py::test_one_missing_check_stops_execute_each_time` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-59 | `rule.policy_copies_agree`; `policy.opa.access_matrix` | `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_every_ai_action_combination` | existing. Skips when `opa` is missing. | `policy/tests/test_policy_python.py::test_opa_and_python_agree_on_access` | `docs/06-policy/ai-action-policy-design.md` |
| RQ-60 | `rule.no_secret_value_committed` | `tests/security/test_docs_secret_scan.py::test_docs_have_no_real_secret_formats` | existing | none | `docs/04-secrets/sensitive-field-handling-checklist.md` |
| RQ-61 | `rule.no_secret_value_committed` | `semantic-layer/tests/test_semantic_layer.py::test_no_secret_value_anywhere_in_the_tree` | existing | none | `docs/04-secrets/sensitive-field-handling-checklist.md` |
| RQ-62 | `concept.flow_topology_lookup_to_ai_recommendation`; `concept.flow_alarm_storm_to_incident_correlation` | `tests/app/test_page.py::test_page_serves_and_names_every_demo_step` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/approval-workflow.md` |
| RQ-63 | `metric.alarm_storm_size`; `metric.tokens_per_invocation`; `metric.recommendation_latency`; `status.code.token_estimate_method.word_count_x2_educational`; `metric.ai_outcome_count`; `metric.audit_completeness`; `metric.repeated_prompt_share`; `metric.api_availability` | `tests/app/test_page.py::test_every_number_on_the_page_has_a_label` | passed in S07 (2026-10-13) | `tests/finops/test_metrics_from_audit.py::test_every_printed_metric_line_has_a_label` | `docs/08-observability/metric-catalogue.md` |
| RQ-64 | `policy.fail_to_person`; `outcome.hold_for_review`; `outcome.block` | `tests/app/test_page.py::test_held_case_shows_the_reason_and_no_text` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-65 | `status.code.cannot_prove.caller_identity`; `rule.shared_admin_not_least_privilege` | `tests/app/test_page.py::test_page_shows_the_cannot_prove_list_and_the_role_it_sent` | passed in S07 (2026-10-13) | none | `docs/14-audit/decision-provenance-model.md` |
| RQ-66 | `metric.api_availability`; `metric.recommendation_latency`; `metric.audit_completeness` | `semantic-layer/tests/test_semantic_layer.py::test_no_metric_has_a_target_value` | existing | none | `docs/08-observability/slo-proposal.md` |
| RQ-67 | `metric.recommendation_latency` | `tests/finops/test_metrics_from_audit.py::test_latency_percentiles_and_outcome_split` | existing | none | `docs/08-observability/slo-proposal.md` |
| RQ-68 | `rule.no_default_role`; `status.code.role_header.absent`; `status.code.audit_action.policy_deny`; `status.code.error.forbidden` | `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` | passed in S07 (2026-10-13) | none | `docs/13-security-validation/remediation-backlog.md` |
| RQ-69 | `rule.audit_case_id_limit`; `status.code.role_header.absent`; `status.code.error.id_too_long` | `tests/app/test_audit_row_keys.py::test_unknown_role_word_is_not_stored_as_sent` | passed in S07 (2026-10-13) | none | `docs/13-security-validation/remediation-backlog.md` |
| RQ-70 | `failmode.forbidden_field_in_prompt`; `rule.forbidden_fields_never_enter_prompt`; `outcome.hold_for_review` | `tests/app/test_recommend_route.py::test_forbidden_value_in_the_answer_is_held_with_no_text` | passed in S07 (2026-10-13) | none | `docs/13-security-validation/remediation-backlog.md` |
| RQ-71 | `failmode.command_text_in_recommendation`; `rule.ai_output_cannot_execute`; `outcome.hold_for_review` | `tests/app/test_command_phrases.py::test_a_near_miss_phrase_is_held` | passed in S07 (2026-10-13) | none | `docs/09-ai-guardrails/unsafe-output-handling-rules.md` |
| RQ-72 | `status.code.cannot_prove.log_integrity`; `concept.audit_row` | `tests/app/test_audit_row_keys.py::test_app_tests_do_not_write_to_the_real_audit_log` | passed in S07 (2026-10-13) | none | `docs/14-audit/decision-provenance-model.md` |
| RQ-73 | `status.code.runbook_level.degraded`; `status.code.fault.data_file_missing`; `status.code.fault.audit_log_unwritable`; `metric.api_availability` | `tests/app/test_readiness_route.py::test_readiness_returns_503_when_devices_csv_is_missing` | passed in S07 (2026-10-13) | none | `docs/11-reliability/degraded-mode-design.md` |

**Tests S07 must change (O-4).** Four existing tests lock the behaviour that RQ-03 and RQ-68 remove. They are not acceptance tests for those rows. S07 changes them when it writes the planned tests. **Verified Fact** (function names found in the named files): `tests/characterization/test_current_behaviour.py::test_missing_id_returns_first_row`; `tests/performance/test_load_once.py::test_missing_id_still_returns_the_first_row`; `tests/access/test_negative_access.py::test_missing_role_header_keeps_operator_default`; `policy/tests/test_policy_python.py::test_record_route_keeps_missing_header_default_operator`.

## 2. Planned tests, grouped by the file S07 writes

Stage S07 writes these files under `tests/app/`. Each test turns one row of section 1 from planned to existing.

| File | Test | Requirement |
|---|---|---|
| `tests/app/test_records_route.py` | `test_missing_id_returns_404_and_no_row` | RQ-03 |
| `tests/app/test_records_route.py` | `test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile` | RQ-05 |
| `tests/app/test_records_route.py` | `test_network_engineer_read_returns_mgmt_ip_and_credential_profile` | RQ-06 |
| `tests/app/test_storm_route.py` | `test_storm_returns_raw_count_deduped_count_and_alarm_ids` | RQ-08 |
| `tests/app/test_storm_route.py` | `test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` | RQ-09 |
| `tests/app/test_storm_route.py` | `test_unknown_storm_returns_404` | RQ-10 |
| `tests/app/test_storm_route.py` | `test_roles_without_an_alarm_read_row_get_403` | RQ-11 |
| `tests/app/test_storm_route.py` | `test_storm_read_leaves_alarms_csv_unchanged` | RQ-12 |
| `tests/app/test_storm_route.py` | `test_storm_response_has_no_size_flag` | RQ-13 |
| `tests/app/test_storm_route.py` | `test_missing_alarms_file_returns_500_and_health_stays_200` | RQ-14 |
| `tests/app/test_storm_route.py` | `test_storm_read_writes_one_audit_row` | RQ-15 |
| `tests/app/test_recommend_route.py` | `test_healthy_recommend_is_hold_for_review_with_the_sentence` | RQ-18 |
| `tests/app/test_recommend_route.py` | `test_recommend_never_returns_execute` | RQ-19 |
| `tests/app/test_recommend_route.py` | `test_missing_id_is_blocked_and_the_model_is_not_called` | RQ-20 |
| `tests/app/test_recommend_route.py` | `test_stale_true_is_blocked_and_the_model_is_not_called` | RQ-21 |
| `tests/app/test_recommend_route.py` | `test_blank_stale_flag_is_held_and_the_model_is_not_called` | RQ-22 |
| `tests/app/test_recommend_route.py` | `test_timeout_returns_hold_for_review_with_no_summary` | RQ-23 |
| `tests/app/test_recommend_route.py` | `test_model_error_and_open_breaker_return_hold_for_review` | RQ-24 |
| `tests/app/test_recommend_route.py` | `test_schema_failure_returns_hold_for_review_with_no_text` | RQ-25 |
| `tests/app/test_recommend_route.py` | `test_forbidden_value_in_prompt_is_blocked_and_not_logged` | RQ-26 |
| `tests/app/test_recommend_route.py` | `test_roles_without_a_recommend_row_get_403` | RQ-28 |
| `tests/app/test_command_phrases.py` | `test_each_listed_phrase_is_held_with_no_text` | RQ-30 |
| `tests/app/test_approvals_route.py` | `test_yes_is_stored_with_decision_approver_and_a_server_made_id` | RQ-32 |
| `tests/app/test_approvals_route.py` | `test_a_no_never_unlocks_the_approval_check` | RQ-33 |
| `tests/app/test_approvals_route.py` | `test_decision_without_a_shown_recommendation_returns_404` | RQ-34 |
| `tests/app/test_approvals_route.py` | `test_other_roles_get_403_and_a_deny_row` | RQ-35 |
| `tests/app/test_audit_before_state_change.py` | `test_audit_row_exists_when_the_approval_write_fails` | RQ-36 |
| `tests/app/test_audit_before_state_change.py` | `test_no_approval_is_stored_when_the_audit_row_cannot_be_written` | RQ-37 |
| `tests/app/test_approvals_route.py` | `test_an_approval_leaves_every_data_file_unchanged` | RQ-39 |
| `tests/app/test_audit_row_keys.py` | `test_every_row_has_final_action_none` | RQ-40 |
| `tests/app/test_audit_row_keys.py` | `test_every_row_has_record_id_as_the_16th_key` | RQ-41 |
| `tests/app/test_demo_flow.py` | `test_one_case_rebuilds_from_one_correlation_id` | RQ-48 |
| `tests/app/test_audit_before_state_change.py` | `test_read_routes_return_500_with_no_data_when_the_audit_row_cannot_be_written` | RQ-56 |
| `tests/app/test_page.py` | `test_page_serves_and_names_every_demo_step` | RQ-62 |
| `tests/app/test_page.py` | `test_every_number_on_the_page_has_a_label` | RQ-63 |
| `tests/app/test_page.py` | `test_held_case_shows_the_reason_and_no_text` | RQ-64 |
| `tests/app/test_page.py` | `test_page_shows_the_cannot_prove_list_and_the_role_it_sent` | RQ-65 |
| `tests/app/test_records_route.py` | `test_missing_header_returns_403_and_a_deny_row` | RQ-68 |
| `tests/app/test_audit_row_keys.py` | `test_unknown_role_word_is_not_stored_as_sent` | RQ-69 |
| `tests/app/test_recommend_route.py` | `test_forbidden_value_in_the_answer_is_held_with_no_text` | RQ-70 |
| `tests/app/test_command_phrases.py` | `test_a_near_miss_phrase_is_held` | RQ-71 |
| `tests/app/test_audit_row_keys.py` | `test_app_tests_do_not_write_to_the_real_audit_log` | RQ-72 |
| `tests/app/test_readiness_route.py` | `test_readiness_returns_503_when_devices_csv_is_missing` | RQ-73 |

The list has 43 tests. RQ-31 is deferred (ADR 0004), so its test is not in this list. The name stays in section 1: `tests/app/test_recommend_cache.py::test_second_identical_request_within_300_seconds_makes_no_model_call`.

## 3. Route to requirements

| Route | Requirements |
|---|---|
| `GET /health` | RQ-01 |
| `GET /ready` | RQ-73 |
| `GET /records/{id}` | RQ-02 to RQ-07, RQ-68 |
| `GET /alarms/storms/{storm_batch_id}` | RQ-08 to RQ-15 |
| `POST /ai/summarize/{id}` | RQ-16 and RQ-17 |
| `POST /ai/recommend/{id}` | RQ-18 to RQ-30, RQ-70 and RQ-71 (RQ-31 is deferred) |
| `POST /approvals/{id}` | RQ-32 to RQ-41 |
| `GET /audit/{correlation_id}` | RQ-42 to RQ-52 |
| `GET /` (page) | RQ-62 to RQ-65 |
| No EXECUTE route | RQ-57 and RQ-58 |

## 4. Decision to requirement

| Decision | Requirement |
|---|---|
| D-03 approval `decision` and `approver` | RQ-32, RQ-33 |
| D-05 final action | RQ-40 |
| D-06 `record_id` | RQ-41 |
| D-08 command phrases | RQ-30 |
| D-12 rotation log | RQ-60 |
| D-16 p95 | RQ-67 |
| N-01 id limit 128 | RQ-44, RQ-69 |
| OB-01 answer store 300 s | RQ-31 (deferred, ADR 0004) |
| D-07 login out of scope | RQ-65 |
| F15 no-header 403 | RQ-68 |
| RK-03 header text | RQ-69 |
| RK-04 answer check | RQ-70 |
| RK-05 near miss | RQ-71 |
| RK-08 test log | RQ-72 |
| RK-11 readiness | RQ-73 |

## 5. How this file was checked

| Check | Result | Label |
|---|---|---|
| Every YAML id in section 1 exists in the seven YAML files | All found | **Verified Fact** (script on 2026-10-12) |
| Every existing test name is a function in the named file | 29 primary tests found | **Verified Fact** |
| The existing tests cited (67 node ids) were run | 101 passed, 2 skipped (both need `opa`) | **Verified Fact** (`pytest`, 2026-10-12) |
| Every design file in section 1 exists | All found | **Verified Fact** |
| `semantic-layer/build.py --check` | Passed. Version 1.2.0 (2026-10-13). | **Verified Fact** |
