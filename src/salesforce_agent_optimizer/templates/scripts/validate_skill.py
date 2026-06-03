#!/usr/bin/env python3
"""Validate the Salesforce Agent Optimizer skill package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if (ROOT / "src").exists():
    sys.path.insert(0, str(ROOT / "src"))

from salesforce_agent_optimizer.validation import validate_source_tree  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Salesforce Agent Optimizer skill compatibility.")
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate_source_tree(Path(args.root).resolve())
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    elif result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in result.warnings:
            print(f"WARN: {warning}", file=sys.stderr)
    else:
        print("Skill validation passed.")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
