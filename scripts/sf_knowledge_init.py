#!/usr/bin/env python3
"""Build a compact indexed Salesforce metadata Knowledge folder."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


KNOWLEDGE_DIR = ".salesforce-agent-knowledge"
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".sf",
    ".sfdx",
    ".salesforce-agent-knowledge",
    "node_modules",
    "__pycache__",
}

DEFAULT_CONFIG: dict[str, Any] = {
    "metadata_types": {
        "CustomObject": ["**/objects/*/*.object-meta.xml"],
        "CustomField": ["**/objects/*/fields/*.field-meta.xml"],
        "RecordType": ["**/objects/*/recordTypes/*.recordType-meta.xml"],
        "ValidationRule": ["**/objects/*/validationRules/*.validationRule-meta.xml"],
        "BusinessProcess": ["**/objects/*/businessProcesses/*.businessProcess-meta.xml"],
        "WebLink": ["**/objects/*/webLinks/*.webLink-meta.xml"],
        "ListView": ["**/objects/*/listViews/*.listView-meta.xml"],
        "CompactLayout": ["**/objects/*/compactLayouts/*.compactLayout-meta.xml"],
        "GlobalValueSet": ["**/globalValueSets/*.globalValueSet-meta.xml"],
        "Flow": ["**/flows/*.flow-meta.xml"],
        "Workflow": ["**/workflows/*.workflow-meta.xml"],
        "ApprovalProcess": ["**/approvalProcesses/*.approvalProcess-meta.xml"],
        "AssignmentRules": ["**/assignmentRules/*.assignmentRules-meta.xml"],
        "AutoResponseRules": ["**/autoResponseRules/*.autoResponseRules-meta.xml"],
        "EscalationRules": ["**/escalationRules/*.escalationRules-meta.xml"],
        "DuplicateRule": ["**/duplicateRules/*.duplicateRule-meta.xml"],
        "MatchingRule": ["**/matchingRules/*.matchingRule-meta.xml"],
        "ApexClass": ["**/classes/*.cls"],
        "ApexTrigger": ["**/triggers/*.trigger"],
        "LightningComponentBundle": ["**/lwc/*/*.js", "**/lwc/*/*.html", "**/lwc/*/*.js-meta.xml"],
        "AuraDefinitionBundle": ["**/aura/*/*"],
        "PermissionSet": ["**/permissionsets/*.permissionset-meta.xml"],
        "PermissionSetGroup": ["**/permissionsetgroups/*.permissionsetgroup-meta.xml"],
        "MutingPermissionSet": ["**/mutingpermissionsets/*.mutingpermissionset-meta.xml"],
        "Profile": ["**/profiles/*.profile-meta.xml"],
        "SharingRules": ["**/sharingRules/*.sharingRules-meta.xml"],
        "CustomPermission": ["**/customPermissions/*.customPermission-meta.xml"],
        "CustomMetadata": ["**/customMetadata/*.md-meta.xml"],
        "CustomApplication": ["**/applications/*.app-meta.xml"],
        "FlexiPage": ["**/flexipages/*.flexipage-meta.xml"],
        "Layout": ["**/layouts/*.layout-meta.xml"],
        "CustomTab": ["**/tabs/*.tab-meta.xml"],
        "LightningMessageChannel": ["**/messageChannels/*.messageChannel-meta.xml"],
        "NamedCredential": ["**/namedCredentials/*.namedCredential-meta.xml"],
        "ExternalCredential": ["**/externalCredentials/*.externalCredential-meta.xml"],
        "RemoteSiteSetting": ["**/remoteSiteSettings/*.remoteSite-meta.xml"],
        "AuthProvider": ["**/authproviders/*.authprovider-meta.xml"],
        "ConnectedApp": ["**/connectedApps/*.connectedApp-meta.xml"],
        "CustomLabel": ["**/labels/*.labels-meta.xml"],
        "StaticResource": ["**/staticresources/*"],
        "EmailTemplate": ["**/email/**/*.email-meta.xml"],
        "Report": ["**/reports/**/*.report-meta.xml"],
        "Dashboard": ["**/dashboards/**/*.dashboard-meta.xml"],
        "ExperienceBundle": ["**/experiences/**"],
        "SiteDotCom": ["**/sites/*.site-meta.xml"],
    },
    "exclude_patterns": [
        "**/.git/**",
        "**/.sf/**",
        "**/.sfdx/**",
        "**/node_modules/**",
        "**/.salesforce-agent-knowledge/**",
    ],
}

XML_TAGS = {
    "fullName",
    "label",
    "description",
    "active",
    "status",
    "processType",
    "triggerType",
    "object",
    "type",
    "required",
    "unique",
    "externalId",
    "referenceTo",
    "relationshipName",
    "valueSetName",
    "apiVersion",
    "url",
    "principalType",
    "protocol",
    "authenticationProtocol",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def posix(path: Path) -> str:
    return path.as_posix()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned[:120] or "metadata"


def read_text(path: Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return text[:max_chars]


def load_config(knowledge_dir: Path) -> dict[str, Any]:
    config_path = knowledge_dir / "config.json"
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return DEFAULT_CONFIG


def write_default_config(knowledge_dir: Path) -> None:
    config_path = knowledge_dir / "config.json"
    if not config_path.exists():
        config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2, sort_keys=True), encoding="utf-8")


def is_skipped(path: Path, root: Path, knowledge_dir: Path, exclude_patterns: list[str]) -> bool:
    rel = posix(path.relative_to(root))
    if knowledge_dir in path.parents or path == knowledge_dir:
        return True
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return any(fnmatch.fnmatch(rel, pattern) for pattern in exclude_patterns)


def classify(rel: str, metadata_types: dict[str, list[str]]) -> str | None:
    for metadata_type, patterns in metadata_types.items():
        if any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
            return metadata_type
    return None


def infer_name(path: Path, metadata_type: str) -> str:
    name = path.name
    suffixes = [
        ".object-meta.xml",
        ".field-meta.xml",
        ".recordType-meta.xml",
        ".validationRule-meta.xml",
        ".flow-meta.xml",
        ".permissionset-meta.xml",
        ".permissionsetgroup-meta.xml",
        ".profile-meta.xml",
        ".cls",
        ".trigger",
        ".js-meta.xml",
        ".html",
        ".js",
        ".xml",
    ]
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    if metadata_type in {"LightningComponentBundle", "AuraDefinitionBundle"}:
        return path.parent.name
    return name


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1]


def summarize_xml(text: str) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if not text.strip():
        return summary
    try:
        root = ElementTree.fromstring(text.encode("utf-8"))
    except ElementTree.ParseError:
        return summary
    counts: dict[str, int] = defaultdict(int)
    for elem in root.iter():
        tag = strip_ns(elem.tag)
        counts[tag] += 1
        value = (elem.text or "").strip()
        if tag in XML_TAGS and value and tag not in summary:
            summary[tag] = value[:300]
    for tag in ("fields", "recordTypes", "validationRules", "rules", "processMetadataValues", "assignments"):
        if counts.get(tag):
            summary[f"{tag}_count"] = counts[tag]
    return summary


def summarize_apex(text: str) -> dict[str, Any]:
    lower = text.lower()
    declarations = re.findall(r"\b(public|private|global)\s+(?:with\s+sharing|without\s+sharing|inherited\s+sharing\s+)?(?:virtual\s+|abstract\s+)?(class|interface|enum)\s+(\w+)", text)
    methods = re.findall(r"\b(public|private|global|protected)\s+(?:static\s+)?[\w<>\[\],\s]+\s+(\w+)\s*\(", text)
    return {
        "declarations": [item[2] for item in declarations[:10]],
        "method_count": len(methods),
        "aura_enabled_count": len(re.findall(r"@AuraEnabled", text)),
        "soql_count": len(re.findall(r"\[[\s\n]*SELECT\b", text, re.IGNORECASE)),
        "dml_keyword_count": sum(lower.count(word) for word in [" insert ", " update ", " upsert ", " delete ", " undelete "]),
        "sharing": "inherited sharing"
        if "inherited sharing" in lower
        else "with sharing"
        if "with sharing" in lower
        else "without sharing"
        if "without sharing" in lower
        else "unspecified",
    }


def summarize_trigger(text: str) -> dict[str, Any]:
    match = re.search(r"trigger\s+(\w+)\s+on\s+(\w+)\s*\(([^)]*)\)", text, re.IGNORECASE)
    return {
        "trigger": match.group(1) if match else None,
        "object": match.group(2) if match else None,
        "events": [item.strip() for item in match.group(3).split(",")] if match else [],
    }


def summarize_lwc(text: str) -> dict[str, Any]:
    imports = re.findall(r"import\s+(?:[^'\"]+\s+from\s+)?['\"]([^'\"]+)['\"]", text)
    wires = re.findall(r"@wire\s*\(([^)]*)\)", text)
    return {
        "imports": imports[:20],
        "wire_count": len(wires),
        "uses_lightning_data_service": any("lightning/ui" in item for item in imports),
    }


def summarize_file(path: Path, metadata_type: str, max_chars: int) -> dict[str, Any]:
    text = read_text(path, max_chars)
    summary: dict[str, Any] = {"hash": sha256_text(text), "size": path.stat().st_size}
    if path.suffix == ".xml" or path.name.endswith("-meta.xml"):
        summary.update(summarize_xml(text))
    elif metadata_type == "ApexClass":
        summary.update(summarize_apex(text))
    elif metadata_type == "ApexTrigger":
        summary.update(summarize_trigger(text))
    elif metadata_type == "LightningComponentBundle" and path.suffix == ".js":
        summary.update(summarize_lwc(text))
    return summary


def entry_text(entry: dict[str, Any]) -> str:
    summary = entry["summary"]
    parts = [entry["name"], entry["type"]]
    for key in ("label", "object", "type", "status", "processType", "triggerType", "sharing"):
        if summary.get(key):
            parts.append(f"{key}: {summary[key]}")
    if summary.get("declarations"):
        parts.append("declarations: " + ", ".join(summary["declarations"]))
    return " | ".join(parts)


def build_entries(root: Path, knowledge_dir: Path, config: dict[str, Any], selected_types: set[str] | None, max_chars: int) -> list[dict[str, Any]]:
    metadata_types = config.get("metadata_types", {})
    exclude_patterns = config.get("exclude_patterns", [])
    entries: list[dict[str, Any]] = []
    for path in root.rglob("*"):
        if not path.is_file() or is_skipped(path, root, knowledge_dir, exclude_patterns):
            continue
        rel = posix(path.relative_to(root))
        metadata_type = classify(rel, metadata_types)
        if not metadata_type or (selected_types and metadata_type not in selected_types):
            continue
        summary = summarize_file(path, metadata_type, max_chars)
        entry = {
            "id": sha256_text(f"{metadata_type}:{rel}"),
            "type": metadata_type,
            "name": infer_name(path, metadata_type),
            "path": rel,
            "summary": summary,
            "search_text": entry_text({"name": infer_name(path, metadata_type), "type": metadata_type, "summary": summary}),
        }
        entry["doc_path"] = f"metadata/{slug(metadata_type)}/{slug(entry['name'])}-{entry['id']}.md"
        entries.append(entry)
    return sorted(entries, key=lambda item: (item["type"], item["name"], item["path"]))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def md_list(entries: list[dict[str, Any]]) -> str:
    lines = []
    for entry in entries:
        lines.append(f"- [`{entry['name']}`]({entry['doc_path']}) ({entry['type']}): `{entry['path']}`")
    return "\n".join(lines) if lines else "- No matching metadata found."


def entry_object_key(entry: dict[str, Any]) -> str | None:
    path = entry["path"]
    match = re.search(r"/objects/([^/]+)/", f"/{path}")
    if match:
        return match.group(1)
    if entry["summary"].get("object"):
        return str(entry["summary"]["object"])
    return None


def describe_entry(entry: dict[str, Any]) -> str:
    summary = entry["summary"]
    if summary.get("description"):
        return str(summary["description"])[:240]
    label = summary.get("label")
    if label:
        return f"{entry['type']} metadata for {label}."
    declarations = summary.get("declarations")
    if declarations:
        return f"{entry['type']} containing {', '.join(declarations[:3])}."
    return f"{entry['type']} metadata sourced from `{entry['path']}`."


def essential_content(entry: dict[str, Any]) -> list[str]:
    summary = entry["summary"]
    keys = [
        "label",
        "fullName",
        "object",
        "type",
        "active",
        "status",
        "processType",
        "triggerType",
        "sharing",
        "method_count",
        "aura_enabled_count",
        "soql_count",
        "dml_keyword_count",
        "wire_count",
        "uses_lightning_data_service",
        "fields_count",
        "recordTypes_count",
        "validationRules_count",
        "hash",
        "size",
    ]
    lines = []
    for key in keys:
        if key in summary and summary[key] not in (None, "", []):
            lines.append(f"- {key}: `{summary[key]}`")
    if summary.get("declarations"):
        lines.append("- declarations: `" + ", ".join(summary["declarations"][:8]) + "`")
    if summary.get("events"):
        lines.append("- events: `" + ", ".join(summary["events"][:8]) + "`")
    if summary.get("imports"):
        lines.append("- imports: `" + ", ".join(summary["imports"][:8]) + "`")
    return lines[:18] or ["- No compact summary fields detected; inspect the source file before editing."]


def related_entries(entry: dict[str, Any], entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    object_key = entry_object_key(entry)
    related = []
    for candidate in entries:
        if candidate["id"] == entry["id"]:
            continue
        if object_key and entry_object_key(candidate) == object_key:
            related.append(candidate)
        elif candidate["name"] == entry["name"]:
            related.append(candidate)
    return related[:12]


def relative_link(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, from_file.parent)).as_posix()


def write_metadata_docs(root: Path, knowledge_dir: Path, entries: list[dict[str, Any]], generated_at: str) -> None:
    metadata_dir = knowledge_dir / "metadata"
    if metadata_dir.exists():
        shutil.rmtree(metadata_dir)
    for entry in entries:
        doc_file = knowledge_dir / entry["doc_path"]
        source_file = root / entry["path"]
        related = related_entries(entry, entries)
        related_lines = [
            f"- [`{item['type']}: {item['name']}`]({relative_link(doc_file, knowledge_dir / item['doc_path'])})"
            for item in related
        ]
        body = [
            f"# {entry['type']}: {entry['name']}",
            "",
            "## File",
            "",
            f"- Knowledge file: `{entry['doc_path']}`",
            f"- Source file: [`{entry['path']}`]({relative_link(doc_file, source_file)})",
            f"- Generated: `{generated_at}`",
            "",
            "## Brief Description",
            "",
            describe_entry(entry),
            "",
            "## Essential Content",
            "",
            *essential_content(entry),
            "",
            "## Links",
            "",
            "- [Knowledge index](../../index.md)",
            "- [Markdown index](../../markdown-index.md)",
            "- [Metadata catalog](../../wiki/metadata-catalog.md)",
            *(related_lines or ["- No related metadata detected in this compact index."]),
            "",
            "## Agent Notes",
            "",
            "- Use this page for planning context only.",
            "- Verify the source file before editing or deploying.",
            "- Keep responses compact; open related pages only when the task needs them.",
            "",
        ]
        write(doc_file, "\n".join(body))


def write_wiki(knowledge_dir: Path, entries: list[dict[str, Any]], generated_at: str) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["type"]].append(entry)

    counts = "\n".join(f"- {metadata_type}: {len(items)}" for metadata_type, items in sorted(grouped.items()))
    write(
        knowledge_dir / "wiki" / "overview.md",
        f"# Salesforce Metadata Knowledge Overview\n\nGenerated: `{generated_at}`\n\n## Counts\n\n{counts or '- No metadata found.'}\n\n## Use\n\nRead `index.md` first, then the relevant wiki page, then verify against source files before editing.\n",
    )

    catalog = ["# Metadata Catalog", "", f"Generated: `{generated_at}`", ""]
    for metadata_type, items in sorted(grouped.items()):
        catalog.extend([f"## {metadata_type}", "", md_list(items), ""])
    write(knowledge_dir / "wiki" / "metadata-catalog.md", "\n".join(catalog))

    pages = {
        "data-model.md": {"CustomObject", "CustomField", "RecordType", "ValidationRule", "ListView", "CompactLayout", "GlobalValueSet", "Layout"},
        "automation.md": {"Flow", "Workflow", "ApprovalProcess", "AssignmentRules", "AutoResponseRules", "EscalationRules", "DuplicateRule", "MatchingRule"},
        "apex.md": {"ApexClass", "ApexTrigger"},
        "lwc.md": {"LightningComponentBundle", "AuraDefinitionBundle", "LightningMessageChannel"},
        "security.md": {"PermissionSet", "PermissionSetGroup", "MutingPermissionSet", "Profile", "SharingRules", "CustomPermission"},
        "integrations.md": {"NamedCredential", "ExternalCredential", "RemoteSiteSetting", "AuthProvider", "ConnectedApp"},
    }
    for filename, types in pages.items():
        selected = [entry for entry in entries if entry["type"] in types]
        title = filename[:-3].replace("-", " ").title()
        body = [f"# {title}", "", f"Generated: `{generated_at}`", "", md_list(selected), ""]
        write(knowledge_dir / "wiki" / filename, "\n".join(body))


def write_indexes(root: Path, knowledge_dir: Path, entries: list[dict[str, Any]], generated_at: str) -> None:
    payload = {
        "generated_at": generated_at,
        "project_root": str(root),
        "entry_count": len(entries),
        "entries": entries,
    }
    write(knowledge_dir / "index.json", json.dumps(payload, indent=2, sort_keys=True))
    write(
        knowledge_dir / "sources.json",
        json.dumps(
            [
                {"path": entry["path"], "type": entry["type"], "name": entry["name"], "hash": entry["summary"].get("hash"), "doc_path": entry["doc_path"]}
                for entry in entries
            ],
            indent=2,
            sort_keys=True,
        ),
    )

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["type"]].append(entry)

    lines = ["# Salesforce Agent Knowledge Index", "", f"Generated: `{generated_at}`", "", "## Read First", "", "- Consult this index before planning Salesforce modifications.", "- Drill into `wiki/` pages for the relevant metadata area.", "- Verify source files before editing.", "", "## Metadata Types", ""]
    for metadata_type, items in sorted(grouped.items()):
        lines.append(f"- [{metadata_type}](wiki/metadata-catalog.md#{metadata_type.lower()}): {len(items)}")
    lines.extend(["", "## Markdown Files", "", "- [All Markdown files](markdown-index.md)", "- [Project deploy history](history/project-history.md)", "", "## Top Entries", ""])
    for entry in entries[:200]:
        lines.append(f"- [`{entry['type']}` `{entry['name']}`]({entry['doc_path']}) -> `{entry['path']}`")
    if len(entries) > 200:
        lines.append(f"- ... {len(entries) - 200} more entries in `index.json`")
    write(knowledge_dir / "index.md", "\n".join(lines) + "\n")

    write(
        knowledge_dir / "AGENTS.md",
        "# Salesforce Agent Knowledge Schema\n\n"
        "Before planning or modifying Salesforce metadata, read `index.md`, then the exact metadata page under `metadata/`, then source metadata files.\n\n"
        "Raw source metadata remains in the repository and is the source of truth. This Knowledge stores compact summaries, hashes, paths, and cross-project navigation.\n\n"
        "The user may edit `config.json` to add project-specific metadata types or path patterns. Preserve those edits on refresh.\n\n"
        "After successful deploys, append compact entries to `history/project-history.md` so future agents can understand what changed without rereading full logs.\n",
    )


def ensure_history(knowledge_dir: Path) -> None:
    history_path = knowledge_dir / "history" / "project-history.md"
    if not history_path.exists():
        write(
            history_path,
            "# Project History\n\n"
            "Compact deployment, push, and change history for AI-agent planning.\n\n"
            "| Timestamp | Action | Requirement | Modified Metadata | Event | Result |\n"
            "|---|---|---|---|---|---|\n",
        )


def ensure_memory(knowledge_dir: Path) -> None:
    memory_path = knowledge_dir / "memory.md"
    if memory_path.exists():
        return
    write(
        memory_path,
        "# Salesforce Agent Project Memory\n\n"
        "Generated/managed by Salesforce Agent Optimizer.\n\n"
        "Use this curated planning memory after Knowledge indexes/history and before raw metadata. "
        "Keep it compact and redacted. Do not store secrets, auth URLs, tokens, customer data, raw "
        "records, screenshots with PII, large logs, or raw diffs.\n\n"
        "## Current Project Facts\n- None recorded yet.\n\n"
        "## Durable Decisions\n- None recorded yet.\n\n"
        "## Recent Bugfixes\n- None recorded yet.\n\n"
        "## Recent Developments\n- None recorded yet.\n\n"
        "## Validation Lessons\n- None recorded yet.\n\n"
        "## Risks And Follow-ups\n- None recorded yet.\n\n"
        "## Deprecated Or Superseded Notes\n- None recorded yet.\n",
    )


def markdown_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return path.stem


def write_markdown_index(knowledge_dir: Path, generated_at: str) -> None:
    index_path = knowledge_dir / "markdown-index.md"
    files = sorted(path for path in knowledge_dir.rglob("*.md") if path.name != "markdown-index.md")
    lines = [
        "# Knowledge Markdown Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Use this file to jump directly to the smallest relevant Knowledge page.",
        "",
        "| File | Description |",
        "|---|---|",
    ]
    for path in files:
        rel = posix(path.relative_to(knowledge_dir))
        lines.append(f"| [{rel}]({rel}) | {markdown_title(path)} |")
    write(index_path, "\n".join(lines) + "\n")


def append_log(knowledge_dir: Path, generated_at: str, count: int) -> None:
    log_path = knowledge_dir / "log.md"
    line = f"## [{generated_at}] init | refreshed metadata knowledge | entries={count}\n\n"
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Knowledge Log\n\n"
    log_path.write_text(existing + line, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Salesforce metadata Knowledge for AI agents.")
    parser.add_argument("--project-root", default=".", help="Salesforce project root to inspect.")
    parser.add_argument("--knowledge-dir", default=KNOWLEDGE_DIR, help="Knowledge folder path, relative to project root unless absolute.")
    parser.add_argument("--metadata-types", help="Comma-separated metadata types to include for this run.")
    parser.add_argument("--max-file-chars", type=int, default=120000, help="Maximum characters to inspect per file.")
    parser.add_argument("--refresh", action="store_true", help="Overwrite generated indexes/wiki and append a refresh log entry.")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing Knowledge files.")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    knowledge_dir = Path(args.knowledge_dir)
    if not knowledge_dir.is_absolute():
        knowledge_dir = root / knowledge_dir
    selected_types = {item.strip() for item in args.metadata_types.split(",") if item.strip()} if args.metadata_types else None

    knowledge_dir.mkdir(parents=True, exist_ok=True) if not args.dry_run else None
    config = load_config(knowledge_dir) if knowledge_dir.exists() else DEFAULT_CONFIG
    entries = build_entries(root, knowledge_dir, config, selected_types, args.max_file_chars)
    generated_at = now_iso()

    if args.dry_run:
        print(json.dumps({"project_root": str(root), "entry_count": len(entries)}, indent=2))
        return 0

    write_default_config(knowledge_dir)
    ensure_history(knowledge_dir)
    ensure_memory(knowledge_dir)
    write_indexes(root, knowledge_dir, entries, generated_at)
    write_wiki(knowledge_dir, entries, generated_at)
    write_metadata_docs(root, knowledge_dir, entries, generated_at)
    write_markdown_index(knowledge_dir, generated_at)
    append_log(knowledge_dir, generated_at, len(entries))
    print(f"Knowledge refreshed: {knowledge_dir}")
    print(f"Indexed metadata entries: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
