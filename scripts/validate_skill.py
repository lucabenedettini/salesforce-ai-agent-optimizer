#!/usr/bin/env python3
"""Validate the Salesforce Agent Optimizer skill package."""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by environment setup
    raise SystemExit("PyYAML is required. Install with: python -m pip install PyYAML") from exc


SKILL_NAME = "salesforce-agent-optimizer"
MAX_DESCRIPTION_LENGTH = 1024
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".toml"}
REQUIRED_COMPATIBILITY = {
    "agents": {"Codex", "Claude Code", "GitHub Copilot"},
    "platforms": {"Windows", "macOS", "Linux"},
    "prerequisites": {"Python 3.10+", "Git", "Salesforce CLI"},
}
REQUIRED_FILES = [
    "SKILL.md",
    "VERSION",
    "CHANGELOG.md",
    "README.md",
    "README.it.md",
    "README.es.md",
    "README.zh-CN.md",
    "AGENTS.md",
    "agents/openai.yaml",
    ".agents/skills/salesforce-agent-optimizer/SKILL.md",
    ".claude/skills/salesforce-agent-optimizer/SKILL.md",
    ".github/copilot-instructions.md",
    ".github/instructions/salesforce-agent-optimizer.instructions.md",
    ".github/workflows/validate.yml",
]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = read_text(path)
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path} missing opening YAML frontmatter delimiter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError(f"{path} missing closing YAML frontmatter delimiter") from exc
    raw = "\n".join(lines[1:end])
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter must be a YAML mapping")
    body = "\n".join(lines[end + 1 :])
    return data, body


def validate_frontmatter(root: Path, errors: list[str]) -> None:
    version = read_text(root / "VERSION").strip()
    try:
        data, _ = parse_frontmatter(root / "SKILL.md")
    except ValueError as exc:
        fail(errors, str(exc))
        return

    if data.get("name") != SKILL_NAME:
        fail(errors, "SKILL.md name must be salesforce-agent-optimizer")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", str(data.get("name", ""))):
        fail(errors, "SKILL.md name must be lowercase letters, digits, and hyphens only")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        fail(errors, "SKILL.md description must be a non-empty string")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        fail(errors, f"SKILL.md description exceeds {MAX_DESCRIPTION_LENGTH} characters")
    if data.get("license") != "MIT":
        fail(errors, "SKILL.md license must be MIT")
    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict) or str(metadata.get("version")) != version:
        fail(errors, "SKILL.md metadata.version must match VERSION")
    compatibility = data.get("compatibility", {})
    if not isinstance(compatibility, dict):
        fail(errors, "SKILL.md compatibility must be a mapping")
        return
    for key, required_values in REQUIRED_COMPATIBILITY.items():
        values = compatibility.get(key, [])
        if not isinstance(values, list):
            fail(errors, f"SKILL.md compatibility.{key} must be a list")
            continue
        missing = required_values - {str(item) for item in values}
        if missing:
            fail(errors, f"SKILL.md compatibility.{key} missing: {', '.join(sorted(missing))}")


def validate_yaml_files(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or path.suffix.lower() not in {".yaml", ".yml"}:
            continue
        try:
            yaml.safe_load(read_text(path))
        except Exception as exc:  # noqa: BLE001 - validation should report parser detail
            fail(errors, f"Invalid YAML {path.relative_to(root)}: {exc}")
    try:
        openai = yaml.safe_load(read_text(root / "agents" / "openai.yaml"))
    except Exception as exc:  # noqa: BLE001
        fail(errors, f"Invalid agents/openai.yaml: {exc}")
        return
    if not isinstance(openai, dict) or "interface" not in openai:
        fail(errors, "agents/openai.yaml must contain an interface mapping")
    if len(read_text(root / "agents" / "openai.yaml").splitlines()) < 3:
        fail(errors, "agents/openai.yaml must be multi-line YAML")


def validate_python(root: Path, errors: list[str]) -> None:
    for path in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(errors, f"Python compile failed for {path.relative_to(root)}: {exc.msg}")


def validate_required_files(root: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (root / relative).exists():
            fail(errors, f"Missing required file: {relative}")


def validate_text_shape(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            data = path.read_bytes()
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(errors, f"File is not UTF-8: {path.relative_to(root)}: {exc}")
            continue
        if data and not data.endswith(b"\n"):
            fail(errors, f"Missing final newline: {path.relative_to(root)}")
        if len(text) > 300 and len(text.splitlines()) <= 1:
            fail(errors, f"File appears collapsed into one line: {path.relative_to(root)}")
        if "\\n" in text and len(text.splitlines()) <= 2 and len(text) > 300:
            fail(errors, f"File may contain escaped newlines instead of real newlines: {path.relative_to(root)}")


def validate_json(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.json")):
        if ".git" in path.parts:
            continue
        try:
            json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            fail(errors, f"Invalid JSON {path.relative_to(root)}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Salesforce Agent Optimizer skill compatibility.")
    parser.add_argument("root", nargs="?", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    validate_required_files(root, errors)
    validate_frontmatter(root, errors)
    validate_yaml_files(root, errors)
    validate_json(root, errors)
    validate_python(root, errors)
    validate_text_shape(root, errors)

    result = {"ok": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print("Skill validation passed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
