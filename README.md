# ADP: Agentic Development Pipeline

A reusable pipeline for building projects with coding agents. It is a set of rules, skills, and scripts that you export into a target project to make agent-driven development faster and more consistent.

## Status

Early design. The working notes are in [docs/NOTES.md](docs/NOTES.md).

## How it's meant to work

1. Clone ADP next to your project. It lives in its own repo.
2. Run the export script to copy the pipeline into the project root.
3. Run the setup skill. It asks about your goals in an interactive Q&A and adapts the pipeline to the project.
4. Develop with the bundled skills for testing, security, development, pipeline updates, and cleanup.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Rules for agents working on this repo (not the template that gets shipped) |
| `.claude/CLAUDE.md` | Points Claude Code at `AGENTS.md` |
| `docs/` | Documentation |
