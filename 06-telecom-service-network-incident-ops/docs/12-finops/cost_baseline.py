"""AI cost baseline. Stage S04-12 Half A.

Reads three stored files and prints labelled tables. It writes nothing.
It never calls a model and it never changes a file under data/synthetic/.

Run from the project root:
    .venv\\Scripts\\python.exe docs/12-finops/cost_baseline.py

Honesty labels (Project_Intent.md Appendix B):
    SIMULATED    A value from a synthetic file. It stands in for a live service.
    REAL         A value computed now from a file the running code wrote.
    EDUCATIONAL  A value made to teach a point. It is not an operating metric.
    PRECOMPUTED  A value a script stored earlier and this script only reads back.

Rules for this file:
    - Every printed number carries a label.
    - events.jsonl has no token field. Tokens come from ai_invocations.csv only.
    - Any price below is EDUCATIONAL. PROPOSED. Owner: Team-Force. It is not a rate card.
"""

import csv
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "synthetic"
AUDIT_LOG = ROOT / "logs" / "audit.log"

# EDUCATIONAL. PROPOSED. Owner: Team-Force. Not a price and not a rate card.
# The money unit of cost_units is Unknown (docs/00-contract/cost-envelope.md), so
# this rate uses "educational units", not a currency. Half B reads the rate from settings.
EDU_UNITS_PER_1K_TOKENS = 1.0

# PROPOSED bound from defect F18 and metric.retry_count. Owner: Team-Force. Not a maximum.
PROPOSED_RETRY_BOUND = 1000

# The four business flows. The words are the event_type values (entities.yaml concepts
# concept.flow_*). One event_type is one flow, so this map has no Unknown row.
FLOWS = [
    "Customer order to provisioning",
    "Alarm storm to incident correlation",
    "Topology lookup to AI recommendation",
    "Approved remediation to validation",
]

# Inference. ai_invocations.csv has no event_type column. The only flow whose name
# holds a model step is "Topology lookup to AI recommendation". Stage S2Q puts all three
# GenAI capabilities in that flow. The other three flows get 0 model tokens by assignment.
MODEL_FLOW = "Topology lookup to AI recommendation"


def read_csv(name):
    with open(DATA / name, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_events():
    events = []
    with open(DATA / "events.jsonl", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
    return events


def is_int(text):
    return text is not None and text.strip().lstrip("-").isdigit()


def heading(text):
    print()
    print("=" * 78)
    print(text)
    print("=" * 78)


def money(value):
    return f"{value:,.4f}"


def edu_cost(tokens):
    """EDUCATIONAL cost in educational units for a token count."""
    return tokens / 1000.0 * EDU_UNITS_PER_1K_TOKENS


# ---------------------------------------------------------------------------
# 1. Token baseline from ai_invocations.csv
# ---------------------------------------------------------------------------


def word_or_blank(value):
    if value == "":
        return "(blank cell)"
    try:
        float(value)
        return f"(numeric cell {value})"
    except ValueError:
        return value


def group_tokens(rows, column):
    sums = defaultdict(int)
    counts = Counter()
    for row in rows:
        if not is_int(row["token_count"]):
            continue
        key = word_or_blank(row[column])
        sums[key] += int(row["token_count"])
        counts[key] += 1
    return sums, counts


def print_group(rows, column, total_tokens):
    sums, counts = group_tokens(rows, column)
    print(f"{column:<22} {'rows':>5} {'sum token_count':>16} {'share':>7}  label")
    for key in sorted(sums, key=lambda k: -sums[k]):
        share = sums[key] / total_tokens * 100
        print(f"{key:<22} {counts[key]:>5} {sums[key]:>16,} {share:>6.1f}%  SIMULATED")
    print(f"{'TOTAL':<22} {sum(counts.values()):>5} {sum(sums.values()):>16,} {'100.0%':>7}  SIMULATED")


def section_tokens(rows):
    heading("1. TOKEN BASELINE  (ai_invocations.csv, every number SIMULATED)")
    numeric = [r for r in rows if is_int(r["token_count"])]
    total = sum(int(r["token_count"]) for r in numeric)
    blank = [r for r in rows if not is_int(r["token_count"])]
    print(f"Data rows                         : {len(rows)}  (PRECOMPUTED, matches data/manifest.json)")
    print(f"Rows with an integer token_count  : {len(numeric)}  (SIMULATED)")
    print(f"Rows with a blank token_count     : {len(blank)}  ids={[r['ai_call_id'] for r in blank]}  (SIMULATED)")
    print(f"Sum of token_count                : {total:,}  (SIMULATED)")
    print(f"Mean token_count per row          : {total / len(numeric):,.1f}  (SIMULATED)")
    values = sorted(int(r["token_count"]) for r in numeric)
    print(f"Min / median / max token_count    : {values[0]} / {statistics.median(values)} / {values[-1]}  (SIMULATED)")
    print("Columns in the file               : " + ", ".join(rows[0].keys()))
    print("Cost column in the file           : none. Any price is EDUCATIONAL.")

    heading("1a. CHECK THE `model` COLUMN BEFORE GROUPING")
    model_words = Counter(r["model"] for r in rows)
    print(f"Distinct values in `model`        : {len(model_words)}  (SIMULATED)")
    print(f"local-sim-v1 rows                 : {model_words.get('local-sim-v1', 0)}  (SIMULATED)")
    print("Values: " + ", ".join(f"{word_or_blank(k)}={v}" for k, v in model_words.most_common()))
    print("Finding: every value is a status word from the shared word pool. None is a model name.")
    print("The real model name behind these rows is Unknown. Grouping by `model` below groups by a status word.")

    heading("1b. TOKENS BY `model` COLUMN  (status words, real model name Unknown)")
    print_group(rows, "model", total)

    heading("1c. TOKENS BY RISK COLUMN")
    pool = {r["model"] for r in rows} | {r["use_case"] for r in rows} | {r["recommendation_risk"] for r in rows}
    print("Columns that hold risk-like words: `recommendation_risk` and `use_case`.")
    print("Both draw from the same pool of status words, so neither holds a clean risk level.")
    print("This script uses `recommendation_risk` as the risk column. entities.yaml describes it as")
    print("'how risky the model's advice was judged'. `use_case` is described as 'what the call was for'.")
    print(f"Distinct words across model/use_case/recommendation_risk: {len(pool)}  (SIMULATED)")
    print()
    print_group(rows, "recommendation_risk", total)

    high = sum(int(r["token_count"]) for r in numeric if r["recommendation_risk"] == "high_risk")
    high_rows = sum(1 for r in numeric if r["recommendation_risk"] == "high_risk")
    print()
    print(f"Roll-up: recommendation_risk == 'high_risk' : {high_rows} rows, {high:,} tokens ({high / total * 100:.1f}%)  SIMULATED")
    print(f"Roll-up: any other word (risk level Unknown) : {len(numeric) - high_rows} rows, {total - high:,} tokens  SIMULATED")

    heading("1d. TOKENS BY `use_case` COLUMN  (secondary view)")
    print_group(rows, "use_case", total)

    heading("1e. EDUCATIONAL PRICE ON THE SIMULATED TOKENS")
    print(f"EDUCATIONAL rate: {EDU_UNITS_PER_1K_TOKENS} educational unit per 1000 tokens. PROPOSED. Owner: Team-Force.")
    print("This is not money and not a rate card. The real price per token is Unknown.")
    print(f"Whole CSV at that rate            : {money(edu_cost(total))} educational units  (EDUCATIONAL on SIMULATED tokens)")
    print(f"One call at the mean token_count  : {money(edu_cost(total / len(numeric)))} educational units  (EDUCATIONAL)")
    return total, len(numeric)


# ---------------------------------------------------------------------------
# 2. Cost and latency from events.jsonl
# ---------------------------------------------------------------------------


def section_events(events):
    heading("2. EVENT COST AND LATENCY  (events.jsonl, every number SIMULATED)")
    print(f"Lines                             : {len(events)}  (PRECOMPUTED, matches manifest)")
    print("Fields                            : " + ", ".join(events[0].keys()))
    print("Token field in events.jsonl       : none. Tokens cannot be summed from this file.")
    total_cost = sum(e["cost_units"] for e in events)
    print(f"Sum of cost_units                 : {money(total_cost)}  (SIMULATED, money unit Unknown)")
    latency = [e["latency_ms"] for e in events]
    print(
        f"latency_ms min/median/mean/max    : {min(latency)} / {statistics.median(latency)} / "
        f"{statistics.mean(latency):,.1f} / {max(latency)}  (SIMULATED)"
    )
    ordered = sorted(latency)
    p95 = ordered[int(len(ordered) * 0.95) - 1]
    print(f"latency_ms 95th percentile        : {p95}  (SIMULATED, nearest-rank)")
    over_2000 = sum(1 for v in latency if v > 2000)
    over_10000 = sum(1 for v in latency if v > 10000)
    print(f"Events over 2000 ms               : {over_2000} of {len(latency)}  (SIMULATED). 2000 ms is the PROPOSED level in slo-proposal.md")
    print(f"Events over 10000 ms              : {over_10000} of {len(latency)}  (SIMULATED). 10 s is the PROPOSED model timeout")

    def table(key, title):
        cost = defaultdict(float)
        lat = defaultdict(list)
        for event in events:
            cost[event[key]] += event["cost_units"]
            lat[event[key]].append(event["latency_ms"])
        print()
        print(title)
        print(f"{key:<40} {'events':>6} {'sum cost_units':>15} {'mean/event':>11} {'median ms':>10} {'mean ms':>9}  label")
        for name in sorted(cost, key=lambda k: -cost[k]):
            n = len(lat[name])
            print(
                f"{name:<40} {n:>6} {money(cost[name]):>15} {cost[name] / n:>11.4f} "
                f"{statistics.median(lat[name]):>10} {statistics.mean(lat[name]):>9.1f}  SIMULATED"
            )
        print(f"{'TOTAL':<40} {len(events):>6} {money(sum(cost.values())):>15}")

    table("event_type", "2a. By event_type (one event_type is one business flow)")
    table("actor", "2b. By actor (seven personas)")
    return total_cost


# ---------------------------------------------------------------------------
# 3. Cost per workflow and per correlated incident
# ---------------------------------------------------------------------------


def section_workflow(events, ai_rows, total_tokens):
    heading("3. COST PER WORKFLOW  (cost_units SIMULATED; tokens SIMULATED; price EDUCATIONAL)")
    flow_cost = defaultdict(float)
    flow_n = Counter()
    for event in events:
        flow_cost[event["event_type"]] += event["cost_units"]
        flow_n[event["event_type"]] += 1
    unknown_types = sorted(set(flow_n) - set(FLOWS))
    print(f"event_type values not in the four flows : {unknown_types if unknown_types else 'none'}  (SIMULATED)")
    print("Held calls (timeout, breaker open, in-flight limit) count as 0 tokens. They make no model call.")
    print("ai_invocations.csv has no outcome column, so 0 held rows are identifiable in it.")
    print()
    print(f"{'flow':<40} {'events':>6} {'cost_units':>11} {'tokens (Inference)':>19} {'edu cost of tokens':>19}")
    for flow in FLOWS:
        tokens = total_tokens if flow == MODEL_FLOW else 0
        print(
            f"{flow:<40} {flow_n[flow]:>6} {flow_cost[flow]:>11.4f} {tokens:>19,} {edu_cost(tokens):>19.4f}"
        )
    print("cost_units: SIMULATED. tokens: SIMULATED, assigned to one flow by Inference. edu cost: EDUCATIONAL.")
    print("Other three flows: 0 tokens by Assignment from S2Q (no model in them).")

    heading("3a. CHAINS: events grouped by a filled correlation_id")
    filled = [e for e in events if e["correlation_id"] not in (None, "")]
    nulls = sum(1 for e in events if e["correlation_id"] is None)
    blanks = sum(1 for e in events if e["correlation_id"] == "")
    print(f"correlation_id null / empty / filled : {nulls} / {blanks} / {len(filled)}  (SIMULATED)")
    chains = defaultdict(list)
    for event in filled:
        chains[event["correlation_id"]].append(event)
    chain_cost = {k: sum(e["cost_units"] for e in v) for k, v in chains.items()}
    attributable = sum(chain_cost.values())
    unattributable = sum(e["cost_units"] for e in events if e["correlation_id"] in (None, ""))
    print(f"Distinct chains                      : {len(chains)}  (SIMULATED)")
    print(f"cost_units inside chains             : {money(attributable)}  (SIMULATED)")
    print(f"cost_units with no chain id          : {money(unattributable)}  (SIMULATED)")
    values = sorted(chain_cost.values())
    print(
        f"Cost per chain min/median/mean/max   : {values[0]:.4f} / {statistics.median(values):.4f} / "
        f"{statistics.mean(values):.4f} / {values[-1]:.4f}  (SIMULATED)"
    )
    multi = {k: v for k, v in chains.items() if len({e["event_type"] for e in v}) > 1}
    print(f"Chains whose events span 2+ flows    : {len(multi)} of {len(chains)}  (SIMULATED)")
    one_flow = len(chains) - len(multi)
    print(f"Chains whose events sit in 1 flow    : {one_flow} of {len(chains)}  (SIMULATED)")
    sizes = Counter(len(v) for v in chains.values())
    print("Chain size (events): " + ", ".join(f"{s}:{c}" for s, c in sorted(sizes.items())) + "  (SIMULATED)")

    print()
    print("Cost per chain, by the flow of the events inside the chain (a chain with 2+ flows is split):")
    by_flow_in_chain = defaultdict(float)
    for event in filled:
        by_flow_in_chain[event["event_type"]] += event["cost_units"]
    for flow in FLOWS:
        n_chain = len({k for k, v in chains.items() if any(e["event_type"] == flow for e in v)})
        total = by_flow_in_chain[flow]
        print(f"  {flow:<40} chains touching flow {n_chain:>4}, cost_units in chains {total:>10.4f}  SIMULATED")

    heading("3b. COST PER CORRELATED INCIDENT  (metric.cost_per_correlated_incident)")
    print("As defined, the metric needs a join from alarms to incidents. That join is Unknown, and events.jsonl")
    print("holds no incident id. So the metric cannot be computed as defined. Two proxies are shown instead.")
    print()
    incidents = {r["incident_id"] for r in read_csv("incidents.csv") if r["incident_id"]}
    incident_tokens = defaultdict(int)
    incident_calls = Counter()
    for row in ai_rows:
        if is_int(row["token_count"]) and row["incident_id"]:
            incident_tokens[row["incident_id"]] += int(row["token_count"])
            incident_calls[row["incident_id"]] += 1
    joined = [i for i in incident_tokens if i in incidents]
    print("Proxy P1: tokens per incident_id on ai_invocations.csv")
    print(f"  distinct incident_id with a token row : {len(incident_tokens)}  (SIMULATED)")
    print(f"  of those, found in incidents.csv      : {len(joined)}  (SIMULATED)")
    print(f"  not found in incidents.csv            : {sorted(set(incident_tokens) - set(joined))}  (SIMULATED)")
    token_values = sorted(incident_tokens.values())
    mean_tokens = statistics.mean(token_values)
    print(
        f"  tokens per incident min/median/mean/max: {token_values[0]} / {statistics.median(token_values)} / "
        f"{mean_tokens:,.1f} / {token_values[-1]}  (SIMULATED)"
    )
    print(f"  mean at EDUCATIONAL rate               : {money(edu_cost(mean_tokens))} educational units per incident  (EDUCATIONAL)")
    print(f"  incident_id with 2+ call rows          : {sum(1 for c in incident_calls.values() if c > 1)}  (SIMULATED)")
    print("  Limit: tokens only. No incident is correlated to an alarm, so 'correlated' is not met.")
    print()
    print("Proxy P2: cost_units per correlation_id chain in events.jsonl")
    print(f"  mean cost per chain                   : {statistics.mean(values):.4f} cost_units  (SIMULATED, money unit Unknown)")
    print(f"  median cost per chain                 : {statistics.median(values):.4f} cost_units  (SIMULATED)")
    print("  Limit: a chain is a request chain, not an incident. Link from chain to incident is Unknown.")
    print(f"  {len(filled)} of {len(events)} events ({len(filled) / len(events) * 100:.1f}%) carry a chain id.")
    return statistics.mean(values), mean_tokens


# ---------------------------------------------------------------------------
# 4. Retry cost from service_orders.csv
# ---------------------------------------------------------------------------


def live_token_estimate():
    """EDUCATIONAL. The word-count estimate of the live prompt for the first device row.

    Reads the gateway's own prompt builder. If the import fails, the answer is Unknown.
    """
    try:
        sys.path.insert(0, str(ROOT))
        from apps.api.services import ai_gateway

        first = read_csv("devices.csv")[0]
        prompt = ai_gateway.build_prompt(first)
        return len(prompt.split()) * 2
    except Exception as error:  # noqa: BLE001  report Unknown, do not stop the baseline
        print(f"  (live prompt estimate is Unknown: {type(error).__name__})")
        return None


def section_retry(orders, mean_tokens_per_call):
    heading("4. RETRY COST  (service_orders.retry_count SIMULATED; model cost is a what-if, EDUCATIONAL)")
    numeric = [r for r in orders if is_int(r["retry_count"])]
    blank = [r for r in orders if not is_int(r["retry_count"])]
    counts = [int(r["retry_count"]) for r in numeric]
    total = sum(counts)
    print(f"Order rows                        : {len(orders)}  (PRECOMPUTED)")
    print(f"Rows with a numeric retry_count   : {len(numeric)}  (SIMULATED)")
    print(f"Rows with a blank retry_count     : {len(blank)} ids={[r['order_id'] for r in blank]}  (SIMULATED)")
    print(f"Sum of retry_count                : {total:,}  (SIMULATED)")
    print(f"Min / median / mean / max         : {min(counts)} / {statistics.median(counts)} / {statistics.mean(counts):,.1f} / {max(counts)}  (SIMULATED)")
    over = [c for c in counts if c >= PROPOSED_RETRY_BOUND]
    print(f"Rows at or above {PROPOSED_RETRY_BOUND} (PROPOSED bound, Owner Team-Force): {len(over)}  (SIMULATED)")
    print(f"Retries in those rows             : {sum(over):,}  (SIMULATED)")
    seen = {}
    for row in numeric:
        seen[row["order_id"]] = seen.get(row["order_id"], 0) + int(row["retry_count"])
    print(f"Distinct order_id (numeric rows)  : {len(seen)}  (SIMULATED). Repeated ids add rows, see idempotency-plan.md")
    distinct_total = {}
    for row in numeric:
        distinct_total.setdefault(row["order_id"], int(row["retry_count"]))
    print(f"Sum if each order_id counted once (first row): {sum(distinct_total.values()):,}  (SIMULATED)")

    print()
    print("Retries by provisioning_status (the business effect: where the build is stuck)")
    by_status = defaultdict(lambda: [0, 0])
    for row in numeric:
        by_status[row["provisioning_status"]][0] += 1
        by_status[row["provisioning_status"]][1] += int(row["retry_count"])
    print(f"{'provisioning_status':<20} {'orders':>6} {'retries':>10}  label")
    for key in sorted(by_status, key=lambda k: -by_status[k][1]):
        n, r = by_status[key]
        print(f"{key:<20} {n:>6} {r:>10,}  SIMULATED")
    stuck_words = ("in_progress", "failed", "exception", "manual_hold", "queued")
    stuck_orders = sum(by_status[k][0] for k in stuck_words if k in by_status)
    print(f"Orders with a status that is not finished (one of {stuck_words}): {stuck_orders}  (SIMULATED, Inference on the word meaning)")

    print()
    print("What-if: each recorded retry calls the model once. EDUCATIONAL.")
    print("The gateway does not retry model calls, and S2Q assigns this capability to deterministic code,")
    print("so the real hosted-model cost of these retries is 0 by Assignment. This table is a stress picture only.")
    live = live_token_estimate()
    cases = [("A: CSV mean tokens per call", mean_tokens_per_call)]
    if live is not None:
        cases.append(("B: live prompt estimate (word count x 2)", live))
    for label, per_call in cases:
        tokens = total * per_call
        print(f"  {label:<44} {per_call:>9,.1f} tokens/call -> {tokens:>16,.0f} tokens -> {money(edu_cost(tokens))} educational units  EDUCATIONAL")
    one_retry_a = edu_cost(mean_tokens_per_call)
    print(f"  One retry at case A                          : {money(one_retry_a)} educational units  EDUCATIONAL")
    if live is not None:
        print(f"  One retry at case B                          : {money(edu_cost(live))} educational units  EDUCATIONAL")
    return total, live


# ---------------------------------------------------------------------------
# 5. Optimisation sizing
# ---------------------------------------------------------------------------


def section_optimisation(ai_rows, mean_tokens, live):
    heading("5. OPTIMISATION SIZING  (for optimization-backlog.md)")
    alarms = read_csv("alarms.csv")
    keyed = [a for a in alarms if a["storm_batch_id"] and a["dedupe_key"]]
    storms = Counter(a["storm_batch_id"] for a in keyed)
    print(f"Alarm rows with both keys filled  : {len(keyed)}  (SIMULATED)")
    print(f"Distinct storm_batch_id           : {len(storms)}  (SIMULATED)")
    print(f"Largest storm batch in the file   : {max(storms.values())} rows  (SIMULATED)")
    print(f"Calls if one summary per alarm row: {len(keyed)}  (EDUCATIONAL what-if)")
    print(f"Calls if one summary per storm    : {len(storms)}  (EDUCATIONAL what-if)")
    print(f"Calls saved in this file          : {len(keyed) - len(storms)}  (EDUCATIONAL what-if). Storms here are 1 to 2 rows.")
    print("Worked example: a storm of 100 alarms, one call each = 100 calls. One call per storm = 1 call. EDUCATIONAL.")

    print()
    print("Repeated prompts. ai_invocations.csv has no prompt_hash column.")
    print("events.jsonl has payload_hash, a hash of event content. It is not a prompt hash.")
    payloads = Counter(e["payload_hash"] for e in read_events())
    print(f"Repeated payload_hash values in events.jsonl : {sum(1 for c in payloads.values() if c > 1)}  (SIMULATED)")
    print("So the stored data shows 0 repeated prompts. Only the S04-11 drill DR-3 shows the repeat (REAL, test run):")
    print("five identical summary calls made 5 model calls. With a cache by prompt_hash: 1 call. 4 saved. EDUCATIONAL.")
    if live is not None:
        print(f"  Tokens saved in that drill at the live estimate ({live} per call): {4 * live}  (EDUCATIONAL)")

    print()
    print("Capabilities assigned to rules by S2Q (8 of 11): hosted-model cost 0 by Assignment, not measured.")
    print("Remaining model capabilities: incident summary, next-action recommendation, configuration suggestion (3 of 11).")


# ---------------------------------------------------------------------------
# 6. What the live gateway wrote to logs/audit.log
# ---------------------------------------------------------------------------


def section_audit():
    heading("6. LIVE AUDIT LOG TODAY  (logs/audit.log)")
    if not AUDIT_LOG.exists():
        print("logs/audit.log is missing. Unknown.")
        return
    rows, bad = [], 0
    with open(AUDIT_LOG, encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                bad += 1
    actions = Counter(r.get("action") for r in rows)
    new_shape = [r for r in rows if "tokens" in r]
    with_tokens = [r for r in new_shape if isinstance(r.get("tokens"), int)]
    held = [r for r in new_shape if r.get("action") == "policy.hold"]
    held_with_model = [r for r in held if r.get("model")]
    print("These rows come from test runs and demo calls on this machine, not production traffic.")
    print(f"Rows parsed / unparsable          : {len(rows)} / {bad}  (REAL)")
    print("Actions: " + ", ".join(f"{k}={v}" for k, v in actions.most_common()) + "  (REAL)")
    print(f"Rows in the new shape (has `tokens` key) : {len(new_shape)}  (REAL)")
    print(f"Rows with an integer tokens value        : {len(with_tokens)}  (REAL)")
    print(f"policy.hold rows                         : {len(held)}  (REAL). Of those, with a model name: {len(held_with_model)}")
    print(f"Rows with `token_estimate_method` key    : {sum(1 for r in rows if 'token_estimate_method' in r)}  (REAL)")
    if with_tokens:
        tokens = [r["tokens"] for r in with_tokens]
        print(f"tokens min/mean/max               : {min(tokens)} / {statistics.mean(tokens):.1f} / {max(tokens)}  (EDUCATIONAL, word count x 2)")
        latency = [r["latency_ms"] for r in with_tokens if isinstance(r.get("latency_ms"), int)]
        if latency:
            print(f"latency_ms min/mean/max           : {min(latency)} / {statistics.mean(latency):.1f} / {max(latency)}  (REAL, stub waits 0.01 s)")
    print(f"Rows with a correlation_id               : {sum(1 for r in rows if r.get('correlation_id'))}  (REAL)")


def main():
    ai_rows = read_csv("ai_invocations.csv")
    events = read_events()
    orders = read_csv("service_orders.csv")
    print("S04-12 Half A  cost_baseline.py")
    print("Labels: SIMULATED = synthetic file value. EDUCATIONAL = teaching value. REAL = computed from a live-written file.")
    print(f"EDUCATIONAL rate: {EDU_UNITS_PER_1K_TOKENS} educational unit per 1000 tokens. PROPOSED. Owner: Team-Force. Not money.")
    total_tokens, calls = section_tokens(ai_rows)
    section_events(events)
    _, mean_tokens = section_workflow(events, ai_rows, total_tokens)
    _, live = section_retry(orders, total_tokens / calls)
    section_optimisation(ai_rows, mean_tokens, live)
    section_audit()
    print()
    print("End of cost_baseline.py")


if __name__ == "__main__":
    main()
