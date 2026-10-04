# AGENTS.md

The one source of agent instructions for this project. `.claude/CLAUDE.md` imports this file, and other tools read it directly. Put rules here, not in tool-specific config.

## Layout

- `AGENTS.md`: agent rules (this file)
- `.claude/`: Claude Code config. `CLAUDE.md` imports this file, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory
- `plan/`: work that isn't done yet
- `docs/`: how things work now

General plans and docs go in the root `plan/` and `docs/`. Each module keeps its in-depth plan and docs in its own `plan/` and `docs/`.

## Workflow

1. **Plan first.** Write the plan in `plan/` before writing code. Use one file per scope or module.
2. **Follow the plan.** Document what you build in `docs/`, with one file per scope or module.
3. **Prune the plan.** Remove completed items. `plan/` holds what's left and `docs/` holds what exists.

## Code

- Write self-explanatory, well-named code. Only add a comment when the code can't carry the context itself.
- Reuse shared libraries and protobufs instead of repeating code.
- Follow these guidelines strictly. If a rule blocks you, raise it. Don't work around it.

## Modules

- Dockerize each module.
- Modules talk over gRPC, with contracts defined in shared protobufs.
- Aim to keep each module under about 10k lines. Consider splitting a module that grows past that.

## Testing

- Write unit tests for all new logic.
- Run mutation testing on a separate branch or worktree created from the current one.

## Security

- Run security audits and penetration testing.

## Reasoning

- Use lower reasoning effort with larger, richer prompts. Save higher reasoning for when context is thin.

## Documentation

- Write for human reviewers first. Keep it short and current, and delete anything stale.

## Memory

`.agents/memory/` holds what agents learn while working on this project. Its index, `MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@.agents/memory/MEMORY.md
