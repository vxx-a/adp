---
name: adp-implement
description: Implement an agreed scoped change, verify affected behavior, and reconcile current design documentation while preserving unfinished plans.
---

# Implementation

Read project instructions, requirements, acceptance criteria, agreed delta plan, current design, and connected code. Follow the shared [workflow](../../adp/development.md), [security guidance](../../adp/security.md), and [coding rules](../adp-coding-rules/SKILL.md).

1. Confirm implementation of this bounded step is authorized and its concrete architecture/program-design delta is documented before code, schema, configuration, or test edits. The design must settle affected behavior, owners, responsibilities, interfaces, state, invariants, flows, and failure policy. Design-only approval does not authorize implementation. Block dependent work on missing decisions.
2. Read affected callers and checks; establish existing failures separately. Add meaningful acceptance or regression checks from requirements, including relevant failure paths. Define schemas, constraints, and configuration precisely rather than duplicating prose definitions.
3. Implement the agreed portion. Document any needed design change before further code edits; pause for user discussion when it changes agreed behavior or scope. Routine local choices stay within the authorized step.
4. Run the selected checks and the documentation checker for affected files. Report tested revision/diff, environment, initial failures, retries, unavailable checks, and limits accurately. A local result does not verify a live system.
5. Reconcile the implemented portion into existing docs in the same scoped change. Assess program design, architecture, and overview upward; update only changed meaning. Preserve transitional behavior, compatibility limits, lasting rationale, and unfinished plans.
6. Hand off code, docs, check results, discrepancies, and remaining work for independent review. A requirement violation remains a defect even if docs and tests are changed to match it. Report the authorized step's result and stop; do not start the next plan item unless continuation was explicitly authorized.

Do not merge, deploy, change live systems, or perform destructive operations under implementation-only authorization.
