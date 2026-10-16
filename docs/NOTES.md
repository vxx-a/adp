# Notes

## Testing

- [Testing workflow](../plan/testing/workflow.md): commit and release gates; individual plans for each testing step.

## Security

- claude-red
- Pre-release penetration testing

## Development

- [Development completion](../plan/development/completion.md): next step after development; feature acceptance, release readiness, and deployment handoff.
- First write docs for a plan, under `/plan`. Then follow the plan and document the codebase in `/docs`. Remove done items from the plan. Separate plan per scope or module, same for docs. General docs and plan in root, in depth per module.
- Code should be self-explanatory and well defined. Comments only when code needs more context.
- Prioritize lower reasoning with larger, richer prompts. Higher reasoning for less context.
- Shared libs and protobufs; minimize code repetition.
- Strict guidelines.
- Do not rely on fallbacks.
- No repetitions.
- Explicit class design and diagrams showing interaction.
- Readability, explicit naming of everything. (no o, t, p, etc..), use full words when mostly, shorten when it is completely clear what the short name implies. minimize comments.

## CI/CD

- Deployment scripts
- Testing
- Production / pre-production / development
- Future option: a nightly release stage after mutation testing, before full release. Decide later.

## Modules

- Dockerized
- Each module up to ~10k lines (a guideline, not a hard limit)
- gRPC communication
- Protobufs

## Project start

- Export script to project root
- Setup skill: interactive Q&A, goals, description

## Skills

- Testing skills: follow the [individual testing plans](../plan/testing/workflow.md#testing-steps).
- Security skill
  - Audit
- Development skills
- Project setup skill
  - Adjust for specific project needs
- Pipeline update skill
- Cleanup skill
## GIT
#### Pull requests
- review pull requests and merge
- run 2 independent reviewers on proposed changes
#### Branches
- release / main
- dev 
- feature-\[name]
- `<dev-branch>-mutation-testing`: one per dev branch; merge back into its source after checks pass
- Combined dev branches must pass checks as one release candidate before merging into release

## Documentation

- Keep clean, for human reviewers primarily

## UI/UX

- Figma
- react + tailwind
- react native
- typeui
- [aiux](https://www.aiuxplayground.com/skills)

## Pipeline

- One `AGENTS.md`, `.claude` pointing to it
- `.agents/` for skills, memory
- Pipeline should live under separate repo clone
- Versioning

## Guidelines
- [Human guidelines draft](../plan/guidelines/human-guidelines.md): product guidance for ADP users developing their own projects; intended to ship under `template/docs/`.

## Monitoring
- grafana

## OPS
- Include monitoring, ci/cd etc

## Gaps and ideas

### Biggest gaps

- **Enforce rules with checks.** Agents drift from rules that are only written down. Back each hard rule with a check: Claude Code hooks (lint/format after each edit, tests when the agent finishes), pre-commit, and CI (warn when a module grows past ~10k lines). If a rule isn't checked, it's a suggestion.
- **Definition of done.** Give agents a clear finish line: tests pass, mutation score of at least X on changed code, lint clean, docs updated, plan item removed.
- **Keep the "why".** Removing done items from `plan/` loses the reasons behind decisions. Add short decision records in `docs/decisions/`.
- **Setup vs update conflict.** Setup customizes the exported files and update overwrites them. Split the files into pipeline-owned (replaced on update) and project-owned (never touched), and put a version stamp in each target project. This is where versioning becomes concrete.
- **Measure efficiency.** Track cost/tokens per task, rework rate and bugs that reach production, so pipeline changes are judged on data. Add evals for skills.

### Stack

- `buf lint` and `buf breaking` in CI to catch contract changes that break existing clients
- Integration or contract tests between modules; unit and mutation tests won't catch one module breaking another
- Secrets: block agent access to `.env` and secret files in `.claude/settings.json`, and pick a secrets approach for deployments
- Supply chain: dependency and container image scanning (Renovate, Trivy)
- Observability: logs, metrics, tracing (OpenTelemetry), health/readiness probes
- Fast local dev loop: docker compose
- Environments (dev/staging/prod), rollback in the deploy scripts, pentests against staging only
- Language-agnostic or not? Mutation tools, linters and shared libs are per-language, so the setup skill needs templates for each stack

### Agents

- Claude Code loads skills from `.claude/skills/`, so symlink it to `.agents/skills`. Memory in `.agents/memory` must be referenced from `AGENTS.md` or it won't load.
- A nested `AGENTS.md` per module, picked up when an agent works in that folder
- Human checkpoints: approve the plan before implementation, review the PR
- Concrete model and effort defaults per skill or agent, set in their frontmatter
- One plan file per scope, each with its own worktree and agent, so work runs in parallel
