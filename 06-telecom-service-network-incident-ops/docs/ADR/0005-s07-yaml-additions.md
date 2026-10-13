# ADR 0005: The YAML additions that stage S07 makes

| Field | Value |
|---|---|
| Stage | S07. Application and demo. The PRD says each addition is built in S07 under a new ADR (`docs/prd/prd.md` section 15, "Planned YAML additions"). |
| Date / version | 2026-10-13, v1.0 |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Accepted by earlier decisions, except one item. D-03, D-05, D-06 and D-08 are DECIDED in `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`. The three audit action words are required by RQ-52. The near-miss list (RQ-71) is a first draft that S07 wrote. It stays PROPOSED until Team-Force reviews it. |
| Evidence sources | `docs/prd/prd.md` (RQ-30, RQ-32, RQ-40, RQ-41, RQ-52, RQ-71, section 12, section 15); `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` (D-03, D-05, D-06, D-08); `docs/ADR/0004-defer-rq-31-answer-store.md`; `semantic-layer/tests/test_semantic_layer.py::test_audit_action_words_in_main_py_all_have_an_id`; `semantic-layer/tests/test_semantic_layer.py::test_audit_row_fields_are_the_keys_the_code_writes` |
| Assumptions | (1) Mangesh (FDE) speaks for Team-Force on open choices (`operating-contract.md` row 10). (2) A key name that the PRD already fixes is not a new choice. (3) The words in the near-miss list are forms of the seven command phrases, so the list adds no new verb. |
| Unresolved issues | The near-miss list needs a Team-Force review. The cache flag (D-18) is not added, because RQ-31 is deferred (ADR 0004). The failmode id for a forbidden value in a model answer (RQ-70) is not added. The reasons list keeps `failmode.forbidden_field_in_prompt` until Team-Force decides. The word to store for an unknown role (RQ-69) is not added (see the PRD gaps in `docs/demo/evidence.md`). |
| Residual risks | The two phrase lists are short. A phrase that means "reboot" in other words passes (D-08). The device values (`mgmt_ip`, `credential_profile`) are plain words such as `alpha`, so a harmless answer that holds one of them is held too. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## Context

The S07 app writes three audit action words, two audit keys, two approval fields and two phrase lists that the semantic layer `1.1.1` does not define. **Verified Fact.** The test `test_audit_action_words_in_main_py_all_have_an_id` fails when `main.py` holds an action word with no id. The test `test_audit_row_fields_are_the_keys_the_code_writes` fails when `SCHEMA_KEYS` and the YAML list differ. The PRD names each addition and says a new ADR comes first.

## Decision

The semantic layer goes from `1.1.1` to `1.2.0`. No id is removed. Eight ids are added (757 to 765, counted by the test helper `defined_ids`).

| Id added | What it names | Where the choice comes from |
|---|---|---|
| `field.audit_row.record_id` | The 16th audit key. The device id the caller asked for. Null when the row names no device. | D-06, RQ-41 |
| `field.audit_row.final_action` | The 17th audit key. The value is `none` on every row. | D-05, RQ-40 |
| `field.approval.decision` | The word `yes` or `no` on an approval record. | D-03, RQ-32 |
| `field.approval.approver` | The persona id of the caller's role, set by the server. A claim, not proof (D-07). | D-03, RQ-32 |
| `status.code.audit_action.storm_read` | The audit action word `record.storm_read`. | RQ-15, RQ-52 |
| `status.code.audit_action.ai_recommendation` | The audit action word `ai.recommendation`. | RQ-18, RQ-52 |
| `status.code.audit_action.ai_approval` | The audit action word `ai.approval`. | RQ-32, RQ-52 |
| `policy.command_phrases` | One block with two lists. `phrases` holds the seven starting phrases of D-08. `near_miss_phrases` holds forms of the same verbs, such as rebooting. | D-08, RQ-30, RQ-71 |

The two approval fields sit in a new `record_fields` list under `concept.approval`. The glossary gets 8 new rows, one for each id (273 to 281).

Five rules change `enforced_today` from false to true, because code now runs them. The PRD names them in section 12.

| Rule | Code that runs it |
|---|---|
| `rule.missing_id_not_other_device` | `domain_service.load_record` returns None. `GET /records/{id}` returns 404. |
| `rule.alarm_last_seen_not_before_first_seen` | `alarm_service.read_storm` flags each row. |
| `rule.duplicate_dedupe_key_in_storm_is_one_alarm` | `alarm_service.read_storm` groups rows with `DedupeSet`. |
| `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | `POST /approvals/{id}` writes the audit row first, then stores the decision. |
| `rule.no_default_role` | `GET /records/{id}` refuses a call with no role header. |

The phrase lists:

- `phrases`: reboot, restart, shut down, delete, clear config, push config, apply.
- `near_miss_phrases`: reboots, rebooting, rebooted, restarts, restarting, restarted, shutdown, shut-down, shuts down, shutting down, deletes, deleting, deleted, clear the config, clearing config, clears config, push the config, pushing config, pushes config, applies, applying, applied.

A phrase matches when it appears as whole words, in any letter case. The word `reboot` does not match inside `rebooting`. That is why the near-miss list exists.

## Consequences

- `build.py`, the schema, the 41 semantic-layer tests, the README and the glossary all carry `1.2.0`.
- The PRD header, `traceability.md` and the S08 hash step carry `1.2.0` (PRD section 15).
- The code reads the two phrase lists from the YAML. The code and the YAML cannot differ.
- `POST /ai/summarize/{id}` keeps its one legacy command sentence and its old reason string (RQ-16 says it stays as it is).

## Open items

| Item | Owner |
|---|---|
| Review the near-miss list | Team-Force. PROPOSED. |
| A failmode id for a forbidden value in a model answer (RQ-70) | Team-Force. Open question for S03. |
| The word to store for an unknown role (RQ-69) | Team-Force. Open question for S03. |
| The cache flag (D-18) | Team-Force. Deferred with RQ-31. |

## Text-only update to metrics.yaml

After the routes ran, `semantic-layer/metrics.yaml` still said that the audit row has no `record_id` key. The text of `metric.audit_completeness` (`live_source` and `today`) now says that `record_id` is the 16th key and `final_action` is the 17th. No id, formula, unit or target changed. `build.py` was run again and `--check` passes at version 1.2.0.
