# Brief: build the application the PRD describes

| Field | Value |
|---|---|
| Stage | S08 Part 1. A second model builds an application from the semantic layer and the PRD. |
| Date / version | 2026-10-13. Semantic layer `1.2.1`. PRD `v1.9`. This brief is version 1.0. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Ready to paste after the model name is filled in below. |
| Evidence sources | The attached files listed in section 2. Nothing else. |
| Assumptions | The attached files are complete and agree with each other. |
| Unresolved issues | The PRD may be silent on a point. Section 5 says what to do then. |
| Residual risks | A point where the PRD is silent can lead to a guess. Section 5 asks you to record each guess. |

## 1. Model to use

Model name: **GPT-5.6 Sol**

The model must be a different model from the one that wrote the PRD. That model is Claude Sonnet 5.5.

## 2. Files to attach

All paths are relative to `06-telecom-service-network-incident-ops/`. Attach them read-only.

| Group | Files |
|---|---|
| Semantic layer | The whole folder `semantic-layer/` (20 files: seven `.yaml` files, `glossary.md`, `README.md`, `build.py`, `schemas/semantic-layer.schema.json`, `tests/test_semantic_layer.py`, and the eight files under `generated/`) |
| PRD | `docs/prd/prd.md` and `docs/prd/traceability.md` |
| Data the PRD names | `data/synthetic/devices.csv` and `data/synthetic/alarms.csv` |
| Tests | `tests/app/helpers.py`, `tests/test_api_contract.py`, `tests/access/test_negative_access.py`, `tests/app/test_records_route.py`, `tests/app/test_storm_route.py`, `tests/app/test_recommend_route.py`, `tests/app/test_approvals_route.py`, `tests/app/test_audit_row_keys.py`, `tests/app/test_demo_flow.py`, `tests/audit/test_audit_rebuild.py`, `policy/tests/test_policy_python.py`, `tests/security/test_client_flags_ignored.py` |

Read only these files. Do not open any other file in the repository.

## 3. The task

Build the application the PRD describes, under `apps/api_model_b/`, using only the terms and ids in `semantic-layer/`.

What this means:

1. Build every route that section 9 of the PRD says to build. Build none of the routes that section 9 lists as not built.
2. Meet every requirement row `RQ-01` to `RQ-73` in section 10 of the PRD, except `RQ-31`. The PRD marks `RQ-31` as deferred.
3. Give each word that your application returns, stores or shows a meaning from `semantic-layer/`. Use the ids and the status words that file defines. Do not add a word of your own.
4. Treat the two data files as read-only.
5. Put your application in a Python package at `apps/api_model_b/`. The module `apps/api_model_b/main.py` must hold a FastAPI application object named `app`.
6. Where the PRD names a file path for a runtime file, use that path. Where it does not, choose a path under `apps/api_model_b/`.

## 4. Tests the application must pass

The owner runs these 22 tests against your application after you finish. Each line gives the PRD row, then the test.

| PRD row | Test |
|---|---|
| RQ-01 | `tests/test_api_contract.py::test_health_contract` |
| RQ-03 | `tests/app/test_records_route.py::test_missing_id_returns_404_and_no_row` |
| RQ-04 | `tests/access/test_negative_access.py::test_clinician_role_is_denied_on_record_read` |
| RQ-05 | `tests/app/test_records_route.py::test_noc_operator_read_leaves_out_mgmt_ip_and_credential_profile` |
| RQ-06 | `tests/app/test_records_route.py::test_network_engineer_read_returns_mgmt_ip_and_credential_profile` |
| RQ-68 | `tests/app/test_records_route.py::test_missing_header_returns_403_and_a_deny_row` |
| RQ-08 | `tests/app/test_storm_route.py::test_storm_returns_raw_count_deduped_count_and_alarm_ids` |
| RQ-09 | `tests/app/test_storm_route.py::test_flagged_alarm_is_listed_and_is_not_an_incident_candidate` |
| RQ-10 | `tests/app/test_storm_route.py::test_unknown_storm_returns_404` |
| RQ-11 | `tests/app/test_storm_route.py::test_roles_without_an_alarm_read_row_get_403` |
| RQ-12 | `tests/app/test_storm_route.py::test_storm_read_leaves_alarms_csv_unchanged` |
| RQ-13 | `tests/app/test_storm_route.py::test_storm_response_has_no_size_flag` |
| RQ-15 | `tests/app/test_storm_route.py::test_storm_read_writes_one_audit_row` |
| RQ-18 | `tests/app/test_recommend_route.py::test_healthy_recommend_is_hold_for_review_with_the_sentence` |
| RQ-38 | `tests/security/test_client_flags_ignored.py::test_no_route_reads_an_approval_id_from_the_caller` |
| RQ-39 | `tests/app/test_approvals_route.py::test_an_approval_leaves_every_data_file_unchanged` |
| RQ-42 | `tests/audit/test_audit_rebuild.py::test_the_chain_comes_back_in_time_order` |
| RQ-46 | `tests/audit/test_audit_rebuild.py::test_the_response_holds_no_forbidden_field_or_credential_name` |
| RQ-47 | `tests/audit/test_audit_rebuild.py::test_cannot_prove_names_approval_id_and_log_integrity` |
| RQ-48 | `tests/app/test_demo_flow.py::test_one_case_rebuilds_from_one_correlation_id` |
| RQ-57 | `policy/tests/test_policy_python.py::test_no_route_can_execute` |
| RQ-69 | `tests/app/test_audit_row_keys.py::test_unknown_role_word_is_not_stored_as_sent` |

Rules for the tests:

1. Do not edit any test file.
2. The owner supplies the setup that points each test at your application. You cannot run these test files unchanged. Read them to learn what each check asserts.
3. You may write your own checks under `apps/api_model_b/tests/` and run them. List every check you wrote in your final response, with its result.
4. The PRD names other tests. Only the 22 above are asked of you.

## 5. Rules

1. **No edits outside `apps/api_model_b/`.** You may not edit anything under `semantic-layer/`. You may not edit `docs/prd/prd.md` or `docs/prd/traceability.md`. You may not edit any test, any data file or any other file in the repository.
2. **If the semantic layer or the PRD looks wrong,** do not change it. Write the problem as an open question in your final response.
3. **If the PRD and the semantic layer are silent on a point,** do not give a word a meaning of your own. Choose the smallest behaviour that fits the text. Write the point and your choice under item 4 of your final response.
4. **If you have a question,** ask it. The only answer you will get is: "use the glossary and YAML only". The owner records each question.
5. **No secrets.** Write no password, key or token value in any file or in your response.

## 6. Output paths

| What | Where |
|---|---|
| The application | `apps/api_model_b/` |
| Your own checks | `apps/api_model_b/tests/` |
| Your final response | The chat. The owner saves it. |

## 7. Required final response

End your last message with these seven items, in this order.

1. Stage status.
2. Key findings.
3. Major risks.
4. Assumptions and unknowns.
5. Artifacts created.
6. Blocking issues.
7. Recommended next action.

Label each claim in the response: Verified Fact (names a file, a test and its result, or a command), Inference, Assumption or Unknown.
