# ADP rules

Rules from ADP, the Agentic Development Pipeline. `AGENTS.md` imports this file. Rules in `AGENTS.md` take precedence over these.

## Working with the user

- Follow the user's instructions. Raise conflicts or known problems before acting, with a recommended resolution. Use the [task context guide](usage.md) when shaping requirements or acceptance.
- Keep replies concise and lead with the main point. Omit repeated background and routine work narration. Keep progress updates to material changes or blockers; link supporting detail while keeping material risks and unresolved questions visible.
- Before editing, identify the authorized step: intended result, affected artifacts, design decisions, and acceptance checks. Obtain agreement for that step; existing authorization applies only to that step or an explicitly named sequence. Agreement on a design alone does not authorize implementation.
- Make routine choices within the authorized step. Keep the user informed of additions, decisions, failures, and blockers. Pause before changing scope, requirements, contracts, acceptance criteria, or agreed behavior; while waiting, continue only independent work within that step.
- Reuse existing context and authorization. Before a merge, deployment, destructive operation, or live-system change, make the result reviewable and check that authorization covers the action and target. Ask again if scope or material facts change; silence is not approval.
- Report blockers, risks, and mistakes when they affect a decision, including their impact and correction. Distinguish verified results from assumptions.
- Do not weaken checks to finish. Failed, skipped, unavailable, or inconclusive required checks cannot count as passes. Preserve earlier failures after retries.
- End with the result, checks, and unfinished work. State blockers before acceptance or authorization; link routine details. Distinguish readiness from a completed action. Keep secrets out of reports.
- Complete the step's checks and independent review, report its result, and stop before another step unless continuation was explicitly authorized. Progress messages and reviewer approval do not extend user authorization.

## Layout

- `AGENTS.md`: this project's agent rules. It imports this file.
- `.claude/`: Claude Code config. `CLAUDE.md` imports `AGENTS.md`, and `skills/` is a symlink to `.agents/skills/`.
- `.agents/`: skills and memory. `.agents/adp/` holds ADP's rules.
- `plan/`: work that isn't done yet
- `docs/`: how things work now

General plans and docs go in the root `plan/` and `docs/`. Each module keeps its in-depth plan and docs in its own `plan/` and `docs/`.

## ADP files

ADP owns the recorded root `ADP.md` guide, `.agents/adp/`, and the skills in `.agents/skills/` whose names start with `adp-`. Pipeline updates replace them, so edits there are lost. Project-owned integration and update safety follow the [installation policy](installation.md).

- Don't edit ADP's files. Changes to an ADP rule for this project go in `AGENTS.md`, once the user agrees.
- Name project skills without the `adp-` prefix.

## Workflow

1. **Design first.** Before editing code, schemas, configuration, or tests, use the shared [change-planning guidance](development.md#each-change). Record consequential design deltas in `plan/`; eligible [small changes](development.md#small-changes) need only a brief task summary. Reuse an agreed design when it already covers the work.
2. **Follow the plan.** Reconcile each implemented portion into existing `docs/` within the same scoped change. Assess design, architecture, and overview upward; update only changed meaning. Keep requirements distinct from implemented descriptions.
3. **Prune the plan.** Remove completed items. `plan/` holds what's left and `docs/` holds what exists.

Follow the shared [development workflow](development.md) for baseline discovery, canonical definitions, partial delivery, and evidence, and [collaboration policy](collaboration.md) for delegation and independent review.

## Skill routing

- At each user request, authorized phase transition, or material scope change, use the generated [skill catalog](skills.md) to select applicable skills. Users describe their goal; they do not need to name a skill.
- Match the intended result, requested mode (question, proposal, implementation, or review), current phase, and affected scope to the catalog descriptions. Load only the matching skills and their referenced guidance; a keyword or mention alone is not a match. Reuse settled decisions and use the [development workflow](development.md) for prerequisite and review order.
- Use the host's skill invocation mechanism when available. Otherwise read the linked installed `SKILL.md` and follow its procedure. Briefly state the selected skills and immediate purpose before acting.
- Apply [user authorization and stopping rules](#working-with-the-user) to every selected step. Select setup for a requested ADP integration or instruction update, not as an automatic prerequisite to unrelated work.
- If no skill applies, handle the request directly under the shared rules. Ask a focused question only when ambiguity changes the intended result or authorized scope.
- A missing or unreadable catalog or required skill is an unavailable prerequisite, not a no-match result. Report it and the affected work it blocks; do not silently bypass it or claim the skill ran.

## Code

Use [adp-coding-rules](../skills/adp-coding-rules/SKILL.md) when writing, changing, or reviewing code, alongside the project's language and formatter rules.

## Modules

- A **module** is a logical code boundary with a focused responsibility, an explicit API, and ownership of any data or state it manages. Its API can be functions, types, or an interface called in-process; it does not require a network endpoint.
- A **service** is an independently deployed runtime unit that hosts one or more modules. Modules within it share deployment, scaling, and process failure boundaries; their APIs and data ownership remain separate.
- Split modules for clear responsibilities. Keep services few; create a separate service only for a named deployment, scaling, security, or failure-isolation need. A module split or API does not require a service split.
- Packaging and remote protocols are explicit project decisions under [setup](setup.md#instructions-and-stack). Preserve existing choices; use Docker, gRPC, and protobuf only when selected for a stated need. A project without remote services needs no remote protocol.
- Modules hosted by a service share its deployment. Modules within a service can call each other's APIs in-process; do not require gRPC or protobufs for local APIs.
- Aim to keep each module under about 10k lines. Consider splitting a module that grows past that.

## Testing

Use [adp-test](../skills/adp-test/SKILL.md) with the [testing policy](testing.md) for meaningful checks, deterministic environments, project commands, and stage gates. Required tooling and thresholds are explicit project selections; missing required evidence blocks its gate.

## Security

Apply [security guidance](security.md). Every PR needs [security review](../skills/adp-security-code-review/SKILL.md) and its report before general review. Runtime attack testing requires the project's explicitly authorized staging scope.

## Operations

- When establishing or changing CI/CD, deployment, recovery, or monitoring configuration, read the [ops setup policy](ops-setup.md).
- When checking an environment's health, investigating alerts, or inspecting service and agent runs, read the [monitoring policy](monitoring.md).
- Load neither for other work.

## Host configuration

The project selects supported hosts, model and reasoning effort, tools, permissions, and cost limits during [setup](../skills/adp-setup/SKILL.md). Use supported host settings; skill metadata is routing information, not proof a host enforces configuration. Do not invent model defaults or change host settings implicitly.

## Documentation

- Keep current docs factual: boundaries, responsibilities, contracts, behavior, commands, and actual limitations. Plans hold concrete proposed changes, unresolved decisions, and remaining work. Remove repeated explanations, review histories, unnecessary examples, and evidence narratives. Keep required review reports with their changes.

## Memory

`.agents/memory/` holds what agents learn while working on this project. Its index, `.agents/memory/MEMORY.md`, is imported below. Agents that don't follow `@` imports should read it at the start of a session.

- Save one fact per file, and add a one-line pointer to it in `MEMORY.md`.
- Update an existing memory instead of adding a duplicate. Delete memories that turn out to be wrong.
- Don't save anything the repo or git history already records.

@../memory/MEMORY.md
