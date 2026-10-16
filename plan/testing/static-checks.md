# Static checks

## Scope

Check formatting, lint, types, and builds before every commit and on the release candidate.

## Inputs

- Changed files and affected modules, consumers, and generated code.
- Existing formatter, linter, type checker, build commands, and project configuration.

## Steps

1. Use the project's existing tools and rules. Identify checks affected by the change, including consumers of shared code.
2. Run formatting, lint, type, and build checks where configured. Delegate API compatibility checks to the contract-testing step.
3. Apply formatting fixes only to the intended files. Review automatic changes and keep unrelated work intact.
4. Verify generated code matches its source when contracts or generators change.
5. Run the same commands in CI on the candidate content. Do not count successful compilation as proof of runtime behavior.

## Output and gate

- Required static and build checks pass without new unexplained suppressions.
- Commands, tool versions, results, and justified exclusions recorded.
