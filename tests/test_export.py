import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adp_export", ROOT / "export.py")
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.target = Path(self.directory.name) / "project"

    def run_export(self, *arguments):
        return subprocess.run([sys.executable, "-B", str(ROOT / "export.py"), str(self.target), *arguments], capture_output=True, text=True)

    def test_preview_is_read_only_and_install_is_discoverable(self):
        result = self.run_export()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())
        self.assertNotIn("create AGENTS.md", result.stdout)
        self.assertNotIn("create .claude/CLAUDE.md", result.stdout)
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / ".claude/skills/adp-setup/SKILL.md").is_file())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".claude/CLAUDE.md").exists())
        result = subprocess.run([sys.executable, "-B", str(self.target / ".agents/adp/scripts/check_docs.py"), "--root", str(self.target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rerun_preserves_project_files_and_unrelated_skills(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        instructions = self.target / "AGENTS.md"
        custom = "Custom project rules.\n"
        instructions.write_text(custom)
        user_skill = self.target / ".agents/skills/my-skill/SKILL.md"
        user_skill.parent.mkdir()
        user_skill.write_text("My skill\n")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Installed 0 missing paths", result.stdout)
        self.assertEqual(instructions.read_text(), custom)
        self.assertEqual(user_skill.read_text(), "My skill\n")

    def test_existing_instructions_need_no_imports_and_are_not_read_or_written(self):
        (self.target / ".claude").mkdir(parents=True)
        instructions = [self.target / "AGENTS.md", self.target / ".claude/CLAUDE.md"]
        for path in instructions:
            path.write_bytes(b"Project-owned instructions without ADP imports\n\xff")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in instructions:
            self.assertEqual(path.read_bytes(), b"Project-owned instructions without ADP imports\n\xff")
        self.assertTrue((self.target / ".agents/skills/adp-setup/SKILL.md").is_file())

    def test_different_installed_content_fails_before_writes(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        modified = self.target / ".agents/adp/rules.md"
        modified.write_text("Changed installed pipeline\n")
        missing = self.target / ".agents/skills/adp-completion/SKILL.md"
        missing.unlink()
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("initial export cannot update", result.stderr)
        self.assertFalse(missing.exists())
        self.assertEqual(modified.read_text(), "Changed installed pipeline\n")

    def test_symlink_parent_and_leaf_cannot_write_outside_project(self):
        with tempfile.TemporaryDirectory() as outside:
            self.target.mkdir()
            (self.target / ".agents").symlink_to(outside, target_is_directory=True)
            result = self.run_export("--apply")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(list(Path(outside).iterdir()), [])
            self.assertFalse((self.target / "AGENTS.md").exists())
            (self.target / ".agents").unlink()
            leaf = Path(outside) / "instructions.md"
            leaf.write_text("Unrelated content\n")
            (self.target / ".agents/adp").mkdir(parents=True)
            (self.target / ".agents/adp/rules.md").symlink_to(leaf)
            result = self.run_export("--apply")
            self.assertEqual(result.returncode, 1)
            self.assertEqual(leaf.read_text(), "Unrelated content\n")
            self.assertFalse((self.target / ".agents/skills").exists())

    def test_existing_discovery_directory_is_preserved(self):
        discovery = self.target / ".claude/skills"
        discovery.mkdir(parents=True)
        (discovery / "custom.md").write_text("Custom discovery\n")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("integrate discovery manually", result.stderr)
        self.assertEqual((discovery / "custom.md").read_text(), "Custom discovery\n")
        self.assertFalse((self.target / ".agents").exists())

    def test_existing_instruction_symlinks_are_outside_export_scope(self):
        (self.target / ".claude").mkdir(parents=True)
        outside = Path(self.directory.name) / "external-instructions.md"
        outside.write_text("External project rules\n")
        for relative in ("AGENTS.md", ".claude/CLAUDE.md"):
            (self.target / relative).symlink_to(outside)
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(outside.read_text(), "External project rules\n")
        for relative in ("AGENTS.md", ".claude/CLAUDE.md"):
            self.assertTrue((self.target / relative).is_symlink())

    def test_plain_python_preview_does_not_create_source_bytecode_or_target_files(self):
        checkout = Path(self.directory.name) / "checkout"
        exporter.shutil.copytree(exporter.TEMPLATE, checkout / "template", symlinks=True)
        exporter.shutil.copyfile(ROOT / "export.py", checkout / "export.py")
        self.target.mkdir()
        instructions = self.target / "AGENTS.md"
        instructions.write_text("Project rules without imports\n")
        before = sorted(p.relative_to(checkout) for p in checkout.rglob("*"))
        environment = os.environ.copy()
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run([sys.executable, str(checkout / "export.py"), str(self.target)], capture_output=True, text=True, env=environment)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, sorted(p.relative_to(checkout) for p in checkout.rglob("*")))
        self.assertEqual(list(self.target.iterdir()), [instructions])

    def test_overlap_and_template_symlinks_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            exporter.installation_plan(ROOT / "nested-project")
        source = Path(self.directory.name) / "source"
        source.mkdir()
        (source / "escape").symlink_to("/", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "unsupported template symlink"):
            exporter.installation_plan(self.target, source)

    def test_unreadable_source_directory_and_missing_rules_fail_preflight(self):
        source = Path(self.directory.name) / "source"
        exporter.shutil.copytree(exporter.TEMPLATE, source, symlinks=True)
        original = exporter.os.scandir
        denied = source / ".agents/adp"

        def scandir(path):
            if Path(path) == denied:
                raise PermissionError(13, "Permission denied", str(denied))
            return original(path)

        with mock.patch.object(exporter.os, "scandir", side_effect=scandir):
            with self.assertRaisesRegex(ValueError, "cannot read template directory"):
                exporter.installation_plan(self.target, source)
        self.assertFalse(self.target.exists())
        (denied / "rules.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing required"):
            exporter.installation_plan(self.target, source)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
