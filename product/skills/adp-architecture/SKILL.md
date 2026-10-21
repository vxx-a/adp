---
name: adp-architecture
description: Design or revise system boundaries, data ownership, dependencies, and shared technical decisions before program design.
---

# Architecture

Read project requirements, the affected baseline, shared [workflow](../../adp/development.md), [module and service definitions](../../adp/rules.md#modules), and [security guidance](../../adp/security.md). Revisit only decisions affected by the task.

- Define purpose, users, external systems, module responsibilities and APIs, data owners, dependency direction, and calls or messaging. Map modules to their hosting services and identify in-process versus remote calls. Follow project rules for deployment and contracts.
- Use as few services as requirements allow. Split for a named scaling, deployment, security, or failure-isolation need; data ownership or size alone does not require a separate service. Review modules approaching 10k lines at responsibility boundaries.
- Keep operations that must succeed together within a defined transaction boundary where practical. Modules in one service may share a designed transaction; co-location alone does not ensure atomicity. Define partial-success and recovery ownership across transaction or service boundaries. Modules access another owner's data through its API.
- Prefer stateless application processes with durable state outside replicas. Name concurrency needs and avoid relying on one replica's memory for correctness.
- Define shared stack, authentication, configuration/secrets, observability, deployment, and environments. Prefer established technology; justify additions against requirements.
- Record stated load, data volume, latency targets, and headroom without inventing targets. Identify assets, trust boundaries, abuse cases, and required controls.

Write the proposed delta in `plan/`, linked to current architecture. Identify missing requirements and exactly which work is blocked. Independently review consequential boundary and shared decisions before implementation under the workflow's review rules.

Return boundaries, ownership, shared decisions, constraints, verification needs, and unresolved questions for discussion. Stop at the authorized architecture step unless continuation into program design was explicitly authorized. As portions are implemented, reconcile architecture and affected overview claims in place; retain unfinished plans. Contracts and internal components belong to program design.
