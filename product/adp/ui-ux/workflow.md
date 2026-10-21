# UI/UX workflow

Use the [project brief and policy](guidelines.md), [design system](design-system.md), shared [development workflow](../development.md), and [UI testing](../testing.md#ui). Apply only affected steps and existing gates.

## Define and evaluate

Define critical tasks from requirements, current behavior, research/support evidence, and explicit assumptions. Acceptance states starting conditions, actions, resulting state, and applicable completion/error/time targets. Map entry points, navigation/back/deep links, permissions, decisions, interruption, and recovery. Sketch content hierarchy and actions before detailed visuals; prototype uncertain interactions and label simulations.

The brief's decision owner determines whether changed critical journeys, uncertainty, or impact require representative-user evaluation. Established interactions/cosmetic changes need no new study unless they invalidate evidence. Where required, test realistic tasks before detailed-screen commitment, without coaching, with consent and non-sensitive data. Record completion, confusion, errors/recovery, and sample limits. Missing required user evidence blocks dependent handoff; otherwise label usability unvalidated.

## Specify

- Agree visual direction and reuse components/tokens. Specify applicable default, hover, focus, pressed, selected, disabled, invalid, and pending states, accessible names, keyboard/focus behavior, and feedback.
- Cover loading, empty, partial, error, success, denied, and recovery states. Distinguish unknown/pending from success; state which input survives. Choose confirmation/undo according to recoverability and write actionable labels/errors.
- Define responsive hierarchy, wrapping/overflow, navigation/touch behavior. Exercise long/real content, large data, text scaling, localization, and right-to-left when supported.
- Apply the accessibility target. For native platforms include safe areas, platform controls, back navigation, keyboards, permissions, and resume. Version handoff with flows, behavior, tokens, assets/rights, and acceptance. Resolve missing behavior before implementing it.

## Implement

Reuse local patterns; share components only for an actual need. Respect project boundaries and contract/state/failure guarantees under [architecture](../../skills/adp-architecture/SKILL.md) and [program design](../../skills/adp-program-design/SKILL.md).

Distinguish interaction/navigation state, cached server data, and persisted state. Keep authorization/business validation with the owning backend. Use semantic platform controls; implement keyboard, focus/restoration, scaling, and accessible feedback with each interaction.

Handle slow, failed, canceled, stale, and overlapping requests; old results must not replace current state. Preserve useful input, follow retry/duplicate protection, and reconcile unknown writes before resubmission/success. Provide rollback for optimistic updates and offline/reconnect behavior where required.

Set applicable readiness/interaction, asset/bundle, and large-list budgets against a named device, network, workload, and baseline. Fix measured bottlenecks. Verify each supported platform, including shared code, and record intentional deviations.

## Verify and accept

Map acceptance to component/integration, critical end-to-end/recovery/persistence, accessibility, compatibility, visual, performance, and required usability evidence under the testing policy. Automated accessibility/functional tests cannot establish conformance/usability alone. Use controlled fixtures for failures and assembled systems for real integration.

Investigate visual differences before updating baselines. Record expected/observed behavior, environment, impact/criterion, and useful images. Evidence identifies candidate/design revision, commands, fixtures, environments, and manual coverage; refresh affected results when inputs change. Fix findings and rerun affected checks.

Compare the final candidate with agreed design/criteria; report intentional deviations, unsupported environments, and unresolved issues with owners/dispositions. Missing or failed required evidence blocks its gate. Reconcile project docs and completed plans through [completion](../../skills/adp-completion/SKILL.md); release handoff uses [CI/CD](../ci-cd/workflow.md).

For authorized post-release evaluation, define question, measures/baseline, window, owner, response, consent, collection limits, access, retention/deletion; review session recording separately. Report gaps/uncertainty and route findings into scoped fixes through the same gates.
