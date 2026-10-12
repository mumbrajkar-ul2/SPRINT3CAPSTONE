"""Security test: the secret scan finds planted values. Stage S05-13 Half B (NG-04).

Design: docs/13-security-validation/negative-tests.md. The planted strings are built in
pieces so that test_secret_patterns.py does not flag this file.
"""

import pytest

from tests.security import test_secret_patterns as scan

pytestmark = pytest.mark.security


def test_secret_scan_finds_planted_values_and_ignores_the_placeholder(tmp_path, monkeypatch):
    root = tmp_path / "scanme"
    root.mkdir()
    # File 1: a key prefix followed by letters.
    (root / "one.txt").write_text("value = " + "sk" + "-" + "abcdef123456\n", encoding="utf-8")
    # File 2: a password assignment with a real-looking value.
    (root / "two.txt").write_text("PASS" + "WORD = realvalue99\n", encoding="utf-8")
    # File 3: a named key assignment with a real-looking value.
    (root / "three.txt").write_text("AI_GATEWAY_" + "KEY=abc123\n", encoding="utf-8")
    # File 4: the placeholder. The scan must allow it.
    (root / "four.txt").write_text("AI_GATEWAY_" + "KEY=" + scan.PLACEHOLDER + "\n", encoding="utf-8")

    monkeypatch.setattr(scan, "REPO", root)

    # The scan read all four files. A scan that read none would also find nothing.
    assert len(list(scan._iter_scanned_files())) == 4

    hits = scan.find_secret_pattern_hits()
    assert any(h.startswith("one.txt:") for h in hits), hits
    assert any(h.startswith("two.txt:") for h in hits), hits
    assert any(h.startswith("three.txt:") for h in hits), hits
    assert not any(h.startswith("four.txt:") for h in hits), hits


def test_secret_scan_reads_files_when_a_parent_folder_is_named_docs(tmp_path, monkeypatch):
    """SB-18. A folder named docs above the repo must not make the scan skip every file."""
    root = tmp_path / "docs" / "venv" / "scanme"
    root.mkdir(parents=True)
    (root / "one.txt").write_text("value = " + "sk" + "-" + "abcdef123456\n", encoding="utf-8")
    monkeypatch.setattr(scan, "REPO", root)
    assert len(list(scan._iter_scanned_files())) == 1
    assert scan.find_secret_pattern_hits() != []
