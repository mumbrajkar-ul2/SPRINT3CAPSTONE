"""Stage S04-11 Half A. Read-only probe of how the system fails today.

Run from anywhere:

    .venv\\Scripts\\python.exe docs\\11-reliability\\probe_half_a.py
    .venv\\Scripts\\python.exe docs\\11-reliability\\probe_half_a.py --json docs\\11-reliability\\probe-output.json

Every number it prints is REAL: it comes from this machine on the day of the run.

What it does.

  D1 to D3  Count facts in alarms.csv, service_orders.csv, and events.jsonl.
  P1 to P10 Call the running app in memory (no server) with one thing broken at a time.
  P11       Run etl/run_daily_batch.py on a copy of the tree with damaged rows.

The script changes no repo file. Audit rows go to a temporary folder. The ETL
runs on a copy in a temporary folder. data/synthetic is only read.
"""

import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from apps.api.main import app  # noqa: E402
from apps.api.services import ai_gateway, audit, domain_service, policy  # noqa: E402

DATA = ROOT / "data" / "synthetic"
OPERATOR = {"X-User-Role": "operator"}
GOOD_ID = "DEV-00002"  # row 2 of devices.csv, stale_topology_flag false

RESULTS = {}


def record(key, value):
    RESULTS[key] = value
    print(f"{key}: {json.dumps(value, default=str)}")


def valid_answer(record_id=GOOD_ID):
    return json.dumps(
        {
            "record_id": record_id,
            "summary": "SIMULATED probe summary",
            "recommendation": "Review and approve before action",
            "outcome": "RECOMMEND_ONLY",
            "source_count": 1,
        }
    )


class CountingModel:
    """A stand-in for call_model that counts calls and can sleep or raise."""

    def __init__(self, sleep=0.0, error=None):
        self.calls = 0
        self.sleep = sleep
        self.error = error
        self._lock = threading.Lock()

    def __call__(self, prompt):
        with self._lock:
            self.calls += 1
        if self.sleep:
            time.sleep(self.sleep)
        if self.error is not None:
            raise self.error
        return valid_answer()


class Env:
    """Set environment variables for a block, then put them back."""

    def __init__(self, **values):
        self.values = values
        self.old = {}

    def __enter__(self):
        for key, value in self.values.items():
            self.old[key] = os.environ.get(key)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def __exit__(self, *exc):
        for key, value in self.old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def read_rows(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


# ---------------------------------------------------------------------------
# D. Data facts
# ---------------------------------------------------------------------------


def data_facts():
    with (DATA / "alarms.csv").open(newline="", encoding="utf-8") as handle:
        alarms = list(csv.DictReader(handle))
    before_first = 0
    unreadable = []
    line_of = {}
    for number, row in enumerate(alarms, start=2):
        line_of.setdefault(row["alarm_id"], number)
        try:
            first = datetime.fromisoformat(row["first_seen_at"])
            last = datetime.fromisoformat(row["last_seen_at"])
        except ValueError:
            unreadable.append(row["alarm_id"])
            continue
        if last < first:
            before_first += 1
    keys = Counter(row["dedupe_key"] for row in alarms if row["dedupe_key"])
    repeated = {key: count for key, count in keys.items() if count > 1}
    pair_counts = Counter(
        (row["dedupe_key"], row["storm_batch_id"])
        for row in alarms
        if row["dedupe_key"] and row["storm_batch_id"]
    )
    same_pair = {f"{k[0]}|{k[1]}": c for k, c in pair_counts.items() if c > 1}
    record(
        "D1_alarms",
        {
            "rows": len(alarms),
            "last_seen_before_first_seen": before_first,
            "unreadable_timestamp_rows": unreadable,
            "ALA-00002_file_line": line_of.get("ALA-00002"),
            "blank_dedupe_key_rows": sum(1 for r in alarms if not r["dedupe_key"]),
            "dedupe_keys_seen_more_than_once": repeated,
            "dedupe_key_and_storm_batch_both_equal_more_than_once": same_pair,
            "alarm_ids_seen_more_than_once": {
                k: c
                for k, c in Counter(r["alarm_id"] for r in alarms).items()
                if c > 1
            },
        },
    )

    with (DATA / "service_orders.csv").open(newline="", encoding="utf-8") as handle:
        orders = list(csv.DictReader(handle))
    numeric = []
    blank = []
    for row in orders:
        text = row["retry_count"].strip()
        if text == "":
            blank.append(row["order_id"])
        else:
            numeric.append(int(float(text)))
    ids = Counter(row["order_id"] for row in orders)
    pairs = Counter((row["order_id"], row["retry_count"]) for row in orders)
    record(
        "D2_service_orders",
        {
            "rows": len(orders),
            "retry_count_numeric_rows": len(numeric),
            "retry_count_blank_rows": blank,
            "retry_count_sum": sum(numeric),
            "retry_count_at_or_above_1000": sum(1 for v in numeric if v >= 1000),
            "order_ids_seen_more_than_once": {k: c for k, c in ids.items() if c > 1},
            "order_id_and_retry_count_both_equal_more_than_once": {
                f"{k[0]}|{k[1]}": c for k, c in pairs.items() if c > 1
            },
            "rows_with_same_order_id_and_different_retry_count": sum(
                1
                for order_id, count in ids.items()
                if count > 1
                and len({r["retry_count"] for r in orders if r["order_id"] == order_id}) > 1
            ),
        },
    )

    events = read_rows(DATA / "events.jsonl")
    filled = [e for e in events if (e.get("correlation_id") or "").strip()]
    hashes = Counter(e["payload_hash"] for e in events)
    chain = defaultdict(list)
    for e in filled:
        chain[e["correlation_id"]].append(e)
    same_chain_same_hash = sum(
        1
        for items in chain.values()
        if len({e["payload_hash"] for e in items}) < len(items)
    )
    record(
        "D3_events",
        {
            "lines": len(events),
            "field_names": sorted(events[0].keys()),
            "has_a_sequence_field": any("seq" in key for key in events[0]),
            "distinct_event_id": len({e["event_id"] for e in events}),
            "correlation_id_filled": len(filled),
            "correlation_id_blank_or_null": len(events) - len(filled),
            "distinct_payload_hash": len(hashes),
            "payload_hash_seen_more_than_once": sum(1 for c in hashes.values() if c > 1),
            "chains_with_two_lines_sharing_a_payload_hash": same_chain_same_hash,
            "ids_with_more_than_one_line": sum(1 for v in chain.values() if len(v) > 1),
        },
    )

    with (DATA / "devices.csv").open(newline="", encoding="utf-8") as handle:
        devices = list(csv.DictReader(handle))
    flags = Counter((row["stale_topology_flag"] or "<blank>") for row in devices)
    record("D4_devices_stale_flag", dict(flags))


# ---------------------------------------------------------------------------
# P. The running app with one thing broken
# ---------------------------------------------------------------------------


def probes(tmp):
    log = tmp / "audit.log"
    audit.LOG = log

    def audit_rows():
        if not log.exists():
            return []
        return [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]

    domain_service.reset_cache()
    policy.reset_engine_cache()
    real_model = ai_gateway.call_model
    client = TestClient(app, raise_server_exceptions=False)

    # P1. Missing correlation id.
    response = client.get("/health")
    cid = response.headers.get("x-correlation-id", "")
    try:
        is_uuid = str(uuid.UUID(cid)) == cid
    except ValueError:
        is_uuid = False
    response_sent = client.get("/health", headers={"X-Correlation-Id": "demo-123"})
    blank = client.get("/health", headers={"X-Correlation-Id": "   "})
    record(
        "P1_missing_correlation_id",
        {
            "status": response.status_code,
            "response_header_is_uuid": is_uuid,
            "sent_value_kept": response_sent.headers.get("x-correlation-id"),
            "blank_value_replaced_by_uuid": blank.headers.get("x-correlation-id") != "   ",
            "health_writes_an_audit_row": len(audit_rows()) > 0,
        },
    )
    client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    rows = audit_rows()
    record(
        "P1b_record_read_audit_row_has_correlation_id",
        {"rows": len(rows), "correlation_id_filled": bool(rows and rows[-1].get("correlation_id"))},
    )
    log.write_text("", encoding="utf-8")

    # P2. AI timeout. The model sleeps longer than the deadline.
    model = CountingModel(sleep=1.0)
    ai_gateway.call_model = model
    with Env(AI_MODEL_TIMEOUT_SECONDS="0.1"):
        started = time.perf_counter()
        response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
        elapsed_ms = round((time.perf_counter() - started) * 1000)
    body = response.json()
    health_after = client.get("/health")
    record_after = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    rows = audit_rows()
    record(
        "P2_ai_timeout",
        {
            "status": response.status_code,
            "outcome": body.get("outcome"),
            "reasons": body.get("reasons"),
            "summary": body.get("summary"),
            "recommendation": body.get("recommendation"),
            "elapsed_ms": elapsed_ms,
            "health_status": health_after.status_code,
            "record_read_status": record_after.status_code,
            "audit_actions": [r["action"] for r in rows],
            "audit_outcome": rows[0].get("outcome") if rows else None,
        },
    )
    time.sleep(1.0)
    log.write_text("", encoding="utf-8")

    # P3. The model raises a connection error. What reason does the user get?
    ai_gateway.call_model = CountingModel(error=ConnectionRefusedError("refused"))
    response = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    body = response.json()
    record(
        "P3_model_connection_refused",
        {
            "status": response.status_code,
            "outcome": body.get("outcome"),
            "reasons": body.get("reasons"),
            "summary": body.get("summary"),
        },
    )
    log.write_text("", encoding="utf-8")

    # P4. What does one retry duplicate? Five identical summarize calls.
    model = CountingModel()
    ai_gateway.call_model = model
    same = {**OPERATOR, "X-Correlation-Id": "retry-probe-1"}
    codes = [client.post(f"/ai/summarize/{GOOD_ID}", headers=same).status_code for _ in range(5)]
    rows = audit_rows()
    record(
        "P4_five_identical_summarize_calls",
        {
            "status_codes": codes,
            "model_calls": model.calls,
            "audit_rows": len(rows),
            "audit_rows_with_that_correlation_id": sum(
                1 for r in rows if r.get("correlation_id") == "retry-probe-1"
            ),
            "alarm_incident_or_order_writers_in_apps": _writers_found(),
        },
    )
    log.write_text("", encoding="utf-8")

    # P5. Threads. 50 slow summaries, then /health and /records while they wait.
    ai_gateway.call_model = CountingModel(sleep=3.0)
    quiet = []
    with TestClient(app) as shared:
        for _ in range(5):
            t0 = time.perf_counter()
            shared.get("/health")
            quiet.append((time.perf_counter() - t0) * 1000)
        quiet_record = []
        for _ in range(5):
            t0 = time.perf_counter()
            shared.get(f"/records/{GOOD_ID}", headers=OPERATOR)
            quiet_record.append((time.perf_counter() - t0) * 1000)
        threads_before = threading.active_count()
        done = []
        with Env(AI_MODEL_TIMEOUT_SECONDS="1.5"):

            def summarize():
                t0 = time.perf_counter()
                r = shared.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
                done.append((r.status_code, (time.perf_counter() - t0) * 1000))

            pool = ThreadPoolExecutor(max_workers=60)
            futures = [pool.submit(summarize) for _ in range(50)]
            time.sleep(0.4)
            health = []
            records = []

            def timed_health():
                t0 = time.perf_counter()
                r = shared.get("/health")
                health.append((r.status_code, (time.perf_counter() - t0) * 1000))

            def timed_record():
                t0 = time.perf_counter()
                r = shared.get(f"/records/{GOOD_ID}", headers=OPERATOR)
                records.append((r.status_code, (time.perf_counter() - t0) * 1000))

            side = [threading.Thread(target=timed_health) for _ in range(3)] + [
                threading.Thread(target=timed_record) for _ in range(3)
            ]
            for t in side:
                t.start()
            time.sleep(0.2)
            threads_during = threading.active_count()
            for t in side:
                t.join()
            for f in futures:
                f.result()
            pool.shutdown()
        threads_just_after = threading.active_count()
    time.sleep(3.2)
    threads_later = threading.active_count()
    record(
        "P5_thread_use_while_the_model_hangs",
        {
            "summaries_sent": 50,
            "route_thread_limit": 40,
            "model_wait_s": 3.0,
            "timeout_s": 1.5,
            "health_idle_ms_max": round(max(quiet), 1),
            "record_read_idle_ms_max": round(max(quiet_record), 1),
            "health_during_hang": [(s, round(ms)) for s, ms in health],
            "record_read_during_hang": [(s, round(ms)) for s, ms in records],
            "summary_status_counts": dict(Counter(s for s, _ in done)),
            "process_threads_before": threads_before,
            "process_threads_during": threads_during,
            "process_threads_just_after_all_returned": threads_just_after,
            "process_threads_3s_later": threads_later,
        },
    )
    log.write_text("", encoding="utf-8")

    # P6. The policy engine is not available.
    ai_gateway.call_model = CountingModel()
    with Env(POLICY_ENGINE="opa"):
        policy.reset_engine_cache()
        read = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
        summary = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
        health = client.get("/health")
        decision = policy.check_record_read("role.operator")
    rows = audit_rows()
    policy.reset_engine_cache()
    record(
        "P6_policy_engine_unavailable",
        {
            "opa_on_path": shutil.which("opa") is not None,
            "record_read_status": read.status_code,
            "record_read_body": read.json(),
            "summary_status": summary.status_code,
            "summary_body": summary.json(),
            "health_status": health.status_code,
            "decision": decision,
            "audit_actions": [r["action"] for r in rows],
            "audit_row_has_the_reason": any("reason" in json.dumps(r).lower() for r in rows),
        },
    )
    log.write_text("", encoding="utf-8")

    # P7. devices.csv is missing.
    good_dir = domain_service.DATA_DIR
    empty = tmp / "empty_data"
    empty.mkdir()
    domain_service.DATA_DIR = empty
    domain_service.reset_cache()
    model = CountingModel()
    ai_gateway.call_model = model
    read = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    summary = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    health = client.get("/health")
    rows = audit_rows()
    record(
        "P7_devices_csv_missing",
        {
            "record_read_status": read.status_code,
            "record_read_body": read.text[:40],
            "record_read_has_correlation_header": "x-correlation-id" in read.headers,
            "summary_status": summary.status_code,
            "model_calls": model.calls,
            "health_status": health.status_code,
            "audit_rows_written": len(rows),
        },
    )
    # Header-only file: the loader answers with an error body, not an exception.
    (empty / "devices.csv").write_text(
        (good_dir / "devices.csv").read_text(encoding="utf-8").splitlines()[0] + "\n",
        encoding="utf-8",
    )
    domain_service.reset_cache()
    read = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    summary = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    record(
        "P7b_devices_csv_has_header_only",
        {
            "record_read_status": read.status_code,
            "record_read_body": read.json(),
            "summary_status": summary.status_code,
            "summary_outcome": summary.json().get("outcome"),
            "summary_reasons": summary.json().get("reasons"),
        },
    )
    domain_service.DATA_DIR = good_dir
    domain_service.reset_cache()
    log.write_text("", encoding="utf-8")

    # P8. The audit log cannot be written.
    blocker = tmp / "not_a_folder"
    blocker.write_text("x", encoding="utf-8")
    audit.LOG = blocker / "audit.log"
    model = CountingModel()
    ai_gateway.call_model = model
    read = client.get(f"/records/{GOOD_ID}", headers=OPERATOR)
    summary = client.post(f"/ai/summarize/{GOOD_ID}", headers=OPERATOR)
    health = client.get("/health")
    record(
        "P8_audit_log_unwritable",
        {
            "record_read_status": read.status_code,
            "record_read_body_has_device_data": "device_id" in read.text,
            "summary_status": summary.status_code,
            "summary_body_has_summary_text": "SIMULATED" in summary.text,
            "model_calls_before_the_failure": model.calls,
            "health_status": health.status_code,
            "has_correlation_header_on_500": "x-correlation-id" in read.headers,
        },
    )
    audit.LOG = log

    # P9. Eight threads append to the audit log at once.
    log.write_text("", encoding="utf-8")

    def writer(n):
        for i in range(250):
            audit.write_event(
                "probe.write",
                correlation_id=f"c-{n}-{i}",
                actor=None,
                role="operator",
                resource="resource.device",
            )

    rounds = []
    for _ in range(3):
        log.write_text("", encoding="utf-8")
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(writer, range(8)))
        lines = log.read_text(encoding="utf-8").splitlines()
        parsed = set()
        bad = 0
        for line in lines:
            try:
                parsed.add(json.loads(line)["correlation_id"])
            except (ValueError, KeyError):
                bad += 1
        rounds.append(
            {
                "rows_expected": 2000,
                "lines_in_file": len(lines),
                "lines_that_do_not_parse": bad,
                "distinct_rows_recovered": len(parsed),
                "rows_lost": 2000 - len(parsed),
            }
        )
    record("P9_concurrent_audit_writes_3_rounds_8_threads", rounds)
    log.write_text("", encoding="utf-8")

    # P10. A true, a blank, and a false stale flag.
    ai_gateway.call_model = CountingModel()
    stale = None
    clear = None
    blank_row = None
    with (DATA / "devices.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            flag = row["stale_topology_flag"].strip().lower()
            if flag == "true" and stale is None and row["device_id"].startswith("DEV-"):
                stale = row["device_id"]
            if flag == "false" and clear is None and row["device_id"].startswith("DEV-"):
                clear = row["device_id"]
            if flag == "" and blank_row is None and row["device_id"].startswith("DEV-"):
                blank_row = row["device_id"]
    out = {}
    for name, device in (("true", stale), ("false", clear), ("blank", blank_row)):
        if device is None:
            out[name] = None
            continue
        read = client.get(f"/records/{device}", headers=OPERATOR)
        summary = client.post(f"/ai/summarize/{device}", headers=OPERATOR)
        out[name] = {
            "device": device,
            "record_read_status": read.status_code,
            "record_read_shows_flag_value": read.json().get("stale_topology_flag"),
            "summary_status": summary.status_code,
            "summary_outcome": summary.json().get("outcome"),
            "summary_reasons": summary.json().get("reasons"),
            "summary_text": summary.json().get("summary"),
        }
    record("P10_stale_topology_flag", out)

    ai_gateway.call_model = real_model
    audit.LOG = Path(__file__).resolve().parents[2] / "logs" / "audit.log"


def _writers_found():
    """Lines in apps/ that open alarms.csv, service_orders.csv, or events.jsonl for writing."""
    hits = 0
    for path in (ROOT / "apps").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for name in ("alarms.csv", "service_orders.csv", "events.jsonl", "incidents.csv"):
            if name in text:
                hits += 1
    return hits


# ---------------------------------------------------------------------------
# P11. The daily batch on a damaged copy
# ---------------------------------------------------------------------------


def etl_probe(tmp):
    base = tmp / "etl_tree"
    (base / "etl").mkdir(parents=True)
    (base / "data" / "synthetic").mkdir(parents=True)
    shutil.copy(ROOT / "etl" / "run_daily_batch.py", base / "etl" / "run_daily_batch.py")
    lines = (DATA / "devices.csv").read_bytes().splitlines()
    header = lines[0]
    good = lines[1:4]
    cells = good[0].split(b",")
    blank_cell = b",".join(cells[:3] + [b""] + cells[4:])
    short_row = b",".join(cells[:-2])
    long_row = good[0] + b",extra,extra"
    target = base / "data" / "synthetic" / "devices.csv"

    def run():
        proc = subprocess.run(
            [sys.executable, str(base / "etl" / "run_daily_batch.py"), "--sample"],
            cwd=base,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""
        return {"exit_code": proc.returncode, "stdout": proc.stdout.strip(), "stderr_last_line": tail}

    # A. Three good rows, one blank cell, one short row, one long row.
    target.write_bytes(b"\n".join([header, *good, blank_cell, short_row, long_row]) + b"\n")
    a = run()
    a["rows_written"] = 6
    a["rows_that_are_bad"] = 3
    # B. The same rows plus a line that is not UTF-8, then two more good rows.
    target.write_bytes(
        b"\n".join([header, *good, blank_cell, b"\xff\xfe,not,utf8", *good[:2]]) + b"\n"
    )
    b = run()
    b["rows_written"] = 7
    # C. No file.
    target.unlink()
    c = run()
    record("P11a_etl_blank_short_long_rows", a)
    record("P11b_etl_line_that_is_not_utf8", b)
    record("P11c_etl_file_missing", c)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", help="Write the results to this file.")
    args = parser.parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    audit_before = (ROOT / "logs" / "audit.log")
    size_before = audit_before.stat().st_size if audit_before.exists() else 0
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        data_facts()
        probes(tmp)
        etl_probe(tmp)
    size_after = audit_before.stat().st_size if audit_before.exists() else 0
    record("Z_repo_audit_log_bytes_changed", size_after - size_before)
    meta = {
        "run_at": started,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cpus": os.cpu_count(),
    }
    if args.json:
        Path(args.json).write_text(
            json.dumps({"meta": meta, "results": RESULTS}, indent=2, default=str) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
