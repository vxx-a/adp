# Deployment and recovery

## Scope

Deploy artifacts accepted by the [CI/CD workflow](workflow.md), verify them, and recover from failures. Authorization must cover the target environment, promotion, and recovery actions.

## Environments

| Environment | Purpose | Boundaries |
|---|---|---|
| Development | Fast local work and isolated integration checks | Disposable services and data; no production credentials |
| Staging / pre-production | Validate the assembled release and rehearse deployment | Representative topology and configuration; isolated identities and sanitized data; authorized breach targets |
| Production | Serve real users | Protected deployment access, controlled migrations, monitoring, and tested recovery |

Record material differences between staging and production and their verification limits. Environment-specific values are versioned separately from secrets; secrets are injected through the selected store.

## Deployment interface

The project supplies scripts or jobs for preflight, deployment, status, verification, and recovery. Each accepts the target environment and immutable release identity, returns a clear success or failure, and records evidence without secrets.

- Preflight is read-only. Mutating operations must not silently default to production or select the latest artifact.
- Repeated execution checks current state before acting. Migration steps record completion; partial failure must not blindly repeat destructive work.
- Allow one deployment or recovery operation per environment. Acquire an environment lock and recheck the current release before changes. A timed-out job with unknown remote state keeps the environment blocked until reconciled.
- Set timeouts and explicit failure handling for each stage. Keep status available during failures; do not discard the previous working release before verification.

## Before deployment

1. Confirm the authorized release, target, deployment window where required, and recovery scope. Present material migrations, downtime, risks, and remaining limits before execution.
2. Verify release gates, artifact provenance and digests, configuration identity, required secrets and permissions, environment health, capacity, and dependency availability.
3. Record the current deployed release and configuration. Keep its artifacts available for recovery.
4. For data changes, verify the migration against representative prior data and document supported old/new service combinations. Prefer compatible expand/contract changes; delay destructive cleanup until older versions no longer need the data.
5. Verify the backup and restore procedure where data is at risk, including a restore rehearsal and expected recovery time and data loss. A backup's existence alone does not establish recoverability.
6. Set rollout steps, smoke checks, health and business-metric thresholds, observation window, abort conditions, recovery action, and responsible owner. Missing required evidence blocks deployment.

## Deploy and verify

1. Lock the environment and record the starting state. Apply configuration, schema changes, and service rollout in the tested order.
2. Promote the accepted artifact digests. Choose rolling, canary, or replacement rollout during setup based on compatibility and availability requirements; do not invent a strategy during an incident.
3. Check startup and readiness before sending traffic. Then verify critical user/system flows, persisted outcomes, access controls, secret injection, external integrations, and the actual running digests and configuration.
4. Observe error rate, latency, resource use, and relevant business outcomes against the configured baseline for the agreed window. Keep secrets and sensitive data out of probes and reports.
5. If checks pass, record the deployed release, results, and observation window; release the lock. Report deployment verified with any remaining limits.
6. On failure or an abort threshold, stop promotion, preserve logs and state, and follow the recovery procedure. A successful process exit alone does not establish deployed behavior.

## Recovery

- Recover within the authorized scope when the recorded abort conditions occur. If recovery needs a new destructive action or material data-loss decision, stop the dependent action and obtain that decision; perform authorized containment meanwhile.
- Prefer reverting application artifacts and configuration to the previous verified release when they remain compatible with the current schema. Verify digests, health, critical flows, and monitoring again after recovery.
- Do not automatically reverse database migrations. Use the tested rollback, restore, or forward-fix procedure appropriate to the data state. Restoring data requires explicit treatment of writes received since the backup.
- If recovery fails, preserve the environment lock or incident ownership, report the actual state and user impact, and escalate to the named operator. Do not declare success because the rollback command completed.
- Keep the failed release and recovery evidence. Fixes return through affected release gates before another deployment attempt.

## Ongoing operations and output

- Assign owners for health alerts, security findings, backup/restore checks, and expired credentials. Configure actionable thresholds and notification destinations during setup.
- Retain sanitized logs, metrics, and traces sufficient to connect a regression to a release; control access and retention for sensitive telemetry.
- Record target, authorization scope, previous and new release identities, digests, configuration version, migrations, checks, failures, and recovery outcome in the release record.
- Report the observed state: verified deployment, blocked deployment, failed deployment, or verified recovery. Monitoring after the deployment window remains an operational responsibility.

## To decide before implementation

Environment infrastructure, deployment commands, identity and secret handling, rollout strategy per service, migration ordering, backup and recovery targets, verification thresholds, monitoring tools, on-call ownership, and evidence retention.
