"""Read numbers and secrets from the process environment.

Added in the S08 load fix. `docs/12-finops/metrics_from_audit.py` imports this module to read a
rate from the environment. The second app's routes do not use it.
"""

import math
import os

PLACEHOLDER = "CHANGE_ME"


class SettingsError(Exception):
    """A required setting is absent, empty, or still the placeholder."""


def require(name: str) -> str:
    value = os.environ.get(name)
    if value is None or not value.strip() or value.strip() == PLACEHOLDER:
        raise SettingsError(f"Required setting {name} is absent")
    return value


def positive_number(name: str, default: float) -> float:
    """A number above zero from the environment. Any other value gives `default`."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    if not math.isfinite(value) or value <= 0:
        return default
    return value


def positive_int(name: str, default: int) -> int:
    """A whole number of 1 or more from the environment. Any other value gives `default`."""
    value = positive_number(name, float(default))
    return int(value) if value == int(value) else default
