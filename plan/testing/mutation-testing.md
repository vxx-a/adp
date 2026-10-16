# Mutation testing

## Scope

Check whether tests detect deliberately changed application logic before release. On later releases, test logic changed since the previous release; on the first release, include all application logic.

## Inputs

- Source dev branch, candidate revision, previous release revision, and passing normal tests.
- Mutation tool, required threshold, allowed exclusions, and affected test commands.

## Steps

1. Create `dev-mutation-testing` from `dev`; for other dev branches, use `<dev-branch>-mutation-testing`. Use an isolated worktree and test environment.
2. Verify normal tests pass before mutation. Limit mutation to the defined application scope; record exclusions with reasons.
3. Run the tool and inspect surviving mutants. Add tests for missed behavior and fix real bugs. Justify equivalent mutants, whose changes cannot affect observable behavior.
4. Keep generated mutations out of commits. Before each commit, review fixes and test additions and run required checks under the workflow rules.
5. Resolve unexplained survivors and meet the configured threshold. Tool failures, unexpectedly empty discovery, and timeouts block the gate until investigated; they are not successful mutation results. Record a justified not-applicable result if there is no application logic in scope.
6. Run the configured release suite on the resulting candidate. Changes invalidate affected results, including mutation results.
7. Merge back only into the source dev branch after all required checks pass. If it has advanced, incorporate its changes into the mutation branch and rerun affected checks. Fast-forward the source branch to the tested revision.

## Multiple dev branches

- Each source has its own branch: `dev-api → dev-api-mutation-testing → dev-api`.
- Integrate dev branches into a chosen dev branch before validating a combined release. Passing results from individual branches do not validate their combination.
- Changes made while a run is in progress require affected checks on the updated candidate before merging.

## Output and gate

- Tested source branch and revision, scope, tool version, score, and mutant counts by outcome recorded.
- Surviving mutants resolved or explicitly justified; required threshold passes.
- Exclusions, commands, reports, and test improvements recorded. Threshold and exclusion policy must be configured before implementation.
