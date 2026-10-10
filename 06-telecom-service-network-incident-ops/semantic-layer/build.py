"""Build generated/*.json from the seven YAML files in semantic-layer/.

Usage, from the repo root 06-telecom-service-network-incident-ops:

    python semantic-layer/build.py          # validate every YAML file, then write generated/
    python semantic-layer/build.py --check  # validate, and fail if generated/ differs from the YAML

The YAML files are the source of truth. This script reads them, checks each one against
schemas/semantic-layer.schema.json, and writes one JSON file per YAML file plus generated/manifest.json.
Nothing under generated/ is edited by hand. Run this script again after any YAML change.

The output has no timestamp. The same YAML always produces the same bytes.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    print("jsonschema is required. Install it into the active environment: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "schemas" / "semantic-layer.schema.json"
GENERATED = ROOT / "generated"

# The seven YAML files, in the order the README lists them.
YAML_FILES = [
    "entities.yaml",
    "relationships.yaml",
    "status-taxonomy.yaml",
    "business-rules.yaml",
    "metrics.yaml",
    "access-semantics.yaml",
    "ai-context-policy.yaml",
]


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema() -> Draft202012Validator:
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate(validator: Draft202012Validator, name: str, data: dict) -> list[str]:
    """Return a list of readable error strings. Empty list means the file is valid."""
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        # The top level is a oneOf over seven branches. Report the branch that matches the file key.
        if err.validator == "oneOf" and err.context:
            file_kind = data.get("file")
            for sub in err.context:
                # Keep sub-errors from the branch whose const matches, skip the "const" mismatch of other branches.
                if sub.validator == "const":
                    continue
                path = "/".join(str(p) for p in sub.absolute_path) or "<root>"
                errors.append(f"{name} [{file_kind}] at {path}: {sub.message}")
        else:
            path = "/".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{name} at {path}: {err.message}")
    return errors


def to_json_bytes(data: dict) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build(check_only: bool = False) -> int:
    validator = load_schema()
    all_errors: list[str] = []
    outputs: dict[str, bytes] = {}
    manifest = {"version": None, "schema": "schemas/semantic-layer.schema.json", "files": []}

    for fname in YAML_FILES:
        path = ROOT / fname
        if not path.exists():
            all_errors.append(f"{fname}: file is missing")
            continue
        data = load_yaml(path)
        all_errors.extend(validate(validator, fname, data))
        version = str(data.get("version"))
        if manifest["version"] is None:
            manifest["version"] = version
        elif manifest["version"] != version:
            all_errors.append(f"{fname}: version {version} differs from {manifest['version']}")
        out_name = Path(fname).stem + ".json"
        body = to_json_bytes(data)
        outputs[out_name] = body
        manifest["files"].append({
            "yaml": fname,
            "json": f"generated/{out_name}",
            "yaml_sha256": sha256(path.read_bytes()),
            "json_sha256": sha256(body),
        })

    if all_errors:
        print("Schema validation failed:")
        for e in all_errors:
            print("  -", e)
        return 1

    outputs["manifest.json"] = to_json_bytes(manifest)

    if check_only:
        drift = []
        for out_name, body in outputs.items():
            target = GENERATED / out_name
            if not target.exists() or target.read_bytes() != body:
                drift.append(out_name)
        if drift:
            print("generated/ differs from the YAML for:", ", ".join(drift))
            print("Run: python semantic-layer/build.py")
            return 1
        print(f"generated/ matches the YAML. {len(YAML_FILES)} files validated. Version {manifest['version']}.")
        return 0

    GENERATED.mkdir(exist_ok=True)
    for out_name, body in outputs.items():
        (GENERATED / out_name).write_bytes(body)
    print(f"Validated {len(YAML_FILES)} YAML files against {SCHEMA_PATH.name}. Version {manifest['version']}.")
    for out_name in outputs:
        print(f"  wrote generated/{out_name}")
    return 0


if __name__ == "__main__":
    sys.exit(build(check_only="--check" in sys.argv[1:]))
