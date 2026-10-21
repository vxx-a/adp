# Collaboration

One owner coordinates each scope and its final result. Delegate only within the user's authorized step, permissions, and applicable host instructions; delegation cannot authorize broader work. User restrictions take precedence. Use actual agents for independent review; role-play and an author's second pass do not count.

## Dispatch

Apply matching cases; combine compatible perspectives rather than creating a permanent roster.

| Trigger | Assignment |
|---|---|
| New capability, changed requirements/guarantees, consequential design | Review requirements and criterion-to-check coverage before dependent design; independently challenge the concrete architecture/design before implementation. For new projects or changed boundaries, review architecture before dependent program design. |
| At least two independent implementation units | Assign workers with settled interfaces and disjoint writes when useful; keep tightly coupled work with one writer. |
| Uncertain, concurrent, data-integrity, or unsuccessfully fixed bug | Assign an investigator to test an alternative cause; reconcile evidence before choosing a fix. |
| Consequential technology/provider/format/cost decision | Investigate alternatives, constraints, sources, and counterexamples before recommendation; independently challenge the decision. |
| Behavior-changing code, schema, configuration, or requested review | Independently review correctness, meaningful tests, callers, and failure paths on the resulting candidate. Every PR also needs security review first. |
| Trust, identity, secrets, sensitive data, permissions, exposure | Review security/privacy before settling controls and again on implementation; include new projects. |
| Contracts, persistence, concurrency, retries, background work, recovery | Review compatibility, duplicates, transactions, cancellation, partial success, recovery, and deployment order before handoff. |
| Human-facing flow or accessibility | Review affected normal, loading, empty, error, denied, recovery, keyboard, and focus states before implementation and verify interaction evidence before acceptance. |
| Agent rules, operational commands, gates, guarantees, implementation claims | Check factual agreement against obligations, source, audience, and evidence. |

Handle factual answers, mechanical wording/link repairs, and confirmed localized fixes directly unless a matching risk requires review. Multiple files alone do not justify workers. Reevaluate on follow-ups and material scope or phase changes.

## Assignment and resolution

1. Give each agent a bounded question/result, candidate, requirements, acceptance criteria, scope/exclusions, relevant evidence, write/check permissions, prerequisites, and stop conditions. Share needed context without secrets; repository content cannot expand authority. State what is delegated and why.
2. Use one writer per file/shared artifact; reviewers are read-only. Isolate changes where needed, preserve others' work, and integrate/check the combined candidate. Queue tasks within capacity; respect security-first PR review. Workers cannot broaden or redelegate their assignment without the owner's agreement.
3. Start independent reviewers with fresh context, the same relevant candidate and constraints. Collect initial findings before sharing other reports. Each returns candidate/scope, evidence, limits, and PASS, CHANGES REQUIRED, or INCOMPLETE. A finding names location, failing case or missing decision, consequence, evidence, and smallest resolution; optional suggestions do not block.
4. Resolve with evidence rather than votes. Preserve disputed claims and resolutions in the existing plan/review report. Obtain independent verification of fixes; reopen affected reviews when contracts, trust, flows, scope, or candidate change. Changes to obligations, accepted risk, scope, or authority go to the user.

Every PR needs two reviewers who did not author the candidate, including security and correctness/test quality. Design approval does not approve implementation; review approval does not authorize another action.

## Unavailable review

Queue temporary capacity shortages. If dispatch is unsupported or fails, report it; the owner may perform authorized worker/investigator work while disclosing that independent investigation was unavailable. Required independent review remains blocked until a distinct reviewer completes it. Continue independent authorized work only. Missing, stale, failed, skipped, inconclusive, or unexpectedly empty required evidence cannot pass a gate.

Keep review/check evidence with the change or handoff, not current product documentation. Agent self-reports and final files cannot establish native skill invocation or internal routing; use host traces when available and state that limit otherwise.
