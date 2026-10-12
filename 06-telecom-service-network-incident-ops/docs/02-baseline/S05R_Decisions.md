# S05R decisions for Team-Force

| Field | Value |
|---|---|
| Stage | S05R follow-up. A decision guide for the items that stage S05R left open. |
| Date / version | 2026-10-12, v1.0. Based on semantic layer `1.1.0`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Decided on 2026-10-12 and recorded in `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`. Every decision below is the recommendation, as Mangesh (FDE) asked. One YAML sentence changed (D-16), so the layer is now `1.1.1`. D-03, D-06, and D-08 are decided here and built in stage S07. |
| Evidence sources | `docs/02-baseline/semantic-layer-revision.md` (sections 2 and 11, the deferred list D-01 to D-20); `semantic-layer/*.yaml` at version `1.1.0` (every item with `proposed: true`, found by script on 2026-10-12: 120 items); `docs/` design files named in each item; `apps/api/services/audit.py`, `audit_query.py`, `ai_gateway.py`, `breaker.py`; `policy/opa/policy_data.json`; `docs/08-observability/slo-proposal.md`; `docs/11-reliability/retry-and-circuit-breaker-strategy.md` |
| Assumptions | (1) Team-Force is the owner of every open choice (`docs/00-contract/operating-contract.md` row 10). Mangesh (FDE) decides for Team-Force. (2) A recommendation here is advice. The owner decides. (3) After S05R, any change to the YAML needs an ADR under `docs/ADR/`. So accepting an item is recorded in this file and in ADR 0002. The YAML flag `proposed: true` marks an item that is not in the inherited repo. It stays after acceptance. |
| Unresolved issues | The letters of MAESTRO (D-20) are Unknown. Whether a login system is in scope (D-07) is Unknown. A real model is not in use, so every time and cost number is from a stub. |
| Residual risks | A recommendation to accept a number can make a proposal look measured. Each number below says where it came from. |

Claim labels: **Verified Fact** (read in a file or run), **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/` unless they start with `playbook/`.

## How to use this file

Part 1 has the 20 deferred items. Each one says what it is, why it waits, the options, and my recommendation.

Part 2 has the PROPOSED items. There are 120 in the YAML. They are grouped into 11 bundles (P-01 to P-11), so you decide once for each bundle. Part 2 also covers the matrix rows (P-12) and lists the PROPOSED numbers that sit outside the YAML ids, and the 35 access matrix rows.

Part 3 is a short list of what to decide first.

Each item has a line `Your decision:`. The lines are filled in with the recommended answers (ADR 0002, 2026-10-12).

**What "deferred" means.** The design asked for a new term. S05R did not add it, because no code, test, or policy file uses it yet. Adding it now would describe something that does not exist.

**What "PROPOSED" means.** S05R wrote the item into the YAML. The item is not in the inherited repo. It carries `owner: Team-Force`. Accepting an item removes doubt about it, and the flag stays to show where the item came from. Rejecting an item means it should come out of the YAML, under an ADR.

**Recommendation words.**

| Word | Meaning |
|---|---|
| Decide now | The answer unblocks the next stage. |
| Keep deferred | Wait. Nothing needs it yet. A later trigger is named. |
| Close it | The question can end. No new id is needed. |
| Accept | Keep the item as written. |
| Accept with a note | Keep it, and write down one limit. |

---

# Part 1. The 20 deferred items

## Summary table

| Id | In plain words | Recommendation | When |
|---|---|---|---|
| D-01 | Names for the checks a release must pass | Keep deferred | Stage S09 |
| D-02 | Audit entries for granting and using a waiver | Keep deferred | Only if a waiver feature is built |
| D-03 | A record of who said yes or no to an AI recommendation | Decide now | Before S07 |
| D-04 | A narrower permission to read one audit case | Keep deferred | When more than the admin needs audit access |
| D-05 | Four more facts on the audit row | Keep deferred, except final action | Final action at S07 |
| D-06 | The device or record id on the audit row | Decide now | Before S07 |
| D-07 | The name of the person who made a call | Keep deferred | When login is in scope |
| D-08 | A full list of command phrases to catch in AI text | Decide now, start small | Start of S07 |
| D-09 | Catching instructions hidden inside an allowed field | Keep deferred | When real data or a real model arrives |
| D-10 | A version number for the prompt wording | Keep deferred | When the wording changes |
| D-11 | How many seconds the model may take | Keep deferred | After a real model is measured |
| D-12 | Where a password rotation is written down | Decide now (small) | Before S09 |
| D-13 | A role for who owns environment settings | Close it | Now |
| D-14 | A measure of how often the model path is shut off | Keep deferred | When a dashboard exists |
| D-15 | Lists of model names and risk levels | Keep deferred | When a real model is chosen |
| D-16 | Which percentile to report for model delay | Decide now | Now |
| D-17 | Extra alarm fields allowed in a prompt | Keep deferred | When a batch summary is designed |
| D-18 | Four more fields on the audit row for cost grouping | Keep deferred | When the feature that needs each one is built |
| D-19 | A saved place for the count of damaged rows | Keep deferred | Stage S09 dashboard |
| D-20 | The MAESTRO list | Keep deferred | When the course gives the definition |

## D-01. Names for the checks a release must pass

**What it is.** A release needs proof. Examples: policy tests passed, the secret scan passed, a CI run was seen, each evidence section is present. The design asks for an id for each check, so a policy can name what it reads.

**Why it waits.** No policy file and no test reads these checks yet. An id with no reader is a term nothing uses. Source: `docs/06-policy/policy-catalogue.md` lines 89 and 98.

**Options.**
- A. Add ids now.
- B. Add them when the readiness stage (S09) writes the evidence pack.

**Recommendation: Keep deferred (B).**

**Why.** S09 will show which checks the evidence pack needs. Ids written now would be a guess. If the guess is wrong, a rename needs an ADR.

Your decision: Keep deferred. Names for the release checks are added at stage S09. (ADR 0002, 2026-10-12)

## D-02. Audit entries for granting and using a waiver

**What it is.** A waiver is a dated, named exception to one rule. The design wants two audit actions: "waiver granted" and "waiver used".

**Why it waits.** No register, no route, and no code writes a waiver row. `concept.waiver` exists in the YAML and says this. Source: `docs/06-policy/exception-handling-model.md` line 64.

**Options.**
- A. Add the two action ids now.
- B. Wait until someone builds a waiver feature.

**Recommendation: Keep deferred (B).**

**Why.** The two ids would describe a behaviour that does not exist. Nothing in the demo flow needs a waiver.

Your decision: Keep deferred. Waiver audit entries are added only if a waiver feature is built. (ADR 0002, 2026-10-12)

## D-03. A record of who said yes or no to an AI recommendation

**What it is.** A live change needs a person to approve it. Today an approval is only an id string. Nothing stores whether the answer was yes or no, or who gave it. The design wants two fields: `decision` and `approver`.

**Why it waits.** No approval store and no approval route exist. Stage S07 is meant to add them. Source: `docs/06-policy/ai-action-policy-design.md` lines 66 and 220, `docs/13-security-validation/remediation-backlog.md` row `SB-08`.

**Example.** A person rejects a change. The system stores an approval id anyway. The policy only checks that the id is not empty. The change would pass the check. With a `decision` field, a "no" blocks it.

**Options.**
- A. Decide the two fields now, and build them in S07.
- B. Wait and decide inside S07.

**Recommendation: Decide now (A).**

**Why.** The demo (D6) must end in a human decision. The approval record is the center of that flow. Naming the fields before S07 starts avoids rework. Suggested fields: `decision` with the values yes and no, and `approver` with a persona id. The approver for a live change is `persona.network_engineer` (confirmed 2026-10-10). The approver for a next-action sentence is `persona.noc_operator`.

Your decision: Decided. The approval record gets `decision` (yes or no) and `approver` (a persona id). Stage S07 builds it and adds the ids under a new ADR. (ADR 0002, 2026-10-12)

## D-04. A narrower permission to read one audit case

**What it is.** Row TA-35 lets `role.admin` read the audit log for all records. The design asks whether a person could be allowed to read one case only.

**Why it waits.** Only the admin reads the log today. One scope covers that.

**Options.**
- A. Add a scope for one case now.
- B. Keep `scope.all_records` for the admin.

**Recommendation: Keep deferred (B).**

**Why.** A narrower scope matters when more people need audit access. Today that is one role. Revisit when an auditor persona or a customer-facing audit view is planned.

Your decision: Keep deferred (B). `scope.all_records` stays for the admin. (ADR 0002, 2026-10-12)

## D-05. Four more facts on the audit row

**What it is.** The audit row has 15 keys. Four facts have no key: the final action (what changed, or none), the route and method used, which sensitive cells the caller received, and a flag for test calls versus real calls. Source: `docs/14-audit/decision-provenance-model.md` lines 127 to 133, `docs/14-audit/audit-gap-report.md` lines 124 and 157.

**Why it waits.** Adding a field to the YAML without adding it to the audit row would describe a column that does not exist. The row is written by `apps/api/services/audit.py`.

**Options.**
- A. Add all four in a code change, then add the ids.
- B. Add only the final action, when S07 first writes a decision.
- C. Leave all four.

**Recommendation: Keep deferred, except final action (B).**

**Why.** Final action answers "what actually happened". S07 is the first stage that can change anything, so S07 is the first time the field has a value. The route and method can be read from the request path. The test-versus-real flag helps counting, and the log already holds test rows mixed with real ones (the earlier gap report counted 240 lines). That mix is a known limit. Record it in the PRD.

Your decision: Keep deferred, except final action. Final action is built at stage S07. (ADR 0002, 2026-10-12)

## D-06. The device or record id on the audit row

**What it is.** The audit row does not say which record was asked for. A reviewer sees "someone read a record" and cannot see which one. The design calls this `record_id` (LS-Q7). The row also lacks the list of policy reasons.

**Why it waits.** The row has no such key. Adding it is a code change. Source: `docs/08-observability/log-schema.md` line 144.

**Example.** A case shows a read at 10:02. The reviewer wants to know whether that read returned `DEV-00013` or `REC-0001`. The row cannot say. The metric `metric.audit_completeness` cannot be worked out either, because it needs `record_id`.

**Options.**
- A. Add `record_id` and `reasons` as a 16th and 17th key, in S07.
- B. Add `record_id` only.
- C. Leave it.

**Recommendation: Decide now, and choose B (add `record_id` first).**

**Why.** This is the cheapest gap to close and the one a defence question is most likely to hit ("which record did this person read?"). The reason list is useful, and it can follow. Note that a record id may be a device id. It is not on the forbidden list, so it is safe to store.

Your decision: Decided (B). Stage S07 adds `record_id` to the audit row. The reasons list comes later. (ADR 0002, 2026-10-12)

## D-07. The name of the person who made a call

**What it is.** The API trusts a role word typed in the header. Nothing proves who the caller is. The design wants a field for the person.

**Why it waits.** There is no login in the repo. A field with nothing to fill it would stay empty. Source: `docs/08-observability/log-schema.md` line 134, backlog row `SB-09`.

**Options.**
- A. Add a login in scope for the demo.
- B. Say in the PRD that the caller identity is a claim, and keep the field out.

**Recommendation: Keep deferred (B).**

**Why.** A login system is a large piece of work. Whether it is in scope is Unknown. The audit design already lists "caller identity" on the cannot-prove list (`status.code.cannot_prove.caller_identity`), so the gap is stated. Decide the scope question when you write the PRD (S06).

Your decision: Keep deferred. Waits until a login system is in scope. (ADR 0002, 2026-10-12)

## D-08. A full list of command phrases to catch in AI text

**What it is.** The gateway holds one command sentence ("Reboot the core router now and clear the config"). A model answer that contains it is held for review. Any other command wording passes as a recommendation.

**Why it waits.** Nobody wrote the full list. S05R added `failmode.command_text_in_recommendation` for the reason, but not the phrases. Source: `docs/09-ai-guardrails/guardrail-test-pack.md` line 104.

**Options.**
- A. Write a short list of obvious verbs now (reboot, restart, shut down, delete, clear config, push config, apply).
- B. Wait until a real model is used.

**Recommendation: Decide now, start small (A).**

**Why.** Stage S07 shows the text to a person. A person who trusts a recommendation could run a command it names. The code never runs a command, and that is the strongest protection. A short list adds a second layer for little work. Keep the list in one place and mark it PROPOSED. A short list will miss some phrases. Say so in the PRD.

Your decision: Decided. Stage S07 writes a short PROPOSED list: reboot, restart, shut down, delete, clear config, push config, apply. (ADR 0002, 2026-10-12)

## D-09. Catching instructions hidden inside an allowed field

**What it is.** The prompt may include `hostname` and `vendor`. Someone could type an instruction into one of those cells. The gateway checks for forbidden names and values. It does not read the meaning of an allowed cell.

**Why it waits.** No code detects it. The data is synthetic. The model is a stub. Source: `docs/09-ai-guardrails/ai-risk-register.md` line 53, backlog row `SB-14`.

**Options.**
- A. Add a failmode id now.
- B. Wait until real data or a real model is used.

**Recommendation: Keep deferred (B).**

**Why.** With a stub model, the text goes nowhere. The risk starts with a real model. When that day comes, add a simple check first, such as a length limit and a ban on certain characters, then add the failmode id.

Your decision: Keep deferred. Waits for real data or a real model. (ADR 0002, 2026-10-12)

## D-10. A version number for the prompt wording

**What it is.** The audit row stores `prompt_hash`, a SHA-256 hash of the exact prompt. The design also wants a `prompt_template_version`, a label such as v1 or v2.

**Why it waits.** The row has no such key. The hash already proves exactly what was sent.

**Options.**
- A. Add a label field.
- B. Rely on the hash.

**Recommendation: Keep deferred (B).**

**Why.** The hash is stronger than a label, because a label can be forgotten when the wording changes. A label helps people read reports. Add it if the wording starts changing often.

Your decision: Keep deferred. Waits until the prompt wording changes. (ADR 0002, 2026-10-12)

## D-11. How many seconds the model may take

**What it is.** A call that takes too long goes to a person. The code default is 10 seconds, set by the environment value `AI_MODEL_TIMEOUT_SECONDS`. The YAML keeps `timeout_seconds` as `null`.

**Why it waits.** The test `test_gr05_yaml_timeout_slot_stays_null_in_this_stage` requires `null`. The 10 seconds was never run against a real model (`EV-08` in `docs/09-ai-guardrails/evidence.md`).

**Options.**
- A. Accept 10 seconds now. Change the test and the YAML under an ADR.
- B. Keep `null` until a real model is measured.

**Recommendation: Keep deferred (B).**

**Why.** The only model today is a stub that waits 10 milliseconds. Any number is a guess. Measure a real model first. Then write the number and change the test in one ADR.

Your decision: Keep deferred. The YAML timeout stays `null` until a real model is measured. (ADR 0002, 2026-10-12)

## D-12. Where a password rotation is written down

**What it is.** A secret was removed from the code. Nothing records that the old value was replaced where it was used. The design asks for a named place for a rotation record. Source: `docs/04-secrets/rotation-evidence-plan.md` lines 43 and 58.

**Why it waits.** No file or table is named as the store.

**Options.**
- A. Use a simple log file under `docs/04-secrets/`, with one row for each rotation: date, secret name, who did it, where it was replaced. Never store the value.
- B. Name a secret manager as the future store, and write nothing now.

**Recommendation: Decide now (A), and keep it small.**

**Why.** This is a lab, and a markdown log is enough to show the habit. It answers the defence question "how do you know the old secret is gone?" Say in the PRD that production would use a secret manager.

Your decision: Decided (A). The log is `docs/04-secrets/rotation-log.md`. It has no entries and never holds a secret value. (ADR 0002, 2026-10-12)

## D-13. A role for who owns environment settings

**What it is.** The settings map (`docs/05-iac/configuration-ownership-map.md`) asks for an owner role for settings such as the Python version and the pins.

**Why it waits.** No persona fits.

**Options.**
- A. Add a role.
- B. Close the question. Team-Force owns settings.

**Recommendation: Close it (B).**

**Why.** Operating contract row 10 already makes Team-Force the owner of open choices. A persona is a person who uses the system. A settings owner is a team job, so no new id is needed. The personas stay at the locked seven.

Your decision: Closed (B). No new role id. Team-Force owns environment settings. (ADR 0002, 2026-10-12)

## D-14. A measure of how often the model path is shut off

**What it is.** The circuit breaker shuts off model calls after repeated failures. The design asks for a metric: how much time the path was shut off.

**Why it waits.** The three breaker states already have ids (`status.code.breaker_state.*`). A metric needs a formula and a place to read it from, and the design does not set either.

**Options.**
- A. Define the metric now.
- B. Wait until a dashboard needs it.

**Recommendation: Keep deferred (B).**

**Why.** The metric has no data source today. The breaker keeps its state in memory only. Define the metric together with a place to store the state.

Your decision: Keep deferred. Waits for a dashboard. (ADR 0002, 2026-10-12)

## D-15. Lists of model names and risk levels

**What it is.** The FinOps design wants to group cost by model name and by risk level. The YAML has no list of either.

**Why it waits.** One model exists (`local-sim-v1`). No file lists the risk levels the model advice can have.

**Options.**
- A. Add both lists now.
- B. Add them when a real model or a risk rule exists.

**Recommendation: Keep deferred (B).**

**Why.** A list of one model name is no list. The risk levels need a rule for what each level means, and nobody has written that rule. Grouping by risk is a nice view and no stage needs it yet.

Your decision: Keep deferred. Waits for a real model. (ADR 0002, 2026-10-12)

## D-16. Which percentile to report for model delay

**What it is.** Average delay hides slow calls. The FinOps design asks for a rule that picks the tail value to report for `metric.recommendation_latency`.

**Why it waits.** Nobody named the percentile.

**Options.**
- A. p95: 95 of every 100 calls finish at or under this time.
- B. p99.
- C. Keep deferred.

**Recommendation: Decide now, choose p95 (A).**

**Why.** The SLO proposal already uses 95 of 100. The FinOps report already shows a p95 (14 ms over 17 model calls on the stub). One percentile everywhere keeps reports consistent. This choice sets a method. It sets no target number, so `target` stays `null`.

Your decision: Decided. Report p95. Written into `metric.recommendation_latency` and the glossary. The layer is now version `1.1.1`. `target` stays `null`. (ADR 0002, 2026-10-12)

## D-17. Extra alarm fields allowed in a prompt

**What it is.** The prompt allow list holds device fields only. A summary of a whole alarm storm would need alarm fields such as `storm_batch_id` and `alarm_type`.

**Why it waits.** No batch summary is designed. Allowing more fields widens what leaves the system.

**Options.**
- A. Add alarm fields to the allow list now.
- B. Wait for a batch summary design.

**Recommendation: Keep deferred (B).**

**Why.** The allow list is a safety control. Widen it with a design in hand, and check each field against the forbidden list. Customer ids stay out.

Your decision: Keep deferred. Waits for the batch summary design. (ADR 0002, 2026-10-12)

## D-18. Four more fields on the audit row for cost grouping

**What it is.** FinOps wants to group cost by capability, incident id, flow name, and whether a stored answer was used (a cache hit). The audit row has none of these.

**Why it waits.** The row has no such keys. The cache is a decided item for S07 (`OB-01`, 300 seconds), and it is not built.

**Options.**
- A. Add all four now.
- B. Add each with the feature that needs it.

**Recommendation: Keep deferred (B).** If the cache is built in S07, add the cache flag first.

**Why.** Without a cache flag, a cached answer would be counted as a held call or a model call. That would make the cost numbers wrong. The other three can wait for the cost dashboard.

Your decision: Keep deferred. Each field is added when its feature is built. (ADR 0002, 2026-10-12)

## D-19. A saved place for the count of damaged rows

**What it is.** The daily batch counts rows it holds aside (`quarantined`) and prints the number. The metric `metric.quarantine_rate` needs the number stored somewhere.

**Why it waits.** The batch prints the count and stores it nowhere.

**Options.**
- A. Write one summary line per run to a file.
- B. Wait for the dashboard stage.

**Recommendation: Keep deferred (B).**

**Why.** The dashboard (S09) decides where it reads from. Pick the store then, so the batch and the dashboard agree.

Your decision: Keep deferred. Waits for the stage S09 dashboard. (ADR 0002, 2026-10-12)

## D-20. The MAESTRO list

**What it is.** `security/threat-model.md` names STRIDE and MAESTRO. The letters and layers of MAESTRO have no definition in the repo.

**Why it waits.** No file defines the list. Writing letters from memory would invent facts.

**Options.**
- A. Get the definition from the course material, then add ids and a map.
- B. Drop the MAESTRO name from the threat model.

**Recommendation: Keep deferred, and take A when the course material is at hand.**

**Why.** The name is in the repo, so a reader will ask. Copy the list from the source and cite it. Do not write it from memory.

Your decision: Keep deferred. Option A (copy the course list) when the course material is at hand. (ADR 0002, 2026-10-12)

---

# Part 2. The PROPOSED items

**Verified Fact.** A script read the seven YAML files on 2026-10-12. It found 120 items with `proposed: true`. 28 existed at `1.0.0`. 92 were added by S05R. The owner of all 120 is Team-Force.

For each bundle: what it is, an example, my recommendation, and why.

## Summary table

| Bundle | Items | In plain words | Recommendation |
|---|---|---|---|
| P-01 | 7 | The seven personas | Accept |
| P-02 | 12 | Eight purposes and four scopes | Accept |
| P-03 | 4 | Four AI uses and their approver jobs | Accept |
| P-04 | 5 | Five reasons a call goes to a person | Accept |
| P-05 | 2 | The prompt allow list and the answer shape | Accept |
| P-06 | 6 | Six metrics | Accept with a note |
| P-07 | 15 | The 15 keys of the audit row | Accept |
| P-08 | 8 | The eight inputs of the AI action policy | Accept |
| P-09 | 47 | Forty-seven status codes the code writes | Accept |
| P-10 | 7 | Seven new rules | Accept with a note |
| P-11 | 7 | Concepts, collisions, one resource, and three policy items | Accept |
| P-12 | 0 (data) | The 35 access matrix rows | Accept, and decide TA-15 |
| N-01 to N-06 | numbers | PROPOSED numbers outside the YAML ids | See the numbers table |

The items in P-01 to P-11 add up to 120.

## P-01. The seven personas (7 items)

**What it is.** The seven kinds of people the system serves: `persona.noc_operator`, `persona.network_engineer`, `persona.field_engineer`, `persona.customer_support`, `persona.automation_service`, `persona.vendor_account`, `persona.ai_agent`.

**Why it is PROPOSED.** The inherited repo has no persona list. The seven names come from `Project_Intent.md` and are locked in the stage rules.

**Recommendation: Accept.**

**Why.** The brief locks them. Changing one would break the access rows and the glossary.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-02. Eight purposes and four scopes (12 items)

**What it is.** A purpose is why a caller acts, such as `purpose.incident_triage`. A scope is which records the caller may touch, such as `scope.one_site`. The 12 PROPOSED items are `purpose.incident_triage`, `network_change_planning`, `field_repair`, `customer_enquiry`, `scheduled_automation`, `vendor_support`, `ai_assistance`, `audit_review`, and `scope.one_site`, `one_customer`, `assigned_incident`, `own_vendor_devices`.

**Example.** A field engineer reads a device for `purpose.field_repair`. Scope `scope.one_site` limits the read to that engineer's site.

**Recommendation: Accept.**

**Why.** The access matrix rows use these words. The policy tests pass with them. **Inference:** four scopes need data that the CSV files do not hold (for example, which site an engineer belongs to). That is a limit to write in the PRD. It is no reason to remove the words.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-03. Four AI uses and their approver jobs (4 items)

**What it is.** Four of the eleven AI uses carry a PROPOSED desk job for the person who approves:

| AI use | What the AI does | Approver job |
|---|---|---|
| `ai_use.incident_summary` | Writes a short account of an incident | `persona.noc_operator` |
| `ai_use.next_action_recommendation` | Suggests the next step | `persona.noc_operator` |
| `ai_use.configuration_suggestion` | Suggests a config change | `persona.network_engineer` |
| `ai_use.remediation_execution` | A live change | `persona.network_engineer` (confirmed by Mangesh on 2026-10-10) |

None of these gives a model execute agency. The live change is done by workflow automation, after a person approves.

**Recommendation: Accept.**

**Why.** Each job matches the role's duty. The network engineer owns config changes. The NOC operator owns triage. The incident summary also carries a stale-topology block that S05R added: stale data holds the summary. That follows policy row B5 and is the safer choice.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-04. Five reasons a call goes to a person (5 items)

**What it is.** Five failmodes: `failmode.stale_topology_blank` (a blank stale flag holds the case), `failmode.input_invalid`, `failmode.model_unreachable`, `failmode.command_text_in_recommendation`, `failmode.policy_version_differs`.

**Example.** The model does not answer. The breaker is open. The case goes to a person with the reason `failmode.model_unreachable`. Without the id, the log would call it a schema failure.

**Recommendation: Accept.**

**Why.** Each one names behaviour the code already has (breaker, policy reasons, validation). Naming them makes logs and tests agree.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-05. The prompt allow list and the answer shape (2 items)

**What it is.** `policy.prompt_fields` lists which fields may enter a prompt and which never may. S05R added `field.service_order.customer_id` to the never list. `policy.output_schema` says what a model answer must look like. S05R marked seven fields as allowed to be empty on a failed call.

**Recommendation: Accept.**

**Why.** The customer id was on the never list for incidents and circuits only. The same field on orders had no rule. Forbidding it is the safer direction and costs no feature.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-06. Six metrics (6 items)

**What it is.** `metric.audit_completeness`, `metric.ai_outcome_count`, `metric.api_availability`, `metric.record_read_latency`, `metric.repeated_prompt_share`, `metric.cost_per_flow`. Every metric `target` is `null`.

**Recommendation: Accept with a note.**

**Why.** The names say what to measure. No target number is set, so nothing here is a promise. Note that `metric.audit_completeness` cannot be worked out until `record_id` is on the audit row (D-06).

Your decision: Accept with a note. `metric.audit_completeness` waits for `record_id` (D-06). (ADR 0002, 2026-10-12)

## P-07. The 15 keys of the audit row (15 items)

**What it is.** One id for each key that `audit.py` writes: `ts`, `correlation_id`, `actor`, `role`, `action`, `resource`, `policy_decision`, `approval_id`, `model`, `model_version`, `prompt_hash`, `tokens`, `latency_ms`, `outcome`, `token_estimate_method`.

**Example.** `field.audit_row.approval_id` is null on every row, because no route writes an approval id yet.

**Recommendation: Accept.**

**Why.** A test (`test_audit_row_fields_are_the_keys_the_code_writes`) fails if these ids and the code disagree. They mirror the code.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-08. The eight inputs of the AI action policy (8 items)

**What it is.** `field.policy_input.*`: `policy_version`, `output_schema_ok`, `timeout_hit`, `forbidden_field_in_prompt`, `record_found`, `audit_row_written`, `change_plan_ok`, `approval_required`. The policy reads these to choose RECOMMEND_ONLY, HOLD_FOR_REVIEW, BLOCK, or EXECUTE.

**Recommendation: Accept.**

**Why.** They are the names the Rego file and the Python copy already read. `change_plan_ok` has one open point: what "validated" means is Unknown. No route sets it, so no live change can pass the fourth gate today. That is the safe state.

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-09. Forty-seven status codes the code writes (47 items)

**What it is.** Words the code or the design writes, in 14 groups.

| Group | Count | Example |
|---|---|---|
| Audit actions | 5 | `status.code.audit_action.audit_read` |
| Errors | 2 | `status.code.error.id_too_long` |
| Guardrail status | 1 | `status.code.guardrail_status.enforced` |
| Role header | 1 | `status.code.role_header.absent` |
| Policy reasons | 3 | `status.code.policy_reason.input_invalid` |
| Token estimate method | 1 | `status.code.token_estimate_method.word_count_x2_educational` |
| Breaker states | 3 | `status.code.breaker_state.half_open` |
| Model call queue states | 3 | `status.code.model_call_queue_state.queued` |
| Runbook levels | 4 | `status.code.runbook_level.degraded` |
| Field destinations | 3 | `status.code.field_destination.prompt` |
| Faults | 3 | `status.code.fault.audit_log_unwritable` |
| Alarm flags | 2 | `status.code.alarm_flag.times_unreadable` |
| Dedupe results | 3 | `status.code.dedupe_result.repeat` |
| Cannot-prove items | 13 | `status.code.cannot_prove.log_integrity` |

**Recommendation: Accept, and pay attention to two groups.**

**Why.** Most mirror code and are checked by tests (the audit action words and the 13 cannot-prove names are tested against the code). Two groups need your eye:
- **Runbook levels (4).** `stopped`, `degraded`, `data_fault`, `watch` are new names for how bad an incident is. They carry no number. They fill a gap that the reliability design named (OQ-7). Accept them if the names read well to an operator.
- **Model call queue states (3).** They name a queue that no code builds (scaling item `SR-04`). Accepting them is harmless. Remove them if you decide not to build the queue.

Your decision: Accept. Runbook level names accepted if they read well to an operator. Queue states removed if the queue is never built. (ADR 0002, 2026-10-12)

## P-10. Seven new rules (7 items)

**What it is.** Seven rules added in S05R, each with a flag `enforced_today`:

| Rule | Plain words | `enforced_today` |
|---|---|---|
| `rule.audit_case_id_limit` | A case id over 128 characters is refused | true |
| `rule.audit_log_holds_no_forbidden_field` | The audit log never stores `mgmt_ip` or a credential name | true |
| `rule.no_secret_value_committed` | No file holds a secret value | false (a test checks it, no code does) |
| `rule.policy_copies_agree` | The Python and Rego policy give the same answer | false (tests check it, no route does) |
| `rule.bad_row_held_aside_batch_goes_on` | A bad row is set aside and the batch continues | true |
| `rule.repeat_event_is_one_event` | The same event id twice is one event | false (`dedupe.py` has no caller) |
| `rule.order_attempt_same_retry_is_one_attempt` | Same order id and retry count is one attempt | false (`dedupe.py` has no caller) |

**Recommendation: Accept with a note.**

**Why.** The rules match tests or code. The note: three rules say `false` because nothing runs them in a live flow. Stage S07 should connect `dedupe.py` to the alarm intake, or the PRD should say the rules are designs only.

Your decision: Accept with a note. Stage S07 connects `dedupe.py` to the alarm intake, or the PRD says three rules are designs only. (ADR 0002, 2026-10-12)

## P-11. Concepts, collisions, one resource, and three policy items (7 items)

**What it is.**
- `concept.waiver` and `concept.decision_provenance` (the nine groups of facts about one decision).
- `collision.approval_required_column_and_policy_input` and `collision.degraded_as_runbook_level_and_status_word` (two words with two meanings each).
- `resource.model_call_queue` (the queue from `SR-04`).
- `policy.model_now` (what the live gateway does today, next to the older `model_today`).
- `policy.opa.access_matrix` (the 35-row matrix; it replaces two deprecated ids).

**Recommendation: Accept.**

**Why.** These are naming items with no behaviour. Two things to know. `concept.waiver` describes something that is not built (see D-02). `resource.model_call_queue` names a queue that is not built (see P-09).

Your decision: Accept. (ADR 0002, 2026-10-12)

## P-12. The 35 access matrix rows (data, outside the 120)

**What it is.** `policy/opa/policy_data.json` holds 35 allow rows, TA-01 to TA-35. Every row is PROPOSED. TA-01 to TA-34 come from the YAML. TA-35 lets `role.admin` read the audit log, and Mangesh accepted it on 2026-10-12.

**Recommendation: Accept the matrix. Make one explicit decision on TA-15.**

**TA-15.** Only `persona.network_engineer` may read the two sensitive device fields, `mgmt_ip` and `credential_profile`. Written acceptance by Team-Force is Unknown.

**Options for TA-15.**
- A. Accept TA-15 as written.
- B. Remove the row, so no persona reads those two fields through the policy.

**Recommendation: A.**

**Why.** A network engineer planning a change may need the management address. One role, one purpose. A second point to know: the record route today returns the whole device row to every allowed role (`SB-06`). TA-15 states who should see the two fields. The route does not enforce that yet. Closing `SB-06` is a code change for a later stage.

Your decision (matrix): Accept. (ADR 0002, 2026-10-12)
Your decision (TA-15): Accept as written (A). (ADR 0002, 2026-10-12)

---

## Numbers marked PROPOSED outside the YAML ids

These numbers sit in code, settings, or design files. Each is PROPOSED with owner Team-Force, unless the table says it is decided.

| Id | The number | Where it lives | Where it came from | Recommendation |
|---|---|---|---|---|
| N-01 | 128 characters, the longest case id the audit route accepts | `apps/api/services/audit_query.py` (`MAX_ID_LENGTH`), `rule.audit_case_id_limit` | Chosen in S05-14 Half B. Mangesh accepted it on 2026-10-12. A UUID is 36 characters. | Accept. Record it in an ADR. |
| N-02 | 1000, the retry count above which the data-quality baseline flags an order | `metric.retry_count`, `docs/02-baseline/data-quality-baseline.md` | A counting line. In `service_orders.csv`, 294 rows are at or above 1000. | Accept with a note. It is a flag, not a legal maximum. The legal maximum stays Unknown. |
| N-03 | 0 to 1, the allowed range of `sla_breach_risk` | `metric.sla_breach_risk`, `entities.yaml` | The baseline's valid range for a risk score | Accept. Keep the label PROPOSED until the data owner confirms the meaning. |
| N-04 | 10 seconds, the model timeout default | `.env.example`, `apps/api/services/ai_gateway.py` | Chosen in S04-09. Never run against a real model. | Accept as a default for the stub. Write it into the YAML only after a real model is measured (see D-11). |
| N-05 | The breaker: open after 5 failures, stay open 30 seconds, allow 10 calls at once | `apps/api/services/breaker.py`, `docs/11-reliability/retry-and-circuit-breaker-strategy.md` | Proposed in S04-11. The repo has no measured failure rate to base them on. | Accept for the lab. Revisit with a real model. |
| N-06 | Three service levels: 99 of 100 `GET /health` calls return 200 each day; 95 of 100 summaries finish in 2000 ms; audit completeness 1.0 | `docs/08-observability/slo-proposal.md` | Proposed in S04-08. No `metrics.yaml` target holds them. | Accept the first and third. Accept the second only for a real model, because the stub waits 10 ms and passes with no real test. |

**Already decided. No action.** The cache lifetime of 300 seconds (`OB-01`, built in S07). The cost rate of 1.0 unit per 1000 tokens (decided 2026-10-11, EDUCATIONAL).

**Why accepting a number needs care.** A number in a document can be copied into a report as if it were measured. After you accept one, keep the word PROPOSED in the metric text until a real run backs it.

---

# Part 3. What to decide first

| Order | Decision | Why first |
|---|---|---|
| 1 | D-03 approval record fields | The demo ends in a human decision. S07 builds it. |
| 2 | D-06 `record_id` on the audit row | A defence question asks which record was read. One small code change closes it. |
| 3 | D-16 percentile (p95) | A one-line choice. Reports then agree. |
| 4 | D-08 a short command list | S07 shows AI text to a person. |
| 5 | TA-15 | It decides who sees `mgmt_ip` and `credential_profile`. |
| 6 | D-12 rotation log place | Small. **Inference:** S09 asks for proof of rotation. |
| 7 | D-13 close the question | It needs no work. |

Everything else can stay as it is until the trigger in the summary table.

## What happens after you decide

All decisions were made on 2026-10-12 and recorded in `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`.

- An Accept needs no action. This file and the ADR record it.
- D-16 changed one sentence in the YAML, so the layer is now `1.1.1`. `build.py --check` and 41 semantic-layer tests pass.
- D-12 created `docs/04-secrets/rotation-log.md`, with no entries.
- D-03, D-06, and D-08 are decided and need code. Stage S07 is the first stage that edits code. S07 adds each new YAML id under a new ADR.
- The 14 items that stay deferred each wait for the trigger in the summary table.
