"""Keep the evidence pipeline files in step with each other.

`scripts/evidence.sh` (Linux and CI) and `scripts/evidence.ps1` (Windows) must write the same files.
`docs/07-cicd/release-evidence-checklist.md` lists those files. The Makefile must have an `evidence` target.
`requirements-dev.txt` must pin every tool with `==`.

These tests read files only. They run no scan and write nothing.
"""

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
PROJECT_ROOT = REPO.parent

# Files the scripts write. README.md is written by hand and is not in this list.
SCRIPT_OUTPUT_FILES = [
    "run-info.txt",
    "pip-freeze.txt",
    "ruff.json",
    "junit-tests.xml",
    "junit-semantic-layer.xml",
    "junit-policy.xml",
    "opa-test.json",
    "junit-security.xml",
    "sbom.cdx.json",
    "pip-audit.json",
    "bandit.json",
    "source-checksums.txt",
    "exit-codes.txt",
]

STAGE_NAMES = [
    "install", "lint", "tests", "semantic_layer", "policy",
    "security", "sbom", "pip_audit", "bandit", "checksums",
]

TOOLS = ["jsonschema", "ruff", "bandit", "pip-audit", "cyclonedx-bom"]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_both_scripts_name_every_output_file():
    sh = _read(REPO / "scripts" / "evidence.sh")
    ps1 = _read(REPO / "scripts" / "evidence.ps1")
    missing_sh = [name for name in SCRIPT_OUTPUT_FILES if name not in sh]
    missing_ps1 = [name for name in SCRIPT_OUTPUT_FILES if name not in ps1]
    assert missing_sh == [], f"evidence.sh does not write: {missing_sh}"
    assert missing_ps1 == [], f"evidence.ps1 does not write: {missing_ps1}"


def test_both_scripts_run_every_stage():
    sh = _read(REPO / "scripts" / "evidence.sh")
    ps1 = _read(REPO / "scripts" / "evidence.ps1")
    for name in STAGE_NAMES:
        assert f"stage_{name}()" in sh, f"evidence.sh has no stage {name}"
        assert re.search(rf"\b{name}\s*=\s*\"Stage-", ps1), f"evidence.ps1 has no stage {name}"


def test_checklist_lists_every_output_file():
    checklist = _read(REPO / "docs" / "07-cicd" / "release-evidence-checklist.md")
    missing = [name for name in SCRIPT_OUTPUT_FILES if f"evidence/{name}" not in checklist]
    assert missing == [], f"checklist does not list: {missing}"


def test_makefile_has_an_evidence_target():
    makefile = _read(REPO / "Makefile")
    assert re.search(r"^evidence:", makefile, re.MULTILINE)
    assert "scripts/evidence.sh" in makefile


def test_dev_requirements_pin_every_tool():
    lines = [
        line.strip() for line in _read(REPO / "requirements-dev.txt").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    pinned = {line.split("==")[0].lower(): line for line in lines if "==" in line}
    assert [t for t in TOOLS if t not in pinned] == []
    assert [line for line in lines if "==" not in line] == []


def test_workflow_calls_every_stage_when_it_exists():
    """The workflow sits at the git root. If this folder is copied alone, there is nothing to check."""
    workflow = PROJECT_ROOT / ".github" / "workflows" / "ci.yml"
    if not workflow.exists():
        pytest.skip("no workflow at the git root")
    text = _read(workflow)
    assert "scripts/evidence.sh prepare" in text
    for name in STAGE_NAMES:
        assert f"scripts/evidence.sh {name}" in text, f"ci.yml does not run stage {name}"
    assert "upload-artifact" in text
    # No step may switch a failure off. Read the parsed steps so a comment cannot trip the check.
    parsed = yaml.safe_load(text)
    for job in parsed["jobs"].values():
        for step in job["steps"]:
            assert "continue-on-error" not in step, f"step {step.get('name')} sets continue-on-error"
