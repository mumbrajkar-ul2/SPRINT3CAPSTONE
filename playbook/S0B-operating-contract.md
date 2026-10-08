# S0B — Operating contract, cost envelope, and crosswalk

Phase 0B in `Execution Plan.md`. Spine stages 0B and 0C. This stage writes down what the work may change before anything is read in depth. It also writes the first cost view and the challenge-to-spine crosswalk.

## Inputs

- `Project_Intent.md` (sections 2.3, 3.1, 4.3, Appendix B)
- `AI-FDE_Brownfield_Repo_Transformation_Challenge_Guide.pdf`
- `How the product spine addresses the 16 challenges - plain speak.md` (for the crosswalk)
- `06-telecom-service-network-incident-ops/docs/00-setup/replay-log.md`
- `06-telecom-service-network-incident-ops/data/synthetic/ai_invocations.csv`
- `06-telecom-service-network-incident-ops/data/synthetic/events.jsonl`
- `06-telecom-service-network-incident-ops/apps/api/services/ai_gateway.py`

## Prompt

```text
# Stage S0B — Operating contract, cost envelope, and crosswalk

## Objective
Write the operating contract for this transformation: what may change, what may not, who approves, and what stops the work. Write a provisional cost envelope from the figures that exist in the repo. Write the crosswalk that maps each challenge folder to the 42-stage spine folders.

## Scope
Include:
- Repository write boundaries, data use, production access, human approval triggers, stop conditions.
- A provisional cost view with three scenarios: deterministic rules, conventional automation, a hosted model.
- The crosswalk table.
Exclude:
- Any decision about which capability uses AI. That is stage S2Q.
- Any code or test change.

## Required analysis
Answer each operating-contract question with Allowed, Prohibited, or PROVISIONAL plus the owner who must confirm:
1. May database or CSV schemas change?
2. May API routes be added, changed, or removed?
3. May `apps/api/services/ai_gateway.py` change?
4. May `legacy/reconcile_legacy.py` change?
5. Is the Angular scaffold under `apps/web/` in scope?
6. Are the files under `data/synthetic/` read-only?
7. Who approves a code change before it merges?
8. What condition stops the work (for example: a change would push to a live device)?
9. What is the irreversible action, and where must a human approve it?
For the cost envelope: count rows and sum `token_count` in `ai_invocations.csv`; sum the cost fields in `events.jsonl` by `event_type`; note that `local-sim-v1` is a stub with no real cost. For each scenario state what is known, what is Unknown, and the honesty label of every number.
For the crosswalk: one row per challenge folder `docs/01-discovery` to `docs/16-evidence-pack`, listing the spine stage ids and folder names that cover the same ground, and a Match / Partial / None verdict.

## Evidence rules
- Label every claim: Verified Fact, Inference, Assumption, or Unknown.
- A Verified Fact names a file path, a command, or a replay result.
- Every number carries one honesty label: REAL, PRECOMPUTED, SIMULATED, or EDUCATIONAL. Write Unknown where the repo has no figure.

## Constraints and guardrails
- Plain speech. Short sentences. Everyday words.
- Do not invent a budget, a rate card, or a cutoff. Mark a proposal PROPOSED with an owner.
- Redact secrets. Write <redacted> for any password, key, or token.
- Each artifact starts with a header table: Stage, Date / version, Author, Status, Evidence sources, Assumptions, Unresolved issues, Residual risks.

## Locked facts (from Project_Intent.md; read, do not re-derive)
| Fact | Value |
|---|---|
| Irreversible action | A live network change: config push, automated remediation, provisioning change, or closing an incident that hides a real outage |
| Current execute path | None exists. AI summarize can still recommend with guardrail_status not_enforced |
| AI model version | local-sim-v1 (stub; sleeps 0.01s; synthetic summary) |
| Token estimate formula | len(prompt.split()) * 2 (EDUCATIONAL) |
| CSV row counts / event count | 354 each / 3000 |
| Deliverables | D0 to D8 plus presentation |

## Required artifacts
1. `06-telecom-service-network-incident-ops/docs/00-contract/operating-contract.md` — the nine answers as a table, plus the stop conditions and the approval chain.
2. `06-telecom-service-network-incident-ops/docs/00-contract/cost-envelope.md` — three scenarios, every number labelled, Unknown rows kept visible. Mark the file PROVISIONAL; stage S2Q will revise it.
3. `06-telecom-service-network-incident-ops/docs/00-contract/challenge-to-spine-crosswalk.md` — sixteen rows plus rows for `00-setup` and `00-contract`.

## Completion gate
PASS when every write boundary is Allowed, Prohibited, or PROVISIONAL with an owner, and no number in the cost envelope lacks an honesty label. CONDITIONAL PASS when one boundary is PROVISIONAL with no owner named yet. BLOCKED when the irreversible action or its approval point is not written.

## Lifecycle linkage
Cite `Project_Intent.md` 2.3, 3.1, 4.3 and `docs/00-setup/replay-log.md`. Stage S2Q revises the cost envelope. Stage S09 checks every change made against this contract.

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
| `docs/00-contract/operating-contract.md` | Header table. Nine-row answer table with Allowed / Prohibited / PROVISIONAL and owner. Stop conditions. The irreversible action and its human approval point. |
| `docs/00-contract/cost-envelope.md` | Header table. Three scenarios. Token and cost sums with REAL / PRECOMPUTED / SIMULATED / EDUCATIONAL labels. Unknown rows. Status PROVISIONAL. |
| `docs/00-contract/challenge-to-spine-crosswalk.md` | Header table. Eighteen rows (00-setup, 00-contract, 01 to 16). Spine stage ids and folder names per row. Match / Partial / None verdict. |

## Done test

A reader can answer "may the AI gateway change, and who approves it?" from the contract alone. Every number in the cost envelope has a label.
