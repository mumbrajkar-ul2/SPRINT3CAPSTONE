# How stages 0A through 20 cover the 16 transformation challenges

This note is a plain-language rewrite of “How the product spine addresses the 16 challenges.” The counts and the file names are the same. The sentences are shorter. Each product word is followed by what it means in this note.

## The two guides

The challenge guide lists 16 jobs for taking over a system that already exists and is in use. Each job names the outputs the team must produce. Each job also has a pass test.

The Spine is the ordered production plan. It runs from stage 0A through stage 42. Each stage must save named files before the team moves on.

This note covers stages 0A, 0B, 0C, and stages 1 through 20. That is the range in the source comparison. Stages 21 through 42 appear only when they are the later stage that requires a file this range leaves out.

## What was counted

The comparison counts 110 requirements.

A requirement is one of three things.

- A named output in the challenge. The guide calls this an expected deliverable.
- The pass test for that challenge. The guide calls this the acceptance standard.
- A check the team must run, when that check is a separate piece of work from the named outputs. The guide calls this the execution focus.

Three results follow from that count.

- 11 requirements are the same work a stage in this range must already do.
- 39 requirements have a related file. The file is smaller, earlier, or still marked provisional. Provisional means the file is a draft and is not the final decision.
- 60 requirements have no required file in stages 0A through 20.

The row-by-row table is in the canvas file Challenge–spine mapping. A canvas is a live view you can open beside the chat. The table can be filtered to Match, Partial, or No mapping. Match means the stage requires the same work. Partial means a related file exists and the pass test is still open. No mapping means this range does not require that work.

## Which challenges this range covers

The table uses five labels. Each label is defined here so a row can be read on its own.

- Pass test met, outputs required. The pass test is met, and each named output has a required file in this range.
- Pass test met, one output missing. The pass test is met. One named output still has no required file.
- Related files, pass test open. Some related files exist. The pass test is still open.
- Only a related file or two. There is no full match. At most two related files exist.
- No required file in this range. No stage from 0A through 20 requires this work.

| What stages 0A through 20 do | Challenges |
| --- | --- |
| Pass test met, outputs required | 1. Understand Existing Repo |
| Pass test met, one output missing | 2. Establish Behavioural Baseline |
| Related files, pass test open | 4. Secrets and Encryption. 7. CI/CD and Supply Chain. 9. AI Security and Guardrails. 12. Cost and AI FinOps. 13. Automated Security Validation. 15. Production Readiness Gate. |
| Only a related file or two | 3. Identity and Least Privilege. 5. Infrastructure as Code. 8. Observability and Traceability. 10. Performance and Scalability. 11. Reliability and Failure Engineering. 14. Auditability and Compliance Evidence. 16. Production Evidence Pack. |
| No required file in this range | 6. Policy as Code |

Worked example. Challenge 1, Understand Existing Repo, is in the first row. The match list for that challenge has six items: the architecture map, the component list, the business flows, the data and integration map, the risk list, and the pass test. Challenge 2, Establish Behavioural Baseline, is in the second row. Three items match. The missing output is a data-quality profile of the synthetic data. Synthetic data is made-up data used in place of production data.

Stages 0A through 20 discover the current system, decide whether to use a model, write the product intent and the design, and start the build. The control work and the proof work are required mainly from stage 21 onward. That work is least privilege, secrets, infrastructure as code, policy, the build-and-release path, the production trail, load tests, failure injection, abuse-case tests, the audit chain, the production go or no-go, and the evidence pack.

Later stages save written controls, approval gates, and compliance matrices. An executable policy, with an allow case and a deny case, is absent from stages 0A through 42.

## Requirements this range already requires

### 1. Understand Existing Repo

Stages 0A, 5, and 7 must produce these files.

- high-level-architecture.md, system-landscape.md, and architecture-drift.md. These are maps of how the system is built today, plus a note of where the code has drifted from that shape. Drift means the code no longer matches the last written design.
- technology-inventory.md and brownfield-inventory.md. These list the parts in the repository. Brownfield means the system already exists and is in use.
- workflow-overview.md, current-process-map.md, and business-workflow-map.md. These record the business steps the system carries out.
- data-flow-overview.md, integration-overview.md, and integration-landscape.md. These record where data moves and which other systems connect.
- initial-risk-register.md, dependency-hotspots.md, and technical-debt-register.md. These record known risks, fragile dependencies, and code that will be costly to change. A dependency is a library or another system this one needs.
- Pass test. The files cite code, data, configuration, tests, or documents already in the repository. Stage 0A and the global contract also require each claim to be marked as a verified fact, an inference, an assumption, or an unknown. The global contract is the rule set that applies to every stage.

### 2. Establish Behavioural Baseline

Stage 7 produces the snapshot. Stage 16 checks it again after changes.

- baseline-test-results.md. This file holds the results of tests that already exist, run where that is safe.
- baseline-behaviour.md and critical-workflow-inventory.md. These record what the API and the data jobs do today. An API is the interface other programs call. The data jobs extract data, change it, and load it. The guide calls those jobs ETL.
- Pass test. The team can tell intended old behaviour from a defect. Stage 16 behavior-difference-report.md explains every difference from the Stage 7 snapshot.

### 9. AI Security and Guardrails

Two requirements match. The rest of this challenge is still in the “related files, pass test open” row.

- Stage 8 deterministic-vs-ai-boundaries.md and Stage 20 deterministic-ai-boundary.md record where a model output can change an operational decision. Deterministic code returns the same result for the same input. Model output can vary.
- Stage 19 requires structured outputs. The model must return named fields in a defined shape.

## Related files that cover less than the challenge asks

Each item below has a file in stages 0A through 20. The file covers part of the topic. The challenge pass test is still open.

### 1. Understand Existing Repo

- Stage 0A technology-inventory.md records the technologies found in the repository. An AI subsystem can appear in that list if the repository contains one. A separate file whose only job is to describe the AI subsystem is still absent.
- Stage 0B scope-boundaries.md records what this engagement may change. Stage 2 decision-rights-map.md records who may decide. A list of who owns each system component is still absent.

### 2. Establish Behavioural Baseline

- Stage 7 writes characterization-test-plan.md. A characterization test locks in current behaviour before a change. Stage 16 runs those tests after the change. The pre-change record is the plan plus the results of tests that already existed.
- The current defect list is Stage 7 security-code-quality-findings.md and technical-debt-register.md. Those files list security issues and costly code. A list that splits intended old behaviour from bugs is still a separate output.

### 3. Identity and Least Privilege

- Stage 10 security-architecture.md, Stage 12 security-spec.md, and Stage 20 access-control-implementation.md describe authorization. Authorization is the rule for who may do an action. A grid of role, resource, and context is still absent.

### 4. Secrets and Encryption

- Stage 7 security-code-quality-findings.md looks at security and at how the code handles data. A secret is a password, a key, or a token. A required search for secrets in logs, and a required note of missing encryption, are still absent.
- Stage 15 changes configuration as part of the cleanup. A cleaned configuration model, with proof that example files contain no real secret, is still absent.
- Stages 11 and 12 cover personal data and a security spec. Personal data includes a name or an account number. A checklist of how each sensitive field is handled is still absent.

### 5. Infrastructure as Code

- Stage 0B environment-access-boundaries.md records who may enter each environment. Stage 10 deployment-architecture.md describes the target way to deploy. An environment model a new person can rebuild from is still absent.
- Stage 14 dependency-sequence.md lists the order of the migration. A list of what the deployment depends on is still absent.

### 7. CI/CD and Supply Chain

- Stages 7 and 16 produce dependency-map.md and dependency-scan-summary.md. The map lists libraries. The scan summary lists what the scan found. A risk register with an owner and a disposition for each dependency is still absent. Disposition means the recorded decision: fix, accept, or defer.
- Stage 16 saves security-scan-summary.md and dependency-scan-summary.md. Those are results. A written scan plan is still absent.
- Stage 18 evidence-checklist.md lists the proof a work item must include before that item is done. A release checklist produced by the pipeline is still absent.

### 8. Observability and Traceability

- Stages 10, 12, and 20 include observability. Observability means logs, metrics, and traces from the running system. A log is a text record. A metric is a number, such as error count. A trace follows one request across parts of the system. Stage 20 also says to add hooks. A hook is the place in the code that records the signal.
- A design that ties together the screen, the API, old jobs, data jobs, the model call, the policy decision, the human approval, and the audit event is still absent.
- A log field list can sit inside Stage 12 observability-spec.md. A file whose name is the log schema is still absent.

### 9. AI Security and Guardrails

- Stages 8 and 20 record the boundary between ordinary code and model output. A diagram of the trust boundary across the prompt, the retrieved text, the tools, and the output is still absent. A prompt is the instruction text sent to the model.
- Stage 11 retrieval-strategy.md and Stage 19 grounding-results.md check whether an answer stays tied to retrieved text. Grounding means the answer points at source text. A security check on whether that retrieved text is trusted is still absent.
- Stages 8, 9, and 10 save risk lists for the product and the architecture. A risk list that contains only AI risks is still absent.
- Stage 19 records quality results for hallucination, unsupported claims, abstention, and grounding. Hallucination means the model states a fact the source text does not support. Abstention means the model refuses to answer. These are quality checks. A security guardrail test pack is still absent.
- Stage 19 prompt-registry.md and model-configuration.md store the prompt text and the model settings under version control. A design that ties one decision to one model version is still absent.
- Stage 0B provisional-human-approval-rules.md and Stage 2 approval-authority-map.md record who must approve, as a draft. Stage 23 is the stage that requires the human approval path for model output.
- The pass test asks that a model recommendation become an operational action only after the required control. Stages 8 and 20 require the split between ordinary code and model output. The enforced approval gate is Stage 23.

### 10. Performance and Scalability

- Stage 0C and Stage 19 record how long the model call takes. Latency is the wait from request to answer. A load profile of the API, the data jobs, and the database is still absent.
- Stage 10 uses scalability as one reason to choose an architecture. Scalability means the design can take more traffic or more events. Recommendations drawn from a measured load test are still absent.

### 11. Reliability and Failure Engineering

- Stage 20 says the application must implement idempotency. Idempotency means sending the same request twice leaves the same end state as sending it once. A written idempotency plan and failure-test evidence are still absent.

### 12. Cost and AI FinOps

- Stage 0C writes a draft cost envelope: preliminary-finops-baseline.md, a cost per request, and a cost per case. A token is a chunk of text the model reads or writes. TCO means total cost of ownership. The numbers are provisional.
- Stage 8 economics-baseline-reconciliation.md drops the AI cost numbers if the team decides not to use a model.
- Stage 19 quality-latency-cost-results.md records quality, wait time, and cost for the model layer.
- cost-scenarios.md and the volume notes in Stage 0C sketch cost. A measured cost per workflow is still absent. Stage 32 is the stage that requires cost per workflow and cost per business outcome.
- Stage 0C includes retries inside the token and loop budgets. A retry sends the model call again. A separate analysis of retry cost and fallback cost is still absent. Fallback means the path used when the model call fails.
- Stage 0C volume-assumptions.md includes event volume where the repository already has evidence. The cost of storing logs, metrics, and traces is still absent.
- The pass test asks for cost per business outcome, such as cost per case closed. Stage 0C sets draft ceilings for cost per request and cost per case. The measured cost per outcome is Stage 32.

### 13. Automated Security Validation

- Stage 16 runs security scans and dependency scans and saves the summaries. The abuse cases named in the challenge are still absent from that plan. An abuse case is a deliberate unsafe action, such as a user without permission.
- Stages 7 and 16 save technical-debt-register.md and remaining-debt-register.md. Those lists record leftover engineering work. A security remediation backlog, with a fix for each failed control, is still absent.
- The pass test asks for repeatable proof of the security claims. Stage 16 repeats the scans. Repeatable tests for the abuse cases are still absent.

### 14. Auditability and Compliance Evidence

- Stage 20 says the application must include audit hooks. An audit hook records who did an action. The evidence chain for one business event is still absent.

### 15. Production Readiness Gate

- These stage-done files exist: repo-transformation-readiness.md, spec-readiness.md, intelligence-release-gate.md, and application-readiness.md. Each file says whether that stage can move on. A production readiness checklist for release is still absent. Stage 27 is the stage that requires production-readiness-checklist.md.
- Risk lists exist in stages 0A, 10, 14, and 18. A single residual-risk register for the production decision is still absent. Residual risk is the risk still open after the controls in this range.
- Stage 2 decision-rights-map.md records who may decide. A table of who owns each production risk is still absent.
- Stage 9 non-goals.md lists work the product will leave out. Stage 16 remaining-debt-register.md lists debt still open. Together they are a start on the deferred-work list.

### 16. Production Evidence Pack

- Stage 7 and Stage 16 save test results. Stage 16 saves scan summaries. Stage 19 saves model evaluation results. Each result is its own stage file. A single evidence pack that holds them is still absent.

## Work stages 0A through 20 leave out

The items below have no required file in this range. The source comparison left them off the match list and off the related-file list.

### 2. Establish Behavioural Baseline

- A data-quality baseline made by profiling the synthetic data. Profiling means measuring what is in the data: missing fields, bad values, and row counts.

### 3. Identity and Least Privilege

- A current role matrix for human roles, service accounts, AI identities, and vendor accounts. A service account is an identity a program uses. An AI identity is the identity the model or agent uses when it calls a tool.
- A policy input model with five inputs: role, resource, purpose, scope, and risk. This includes RBAC and ABAC. RBAC grants access from a job role. ABAC grants access from extra facts, such as purpose and risk.
- Negative access tests. A negative test checks that a forbidden caller is denied.
- A privilege-reduction backlog. A privilege is a permission an account currently has. The backlog is the list of permissions to remove.
- Pass test. An access decision uses role, resource, purpose, scope, and risk together.

### 4. Secrets and Encryption

- A secrets inventory.
- A remediation plan for unsafe secrets. Remediation means the steps that remove or replace the unsafe secret.
- A rotation evidence plan. Rotation means replacing a secret on a schedule and recording that the old secret is retired.
- Pass test. Committed code and example configuration can run without a real secret in the file.

### 5. Infrastructure as Code

- An infrastructure-as-code gap report. Infrastructure as code means files that create the environment, so a new person can rebuild it. The report covers incomplete files, hidden setup steps, environment drift, gaps in local startup, and dependencies people assume by hand. Environment drift means the running machines differ from those files.
- A setup guide a new team can follow.
- A map of who owns each configuration item.
- Pass test. A new team can rebuild the intended local environment from the written steps.

### 6. Policy as Code

Policy as code means a rule the computer executes, such as allow or deny, with tests. Stages 0A through 42 save written rules, control matrices, and approval tests. An executable policy file is absent from that list. Stage 12 business-rules.md is a specification for people and for the build.

- A policy catalogue for access, AI approval, data use, operational safety, and production readiness.
- The executable rules.
- Allow examples and deny examples.
- Tests for those rules.
- An exception model. An exception is a recorded case where a rule is waived, and who waived it.
- Pass test. At least one high-risk business decision is controlled by an executable policy. The tests include one case that should pass and one case that should fail.

### 7. CI/CD and Supply Chain

- A pipeline improvement plan. The pipeline is the automated path that builds, tests, and releases the software. CI/CD is the name for that path. The plan covers missing pipeline stages, too few test stages, and release steps people still do by hand.
- An SBOM recommendation. An SBOM is a software bill of materials: the list of libraries and other parts inside a build.
- Pass test. The pipeline saves evidence of what it checked and what it released. Command output alone leaves that evidence out.

### 8. Observability and Traceability

- A catalogue of operational metrics.
- A dashboard sketch. A dashboard is a screen of those metrics.
- An SLO proposal. An SLO is a service level objective: a stated target, such as 99 percent of requests finishing within a set time, over a named window.
- One example that reconstructs an incident from logs and traces.
- Pass test. The team can explain one business event from the first user action through the final system action, using that production trail.

### 9. AI Security and Guardrails

- Prompt-injection tests. Prompt injection means untrusted text tries to override the model’s instructions.
- Rules for what the system does with unsafe model output.

### 10. Performance and Scalability

- A performance baseline for the API, the data jobs, event volume, data access, and chains of synchronous calls, using the synthetic data. Synchronous means the caller waits for each step to finish before the next step starts.
- A bottleneck list. A bottleneck is the step that limits how much work gets through, or that adds the most wait.
- Load scenarios. A load scenario is a defined volume of traffic or events used for the measurement.
- Findings about slow or heavy data access.
- Pass test. Each technical bottleneck is tied to a business effect, such as a longer case time or a missed response target.

### 11. Reliability and Failure Engineering

- A failure-mode catalogue, with tests that inject duplicate events, stale data, an AI timeout, a partner or API failure, a gap in telemetry, and a partial batch failure. Stale data is older than the decision should use. Telemetry is the logs, metrics, and traces. A partial batch failure means some rows in a job succeed and some fail.
- A retry and circuit-breaker strategy. A retry sends the call again after a failure. A circuit breaker stops calling a dependency after repeated failures, so one outage does not trigger a pile of new calls.
- A degraded-mode design. Degraded mode is the smaller set of actions that still run when a dependency is down.
- Recovery evidence. This is the record that the system returned to its normal path after a failure.
- Pass test. The design states which actions continue safely when a dependency fails.

### 12. Cost and AI FinOps

- The cost of observability volume. That is the cost of storing and sending logs, metrics, and traces.
- An optimization backlog. That is the list of later cost cuts.
- The fields a FinOps dashboard must show. FinOps in this guide means tracking model cost and platform cost against the business work the system completes.

### 13. Automated Security Validation

- Negative security tests.
- A scanning checklist.
- Abuse-case evidence for a caller without permission, a bypass of a policy, prompt injection, leakage of sensitive data, and an unsafe AI action.

### 14. Auditability and Compliance Evidence

- An audit gap report. The report lists which facts about a decision the system still cannot prove.
- A decision provenance model. Provenance here means the record of how one decision was made: the actor, the request, the data used, the model and version, the policy result, the approval, the final action, and the facts still missing.
- An evidence chain for one business event. The chain links those facts for one event.
- A map from each compliance duty to the evidence that shows the duty is met.
- One before-and-after audit example. The example shows the same kind of decision before the change and after the change.
- Pass test. The chain shows what happened, who or what influenced it, and which facts are still unproven.

### 15. Production Readiness Gate

- A production go or no-go decision. Go means release. No-go means hold the release.
- Pass test. The team states what is ready for production, what is not ready, and which risk is accepted.

### 16. Production Evidence Pack

- One final evidence pack. The pack is the set of files a reviewer uses to check the work.
- An executive summary.
- Observability evidence, reliability evidence, and FinOps evidence inside that pack.
- Runbooks inside the pack. A runbook is the written steps an operator follows during an incident.
- The production readiness decision inside the pack.
- Pass test. A reviewer checks the transformation from the pack. A spoken walkthrough is outside that pass test.

## Stage files whose names sound like the challenge

The file name sounds like the challenge. The comparison counted the file as different work, because the file holds a different record. The first sentence says what the file contains. The second sentence says what the challenge asks for.

- Stage 4 baseline-data-quality.md records whether the KPI numbers are measured well. A KPI is a business measure, such as cycle time or error rate. The behavioural-baseline challenge asks for a profile of the current data and the synthetic data.
- Stage 5 process-bottlenecks.md records delays, rework, and handoffs in the business process. The performance challenge asks for the technical steps that limit the system under a defined load.
- Stage 1 engagement-go-no-go.md records whether to start the engagement. The choices are Go, Conditional Go, or No-Go. The production-readiness challenge asks whether to release. That release decision is Stage 30, in go-no-go-criteria.md and release-outcome.md.
- Stage 13 links a requirement to a spec, a test, and the delivery evidence for that test. Challenge 8 asks for a production trace of one live event. Challenge 14 asks for the audit chain of one decision.
- Stage 11 provenance-policy.md sets rules for data lineage and for citations. Lineage means which source a data field came from. Challenge 14 asks for the provenance of a decision.
- Stage 14 rollback-strategy.md describes how to undo a migration or a cutover. A cutover is the moment traffic moves to the new path. Challenge 11 asks for evidence that the running system recovered after a failure.
- Stage 12 business-rules.md writes the business rules as a specification for the build. Challenge 6 asks for those rules as executable policy, with an allow case and a deny case.
