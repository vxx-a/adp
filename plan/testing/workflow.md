# Testing workflow

## Inputs

- Project requirements, acceptance criteria, and relevant load targets.
- Change diff, affected modules, callers, contracts, and shared libraries.
- Existing tests, commands, fixtures, environments, and configured gates.

## Testing steps

Select checks when scoping the feature; record why any step is inapplicable. Required checks must pass at their gates, with evidence tied to the candidate.

| Step | During feature work | Before every commit | Before merging into dev | Before release |
|---|---|---|---|---|
| [Unit tests](unit-tests.md) | Test changed logic; reproduce bugs first | Affected modules and shared-code consumers | CI on combined revision | Full configured suite |
| [Integration tests](integration-tests.md) | Test changed storage and service interactions | Affected interactions with real dependencies | CI on combined revision | Release interactions and migrations |
| [Contract tests](contract-tests.md) | Check changed APIs and consumers | Compatibility and behavior | Combined contracts and consumers | Supported client/server versions |
| [End-to-end tests](end-to-end-tests.md) | Update changed critical flows | Affected critical flows | CI against assembled application | Smoke suite with candidate images and config |
| [UI tests](ui-tests.md) | Check interactions, states, accessibility, layouts | Affected web/native flows and visuals | Repeat automation; refresh affected manual checks | Required flows, platforms, browsers/devices, screen sizes, accessibility coverage |
| [Performance tests](performance-tests.md) | Establish baseline and workload | Affected required targets | Recheck targets affected by integration | Required workloads against baseline |
| [Mutation testing](mutation-testing.md) | Build normal coverage | Normal checks for test fixes | Normal checks | Mutation branch after normal tests; final checks before merge-back |
| [Static checks](static-checks.md) | Format, lint, type, build feedback | All affected required checks | CI on combined revision | Release builds and generated-code checks |
| [Code review](code-review.md) | Trace behavior, callers, test expectations | Resolve correctness and coverage findings | Review integration and conflict resolutions | Review combined changes and mutation-stage fixes |

## During feature work

1. Map changed behavior and affected callers to the required steps above. Missing requirements block checks that depend on them.
2. Run existing tests for the affected scope before editing. Record existing failures separately; they do not count as passes.
3. Add or update applicable tests as behavior changes; follow the step plans above.

## Before every commit

1. Review the diff and connected code. Resolve correctness and required-coverage findings.
2. Run the affected checks selected above, including unit tests for shared-code consumers.
3. Test the exact content being committed; partial staging must not depend on unstaged changes. Commit only after required checks pass. This gate also applies to commits on mutation-testing branches.

## Before merging into dev

1. Test the combined feature/dev revision with the same automated commands in CI. Passing feature-branch results alone do not validate the merge.
2. Review integration changes and conflict resolutions. Refresh affected manual UI or performance checks if the combined revision changes their results.
3. Merge only after required checks pass. If dev advances, validate the updated combined revision.

## Before release

1. Integrate dev branches into a chosen dev branch. Separate passing runs do not validate the combined candidate.
2. Create the mutation-testing branch and verify normal release tests pass before mutation. Complete mutation testing using its individual plan.
3. Review integration changes and mutation-stage fixes. Run the full configured release suite on the final candidate: unit, integration, contract, critical end-to-end, static checks, and required UI and performance checks.
4. Require passing CI results and other required evidence for the candidate, then fast-forward the source dev branch to the tested mutation branch and merge the tested dev candidate into `release`.
5. New commits, integration changes, or conflict resolutions invalidate affected results and require reruns before merge-back or release.

## Shared execution rules

- Setup records each check's command, scope, environment, and blocking status. Required CI checks enforce the merge gates.
- Use isolated test data and services, pinned dependencies and images, and repeatable fixture setup and cleanup.
- Failed, skipped, unavailable, or unexpectedly empty required checks block the gate. Distinguish product failures from environment or tool failures.
- Keep the first failure visible. Diagnostic retries do not erase it. Intermittent failures need investigation; exclusions require a reason, owner, and expiry and must leave the required behavior covered.
- Record source branch, tested revision or diff, commands, environment versions, results, and exclusions. Preserve failure logs and relevant test artifacts.

## Output and gate

- Acceptance criteria have passing checks; required gates pass on the final candidate.
- No unresolved correctness findings.
- Report results and remaining limits under the shared execution rules. Local tests do not establish deployed behavior.

## To decide before implementation

- Commands, environments, and CI gates for each supported stack.
- Critical application flows and required release suite.
- Mutation tools, threshold, and allowed exclusions; performance targets where applicable.
