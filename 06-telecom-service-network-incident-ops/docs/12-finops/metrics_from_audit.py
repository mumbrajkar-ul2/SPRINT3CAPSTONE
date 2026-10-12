"""FinOps metrics from the audit log. Stage S04-12 Half B.

Reads logs/audit.log, one JSON object per line, and prints the metrics from
semantic-layer/metrics.yaml that the audit row can feed. It writes nothing and
calls no model.

Run from the project root:
    .venv\\Scripts\\python.exe docs/12-finops/metrics_from_audit.py
    .venv\\Scripts\\python.exe docs/12-finops/metrics_from_audit.py --log some.log
    .venv\\Scripts\\python.exe docs/12-finops/metrics_from_audit.py --json

Honesty labels (Project_Intent.md Appendix B):
    REAL         Computed now from rows the running code wrote.
    EDUCATIONAL  Made to teach a point. Every token number here is EDUCATIONAL.

Token formula. The gateway computes `tokens` as len(prompt.split()) * 2. That is a
word count doubled. It is not a tokenizer and not a bill, so it is EDUCATIONAL. The
audit row carries the word "word_count_x2_EDUCATIONAL" in `token_estimate_method`.

Price. The only price used is the EDUCATIONAL rate from the setting
FINOPS_EDU_RATE_PER_1K (default 1.0 educational unit per 1000 tokens).
PROPOSED. Owner: Team-Force. It is not money and not a rate card.

Row kinds. The script keeps these apart so one kind cannot lower the mean of another.
    old three-key row  No `tokens` key. Written before stage S04-08. No model fields at the top level.
    model call    `model` is not null. The model was asked. `tokens` and `latency_ms` are set.
    held, no call The outcome is HOLD_FOR_REVIEW and `model` is null. No model call ran, so
                  `tokens` and `latency_ms` are null. Counted on their own line.
    no token row  An `ai.summary` row with `model` null that is not held. It was written
                  before stage S04-09 filled the five model fields.
    other         `record.read`, `policy.deny`, and old three-key rows. No model call.
"""

import argparse
import importlib.util
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from apps.api import settings

DEFAULT_LOG = ROOT / "logs" / "audit.log"

RATE_ENV = "FINOPS_EDU_RATE_PER_1K"
# EDUCATIONAL. PROPOSED. Owner: Team-Force. Not a price and not a rate card.
DEFAULT_RATE = 1.0

# metric.audit_completeness. The required-field list is PROPOSED. Owner: Team-Force.
# The metric names `policy_result`. The audit column is `policy_decision`.
# The metric names `record_id`. The audit row has no such column (log-schema.md LS-Q7).
REQUIRED_ALL = ("ts", "action", "actor", "correlation_id", "record_id")
REQUIRED_MODEL_EXTRA = ("model", "approval_id", "policy_decision")

OUTCOMES = ("RECOMMEND_ONLY", "HOLD_FOR_REVIEW", "BLOCK", "EXECUTE")


def read_rows(path):
    """Parsed rows and the count of lines that were not JSON."""
    rows, bad = [], 0
    if not Path(path).exists():
        return rows, bad
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if isinstance(value, dict):
                rows.append(value)
            else:
                bad += 1
    return rows, bad


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def percentile(sorted_values, fraction):
    """Nearest-rank percentile. `sorted_values` must not be empty."""
    rank = min(len(sorted_values), max(1, math.ceil(len(sorted_values) * fraction)))
    return sorted_values[rank - 1]


def classify(row):
    """One of: old_shape, model_call, held_no_call, no_token_row, other.

    An old three-key row (no `tokens` key) has none of the model fields at top level,
    so it is its own kind.
    """
    if "tokens" not in row:
        return "old_shape"
    if row.get("model"):
        return "model_call"
    if row.get("outcome") == "HOLD_FOR_REVIEW":
        return "held_no_call"
    if row.get("action") == "ai.summary":
        return "no_token_row"
    return "other"


def completeness(row):
    """Filled required fields over required fields for one new-shape row.

    See metric.audit_completeness. A model call (`model` not null) also needs
    `model`, `approval_id`, and `policy_decision`. The new shape has no `record_id`
    column, so that field is never filled on it.
    """
    required = list(REQUIRED_ALL)
    if row.get("model"):
        required += list(REQUIRED_MODEL_EXTRA)
    filled = sum(1 for name in required if name != "record_id" and row.get(name) not in (None, ""))
    return filled, len(required)


def compute(rows, rate):
    """All numbers in one dictionary. The printed table and the tests both read it."""
    result = {"rate_edu_units_per_1k_tokens": rate, "rows": len(rows)}

    kinds = Counter(classify(r) for r in rows)
    new_shape = [r for r in rows if "tokens" in r]
    result["row_counts"] = {
        "all": len(rows),
        "old_three_key_shape": kinds["old_shape"],
        "new_shape": len(new_shape),
        "model_call": kinds["model_call"],
        "held_no_call": kinds["held_no_call"],
        "no_token_row": kinds["no_token_row"],
        "other": kinds["other"],
    }

    calls = [r for r in rows if classify(r) == "model_call"]
    with_tokens = [r for r in calls if is_int(r.get("tokens"))]
    methods = Counter(r.get("token_estimate_method") or "(missing)" for r in with_tokens)
    result["method_counts"] = dict(methods)

    # metric.tokens_per_invocation. Model calls only. Held rows stay out of the mean.
    if with_tokens:
        tokens = [r["tokens"] for r in with_tokens]
        result["tokens_per_invocation"] = {
            "calls": len(tokens),
            "sum": sum(tokens),
            "mean": statistics.mean(tokens),
            "min": min(tokens),
            "max": max(tokens),
        }
    else:
        result["tokens_per_invocation"] = None

    # metric.cost_per_correlated_incident. Proxy: tokens per correlation_id, times the rate.
    chains = defaultdict(int)
    for r in with_tokens:
        chains[r["correlation_id"]] += r["tokens"]
    if chains:
        costs = sorted(tokens / 1000.0 * rate for tokens in chains.values())
        result["cost_per_correlation_id"] = {
            "chains": len(costs),
            "mean": statistics.mean(costs),
            "median": statistics.median(costs),
            "max": costs[-1],
            "total": sum(costs),
        }
    else:
        result["cost_per_correlation_id"] = None

    # metric.recommendation_latency. Model calls only. Held rows have null latency.
    with_latency = [r for r in calls if is_int(r.get("latency_ms"))]
    if with_latency:
        values = sorted(r["latency_ms"] for r in with_latency)
        by_outcome = {}
        for name in sorted({r.get("outcome") for r in with_latency}, key=str):
            part = sorted(r["latency_ms"] for r in with_latency if r.get("outcome") == name)
            by_outcome[str(name)] = {"calls": len(part), "median": statistics.median(part), "max": part[-1]}
        result["recommendation_latency"] = {
            "calls": len(values),
            "min": values[0],
            "median": statistics.median(values),
            "mean": statistics.mean(values),
            "p95": percentile(values, 0.95),
            "max": values[-1],
            "by_outcome": by_outcome,
        }
    else:
        result["recommendation_latency"] = None

    # metric.ai_outcome_count. Rows that carry an outcome word.
    outcome_counts = Counter(r.get("outcome") for r in rows if r.get("outcome"))
    result["ai_outcome_count"] = {name: outcome_counts.get(name, 0) for name in OUTCOMES}
    result["outcome_other_words"] = {
        k: v for k, v in outcome_counts.items() if k not in OUTCOMES
    }

    # metric.audit_completeness over rows in the new shape.
    if new_shape:
        fractions = []
        for r in new_shape:
            filled, required = completeness(r)
            fractions.append(filled / required)
        result["audit_completeness"] = {
            "rows": len(fractions),
            "mean": statistics.mean(fractions),
            "min": min(fractions),
            "max": max(fractions),
        }
    else:
        result["audit_completeness"] = None

    # Supplement. Not a metrics.yaml metric. Calls whose prompt_hash was already seen: the
    # calls a cache by prompt_hash would have saved (optimization-backlog.md OB-01).
    seen, repeats = set(), 0
    for r in with_tokens:
        key = r.get("prompt_hash")
        if not key:
            continue
        if key in seen:
            repeats += 1
        seen.add(key)
    result["repeat_prompt_calls"] = {
        "model_calls_with_hash": sum(1 for r in with_tokens if r.get("prompt_hash")),
        "distinct_hashes": len(seen),
        "repeat_calls": repeats,
        "tokens_in_repeat_calls": None,
    }
    tokens_by_hash = defaultdict(list)
    for r in with_tokens:
        if r.get("prompt_hash"):
            tokens_by_hash[r["prompt_hash"]].append(r["tokens"])
    result["repeat_prompt_calls"]["tokens_in_repeat_calls"] = sum(sum(v[1:]) for v in tokens_by_hash.values())

    # Share of rows for the other two metrics. Both have no audit source.
    result["no_audit_source"] = ["metric.quarantine_rate", "metric.retry_count"]
    return result


def fmt(value, places=1):
    return f"{value:,.{places}f}"


def render(result, log_path, bad_lines):
    rc = result["row_counts"]
    rate = result["rate_edu_units_per_1k_tokens"]
    print("S04-12 Half B  metrics_from_audit.py")
    print(f"Log file       : {log_path}")
    print(f"EDUCATIONAL rate: {rate} educational unit per 1000 tokens (setting {RATE_ENV}). PROPOSED. Owner: Team-Force. Not money.")
    print("Token formula  : len(prompt.split()) * 2, named word_count_x2_EDUCATIONAL. Every token number is EDUCATIONAL.")
    print("Rows come from test runs and demo calls on this machine unless the log was made by live traffic.")
    print()
    print("ROWS READ (label: REAL)")
    print(f"  lines not JSON                 : {bad_lines}")
    print(f"  all rows                       : {rc['all']}")
    print(f"  old three-key rows             : {rc['old_three_key_shape']}")
    print(f"  new-shape rows (has `tokens`)  : {rc['new_shape']}")
    print(f"  model-call rows                : {rc['model_call']}")
    print(f"  held rows, no model call       : {rc['held_no_call']}   (tokens null; kept out of every mean below)")
    print(f"  ai.summary rows with no tokens : {rc['no_token_row']}   (new shape, before S04-09 filled the model fields; not held; kept out of every mean)")
    print(f"  other new-shape rows (read, deny): {rc['other']}")
    if result["method_counts"]:
        print("  token_estimate_method on model-call rows: " + ", ".join(f"{k}={v}" for k, v in sorted(result["method_counts"].items())))
    print()

    header = f"{'metric id':<36} {'value':<60} {'label'}"
    print(header)
    print("-" * len(header))

    t = result["tokens_per_invocation"]
    if t:
        print(f"{'metric.tokens_per_invocation':<36} {'mean ' + fmt(t['mean']) + ' tokens over ' + str(t['calls']) + ' calls':<60} EDUCATIONAL")
        print(f"{'':<36} {'sum ' + fmt(t['sum'], 0) + ', min ' + str(t['min']) + ', max ' + str(t['max']):<60} EDUCATIONAL")
    else:
        print(f"{'metric.tokens_per_invocation':<36} {'no model-call rows with tokens: Unknown':<60} Unknown")

    c = result["cost_per_correlation_id"]
    if c:
        print(f"{'metric.cost_per_correlated_incident':<36} {'proxy: mean ' + fmt(c['mean'], 4) + ' edu units per correlation_id':<60} EDUCATIONAL")
        print(f"{'':<36} {str(c['chains']) + ' chains, median ' + fmt(c['median'], 4) + ', max ' + fmt(c['max'], 4) + ', total ' + fmt(c['total'], 4):<60} EDUCATIONAL")
        print(f"{'':<36} {'a chain is not an incident; the metric stays Unknown as defined':<60} Unknown")
    else:
        print(f"{'metric.cost_per_correlated_incident':<36} {'no model-call rows with tokens: Unknown':<60} Unknown")

    lat = result["recommendation_latency"]
    if lat:
        print(f"{'metric.recommendation_latency':<36} {'median ' + fmt(lat['median']) + ' ms, p95 ' + str(lat['p95']) + ' ms over ' + str(lat['calls']) + ' calls':<60} REAL, stub model")
        print(f"{'':<36} {'min ' + str(lat['min']) + ', mean ' + fmt(lat['mean']) + ', max ' + str(lat['max']) + ' ms':<60} REAL, stub model")
        for name, part in lat["by_outcome"].items():
            print(f"{'':<36} {'outcome ' + name + ': ' + str(part['calls']) + ' calls, median ' + fmt(part['median']) + ' ms':<60} REAL, stub model")
    else:
        print(f"{'metric.recommendation_latency':<36} {'no model-call rows with latency_ms: Unknown':<60} Unknown")

    o = result["ai_outcome_count"]
    print(f"{'metric.ai_outcome_count':<36} {', '.join(k + '=' + str(v) for k, v in o.items()):<60} REAL")
    if result["outcome_other_words"]:
        print(f"{'':<36} {'other outcome words: ' + str(result['outcome_other_words']):<60} REAL")

    a = result["audit_completeness"]
    if a:
        print(f"{'metric.audit_completeness':<36} {'mean ' + fmt(a['mean'], 3) + ' over ' + str(a['rows']) + ' new-shape rows':<60} REAL. Required list PROPOSED")
        print(f"{'':<36} {'record_id has no column, so the best row is 4 of 5':<60} gap, log-schema.md LS-Q7")
    else:
        print(f"{'metric.audit_completeness':<36} {'no new-shape rows: Unknown':<60} Unknown")

    rp = result["repeat_prompt_calls"]
    print(f"{'(supplement, not in metrics.yaml)':<36} {str(rp['repeat_calls']) + ' of ' + str(rp['model_calls_with_hash']) + ' calls repeat a prompt_hash; ' + str(rp['tokens_in_repeat_calls']) + ' tokens':<60} EDUCATIONAL")
    print(f"{'':<36} {'a cache by prompt_hash would serve those repeats (OB-01)':<60} EDUCATIONAL")
    print(f"{'metric.quarantine_rate':<36} {'NOT FROM THE AUDIT LOG':<60} gap")
    print(f"{'':<36} {'source: etl/run_daily_batch.py prints `quarantined` (S04-11)':<60} gap")
    print(f"{'':<36} {'Open question for S03: no stored place for that count':<60} gap")
    print(f"{'metric.retry_count':<36} {'NOT FROM THE AUDIT LOG':<60} gap")
    print(f"{'':<36} {'source: service_orders.csv; see cost_baseline.py section 4':<60} gap")
    print()
    print("Held rows are counted on their own line above. They have no tokens and no latency.")
    print("A mean over all rows would be lower than the mean over model calls.")


def load_rate():
    return settings.positive_number(RATE_ENV, DEFAULT_RATE)


def load_module(path=None):
    """Import this file by path. For tests, since the folder name has a hyphen."""
    target = Path(path or __file__)
    spec = importlib.util.spec_from_file_location("metrics_from_audit", target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(description="FinOps metrics from the audit log.")
    parser.add_argument("--log", default=str(DEFAULT_LOG), help="path to an audit log")
    parser.add_argument("--json", action="store_true", help="print the numbers as JSON")
    args = parser.parse_args(argv)

    rows, bad = read_rows(args.log)
    result = compute(rows, load_rate())
    result["lines_not_json"] = bad
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
    else:
        render(result, args.log, bad)
    return 0


if __name__ == "__main__":
    sys.exit(main())
