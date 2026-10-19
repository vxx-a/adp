# Checks

Requires Python 3.10 or newer; no third-party packages.

From the ADP checkout:

```sh
python3 -B scripts/check.py
git diff --check
```

The aggregate command runs tests, catalog validation, and local reference checks for maintainer docs and the exported template. After editing skill metadata, regenerate the catalog with `python3 -B scripts/build_catalog.py`.

In an installed project, run `python3 .agents/adp/scripts/check_docs.py --root .`, optionally followed by selected files or directories.

## Reference syntax and limits

- Default selections: existing README, AGENTS, docs, plan, and `.agents`. Explicit missing inputs and empty selections fail.
- Supports local inline/image/reference links, headings, explicit HTML identifiers, and source lines. Repeated reference labels use their first definition.
- Leading `/` means the selected project root. Escaping symlinks and unreadable selected trees fail. Discovery skips symlinked child directories.
- Fenced examples, inline code, HTML comments, and network URLs are excluded. Indented lines are inspected; use fences for code examples containing links.
- Use `./LICENSE:3` or `LICENSE#L3` to disambiguate extensionless source paths from URI schemes.

The checker supports a Markdown subset. It does not check remote URLs, semantic agreement, or deployed behavior.
