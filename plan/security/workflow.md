# Security workflow

Development applies the [security guidelines](guidelines.md). CI/CD enforces checks alongside [security code review](code-review.md) and [vulnerability search](vulnerability-search.md).

## Setup

- Record project-specific assets, boundaries, abuse cases, and required controls.
- Choose check commands for the stack: secret detection, security static analysis, dependency vulnerabilities, container images, and deployment or infrastructure configuration where applicable.
- Record each check's scope, tool version, vulnerability database freshness requirement, environment, blocking status, and evidence location. Dependency update tools do not replace scanning and validation.
- Define isolated staging targets, test identities and data, attack limits, and cleanup. Identify relevant Claude-Red skills.

## Gates

| Point | Required security work |
|---|---|
| Design and implementation | Apply the guidelines, map abuse cases to controls, and add security regression tests. |
| Before every commit | Run configured local secret checks and affected security checks; review changes to security controls. |
| Every pull request, first | Run the security audit and generate its [report](code-review.md#report); apply the blocking policy below. |
| Before merging into dev | CI checks the combined feature/dev revision. Refresh the audit for integration changes; run vulnerability searches where runtime evidence is needed. |
| Before release | Scan final dependencies, images, and configuration; review combined release changes; run required breach scenarios against that candidate in staging and retest fixes. |
| Deployment | Promote the images that passed the release gate. Verify target configuration and permissions match the reviewed deployment design; check access controls, secret injection, and monitoring through the deployment workflow. |

New commits, rebuilt images, configuration changes, or integrations invalidate affected results. Validate the updated candidate before passing its gate.

## CI/CD integration

- Require CI checks and audit reports for merge and release. Scanner passes do not replace review. Reject evidence invalidated by PR or target-branch changes; preserve review and staging evidence alongside automated results.
- Scan the built artifacts intended for deployment, not only source manifests. Include reachable application dependencies, base images, and deployment configuration.
- Keep runners and test services isolated. Untrusted contributions must not receive deployment credentials or privileged runner access. Scope job permissions and credentials to their task.
- Preserve the output below in sanitized CI artifacts, including commands and tool/database versions. Restrict sensitive evidence and exclude credentials.
- Repeat configured scans periodically for newly disclosed vulnerabilities in deployed dependencies and images; define ownership and response deadlines during setup.

## Blocking policy

Every PR, regardless of change type, requires an audit and report before other review. Any confirmed vulnerability blocks approval and merge until the development agent fixes it and the reviewer verifies the fix. Incomplete audits block the PR.

Additional proposed defaults for target-project setup:

- Confirmed critical and high findings block merge or release until fixed and verified. Assess impact and exploitability in the project's context.
- Lower-severity findings outside the PR audit need a fix or explicit risk acceptance with an owner, reason, and resolution or review date. This does not waive the PR fix requirement.
- False positives and inapplicable checks need evidence and a recorded reason. Suppressions must be narrow and reviewed when the affected code or dependency changes.
- Failed, unavailable, unexpectedly empty, or inconclusive required checks block their gate. Record tool and environment failures separately from product vulnerabilities.
- A previously accepted finding or existing baseline is not automatically acceptable for a new release. Reassess changes in exposure and expired exceptions.

## Output

- Candidate revision, image digests, relevant configuration identity, checks and attack scenarios, results, and evidence.
- Findings, fixes and retests, accepted lower risks, exclusions, and remaining coverage limits.
- PR reports in the [change review](code-review.md#report); ongoing product constraints in current design docs.
- Security gate passed or blocked, with concrete reasons. [Development completion](../development/completion.md) consumes this result.

## To decide before implementation

- Commands, tools, severity assessment, freshness requirements, and CI enforcement for each stack.
- Required attack scenarios, staging setup, and who can define or expand the execution scope.
- Secret storage and credential lifecycle for deployment environments.
- Initial Claude-Red skill selection and packaging; later upstream updates remain roadmap work.
