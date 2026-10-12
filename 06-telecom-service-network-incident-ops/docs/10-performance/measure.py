"""Stage S04-10. Performance baseline for the live read path.

Run from anywhere:

    .venv\\Scripts\\python.exe docs\\10-performance\\measure.py
    .venv\\Scripts\\python.exe docs\\10-performance\\measure.py --json docs\\10-performance\\measure-before.json

What it times. Every number it prints is REAL: it comes from this machine on
the day of the run. Nothing here is a production figure.

  1. load_record for an id that exists, 1000 calls.
  2. load_record for an id that is missing, 1000 calls.
  3. The same 1000 calls spread over 8 threads (does a thread pool help?).
  4. One call to the file read alone, and the memory one call allocates.
  5. Group alarms.csv by storm_batch_id and find the largest storm.
  6. Group alarms.csv by dedupe_key.
  7. Replay the 3000 lines of events.jsonl through a handler that does nothing.
  7b. The policy check every route runs, and the PATH search inside it.
  8. The AI stub (call_model) and the whole gateway call.
  9. Three routes through the app: /health, /records/{id}, /ai/summarize/{id}.
 10. One audit row append.
 11. Facts about the data that the load scenarios use.

The script changes no repo file. Route calls write their audit rows to a
temporary folder, not to logs/audit.log.

Each timing runs several rounds. The table shows the middle round (median),
and the lowest and highest per-call time.
"""

import argparse
import csv
import json
import os
import platform
import shutil
import statistics
import sys
import tempfile
import time
import tracemalloc
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from apps.api.services import ai_gateway, audit, domain_service, policy

DATA = ROOT / "data" / "synthetic"

EXISTING_ID = "DEV-00002"  # row 2 of devices.csv, stale_topology_flag false
MISSING_ID = "DEV-NO-SUCH-ID"

RESULTS: list[dict] = []


def timed(name, fn, calls, rounds, note=""):
    """Run fn() `calls` times per round. Record wall time and per-call time."""
    per_round = []
    for _ in range(rounds):
        start = time.perf_counter()
        for _ in range(calls):
            fn()
        per_round.append(time.perf_counter() - start)
    median_wall = statistics.median(per_round)
    per_call_ms = [wall / calls * 1000 for wall in per_round]
    row = {
        "name": name,
        "calls": calls,
        "rounds": rounds,
        "wall_s_median": round(median_wall, 4),
        "per_call_ms_median": round(median_wall / calls * 1000, 4),
        "per_call_ms_min": round(min(per_call_ms), 4),
        "per_call_ms_max": round(max(per_call_ms), 4),
        "note": note,
    }
    RESULTS.append(row)
    return row


def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# Item 5 and 6. Alarm grouping.
# ---------------------------------------------------------------------------


def group_alarms(column):
    counts = Counter(row[column] for row in read_csv("alarms.csv"))
    return counts


def largest_group(counts):
    """Largest group size, ignoring the blank key. Blank is not a storm id."""
    sizes = [count for key, count in counts.items() if key.strip()]
    return max(sizes) if sizes else 0


# ---------------------------------------------------------------------------
# Item 7. Event replay.
# ---------------------------------------------------------------------------


def replay_events():
    handled = 0

    def handler(_event):  # no-op
        return None

    with (DATA / "events.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                handler(json.loads(line))
                handled += 1
    return handled


# ---------------------------------------------------------------------------
# Item 11. Data facts for the scenarios.
# ---------------------------------------------------------------------------


def data_facts():
    devices = read_csv("devices.csv")
    alarms = read_csv("alarms.csv")
    orders = read_csv("service_orders.csv")
    storm_counts = group_alarms("storm_batch_id")
    dedupe_counts = group_alarms("dedupe_key")

    retry_values, retry_bad = [], 0
    for row in orders:
        try:
            retry_values.append(int(float(row["retry_count"])))
        except (TypeError, ValueError):
            retry_bad += 1

    event_types = Counter()
    event_lines = 0
    with (DATA / "events.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                event_lines += 1
                event_types[json.loads(line)["event_type"]] += 1

    storm_sizes = Counter(count for key, count in storm_counts.items() if key.strip())
    return {
        "devices_rows": len(devices),
        "alarms_rows": len(alarms),
        "service_orders_rows": len(orders),
        "events_lines": event_lines,
        "file_bytes": {
            name: (DATA / name).stat().st_size
            for name in ("devices.csv", "alarms.csv", "service_orders.csv", "events.jsonl")
        },
        "storm_batch_id_distinct_non_blank": sum(1 for key in storm_counts if key.strip()),
        "storm_batch_id_blank_rows": storm_counts.get("", 0),
        "largest_storm_size": largest_group(storm_counts),
        "storm_size_histogram": dict(sorted(storm_sizes.items())),
        "largest_storm_ids": sorted(
            key for key, count in storm_counts.items()
            if key.strip() and count == largest_group(storm_counts)
        ),
        "dedupe_key_distinct_non_blank": sum(1 for key in dedupe_counts if key.strip()),
        "dedupe_key_blank_rows": dedupe_counts.get("", 0),
        "dedupe_key_largest_group": largest_group(dedupe_counts),
        "retry_count_rows_numeric": len(retry_values),
        "retry_count_rows_not_numeric": retry_bad,
        "retry_count_sum": sum(retry_values),
        "retry_count_min": min(retry_values),
        "retry_count_max": max(retry_values),
        "retry_count_rows_at_or_above_1000": sum(1 for value in retry_values if value >= 1000),
        "events_by_flow": dict(event_types),
    }


def scenarios(facts, per_call_ms):
    """EDUCATIONAL arithmetic. Every row rests on an Assumption named in the key."""
    capacity_per_minute = round(60_000 / per_call_ms)
    storm = facts["largest_storm_size"]
    out = {
        "label": "EDUCATIONAL",
        "assumption": "One load_record call per alarm, per event, or per retry. No route does this today.",
        "load_record_per_call_ms_used": per_call_ms,
        "one_thread_capacity_calls_per_minute": capacity_per_minute,
        "storm": [],
        "replay": {},
        "retries": {},
    }
    for multiplier in (1, 10, 100, 1000):
        calls = storm * multiplier
        out["storm"].append(
            {
                "multiplier_N": multiplier,
                "alarms_in_storm": calls,
                "seconds_one_thread": round(calls * per_call_ms / 1000, 2),
                "fits_in_one_minute_one_thread": calls <= capacity_per_minute,
            }
        )
    out["storm_largest_N_that_fits_one_minute"] = capacity_per_minute // storm
    events = facts["events_lines"]
    out["replay"] = {
        "events": events,
        "calls_per_minute_if_done_in_one_minute": events,
        "seconds_one_thread_if_each_event_reads_a_record": round(events * per_call_ms / 1000, 2),
    }
    total = facts["retry_count_sum"]
    out["retries"] = {
        "sum_retry_count": total,
        "seconds_one_thread_if_each_retry_reads_a_record": round(total * per_call_ms / 1000, 1),
        "calls_per_minute_if_spread_over_24h": round(total / 1440, 1),
        "calls_per_minute_if_spread_over_1h": round(total / 60, 1),
    }
    return out


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--json", help="write the results to this file")
    args = parser.parse_args()
    rounds = args.rounds

    # 1 and 2. The record read.
    existing = timed(
        "load_record existing id", lambda: domain_service.load_record(EXISTING_ID), 1000, rounds,
        "reads devices.csv on every call",
    )
    timed(
        "load_record missing id", lambda: domain_service.load_record(MISSING_ID), 1000, rounds,
        "reads devices.csv, scans every row, returns row 1",
    )
    assert domain_service.load_record(MISSING_ID)["device_id"] == "REC-0001"

    # 3. Eight threads.
    def threaded_round():
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda _i: domain_service.load_record(EXISTING_ID), range(1000)))

    per_round = []
    for _ in range(rounds):
        start = time.perf_counter()
        threaded_round()
        per_round.append(time.perf_counter() - start)
    median_wall = statistics.median(per_round)
    RESULTS.append(
        {
            "name": "load_record existing id, 8 threads",
            "calls": 1000,
            "rounds": rounds,
            "wall_s_median": round(median_wall, 4),
            # 1000 calls, so wall seconds equal milliseconds per call.
            "per_call_ms_median": round(median_wall, 4),
            "per_call_ms_min": round(min(per_round), 4),
            "per_call_ms_max": round(max(per_round), 4),
            "note": "1000 calls shared by 8 threads. Per-call is wall time divided by 1000.",
        }
    )

    # 4. The read alone, and the memory one call allocates.
    timed("read devices.csv into rows (no search)", lambda: read_csv("devices.csv"), 1000, rounds,
          "the part of load_record that is repeated")
    tracemalloc.start()
    domain_service.load_record(EXISTING_ID)
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 5 and 6. Alarm grouping.
    timed("group alarms by storm_batch_id", lambda: group_alarms("storm_batch_id"), 100, rounds,
                  "reads alarms.csv, counts by storm_batch_id")
    timed("group alarms by dedupe_key", lambda: group_alarms("dedupe_key"), 100, rounds,
          "reads alarms.csv, counts by dedupe_key")

    # 7. Event replay.
    replay = timed("replay events.jsonl (3000 lines, no-op handler)", replay_events, 20, rounds,
                   "one call is the whole file")
    replay["per_line_us_median"] = round(replay["per_call_ms_median"] / 3000 * 1000, 3)

    # 7b. The policy check that every route runs first. engine_name() looks for
    # the `opa` program on the PATH on every call.
    timed("shutil.which('opa') (inside every policy call)", lambda: shutil.which("opa"), 200, rounds,
          "searches every PATH folder. Cost depends on the machine")
    timed("policy.check_record_read (python engine)", lambda: policy.check_record_read("role.operator"),
          200, rounds, "one access decision")

    # 8. The AI stub, and the whole gateway call.
    prompt = ai_gateway.build_prompt(domain_service.load_record(EXISTING_ID))
    timed("ai_gateway.call_model (stub)", lambda: ai_gateway.call_model(prompt), 100, rounds,
                 "sleeps 0.01 s inside the stub")
    role_id = policy.role_id_from_header("operator")
    access = policy.check_summarize(role_id)
    record = domain_service.load_record(EXISTING_ID)
    timed(
        "ai_gateway.summarize_record (whole call)",
        lambda: ai_gateway.summarize_record(record, record_id=EXISTING_ID, role_id=role_id, access=access),
        100, rounds,
        "policy twice, prompt, hash, thread pool, stub, output check",
    )
    assert ai_gateway.summarize_record(
        record, record_id=EXISTING_ID, role_id=role_id, access=access
    ).outcome == "RECOMMEND_ONLY"

    # 9. Routes. Audit rows go to a temporary folder.
    from fastapi.testclient import TestClient

    real_log = audit.LOG
    with tempfile.TemporaryDirectory() as tmp:
        audit.LOG = Path(tmp) / "audit.log"
        from apps.api.main import app

        client = TestClient(app)
        timed("route GET /health", lambda: client.get("/health"), 200, rounds,
              "no file read, no audit row")
        timed("route GET /records/{id}", lambda: client.get(f"/records/{EXISTING_ID}"), 200, rounds,
              "policy, load_record, one audit row")
        timed(
            "route POST /ai/summarize/{id}",
            lambda: client.post(f"/ai/summarize/{EXISTING_ID}", headers={"X-User-Role": "operator"}),
            100, rounds,
            "policy, load_record, gateway, one audit row",
        )
        # 10. One audit append.
        timed(
            "audit.write_event (one row)",
            lambda: audit.write_event(
                "record.read", correlation_id="perf", actor="noc_operator", role="operator",
                resource="resource.device",
            ),
            1000, rounds, "opens the log, appends one line, closes it",
        )
    audit.LOG = real_log

    facts = data_facts()
    scen = scenarios(facts, existing["per_call_ms_median"])

    report = {
        "label": "REAL (this machine, this run)",
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "policy_engine": policy.engine_name(),
        "rounds_per_timing": rounds,
        "timings": RESULTS,
        "load_record_peak_alloc_kib_one_call": round(peak / 1024, 1),
        "anyio_default_thread_limit_for_sync_routes": 40,
        "data_facts": facts,
        "scenarios": scen,
    }

    # The table.
    print(f"Run at {report['run_at']}  Python {report['python']}  engine {report['policy_engine']}  "
          f"CPUs {report['cpu_count']}")
    print(f"{'Measured item':<52}{'calls':>6}{'wall s':>9}{'ms/call':>10}{'min':>9}{'max':>9}")
    for row in RESULTS:
        print(f"{row['name']:<52}{row['calls']:>6}{row['wall_s_median']:>9.3f}"
              f"{row['per_call_ms_median']:>10.3f}{row['per_call_ms_min']:>9.3f}{row['per_call_ms_max']:>9.3f}")
    print(f"\nOne load_record call allocates a peak of {report['load_record_peak_alloc_kib_one_call']} KiB")
    print(f"Largest storm: {facts['largest_storm_size']} alarms {facts['largest_storm_ids']}")
    print(f"Sum of retry_count: {facts['retry_count_sum']}")
    print(f"One-thread capacity at {existing['per_call_ms_median']} ms/call: "
          f"{scen['one_thread_capacity_calls_per_minute']} calls per minute")

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
