"""Fail when a JUnit XML file shows a skipped test, or shows no test at all.

Used by the security stage of scripts/evidence.sh and scripts/evidence.ps1.
Stage S05-13 Half B, backlog row SB-10. PROPOSED. Owner: Team-Force.

pytest exits 0 when a test is skipped. The playbook says a skipped security test is a
failure, so this script turns a skip into exit code 1. It also fails on an empty run,
because a run that selected no test proves nothing.

The file is read as text with regular expressions. That avoids an XML parser, which bandit
flags, and the file is the one pytest just wrote.

usage: python scripts/check_junit_no_skips.py evidence/junit-security.xml
"""

import re
import sys

SUITE_RE = re.compile(r"<testsuite\b[^>]*>")
SKIPPED_CASE_RE = re.compile(
    r'<testcase\b[^>]*?classname="(?P<cls>[^"]*)"[^>]*?name="(?P<name>[^"]*)"[^>]*?>\s*<skipped\b'
)


def _count(tag, key):
    match = re.search(rf'\b{key}="(\d+)"', tag)
    return int(match.group(1)) if match else 0


def check_text(text):
    """Return a list of problems. An empty list means the text is clean."""
    suites = SUITE_RE.findall(text)
    tests = sum(_count(tag, "tests") for tag in suites)
    skipped = sum(_count(tag, "skipped") for tag in suites)
    problems = []
    if not suites or tests == 0:
        problems.append("no test ran")
    if skipped:
        names = [f"{m.group('cls')}::{m.group('name')}" for m in SKIPPED_CASE_RE.finditer(text)]
        problems.append(f"{skipped} security test(s) skipped: " + ", ".join(names))
    return problems


def check(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return check_text(handle.read())
    except OSError as error:
        return [f"cannot read {path}: {error}"]


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    problems = check(argv[1])
    for problem in problems:
        print("security gate FAILED: " + problem)
    if not problems:
        print(f"security gate ok: {argv[1]} has no skipped test")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
