# UI/UX guidelines

Apply these rules through the [workflow](workflow.md). Each project chooses its visual direction, stack, tools, and services.

## Rules

1. Start with the user's goals, preferences, references, and existing project decisions. Separate requirements from preferences and assumptions. Ask only about missing decisions that materially affect the work; continue unaffected work.
2. Agree the visual direction before applying it broadly. Reuse the existing design system where suitable. If direction is unclear, compare relevant references or one representative screen; do not impose a default style.
3. Specify behavior and acceptance criteria independently of tools. Text, sketches, code, or design files are valid when they convey the required information. Use prototypes where they resolve uncertainty.
4. Reuse the project's stack and services. Add dependencies or providers only for a stated requirement. No particular framework, design app, paid service, or agent connector is required by ADP.
5. Support the agreed devices, input methods, languages, and the [accessibility baseline](#accessibility). Define defaults and persistence for user preferences in scope; add settings or multiple providers only when the product needs them.
6. Preserve clear actions, honest feedback, useful input, and recovery. Resolve conflicts between visual preferences and required usability or accessibility before implementing affected behavior.
7. Follow [shared collaboration rules](../guidelines/agent-collaboration.md) for scope changes and authorization. Missing tools or evidence do not count as completed required checks.

## Project brief

Record affected decisions in the target project's scoped plan; link existing answers and omit unrelated areas.

| Area | Specify |
|---|---|
| Purpose | Users, tasks, context, desired outcomes, and excluded scope |
| Preferences | Brand, references, visual direction, existing decisions, constraints, and assumptions |
| Behavior | Flows, content, interaction states, permissions, interruption, and recovery |
| Support | Platforms, viewports, input methods, languages, accessibility standard and version, verification methods, and applicable user settings |
| Tools and services | Existing stack, integrations, access, budget, privacy constraints, and reasons for additions |
| Acceptance | Observable outcomes, quality targets, required checks, design revision, assets and usage rights, and decision owner |

## Accessibility

- Minimum: keyboard operation on keyboard-capable platforms, logical focus order and restoration, visible focus, and accessible names, roles, states, and feedback for assistive technology.
- Preserve readable contrast, non-color cues, usable targets, understandable errors and recovery, and content and controls under text scaling. Respect applicable platform accessibility settings, including reduced motion.
- Setup records the applicable web/native accessibility standard and version, supported assistive-technology combinations, verification methods, and owner. Project requirements may add to this baseline; visual preferences do not waive it. Missing decisions block dependent design or checks.

## Tools and services

- Evaluate changes against required capabilities, existing alternatives, licensing, cost, privacy, maintenance, and replacement effort. Verify claims from primary sources and try a representative flow with non-sensitive data before adoption.
- Define user-visible integration outcomes, connection and permission behavior, disconnection, and failures. Follow project architecture and security rules; keep secrets out of design artifacts and client bundles.
- Identify authoritative design/code artifacts, revisions, ownership, and import/export direction. When access is unavailable, use an export, screenshots, written behavior, or existing code only if it preserves required information. Record gaps; do not invent behavior or silently replace a service.
- If no adequate fallback exists, request the specific access or decision needed and keep affected work or gates open.
