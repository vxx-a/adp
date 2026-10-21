# Project setup decisions

Setup discovers project facts and records selected configuration. A policy is not evidence that tools or a provider enforce it. Use existing project locations; otherwise the [development baseline](development.md#baseline-and-files) supplies defaults.

## Instructions and stack

Record purpose, layout, requirements locations, supported language/runtime versions, package manager/lockfiles, build/run commands, development environment, and meaningful check commands with prerequisites. Inspect actual manifests and checks; do not promise a fixed list of supported stacks. Select maintained stack tools compatible with the project. Configuration changes require authorized scope and verification.

Record existing packaging and in-process/remote communication choices. For new or changed services, settle packaging (including whether containers are needed), remote protocols, and contract tooling with the user against requirements; record the decision and reason in project-owned architecture/configuration. Docker, gRPC, and protobuf are options. Mark remote transport not applicable for a project without remote services; defer decisions outside setup scope until affected architecture work.

For projects with a UI, establish the [accessibility selections](ui-ux/guidelines.md#accessibility) with the user: applicable standard/version, supported platforms and assistive technology, checks, and owner. Reuse established requirements; record unresolved selections and only their dependent work. Projects without UI mark this not applicable. If UI is added later, the first affected UI task settles these selections without requiring a setup rerun.

Select formatter/linter, type, contract/generator, unit/integration/end-to-end, mutation, performance, and security checks where applicable using [testing configuration](testing.md#project-configuration) and [security configuration](security.md#project-configuration). Record exact commands, environment/data needs, stage gates, thresholds/exclusions, and owners in project-owned check docs/config. No universal threshold or generic passing command substitutes for a selected gate. CI, staging attack testing, deployment, and monitoring use [ops setup](ops-setup.md) under their own scope.

Where local gates require enforcement, select supported host hooks/pre-commit integration, module-size warnings, and applicable contract commands. Configure them only within authorized scope; verify actual triggering and record bypass limits.

Add nested `AGENTS.md` only where a module needs distinct commands, ownership, constraints, or checks. Link shared rules rather than copy them; state its directory scope, preserve ancestor rules, and resolve conflicts before dependent work. Do not multiply identical instruction files.

## Host and secret boundaries

Project-owned host settings, hooks, agents, commands, and permission files remain in place. Read supported host documentation/configuration before proposing changes; preserve unrelated settings and explicit user decisions. A permission conflict blocks that configuration change rather than justifying a broader grant.

Identify secret paths and approved access: environment files containing values, credentials, tokens, private keys, and local secret stores. Keep secrets out of agent context, reports, version control, generated fixtures, and build artifacts. Sanitized example configuration can remain readable. Reference secret names/paths, never print values to prove a rule works.

Within authorized host-configuration scope, merge targeted read-deny rules for identified secret files and least-privilege execution/network access using supported host syntax. Keep project settings project-owned; do not overwrite the whole file or silently alter global/user settings. Verify harmless allow/deny cases without reading secret content. If the host cannot enforce a restriction, disclose the limit and use an approved isolation/access alternative; a deny pattern alone does not prove all tool paths are blocked. Application/CI secret injection is configured separately with the responsible owner.

Select supported hosts/versions, available models and reasoning effort, tool permissions, and task cost limits with the user or existing project policy. Configure only supported host mechanisms; do not put invented model/effort keys in skill frontmatter. Record unavailable capabilities and the work they block. Native skill discovery may require a host restart; report whether it was actually exercised.
