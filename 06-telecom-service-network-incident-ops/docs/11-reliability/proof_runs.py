"""Proof runs for S04-11 Half B. Each run switches ONE protection off and runs the drill that guards it.

A drill that still passes with its protection off proves nothing. Each run here must FAIL.
Nothing on disk changes. The switch-off happens inside the test process only.

Run from the project root:
    .venv\\Scripts\\python.exe docs/11-reliability/proof_runs.py
"""

import contextlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402

RUNS = {
    "no-audit-lock": (
        "tests/reliability/test_breaker.py::test_eight_threads_writing_the_audit_log_lose_no_row"
    ),
    "no-breaker-no-limit": "tests/reliability/test_breaker.py -k route_",
}


def run_in_process(name):
    from apps.api.services import audit, breaker

    if name == "no-audit-lock":
        audit._WRITE_LOCK = contextlib.nullcontext()
    elif name == "no-breaker-no-limit":

        class Open:
            def ok(self):
                pass

            failed = neutral = ok

        breaker.CircuitBreaker.admit = lambda self: Open()
    target = RUNS[name].split(" -k ")
    args = [target[0], "-q", "-p", "no:cacheprovider", "-W", "ignore", "--tb=line"]
    if len(target) == 2:
        args += ["-k", target[1]]
    return pytest.main(args)


def run_old_etl():
    """Put the ORIGINAL ETL (from git HEAD) in place for one run, then restore this one."""
    path = ROOT / "etl" / "run_daily_batch.py"
    current = path.read_bytes()
    original = subprocess.run(
        ["git", "show", "HEAD:06-telecom-service-network-incident-ops/etl/run_daily_batch.py"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    try:
        path.write_bytes(original)
        return subprocess.run(
            [sys.executable, "-m", "pytest", "tests/reliability/test_drills.py", "-q", "-k", "dr5",
             "-p", "no:cacheprovider", "-W", "ignore", "--tb=line"],
            cwd=ROOT,
        ).returncode
    finally:
        path.write_bytes(current)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in RUNS:
        sys.exit(run_in_process(sys.argv[1]))
    if len(sys.argv) == 2 and sys.argv[1] == "old-etl":
        sys.exit(run_old_etl())
    for label in [*RUNS, "old-etl"]:
        print(f"=== proof run: {label}")
        code = subprocess.run([sys.executable, __file__, label], cwd=ROOT).returncode
        print(f"=== {label}: exit {code} ({'FAILED as expected' if code else 'STILL PASSED: drill proves nothing'})")
