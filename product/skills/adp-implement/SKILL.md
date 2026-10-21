---
name: adp-implement
description: Diagnose and fix a bug or implement an authorized scoped change, verify affected behavior, and reconcile documentation using proportional planning.
---

# Implementation

Read project instructions, requirements, acceptance criteria, agreed delta plan when required, current design, and connected code. Follow the shared [workflow](../../adp/development.md), [security guidance](../../adp/security.md), and [coding rules](../adp-coding-rules/SKILL.md).

1. Confirm the bounded implementation is authorized. For bug reports, reproduce the failure or establish it from evidence, trace connected callers, and identify the cause before choosing a fix. Apply the canonical [change-planning requirements](../../adp/development.md#each-change), including the [small-change path](../../adp/development.md#small-changes); write a delta plan only when required. Design-only approval does not authorize implementation. Block dependent work on missing decisions.
2. Read affected callers and checks; establish existing failures separately. Add meaningful acceptance or regression checks from requirements, including relevant failure paths. Define schemas, constraints, and configuration precisely rather than duplicating prose definitions.
3. Implement the agreed portion. Document any needed design change before further code edits; pause for user discussion when it changes agreed behavior or scope. Routine local choices stay within the authorized step.
4. Use [adp-test](../adp-test/SKILL.md) to run selected checks and the documentation checker for affected files. Report tested revision/diff, environment, initial failures, retries, unavailable checks, and limits accurately. A local result does not verify a live system.
5. Reconcile the implemented portion into existing docs in the same scoped change. Assess program design, architecture, and overview upward; update only changed meaning. Preserve transitional behavior, compatibility limits, lasting rationale, and unfinished plans.
6. Hand off code, docs, check results, discrepancies, and remaining work for independent review. A requirement violation remains a defect even if docs and tests are changed to match it. Report the authorized step's result and stop; do not start the next plan item unless continuation was explicitly authorized.

Do not merge, deploy, change live systems, or perform destructive operations under implementation-only authorization.
