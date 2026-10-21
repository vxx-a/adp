"""Preview or apply ADP installs and updates; project instructions are created by setup."""

import argparse
import difflib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


REPO = Path(__file__).resolve().parent
PRODUCT = Path("product")
# Only these sources under product/ ship; maintainer content stays outside.
SOURCES = {
    "adp": ".agents/adp",
    "skills": ".agents/skills",
    "scripts/check_docs.py": ".agents/adp/scripts/check_docs.py",
    "memory/MEMORY.md": ".agents/memory/MEMORY.md",
    "USAGE.md": "ADP.md",
    "LICENSE": ".agents/adp/LICENSE",
    "CHANGELOG.md": ".agents/adp/CHANGELOG.md",
    "release.json": ".agents/adp/release.json",
}
DISCOVERY = Path(".claude/skills")
DISCOVERY_TARGET = "../.agents/skills"


def owned(path):
    return path == Path("ADP.md") or path.is_relative_to(".agents/adp") or (
        len(path.parts) >= 3 and path.parts[:2] == (".agents", "skills") and path.parts[2].startswith("adp-")
    )


def source_identity(repo):
    """Archives have no Git identity; do not imply their version names a clean revision."""
    try:
        toplevel = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], check=True, capture_output=True, text=True).stdout.strip()
        if Path(toplevel).resolve() != repo.resolve():
            return {"revision": None, "modified": None}
        revision = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        status = subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--", "product", "export.py"], check=True, capture_output=True, text=True).stdout
        return {"revision": revision, "modified": bool(status)}
    except (OSError, subprocess.CalledProcessError):
        return {"revision": None, "modified": None}


def no_symlink_parents(root, relative):
    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink():
            raise ValueError(f"{relative}: refusing symlink directory {current.relative_to(root)}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"{relative}: parent is not a directory")


def obsolete_paths(target, sources):
    """Owned files the product no longer ships, and owned directories that would be left empty, deepest first."""
    skills = target / ".agents/skills"
    roots = [target / ".agents/adp"] + ([p for p in sorted(skills.glob("adp-*")) if p.is_dir()] if skills.is_dir() else [])
    # Compare by identity so a case-only name difference on a case-insensitive filesystem is not removed.
    identity = lambda path: (path.lstat().st_dev, path.lstat().st_ino)
    shipped_paths = set(sources) | {parent for relative in sources for parent in relative.parents}
    shipped = {identity(target / relative) for relative in shipped_paths if os.path.lexists(target / relative)}
    def traversal_error(error):
        raise ValueError(f"cannot read installed directory {error.filename}: {error.strerror}") from error

    found = []
    for root in roots:
        if root.is_symlink():
            raise ValueError(f"{root.relative_to(target)}: refusing symlink in ADP-owned path")
        if not root.is_dir():
            continue
        for current, directories, names in os.walk(root, topdown=False, followlinks=False, onerror=traversal_error):
            current = Path(current)
            kept = False
            for path in (current / name for name in directories + names):
                relative = path.relative_to(target)
                if path.is_symlink():
                    raise ValueError(f"{relative}: refusing symlink in ADP-owned path")
                if path.is_file() and relative not in sources and identity(path) not in shipped:
                    found.append(relative)
                elif relative not in found:  # bottom-up walk: emptied subdirectories are already listed
                    kept = True
            if not kept and identity(current) not in shipped:
                found.append(current.relative_to(target))
    return found


def product_files(repo=REPO):
    """Collect the explicit product roots and reject links or special files."""
    files = {}

    def traversal_error(error):
        raise ValueError(f"cannot read product directory {error.filename}: {error.strerror}") from error

    for name, destination in SOURCES.items():
        source = repo / PRODUCT / name
        no_symlink_parents(repo, PRODUCT / name)
        if source.is_symlink():
            raise ValueError(f"unsupported product symlink: {name}")
        if not source.exists():
            raise ValueError(f"missing required product source: {name}")
        paths = [source]
        if source.is_dir():
            paths = []
            for current, directories, names in os.walk(source, followlinks=False, onerror=traversal_error):
                for entry in sorted(directories + names):
                    path = Path(current) / entry
                    if path.is_symlink():
                        raise ValueError(f"unsupported product symlink: {path.relative_to(repo)}")
                    if not path.is_dir():
                        paths.append(path)
        for path in sorted(paths):
            if not path.is_file():
                raise ValueError(f"unsupported product file: {path.relative_to(repo)}")
            relative = path.relative_to(source) if source.is_dir() else Path()
            target = Path(destination) / relative
            if name == "skills" and (len(relative.parts) < 2 or not relative.parts[0].startswith("adp-")):
                raise ValueError(f"unsupported product skill: {relative}")
            if name == "adp" and path.suffix != ".md":
                raise ValueError(f"unsupported policy file: {path.relative_to(repo)}")
            files[target] = path.read_bytes()
    required = {Path(".agents/adp/rules.md"), Path(".agents/adp/skills.md"), Path(".agents/memory/MEMORY.md"), Path(".agents/skills/adp-setup/SKILL.md")}
    if not required <= files.keys():
        raise ValueError("product is missing required shared rules, catalog, memory starter, or setup skill")
    release = json.loads(files[Path(".agents/adp/release.json")])
    if not isinstance(release, dict) or not isinstance(release.get("version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", release["version"]) or not isinstance(release.get("repository"), str) or not release["repository"].startswith("https://"):
        raise ValueError("release.json requires a numeric version and HTTPS repository URL")
    digest = hashlib.sha256()
    for name, content in sorted(files.items()):
        digest.update(str(name).encode("utf-8") + b"\0" + str(len(content)).encode("ascii") + b"\0" + content)
    metadata = {"schema": 2, "version": release["version"], "repository": release["repository"], "source": source_identity(repo), "sha256": digest.hexdigest(), "owned_root_files": ["ADP.md"]}
    files[Path(".agents/adp/version.json")] = (json.dumps(metadata, indent=2) + "\n").encode("utf-8")
    files[DISCOVERY] = None
    return files


def installation_plan(target, repo=REPO):
    # Resolve only the user-selected root; never traverse symlinks below it.
    target = Path(target).absolute().resolve()
    if target.is_relative_to(repo.resolve()) or repo.resolve().is_relative_to(target):
        raise ValueError("target must not overlap this ADP checkout")
    if target.exists() and not target.is_dir():
        raise ValueError("target must be a directory")
    sources = product_files(repo)
    actions = []
    for relative in sorted(sources):
        destination = target / relative
        no_symlink_parents(target, relative)
        if relative == DISCOVERY:
            if destination.is_symlink():
                if os.readlink(destination) != DISCOVERY_TARGET:
                    raise ValueError(f"{relative}: expected symlink to {DISCOVERY_TARGET}; integrate discovery manually")
                continue
            if destination.is_dir():
                # adp-setup migrates the project's skills to .agents/skills and then creates the link.
                actions.append(("skip", relative))
                continue
            if destination.exists():
                raise ValueError(f"{relative}: existing path must remain intact; integrate discovery manually")
        else:
            if destination.is_symlink():
                raise ValueError(f"{relative}: refusing existing symlink")
            if destination.exists():
                if not destination.is_file():
                    raise ValueError(f"{relative}: existing path is not a file")
                if relative == Path("ADP.md"):
                    version = Path(".agents/adp/version.json")
                    no_symlink_parents(target, version)
                    installed = target / version
                    try:
                        metadata = json.loads(installed.read_bytes()) if installed.is_file() and not installed.is_symlink() else {}
                    except (ValueError, UnicodeError):
                        metadata = {}
                    roots = metadata.get("owned_root_files") if isinstance(metadata, dict) else None
                    if not isinstance(roots, list) or metadata.get("schema") != 2 or "ADP.md" not in roots:
                        raise ValueError("ADP.md: existing project file has no recorded ADP ownership; move it explicitly before installing")
                if owned(relative) and sources[relative] != destination.read_bytes():
                    actions.append(("update", relative))
                continue
        actions.append(("create", relative))
    actions.sort(key=lambda action: action[1])
    version = Path(".agents/adp/version.json")
    # Publish the fingerprint only after content updates and obsolete cleanup succeed.
    content = [action for action in actions if action[1] != version]
    metadata = [action for action in actions if action[1] == version]
    return target, content + [("remove", relative) for relative in obsolete_paths(target, set(sources))] + metadata


def install(target, actions, repo=REPO):
    sources = product_files(repo)
    for verb, relative in actions:
        destination = target / relative
        no_symlink_parents(target, relative)
        if verb == "skip":
            continue
        if verb == "remove":
            destination.rmdir() if destination.is_dir() and not destination.is_symlink() else destination.unlink()
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative == DISCOVERY:
            destination.symlink_to(DISCOVERY_TARGET, target_is_directory=True)
            continue
        # Write a temporary sibling first so an interrupted run never leaves a partial file.
        output = tempfile.NamedTemporaryFile(mode="wb", prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent, delete=False)
        temporary = Path(output.name)
        try:
            with output, io.BytesIO(sources[relative]) as source:
                shutil.copyfileobj(source, output)
            if verb == "create":
                # Linking refuses a file added after preflight.
                os.link(temporary, destination)
            else:
                os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)


def content_diff(target, actions, repo=REPO):
    """Render file contents for review; preview never creates the destination."""
    sources = product_files(repo)
    lines = []
    for verb, relative in actions:
        path = target / relative
        if verb == "skip" or relative == DISCOVERY or (verb == "remove" and path.is_dir()):
            continue
        before = path.read_bytes() if path.is_file() else b""
        after = b"" if verb == "remove" else sources[relative]
        old = before.decode("utf-8", errors="replace").splitlines(keepends=True)
        new = after.decode("utf-8", errors="replace").splitlines(keepends=True)
        for line in difflib.unified_diff(old, new, fromfile=f"installed/{relative}", tofile=f"proposed/{relative}"):
            lines.append(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n")
    return "".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--apply", action="store_true", help="apply the previewed changes")
    parser.add_argument("--diff", action="store_true", help="include unified content diffs in the preview")
    args = parser.parse_args()
    try:
        target, actions = installation_plan(args.target)
        for verb, relative in actions:
            if verb == "skip":
                print(f"skip {relative}: existing directory; ask your agent to read .agents/skills/adp-setup/SKILL.md, which migrates it")
            else:
                print(f"{verb} {relative}")
        changes = sum(verb != "skip" for verb, _ in actions)
        if args.diff:
            print(content_diff(target, actions), end="")
        if args.apply:
            install(target, actions)
            print(f"Applied {changes} changes to {target}. Project-owned files preserved.")
        else:
            print(f"Preview: {changes} changes for {target}. Use --apply to apply them.")
        return 0
    except (ValueError, OSError, UnicodeError, RuntimeError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        print("Files are replaced one at a time with no rollback. Retry from the same source; if ADP.md ownership was not recorded, inspect and explicitly relocate that guide before retrying.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
