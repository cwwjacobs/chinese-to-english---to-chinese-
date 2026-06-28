#!/usr/bin/env python3
"""test_bundle.py — Unit tests for the CLI Translation Overlay bundle."""
import re
import unittest
import py_compile
from pathlib import Path

ROOT = Path(__file__).parent.parent


class TestBundle(unittest.TestCase):
    def test_files_exist(self):
        for f in [
            "translator.py",
            "overlay.py",
            "replay.py",
            "SKILL.md",
            "README.md",
            "Makefile",
            "requirements.txt",
            "U-KSL.md",
        ]:
            self.assertTrue((ROOT / f).exists(), f"Missing: {f}")

    def test_scripts_compile(self):
        for s in [
            "translator.py",
            "overlay.py",
            "replay.py",
            "scripts/export_training_trace.py",
            "scripts/build_final_receipt.py",
            "scripts/validate_package.py",
        ]:
            try:
                py_compile.compile(str(ROOT / s), doraise=True)
            except py_compile.PyCompileError as e:
                self.fail(f"{s}: {e}")

    def test_storefront(self):
        for f in ["short-description.txt", "long-description.md", "faq.md"]:
            self.assertTrue((ROOT / "storefront" / f).exists(), f"Missing storefront: {f}")

    def test_skillmd_frontmatter(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"), "Missing YAML frontmatter")
        self.assertIn("Operating Boundary", content)
        self.assertIn("never do", content.lower(), "Missing 'Never Do' section")
        self.assertIn("Claim Boundary", content)
        self.assertIn("/tmp/op_trans_fifo", content)

    def test_makefile_targets(self):
        mk = (ROOT / "Makefile").read_text(encoding="utf-8")
        for t in [
            "clean",
            "validate",
            "test",
            "package",
            "receipt",
            "prepare-fifos",
            "run-deepseek",
            "smoke",
        ]:
            self.assertIn(t, mk, f"Makefile missing target: {t}")

    def test_release_version_alignment(self):
        mk = (ROOT / "Makefile").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        mk_version = re.search(r"PACKAGE_VERSION \?= v?([^\s]+)", mk)
        skill_version = re.search(r"^version:\s*([^\s]+)", skill, re.MULTILINE)
        self.assertIsNotNone(mk_version, "Makefile version not found")
        self.assertIsNotNone(skill_version, "SKILL.md version not found")
        self.assertEqual(mk_version.group(1), skill_version.group(1))

    def test_readme_documents_fifo_bridge(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("/tmp/trans_fifo", readme)
        self.assertIn("/tmp/op_trans_fifo", readme)
        self.assertIn("make run-deepseek", readme)


if __name__ == "__main__":
    unittest.main()
