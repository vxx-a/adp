---
name: adp-test
description: Select, implement, or run scoped unit, integration, contract, end-to-end, UI, performance, mutation, and static checks against project requirements and candidate gates.
---

# Test a change

Read requirements, acceptance criteria, candidate/diff, connected callers/contracts, project check configuration, and the [testing policy](../../adp/testing.md). Apply [change planning and authorization](../../adp/development.md#each-change) before modifying tests or code.

1. Map changed behavior and risks to applicable test layers and the requested gate. Select documented project commands, candidate identity, prerequisites, supported versions/platforms, and required evidence. Record inapplicable layers with reasons. Resolve missing commands, thresholds, or environments before dependent acceptance claims; do not fabricate them.
2. Inspect commands for effects and scope. Establish existing failures. Prepare isolated data/dependencies and bounded readiness checks; running a live, destructive, deployment, or attack command requires authorization for that target and action.
3. For authorized test changes, derive assertions from requirements and follow the selected layer's policy. Reproduce bugs before fixing them. Exercise real boundaries where required; check a deliberately wrong result would fail. Keep changes within the agreed design.
4. Run selected checks on exact candidate content. Review failures and meaningful discovery/counts; retain initial failures and investigate retries. Clean up fixtures/resources even after failure. Mutation-generated code never enters commits.
5. Refresh affected checks after fixes or integration and hand off for the required independent reviews. Return candidate, layers/commands, counts/results, environment, exclusions, artifacts, unresolved findings, and limits.

Report passed or blocked for the requested gate. A test result cannot substitute for a missing required review, environment, or deployment verification.
