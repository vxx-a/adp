# TODO

What's done and what's left for ADP. Each step gets notes in `plan/<feature>/<step>.md` before its skill is built. Sources: `docs/NOTES.md` and the plans under `plan/`.

## Repo

- [x] Repo scaffolding: `AGENTS.md`, `.claude/`, `.agents/`, `plan/`, `docs/`
- [x] Repo memory index and first memories
- [x] README and working notes (`docs/NOTES.md`)
- [x] Ignore `.DS_Store`
- [ ] `docs/`: describe how ADP works once pieces are built (only `NOTES.md` so far)
- [ ] Decision records in `docs/decisions/`

## Template (shipped product)

- [x] `template/AGENTS.md`, `template/.claude/CLAUDE.md`, `skills/` symlink, memory index
- [ ] Replace the Code section of `template/AGENTS.md` with a pointer to the coding-rules skill
- [ ] Split files into pipeline-owned (replaced on update) and project-owned (never touched)
- [ ] Version stamp in each target project
- [ ] Nested `AGENTS.md` per module
- [ ] Model and effort defaults in each skill's frontmatter
- [ ] Block agent access to `.env` and secret files in `.claude/settings.json`

## Project start

- [ ] Export script: copy `template/` into a project root
- [ ] Setup notes (`plan/setup/`)
  - [ ] Interactive Q&A: goals, description
  - [ ] Where the project description file lives (open in architecture notes)
  - [ ] Per-stack templates: formatter, linter, test commands, mutation tool
  - [ ] Language-agnostic or not
- [ ] Setup skill

## Development

- [x] Architecture notes (`plan/development/architecture.md`)
- [ ] Architecture skill
- [ ] Program design notes: gRPC services, protobufs, layers, class design and interaction diagrams
- [ ] Program design skill
- [ ] Implementation notes: plan first, document, prune the plan
- [ ] Implementation skill
- [x] Coding rules notes (`plan/development/coding-rules.md`)
- [ ] Coding rules skill
- [x] Completion notes (`plan/development/completion.md`)
  - [x] Point to the testing and security gates instead of restating their steps
- [ ] Completion skill
- [ ] Definition of done for development: acceptance criteria met, docs updated, plan item removed

## Testing

- [x] Workflow and gates (`plan/testing/workflow.md`)
- [x] Step notes: unit, integration, contract, end-to-end, UI, performance, mutation, static checks, code review
- [ ] Decide before implementation
  - [ ] Commands, environments, CI gates per stack
  - [ ] Critical flows and release suite
  - [ ] Mutation tool, threshold, allowed exclusions
  - [ ] Performance targets
- [ ] Testing skills, one per step
- [ ] Two independent reviewers on proposed changes

## Security

- [ ] Security notes (`plan/security/`)
  - [ ] Audit: code, dependency, image, secret checks
  - [ ] claude-red
  - [ ] Check commands and blocking policy
  - [ ] Pre-release penetration testing: scope, staging only
  - [ ] Supply chain scanning (Renovate, Trivy)
  - [ ] Secrets approach for deployments
- [ ] Security skill

## Git

- [ ] Git notes: branches (release/main, dev, feature-name, mutation branches), PR review and merge
- [ ] Enforce rules with checks: Claude Code hooks, pre-commit, CI (module size warning, `buf lint`, `buf breaking`)

## CI/CD and ops

- [ ] CI/CD notes: deploy scripts, environments (dev, staging, prod), rollback
  - [ ] Release merge, deploy, smoke-check, monitoring, rollback per environment
- [ ] Decide on a nightly release stage after mutation testing
- [ ] Local dev loop with docker compose
- [ ] Observability: logs, metrics, tracing (OpenTelemetry), health and readiness probes, Grafana

## UI/UX

- [ ] UI/UX notes: Figma, React + Tailwind, React Native, typeui, aiux skills

## Pipeline maintenance

- [ ] Pipeline update skill
- [ ] Cleanup skill
- [ ] Measure efficiency: cost and tokens per task, rework rate, bugs reaching production
- [ ] Evals for skills

## Guidelines

- [x] Human guidelines draft (`plan/guidelines/human-guidelines.md`)
- [ ] Review and agree on the draft
- [ ] Ship it as `template/docs/human-guidelines.md`
