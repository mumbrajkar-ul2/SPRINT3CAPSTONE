# Approval workflow

| Field | Value |
|---|---|
| Stage | S04-09 — AI security and guardrails (Challenge 9), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | CONDITIONAL PASS. The workflow names who approves, what they see, where the id is stored, what it unlocks, and how a person contests a sentence. No approval store exists. This stage does not add the approvals route. |
| Evidence sources | `docs/02-baseline/ai-qualification.md`; `semantic-layer/ai-context-policy.yaml` (`ai_uses`, `outcomes`, `provenance.approval_id`); `docs/06-policy/ai-action-policy-design.md`; `docs/08-observability/log-schema.md`; `apps/api/main.py`; `apps/api/services/audit.py`; `semantic-layer/access-semantics.yaml` |
| Assumptions | The summarize route in this stage shows text or a hold reason. It does not write an approval id. S07 adds `POST /approvals/{id}`. |
| Unresolved issues | An approval record has no decision field and no approver field in the YAML. The desk job that reads a summary, and the desk job that accepts a next-action sentence, stay PROPOSED. Owner: Team-Force. |
| Residual risks | An id string alone does not prove the person said yes. S04-06 finding AA-02. A rejected id could later pass an execute check if the decision is not stored. |

## What this file is

This file describes the human step around a model sentence. The model writes text. A named person accepts or rejects it. A different named person approves a live device change. The model does neither.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

This half does not confirm the PROPOSED desk jobs. It uses the titles already written in `ai-qualification.md`. The one title a person confirmed is the live-change approver.

## Who approves

| AI use | Agency | Outcome of the model step | Who acts | What they do | Label |
|---|---|---|---|---|---|
| `ai_use.incident_summary` | recommend | `outcome.recommend_only` | `persona.noc_operator` | Reads the account when it is shown. The incident row stays as stored. | PROPOSED. Owner: Team-Force. `ai-qualification.md`, incident summary row. |
| `ai_use.next_action_recommendation` | recommend | `outcome.hold_for_review` | `persona.noc_operator` | Accepts or rejects the sentence before any change ticket exists. | PROPOSED. Owner: Team-Force. Same file, next-action row. |
| `ai_use.configuration_suggestion` | recommend | `outcome.hold_for_review` | `persona.network_engineer` | Accepts or rejects the suggestion before it enters a change plan. | PROPOSED. Owner: Team-Force. Same file, configuration suggestion row. |
| `ai_use.remediation_execution` | execute | `outcome.execute` | `persona.network_engineer` writes the approval. `persona.automation_service` runs the change after that id exists. | Approves a live change. The model does not approve. | Confirmed by Mangesh (FDE) on 2026-10-10. Owner: Team-Force. Same file, remediation execution row. |

The live route is `POST /ai/summarize/{record_id}`. That route is the incident-summary use. Its healthy policy outcome is RECOMMEND_ONLY (row O1). The next-action use is a later route. S07 builds `/ai/recommend` on this gateway. This stage hardens the summarize route and does not add the recommend route.

`persona.ai_agent` may summarize and recommend. It is denied `action.approve` and `action.execute`. **Verified Fact:** `access-semantics.yaml`, `persona.ai_agent` denied list. `persona.automation_service` is denied `action.approve`. It does not write the approval id.

## What the person sees

The person sees the record id, the policy `outcome`, the `reasons`, `model`, `model_version`, and `prompt_hash`.

The person sees `summary` and `recommendation` only when both strings passed the schema and the outcome is one that shows text. RECOMMEND_ONLY shows the account. A next-action HOLD_FOR_REVIEW that came from row O2 shows the sentence so the person can accept or reject it. A HOLD_FOR_REVIEW from timeout, schema failure, or a blank stale flag shows no sentence. `summary` is null. The reason says why.

The person does not see the prompt text. The person does not see `mgmt_ip` or `credential_profile` in the model answer. Those two cells can still appear on `GET /records/{id}` for an allowed reader. That read is checklist SF-02. This workflow does not change it.

Worked example. Role `operator` asks for a summary of `REC-0001`. The flag is false. The answer matches the schema. The person in the noc_operator job sees the account and the outcome RECOMMEND_ONLY. The incident row is unchanged. No approval id is required for that text (`outcome.recommend_only`).

Same person, device `DEV-00003`, flag true. The person sees outcome BLOCK and the reason `failmode.stale_topology_true`. There is no account to accept.

## Where approval_id is stored

| Place | What is stored now | What this stage writes |
|---|---|---|
| Response field `approval_id` | Absent from the stub body. | Null. The model never fills it (`policy.output_schema`, field `approval_id`). |
| Audit column `approval_id` | Null. `audit.py` line 68. `log-schema.md` says S07 fills it. | Null. |
| An approval store | No store and no route. **Verified Fact:** `ai-action-policy-design.md`, unresolved issues. `main.py` has no approvals route. | Nothing. The later route named in the qualification file is `POST /approvals/{id}`. |

The id is a string on `provenance.approval_id`. An empty string and a string of spaces count as empty in the policy (`ai-action-policy-design.md`, input 5).

## What the approval unlocks

Accepting a summary unlocks nothing on the device. The outcome is RECOMMEND_ONLY. The stored rows stay as they are.

Accepting a next-action sentence means a person has said yes to the text. It does not open a change ticket. The qualification row says the acceptance happens before any change ticket exists.

The approval id unlocks a live change only when all of these are true together. They are the fourteen conditions in `ai-action-policy-design.md`, section "EXECUTE conditions". The four gates from `outcome.execute` are the core:

1. The access policy returned allow.
2. A named human wrote an approval id. The writer is `persona.network_engineer`.
3. An audit row was written first.
4. The change is reversible and validated.

The actor that then runs the change is `persona.automation_service`. The summarize route does not send `action.execute`. This stage never returns the outcome word EXECUTE.

`rule.ai_recommendation_needs_policy_approval_audit_before_state_change` states the same order. `enforced_today` is false. Half B enforces the "no EXECUTE from this route" part. It does not add the change.

## How a person contests a recommendation

The noc_operator rejects the next-action sentence. The network_engineer rejects a configuration suggestion. A rejection writes no approval id. No ticket is opened. The device row stays as stored.

There is no contest status word in the YAML. The qualification file already says "accepts or rejects". This design uses those two words and does not add a third.

Open question for S03: an approval record has no decision field and no approver field. S04-06 already filed this. This design needs both so a rejected id cannot unlock EXECUTE, and so the approver can be checked as `persona.network_engineer` for a live change and as `persona.noc_operator` for a next-action sentence.

The summarize route has no reject button in this stage. The person contests a summary by leaving the incident row unchanged. The outcome RECOMMEND_ONLY does not ask for an approval id.

## Steps in order

1. The route checks the role (boundary B1).
2. The gateway builds an allow-list prompt or stops.
3. The policy returns one outcome.
4. If the outcome is RECOMMEND_ONLY, the noc_operator reads the account. Stop.
5. If the outcome is HOLD_FOR_REVIEW from a failure, the person sees the reason and no sentence. Stop.
6. If the outcome is HOLD_FOR_REVIEW because the use is a next-action recommendation (row O2, later route), the noc_operator accepts or rejects the sentence.
7. A live change, later, needs a new approval id from the network_engineer, then the four gates. That path is not this route.

## Findings

| Id | Finding | Evidence | Impact | Risk | Confidence | Open questions |
|---|---|---|---|---|---|---|
| AW-01 | Three human jobs sit on three different rows. Only the live-change job is confirmed. | **Verified Fact.** `ai-qualification.md` rows for incident summary, next-action recommendation, configuration suggestion, and remediation execution. | A summary reader and a change approver are different people. | Treating the noc_operator's reading of a summary as approval to change a device. | High | The two PROPOSED desk jobs stay with Team-Force. |
| AW-02 | No store holds the id. | **Verified Fact.** `audit.py` line 68. No approvals route in `main.py`. | This stage cannot show a stored yes. | An invented id in a client field. The policy reads the id from the server, not from the client (`ai-action-policy-design.md`, input 5). | High | Decision field and approver field. |
| AW-03 | This route's healthy outcome does not need an approval id. | **Verified Fact.** `outcome.recommend_only`: no approval step for the text itself. `ai_use.incident_summary`. | The person reads. The row stays. | A client that treats RECOMMEND_ONLY as a ticket. GR-09 and GR-10 assert no EXECUTE and a policy outcome. | High | None. |

## Lifecycle

Stage S07 adds the approvals route and fills `approval_id`. Stage S10 uses this workflow for the defence questions on approval and on unsafe output. The qualification file is the source for agency and for the approval point on each row above.
