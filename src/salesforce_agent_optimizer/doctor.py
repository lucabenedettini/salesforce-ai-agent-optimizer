"""Environment diagnostics for Salesforce Agent Optimizer."""

from __future__ import annotations

import json
import os
import platform
import shutil
import site
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import __version__
from .validation import SKILL_NAME, validate_auto


@dataclass
class Check:
    name: str
    status: str
    detail: str = ""


@dataclass
class DoctorReport:
    sections: dict[str, list[Check]] = field(default_factory=dict)

    def add(self, section: str, name: str, status: str, detail: str = "") -> None:
        self.sections.setdefault(section, []).append(Check(name, status, detail))

    @property
    def has_errors(self) -> bool:
        return any(check.status == "ERROR" for checks in self.sections.values() for check in checks)

    @property
    def has_warnings(self) -> bool:
        return any(check.status == "WARN" for checks in self.sections.values() for check in checks)

    @property
    def status(self) -> str:
        if self.has_errors:
            return "ERROR"
        if self.has_warnings:
            return "WARN"
        return "OK"

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"ok": not self.has_errors, "status": self.status}
        payload.update(
            {
                section: [check.__dict__ for check in checks]
                for section, checks in self.sections.items()
            }
        )
        return payload


def run_doctor(root: Path | None = None) -> DoctorReport:
    root = (root or Path.cwd()).resolve()
    report = DoctorReport()
    report.add("Core", "Package", "OK", f"salesforce-agent-optimizer v{__version__}")
    py_status = "OK" if sys.version_info >= (3, 10) else "ERROR"
    report.add("Core", "Python", py_status, platform.python_version())
    report.add("Core", "OS", "OK", platform.system() or sys.platform)
    report.add("Core", "Git", "OK" if shutil.which("git") else "WARN", shutil.which("git") or "not found")
    report.add(
        "Core",
        "Salesforce CLI sf",
        "OK" if shutil.which("sf") else "WARN",
        shutil.which("sf") or "not found",
    )
    report.add(
        "Core",
        "Git repository",
        "OK" if is_git_repo(root) else "WARN",
        str(root),
    )
    report.add(
        "Core",
        "Salesforce DX project",
        "OK" if (root / "sfdx-project.json").exists() else "WARN",
        "sfdx-project.json found" if (root / "sfdx-project.json").exists() else "not found",
    )
    report.add(
        "Agent adapters",
        "Codex skill",
        "OK" if (root / ".agents" / "skills" / SKILL_NAME / "SKILL.md").exists() else "WARN",
        ".agents/skills/salesforce-agent-optimizer",
    )
    report.add(
        "Agent adapters",
        "Claude skill",
        "OK" if (root / ".claude" / "skills" / SKILL_NAME / "SKILL.md").exists() else "WARN",
        ".claude/skills/salesforce-agent-optimizer",
    )
    report.add(
        "Agent adapters",
        "GitHub Copilot project skill",
        "OK" if (root / ".github" / "skills" / SKILL_NAME / "SKILL.md").exists() else "WARN",
        ".github/skills/salesforce-agent-optimizer",
    )
    copilot_ok = (root / ".github" / "copilot-instructions.md").exists() and (
        root / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md"
    ).exists()
    report.add("Agent adapters", "GitHub Copilot instructions", "OK" if copilot_ok else "WARN")
    report.add("Agent adapters", "AGENTS.md", "OK" if (root / "AGENTS.md").exists() else "WARN")
    validation = validate_auto(root, expected_version=__version__)
    report.add(
        "Validation",
        "Skill package",
        "OK" if validation.ok else "ERROR",
        "valid" if validation.ok else "; ".join(validation.errors[:3]),
    )
    if validation.warnings:
        report.add("Validation", "Warnings", "WARN", "; ".join(validation.warnings[:3]))
    report.add("Validation", "Version alignment", "OK" if validation.ok else "ERROR", f"v{__version__}")
    if platform.system().lower().startswith("windows"):
        report.add("Windows", "PATH", "OK" if user_scripts_on_path() else "WARN", windows_path_detail())
    return report


def is_git_repo(root: Path) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def user_scripts_on_path() -> bool:
    scripts = Path(site.USER_BASE) / "Scripts"
    path_parts = [Path(part) for part in (os.environ.get("PATH") or "").split(os.pathsep) if part]
    return any(part == scripts for part in path_parts)


def windows_path_detail() -> str:
    scripts = Path(site.USER_BASE) / "Scripts"
    return f"{scripts} is {'on' if user_scripts_on_path() else 'not on'} PATH"


def format_report(report: DoctorReport, verbose: bool = False) -> str:
    lines = [f"Salesforce Agent Optimizer Doctor: {report.status}"]
    if not verbose:
        issues = [
            (section, check)
            for section, checks in report.sections.items()
            for check in checks
            if check.status in {"WARN", "ERROR"}
        ]
        if issues:
            lines.append("Warnings and errors:")
            for section, check in issues:
                detail = f" {check.detail}" if check.detail else ""
                lines.append(f"- {section} / {check.name}: {check.status}{detail}")
        else:
            lines.append("No warnings or errors.")
        lines.append("Use --verbose for full diagnostics.")
        return "\n".join(lines).rstrip() + "\n"
    lines.append("")
    for section, checks in report.sections.items():
        lines.append(f"{section}:")
        for check in checks:
            detail = f" {check.detail}" if check.detail else ""
            lines.append(f"- {check.name}: {check.status}{detail}")
        lines.append("")
    lines.append("Status:")
    lines.append("Everything looks good." if not report.has_errors else "Problems found.")
    return "\n".join(lines).rstrip() + "\n"


def report_to_json(report: DoctorReport) -> str:
    return json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True) + "\n"
