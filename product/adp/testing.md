# Testing policy

Select tests from changed behavior, affected callers, contracts, risks, and acceptance criteria. A check is required when the project gate or an affected obligation requires it; record why a layer is inapplicable. Use [shared evidence and review rules](development.md#acceptance-and-evidence) and the [test skill](../skills/adp-test/SKILL.md).

## Project configuration

Before implementing affected behavior, record executable commands, prerequisites, scope, environment, blocking status, and evidence location in the project's existing check documentation, otherwise `docs/checks.md`. Reuse configured tools; do not invent a command or assume every project needs every layer. Record:

- Required checks for local work, exact commits, combined PR candidates, and releases; include affected consumers of shared code.
- Critical flows, supported platforms and contract versions, test fixtures, isolated dependencies, and cleanup.
- Mutation tool, threshold, exclusions, and explicit qualified source baseline; performance targets, representative workload, and baseline where applicable.
- Required automated and manual UI/accessibility coverage. Missing decisions block dependent acceptance claims.

## Gates

| Gate | Required work |
|---|---|
| During development | Establish existing failures before editing. Add applicable checks with the behavior; reproduce bugs before fixing them. |
| Before each commit | Review connected code and test quality. Run affected static, unit, interaction, contract, critical flow, UI, and performance checks selected for this scope. Test the exact staged content independently of unstaged changes. |
| Before merging a PR | Run required automation in CI on the combined source/target candidate, including release, hotfix, and maintenance integrations. Review integration/conflict changes; refresh affected manual and performance evidence. |
| Before release | Freeze the intended scope under project release policy. Run normal source checks, mutation where required, and reviews; qualify the actual merged candidate with the full configured release suite, including migrations and critical smoke flows on its built artifacts/configuration. Apply the [security gate](security.md#gates). |

Refresh affected checks/reviews after fixes, target movement, integration, rebuilds, or configuration/schema drift. Separate branch passes do not validate their combination. Use the [release identity and evidence-reuse policy](ci-cd/git-policy.md#pull-requests-and-merge-identity) and [artifact/staging promotion rules](ci-cd/workflow.md#build-and-promotion); a prior revision's results do not automatically qualify a new candidate.

Use isolated data/services, pinned dependencies and images, repeatable setup, readiness checks, and cleanup even after failure. Control clocks/date/DST, time zones, locale, randomness, environment, external dependencies, and execution order. Use bounded condition/event waits rather than fixed sleeps. Tests must tolerate intended parallel execution without sharing mutable fixtures.

Failed, unavailable, skipped, inconclusive, timed-out, or unexpectedly empty required checks block their gate. Preserve first failures after retries; investigate intermittent failures. Any exclusion needs a reason, owner, expiry, and coverage for required behavior. Record tested revision/diff, commands, tool/dependency versions, environment, counts, results, exclusions, logs, and relevant artifacts. Local tests do not establish deployed behavior.

## Unit

Derive expectations from requirements, not implementation. Cover relevant boundaries, invalid inputs, errors, state changes, observable results, and side effects using real local logic; replace network/storage dependencies at their boundaries. Avoid private implementation assertions unless required behavior depends on them. Run affected units and shared-code consumers. A regression must fail against old behavior and pass with the fix; verify that a wrong result would fail the test.

## Integration

Exercise real module interactions and the actual dependency under test, including storage and services where needed; do not mock that boundary. Verify responses and persisted effects. Cover affected timeouts, unavailability, retries, duplicate effects, concurrency, and partial success. For storage changes test clean initialization and upgrades from representative supported data; test rollback only when the release procedure supports it. Run affected interactions and downstream consumers on the combined candidate; leave no unintended writes or test state.

## Contracts

Identify providers, consumers, generated clients, and previous supported contract baseline, including in-process APIs. Run applicable compatibility/lint checks; for protobuf inspect field numbers/types/presence, enum values, and removed-field reservations. Regenerate clients and build affected consumers where used. Check request/response semantics, defaults, validation, errors, and status codes; schema compatibility does not imply behavioral compatibility. Exercise supported provider/consumer combinations, including old/new remote versions permitted during rolling upgrades. Breaking changes need a version/migration plan and a tested transition.

## End to end

Select critical acceptance flows and relevant failures. Exercise public entry points through the assembled candidate with real internal services/storage and representative deployment configuration. Check identity, authorization, routing, responses, final persisted effects, startup, and readiness. Use external sandboxes or controlled substitutes and record what they cannot validate. Run affected flows during development and the critical smoke suite before release. Record revision, artifact identifiers, configuration, accounts/fixtures, results, and cleanup; candidate checks do not prove production behavior.

## UI

Apply the [accessibility baseline and project target](ui-ux/guidelines.md#accessibility) and selected platform targets. Reuse component tests for local behavior and end-to-end tests across the application. Check affected navigation, forms, validation, loading, empty/partial/error/success/denied states, and recovery.

- Accessibility: required automation plus manual keyboard/focus movement and restoration, names/feedback, supported screen readers, contrast/non-color cues, usable targets, text scaling, and applicable accessibility settings. Automation alone cannot establish conformance.
- Web: supported browsers, viewports, responsive navigation, input methods, clipping, overflow, readability, and control usability.
- Native: supported OS/devices, safe areas, platform navigation/controls, keyboard, permissions, app resume, and applicable platform accessibility services/settings.

Compare changed visuals to acceptance/design references with controlled data, fonts, viewport, locale, time, and animation. Capture visual defects; review changes before replacing screenshot baselines. Record tested platform/browser/OS/device/assistive-technology combinations, sizes, commands, manual coverage, screenshots, and limitations. Required missing platforms or manual checks remain blockers.

## Performance

Define affected workload, measurable latency/throughput/capacity/resource targets, and acceptance thresholds before claiming a pass. Compare baseline and candidate with matching representative data, resources, dependencies, and workloads, isolated from unrelated work. Measure relevant percentiles, throughput, errors, resources, and required sustained/burst behavior; verify correctness under load, including concurrency, duplicates, and queue completion. Repeat enough to distinguish variation from regression. Record warmup, duration, counts, environment differences, and limitations; results apply only to tested load/environment.

## Mutation

When required, test application logic changed since the explicit qualified [source-line baseline](ci-cd/git-policy.md#release-identities); the newest tag or deployed predecessor is not automatically that baseline. Include all application logic for a first release. Use a separate branch/worktree at the recorded source/candidate and an isolated environment. Confirm normal tests pass first; record scope, exclusions, tool version, score, and counts by outcome.

Inspect survivors, add meaningful tests, fix defects, and justify equivalent mutants whose changes cannot affect observable behavior. Meet the preconfigured threshold and resolve unexplained survivors. Empty discovery, timeouts, and tool failures need investigation; record not-applicable only when no application logic is in scope. Never commit generated mutants. Return real fixes/tests through the applicable review/PR gates to the branch from which the mutation run was created; refresh affected mutation, normal checks, and reviews on the resulting candidate. Develop may advance without expanding frozen release scope; reconcile release/hotfix fixes under project Git policy.

## Static and build

Use configured formatters, linters, type checks, and builds for affected code and consumers. Limit automatic edits to intended files; inspect them. Verify generated code matches changed schemas/generators; use contract checks for compatibility. Run the same commands in CI and release builds on candidate content. Required checks pass without new unexplained suppressions. Compilation does not establish runtime behavior.

## Review

Use [security review](../skills/adp-security-code-review/SKILL.md) first and then independent [code review](../skills/adp-code-review/SKILL.md). Review connected behavior, test expectations, weakened assertions/exclusions, and affected documentation on the combined candidate. Passing tests do not replace review; unresolved required behavior or coverage gaps block acceptance.
