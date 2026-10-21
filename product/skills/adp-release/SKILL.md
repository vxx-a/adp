---
name: adp-release
description: Prepare a release and assess release readiness, qualify or publish it, deploy an authorized candidate, or recover a named environment using project commands and immutable identities.
---

# Release and deployment

Read the requested mode/target, project commands/runbooks, [Git](../../adp/ci-cd/git-policy.md), [CI/CD](../../adp/ci-cd/workflow.md), and [deployment/recovery](../../adp/ci-cd/deployment.md) policies. Apply shared [authorization](../../adp/rules.md#working-with-the-user). A readiness request does not authorize merge, publication, deployment, or recovery.

1. Identify authorized scope, candidate and source baseline, actual deployed predecessor/configuration/schema, and designated recovery target. Check included changes and required hotfix/stabilization reconciliation. Missing release definitions route to [ops setup](../adp-ops-setup/SKILL.md), not invented defaults.
2. For release preparation, freeze the intended source scope and verify source gates/reviews under the Git and CI/CD policies; report source readiness for the protected PR separately from release readiness. For release qualification, qualify the actual merged revision, trusted immutable artifacts, and configured staging evidence under CI/CD stage gates. Refresh invalidated checks/reviews; record limits and provenance. Readiness-only work stops with evidence and blockers.
3. If publication is authorized, serialize eligibility/supersession checks and publish the exact qualified tag/record. Reconcile partial publication; never move/reuse a tag.
4. If deployment is authorized, follow deployment preflight, locking, predecessor/evidence rechecks, tested rollout order, critical-flow checks, and observation. Reconcile unknown remote effects before retrying.
5. On abort, perform only authorized recovery compatible with current data state; preserve ownership and escalate when required. Verify recovery outcomes. Update the release record and affected current docs.

Return source ready, release ready, blocked, or the observed deployment/recovery state, with identities, check/review evidence, failures/retries, cleanup/recovery, and blockers. Missing tools, credentials, locks, required evidence, or current authorization blocks the affected action; never substitute command success for observed deployment or recovery.
