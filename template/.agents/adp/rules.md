# ADP rules

Rules from ADP, the Agentic Development Pipeline. `AGENTS.md` imports this file. Rules in `AGENTS.md` take precedence over these.

## Working with the user

- Follow the user's instructions. Raise conflicts or known problems before acting, with a recommended resolution.
- Before editing, identify the authorized step: intended result, affected artifacts, design decisions, and acceptance checks. Obtain agreement for that step; existing authorization applies only to that step or an explicitly named sequence. Agreement on a design alone does not authorize implementation.
- Make routine choices within the authorized step. Keep the user informed of additions, decisions, failures, and blockers. Pause before changing scope, requirements, contracts, acceptance criteria, or agreed behavior; while waiting, continue only independent work within that step.
- Reuse existing context and authorization. Before a merge, deployment, destructive operation, or live-system change, make the result reviewable and check that authorization covers the action and target. Ask again if scope or material facts change; silence is not approval.
- Report blockers, risks, and mistakes when they affect a decision, including their impact and correction. Distinguish verified results from assumptions.
- Do not weaken checks to finish. Failed, skipped, unavailable, or inconclusive required checks cannot count as passes. Preserve earlier failures after retries.
- End with the result, checks, and unfinished work. State blockers before acceptance or authorization; link routine details. Distinguish readiness from a completed action. Keep secrets out of reports.
- Complete the step's checks and independent review, report its result, and stop before another step unless continuation was explicitly authorized. Progress messages and reviewer approval do not extend user authorization.

## Layout

- `AGENTS.md`: this project's agent rules. It imports this file.
- `.claude/`: Claude Code config. `CLAUDE.md` imports `AGENTS.md`, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory. `.agents/adp/` holds ADP's rules.
- `plan/`: work that isn't done yet
- `docs/`: how things work now

General plans and docs go in the root `plan/` and `docs/`. Each module keeps its in-depth plan and docs in its own `plan/` and `docs/`.

## ADP files

ADP owns `.agents/adp/` and the skills in `.agents/skills/` whose names start with `adp-`. Pipeline updates replace them, so edits there are lost. Everything else belongs to this project, and updates never touch it.

- Don't edit ADP's files. Changes to an ADP rule for this project go in `AGENTS.md`, once the user agrees.
- Name project skills without the `adp-` prefix.

## Workflow

1. **Design first.** Before editing code, schemas, configuration, or tests, write the concrete architecture and program-design delta in `plan/`. Define affected boundaries, owners, responsibilities, interfaces, state, invariants, flows, failure behavior, and acceptance checks. Include only what changes; reuse an agreed design when it already covers the work. A task list alone is not a design.
2. **Follow the plan.** Reconcile each implemented portion into existing `docs/` within the same scoped change. Assess design, architecture, and overview upward; update only changed meaning. Keep requirements distinct from implemented descriptions.
3. **Prune the plan.** Remove completed items. `plan/` holds what's left and `docs/` holds what exists.

Follow the shared [development workflow](development.md) for baseline discovery, canonical definitions, independent review, partial delivery, and evidence. One owner maintains each scope; reviewers challenge consequential decisions and verify the resulting implementation independently. Use the generated [skill catalog](skills.md) to select the relevant step.

## Code

Use [adp-coding-rules](../skills/adp-coding-rules/SKILL.md) when writing, changing, or reviewing code, alongside the project's language and formatter rules.

## Modules

- Dockerize each module.
- Modules talk over gRPC, with contracts defined in shared protobufs.
- Aim to keep each module under about 10k lines. Consider splitting a module that grows past that.

## Testing

- Write unit tests for all new logic.
- Keep tests isolated and deterministic: control clocks (date, month, DST), time zones, locale, randomness, environment settings, and external dependencies. Use fresh test data and cleanup; results must not depend on test order, parallel runs, or host state. Synchronize on events or readiness instead of fixed sleeps.
- When the project's gate requires mutation testing, run it on a separate branch or worktree created from the current one. Missing required tooling remains an unavailable check; do not apply release-only checks to unrelated bounded work.

## Security

Apply [security guidance](security.md). Every PR needs [security review](../skills/adp-security-code-review/SKILL.md) and its report before general review. Runtime attack testing requires the project's explicitly authorized staging scope.

## Reasoning

- Use lower reasoning effort with larger, richer prompts. Save higher reasoning for when context is thin.

## Documentation

- Keep current docs factual: boundaries, responsibilities, contracts, behavior, commands, and actual limitations. Plans hold concrete proposed changes, unresolved decisions, and remaining work. Remove repeated explanations, review histories, unnecessary examples, and evidence narratives. Keep required review reports with their changes.

## Memory

`.agents/memory/` holds what agents learn while working on this project. Its index, `.agents/memory/MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@../memory/MEMORY.md
