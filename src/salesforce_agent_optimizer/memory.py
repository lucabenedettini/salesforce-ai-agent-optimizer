"""Curated project memory for Salesforce Agent Optimizer."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


KNOWLEDGE_DIR = ".salesforce-agent-knowledge"
MEMORY_RELATIVE = "memory.md"
DEFAULT_MEMORY_MAX_BYTES = 60000
TASK_SECTIONS = {
    "bugfix": "Recent Bugfixes",
    "development": "Recent Developments",
    "config": "Recent Developments",
    "release": "Recent Developments",
    "validation": "Validation Lessons",
    "decision": "Durable Decisions",
    "note": "Current Project Facts",
}
SECTION_NAMES = [
    "Current Project Facts",
    "Durable Decisions",
    "Recent Bugfixes",
    "Recent Developments",
    "Validation Lessons",
    "Risks And Follow-ups",
    "Deprecated Or Superseded Notes",
]
SECRET_PATTERNS = [
    re.compile(r"(?i)(access[_-]?token|refresh[_-]?token|session[_-]?id|sid|auth[_-]?url)=\S+"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)(force://[^:\s]+:)[^@\s]+(@)"),
    re.compile(r"00D[A-Za-z0-9]{12,}![A-Za-z0-9._~+/=-]+"),
]


@dataclass
class MemoryReport:
    action: str
    project_root: str
    memory_path: str
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
            "memory_path": self.memory_path,
            "changed": self.changed,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def memory_path(project_root: Path) -> Path:
    return project_root / KNOWLEDGE_DIR / MEMORY_RELATIVE


def memory_template() -> str:
    sections = "\n\n".join(f"## {section}\n- None recorded yet." for section in SECTION_NAMES)
    return (
        "# Salesforce Agent Project Memory\n\n"
        "Generated/managed by Salesforce Agent Optimizer.\n\n"
        "Use this curated planning memory after Knowledge indexes/history and before raw metadata. "
        "Keep it compact and redacted. Do not store secrets, auth URLs, tokens, customer data, raw "
        "records, screenshots with PII, large logs, or raw diffs.\n\n"
        f"{sections}\n"
    )


def redact(text: str) -> str:
    value = text
    for pattern in SECRET_PATTERNS:
        value = pattern.sub(lambda match: f"{match.group(1)}[REDACTED]" if match.lastindex else "[REDACTED]", value)
    return value


def write_if_changed(path: Path, text: str, changed: list[str], root: Path) -> None:
    text = text.rstrip() + "\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    changed.append(path.relative_to(root).as_posix())


def ensure_memory(project_root: Path, changed: list[str]) -> Path:
    path = memory_path(project_root)
    if not path.exists():
        write_if_changed(path, memory_template(), changed, project_root)
    return path


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {section: [] for section in SECTION_NAMES}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            name = line[3:].strip()
            current = name if name in sections else None
            continue
        if current:
            sections[current].append(line)
    return sections


def render_sections(sections: dict[str, list[str]]) -> str:
    lines = [
        "# Salesforce Agent Project Memory",
        "",
        "Generated/managed by Salesforce Agent Optimizer.",
        "",
        "Use this curated planning memory after Knowledge indexes/history and before raw metadata. "
        "Keep it compact and redacted. Do not store secrets, auth URLs, tokens, customer data, raw "
        "records, screenshots with PII, large logs, or raw diffs.",
        "",
    ]
    for section in SECTION_NAMES:
        lines.append(f"## {section}")
        body = [line for line in sections.get(section, []) if line.strip()]
        if not body:
            lines.append("- None recorded yet.")
        else:
            lines.extend(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def append_to_section(text: str, section: str, entry: str) -> str:
    sections = split_sections(text)
    body = [line for line in sections[section] if line.strip() != "- None recorded yet."]
    body.extend(entry.rstrip().splitlines())
    sections[section] = body
    return render_sections(sections)


def build_entry(
    task_type: str,
    summary: str,
    metadata: list[str] | None = None,
    files: list[str] | None = None,
    validation: str | None = None,
    risk: str | None = None,
    follow_up: str | None = None,
    decision: str | None = None,
) -> str:
    lines = [f"- {now_iso()[:10]} | {task_type} | {redact(summary)}"]
    if metadata:
        lines.append("  - Artifacts: " + ", ".join(redact(item) for item in metadata))
    if files:
        lines.append("  - Files: " + ", ".join(redact(item) for item in files))
    if decision:
        lines.append(f"  - Decision: {redact(decision)}")
    if validation:
        lines.append(f"  - Validation: {redact(validation)}")
    if risk:
        lines.append(f"  - Risk: {redact(risk)}")
    if follow_up:
        lines.append(f"  - Follow-up: {redact(follow_up)}")
    return "\n".join(lines)


def compact_memory_text(text: str, max_bytes: int) -> str:
    if len(text.encode("utf-8")) <= max_bytes:
        return text.rstrip() + "\n"
    sections = split_sections(text)
    compacted: dict[str, list[str]] = {}
    for section, lines in sections.items():
        clean = [line for line in lines if line.strip() and line.strip() != "- None recorded yet."]
        if section in {"Current Project Facts", "Durable Decisions", "Risks And Follow-ups"}:
            compacted[section] = list(dict.fromkeys(clean))[-120:]
        elif section == "Deprecated Or Superseded Notes":
            compacted[section] = list(dict.fromkeys(clean))[-40:]
        else:
            compacted[section] = list(dict.fromkeys(clean))[-80:]
    note = f"- Memory compacted on {now_iso()}. Older duplicate or superseded notes were removed or summarized."
    compacted["Deprecated Or Superseded Notes"] = compacted.get("Deprecated Or Superseded Notes", []) + [note]
    rendered = render_sections(compacted)
    while len(rendered.encode("utf-8")) > max_bytes and max_bytes > 2000:
        for section in ("Recent Bugfixes", "Recent Developments", "Validation Lessons"):
            if len(compacted.get(section, [])) > 20:
                compacted[section] = compacted[section][10:]
        rendered = render_sections(compacted)
        if all(len(compacted.get(section, [])) <= 20 for section in ("Recent Bugfixes", "Recent Developments", "Validation Lessons")):
            break
    return rendered


def run_memory(
    action: str,
    project_root: Path,
    *,
    task_type: str | None = None,
    summary: str | None = None,
    metadata: list[str] | None = None,
    files: list[str] | None = None,
    validation: str | None = None,
    risk: str | None = None,
    follow_up: str | None = None,
    decision: str | None = None,
    max_bytes: int = DEFAULT_MEMORY_MAX_BYTES,
) -> MemoryReport:
    root = project_root.resolve()
    path = memory_path(root)
    report = MemoryReport(action=action, project_root=str(root), memory_path=str(path))
    changed: list[str] = []
    if action == "init":
        ensure_memory(root, changed)
        report.changed = changed
        return report
    if action == "doctor":
        if not path.exists():
            report.errors.append(f"Missing project memory file: {path.relative_to(root).as_posix()}")
            return report
        text = path.read_text(encoding="utf-8")
        for section in SECTION_NAMES:
            if f"## {section}" not in text:
                report.errors.append(f"Project memory missing section: {section}")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            report.errors.append("Project memory appears to contain unredacted secrets")
        return report
    ensure_memory(root, changed)
    text = path.read_text(encoding="utf-8")
    if action == "add":
        if task_type not in TASK_SECTIONS:
            report.errors.append("Unsupported memory task type")
            return report
        if not summary:
            report.errors.append("Missing --summary for memory add")
            return report
        entry = build_entry(task_type, summary, metadata, files, validation, risk, follow_up, decision)
        text = append_to_section(text, TASK_SECTIONS[task_type], entry)
        write_if_changed(path, text, changed, root)
    elif action == "compact":
        text = compact_memory_text(text, max_bytes)
        write_if_changed(path, text, changed, root)
    else:
        report.errors.append(f"Unsupported memory action: {action}")
        return report
    report.changed = changed
    return report


def format_memory_report(report: MemoryReport, verbose: bool = False) -> str:
    status = "OK" if report.ok else "ERROR"
    lines = [f"Salesforce Agent Memory: {status}", f"- action: {report.action}"]
    if report.changed:
        lines.append(f"- changed: {len(report.changed)}")
    for warning in report.warnings:
        lines.append(f"WARN: {warning}")
    for error in report.errors:
        lines.append(f"ERROR: {error}")
    if verbose and report.changed:
        lines.append("Changed files:")
        lines.extend(f"- {item}" for item in report.changed)
    return "\n".join(lines) + "\n"
