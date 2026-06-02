#!/usr/bin/env python3
"""Generate compact docs for installed Salesforce CLI commands."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sf_agent_cli import classify_official_safety, sf_binary


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_commands() -> list[dict[str, Any]]:
    completed = subprocess.run(
        [sf_binary(), "commands", "--json"],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr or completed.stdout or "Failed to run sf commands --json")
    text = completed.stdout.strip()
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise SystemExit("Could not find a JSON array in sf commands output.")
    return json.loads(text[start : end + 1])


def command_record(command: dict[str, Any]) -> dict[str, Any]:
    command_id = command.get("id", "")
    flags = command.get("flags", {})
    return {
        "id": command_id,
        "summary": command.get("summary") or "",
        "safety": classify_official_safety(command_id, connects_to_org="target-org" in flags or "target-dev-hub" in flags),
        "requires_project": bool(command.get("requiresProject")),
        "enable_json": bool(command.get("enableJsonFlag")),
        "has_target_org": "target-org" in flags,
        "has_target_dev_hub": "target-dev-hub" in flags,
        "plugin": command.get("pluginName") or command.get("pluginAlias") or "",
        "aliases": command.get("aliases") or [],
    }


def to_markdown(records: list[dict[str, Any]], generated_at: str) -> str:
    lines = [
        "# Official Salesforce CLI Command Catalog",
        "",
        f"Generated: `{generated_at}`",
        "",
        "This catalog is generated from the installed `sf commands --json` output. Use `scripts/sf_agent_cli.py safe-run` for commands not exposed as first-class facade commands.",
        "",
        "Safety values are heuristic and intentionally conservative. `write` and `execute` commands are blocked on production by the agent facade.",
        "",
        "| Command | Safety | Target Org | JSON | Project | Summary |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for record in records:
        summary = str(record["summary"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{record['id']}` | `{record['safety']}` | {yes(record['has_target_org'])} | {yes(record['enable_json'])} | {yes(record['requires_project'])} | {summary} |"
        )
    lines.extend(
        [
            "",
            "## Usage",
            "",
            "```bash",
            "python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- data query --query \"SELECT Id, Name FROM Account LIMIT 20\" --select result.records",
            "```",
            "",
            "Refresh this catalog after upgrading Salesforce CLI:",
            "",
            "```bash",
            "python scripts/sf_agent_cli.py catalog-refresh",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def yes(value: bool) -> str:
    return "yes" if value else "no"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a compact Salesforce CLI command catalog.")
    parser.add_argument("--output-dir", default=str(Path(__file__).resolve().parent.parent / "references"))
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = now_iso()
    records = sorted((command_record(command) for command in load_commands()), key=lambda item: item["id"])

    payload = {
        "generated_at": generated_at,
        "sf_binary": sf_binary(),
        "count": len(records),
        "commands": records,
    }
    (output_dir / "sf-official-command-catalog.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "sf-official-command-catalog.md").write_text(to_markdown(records, generated_at), encoding="utf-8")
    print(f"Generated {len(records)} Salesforce CLI command records in {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
