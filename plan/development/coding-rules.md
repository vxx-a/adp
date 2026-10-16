# Coding rules

The rules an agent follows whenever it writes, changes, or reviews code in a target project. They ship as their own skill. This file is the reference for building that skill.

Sources: the Development list in `docs/NOTES.md`, the Code section of `template/AGENTS.md`, and the user's review of the first draft.

## Scope

- Naming and comments.
- Fallbacks and error handling.
- Repetition between modules and functions.
- Language conventions.

Covered elsewhere:

- Plan first, document, prune: `template/AGENTS.md` Workflow.
- Class design and interaction diagrams: program design.
- Docker, gRPC, module size: architecture and `template/AGENTS.md` Modules.
- Reasoning effort: `template/AGENTS.md` Reasoning.
- Tests: `plan/testing/`.

## Skill

ADP is a set of skills used at different points of development and operations. Coding rules is one of them, shipped in `template/.agents/skills/`.

- **When it applies:** any time the agent writes, changes, or reviews code. The skill's description must say so, so it triggers on those tasks.
- **Used by:** implementation, when writing code, and [code review](../testing/code-review.md), which checks changed code against these rules.
- **`template/AGENTS.md`:** the Code section is replaced by one line pointing to the skill. The rules live only in the skill.

### Input

- The plan or design for the current scope.
- The code being written, changed, or reviewed, and the code around it.
- The formatter and linter configured for the project.

### Output

- When writing: code that follows these rules. A rule that blocks the work is raised with the user.
- When reviewing: findings with the location, the rule broken, and the smallest fix.

## Rules

### Naming

- Use full, explicit words for names, such as `order`, `total_price`, and `retry_count`, not `o`, `t`, or `p`.
- A short name is fine when the surrounding code makes its meaning clear, such as `x` and `y` for coordinates, an index in a short loop, or common abbreviations like `id` and `url`.
- Judge a name in its context. A reader of the surrounding code should know what it holds or does without looking elsewhere.

### Comments

- Code should explain itself. Keep comments to a minimum.
- Comment only when the code can't carry the context, such as why a choice was made or a constraint that comes from outside the code.
- Don't comment what the code already says.

### Fallbacks and error handling

- Don't rely on fallbacks. Write code for the expected path, and make that path work.
- Report a failure as a failure. Don't hide it behind substitute data, a default, or an empty result.
- Add a fallback only where it is really necessary, such as when a requirement or the design calls for degraded behavior. Make it explicit: a named code path with its reason recorded in the plan or docs, logged when it runs, and covered by a test.
- Handle an error where the code can do something useful with it: recover, add context, or report it. Let other errors propagate. Don't wrap code in error handling by default.
- Required config and input have no defaults. When something required is missing, stop with a clear error that names it.

### Repetition

- No two modules or functions should do the same or nearly the same job.
- Prevent repetition mainly through design. Architecture gives each responsibility one owning module. Program design puts shared logic in shared libraries and contracts between modules in shared protobufs. Follow the design and reuse what it names.
- Before writing new code, look for existing code that already does the job.
- When the same logic is needed in a second place within a module, extract it. When it crosses modules or the design doesn't cover it, raise a design change instead of copying.
- Keep it reasonable. Code that only looks alike but serves different responsibilities stays separate. Don't add an abstraction just to remove a few repeated lines.

### Language conventions

- Follow the language's standard conventions and the formatter and linter configured for the project. This skill adds no language-specific rules.

### Follow strictly

- Follow these rules and the project's guidelines strictly. If a rule blocks you, raise it with the user. Don't work around it.

## Enforcement

- The formatter and linter, configured per stack by setup, check formatting, language conventions, and unused code.
- Code review checks what needs judgment: names in context, comments, fallbacks and error handling, and repetition.

## Decisions

- **Names are judged in context, not by length.** Short names like `x` and `y` are clear in the right surrounding code. A fixed length rule would reject them.
- **Fallbacks are allowed but never relied on.** A full ban was too strict. The problem is fallbacks used by default and error handling scattered through the code, which hide failures.
- **Repetition is mainly a design concern.** Code that follows a design with one owner per responsibility doesn't repeat. The rule stops short of merging code that only looks alike.
- **The rules live in their own skill.** ADP is a set of skills used at different points, and these rules are needed whenever code is written or reviewed. Keeping a copy in `template/AGENTS.md` would repeat them.
- **No language-specific rules.** These would cover type annotations, formatting, naming case, and error idioms. Formatters and linters already encode them for each language and check them automatically. A written copy would repeat the tools and go stale.
