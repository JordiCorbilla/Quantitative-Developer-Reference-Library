"""Regression checks for validation behavior that can silently skip errors."""

import tempfile
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_docs


class DocumentationToolsTests(unittest.TestCase):
    def test_anchors_ignore_code_and_preserve_duplicate_suffixes(self):
        text = "# Risk & PnL\n## Risk & PnL\n```python\n# Ghost\n```\n## Café [curve](curve.md)\n"
        self.assertEqual(validate_docs.markdown_heading_anchors(text), {"risk--pnl", "risk--pnl-1", "café-curve"})

    def test_local_fragments_are_checked_and_url_decoded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            target = root / "curve notes.md"
            target.write_text("# Curve\n## Zero Rate\n", encoding="utf-8")
            source.write_text("# Source\n[good](curve%20notes.md#zero-rate)\n[bad](curve%20notes.md#missing)\n", encoding="utf-8")
            with patch.object(validate_docs, "ROOT", root), patch.object(validate_docs, "tracked_markdown_files", return_value=[source]):
                errors = []
                validate_docs.validate_local_links(errors)
            self.assertEqual(len(errors), 1)
            self.assertIn("Missing heading anchor", errors[0])

    def test_math_rendering_rejects_raw_delimiters_and_setext_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "formula.md"
            source.write_text("# Formula\nRaw \\(x\\).\n$$\nx\n=\ny\n$$\n```math\nx\n=\ny\n```\n", encoding="utf-8")
            with patch.object(validate_docs, "ROOT", root), patch.object(validate_docs, "tracked_markdown_files", return_value=[source]):
                errors = []
                validate_docs.validate_math_rendering(errors)
            self.assertEqual(len(errors), 2)
            self.assertIn("GitHub math delimiters", errors[0])
            self.assertIn("heading underline", errors[1])

    def test_git_scan_skips_deleted_paths_during_a_rename(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            renamed = root / "new.md"
            renamed.write_text("# Renamed\n", encoding="utf-8")
            listing = subprocess.CompletedProcess([], 0, b"old.md\0new.md\0")
            with patch.object(validate_docs, "ROOT", root), patch.object(validate_docs.subprocess, "run", return_value=listing):
                self.assertEqual(validate_docs.tracked_markdown_files(), [renamed])

    def test_archive_scan_excludes_environment_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Reference\n", encoding="utf-8")
            (root / ".venv").mkdir()
            (root / ".venv" / "vendor.md").write_text("# Vendor\n", encoding="utf-8")
            with patch.object(validate_docs, "ROOT", root):
                self.assertEqual(validate_docs.tracked_markdown_files(), [root / "README.md"])


if __name__ == "__main__":
    unittest.main()
