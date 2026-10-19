---
name: adp-coding-rules
description: Apply ADP coding conventions when writing, changing, or reviewing code alongside the project's own language and formatting rules.
---

# Coding rules

Read the agreed design and connected code. Project instructions take precedence; apply [security guidance](../../adp/security.md).

- Use explicit names understandable in context. Short coordinates, loop indices, and established `id` or `url` names are fine when clear.
- Comment reasons or external constraints the code cannot express, not restatements of code.
- Report failures instead of hiding them behind substitute data or empty results. Add degraded behavior only when required, with a named path, reason, log, and meaningful test.
- Handle errors where recovery, context, or reporting is useful; otherwise propagate them. Do not wrap every operation by default.
- Missing required input/configuration fails with a clear error naming it; do not silently default a required value.
- Give each responsibility one owner. Search for existing logic, shared libraries, and contracts before adding more. Extract repeated logic within a module when the responsibility is shared; propose a design change for shared responsibility across modules.
- Keep similar-looking code separate when responsibilities differ. Do not add an abstraction solely to remove a few repeated lines.
- Follow language conventions and existing formatter/linter configuration. A blocking rule needs a focused decision rather than a workaround.

When reviewing, report concrete location, consequence, violated rule, and smallest fix. Formatting checks do not replace contextual review.
