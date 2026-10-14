# YAML and PRD hashes before the second-model run

| Field | Value |
|---|---|
| Stage | S08 Part 1. This file records the state of the inputs before the second model builds anything. |
| Date / version | 2026-10-13. Semantic layer `1.2.1`. PRD `v1.9`. |
| Author | Cursor agent (Claude Sonnet 5.5) for Mangesh (FDE) |
| Status | Version check PASSED. The three version sources agree. The 20 files of `semantic-layer/` and `docs/prd/prd.md` are hashed below. Part 3 writes `yaml-hashes-after.md` and compares. |
| Evidence sources | `semantic-layer/README.md`; `docs/02-baseline/semantic-layer-revision.md` (header); `docs/prd/prd.md` (header); `semantic-layer/generated/manifest.json`; `docs/ADR/0006-s07-gaps-g5-g7.md`; output of the commands in section 1 and section 2, run on 2026-10-13 |
| Assumptions | (1) Each hash covers the file as it sits on this Windows copy, with CRLF line endings where the file has them. A copy with other line endings gives other hashes. Part 3 must hash the same copy. (2) `__pycache__` folders are left out. They are build leftovers, git ignores them (`.gitignore` line 10), and a test run rewrites them. |
| Unresolved issues | None for the hashes. |
| Residual risks | The last commit, `09cb048` (2026-10-13), holds the layer at `1.2.0`. The `1.2.1` files and ADR 0006 are not committed. The hashes in this file are the only record of the exact `1.2.1` bytes. Commit before the second-model run so that a commit id also names them. |

Claim labels: **Verified Fact** (a command or a file read, named here), **Inference**, **Assumption**, **Unknown**.

Paths are relative to `06-telecom-service-network-incident-ops/`.

## 1. Version check

**Verified Fact.** All sources name the same version, `1.2.1`.

| Source | What it says | Match with `1.2.1` |
|---|---|---|
| `semantic-layer/README.md`, section "Version" | "This is version `1.2.1`." The file has no line that starts with `version:`. The header table and the change log say `1.2.1` too. | Yes |
| `docs/02-baseline/semantic-layer-revision.md`, header row "Date / version" | "**The current version is `1.2.1`.**" | Yes |
| `docs/prd/prd.md`, header rows "Date / version" and "Evidence sources" | "Semantic layer 1.2.1." and "Semantic layer version `1.2.1`". | Yes |
| `semantic-layer/*.yaml` (seven files), first `version:` line | `version: "1.2.1"` in six files and `version: 1.2.1` in the seventh | Yes |
| `semantic-layer/generated/manifest.json` | `"version": "1.2.1"` | Yes |

## 2. Proof that no change came after the last ADR

The last ADR is `docs/ADR/0006-s07-gaps-g5-g7.md`. It raised the layer from `1.2.0` to `1.2.1`.

**Verified Fact.** Command: `git diff --stat -- semantic-layer` against the last commit `09cb048`. Result: 19 files changed, 52 insertions, 51 deletions. A second command listed every changed line that does not carry `1.2.0` or `1.2.1`. It printed three removed lines and three added lines. They are the formula sentence of `metric.audit_completeness` (`policy_result` became `outcome`) and the sentence that explains it. ADR 0006 records both changes. No other line differs from `1.2.0`.

**Verified Fact.** Command: `python semantic-layer\build.py --check`. Result: `generated/ matches the YAML. 7 files validated. Version 1.2.1.` Exit code 0.

**Verified Fact.** Command: `pytest semantic-layer/tests -q -p no:cacheprovider`. Result: `41 passed in 2.62s`.

## 3. Hashes of the semantic layer (20 files)

SHA-256 of the file bytes. Size in bytes. Column "Match after" stays empty until Part 3.

| File | SHA-256 | Bytes | Match after |
|---|---|---|---|
| `semantic-layer/access-semantics.yaml` | `a74bb3b2fe18f41ece0eba250d362d98924e65ee2cf72f1bd5390fdda6b516df` | 25600 | pending |
| `semantic-layer/ai-context-policy.yaml` | `ed4947038cbec87f80eef531c9b94fa29993790541758c68eb858aab17fa84e2` | 40704 | pending |
| `semantic-layer/build.py` | `d6fbaf242aab085241d798b81e9524913cfeb6938a85b39ba018f4cb771e1c88` | 5217 | pending |
| `semantic-layer/business-rules.yaml` | `faec3e64c62486eaf190d69cabeedc245b640669371957f39ee199947933a450` | 25134 | pending |
| `semantic-layer/entities.yaml` | `fd1b6464366f187e989bb60bab580e75f913047287d80590a9cccb24e4013bc1` | 46819 | pending |
| `semantic-layer/generated/access-semantics.json` | `e013b22342209483940ab1622b0afd44014a8a93244134edcf5829d0fba5edcf` | 29254 | pending |
| `semantic-layer/generated/ai-context-policy.json` | `d098f6b570c4ae0c5b164cd0a975ce2cfc1c4d2e477c698d83031cb3c98c845c` | 44129 | pending |
| `semantic-layer/generated/business-rules.json` | `529d5a574211553faa13d4f0ba73fb5745d699f4b0464373408ba41265658a69` | 27142 | pending |
| `semantic-layer/generated/entities.json` | `f90a77f6a86be2b6f5d1eca9f88f5d7d6f12f4f974e082a0ac86798208dee82f` | 56749 | pending |
| `semantic-layer/generated/manifest.json` | `f863b3ee36499434d48e78f77c7a4629ea2aca6a662739b879cc2244a2ec9af8` | 1994 | pending |
| `semantic-layer/generated/metrics.json` | `875a1cb01e652e29c15cc53e217acc52d59533226d25780eebf66a47939f5a9b` | 15847 | pending |
| `semantic-layer/generated/relationships.json` | `f72fc4d04c62bb9fa1f92124a924d01e542207c0d48da327d5a06a17fd6cc81e` | 10737 | pending |
| `semantic-layer/generated/status-taxonomy.json` | `5d4c6ccfa2aeeb643c883aff20e8e9c7a0efa45791951de138a7e08d858fc3af` | 181440 | pending |
| `semantic-layer/glossary.md` | `f2a06448fb5934a60f47b009c6c7e4d43457e47ddb5f95b3e40cbb0f1a7a9f2d` | 51145 | pending |
| `semantic-layer/metrics.yaml` | `bff90a9d6719491b7865c6ad84af30aff80498072bbec7c8b8569700a99b319d` | 14874 | pending |
| `semantic-layer/README.md` | `e6bb1f9ad209b515c87861a49d560730100283e8fc6cbef7e80761d49888dd81` | 26913 | pending |
| `semantic-layer/relationships.yaml` | `95206dba92703100ab70be5c77eaf8144d8e01ed81d8a90151435fda56a7f201` | 9130 | pending |
| `semantic-layer/schemas/semantic-layer.schema.json` | `a88c6d51ef7e4a4ad307016e650f2f0548093ed1892820ee8ee035d247b55fc4` | 25201 | pending |
| `semantic-layer/status-taxonomy.yaml` | `1794e726d41c0b3b1b933bfd2ede5c4b11a86dac5f3ce9e22e5e8e8c95aa4d6c` | 132152 | pending |
| `semantic-layer/tests/test_semantic_layer.py` | `18bb870230eb89dbdca73dc0c1a6e8742a501fc44b110a12488218af8ba8e266` | 30157 | pending |

**Verified Fact.** The hash of `semantic-layer/entities.yaml` equals the `yaml_sha256` value for `entities.yaml` in `generated/manifest.json`.

## 4. Hash of the PRD

| File | SHA-256 | Bytes | Match after |
|---|---|---|---|
| `docs/prd/prd.md` | `4802aea664852a0dda7bbb076934f21b6127fd67ca7b063035d4c988a93177a2` | 164179 | pending |

## 5. Other files the second model receives

These files are not part of the Part 3 gate. The table records them so Part 3 can show that the run did not change them.

| File | SHA-256 | Bytes | Match after |
|---|---|---|---|
| `docs/prd/traceability.md` | `cbf966edd93ea1dcf36c39a88d5831ee6b31d1715ea036bef79110a7c87fd0a6` | 34211 | pending |
| `data/synthetic/devices.csv` | `32440b017dcd8f480738fcba31ee6b56bbf92055ebaa5c2f058a4f2d1ecf9477` | 41883 | pending |
| `data/synthetic/alarms.csv` | `b8a9d8e6bfbdc7b86cea60573916190b60044059b3a56473f66c477436dab42b` | 41006 | pending |
| `tests/app/helpers.py` | `94f000565c3eb9306ef8b4fc6d99ad3973951f56110bc6597ec9de637a6daafd` | 502 | pending |
| `tests/test_api_contract.py` | `e754c0fdf7dfad926984accd33b80409bf9e77a44c716904eaecf870405c2907` | 573 | pending |
| `tests/access/test_negative_access.py` | `1cbf968dd8514c0149d5f66452a16575fbb60a6e64daa78591713d3d0962a947` | 6445 | pending |
| `tests/app/test_records_route.py` | `d59c2e4263592a6f19303ca944eacd15b22f7832956c2aa043b821d92d4c0381` | 2921 | pending |
| `tests/app/test_storm_route.py` | `1290fe38720a3265fba9af36f91704974cced882d00c23b97a4537056cd4c71f` | 5358 | pending |
| `tests/app/test_recommend_route.py` | `2dfa80fa72d10310ebc1d0e17a58eb5dce6033ac52a6ae78b1f07a3e1adff308` | 9830 | pending |
| `tests/app/test_approvals_route.py` | `a45fa453d582b750b2b391745b78fde931f24b286c043c0a8b0254413ee1be5b` | 8042 | pending |
| `tests/app/test_audit_row_keys.py` | `a5ba8556b156e10c60348f18dc42dde491f4afa08e6d71e15a823f33ce3a7fef` | 4764 | pending |
| `tests/app/test_demo_flow.py` | `036d33b28bd0dd4d26d539efa9f6f80fb177c035f1ba8448c312eb06f77ec1d1` | 5276 | pending |
| `tests/audit/test_audit_rebuild.py` | `669813755bad0a57aab5ec020010c20ba7388c53fdde7e5bc2c3065e6f97a373` | 14517 | pending |
| `policy/tests/test_policy_python.py` | `6a4930fdb42d0f52fd4bde48204062de9fc5335823b2394c01f42c4050f221de` | 24578 | pending |
| `tests/security/test_client_flags_ignored.py` | `00cbbadb52799e8491a78f2758bb601a722c832e875e6391bd4500bb99bb94ac` | 2838 | pending |

## 6. How Part 3 repeats this

Run the same hash script over the same 21 gate files (20 under `semantic-layer/` plus `docs/prd/prd.md`). Write the result to `yaml-hashes-after.md` with the Match column filled. One differing hash makes the stage BLOCKED.
