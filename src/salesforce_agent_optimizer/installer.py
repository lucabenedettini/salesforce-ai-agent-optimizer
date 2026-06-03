"""Install package templates for supported AI agents."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from typing import Iterable

from . import __version__
from .validation import GENERATED_MARKER, SKILL_NAME


MANIFEST_NAME = ".sfao-install.json"
MARKER_MD = f"<!-- {GENERATED_MARKER} -->"
MARKER_COMMENT = f"# {GENERATED_MARKER}"
SUPPORTED_PLATFORMS = {"codex", "claude", "copilot", "all"}


@dataclass
class InstallReport:
    installed: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, list[str] | bool]:
        return {
            "ok": self.ok,
            "installed": self.installed,
            "updated": self.updated,
            "skipped": self.skipped,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def template_root():
    return resources.files("salesforce_agent_optimizer").joinpath("templates")


def install(
    destination: Path,
    project: bool = False,
    platform: str = "all",
) -> InstallReport:
    destination = destination.resolve()
    report = InstallReport()
    selected = expand_platforms(platform)
    root = template_root()
    for item in selected:
        if item == "codex":
            install_codex(root, destination, project, report)
        elif item == "claude":
            install_claude(root, destination, project, report)
        elif item == "copilot":
            install_copilot(root, destination, project, report)
    write_manifest(destination, selected, project, report)
    return report


def expand_platforms(platform: str) -> list[str]:
    normalized = platform.lower()
    if normalized not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform}")
    if normalized == "all":
        return ["codex", "claude", "copilot"]
    return [normalized]


def install_codex(root, destination: Path, project: bool, report: InstallReport) -> None:
    base = destination / ".agents" / "skills" / SKILL_NAME if project else destination / ".agents" / "skills" / SKILL_NAME
    copy_template_file(root / "codex" / "SKILL.md", base / "SKILL.md", report)
    copy_template_file(root / "agents" / "openai.yaml", base / "agents" / "openai.yaml", report)
    copy_template_tree(root / "references", base / "references", report)
    copy_template_tree(root / "scripts", base / "scripts", report)


def install_claude(root, destination: Path, project: bool, report: InstallReport) -> None:
    base = destination / ".claude" / "skills" / SKILL_NAME if project else destination / ".claude" / "skills" / SKILL_NAME
    copy_template_file(root / "claude" / "SKILL.md", base / "SKILL.md", report)
    copy_template_tree(root / "references", base / "references", report)
    copy_template_tree(root / "scripts", base / "scripts", report)


def install_copilot(root, destination: Path, project: bool, report: InstallReport) -> None:
    if not project:
        report.warnings.append("GitHub Copilot instructions are repository-scoped; rerun with --project.")
        return
    copy_template_file(root / "AGENTS.md", destination / "AGENTS.md", report)
    copy_template_file(
        root / "github" / "copilot-instructions.md",
        destination / ".github" / "copilot-instructions.md",
        report,
    )
    copy_template_file(
        root / "github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
        destination / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
        report,
    )


def copy_template_tree(source, target: Path, report: InstallReport) -> None:
    for child in source.iterdir():
        if child.name == "__pycache__" or child.name.endswith(".pyc"):
            continue
        child_target = target / child.name
        if child.is_dir():
            copy_template_tree(child, child_target, report)
        else:
            copy_template_file(child, child_target, report)


def copy_template_file(source, target: Path, report: InstallReport) -> None:
    content = source.read_bytes()
    generated = generated_bytes(content, target.suffix.lower())
    existed = target.exists()
    if existed and not is_managed_file(target):
        relative = display_path(target)
        report.skipped.append(relative)
        report.warnings.append(f"Skipped existing non-generated file: {relative}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(generated)
    if existed:
        report.updated.append(display_path(target))
    else:
        report.installed.append(display_path(target))


def generated_bytes(content: bytes, suffix: str) -> bytes:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return content
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    marked = add_marker(text, suffix)
    return marked.encode("utf-8")


def add_marker(text: str, suffix: str) -> str:
    if GENERATED_MARKER in text:
        return ensure_final_newline(text)
    marker = marker_for_suffix(suffix)
    if not marker:
        return ensure_final_newline(text)
    if suffix == ".md" and text.startswith("---\n"):
        lines = text.splitlines()
        try:
            end = lines[1:].index("---") + 1
        except ValueError:
            return ensure_final_newline(f"{marker}\n{text}")
        lines.insert(end + 1, "")
        lines.insert(end + 2, marker)
        return ensure_final_newline("\n".join(lines))
    if suffix == ".py" and text.startswith("#!"):
        first, _, rest = text.partition("\n")
        return ensure_final_newline(f"{first}\n{marker}\n{rest}")
    return ensure_final_newline(f"{marker}\n{text}")


def marker_for_suffix(suffix: str) -> str:
    if suffix == ".md":
        return MARKER_MD
    if suffix in {".yaml", ".yml", ".py", ".toml", ".txt"}:
        return MARKER_COMMENT
    return ""


def ensure_final_newline(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def is_managed_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return GENERATED_MARKER in text


def write_manifest(
    destination: Path,
    platforms: Iterable[str],
    project: bool,
    report: InstallReport,
) -> None:
    if report.errors:
        return
    manifest = {
        "name": SKILL_NAME,
        "version": __version__,
        "project": project,
        "platforms": list(platforms),
        "installed": report.installed,
        "updated": report.updated,
        "skipped": report.skipped,
    }
    target = destination / MANIFEST_NAME
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def display_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def user_destination() -> Path:
    return Path.home()


def project_destination() -> Path:
    return Path.cwd()


def remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
