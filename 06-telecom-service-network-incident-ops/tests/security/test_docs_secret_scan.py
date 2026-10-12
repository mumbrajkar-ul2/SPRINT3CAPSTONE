"""Security test: scan docs/ for real secret formats. Stage S05-13 Half B (BL-03).

test_secret_patterns.py skips docs/. A document can still hold a pasted key. This test
scans docs/ with narrower patterns that match real key formats only. The three wide
patterns of test_secret_patterns.py give 4 false hits on docs/ (stand-in text and a
constant named EDU_UNITS_PER_1K_TOKENS), so they are not reused here.
Decision by Mangesh (FDE), 2026-10-11, choice (a). Owner: Team-Force.

Patterns are built in pieces so this file does not match its own scan.
"""

import re
from pathlib import Path

import pytest

pytestmark = pytest.mark.security

REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
SCANNED_SUFFIXES = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".csv"}

# 1. A secret-key prefix followed by 20 or more letters and digits.
SK_KEY_RE = re.compile(r"(?<![A-Za-z0-9])" + "sk" + "-" + r"[A-Za-z0-9]{20,}")
# 2. A cloud access key id (AKIA plus 16 capitals and digits).
CLOUD_KEY_RE = re.compile(r"(?<![A-Z0-9])" + "AK" + "IA" + r"[0-9A-Z]{16}(?![A-Z0-9])")
# 3. A source-host token (ghp_ plus 36 characters).
HOST_CRED_RE = re.compile(r"(?<![A-Za-z0-9])" + "gh" + "p_" + r"[A-Za-z0-9]{36}")
# 4. A private key block header.
PRIVATE_KEY_RE = re.compile("-----BEGIN " + r"(?:[A-Z]+ )?" + "PRIVATE" + " KEY-----")
# 5. A quoted value of 8 or more characters assigned to a secret-named key.
QUOTED_ASSIGN_RE = re.compile(
    r"""(?i)\b(?:pass""" + r"""word|secret|api_?key|access_?token|auth_?token)\b\s*[:=]\s*(["'])(?P<val>[^"'\s]{8,})\1"""
)
# Values that are placeholders or environment lookups are allowed.
ALLOWED_VALUE_RE = re.compile(r"(?i)^(?:change_?me|<.*>|\$\{.*\}|%.*%|redacted|example|xxx+|\*+)$")

PATTERNS = (
    ("secret-key prefix", SK_KEY_RE),
    ("cloud key id", CLOUD_KEY_RE),
    ("source-host token", HOST_CRED_RE),
    ("private key block", PRIVATE_KEY_RE),
)


def scan_text(text):
    """Return (line number, pattern name) for every line that holds a real secret format."""
    hits = []
    for line_no, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS:
            if pattern.search(line):
                hits.append((line_no, name))
        for match in QUOTED_ASSIGN_RE.finditer(line):
            if not ALLOWED_VALUE_RE.match(match.group("val")):
                hits.append((line_no, "quoted secret assignment"))
    return hits


def iter_doc_files(root=DOCS):
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SCANNED_SUFFIXES:
            yield path


def test_docs_scan_finds_planted_values_and_ignores_placeholders():
    planted = "\n".join(
        [
            "sk" + "-" + "abcdefghijklmnopqrstuv",
            "AK" + "IA" + "ABCDEFGHIJKLMNOP",
            "gh" + "p_" + "a" * 36,
            "-----BEGIN " + "RSA PRIVATE" + " KEY-----",
            'pass' + 'word = "realvalue99"',
        ]
    )
    names = [name for _, name in scan_text(planted)]
    assert names == [
        "secret-key prefix",
        "cloud key id",
        "source-host token",
        "private key block",
        "quoted secret assignment",
    ]
    placeholders = "\n".join(
        [
            "sk" + "-" + "temp-should-fail",
            'pass' + 'word = "CHANGE_ME"',
            'api_key = "<redacted>"',
            "EDU_UNITS_PER_1K_TOKENS = 1.0",
        ]
    )
    assert scan_text(placeholders) == []


def test_docs_have_no_real_secret_formats():
    files = list(iter_doc_files())
    # A scan that read no file would also find nothing.
    assert len(files) > 50
    hits = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(REPO).as_posix()
        hits.extend(f"{rel}:{line_no}: {name}" for line_no, name in scan_text(text))
    assert hits == [], hits
