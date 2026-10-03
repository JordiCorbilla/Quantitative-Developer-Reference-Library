"""Regression checks for validation behavior that can silently skip errors."""

import tempfile
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
