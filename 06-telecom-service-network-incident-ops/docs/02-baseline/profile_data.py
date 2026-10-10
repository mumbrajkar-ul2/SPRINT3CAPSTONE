"""Read the synthetic files and print a data profile.

This script does not change files under data/. It writes profile-output.json
next to this file. Numbers in that JSON are the counts from this run.
"""

import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data"
SYNTH = DATA / "synthetic"
OUT = Path(__file__).resolve().parent / "profile-output.json"

# PROPOSED. Owner: Unknown.
# The repo states no legal maximum for retry_count.
# This script flags a retry_count at or above 1000.
# Project_Intent.md section 4.3 names values in the thousands as the known odd case.
RETRY_COUNT_FLAG_AT = 1000

# PROPOSED. Owner: Unknown.
# The repo states no legal range for sla_breach_risk.
# This script flags a number below 0 or above 1.
SLA_RISK_LOW = 0.0
SLA_RISK_HIGH = 1.0

KEY_BY_FILE = {
    "devices.csv": "device_id",
    "circuits.csv": "circuit_id",
    "alarms.csv": "alarm_id",
    "incidents.csv": "incident_id",
    "service_orders.csv": "order_id",
    "ai_invocations.csv": "ai_call_id",
}


def load_csv(name):
    path = SYNTH / name
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_timestamp(value):
    text = value.strip()
    if text == "":
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return "unparsed"


def timestamp_columns(rows):
    found = []
    for column in rows[0].keys():
        values = [row[column].strip() for row in rows if row[column].strip() != ""]
        if not values:
            continue
        parsed = 0
        for value in values:
            if isinstance(parse_timestamp(value), datetime):
                parsed += 1
        if parsed == len(values):
            found.append(column)
    return found


def profile_csv(name, expected_rows):
    rows = load_csv(name)
    key = KEY_BY_FILE[name]
    counts = Counter(row[key] for row in rows)
    duplicates = {value: count for value, count in sorted(counts.items()) if count > 1}
    blanks = {}
    for column in rows[0].keys():
        blank_count = sum(1 for row in rows if row[column].strip() == "")
        if blank_count:
            blanks[column] = blank_count
    blank_rows = []
    for index, row in enumerate(rows, start=2):
        empty_columns = [column for column, value in row.items() if value.strip() == ""]
        if empty_columns:
            blank_rows.append(
                {"line": index, "key": row[key], "blank_columns": empty_columns}
            )
    duplicate_pairs = []
    grouped = {}
    for index, row in enumerate(rows, start=2):
        grouped.setdefault(row[key], []).append((index, row))
    for value, items in sorted(grouped.items()):
        if len(items) < 2:
            continue
        first = items[0][1]
        second = items[1][1]
        duplicate_pairs.append(
            {
                "key": value,
                "lines": [item[0] for item in items],
                "identical": first == second,
                "columns_that_differ": [
                    column for column in first if first[column] != second[column]
                ],
            }
        )
    time_cols = timestamp_columns(rows)
    odd_years = []
    year_counts = {}
    for column in time_cols:
        years = Counter()
        for index, row in enumerate(rows, start=2):
            parsed = parse_timestamp(row[column])
            if isinstance(parsed, datetime):
                years[parsed.year] += 1
                if parsed.year != 2026:
                    odd_years.append(
                        {
                            "line": index,
                            "key": row[key],
                            "column": column,
                            "value": row[column],
                            "year": parsed.year,
                        }
                    )
        year_counts[column] = {str(year): count for year, count in sorted(years.items())}
    return {
        "file": name,
        "rows": len(rows),
        "expected_rows": expected_rows,
        "row_count_matches_manifest": len(rows) == expected_rows,
        "key_column": key,
        "distinct_keys": len(counts),
        "duplicate_keys": duplicates,
        "extra_rows_from_duplicates": sum(count - 1 for count in duplicates.values()),
        "duplicate_pairs": duplicate_pairs,
        "blanks_per_column": blanks,
        "blank_rows": blank_rows,
        "timestamp_columns": time_cols,
        "timestamp_year_counts": year_counts,
        "timestamps_whose_year_is_not_2026": odd_years,
    }


def alarm_order_check(rows):
    hits = []
    for index, row in enumerate(rows, start=2):
        first = parse_timestamp(row["first_seen_at"])
        last = parse_timestamp(row["last_seen_at"])
        if isinstance(first, datetime) and isinstance(last, datetime) and last < first:
            hits.append(
                {
                    "line": index,
                    "alarm_id": row["alarm_id"],
                    "first_seen_at": row["first_seen_at"],
                    "last_seen_at": row["last_seen_at"],
                }
            )
    examples = hits[:3]
    named = [hit for hit in hits if hit["alarm_id"] == "ALA-00002"]
    for hit in named:
        if hit not in examples:
            examples.append(hit)
    return {"count": len(hits), "examples": examples}


def retry_check(rows):
    values = []
    blank = 0
    non_numeric = []
    for index, row in enumerate(rows, start=2):
        text = row["retry_count"].strip()
        if text == "":
            blank += 1
            continue
        try:
            values.append((index, row["order_id"], int(text)))
        except ValueError:
            non_numeric.append({"line": index, "order_id": row["order_id"], "value": text})
    flagged = [item for item in values if item[2] >= RETRY_COUNT_FLAG_AT]
    below = [item for item in values if item[2] < RETRY_COUNT_FLAG_AT]
    return {
        "bound": RETRY_COUNT_FLAG_AT,
        "bound_status": "PROPOSED",
        "bound_owner": "Unknown",
        "numeric_rows": len(values),
        "blank_rows": blank,
        "non_numeric": non_numeric,
        "minimum": min(item[2] for item in values) if values else None,
        "maximum": max(item[2] for item in values) if values else None,
        "at_or_above_bound": len(flagged),
        "below_bound": len(below),
        "below_bound_examples": [
            {"line": item[0], "order_id": item[1], "retry_count": item[2]}
            for item in sorted(below, key=lambda item: item[2])[:5]
        ],
    }


def severity_check(rows):
    counts = Counter(row["severity"] for row in rows)
    values = sorted(counts)
    return {
        "distinct_values": values,
        "counts": dict(counts),
        "includes_gold": "gold" in counts,
        "includes_bronze": "bronze" in counts,
        "gold_rows": counts.get("gold", 0),
        "bronze_rows": counts.get("bronze", 0),
    }


def ai_call_id_check(rows):
    malformed = []
    other = []
    for index, row in enumerate(rows, start=2):
        value = row["ai_call_id"]
        if value.startswith("AI_-"):
            malformed.append({"line": index, "ai_call_id": value})
        else:
            other.append({"line": index, "ai_call_id": value})
    bad_token = [item for item in malformed if item["ai_call_id"] == "AI_-BAD1"]
    like_example = [item for item in malformed if item["ai_call_id"] == "AI_-00002"]
    return {
        "rule": "A value is malformed when it starts with AI_-",
        "malformed_count": len(malformed),
        "other_ids": other,
        "includes_AI_-00002": len(like_example) == 1,
        "includes_AI_-BAD1": len(bad_token) == 1,
        "well_formed_AI_dash_digits": sum(
            1
            for row in rows
            if row["ai_call_id"].startswith("AI-") and not row["ai_call_id"].startswith("AI_-")
        ),
    }


def sla_risk_check(rows):
    outside = []
    inside = 0
    blank = 0
    for index, row in enumerate(rows, start=2):
        text = row["sla_breach_risk"].strip()
        if text == "":
            blank += 1
            continue
        number = float(text)
        if number < SLA_RISK_LOW or number > SLA_RISK_HIGH:
            outside.append(
                {
                    "line": index,
                    "incident_id": row["incident_id"],
                    "sla_breach_risk": text,
                }
            )
        else:
            inside += 1
    return {
        "range_low": SLA_RISK_LOW,
        "range_high": SLA_RISK_HIGH,
        "range_status": "PROPOSED",
        "range_owner": "Unknown",
        "inside_range": inside,
        "blank": blank,
        "outside_range": outside,
    }


def recommendation_risk_check(rows):
    numeric = []
    words = Counter()
    for index, row in enumerate(rows, start=2):
        text = row["recommendation_risk"].strip()
        if text == "":
            words["<blank>"] += 1
            continue
        try:
            float(text)
        except ValueError:
            words[text] += 1
        else:
            numeric.append(
                {
                    "line": index,
                    "ai_call_id": row["ai_call_id"],
                    "recommendation_risk": text,
                }
            )
    return {"numeric_cells": numeric, "word_counts": dict(words)}


def events_check():
    path = SYNTH / "events.jsonl"
    null_count = 0
    blank_count = 0
    filled_count = 0
    bad_json = 0
    lines = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip() == "":
                continue
            lines += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                bad_json += 1
                continue
            correlation = item.get("correlation_id", "<missing key>")
            if correlation is None:
                null_count += 1
            elif isinstance(correlation, str) and correlation.strip() == "":
                blank_count += 1
            else:
                filled_count += 1
    return {
        "lines": lines,
        "bad_json": bad_json,
        "correlation_id_null": null_count,
        "correlation_id_blank": blank_count,
        "correlation_id_null_or_blank": null_count + blank_count,
        "correlation_id_filled": filled_count,
    }


def confirm_quality(profiles, alarms, retries, sla, recommendation):
    by_file = {item["file"]: item for item in profiles}
    entity_file = {
        "devices": "devices.csv",
        "circuits": "circuits.csv",
        "alarms": "alarms.csv",
        "incidents": "incidents.csv",
        "service_orders": "service_orders.csv",
        "ai_invocations": "ai_invocations.csv",
    }
    issues = json.loads((DATA / "quality_issues.json").read_text(encoding="utf-8"))
    results = []
    for entity, labels in issues["seeded_issues"].items():
        profile = by_file[entity_file[entity]]
        for label in labels:
            if label == "duplicate business key":
                status = "Confirmed" if profile["duplicate_keys"] else "Not found"
                evidence = (
                    f"{profile['extra_rows_from_duplicates']} extra rows. "
                    f"Keys: {profile['duplicate_keys']}."
                )
            elif label == "blank mandatory fields":
                status = "Confirmed" if profile["blank_rows"] else "Not found"
                evidence = (
                    "Blank cells are on these rows: "
                    + json.dumps(profile["blank_rows"])
                    + ". The repo does not name which columns are mandatory. "
                    "This mark treats a blank cell as the seeded blank."
                )
            elif label == "impossible timestamp":
                odd = profile["timestamps_whose_year_is_not_2026"]
                order_note = ""
                if entity == "alarms" and alarms["count"]:
                    order_note = (
                        f" Also {alarms['count']} alarms have last_seen_at before first_seen_at."
                    )
                if odd or (entity == "alarms" and alarms["count"]):
                    status = "Confirmed"
                    evidence = f"Timestamp columns: {profile['timestamp_columns']}. Year is not 2026: {odd}.{order_note}"
                elif not profile["timestamp_columns"]:
                    status = "Not found"
                    evidence = (
                        "No column in this file is a full set of date-time values. "
                        f"Columns: {list(load_csv(entity_file[entity])[0].keys())}."
                    )
                else:
                    status = "Not found"
                    evidence = (
                        f"Timestamp columns {profile['timestamp_columns']} are all year 2026, "
                        "and this file has no last-before-first pair."
                    )
            elif label == "out-of-range score or risk marker":
                if entity == "incidents":
                    status = "Confirmed" if sla["outside_range"] else "Not found"
                    evidence = (
                        "PROPOSED range 0 to 1 inclusive. Owner: Unknown. "
                        f"Outside that range: {sla['outside_range']}. "
                        f"Inside: {sla['inside_range']}."
                    )
                elif entity == "service_orders":
                    status = "Confirmed" if retries["at_or_above_bound"] else "Not found"
                    evidence = (
                        f"PROPOSED bound retry_count >= {RETRY_COUNT_FLAG_AT}. Owner: Unknown. "
                        f"At or above the bound: {retries['at_or_above_bound']}. "
                        f"Below the bound: {retries['below_bound']}. "
                        f"Minimum {retries['minimum']}. Maximum {retries['maximum']}."
                    )
                elif entity == "ai_invocations":
                    status = "Confirmed" if recommendation["numeric_cells"] else "Not found"
                    evidence = (
                        "recommendation_risk holds words on the other rows. "
                        f"Numeric cells: {recommendation['numeric_cells']}."
                    )
                else:
                    status = "Not found"
                    evidence = (
                        "This file has no sla_breach_risk, retry_count, or recommendation_risk column. "
                        "No numeric cutoff was applied to the other columns. "
                        f"Columns: {list(load_csv(entity_file[entity])[0].keys())}."
                    )
            else:
                status = "Not found"
                evidence = "This script has no check for that label."
            results.append(
                {"entity": entity, "item": label, "mark": status, "evidence": evidence}
            )
    return results


def main():
    manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
    profiles = [
        profile_csv(name, expected)
        for name, expected in manifest["csv_files"].items()
    ]
    alarms = alarm_order_check(load_csv("alarms.csv"))
    retries = retry_check(load_csv("service_orders.csv"))
    severity = severity_check(load_csv("incidents.csv"))
    alarm_severity = severity_check(load_csv("alarms.csv"))
    call_ids = ai_call_id_check(load_csv("ai_invocations.csv"))
    sla = sla_risk_check(load_csv("incidents.csv"))
    recommendation = recommendation_risk_check(load_csv("ai_invocations.csv"))
    events = events_check()
    quality = confirm_quality(profiles, alarms, retries, sla, recommendation)
    report = {
        "source": "docs/02-baseline/profile_data.py",
        "numbers_are": "REAL counts from this run",
        "files": profiles,
        "alarms_last_seen_before_first_seen": alarms,
        "service_orders_retry_count": retries,
        "incidents_severity": severity,
        "alarms_severity": alarm_severity,
        "ai_call_id": call_ids,
        "incidents_sla_breach_risk": sla,
        "ai_recommendation_risk": recommendation,
        "events": events,
        "quality_issues": quality,
        "manifest_jsonl_events": manifest["jsonl_events"],
        "events_line_count_matches_manifest": events["lines"] == manifest["jsonl_events"],
    }
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"numbers are REAL counts from this run")
    for item in profiles:
        print(
            f"{item['file']}: rows {item['rows']} expected {item['expected_rows']} "
            f"match {item['row_count_matches_manifest']} "
            f"duplicate_keys {item['duplicate_keys']} "
            f"blank_rows {len(item['blank_rows'])}"
        )
    print(
        f"alarms last before first: {alarms['count']}"
    )
    print(
        f"retry_count >= {RETRY_COUNT_FLAG_AT} (PROPOSED, owner Unknown): "
        f"{retries['at_or_above_bound']} of {retries['numeric_rows']} "
        f"min {retries['minimum']} max {retries['maximum']}"
    )
    print(f"incident severity: {severity['counts']}")
    print(f"malformed ai_call_id (starts with AI_-): {call_ids['malformed_count']}")
    print(
        "events correlation_id null "
        f"{events['correlation_id_null']} blank {events['correlation_id_blank']} "
        f"filled {events['correlation_id_filled']}"
    )
    confirmed = sum(1 for item in quality if item["mark"] == "Confirmed")
    missing = sum(1 for item in quality if item["mark"] == "Not found")
    print(f"quality_issues Confirmed {confirmed} Not found {missing}")
    for item in quality:
        if item["mark"] == "Not found":
            print(f"Not found: {item['entity']} / {item['item']}")


if __name__ == "__main__":
    main()
