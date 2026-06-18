from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SECTIONS = [
    "## What This Domain Covers",
    "## Product Taxonomy and Market Structure",
    "## Quoting and Market Conventions",
    "## Core Pricing Framework",
    "## Key Risk Measures and Sensitivities",
    "## Required Data, Curves, Surfaces, and Calibration Objects",
    "## Numerical and Implementation Approaches",
    "## Production Pitfalls and Sanity Checks",
    "## Illustrative Code",
    "## References and Further Reading",
]


def tracked_markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and ".codex-remote-attachments" not in path.parts
    )


def validate_local_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    image_pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for path in tracked_markdown_files():
        text = path.read_text(encoding="utf-8")
        for pattern, kind in ((link_pattern, "link"), (image_pattern, "image")):
            for match in pattern.finditer(text):
                target = match.group(1).split("#", 1)[0]
                if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                target_path = (path.parent / target).resolve()
                if not target_path.exists():
                    errors.append(f"Missing {kind}: {path.relative_to(ROOT)} -> {target}")


def validate_svgs(errors: list[str]) -> None:
    for path in sorted((ROOT / "assets").glob("*.svg")):
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG XML: {path.relative_to(ROOT)}: {exc}")


def validate_chapter_sections(errors: list[str]) -> None:
    for path in sorted(ROOT.glob("[0-9][0-9]-*.md")):
        if path.name == "00-overview.md":
            continue
        text = path.read_text(encoding="utf-8")
        missing = [section for section in EXPECTED_SECTIONS if section not in text]
        if missing:
            errors.append(f"{path.name} missing sections: {', '.join(missing)}")


def validate_duplicate_h1(errors: list[str]) -> None:
    for path in tracked_markdown_files():
        h1_count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("# "))
        if h1_count != 1:
            errors.append(f"{path.relative_to(ROOT)} has {h1_count} H1 headings")


def main() -> int:
    errors: list[str] = []
    validate_local_links(errors)
    validate_svgs(errors)
    validate_chapter_sections(errors)
    validate_duplicate_h1(errors)

    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
