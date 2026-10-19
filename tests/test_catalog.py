import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/build_catalog.py"
spec = importlib.util.spec_from_file_location("catalog", SCRIPT)
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def test_catalog_comes_from_metadata_and_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("adp-zebra", "adp-alpha"):
                path = root / name / "SKILL.md"
                path.parent.mkdir()
                path.write_text(f"---\nname: {name}\ndescription: Original purpose\n---\n# Skill\n")
            first = catalog.render(root)
            self.assertEqual(first, catalog.render(root))
            self.assertLess(first.index("adp-alpha"), first.index("adp-zebra"))
            path.write_text("---\nname: adp-alpha\ndescription: Changed purpose\n---\n# Skill\n")
            self.assertIn("Changed purpose", catalog.render(root))
            path.write_text("---\nname: another-name\ndescription: Wrong folder\n---\n# Skill\n")
            with self.assertRaisesRegex(ValueError, "name must match"):
                catalog.render(root)

    def test_missing_metadata_and_empty_catalog_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "no shipped skills"):
                catalog.render(root)
            path = root / "adp-example" / "SKILL.md"
            path.parent.mkdir()
            path.write_text("# Missing metadata\n")
            with self.assertRaisesRegex(ValueError, "missing frontmatter"):
                catalog.render(root)

    def test_incomplete_skill_folder_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            good = root / "adp-good" / "SKILL.md"
            good.parent.mkdir()
            good.write_text("---\nname: adp-good\ndescription: Good skill\n---\n# Skill\n")
            (root / "adp-missing").mkdir()
            with self.assertRaisesRegex(ValueError, "regular SKILL.md"):
                catalog.render(root)

    def test_plain_metadata_cannot_hide_invalid_yaml_or_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "adp-example" / "SKILL.md"
            path.parent.mkdir()
            for description in ['purpose: invalid YAML', 'A description # hidden comment', 'true']:
                with self.subTest(description=description):
                    path.write_text(f'---\nname: adp-example\ndescription: {description}\n---\n# Skill\n')
                    with self.assertRaisesRegex(ValueError, "plain YAML string"):
                        catalog.render(root)


if __name__ == "__main__":
    unittest.main()
