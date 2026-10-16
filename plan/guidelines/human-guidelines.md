# Human guidelines

Audience: people using ADP to develop their own projects with a coding agent.

This is a product draft, kept in `plan/` for review. Once agreed, ship it as `template/docs/human-guidelines.md`. ADP is in early design: export, setup, and the bundled skills describe the intended workflow and are not implemented yet.

## Start with the project context

Write down the project's purpose, users, main flows, constraints, external systems, expected load, and what success means. Keep this project description current when requirements change. Its location will be decided as part of setup.

Once export and setup exist, export the pipeline into the project root and ask your agent to run setup. Review the resulting rules and project description before starting development. For an existing project, include its current architecture, conventions, and working test commands.

## Give the agent a bounded task

Each task should include:

- The behavior you want, with an example of the expected result.
- Relevant files, requirements, and existing behavior.
- What is in scope and what must stay unchanged.
- Acceptance criteria and the checks that establish success.
- Whether you want a proposal, implementation, or a review.

For example:

> Plan password reset for the existing sign-in flow. Read the current auth code and rules. Cover expired and reused links. Keep registration unchanged. Write the plan and list any missing decisions before implementing.

Answer questions that affect correctness. If requirements change, update the project description or plan so the next agent sees the same decision.

## Review the plan, then implement

1. Ask the agent to write the plan in `plan/`, using one file per scope or module.
2. Review the behavior, affected callers and contracts, risks, and verification steps. Resolve missing requirements before implementation.
3. Ask the agent to implement the agreed scope and run the relevant checks.
4. Review the diff and results. Update `docs/` to describe what exists, then remove completed work from `plan/`. Keep lasting decisions and their reasons in the documentation.

For a new project, ask your agent to run the architecture skill, then proceed to program design and implementation. Architecture covers responsibilities, data ownership, dependencies, and shared technical decisions. Program design defines contracts and internal structure.

## Verify before accepting work

- Review the changed behavior and connected code, including callers of shared libraries or contracts.
- Require tests for new logic and regressions. Check module boundaries when a change crosses them; for UI changes, exercise the affected flow in a browser.
- Ask for the commands run, their results, and any skipped or blocked checks. Passing local tests does not establish deployed behavior.
- Ask your agent to follow your project's testing and release rules. Mutation testing runs on a branch tied to its source dev branch, and a combined release candidate needs checks on the combined code.
- Give explicit scope for deployment, destructive operations, or changes to live systems. A request to implement code should not leave those actions ambiguous.

Keep parallel tasks in separate branches or worktrees with clear ownership. Review their integration as a single change before release.

## When development is finished

Ask your agent to follow the [development completion plan](../development/completion.md). State whether you want to accept a feature or prepare a release candidate. The agent reviews completion, runs the applicable gates, updates the documentation, and reports readiness or blockers. Release preparation also includes mutation testing and required security checks.

Include the target branch or environment when requesting a merge or deployment. A ready candidate still needs the deployment workflow and checks in that environment.

## Update your installed pipeline

Before updating an installed pipeline, review the diff against that project's customizations. Ownership of exported files and the update process are still unresolved; do not assume replacing files preserves local changes.
