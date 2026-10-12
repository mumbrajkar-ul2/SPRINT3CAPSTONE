#!/usr/bin/env bash
# One-command setup for Linux and macOS.
# Creates .venv, installs requirements.txt, then runs pytest -q.
#
# Run from any folder:
#   bash scripts/bootstrap.sh
#   PYTHON=python3.11 bash scripts/bootstrap.sh
#   SKIP_TESTS=1 bash scripts/bootstrap.sh
#
# The Python name comes from the PYTHON environment variable, then "python3".
# The script exits with a non-zero code when any step fails.
# Stage S04-05 Half B. PROPOSED. Owner: Team-Force.

set -euo pipefail

PYTHON="${PYTHON:-python3}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
VENV_PYTHON="$ROOT/.venv/bin/python"
export PIP_DISABLE_PIP_VERSION_CHECK=1

fail() {
    echo "bootstrap FAILED: $1"
    exit "$2"
}

echo "== Step 1 of 4: check Python"
"$PYTHON" --version || fail "Python command '$PYTHON' did not run. Set the PYTHON variable." 1
"$PYTHON" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" \
    || fail "Python 3.10 or newer is needed. CI uses 3.11." 1

echo "== Step 2 of 4: create .venv"
if [ -x "$VENV_PYTHON" ]; then
    echo ".venv already exists. Reusing it."
else
    "$PYTHON" -m venv "$ROOT/.venv" \
        || fail "could not create .venv. On Ubuntu or Debian, install the python3-venv package for your Python version." 2
fi
"$VENV_PYTHON" --version

echo "== Step 3 of 4: install requirements.txt"
"$VENV_PYTHON" -m pip install -r requirements.txt || fail "pip install failed" 3

if [ "${SKIP_TESTS:-0}" = "1" ]; then
    echo "== Step 4 of 4: skipped (SKIP_TESTS=1)"
    echo "bootstrap OK (tests skipped)"
    exit 0
fi

echo "== Step 4 of 4: run pytest -q"
"$VENV_PYTHON" -m pytest -q || fail "pytest reported a failure" 4

echo "bootstrap OK"
