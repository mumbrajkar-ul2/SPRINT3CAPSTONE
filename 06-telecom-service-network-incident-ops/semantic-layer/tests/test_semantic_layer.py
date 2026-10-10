"""Tests that protect semantic-layer/.

Run from the repo root 06-telecom-service-network-incident-ops:

    pytest semantic-layer/tests -q

What these tests fail on:
- a file in the fixed tree is missing, or an extra file appears
- the schema rejects any YAML file
- a required entity, persona, status word, rule, metric, outcome, or collision is missing
- glossary.md and the YAML disagree on a term or an id
- a file under generated/ differs from its YAML
- any id is referenced but never defined, or defined twice
- an item has no source, a source path that does not exist, or proposed true with no owner
- a metric carries a target value
- a secret value from .env.example or legacy/reconcile_legacy.py appears anywhere in the tree
- a status word in a CSV column is missing from status-taxonomy.yaml
- an entity's fields differ from the CSV header
"""
from __future__ import annotations

import copy
import csv
import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

SL = Path(__file__).resolve().parents[1]          # semantic-layer/
REPO = SL.parent                                  # 06-telecom-service-network-incident-ops/
SCHEMA = SL / "schemas" / "semantic-layer.schema.json"
GENERATED = SL / "generated"

YAML_FILES = [
    "entities.yaml", "relationships.yaml", "status-taxonomy.yaml", "business-rules.yaml",
    "metrics.yaml", "access-semantics.yaml", "ai-context-policy.yaml",
]
EXPECTED_TREE = {
    "README.md", "glossary.md", "build.py",
    *YAML_FILES,
    "schemas/semantic-layer.schema.json",
    "tests/test_semantic_layer.py",
}
VERSION = "1.0.0"

ID_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$")
# Every id in the tree starts with one of these words. A whole-string value with one of these
# prefixes is a reference and must be defined somewhere.
ID_PREFIXES = (
    "entity.", "field.", "concept.", "relationship.", "valueset.", "status.", "collision.", "rule.", "metric.",
    "persona.", "role.", "policy.", "action.", "resource.", "purpose.", "scope.", "risk.", "outcome.",
    "provenance.", "ai_use.", "failmode.",
)
# Items with these prefixes must each have a glossary row.
GLOSSARY_PREFIXES = (
    "entity.", "concept.", "persona.", "status.word.", "outcome.", "metric.", "rule.", "action.", "resource.",
    "purpose.", "scope.", "risk.", "role.", "failmode.", "collision.",
)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def load(name: str) -> dict:
    with (SL / name).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def docs() -> dict[str, dict]:
    return {name: load(name) for name in YAML_FILES}


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def walk(node, path=()):
    """Yield (path, value) for every scalar and every dict in a YAML tree."""
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from walk(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, path + (i,))
    else:
        yield path, node


def defined_ids(docs) -> dict[str, list]:
    out: dict[str, list] = {}
    for name, doc in docs.items():
        for path, node in walk(doc):
            if isinstance(node, dict) and isinstance(node.get("id"), str):
                out.setdefault(node["id"], []).append((name, path))
    return out


def items_with_id(docs):
    for name, doc in docs.items():
        for path, node in walk(doc):
            if isinstance(node, dict) and "id" in node:
                yield name, path, node


def glossary_rows() -> list[tuple[str, str, str]]:
    """Rows of every markdown table in glossary.md whose second cell is an id."""
    rows = []
    for line in (SL / "glossary.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        term, ident = cells[0].strip("`"), cells[1].strip("`")
        if ID_RE.match(ident):
            rows.append((term, ident, cells[2]))
    return rows


def names_for_glossary(docs) -> dict[str, str]:
    """id -> the text the glossary Term column must show."""
    out = {}
    for _, _, node in items_with_id(docs):
        ident = node["id"]
        if not ident.startswith(GLOSSARY_PREFIXES):
            continue
        if ident.startswith("status.word."):
            out[ident] = node["word"]
        else:
            out[ident] = node["name"]
    return out


# ---------------------------------------------------------------------------
# tree, version, schema
# ---------------------------------------------------------------------------

def test_tree_is_exactly_the_capture_layout_plus_generated_and_build():
    found = set()
    for p in SL.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(SL).as_posix()
        if rel.startswith("generated/") or "__pycache__" in rel or ".pytest_cache" in rel:
            continue
        found.add(rel)
    assert found == EXPECTED_TREE, f"missing={EXPECTED_TREE - found} extra={found - EXPECTED_TREE}"


def test_every_yaml_carries_version_and_readme_repeats_it(docs):
    for name, doc in docs.items():
        assert doc.get("version") == VERSION, f"{name} version is {doc.get('version')!r}"
    readme = (SL / "README.md").read_text(encoding="utf-8")
    assert f"`{VERSION}`" in readme or f"Version {VERSION}" in readme or f"version {VERSION}" in readme


def test_schema_validates_every_yaml_file(docs, validator):
    for name, doc in docs.items():
        errors = list(validator.iter_errors(doc))
        assert not errors, f"{name}: {errors[0].message} at {list(errors[0].absolute_path)}"


def test_schema_rejects_proposed_item_without_owner(docs, validator):
    doc = copy.deepcopy(docs["access-semantics.yaml"])
    del doc["purposes"][0]["owner"]
    assert list(validator.iter_errors(doc)), "schema accepted proposed true with no owner"


def test_schema_rejects_six_entities(docs, validator):
    doc = copy.deepcopy(docs["entities.yaml"])
    doc["entities"].pop()
    assert list(validator.iter_errors(doc)), "schema accepted an entities file with six entities"


def test_schema_rejects_missing_source(docs, validator):
    doc = copy.deepcopy(docs["business-rules.yaml"])
    del doc["rules"][0]["source"]
    assert list(validator.iter_errors(doc)), "schema accepted a rule with no source"


# ---------------------------------------------------------------------------
# required content
# ---------------------------------------------------------------------------

REQUIRED_ENTITIES = {
    "entity.device", "entity.circuit", "entity.alarm", "entity.incident",
    "entity.service_order", "entity.ai_invocation", "entity.event",
}
REQUIRED_PERSONAS = {
    "persona.noc_operator", "persona.network_engineer", "persona.field_engineer", "persona.customer_support",
    "persona.automation_service", "persona.vendor_account", "persona.ai_agent",
}
REQUIRED_STATUSES = {
    "status.incident.severity.gold", "status.incident.severity.bronze",
    "status.alarm.severity.gold", "status.alarm.severity.bronze",
    "status.device.hostname.legacy", "status.device.vendor.requires_review",
    "status.ai_invocation.guardrail_status.not_enforced", "status.code.guardrail_status.not_enforced",
    "status.code.model.local_sim_v1",
    "status.word.gold", "status.word.bronze", "status.word.silver", "status.word.critical",
    "status.word.not_enforced", "status.word.requires_review", "status.word.legacy",
}
REQUIRED_RULES = {
    "rule.missing_id_not_other_device",
    "rule.ai_output_cannot_execute",
    "rule.alarm_last_seen_not_before_first_seen",
    "rule.shared_admin_not_least_privilege",
    "rule.duplicate_dedupe_key_in_storm_is_one_alarm",
    "rule.ai_recommendation_needs_policy_approval_audit_before_state_change",
}
REQUIRED_METRICS = {
    "metric.tokens_per_invocation", "metric.cost_per_correlated_incident", "metric.quarantine_rate",
    "metric.retry_count", "metric.audit_completeness", "metric.recommendation_latency",
}
REQUIRED_OUTCOMES = {"outcome.recommend_only", "outcome.hold_for_review", "outcome.block", "outcome.execute"}
REQUIRED_COLLISIONS = {
    "collision.gold_bronze_as_severity", "collision.status_words_in_hostname_and_vendor",
    "collision.rec_0001_first_key_in_six_tables", "collision.clinician_role_in_telecom_api",
}
REQUIRED_API_ROLES = {"role.admin", "role.operator", "role.clinician", "role.engineer", "role.ai_agent"}


def test_required_entities_present(docs):
    ids = {e["id"] for e in docs["entities.yaml"]["entities"]}
    assert ids == REQUIRED_ENTITIES


def test_required_personas_present(docs):
    ids = {p["id"] for p in docs["access-semantics.yaml"]["personas"]}
    assert ids == REQUIRED_PERSONAS


def test_required_statuses_present(docs):
    ids = set(defined_ids(docs))
    missing = REQUIRED_STATUSES - ids
    assert not missing, missing


def test_required_rules_present(docs):
    ids = {r["id"] for r in docs["business-rules.yaml"]["rules"]}
    missing = REQUIRED_RULES - ids
    assert not missing, missing
    assert len(ids) >= 6


def test_required_metrics_present_with_source_fields(docs):
    metrics = docs["metrics.yaml"]["metrics"]
    ids = {m["id"] for m in metrics}
    assert REQUIRED_METRICS <= ids, REQUIRED_METRICS - ids
    for m in metrics:
        assert m["source_fields"], f"{m['id']} names no source field"


def test_four_outcomes_present_and_model_never_executes(docs):
    pol = docs["ai-context-policy.yaml"]
    ids = {o["id"] for o in pol["outcomes"]["values"]}
    assert ids == REQUIRED_OUTCOMES
    names = {o["name"] for o in pol["outcomes"]["values"]}
    assert names == {"RECOMMEND_ONLY", "HOLD_FOR_REVIEW", "BLOCK", "EXECUTE"}
    for use in pol["ai_uses"]:
        if use["pick"] == "genai":
            assert use["agency"] == "recommend", use["id"]
            assert use["outcome"] in {"outcome.recommend_only", "outcome.hold_for_review"}, use["id"]
            assert use["approver"] is not None, f"{use['id']} names no human approval point"
        assert not (use["pick"] == "genai" and use["outcome"] == "outcome.execute")
    execute_uses = [u for u in pol["ai_uses"] if u["outcome"] == "outcome.execute"]
    assert len(execute_uses) == 1 and execute_uses[0]["pick"] == "workflow_automation"


def test_eleven_ai_uses_copied_from_qualification(docs):
    ids = {u["id"] for u in docs["ai-context-policy.yaml"]["ai_uses"]}
    assert ids == {
        "ai_use.order_qualification", "ai_use.provisioning_retry_and_rollback", "ai_use.alarm_dedupe",
        "ai_use.alarm_to_incident_correlation", "ai_use.topology_lookup", "ai_use.incident_summary",
        "ai_use.next_action_recommendation", "ai_use.configuration_suggestion", "ai_use.capacity_forecast",
        "ai_use.remediation_execution", "ai_use.remediation_validation",
    }


def test_collisions_block_has_the_four_named_entries(docs):
    ids = {c["id"] for c in docs["status-taxonomy.yaml"]["collisions"]}
    assert ids == REQUIRED_COLLISIONS


def test_api_roles_today_and_clinician_removed(docs):
    acc = docs["access-semantics.yaml"]
    assert {r["id"] for r in acc["api_roles_today"]} == REQUIRED_API_ROLES
    removed = {r["role"] for r in acc["removed_roles"]}
    assert "role.clinician" in removed
    # No persona maps to clinician.
    for p in acc["personas"]:
        assert p.get("api_role_today") != "role.clinician"


def test_five_access_value_lists_have_ids(docs):
    acc = docs["access-semantics.yaml"]
    for key, prefix in [("actions", "action."), ("resources", "resource."), ("purposes", "purpose."),
                        ("scopes", "scope."), ("risks", "risk.")]:
        assert acc[key], key
        for item in acc[key]:
            assert item["id"].startswith(prefix), item["id"]


def test_every_persona_grant_uses_defined_value_list_ids(docs):
    acc = docs["access-semantics.yaml"]
    lists = {k: {i["id"] for i in acc[k]} for k in ("actions", "resources", "purposes", "scopes", "risks")}
    for p in acc["personas"]:
        for g in p["grants"]:
            assert g["action"] in lists["actions"], (p["id"], g["action"])
            assert set(g["resources"]) <= lists["resources"], (p["id"], g["resources"])
            assert g["purpose"] in lists["purposes"], (p["id"], g["purpose"])
            assert g["scope"] in lists["scopes"], (p["id"], g["scope"])
            assert g["risk"] in lists["risks"], (p["id"], g["risk"])
        for d in p["denied"]:
            assert d in lists["actions"], (p["id"], d)
        assert not (set(g["action"] for g in p["grants"]) & set(p["denied"])), p["id"]


def test_forbidden_prompt_fields_locked(docs):
    pf = docs["ai-context-policy.yaml"]["prompt_fields"]
    forbidden = {f["field"] for f in pf["forbidden"]}
    assert {"field.device.mgmt_ip", "field.device.credential_profile"} <= forbidden
    assert not (forbidden & set(pf["allowed"])), "a field is both allowed and forbidden"
    ents = docs["entities.yaml"]["entities"]
    for e in ents:
        for f in e["fields"]:
            if f.get("never_in_prompt"):
                assert f["id"] in forbidden, f["id"]


def test_api_reads_today_is_true_for_devices_only(docs):
    for e in docs["entities.yaml"]["entities"]:
        expected = e["id"] == "entity.device"
        assert e["api_reads_today"] is expected, e["id"]
        for f in e["fields"]:
            assert f["api_reads_today"] is expected, f["id"]


def test_model_today_matches_code(docs):
    mt = docs["ai-context-policy.yaml"]["model_today"]
    assert mt["model"] == "local-sim-v1"
    assert mt["guardrail_status"] == "not_enforced"
    code = (REPO / "apps" / "api" / "services" / "ai_gateway.py").read_text(encoding="utf-8")
    assert 'MODEL_VERSION = "local-sim-v1"' in code
    assert '"guardrail_status": "not_enforced"' in code


# ---------------------------------------------------------------------------
# ids, sources, proposals
# ---------------------------------------------------------------------------

def test_every_id_is_dot_form_and_unique(docs):
    seen = defined_ids(docs)
    for ident, places in seen.items():
        assert ID_RE.match(ident), ident
        assert ident.startswith(ID_PREFIXES), f"{ident} uses an unknown prefix"
        assert len(places) == 1, f"{ident} is defined {len(places)} times: {places}"


def test_every_referenced_id_is_defined(docs):
    defined = set(defined_ids(docs))
    undefined = set()
    for name, doc in docs.items():
        for path, value in walk(doc):
            if isinstance(value, str) and value.startswith(ID_PREFIXES) and ID_RE.match(value):
                if path and path[-1] == "id":
                    continue
                if value not in defined:
                    undefined.add((name, "/".join(str(p) for p in path), value))
    assert not undefined, sorted(undefined)


def test_every_item_has_a_source_list_of_existing_paths(docs):
    bad = []
    for name, path, node in items_with_id(docs):
        src = node.get("source")
        if not isinstance(src, list) or not src:
            bad.append((name, node["id"], "no source"))
            continue
        for s in src:
            if not (REPO / s).exists():
                bad.append((name, node["id"], s))
    assert not bad, bad


def test_every_proposed_item_names_an_owner(docs):
    bad = []
    for name, doc in docs.items():
        for path, node in walk(doc):
            if isinstance(node, dict) and node.get("proposed") is True and not node.get("owner"):
                bad.append((name, path))
    assert not bad, bad


def test_no_metric_has_a_target_value(docs):
    for m in docs["metrics.yaml"]["metrics"]:
        t = m["target"]
        if t is not None:
            assert isinstance(t, dict) and t.get("proposed") is True and t.get("owner"), m["id"]


def test_fail_to_person_sets_no_timeout_number_without_owner(docs):
    ftp = docs["ai-context-policy.yaml"]["fail_to_person"]
    assert ftp["audit_row_required"] is True
    assert ftp["hand_to"].startswith("persona.")
    trig = {t["id"] for t in ftp["triggers"]}
    assert {"failmode.timeout", "failmode.schema_failure"} <= trig


# ---------------------------------------------------------------------------
# glossary
# ---------------------------------------------------------------------------

def test_glossary_and_yaml_agree_on_every_term(docs):
    rows = glossary_rows()
    assert rows, "glossary.md has no table rows with an id"
    expected = names_for_glossary(docs)
    defined = set(defined_ids(docs))

    glossary_ids = [ident for _, ident, _ in rows]
    dupes = {i for i in glossary_ids if glossary_ids.count(i) > 1}
    assert not dupes, f"glossary lists an id twice: {dupes}"

    missing = set(expected) - set(glossary_ids)
    assert not missing, f"glossary has no row for: {sorted(missing)}"

    unknown = set(glossary_ids) - defined
    assert not unknown, f"glossary names an id the YAML does not define: {sorted(unknown)}"

    mismatched = [(term, ident, expected[ident]) for term, ident, _ in rows
                  if ident in expected and term != expected[ident]]
    assert not mismatched, f"glossary term differs from YAML name or word: {mismatched}"

    empty = [ident for _, ident, meaning in rows if not meaning.strip()]
    assert not empty, f"glossary rows with no meaning: {empty}"


# ---------------------------------------------------------------------------
# generated/
# ---------------------------------------------------------------------------

def test_generated_json_matches_each_yaml(docs):
    assert GENERATED.exists(), "generated/ is missing. Run: python semantic-layer/build.py"
    for name, doc in docs.items():
        target = GENERATED / (Path(name).stem + ".json")
        assert target.exists(), f"{target.name} is missing. Run: python semantic-layer/build.py"
        generated = json.loads(target.read_text(encoding="utf-8"))
        assert generated == doc, f"{target.name} differs from {name}. Run: python semantic-layer/build.py"


def test_generated_manifest_hashes_match_yaml_bytes(docs):
    import hashlib
    manifest = json.loads((GENERATED / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == VERSION
    listed = {f["yaml"]: f for f in manifest["files"]}
    assert set(listed) == set(YAML_FILES)
    for name, entry in listed.items():
        assert hashlib.sha256((SL / name).read_bytes()).hexdigest() == entry["yaml_sha256"], \
            f"{name} changed after the last build. Run: python semantic-layer/build.py"
        assert hashlib.sha256((GENERATED / (Path(name).stem + ".json")).read_bytes()).hexdigest() == entry["json_sha256"], \
            f"generated/{Path(name).stem}.json was edited by hand. Run: python semantic-layer/build.py"


# ---------------------------------------------------------------------------
# data harvest checks against the CSV files (read-only)
# ---------------------------------------------------------------------------

CSV_FOR_ENTITY = {
    "entity.device": "devices.csv", "entity.circuit": "circuits.csv", "entity.alarm": "alarms.csv",
    "entity.incident": "incidents.csv", "entity.service_order": "service_orders.csv",
    "entity.ai_invocation": "ai_invocations.csv",
}


def read_csv(name: str) -> list[dict]:
    with (REPO / "data" / "synthetic" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_entity_fields_match_csv_headers(docs):
    for e in docs["entities.yaml"]["entities"]:
        names = [f["name"] for f in e["fields"]]
        if e["id"] in CSV_FOR_ENTITY:
            with (REPO / "data" / "synthetic" / CSV_FOR_ENTITY[e["id"]]).open(newline="", encoding="utf-8") as f:
                header = next(csv.reader(f))
            assert names == header, e["id"]
        else:
            with (REPO / "data" / "synthetic" / "events.jsonl").open(encoding="utf-8") as f:
                keys = list(json.loads(f.readline()).keys())
            assert names == keys, e["id"]


def test_every_word_in_every_word_column_is_in_the_taxonomy(docs):
    tax = docs["status-taxonomy.yaml"]
    fields_by_id = {sf["id"]: sf for sf in tax["status_fields"]}
    ent_fields = {}
    for e in docs["entities.yaml"]["entities"]:
        for f in e["fields"]:
            if f.get("status_field"):
                ent_fields[(e["id"], f["name"])] = f["status_field"]
    missing = []
    for eid, fname in CSV_FOR_ENTITY.items():
        rows = read_csv(fname)
        for (e2, col), sfid in ent_fields.items():
            if e2 != eid:
                continue
            assert sfid in fields_by_id, sfid
            observed = {v["value"] for v in fields_by_id[sfid]["observed_values"]}
            off = {v["value"] for v in fields_by_id[sfid].get("off_vocabulary_values", [])}
            for r in rows:
                v = r[col]
                if v == "" or v in observed or v in off:
                    continue
                missing.append((sfid, v))
    assert not missing, sorted(set(missing))


def test_observed_counts_match_the_csv(docs):
    tax = docs["status-taxonomy.yaml"]
    by_entity = {}
    for sf in tax["status_fields"]:
        by_entity.setdefault(sf["entity"], []).append(sf)
    for eid, fname in CSV_FOR_ENTITY.items():
        rows = read_csv(fname)
        for sf in by_entity.get(eid, []):
            col = sf["field"].split(".")[-1]
            for v in sf["observed_values"]:
                actual = sum(1 for r in rows if r[col] == v["value"])
                assert actual == v["observed_count"], (sf["id"], v["value"], actual, v["observed_count"])
            assert sum(1 for r in rows if r[col] == "") == sf["blank_count"], sf["id"]


def test_every_status_word_appears_where_it_says(docs):
    tax = docs["status-taxonomy.yaml"]
    fields_by_id = {sf["id"]: sf for sf in tax["status_fields"]}
    for w in tax["words"]:
        for sfid in w["appears_in"]:
            assert sfid in fields_by_id, (w["id"], sfid)
            assert w["word"] in {v["value"] for v in fields_by_id[sfid]["observed_values"]}, (w["id"], sfid)
    for sf in tax["status_fields"]:
        for v in sf["observed_values"]:
            if "word" in v:
                assert v["word"] == "status.word." + v["value"].replace("-", "_"), v


# ---------------------------------------------------------------------------
# secrets
# ---------------------------------------------------------------------------

def secret_values() -> set[str]:
    """Secret values from the repo, read at test time so none is copied into this file."""
    values = set()
    env = REPO / ".env.example"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, _, val = line.partition("=")
                val = val.strip().strip('"').strip("'")
                if len(val) >= 6 and key.strip().upper() != "LOG_LEVEL":
                    values.add(val)
                    # A URL may embed a password after a colon and before an at sign.
                    m = re.search(r":([^:@/]+)@", val)
                    if m and len(m.group(1)) >= 6:
                        values.add(m.group(1))
    legacy = REPO / "legacy" / "reconcile_legacy.py"
    if legacy.exists():
        for m in re.finditer(r"SHARED_DB_PASSWORD\s*=\s*[\"'](.+?)[\"']", legacy.read_text(encoding="utf-8")):
            values.add(m.group(1))
    return values


def test_no_secret_value_anywhere_in_the_tree():
    secrets = secret_values()
    assert secrets, "no secret values found to check against; .env.example or legacy script changed shape"
    hits = []
    for p in SL.rglob("*"):
        if p.is_dir() or "__pycache__" in p.parts or ".pytest_cache" in p.parts:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for s in secrets:
            if s in text:
                hits.append((p.relative_to(SL).as_posix(), s[:2] + "..."))
    assert not hits, hits
