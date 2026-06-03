"""Compact local Salesforce project Knowledge generation."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
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
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
}
DEFAULT_METADATA_TYPES: dict[str, list[str]] = {
    "CustomObject": ["**/objects/*/*.object-meta.xml"],
    "CustomField": ["**/objects/*/fields/*.field-meta.xml"],
    "RecordType": ["**/objects/*/recordTypes/*.recordType-meta.xml"],
    "ValidationRule": ["**/objects/*/validationRules/*.validationRule-meta.xml"],
    "Layout": ["**/layouts/*.layout-meta.xml"],
    "FlexiPage": ["**/flexipages/*.flexipage-meta.xml"],
    "Flow": ["**/flows/*.flow-meta.xml"],
    "ApexClass": ["**/classes/*.cls"],
    "ApexTrigger": ["**/triggers/*.trigger"],
    "LightningComponentBundle": ["**/lwc/*/*.js", "**/lwc/*/*.html", "**/lwc/*/*.js-meta.xml"],
    "PermissionSet": ["**/permissionsets/*.permissionset-meta.xml"],
    "PermissionSetGroup": ["**/permissionsetgroups/*.permissionsetgroup-meta.xml"],
    "Profile": ["**/profiles/*.profile-meta.xml"],
    "CustomMetadata": ["**/customMetadata/*.md-meta.xml"],
    "NamedCredential": ["**/namedCredentials/*.namedCredential-meta.xml"],
    "ExternalCredential": ["**/externalCredentials/*.externalCredential-meta.xml"],
    "ConnectedApp": ["**/connectedApps/*.connectedApp-meta.xml"],
    "CustomApplication": ["**/applications/*.app-meta.xml"],
    "CustomTab": ["**/tabs/*.tab-meta.xml"],
    "Report": ["**/reports/**/*.report-meta.xml"],
    "Dashboard": ["**/dashboards/**/*.dashboard-meta.xml"],
}
DEFAULT_CONFIG: dict[str, Any] = {
    "metadata_types": DEFAULT_METADATA_TYPES,
    "exclude_patterns": [
        "**/.git/**",
        "**/.sf/**",
        "**/.sfdx/**",
        "**/node_modules/**",
        "**/.salesforce-agent-knowledge/**",
        "**/dist/**",
        "**/build/**",
    ],
}
XML_SUMMARY_TAGS = {
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
}
REQUIRED_KNOWLEDGE_FILES = [
    "AGENTS.md",
    "config.json",
    "index.json",
    "index.md",
    "markdown-index.md",
    "log.md",
    "sources.json",
    "history/project-history.md",
    "wiki/overview.md",
    "wiki/metadata-catalog.md",
    "wiki/data-model.md",
    "wiki/automation.md",
    "wiki/apex.md",
    "wiki/lwc.md",
    "wiki/security.md",
    "wiki/integrations.md",
]


@dataclass
class KnowledgeReport:
    action: str
    project_root: str
    knowledge_dir: str
    entry_count: int = 0
    changed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "action": self.action,
            "project_root": self.project_root,
            "knowledge_dir": self.knowledge_dir,
            "entry_count": self.entry_count,
            "changed": self.changed,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def posix(path: Path) -> str:
    return path.as_posix()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return re.sub(r"-+", "-", cleaned).strip("-")[:120] or "metadata"


def load_config(knowledge_dir: Path) -> dict[str, Any]:
    path = knowledge_dir / "config.json"
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass
    return DEFAULT_CONFIG


def write_text(path: Path, text: str, changed: list[str], root: Path) -> None:
    text = text.rstrip() + "\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    changed.append(posix(path.relative_to(root)))


def is_skipped(path: Path, root: Path, knowledge_dir: Path, exclude_patterns: list[str]) -> bool:
    if knowledge_dir in path.parents or path == knowledge_dir:
        return True
    if any(part in SKIP_DIRS or part.endswith(".egg-info") for part in path.parts):
        return True
    rel = posix(path.relative_to(root))
    return any(fnmatch.fnmatch(rel, pattern) for pattern in exclude_patterns)


def classify(rel: str, metadata_types: dict[str, list[str]]) -> str | None:
    for metadata_type, patterns in metadata_types.items():
        if any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
            return metadata_type
    return None


def infer_name(path: Path, metadata_type: str) -> str:
    if metadata_type in {"LightningComponentBundle"}:
        return path.parent.name
    name = path.name
    for suffix in (
        ".object-meta.xml",
        ".field-meta.xml",
        ".recordType-meta.xml",
        ".validationRule-meta.xml",
        ".layout-meta.xml",
        ".flexipage-meta.xml",
        ".flow-meta.xml",
        ".permissionset-meta.xml",
        ".permissionsetgroup-meta.xml",
        ".profile-meta.xml",
        ".cls",
        ".trigger",
        ".xml",
    ):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def summarize_file(path: Path) -> dict[str, Any]:
    summary: dict[str, Any] = {"hash": file_hash(path), "bytes": path.stat().st_size}
    if path.suffix.lower() != ".xml":
        if path.suffix.lower() in {".cls", ".trigger", ".js", ".html"}:
            text = path.read_text(encoding="utf-8", errors="replace")[:12000]
            summary["lines"] = text.count("\n") + 1 if text else 0
            summary["symbols"] = sorted(set(re.findall(r"\b(class|trigger|@wire|import)\b", text)))[:8]
        return summary
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:120000]
        root = ElementTree.fromstring(text.encode("utf-8"))
    except (OSError, ElementTree.ParseError):
        return summary
    counts: dict[str, int] = defaultdict(int)
    for elem in root.iter():
        tag = elem.tag.split("}", 1)[-1]
        counts[tag] += 1
        value = (elem.text or "").strip()
        if tag in XML_SUMMARY_TAGS and value and tag not in summary:
            summary[tag] = value[:240]
    for tag in ("fields", "recordTypes", "validationRules", "rules", "assignments"):
        if counts.get(tag):
            summary[f"{tag}_count"] = counts[tag]
    return summary


def build_entries(root: Path, knowledge_dir: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    metadata_types = config.get("metadata_types", DEFAULT_METADATA_TYPES)
    exclude_patterns = config.get("exclude_patterns", DEFAULT_CONFIG["exclude_patterns"])
    if not isinstance(metadata_types, dict) or not isinstance(exclude_patterns, list):
        metadata_types = DEFAULT_METADATA_TYPES
        exclude_patterns = DEFAULT_CONFIG["exclude_patterns"]
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or is_skipped(path, root, knowledge_dir, exclude_patterns):
            continue
        rel = posix(path.relative_to(root))
        metadata_type = classify(rel, metadata_types)
        if metadata_type is None:
            continue
        name = infer_name(path, metadata_type)
        doc_path = f"metadata/{metadata_type}/{slug(name)}.md"
        entries.append(
            {
                "type": metadata_type,
                "name": name,
                "path": rel,
                "doc_path": doc_path,
                "summary": summarize_file(path),
            }
        )
    return entries


def render_entry(entry: dict[str, Any], generated_at: str) -> str:
    summary = entry["summary"]
    facts = "\n".join(f"- {key}: `{value}`" for key, value in sorted(summary.items())[:16])
    return "\n".join(
        [
            f"# {entry['type']}: {entry['name']}",
            "",
            f"Generated: `{generated_at}`",
            "",
            "## Source",
            "",
            f"- Path: `{entry['path']}`",
            f"- Hash: `{summary.get('hash', '')}`",
            "",
            "## Compact Facts",
            "",
            facts or "- No compact facts extracted.",
            "",
            "## Agent Links",
            "",
            "- [Knowledge index](../../index.md)",
            "- [Metadata catalog](../../wiki/metadata-catalog.md)",
            "",
        ]
    )


def write_knowledge(root: Path, knowledge_dir: Path, entries: list[dict[str, Any]]) -> list[str]:
    generated_at = now_iso()
    changed: list[str] = []
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    if not (knowledge_dir / "config.json").exists():
        write_text(
            knowledge_dir / "config.json",
            json.dumps(DEFAULT_CONFIG, indent=2, sort_keys=True),
            changed,
            root,
        )
    ensure_history(root, knowledge_dir, changed)
    write_indexes(root, knowledge_dir, entries, generated_at, changed)
    write_wiki(root, knowledge_dir, entries, generated_at, changed)
    for entry in entries:
        write_text(
            knowledge_dir / entry["doc_path"],
            render_entry(entry, generated_at),
            changed,
            root,
        )
    write_markdown_index(root, knowledge_dir, generated_at, changed)
    append_log(root, knowledge_dir, generated_at, len(entries), changed)
    return changed


def ensure_history(root: Path, knowledge_dir: Path, changed: list[str]) -> None:
    path = knowledge_dir / "history" / "project-history.md"
    if path.exists():
        return
    write_text(
        path,
        "# Project History\n\n"
        "| Timestamp | Action | Requirement | Modified Metadata | Event | Result |\n"
        "|---|---|---|---|---|---|\n",
        changed,
        root,
    )


def write_indexes(
    root: Path,
    knowledge_dir: Path,
    entries: list[dict[str, Any]],
    generated_at: str,
    changed: list[str],
) -> None:
    payload = {"generated_at": generated_at, "entry_count": len(entries), "entries": entries}
    write_text(knowledge_dir / "index.json", json.dumps(payload, indent=2, sort_keys=True), changed, root)
    sources = [
        {
            "path": entry["path"],
            "type": entry["type"],
            "name": entry["name"],
            "hash": entry["summary"].get("hash"),
            "doc_path": entry["doc_path"],
        }
        for entry in entries
    ]
    write_text(knowledge_dir / "sources.json", json.dumps(sources, indent=2, sort_keys=True), changed, root)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["type"]].append(entry)
    lines = [
        "# Salesforce Agent Knowledge Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Read this before planning Salesforce changes, then open only the relevant metadata pages.",
        "",
        "## Metadata Types",
        "",
    ]
    for metadata_type, items in sorted(grouped.items()):
        lines.append(f"- {metadata_type}: {len(items)}")
    lines.extend(["", "## Top Entries", ""])
    for entry in entries[:100]:
        lines.append(f"- [`{entry['type']}` `{entry['name']}`]({entry['doc_path']}) -> `{entry['path']}`")
    if len(entries) > 100:
        lines.append(f"- ... {len(entries) - 100} more entries in `index.json`")
    write_text(knowledge_dir / "index.md", "\n".join(lines), changed, root)
    write_text(
        knowledge_dir / "AGENTS.md",
        "# Salesforce Agent Knowledge\n\n"
        "Use `index.md` first, then the smallest relevant metadata page. Source metadata remains "
        "the source of truth. Keep task summaries compact and preserve safety warnings.\n",
        changed,
        root,
    )


def write_wiki(
    root: Path,
    knowledge_dir: Path,
    entries: list[dict[str, Any]],
    generated_at: str,
    changed: list[str],
) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        grouped[entry["type"]].append(entry)
    counts = "\n".join(f"- {key}: {len(value)}" for key, value in sorted(grouped.items()))
    write_text(
        knowledge_dir / "wiki" / "overview.md",
        f"# Knowledge Overview\n\nGenerated: `{generated_at}`\n\n{counts or '- No metadata found.'}\n",
        changed,
        root,
    )
    catalog = ["# Metadata Catalog", "", f"Generated: `{generated_at}`", ""]
    for metadata_type, items in sorted(grouped.items()):
        catalog.extend([f"## {metadata_type}", ""])
        catalog.extend(f"- `{item['name']}` -> `{item['path']}`" for item in items[:200])
        if len(items) > 200:
            catalog.append(f"- ... {len(items) - 200} more in `index.json`")
        catalog.append("")
    write_text(knowledge_dir / "wiki" / "metadata-catalog.md", "\n".join(catalog), changed, root)
    page_types = {
        "data-model.md": {"CustomObject", "CustomField", "RecordType", "ValidationRule", "Layout"},
        "automation.md": {"Flow"},
        "apex.md": {"ApexClass", "ApexTrigger"},
        "lwc.md": {"LightningComponentBundle"},
        "security.md": {"PermissionSet", "PermissionSetGroup", "Profile"},
        "integrations.md": {"NamedCredential", "ExternalCredential", "ConnectedApp"},
    }
    for filename, types in page_types.items():
        selected = [entry for entry in entries if entry["type"] in types]
        body = [f"# {filename[:-3].replace('-', ' ').title()}", "", f"Generated: `{generated_at}`", ""]
        body.extend(f"- `{entry['type']}` `{entry['name']}` -> `{entry['path']}`" for entry in selected[:200])
        if not selected:
            body.append("- No matching metadata found.")
        write_text(knowledge_dir / "wiki" / filename, "\n".join(body), changed, root)


def write_markdown_index(root: Path, knowledge_dir: Path, generated_at: str, changed: list[str]) -> None:
    files = sorted(path for path in knowledge_dir.rglob("*.md") if path.name != "markdown-index.md")
    lines = ["# Knowledge Markdown Index", "", f"Generated: `{generated_at}`", ""]
    for path in files:
        rel = posix(path.relative_to(knowledge_dir))
        lines.append(f"- [{rel}]({rel})")
    write_text(knowledge_dir / "markdown-index.md", "\n".join(lines), changed, root)


def append_log(root: Path, knowledge_dir: Path, generated_at: str, count: int, changed: list[str]) -> None:
    path = knowledge_dir / "log.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Knowledge Log\n\n"
    line = f"## [{generated_at}] refresh | entries={count}\n\n"
    write_text(path, existing.rstrip() + "\n\n" + line, changed, root)


def run_knowledge(
    action: str,
    project_root: Path,
    target_org: str | None = None,
    max_items: int | None = None,
) -> KnowledgeReport:
    root = project_root.resolve()
    knowledge_dir = root / KNOWLEDGE_DIR
    report = KnowledgeReport(action=action, project_root=str(root), knowledge_dir=str(knowledge_dir))
    if target_org:
        report.warnings.append("Org enrichment is not performed by default; alias was recorded only.")
    if action in {"init", "refresh"}:
        config = load_config(knowledge_dir)
        entries = build_entries(root, knowledge_dir, config)
        if max_items is not None:
            entries = entries[:max_items]
        report.entry_count = len(entries)
        report.changed = write_knowledge(root, knowledge_dir, entries)
        return report
    if action == "doctor":
        missing = [relative for relative in REQUIRED_KNOWLEDGE_FILES if not (knowledge_dir / relative).exists()]
        if missing:
            report.errors.extend(f"Missing Knowledge file: {item}" for item in missing)
            return report
        try:
            index = json.loads((knowledge_dir / "index.json").read_text(encoding="utf-8"))
            report.entry_count = int(index.get("entry_count", 0))
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            report.errors.append(f"Invalid Knowledge index.json: {exc}")
        return report
    report.errors.append(f"Unsupported knowledge action: {action}")
    return report


def format_knowledge_report(report: KnowledgeReport, verbose: bool = False) -> str:
    status = "OK" if report.ok else "ERROR"
    lines = [f"Salesforce Agent Knowledge: {status}", f"- action: {report.action}"]
    lines.append(f"- entries: {report.entry_count}")
    if report.changed:
        lines.append(f"- changed: {len(report.changed)}")
    for warning in report.warnings:
        lines.append(f"WARN: {warning}")
    for error in report.errors:
        lines.append(f"ERROR: {error}")
    if verbose and report.changed:
        lines.append("Changed files:")
        lines.extend(f"- {item}" for item in report.changed[:200])
    return "\n".join(lines) + "\n"
