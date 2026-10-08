# S03 — Semantic layer (product path step 1, D3)

Phase 3 in `Execution Plan.md`. This stage writes the one shared meaning set that the PRD, the policies, the app, and the second model will all read.

## Inputs

- `Semantic_Layer_capture.pdf`
- `Project_Intent.md` (sections 5.1, 6.2, Appendix E)
- `06-telecom-service-network-incident-ops/docs/domain-specific-spec.md`
- `06-telecom-service-network-incident-ops/docs/01-discovery/` (all six)
- `06-telecom-service-network-incident-ops/docs/02-baseline/data-quality-baseline.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/defect-list.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/apps/api/main.py`
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py`
- `06-telecom-service-network-incident-ops/policy/opa/access.rego`
- `06-telecom-service-network-incident-ops/data/synthetic/` (headers and distinct status values)

## Prompt

```text
# Stage S03 — Semantic layer

## Objective
Build `semantic-layer/` in the exact tree from `Semantic_Layer_capture.pdf`, plus `generated/` and `build.py`. The YAML is the source of truth. Markdown explains it. JSON Schema validates it. Tests protect it. Generated JSON serves it.

## Scope
Include: vocabulary from the domain spec, `main.py` roles, the seven personas, OPA roles, status words from every CSV column, AI fields from `ai_invocations.csv` and `ai_gateway.py`, rules from the defect list, picks from the S2Q table.
Exclude: application code; any second meaning file outside `semantic-layer/`; any new status word that does not appear in code, docs, or data unless it is marked `proposed: true` with an owner.

## Required analysis
1. Harvest: list every entity, field, role, persona, status word, AI field, and rule candidate with the file it came from.
2. Ids: give every entity, status, rule, metric, role, persona, and policy a stable id in dot form, for example `entity.device`, `status.incident.severity.gold`, `rule.missing_id_not_other_device`, `metric.tokens_per_invocation`, `persona.noc_operator`.
3. Collisions: in `status-taxonomy.yaml` write a `collisions` block for: `gold` and `bronze` used as incident severity; status words appearing inside `hostname` and `vendor`; `REC-0001` as the first key in six tables; `clinician` as an API role in a telecom system.
4. Rules: `business-rules.yaml` holds at least: a missing id must not return another device; AI output cannot execute; alarm `last_seen_at` cannot precede `first_seen_at`; a shared admin account is not least privilege; duplicate `dedupe_key` within a `storm_batch_id` is one alarm; an AI recommendation needs policy result, approval id, and audit row before any state change.
5. Access: `access-semantics.yaml` maps the seven personas to actions, resources, purpose, and risk. List `clinician` under `removed_roles` with the reason.
6. AI: `ai-context-policy.yaml` names fields allowed into a prompt; fields never allowed (`mgmt_ip`, `credential_profile`, credentials of any kind); the required output schema; model provenance fields (model, model_version, prompt_hash, tokens, latency_ms); the four outcomes RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE; fail-to-person on timeout or schema failure; and for each AI use the agency and approval point copied from `ai-qualification.md`.
7. Metrics: `metrics.yaml` defines at least tokens per invocation, cost per correlated incident, quarantine rate, retry count, audit completeness, recommendation latency. Each metric names its source fields. No target value unless PROPOSED with an owner.
8. Mark on each entity field whether the API reads it today.

## Evidence rules
- Every YAML item carries a `source:` list of file paths it came from.
- Every item not found in the repo carries `proposed: true` and `owner:`.
- Label claims in the Markdown files: Verified Fact, Inference, Assumption, Unknown.

## Constraints and guardrails
- The tree must be exactly: README.md, glossary.md, entities.yaml, relationships.yaml, status-taxonomy.yaml, business-rules.yaml, metrics.yaml, access-semantics.yaml, ai-context-policy.yaml, schemas/semantic-layer.schema.json, tests/test_semantic_layer.py, plus generated/ and build.py. The README says why generated/ and build.py were added.
- `schemas/semantic-layer.schema.json` validates every YAML file.
- `tests/test_semantic_layer.py` fails when a required entity, status, rule, or persona is missing; when the glossary and YAML disagree on a term; when a generated JSON file differs from its YAML; when any id is referenced but not defined.
- `build.py` reads YAML and writes `generated/*.json`. No hand edits in generated/.
- `glossary.md` explains each term in everyday words. One idea per sentence.
- Plain speech in Markdown and in YAML `description:` fields.
- No invented severity cutoff, SLA threshold, or target number.
- Redact secrets. No password, key, or token value anywhere in the tree.
- Each Markdown file starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md 4.3; read, do not re-derive)
| Constant | Value |
|---|---|
| Entities | devices, circuits, alarms, incidents, service_orders, ai_invocations, events |
| Personas | noc_operator, network_engineer, field_engineer, customer_support, automation_service, vendor_account, ai_agent |
| API roles today | admin, operator, clinician, engineer, ai_agent |
| OPA rules today | any admin; operator + read |
| Four AI outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Fields never in a prompt | mgmt_ip, credential_profile |
| Collisions | gold/bronze as severity; status words in hostname and vendor; REC-0001 first key in six tables |
| Model today | local-sim-v1; guardrail_status not_enforced |

## Required artifacts
The full tree under `06-telecom-service-network-incident-ops/semantic-layer/` as listed under Constraints. Run `python semantic-layer/build.py` and `pytest semantic-layer/tests -q` and record the output in README.md under "Last build".

## Completion gate
PASS when the schema validates every YAML file, every test passes, `generated/` is reproduced by `build.py`, and every item in `Project_Intent.md` 6.2 is ticked in README.md. CONDITIONAL PASS when one 6.2 item is ticked with a stated gap. BLOCKED when any YAML file is missing or a test fails.

## Lifecycle linkage
Cite `docs/01-discovery/`, `docs/02-baseline/data-quality-baseline.md`, `docs/02-baseline/defect-list.md`, and `docs/02-baseline/ai-qualification.md`. Stage S03R reviews this tree before any Phase 4 work. Stages S04-03, S04-06, S04-09, S04-12 reuse ids from here. Stage S06 cites ids per requirement. Stage S08 gives this tree, unchanged, to the second model.

## Required final response
End with exactly these seven items:
1. Stage status: PASS, CONDITIONAL PASS, or BLOCKED, with one sentence why.
2. Key findings.
3. Major risks.
4. Assumptions and unknowns.
5. Artifacts created, with paths.
6. Blocking issues.
7. Recommended next action.
```

## Expected output

| File | Must contain |
|---|---|
| `semantic-layer/README.md` | Header. The five format rules. Why `generated/` and `build.py` exist. Checklist 6.2 ticked. "Last build" output. |
| `semantic-layer/glossary.md` | Header. One entry per term. Everyday words. |
| `entities.yaml` | Seven entities. Fields with type, source, and `api_reads_today`. |
| `relationships.yaml` | Links between entities with cardinality and key fields. |
| `status-taxonomy.yaml` | Allowed values per status field. `collisions` block with four entries. |
| `business-rules.yaml` | At least six rules with ids and sources. |
| `metrics.yaml` | At least six metrics with source fields. |
| `access-semantics.yaml` | Seven personas by action, resource, purpose, risk. `removed_roles` with `clinician`. |
| `ai-context-policy.yaml` | Allowed and forbidden prompt fields. Output schema. Provenance fields. Four outcomes. Fail-to-person. Per-use agency and approval point. |
| `schemas/semantic-layer.schema.json` | Validates all seven YAML files. |
| `tests/test_semantic_layer.py` | Passing tests for presence, glossary match, generated match, id references. |
| `build.py` and `generated/*.json` | Reproducible. |

## Done test

Delete `generated/`, run `build.py`, run the tests. Everything passes. Change one status word in the glossary only. The tests fail.
