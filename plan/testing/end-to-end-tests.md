# End-to-end tests

## Scope

Test critical user or system flows through the assembled application. Run affected flows during development and the critical smoke suite before release.

## Inputs

- Critical flows and their acceptance criteria.
- Candidate images, deployment configuration, migrations, test accounts, and fixtures.

## Steps

1. Select the smallest set of flows that demonstrates the required application behavior, including important failure paths.
2. Start the candidate images with representative deployment configuration in an isolated environment. Use real internal services and storage.
3. Exercise flows through public entry points. Verify authentication, authorization, routing, responses, and final persisted effects where applicable.
4. Use condition-based waits with time limits for asynchronous work. Avoid fixed sleeps that hide timing failures.
5. Use external-service sandboxes when available. Record substituted external dependencies and the behavior they cannot validate.
6. Run the critical smoke suite on the combined release candidate, including startup and readiness. Clean up test resources after each run.

## Output and gate

- Passing acceptance checks for affected flows and the release smoke suite.
- Candidate revision and image identifiers, configuration, commands, and results recorded.
- External dependency limits remain visible; candidate checks do not prove production deployment behavior.
