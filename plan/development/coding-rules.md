# Coding rules

Rules for writing, changing, or reviewing code in target projects. Follow the [security guidelines](../security/guidelines.md) alongside these rules.

## Skill

Ship an `adp-` skill in `template/.agents/skills/`. Its description must trigger on writing, changing, and reviewing code. Implementation and [code review](../testing/code-review.md) use it. Replace the Code section of `template/.agents/adp/rules.md` with a pointer to the skill.

### Input

- The plan or design for the current scope.
- The code being written, changed, or reviewed, and the code around it.
- The formatter and linter configured for the project.

### Output

- When writing: code that follows these rules. A rule that blocks the work is raised with the user.
- When reviewing: findings with the location, the rule broken, and the smallest fix.

## Rules

### Naming

- Use explicit names such as `order`, `total_price`, and `retry_count`.
- Short names are allowed when clear in context: coordinates, short-loop indices, `id`, or `url`. Readers should understand a name without looking elsewhere.

### Comments

- Comment only context the code cannot express: reasons for a choice or external constraints. Omit comments that repeat the code.

### Fallbacks and error handling

- Make the expected path work. Report failures instead of hiding them behind substitute data, defaults, or empty results.
- Add a fallback only for required degraded behavior. Give it a named path, a documented reason, a log when it runs, and a test.
- Handle an error where the code can do something useful with it: recover, add context, or report it. Let other errors propagate. Don't wrap code in error handling by default.
- Required config and input have no defaults. When something required is missing, stop with a clear error that names it.

### Repetition

- Give each responsibility one owner. Follow the design's shared libraries and protobuf contracts; check for existing code before writing more.
- When the same logic is needed in a second place within a module, extract it. When it crosses modules or the design doesn't cover it, raise a design change instead of copying.
- Keep similar-looking code separate when responsibilities differ. Don't add an abstraction solely to remove a few repeated lines.

### Language conventions

- Follow the language's conventions and the project's formatter and linter.

## Enforcement

- The formatter and linter, configured per stack by setup, check formatting, language conventions, and unused code.
- Code review checks what needs judgment: names in context, comments, fallbacks and error handling, and repetition.
