#!/usr/bin/env python3
"""Record compact Salesforce project history entries in the Knowledge folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


KNOWLEDGE_DIR = ".salesforce-agent-knowledge"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned[:80] or "event"


def event_id(action: str, timestamp: str, requirements: str, metadata: list[str]) -> str:
    raw = "|".join([action, timestamp, requirements, *metadata])
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:12]


def rel_link(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def ensure_history(knowledge_dir: Path) -> Path:
    history_path = knowledge_dir / "history" / "project-history.md"
    history_path.parent.mkdir(parents=True, exist_ok=True)
    if not history_path.exists():
        history_path.write_text(
            "# Project History\n\n"
            "Compact deployment, push, and change history for AI-agent planning.\n\n"
            "| Timestamp | Action | Requirement | Modified Metadata | Event | Result |\n"
            "|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    return history_path


def ensure_markdown_index(knowledge_dir: Path, event_file: Path) -> None:
    index_path = knowledge_dir / "markdown-index.md"
    rel = event_file.relative_to(knowledge_dir).as_posix()
    line = f"| [{rel}]({rel}) | History Event |\n"
    if not index_path.exists():
        index_path.write_text(
            "# Knowledge Markdown Index\n\n"
            "| File | Description |\n"
            "|---|---|\n"
            "| [history/project-history.md](history/project-history.md) | Project History |\n"
            + line,
            encoding="utf-8",
        )
        return
    text = index_path.read_text(encoding="utf-8", errors="replace")
    if rel not in text:
        with index_path.open("a", encoding="utf-8") as handle:
            handle.write(line)


def metadata_lines(metadata: list[str]) -> list[str]:
    return [f"- `{item}`" for item in metadata] if metadata else ["- `unspecified`"]


def append_event(args: argparse.Namespace) -> Path:
    root = Path(args.project_root).resolve()
    knowledge_dir = Path(args.knowledge_dir)
    if not knowledge_dir.is_absolute():
        knowledge_dir = root / knowledge_dir
    history_path = ensure_history(knowledge_dir)
    timestamp = args.timestamp or now_iso()
    metadata = args.metadata or []
    event_name = f"{timestamp}-{args.action}-{event_id(args.action, timestamp, args.requirements, metadata)}"
    event_file = knowledge_dir / "history" / "events" / f"{slug(event_name)}.md"
    event_file.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "timestamp": timestamp,
        "action": args.action,
        "requirements": args.requirements,
        "modified_metadata": metadata,
        "target_org": args.target_org,
        "remote": args.remote,
        "branch": args.branch,
        "commit": args.commit,
        "summary": args.summary,
        "result": args.result,
        "command": args.command,
    }
    event_file.write_text(
        "\n".join(
            [
                f"# History Event: {args.action}",
                "",
                "## Requirement",
                "",
                args.requirements,
                "",
                "## Modified Metadata",
                "",
                *metadata_lines(metadata),
                "",
                "## Context",
                "",
                f"- Timestamp: `{timestamp}`",
                f"- Target org: `{args.target_org or 'n/a'}`",
                f"- Remote: `{args.remote or 'n/a'}`",
                f"- Branch: `{args.branch or 'n/a'}`",
                f"- Commit: `{args.commit or 'n/a'}`",
                f"- Summary: {args.summary or 'n/a'}",
                f"- Result: {args.result or 'n/a'}",
                f"- Command: `{args.command or 'n/a'}`",
                "",
                "## Links",
                "",
                f"- [Project history]({rel_link(event_file, history_path)})",
                f"- [Knowledge index]({rel_link(event_file, knowledge_dir / 'index.md')})",
                f"- [Markdown index]({rel_link(event_file, knowledge_dir / 'markdown-index.md')})",
                "",
                "## Machine Record",
                "",
                "```json",
                json.dumps(payload, indent=2, sort_keys=True),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )

    requirement_short = args.requirements.replace("\n", " ")[:120]
    metadata_short = ", ".join(metadata[:12]) if metadata else "unspecified"
    if len(metadata) > 12:
        metadata_short += f", +{len(metadata) - 12} more"
    event_rel = event_file.relative_to(knowledge_dir).as_posix()
    row = f"| {timestamp} | `{args.action}` | {requirement_short} | `{metadata_short}` | [{event_rel}]({event_rel}) | {args.result or args.summary or 'recorded'} |\n"
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(row)
    ensure_markdown_index(knowledge_dir, event_file)
    return event_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append compact entries to Salesforce Agent Knowledge history.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--knowledge-dir", default=KNOWLEDGE_DIR)
    parser.add_argument("--action", required=True, choices=["change", "deploy", "git-push", "validation", "note"])
    parser.add_argument("--requirements", required=True, help="Requirement or user request that caused the change.")
    parser.add_argument("--metadata", action="append", required=True, help="Modified metadata, for example ApexClass:AccountService.")
    parser.add_argument("--target-org")
    parser.add_argument("--remote")
    parser.add_argument("--branch")
    parser.add_argument("--commit")
    parser.add_argument("--summary")
    parser.add_argument("--result")
    parser.add_argument("--command")
    parser.add_argument("--timestamp")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    event_file = append_event(args)
    print(f"History recorded: {event_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
