# Git and release policy

Use the project's protected PR workflow. [Ops setup](../ops-setup.md) maps existing branches to the roles below, or agrees a simpler flow for continuous delivery; do not impose new branch names on an established project. Apply [shared authorization](../rules.md#working-with-the-user), [testing](../testing.md), [security](../security.md), and [independent review](../development.md#ownership-and-review).

## Branch roles

| Role | Purpose |
|---|---|
| `develop` | Integration for upcoming work; `dev` may keep its name |
| `feature/*` | One feature or fix, based on integration |
| `release/<version>` | Frozen agreed integration scope; stabilization only |
| `main` | Reviewed candidate history; not necessarily qualified or deployed |
| `hotfix/*` | Narrow repair based on the affected deployed immutable tag |
| `maintenance/<line>` | Protected production-based target when production trails main; explicit owner, support scope, and retirement rule |

Use separate branches/worktrees for concurrent tasks; preserve unrelated work and commit only intended files. Never rewrite shared history. Private branch rebases need fresh affected evidence. Keep secrets, generated mutants, local data, and unrelated artifacts out of commits.

Protect integration, main, release/maintenance targets, and release tags against unauthorized direct changes, force pushes, movement, or deletion. Require PR checks and reviews. Ops setup verifies native protections, merge settings, required check names, and how subagent reports satisfy hosted review requirements; instructions alone do not enforce them.

## Pull requests and merge identity

Describe the problem, resulting behavior, source/target, acceptance evidence, migrations/configuration, and limits. Follow the canonical security-first review and testing gates rather than substituting approval for evidence.

- Test the combined source/target candidate, including connected contracts, callers, and shared docs. Target movement, conflict resolution, or substantive fixes refresh affected checks and reviews.
- Merge only the validated combination through protected PRs. Capture the actual resulting revision; queues, squash, or provider merges can change its identity. Qualify that revision before release publication.
- Record source, tested combination, final merge, and artifact relationships. Evidence reuse requires a verified mapping of relevant source and inputs; retain its actual tested identity. Never relabel another revision's result as an exact-revision check.
- Changed content or build inputs return through affected gates. Do not resolve conflicts, edit content, or rebuild silently during merge. Missing, stale, skipped, or failed required evidence blocks the affected gate.

## Release identities

Keep three identities separate: the qualified source baseline for change/mutation scope, the expected deployed predecessor with configuration/schema, and the designated recovery target. The newest tag is not a substitute. A first release covers all application logic; a non-ancestor baseline requires explicit scope validation.

Compare candidate contents with authorized scope. Main or maintenance may contain an earlier failed candidate; remove unintended content through reviewed reverts or choose a fresh protected production-based target. Never inherit it silently.

## Release flow

1. Reconcile required main/hotfix fixes into integration. Record scope, source baseline, version, and acceptance; freeze that revision on a release branch. Integration can continue independently.
2. Admit stabilization, test, and necessary metadata/migration fixes only. New features reopen scope and invalidate affected evidence. Complete source gates, mutation testing, and reviews before the protected PR into main.
3. Qualify the actual merged revision under [CI/CD](workflow.md): source evidence, immutable artifacts/scans, and full staging release gates. Failure leaves an unqualified candidate; repairs or reverts arrive through reviewed PRs.
4. Publish an immutable tag at that exact qualified revision and complete its release record. Reconcile interrupted publication against intended version, revision, and digests; conflicts block. Never move or reuse a published tag. Production requires complete publication; staging uses [candidate prerequisites](deployment.md#before-deployment).
5. Reconcile useful stabilization fixes from completed or abandoned releases into integration before the next cut. Retire temporary branches only after fixes and evidence are reconciled or explicitly dispositioned.
6. Deploy recorded digests only through the [deployment procedure](deployment.md) with authorization for the action and target. A merge/tag event grants no deployment authority.

Allow one normal qualification per supported line. Serialize publication, hotfix supersession, and rollout-start decisions against protected release state, with consistent lock ordering relative to environment locks. Recheck eligibility inside that operation. Already-running mutations require reconciliation, not blind cancellation.

## Urgent fixes

Identify affected production from its deployment record, artifacts, configuration, and schema. Branch from that deployed tag. When main includes undeployed changes, qualify the hotfix on a protected production-based maintenance target. Check scope even after a previous failed hotfix; use reviewed reverts or a fresh target, never reset shared history.

Keep normal testing, security, review, artifact, and staging gates. Hotfix acceptance atomically supersedes affected normal candidates before the hotfix becomes deployable. Publication and rollout reject superseded candidates; reconcile any running normal rollout under the environment lock first.

Forward-port through reviewed PRs into main, integration, and affected open release branches. Production repair need not wait for forward-ports, but the next affected release must wait for reconciliation and refreshed qualification. Retire maintenance after production leaves it and required forward-ports finish.
