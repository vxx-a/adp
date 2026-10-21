# Product and export boundary

`export.py` collects the following canonical sources from `product/`. It never copies this repository wholesale.

| Source | Installed path |
|---|---|
| `product/adp/` Markdown policies and catalog | `.agents/adp/` |
| `product/skills/adp-*/` | `.agents/skills/adp-*/` |
| `product/scripts/check_docs.py` | `.agents/adp/scripts/check_docs.py` |
| `product/memory/MEMORY.md` | `.agents/memory/MEMORY.md`, created only if absent |
| `product/USAGE.md` human guide | `ADP.md` at the project root |
| `product/LICENSE`, `product/CHANGELOG.md`, `product/release.json` | `.agents/adp/` under the same filenames |
| Generated version/source/fingerprint metadata | `.agents/adp/version.json` |
| Generated discovery link | `.claude/skills` → `../.agents/skills` |

Root `AGENTS.md`, `.agents/`, `.claude/`, `docs/`, `plan/`, tests, and root `scripts/` are maintainer content and never ship. Shared policies and skills are product content, not instructions for agents developing ADP itself.

## Installation and updates

The [installation policy](../product/adp/installation.md) defines installed ownership. Export preview does not write. Apply replaces changed ADP-owned files, restores missing files, and removes obsolete owned files/directories. Project-owned memory, instructions, docs, plans, configuration, and unrelated skills are preserved. Setup integrates project instructions and existing skill discovery separately.

Preflight rejects source symlinks and destination symlinks below the selected project root. Files use unique temporary siblings and atomic replacement; an unexpected I/O error can leave a partially updated installation. Rerun export to finish it; an interrupted first/legacy install may require explicit relocation of an unrecorded root guide under the installation recovery steps. Concurrent mutation of the source or target during export is unsupported.

`product/release.json` declares the product version and repository; `product/CHANGELOG.md` records versioned changes and migrations. `version.json` schema `2` combines those with source Git revision/modified status when available (null for archives), a SHA-256 fingerprint of sorted installed source paths and bytes, and ownership of root `ADP.md`. Generated metadata and discovery are excluded from the fingerprint. Modified checkouts retain their declared version; source metadata does not imply a published or qualified release.

An existing root guide without explicit prior metadata ownership blocks installation. The exporter never scans the project root for obsolete files. Metadata is written only after content and obsolete cleanup succeed; an interrupted update can leave partial content behind old metadata. Project-owned memory may differ from its starter. The installed MIT notice matches the repository license.

## Guidance and validation

The shipped [catalog](../product/adp/skills.md) routes setup, design, implementation, testing, review, UI, security, operations, completion, and maintenance. Policies specify project selection of stack tools, CI providers, credentials, model settings, performance targets, and gates; they do not provision external systems automatically.

All former product drafts are consolidated into these policies and skills. Target projects use their own `plan/` for unfinished consequential changes; eligible small fixes need no plan file. [Behavioral evaluations](evaluations.md) distinguish tested agent scenarios from host and runtime limits.
