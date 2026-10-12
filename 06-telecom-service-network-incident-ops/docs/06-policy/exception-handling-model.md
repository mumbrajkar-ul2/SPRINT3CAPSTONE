# Exception handling model

| Field | Value |
|---|---|
| Stage | S04-06 — Policy as code (Challenge 6), Half A |
| Date / version | 2026-10-11, v1.0 |
| Author | Mangesh (FDE), drafted with Cursor |
| Status | PASS. The model answers four questions: who may waive a rule, for how long, where the waiver is logged, and how it expires. The repo has no waiver today, so every answer is PROPOSED with Team-Force as owner. Four rules cannot be waived. |
| Evidence sources | `docs/00-contract/operating-contract.md` rows 7, 8, 9, 10; `semantic-layer/business-rules.yaml`; `semantic-layer/access-semantics.yaml`; `docs/03-identity/privilege-reduction-backlog.md`; `docs/03-identity/policy-input-model.md`; `docs/06-policy/ai-action-policy-design.md`; `Project_Intent(sections 5.3, Appendix C).md`; a search of the project folder for the words waiver and waive |
| Assumptions | A waiver changes the result of one named rule for one named scope for a limited time. A waiver never comes from a request. Half B builds no waiver handling. This model is for stage S09 and for later stages. Mangesh (FDE) acts for Team-Force (`operating-contract.md` row 10). |
| Unresolved issues | The other members of Team-Force are Unknown. The longest time a waiver may last is Unknown. The place that stores waivers is Unknown. No persona names the person who may waive a rule. |
| Residual risks | The person who asks for a waiver and the person who approves it may be the same person. `operating-contract.md` records that risk for code review in row 7. A waiver register that nobody reads gives no protection. Stage S09 should list both as accepted risks. |

## What this file is

This file says how a person may set aside one policy rule for a limited time, and what record that leaves. It also says which rules nobody may set aside.

Half A writes this model. No code, Rego, or test changes in this half.

Claim labels: **Verified Fact**, **Inference**, **Assumption**, **Unknown**. PROPOSED items name an owner. The owner is Team-Force.

## What the repo says today

| Fact | Evidence | Label |
|---|---|---|
| Team-Force owns every PROPOSED item. Mangesh (FDE) acts for Team-Force. A team name is not an approver of a live change. | `operating-contract.md` row 10 | Verified Fact |
| One reviewer approves a code change before it merges. | `operating-contract.md` row 7 | Verified Fact |
| A live network change needs a named human and a stored approval id. The row is Prohibited, and no waiver can lift it. | `operating-contract.md` row 9 | Verified Fact |
| Work stops when the next change would push a config, provision a circuit, run an automated remediation, or hide a real outage. | `operating-contract.md` row 8 | Verified Fact |
| Every rule in `business-rules.yaml` has `enforced_today: false`. | `business-rules.yaml`, file header and each rule | Verified Fact |
| The words waiver and waive appear nowhere in the project's Markdown, YAML, Python, Rego, or JSON files. | Search of the project folder in this stage | Verified Fact |
| No persona or role id names a person who may waive a rule. | `access-semantics.yaml` `personas` and `api_roles_today` | Verified Fact |
| An AI recommendation must not silently become an operational decision. | `Project_Intent(sections 5.3, Appendix C).md`, Appendix C | Verified Fact |

## The four answers

| Question | Answer | Label | Owner |
|---|---|---|---|
| Who may waive a rule? | The owner of that rule. For a PROPOSED rule the owner is Team-Force, and Mangesh (FDE) acts for it. A different person writes the request when one is available. When Mangesh writes and approves the same waiver, the register marks it self-approved. | PROPOSED | Team-Force |
| For how long? | Until the date the waiver names. That date is no later than the stage S09 review. The longest span the repo allows is Unknown. This model sets no number of days. | PROPOSED | Team-Force |
| Where is it logged? | In two places. First, a row in a waiver register file at `docs/06-policy/waiver-register.md`. Second, an audit row in `logs/audit.log` when the waiver is granted and each time the policy uses it. The file does not exist yet. | PROPOSED | Team-Force |
| How does it expire? | The waiver stops applying on its date, or at the S09 review, whichever comes first. After that the rule applies in full. The register row stays and is marked expired. A renewal is a new waiver with a new row and a new approval. | PROPOSED | Team-Force |

How the policy reads a waiver. The server loads waivers from a policy data file. A request cannot carry a waiver. A waiver names one rule id and one scope. The policy ignores a waiver whose date has passed. This reading is PROPOSED. Half B builds none of it.

### What a waiver record holds

| Part | What it says |
|---|---|
| Waiver id | A short identifier for this waiver |
| Rule id | The YAML id of the rule, for example `rule.no_default_role` |
| What changes | The result that changes and for which scope |
| Reason | Why the rule cannot apply |
| Requester | The named person who asked |
| Approver | The named person who accepted. Marked self-approved when the same as the requester |
| Granted on | The date |
| Expires on | The date the waiver stops |
| Evidence | The file or test that shows the reason |

### Open questions for S03

Open question for S03: the term `waiver` (a dated, named exception to one rule id) has no concept id. This design needs it to name what the register and the audit row hold.

Open question for S03: the audit action names for a waiver being granted and a waiver being used have no ids. This design needs them to write the two audit rows. `status.code.audit_action.record_read` and `status.code.audit_action.ai_summary` are the only two audit action ids today.

Open question for S03: no persona or role id names the person who may waive a rule. This design names Team-Force (`operating-contract.md` row 10). Team-Force is a team. It is not a persona.

## Which rules can be waived

| Rule id | Can it be waived | Why | Who decides |
|---|---|---|---|
| `rule.ai_recommendation_needs_policy_approval_audit_before_state_change` | No | Operating contract row 9 is Prohibited. A change to a live device always needs a policy allow, an approval id, and an audit row. | Nobody |
| `rule.ai_output_cannot_execute` | No | Appendix C says an AI recommendation must not silently become a decision. | Nobody |
| `rule.forbidden_fields_never_enter_prompt` | No | `mgmt_ip` and `credential_profile` are locked out of prompts in `policy.prompt_fields`. | Nobody |
| `rule.denied_access_is_audited` | No | A waiver would hide the refusal itself. | Nobody |
| `rule.stale_topology_blocks_recommendation` | Yes, narrowly. PROPOSED. | The waiver may lower BLOCK to HOLD_FOR_REVIEW for one named device. It never gives RECOMMEND_ONLY or EXECUTE. | Team-Force |
| `rule.no_default_role` | Yes. PROPOSED. | A local demo may need a call with no role header. Today the server fills in `operator` with no record (F15). A waiver puts that choice on record. | Team-Force |
| `rule.shared_admin_not_least_privilege` | Not recommended. See EX-06. | `role.admin` has no row in the target matrix. | Team-Force |
| A grant in the target matrix (TA-01 to TA-34) | Not a waiver. | A person with no grant needs a new row accepted in writing, not a waiver. | Team-Force, `operating-contract.md` row 10 |
| A readiness check (area 5) | Yes. PROPOSED. | Stage S09 may list a missing check as an accepted risk in the readiness decision. | Mangesh (FDE), acting for Team-Force |

Worked example. A demo needs one `GET /records/REC-0001` call with no role header. Rule `rule.no_default_role` would refuse it. Mangesh writes a register row for that rule. The row has a requester, an approver, a reason, and an expiry date. The row is marked self-approved when he is both. The audit log gets one row when the waiver is granted. After the date, the call is refused again. The date in a real row is chosen by the requester. This model does not choose one.

## No emergency override

A network outage does not unlock a live change. The change still needs a named human to write an approval id and an audit row first. If no `network_engineer` is available, the stop condition in row 8 applies and the work stops. The approval is the fast path. No waiver is.

## Findings

| id | finding | evidence | impact | risk | confidence | open questions |
|---|---|---|---|---|---|---|
| EX-01 | Every business rule is set aside today without a record. | Verified Fact. `enforced_today: false` on every rule in `business-rules.yaml`. | A reader cannot tell a rule that is waived from a rule that is not built yet. | A rule can look enforced when it is not. | High | None. |
| EX-02 | The repo has no waiver, no waiver register, and no persona that may waive. | Verified Fact. Search result for waiver and waive. `access-semantics.yaml`. | The model has nothing to extend. All four answers are PROPOSED. | A waiver granted in chat leaves no record. | High | Three open questions for S03 above. |
| EX-03 | An approval id approves one change. It does not waive a rule. | Inference from `concept.approval` and `operating-contract.md` row 9. | A person must not use an approval id to skip the audit row or the policy allow. | The two terms could be confused in code. | Medium | None. |
| EX-04 | The requester and the approver may be the same person. | Verified Fact. `operating-contract.md` row 10 names one known member, Mangesh (FDE). The other members are Unknown. | A self-approved waiver has no second check. | A waiver nobody questions. | High | Who else is in Team-Force is Unknown. |
| EX-05 | Four rules cannot be waived by anyone. | Verified Fact. `operating-contract.md` row 9. Appendix C. `policy.prompt_fields`. `rule.denied_access_is_audited`. | The policy needs no waiver handling for these four. | A later stage adds a waiver for one of them. | High | None. |
| EX-06 | `role.admin` can be denied outright, or kept through a dated waiver. Recommended: deny outright. | Verified Fact. `target-access-matrix.md`: `role.admin` has no row. K02: admin reads `REC-0001` today. | Existing tests that send `X-User-Role: admin` fail after Half B wires the policy. | A waiver for admin reads weakens `rule.shared_admin_not_least_privilege` and could outlast its date. | Medium. The recommendation is a design choice. | Decision for acceptance: deny admin and replace the admin tests, or grant one dated waiver. |

## Lifecycle

This file cites `docs/00-contract/operating-contract.md` rows 7 to 10 and `docs/03-identity/privilege-reduction-backlog.md` for PB-04 (the default role header) and for the line that stage S04-06 replaces the admin-any rule. Stage S04-06 Half B builds no waiver handling. Stage S09 reads the waiver register, lists every self-approved waiver as an accepted risk, and checks that no waiver is past its date.
