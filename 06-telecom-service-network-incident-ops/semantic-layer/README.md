# Semantic layer

| Field | Value |
|---|---|
| Stage | S03 — Semantic layer (Execution Plan Phase 3; product path step 1, D3). Revised in S05R on 2026-10-12. |
| Date / version | 2026-10-12, semantic layer `1.1.1`. The first version, `1.0.0`, is dated 2026-10-10. |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | S05R revision applied, then one text change under ADR 0002 (the p95 choice for model delay). The version is `1.1.1` in every YAML file, in the schema, and here. The schema validates all seven YAML files. 41 tests pass. `generated/` is rebuilt from the YAML by `build.py`. The S03R rows run again in `docs/02-baseline/semantic-layer-revision.md`. Every item in `Project_Intent.md` 6.2 is ticked below. |
| Evidence sources | `Semantic_Layer_capture.pdf`; `Project_Intent.md` 4.3, 5.1, 6.2, Appendix E; `docs/domain-specific-spec.md`; `docs/01-discovery/` (all six); `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/ai-qualification.md`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/domain_service.py`; `apps/api/services/audit.py`; `policy/opa/access.rego`; `data/synthetic/` (headers and distinct values, read-only, 2026-10-10) |
| Assumptions | A column whose cells are all drawn from a small word pool is a status column. The persona grants, the purposes, the prompt allow list, and the output schema are PROPOSED with owner Team-Force. The API role `operator` maps to `noc_operator` and `engineer` maps to `network_engineer`. Both mappings are Inference. |
| Unresolved issues | The repo defines no allowed list for any status column. The alarm-to-incident join key, the storm size, the retry maximum, the `sla_breach_risk` range, and the timeout are Unknown or PROPOSED. The live-change approver's desk job is `network_engineer`, confirmed on 2026-10-10. `jsonschema` is installed in `.venv` only. `requirements.txt` does not list it. |
| Residual risks | A reader can treat a PROPOSED grant or allow list as approved. A later stage can add a term outside this tree. `status-taxonomy.yaml` is 3500 lines. A reviewer may skim it. The tests check its counts against the CSV files so a skim is safer. |

## What this folder is

This folder holds the one shared set of meanings for the telecom packet. The PRD, the policies, the app, and the second model all read it. Nothing outside this folder defines a term.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

## The five format rules

From `Semantic_Layer_capture.pdf`. **Verified Fact.**

1. Markdown explains it. `README.md` and `glossary.md` say what each term means in everyday words.
2. YAML defines it. The seven `.yaml` files are the source of truth.
3. JSON Schema validates it. `schemas/semantic-layer.schema.json` checks the shape of every YAML file.
4. Tests protect it. `tests/test_semantic_layer.py` fails when the tree, the YAML, the glossary, or the generated JSON drift.
5. Generated JSON serves it. `generated/*.json` is what a service or a second model loads.

## The tree

```text
semantic-layer/
├── README.md
├── glossary.md
├── entities.yaml
├── relationships.yaml
├── status-taxonomy.yaml
├── business-rules.yaml
├── metrics.yaml
├── access-semantics.yaml
├── ai-context-policy.yaml
├── schemas/
│   └── semantic-layer.schema.json
├── tests/
│   └── test_semantic_layer.py
├── build.py
└── generated/
    ├── entities.json
    ├── relationships.json
    ├── status-taxonomy.json
    ├── business-rules.json
    ├── metrics.json
    ├── access-semantics.json
    ├── ai-context-policy.json
    └── manifest.json
```

The first eleven entries are the layout in `Semantic_Layer_capture.pdf` and `Project_Intent.md` Appendix E. `build.py` and `generated/` are the two additions.

### Why `generated/` and `build.py` were added

Rule 5 says generated JSON serves the layer. The capture names the format. It does not name a file. `build.py` is the one script that turns the YAML into JSON. `generated/` is where that JSON lands. Without them, a service would parse YAML itself, and two parsers could read the same file two ways. With them, every reader loads the same bytes.

`generated/manifest.json` records the SHA-256 of each YAML file and each JSON file. The tests compare those hashes to the files on disk. A hand edit under `generated/` fails the test. A YAML edit without a rebuild fails the test.

## Version

This is version `1.1.1`. Every YAML file carries `version: "1.1.1"` at the top. `build.py` refuses to write when two files disagree on the version.

Stage S05R raised the version from `1.0.0` to `1.1.0` when it folded in the terms the control designs introduce. A change here now needs an ADR under `docs/ADR/`.

### Change log

| Version | Date | Stage | Change |
|---|---|---|---|
| `1.0.0` | 2026-10-10 | S03 | First version. Seven entities, 68 fields, 15 concepts, 15 relationships, 44 status words across 36 status fields, 4 collisions plus 5 other overlaps, 13 rules, 9 metrics, 7 personas with 5 value lists, 11 AI uses, 4 outcomes, 6 fail modes. |
| `1.0.0` | 2026-10-10 | S03F | S03R fixes applied, round 1. Fixes 1 to 9 from `docs/02-baseline/semantic-layer-review.md`. Added 4 `agency.*` and 4 `pick.*` ids, 28 glossary rows, and one test. Named Team-Force as owner of every PROPOSED item. |
| `1.0.0` | 2026-10-10 | S03F | S03R fixes applied, round 2. Fixes 1 to 3 and advisory A7 from `docs/02-baseline/semantic-layer-review.md`. Named Team-Force on the two bounds in the data-quality baseline, on the severity-list resolution, and on the legal-maximum cells. |
| `1.0.0` | 2026-10-10 | Owner decision | The live-change approver's desk job is `network_engineer`. Mangesh (FDE) confirmed it. Stage S04-09 uses this title. The semantic-layer version stays `1.0.0`. |
| `1.1.0` | 2026-10-12 | S05R (caused by designs from S04-03, S04-06, S04-08, S04-09, S04-10, S04-11, S04-12, S05-13, S05-14) | Folded in the terms the Phase 4 and 5 designs introduced. 92 ids added and 0 removed (665 to 757). Two OPA ids are deprecated with `replaced_by`. 92 glossary rows added (181 to 273). One schema rule added (`deprecated` needs `replaced_by`), plus new shapes for audit row fields, policy inputs, and `model_now`. Six tests added (35 to 41). Sentences that described the state before stages S04-06 to S04-12 were corrected. The full list is in `docs/02-baseline/semantic-layer-revision.md`. |
| `1.1.1` | 2026-10-12 | ADR 0002 (the owner's decisions on the S05R open items) | One sentence changed in `metric.recommendation_latency`: the percentile to report is p95 (D-16). The glossary row has the same sentence. No id added, removed, or deprecated (757 ids). The `proposed: true` flags stay, because the flag marks items that are not in the inherited repo. |

## How to run

From the repo root `06-telecom-service-network-incident-ops`, with the `.venv` active or by calling `.venv\Scripts\python.exe`:

```text
python semantic-layer/build.py          # validate the YAML and write generated/
python semantic-layer/build.py --check  # validate, and fail if generated/ is stale
pytest semantic-layer/tests -q          # run the 41 tests
```

`build.py` and the tests need `PyYAML` and `jsonschema`. `requirements.txt` pins `PyYAML` and not `jsonschema`. This stage installed `jsonschema` 4.26.0 into `.venv` only, the same way S00 installed `httpx`. Adding it to `requirements.txt` is a repo change for a later stage to decide.

## Id conventions

Every item has one stable id in dot form. The first word is the kind. The tests reject an id with an unknown first word, an id defined twice, and a reference to an id that is not defined.

| Prefix | What it names | Example | Defined in |
|---|---|---|---|
| `entity.` | A table or the event log | `entity.device` | `entities.yaml` |
| `field.` | One column | `field.device.mgmt_ip` | `entities.yaml` |
| `field.audit_row.` | One key of the audit row (S05R) | `field.audit_row.correlation_id` | `entities.yaml`, under `concept.audit_row` |
| `field.policy_input.` | One input of the AI action policy (S05R) | `field.policy_input.record_found` | `ai-context-policy.yaml` |
| `concept.` | A term with no table | `concept.topology` | `entities.yaml` |
| `relationship.` | A link between entities | `relationship.device_has_alarms` | `relationships.yaml` |
| `status.word.` | One distinct status word | `status.word.gold` | `status-taxonomy.yaml` |
| `status.<entity>.<column>` | One status column | `status.incident.severity` | `status-taxonomy.yaml` |
| `status.<entity>.<column>.<word>` | One word in one column | `status.incident.severity.gold` | `status-taxonomy.yaml` |
| `status.code.` | A word the live code returns | `status.code.model.local_sim_v1` | `status-taxonomy.yaml` |
| `valueset.` | A pool of words | `valueset.severity_words` | `status-taxonomy.yaml` |
| `collision.` | One word or key with two meanings | `collision.gold_bronze_as_severity` | `status-taxonomy.yaml` |
| `rule.` | A business rule | `rule.missing_id_not_other_device` | `business-rules.yaml` |
| `metric.` | A measure | `metric.tokens_per_invocation` | `metrics.yaml` |
| `persona.` | One of the seven personas | `persona.noc_operator` | `access-semantics.yaml` |
| `role.` | One of the five API role strings today | `role.clinician` | `access-semantics.yaml` |
| `action.` `resource.` `purpose.` `scope.` `risk.` | The five access value lists | `scope.one_site` | `access-semantics.yaml` |
| `policy.` | A named policy block | `policy.prompt_fields` | `access-semantics.yaml`, `ai-context-policy.yaml` |
| `outcome.` | One of the four AI outcomes | `outcome.hold_for_review` | `ai-context-policy.yaml` |
| `provenance.` | A field that says where an answer came from | `provenance.prompt_hash` | `ai-context-policy.yaml` |
| `ai_use.` | One of the eleven capabilities | `ai_use.incident_summary` | `ai-context-policy.yaml` |
| `failmode.` | A fail-to-person trigger | `failmode.timeout` | `ai-context-policy.yaml` |
| `agency.` | One of the four words for how far a step may go | `agency.recommend` | `ai-context-policy.yaml` |
| `pick.` | One of the four words for what kind of tool does a step | `pick.deterministic_code` | `ai-context-policy.yaml` |

A hyphen in a data value becomes an underscore in the id. `east-4` is `status.word.east_4`. The `value` or `word` key keeps the original text.

## Evidence rules used in the YAML

- Every item carries a `source:` list. Each path is relative to the repo root. `../Project_Intent.md` points one level up. The tests check that every path exists.
- Every item the repo does not contain carries `proposed: true` and `owner:`. The schema rejects `proposed: true` without an owner.
- No YAML item sets a severity cutoff, an SLA threshold, a retry maximum, a timeout number, or a target. Where the baseline proposed a bound, the YAML records it as a note with Owner: Team-Force.
- No password, key, or token value is in this tree. The test reads the secret values from `.env.example` and `legacy/reconcile_legacy.py` at run time and fails if any of them appears here.

## Harvest

Where each kind of item came from. **Verified Fact** for every path.

| Kind | Count | Source files |
|---|---|---|
| Entities | 7 | `docs/domain-specific-spec.md` (six); `Project_Intent.md` 4.3 and `data/synthetic/events.jsonl` (events) |
| Fields | 68 | The header row of each CSV; the keys of the first line of `events.jsonl`; `docs/01-discovery/data-and-integration-map.md` |
| Which fields the API reads today | 12 of 68 | `apps/api/services/domain_service.py` reads `devices.csv` and matches the id against every cell. Every device field is `api_reads_today: true`. Every other field is `false`. |
| Concepts | 17 | `Project_Intent.md` Appendix E (topology, SLA, remediation, guardrail); id columns with no table (customer, site, storm); `docs/00-contract/operating-contract.md` (approval, audit row, prompt, policy decision); `docs/domain-specific-spec.md` (four flows); `docs/06-policy/exception-handling-model.md` (waiver) and `docs/14-audit/decision-provenance-model.md` (decision provenance), added in S05R |
| Audit row fields | 15 | `apps/api/services/audit.py` `SCHEMA_KEYS`; `docs/08-observability/log-schema.md`. Added in S05R under `concept.audit_row`. |
| Policy inputs | 8 | `policy/opa/ai_action.rego`; `docs/06-policy/ai-action-policy-design.md`. Added in S05R. |
| Relationships | 15 | `Project_Intent.md` Appendix E; shared id columns in the CSVs; `docs/01-discovery/business-flow-reconstruction.md` |
| Status words | 44 | Every distinct non-blank word in 33 CSV word columns and 3 event fields, counted on 2026-10-10 |
| Status fields | 36 | 33 CSV columns plus `events.jsonl` `severity`, `actor`, `business_entity`, `event_type` |
| Code words | 55 | 8 from `apps/api/main.py`, `apps/api/services/ai_gateway.py`, and `apps/api/services/audit.py`. 47 added in S05R from the same files plus `apps/api/services/audit_query.py`, `breaker.py`, `dedupe.py`, `policy.py`, `policy/opa/*.rego`, and `docs/runbooks/incident-response.md`. |
| Collisions | 4 + 7 | `Project_Intent.md` 4.3; `docs/02-baseline/defect-list.md` F03, F09, F17, F21, F22; `docs/01-discovery/ai-subsystem-discovery.md`; two added in S05R from `docs/06-policy/ai-action-policy-design.md` and `docs/runbooks/incident-response.md` |
| Rules | 20 | `docs/02-baseline/defect-list.md` F01, F02, F05, F06, F08, F10, F11, F12, F14, F15, F16, F17, F22; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/operating-contract.md` rows 2 and 9. Seven added in S05R from `docs/13-security-validation/`, `docs/11-reliability/`, `docs/14-audit/`, and `apps/api/services/dedupe.py`. |
| Metrics | 13 | `Project_Intent.md` Appendix E; `docs/02-baseline/data-quality-baseline.md`; `docs/00-contract/cost-envelope.md`; `etl/run_daily_batch.py`. Four added in S05R from `docs/08-observability/slo-proposal.md`, `docs/10-performance/scaling-recommendations.md`, `docs/12-finops/optimization-backlog.md`, and `docs/12-finops/cost-per-workflow.md`. |
| API roles today | 5 | `apps/api/main.py` line 13 |
| OPA rules today | 4 | `policy/opa/access.rego`. Two of the three original ids are deprecated. One id was added for the access matrix. |
| Personas | 7 | `docs/domain-specific-spec.md`; `events.jsonl` `actor` counts |
| AI uses | 11 | `docs/02-baseline/ai-qualification.md`, one row each, pick and agency and approval point copied |
| AI fields | 10 CSV + 6 live | `data/synthetic/ai_invocations.csv` header; `ai_gateway.py` return dict |

### Status word pools

The 44 words fall into seven pools. The same 14-word pool fills 16 columns whose names promise different kinds of value. **Verified Fact** from the counts in `status-taxonomy.yaml`.

| Pool | Words | Columns it fills |
|---|---|---|
| Severity | `bronze` `critical` `gold` `high` `low` `medium` `silver` | `alarms.severity`, `incidents.severity`, `circuits.service_class`, `circuits.sla_tier` |
| Workflow | `approved` `closed` `exception` `failed` `in_progress` `manual_hold` `new` `queued` | `circuits.status`, `incidents.status`, `service_orders.qualification_status`, `provisioning_status`, `rollback_status` |
| Generic | `ai_assisted` `approved` `degraded` `high_risk` `internal` `legacy` `manual` `normal` `not_enforced` `pending` `rejected` `requires_review` `standard` `vendor` | `hostname`, `vendor`, `device_type`, `firmware`, `owner_team`, `credential_profile`, `interface`, `alarm_type`, `maintenance_window`, `root_cause`, `service_type`, `use_case`, `model`, `recommendation_risk`, `approval_required`, `guardrail_status` |
| Boolean | `true` `false` | `stale_topology_flag`, `orphan_flag`, `automation_used` |
| Endpoint | `alpha` `beta` `gamma` `legacy` `modernized` | `mgmt_ip`, `a_end`, `z_end` |
| Network zone | `north-1` `south-2` `west-3` `east-4` `central-5` `remote-6` | `network_zone` |
| Event log level | `debug` `info` `warn` `error` `critical` | `events.severity` |

Worked example. `incidents.csv` line 3 is `INC-00002` with `severity` `gold`. A report grouped by severity counts 41 `gold` rows next to 39 `critical` rows. The repo does not say which is worse. The YAML lists both words and marks the mix as `collision.gold_bronze_as_severity`. It does not rank them.

## The four collisions

| Id | What collides | Defect |
|---|---|---|
| `collision.gold_bronze_as_severity` | Service-class words `gold`, `silver`, `bronze` fill the incident and alarm severity columns next to `critical`, `high`, `medium`, `low`. | F09 |
| `collision.status_words_in_hostname_and_vendor` | The first device row has `hostname` `legacy` and `vendor` `requires_review`. The same 14 words fill 16 columns. The API matches an id against every cell. | F17, F22 |
| `collision.rec_0001_first_key_in_six_tables` | Six different objects share the key text `REC-0001`. The other keys use `DEV-`, `CIR-`, `ALA-`, `INC-`, `ORD-`, `AI_-`. | F21 |
| `collision.clinician_role_in_telecom_api` | A health-care job word is on the telecom API allow list. `access-semantics.yaml` lists it under `removed_roles`. | F03 |

Seven more overlaps are listed under `other_overlaps` in `status-taxonomy.yaml`. They are not in the locked list of four.

## What the tests check

`tests/test_semantic_layer.py` has 41 tests. They fail when:

- a file in the fixed tree is missing or an extra file appears
- a YAML file does not carry `version: "1.1.1"`, or this README does not repeat it
- the schema rejects any YAML file, or the schema accepts a known-bad document (three negative tests)
- a required entity, persona, status word, rule, metric, outcome, collision, or API role is missing
- a GenAI use has an agency other than recommend, or any use other than workflow automation reaches EXECUTE
- an `agency` or `pick` value anywhere in the YAML has no matching `agency.*` or `pick.*` item
- a forbidden prompt field is also on the allow list, or a `never_in_prompt` field is not forbidden
- `api_reads_today` is true on any field outside `entity.device`, or false on any device field
- an id is not in dot form, uses an unknown prefix, or is defined twice
- any whole-string value with an id prefix is not a defined id
- an item has no `source`, or a `source` path does not exist on disk
- an item has `proposed: true` and no `owner`
- a metric has a target value
- `glossary.md` has no row for an id, names an id the YAML lacks, lists an id twice, or shows a Term that differs from the YAML `name` or `word`
- a file under `generated/` differs from its YAML, or a hash in `manifest.json` does not match the file on disk
- an entity's field list differs from the CSV header or the event keys
- a word in a CSV status column is missing from `status-taxonomy.yaml`, or an `observed_count` or `blank_count` differs from the file
- a secret value from `.env.example` or `legacy/reconcile_legacy.py` appears anywhere in this tree
- (S05R) an item has `deprecated: true` and no defined `replaced_by`, or the schema accepts that shape
- (S05R) the audit row fields in `concept.audit_row` differ from `SCHEMA_KEYS` in `audit.py`
- (S05R) the `status.code.cannot_prove.*` values differ from the 13 item names in `audit_query.py`
- (S05R) an audit action word in `apps/api/main.py` has no `status.code.audit_action.*` id
- (S05R) an id that `apps/`, `policy/`, `tests/`, or `etl/` cite in quotes has lost its definition

A code value is the exact text the code writes. The reference test skips the `value` key of a code value for that reason. The word `policy.deny` is a code value and is not a reference.

### Done test

This is the S03 done test. Run on 2026-10-10. **Verified Fact.**

1. Deleted `generated/`. Ran `build.py`. It wrote eight files. Ran the tests. 34 passed.
2. Changed the glossary Term `gold` to `golden` and nothing else. Ran the tests. `test_glossary_and_yaml_agree_on_every_term` failed with `glossary term differs from YAML name or word: [('golden', 'status.word.gold', 'gold')]`. Restored the word.

## Checklist from `Project_Intent.md` 6.2

- [x] The folder matches `Semantic_Layer_capture.pdf`. The eleven entries are present. `build.py` and `generated/` are the two stated additions. `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` locks the tree.
- [x] `glossary.md` explains terms in everyday words. 273 rows (181 at 1.0.0 and 92 added in S05R). One row per entity, concept, status word, collision, rule, metric, action, resource, purpose, scope, risk, API role, persona, outcome, fail mode, agency word, pick word, AI use, and provenance field. S05R also adds a row for each audit row field, policy input, and new code word.
- [x] YAML defines entities, relationships, statuses, rules, metrics, access, and AI context. Seven files. Each carries `version`, `file`, `description`, and `source`.
- [x] Status words used in code, docs, and CSV are listed. Collisions such as `gold` used as incident severity are named. 44 words, 36 status fields, 55 code words, 4 collisions, 7 other overlaps.
- [x] JSON Schema validates the YAML. One schema, seven branches picked by the `file` key. `build.py` refuses to write on a validation error.
- [x] Tests fail when a required entity, status, or rule is missing. Also when a persona, metric, outcome, collision, or API role is missing, when the glossary disagrees, when `generated/` drifts, and when an id is referenced but not defined.
- [x] Generated JSON is produced from YAML, not edited by hand. `build.py` writes it. `manifest.json` hashes catch a hand edit.

## Open questions for later stages

These are Unknown in the repo. The YAML records each one where it sits. A later stage that decides one writes an "Open question for S03" line and S05R folds the answer in.

| Question | Where it sits | Stage that decides |
|---|---|---|
| Which severity words are allowed, and in what order | `status.incident.severity`, `status.alarm.severity` | S05R, owner Team-Force |
| Which columns join an alarm to an incident | `relationship.alarm_to_incident` | S04-11 |
| How many alarms make a storm | `metric.alarm_storm_size` | S04-11, owner Team-Force |
| The legal maximum for `retry_count` | `metric.retry_count` | Owner: Team-Force |
| The legal range for `sla_breach_risk` | `metric.sla_breach_risk` | Owner: Team-Force |
| The timeout for a model call | `policy.fail_to_person` | Deferred in S05R. The slot stays null until Team-Force states the number. The code default is PROPOSED. |
| What a blank `stale_topology_flag` should do | `failmode.stale_topology_blank` | The gateway holds the case for review (PROPOSED, Team-Force). The final answer is still Unknown. |
| The desk job of the human who approves a live change | `ai_use.remediation_execution` | Confirmed 2026-10-10 as `network_engineer`. S04-09 uses this title. |
| Which personas may read `mgmt_ip` and `credential_profile` | `resource.sensitive_device_fields` | S04-03 proposed row TA-15 for `persona.network_engineer`. Team-Force accepted it as written in ADR 0002 on 2026-10-12. |
| Whether `automation_service` is the shared user `app_shared` | `persona.automation_service` | S04-04 |
| Whether `engineer` stays on the API role list | `role.engineer` | S04-03 |
| Which order built which circuit | `relationship.order_to_circuit` | owner Team-Force |

## Last build

Run on 2026-10-12 after ADR 0002 (the first run was by stage S05R, at version `1.1.0`), from `06-telecom-service-network-incident-ops` with `.venv\Scripts\python.exe`, after deleting `generated/`. `PYTHONDONTWRITEBYTECODE=1` was set. The S05R record, with the full test run, is in `docs/02-baseline/semantic-layer-revision.md`. The S03F round 2 output is in `docs/02-baseline/semantic-layer-fixes.md`. **Verified Fact.**

```text
> python semantic-layer/build.py
Validated 7 YAML files against semantic-layer.schema.json. Version 1.1.1.
  wrote generated/entities.json
  wrote generated/relationships.json
  wrote generated/status-taxonomy.json
  wrote generated/business-rules.json
  wrote generated/metrics.json
  wrote generated/access-semantics.json
  wrote generated/ai-context-policy.json
  wrote generated/manifest.json
exit=0

> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.1.1.
exit=0

> pytest semantic-layer/tests -q -p no:cacheprovider
.........................................                                [100%]
41 passed in 2.50s
exit=0
```

S05R changed no file under `apps/`, `policy/`, `data/`, `etl/`, or `legacy/`. The full run `pytest tests policy/tests semantic-layer/tests -q` printed `333 passed`.

## Lifecycle

This tree cites `docs/01-discovery/` (all six files), `docs/02-baseline/data-quality-baseline.md`, `docs/02-baseline/defect-list.md`, and `docs/02-baseline/ai-qualification.md`.

Stage S03R reviews this tree before any Phase 4 work. Stages S04-03 (identity), S04-06 (policy), S04-09 (AI guardrails), and S04-12 (FinOps) reuse ids from here. S04-03 builds the policy input model from the five value lists in `access-semantics.yaml`. S04-06 reads the same ids in Rego. S04-09 cites the `ai_use.*` rows and `policy.prompt_fields`. S04-12 cites `metric.tokens_per_invocation` and `metric.cost_per_correlated_incident`.

A Phase 4 or 5 design that needs a term this tree lacks writes an "Open question for S03" line. Stage S05R folds those terms in and raises the version. Stage S06 cites ids at that version. Stage S08 gives that version, unchanged, to the second model.
