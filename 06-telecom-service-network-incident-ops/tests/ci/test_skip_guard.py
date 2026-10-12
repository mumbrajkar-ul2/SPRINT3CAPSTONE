"""Tests for scripts/check_junit_no_skips.py. Stage S05-13 Half B (SB-10).

The guard turns a skipped security test into a failed stage. These tests feed it small
XML texts and check both scripts call it. They run no scan and write nothing.
"""

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("check_junit_no_skips", REPO / "scripts" / "check_junit_no_skips.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)

CLEAN = (
    '<?xml version="1.0"?><testsuites><testsuite name="pytest" errors="0" failures="0" '
    'skipped="0" tests="2"><testcase classname="a.b" name="t1" time="0.1" />'
    '<testcase classname="a.b" name="t2" time="0.1" /></testsuite></testsuites>'
)
SKIPPED = (
    '<?xml version="1.0"?><testsuites><testsuite name="pytest" errors="0" failures="0" '
    'skipped="1" tests="2"><testcase classname="a.b" name="t1" time="0.1" />'
    '<testcase classname="a.b" name="t_opa" time="0.1"><skipped type="pytest.skip" '
    'message="opa binary not on PATH">x</skipped></testcase></testsuite></testsuites>'
)
EMPTY = (
    '<?xml version="1.0"?><testsuites><testsuite name="pytest" errors="0" failures="0" '
    'skipped="0" tests="0" /></testsuites>'
)


def test_a_clean_run_passes():
    assert guard.check_text(CLEAN) == []


def test_a_skipped_test_fails_and_is_named():
    problems = guard.check_text(SKIPPED)
    assert len(problems) == 1
    assert "1 security test(s) skipped" in problems[0]
    assert "a.b::t_opa" in problems[0]


def test_an_empty_run_fails():
    assert guard.check_text(EMPTY) == ["no test ran"]


def test_a_missing_file_fails(tmp_path):
    problems = guard.check(tmp_path / "missing.xml")
    assert len(problems) == 1 and problems[0].startswith("cannot read")


def test_main_returns_the_exit_code(tmp_path, capsys):
    ok = tmp_path / "ok.xml"
    ok.write_text(CLEAN, encoding="utf-8")
    bad = tmp_path / "bad.xml"
    bad.write_text(SKIPPED, encoding="utf-8")
    assert guard.main(["x", str(ok)]) == 0
    assert guard.main(["x", str(bad)]) == 1
    assert guard.main(["x"]) == 2
    capsys.readouterr()


@pytest.mark.parametrize("script", ["evidence.sh", "evidence.ps1"])
def test_both_scripts_call_the_guard_in_the_security_stage(script):
    text = (REPO / "scripts" / script).read_text(encoding="utf-8")
    assert "check_junit_no_skips.py" in text
    assert "junit-security.xml" in text


def test_makefile_has_a_security_target_that_runs_the_security_stage():
    makefile = (REPO / "Makefile").read_text(encoding="utf-8")
    assert "\nsecurity:" in makefile
    assert "scripts/evidence.sh security" in makefile
