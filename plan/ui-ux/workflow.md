# UI/UX workflow

Follow the [guidelines and project brief](guidelines.md). Apply only affected steps; small changes need only the relevant decisions and checks. Record design plans under the target project's `plan/` and implemented behavior under `docs/`.

## 1. Define the experience

- Use the brief, existing behavior, research, and support findings to define critical tasks. Record assumptions and missing evidence.
- Set acceptance criteria with starting conditions, actions, resulting state, and relevant completion, error, or time targets.
- Map navigation, entry points, permissions, decisions, completion, interruption, and recovery, including deep links and back navigation where applicable.
- Sketch hierarchy, content, primary actions, and alternative paths before detailed visuals. Prototype uncertain interactions and identify simulated behavior.
- The brief's decision owner determines whether new or substantially changed critical journeys, uncertainty, or user impact require representative-user evaluation. Record the decision and evidence; established interactions and cosmetic changes need no new study unless they invalidate existing evidence.
- Where evaluation is required, validate critical tasks before committing to detailed screens. Give realistic tasks without coaching; obtain consent and avoid exposing personal or production data. Record completion, confusion, errors, recovery, and sample limits. Where applicable user evidence is missing, mark usability unvalidated; required evidence blocks the dependent handoff.

## 2. Specify the interface

- Agree the visual direction. Reuse components and purpose-named tokens for typography, color, spacing, layout, and motion; map design values to code. Follow the [design system](design-system.md) rules.
- Specify applicable control states: default, hover, focus, pressed, selected, disabled, invalid, and pending. Define accessible names, keyboard behavior, focus movement, and feedback.
- Cover loading, empty, partial, error, success, denied access, and recovery. Distinguish pending or unknown outcomes from success; specify which input survives.
- Define responsive hierarchy, wrapping, overflow, navigation, and touch behavior. Exercise real content, long text, large data, text scaling, localization, and right-to-left layout where required.
- Apply the [accessibility baseline and project target](guidelines.md#accessibility). Write clear labels and recovery messages; use confirmation or undo according to an action's recoverability.
- For native interfaces, define safe areas, platform controls, back navigation, keyboard handling, permissions, and app resume. Version the handoff with flow references, tokens, assets and usage rights, behavior, and acceptance criteria. Resolve missing behavior before implementing it.

## 3. Implement

- Reuse existing patterns; keep components local until sharing serves a real need. Follow [architecture](../development/architecture.md) for system boundaries and [program design](../development/program-design.md) for contracts, state, and failure guarantees.
- Implement navigation and forms against the agreed flows. Distinguish local interaction state, navigation, cached server data, and persisted state. Keep authorization and business validation in the owning backend; map errors to actionable feedback and preserve useful input.
- Use semantic platform controls. Implement accessibility, keyboard operation, focus placement/restoration, and text scaling with each interaction.
- Handle slow, failed, cancelled, stale, and overlapping requests. Prevent old results from replacing current state. Follow agreed retry and duplicate-protection rules; reconcile unknown write outcomes before reporting success or resubmitting. Provide rollback for optimistic updates and offline/reconnect behavior where required.
- Set relevant screen-readiness, interaction, asset/bundle, and large-list budgets with a device, network, workload, and baseline. Fix measured bottlenecks. Check each supported platform even when sharing code; record intentional design deviations.

## 4. Verify

Use the [testing workflow](../testing/workflow.md) and [UI tests](../testing/ui-tests.md) for execution and gates. Map acceptance criteria to applicable checks and explain exclusions.

| Check | Evidence |
|---|---|
| Component and integration | Interactions, validation, routing, state, API outcomes, and slow/failed requests |
| End-to-end | Critical journeys, recovery, authoritative write results, and persistence after reload |
| Accessibility | Automated checks plus manual keyboard, focus, screen-reader, and applicable native checks |
| Compatibility | Supported browsers/devices, layouts, text scaling, input methods, and localization |
| Visual | Reviewed screenshots against the design revision; controlled data, fonts, viewport, locale, time, and animation |
| Performance | Measurements against budgets on the named device, network, and workload |
| Usability | Representative task completion, confusion, errors, and recovery; participant and sample limits |

- Use controlled fixtures for isolated failure cases and assembled-system checks for real integration. Automation alone does not establish accessibility conformance; functional tests do not establish usability.
- Investigate visual differences before updating baselines. Record reproducible findings with expected/observed behavior, environment, impact, affected criterion, and useful screenshots or recordings.
- Return findings to design or implementation and rerun affected checks. Evidence identifies candidate/design revisions, commands, fixtures, environments, and manual coverage; refresh it when relevant inputs change. Distinguish source checks from assembled-candidate evidence.

## 5. Accept and evaluate

- Compare the final candidate with the design and acceptance criteria. Record intentional differences, verification limits, unsupported environments, and unresolved issues with owners and resolutions or deferrals. Failed, missing, skipped, unavailable, or inconclusive required checks block their gate.
- Hand evidence to [development completion](../development/completion.md) and the existing [CI/CD workflow](../ci-cd/workflow.md). Update project docs and remove completed plan items while retaining unfinished work. Use existing gates and deployment authorization.
- Where post-release evaluation is in scope, define the question, measures, baseline, observation window, owner, and response. Set consent, collection limits, access, retention, and deletion; review session recording separately. Report data gaps and uncertainty, and route findings into scoped fixes through the same checks.

## ADP implementation boundary

These are planning notes. Decide skill boundaries after agreeing the workflow; reuse development and testing skills rather than duplicating shared rules or gates. Each proposed skill needs a trigger, inputs, outputs, permissions, checks, and unavailable-tool behavior. Evaluate against the [collaboration review cases](../guidelines/agent-collaboration.md#review-cases) and supported web/native work. Ship implemented `adp-` skills under `template/.agents/skills/`, following [file ownership](../template/file-ownership.md).
