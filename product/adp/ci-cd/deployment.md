# Deployment and recovery

Use the [CI/CD](workflow.md) and [Git](git-policy.md) policies with [shared authorization](../rules.md#working-with-the-user). Authorization names the target, promotion, and permitted recovery actions. [Ops setup](../ops-setup.md) selects infrastructure, commands, identities, rollout strategy, migration order, recovery targets, thresholds, ownership, and retention; never invent these during an incident.

## Environments and interface

Development uses disposable isolated data without production credentials. Staging represents production topology/configuration with isolated identities, sanitized data, and authorized security-test targets. Production uses protected deployment access, controlled migrations, monitoring, and tested recovery. Record material differences and verification limits. Version non-secret environment configuration; inject secrets from the selected store.

Project scripts/jobs expose preflight, deploy, status, verify, and recover. Document prerequisites, explicit target and immutable identity, timeout, exit meaning, and evidence location. Preflight is read-only; mutations never default to production or `latest`.

Bind deployment intent to authorization, artifact/configuration identity, target, expected predecessor release/configuration/schema, and recovery scope. Repeated operations reconcile actual state first; migration completion records prevent blind repeats. Keep status available through failures and retain the working predecessor until verification.

Allow one deployment/recovery operation per environment. Use consistent lock ordering with protected publication/supersession state; staging ownership spans full qualification and cleanup. Unknown remote outcomes keep the environment blocked until reconciled.

## Before deployment

1. Confirm candidate/release, target, allowed window, and recovery scope. Make migrations, downtime, risks, and remaining limits reviewable.
2. Check stage prerequisites: staging needs qualified source/build/scan evidence and exact candidate identity; production needs full qualification, immutable tag, and complete release record. Verify trusted provenance/digests, configuration identity, scoped secrets/access, capacity, dependencies, and environment health.
3. Record actual expected predecessor separately from source baseline and recovery target. Verify retained recovery assets under [CI/CD retention](workflow.md#build-and-promotion).
4. Test migrations on representative prior data and define supported old/new service combinations. Prefer compatible expand/contract changes; defer destructive cleanup until old versions no longer need the data.
5. Where data is at risk, rehearse restoration and verify recovery time and expected loss, including writes since backup. Backup existence alone is insufficient.
6. Set rollout steps, critical-flow checks, health/business thresholds, observation window, abort/recovery actions, and owner. Verify [telemetry freshness and alert delivery](../monitoring.md) before rollout. Missing required evidence blocks.

## Deploy and verify

1. Acquire locks and recheck current authorization, eligibility, trusted evidence/freshness, and stage prerequisites. Compare predecessor release/configuration/schema with intent. Supersession, revoked authorization, expired evidence, or drift blocks mutation; refresh compatibility and materially changed authorization before retrying.
2. Apply configuration, migrations, and accepted artifact digests in tested order using the selected rolling, canary, or replacement strategy.
3. Verify startup/readiness before traffic, then critical flows and persisted outcomes, access controls, secret injection, integrations, and actual running digests/configuration. Keep sensitive values out of probes and reports.
4. Observe errors, latency, resources, and relevant business outcomes against baseline for the configured window. A successful command exit does not establish deployed behavior.
5. On success, record identities, checks, and limits, then release the lock. On failure/abort, stop promotion, preserve evidence/state, and enter authorized recovery. Do not release ownership while effects remain uncertain.

## Recovery

Use the designated verified recovery release/configuration when compatible with current schema; a queued old deployment is not rollback authorization. Never automatically reverse migrations. Use the tested rollback, restore, or forward-fix procedure for actual data state, accounting for writes since backup.

New destructive actions or material data-loss decisions need authorization; continue authorized containment meanwhile. Verify recovery digests, critical flows, monitoring, and data outcomes. Failed recovery retains the lock or incident ownership and escalates actual impact to the named operator. Keep failed-release and recovery evidence; fixes return through affected gates before retrying.

Record target, authorization, previous/new identities, configuration, migrations, checks, failures, and recovery in the release record. Report verified deployment/recovery, blocked, or failed with remaining limits. Ongoing monitoring remains an operational responsibility after the deployment window.
