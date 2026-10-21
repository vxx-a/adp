# Development workflow

## Definitions

| Artifact | Canonical information |
|---|---|
| Requirements and acceptance criteria | Required behavior, constraints, external promises |
| Code, schemas, configuration | Executable definitions and implemented behavior |
| Program design | Components, interactions, state, contract semantics, failure guarantees |
| Architecture | Module boundaries, service deployment and module placement, data ownership, dependencies, shared decisions |
| Overview | Implemented capabilities, major flows, limitations |

Keep one canonical definition and use linked summaries. Requirements and current descriptions have different roles even if they share a document. Schemas do not express every semantic guarantee; keep missing semantics with the owning contract or design. Keep lasting rationale with its decision.

Use the shared [module and service definitions](rules.md#modules); a module API does not imply a separate deployment.

Plan downward from requirements through architecture and program design to code. Verify current descriptions upward from implementation and evidence through design and architecture to overview. This is a verification path, not permission for code to override obligations.

## Baseline and files

- Inspect affected source, contracts, configuration, callers, checks, and current docs. Record disagreements and unknowns rather than trusting existing descriptions or inventing requirements.
- Reuse project locations. Otherwise use `docs/requirements.md`, `docs/overview.md`, `docs/architecture.md`, and module `docs/design.md`. Create only needed documents; use root `docs/design.md` for a project without modules.
- `plan/` holds proposed deltas and unfinished work. Maintain current design in existing `docs/` files. Requirements are explicit obligations; they need not already be implemented to be recorded there.
- General design goes at the project root; detailed module design stays with its owner. Link shared definitions instead of copying them.
- Establish missing docs as an area changes; no whole-project rewrite is required. New capabilities remain proposed until implemented.
- Distinguish source evidence from behavior verified in a named environment. Defaults and local tests do not prove deployed configuration, migrations, or live behavior.

## Each change

1. Identify affected requirements, components, contracts, callers, guarantees, and documentation.
2. Classify the change using [small changes](#small-changes). Otherwise, before editing code, schemas, configuration, or tests, write a concise change summary in `plan/`: intended result, what will change, and acceptance checks. Include only affected design decisions and necessary rationale to settle behavior, boundaries, ownership, contracts, state, invariants, flows, and failure policy. Keep material risks, blockers, and unresolved decisions visible. Reuse settled design and link canonical detail; omit repeated background, unaffected checklist sections, and routine implementation steps. Do not create extra documents merely to move detail out of the summary. A summary must still settle the design needed for the authorized portion; a task list alone is insufficient.
3. Agree on the step under [user involvement](rules.md#working-with-the-user). Design-only agreement does not authorize implementation. During implementation, put exact definitions in API declarations, schemas, constraints, and configuration as applicable; current docs link to them instead of duplicating inventories.
4. Implement the agreed portion, applying [security guidance](security.md). Update invalidated decisions before implementing different behavior.
5. Reconcile the implemented portion into current docs within the same scoped change. Assess impact upward; update only views whose meaning changes. Describe relevant transitional behavior and compatibility limits.
6. Review implementation against the agreed design and current descriptions against code. Preserve lasting decisions before pruning completed plan items; retain unfinished work. Report completion and stop at the authorized step boundary.

## Small changes

A wording/link correction, mechanical edit, or localized bug fix may proceed without a plan file when the expected behavior is already settled and it changes no requirements, public contracts, architecture, persistence, permissions/security controls, dependencies, or deployment behavior. File count alone does not determine eligibility.

Before editing, state the intended result, affected scope, and meaningful check in the task conversation. An explicit request to fix an eligible issue authorizes that bounded implementation; no separate planning approval is needed. Inspect connected code and existing failures, make the fix, run proportionate checks, and update docs only if their meaning changes. A typo needs no new test; a logic bug needs a regression check. Apply the existing review rules and PR gates.

If investigation reveals an unresolved design decision or a change outside those limits, record the necessary delta in `plan/` and resolve it before dependent edits. Ask only when the user's scope or agreed behavior must change.

## Ownership and review

Follow the [collaboration policy](collaboration.md) for ownership, dispatch triggers, independent review, unavailable agents, and resolution. Every PR requires a passing security audit/report before general review and two independent reviewers including security and correctness/test quality. Review the resulting implementation separately from design; refresh affected evidence after fixes or integration.

## Acceptance and evidence

- Examine connected code and failure paths behind stated guarantees. Source references help find evidence; valid links and passing tests alone do not establish agreement.
- Defects, stale descriptions, and missing checks can coexist. Resolve disagreements or record limitations; unresolved differences block affected acceptance claims. Describing a defect does not accept it or change a requirement.
- Failed, unavailable, skipped, inconclusive, or unexpectedly empty required checks cannot pass a gate. Preserve initial failures after diagnostic retries. Do not weaken obligations or checks to fit an implementation.
- Keep check results and review findings with the change or handoff. Current docs retain commands and actual product limits, not review chronology or fixture narratives. Keep secrets out of reports.
- Use stable source, contract, and check references where useful. No mandatory claim registry, sentence-level citations, copied hashes throughout docs, or parallel system model is needed.
- Run `python3 .agents/adp/scripts/check_docs.py --root .` for deterministic local references; select explicit files or directories to narrow scope. It does not establish semantic agreement or fetch URLs. Use project-selected contract checks and reliable generators where canonical artifacts support them.
- Completion reports readiness and blockers. It does not merge, publish, deploy, or run live or destructive operations without authorization for that action and target.
