# Development completion

## Scope

When the user says development is finished, run a readiness review of the completed scope. For a feature, finish at the handoff to its source dev branch. For a release, continue with the combined candidate and release gates. Deployment needs an explicit target and authorization.

Testing and security own their checks. This step runs their gates and doesn't restate them.

## Inputs

- Completed scope, plan, acceptance criteria, and current project documentation.
- Source branch, candidate revision or diff, target dev branch, and previous release where applicable.
- Whether the user wants feature acceptance or a release candidate. If unclear, complete the feature review first and ask before assembling a release.

## Steps

| Order | Action | Required result |
|---|---|---|
| 1 | Review completion | Each acceptance criterion maps to implemented behavior and a check. List unfinished work and missing requirements. |
| 2 | Pass the feature gates | The testing gates [before every commit](../testing/workflow.md#before-every-commit) and [before merging into dev](../testing/workflow.md#before-merging-into-dev) pass. |
| 3 | Prepare a release candidate, when requested | Combine the intended dev branches into one chosen dev branch. Record its revision, included changes, and previous release. |
| 4 | Pass the release gates | The testing gate [before release](../testing/workflow.md#before-release) and the security gate (`plan/security/`, not written yet) pass on the same candidate. |
| 5 | Finish the handoff | Update `docs/` for implemented behavior and lasting decisions. Remove completed plan items; retain unfinished work. Report readiness and remaining blockers. |

Fixes go back through the gates they affect.

## Output and gate

- Status: **feature ready**, **release ready**, or **blocked**, with concrete reasons.
- Acceptance results, plus the results the testing and security gates report for the candidate.
- For releases: candidate revision, migration requirements, configuration changes, and rollback requirements.
- A readiness report does not merge, publish, or deploy. Perform those actions when included in the user's requested scope; deployment also requires its target environment and rollback procedure.

## Next action

- **Feature ready:** hand off the tested feature for merge into its source dev branch.
- **Release ready:** hand off the tested candidate for the release merge, then the requested deployment workflow.
- **Blocked:** report the failed gate and the smallest fix or missing decision needed to continue.
