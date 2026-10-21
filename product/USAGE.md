# Using ADP

ADP gives your existing coding agent project rules and task skills. Describe the result you want; you do not need to know skill names. This guide is installed as `ADP.md` in your project root.

## Start

Install from a trusted ADP checkout with Python 3.10 or newer:

```sh
python3 /path/to/adp/export.py /path/to/project --diff
python3 /path/to/adp/export.py /path/to/project --apply
```

Ask: “Set up ADP for this project.” If skills are not discovered, ask the agent to read `.agents/skills/adp-setup/SKILL.md`. Review the resulting project instructions, context, commands, stack decisions, and any unresolved selections. Export does not integrate instructions itself.

Keep a project description with purpose, users, flows, constraints, external systems, expected load, and success criteria. Setup records its location. Packaging, remote protocols, accessibility, checks, and operations are project decisions; review those that apply to your scope.

## Give a bounded task

State the desired behavior with an example, relevant context/files, scope, acceptance checks, and whether you want a proposal, implementation, or review. For example:

- “Fix this bug: zero quantities are rejected, but requirements permit them. Add a regression check.”
- “Plan this feature; stop before implementation.”
- “Implement the approved add step; leave multiply for later.”
- “Commit these changes,” “Open a PR into develop,” or “Merge this PR into develop after its gates pass.”

Explicit implementation requests authorize the bounded fix. Small changes with settled behavior can use a short summary in the conversation instead of a plan file. Changes to requirements, contracts, architecture, persistence, security, dependencies, or deployment need a concrete design plan. The agent stops at the requested boundary unless you authorized a sequence.

## Review the plan

- Check intended behavior and acceptance against your requirements.
- Review affected boundaries, callers/contracts, state, failure/recovery behavior, and compatibility where changed.
- Resolve material assumptions, risks, and blocked decisions before dependent implementation.
- Check the verification approach and scope. Design agreement alone does not authorize implementation; request that step explicitly.

The agent reconciles implemented portions into current `docs/` and retains unfinished plans. You need not approve ordinary local implementation choices again.

## Verify before accepting

- Read the diff and affected descriptions together; check behavior and connected callers.
- Inspect meaningful tests for new logic and regressions. For UI, exercise affected interactions and applicable accessibility checks.
- Check results, independent reviews, initial failures, retries, and skipped/unavailable checks. Local checks establish only what their environment exercised.
- Verify the tested candidate includes the actual combined changes. Do not change requirements to fit a defect or accept missing required evidence as a pass.
- Keep deployment, destructive operations, and live changes explicitly scoped to an action and target.

Ask “Is this feature complete?” for feature acceptance. Ask “Is this release ready?” for release preparation/qualification. Readiness does not itself commit, merge, publish, or deploy; request those actions with their targets.

## Update or remove ADP

Preview an update with `--diff`, read `.agents/adp/CHANGELOG.md` in the proposed checkout/export, and review compatibility before applying. `.agents/adp/version.json` records the installed version, source identity where available, and content hash. Modified checkouts are not clean release revisions.

`ADP.md`, `.agents/adp/`, and `adp-*` skill directories are ADP-owned; updates replace them. Keep project overrides in `AGENTS.md`, and use other names for project skills. Project instructions, docs, plans, memory, and host settings are preserved by export.

For update recovery and exact uninstall steps, read `.agents/adp/installation.md`. Uninstall removes ADP imports and owned files while retaining project rules, migrated skills, memory, and configuration. Preserve the MIT notice with any ADP copies you retain or redistribute.
