# S05R decisions taken

| Field | Value |
|---|---|
| Stage | S05R follow-up. The short record of what was decided on the items that stage S05R left open. |
| Date / version | 2026-10-12, v1.0. Based on semantic layer `1.1.1`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Decided on 2026-10-12. Mangesh (FDE) decided for Team-Force by taking every recommendation in `S05R_Decisions.md`. The formal record is `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`. |
| Evidence sources | `docs/02-baseline/S05R_Decisions.md` (the options, the reasons, and the filled decision lines); `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md`; `docs/02-baseline/semantic-layer-revision.md` |
| Assumptions | (1) Mangesh (FDE) speaks for Team-Force on these choices (`docs/00-contract/operating-contract.md` row 10). (2) "Decided" means the choice is made and written down. It does not mean the code or the test exists. |
| Unresolved issues | The letters of MAESTRO (D-20) are Unknown. Whether a login system is in scope (D-07) is Unknown. A real model is not in use, so every time and cost number comes from a stub. |
| Residual risks | D-03, D-06, and D-08 are decided here and built in stage S07. Until S07 the code does not match them. |

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

This file has the decision and the reason for each item in one table row. `S05R_Decisions.md` has the full explanation, the options, and an example for each item.

## Count of decisions

| Result | Number | Items |
|---|---|---|
| Decided now | 5 | D-03, D-06, D-08, D-12, D-16 |
| Closed | 1 | D-13 |
| Kept deferred, each with a named trigger | 14 | D-01, D-02, D-04, D-05, D-07, D-09, D-10, D-11, D-14, D-15, D-17, D-18, D-19, D-20 |
| PROPOSED items accepted | 120 | Bundles P-01 to P-11 |
| Access matrix rows accepted | 35 | TA-01 to TA-35, with TA-15 as written |
| PROPOSED numbers accepted | 6 | N-01 to N-06 |

## Part 1. The 20 deferred items

| Id | In plain words | Decision taken | Reasoning | What happens next |
|---|---|---|---|---|
| D-01 | Names for the checks a release must pass | Keep deferred (B) | Stage S09 shows which checks the evidence pack needs. Ids written now would be a guess. A wrong guess needs an ADR to rename. | Add the names at stage S09. |
| D-02 | Audit entries for granting and using a waiver | Keep deferred (B) | No waiver register, route, or code exists. Two ids would describe behaviour that does not exist. The demo flow needs no waiver. | Add the entries only if a waiver feature is built. |
| D-03 | A record of who said yes or no to an AI recommendation | **Decided (A).** The approval record gets `decision` (yes or no) and `approver` (a persona id). | The demo (D6) must end in a human decision. The approval record is the center of that flow. Naming the fields before S07 avoids rework. Today an approval is only an id string, so a "no" could still pass the check. | Stage S07 builds the fields and adds the YAML ids under a new ADR. |
| D-04 | A narrower permission to read one audit case | Keep deferred (B). `scope.all_records` stays for the admin. | Only the admin reads the audit log today. One scope covers that. A narrower scope matters when more people need audit access. | Revisit when an auditor persona or a customer-facing audit view is planned. |
| D-05 | Four more facts on the audit row | Keep deferred, except final action (B) | Final action answers "what actually happened". S07 is the first stage that can change anything, so it is the first time the field has a value. The route and method can be read from the request path. The test-versus-real flag has a known limit: the log mixes test rows and real rows. | Add final action at stage S07. Write the log-mix limit in the PRD. |
| D-06 | The device or record id on the audit row | **Decided (B).** Add `record_id` first. The reasons list comes later. | It is the cheapest gap to close. A defence question will likely ask which record a person read. A record id may be a device id. It is not on the forbidden list, so it is safe to store. | Stage S07 adds `record_id` as the 16th key and adds the YAML id under a new ADR. |
| D-07 | The name of the person who made a call | Keep deferred (B) | There is no login in the repo. A field with nothing to fill it would stay empty. A login system is a large piece of work. Whether it is in scope is Unknown. The gap is already stated as `status.code.cannot_prove.caller_identity`. | Decide the login scope when the PRD is written (S06). |
| D-08 | A full list of command phrases to catch in AI text | **Decided (A).** Start small. | The code never runs a command, and that is the strongest protection. A person who trusts a recommendation could still run a command it names. A short list adds a second layer for little work. | Stage S07 writes the list: reboot, restart, shut down, delete, clear config, push config, apply. The list is PROPOSED. The PRD says a short list misses some phrases. |
| D-09 | Catching instructions hidden inside an allowed field | Keep deferred (B) | The model is a stub and the data is synthetic, so the text goes nowhere. The risk starts with a real model. | When a real model arrives, add a simple check first (a length limit and a ban on certain characters), then add the failmode id. |
| D-10 | A version number for the prompt wording | Keep deferred (B) | `prompt_hash` already proves exactly what was sent. A label can be forgotten when the wording changes. | Add the label if the wording starts changing often. |
| D-11 | How many seconds the model may take | Keep deferred (B). The YAML `timeout_seconds` stays `null`. | The only model is a stub that waits 10 milliseconds. Any number is a guess. The 10 seconds in the code was never run against a real model. | Measure a real model. Then write the number and change the test in one ADR. |
| D-12 | Where a password rotation is written down | **Decided (A).** A simple log file. | This is a lab, and a markdown log is enough to show the habit. It answers the defence question "how do you know the old secret is gone?". | Done: `docs/04-secrets/rotation-log.md` exists. It has no entries. The PRD says production would use a secret manager. |
| D-13 | A role for who owns environment settings | **Closed (B).** No new role id. | Operating contract row 10 already makes Team-Force the owner of open choices. A persona is a person who uses the system. A settings owner is a team job. The personas stay at the locked seven. | No work. |
| D-14 | A measure of how often the model path is shut off | Keep deferred (B) | The breaker keeps its state in memory only, so the metric has no data source. A metric needs a formula and a place to read it from. | Define the metric together with a place to store the state, when a dashboard needs it. |
| D-15 | Lists of model names and risk levels | Keep deferred (B) | One model exists (`local-sim-v1`). A list of one is no list. Nobody has written the rule for what each risk level means. | Add the lists when a real model or a risk rule exists. |
| D-16 | Which percentile to report for model delay | **Decided (A).** Report p95. | The SLO proposal already uses 95 of 100. The FinOps report already shows a p95 (14 ms over 17 model calls on the stub). One percentile everywhere keeps reports consistent. The choice sets a method. It sets no target. | Done: written into `metric.recommendation_latency` and the glossary. The layer is now `1.1.1`. `target` stays `null`. |
| D-17 | Extra alarm fields allowed in a prompt | Keep deferred (B) | The allow list is a safety control. Allowing more fields widens what leaves the system. No batch summary is designed. | Widen the list when a batch summary is designed. Check each field against the forbidden list. Customer ids stay out. |
| D-18 | Four more fields on the audit row for cost grouping | Keep deferred (B) | Without a cache flag, a cached answer would be counted as a held call or a model call, and the cost numbers would be wrong. The other three can wait for the cost dashboard. | Add each field with the feature that needs it. If the cache is built in S07, add the cache flag first. |
| D-19 | A saved place for the count of damaged rows | Keep deferred (B) | The stage S09 dashboard decides where it reads from. Picking the store then keeps the batch and the dashboard in agreement. | Pick the store at the S09 dashboard. |
| D-20 | The MAESTRO list | Keep deferred. Take option A (copy the course list) when the course material is at hand. | No file in the repo defines the list. Writing letters from memory would invent facts. The name is in the repo, so a reader will ask. | Copy the list from the course source, cite it, then add ids and a map. |

**Worked example for D-03.** A recommendation says "restart the router". An operator says no. The approval record then holds `decision: no` and `approver: persona.noc_operator`. The policy sees the "no" and blocks the change. Before this decision the record held only an id string, and the policy checked only that the string was not empty.

## Part 2. The PROPOSED items

An item marked `proposed: true` is not in the inherited repo. It carries `owner: Team-Force`. The flag stays on after acceptance, because it records where the item came from.

| Bundle | Items | In plain words | Decision taken | Reasoning |
|---|---|---|---|---|
| P-01 | 7 | The seven personas | Accept | The brief locks them. Changing one would break the access rows and the glossary. |
| P-02 | 12 | Eight purposes and four scopes | Accept | The access matrix rows use these words, and the policy tests pass with them. **Inference:** four scopes need data the CSV files do not hold, such as which site an engineer belongs to. That is a limit to write in the PRD. It is no reason to remove the words. |
| P-03 | 4 | Four AI uses and their approver jobs | Accept | Each job matches the role's duty. The network engineer owns config changes. The NOC operator owns triage. None of the four gives a model execute agency. A stale topology holds the incident summary, which follows policy row B5. |
| P-04 | 5 | Five reasons a call goes to a person | Accept | Each one names behaviour the code already has (breaker, policy reasons, validation). Naming them makes logs and tests agree. |
| P-05 | 2 | The prompt allow list and the answer shape | Accept | The customer id was on the never list for incidents and circuits only. The same field on orders had no rule. Forbidding it is the safer direction and costs no feature. |
| P-06 | 6 | Six metrics | Accept with a note | The names say what to measure. No target is set, so nothing here is a promise. **Note:** `metric.audit_completeness` cannot be worked out until `record_id` is on the audit row (D-06). |
| P-07 | 15 | The 15 keys of the audit row | Accept | A test (`test_audit_row_fields_are_the_keys_the_code_writes`) fails if these ids and the code disagree. They mirror the code. |
| P-08 | 8 | The eight inputs of the AI action policy | Accept | They are the names the Rego file and the Python copy already read. No route sets `change_plan_ok`, so no live change can pass the fourth gate today. That is the safe state. |
| P-09 | 47 | Forty-seven status codes the code writes | Accept | Most mirror code, and tests check them. The four runbook level names are accepted if they read well to an operator. The three queue states name a queue that no code builds, and they are removed if the queue is never built. |
| P-10 | 7 | Seven new rules | Accept with a note | The rules match tests or code. **Note:** three rules have `enforced_today: false` because nothing runs them in a live flow. Stage S07 connects `dedupe.py` to the alarm intake, or the PRD says these three rules are designs only. |
| P-11 | 7 | Concepts, collisions, one resource, and three policy items | Accept | These are naming items with no behaviour. `concept.waiver` and `resource.model_call_queue` describe things that are not built. The PRD says so. |
| P-12 | 35 rows | The access matrix rows TA-01 to TA-35 | Accept | The rows come from the YAML. Mangesh accepted TA-35 on 2026-10-12. |
| TA-15 | 1 row | Only `persona.network_engineer` reads `mgmt_ip` and `credential_profile` | Accept as written (A) | A network engineer planning a change may need the management address. One role, one purpose. **Note:** the record route today returns the whole device row to every allowed role (`SB-06`). TA-15 states who should see the two fields. The route does not enforce it yet. |

The items in P-01 to P-11 add up to 120: 7 + 12 + 4 + 5 + 2 + 6 + 15 + 8 + 47 + 7 + 7.

## Part 3. The PROPOSED numbers

| Id | The number | Decision taken | Reasoning |
|---|---|---|---|
| N-01 | 128 characters, the longest case id the audit route accepts | Accept. ADR 0002 is its ADR. | Chosen in S05-14 Half B, and Mangesh accepted it on 2026-10-12. A UUID is 36 characters, so 128 leaves room. |
| N-02 | 1000, the retry count above which the data-quality baseline flags an order | Accept with a note | In `service_orders.csv`, 294 rows are at or above 1000. **Note:** it is a flag level. It is not a legal maximum. The legal maximum stays Unknown. |
| N-03 | 0 to 1, the allowed range of `sla_breach_risk` | Accept | It is the baseline's valid range for a risk score. The label stays PROPOSED until the data owner confirms the meaning. |
| N-04 | 10 seconds, the model timeout default | Accept as the stub default | It was chosen in S04-09 and never run against a real model. The YAML stays `null` until a real model is measured (D-11). |
| N-05 | The breaker: open after 5 failures, stay open 30 seconds, allow 10 calls at once | Accept for the lab | The repo has no measured failure rate to base other numbers on. Revisit with a real model. |
| N-06 | Three service levels: 99 of 100 `GET /health` calls return 200 each day; 95 of 100 summaries finish in 2000 ms; audit completeness 1.0 | Accept the first and third. Accept the 2000 ms level for a real model only. | The stub waits 10 ms, so the 2000 ms level passes with no real test. |

**Why a number needs care.** A number in a document can be copied into a report as if it were measured. Each number above came from a design or a stub. None was measured with a real model.

**Already decided before this file.** The cache lifetime of 300 seconds (`OB-01`, built in S07). The cost rate of 1.0 unit per 1000 tokens (decided 2026-10-11, EDUCATIONAL).

## Part 4. What changed because of these decisions

| Change | Where |
|---|---|
| One sentence in the YAML: report p95 for `metric.recommendation_latency` | `semantic-layer/metrics.yaml`, `semantic-layer/glossary.md` |
| Semantic layer version `1.1.0` to `1.1.1` | Seven YAML files, the schema, the glossary, the README, the test constant |
| A rotation log with no entries | `docs/04-secrets/rotation-log.md` |
| The formal record of all decisions | `docs/ADR/0002-s05r-deferred-and-proposed-decisions.md` |
| No code, Rego, CI file, Terraform, fixture, or `policy_data.json` changed | Not applicable |

Checks run on 2026-10-12 after the change: `build.py --check` passes, 41 semantic-layer tests pass, the full run passes 333, and the security stage passes 195.
