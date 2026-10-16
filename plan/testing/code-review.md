# Code review

## Scope

Review correctness and test quality before committing, and review integration changes on the combined release candidate.

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

## Output and gate

- Reviewed revision or diff and findings recorded.
- No unresolved correctness findings; test gaps affecting required behavior are fixed.
- Passing tests alone do not replace review of the changed behavior.
