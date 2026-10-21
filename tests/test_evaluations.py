import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/evaluate_skills.py"
spec = importlib.util.spec_from_file_location("evaluations", SCRIPT)
evaluations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluations)


class EvaluationTests(unittest.TestCase):
    def test_prepare_refuses_existing_workspace_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            marker = workspace / "keep.txt"
            marker.write_text("Keep this\n")
            with self.assertRaises(FileExistsError):
                evaluations.prepare("setup-new", workspace)
            self.assertEqual(list(workspace.iterdir()), [marker])
            self.assertEqual(marker.read_text(), "Keep this\n")

    def test_unexecuted_setup_and_modified_adp_files_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "case"
            evaluations.prepare("setup-new", workspace)
            self.assertTrue(evaluations.check(workspace))
            rules = workspace / "project/.agents/adp/rules.md"
            rules.write_text("Weakened rules\n")
            self.assertIn("ADP-owned entries changed", evaluations.check(workspace))

    def test_modified_visible_human_guide_is_an_owned_change(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "case"
            evaluations.prepare("setup-new", workspace)
            (workspace / "project/ADP.md").write_text("Changed ADP guide\n")
            self.assertEqual(evaluations.check(workspace), ["ADP-owned entries changed"])

    def test_example_imports_and_added_owned_symlinks_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "case"
            evaluations.prepare("setup-new", workspace)
            project = workspace / "project"
            for text in ("```markdown\n@.agents/adp/rules.md\n```\n", "<!--\n@.agents/adp/rules.md\n-->\n"):
                with self.subTest(text=text):
                    (project / "AGENTS.md").write_text(text)
                    self.assertIn("missing or duplicate active ADP import", evaluations.check(workspace))
            (project / ".agents/adp/extra-link").symlink_to("/outside/path")
            self.assertEqual(evaluations.check(workspace), ["ADP-owned entries changed"])

    def test_approved_signature_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "case"
            evaluations.prepare("partial-delivery", workspace)
            source = workspace / "project/calculator.py"
            source.write_text(source.read_text().replace("def add(left, right)", "def add(lhs, rhs)"))
            self.assertIn("approved add signature changed", evaluations.check(workspace))

    def test_migrated_helper_accepts_python_options_and_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            helper = project / ".claude/commands/helper.py"
            helper.parent.mkdir(parents=True)
            helper.write_text("print('fixture-helper')\n")
            (helper.parent / "helper.md").write_text("# Helper\n")
            skill = project / ".agents/skills/sample"
            skill.mkdir(parents=True)
            (skill / "helper.py").symlink_to("../../../.claude/commands/helper.py")
            for options in ("", "-B ", "-X dev "):
                with self.subTest(options=options):
                    (skill / "SKILL.md").write_text(f"Read [helper](../../../.claude/commands/helper.md). Run `python3 {options}../../../.claude/commands/helper.py`.\n")
                    self.assertEqual(evaluations.check_migrated_skill(project), [])
            for options in ("-c'print(\"fixture-helper\")' ", "-c 'print(\"fixture-helper\")' ", "-mjson.tool "):
                with self.subTest(options=options):
                    (skill / "SKILL.md").write_text(f"Read [helper](../../../.claude/commands/helper.md). Run `python3 {options}../../../.claude/commands/helper.py`.\n")
                    self.assertIn("migrated skill command changed its target", evaluations.check_migrated_skill(project))

    def test_completed_setup_does_not_require_a_retained_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "case"
            evaluations.prepare("setup-new", workspace)
            project = workspace / "project"
            (project / "AGENTS.md").write_text("@.agents/adp/rules.md\nRead that file when imports are unsupported.\n")
            (project / ".claude/CLAUDE.md").write_text("@../AGENTS.md\n")
            self.assertFalse((project / "plan").exists())
            self.assertEqual(evaluations.check(workspace), [])


if __name__ == "__main__":
    unittest.main()
