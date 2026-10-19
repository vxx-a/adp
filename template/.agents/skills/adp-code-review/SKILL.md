---
name: adp-code-review
description: Independently review a scoped implementation or combined candidate for correctness, meaningful tests, and agreement between requirements, code, and documentation.
---

# Code review

Read the requirements, acceptance criteria, candidate diff/revision, connected code, callers, contracts, configuration, check results, and affected docs. Use the shared [workflow](../../adp/development.md) and [coding rules](../adp-coding-rules/SKILL.md).

For a PR, verify that the [security audit](../adp-security-code-review/SKILL.md) and report passed first. A new security concern reopens that audit. An author reviewing its own work cannot claim independent acceptance.

1. Trace inputs, outputs, state changes, concurrency, resources, failures, and shared consumers. Review beyond changed lines.
2. Compare implemented behavior against requirements. Check test expectations came from those requirements, and that meaningful checks reject incorrect behavior. Review weakened assertions, exclusions, and skipped checks.
3. Independently compare affected current descriptions against code, contracts, configuration, failure paths, and evidence. Links help locate implementation; they do not prove a guarantee.
4. Assess impact through program design, architecture, and overview. Require updates only where meaning changed; retain unimplemented portions in the plan. Do not accept a changed obligation implicitly through rewritten docs.
5. On combined candidates, reassess interacting contracts, callers, guarantees, and shared docs even without textual conflicts. Refresh invalidated evidence after fixes/integration.
6. Report each finding with location, a concrete failing case, consequence, evidence, and smallest fix. Resolve findings using evidence rather than reviewer votes; obligation or authorization changes go to the user.

Return reviewed candidate, scope, findings, verification limits, and pass or blocked. Confirmed correctness defects, unresolved required behavior, and missing required checks block affected acceptance. Preserve disagreement and independent reviewer limits in the existing report; do not replace a missing reviewer with the owner's second pass.
