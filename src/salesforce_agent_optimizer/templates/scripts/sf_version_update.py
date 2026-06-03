#!/usr/bin/env python3
"""Update Salesforce release/API version context resources for the skill."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_ROLLOUT_NOTE = (
    "Confirm the target org release before changing project sourceApiVersion because "
    "Salesforce releases roll out by org and instance."
)
DEFAULT_PACKAGE_POLICY = (
    "Do not assume managed package versions from public docs. Inspect installed packages "
    "in the target org and use official package release notes only when available."
)
DEFAULT_SOAP_LOGIN_POLICY = (
    "SOAP API login() is unavailable in API versions 65.0 and later. Salesforce has "
    "announced retirement for login() in SOAP API versions 31.0 through 64.0 with Summer '27."
)


def parse_source(value: str) -> dict[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Sources must use Label=https://example format")
    label, url = value.split("=", 1)
    label = label.strip()
    url = url.strip()
    if not label or not url.startswith("https://"):
        raise argparse.ArgumentTypeError("Source label is required and URL must start with https://")
    return {"label": label, "url": url}


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def render_markdown(payload: dict[str, object], functional_notes: list[str], package_notes: list[str]) -> str:
    sources = payload.get("sources", [])
    lines = [
        "# Salesforce Current Version Context",
        "",
        f"Last verified: {payload['last_verified_date']}",
        "",
        "## Current Production Reference",
        "",
        f"- Current Salesforce release reference: {payload['current_release']}.",
        f"- Current Salesforce Platform API version: {payload['current_platform_api_version']}.",
        f"- Current Metadata API version for new manifests when no project version exists: {payload['current_metadata_api_version']}.",
        f"- Current SOAP API version reference: {payload['current_soap_api_version']}.",
        "",
        str(payload["production_rollout_note"]),
        "",
        "## SOAP API Guardrails",
        "",
        f"- {payload['soap_login_policy']}",
        "- Do not design new authentication around SOAP `login()`.",
        "- Prefer OAuth, External Client Apps, JWT bearer, named credentials, or other current Salesforce-supported auth patterns.",
        "",
        "## Project API Version Rules",
        "",
        "- Read `sfdx-project.json` first. Preserve the existing `sourceApiVersion` unless the task explicitly requires an upgrade or the user approves one.",
        "- Use the current API version for new sample manifests only when the project has no version.",
        "- Upgrading API versions can change runtime or compile behavior for Apex, LWC, Flow, metadata deployments, integrations, and security defaults. Plan and test it as a change, not as formatting.",
        "- For LWC, Salesforce validates `apiVersion` and the latest valid API version is the current Salesforce release. Update component API versions when modifying components and after compatibility checks.",
        "",
        "## Managed Package Version Rules",
        "",
        str(payload["package_version_policy"]),
        "",
        "Before package-specific planning, ask for the org alias when package evidence is needed and run:",
        "",
        "```bash",
        "python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result",
        "```",
        "",
        "Record package name, namespace, installed version name/number, subscriber package version id when available, target org, and verification date in the plan or Knowledge. Use official package release notes only when they exist and are clearly tied to the installed version.",
    ]

    if functional_notes:
        lines.extend(["", "## Release-Sensitive Functional Notes", ""])
        lines.extend(f"- {note}" for note in functional_notes)

    if package_notes:
        lines.extend(["", "## Package Notes", ""])
        lines.extend(f"- {note}" for note in package_notes)

    lines.extend(["", "## Sources", ""])
    for source in sources:
        if isinstance(source, dict):
            lines.append(f"- {source.get('label')}: {source.get('url')}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Salesforce current version JSON and Markdown resources.")
    parser.add_argument("--skill-root", default=".", help="Skill repository root.")
    parser.add_argument("--verified-date", required=True, help="Verification date in yyyy-mm-dd format.")
    parser.add_argument("--release-name", required=True, help="Current Salesforce release name, for example Summer '26.")
    parser.add_argument("--api-version", required=True, help="Current Salesforce Platform API version, for example 67.0.")
    parser.add_argument("--metadata-api-version", help="Current Metadata API version. Defaults to --api-version.")
    parser.add_argument("--soap-api-version", help="Current SOAP API version. Defaults to --api-version.")
    parser.add_argument("--rollout-note", default=DEFAULT_ROLLOUT_NOTE)
    parser.add_argument("--package-policy", default=DEFAULT_PACKAGE_POLICY)
    parser.add_argument("--soap-login-policy", default=DEFAULT_SOAP_LOGIN_POLICY)
    parser.add_argument("--source", action="append", type=parse_source, default=[], help="Official source as Label=https://url.")
    parser.add_argument("--functional-note", action="append", default=[], help="Version-sensitive functional note for Markdown.")
    parser.add_argument("--package-note", action="append", default=[], help="Package-specific version note for Markdown.")
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve()
    references = skill_root / "references"
    payload: dict[str, object] = {
        "last_verified_date": args.verified_date,
        "current_release": args.release_name,
        "current_platform_api_version": args.api_version,
        "current_metadata_api_version": args.metadata_api_version or args.api_version,
        "current_soap_api_version": args.soap_api_version or args.api_version,
        "production_rollout_note": args.rollout_note,
        "package_version_policy": args.package_policy,
        "soap_login_policy": args.soap_login_policy,
        "sources": args.source,
    }

    write_json(references / "salesforce-version.json", payload)
    (references / "salesforce-current-version.md").write_text(
        render_markdown(payload, args.functional_note, args.package_note),
        encoding="utf-8",
    )
    print(str(references / "salesforce-version.json"))
    print(str(references / "salesforce-current-version.md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
