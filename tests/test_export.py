import importlib.util
import json
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

    def copy_product(self, checkout):
        for name in exporter.SOURCES:
            source, destination = ROOT / exporter.PRODUCT / name, checkout / exporter.PRODUCT / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                exporter.shutil.copytree(source, destination)
            else:
                exporter.shutil.copyfile(source, destination)

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


    def test_content_preview_shows_creates_updates_and_deletions_without_writes(self):
        result = self.run_export("--diff")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("+++ proposed/ADP.md", result.stdout)
        self.assertIn("+# Using ADP", result.stdout)
        self.assertFalse(self.target.exists())
        self.assertEqual(self.run_export("--apply").returncode, 0)
        rules = self.target / ".agents/adp/rules.md"
        rules.write_text("Local rule without newline")
        obsolete = self.target / ".agents/adp/retired.md"
        obsolete.write_text("Obsolete policy\n")
        result = self.run_export("--diff")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("-Local rule without newline\n\\ No newline at end of file", result.stdout)
        self.assertIn("+# ADP rules", result.stdout)
        self.assertIn("-Obsolete policy", result.stdout)
        self.assertEqual(rules.read_text(), "Local rule without newline")
        self.assertEqual(obsolete.read_text(), "Obsolete policy\n")

    def test_install_ships_human_guide_version_changelog_and_exact_mit_notice(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        self.assertEqual((self.target / ".agents/adp/LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
        guide = (self.target / "ADP.md").read_text()
        self.assertIn("## Review the plan", guide)
        self.assertIn("## Verify before accepting", guide)
        release = json.loads((ROOT / "product/release.json").read_text())
        metadata = json.loads((self.target / ".agents/adp/version.json").read_text())
        self.assertEqual(metadata["version"], release["version"])
        self.assertEqual(metadata["repository"], release["repository"])
        self.assertEqual(metadata["owned_root_files"], ["ADP.md"])
        self.assertIn(metadata["version"], (self.target / ".agents/adp/CHANGELOG.md").read_text())

    def test_unowned_root_guide_blocks_install_even_on_legacy_or_matching_copy(self):
        self.target.mkdir()
        guide = self.target / "ADP.md"
        original = (ROOT / "product/USAGE.md").read_bytes()
        guide.write_bytes(original)
        metadata = self.target / ".agents/adp/version.json"
        for prior in (None, {"schema": 1, "sha256": "legacy"}, {"schema": 2}, {"schema": 2, "owned_root_files": 1}, []):
            with self.subTest(prior=prior):
                if prior is not None:
                    metadata.parent.mkdir(parents=True, exist_ok=True)
                    metadata.write_text(json.dumps(prior))
                result = self.run_export("--apply")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("no recorded ADP ownership", result.stderr)
                self.assertEqual(guide.read_bytes(), original)
                self.assertFalse((self.target / ".agents/adp/rules.md").exists())

    def test_legacy_hash_only_install_upgrades_and_then_updates_owned_guide(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        guide = self.target / "ADP.md"
        guide.unlink()
        version = self.target / ".agents/adp/version.json"
        version.write_text('{"schema": 1, "sha256": "legacy"}\n')
        self.assertEqual(self.run_export("--apply").returncode, 0)
        guide.write_text("Edited installed guide\n")
        result = self.run_export("--diff")
        self.assertIn("-Edited installed guide", result.stdout)
        self.assertEqual(self.run_export("--apply").returncode, 0)
        self.assertEqual(guide.read_bytes(), (ROOT / "product/USAGE.md").read_bytes())

    def test_source_identity_distinguishes_modified_git_sources_and_archives(self):
        checkout = Path(self.directory.name) / "checkout"
        self.copy_product(checkout)
        metadata = json.loads(exporter.product_files(checkout)[Path(".agents/adp/version.json")])
        self.assertEqual(metadata["source"], {"revision": None, "modified": None})
        revision = "a" * 40
        results = [subprocess.CompletedProcess([], 0, str(checkout) + "\n"), subprocess.CompletedProcess([], 0, revision + "\n"), subprocess.CompletedProcess([], 0, " M product/adp/rules.md\n")]
        with mock.patch.object(exporter.subprocess, "run", side_effect=results):
            self.assertEqual(exporter.source_identity(checkout), {"revision": revision, "modified": True})
        results[2] = subprocess.CompletedProcess([], 0, "")
        with mock.patch.object(exporter.subprocess, "run", side_effect=results):
            self.assertEqual(exporter.source_identity(checkout), {"revision": revision, "modified": False})

    def test_archive_under_another_git_checkout_does_not_inherit_its_identity(self):
        with tempfile.TemporaryDirectory(prefix=".adp-source-test-", dir=ROOT) as directory:
            self.assertEqual(exporter.source_identity(Path(directory)), {"revision": None, "modified": None})

    def test_invalid_release_metadata_fails_before_target_writes(self):
        checkout = Path(self.directory.name) / "checkout"
        self.copy_product(checkout)
        for release in ([], {"version": None}, {"version": "unversioned", "repository": "https://example.test"}):
            with self.subTest(release=release):
                (checkout / "product/release.json").write_text(json.dumps(release))
                with self.assertRaisesRegex(ValueError, "release.json requires"):
                    exporter.installation_plan(self.target, checkout)
                self.assertFalse(self.target.exists())

    def test_interrupted_first_or_legacy_install_requires_explicit_guide_recovery(self):
        base = self.target
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                self.target = base / str(legacy)
                version = self.target / ".agents/adp/version.json"
                if legacy:
                    version.parent.mkdir(parents=True)
                    version.write_text('{"schema": 1, "sha256": "legacy"}\n')
                original_replace, original_link = exporter.os.replace, exporter.os.link

                def publish(source, destination):
                    if destination == version.resolve():
                        raise OSError("metadata interrupted")
                    original_replace(source, destination)

                def create(source, destination):
                    if destination == version.resolve():
                        raise OSError("metadata interrupted")
                    original_link(source, destination)

                with mock.patch.object(exporter.os, "replace", side_effect=publish), mock.patch.object(exporter.os, "link", side_effect=create):
                    with self.assertRaisesRegex(OSError, "metadata interrupted"):
                        exporter.install(*exporter.installation_plan(self.target))
                guide = self.target / "ADP.md"
                self.assertTrue(guide.is_file())
                before = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob("*") if p.is_file()}
                with self.assertRaisesRegex(ValueError, "no recorded ADP ownership"):
                    exporter.installation_plan(self.target)
                self.assertEqual(before, {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob("*") if p.is_file()})
                preserved = self.target / "preserved-guide.md"
                guide.rename(preserved)
                exporter.install(*exporter.installation_plan(self.target))
                self.assertEqual(guide.read_bytes(), preserved.read_bytes())
                self.assertEqual(exporter.installation_plan(self.target)[1], [])
        self.target = base

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
        self.assertIn("Applied 0 changes", result.stdout)
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

    def test_update_replaces_changed_restores_missing_and_removes_obsolete(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        modified = self.target / ".agents/adp/rules.md"
        modified.write_text("Changed installed pipeline\n")
        missing = self.target / ".agents/skills/adp-completion/SKILL.md"
        missing.unlink()
        obsolete = self.target / ".agents/skills/adp-retired/references/notes.md"
        obsolete.parent.mkdir(parents=True)
        obsolete.write_text("Old skill\n")
        stale = self.target / ".agents/adp/old.md"
        stale.write_text("Old rules\n")
        memory = self.target / ".agents/memory/MEMORY.md"
        memory.write_text("Project memory\n")
        user_skill = self.target / ".agents/skills/my-skill/SKILL.md"
        user_skill.parent.mkdir()
        user_skill.write_text("My skill\n")
        result = self.run_export()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines()[:-1], [
            "update .agents/adp/rules.md",
            "create .agents/skills/adp-completion/SKILL.md",
            "remove .agents/adp/old.md",
            "remove .agents/skills/adp-retired/references/notes.md",
            "remove .agents/skills/adp-retired/references",
            "remove .agents/skills/adp-retired",
        ])
        self.assertEqual(modified.read_text(), "Changed installed pipeline\n")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(modified.read_bytes(), (ROOT / "product/adp/rules.md").read_bytes())
        self.assertTrue(missing.is_file())
        self.assertFalse((self.target / ".agents/skills/adp-retired").exists())
        self.assertFalse(stale.exists())
        self.assertEqual(memory.read_text(), "Project memory\n")
        self.assertEqual(user_skill.read_text(), "My skill\n")
        self.assertEqual(list(self.target.rglob(".*.tmp")), [])
        self.assertIn("Preview: 0 changes", self.run_export().stdout)

    def test_rerun_prunes_empty_owned_directories_and_keeps_shipped_and_unowned_paths(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        (self.target / ".agents/skills/adp-retired/assets").mkdir(parents=True)
        emptied = self.target / ".agents/skills/adp-completion"
        (emptied / "SKILL.md").unlink()
        (self.target / ".agents/adp/scripts/check_docs.py").unlink()
        (self.target / ".agents/adp/scripts").rename(self.target / ".agents/adp/Scripts")
        shipped = self.target / ".agents/skills/adp-setup/SKILL.md"
        case_variant = shipped.with_name("skill.md")
        shipped.rename(case_variant)
        loose = self.target / ".agents/skills/adp-notes.md"
        loose.write_text("Project notes\n")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / ".agents/skills/adp-retired").exists())
        self.assertTrue((emptied / "SKILL.md").is_file())
        self.assertTrue(shipped.is_file())
        self.assertTrue((self.target / ".agents/adp/scripts/check_docs.py").is_file())
        self.assertEqual(loose.read_text(), "Project notes\n")
        self.assertIn("Preview: 0 changes", self.run_export().stdout)

    def test_interrupted_update_with_reused_pid_does_not_block_retry(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        rules = self.target / ".agents/adp/rules.md"
        rules.write_text("Previous rules\n")
        leftover = rules.with_name(f".{rules.name}.{os.getpid()}.tmp")
        leftover.write_text("Interrupted write\n")
        target, actions = exporter.installation_plan(self.target)
        exporter.install(target, actions)
        self.assertEqual(rules.read_bytes(), (ROOT / "product/adp/rules.md").read_bytes())
        self.assertFalse(leftover.exists())
        self.assertEqual(exporter.installation_plan(self.target)[1], [])

    def test_failed_copy_or_replace_preserves_destination_and_allows_retry(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        rules = self.target / ".agents/adp/rules.md"
        for owner, operation in ((exporter.shutil, "copyfileobj"), (exporter.os, "replace")):
            with self.subTest(operation=operation):
                rules.write_text("Previous rules\n")
                target, actions = exporter.installation_plan(self.target)
                with mock.patch.object(owner, operation, side_effect=OSError("interrupted write")):
                    with self.assertRaisesRegex(OSError, "interrupted write"):
                        exporter.install(target, actions)
                self.assertEqual(rules.read_text(), "Previous rules\n")
                self.assertEqual(list(rules.parent.glob(".*.tmp")), [])
                exporter.install(*exporter.installation_plan(self.target))
                self.assertEqual(rules.read_bytes(), (ROOT / "product/adp/rules.md").read_bytes())

    def test_symlink_in_owned_path_fails_before_writes(self):
        self.assertEqual(self.run_export("--apply").returncode, 0)
        modified = self.target / ".agents/adp/rules.md"
        modified.write_text("Changed installed pipeline\n")
        outside = Path(self.directory.name) / "outside"
        (outside / "SKILL.md").parent.mkdir()
        (outside / "SKILL.md").write_text("Linked skill\n")
        (self.target / ".agents/skills/adp-linked").symlink_to(outside, target_is_directory=True)
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing symlink in ADP-owned path", result.stderr)
        self.assertEqual(modified.read_text(), "Changed installed pipeline\n")
        self.assertEqual((outside / "SKILL.md").read_text(), "Linked skill\n")

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

    def test_existing_discovery_directory_is_left_for_setup(self):
        discovery = self.target / ".claude/skills"
        (discovery / "custom").mkdir(parents=True)
        (discovery / "custom/SKILL.md").write_text("Custom skill\n")
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skip .claude/skills", result.stdout)
        self.assertFalse(discovery.is_symlink())
        self.assertEqual(sorted(p.name for p in discovery.iterdir()), ["custom"])
        self.assertTrue((self.target / ".agents/skills/adp-setup/SKILL.md").is_file())
        # After setup moves the skills and links discovery, a rerun has nothing to change.
        (self.target / ".agents/skills/custom").mkdir()
        (discovery / "custom/SKILL.md").rename(self.target / ".agents/skills/custom/SKILL.md")
        (discovery / "custom").rmdir()
        discovery.rmdir()
        discovery.symlink_to("../.agents/skills", target_is_directory=True)
        result = self.run_export()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Preview: 0 changes", result.stdout)

    def test_discovery_symlink_elsewhere_is_refused(self):
        (self.target / ".claude").mkdir(parents=True)
        (self.target / ".claude/skills").symlink_to("../elsewhere", target_is_directory=True)
        result = self.run_export("--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("integrate discovery manually", result.stderr)
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
        self.copy_product(checkout)
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

    def test_overlap_and_product_symlinks_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            exporter.installation_plan(ROOT / "nested-project")
        source = Path(self.directory.name) / "source"
        source.mkdir()
        (source / "product").mkdir()
        (source / "product/adp").symlink_to("/", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "unsupported product symlink"):
            exporter.installation_plan(self.target, source)
        (source / "product/adp").unlink()
        (source / "product").rename(source / "real-product")
        (source / "product").symlink_to(source / "real-product", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink directory"):
            exporter.installation_plan(self.target, source)

    def test_export_map_excludes_maintainer_content_and_versions_product_only(self):
        checkout = Path(self.directory.name) / "checkout"
        self.copy_product(checkout)
        files = exporter.product_files(checkout)
        for relative in ("docs/private.md", "plan/unfinished.md", "AGENTS.md", ".agents/memory/private.md", "scripts/private.py", "tests/private.py", "README.md"):
            path = checkout / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Maintainer content must stay here\n")
        self.assertEqual(files, exporter.product_files(checkout))
        self.assertTrue(all(exporter.owned(name) or name in {Path(".agents/memory/MEMORY.md"), exporter.DISCOVERY} for name in files))
        version = Path(".agents/adp/version.json")
        metadata = json.loads(files[version])
        self.assertEqual(metadata["schema"], 2)
        self.assertRegex(metadata["sha256"], r"^[a-f0-9]{64}$")
        policy = checkout / "product/adp/rules.md"
        policy.write_bytes(policy.read_bytes() + b"\nChanged policy\n")
        changed = exporter.product_files(checkout)
        self.assertNotEqual(files[version], changed[version])
        exporter.install(*exporter.installation_plan(self.target, checkout), checkout)
        self.assertEqual((self.target / version).read_bytes(), changed[version])
        self.assertFalse((self.target / "docs").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".agents/adp/private.md").exists())

    def test_failed_update_keeps_previous_fingerprint_until_content_and_cleanup_succeed(self):
        checkout = Path(self.directory.name) / "checkout"
        self.copy_product(checkout)
        exporter.install(*exporter.installation_plan(self.target, checkout), checkout)
        version = self.target / ".agents/adp/version.json"
        previous = version.read_bytes()
        source_skill = checkout / "product/skills/adp-setup/SKILL.md"
        old_skill = source_skill.read_bytes()
        source_skill.write_bytes(old_skill + b"\nNew setup behavior\n")
        stale = self.target / ".agents/adp/retired.md"
        stale.write_text("Obsolete\n")
        installed_skill = self.target / ".agents/skills/adp-setup/SKILL.md"
        original = exporter.os.replace

        def replace(source, destination):
            if destination == installed_skill.resolve():
                raise OSError("skill update failed")
            original(source, destination)

        with mock.patch.object(exporter.os, "replace", side_effect=replace):
            with self.assertRaisesRegex(OSError, "skill update failed"):
                exporter.install(*exporter.installation_plan(self.target, checkout), checkout)
        self.assertEqual(version.read_bytes(), previous)
        self.assertEqual(installed_skill.read_bytes(), old_skill)
        original_unlink = Path.unlink
        def unlink(path, **options):
            if path == stale.resolve():
                raise OSError("cleanup failed")
            return original_unlink(path, **options)
        with mock.patch.object(exporter.Path, "unlink", unlink):
            with self.assertRaisesRegex(OSError, "cleanup failed"):
                exporter.install(*exporter.installation_plan(self.target, checkout), checkout)
        self.assertEqual(version.read_bytes(), previous)
        exporter.install(*exporter.installation_plan(self.target, checkout), checkout)
        self.assertEqual(version.read_bytes(), exporter.product_files(checkout)[Path(".agents/adp/version.json")])
        self.assertFalse(stale.exists())

    def test_mapped_script_parent_symlink_and_invalid_product_content_fail_preflight(self):
        checkout = Path(self.directory.name) / "checkout"
        self.copy_product(checkout)
        scripts = checkout / "product/scripts"
        scripts.rename(checkout / "real-scripts")
        scripts.symlink_to(checkout / "real-scripts", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink directory"):
            exporter.installation_plan(self.target, checkout)
        scripts.unlink()
        (checkout / "real-scripts").rename(scripts)
        invalid = checkout / "product/adp/maintainer.py"
        invalid.write_text("print('not a policy')\n")
        with self.assertRaisesRegex(ValueError, "unsupported policy file"):
            exporter.installation_plan(self.target, checkout)
        self.assertFalse(self.target.exists())

    def test_unreadable_source_directory_and_missing_rules_fail_preflight(self):
        source = Path(self.directory.name) / "source"
        self.copy_product(source)
        original = exporter.os.scandir
        denied = source / "product/adp"

        def scandir(path):
            if Path(path) == denied:
                raise PermissionError(13, "Permission denied", str(denied))
            return original(path)

        with mock.patch.object(exporter.os, "scandir", side_effect=scandir):
            with self.assertRaisesRegex(ValueError, "cannot read product directory"):
                exporter.installation_plan(self.target, source)
        self.assertFalse(self.target.exists())
        (denied / "rules.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing required"):
            exporter.installation_plan(self.target, source)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
