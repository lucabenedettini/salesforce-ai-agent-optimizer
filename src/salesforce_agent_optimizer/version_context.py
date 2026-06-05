"""Salesforce release and API version-context maintenance."""

from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


OFFICIAL_DOMAINS = {
    "developer.salesforce.com",
    "help.salesforce.com",
    "architect.salesforce.com",
}
DEFAULT_CONTEXT: dict[str, Any] = {
    "last_verified_date": date.today().isoformat(),
    "current_release": "Summer '26",
    "current_platform_api_version": "67.0",
    "current_metadata_api_version": "67.0",
    "current_soap_api_version": "67.0",
    "production_rollout_note": (
        "Confirm the target org release before changing project sourceApiVersion because "
        "Salesforce releases roll out by org and instance."
    ),
    "package_version_policy": (
        "Do not assume managed package versions from public docs. Inspect installed packages "
        "in the target org and use official package release notes only when available."
    ),
    "soap_login_policy": (
        "SOAP API login() is unavailable in API versions 65.0 and later. Salesforce has "
        "announced retirement for login() in SOAP API versions 31.0 through 64.0 with Summer '27."
    ),
    "sources": [
        {
            "label": "Salesforce Release Notes",
            "url": "https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5",
        },
        {
            "label": "Salesforce API Release Notes",
            "url": "https://help.salesforce.com/s/articleView?id=release-notes.rn_api.htm&language=en_US&type=5",
        },
        {
            "label": "Salesforce SOAP API Release Notes",
            "url": "https://help.salesforce.com/s/articleView?id=release-notes.rn_api_soap.htm&language=en_US&type=5",
        },
        {
            "label": "Salesforce API and Data Loader versions",
            "url": "https://help.salesforce.com/s/articleView?id=000349115&language=en_US&type=1",
        },
        {
            "label": "LWC component versioning",
            "url": "https://developer.salesforce.com/docs/platform/lwc/guide/create-version-components.html",
        },
        {
            "label": "Metadata Coverage Report",
            "url": "https://developer.salesforce.com/docs/metadata-coverage",
        },
    ],
}
ProgressCallback = Callable[[str], None]


@dataclass
class VersionContextReport:
    action: str
    root: str
    changed: list[str] = field(default_factory=list)
    checked_sources: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "action": self.action,
            "root": self.root,
            "changed": self.changed,
            "checked_sources": self.checked_sources,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def progress_line(progress: ProgressCallback | None, message: str) -> None:
    if progress:
        progress(f"sfao version-context: {message}")


def references_dir(root: Path) -> Path:
    return root / "references"


def version_json_path(root: Path) -> Path:
    return references_dir(root) / "salesforce-version.json"


def current_version_md_path(root: Path) -> Path:
    return references_dir(root) / "salesforce-current-version.md"


def official_sources_path(root: Path) -> Path:
    return references_dir(root) / "official-salesforce-sources.md"


def load_context(root: Path) -> dict[str, Any]:
    path = version_json_path(root)
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                merged = DEFAULT_CONTEXT | payload
                merged["last_verified_date"] = date.today().isoformat()
                return merged
        except json.JSONDecodeError:
            return DEFAULT_CONTEXT
    return DEFAULT_CONTEXT


def write_if_changed(path: Path, text: str, changed: list[str], root: Path) -> None:
    text = text.rstrip() + "\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    changed.append(path.relative_to(root).as_posix())


def render_current_version(payload: dict[str, Any], source_status: list[str]) -> str:
    lines = [
        "# Salesforce Current Version Context",
        "",
        f"Last verified: {payload['last_verified_date']}",
        "",
        "## Current Production Reference",
        "",
        f"- Current Salesforce release reference: {payload['current_release']}.",
        f"- Current Salesforce Platform API version: {payload['current_platform_api_version']}.",
        f"- Current Metadata API version: {payload['current_metadata_api_version']}.",
        f"- Current SOAP API version: {payload['current_soap_api_version']}.",
        "",
        str(payload["production_rollout_note"]),
        "",
        "## SOAP API Guardrails",
        "",
        f"- {payload['soap_login_policy']}",
        "- Prefer OAuth, External Client Apps, JWT bearer, named credentials, or current Salesforce-supported auth patterns.",
        "",
        "## Project API Version Rules",
        "",
        "- Read `sfdx-project.json` first and preserve `sourceApiVersion` unless the user approves an upgrade.",
        "- Treat API upgrades as functional changes requiring planning and tests.",
        "- For LWC, update component `apiVersion` only after compatibility checks.",
        "",
        "## Managed Package Version Rules",
        "",
        str(payload["package_version_policy"]),
        "",
        "## Official Source Check Summary",
        "",
    ]
    lines.extend(f"- {item}" for item in source_status)
    lines.extend(["", "## Sources", ""])
    for source in payload.get("sources", []):
        if isinstance(source, dict):
            lines.append(f"- {source.get('label')}: {source.get('url')}")
    return "\n".join(lines)


def render_official_sources(payload: dict[str, Any]) -> str:
    lines = [
        "# Official Salesforce Sources",
        "",
        "Use only official Salesforce sources for release-sensitive version context. "
        "Prefer concise summaries and links over copied release-note text.",
        "",
    ]
    for source in payload.get("sources", []):
        if isinstance(source, dict):
            lines.append(f"- {source.get('label')}: {source.get('url')}")
    lines.extend(
        [
            "- Salesforce CLI command reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm",
            "- Salesforce Well-Architected: https://architect.salesforce.com/docs/architect/well-architected/guide/overview.html",
            "",
        ]
    )
    return "\n".join(lines)


def verify_official_sources(
    payload: dict[str, Any],
    timeout: int = 8,
    progress: ProgressCallback | None = None,
) -> tuple[list[str], list[str]]:
    checked: list[str] = []
    warnings: list[str] = []
    sources = [source for source in payload.get("sources", []) if isinstance(source, dict)]
    total = len(sources)
    progress_line(progress, f"checking official sources 0/{total} (0%)")
    for index, source in enumerate(sources, start=1):
        url = str(source.get("url", ""))
        host = urlparse(url).netloc.lower()
        if host not in OFFICIAL_DOMAINS:
            warnings.append(f"Skipped non-official source host: {url}")
            progress_line(progress, f"checking official sources {index}/{total}")
            continue
        try:
            progress_line(progress, f"checking {source.get('label')} ({index}/{total})")
            request = urllib.request.Request(url, method="GET", headers={"User-Agent": "sfao/1.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                status = getattr(response, "status", 200)
                checked.append(f"{source.get('label')}: HTTP {status}")
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"Could not verify {source.get('label')}: {exc}")
        percent = round(index * 100 / total) if total else 100
        progress_line(progress, f"checking official sources {index}/{total} ({percent}%)")
    return checked, warnings


def scaffold(root: Path, progress: ProgressCallback | None = None) -> VersionContextReport:
    root = root.resolve()
    report = VersionContextReport(action="scaffold", root=str(root))
    progress_line(progress, f"scaffold started for {root}")
    progress_line(progress, "loading version context")
    payload = load_context(root)
    if not version_json_path(root).exists():
        progress_line(progress, "writing references/salesforce-version.json")
        write_if_changed(
            version_json_path(root),
            json.dumps(payload, indent=2, sort_keys=False),
            report.changed,
            root,
        )
    if not current_version_md_path(root).exists():
        progress_line(progress, "writing references/salesforce-current-version.md")
        write_if_changed(current_version_md_path(root), render_current_version(payload, []), report.changed, root)
    if not official_sources_path(root).exists():
        progress_line(progress, "writing references/official-salesforce-sources.md")
        write_if_changed(official_sources_path(root), render_official_sources(payload), report.changed, root)
    progress_line(progress, "done")
    return report


def update(
    root: Path,
    offline: bool = False,
    progress: ProgressCallback | None = None,
) -> VersionContextReport:
    root = root.resolve()
    report = VersionContextReport(action="update", root=str(root))
    progress_line(progress, f"update started for {root}")
    progress_line(progress, "loading version context")
    payload = load_context(root)
    source_status: list[str] = []
    if offline:
        report.warnings.append("Offline update used existing official-source metadata.")
        progress_line(progress, "offline mode: skipping network checks")
    else:
        checked, warnings = verify_official_sources(payload, progress=progress)
        report.checked_sources = checked
        report.warnings.extend(warnings)
        source_status = checked or ["Official source links configured; no source returned content."]
    progress_line(progress, "writing references/salesforce-version.json")
    write_if_changed(
        version_json_path(root),
        json.dumps(payload, indent=2, sort_keys=False),
        report.changed,
        root,
    )
    progress_line(progress, "writing references/salesforce-current-version.md")
    write_if_changed(
        current_version_md_path(root),
        render_current_version(payload, source_status),
        report.changed,
        root,
    )
    progress_line(progress, "writing references/official-salesforce-sources.md")
    write_if_changed(official_sources_path(root), render_official_sources(payload), report.changed, root)
    progress_line(progress, "done")
    return report


def validate(root: Path, progress: ProgressCallback | None = None) -> VersionContextReport:
    root = root.resolve()
    report = VersionContextReport(action="validate", root=str(root))
    progress_line(progress, f"validate started for {root}")
    for path in (version_json_path(root), current_version_md_path(root), official_sources_path(root)):
        progress_line(progress, f"checking {path.relative_to(root).as_posix()}")
        if not path.exists():
            report.errors.append(f"Missing version-context file: {path.relative_to(root).as_posix()}")
    if report.errors:
        return report
    try:
        payload = json.loads(version_json_path(root).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.errors.append(f"Invalid references/salesforce-version.json: {exc}")
        return report
    for key in (
        "last_verified_date",
        "current_release",
        "current_platform_api_version",
        "current_metadata_api_version",
        "current_soap_api_version",
        "sources",
    ):
        if key not in payload:
            report.errors.append(f"Missing version-context key: {key}")
    for key in (
        "current_platform_api_version",
        "current_metadata_api_version",
        "current_soap_api_version",
    ):
        if not re.fullmatch(r"\d+\.\d+", str(payload.get(key, ""))):
            report.errors.append(f"Invalid API version value for {key}")
    for source in payload.get("sources", []):
        if not isinstance(source, dict):
            report.errors.append("Version-context source must be an object")
            continue
        url = str(source.get("url", ""))
        if urlparse(url).netloc.lower() not in OFFICIAL_DOMAINS:
            report.errors.append(f"Non-official version-context source: {url}")
    return report


def format_report(report: VersionContextReport, verbose: bool = False) -> str:
    status = "OK" if report.ok else "ERROR"
    lines = [f"Salesforce Version Context: {status}", f"- action: {report.action}"]
    if report.changed:
        lines.append(f"- changed: {len(report.changed)}")
    if report.checked_sources:
        lines.append(f"- official sources checked: {len(report.checked_sources)}")
    for warning in report.warnings:
        lines.append(f"WARN: {warning}")
    for error in report.errors:
        lines.append(f"ERROR: {error}")
    if verbose:
        if report.changed:
            lines.append("Changed files:")
            lines.extend(f"- {item}" for item in report.changed)
        if report.checked_sources:
            lines.append("Checked official sources:")
            lines.extend(f"- {item}" for item in report.checked_sources)
    return "\n".join(lines) + "\n"
