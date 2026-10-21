# Installation and ownership

## Get and install ADP

Requires Python 3.10 or newer, with no third-party packages. Obtain and inspect a trusted checkout:

```sh
git clone https://github.com/vxx-a/adp.git /path/to/adp
python3 /path/to/adp/export.py /path/to/project --diff
python3 /path/to/adp/export.py /path/to/project --apply
```

The checkout stays separate from the target project. Choose a reviewed revision/version before applying; the clone's current branch is not automatically a qualified release. The exporter never fetches or selects updates itself.

Run [setup](../skills/adp-setup/SKILL.md) after first export; export alone does not integrate project instructions. If discovery is unavailable, ask the agent to read `.agents/skills/adp-setup/SKILL.md` directly. Review its resulting instructions and project selections. ADP's maintainer docs, tests, plans, and repository agent configuration are never installed. The human guide is `ADP.md` in the project root.

## Ownership

- ADP owns `.agents/adp/`, directories named `adp-*` under `.agents/skills/`, and the root `ADP.md` guide once recorded in installed metadata. Updates replace changed files and remove obsolete owned files/directories. Loose `adp-*` files are not owned. Put project overrides in `AGENTS.md` and give project skills other names.
- An existing root `ADP.md` without explicit ownership in prior schema-2 metadata blocks installation, even on legacy installs. Inspect and explicitly relocate it before retrying; export never infers ownership from matching content.
- Project instructions, non-ADP skills, memory, source, docs, plans, and host settings are preserved by export. Starter memory is created only when absent. Setup amends project instructions within its authorized scope.
- Export creates `.claude/skills` pointing to `../.agents/skills`. A real existing directory is left for safe setup migration. A different link, or a symlink inside an owned path, blocks export before writes. Case aliases retain existing spelling rather than being deleted as obsolete.
- `.agents/adp/LICENSE` carries ADP's MIT copyright and permission notice. Keep it with copies or substantial portions you retain or redistribute.

## Version and source

`.agents/adp/version.json` schema `2` records the declared version and repository from `release.json`, source Git revision and modified flag when Git is available, content SHA-256, and owned root files. Archives without Git record null source fields. A version label does not imply a clean tagged release: modified sources retain that label and require the fingerprint to identify content. A hash alone cannot locate or reconstruct a checkout. Schema-1 hash-only installations can be updated; obtain a trusted source explicitly.

`CHANGELOG.md` records compatibility and migration changes by declared version. Maintainers bump `release.json` and update the changelog when preparing a release; tags/publication require separate qualification. Keep the selected checkout/revision or archive with update evidence if exact reconstruction is needed.

## Updates and recovery

Use the same preview/apply commands from a trusted updated checkout. Default preview lists create, update, remove, and skip actions; `--diff` also shows unified contents for created/changed/deleted files, including local edits that would be lost. Inspect both before applying, plus the proposed changelog and source identity. Use a private review location if owned files contain accidental secrets; never paste such diffs into reports. Shared import/discovery changes need an explicit migration because project-owned integration is preserved. Follow [maintenance](../skills/adp-maintain/SKILL.md) for target integration checks.

Files are replaced individually with unique temporary siblings; there is no transaction across the export. A failed write preserves that file's prior destination. Content and obsolete cleanup complete before metadata is written. An interrupted run can leave a partial update or temporary siblings; rerun preview and apply from the same reviewed source, then verify metadata, an empty change preview, imports/discovery, and local references. Do not interpret old metadata as proof every file still matches it after failure.

If a first install or legacy upgrade stops after creating `ADP.md` but before recording ownership, retry will safely refuse that guide as unowned. Inspect and explicitly relocate it outside ADP-owned paths, then rerun from the same reviewed source. Retain the relocated copy until the installation is verified; do not bypass the ownership check.

Obsolete temporary files inside owned directories are cleaned by export; inspect leftovers elsewhere before removing them. A destination added after preflight blocks creation. Export does not back up locally edited owned files; retain a copy before applying if needed. To restore an earlier ADP version, export from its retained trusted source and review compatibility first; this does not undo project-owned setup migrations.

## Uninstall

Uninstall is a manual, explicitly authorized project change; the exporter has no uninstall command.

1. Inspect `version.json` and local changes; preserve any needed ADP copies and their MIT notice. Identify active ADP imports and references in root/nested instructions and project docs.
2. Remove active imports of `.agents/adp/rules.md` and ADP-only fallback/loading instructions from project-owned files. Remove or update links to removed ADP content. Keep project rules and all unrelated instructions. Keep `.claude/CLAUDE.md` importing `AGENTS.md` when that bridge remains useful.
3. Remove `.agents/adp/` and only `adp-*` directories under `.agents/skills/`. Remove root `ADP.md` only if installed metadata explicitly records its ownership; preserve a colliding project guide. Never remove all of `.agents/` or `.agents/skills/`.
4. Preserve non-ADP skills, migrated Claude rules/resources, memory, docs, plans, source, and host settings. Keep `.claude/skills` when project skills use it. If no skills use it and it is exactly the ADP-created `../.agents/skills` symlink, it may be removed; leave other directories/links intact. Do not reverse setup migrations automatically.
5. Review the scoped diff and check for dangling ADP imports/links using project tools. Run applicable project checks and verify remaining skill discovery. Restore from the retained trusted checkout if uninstall was incomplete; repeat setup only when instruction integration needs repair.
