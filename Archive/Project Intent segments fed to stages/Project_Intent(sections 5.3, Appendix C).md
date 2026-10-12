# Project Intent — Telecom Service, Network, and Incident Operations - (sections 5.3, Appendix C)



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
