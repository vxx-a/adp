import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "template/.agents/adp/scripts/check_docs.py"
spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def check(self, text, paths=None):
        self.write("README.md", text)
        return checker.check(self.root, paths)

    def test_valid_links_references_anchors_and_code_headings(self):
        self.write("docs/My File.md", '# `API` behavior\n\n# Repeat\n# Repeat\n<a id="explicit"></a>\n')
        self.write("docs/a(b).md", "# Nested\n")
        self.write("image.png", "binary placeholder")
        errors, files, count = self.check(
            '[API](<docs/My File.md#api-behavior>)\n'
            '[repeat][ref]\n[ref]: <docs/My File.md#repeat-1> "Title"\n'
            '[explicit](docs/My%20File.md#explicit)\n'
            '[nested](docs/a(b).md#nested)\n'
            '![image](image.png)\n[external](https://example.invalid/x)\n[call](tel:123)\n[port](https://example.invalid:443)\n'
            '[root](/docs/a(b).md)\n'
        )
        self.assertEqual(errors, [])
        self.assertEqual(files, 3)
        self.assertEqual(count, 6)

    def test_missing_targets_fragments_and_reference_definitions_fail(self):
        self.write("docs/design.md", "# Existing\n")
        errors, _, _ = self.check('[bad](missing.md)\n[bad](docs/design.md#absent)\n[x][undefined]\n')
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("README.md:1:" in e and "missing target" in e for e in errors))
        self.assertTrue(any("missing fragment" in e for e in errors))
        self.assertTrue(any("undefined reference" in e for e in errors))

    def test_code_examples_and_comments_are_not_links(self):
        errors, _, count = self.check(
            '# Example\n```markdown\n[bad](missing.md)\n```\n'
            '~~~\n[bad](missing.md)\n~~~\n'
            '`[bad](missing.md)`\n<!-- [bad](missing.md) -->\n'
            '    ```markdown\n    [bad](missing.md)\n    ```\n[real](#example)\n'
        )
        self.assertEqual(errors, [])
        self.assertEqual(count, 1)

    def test_nested_escaped_and_image_labels_check_every_destination(self):
        errors, _, count = self.check('[see [details]](missing.md)\n[see \\] details](missing.md)\n[![icon](image.png)](missing.md)\n')
        self.assertEqual(count, 4)
        self.assertEqual(len(errors), 4)
        self.assertTrue(all("missing target" in error for error in errors))

    def test_nested_lists_are_checked_and_first_reference_definition_wins(self):
        errors, _, count = self.check('- Parent\n    - [bad](missing.md)\n[x][ref]\n[ref]: missing.md\n[ref]: README.md\n')
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 2)
        errors, _, _ = self.check('[x][ref]\n[ref]: README.md\n[ref]: missing.md\n')
        self.assertEqual(errors, [])

    def test_multiline_labels_cannot_hide_missing_targets(self):
        errors, _, count = self.check('[target\nname](missing.md)\n')
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("README.md:1: missing target", errors[0])

    def test_unreadable_directory_cannot_pass(self):
        self.write("README.md", "# Root\n")
        denied = self.root.resolve() / "docs"
        denied.mkdir()
        original = checker.os.scandir

        def scandir(path):
            if Path(path) == denied:
                raise PermissionError(13, "Permission denied", str(denied))
            return original(path)

        with mock.patch.object(checker.os, "scandir", side_effect=scandir):
            errors, _, _ = checker.check(self.root)
        self.assertTrue(any("cannot traverse" in error for error in errors))

    def test_source_line_bounds(self):
        self.write("module.py", "a = 1\nb = 2\n")
        errors, _, count = self.check('[one](module.py#L1-L2)\n[two](module.py:2)\n[bad](module.py#L3)\n[zero](module.py:0)\n')
        self.assertEqual(count, 4)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("source line outside target" in error for error in errors))

    def test_extensionless_local_source_lines_are_not_treated_as_uri_schemes(self):
        self.write("Dockerfile", "FROM scratch\n")
        errors, _, count = self.check('[bad](Dockerfile:999)\n[good](Dockerfile:1)\n[call](tel:123)\n')
        self.assertEqual(count, 2)
        self.assertEqual(len(errors), 1)
        self.assertIn("source line outside target", errors[0])

    def test_path_escape_and_symlink_escape_fail(self):
        with tempfile.TemporaryDirectory() as outside:
            secret = Path(outside) / "private.md"
            secret.write_text("# Private\n")
            (self.root / "escaped.md").symlink_to(secret)
            errors, _, _ = self.check('[escape](escaped.md)\n[parent](../private.md)\n', ["README.md"])
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("escapes project root" in e for e in errors))
            errors, _, _ = checker.check(self.root, ["escaped.md"])
            self.assertTrue(any("escapes project root" in e for e in errors))

    def test_duplicate_heading_collision_and_setext(self):
        errors, _, _ = self.check('# Repeat\n# Repeat\n# Repeat-1\nSetext\n======\n[x](#repeat-1-1)\n[y](#setext)\n')
        self.assertEqual(errors, [])

    def test_discovery_skips_symlink_directories_and_dependencies(self):
        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "README.md").write_text('[bad](missing.md)\n')
            (self.root / "docs").symlink_to(outside, target_is_directory=True)
            self.write("node_modules/bad.md", '[bad](missing.md)\n')
            self.write("README.md", "# Root\n")
            errors, files, _ = checker.check(self.root, ["."])
            self.assertEqual(errors, [])
            self.assertEqual(files, 1)

    def test_explicit_missing_paths_and_empty_selection_fail(self):
        errors, _, _ = checker.check(self.root, ["absent.md"])
        self.assertTrue(any("does not exist" in error for error in errors))
        errors, _, _ = checker.check(self.root)
        self.assertIn("no Markdown files selected", errors)

    def test_cli_returns_nonzero_and_never_modifies_input(self):
        path = self.write("README.md", '[bad](missing.md)\n')
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md:1:", result.stderr)
        self.assertEqual(path.read_bytes(), before)
        path.write_text("# Valid\n")
        result = subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
