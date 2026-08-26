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
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|LOREM IPSUM|CITATION NEEDED)\b", re.IGNORECASE)
NUMERIC_CURRENCY_PATTERN = re.compile(r"(?<!\\)\$(?=[+-]?\d)")
INLINE_MATH_PATTERN = re.compile(r"(?<!\\)\$(?!\$).*?(?<!\\)\$(?!\$)")
PYTHON_FENCE_PATTERN = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)


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
    svg_paths = [
        path
        for directory in (ROOT / "assets", ROOT / "blog-assets")
        for path in directory.glob("*.svg")
    ]
    for path in sorted(svg_paths):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"Invalid SVG XML: {path.relative_to(ROOT)}: {exc}")
            continue

        required_attributes = ("width", "height", "viewBox", "role", "aria-labelledby")
        missing = [attribute for attribute in required_attributes if not root.get(attribute)]
        namespace = {"svg": "http://www.w3.org/2000/svg"}
        if root.find("svg:title", namespace) is None:
            missing.append("title")
        if root.find("svg:desc", namespace) is None:
            missing.append("desc")
        if missing:
            errors.append(
                f"Incomplete SVG metadata: {path.relative_to(ROOT)}: {', '.join(missing)}"
            )
            continue

        ids = [element.get("id") for element in root.iter() if element.get("id")]
        duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
        if duplicate_ids:
            errors.append(
                f"Duplicate SVG IDs: {path.relative_to(ROOT)}: {', '.join(duplicate_ids)}"
            )

        labelled_ids = root.get("aria-labelledby", "").split()
        missing_label_ids = [item for item in labelled_ids if item not in ids]
        if missing_label_ids:
            errors.append(
                f"Unresolved SVG aria-labelledby IDs: {path.relative_to(ROOT)}: "
                f"{', '.join(missing_label_ids)}"
            )


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


def validate_markdown_integrity(errors: list[str]) -> None:
    for path in tracked_markdown_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        if text.count("```") % 2:
            errors.append(f"Unbalanced code fences: {relative}")
        if text.count("$$") % 2:
            errors.append(f"Unbalanced display-math fences: {relative}")
        if "\ufffd" in text:
            errors.append(f"Unicode replacement character found: {relative}")
        for match in PLACEHOLDER_PATTERN.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"Placeholder text in {relative}:{line}: {match.group(0)}")


def validate_python_fences(errors: list[str]) -> None:
    for path in tracked_markdown_files():
        text = path.read_text(encoding="utf-8")
        for index, block in enumerate(PYTHON_FENCE_PATTERN.findall(text), start=1):
            try:
                compile(block, f"{path.relative_to(ROOT)}:python-block-{index}", "exec")
            except SyntaxError as exc:
                errors.append(
                    f"Invalid Python fence: {path.relative_to(ROOT)} block {index}: {exc.msg}"
                )


def validate_worked_example_checks(errors: list[str]) -> None:
    """Require each standalone worked example to contain executable checks."""
    for path in sorted((ROOT / "examples").glob("*.md")):
        if path.name == "README.md":
            continue
        blocks = PYTHON_FENCE_PATTERN.findall(path.read_text(encoding="utf-8"))
        if not blocks:
            errors.append(f"Worked example has no Python fence: {path.relative_to(ROOT)}")
        elif not any(re.search(r"\bassert\b", block) for block in blocks):
            errors.append(f"Worked example has no assertion: {path.relative_to(ROOT)}")


def validate_currency_style(errors: list[str]) -> None:
    """Keep dollar signs from being mistaken for inline-math delimiters."""
    for path in tracked_markdown_files():
        in_code = False
        in_display_math = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if stripped == "$$":
                in_display_math = not in_display_math
                continue
            if in_display_math:
                continue
            prose = INLINE_MATH_PATTERN.sub("", line)
            if NUMERIC_CURRENCY_PATTERN.search(prose):
                errors.append(
                    f"Use an explicit currency code instead of '$' in "
                    f"{path.relative_to(ROOT)}:{line_number}"
                )


def validate_story_openings(errors: list[str]) -> None:
    """Require each chapter to begin its scope with a reader-oriented narrative."""
    marker = "## What This Domain Covers"
    for path in sorted(ROOT.glob("[0-9][0-9]-*.md")):
        if path.name == "00-overview.md":
            continue
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            continue  # validate_chapter_sections reports the missing section.
        section = text.split(marker, 1)[1].split("\n## ", 1)[0]
        content = [line.strip() for line in section.splitlines() if line.strip()]
        if not content or content[0].startswith(("-", "*", "|", "#")):
            errors.append(
                f"{path.name} must open 'What This Domain Covers' with explanatory prose"
            )


def validate_navigation_completeness(errors: list[str]) -> None:
    chapters = [path.name for path in sorted(ROOT.glob("[0-9][0-9]-*.md"))]
    for navigation_file in ("README.md", "00-overview.md", "INDEX.md"):
        text = (ROOT / navigation_file).read_text(encoding="utf-8")
        for chapter in chapters:
            if chapter != "00-overview.md" and chapter not in text:
                errors.append(f"{navigation_file} does not reference {chapter}")

    examples_index = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    for example in sorted((ROOT / "examples").glob("*.md")):
        if example.name != "README.md" and example.name not in examples_index:
            errors.append(f"examples/README.md does not reference {example.name}")


def main() -> int:
    errors: list[str] = []
    validate_local_links(errors)
    validate_svgs(errors)
    validate_chapter_sections(errors)
    validate_duplicate_h1(errors)
    validate_markdown_integrity(errors)
    validate_python_fences(errors)
    validate_worked_example_checks(errors)
    validate_currency_style(errors)
    validate_story_openings(errors)
    validate_navigation_completeness(errors)

    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
