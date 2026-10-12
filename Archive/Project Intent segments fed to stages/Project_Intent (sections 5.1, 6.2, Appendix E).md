# Project Intent — Telecom Service, Network, and Incident Operations -  (sections 5.1, 6.2, Appendix E)



### 5.1 How this packet maps to the challenge guide

**Primary method:** inherited brownfield repo. Inspect first. Replay the API and the ETL. Treat a missing control as missing.

**Do not:** tidy Repo files on day one, invent a severity cutoff, or treat `docs/architecture/known-gaps.md` as the full defect list.

**Semantic layer method:** follow `Semantic_Layer_capture.pdf`.

- Markdown explains it.
- YAML defines it.
- JSON Schema validates it.
- Tests protect it.
- Generated JSON serves it.

YAML is the core because people can read it, machines can parse it, Git can diff it, and a second model can consume it.



### 6.2 Semantic layer done

- [ ] The folder matches `Semantic_Layer_capture.pdf`.
- [ ] `glossary.md` explains terms in everyday words.
- [ ] YAML defines entities, relationships, statuses, rules, metrics, access, and AI context.
- [ ] Status words used in code, docs, and CSV are listed. Collisions such as `gold` used as incident severity are named.
- [ ] JSON Schema validates the YAML.
- [ ] Tests fail when a required entity, status, or rule is missing.
- [ ] Generated JSON is produced from YAML, not edited by hand.



## Appendix E — Semantic layer file map

Copy this layout from `Semantic_Layer_capture.pdf`. Fill it from this telecom packet. Do not add a parallel meaning file outside this tree.

```text
semantic-layer/
├── README.md
├── glossary.md
├── entities.yaml
├── relationships.yaml
├── status-taxonomy.yaml
├── business-rules.yaml
├── metrics.yaml
├── access-semantics.yaml
├── ai-context-policy.yaml
├── schemas/
│   └── semantic-layer.schema.json
└── tests/
    └── test_semantic_layer.py
```

| File | What it must define for this domain |
|---|---|
| `glossary.md` | Everyday meanings for device, circuit, alarm, incident, service order, AI invocation, topology, SLA, remediation, guardrail. |
| `entities.yaml` | The six domain entities and their fields from `docs/domain-specific-spec.md`. Mark which fields the API actually reads today. |
| `relationships.yaml` | Device to alarm. Circuit to customer and incident. Incident to AI invocation. Order to circuit. Event to entity. |
| `status-taxonomy.yaml` | Allowed values for severity, incident status, order status, guardrail status, approval. List collisions found in the CSVs. |
| `business-rules.yaml` | Missing id must not return another device. AI output cannot execute. Alarm last_seen cannot precede first_seen. Shared admin is not least privilege. |
| `metrics.yaml` | SLA breach risk, alarm-storm size, token count per invocation, cost per correlated incident, quarantine rate, retry count. |
| `access-semantics.yaml` | Map domain personas to actions, resources, purpose, scope, and risk. Scope is the set of records a persona may touch. Do not keep `clinician` as a telecom role. |
| `ai-context-policy.yaml` | Which fields may enter a prompt, required output schema, model provenance, approval gate, and fail-to-person behaviour. |

YAML is the source of truth. If the PRD and the YAML disagree, fix the PRD or record an ADR. Do not keep two meanings.

The control designs (D4) may need a term the YAML lacks. A design does not define it. It writes an "Open question for S03" line. Stage S05R folds those terms into the YAML, raises the version, and reruns the S03R checks before the PRD is written. The PRD and the second model use that revised version. After S05R, a YAML change needs an ADR.

A review of this tree can fail. That review is S03R, or the S03R rows that S05R reruns. Then stage S03F applies the review's fix list, keeps the version, and rebuilds and retests. S03R then runs again in a fresh chat. S03F runs only until the PRD cites the version.