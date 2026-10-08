# Synthetic Data

Domain: Telecommunications: Service Provisioning, Network & Incident Operations

This data is fully synthetic and designed for realistic workshop discovery. It includes enough volume for baseline profiling, ETL validation, event-correlation exercises, observability design, AI FinOps analysis, and data-quality remediation.

## Included Files

- `synthetic/devices.csv`: 354 rows
- `synthetic/circuits.csv`: 354 rows
- `synthetic/alarms.csv`: 354 rows
- `synthetic/incidents.csv`: 354 rows
- `synthetic/service_orders.csv`: 354 rows
- `synthetic/ai_invocations.csv`: 354 rows
- `synthetic/events.jsonl`: 3000 operational events

## Deliberate Data Problems

- duplicate identifiers and duplicate business events
- blank mandatory fields
- stale or impossible timestamps
- out-of-range scores
- untrusted text payloads suitable for prompt-injection testing
- missing correlation identifiers
- mixed legacy and modern source-system semantics
