# Policy catalogue

| Field | Value |
|---|---|
| Stage | S04-06 — Policy as code (Challenge 6), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The catalogue names five policy areas. Each area has a decision, inputs, YAML rule ids, and an exists-today label. Only the access area has any policy code today, and no Python file calls it. Three terms the YAML lacks are listed as open questions for S03. |
| Evidence sources | `policy/opa/access.rego`; `apps/api/main.py`; `semantic-layer/access-semantics.yaml`; `semantic-layer/business-rules.yaml`; `semantic-layer/ai-context-policy.yaml`; `docs/03-identity/policy-input-model.md`; `docs/03-identity/target-access-matrix.md`; `docs/04-secrets/sensitive-field-handling-checklist.md`; `docs/02-baseline/ai-qualification.md`; `docs/02-baseline/defect-list.md`; `docs/01-discovery/brownfield-risk-register.md`; `docs/00-contract/operating-contract.md`; `docs/05-iac/iac-gap-report.md`; `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md`; `Project_Intent(sections 5.3, Appendix C).md` |
| Assumptions | A policy area is one kind of decision with one set of inputs. The five area names come from the playbook for this stage. Half B writes Rego for areas 1 and 2 only. That scope for Half B is PROPOSED. Owner: Team-Force. |
| Unresolved issues | No YAML id names the data-use destination (prompt, response, log). No YAML value list names the release checks. No YAML id names a call that sends no role header. See "Open questions for S03". |
| Residual risks | The catalogue describes policy that does not run yet. Every rule in `business-rules.yaml` has `enforced_today: false`, so a reader who sees a rule id here must not read it as a working control. The proposed 403 on a denied call changes tests that lock today's HTTP 200. See PC-07. |

## What this file is

This file lists the five kinds of policy decision this system needs. For each one it says what the decision is, what facts the decision reads, which YAML rule ids it enforces, and whether anything enforces it today.

Half A writes this catalogue. No code, test, or Rego file changes in this half.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. A Verified Fact names a file, a YAML id, or a test name. PROPOSED items name an owner. The owner is Team-Force (`docs/00-contract/operating-contract.md` row 10).

## The five areas

| # | Area | Decision it controls | Inputs it reads | YAML rule ids it enforces | Exists today | Half B enforces it |
|---|---|---|---|---|---|---|
| 1 | Access | May this caller take this action on this resource, for this purpose, over this set of records, at this risk? The answer is allow or deny. | `role`, `action`, `resource`, `purpose`, `scope`, `risk`. Rows TA-24 and TA-25 also read `approval_id`. | `rule.no_default_role`; `rule.shared_admin_not_least_privilege`; `rule.denied_access_is_audited`. Today's OPA rule ids are `policy.opa.admin_any`, `policy.opa.operator_read`, and `policy.opa.default_deny`. | Partly. `policy/opa/access.rego` exists with two allow rules and a default deny. The API does not call it. The API checks a Python list. | Yes. Rego and a test. |
| 2 | AI approval | What happens to one AI call: show the text, hold it for a person, block it, or run a change? The answer is one of RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE. | `persona`, `action`, `resource`, `risk`, `approval_id`, `policy_version`, `stale_topology_flag`, `output_schema_ok`, `timeout_hit`, plus six supporting inputs named in `ai-action-policy-design.md`. | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `rule.ai_output_cannot_execute`; `rule.stale_topology_blocks_recommendation`; fail modes `failmode.timeout`, `failmode.schema_failure`, `failmode.missing_id`, `failmode.stale_topology_true`, `failmode.stale_topology_blank`, `failmode.forbidden_field_in_prompt`. | No. The live gateway returns `guardrail_status` `not_enforced`. No route writes an approval id. | Yes. Rego and tests. |
| 3 | Data use | May these fields go into this prompt, this API response, or this log line? The answer is allow or deny. | `persona`, the list of field ids, and the destination of those fields. | `rule.forbidden_fields_never_enter_prompt`; `policy.prompt_fields`; grant TA-15 for the two sensitive device fields. | No. The prompt holds the whole device row. The record read returns every cell. | Partly. The prompt check is one input flag to area 2. Half B also tests the area 3 fixtures with a small set comparison. |
| 4 | Operational safety | May a change to a live device or circuit start now? The answer is allow or deny. | `persona`, `action`, `risk`, `approval_id`, `audit_row_written`, `change_plan_ok`. | `rule.ai_recommendation_needs_policy_approval_audit_before_state_change`; `rule.ai_output_cannot_execute`. | Only as the absence of a route. `main.py` has three routes and none changes a device. | Through the EXECUTE rows of area 2. No separate Rego file. |
| 5 | Production readiness | May this build be called ready for release? The answer is allow or deny. | The evidence sections still missing, the policy test result, the secret-pattern test result, and whether a CI run has been seen. | None. `business-rules.yaml` has no readiness rule. | No. `ci.yml` runs `pytest -q` only. The evidence pack file holds headings only. | No. Stage S09 uses the fixtures. |

How to read the table. Take area 2 and a call that asks to run a change on one device with no approval id. The area 2 decision is BLOCK. Area 4 gives deny for the same call. Area 2 answers for any AI call. Area 4 answers for any change to a live device, including a change that no model suggested.

## Area 1 — Access

**Decision.** The six input fields come from `docs/03-identity/policy-input-model.md`. The allow rows are TA-01 to TA-34 in `docs/03-identity/target-access-matrix.md`. A call is allowed only when one row matches on all six fields and the action is not on the persona's denied list.

**Today.** `access.rego` has three rules and no function call from Python. **Verified Fact:** `policy/opa/access.rego` lines 3 to 12. `docs/01-discovery/brownfield-risk-register.md` R19. `concept.policy_decision`. The live gate is the Python list on `apps/api/main.py` line 13.

The two gates give different answers for the same header. This table shows the answer each one gives for a record read.

| Header word | Python list, `main.py` line 13 | `access.rego` if it were called |
|---|---|---|
| `admin` | allow | allow (any action) |
| `operator` | allow | allow (read only) |
| `engineer` | allow | deny, because the file has no `engineer` rule |
| `ai_agent` | allow | deny, because the file has no `ai_agent` rule |
| `clinician` | deny (removed in S04-03 Half B) | deny |
| `vendor` | deny | deny |
| header absent | allow (the server fills in `operator`, line 11) | allow, as `operator` |

Worked example. A caller sends `GET /records/REC-0001` with header `engineer`. The Python list allows it and the response holds the whole row. If the API called today's `access.rego` with the same word, the answer would be deny. Half B replaces both with the TA rows.

## Area 2 — AI approval

**Decision.** This is the `ai_action` policy. The full design is in `ai-action-policy-design.md`. It returns one of the four outcomes locked in `Project_Intent(sections 5.3, Appendix C).md`.

**Today.** The summary route calls no policy. **Verified Fact:** `apps/api/main.py` lines 19 to 24. `guardrail_status` is `not_enforced` (`ai_gateway.py` line 17). `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` has `enforced_today: false`.

## Area 3 — Data use

**Decision.** Three destinations matter. A prompt sent to the model. An API response. A log line. The prompt allow list and the forbidden list are in `policy.prompt_fields`. Per-field rules are in `docs/04-secrets/sensitive-field-handling-checklist.md`.

**Today.** The prompt holds the whole device row, including `mgmt_ip` and `credential_profile` (F12). Every allowed role receives both cells on a record read (F10). **Verified Fact:** `ai_gateway.py` line 7. `domain_service.py` returns every cell.

Worked example. The model prompt for `REC-0001` is built with the cell values of `mgmt_ip` and `credential_profile`. The data-use policy returns deny for any prompt that holds either field, whatever the cell contains.

## Area 4 — Operational safety

**Decision.** A live network change needs four things together: a policy allow, a stored human approval id, an audit row written first, and a reversible, validated change. The YAML calls these four gates. **Verified Fact:** `outcome.execute` in `semantic-layer/ai-context-policy.yaml`. Operating contract row 9.

**Today.** No route changes a device. **Verified Fact:** `main.py` has `/health`, `/records/{record_id}`, and `/ai/summarize/{record_id}`. Defect K08. That absence is the only control. Project Intent section 5.3 says the absence is safer than a silent execute and to keep it until policy, approval, and audit exist.

## Area 5 — Production readiness

**Decision.** A release is allowed only when every evidence section is present and the tests that guard policy and secrets pass. The 15 section headings come from `PRODUCTION_EVIDENCE_PACK_TEMPLATE.md`.

**Today.** `ci.yml` installs `requirements.txt` and runs `pytest -q`. It sits below the git root, so it probably never runs (IG-09). **Verified Fact:** `docs/05-iac/iac-gap-report.md` IG-09. The evidence pack has 15 headings and no content.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| PC-01 | Only the access area has any policy code, and the API does not call it. | Verified Fact. `access.rego` lines 3 to 12. `main.py` line 13. R19. `concept.policy_decision`. IG-13 says nothing calls OPA. | A reviewer who reads the Rego learns nothing about what the API does. | The Rego file can drift from the Python list without a test failing. | High | None. |
| PC-02 | The Python list and the Rego file disagree for three header words. | Verified Fact. `engineer` and `ai_agent` are allowed by the list and have no Rego rule. `admin` is allowed by both and has no target row. Table in Area 1. | Wiring the Rego in without a map changes who can read a device. | A silent change to `engineer` and `ai_agent` reads. | High | None. |
| PC-03 | `policy.opa.admin_any` allows every action to one role that has no persona. | Verified Fact. `access.rego` lines 6 to 8. `role.admin` has `maps_to_persona: null`. `rule.shared_admin_not_least_privilege`. | Any admin can take any action. | The target matrix gives `role.admin` no row, so Half B turns today's admin read into a deny. K02 says admin reads `REC-0001` today. | High | Whether admin reads stay allowed through a dated waiver is a decision for acceptance. See `exception-handling-model.md`. |
| PC-04 | The data-use area has no enforcement in either direction. | Verified Fact. F10 and F12. `ai_gateway.py` line 7. `domain_service.py`. | Sensitive cells leave the API and enter the prompt. | The prompt text holds credentials-related cells. | High | Open question for S03 below on the destination list. |
| PC-05 | Operational safety exists only because no execute route exists. | Verified Fact. K08. Project Intent section 5.3. | A worker who adds a route later meets no check. | The first execute route would run with no gate. | High | None. |
| PC-06 | The readiness area has no rule in the YAML and no running CI. | Verified Fact. `business-rules.yaml` rule list. IG-09. Evidence pack template. | Stage S09 has no rule id to cite for a release decision. | A release decision rests on the author's judgment. | Medium. The CI path claim is an Inference in IG-09. | Open question for S03 below on release checks. |
| PC-07 | Wiring the policy into two routes changes behaviour that today's tests lock. | Verified Fact. `test_ai_summarize_accepts_request_with_no_role_header` and `test_clinician_role_is_denied_on_record_read` in `tests/characterization/test_current_behaviour.py`. `test_ai_summary_has_minimum_contract` in `tests/test_api_contract.py` posts with no header. | Half B must replace or update these tests when deny returns 403 and a missing role is refused. | A test change can hide a real regression if the new test is weaker. | High for the test names. Medium for which of them fail, because Half B has not run. | Whether the no-header call is refused in Half B is PROPOSED. Owner: Team-Force. `rule.no_default_role`. |

## Open questions for S03

Open question for S03: there is no id for a call that sends no role header. This design needs that id so a deny rule can name the role field when the header is absent, without first storing `role.operator`.

Open question for S03: the destination of a field (prompt, API response, log line) has no value list. The data-use policy needs it to say where a field may go.

Open question for S03: the checks a release must show (policy tests passed, secret-pattern test passed, a CI run seen, each evidence section present) have no ids. The production-readiness policy needs them to name what it reads.

## Lifecycle

This file cites `docs/03-identity/policy-input-model.md`, `docs/03-identity/target-access-matrix.md`, and `docs/02-baseline/ai-qualification.md`. Stage S04-06 Half B reads areas 1 and 2. Stage S04-09 calls `ai_action` from the gateway. Stage S05-13 collects the policy tests. Stage S07 relies on `policy.py` in every route. Stage S09 uses areas 4 and 5 and cites the allow and deny tests as D4 proof.
