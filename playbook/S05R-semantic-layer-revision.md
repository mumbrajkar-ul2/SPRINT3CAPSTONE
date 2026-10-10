# S05R — Semantic layer revision

Phase 5R in `Execution Plan.md`. Runs after S05-14 and before S06. The control designs in Phase 4 and Phase 5 introduce terms, ids, fields, and rules the S03 tree did not have. This stage folds each one into the YAML. The PRD and the second model then receive one meaning set that holds every meaning the modernization introduced.

Why this stage exists. The challenge guide asks that the semantic layer be tested with a new model. The trainer's rule is that if the first model is lost, the semantic layer is the fallback a new model builds from. A meaning that sits only in `docs/03-identity/` through `docs/14-audit/` as Markdown does not reach that new model. S08 attaches `semantic-layer/` and the PRD. It does not attach the design folders.

What goes in: a persona, a resource name, a scope value, a status word, a rule, a metric, a log field, a provenance field, an outcome, an allow-list field. What stays out: Rego text, Python, CI YAML, Terraform, test code. Code is what a model rebuilds from the meaning. The `source:` list on a YAML item may name the code file that implements it.

## Inputs

- `Semantic_Layer_capture.pdf`
- `Project_Intent.md` (sections 6.2, 6.3, Appendix E)
- `playbook/S03R-semantic-layer-review.md` (the fifteen check rows)
- `playbook/README.md` (the failure list)
- `06-telecom-service-network-incident-ops/semantic-layer/` (the whole tree)
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-review.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/docs/03-identity/` through `docs/14-audit/` (every Half A design file)
- `06-telecom-service-network-incident-ops/policy/` (to read ids the Rego comments cite)
- `06-telecom-service-network-incident-ops/tests/` (to read ids the tests cite)

## Prompt

```text
# Stage S05R — Semantic layer revision

## Objective
Collect every term, id, field, status word, persona, metric, rule, and outcome that the Phase 4 and Phase 5 designs introduced or needed and the YAML lacks. Fold each one into `semantic-layer/` with a source list. Raise the version. Rebuild. Rerun the tests. Rerun the S03R check rows. Record the diff. After this stage the YAML holds every meaning the modernization introduced, and no later stage changes it without an ADR.

## Scope
Include: every file under `semantic-layer/`; every Half A design file under `docs/03-identity/` through `docs/14-audit/`; `docs/02-baseline/semantic-layer-review.md`; ids cited in `policy/` comments and in `tests/`.
Exclude: application code; Rego text; CI YAML; Terraform; test code; any term that no design, policy, or test asks for; any change to the meaning of an id that already exists.

## Required analysis
1. Collect. Search every Half A design file, the S03R review, the Rego comments, and the tests for: the phrase "Open question for S03"; any term, id, status word, persona, resource, scope value, metric, or field the file uses that does not resolve in the YAML; any "Fixes required" row from S03R still open. Write one table. Columns: source file and line; the term or id as the design wrote it; what the design needs it for; which YAML file it belongs in; decision.
2. Decide. The decision is one of: add (new id); alias (the design used a different word for an id that exists; add the alias, keep the id); reject (the design can use an existing id; name it); defer (not a meaning; it is code, a number, or an open business question; name the owner). Every row has a decision and a one-sentence reason.
3. Fold. For each add or alias: write the item in its YAML file with a stable dot-form id, a plain-speech `description:`, a `source:` list that names the design file and the repo file or test it came from, and `proposed: true` with `owner:` when the term is not in the inherited repo. Add a glossary entry in everyday words. Add the schema rule if the item needs a new shape. Add a test row if the item is required.
4. Protect existing ids. Do not remove or rename an id that `apps/`, `policy/`, `tests/`, or `docs/` cite. If an id must change, keep the old id with `deprecated: true` and `replaced_by:`. Grep for every id you touched and list each file that cites it.
5. Version. Raise `version:` in every YAML file and in `README.md`. Use one new value for the whole tree, for example `1.1.0`. Add one row to the README change log: date, old version, new version, the number of ids added, and the design stages that caused them.
6. Rebuild and test. Delete `generated/`. Run `python semantic-layer/build.py`. Run `pytest semantic-layer/tests -q`. Paste both outputs.
7. Rerun S03R. Write rows R1 to R15 and failure-list rows 1 to 8 against the revised tree, in the same form S03R used. For every FAIL, write a numbered "Fixes required" list in the S03R form: the check ids it clears, the files and lines or ids, the change, and "Choice needed" with the options when the owner must decide.
8. Diff. Record the change per file: ids added, aliases added, ids deprecated, glossary entries added, schema rules added, tests added. If the folder is a git repository, also paste `git diff --stat -- semantic-layer/`.

## Evidence rules
- Every YAML item added carries a `source:` list of file paths.
- Every item not in the inherited repo carries `proposed: true` and `owner:`.
- Label claims: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file path with line, a YAML id, or a test name.

## Constraints and guardrails
- The tree stays exactly the capture-PDF tree plus `generated/` and `build.py`. Add no file.
- Do not change the meaning of an existing id. Add a new id instead.
- Do not add a term no design, policy, or test asked for.
- No AI use may gain execute agency. The agency and approval point per AI use still match `docs/02-baseline/ai-qualification.md`.
- No invented cutoff, threshold, or target number. PROPOSED with owner only.
- A design file that used a provisional word may gain one line: "Resolved in S05R as <id>." Make no other change to Phase 4 or 5 files.
- Redact secrets. No password, key, or token value anywhere in the tree.
- Plain speech. Short sentences. Everyday words.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md 4.3 and the S03 prompt; read, do not re-derive)
| Constant | Value |
|---|---|
| Entities | devices, circuits, alarms, incidents, service_orders, ai_invocations, events |
| Personas | noc_operator, network_engineer, field_engineer, customer_support, automation_service, vendor_account, ai_agent |
| Access fields | role, resource, purpose, scope, risk |
| Four AI outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Fields never in a prompt | mgmt_ip, credential_profile |
| Log fields (S04-08) | ts, correlation_id, actor, role, action, resource, policy_decision, approval_id, model, model_version, prompt_hash, tokens, latency_ms, outcome |
| Provenance groups (S05-14) | actor, request, data used, model, policy, approval, final action, trace, cannot be proven |
| S03 version | 1.0.0 |

## Required artifacts
1. The revised files under `06-telecom-service-network-incident-ops/semantic-layer/`, with the new version in every YAML file and in `README.md`, and one new row in the README change log.
2. `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md` — the collection table with decisions, the fold list per YAML file, the build and test output, the fifteen S03R rows and eight failure-list rows, the id-citation check, and the diff.

## Completion gate
PASS when every collected row has a decision and a reason, every add or alias is in the YAML with a source list and a glossary entry, the build and the tests pass, every S03R row is PASS, no cited id lost its meaning, and the new version is in every YAML file and the README. CONDITIONAL PASS when a deferred row names an owner, or when the only FAIL rows are R12 or R15 with a one-line fix. BLOCKED when a test fails, a YAML file is missing, an id that code or tests cite was removed, or any AI use has execute agency.

## Lifecycle linkage
Cite `docs/02-baseline/semantic-layer-review.md`, the Phase 4 and 5 design files by path, and `docs/02-baseline/ai-qualification.md`. If a rerun row is FAIL, stage S03F applies this file's "Fixes required" list and keeps this version. Then S03R runs again in a fresh chat. S06 starts when that review reads PASS, or CONDITIONAL PASS with fixes applied. Stage S06 writes the version string from this stage into the PRD header and cites ids at this version. Stage S07 builds against this version. Stage S08 hashes this version and hands it to the second model unchanged. After this stage, a YAML change needs an ADR under `docs/ADR/` that names the id and the reason.

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
| `semantic-layer/*.yaml` | New `version:` on every file. New ids with `source:` lists. Deprecated ids kept with `replaced_by:`. |
| `semantic-layer/glossary.md` | One entry per new id, in everyday words. |
| `semantic-layer/README.md` | New version. Change log row: date, old version, new version, ids added, stages that caused them. "Last build" output from this stage. |
| `semantic-layer/schemas/semantic-layer.schema.json` | Rules for any new shape. Still validates every YAML file. |
| `semantic-layer/tests/test_semantic_layer.py` | A row for each new required item. All tests pass. |
| `docs/02-baseline/semantic-layer-revision.md` | Header. Collection table with decision per row. Fold list per YAML file. Build and test output. Fifteen S03R rows and eight failure-list rows. Numbered "Fixes required" list for every FAIL. Id-citation check. Diff. |

## Done test

Pick one "Open question for S03" line from `docs/03-identity/`. Its id resolves in a YAML file with a `source:` list and a glossary entry. Delete `generated/`, run `build.py`, run the tests. Everything passes. The version in `README.md` is higher than `1.0.0`, and the same string is in every YAML file. The S06 PRD header will cite that string.
