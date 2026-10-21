---
name: adp-setup
description: Integrate installed ADP with project instructions and existing Claude rules/skills; establish project context, stack checks, and authorized host configuration without overwriting project ownership.
---

# Setup

Read [rules](../../adp/rules.md), [development](../../adp/development.md), [installation ownership](../../adp/installation.md), and [setup decisions](../../adp/setup.md) directly; imports may not exist yet. Setup establishes context and instruction integration. Installing tools, changing CI/host permissions, or configuring external services requires the corresponding authorized scope.

1. Inspect requested scope, project instructions (including nested files), root `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/skills`, requirements, affected source/configuration/docs, and checks. Inspect path parents and symlinks before writing; never write through a path outside the project. Conflicting rules or unsafe paths block dependent changes.
2. Record the setup delta in `plan/`: changed files/sections, rules/skills to migrate, discovered facts, project selections, and acceptance checks. Reuse existing setup authorization; ask before changing existing rules or expanding scope.
3. Amend or create `AGENTS.md` with inspected purpose, layout, working commands, relevant conventions, and requirement/doc locations; preserve project rules and omit unknown placeholders. Keep detailed design in docs. Include one active `@.agents/adp/rules.md` import plus an instruction to read it when imports are unsupported. Project rules take precedence. Do not count examples/comments as integration. Add justified nested instructions under the setup policy.
4. Make `AGENTS.md` canonical without losing Claude rules:
   - If instruction files link to one another, first make `AGENTS.md` a regular file preserving its content. Remove instruction symlinks before replacement; never write through them.
   - Merge project rules from root `CLAUDE.md` and `.claude/CLAUDE.md` into `AGENTS.md`, rebasing relative links and `@` imports from the project root. Resolve conflicts before moving affected rules.
   - Only after every rule is moved or decided, leave `.claude/CLAUDE.md` containing `@../AGENTS.md` and remove root `CLAUDE.md`. Until then preserve both. Leave local/nested Claude files and unrelated `.claude` configuration in place.
5. Migrate a real `.claude/skills/` directory safely. Inspect each skill's relative links, resources, command working directory, and symlinks, including outside-skill references. Rebase these inside the moved skill to preserve intended resolution; leave unrelated resources in place. An escaping/missing path, ambiguous command context, destination conflict, `adp-` name, or non-skill entry blocks that move before mutation. Move safe skills to `.agents/skills/` under the same name (`git mv` when tracked); verify resources/commands within authorized check scope. Replace the discovery directory with `../.agents/skills` only once empty. Preserve an existing correct link; do not bypass an incompatible one.
6. Establish only the affected requirements and current baseline, keeping required behavior distinct from implemented capabilities. Complete the setup policy's project selections within scope, including packaging/remote protocols and UI accessibility where applicable; record missing decisions with the work they block. Use [ops setup](../adp-ops-setup/SKILL.md) or [UI/UX](../adp-ui-ux/SKILL.md) only when their work is requested. Keep ADP-owned files unchanged.
7. Inspect commands before running. Check instruction imports, preserved rules/resources, discovery, relevant local references, and selected project checks. Unavailable required checks block their gate; do not run live/destructive commands as setup checks. State whether the host actually discovered/invoked the skills; a correct symlink alone does not prove it.

Return changed instructions/configuration, moved rules/skills, canonical locations, project commands/selections, checks, and unresolved decisions. Reconcile completed setup items, preserve unfinished work, and stop at the authorized boundary.
