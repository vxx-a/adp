# Agent collaboration

Current user checkpoints are defined in [shared rules](../../template/.agents/adp/rules.md#working-with-the-user).

## Ownership and independent review

The implemented owner/reviewer model is maintained in the [development workflow](../../template/.agents/adp/development.md#ownership-and-review). Reviewer identities and hosted enforcement remain [setup and Git-policy decisions](../ci-cd/git-policy.md#output-and-setup-decisions).

## Review cases

Remaining behavioral coverage across the skills:

- Routine choices stay within the authorized step.
- Missing requirements block only dependent work and receive a focused question.
- Conflicting instructions are raised before edits.
- Failed, retried, skipped, and unavailable checks are reported accurately.
- Changed scope or behavior triggers discussion before implementation continues.
- Design-only agreement does not authorize implementation.
- Approval of one step does not start the remaining roadmap.
- Progress reports and reviewer approval do not extend user authorization.
- Mistakes and unresolved risks remain visible at handoff.
