"""Preview or install ADP files; project instructions are created by setup."""

import argparse
import os
from pathlib import Path
import shutil
import sys


REPO = Path(__file__).resolve().parent
TEMPLATE = REPO / "template"
DISCOVERY = Path(".claude/skills")
DISCOVERY_TARGET = "../.agents/skills"


def owned(path):
    return path.is_relative_to(".agents/adp") or (
        len(path.parts) >= 3 and path.parts[:2] == (".agents", "skills") and path.parts[2].startswith("adp-")
    )


def no_symlink_parents(root, relative):
    current = root
    for part in relative.parts[:-1]:
        current /= part
        if current.is_symlink():
            raise ValueError(f"{relative}: refusing symlink directory {current.relative_to(root)}")
        if current.exists() and not current.is_dir():
            raise ValueError(f"{relative}: parent is not a directory")


def installation_plan(target, template=TEMPLATE):
    target = Path(target).absolute()
    # Resolve only the user-selected root; never traverse symlinks below it.
    target = target.resolve()
    if target.is_relative_to(REPO) or REPO.is_relative_to(target):
        raise ValueError("target must not overlap this ADP checkout")
    if target.exists() and not target.is_dir():
        raise ValueError("target must be a directory")
    if not template.is_dir():
        raise ValueError("template directory is missing")
    sources = []
    def traversal_error(error):
        raise ValueError(f"cannot read template directory {error.filename}: {error.strerror}") from error

    for current, directories, names in os.walk(template, followlinks=False, onerror=traversal_error):
        directories.sort()
        for name in sorted(directories + names):
            source = Path(current) / name
            relative = source.relative_to(template)
            if source.is_symlink():
                if relative != DISCOVERY or os.readlink(source) != DISCOVERY_TARGET:
                    raise ValueError(f"unsupported template symlink: {relative}")
                sources.append(relative)
            elif source.is_file():
                sources.append(relative)
    required = [DISCOVERY, Path(".agents/adp/rules.md"), Path(".agents/memory/MEMORY.md"), Path(".agents/skills/adp-setup/SKILL.md")]
    if any(relative not in sources for relative in required):
        raise ValueError("template is missing required shared rules, memory starter, setup skill, or discovery")
    actions = []
    for relative in sorted(sources):
        source, destination = template / relative, target / relative
        no_symlink_parents(target, relative)
        if relative == DISCOVERY:
            if destination.is_symlink():
                if os.readlink(destination) != DISCOVERY_TARGET:
                    raise ValueError(f"{relative}: expected symlink to {DISCOVERY_TARGET}; integrate discovery manually")
                continue
            if destination.exists():
                raise ValueError(f"{relative}: existing path must remain intact; integrate discovery manually")
        else:
            if destination.is_symlink():
                raise ValueError(f"{relative}: refusing existing symlink")
            if destination.exists():
                if not destination.is_file():
                    raise ValueError(f"{relative}: existing path is not a file")
                if owned(relative):
                    if source.read_bytes() != destination.read_bytes():
                        raise ValueError(f"{relative}: installed ADP content differs; initial export cannot update it")
                continue
        actions.append(relative)
    return target, actions


def install(target, actions, template=TEMPLATE):
    for relative in actions:
        destination = target / relative
        no_symlink_parents(target, relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if relative == DISCOVERY:
            destination.symlink_to(DISCOVERY_TARGET, target_is_directory=True)
        else:
            # Exclusive creation prevents replacing a file added after preflight.
            with destination.open("xb") as output, (template / relative).open("rb") as source:
                shutil.copyfileobj(source, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--apply", action="store_true", help="create the previewed missing files")
    args = parser.parse_args()
    try:
        target, actions = installation_plan(args.target)
        for relative in actions:
            print(f"create {relative}")
        if args.apply:
            install(target, actions)
            print(f"Installed {len(actions)} missing paths into {target}. Existing project files preserved.")
        else:
            print(f"Preview: {len(actions)} missing paths for {target}. Use --apply to install.")
        return 0
    except (ValueError, OSError, UnicodeError, RuntimeError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        print("No rollback is promised after an unexpected I/O failure during application.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
