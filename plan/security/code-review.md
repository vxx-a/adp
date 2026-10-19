# Security code review

## Scope and skill

`adp-security-code-review` reviews a diff or named codebase scope. Run first on every PR regardless of change type, during development as needed, and on combined release changes. [General code review](../testing/code-review.md) follows the PR audit.

## Inputs

- Reviewed revision or diff, requirements, architecture, and [security guidelines](guidelines.md).
- For a PR: its identifier, base and head revisions, and the combined merge revision where available.
- Connected code, callers, contracts, configuration, dependencies, and test results.
- User roles, trust boundaries, sensitive assets, and relevant abuse cases.

## Steps

1. Map entry points and trust boundaries in the requested scope. For a diff, follow affected behavior into callers and dependencies rather than reviewing changed lines alone.
2. Trace untrusted input to sensitive operations. Check authentication, resource and tenant authorization, injection, file access, outbound requests, deserialization, secret handling, and data exposure where applicable.
3. Review business logic, state transitions, concurrency, replay, resource limits, and failure paths for ways to bypass required controls.
4. Review affected service, container, dependency, CI, and agent permissions. Check that internal calls enforce their required trust boundaries.
5. Check whether tests reject forbidden behavior, including access by a different user, tenant, or role. Report missing coverage for security requirements.
6. Report each finding with its location, prerequisites, concrete failing case, impact, supporting evidence, and smallest fix. Distinguish confirmed defects from hypotheses needing runtime verification.
7. Generate the report below. Return vulnerabilities to the development agent for fixes and regression tests; apply the [blocking policy](workflow.md#blocking-policy). Send runtime hypotheses to [vulnerability search](vulnerability-search.md); required verification keeps the audit incomplete.
8. Verify fixes, affected paths, and test results; update the report. New PR commits require an updated audit before other review resumes. Reuse evidence only where still valid.

## Report

Keep one report per change in its existing PR or change review; return it in the handoff if no review surface exists. Do not publish or send reports externally without authorization. Current docs retain ongoing product constraints, not review histories.

- **No vulnerabilities found:** record candidate, scope, checks, result, verification limits, and material cautions. Limit the claim to the reviewed scope.
- **Vulnerability found:** record location, prerequisites, reproduction or code evidence, impact, severity, fix, regression-test expectation, and open or verified-fixed state. Include the revision and evidence verifying each fix.
- **Incomplete audit:** record missing checks or evidence and why they block completion.

Tie findings and verified resolutions to the candidate. Include reproduction detail only where needed to assess a finding. Keep credentials and private data out of reports.

## Output and gate

- Report complete; [security workflow gates](workflow.md#blocking-policy) satisfied.
- Severity based on impact and realistic exploitability; a scanner label alone does not establish either.
