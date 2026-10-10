# Project Intent — Telecom Service, Network, and Incident Operations - sections 3.1, 5.2, 5.3, Appendix C

---


## 3. What is expected

### 3.1 Decisions you must write down first

Use the trainer’s words and the repo files. If a row is missing from the packet, write Unknown. Do not guess a business cutoff.

| # | Question | Answer from this packet |
|---|---|---|
| 1 | What event arrives? | One of four named flows: a customer service order, an alarm storm that may become an incident, a topology lookup that asks AI for a next action, or an approved remediation that still needs validation. The running API today only exposes record read and AI summarize. |
| 2 | Which people or objects does it touch? | People named in the domain spec: `noc_operator`, `network_engineer`, `field_engineer`, `customer_support`, `automation_service`, `vendor_account`, `ai_agent`. Objects named in the data model: devices, circuits, alarms, incidents, service orders, AI invocations, and operational events. |
| 3 | What action cannot be undone? | A live network change. That means a config push, an automated remediation, a provisioning change, or a close of an incident that hides a real outage. The current code does not push to a device. The current AI path can still recommend an action with `guardrail_status: not_enforced`. |
| 4 | What did they give you? | A brownfield repo, a challenge guide, and a semantic-layer format PDF. There is no finished PRD and no finished semantic layer in the packet. |
| 5 | What must you hand back? | Discovery and baseline, controlled improvements with evidence, a semantic layer in the capture-PDF format, a PRD, a working app and demo, a second-model semantic-layer test, an app comparison, and a production evidence pack with a go/no-go. |
| 6 | Who is harmed if the score or route is wrong? | A customer, if an SLA on a circuit is missed. The network, if a risky config is applied. Field and NOC staff, if duplicate tickets or stale topology hide the real fault. The company, if an overpowered automation account or an ungoverned AI agent changes production. |
| 7 | Which facts exist at decision time? | The domain spec lists fields on devices, circuits, alarms, incidents, service orders, and AI invocations. The running API does not use those tables. It reads `data/synthetic/devices.csv` only. A missing id returns the first row. The AI prompt interpolates the whole row. |
| 8 | What still works if the AI path is down? | Unknown as a designed degraded mode. `/health` and `/records/{id}` do not call the model. `/ai/summarize/{id}` has no timeout, no circuit breaker, and no fail-to-person path. The failure-injection runbook names an AI timeout drill. The runbook is a draft. |

Worked example for row 3: `POST /ai/summarize/REC-0001` returns `recommendation: Review and approve before action` and `guardrail_status: not_enforced`. There is no approval id, no policy decision, and no role check on that route. If a later worker treats that JSON as a change ticket, the recommendation has become an operational decision.



### 5.2 Use-case split

The repo name is one product. The domain spec names four flows. The current-state note names three AI products. Classify them before you write the PRD.

| Use case | What arrives | What a person or system may do | Irreversible if executed |
|---|---|---|---|
| Order to provisioning | `service_orders` row | Qualify, provision, retry, or roll back a circuit | A wrong circuit or bandwidth in production |
| Alarm storm to incident | `alarms` plus topology | Dedupe, correlate, open or merge an incident | A missed outage or a flood of duplicate tickets |
| Topology to AI recommendation | device / incident / alarm context | Ask the copilot or config assistant | None, if the output stays a recommendation |
| Approved remediation to validation | An approved change | Apply, validate, or roll back | The live device or service change |

The running code implements none of those four flows end to end. It implements health, a device-row read, and a synthetic summary. Section 2.7 names the file evidence for each job, the routes this packet adds, and the two jobs that stay unimplemented when the demo stays topology lookup plus alarm-storm dedupe.

### 5.3 Analyse / recommend / decide / execute

A person can be harmed, so keep these four verbs separate.

| Verb | Who may do it today | What the files show |
|---|---|---|
| Analyse | API `load_record`, ETL blank-field count | Analysis can return the wrong device. ETL does not quarantine. |
| Recommend | `ai_gateway.summarize_record` | Hardcoded prompt. Untrusted fields interpolated. No output schema. |
| Decide | Intended: a named human or executable policy | OPA is not called by the API. AI summarize has no role check. |
| Execute | Intended: automation only after approval | No execute route exists. That absence is safer than a silent execute. Keep it until policy, approval, and audit exist. |



## Appendix C — Why AI must not silently act

The challenge guide acceptance line for AI security is:

> AI recommendations must not silently become operational decisions.

The current gateway returns a recommendation and `guardrail_status: not_enforced`. The summarize route has no role check, no policy call, no approval id, and no output schema.

Keep four outcomes for a recommendation:

| Outcome | Meaning |
|---|---|
| RECOMMEND_ONLY | Show the text. Do not create a change. |
| HOLD_FOR_REVIEW | A named person must accept or reject. |
| BLOCK | Policy or guardrail refused the output. |
| EXECUTE | Allowed only after policy allow, human approval when required, an audit row, and a reversible or validated change plan. |

The inherited API has no EXECUTE route. Do not add one until those four gates exist.

---
