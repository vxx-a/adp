# Development completion

## Scope

When the user says development is finished, run a readiness review of the completed scope. For a feature, finish at the handoff to its source dev branch. For a release, continue with the combined candidate and release gates. Deployment needs an explicit target and authorization.

Verify the reconciliation required throughout the [development workflow](workflow.md). Documentation is maintained during each completed scope; this review checks that it agrees with intent, implementation, and evidence.

## Inputs

- Completed scope, plan, acceptance criteria, and current project documentation.
- Source branch, candidate revision or diff, target dev branch, and previous release where applicable.
- Whether the user wants feature acceptance or a release candidate. If unclear, complete the feature review first and ask before assembling a release.

## Steps

| Order | Action | Required result |
|---|---|---|
| 1 | Review completion | Each acceptance criterion maps to implemented behavior and a check. Verify affected program design, architecture, and overview against the implemented scope. List unfinished work, missing requirements, and unresolved differences. |
| 2 | Pass the feature gates | The testing gates [before every commit](../testing/workflow.md#before-every-commit) and [before merging into dev](../testing/workflow.md#before-merging-into-dev), plus the applicable [security gates](../security/workflow.md#gates), pass. |
| 3 | Prepare a release candidate, when requested | Combine the intended dev branches into one chosen dev branch. Record its revision, included changes, and previous release. Review affected contracts, callers, guarantees, and shared docs together; refresh invalidated evidence. |
| 4 | Pass the release gates | The testing gate [before release](../testing/workflow.md#before-release) and the [security release gate](../security/workflow.md#gates) pass on the same candidate. |
| 5 | Finish the handoff | Verify `docs/` describes the implemented portion, lasting decisions, and ongoing product constraints. Keep the [security report](../security/code-review.md#report) with the change review. Resolve reconciliation gaps, retain unfinished plans, report readiness and blockers, and stop at the authorized step boundary. |

Fixes go back through the gates they affect.

## Output and gate

- **Feature ready:** hand off the tested feature for merge into its source dev branch.
- **Release ready:** hand off the tested candidate for release merge and any requested deployment.
- **Blocked:** report the failed gate and the smallest fix or missing decision.
- Acceptance results, plus the results the testing and security gates report for the candidate.
- Failed or skipped checks, verification limits, and unfinished work.
- Unresolved differences block affected acceptance claims; recording a defect does not accept it. Distinguish source verification from behavior verified in a named environment.
- For releases: candidate revision, migration requirements, configuration changes, and rollback requirements.
- A readiness report does not merge, publish, or deploy. Perform those actions when included in the user's requested scope, following the [Git policy](../ci-cd/git-policy.md) and [CI/CD workflow](../ci-cd/workflow.md); deployment also requires its target environment and [recovery procedure](../ci-cd/deployment.md).
