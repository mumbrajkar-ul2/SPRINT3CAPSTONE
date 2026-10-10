# Semantic layer

| Field | Value |
|---|---|
| Stage | S03 — Semantic layer (Execution Plan Phase 3; product path step 1, D3) |
| Date / version | 2026-10-10, semantic layer `1.0.0` |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The schema validates all seven YAML files. 34 tests pass. `generated/` is rebuilt from the YAML by `build.py`. Every item in `Project_Intent.md` 6.2 is ticked below. |
| Evidence sources | `Semantic_Layer_capture.pdf`; `Project_Intent.md` 4.3, 5.1, 6.2, Appendix E; `docs/domain-specific-spec.md`; `docs/01-discovery/` (all six); `docs/02-baseline/data-quality-baseline.md`; `docs/02-baseline/defect-list.md`; `docs/02-baseline/ai-qualification.md`; `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/domain_service.py`; `apps/api/services/audit.py`; `policy/opa/access.rego`; `data/synthetic/` (headers and distinct values, read-only, 2026-10-10) |
| Assumptions | A column whose cells are all drawn from a small word pool is a status column. The persona grants, the purposes, the prompt allow list, and the output schema are PROPOSED with owner Mangesh (FDE). The API role `operator` maps to `noc_operator` and `engineer` maps to `network_engineer`. Both mappings are Inference. |
| Unresolved issues | The repo defines no allowed list for any status column. The alarm-to-incident join key, the storm size, the retry maximum, the `sla_breach_risk` range, the timeout, and the approver's desk job are Unknown or PROPOSED. `jsonschema` is installed in `.venv` only. `requirements.txt` does not list it. |
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

This is version `1.0.0`. Every YAML file carries `version: "1.0.0"` at the top. `build.py` refuses to write when two files disagree on the version.

Stage S05R raises the version when it folds in the terms the control designs introduce. After S05R, a change here needs an ADR.

### Change log

| Version | Date | Stage | Change |
|---|---|---|---|
| `1.0.0` | 2026-10-10 | S03 | First version. Seven entities, 68 fields, 15 concepts, 15 relationships, 44 status words across 36 status fields, 4 collisions plus 5 other overlaps, 13 rules, 9 metrics, 7 personas with 5 value lists, 11 AI uses, 4 outcomes, 6 fail modes. |

## How to run

From the repo root `06-telecom-service-network-incident-ops`, with the `.venv` active or by calling `.venv\Scripts\python.exe`:

```text
python semantic-layer/build.py          # validate the YAML and write generated/
python semantic-layer/build.py --check  # validate, and fail if generated/ is stale
pytest semantic-layer/tests -q          # run the 34 tests
```

`build.py` and the tests need `PyYAML` and `jsonschema`. `requirements.txt` pins `PyYAML` and not `jsonschema`. This stage installed `jsonschema` 4.26.0 into `.venv` only, the same way S00 installed `httpx`. Adding it to `requirements.txt` is a repo change for a later stage to decide.

## Id conventions

Every item has one stable id in dot form. The first word is the kind. The tests reject an id with an unknown first word, an id defined twice, and a reference to an id that is not defined.

| Prefix | What it names | Example | Defined in |
|---|---|---|---|
| `entity.` | A table or the event log | `entity.device` | `entities.yaml` |
| `field.` | One column | `field.device.mgmt_ip` | `entities.yaml` |
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

A hyphen in a data value becomes an underscore in the id. `east-4` is `status.word.east_4`. The `value` or `word` key keeps the original text.

## Evidence rules used in the YAML

- Every item carries a `source:` list. Each path is relative to the repo root. `../Project_Intent.md` points one level up. The tests check that every path exists.
- Every item the repo does not contain carries `proposed: true` and `owner:`. The schema rejects `proposed: true` without an owner.
- No YAML item sets a severity cutoff, an SLA threshold, a retry maximum, a timeout number, or a target. Where the baseline proposed a bound, the YAML records it as a note with owner Unknown.
- No password, key, or token value is in this tree. The test reads the secret values from `.env.example` and `legacy/reconcile_legacy.py` at run time and fails if any of them appears here.

## Harvest

Where each kind of item came from. **Verified Fact** for every path.

| Kind | Count | Source files |
|---|---|---|
| Entities | 7 | `docs/domain-specific-spec.md` (six); `Project_Intent.md` 4.3 and `data/synthetic/events.jsonl` (events) |
| Fields | 68 | The header row of each CSV; the keys of the first line of `events.jsonl`; `docs/01-discovery/data-and-integration-map.md` |
| Which fields the API reads today | 12 of 68 | `apps/api/services/domain_service.py` reads `devices.csv` and matches the id against every cell. Every device field is `api_reads_today: true`. Every other field is `false`. |
| Concepts | 15 | `Project_Intent.md` Appendix E (topology, SLA, remediation, guardrail); id columns with no table (customer, site, storm); `docs/00-contract/operating-contract.md` (approval, audit row, prompt, policy decision); `docs/domain-specific-spec.md` (four flows) |
| Relationships | 15 | `Project_Intent.md` Appendix E; shared id columns in the CSVs; `docs/01-discovery/business-flow-reconstruction.md` |
| Status words | 44 | Every distinct non-blank word in 33 CSV word columns and 3 event fields, counted on 2026-10-10 |
| Status fields | 36 | 33 CSV columns plus `events.jsonl` `severity`, `actor`, `business_entity`, `event_type` |
| Code words | 8 | `apps/api/main.py`; `apps/api/services/ai_gateway.py`; `apps/api/services/audit.py` |
| Collisions | 4 + 5 | `Project_Intent.md` 4.3; `docs/02-baseline/defect-list.md` F03, F09, F17, F21, F22; `docs/01-discovery/ai-subsystem-discovery.md` |
| Rules | 13 | `docs/02-baseline/defect-list.md` F01, F02, F05, F06, F08, F10, F11, F12, F14, F15, F16, F17, F22; `docs/02-baseline/ai-qualification.md`; `docs/00-contract/operating-contract.md` rows 2 and 9 |
| Metrics | 9 | `Project_Intent.md` Appendix E; `docs/02-baseline/data-quality-baseline.md`; `docs/00-contract/cost-envelope.md`; `etl/run_daily_batch.py` |
| API roles today | 5 | `apps/api/main.py` line 13 |
| OPA rules today | 3 | `policy/opa/access.rego` |
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

Five more overlaps are listed under `other_overlaps` in `status-taxonomy.yaml`. They are not in the locked list of four.

## What the tests check

`tests/test_semantic_layer.py` has 34 tests. They fail when:

- a file in the fixed tree is missing or an extra file appears
- a YAML file does not carry `version: "1.0.0"`, or this README does not repeat it
- the schema rejects any YAML file, or the schema accepts a known-bad document (three negative tests)
- a required entity, persona, status word, rule, metric, outcome, collision, or API role is missing
- a GenAI use has an agency other than recommend, or any use other than workflow automation reaches EXECUTE
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

### Done test

Run on 2026-10-10. **Verified Fact.**

1. Deleted `generated/`. Ran `build.py`. It wrote eight files. Ran the tests. 34 passed.
2. Changed the glossary Term `gold` to `golden` and nothing else. Ran the tests. `test_glossary_and_yaml_agree_on_every_term` failed with `glossary term differs from YAML name or word: [('golden', 'status.word.gold', 'gold')]`. Restored the word.

## Checklist from `Project_Intent.md` 6.2

- [x] The folder matches `Semantic_Layer_capture.pdf`. The eleven entries are present. `build.py` and `generated/` are the two stated additions. `test_tree_is_exactly_the_capture_layout_plus_generated_and_build` locks the tree.
- [x] `glossary.md` explains terms in everyday words. 153 rows. One row per entity, concept, status word, collision, rule, metric, action, resource, purpose, scope, risk, API role, persona, outcome, and fail mode.
- [x] YAML defines entities, relationships, statuses, rules, metrics, access, and AI context. Seven files. Each carries `version`, `file`, `description`, and `source`.
- [x] Status words used in code, docs, and CSV are listed. Collisions such as `gold` used as incident severity are named. 44 words, 36 status fields, 8 code words, 4 collisions, 5 other overlaps.
- [x] JSON Schema validates the YAML. One schema, seven branches picked by the `file` key. `build.py` refuses to write on a validation error.
- [x] Tests fail when a required entity, status, or rule is missing. Also when a persona, metric, outcome, collision, or API role is missing, when the glossary disagrees, when `generated/` drifts, and when an id is referenced but not defined.
- [x] Generated JSON is produced from YAML, not edited by hand. `build.py` writes it. `manifest.json` hashes catch a hand edit.

## Open questions for later stages

These are Unknown in the repo. The YAML records each one where it sits. A later stage that decides one writes an "Open question for S03" line and S05R folds the answer in.

| Question | Where it sits | Stage that decides |
|---|---|---|
| Which severity words are allowed, and in what order | `status.incident.severity`, `status.alarm.severity` | S05R, owner Unknown |
| Which columns join an alarm to an incident | `relationship.alarm_to_incident` | S04-11 |
| How many alarms make a storm | `metric.alarm_storm_size` | S04-11, owner Unknown |
| The legal maximum for `retry_count` | `metric.retry_count` | Owner Unknown |
| The legal range for `sla_breach_risk` | `metric.sla_breach_risk` | Owner Unknown |
| The timeout for a model call | `policy.fail_to_person` | S04-09 |
| What a blank `stale_topology_flag` should do | `failmode.stale_topology_blank` | S04-09 |
| The desk job of the human who approves a live change | `ai_use.remediation_execution` | S04-09 |
| Which personas may read `mgmt_ip` and `credential_profile` | `resource.sensitive_device_fields` | S04-03 |
| Whether `automation_service` is the shared user `app_shared` | `persona.automation_service` | S04-04 |
| Whether `engineer` stays on the API role list | `role.engineer` | S04-03 |
| Which order built which circuit | `relationship.order_to_circuit` | Owner Unknown |

## Last build

Run on 2026-10-10 from the repo root with `.venv\Scripts\python.exe`. **Verified Fact.**

```text
> python semantic-layer/build.py
Validated 7 YAML files against semantic-layer.schema.json. Version 1.0.0.
  wrote generated/entities.json
  wrote generated/relationships.json
  wrote generated/status-taxonomy.json
  wrote generated/business-rules.json
  wrote generated/metrics.json
  wrote generated/access-semantics.json
  wrote generated/ai-context-policy.json
  wrote generated/manifest.json

> python semantic-layer/build.py --check
generated/ matches the YAML. 7 files validated. Version 1.0.0.

> pytest semantic-layer/tests -q
..................................                                       [100%]
34 passed in 0.95s
```

The inherited suite was run after this build to confirm nothing outside this folder changed: `pytest -q` from the repo root printed `8 passed, 5 warnings`. That run appends `record.read` and `ai.summary` lines to `logs/audit.log`, as it did in S00 and S02.

## Lifecycle

This tree cites `docs/01-discovery/` (all six files), `docs/02-baseline/data-quality-baseline.md`, `docs/02-baseline/defect-list.md`, and `docs/02-baseline/ai-qualification.md`.

Stage S03R reviews this tree before any Phase 4 work. Stages S04-03 (identity), S04-06 (policy), S04-09 (AI guardrails), and S04-12 (FinOps) reuse ids from here. S04-03 builds the policy input model from the five value lists in `access-semantics.yaml`. S04-06 reads the same ids in Rego. S04-09 cites the `ai_use.*` rows and `policy.prompt_fields`. S04-12 cites `metric.tokens_per_invocation` and `metric.cost_per_correlated_incident`.

A Phase 4 or 5 design that needs a term this tree lacks writes an "Open question for S03" line. Stage S05R folds those terms in and raises the version. Stage S06 cites ids at that version. Stage S08 gives that version, unchanged, to the second model.
