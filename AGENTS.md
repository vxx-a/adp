# AGENTS.md

Instructions for agents working on **this repo**. `.claude/CLAUDE.md` imports this file.

## What this repo is

ADP (Agentic Development Pipeline) builds the pipeline that gets installed into other projects: a setup script, an `AGENTS.md` template, skills, and supporting scripts. It lives in its own repo clone, separate from the projects it serves.

## This repo vs. what it ships

Keep these two apart:

- **This repo's agent config** is `AGENTS.md`, `.claude/`, and `.agents/`. It only affects agents working on ADP itself.
- **The pipeline product** is the `AGENTS.md`, skills, memory layout, and setup that get copied into target projects. It isn't written yet. When it is, it gets its own directory and never mixes with the config above.

Rules meant for target projects belong in the shipped `AGENTS.md`, not here. That includes code style, modules, Docker, gRPC, and testing. Changing a shipped skill doesn't change how agents work in this repo, and vice versa.

## Layout

- `AGENTS.md`: rules for working on this repo (this file)
- `.claude/`: Claude Code config. `CLAUDE.md` imports this file, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory for working on this repo
- `plan/`: work that isn't done yet
- `docs/`: how ADP works now. `docs/NOTES.md` holds the working design notes.
