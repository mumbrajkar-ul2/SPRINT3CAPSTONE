# Operating contract

| Field | Value |
|---|---|
| Stage | S0B — Operating contract (Execution Plan Phase 0B; spine stage 0B) |
| Date / version | 2026-10-09, v1.0. 2026-10-10, v1.1: row 10 added (Team-Force owns every PROPOSED item). |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PROVISIONAL. Rows 1, 5, and 7 still need the owner named in the table to confirm them. The other rows are the working rules until that confirmation. |
| Evidence sources | `Project_Intent.md` sections 2.3, 2.7, 3.1, 4.2, 4.3, 4.4, Appendix B, Appendix C; `Execution Plan.md` Phase 0B, Phase 4, Phase 7; `playbook/S04-04-secrets.md`; `docs/00-setup/replay-log.md`; `apps/api/services/ai_gateway.py`; `data/manifest.json` |
| Assumptions | This workspace is the only system under change. The data on disk is local and synthetic. Mangesh (FDE) is the person who accepts each stage of this assignment. |
| Unresolved issues | Team-Force, the owner in row 10, is the FDE team Mangesh belongs to. Its other members are Unknown. No second person is named to approve a code change. The job title of the human who may approve a live network change is not named. Whether the Angular scaffold is wired is not decided. Whether a CSV column may ever change is not confirmed. |
| Residual risks | Under row 10, the team that proposes an item also owns it. No business owner outside the FDE team checks the business numbers. Stage S09 should list this as an accepted risk. A later stage can treat the summarize JSON as a work order. The audit row from the replay has no approval id, so nothing in today's log can prove a human agreed. |

## What this file is

This file says what the transformation may change, what it must leave alone, who accepts a change, and what stops the work. It is written before the deep read of the repo. It does not decide which desk job uses a model. That decision is stage S2Q.

Stage S09 reads this file and lists any change that crossed a Prohibited row or a PROVISIONAL row.

## The ten answers

The status word is Allowed, Prohibited, or PROVISIONAL. PROVISIONAL means the packet does not settle the point, the working rule below is in force, and the named owner must confirm it.

| # | Question | Status | Working rule | Owner who must confirm | Evidence |
|---|---|---|---|---|---|
| 1 | May database or CSV schemas change? | PROVISIONAL | Leave the six CSV column sets as they are. The files are `devices.csv`, `circuits.csv`, `alarms.csv`, `incidents.csv`, `service_orders.csv`, and `ai_invocations.csv` under `data/synthetic/`. Each file has 354 data rows in `data/manifest.json`. The running API reads `devices.csv` only. A later semantic-layer schema is a new file under `semantic-layer/`. The CSV columns stay as they are until you confirm a change. | Mangesh (FDE) | Verified Fact: `Project_Intent.md` 4.3; `data/manifest.json` key `csv_files`. Inference: `Execution Plan.md` never lists an edit to those columns. |
| 2 | May API routes be added, changed, or removed? | Allowed | Add only the routes `Project_Intent.md` 2.7 names: `GET /alarms/storms/{storm_batch_id}`, `POST /ai/recommend/{id}`, and `POST /approvals/{id}`. `GET /records/{id}` may change so a missing id returns 404. `POST /ai/summarize/{id}` stays. Harden it. Do not remove it. Do not add a route for qualify, provision, retry, rollback, or a check that a fix worked. An execute route waits until four gates exist together: a policy allow, a human approval id, an audit row written first, and a reversible validated change. The PRD must name a route before stage S07 adds it. | Mangesh (FDE), at the S06R review of the PRD | Verified Fact: `Project_Intent.md` 2.7 and Appendix C. |
| 3 | May `apps/api/services/ai_gateway.py` change? | Allowed | Yes, from stage S04-09 onward, after S2Q. The change adds an allow-list of prompt fields, a fixed output shape, a timeout, a stale-topology check, and a path that returns the case to a person when the call fails. Stage S07 may add the recommend call on the same file. The file must not gain an execute path. This stage does not edit the file. Today the file sets model `local-sim-v1`, waits 0.01 seconds, and returns `guardrail_status` `not_enforced`. | Mangesh (FDE) | Verified Fact: `ai_gateway.py` lines 3 to 17; `Project_Intent.md` 2.7; `Execution Plan.md` Challenge 9. |
| 4 | May `legacy/reconcile_legacy.py` change? | Allowed | Yes, at stage S04-04 Half B, for one purpose: the shared database password leaves the source file and the script reads it from the environment. Do not copy that password into a new file. Write `<redacted>` if a note must mention it. Keep the device-row count behaviour until stage S02 has recorded it. Stage S09 checks the edit against this row. | Mangesh (FDE) | Verified Fact: `Project_Intent.md` 4.2 and 4.3; `playbook/S04-04-secrets.md` Half B item 3. |
| 5 | Is the Angular scaffold under `apps/web/` in scope? | PROVISIONAL | It is in scope to read and to describe. The demo page is a small page served with the API. The scaffold stays a scaffold. Wire it only if stage S07 still has time and the owner below confirms the wiring in writing first. `apps/web` does not open in a browser today. | Mangesh (FDE), at stage S07 | Verified Fact: `Project_Intent.md` 2.7 and 4.2; `Execution Plan.md` Phase 7. |
| 6 | Are the files under `data/synthetic/` read-only? | Prohibited | Writes are prohibited. Read them for discovery, the baseline, and the cost view. The live gateway does not write `ai_invocations.csv`. | Mangesh (FDE) | Verified Fact: `Project_Intent.md` 2.7. Inference: no phase in `Execution Plan.md` lists an edit under `data/synthetic/`. |
| 7 | Who approves a code change before it merges? | PROVISIONAL | Mangesh (FDE) reviews the diff and accepts it before it is kept in this workspace. Stage S03R is the human review of the semantic layer, before any S04 code change. Stage S06R is the human review of the PRD, before the app is built. A second code reviewer is not named in the packet. | Mangesh (FDE) must confirm that one reviewer is enough for this assignment. | Verified Fact: `Execution Plan.md` section 8 names S03R, S06R, and the approvals route. Unknown: any second reviewer. |
| 8 | What condition stops the work? | Prohibited | Stop when the next change would push a device config, provision a circuit, run an automated remediation, or close an incident in a way that hides a real outage. Stop when the next change needs a production login, a live device, or a hosted-model call that stage S2Q has not named. Stop when the next change would edit a Prohibited row in this table. | Mangesh (FDE) stops the work and does not continue past the stop. | Verified Fact: `Project_Intent.md` 3.1 row 3; section 4.4 (no cloud account is required). |
| 9 | What is the irreversible action, and where must a human approve it? | Prohibited | The action is a live network change: a config push, an automated remediation, a provisioning change, or closing an incident that hides a real outage. A named human approves it before the change, and the system stores an approval id. The approval sits after a policy allow and before the change. The approver is a named human. The model text and the `automation_service` account leave that id empty. `POST /ai/summarize/{id}` returns the sentence "Review and approve before action" and `guardrail_status` `not_enforced`. That call writes an audit row with the record id and the model name. The audit row has no approval id. The stored approval id is the human approval. The model text stays a recommendation. No route writes that id today. | The approver is a named human. Which desk job that human holds is PROVISIONAL. Mangesh (FDE) confirms the job title when stage S04-09 writes the approval steps. The approval point in this row is already fixed. | Verified Fact: `Project_Intent.md` 3.1 row 3; Appendix C; `docs/00-setup/replay-log.md` sections 2.7 and 3. |
| 10 | Who owns a PROPOSED item: a business decision the packet leaves open, or a design proposal? | PROVISIONAL | Team-Force owns every PROPOSED item. Team-Force is the FDE team that Mangesh belongs to. It owns two kinds of item. (a) A business decision the packet leaves open: a number, a range, a cutoff, a target, an allowed list of words, or a legal value. Examples are the retry bound of 1000, the `sla_breach_risk` range of 0 to 1, the number of alarms that make a storm, the order of the severity words, and the model timeout. (b) A design proposal: a persona grant, a purpose, a scope, the prompt allow list, the output schema, or a proposed desk job. Write `Owner: Team-Force` next to the word PROPOSED, or `owner: Team-Force` in YAML. Naming the owner does not approve the item. It stays PROPOSED until Team-Force accepts it in writing. Mangesh (FDE) acts for Team-Force. He writes each stage, reviews each diff (row 7), and confirms rows 1 to 9. This row does not change row 9. A live network change still needs one named human to write the approval id. A team name is not an approver. | Mangesh (FDE) set this working rule on 2026-10-10. A business owner named by the packet or the trainer replaces Team-Force for the business decisions in (a). | Verified Fact: decisions by Mangesh (FDE) in chat on 2026-10-10, logged in `transcript/chat_transcript.md`. Unknown: the other members of Team-Force. |

Worked example for row 9. On 2026-10-08 the replay called `POST /ai/summarize/REC-0001` with no role header. The body had `model` `local-sim-v1`, `recommendation` "Review and approve before action", `token_estimate` 64, and `guardrail_status` `not_enforced`. The audit line stored `record_id` and `model` only. A later worker that opens a change ticket from that JSON has turned a recommendation into an operational decision. This contract forbids that step. The human approval is the stored approval id, and that id is absent from the replay log.

## What may be written

This stage may add files under `docs/00-contract/` only. It does not edit application code, tests, CSV files, or configuration.

Later stages may edit a file only when the row above says Allowed, the named owner has accepted the change, and the stage that names the edit has started. A PROVISIONAL row stays closed until the owner confirms it in writing.

## Data use

The files under `data/synthetic/` are synthetic lab data. They stay on this machine. Read them. Do not edit them (row 6). Do not send a row to a hosted model unless stage S2Q names that call and the cost file labels the new numbers. `Project_Intent.md` section 4.4 says no cloud account is required to read or run the inherited repo.

`mgmt_ip` and `credential_profile` are on the device row the API returns today. A later prompt allow-list keeps them out of prompts and logs. This contract does not design that allow-list. It records that those fields are already in the replay response (`docs/00-setup/replay-log.md` section 2.2).

## Production access

Production access is Prohibited. There is no production login, no live device, and no cloud account in this packet. A task that needs one hits the stop in row 8.

## Stop conditions

1. The next edit would push a config, provision a circuit, apply an automated fix, or close an incident so that a real outage is hidden.
2. The next edit needs a production system, a live device, or a secret that is not a placeholder.
3. The next edit would call a hosted model before stage S2Q names that call.
4. The next edit would change a CSV column, a row under `data/synthetic/`, or any other Prohibited row.
5. The next edit would copy the shared database password, or any other secret, into a new file. Write `<redacted>` in notes.

When a stop hits, Mangesh (FDE) writes the blocked step in the stage output and does not do the step.

## Approval chain

The chain has two tracks. A code change and a live network change use different approvals.

Code and document track:

1. Stages S00, S0B, S01, and S02 write documents and, at S02, characterization tests. They do not change the running routes. S00 already ran. This file is S0B.
2. Stage S2Q decides which capability uses a model and revises `cost-envelope.md`. It does not change application code.
3. Stage S03R is a human review of the semantic layer. Mangesh (FDE) accepts it before any S04 chat starts.
4. Stages S04 and S05 may change code only inside the Allowed rows. Mangesh (FDE) reviews each diff before it is kept.
5. Stage S06R is a human review of the PRD. Mangesh (FDE) accepts it before stage S07 builds routes.
6. Stage S09 compares the diff with this contract.

Live network track:

1. The current code has no execute path. `Project_Intent.md` 3.1 row 3 locks that fact.
2. A live network change waits for a policy allow, a human approval id, an audit row written first, and a reversible validated change.
3. The human approval is the stored approval id in row 9. The summarize sentence stays a recommendation.
4. Stage S07 may add `POST /approvals/{id}` so a named person can record approve or reject. That route writes the audit row. It does not push a change.

## Lifecycle

This file cites `Project_Intent.md` 2.3 (the hand-back list), 3.1 (the eight decisions, including the irreversible action), and 4.3 (the constants already in the repo). It cites `docs/00-setup/replay-log.md` for what the three routes do today. Stage S2Q revises the cost envelope and does not reopen a Prohibited row by itself. Stage S09 checks every change against this contract.
