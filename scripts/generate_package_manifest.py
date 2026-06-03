#!/usr/bin/env python3
"""Generate a compact Salesforce Metadata API package.xml for changed metadata."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path.cwd()
PACKAGE_XMLNS = "http://soap.sforce.com/2006/04/metadata"

FOLDER_TYPES: dict[str, tuple[str, str]] = {
    "applications": ("CustomApplication", ".app-meta.xml"),
    "approvalProcesses": ("ApprovalProcess", ".approvalProcess-meta.xml"),
    "assignmentRules": ("AssignmentRules", ".assignmentRules-meta.xml"),
    "aura": ("AuraDefinitionBundle", ""),
    "classes": ("ApexClass", ".cls"),
    "connectedApps": ("ConnectedApp", ".connectedApp-meta.xml"),
    "contentassets": ("ContentAsset", ".asset-meta.xml"),
    "customMetadata": ("CustomMetadata", ".md-meta.xml"),
    "customPermissions": ("CustomPermission", ".customPermission-meta.xml"),
    "dashboards": ("Dashboard", ".dashboard-meta.xml"),
    "duplicateRules": ("DuplicateRule", ".duplicateRule-meta.xml"),
    "email": ("EmailTemplate", ".email-meta.xml"),
    "escalationRules": ("EscalationRules", ".escalationRules-meta.xml"),
    "externalCredentials": ("ExternalCredential", ".externalCredential-meta.xml"),
    "flexipages": ("FlexiPage", ".flexipage-meta.xml"),
    "flowDefinitions": ("FlowDefinition", ".flowDefinition-meta.xml"),
    "flowTests": ("FlowTest", ".flowTest-meta.xml"),
    "flows": ("Flow", ".flow-meta.xml"),
    "globalValueSets": ("GlobalValueSet", ".globalValueSet-meta.xml"),
    "groups": ("Group", ".group-meta.xml"),
    "homePageComponents": ("HomePageComponent", ".homePageComponent-meta.xml"),
    "homePageLayouts": ("HomePageLayout", ".homePageLayout-meta.xml"),
    "labels": ("CustomLabels", ".labels-meta.xml"),
    "layouts": ("Layout", ".layout-meta.xml"),
    "lwc": ("LightningComponentBundle", ""),
    "matchingRules": ("MatchingRules", ".matchingRule-meta.xml"),
    "namedCredentials": ("NamedCredential", ".namedCredential-meta.xml"),
    "notificationtypes": ("CustomNotificationType", ".notiftype-meta.xml"),
    "objectTranslations": ("CustomObjectTranslation", ".objectTranslation-meta.xml"),
    "pages": ("ApexPage", ".page"),
    "pathAssistants": ("PathAssistant", ".pathAssistant-meta.xml"),
    "permissionsetgroups": ("PermissionSetGroup", ".permissionsetgroup-meta.xml"),
    "permissionsets": ("PermissionSet", ".permissionset-meta.xml"),
    "profiles": ("Profile", ".profile-meta.xml"),
    "queues": ("Queue", ".queue-meta.xml"),
    "quickActions": ("QuickAction", ".quickAction-meta.xml"),
    "remoteSiteSettings": ("RemoteSiteSetting", ".remoteSite-meta.xml"),
    "reports": ("Report", ".report-meta.xml"),
    "roles": ("Role", ".role-meta.xml"),
    "sharingRules": ("SharingRules", ".sharingRules-meta.xml"),
    "standardValueSets": ("StandardValueSet", ".standardValueSet-meta.xml"),
    "staticresources": ("StaticResource", ".resource-meta.xml"),
    "tabs": ("CustomTab", ".tab-meta.xml"),
    "triggers": ("ApexTrigger", ".trigger"),
    "workflows": ("Workflow", ".workflow-meta.xml"),
}

OBJECT_CHILD_TYPES: dict[str, tuple[str, str]] = {
    "businessProcesses": ("BusinessProcess", ".businessProcess-meta.xml"),
    "compactLayouts": ("CompactLayout", ".compactLayout-meta.xml"),
    "fieldSets": ("FieldSet", ".fieldSet-meta.xml"),
    "fields": ("CustomField", ".field-meta.xml"),
    "listViews": ("ListView", ".listView-meta.xml"),
    "recordTypes": ("RecordType", ".recordType-meta.xml"),
    "sharingReasons": ("SharingReason", ".sharingReason-meta.xml"),
    "validationRules": ("ValidationRule", ".validationRule-meta.xml"),
    "webLinks": ("WebLink", ".webLink-meta.xml"),
}


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True)


def strip_suffix(name: str, suffix: str) -> str:
    return name[: -len(suffix)] if suffix and name.endswith(suffix) else name


def strip_source_suffix(file_name: str, suffix: str) -> str | None:
    if not suffix:
        return file_name
    candidates = [suffix]
    if not suffix.endswith("-meta.xml"):
        candidates.insert(0, f"{suffix}-meta.xml")
    for candidate in candidates:
        if file_name.endswith(candidate):
            return strip_suffix(file_name, candidate)
    return None


def source_api_version(project_root: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    config = project_root / "sfdx-project.json"
    if config.exists():
        try:
            value = json.loads(config.read_text(encoding="utf-8")).get("sourceApiVersion")
            if value:
                return str(value)
        except json.JSONDecodeError:
            pass
    return "64.0"


def git_status_paths(project_root: Path) -> list[str]:
    completed = run_git(["status", "--porcelain=v1", "--untracked-files=all"], project_root)
    if completed.returncode != 0:
        return []
    paths: list[str] = []
    for line in completed.stdout.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        if "D" in status:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path.strip('"'))
    return paths


def git_ref_paths(project_root: Path, ref: str) -> list[str]:
    completed = run_git(["diff", "--name-status", "--diff-filter=AMRT", ref, "--"], project_root)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or f"git diff failed for {ref}")
    paths: list[str] = []
    for line in completed.stdout.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0]
        if status.startswith("R") or status.startswith("C"):
            paths.append(parts[-1])
        elif len(parts) > 1:
            paths.append(parts[1])
    return paths


def metadata_from_entry(entry: str) -> tuple[str, str]:
    if ":" not in entry:
        raise ValueError(f"Metadata must use Type:Member format: {entry}")
    metadata_type, member = entry.split(":", 1)
    if not metadata_type or not member:
        raise ValueError(f"Metadata must use Type:Member format: {entry}")
    return metadata_type, member


def metadata_from_source_path(path: str) -> tuple[str, str] | None:
    normalized = Path(path.replace("\\", "/"))
    parts = normalized.parts
    if not parts:
        return None

    if "objects" in parts:
        object_index = parts.index("objects")
        if len(parts) <= object_index + 1:
            return None
        object_name = parts[object_index + 1]
        file_name = parts[-1]
        if len(parts) > object_index + 2 and parts[object_index + 2] in OBJECT_CHILD_TYPES:
            child_folder = parts[object_index + 2]
            metadata_type, suffix = OBJECT_CHILD_TYPES[child_folder]
            member = strip_suffix(file_name, suffix)
            return metadata_type, f"{object_name}.{member}"
        if file_name == f"{object_name}.object-meta.xml":
            return "CustomObject", object_name
        return None

    for index, part in enumerate(parts):
        if part not in FOLDER_TYPES:
            continue
        metadata_type, suffix = FOLDER_TYPES[part]
        if part in {"aura", "lwc"} and len(parts) > index + 1:
            return metadata_type, parts[index + 1]
        if part in {"dashboards", "documents", "email", "reports"}:
            relative = "/".join(parts[index + 1 :])
            member = strip_source_suffix(relative, suffix)
            if member is None:
                return None
            return metadata_type, member
        file_name = parts[-1]
        member = strip_source_suffix(file_name, suffix)
        if member is None:
            if part == "staticresources" and file_name.endswith(".resource"):
                return metadata_type, strip_suffix(file_name, ".resource")
            return None
        return metadata_type, member
    return None


def collect_metadata(args: argparse.Namespace, project_root: Path) -> tuple[dict[str, set[str]], list[str]]:
    metadata: dict[str, set[str]] = defaultdict(set)
    unresolved: list[str] = []

    for entry in args.metadata:
        metadata_type, member = metadata_from_entry(entry)
        metadata[metadata_type].add(member)

    changed_paths = list(args.changed_file)
    if args.git_ref:
        changed_paths.extend(git_ref_paths(project_root, args.git_ref))
    if args.from_git_status or not (args.metadata or args.changed_file or args.git_ref):
        changed_paths.extend(git_status_paths(project_root))

    for changed_path in sorted(set(changed_paths)):
        resolved = metadata_from_source_path(changed_path)
        if resolved:
            metadata[resolved[0]].add(resolved[1])
        elif any(segment in Path(changed_path.replace("\\", "/")).parts for segment in (set(FOLDER_TYPES) | {"objects"})):
            unresolved.append(changed_path)

    return metadata, unresolved


def render_package_xml(metadata: dict[str, set[str]], api_version: str) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', f'<Package xmlns="{PACKAGE_XMLNS}">']
    for metadata_type in sorted(metadata):
        members = sorted(member for member in metadata[metadata_type] if member)
        if not members:
            continue
        lines.append("    <types>")
        for member in members:
            lines.append(f"        <members>{escape(member)}</members>")
        lines.append(f"        <name>{escape(metadata_type)}</name>")
        lines.append("    </types>")
    lines.append(f"    <version>{escape(api_version)}</version>")
    lines.append("</Package>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate package.xml for added or modified Salesforce metadata.")
    parser.add_argument("--project-root", default=".", help="Salesforce project root. Defaults to current directory.")
    parser.add_argument("--output", default="release-artifacts/package.xml", help="Output package.xml path.")
    parser.add_argument("--api-version", help="Metadata API version. Defaults to sfdx-project.json sourceApiVersion or 64.0.")
    parser.add_argument("--metadata", action="append", default=[], help="Explicit metadata entry in Type:Member format.")
    parser.add_argument("--changed-file", action="append", default=[], help="Changed source path to include.")
    parser.add_argument("--git-ref", help="Include added/modified/renamed paths changed since this git ref.")
    parser.add_argument("--from-git-status", action="store_true", help="Include added/modified/renamed/untracked paths from git status.")
    parser.add_argument("--allow-unresolved", action="store_true", help="Warn instead of failing on unresolved metadata-looking paths.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    metadata, unresolved = collect_metadata(args, project_root)
    if unresolved and not args.allow_unresolved:
        for path in unresolved:
            print(f"Unresolved metadata path: {path}", file=sys.stderr)
        return 2
    if not metadata:
        print("No added or modified metadata found. Provide --metadata, --changed-file, --git-ref, or --from-git-status.", file=sys.stderr)
        return 1

    package_xml = render_package_xml(metadata, source_api_version(project_root, args.api_version))
    output = Path(args.output)
    if not output.is_absolute():
        output = project_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(package_xml, encoding="utf-8")
    print(str(output))
    if unresolved:
        print(json.dumps({"warnings": unresolved}, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
