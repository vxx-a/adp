# UI tests

## Scope

Test changed user interfaces in a browser, including accessibility and responsive behavior.

## Inputs

- Affected screens, user flows, acceptance criteria, and design references.
- Supported browsers and screen sizes, test accounts, and representative data.

## Steps

1. Reuse component tests for local behavior and end-to-end tests for flows across the application.
2. Verify affected interactions in a browser: navigation, forms, validation, loading, empty, error, and success states where relevant.
3. Check keyboard operation, focus movement, accessible names, and feedback for changed controls. Run existing automated accessibility checks; verify interactions manually as well.
4. Check required screen sizes and supported browsers. Look for clipped content, overflow, unreadable text, and unusable controls.
5. Compare changed visuals with acceptance criteria or design references. Save screenshots for visual findings; update screenshot baselines only after reviewing the changes.

## Output and gate

- Required interactions, accessibility checks, and layouts pass.
- Browsers, screen sizes, commands, results, and relevant screenshots recorded.
- Manual checks and browser limitations listed explicitly.
