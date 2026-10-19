---
name: adp-setup
description: Create or amend project agent instructions and establish requirements, affected implementation context, document locations, and check commands after ADP export.
---

# Setup

Read ADP's [rules](../../adp/rules.md) and [development workflow](../../adp/development.md) directly; project imports may not exist yet. Follow the rules' authorized-step boundary. Setup integrates instructions and establishes project context; stack installation and external service configuration require their own agreed scope.

1. Read the requested scope, existing `AGENTS.md`, nested instructions, `.claude/CLAUDE.md`, requirements, affected source, contracts, configuration, docs, and checks. Inspect instruction paths and parents before writing; do not edit paths resolving outside the project. An incompatible path or conflicting rule blocks dependent integration; ask rather than replace it.
2. Record the setup delta in `plan/` before editing project instructions: which files and sections need changes, discovered project facts, ADP integration, and acceptance checks. Reuse authorization for the agreed setup step; ask before changing existing project rules or expanding scope.
3. Amend existing `AGENTS.md` while preserving project rules, or create it when absent. Fill it with inspected project purpose, layout, working commands, and relevant project conventions; omit unknowns and placeholders. Keep detailed design in docs and ADP rules in ADP files. Include `@.agents/adp/rules.md` and a plain instruction to read that file when imports are unsupported. Project rules take precedence. Reuse an active integration; do not append duplicates or count imports in examples/comments as active.
4. Create or amend `.claude/CLAUDE.md` to import `@../AGENTS.md`, preserving existing tool-specific rules and avoiding duplicate imports. Create the bridge only after `AGENTS.md` exists. Do not bypass a conflict or unsafe path. ADP-owned files remain unchanged.
5. Separate required behavior from observed capabilities. Reuse canonical document locations or the workflow's defaults; create only the affected baseline. Record discrepancies and missing decisions with the work they block. Do not invent requirements or rewrite them to match defects.
6. Record usable check commands and prerequisites in existing check documentation, otherwise `docs/checks.md`. Inspect commands before running; unavailable required checks remain blockers. Do not execute live or destructive commands under setup authorization.
7. Note relevant security boundaries using [security guidance](../../adp/security.md). Check instruction integration and local documentation references; valid links alone do not establish factual accuracy.

Return instruction changes, canonical locations, affected baseline, usable checks, and unresolved decisions. Keep future behavior in `plan/`; reconcile completed setup items. Stop after setup unless the user explicitly authorized subsequent steps.
