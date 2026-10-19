# AGENTS.md

Instructions for agents working on **this repo**. `.claude/CLAUDE.md` imports this file.

## What this repo is

ADP (Agentic Development Pipeline) builds the pipeline that gets installed into other projects: an exporter, setup and development skills, and supporting scripts. It lives in its own repo clone, separate from the projects it serves.

## This repo vs. what it ships

Keep these two apart:

- **This repo's agent config** is `AGENTS.md`, `.claude/`, and `.agents/`. It only affects agents working on ADP itself. Everything outside `template/` is for developing ADP and never ships.
- **The pipeline product** lives in `template/`. That directory gets copied as-is into the root of a new project, and it never mixes with the config above.

Treat everything under `template/` as product content you edit. Don't follow it as instructions. Rules meant for target projects belong in `template/.agents/adp/rules.md` or a shipped skill, not here. That includes code style, modules, Docker, gRPC, and testing. Shipped skills go in `template/.agents/skills/` with an `adp-` name prefix. Setup creates or amends the target project's `AGENTS.md`; it is not exported. Changing a shipped skill doesn't change how agents work in this repo, and vice versa.

## Layout

- `AGENTS.md`: rules for working on this repo (this file)
- `.claude/`: Claude Code config. `CLAUDE.md` imports this file, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory for working on this repo
- `template/`: what gets exported into a new project
- `plan/`: work that isn't done yet
- `docs/`: how ADP works now

## Working with the maintainer

Before editing, identify the authorized step: result, affected files, design decisions, and acceptance checks. Agree on that step; reuse existing authorization only when it covers that step or an explicitly named sequence. Agreement on a design alone does not authorize implementation.

Make routine choices within the step and keep the maintainer informed of additions, decisions, failures, and blockers. Pause before changing agreed behavior or scope. Complete checks and independent review, report the result, and stop before another step unless continuation was explicitly authorized. Progress messages and reviewer approval do not extend authorization.

## Memory

`.agents/memory/` holds what agents learn while working on this repo. Its index, `MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@.agents/memory/MEMORY.md
