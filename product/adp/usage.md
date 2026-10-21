# Agent task context and handoff

The human guide is `ADP.md` at the project root. Use this companion when helping a user frame or accept work; [shared rules](rules.md#working-with-the-user) own authorization.

- Establish purpose, users, important flows, constraints, external systems, stated load, and success criteria in the project's requirements location. Keep obligations distinct from observed capabilities.
- A bounded task states desired behavior, relevant context, scope, acceptance checks, and requested mode: question, proposal, implementation, or review. Ask only for decisions that block dependent work; do not invent requirements.
- Users describe goals rather than skill names; use [routing](rules.md#skill-routing). Reuse settled design and authorization, and state material assumptions or limits.
- Follow [development](development.md): plan affected decisions, implement the authorized portion, reconcile current docs, independently review the candidate, and retain only unfinished plans. For new systems, settle architecture before detailed design.
- Present acceptance evidence with the diff and changed descriptions, including failures, retries, skipped/unavailable checks, environment, and independent review limits. Do not rewrite obligations to match a defect.
- Feature, source, artifact, and deployed readiness are distinct. Use [completion](../skills/adp-completion/SKILL.md) for features and [release](../skills/adp-release/SKILL.md) for release readiness; a merge or deployment request must identify its action and target under the [release policy](ci-cd/workflow.md).
