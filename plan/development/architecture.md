# Architecture

The coding agent runs architecture before [program design](program-design.md), following the [development workflow](workflow.md). Revisit it when boundaries, ownership, dependencies, or shared decisions change.

## Scope

- System purpose, users, and external systems.
- Module responsibilities, data ownership and storage, dependencies, and direct calls or messaging.
- Shared decisions: tech stack, auth, config and secrets, logging and monitoring, deployment and environments.

Program design defines contracts, internal structure, interactions, and algorithms required by correctness or performance. Implementation fills in method details and local choices.

Dockerize each module and use gRPC between modules, per `template/.agents/adp/rules.md`.

Apply the [security guidelines](../security/guidelines.md) to sensitive assets, trust boundaries, identity, secrets, and deployment isolation. Record the affected abuse cases and required controls in the architecture.

## Design principles

A module is a separately deployed service.

- **Use as few modules as the needs allow.** Split only for a named need for independent scaling, deployment, security, or failure isolation. Data ownership alone doesn't require a separate service.
- **Review modules approaching 10k lines.** Split at clear responsibility boundaries; size alone doesn't require it.
- **Each module owns its data.** Modules never access another module's tables; they use its contract. Capabilities within a module can also have distinct data owners.
- **Keep operations that must succeed or fail together within one module where practical.** When an operation spans modules, define what happens if only part succeeds.
- **Prefer stateless application processes.** Keep durable state in datastores. Avoid correctness depending on a particular replica's memory, and handle concurrent work safely when adding replicas.
- **Design for stated load, with headroom.** Record peak traffic, data volume, latency targets, and what would change beyond them. Build for the stated targets.
- **Use established technology.** Add something new only for a requirement in the project description.

## Input

Read the project description maintained through setup and the affected implementation baseline. Keep required behavior distinct from the overview of implemented capabilities. Ask about missing requirements that block design; record agreed answers in the project description.

## Output

Write proposed architecture changes in the target project's `plan/`, linked to the affected current design. For a new system, record the initial design there.

As each scope is implemented, reconcile its boundaries, ownership, dependencies, and lasting decisions into the existing architecture in `docs/`. Check the affected program design and overview for agreement. Preserve unfinished work in `plan/`; do not promote an unverified plan wholesale.

Setup reuses established requirement and document locations; its shipped [defaults](../../template/.agents/adp/development.md#baseline-and-files) apply when no convention exists.
