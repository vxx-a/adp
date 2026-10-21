# UI/UX policy

Use [UI/UX](../../skills/adp-ui-ux/SKILL.md) for interface design, implementation, or evaluation, following the [workflow](workflow.md). Apply affected decisions proportionately; cosmetic changes need no whole-product redesign.

## Project brief

Record affected decisions in the project's scoped plan; link existing answers and omit unrelated sections.

| Area | Settle |
|---|---|
| Purpose | Users, tasks/context, desired outcomes, excluded scope |
| Direction | User preferences, brand/references, existing decisions, constraints, assumptions |
| Behavior | Flows, content, interaction states, permissions, interruption/recovery |
| Support | Platforms/viewports, input methods, languages, accessibility target/version, assistive technology, verification, applicable user settings |
| Tools | Existing stack/integrations, authoritative artifacts/revisions, access, budget/privacy constraints, reasons for additions |
| Acceptance | Observable outcomes, quality targets, required checks, design revision, asset rights, decision owner |

Separate requirements from preferences and assumptions. Ask only about missing decisions that materially affect work; continue unaffected work. Agree visual direction before broad application. When unclear, use relevant references or a representative screen rather than imposing a style. Text, sketches, code, prototypes, or design files are valid when they convey required behavior.

Reuse the existing design system, stack, and services. Dependencies/providers require a stated need; ADP mandates no framework, paid service, design app, or connector. Define user preference defaults/persistence in scope; add settings or provider choice only when needed.

Preserve clear actions, honest feedback, useful input, and recovery. Visual preferences cannot waive required usability or accessibility. Resolve conflicts before affected implementation; apply shared [authorization and scope rules](../rules.md#working-with-the-user).

## Accessibility

Minimum: keyboard operation on keyboard-capable platforms; logical focus order/restoration and visible focus; accessible names, roles, states, and feedback; readable contrast, non-color cues, usable targets; understandable errors/recovery; content and controls under text scaling; respect applicable accessibility settings, including reduced motion.

[Project setup](../setup.md#instructions-and-stack), or the first affected UI task when absent, records the applicable web/native standard and version, supported assistive-technology combinations, verification methods, and owner with the user. Requirements may strengthen this baseline. Unresolved target decisions block only checks/design that depend on them; continue baseline accessibility work and unaffected checks. Automated scans alone do not establish conformance.

## Tools and services

Assess additions against capabilities, existing alternatives, cost, privacy, maintenance, and replacement effort. Verify claims from primary sources and exercise a representative flow with non-sensitive data before adoption. Define connection/permission behavior, disconnection, failures, and user-visible outcomes. Apply project architecture/security; no secrets in design artifacts or client bundles.

Name authoritative design/code artifacts, revisions, owners, and import/export direction. If access is unavailable, use exports, screenshots, written behavior, or existing code only when sufficient. Record gaps; do not invent behavior or silently replace services. Without an adequate fallback, request specific access/decisions and keep affected gates open.
