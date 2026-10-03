#!/usr/bin/env python3
"""Execute chapter and worked-example Python fences in isolated namespaces."""

from __future__ import annotations

import os
import re
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FENCE_PATTERN = re.compile(r"```python\s*\n(.*?)```", re.DOTALL)


def executable_markdown_files() -> list[Path]:
    chapters = sorted(ROOT.glob("[0-9][0-9]-*.md"))
    examples = sorted((ROOT / "examples").glob("*.md"))
    return chapters + examples


def main() -> int:
    # Examples may read sibling chapters; callers need not be in the checkout.
    os.chdir(ROOT)
    failures: list[str] = []
    executed = 0

    for path in executable_markdown_files():
        text = path.read_text(encoding="utf-8")
        for block_number, block in enumerate(
            PYTHON_FENCE_PATTERN.findall(text), start=1
        ):
            executed += 1
            label = f"{path.relative_to(ROOT)}:python-block-{block_number}"
            try:
                code = compile(block, label, "exec", dont_inherit=True)
                exec(code, {"__name__": "__documentation_snippet__"})
            except Exception:
                failures.append(f"{label}\n{traceback.format_exc()}")

    print(f"Executed {executed} Python fences.")
    if failures:
        print(f"{len(failures)} Python fence(s) failed:")
        for failure in failures:
            print(failure)
        return 1

    print("All Python fences passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
