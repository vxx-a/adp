# Ops setup policy

Use for establishing or changing CI/CD, deployment, recovery, monitoring, or operational configuration. Follow [ops setup](../skills/adp-ops-setup/SKILL.md), the shared [workflow](development.md), [authorization](rules.md#working-with-the-user), and [security](security.md). Read-only health investigation follows [monitoring](monitoring.md).

## Project decisions

Inspect existing infrastructure, architecture, commands, runbooks, schedules, secrets, and telemetry first. Reuse working conventions; choose providers, tools, and numeric targets from requirements and observed baselines, not ADP defaults. Resolve only decisions needed for the authorized scope.

| Area | Settle in project-owned configuration/runbooks |
|---|---|
| Scope | Proposal, repository changes, or external setup; explicit targets, owner/fallback, permitted actions, cost/resource limits, and checks |
| Commands | Local startup/check/cleanup, CI, build, deployment/status/verification/recovery, and monitoring; prerequisites, inputs/targets, timeouts, exit meanings, evidence locations |
| CI/Git | Provider, runner isolation, supported stacks, required checks/reviews, branch roles, merge/versioning model, and native enforcement under [Git policy](ci-cd/git-policy.md) |
| Release | Registry, dependency inventory, trusted provenance/producer verification, evidence retention, configuration identity, immutable artifact handoff, and supported recovery windows under [CI/CD](ci-cd/workflow.md) |
| Environments | Ownership/isolation, secret store, scoped read/deploy/admin identities, rotation/revocation, and allowed automation |
| Deployment | Strategy, predecessor/recovery identities, migration compatibility/order, locks, abort conditions, restore procedure, expected loss/time, and [verification](ci-cd/deployment.md) |
| Monitoring | Sources, cadence/freshness, thresholds/windows, service/agent correlation, alert routes/escalation, maintenance expiry, and [signal ownership](monitoring.md#signal-definitions) |

Generated commands, configuration, and runbooks are project-owned, outside ADP paths. Link executable definitions from existing operations/check docs instead of maintaining parallel inventories. Reruns inspect state, preserve customizations, and make no mutations when unchanged. ADP updates must leave these project files intact.

## Apply boundaries

External provisioning, credential changes, schedules/routes, installation, and deployment require authorization for the concrete action and target, with reviewable changes and recovery/cleanup. Proposal-only and repository-only work stop at their boundaries. Separate read/check identities from deploy/recovery/admin access; record references and lifecycle owners without secret values.

Validate before applying; rehearse only in authorized isolated targets. After apply, verify changed resources and relevant paths, including schedule execution and route delivery when changed. Check missing/expired credentials, wrong targets, partial provisioning, unknown remote results, and failed cleanup; preserve actual state and ownership and reconcile before retrying. Static checks and simulations do not establish operational readiness.

## Verification

Choose checks from the project's requirements and the facilities actually changed. Verify command/configuration validity and preservation of existing customizations; after an authorized external change, check the affected resource and execution/delivery path. Include failure, retry, or recovery drills only where needed for the changed guarantees, in an authorized isolated target.

Independently review configuration and evidence for security and correctness. Report repository checks, isolated drills, hosted enforcement, and observed operation separately. Missing required tooling or post-apply evidence blocks only the dependent readiness claim.
