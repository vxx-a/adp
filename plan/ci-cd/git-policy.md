# Git policy

## Scope

Branches, PRs, reviews, and releases for target projects. Provider-specific enforcement is not implemented.

A merge needs an authorized action and target; ask again only if scope or material facts change.

## Branches

Choose one release branch name during setup: `release` or `main`. References to `release` in the plans mean that chosen branch.

| Branch | Purpose | Merge target |
|---|---|---|
| `release` / `main` | Accepted release history; production state is recorded separately by deployment | Receives the tested release candidate |
| `dev`, or named `dev-*` branches | Integrate ongoing work | Chosen dev branch for combined release validation, then release |
| `feature-<name>` | One feature or fix, based on its source dev branch | Source dev branch |
| `<dev-branch>-mutation-testing` | Mutation testing and resulting test or code fixes | Source dev branch only, by fast-forward |

- Use separate branches or worktrees for concurrent tasks. Preserve unrelated work; commit only the intended files.
- Protect release and dev branches: PRs, required checks, and required reviews; block direct pushes, force pushes, and deletion. Allow mutation merge-back only through the same gates and a controlled fast-forward operation.
- Never rewrite shared history. Private feature branches may be rebased; their updated revisions need fresh evidence.
- Keep secrets, generated mutants, local data, and unrelated artifacts out of commits. Apply the [before-commit gate](../testing/workflow.md#before-every-commit), including tests derived from the diff, before every commit.

## Pull requests

1. Name the source and target branches. Describe the problem, resulting behavior, acceptance evidence, configuration or migration changes, and known limits.
2. Run the [security audit](../security/code-review.md) first on every PR, including documentation and configuration changes. Resolve confirmed vulnerabilities and verify fixes before approval; an incomplete audit blocks the PR.
3. Require two independent reviewers on the proposed change. Each examines the diff and connected code and produces its own findings before comparing reports. At least one covers security and one covers correctness and test quality; both must finish. The author cannot count as a reviewer. Setup defines whether reviewers are people or independent agent runs and how their reports are enforced.
4. Resolve blocking findings and refresh affected reviews after fixes, target movement, or conflict resolution. Record reviewed revisions and remaining cautions.
5. Run required CI on the combined source/target candidate. Passing source-branch checks alone do not validate integration. Record why any check is inapplicable; missing, failed, skipped, or stale required evidence blocks merge.
6. Merge only the candidate whose required checks and reviews passed. If the target advances, validate the updated combination before merging.

Use the [testing](../testing/workflow.md) and [security](../security/workflow.md) policies for gate contents and blocking rules. Approval does not waive either gate.

## Merge identity

- Prefer a fast-forward of the tested candidate where supported. When a PR platform creates a merge or squash commit, validate the exact resulting revision through its merge queue or equivalent controlled procedure before promoting it.
- Do not resolve conflicts, edit files, or rebuild artifacts silently during merge. Changed content returns to the affected gates.
- Record the relation between source revision, tested combined revision, final merged revision, and built artifact digests. Reject mismatched or stale evidence.
- Setup must choose a merge method and protection settings that support this flow, including controlled mutation fast-forwards; do not bypass protections to make the procedure work.

## Release flow

1. Select the intended changes and one dev branch to hold their combination. Include release-branch fixes missing from dev before testing.
2. Integrate the selected dev branches there. Validate the combined candidate under [development completion](../development/completion.md).
3. Run [mutation testing](../testing/mutation-testing.md) on `<chosen-dev-branch>-mutation-testing`, then the final release suite and required reviews. Fast-forward only its source dev branch to the tested revision. Source movement requires updated validation.
4. Open the release PR. Require the release checks and evidence defined in the [CI/CD workflow](workflow.md), including staging results for the intended artifacts and configuration. Refresh evidence if the release target changes.
5. Merge the tested candidate, then create an immutable release tag and record the merged revision, artifact digests, evidence, and previous release. A tag identifies a release; deployment records identify where it runs.
6. Deploy through the [deployment procedure](deployment.md) when the environment and action are authorized.

## Urgent fixes

- Branch `feature-<fix>` from the affected release revision when taking unreleased dev changes would be unsafe. Use an isolated dev branch from that revision as its integration and mutation source.
- Keep the fix narrow and pass the same PR, testing, security, staging, and release gates. Urgency does not turn unavailable checks into passes.
- After release, bring the fix into affected dev branches through PRs and validate their combined revisions before the next release.

## Output and setup decisions

Record branch roles, PR and review evidence, tested and merged revisions, release tag, and outstanding blockers. Setup must settle branch names, reviewer identities, check names, merge method, tag/version format, retention, and enforcement permissions before automation is enabled.
