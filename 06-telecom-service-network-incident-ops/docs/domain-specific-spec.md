# Telecommunications: Service Provisioning, Network & Incident Operations

## Centre of Gravity

High-volume telemetry, topology truth, automation safety, change governance, and SLA evidence.

## Enterprise Context

This repository represents a brownfield estate built over several engineering generations: legacy scripts and files, partially modernized APIs, operational portals, synthetic enterprise data, and newly introduced AI assistance. The design is intentionally credible rather than clean. Participants must infer reality by reading code, data, configuration, tests, docs, and operational artifacts.

## Business Flows

- Customer order to provisioning
- Alarm storm to incident correlation
- Topology lookup to AI recommendation
- Approved remediation to validation

## Core Personas and Identities

- `noc_operator`
- `network_engineer`
- `field_engineer`
- `customer_support`
- `automation_service`
- `vendor_account`
- `ai_agent`

## Domain Data Model

- `devices`: device_id, hostname, vendor, device_type, site_id, network_zone, mgmt_ip, firmware, owner_team, credential_profile, last_seen_at, stale_topology_flag
- `circuits`: circuit_id, customer_id, a_end, z_end, bandwidth_mbps, service_class, status, provisioned_at, sla_tier, orphan_flag
- `alarms`: alarm_id, device_id, interface, severity, alarm_type, first_seen_at, last_seen_at, dedupe_key, maintenance_window, storm_batch_id
- `incidents`: incident_id, customer_id, circuit_id, severity, status, opened_at, root_cause, automation_used, sla_breach_risk
- `service_orders`: order_id, customer_id, service_type, requested_bandwidth, qualification_status, provisioning_status, retry_count, rollback_status
- `ai_invocations`: ai_call_id, incident_id, use_case, model, topology_snapshot_id, alarm_count, token_count, recommendation_risk, approval_required, guardrail_status

## What Makes This a Strong Brownfield Candidate

- multiple teams appear to own overlapping capabilities
- legacy and modern paths disagree on semantics
- AI is assistive but insufficiently governed
- audit evidence exists but cannot yet reconstruct the full decision chain
- authorization is role-centric and needs contextual policy
- reliability behavior is uneven across synchronous, batch, and event paths
- cost and token usage are visible in fragments but not tied to business outcomes
