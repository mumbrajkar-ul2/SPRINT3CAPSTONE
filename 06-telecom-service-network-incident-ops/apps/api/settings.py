"""Load required settings from the process environment.

This module stays quiet at import. A missing secret raises only when
a caller asks for that name. The error names the variable and prints
no value.
"""

import math
import os

PLACEHOLDER = "CHANGE_ME"


class SettingsError(Exception):
    """A required setting is absent, empty, or still the placeholder."""


def require(name: str) -> str:
    value = os.environ.get(name)
    if value is None or value.strip() == "" or value.strip() == PLACEHOLDER:
        raise SettingsError(f"Required setting {name} is absent")
    return value


def positive_number(name: str, default: float) -> float:
    """A number above zero from the environment, or `default`.

    Stage S04-11 Half B. For tuning numbers that are not secrets. An absent,
    empty, non-numeric, zero, negative, or non-finite value gives the default.
    The same rule `ai_gateway.configured_timeout_seconds` follows.
    """
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
    """A whole number of 1 or more from the environment, or `default`."""
    value = positive_number(name, float(default))
    if value != int(value):
        return default
    return int(value)
