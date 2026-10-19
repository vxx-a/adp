# TODO

Open ADP work. See [README](../README.md) for available functionality and [checks](../docs/checks.md) for local validation. Document missing steps before implementing them.

## Repo

- [ ] Extend behavioral evaluations beyond the initial setup and partial-delivery fixtures as skills encounter real project cases.

## Template

Follow the [file ownership plan](template/file-ownership.md).

- [ ] Add a version stamp under `.agents/adp/` in target projects.
- [ ] Extend setup to create or update nested `AGENTS.md` when modules need their own instructions.
- [ ] Set model and effort defaults in skill frontmatter.
- [ ] Add secret-file deny rules; settle ownership and merging of `.claude/settings.json`.

## Project start

- [ ] Decide supported languages and per-stack tool/configuration templates.
- [ ] Extend setup beyond baseline discovery with agreed per-stack configuration and CI integration.

## Development

- [ ] Select project-specific contract checks and reliable generators where canonical artifacts support them; the generic reference checker and skill catalog are implemented.

## Testing

Draft: [workflow and steps](testing/workflow.md).

- [ ] Set per-stack commands, environments, and CI gates; define critical flows and the release suite during project setup.
- [ ] Choose mutation tools, thresholds, exclusions, and applicable performance targets.
- [ ] Build the remaining testing skills from the step drafts; code review is shipped.

## Security

Drafts: [workflow](security/workflow.md), [guidelines](security/guidelines.md), [code review](security/code-review.md), [vulnerability search](security/vulnerability-search.md).

- [ ] Review the drafts; settle per-stack checks, staging attack scope, secret storage, and credential lifecycle.
- [ ] Build `adp-vulnerability-search`; select and bundle relevant Claude-Red skills. Shared guidance and `adp-security-code-review` are shipped.
- [ ] Implement security checks, dependency/image scanning, PR reports, and staging breach scenarios through CI/CD.
- [ ] Later: track, review, and incorporate Claude-Red upstream changes.

## Git

Draft: [Git policy](ci-cd/git-policy.md).

- [ ] Review the draft; settle branch protection, merge identity, release versioning, and enforcement of two independent reviewers.
- [ ] Enforce security audit and verified fixes before other PR reviews.
- [ ] Add Claude Code hooks and pre-commit checks; include module-size warnings and applicable protobuf checks (`buf lint`, `buf breaking`).

## CI/CD and ops

Drafts: [CI/CD workflow](ci-cd/workflow.md), [deployment and recovery](ci-cd/deployment.md).

- [ ] Review the drafts; choose provider, environments, commands, permissions, operational owners, and evidence retention.
- [ ] Implement candidate checks, immutable artifact builds/promotion, provenance, release records, and deployment verification using the testing and security gates.
- [ ] Implement deployment scripts, migrations, smoke checks, backups, and tested recovery; settle thresholds and recovery targets.
- [ ] Define the local dev loop with Docker Compose and observability with OpenTelemetry, health/readiness probes, and Grafana.
- [ ] Later: decide whether to add a nightly release stage after mutation testing.

## UI/UX

Drafts: [guidelines](ui-ux/guidelines.md), [workflow](ui-ux/workflow.md), [design system](ui-ux/design-system.md).

- [ ] Review the drafts and decide skill boundaries, reusing development and testing skills where appropriate.
- [ ] Ship the guidelines and build agreed skills; evaluate supported platforms, project-selected tools/services, and unavailable-tool behavior.

## Pipeline maintenance

- [ ] Build pipeline update and cleanup skills.
- [ ] Measure cost/tokens per task, rework, and production defects; add skill evals.
- [ ] Evaluate every skill against the [collaboration review cases](guidelines/agent-collaboration.md#review-cases).

## Guidelines

- [ ] Review the [human guidelines draft](guidelines/human-guidelines.md), settle its shipping path under the file ownership plan, and ship it.H
