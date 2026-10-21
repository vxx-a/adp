---
name: adp-monitor
description: Inspect a named environment, alert, incident, or service/agent run with bounded read-only evidence and no implicit remediation.
---

# Monitoring triage

Read the requested target/window/question, configured signals/runbooks, and [monitoring policy](../../adp/monitoring.md). Configured triggers must provide this scope explicitly; do not infer production.

1. Confirm permitted sources and scoped read access. Inspect queries/commands and establish source-side sanitization before reading logs/payloads. If safe access is unavailable, use other permitted evidence and record the gap.
2. Gather bounded evidence with timestamps, freshness, coverage, and release/service/run identity. Correlate critical outcomes and recent changes. For agents, inspect progress, attempts/failures, completion evidence, and configured time/resource/cost budgets.
3. Classify against configured signal conditions, preserving known failures and unknown coverage separately. Check collector/scheduler health, route failures, and maintenance scope/expiry when relevant. Distinguish observations from hypotheses.
4. Return target/window, state/impact, sanitized evidence references, gaps, confidence, owner/escalation, and proposed response. Reuse incident/release records and configured notification routing.

Missing definitions, tools, access, or fresh evidence limit the affected conclusion; they cannot pass a required health check. Stop before remediation: restarts, retries/cancellation, write probes, rollback, credential/data changes, schedules, and independent messages require their own authorized procedure. Configuration changes route to [ops setup](../adp-ops-setup/SKILL.md).
