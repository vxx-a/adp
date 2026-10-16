# ADP: Agentic Development Pipeline

A reusable pipeline for building projects with coding agents. It is a set of rules, skills, and scripts that you export into a target project to make agent-driven development faster and more consistent.

## Scope

ADP equips the coding agent you already work with to initialize a project and run the skills you request. Each skill supplies the rules, inputs, and outputs for its step. For example, the agent reads the architecture skill to learn how to design the project's architecture.

The shipped product lives in `template/`: project rules, skills, supporting files, and human guidelines for people using ADP in their projects. Human guidelines explain how to develop those projects with ADP.

Work on ADP itself uses this repo's root `AGENTS.md`, `.agents/`, and `.claude/`. Root `plan/` holds product drafts and development plans; root `docs/` describes ADP's design and implementation. These directories are not exported into target projects.

## Status

Early design. The working notes are in [docs/NOTES.md](docs/NOTES.md).

Review the [human guidelines draft](plan/guidelines/human-guidelines.md) for people using ADP in their own projects. Once agreed, it will ship under `template/docs/`.

## How it's meant to work

1. Clone ADP next to your project. It lives in its own repo.
2. Run the export script to copy the pipeline into the project root.
3. Ask your agent to run the setup skill. It asks about your goals in an interactive Q&A and adapts the pipeline to the project.
4. Ask your agent to run the relevant bundled skills for testing, security, development, pipeline updates, and cleanup.

## Layout

| Path | Purpose |
|---|---|
| `AGENTS.md` | Rules for agents working on this repo (not the template that gets shipped) |
| `.claude/CLAUDE.md` | Points Claude Code at `AGENTS.md` |
| `.agents/` | Skills and memory for working on ADP itself |
| `template/` | What gets exported into a new project's root |
| `plan/` | Product drafts and plans for developing ADP |
| `docs/` | ADP design and implementation documentation |
