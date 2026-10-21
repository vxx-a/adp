# CI/CD policy

Use the [Git policy](git-policy.md), project-selected [testing](../testing.md) and [security](../security.md) gates, and [release qualification](../../skills/adp-release/SKILL.md). Configure project-owned facilities through [ops setup](../ops-setup.md); this policy does not supply a CI provider or hosted enforcement.

## Stage gates

| Trigger | Required result |
|---|---|
| Before commit | Intended content passes the configured local gate, including diff-derived tests |
| PR/update | Security-first independent reviews and checks pass on the combined source/target candidate |
| Integration merge | Candidate identity and target freshness remain valid |
| Release preparation | Frozen scope passes source checks, mutation testing, and reviews before the protected merge |
| Candidate merged | Actual merged revision and applicability of reused evidence are qualified for building |
| Candidate built | Immutable scanned artifacts and deployment configuration trace to the qualified source/inputs |
| Staging | Those artifacts pass the full release suite, migration/critical-flow checks, required UI/performance checks, and authorized security scenarios |
| Publication | Current gates and eligibility pass; immutable tag and complete release record bind the qualified revision/artifacts |
| Production | Authorized promotion uses recorded artifacts and verifies actual deployed behavior |
| Scheduled checks | Configured dependency/image rescans and operational checks route new findings to their owner |

Staging does not require evidence it is about to produce. Source acceptance, release qualification, publication, and deployment are separate states.

## Execution

- Reuse one checked-in local/CI command interface. Record each check's scope, tool/runtime versions, environment, timeout, blocking status, and evidence path. Select affected checks for PRs; shared code, contracts, build/CI recipes, or dependency resolution widen scope. Run the full configured suite for the final release candidate.
- Use repeatable isolated services, synthetic/sanitized data, separate environment identities, and failure-safe cleanup. Independent checks may run in parallel; preserve the shared security-before-general-review order.
- Serialize merges or validate their exact combination in a queue. Reassess interacting contracts, callers, guarantees, and shared docs after integration, including conflict-free merges.
- Cancel obsolete work only when safe to interrupt. Preserve failures, reconcile effects, and finish cleanup before releasing resources. Never blindly cancel deployment, migration, recovery, or unknown remote effects. Canceled work cannot pass a gate.
- Apply the canonical testing policy for retries/exclusions and shared evidence rules for unavailable checks; do not duplicate or weaken them in provider jobs.

## Build and promotion

- Build from a clean recorded revision with pinned dependencies/base images and recorded toolchain/build configuration. Capture immutable artifact digests, dependency inventory, provenance, scans, and test evidence. Mutable tags alone cannot identify a promotion.
- Test built artifacts in staging and promote those same digests. Inject environment configuration/secrets at deployment; record configuration identity without values. A rebuild is a new artifact candidate even from identical source, requiring new scans and affected runtime checks.
- Reserve shared staging through the full release suite, security scenarios, observation, and cleanup, or isolate candidates. Bind evidence to observed running digests/configuration/schema. Replacement or drift invalidates affected evidence; reservation expiry cannot release uncertain effects.
- Verify evidence against allowed repository, trusted workflow/job producer, current gate-policy identity, candidate, digests, and environment/configuration. Protect records and gate decisions from contribution jobs and unauthorized alteration. A matching digest or provenance file alone is insufficient. Recheck policy and evidence freshness at publication/promotion.
- Pin active-release and designated-recovery artifacts, configuration references, provenance, and required evidence throughout supported recovery windows. Garbage-collection expiry cannot override these references. Verify availability before promotion and recovery.
- Serialize publication/supersession and rollout start under the [Git policy](git-policy.md#release-flow). Partial tag/record publication must reconcile before production promotion.

## Runner boundaries

Untrusted contribution jobs get no deployment credentials, privileged runner access, or write access to trusted caches/artifacts. Privileged jobs must not execute unreviewed contribution code. Scope job permissions to needed repository, registry, and environment operations; prefer short-lived identities and review-protected release configuration.

Keep secrets in the selected store; mask logs, restrict sensitive evidence, expire temporary credentials/resources, and record failed cleanup. Set job timeouts, resource limits, and retention. Continuous health coverage follows [monitoring](../monitoring.md); scheduled CI checks alone do not provide it.

## Release record

Keep one record with source/combined/final revisions, included scope, source baseline, expected deployed predecessor/configuration/schema, recovery target, and immutable tag; commands/results and tool/environment versions; required review, mutation, security, and staging evidence; artifact digests, trusted producer/gate-policy identities, provenance, configuration identity, migration/compatibility/recovery procedure; authorization, target/operator, timestamps, actual deployment and recovery results; failures, retries, exclusions, permitted accepted risks, blockers, and qualification/publication/supersession state.

Report observed **blocked**, **release ready**, **deployment in progress**, **deployment verified**, or **deployment failed**, with limits. Readiness grants no publication or deployment authority.
