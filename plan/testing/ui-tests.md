# UI tests

## Scope

Test changed web and native interfaces, including accessibility, layouts, and platform behavior. Apply only the platform-specific checks relevant to the change.

## Inputs

- Affected screens, user flows, acceptance criteria, and design references.
- Supported platforms, browsers, OS versions, devices, screen sizes, and input methods; test accounts and representative data.
- The [accessibility baseline and project target](../ui-ux/guidelines.md#accessibility), supported assistive-technology combinations, and required automated and manual checks.

## Steps

1. Reuse component tests for local behavior and end-to-end tests for flows across the application.
2. Verify affected interactions on each supported platform: navigation, forms, validation, loading, empty, partial, error, success, denied access, and recovery states where relevant.
3. Check the accessibility baseline and project target. Run required automated checks and manually verify keyboard operation where supported, focus movement/restoration, accessible names and feedback, and changed interactions with the supported screen readers. Check contrast, non-color cues, target usability, text scaling, and applicable accessibility settings. Automation alone does not establish conformance.
4. For web interfaces, check supported browsers, required viewports, responsive navigation, and input methods. Look for clipped content, overflow, unreadable text, and unusable controls.
5. For native interfaces, check supported OS/device combinations, layouts, safe areas, platform navigation and controls, keyboard handling, permissions, and app resume where affected. Exercise applicable platform accessibility services and settings.
6. Compare changed visuals with acceptance criteria or design references. Save screenshots for visual findings; update screenshot baselines only after reviewing the changes.

## Output and gate

- Required interactions, accessibility checks, and layouts pass.
- Platforms, browsers, OS/device and assistive-technology combinations, screen sizes, commands, results, and relevant screenshots recorded.
- Manual coverage, inapplicable checks with reasons, and platform or tool limitations listed explicitly. Missing required checks block the gate under the [shared testing rules](workflow.md#shared-execution-rules).
