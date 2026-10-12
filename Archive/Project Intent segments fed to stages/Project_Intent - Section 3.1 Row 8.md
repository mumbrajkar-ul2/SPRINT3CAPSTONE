# Project Intent — Telecom Service, Network, and Incident Operations -  Section 3.1 Row 8


## 3. What is expected

### 3.1 Decisions you must write down first

Use the trainer’s words and the repo files. If a row is missing from the packet, write Unknown. Do not guess a business cutoff.

| # | Question | Answer from this packet |
|---|---|---|
| 8 | What still works if the AI path is down? | Unknown as a designed degraded mode. `/health` and `/records/{id}` do not call the model. `/ai/summarize/{id}` has no timeout, no circuit breaker, and no fail-to-person path. The failure-injection runbook names an AI timeout drill. The runbook is a draft. |

