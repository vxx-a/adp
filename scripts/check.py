"""Run ADP's local tests, generated-reference checks, and documentation checks."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "template/.agents/adp/scripts/check_docs.py"


def main():
    commands = [
        ["-m", "unittest", "discover", "-s", "tests", "-v"],
        ["scripts/build_catalog.py", "--check"],
        [str(CHECKER), "--root", str(ROOT)],
        [str(CHECKER), "--root", str(ROOT / "template")],
    ]
    failed = False
    for arguments in commands:
        print("Running:", sys.executable, "-B", *arguments, flush=True)
        result = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT)
        failed = result.returncode != 0 or failed
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
