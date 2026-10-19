# Code review

## Scope

Review correctness and test quality before committing, and review integration changes on the combined release candidate.

Follow the [coding rules](../development/coding-rules.md) and [security guidelines](../security/guidelines.md). PRs must pass [security code review](../security/code-review.md) before this review starts. Reopen the security audit and update its report if new security concerns emerge.

## Inputs

- Requirements, acceptance criteria, diff, connected code, and test results.
- Affected callers, contracts, dependencies, and expected load.

## Steps

1. Read the diff, affected callers, and the code it invokes. Trace inputs, outputs, state changes, and failure handling.
2. Check behavior against requirements, including relevant validation, authorization, data loss, concurrency, retries, and partial success.
3. Verify test expectations come from requirements. Check that tests fail for incorrect behavior and exercise real boundaries where needed.
4. Review deleted or weakened assertions and test exclusions. A passing suite must not depend on removing required behavior checks.
5. Check for unnecessary code and reuse existing patterns. Preserve validation and error handling when simplifying.
6. Report findings with exact locations, a concrete failing case, impact, and the smallest fix. Resolve correctness findings and rerun affected checks before passing the gate.

Apply the development workflow's [review and evidence rules](../development/workflow.md#review-and-evidence): independently check intent against implementation and affected descriptions against code, contracts, configuration, and meaningful checks. Review stated guarantees through failure paths; source links and passing tests alone do not establish agreement. On combined candidates, reassess affected callers and shared design claims.

## Output and gate

- Reviewed revision or diff and findings recorded.
- No unresolved correctness findings; test gaps affecting required behavior are fixed.
- Passing tests alone do not replace review of the changed behavior.
- Affected documentation agrees with the implemented scope; unresolved differences block affected acceptance claims. Requirement changes are explicit authorized decisions.
