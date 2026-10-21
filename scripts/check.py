"""Run ADP's local tests, generated-reference checks, and documentation checks."""

from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "product/scripts/check_docs.py"


def main():
    commands = [
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
        ["scripts/build_catalog.py", "--check"],
        [str(CHECKER), "--root", str(ROOT), "README.md", "AGENTS.md", "docs", "product"],
    ]
    failed = False
    for arguments in commands:
        print("Running:", sys.executable, "-B", *arguments, flush=True)
        result = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT)
        failed = result.returncode != 0 or failed
    with tempfile.TemporaryDirectory(prefix="adp-check-") as directory:
        target = Path(directory) / "project"
        for arguments in ([str(ROOT / "export.py"), str(target), "--apply"],
                          [str(target / ".agents/adp/scripts/check_docs.py"), "--root", str(target), "ADP.md", ".agents"]):
            result = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = result.stdout if result.returncode else "\n".join(result.stdout.splitlines()[-1:]) + "\n"
            print(output, end="", flush=True)
            failed = result.returncode != 0 or failed
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
