---
name: adp-ui-ux
description: Design, implement, or evaluate web/native interfaces against user tasks, accessibility, existing visual direction, and explicit acceptance criteria.
---

# UI/UX

Read the request, affected interface/code/design, project requirements and supported platforms, [UI policy](../../adp/ui-ux/guidelines.md), [workflow](../../adp/ui-ux/workflow.md), and [design system](../../adp/ui-ux/design-system.md). Use shared [scope, planning, and review](../../adp/development.md).

1. Identify the requested mode and affected experience. Reuse existing brief/design decisions; settle missing material requirements, visual direction, accessibility/support targets, and acceptance before dependent work. Use proportional prototypes or user evaluation for uncertainty.
2. For design, specify affected journeys, interaction/failure/recovery states, responsive/native behavior, content/assets, and accessibility. Record the concise delta in project `plan/`; design-only authorization stops at a reviewable handoff.
3. For authorized implementation, use [implementation](../adp-implement/SKILL.md), preserving approved behavior and canonical component/token ownership. Resolve missing behavior before building; do not silently change scope or adopt providers.
4. For evaluation/review, map criteria to [UI checks](../../adp/testing.md#ui), inspect the actual candidate on supported platforms, and record reproducible findings. Investigate differences before baseline updates; refresh affected evidence after fixes.
5. Reconcile implemented docs/design-system guidance and completed plans. Return affected flows/design revision, changes/findings, acceptance evidence, manual coverage, deviations, and blockers; follow completion/release handoff only within authorization.

Unavailable design access, devices, assistive technology, or required tools remain evidence gaps. Use an adequate documented fallback where possible; otherwise keep dependent work/checks blocked and continue unaffected authorized work. Never claim usability, accessibility conformance, or deployed behavior from source or screenshots alone.
