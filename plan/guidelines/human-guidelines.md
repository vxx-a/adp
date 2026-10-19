# Human guidelines

Draft for people developing projects with ADP. The initial exporter, setup baseline, and development skills are available; stack configuration and CI enforcement remain project-specific work. The [shipping location](../template/file-ownership.md#open) for this guide is unresolved.

## Start with the project context

Keep a project description with purpose, users, flows, constraints, external systems, expected load, and success criteria. Update it when requirements change. Setup will define its location.

Export into the project root and explicitly invoke setup. Export does not create project instructions; setup creates or amends `AGENTS.md` and its Claude bridge while preserving existing rules. Review the resulting instructions and project context before development. For existing projects, inspect the affected code and docs; identify stale descriptions and unknowns without requiring a full rewrite.

Keep requirements and promises distinct from the system overview of implemented capabilities and limitations. Source and local test evidence do not establish deployed behavior.

## Give the agent a bounded task

- The behavior you want, with an example of the expected result.
- Relevant files, requirements, and existing behavior.
- What is in scope and what must stay unchanged.
- Acceptance criteria and the checks that establish success.
- Whether you want a proposal, implementation, or a review.

Resolve questions that affect correctness and record changed requirements in the description or plan.

## Review the plan, then implement

Follow the [development workflow](../development/workflow.md): plan downward from requirements through architecture and program design to implementation; verify current descriptions upward from implementation and evidence to design, architecture, and overview.

1. Ask the agent to write the concrete architecture/program-design delta in `plan/` before code edits: boundaries, responsibilities, interfaces, state, invariants, flows, failure behavior, and acceptance checks as applicable.
2. Review the behavior, affected callers and contracts, risks, and verification steps. Resolve missing requirements before implementation.
3. Authorize the bounded implementation step; agreement on a design alone does not start it. The agent implements from that design, runs checks, obtains independent review, and reconciles implemented portions into current `docs/`.
4. Review intent, the diff, evidence, and affected descriptions together. Update only views whose meaning changes; incorporate the implemented portion and retain unfinished plans. Do not change requirements to fit a defect.

The agent reports the step's result and stops unless you explicitly authorized continuation. For new projects, the order is architecture, program design, then implementation.

## Verify before accepting work

- Review the changed behavior and connected code, including callers of shared libraries or contracts.
- Require tests for new logic and regressions. Check module boundaries when a change crosses them; for UI changes, exercise the affected flow in a browser.
- Review check results and failures, including retries and checks that could not run. Passing local tests does not establish deployed behavior.
- Follow the project's [testing workflow](../testing/workflow.md). Test combined release candidates as one candidate.
- Give explicit scope for deployment, destructive operations, or changes to live systems. A request to implement code should not leave those actions ambiguous.

Keep parallel tasks in separate branches or worktrees with clear ownership. Review their integration as a single change before release.

## When development is finished

Run [development completion](../development/completion.md), specifying feature acceptance or release preparation. It checks acceptance, testing and security gates, verifies documentation reconciliation, and reports readiness or blockers.

Include the target branch or environment when requesting a merge or deployment. A ready candidate still needs the deployment workflow and checks in that environment.

## Update your installed pipeline

Updates replace `.agents/adp/` and `adp-*` skills. Put project overrides in `AGENTS.md` and use other names for project skills. Review the update diff; edits to ADP-owned files are lost.
