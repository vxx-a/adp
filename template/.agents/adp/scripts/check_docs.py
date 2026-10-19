"""Read-only checks for local Markdown references; no semantic or network checks."""

import argparse
import html
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


DEFAULT_PATHS = ("README.md", "AGENTS.md", "docs", "plan", ".agents")
EXCLUDED = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", "worktrees"}


def without_examples(text):
    """Blank examples without changing line offsets."""
    text = re.sub(r"<!--.*?(?:-->|\Z)", lambda m: re.sub(r"[^\n]", " ", m[0]), text, flags=re.S)
    lines = text.splitlines(keepends=True)
    fence = None
    for i, line in enumerate(lines):
        match = re.match(r"^[ \t]*(`{3,}|~{3,})", line)
        if fence:
            lines[i] = re.sub(r"[^\n]", " ", line)
            if re.match(rf"^[ \t]*{re.escape(fence[0])}{{{len(fence)},}}\s*$", line):
                fence = None
        elif match:
            fence = match[1]
            lines[i] = re.sub(r"[^\n]", " ", line)
    return "".join(lines)


def without_inline_code(text):
    return re.sub(r"(`+)([^`]|(?!\1)`)*?\1", lambda m: re.sub(r"[^\n]", " ", m[0]), text)


def destination(raw):
    raw = raw.strip()
    if raw.startswith("<"):
        end = raw.find(">")
        if end < 0:
            raise ValueError("unclosed angle-bracket destination")
        value, rest = raw[1:end], raw[end + 1 :].strip()
    else:
        match = re.match(r"((?:\\.|[^\s])*)(.*)", raw, re.S)
        value, rest = match[1], match[2].strip()
    if rest and not re.fullmatch(r'"[^"\n]*"|\x27[^\x27\n]*\x27|\([^\n]*\)', rest):
        raise ValueError("unsupported link destination or title; use <...> for spaces")
    return html.unescape(re.sub(r"\\([!\"#$%&'()*+,./:;<=>?@\[\]\\^_`{|}~-])", r"\1", value))


def references(text):
    text = without_inline_code(without_examples(text))
    definitions = {}
    definition_ranges = []
    errors = []
    links = []
    for match in re.finditer(r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(.+)$", text, re.M):
        line = text.count("\n", 0, match.start()) + 1
        try:
            key = " ".join(match[1].lower().split())
            if key not in definitions:
                definitions[key] = destination(match[2])
        except ValueError as error:
            errors.append((line, str(error)))
        definition_ranges.append((match.start(), match.end()))
    # Mask definitions so their labels are not mistaken for uses.
    for start, end in reversed(definition_ranges):
        text = text[:start] + " " * (end - start) + text[end:]
    labels, stack = [], []
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "[":
            stack.append(index)
        elif char == "]" and stack:
            labels.append((stack.pop(), index))
        index += 1
    excluded = []
    for label_start, label_end in sorted(labels):
        if any(first <= label_start < last for first, last in excluded):
            continue
        label = text[label_start + 1 : label_end]
        start = label_end + 1
        line = text.count("\n", 0, label_start) + 1
        raw = None
        if text[start : start + 1] == "(":
            depth, angle, quoted, escaped = 1, False, None, False
            for end in range(start + 1, len(text)):
                char = text[end]
                if escaped:
                    escaped = False
                    continue
                if char == "\\":
                    escaped = True
                elif quoted:
                    if char == quoted:
                        quoted = None
                elif angle:
                    angle = char != ">"
                elif char == "<":
                    angle = True
                elif char in "\"'" and text[end - 1].isspace():
                    quoted = char
                elif char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        raw = text[start + 1 : end]
                        excluded.append((start, end + 1))
                        break
                elif char == "\n":
                    break
            if raw is None:
                errors.append((line, "unclosed or multiline inline link"))
                continue
        elif text[start : start + 1] == "[":
            end = text.find("]", start + 1)
            if end < 0 or "\n" in text[start:end]:
                errors.append((line, "unclosed reference link"))
                continue
            key = text[start + 1 : end] or label
            excluded.append((start, end + 1))
            key = " ".join(key.lower().split())
            if key not in definitions:
                errors.append((line, f"undefined reference [{key}]"))
                continue
            links.append((line, definitions[key]))
            continue
        else:
            key = " ".join(label.lower().split())
            if key in definitions:
                links.append((line, definitions[key]))
            continue
        try:
            links.append((line, destination(raw)))
        except ValueError as error:
            errors.append((line, str(error)))
    return links, errors


def anchors(text):
    text = without_examples(text)
    found = set(re.findall(r'<[^>]+\b(?:id|name)=["\x27]([^"\x27]+)["\x27]', text))
    used = set()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.match(r"^ {0,3}#{1,6}[ \t]+(.+?)\s*#*\s*$", line)
        heading = match[1] if match else None
        if heading is None and i + 1 < len(lines) and line.strip() and re.fullmatch(r" {0,3}(=+|-+)\s*", lines[i + 1]):
            heading = line.strip()
        if heading is None:
            continue
        heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]*>", "", heading)).lower()
        base = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        slug, suffix = base, 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        found.add(slug)
    return found


def inside(root, path):
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("path escapes project root")
    return resolved


def select_files(root, paths):
    errors, files = [], set()
    for value in paths or [p for p in DEFAULT_PATHS if (root / p).exists()]:
        path = root / value
        try:
            inside(root, path)
            if not path.exists():
                raise ValueError("selected path does not exist")
            if path.is_dir():
                def traversal_error(error):
                    errors.append(f"{value}: cannot traverse {error.filename}: {error.strerror}")

                for current, dirs, names in os.walk(path, followlinks=False, onerror=traversal_error):
                    dirs[:] = sorted(d for d in dirs if d not in EXCLUDED and not (Path(current) / d).is_symlink())
                    for name in sorted(names):
                        item = Path(current) / name
                        if item.suffix.lower() == ".md":
                            inside(root, item)
                            files.add(item)
            elif path.suffix.lower() == ".md":
                files.add(path)
            else:
                raise ValueError("selected file is not Markdown")
        except (ValueError, OSError, RuntimeError) as error:
            errors.append(f"{value}: {error}")
    if not files:
        errors.append("no Markdown files selected")
    return sorted(files), errors


def check(root, paths=None):
    root = Path(root).resolve()
    files, errors = select_files(root, paths)
    checked = 0
    for path in files:
        name = path.relative_to(root)
        try:
            links, parse_errors = references(path.read_text(encoding="utf-8"))
            errors.extend(f"{name}:{line}: {error}" for line, error in parse_errors)
            for line, link in links:
                source_line = re.fullmatch(r"([^:]+):([0-9]+)", link)
                if source_line and not any(char in source_line[1] for char in "/."):
                    candidate = path.parent / source_line[1]
                    if not candidate.exists() and not candidate.is_symlink():
                        source_line = None
                if link.startswith("//") or (re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) and not source_line):
                    continue
                checked += 1
                try:
                    parts = urlsplit(source_line[1] if source_line else link)
                    value = unquote(parts.path)
                    target = root / value.lstrip("/") if value.startswith("/") else path.parent / value if value else path
                    target = inside(root, target)
                    if not target.exists():
                        raise ValueError(f"missing target {link}")
                    fragment = unquote(parts.fragment)
                    line_range = re.fullmatch(r"L([0-9]+)(?:-L?([0-9]+))?", fragment)
                    if source_line or line_range:
                        first = int(source_line[2]) if source_line else int(line_range[1])
                        last = first if source_line else int(line_range[2] or first)
                        if not 1 <= first <= last <= len(target.read_text(encoding="utf-8").splitlines()):
                            raise ValueError(f"source line outside target {link}")
                    elif fragment:
                        if target.suffix.lower() not in {".md", ".html", ".htm", ".svg"}:
                            raise ValueError(f"unsupported fragment on non-document target {link}")
                        if fragment not in anchors(target.read_text(encoding="utf-8")):
                            raise ValueError(f"missing fragment {link}")
                except (ValueError, OSError, UnicodeError, RuntimeError) as error:
                    errors.append(f"{name}:{line}: {error}")
        except (OSError, UnicodeError) as error:
            errors.append(f"{name}: {error}")
    return sorted(errors), len(files), checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root (default: current directory)")
    parser.add_argument("paths", nargs="*", help="Markdown files or directories relative to root")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error("root must be an existing directory")
    errors, files, links = check(args.root, args.paths)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {files} Markdown files and {links} local references; {len(errors)} errors.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
