---
name: adp-maintain
description: Review and apply an authorized installed ADP update or scoped pipeline cleanup while preserving project-owned instructions, skills, memory, and settings.
---

# Pipeline maintenance

Read the [installation policy](../../adp/installation.md), project instructions, installed `version.json`, and authorized scope. Use [development](../../adp/development.md) and [collaboration](../../adp/collaboration.md) for changes and review. This skill maintains the installed integration in the target project.

1. Resolve a trusted local ADP checkout from the user's update source. Compare installed version/source/fingerprint with the proposed checkout's changelog and metadata. Legacy hash-only installs do not identify a checkout or revision; if a trusted source is unavailable, ask for its path or approved release. Metadata is provenance, not permission to fetch or execute code. A modified or archived source may not be reconstructible from a Git revision.
2. Inspect `export.py TARGET --diff` from that trusted checkout. Record compatibility impacts, migration needs, and acceptance under shared planning rules. Preserve project instructions, non-ADP skills, memory, docs, plans, host settings, and unrelated changes. Put agreed project overrides in project instructions; shared ADP fixes belong upstream. Import/discovery changes need an explicitly scoped migration.
3. Apply the reviewed update under existing update authorization. A partial failure is not success: inspect the remaining preview and finish only within scope. An unsafe path or root guide collision blocks export; preserve it until explicitly resolved.
4. Verify installed metadata against the proposed source, rerun preview for remaining changes, check active imports/discovery and catalog links, and run the installed reference checker. Run affected project checks or a bounded installed-skill smoke check when required by this update's acceptance; report actual host discovery/invocation and unavailable evidence separately. ADP's maintainer evaluation runner is not installed and is not a prerequisite for target maintenance.
5. For cleanup or uninstall, follow installation ownership and inspect references before removing only authorized material. Preserve lasting project decisions, constraints, unfinished work, memory, and reports still needed for review or recovery.

Return changed files, installed version/source/fingerprint, compatibility/migrations, checks/reviews, and blockers. Reconcile completed plans and stop at the authorized boundary. Installed updates do not qualify the project's runtime or authorize changes to ADP-owned defaults.
