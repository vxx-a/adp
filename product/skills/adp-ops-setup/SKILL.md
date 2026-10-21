---
name: adp-ops-setup
description: Design or configure project-owned CI/CD, Git protection, deployment, recovery, and monitoring facilities for an explicitly scoped target.
---

# Ops setup

Read the request, project requirements/architecture, current infrastructure/configuration/runbooks, and [ops setup policy](../../adp/ops-setup.md). Use its decision table and scoped verification guidance; follow shared [planning, review, and authorization](../../adp/development.md).

1. Identify proposal, repository, or external scope; targets, owners, resource limits, and checks. Inventory existing facilities and missing decisions. Preserve useful conventions; ask only for decisions blocking this step.
2. Record the concrete configuration/design delta and acceptance in project `plan/`. Settle relevant CI/Git, artifact trust, access lifecycle, deployment/recovery, signals/routes, and command contracts through the linked policies. Proposal-only work stops at that design.
3. For authorized implementation, prepare the smallest project-owned diff, preserving customizations and no-change reruns. Repository-only scope stops before provisioning. Check missing tooling/access, wrong targets, partial results, and cleanup; do not embed credentials.
4. Run static/pre-apply checks and agreed isolated rehearsals; obtain independent review. Apply external changes only within existing authorization for the concrete action/target. Reconcile unknown outcomes before repeating mutations.
5. Verify changed resources and relevant execution/delivery paths in the authorized environment. Reconcile current operations/check docs and prune completed plan items. Keep unapplied or unverified work open.

Return changed files/resources, prerequisites/commands, owners/runbooks, checks by environment, cleanup/recovery state, and blockers. Missing tools, credentials, decisions, or required post-apply evidence remain unavailable; continue independent authorized work and stop at the step boundary.
