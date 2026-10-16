# Contract tests

## Scope

Test API and protobuf compatibility between providers and consumers. Run when contracts or their usage change.

## Inputs

- Current contracts and the previous supported contract revision.
- Providers, consumers, generated clients, and supported deployment combinations.

## Steps

1. Identify affected providers and consumers, including callers outside the changed module.
2. Run contract lint and compatibility checks against the supported baseline. Check protobuf field numbers, types, presence, enum values, and removed-field reservations.
3. Regenerate clients and verify affected consumers build and use the changed contract correctly.
4. Test request and response semantics: required values, defaults, validation, errors, and status codes. A schema-compatible change can still change behavior.
5. Verify provider responses satisfy consumer expectations. For rolling upgrades, test the old/new client and server combinations the deployment procedure permits.
6. For an intentional breaking change, require a version or migration plan and validate the supported transition before release.

## Output and gate

- Passing compatibility and behavioral checks for supported consumers.
- Supported version combinations and intentional breaking changes recorded.
- Contract baseline, commands, results, and migration limits recorded.
