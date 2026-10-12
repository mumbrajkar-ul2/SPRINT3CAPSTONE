#!/usr/bin/env bash
# Runs the CI pipeline stages and writes every output file into evidence/.
# Used by `make evidence` and by .github/workflows/ci.yml (one stage per workflow step).
#
#   bash scripts/evidence.sh all            # every stage, in order
#   bash scripts/evidence.sh lint           # one stage
#   PYTHON=python3.11 bash scripts/evidence.sh all
#
# Stages, in order: prepare install lint tests semantic_layer policy security sbom pip_audit bandit checksums
# Each stage appends "<name>=<exit code>" to evidence/exit-codes.txt.
# With "all", a failed stage does not stop the later stages. The script exits 1 at the end if any stage failed.
# With one stage name, the script exits with that stage's code.
# No stage switches a scan off. A failing scan stays failing.
#
# Windows has no bash by default. scripts/evidence.ps1 does the same work with the same file names.
# docs/07-cicd/pipeline-improvement-plan.md lists the stages and the 14 file names.
# Stage S04-07 Half B. PROPOSED. Owner: Team-Force.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
EV="$ROOT/evidence"
PY="$ROOT/.venv/bin/python"
BIN="$ROOT/.venv/bin"
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONDONTWRITEBYTECODE=1

# The Rego tests need `opa`. The version below is the one the S04-06 run passed on.
# If `opa` is not on the PATH, the Docker image is tried. If neither exists, the opa stage is recorded as not_run.
OPA_VERSION="${OPA_VERSION:-1.21.1}"
OPA_IMAGE="${OPA_IMAGE:-openpolicyagent/opa:${OPA_VERSION}}"

record() { echo "$1=$2" >> "$EV/exit-codes.txt"; }

# run_stage <name> <command...>: run the command, record its exit code, return that code.
run_stage() {
    local name="$1"; shift
    echo "== stage $name"
    "$@"
    local code=$?
    record "$name" "$code"
    echo "== stage $name exit code $code"
    return "$code"
}

stage_prepare() {
    mkdir -p "$EV"
    # Keep README.md. Remove every other file, so the secret-pattern test never reads output from an older run.
    find "$EV" -mindepth 1 ! -name README.md -delete
    : > "$EV/exit-codes.txt"
    {
        echo "commit=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
        echo "date_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "runner=$([ -n "${GITHUB_ACTIONS:-}" ] && echo github-actions || echo local)"
        echo "os=$(uname -sr)"
        echo "python_for_venv=$(${PYTHON:-python3} --version 2>&1)"
        if [ -x "$PY" ]; then echo "python_in_venv=$("$PY" --version 2>&1)"; fi
        if command -v opa >/dev/null 2>&1; then echo "opa=$(opa version | head -1)"; else echo "opa=not on PATH"; fi
    } > "$EV/run-info.txt"
    return 0
}

stage_install() {
    SKIP_TESTS=1 bash "$ROOT/scripts/bootstrap.sh" || return $?
    "$PY" -m pip install -r requirements-dev.txt || return $?
    "$PY" -m pip freeze > "$EV/pip-freeze.txt"
}

stage_lint() {
    "$PY" -m ruff check apps etl legacy scripts tests semantic-layer policy \
        --output-format json --output-file "$EV/ruff.json"
}

stage_tests() {
    "$PY" -m pytest tests -m "not security" -q -p no:cacheprovider --junitxml="$EV/junit-tests.xml"
}

stage_semantic_layer() {
    "$PY" -m pytest semantic-layer/tests -q -p no:cacheprovider --junitxml="$EV/junit-semantic-layer.xml"
}

stage_policy() {
    "$PY" -m pytest policy/tests -q -p no:cacheprovider --junitxml="$EV/junit-policy.xml"
    local pytest_code=$?
    local opa_code=0
    if command -v opa >/dev/null 2>&1; then
        opa test policy/opa policy/tests --format json > "$EV/opa-test.json"
        opa_code=$?
    elif command -v docker >/dev/null 2>&1; then
        echo "opa_image=$OPA_IMAGE" >> "$EV/run-info.txt"
        docker run --rm -v "$ROOT/policy:/policy:ro" "$OPA_IMAGE" test /policy/opa /policy/tests --format json > "$EV/opa-test.json"
        opa_code=$?
    else
        echo "opa binary and docker are both absent. opa-test.json is not written."
        record opa not_run
        return "$pytest_code"
    fi
    record opa "$opa_code"
    if [ "$pytest_code" -ne 0 ]; then return "$pytest_code"; fi
    return "$opa_code"
}

stage_security() {
    "$PY" -m pytest -m security -q -p no:cacheprovider --junitxml="$EV/junit-security.xml"
}

stage_sbom() {
    # A second venv holds only requirements.txt, so the SBOM does not list the scan tools.
    local tmp python_for_sbom
    tmp="$(mktemp -d)"
    python_for_sbom="${PYTHON:-python3}"
    "$python_for_sbom" -m venv "$tmp/venv" || { rm -rf "$tmp"; return 1; }
    "$tmp/venv/bin/python" -m pip install -q -r requirements.txt || { rm -rf "$tmp"; return 1; }
    "$BIN/cyclonedx-py" environment --of JSON -o "$EV/sbom.cdx.json" "$tmp/venv/bin/python"
    local code=$?
    rm -rf "$tmp"
    return "$code"
}

stage_pip_audit() {
    "$PY" -m pip_audit -r requirements.txt -r requirements-dev.txt -f json -o "$EV/pip-audit.json"
}

stage_bandit() {
    "$PY" -m bandit -r apps etl legacy scripts semantic-layer/build.py -f json -o "$EV/bandit.json"
}

stage_checksums() {
    sha256sum legacy/*.py etl/*.py policy/opa/*.rego policy/opa/policy_data.json > "$EV/source-checksums.txt"
}

STAGES="install lint tests semantic_layer policy security sbom pip_audit bandit checksums"

run_one() {
    local name="$1"
    if [ "$name" = "prepare" ]; then stage_prepare; return $?; fi
    if [ ! -d "$EV" ]; then mkdir -p "$EV"; fi
    if [ "$name" != "install" ] && [ ! -x "$PY" ]; then
        echo "evidence FAILED: $PY not found. Run the install stage or scripts/bootstrap.sh first."
        record "$name" 127
        return 127
    fi
    run_stage "$name" "stage_$name"
}

TARGET="${1:-all}"
case "$TARGET" in
    all)
        stage_prepare
        failed=0
        for s in $STAGES; do
            run_one "$s" || failed=$((failed + 1))
        done
        echo "== evidence done. Failed stages: $failed. See evidence/exit-codes.txt"
        [ "$failed" -eq 0 ] || exit 1
        ;;
    prepare | install | lint | tests | semantic_layer | policy | security | sbom | pip_audit | bandit | checksums)
        run_one "$TARGET"
        exit $?
        ;;
    *)
        echo "usage: bash scripts/evidence.sh [all|prepare|$STAGES]"
        exit 2
        ;;
esac
