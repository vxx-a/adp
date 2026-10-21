# Agentic Development Pipeline

Rules, skills, and scripts installed into a project and run by its existing coding agent.
## Use

*Requires Python 3.10 or newer*

1. Preview the content changes and install:

   ```sh
   python3 /path/to/adp/export.py /path/to/project --diff
   python3 /path/to/adp/export.py /path/to/project --apply
   ```

   Use the same commands from a trusted updated checkout to update. Review its [changelog](product/CHANGELOG.md) and [installation, recovery, and uninstall instructions](product/adp/installation.md).
2. Ask your coding agent: "Set up ADP for this project." It uses `adp-setup` to create or amend project instructions, move existing `CLAUDE.md` rules and `.claude/skills/` skills into `AGENTS.md` and `.agents/skills/`, and establish requirements, affected project context, document locations, and check commands. If the host cannot discover installed skills, ask it to read `.agents/skills/adp-setup/SKILL.md` for this initial setup.
3. Describe the result you want, such as "Plan this feature," "Implement the approved plan," or "Review this PR." Once setup integrates the shared rules, the agent [routes the request](product/adp/rules.md#skill-routing) to the relevant [skills](product/adp/skills.md); you do not need to name them.

Read [human usage guide](product/USAGE.md) before starting work.

## Features
#### Development
Architecture: system boundaries, data ownership, dependencies, shared technical decisions.
Program design: components, contracts, state, invariants, interactions, failure behavior.
Code: scoped changes and bug fixes under ADP coding rules, with docs kept current.
Review: independent check of correctness, tests, and agreement between requirements, code, and docs.
Completion: verifies acceptance, review, and docs before work is done.
#### Testing
Selects, writes, and runs unit, integration, contract, end-to-end, UI, performance, mutation, and static checks.
#### Security
Security code review of PRs and changes, before general review.
Vulnerability search against authorized isolated staging targets; verifies security fixes.
#### UI/UX
Designs, implements, and evaluates web and native interfaces for user tasks, accessibility, and existing visual direction. Basic design guidelines. 
#### Git and release
Inspired by git flow.
Commits, pull requests, and merges.
Release preparation, qualification, publishing, deployment, and environment recovery.
#### Operations
Basic ops setup: CI/CD, Git protection, deployment, recovery, and monitoring.
Monitoring: read-only inspection of environments, alerts, incidents, and service or agent runs.

## Documentation

- [Checks](#checks): local commands and supported reference syntax.
- [Operations policies](docs/operations.md): CI/CD and ops setup, service and agent monitoring, and implementation limits.
- [Skill evaluations](docs/evaluations.md): disposable projects, behavioral checks, and host verification limits.
- [Product and export boundary](docs/product.md): canonical sources, ownership, and shipped capabilities.

## Checks

Requires Python 3.10 or newer; no third-party packages.

From the ADP checkout:

```sh
python3 -B scripts/check.py
git diff --check
```

The aggregate command runs tests. After editing skill metadata, regenerate the catalog with `python3 -B scripts/build_catalog.py`.

In an installed project, run `python3 .agents/adp/scripts/check_docs.py --root .`, optionally followed by selected files or directories.

### Reference syntax and limits

- Default selections: existing README, AGENTS, docs, plan, and `.agents`. Explicit missing inputs and empty selections fail.
- Supports local inline/image/reference links, headings, explicit HTML identifiers, and source lines. Repeated reference labels use their first definition.
- Leading `/` means the selected project root. Escaping symlinks and unreadable selected trees fail. Discovery skips symlinked child directories.

## License

[MIT](LICENSE). Installed copies include the notice at `.agents/adp/LICENSE`.
