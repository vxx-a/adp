---
name: adp-program-design
description: Design changed components, contracts, state, invariants, interactions, and failure behavior within established architecture before implementation.
---

# Program design

Read requirements, acceptance criteria, architecture, affected code and callers, and the shared [workflow](../../adp/development.md) and [security guidance](../../adp/security.md). Reuse settled design; document only changed decisions and flows.

## Decisions

- Map behavior to owners, changed components, and callers. Define meaningful responsibilities, owned state, collaborators, important operations, errors, and side effects. Leave helpers and ordinary method details to implementation.
- Define package and dependency direction; add layers only for meaningful responsibilities. Use classes for coherent state or resources and functions for transformations. Pass dependencies explicitly; add interfaces for actual boundaries or alternatives.
- Reuse logic that has the same responsibility and should change together. Keep module-owned business decisions with their owner.
- Document changed contract shapes and semantics in the delta plan before editing schemas, configuration, tests, or code. Specify units, time basis, precision, rounding, absence/default meaning, ordering, validation, errors, and side effects where ambiguous. During authorized implementation, put exact definitions in provider-owned schemas; current docs link to them instead of copying inventories.
- Identify consumers and supported deployment combinations. Check semantic as well as structural compatibility, migration order, and breaking-change transitions.
- Name authentication and authorization enforcement, trusted identities, permissions per resource/operation, and abuse-case checks. Validate shape at boundaries and business rules at the owner.
- Define stored constraints, transaction boundaries, migrations, and invariants under concurrency across replicas. For meaningful lifecycles, define states, allowed transitions, and actors.
- Define resource creation, ownership, lifetime, sharing, and cleanup during failure, cancellation, or shutdown. Keep request state out of shared components.
- Bound growing results, batches, concurrency, queues, and buffers; define saturation and caller-visible outcomes.
- Give remote calls deadlines and propagate remaining budgets. Define cancellation before and after irreversible effects, outcome discovery after timeout, and reconciliation.
- Name the retrying layer, safe retry conditions, attempts/time budget, and delay policy. For duplicate effects, define identity, protection lifetime, concurrent delivery, crash recovery, and expiry behavior. Avoid retry amplification.
- For work spanning modules, define partial success and recovery ownership. For background work, define acceptance guarantees, durable pending work, observable completion/failure, and recovery when persistence and scheduling differ.
- Apply shared configuration, secrets, logging, and monitoring choices at named components. Settle algorithms when correctness or performance requires them; use diagrams only to clarify a specific ambiguity.

## Handoff

Write a delta plan per scope/module; root plans hold cross-module decisions. Link current docs and canonical contracts. Map acceptance criteria to owners, flows, and verification needs; order dependent contracts, libraries, migrations, and callers.

Settle behavior, ownership, invariants, contracts, and failure policy for the portion handed off. Record blocked decisions without inventing answers. Independently review consequential decisions and discuss the design with the user. Stop at the authorized design step; agreement on its design does not itself authorize implementation. Implementation reconciles completed portions into current docs and retains unfinished plans.
