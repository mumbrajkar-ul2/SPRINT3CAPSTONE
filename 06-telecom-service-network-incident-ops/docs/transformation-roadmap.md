# Modernization Notes

## Context

This system has been partially modernized over several years. Legacy scripts, batch data movement, API services, operational UI scaffolding, policy experiments, observability notes, and AI-assisted capabilities coexist.

## Current Modernization Themes

- Reduce dependency on shared privileged service accounts.
- Improve data quality checks before downstream processing.
- Clarify boundaries between legacy scripts and API services.
- Strengthen audit events and request correlation.
- Improve operational telemetry for critical workflows.
- Make AI-assisted recommendations traceable, bounded, and reviewable.
- Move environment assumptions into reproducible configuration.

## Known Engineering Concerns

- Some behavior is captured only by legacy scripts and characterization tests.
- Some documentation is older than the code and may be incomplete.
- AI-related metadata is not consistently captured across workflows.
- Current audit records are useful but insufficient for full decision reconstruction.
- Retry and fallback behavior is inconsistent across integrations.
- Cost and token usage are captured in fragments, not tied to business outcomes.
