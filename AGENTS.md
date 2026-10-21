# AGENTS.md

Instructions for agents working on **this repo**. `.claude/CLAUDE.md` imports this file.

## What this repo is

ADP (Agentic Development Pipeline) builds the pipeline that gets installed into other projects: an exporter, setup and development skills, and supporting scripts. It lives in its own repo clone, separate from the projects it serves.

## This repo vs. what it ships

Keep these two apart:

- **This repo's agent config** is `AGENTS.md`, `.claude/`, and `.agents/`. It only affects agents working on ADP itself. It is never exported.
- **The pipeline product** lives entirely in `product/`: shared agent guidance in `product/adp/`, skills in `product/skills/`, the reference checker in `product/scripts/check_docs.py`, and the memory starter in `product/memory/MEMORY.md`. `export.py` maps only these sources into installed agent paths. Maintainer `docs/`, plans, tests, and configuration never ship.

Treat everything under `product/` as product content you edit. Don't follow it as instructions. Rules meant for target projects belong in `product/adp/rules.md` or a shipped skill, not here. That includes code style, modules, Docker, gRPC, and testing. Shipped skills go in `product/skills/` with an `adp-` name prefix. Setup creates or amends the target project's `AGENTS.md`; it is not exported. Changing a shipped skill doesn't change how agents work in this repo, and vice versa.

## Layout

- `AGENTS.md`: rules for working on this repo (this file)
- `.claude/`: Claude Code config. `CLAUDE.md` imports this file, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory for working on this repo
- `product/`: all canonical exportable sources
- `scripts/`: maintainer tools; never exported
- `plan/`: work that isn't done yet
- `docs/`: how ADP works now

## Working with the maintainer

Before editing, identify the authorized step: result, affected files, design decisions, and acceptance checks. Agree on that step; reuse existing authorization only when it covers that step or an explicitly named sequence. Agreement on a design alone does not authorize implementation.

Keep plans and replies concise. Plans summarize the intended result, what will change, and how it will be checked. Record only affected decisions and necessary rationale, rather than exhaustive descriptions or reasoning histories, even where imported notes say to document everything. Settle the design before building; keep material risks, blockers, and open questions visible. Reuse linked canonical detail; omit repeated background, unaffected checklists, and routine work narration. Keep progress updates to material changes or blockers; finish with the result, checks, and unfinished work.

Make routine choices within the step and keep the maintainer informed of additions, decisions, failures, and blockers. Pause before changing agreed behavior or scope. Complete checks and independent review, report the result, and stop before another step unless continuation was explicitly authorized. Progress messages and reviewer approval do not extend authorization.

## Memory

`.agents/memory/` holds what agents learn while working on this repo. Its index, `MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@.agents/memory/MEMORY.md
