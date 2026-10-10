# S08 — Second model and app comparison (product path steps 5 and 6, D7)

Phase 8 in `Execution Plan.md`. The same semantic layer and PRD go to a different model. The two apps are compared. The YAML does not change during the test.

This stage has three parts. Part 1 writes the brief (first model). Part 2 is run in a new chat with the second model selected; paste the brief. Part 3 compares (first model or you).

## Inputs

- `06-telecom-service-network-incident-ops/semantic-layer/` (whole tree, unchanged since S05R)
- `06-telecom-service-network-incident-ops/docs/02-baseline/semantic-layer-revision.md` (the version string to confirm)
- `06-telecom-service-network-incident-ops/docs/prd/prd.md`
- `06-telecom-service-network-incident-ops/docs/prd/traceability.md`
- `06-telecom-service-network-incident-ops/tests/` (semantic-layer, policy, guardrail, app tests)
- `06-telecom-service-network-incident-ops/docs/demo/evidence.md`

## Part 1 prompt — write the brief (first model)

```text
# Stage S08 Part 1 — Second-model brief

## Objective
Write the brief that a second, different model will receive. The brief gives the unchanged semantic-layer tree and the PRD and asks for an application in apps/api_model_b/. It must not add a private glossary, a hint, or a worked example beyond what the PRD contains.

## Scope
Include: file list to attach; the build task; the tests the result must pass; the output paths.
Exclude: any definition of a term; any route or behaviour not in the PRD; any mention of how the first app solved something.

## Required work
1. Record the SHA-256 of every file under semantic-layer/ and of prd.md in docs/model-comparison/yaml-hashes-before.md. Record the `version:` string from semantic-layer/README.md on the same page. It must equal the version in docs/02-baseline/semantic-layer-revision.md and in the prd.md header. If it does not, stop; the tree changed after S05R without an ADR.
2. Write docs/model-comparison/second-model-brief.md with: the model name to use (fill in); the files to attach; the task ("build the application the PRD describes, under apps/api_model_b/, using only the terms and ids in semantic-layer/"); the tests it must pass (list file paths); the rule that it may not edit semantic-layer/ or prd.md; the required final response (the seven items).

## Constraints and guardrails
- Plain speech.
- The brief is the only text the second model gets besides the attached files.
- Each doc starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Required final response
1. Stage status. 2. Key findings. 3. Major risks. 4. Assumptions and unknowns. 5. Artifacts created. 6. Blocking issues. 7. Recommended next action.
```

## Part 2 — run the brief (second model, new chat)

1. Open a new Cursor chat. Select the second model.
2. Attach `semantic-layer/`, `docs/prd/prd.md`, `docs/prd/traceability.md`, and the test files the brief lists.
3. Paste the full text of `docs/model-comparison/second-model-brief.md`.
4. Save the whole chat output into `docs/model-comparison/second-model-run-log.md` (redact secrets).
5. Do not answer questions from the second model with new meaning. If it asks what a term means, reply "use the glossary and YAML only" and record the question in the run log.

## Part 3 prompt — compare (first model)

```text
# Stage S08 Part 3 — App comparison

## Objective
Compare apps/api/ and apps/api_model_b/ against the same semantic layer and PRD. Decide whether meaning drifted.

## Scope
Include: both apps; the shared tests; the run log; the YAML hashes.
Exclude: fixing either app; changing the YAML.

## Required analysis
1. Confirm the SHA-256 of every file under semantic-layer/ and prd.md is unchanged. Write docs/model-comparison/yaml-hashes-after.md and compare.
2. Run the same suites against both apps: semantic-layer tests, policy tests, guardrail tests, app tests. Record pass and fail counts per suite per app.
3. Compare, one table per item: status words used (any word not in status-taxonomy.yaml is drift); rule ids honoured (grep both apps for rule. ids); routes built versus the PRD list; test pass counts; guardrail outcomes on the same abuse inputs (hostname injection, mgmt_ip present, timeout); latency and token cost on the same calls (labels); places where the second model invented meaning (quote the run log).
4. Verdict: did meanings drift? Where did the apps differ, and does the difference matter to a user? What did the YAML prevent, and what did it fail to prevent?
For each finding: finding, evidence, impact, risk, confidence, open questions.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file, a test name and result, a hash, or a run-log line.
- Test counts and timings are REAL.

## Constraints and guardrails
- Plain speech.
- Do not edit semantic-layer/ or prd.md. If the comparison shows the YAML needs a change, write it as an open question for a later ADR.
- Each doc starts with a header table.

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/model-comparison/yaml-hashes-after.md`
2. `06-telecom-service-network-incident-ops/docs/model-comparison/app-comparison.md`

## Completion gate
PASS when the hashes match, both apps ran the shared suites, every comparison table is filled, and the verdict is written. CONDITIONAL PASS when the second app failed some tests and the failures are explained. BLOCKED when any semantic-layer file or prd.md changed during the test.

## Lifecycle linkage
Cite docs/model-comparison/second-model-brief.md, second-model-run-log.md, yaml-hashes-before.md. Stage S09 cites the verdict. Stage S10 answers defence question 9 from here.

## Required final response
1. Stage status. 2. Key findings. 3. Major risks. 4. Assumptions and unknowns. 5. Artifacts created. 6. Blocking issues. 7. Recommended next action.
```

## Expected output

| File | Must contain |
|---|---|
| `yaml-hashes-before.md`, `yaml-hashes-after.md` | Header. One hash per file. Match column. |
| `second-model-brief.md` | Header. Model name. Files. Task. Tests. No-edit rule. Final response shape. |
| `second-model-run-log.md` | Full chat output, redacted. Questions the model asked. |
| `app-comparison.md` | Header. Seven comparison tables. Verdict. |
| `apps/api_model_b/` | The second app. |

## Done test

Hashes match before and after. `app-comparison.md` names at least one place where the two apps differ and says whether the YAML prevented drift there.
