**Model:** Claude Sonnet 5.5

### User

what is the intent of running S04-03 through S04-12 steps? to modernize the code with each stage? or prepare .md files that incorporate the modernization aspects that will be applied to the code through the creation of the prd in S06?

### Assistant

It is both, but not in the order you describe. The project documents say each S04 stage produces documents first and then a small code change. The PRD in S06 is written after those code changes, and it does not carry them.

**What each S04 stage does**

`Execution Plan.md` (Phase 4, lines 269 to 276) splits every stage into two gated halves:

- Half A (analyse and design). It writes the documents under `docs/NN-<challenge>/`. No code changes. The stage needs PASS or CONDITIONAL PASS before Half B starts.
- Half B (implement and prove). It makes the code change that Half A named. It adds a test and records before and after evidence. The plan says code changes stay "small and reviewable".

So S04-03 through S04-12 do modernize the existing code, a little at a time. S04-10 is one example: Half A wrote the six documents. Half B changed `domain_service.py` and `policy.py` and added 18 tests.

**What the documents are for**

Half A documents also feed later stages. The plan says each stage "feeds Phase 5, Phase 5R, Phase 6, and Phase 9":

- S05R. Any term a design needs that the semantic layer lacks goes in as an "Open question for S03" line. S05R folds these into the YAML and raises the version.
- S06 (the PRD). Its input list names design files from S04, for example `target-access-matrix.md`, `ai-action-policy-design.md`, and `degraded-mode-design.md`. The plan says the PRD "can then require controls that already have a design".

**What S06 and S07 do**

- S06 writes `docs/prd/prd.md` and `traceability.md`. The PRD says what the governed application must do. It lists routes to build (such as `/alarms/storms/{id}`, `/ai/recommend/{id}`, `/approvals/{id}`, and `/audit/{correlation_id}`) and routes it will not build. S06 itself changes no code.
- S07 builds the application "only from the PRD". It adds new capability on top of the code that S04 already hardened.

**Where your two readings fit**

| Your reading | Verdict |
|---|---|
| Modernize the code with each stage | True for Half B of each S04 stage. The change is small. |
| Prepare `.md` files that the PRD uses to apply the modernization in S06 | Half true. The `.md` files feed the PRD, but the code change is not deferred to S06. S06 writes requirements, and S07 builds the new flow. |

There is one exception. S04-03 through S04-12 harden the controls (access, secrets, policy, logging, AI limits, speed, failure handling). The new product flow (the storm view, the recommend route, the approval route) is built in S07, not in Phase 4.


## 2026-10-11 19:50

**Model:** Claude Sonnet 5.5

### User

what is the difference between the hardening that takes place in the S04-03 through S04-12 versus the new capabilities that S07 adds? What did we not do the hardening and new capabilities all at once as part of S06-S07 using the analysis and design outputs (of all the Half As) done in S04-03 through S04-12?

### Assistant

The plan does not state one reason for the split. The reasons below come from its rules and from what happened in S04-10.

**The difference**

| | S04-03 to S04-12 Half B (hardening) | S07 (new capability) |
|---|---|---|
| What it changes | The code that already exists: `main.py`, `domain_service.py`, `ai_gateway.py`, `audit.py`, `access.rego` | New code under the PRD's route list |
| Size | "Small and reviewable", one challenge at a time | The whole governed demo flow (topology lookup plus alarm-storm dedupe) |
| Source | The Half A design for that one challenge | The PRD and the S05R YAML version only |
| Output | A code fix, a test, and before and after evidence | The application, which the tests then run against |
| Example (S04-10) | Load `devices.csv` once and cache the policy program lookup. `GET /records` went from about 14 ms to about 6 ms. | A storm view that groups alarms by `storm_batch_id`, which no current route does |

**Why not do both in S06 and S07**

1. The Half B tests are inputs to S07. The phase table in `Execution Plan.md` (line 94) lists "Phase 4 Half B tests" as an input to Phase 7. Line 106 says the second model's app runs the same tests as the first. Without Half B, those tests would not exist when S07 starts.
2. Half B checks whether a Half A design works. In S04-10, Half A named the CSV read as the main cost. Half B's measurement showed the policy program lookup cost more on each route. Half B also found that matching ids on `device_id` alone changes what `load_record` returns for ids like `SIT-00002`. A PRD written straight from Half A would have required the wrong fix. The plan says the PRD can require only controls that already have a design, and Half B shows that the design holds against real code.
3. A failure in a combined build has many possible causes. If S07 hardened and built together, a failing test could come from the design, the PRD wording, the model's build, or the old code. Hardening first removes the old code from that list.
4. The second model needs a fixed starting point. S08 gives another model the same PRD and the same YAML, then compares results. That comparison only means something if both builds start from the same hardened baseline. S05R also has to fold every "Open question for S03" line into the YAML before the PRD cites it.
5. The playbook requires the evidence. The final checklist item D4 asks for a Half A design and Half B evidence for every Phase 4 challenge. A combined S07 would leave no per-challenge before and after record.
6. Changes stay small. Line 274 says a characterization test that locks a defect is replaced in the same commit that fixes it. That rule needs one defect fixed at a time.

**The line is not perfectly clean**

- S04-06 Half B adds `ai_action.rego`, which is new policy code.
- S05-14 Half B adds a `/audit/{correlation_id}` route before S07 begins.

So the working boundary is this: Phase 4 and 5 add or change only what a single control needs. S07 builds the product flow that uses those controls.
