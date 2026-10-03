#!/usr/bin/env python3
"""Run the reference release checks from any working directory."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if sys.flags.optimize:
        print("Checks require assertions: unset PYTHONOPTIMIZE and run without -O.")
        return 2
    checks = (
        [sys.executable, "scripts/validate_docs.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
        [sys.executable, "scripts/execute_python_fences.py"],
    )
    for command in checks:
        print(f"Running: {' '.join(command[1:])}", flush=True)
        result = subprocess.run(command, cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        if result.returncode:
            return result.returncode
    print("Reference release checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
