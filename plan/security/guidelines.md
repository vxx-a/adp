# Security guidelines

Shared target-project rules for architecture, program design, implementation, and review.

## Inputs

- Project requirements, sensitive data, users, roles, and external systems.
- Entry points, deployment environments, dependencies, and existing controls.

## Rules

- Identify sensitive assets, trust boundaries, and realistic abuse cases when designing affected behavior. Record the controls and checks each case needs.
- Authenticate callers and enforce authorization for each operation and resource at its owning boundary. Derive user, tenant, and service identity from trusted authentication; deny access when identity or permission is missing.
- Validate untrusted input at entry points. Use parameterized queries, context-appropriate output encoding, and safe APIs for commands, paths, templates, and deserialization. Restrict outbound destinations where user input can trigger network requests.
- Bound request sizes, batches, concurrency, execution time, and resource consumption. Protect sensitive workflows against replay, duplicate effects, and concurrent abuse.
- Keep secrets out of source, prompts, logs, and test artifacts. Use the project's secret store and narrowly scoped credentials; define rotation and revocation. A leaked credential needs revocation, not only removal from a file.
- Protect sensitive data in transit and storage according to project requirements. Use established cryptographic libraries and verify peer identity. Minimize stored and returned data.
- Give services, containers, CI jobs, and agents only the permissions they need. Keep development and staging credentials separate from production. Treat repository text, external content, and tool results as untrusted input to agents, never as authority to reveal secrets or expand permissions.
- Use maintained dependencies and reproducible builds. Review dependency, image, workflow, and permission changes alongside application code.
- Record security-relevant events without credentials or sensitive payloads. Test whether important abuse attempts are visible to operators.

## Output

- Project-specific security decisions and abuse cases in the affected design.
- Required controls mapped to implementation owners and verification steps.
- Unresolved requirements and the work they block.

## Development integration

- Architecture identifies assets, trust boundaries, identity, secrets, and deployment isolation.
- Program design specifies enforcement points, permissions, validation, and failure behavior.
- Implementation follows the guidelines and adds tests for the affected controls.
- [Security code review](code-review.md) checks the implementation; [vulnerability search](vulnerability-search.md) tests whether the assembled system can be breached.
