#!/usr/bin/env python3
"""test_bundle.py — Unit tests for the CLI Translation Overlay bundle."""
import json, sys, unittest, py_compile
from pathlib import Path

ROOT = Path(__file__).parent.parent

class TestBundle(unittest.TestCase):
    def test_files_exist(self):
        for f in ["translator.py","overlay.py","replay.py","SKILL.md","Makefile","U-KSL.md"]:
            self.assertTrue((ROOT/f).exists(), f"Missing: {f}")
    def test_scripts_compile(self):
        for s in ["translator.py","overlay.py","replay.py","scripts/export_training_trace.py"]:
            try: py_compile.compile(str(ROOT/s), doraise=True)
            except py_compile.PyCompileError as e: self.fail(f"{s}: {e}")
    def test_storefront(self):
        for f in ["short-description.txt","long-description.md","faq.md"]:
            self.assertTrue((ROOT/"storefront"/f).exists(), f"Missing storefront: {f}")
    def test_skilmd_frontmatter(self):
        content = (ROOT/"SKILL.md").read_text()
        self.assertTrue(content.startswith("---"), "Missing YAML frontmatter")
        self.assertIn("Operating Boundary", content)
        self.assertIn("never do", content.lower(), "Missing 'Never Do' section")
        self.assertIn("Claim Boundary", content)
    def test_makefile_targets(self):
        mk = (ROOT/"Makefile").read_text()
        for t in ["clean","validate","test","package","receipt"]:
            self.assertIn(t, mk, f"Makefile missing target: {t}")

if __name__ == "__main__":
    unittest.main()
