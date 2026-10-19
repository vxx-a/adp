# ADP: Agentic Development Pipeline

Rules, skills, and scripts installed into a project and run by its existing coding agent. Only `template/` is exported.

## Use

1. Clone ADP next to your project.
2. Preview `python3 export.py /path/to/project`, then apply with `--apply`. Export preserves existing project files and rejects differing installed ADP files; updates are not implemented.
3. Explicitly invoke `adp-setup`. It creates or amends project instructions and establishes requirements, affected project context, document locations, and check commands.
4. Use the relevant [skill](template/.agents/adp/skills.md) for the agreed step. One owner coordinates; independent reviewers inspect decisions and results.

The [workflow](template/.agents/adp/development.md) requires concrete design in `plan/` before code changes. Current docs describe implemented behavior. Work stops at the authorized step boundary unless continuation was explicitly authorized.

## Documentation

- [Checks](docs/checks.md): local commands and supported reference syntax.
- [Plans](plan/TODO.md): remaining work and decisions.

Root `AGENTS.md`, `.claude/`, and `.agents/` configure agents developing ADP. Root `docs/`, `plan/`, `scripts/`, and `tests/` do not ship. The [human guide](plan/guidelines/human-guidelines.md) remains a draft with its shipping location undecided.
