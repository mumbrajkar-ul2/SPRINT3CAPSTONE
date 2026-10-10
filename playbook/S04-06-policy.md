# S04-06 — Policy as code (Challenge 6)

Phase 4 in `Execution Plan.md`. Two halves. Half B starts only after you reply "Half A accepted". This is where one high-risk decision becomes an executable policy with allow and deny tests.

## Inputs

- `Project_Intent.md` (sections 5.3, Appendix C)
- `06-telecom-service-network-incident-ops/policy/opa/access.rego`
- `06-telecom-service-network-incident-ops/semantic-layer/access-semantics.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/business-rules.yaml`
- `06-telecom-service-network-incident-ops/semantic-layer/ai-context-policy.yaml`
- `06-telecom-service-network-incident-ops/docs/03-identity/policy-input-model.md`
- `06-telecom-service-network-incident-ops/docs/03-identity/target-access-matrix.md`
- `06-telecom-service-network-incident-ops/docs/02-baseline/ai-qualification.md`
- `06-telecom-service-network-incident-ops/apps/api/main.py`

## Prompt

```text
# Stage S04-06 — Policy as code (Challenge 6)

## Objective
Half A: design the policy catalogue and the `ai_action` policy that decides RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, or EXECUTE. Half B: write the Rego, the fixtures, the tests, and wire the API to call the policy on every record read and every AI recommendation.

## Scope
Include: access policy inputs (role, resource, purpose, scope, risk) from S04-03; the AI action decision; exception handling; policy tests.
Exclude in Half A: any code change. Exclude in Half B: new routes beyond the policy call (S07); prompt changes (S04-09).

## Required analysis (Half A)
1. Policy catalogue: five policy areas (access, AI approval, data use, operational safety, production readiness). Per area: the decision it controls, the inputs, the YAML rule ids it enforces, whether it exists today.
2. ai_action policy design: inputs (persona, action, resource, risk, approval_id, policy_version, stale_topology_flag, output_schema_ok, timeout_hit); outcome table that maps input conditions to the four outcomes; EXECUTE requires policy allow, an approval_id when approval_required is true, and an audit row written first; BLOCK when a forbidden field was in the prompt or the actor may not recommend; HOLD_FOR_REVIEW on timeout, schema failure, or stale topology.
3. Example inputs: at least one allow and one deny JSON fixture per policy area, written out in full.
4. Exception-handling model: who may waive a rule, for how long, where the waiver is logged, how it expires. Unknown where the repo is silent, with PROPOSED and owner.
5. The high-risk decision to prove: "an AI remediation recommendation becomes a change". Write its allow case and its deny case in words.
For each finding: finding, evidence, impact, risk, confidence, open questions.
STOP after Half A. Return the seven-item final response. Wait for "Half A accepted".

## Required work (Half B, after acceptance)
1. Extend `policy/opa/access.rego` to use resource, purpose, scope, and risk from the S04-03 input model. Keep the file readable; comment each rule with its YAML rule id.
2. Add `policy/opa/ai_action.rego` that returns one of the four outcomes.
3. Add fixtures under `policy/tests/fixtures/` (the JSON from Half A) and tests under `policy/tests/`. If the `opa` binary is present, write `*_test.rego` and run `opa test`. If it is absent, write `policy/tests/test_policy_python.py`, a small evaluator that applies the same decision table to the same fixtures, and record the binary gap as Unknown.
4. Add `apps/api/services/policy.py` that evaluates the policy (via `opa eval` when present, else the Python evaluator) and call it from `/records/{id}` and from the AI route. Deny returns 403 and writes an audit row.
5. Run the tests. Record in `docs/06-policy/evidence.md`.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, Unknown.
- A Verified Fact names a file, a YAML id, a fixture name, or a test name.
- Test output is REAL.

## Constraints and guardrails
- Plain speech. Comments in Rego use plain speech too.
- No EXECUTE outcome may be reachable without approval_id and an audit row. Write a test that proves it.
- No invented threshold. The policy decides on named inputs, not on a numeric cutoff, unless the cutoff is PROPOSED with an owner and marked so in the Rego comment.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.
- If this design needs a term, id, status word, persona, resource, scope value, metric, or field the YAML lacks, do not define it here. Write one line that starts with "Open question for S03:" and names the term and what this design needs it for. Stage S05R folds it into the YAML.

## Locked facts (read, do not re-derive)
| Item | Value |
|---|---|
| OPA rules today | any admin; operator + read |
| OPA called by the API today | No |
| Four outcomes | RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, EXECUTE |
| Irreversible action | live network change; a human approves it |
| Policy inputs (S04-03) | role, resource, purpose, scope, risk |

## Required artifacts
Half A, under `06-telecom-service-network-incident-ops/docs/06-policy/`:
1. `policy-catalogue.md`
2. `ai-action-policy-design.md` (with the outcome table)
3. `example-inputs.md` (allow and deny JSON per area)
4. `exception-handling-model.md`
Half B:
5. `policy/opa/access.rego` (extended), `policy/opa/ai_action.rego`
6. `policy/tests/fixtures/*.json`, `policy/tests/*_test.rego` or `policy/tests/test_policy_python.py`
7. `apps/api/services/policy.py` and the two call sites in `main.py`
8. `docs/06-policy/evidence.md`

## Completion gate
Half A PASS when the outcome table covers every input combination the design names and the high-risk decision has an allow case and a deny case in words. Half B PASS when "an AI remediation recommendation becomes a change" has a passing allow test and a passing deny test, and a test proves EXECUTE is unreachable without approval_id. CONDITIONAL PASS when the opa binary is absent and the Python evaluator ran instead, with the gap recorded. BLOCKED when any fixture reaches EXECUTE without approval_id.

## Lifecycle linkage
Cite docs/03-identity/policy-input-model.md, docs/02-baseline/ai-qualification.md, and YAML ids. Stage S04-09 calls ai_action from the gateway. Stage S05-13 collects the policy tests. Stage S07 relies on policy.py in every route. Stage S09 cites the allow and deny tests as D4 proof.

## Required final response (after each half)
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
| `policy-catalogue.md` | Header. Five areas with decision, inputs, rule ids, exists-today. |
| `ai-action-policy-design.md` | Header. Input list. Outcome table. EXECUTE conditions. |
| `example-inputs.md` | Header. At least ten JSON fixtures, allow and deny per area. |
| `exception-handling-model.md` | Header. Who, how long, where logged, expiry. |
| Rego files | Comments with rule ids. |
| Policy tests | Allow and deny for the high-risk decision. EXECUTE-unreachable test. |
| `policy.py` + call sites | Deny returns 403 and writes an audit row. |
| `evidence.md` | Header. Test output. Binary present or absent. |

## Done test

Send an AI recommendation input with `approval_id` empty and `action: execute`. The policy returns BLOCK or HOLD_FOR_REVIEW, never EXECUTE. The test that proves this is in the suite.
