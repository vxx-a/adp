# Development workflow

## Definitions

| Artifact | Canonical information |
|---|---|
| Requirements and acceptance criteria | Required behavior, constraints, external promises |
| Code, schemas, configuration | Executable definitions and implemented behavior |
| Program design | Components, interactions, state, contract semantics, failure guarantees |
| Architecture | System boundaries, data ownership, dependencies, shared decisions |
| Overview | Implemented capabilities, major flows, limitations |

Keep one canonical definition and use linked summaries. Requirements and current descriptions have different roles even if they share a document. Schemas do not express every semantic guarantee; keep missing semantics with the owning contract or design. Keep lasting rationale with its decision.

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
2. Before editing code, schemas, configuration, or tests, write the concrete design delta in `plan/`: affected boundaries, owners, component responsibilities, interfaces, state, invariants, flows, failure behavior, and acceptance checks. Include only affected decisions; a task list alone is insufficient. Reuse settled design when it covers the change.
3. Agree on the step under [user involvement](rules.md#working-with-the-user). Design-only agreement does not authorize implementation. During implementation, put exact definitions in schemas, constraints, and configuration; current docs link to them instead of duplicating inventories.
4. Implement the agreed portion, applying [security guidance](security.md). Update invalidated decisions before implementing different behavior.
5. Reconcile the implemented portion into current docs within the same scoped change. Assess impact upward; update only views whose meaning changes. Describe relevant transitional behavior and compatibility limits.
6. Review implementation against the agreed design and current descriptions against code. Preserve lasting decisions before pruning completed plan items; retain unfinished work. Report completion and stop at the authorized step boundary.

## Ownership and review

- One owner maintains the scope, coordinates implementation, resolves findings, and reports decisions. Reviewers inspect independently; they do not concurrently edit the same scope.
- Independently challenge consequential decisions before implementation: requirements or guarantees, service and data boundaries, public contracts, authorization, secrets, migrations, recovery, installation ownership, or gates that might falsely pass.
- Select review perspectives from the risk. Give reviewers the same scope, constraints, acceptance criteria, and candidate; collect findings before sharing other reports. Separate runs do not guarantee different reasoning.
- Resolve findings with evidence, not votes. Record disputed claims, consequences, evidence, resolutions, and blockers in the existing plan or review report. Escalate changes to obligations, scope, accepted risk, or authorization to the user.
- Design review does not approve implementation. Review the resulting candidate separately. Every PR needs two independent reviewers, including security and correctness/test quality; the author does not count. An owner's second pass cannot replace an unavailable independent reviewer.
- Security audit and its report precede other PR review. After substantive fixes or integration, refresh affected evidence on the combined candidate, including contracts, callers, guarantees, and shared docs.

## Acceptance and evidence

- Examine connected code and failure paths behind stated guarantees. Source references help find evidence; valid links and passing tests alone do not establish agreement.
- Defects, stale descriptions, and missing checks can coexist. Resolve disagreements or record limitations; unresolved differences block affected acceptance claims. Describing a defect does not accept it or change a requirement.
- Failed, unavailable, skipped, inconclusive, or unexpectedly empty required checks cannot pass a gate. Preserve initial failures after diagnostic retries. Do not weaken obligations or checks to fit an implementation.
- Keep check results and review findings with the change or handoff. Current docs retain commands and actual product limits, not review chronology or fixture narratives. Keep secrets out of reports.
- Use stable source, contract, and check references where useful. No mandatory claim registry, sentence-level citations, copied hashes throughout docs, or parallel system model is needed.
- Run `python3 .agents/adp/scripts/check_docs.py --root .` for deterministic local references; select explicit files or directories to narrow scope. It does not establish semantic agreement or fetch URLs. Use project-selected contract checks and reliable generators where canonical artifacts support them.
- Completion reports readiness and blockers. It does not merge, publish, deploy, or run live or destructive operations without authorization for that action and target.
