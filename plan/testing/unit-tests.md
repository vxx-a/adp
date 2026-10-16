# Unit tests

## Scope

Test individual logic for new and changed behavior. Include regression tests for bugs.

## Inputs

- Requirements, acceptance criteria, change diff, and connected code.
- Existing unit tests, fixtures, and test commands.

## Steps

1. Read affected functions, their callers, and existing coverage. Derive expected results from requirements rather than copying the implementation.
2. For a bug, reproduce it with a failing regression test before fixing it. Reuse an existing test if it already demonstrates the failure.
3. Add or update tests for changed behavior. Cover relevant empty and boundary values, invalid inputs, errors, and state transitions.
4. Keep tests deterministic. Control clocks, randomness, and external dependencies. Use real local logic; replace network and storage dependencies at their boundaries.
5. Assert observable results and side effects. Avoid assertions on private implementation details unless those details are the required behavior.
6. Run affected module tests and unit tests for consumers of changed shared code. Ensure a wrong result would fail the new test.

## Output and gate

- Requirement-to-test mapping and passing tests for affected logic.
- Bug regression fails on the old behavior and passes with the fix.
- Test commands, counts, and results recorded under the shared workflow rules.
