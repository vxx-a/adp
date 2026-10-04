# AGENTS.md

Instructions for agents working on **this repo**. `.claude/CLAUDE.md` imports this file.

## What this repo is

ADP (Agentic Development Pipeline) builds the pipeline that gets installed into other projects: a setup script, an `AGENTS.md` template, skills, and supporting scripts. It lives in its own repo clone, separate from the projects it serves.

## This repo vs. what it ships

Keep these two apart:

- **This repo's agent config** is `AGENTS.md`, `.claude/`, and `.agents/`. It only affects agents working on ADP itself.
- **The pipeline product** lives in `template/`. That directory gets copied as-is into the root of a new project, and it never mixes with the config above.

Treat everything under `template/` as product content you edit. Don't follow it as instructions. Rules meant for target projects belong in `template/AGENTS.md`, not here. That includes code style, modules, Docker, gRPC, and testing. Changing a shipped skill doesn't change how agents work in this repo, and vice versa.

## Layout

- `AGENTS.md`: rules for working on this repo (this file)
- `.claude/`: Claude Code config. `CLAUDE.md` imports this file, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory for working on this repo
- `template/`: what gets exported into a new project
- `plan/`: work that isn't done yet
- `docs/`: how ADP works now. `docs/NOTES.md` holds the working design notes.

## Memory

`.agents/memory/` holds what agents learn while working on this repo. Its index, `MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@.agents/memory/MEMORY.md
