# YAML and PRD hashes after the second-model run

| Field | Value |
|---|---|
| Stage | S08 Part 3. This file records the same hashes again after the second app was built and after both apps ran the shared suites. |
| Date / version | 2026-10-13. Semantic layer `1.2.1`. PRD `v1.9`. Compared with `docs/model-comparison/yaml-hashes-before.md`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | **PASS for the hash gate.** All 21 gate files match (20 under `semantic-layer/` and `docs/prd/prd.md`). The 15 other files match too. Checked again after the load fix of the second app: still 36 of 36 (section 7). |
| Evidence sources | `docs/model-comparison/yaml-hashes-before.md` (the 36 before hashes); the hash command in section 1, run on 2026-10-13 after the last test run; `git status` and `git log` output in section 2; `python semantic-layer\build.py --check`; `pytest semantic-layer/tests` |
| Assumptions | (1) Each hash covers the file as it sits on this Windows copy, the same copy that `yaml-hashes-before.md` hashed. (2) `__pycache__` folders are left out, as in the before file. |
| Unresolved issues | None for the hashes. |
| Residual risks | A hash proves that the bytes did not change. It does not prove that the second model read every file. The run log lists no file read, so the claim that the second model read only the attached files is an Assumption. |

Claim labels: **Verified Fact** (a command or a file read, named here), **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Result

**Verified Fact.** 36 of 36 files match in both SHA-256 and byte size. 0 files differ. The completion gate "BLOCKED if any semantic-layer file or `prd.md` changed" does not apply.

Command: a Python script read the 36 rows of `yaml-hashes-before.md`, hashed each file with `hashlib.sha256` over the raw bytes, and compared hash and size. The script ran after the last test run of this stage. Output: `36 rows in before file`, `mismatches: []`.

## 2. Other checks that agree

**Verified Fact.** `git status --short -- semantic-layer docs/prd data tests policy apps/api docs/ADR` printed nothing. The last commit is `51aa787` (2026-10-13, "S08 Part 1: semantic layer 1.2.1 (ADR 0006), PRD v1.9, second-model brief and hashes"). This commit holds the exact `1.2.1` bytes, so the residual risk in the before file (an uncommitted layer) is closed.

**Verified Fact.** `python semantic-layer\build.py --check` printed `generated/ matches the YAML. 7 files validated. Version 1.2.1.`

**Verified Fact.** `pytest semantic-layer/tests -q -p no:cacheprovider` printed `41 passed in 3.54s`. The before file recorded `41 passed in 2.62s`.

## 3. Semantic layer (20 files)

| File | SHA-256 before | SHA-256 after | Bytes before | Bytes after | Match |
|---|---|---|---|---|---|
| `semantic-layer/access-semantics.yaml` | `a74bb3b2fe18f41ece0eba250d362d98924e65ee2cf72f1bd5390fdda6b516df` | `a74bb3b2fe18f41ece0eba250d362d98924e65ee2cf72f1bd5390fdda6b516df` | 25600 | 25600 | MATCH |
| `semantic-layer/ai-context-policy.yaml` | `ed4947038cbec87f80eef531c9b94fa29993790541758c68eb858aab17fa84e2` | `ed4947038cbec87f80eef531c9b94fa29993790541758c68eb858aab17fa84e2` | 40704 | 40704 | MATCH |
| `semantic-layer/build.py` | `d6fbaf242aab085241d798b81e9524913cfeb6938a85b39ba018f4cb771e1c88` | `d6fbaf242aab085241d798b81e9524913cfeb6938a85b39ba018f4cb771e1c88` | 5217 | 5217 | MATCH |
| `semantic-layer/business-rules.yaml` | `faec3e64c62486eaf190d69cabeedc245b640669371957f39ee199947933a450` | `faec3e64c62486eaf190d69cabeedc245b640669371957f39ee199947933a450` | 25134 | 25134 | MATCH |
| `semantic-layer/entities.yaml` | `fd1b6464366f187e989bb60bab580e75f913047287d80590a9cccb24e4013bc1` | `fd1b6464366f187e989bb60bab580e75f913047287d80590a9cccb24e4013bc1` | 46819 | 46819 | MATCH |
| `semantic-layer/generated/access-semantics.json` | `e013b22342209483940ab1622b0afd44014a8a93244134edcf5829d0fba5edcf` | `e013b22342209483940ab1622b0afd44014a8a93244134edcf5829d0fba5edcf` | 29254 | 29254 | MATCH |
| `semantic-layer/generated/ai-context-policy.json` | `d098f6b570c4ae0c5b164cd0a975ce2cfc1c4d2e477c698d83031cb3c98c845c` | `d098f6b570c4ae0c5b164cd0a975ce2cfc1c4d2e477c698d83031cb3c98c845c` | 44129 | 44129 | MATCH |
| `semantic-layer/generated/business-rules.json` | `529d5a574211553faa13d4f0ba73fb5745d699f4b0464373408ba41265658a69` | `529d5a574211553faa13d4f0ba73fb5745d699f4b0464373408ba41265658a69` | 27142 | 27142 | MATCH |
| `semantic-layer/generated/entities.json` | `f90a77f6a86be2b6f5d1eca9f88f5d7d6f12f4f974e082a0ac86798208dee82f` | `f90a77f6a86be2b6f5d1eca9f88f5d7d6f12f4f974e082a0ac86798208dee82f` | 56749 | 56749 | MATCH |
| `semantic-layer/generated/manifest.json` | `f863b3ee36499434d48e78f77c7a4629ea2aca6a662739b879cc2244a2ec9af8` | `f863b3ee36499434d48e78f77c7a4629ea2aca6a662739b879cc2244a2ec9af8` | 1994 | 1994 | MATCH |
| `semantic-layer/generated/metrics.json` | `875a1cb01e652e29c15cc53e217acc52d59533226d25780eebf66a47939f5a9b` | `875a1cb01e652e29c15cc53e217acc52d59533226d25780eebf66a47939f5a9b` | 15847 | 15847 | MATCH |
| `semantic-layer/generated/relationships.json` | `f72fc4d04c62bb9fa1f92124a924d01e542207c0d48da327d5a06a17fd6cc81e` | `f72fc4d04c62bb9fa1f92124a924d01e542207c0d48da327d5a06a17fd6cc81e` | 10737 | 10737 | MATCH |
| `semantic-layer/generated/status-taxonomy.json` | `5d4c6ccfa2aeeb643c883aff20e8e9c7a0efa45791951de138a7e08d858fc3af` | `5d4c6ccfa2aeeb643c883aff20e8e9c7a0efa45791951de138a7e08d858fc3af` | 181440 | 181440 | MATCH |
| `semantic-layer/glossary.md` | `f2a06448fb5934a60f47b009c6c7e4d43457e47ddb5f95b3e40cbb0f1a7a9f2d` | `f2a06448fb5934a60f47b009c6c7e4d43457e47ddb5f95b3e40cbb0f1a7a9f2d` | 51145 | 51145 | MATCH |
| `semantic-layer/metrics.yaml` | `bff90a9d6719491b7865c6ad84af30aff80498072bbec7c8b8569700a99b319d` | `bff90a9d6719491b7865c6ad84af30aff80498072bbec7c8b8569700a99b319d` | 14874 | 14874 | MATCH |
| `semantic-layer/README.md` | `e6bb1f9ad209b515c87861a49d560730100283e8fc6cbef7e80761d49888dd81` | `e6bb1f9ad209b515c87861a49d560730100283e8fc6cbef7e80761d49888dd81` | 26913 | 26913 | MATCH |
| `semantic-layer/relationships.yaml` | `95206dba92703100ab70be5c77eaf8144d8e01ed81d8a90151435fda56a7f201` | `95206dba92703100ab70be5c77eaf8144d8e01ed81d8a90151435fda56a7f201` | 9130 | 9130 | MATCH |
| `semantic-layer/schemas/semantic-layer.schema.json` | `a88c6d51ef7e4a4ad307016e650f2f0548093ed1892820ee8ee035d247b55fc4` | `a88c6d51ef7e4a4ad307016e650f2f0548093ed1892820ee8ee035d247b55fc4` | 25201 | 25201 | MATCH |
| `semantic-layer/status-taxonomy.yaml` | `1794e726d41c0b3b1b933bfd2ede5c4b11a86dac5f3ce9e22e5e8e8c95aa4d6c` | `1794e726d41c0b3b1b933bfd2ede5c4b11a86dac5f3ce9e22e5e8e8c95aa4d6c` | 132152 | 132152 | MATCH |
| `semantic-layer/tests/test_semantic_layer.py` | `18bb870230eb89dbdca73dc0c1a6e8742a501fc44b110a12488218af8ba8e266` | `18bb870230eb89dbdca73dc0c1a6e8742a501fc44b110a12488218af8ba8e266` | 30157 | 30157 | MATCH |

## 4. PRD (1 file)

| File | SHA-256 before | SHA-256 after | Bytes before | Bytes after | Match |
|---|---|---|---|---|---|
| `docs/prd/prd.md` | `4802aea664852a0dda7bbb076934f21b6127fd67ca7b063035d4c988a93177a2` | `4802aea664852a0dda7bbb076934f21b6127fd67ca7b063035d4c988a93177a2` | 164179 | 164179 | MATCH |

## 5. Other files the second model received (15 files)

These files are not part of the gate. They show that the test run did not change the tests, the data or the traceability file.

| File | SHA-256 before | SHA-256 after | Bytes before | Bytes after | Match |
|---|---|---|---|---|---|
| `docs/prd/traceability.md` | `cbf966edd93ea1dcf36c39a88d5831ee6b31d1715ea036bef79110a7c87fd0a6` | `cbf966edd93ea1dcf36c39a88d5831ee6b31d1715ea036bef79110a7c87fd0a6` | 34211 | 34211 | MATCH |
| `data/synthetic/devices.csv` | `32440b017dcd8f480738fcba31ee6b56bbf92055ebaa5c2f058a4f2d1ecf9477` | `32440b017dcd8f480738fcba31ee6b56bbf92055ebaa5c2f058a4f2d1ecf9477` | 41883 | 41883 | MATCH |
| `data/synthetic/alarms.csv` | `b8a9d8e6bfbdc7b86cea60573916190b60044059b3a56473f66c477436dab42b` | `b8a9d8e6bfbdc7b86cea60573916190b60044059b3a56473f66c477436dab42b` | 41006 | 41006 | MATCH |
| `tests/app/helpers.py` | `94f000565c3eb9306ef8b4fc6d99ad3973951f56110bc6597ec9de637a6daafd` | `94f000565c3eb9306ef8b4fc6d99ad3973951f56110bc6597ec9de637a6daafd` | 502 | 502 | MATCH |
| `tests/test_api_contract.py` | `e754c0fdf7dfad926984accd33b80409bf9e77a44c716904eaecf870405c2907` | `e754c0fdf7dfad926984accd33b80409bf9e77a44c716904eaecf870405c2907` | 573 | 573 | MATCH |
| `tests/access/test_negative_access.py` | `1cbf968dd8514c0149d5f66452a16575fbb60a6e64daa78591713d3d0962a947` | `1cbf968dd8514c0149d5f66452a16575fbb60a6e64daa78591713d3d0962a947` | 6445 | 6445 | MATCH |
| `tests/app/test_records_route.py` | `d59c2e4263592a6f19303ca944eacd15b22f7832956c2aa043b821d92d4c0381` | `d59c2e4263592a6f19303ca944eacd15b22f7832956c2aa043b821d92d4c0381` | 2921 | 2921 | MATCH |
| `tests/app/test_storm_route.py` | `1290fe38720a3265fba9af36f91704974cced882d00c23b97a4537056cd4c71f` | `1290fe38720a3265fba9af36f91704974cced882d00c23b97a4537056cd4c71f` | 5358 | 5358 | MATCH |
| `tests/app/test_recommend_route.py` | `2dfa80fa72d10310ebc1d0e17a58eb5dce6033ac52a6ae78b1f07a3e1adff308` | `2dfa80fa72d10310ebc1d0e17a58eb5dce6033ac52a6ae78b1f07a3e1adff308` | 9830 | 9830 | MATCH |
| `tests/app/test_approvals_route.py` | `a45fa453d582b750b2b391745b78fde931f24b286c043c0a8b0254413ee1be5b` | `a45fa453d582b750b2b391745b78fde931f24b286c043c0a8b0254413ee1be5b` | 8042 | 8042 | MATCH |
| `tests/app/test_audit_row_keys.py` | `a5ba8556b156e10c60348f18dc42dde491f4afa08e6d71e15a823f33ce3a7fef` | `a5ba8556b156e10c60348f18dc42dde491f4afa08e6d71e15a823f33ce3a7fef` | 4764 | 4764 | MATCH |
| `tests/app/test_demo_flow.py` | `036d33b28bd0dd4d26d539efa9f6f80fb177c035f1ba8448c312eb06f77ec1d1` | `036d33b28bd0dd4d26d539efa9f6f80fb177c035f1ba8448c312eb06f77ec1d1` | 5276 | 5276 | MATCH |
| `tests/audit/test_audit_rebuild.py` | `669813755bad0a57aab5ec020010c20ba7388c53fdde7e5bc2c3065e6f97a373` | `669813755bad0a57aab5ec020010c20ba7388c53fdde7e5bc2c3065e6f97a373` | 14517 | 14517 | MATCH |
| `policy/tests/test_policy_python.py` | `6a4930fdb42d0f52fd4bde48204062de9fc5335823b2394c01f42c4050f221de` | `6a4930fdb42d0f52fd4bde48204062de9fc5335823b2394c01f42c4050f221de` | 24578 | 24578 | MATCH |
| `tests/security/test_client_flags_ignored.py` | `00cbbadb52799e8491a78f2758bb601a722c832e875e6391bd4500bb99bb94ac` | `00cbbadb52799e8491a78f2758bb601a722c832e875e6391bd4500bb99bb94ac` | 2838 | 2838 | MATCH |

## 6. Files this stage changed outside the gate

**Verified Fact.** The test runs append rows to `logs/audit.log`. The file had 308 lines and SHA-256 `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951` before this stage. The runs raised it to 322 lines. The file was restored from a copy taken before the first run. After the restore it has 308 lines and the same SHA-256 again. The file was already marked modified in `git status` before this stage, and that state is kept.

**Verified Fact.** This stage added four harness files under `docs/model-comparison/harness/`: `alias_model_b.py`, `probe_battery.py`, `probe_battery2.py` and `probe_phrases.py`. They change no gate file.

## 7. Re-check after the load fix of the second app

**Why this section exists.** Sections 1 to 6 were written on 2026-10-13 at 22:21. The load fix of the second app came after that. It changed files under `apps/api_model_b/` and the alias plugin. The hash tables above do not need new numbers, because none of the 36 files is among the files the fix changed. This section records that the same checks were run again on 2026-10-14 at 00:30.

| Check | Result after the load fix |
|---|---|
| Hash of the 36 rows in `yaml-hashes-before.md` (same script as section 1) | `rows hashed: 36`, `mismatches: []` |
| `git status --short -- semantic-layer docs/prd data tests policy apps/api docs/ADR` | Printed nothing |
| `python semantic-layer\build.py --check` | `generated/ matches the YAML. 7 files validated. Version 1.2.1.` |
| `pytest semantic-layer/tests -q -p no:cacheprovider` | `41 passed in 2.50s` |
| `logs/audit.log` | 308 lines, SHA-256 `A51E98494A5286781BAABCD051D92F5B4F47D6135C5B44982529CEEC269C1951`. Same as in section 6. |

**Verified Fact.** The load fix changed these files, and none of them is in the 36:
- `apps/api_model_b/services/ai_gateway.py` (edited)
- `apps/api_model_b/main.py` (edited)
- `apps/api_model_b/services/audit.py` (edited)
- `apps/api_model_b/settings.py` (new)
- `apps/api_model_b/services/dedupe.py` (new; a copy of the first app's file)
- `docs/model-comparison/harness/alias_model_b.py` (edited)

**Verified Fact.** Two commits came after the commit named in section 2: `ec56a34` (2026-10-13 23:19, "After completing S08 - Second Model") and `e956891` (2026-10-14 00:14, "After completing S09-readiness-and-evidence-pack"). The commit `51aa787` named in section 2 was the latest at the time of that check. The 36 hashes match the files as they sit now, so the later commits did not change the layer or the PRD.

Detail of the fix: `docs/model-comparison/second-model-load-fix.md`.