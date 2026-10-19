# File ownership and updates

See [README](../../README.md#use) for initial installation. ADP owns installed `.agents/adp/` and `.agents/skills/adp-*/`. Project instructions are created or amended by setup and remain project-owned.

## Updates to implement

- Replace only `.agents/adp/` and `.agents/skills/adp-*/`. Remove obsolete reserved skills; preserve project instructions, other skills, memories, docs, and plans.
- Add a version stamp under `.agents/adp/` and define compatibility and migration behavior. Changing shared paths or import/discovery locations needs a migration because updates preserve project-owned integration.
- Define update preview, conflict handling, recovery after partial failure, and acceptance checks before building the update skill.

## Open

- **Human guidelines:** choose a shipping location; ordinary project `docs/` cannot be replaced by ADP updates.
- **`.claude/settings.json`:** decide how ADP's secret-file deny rules coexist with project permissions and which component owns integration.
