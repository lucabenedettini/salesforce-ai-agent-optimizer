"""Static local health reports for Salesforce Agent Optimizer."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .memory import (
    DEFAULT_MEMORY_MAX_BYTES,
    SECTION_NAMES,
    SECRET_PATTERNS,
    KNOWLEDGE_DIR,
    memory_path,
)
from .validation import parse_pyproject_version


DEFAULT_REPORT_RELATIVE = Path(KNOWLEDGE_DIR) / "reports" / "sfao-report.md"
SUPPORTED_FORMATS = {"md"}

ADAPTER_FILES = [
    "AGENTS.md",
    ".agents/skills/salesforce-agent-optimizer/SKILL.md",
    ".claude/skills/salesforce-agent-optimizer/SKILL.md",
    ".github/skills/salesforce-agent-optimizer/SKILL.md",
    ".github/copilot-instructions.md",
    ".github/instructions/salesforce-agent-optimizer.instructions.md",
]
KNOWLEDGE_FILES = {
    "index": Path(KNOWLEDGE_DIR) / "index.md",
    "config": Path(KNOWLEDGE_DIR) / "config.json",
    "history": Path(KNOWLEDGE_DIR) / "history" / "project-history.md",
}
SPECIALIZED_GUIDANCE = {
    "Apex": "apex.md",
    "LWC": "lwc.md",
    "Flow": "flow.md",
    "SOQL": "soql.md",
    "Deploy": "deploy.md",
    "Data operations": "data-operations.md",
    "Agentforce": "agentforce.md",
    "Index": "index.md",
}
EVAL_FILES = [
    "evals/salesforce-agent-optimizer-trigger-evals.json",
    "evals/salesforce-agent-optimizer-quality-evals.json",
]
VERSION_CONTEXT_FILES = [
    "references/salesforce-current-version.md",
    "references/salesforce-version.json",
]
GUARDRAILS = [
    "Explicit org alias before org access: active",
    "Production read-only for write/execute: active",
    "Destructive operation approval: active",
    "Secret exposure approval: active",
    "Knowledge/memory-first planning: active",
    "package.xml required after metadata changes: active",
    "External skills cannot bypass SFAO safety: active",
    "Iterative tool loops require completion condition and cap: active",
    "`safe-run --safety` cannot downgrade automatic classification: active",
]


@dataclass
class ReportResult:
    """Result for a generated static report."""

    output_path: Path
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "output_path": str(self.output_path),
            "warnings": self.warnings,
            "errors": self.errors,
        }


def generate_report(project_root: Path, output: Path | None = None, fmt: str = "md") -> ReportResult:
    """Generate a compact static Markdown report from local files only."""
    root = project_root.resolve()
    output_path = (output or root / DEFAULT_REPORT_RELATIVE)
    if not output_path.is_absolute():
        output_path = root / output_path
    result = ReportResult(output_path=output_path)
    if fmt not in SUPPORTED_FORMATS:
        result.errors.append(f"Unsupported report format: {fmt}")
        return result
    try:
        text, warnings = build_markdown_report(root)
        result.warnings = warnings
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8", newline="\n")
    except OSError as exc:
        result.errors.append(f"Could not write report: {exc}")
    return result


def build_markdown_report(root: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    versions = version_rows(root, warnings)
    installation_rows = installation_status(root, warnings)
    knowledge = knowledge_status(root, warnings)
    memory = memory_status(root, warnings)
    guidance_rows = specialized_guidance_status(root, warnings)
    eval_rows = eval_coverage(root, warnings)
    version_context_rows = version_context_status(root, warnings)
    suggestions = suggested_commands(warnings, memory)
    overall = "warning" if warnings else "ok"
    lines = [
        "# Salesforce Agent Optimizer Report",
        "",
        "## Summary",
        "",
        f"- Project root: `{root}`",
        f"- Generated at: `{utc_now()}`",
        f"- SFAO version: `{__version__}`",
        f"- Overall status: `{overall}`",
        "",
        "## Version",
        "",
        "| Source | Value | Status |",
        "| --- | --- | --- |",
        *versions,
        "",
        "## Installation Status",
        "",
        "| Adapter file | Status |",
        "| --- | --- |",
        *installation_rows,
        "",
        "## Knowledge Status",
        "",
        *knowledge,
        "",
        "## Memory Status",
        "",
        *memory["lines"],
        "",
        "## Guardrails",
        "",
        *(f"- {item}" for item in GUARDRAILS),
        "",
        "## Specialized Guidance",
        "",
        "| Guidance | Status |",
        "| --- | --- |",
        *guidance_rows,
        "",
        "## Eval Coverage",
        "",
        "| Eval file | Status | Examples |",
        "| --- | --- | --- |",
        *eval_rows,
        "",
        "## Version Context",
        "",
        *version_context_rows,
        "",
        "## Warnings",
        "",
        *(warnings or ["None."]),
        "",
        "## Suggested Commands",
        "",
    ]
    if suggestions:
        lines.append("```bash")
        lines.extend(suggestions)
        lines.append("```")
    else:
        lines.append("None.")
    return "\n".join(lines).rstrip() + "\n", warnings


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def status(value: bool) -> str:
    return "present" if value else "missing"


def version_rows(root: Path, warnings: list[str]) -> list[str]:
    rows: list[tuple[str, str | None]] = []
    version_path = root / "VERSION"
    rows.append(("VERSION", version_path.read_text(encoding="utf-8").strip() if version_path.exists() else None))
    pyproject = root / "pyproject.toml"
    rows.append(("pyproject.toml", parse_pyproject_version(pyproject) if pyproject.exists() else None))
    readme = root / "README.md"
    rows.append(("README.md", readme_version(readme) if readme.exists() else None))
    known = [value for _, value in rows if value]
    aligned = len(set(known)) <= 1
    if known and not aligned:
        warnings.append("- Version values appear misaligned.")
    return [
        f"| {source} | {value or 'missing'} | {'ok' if value and aligned else 'warning'} |"
        for source, value in rows
        if value is not None or source != "README.md"
    ]


def readme_version(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"\b(?:v)?(\d+\.\d+\.\d+)\b", text)
    return match.group(1) if match else None


def installation_status(root: Path, warnings: list[str]) -> list[str]:
    rows = []
    for relative in ADAPTER_FILES:
        exists = (root / relative).exists()
        rows.append(f"| {relative} | {status(exists)} |")
        if not exists:
            warnings.append(f"- `{relative}` is missing. This may be intentional if that adapter is not used.")
    return rows


def knowledge_status(root: Path, warnings: list[str]) -> list[str]:
    states = {name: (root / relative).exists() for name, relative in KNOWLEDGE_FILES.items()}
    metadata_dir = root / KNOWLEDGE_DIR / "metadata"
    metadata_pages = len(list(metadata_dir.rglob("*.md"))) if metadata_dir.exists() else 0
    initialized = states["index"] and states["config"]
    if not initialized:
        warnings.append("- Knowledge is not initialized. Suggested command: `sfao knowledge init --project-root .`")
    lines = [
        f"- Initialized: `{'yes' if initialized else 'no'}`",
        f"- Index: `{status(states['index'])}`",
        f"- Config: `{status(states['config'])}`",
        f"- Project history: `{status(states['history'])}`",
        f"- Metadata pages: `{metadata_pages}`",
    ]
    return lines


def memory_status(root: Path, warnings: list[str]) -> dict[str, Any]:
    path = memory_path(root)
    if not path.exists():
        warnings.append("- Memory is missing. Suggested command: `sfao memory init --project-root .`")
        return {
            "missing": True,
            "oversized": False,
            "lines": [
                "- Memory file: `missing`",
                "- Size: `0 bytes`",
                "- Above default threshold: `no`",
                "- Required sections: `missing`",
                "- Secret pattern warning: `none`",
            ],
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    size = len(text.encode("utf-8"))
    missing_sections = [section for section in SECTION_NAMES if f"## {section}" not in text]
    has_secrets = any(pattern.search(text) for pattern in SECRET_PATTERNS)
    oversized = size > DEFAULT_MEMORY_MAX_BYTES
    if missing_sections:
        warnings.append("- Memory is missing required sections. Suggested command: `sfao memory doctor --project-root .`")
    if has_secrets:
        warnings.append("- Memory may contain secret patterns. Suggested command: `sfao memory doctor --project-root .`")
    if oversized:
        warnings.append("- Memory is above the default size threshold. Suggested command: `sfao memory compact --project-root . --max-bytes 60000`")
    return {
        "missing": False,
        "oversized": oversized,
        "lines": [
            "- Memory file: `present`",
            f"- Size: `{size} bytes`",
            f"- Above default threshold: `{'yes' if oversized else 'no'}`",
            f"- Required sections: `{'missing' if missing_sections else 'ok'}`",
            f"- Secret pattern warning: `{'detected' if has_secrets else 'none'}`",
        ],
    }


def specialized_guidance_status(root: Path, warnings: list[str]) -> list[str]:
    base = find_references_base(root)
    rows = []
    for label, filename in SPECIALIZED_GUIDANCE.items():
        exists = bool(base and (base / "specialized-guidance" / filename).exists())
        rows.append(f"| {label} | {status(exists)} |")
        if not exists:
            warnings.append(f"- Specialized guidance missing: `{filename}`.")
    return rows


def find_references_base(root: Path) -> Path | None:
    candidates = [
        root / "references",
        root / ".agents" / "skills" / "salesforce-agent-optimizer" / "references",
        root / ".github" / "skills" / "salesforce-agent-optimizer" / "references",
        root / ".claude" / "skills" / "salesforce-agent-optimizer" / "references",
    ]
    for candidate in candidates:
        if (candidate / "specialized-guidance").exists():
            return candidate
    return None


def eval_coverage(root: Path, warnings: list[str]) -> list[str]:
    rows = []
    for relative in EVAL_FILES:
        path = root / relative
        if not path.exists() and relative.endswith("salesforce-agent-optimizer-trigger-evals.json"):
            fallback = root / "evals" / "trigger-evals.json"
            path = fallback if fallback.exists() else path
        if not path.exists():
            rows.append(f"| {relative} | missing | 0 |")
            warnings.append(f"- Eval file missing: `{relative}`.")
            continue
        examples = count_eval_examples(path, warnings)
        rows.append(f"| {path.relative_to(root).as_posix()} | present | {examples} |")
    return rows


def count_eval_examples(path: Path, warnings: list[str]) -> int | str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        warnings.append(f"- Eval file has invalid JSON: `{path.as_posix()}`.")
        return "invalid"
    if isinstance(payload, dict):
        if isinstance(payload.get("examples"), list):
            return len(payload["examples"])
        return sum(len(value) for value in payload.values() if isinstance(value, list))
    if isinstance(payload, list):
        return len(payload)
    return 0


def version_context_status(root: Path, warnings: list[str]) -> list[str]:
    lines = []
    for relative in VERSION_CONTEXT_FILES:
        exists = (root / relative).exists()
        lines.append(f"- {Path(relative).name}: `{status(exists)}`")
        if not exists:
            warnings.append(f"- Version context missing: `{relative}`.")
    lines.append("- Freshness: `not checked`")
    return lines


def suggested_commands(warnings: list[str], memory: dict[str, Any]) -> list[str]:
    suggestions: list[str] = []
    joined = "\n".join(warnings)
    if "Knowledge is not initialized" in joined:
        suggestions.append("sfao knowledge init --project-root .")
    if memory.get("missing"):
        suggestions.append("sfao memory init --project-root .")
    if "Memory is missing required sections" in joined or "Memory may contain secret patterns" in joined:
        suggestions.append("sfao memory doctor --project-root .")
    if memory.get("oversized"):
        suggestions.append("sfao memory compact --project-root . --max-bytes 60000")
    if "Version context missing" in joined:
        suggestions.append("sfao version-context validate --max-age-days 90")
    if warnings:
        suggestions.extend(["sfao validate", "sfao doctor"])
    return list(dict.fromkeys(suggestions))
