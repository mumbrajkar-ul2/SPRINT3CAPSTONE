"""data/contracts/openapi-fragment.yaml lists the full route set. Stage S07."""

from pathlib import Path

import yaml

from apps.api.main import app
from apps.api.services import audit

FRAGMENT = Path(__file__).resolve().parents[2] / "data" / "contracts" / "openapi-fragment.yaml"


def load():
    return yaml.safe_load(FRAGMENT.read_text(encoding="utf-8"))


def app_routes():
    found = set()
    for route in app.routes:
        path = getattr(route, "path", "")
        for method in getattr(route, "methods", None) or ():
            if method in ("GET", "POST") and not path.startswith(("/docs", "/redoc", "/openapi")):
                # The code calls the path name record_id. The PRD and this file call it id.
                found.add((path.replace("{record_id}", "{id}"), method.lower()))
    return found


def test_the_fragment_lists_every_route_of_the_app_and_no_other():
    spec = load()
    listed = {(path, method) for path, item in spec["paths"].items() for method in item}
    assert listed == app_routes()


def test_no_path_is_named_execute():
    assert not [path for path in load()["paths"] if "execute" in path.lower()]


def test_the_audit_row_schema_has_the_same_17_keys_in_the_same_order_as_the_code():
    schema = load()["components"]["schemas"]["AuditRow"]
    assert list(schema["properties"]) == list(audit.SCHEMA_KEYS)
    assert schema["required"] == list(audit.SCHEMA_KEYS)
    assert len(audit.SCHEMA_KEYS) == 17


def test_the_model_routes_name_no_execute_outcome():
    spec = load()
    assert spec["components"]["schemas"]["AiOutcome"]["enum"] == ["RECOMMEND_ONLY", "HOLD_FOR_REVIEW", "BLOCK"]


def test_the_ai_response_schema_matches_the_body_model_in_the_code():
    from apps.api.services.ai_gateway import AiResponse

    schema = load()["components"]["schemas"]["AiResponse"]
    assert set(schema["required"]) == set(AiResponse.model_fields)
    assert set(schema["properties"]) == set(AiResponse.model_fields) | {"error"}


def test_the_approval_request_allows_only_the_decision_key():
    schema = load()["components"]["schemas"]["ApprovalRequest"]
    assert list(schema["properties"]) == ["decision"]
    assert schema["properties"]["decision"]["enum"] == ["yes", "no"]


def test_every_ref_points_to_a_part_that_exists():
    spec = load()
    text = FRAGMENT.read_text(encoding="utf-8")
    import re

    for ref in set(re.findall(r"\$ref: '#/([^']+)'", text)):
        node = spec
        for part in ref.split("/"):
            node = node[part]
