# Integration tests

## Scope

Test application code with real storage and service dependencies. Run for changes to persistence, transactions, or interactions between modules.

## Inputs

- Affected modules and their dependencies, contracts, and failure behavior.
- Test service images, isolated databases, migrations, fixtures, and commands.

## Steps

1. Identify the interactions changed by the diff and the callers that depend on them.
2. Start only the needed dependencies using repeatable setup. Wait for readiness and use isolated data; clean up even after failure.
3. Exercise the real application boundary and verify responses plus persisted state. Do not replace the dependency under test with a mock.
4. Cover relevant timeouts, unavailable dependencies, retries, duplicate requests, concurrency, and partial success. Verify side effects are not repeated when duplicate execution must be prevented.
5. For storage changes, verify clean initialization and upgrading representative previous-schema data. Check rollback only when the release procedure supports it.
6. Run affected interactions and downstream consumers on the combined candidate.

## Output and gate

- Passing checks for the affected interactions and defined failure behavior.
- No unintended writes, lost data, or leftover test state.
- Dependency versions, fixtures, commands, results, and failure logs recorded.
