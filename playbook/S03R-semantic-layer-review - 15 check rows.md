# S03R — Semantic layer review - 15 check rows

## Required analysis
Write one row per check. Each row: check id, PASS / FAIL / NOT APPLICABLE, file and line or id cited, one-sentence reason.
Checks:
R1. The tree matches the capture PDF exactly, plus only generated/ and build.py, and the README says why those two exist.
R2. Every YAML item has a source list or proposed: true with an owner.
R3. Every status word that appears in the CSVs (per data-quality-baseline.md) appears in status-taxonomy.yaml, or is listed as a collision.
R4. The collisions block names gold/bronze severity, status words in hostname and vendor, REC-0001 reused, and clinician.
R5. business-rules.yaml holds the six required rules, each with an id.
R6. access-semantics.yaml covers all seven personas and lists clinician under removed_roles.
R7. ai-context-policy.yaml forbids mgmt_ip and credential_profile, names the four outcomes, names fail-to-person, and copies agency and approval point per AI use from ai-qualification.md with no change in meaning.
R8. No AI use in the YAML has execute agency.
R9. The glossary defines every term the YAML uses, in everyday words, and the meanings agree.
R10. The schema validates every YAML file. Run the tests and build; paste the output.
R11. Deleting generated/ and running build.py reproduces identical files.
R12. No target number, cutoff, or threshold appears without PROPOSED and an owner.
R13. No password, key, or token value appears anywhere in the tree.
R14. Failure-list check from playbook/README.md: items 1 to 8, one row each.
R15. Plain speech: pick three glossary entries at random and state whether a reader new to telecom would know what to picture.
