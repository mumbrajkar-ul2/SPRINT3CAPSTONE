"""Pytest plugin for S08 Part 3. It points the repository tests at apps/api_model_b/.

How it works. The tests import `apps.api.main` and `apps.api.services.*`. When the environment
variable APP_UNDER_TEST is `b`, this plugin loads the second app first. It then registers each
second-app module in `sys.modules` under the first-app name. The test files stay as they are.
A test that patches `audit.LOG` patches the module object of the second app.

When APP_UNDER_TEST is not `b`, this plugin does nothing. The tests run on `apps/api/`.

The plugin adds three constants to the second app's `breaker` module (the names of the
environment variables). `tests/conftest.py` reads them in an autouse fixture. The second app
never reads those environment variables. The plugin changes no file on disk.

Run example (from 06-telecom-service-network-incident-ops/):

    $env:APP_UNDER_TEST = "b"
    $env:PYTHONPATH = "docs/model-comparison/harness"
    python -m pytest -p alias_model_b -p no:cacheprovider <tests>
"""

import importlib
import os
import sys

SERVICES = (
    "ai_gateway",
    "alarm_service",
    "approvals",
    "audit",
    "audit_query",
    "breaker",
    "domain_service",
    "policy",
)


def _install_alias():
    pkg = importlib.import_module("apps.api_model_b")
    main = importlib.import_module("apps.api_model_b.main")
    services = importlib.import_module("apps.api_model_b.services")
    sys.modules["apps.api"] = pkg
    sys.modules["apps.api.main"] = main
    sys.modules["apps.api.services"] = services
    for name in SERVICES:
        module = importlib.import_module(f"apps.api_model_b.services.{name}")
        sys.modules[f"apps.api.services.{name}"] = module
        setattr(services, name, module)
    # S08 load fix. Two more modules the first app's tests import by name.
    for name in ("dedupe",):
        module = importlib.import_module(f"apps.api_model_b.services.{name}")
        sys.modules[f"apps.api.services.{name}"] = module
        setattr(services, name, module)
    settings = importlib.import_module("apps.api_model_b.settings")
    sys.modules["apps.api.settings"] = settings
    pkg.settings = settings
    breaker = sys.modules["apps.api.services.breaker"]
    for attr, value in (
        ("THRESHOLD_ENV", "BREAKER_FAILURE_THRESHOLD"),
        ("OPEN_SECONDS_ENV", "BREAKER_OPEN_SECONDS"),
        ("MAX_IN_FLIGHT_ENV", "MODEL_MAX_IN_FLIGHT"),
    ):
        if not hasattr(breaker, attr):
            setattr(breaker, attr, value)


if os.environ.get("APP_UNDER_TEST", "a").lower() == "b":
    sys.path.insert(0, os.getcwd())
    _install_alias()
