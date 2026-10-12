"""Scan committed files for secret values and common secret patterns."""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "docs",
    "__pycache__",
    ".pytest_cache",
}
PLACEHOLDER = "CHANGE_ME"
# Built in pieces so this file does not contain the trigger as one literal.
SK_PREFIX = "sk" + "-"
PASSWORD_KEY = "password"
TOKEN_KEY = "token"

SK_RE = re.compile(r"(?<![A-Za-z])" + re.escape(SK_PREFIX) + r"[A-Za-z0-9]")
STANDALONE_ASSIGN_RE = re.compile(
    r"(?<![A-Za-z0-9_])(?P<key>" + PASSWORD_KEY + r"|" + TOKEN_KEY + r")\s*=\s*(?P<val>\S+)",
    re.IGNORECASE,
)
NAMED_ASSIGN_RE = re.compile(
    r"^(?P<name>[A-Z][A-Z0-9_]*)\s*=\s*(?:[\"'](?P<quoted>[^\"']+)[\"']|(?P<bare>[^#\s]+))"
)


def _iter_scanned_files():
    self = Path(__file__).resolve()
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() == self:
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".woff", ".woff2"}:
            continue
        yield path


def _value_is_secret(raw: str) -> bool:
    value = raw.strip().strip('"').strip("'")
    if value == "" or value == PLACEHOLDER:
        return False
    if value.startswith("${") or value.startswith("%"):
        return False
    return True


def find_secret_pattern_hits():
    hits = []
    for path in _iter_scanned_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(REPO).as_posix()
        for line_no, line in enumerate(text.splitlines(), 1):
            if SK_RE.search(line):
                hits.append(f"{rel}:{line_no}: {SK_PREFIX} key pattern")
            for match in STANDALONE_ASSIGN_RE.finditer(line):
                if _value_is_secret(match.group("val")):
                    hits.append(f"{rel}:{line_no}: {match.group('key')} assignment")
            named = NAMED_ASSIGN_RE.match(line.strip())
            if named:
                name = named.group("name").upper()
                if "PASSWORD" in name or "TOKEN" in name or name.endswith("KEY"):
                    raw = named.group("quoted") or named.group("bare") or ""
                    if _value_is_secret(raw):
                        hits.append(f"{rel}:{line_no}: {name} holds a non-placeholder")
    return hits


@pytest.mark.security
def test_repo_has_no_secret_patterns():
    hits = find_secret_pattern_hits()
    assert hits == [], hits
