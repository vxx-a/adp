"""Prepare disposable skill cases or check observable outcomes; does not invoke an agent."""

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys


REPO = Path(__file__).resolve().parents[1]
CASES = REPO / "tests/fixtures/skills.json"
SPEC = importlib.util.spec_from_file_location("evaluation_docs", REPO / "product/scripts/check_docs.py")
DOCUMENTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCUMENTS)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owned_entries(project):
    entries = {}
    for parent in (project / ".agents", project / ".agents/skills"):
        if parent.is_symlink():
            return {str(parent.relative_to(project)): "symlink:" + os.readlink(parent)}
    for root in [project / "ADP.md", project / ".agents/adp", *sorted((project / ".agents/skills").glob("adp-*"))]:
        for path in [root, *root.rglob("*")] if not root.is_symlink() else [root]:
            if path.is_symlink():
                entries[str(path.relative_to(project))] = "symlink:" + os.readlink(path)
            elif path.is_file():
                entries[str(path.relative_to(project))] = digest(path)
    return entries


def check_migrated_skill(project):
    skill = project / ".agents/skills/sample"
    content = (skill / "SKILL.md").read_text(encoding="utf-8") if (skill / "SKILL.md").is_file() else ""
    link = re.search(r"\[helper\]\(([^)]+)\)", content)
    command = re.search(r"`(python3 [^`]+)`", content)
    tokens = shlex.split(command[1]) if command else []
    option = 1
    while option < len(tokens) - 1:
        if tokens[option] in {"-B", "-u", "-E", "-s", "-S", "-I", "-O", "-OO", "-Xdev"}:
            option += 1
        elif tokens[option:option + 2] == ["-X", "dev"]:
            option += 2
        else:
            break
    helper = (project / ".claude/commands/helper.py").resolve()
    errors = []
    if link is None or (skill / link[1]).resolve() != (project / ".claude/commands/helper.md").resolve():
        errors.append("migrated skill link changed its target")
    if len(tokens) < 2 or option != len(tokens) - 1 or (skill / tokens[-1]).resolve() != helper:
        errors.append("migrated skill command changed its target")
    resource = skill / "helper.py"
    if not resource.is_symlink() or resource.resolve() != helper:
        errors.append("migrated resource symlink changed its target")
    if not errors:
        for arguments in ([str(resource)], tokens[1:]):
            result = subprocess.run([sys.executable, "-B", *arguments], cwd=skill, capture_output=True, text=True, timeout=10)
            if result.returncode != 0 or result.stdout.strip() != "fixture-helper":
                errors.append("migrated helper no longer runs")
    return errors


def prepare(case, workspace):
    definition = json.loads(CASES.read_text(encoding="utf-8"))[case]
    workspace.mkdir()  # Refuse an existing workspace, including a symlink.
    project = workspace / "project"
    project.mkdir()
    for name, content in definition["files"].items():
        path = project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    for name, target in definition.get("symlinks", {}).items():
        (project / name).symlink_to(target)
    (workspace / "outside.md").write_text("Outside the project; leave unchanged.\n", encoding="utf-8")
    subprocess.run([sys.executable, "-B", str(REPO / "export.py"), str(project), "--apply"], check=True, stdout=subprocess.DEVNULL)
    baseline = {"case": case, "owned": owned_entries(project),
                "preserve": {name: digest(project / name) for name in definition["preserve"]},
                "outside": digest(workspace / "outside.md")}
    (workspace / "baseline.json").write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    (workspace / "request.md").write_text(definition["request"] + "\n", encoding="utf-8")
    print(f"Project: {project}\nRequest: {workspace / 'request.md'}")


def check(workspace):
    baseline = json.loads((workspace / "baseline.json").read_text(encoding="utf-8"))
    case = baseline["case"]
    project = workspace / "project"
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    require(owned_entries(project) == baseline["owned"], "ADP-owned entries changed")
    if errors:
        return errors
    for name, expected in baseline["preserve"].items():
        path = project / name
        require(path.is_file() and not path.is_symlink() and digest(path) == expected, f"protected file changed: {name}")
    require(digest(workspace / "outside.md") == baseline["outside"], "outside resource changed")

    if case == "setup-unsafe":
        original = project / ".claude/skills/sample/helper.md"
        require(original.is_symlink() and os.readlink(original) == "../../../../outside.md", "unsafe skill resource was moved or changed")
        require(not os.path.lexists(project / ".agents/skills/sample"), "unsafe skill was migrated")
        require(not (project / ".claude/skills").is_symlink(), "blocked discovery directory was replaced")
    else:
        instructions = project / "AGENTS.md"
        text = instructions.read_text(encoding="utf-8") if instructions.is_file() else ""
        require(not instructions.is_symlink() and len(re.findall(r"^@\.agents/adp/rules\.md\s*$", DOCUMENTS.without_examples(text), re.M)) == 1, "missing or duplicate active ADP import")
        wrapper = project / ".claude/CLAUDE.md"
        require(wrapper.is_file() and not wrapper.is_symlink() and wrapper.read_text(encoding="utf-8").strip() == "@../AGENTS.md", "Claude wrapper must import AGENTS.md once")
        require(not os.path.lexists(project / "CLAUDE.md"), "root CLAUDE.md remains")
        discovery = project / ".claude/skills"
        require(discovery.is_symlink() and os.readlink(discovery) == "../.agents/skills", "skill discovery is not integrated")
        if case == "setup-existing":
            for rule in ("Never deploy without explicit authorization.", "Use descriptive error messages.", "@.claude/rules/local.md"):
                require(rule in text, f"project rule/import lost: {rule}")
            if not errors:
                errors.extend(check_migrated_skill(project))
        elif case == "partial-delivery":
            source = (project / "calculator.py").read_text(encoding="utf-8")
            functions = {node.name: node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)}
            original = json.loads(CASES.read_text(encoding="utf-8"))[case]["files"]["calculator.py"]
            old_functions = {node.name: node for node in ast.parse(original).body if isinstance(node, ast.FunctionDef)}
            require("multiply" in functions and ast.dump(functions["multiply"]) == ast.dump(old_functions["multiply"]), "unfinished multiply implementation changed")
            require("add" in functions and ast.dump(functions["add"].args) == ast.dump(old_functions["add"].args), "approved add signature changed")
            require((project / "tests").is_dir() and any((project / "tests").rglob("test*.py")), "implementation tests are missing")
            original_docs = json.loads(CASES.read_text(encoding="utf-8"))[case]["files"]["docs/design.md"]
            require((project / "docs/design.md").read_text(encoding="utf-8") != original_docs, "current design was not reconciled")
            if not errors:
                program = "from calculator import add\nassert add(2, 3) == 5\nassert add(0, 0) == 0\nfor pair in ((-1, 2), (2, -1)):\n    try:\n        add(*pair)\n    except ValueError:\n        continue\n    raise AssertionError('negative argument accepted')\n"
                result = subprocess.run([sys.executable, "-B", "-c", program], cwd=project, capture_output=True, text=True, timeout=10)
                require(result.returncode == 0, "add acceptance failed: " + result.stderr.strip())
                result = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=project, capture_output=True, text=True, timeout=30)
                require(result.returncode == 0 and re.search(r"Ran [1-9][0-9]* tests?\b", result.stderr) is not None, "implementation test suite failed or ran no tests: " + result.stderr.strip())

    if not errors:
        result = subprocess.run([sys.executable, "-B", str(project / ".agents/adp/scripts/check_docs.py"), "--root", str(project)], capture_output=True, text=True, timeout=30)
        require(result.returncode == 0, "project documentation references failed: " + result.stderr.strip())
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("prepare", help="create a new workspace; never reuse an existing path")
    create.add_argument("case", choices=sorted(json.loads(CASES.read_text(encoding="utf-8"))))
    create.add_argument("workspace", type=Path)
    verify = commands.add_parser("check", help="check a prepared case; executes fixture Python after preservation checks")
    verify.add_argument("workspace", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.case, args.workspace.absolute())
        else:
            errors = check(args.workspace.absolute())
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print("Observable acceptance passed. Confirm loaded skills, review, and stopping separately.")
        return 0
    except (OSError, ValueError, SyntaxError, subprocess.SubprocessError) as error:
        print(f"Evaluation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
