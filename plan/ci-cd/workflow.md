# CI/CD workflow

## Scope

Validate changes, assemble a release, and promote tested artifacts for projects using ADP. Start with the [Git policy](git-policy.md); use the existing [testing](../testing/workflow.md), [security](../security/workflow.md), and [development completion](../development/completion.md) gates.

Setup will generate project-owned CI and deployment configuration under the [file ownership rules](../template/file-ownership.md).

## Inputs

- Source and target branches, exact candidate revision, included changes, and previous release.
- Configured check commands, required reviews, acceptance criteria, and release suite.
- Build recipe, pinned dependencies and base images, artifact registry, and deployment configuration.
- Authorized environments, deployment and recovery procedures, owners, and evidence retention.

## Stages and gates

| Trigger | Work | Required result |
|---|---|---|
| Before every commit | Diff-derived tests, review, affected static and security checks | Exact committed content passes the local gate |
| PR opened or updated | Security audit first, then independent reviews; automated tests and scans on the combined source/target revision | Required evidence passes and matches the current candidate |
| Merge into dev | Verify candidate identity and target freshness | Only the validated combination enters dev |
| Release requested | Combine changes in one dev branch; mutation testing; source checks and reviews | Candidate source ready to build; artifact and staging gates remain |
| Candidate built | Build deployable artifacts once; scan final artifacts and deployment configuration; record digests | Immutable artifacts trace to the tested revision |
| Candidate deployed to staging | Run the final release suite with those artifacts; verify migrations, critical flows, required UI/performance checks, and security breach scenarios | Testing and security release gates pass; evidence identifies candidate, digests, and configuration |
| Release merge | Confirm staging and review evidence remains applicable; merge and tag under the Git policy | Release record links merged revision to validated artifacts |
| Production deployment | Check authorization and target; promote recorded artifacts; verify deployed behavior | Deployment verified, or recovery started and failure reported |
| Scheduled checks | Rescan deployed dependencies/images and run configured monitoring checks | New findings reach the named owner under the security policy |

## CI execution

- Use one checked-in command interface for local and CI checks. Setup records scope, runtime/tool versions, environment, timeout, blocking status, and evidence path for each check.
- Select affected checks for PRs, including shared-code consumers. Changes to shared libraries, contracts, CI, build recipes, or dependency resolution widen the scope. The final candidate runs the full configured release suite.
- Run isolated test services with repeatable setup and cleanup. Use synthetic or sanitized fixtures and separate credentials for each environment.
- Independent automated checks may run in parallel. Security review must finish before other PR review; release promotion waits for all required results.
- Cancel obsolete runs while retaining failure logs; canceled runs cannot satisfy a gate. Serialize merges or use a queue that validates the exact source/target combination.
- Review affected contracts, callers, guarantees, and shared documentation on the combined candidate under the [development workflow](../development/workflow.md#review-and-evidence). Refresh evidence invalidated by integration even when branches have no textual conflicts.
- Apply the [shared testing rules](../testing/workflow.md#shared-execution-rules) for failures, retries, and exclusions.

## Build and promotion

- Build from a clean checkout of the recorded candidate with pinned dependencies and build inputs. Record the build configuration and toolchain alongside its source revision.
- Store immutable artifact digests, dependency inventory, build provenance, scan reports, and test evidence in the release record. Do not promote by a mutable tag alone.
- Test the built images in staging and promote those same digests to production. Inject environment-specific configuration and secrets at deployment; record configuration identity without secret values.
- A rebuild produces a new candidate artifact even when the source revision is unchanged. Repeat artifact scans and affected runtime checks before promotion.
- A merge that changes the build source or inputs returns to build and validation. Any provider-created revision must have recorded checks and provenance under the Git policy before release.

## Runner and credential boundaries

- Untrusted contributions run without deployment credentials, privileged runner access, or access to trusted caches and artifacts they could overwrite. Privileged jobs must not execute unreviewed contribution code.
- Give jobs only the repository, registry, and environment permissions they need. Prefer short-lived deployment identities; protect the release workflow and its configuration with required review.
- Keep secrets in the selected secret store. Mask logs, restrict sensitive reports, and expire temporary credentials and test resources. Never store secret values in release evidence.
- Set job timeouts, artifact retention, and resource limits. Cleanup must also run after failures; report cleanup failures that leave resources or access behind.

## Release evidence and handoff

Maintain one release record containing:

- Source, combined, and merged revisions; included PRs; previous release and immutable release tag.
- Check commands and results, tool/environment versions, two independent review reports, mutation results, security reports, and staging evidence.
- Artifact digests and provenance, deployment configuration identity, migration order, compatibility constraints, and recovery procedure.
- Authorization scope, target environment, operator or job identity, timestamps, actual deployed digests, verification results, and recovery outcome when applicable.
- Failed or skipped checks, retries, exclusions, accepted risks permitted by the security policy, and unresolved blockers.

Report **blocked**, **release ready**, **deployment in progress**, **deployment verified**, or **deployment failed**, based on observed results.

## To decide before implementation

- CI provider, runner isolation, supported stacks, command interface, required check names, and review enforcement.
- Registry, artifact provenance verification, dependency inventory format, retention, and release versioning.
- Environment ownership, secret store, deployment identities, and allowed automation scope.
- Required smoke tests, security scenarios, operational thresholds, observation windows, recovery targets, and notification destinations.
