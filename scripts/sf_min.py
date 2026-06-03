#!/usr/bin/env python3
"""Run Salesforce CLI with compact, redacted output for AI agents."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SECRET_KEYS = re.compile(
    r"(access.?token|session.?id|auth.?url|refresh.?token|client.?secret|password|cookie|sid)",
    re.IGNORECASE,
)
DESTRUCTIVE_TERMS = {"delete", "uninstall", "purge", "truncate", "hard-delete", "harddelete"}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if SECRET_KEYS.search(str(key)) else redact(inner)
            for key, inner in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return re.sub(r"00D[A-Za-z0-9]{12,}", "[REDACTED_ORG_ID]", value)
    return value


def get_path(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if part == "":
            continue
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def select_paths(payload: Any, selector: str | None) -> Any:
    if not selector:
        return payload
    selected: dict[str, Any] = {}
    for path in [item.strip() for item in selector.split(",") if item.strip()]:
        selected[path] = get_path(payload, path)
    return selected


def compact(value: Any, max_list: int) -> Any:
    if isinstance(value, list):
        items = [compact(item, max_list) for item in value[:max_list]]
        if len(value) > max_list:
            items.append({"_truncated": len(value) - max_list})
        return items
    if isinstance(value, dict):
        return {key: compact(inner, max_list) for key, inner in value.items()}
    return value


def sf_binary() -> str:
    override = os.environ.get("SF_AGENT_SF_BIN")
    if override:
        return override
    if os.name == "nt":
        for name in ("sf.cmd", "sf.exe", "sf"):
            candidate = shutil.which(name)
            if candidate:
                return candidate
        appdata = os.environ.get("APPDATA")
        if appdata:
            npm_cmd = Path(appdata) / "npm" / "sf.cmd"
            try:
                exists = npm_cmd.exists()
            except OSError:
                exists = False
            if exists:
                return str(npm_cmd)
        return "sf.cmd"
    return shutil.which("sf") or "sf"


def is_destructive(sf_args: list[str]) -> bool:
    parts: list[str] = []
    for token in sf_args:
        if token.startswith("-"):
            break
        parts.extend(part for part in token.replace(":", " ").replace("-", " ").split() if part)
    if set(parts) & DESTRUCTIVE_TERMS:
        return True
    lowered = " ".join(sf_args).lower()
    return any(term in lowered for term in ("destructivechanges", "destructive changes", "purge-on-delete", "hard-delete"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run sf with compact redacted output.")
    parser.add_argument("--select", help="Comma-separated JSON paths to keep.")
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--max-list", type=int, default=20)
    parser.add_argument("--raw", action="store_true", help="Do not append --json or parse JSON.")
    parser.add_argument("sf_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    sf_args = args.sf_args
    if sf_args and sf_args[0] == "--":
        sf_args = sf_args[1:]
    if not sf_args:
        parser.error("Provide an sf command, for example: org display --target-org dev")
    if is_destructive(sf_args):
        raise SystemExit("Blocked destructive command. Use scripts/sf_agent_cli.py with explicit deletion approval.")

    command = [sf_binary(), *sf_args]
    if not args.raw and "--json" not in command:
        command.append("--json")

    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    output = completed.stdout if completed.stdout.strip() else completed.stderr

    if args.raw:
        text = output
    else:
        try:
            payload = json.loads(output)
            payload = compact(redact(select_paths(payload, args.select)), args.max_list)
            text = json.dumps(payload, indent=2, sort_keys=True)
        except json.JSONDecodeError:
            text = output

    if len(text) > args.max_chars:
        text = text[: args.max_chars] + f"\n... [truncated to {args.max_chars} chars]"

    print(text)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
