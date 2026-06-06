#!/usr/bin/env python3
"""Agent-native Salesforce CLI facade with compact output and production guardrails."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_KEYS = re.compile(
    r"(access.?token|session.?id|auth.?url|refresh.?token|client.?secret|consumer.?secret|password|cookie|sid|installation.?key|private.?key)",
    re.IGNORECASE,
)
SENSITIVE_VALUE_FLAGS = {
    "--access-token",
    "--auth-url",
    "--client-secret",
    "--consumer-secret",
    "--jwt-key-file",
    "--password",
    "--private-key",
    "--sfdx-url",
}

PROD_CHECK_QUERY = "SELECT IsSandbox, OrganizationType, Name FROM Organization LIMIT 1"
KNOWLEDGE_DIR = ".salesforce-agent-knowledge"
DELETE_APPROVAL_PHRASE = "I explicitly approve this deletion"
SECRET_APPROVAL_PHRASE = "I explicitly approve exposing Salesforce secrets"


@dataclass(frozen=True)
class CommandDoc:
    name: str
    safety: str
    description: str
    maps_to: str
    requires_alias: bool


COMMANDS: list[CommandDoc] = [
    CommandDoc("auth-web", "auth", "Interactive OAuth login with browser/device protection. Use for humans.", "sf org login web", False),
    CommandDoc("auth-device", "auth", "Device-code OAuth login when browser login is not practical.", "sf org login device", False),
    CommandDoc("auth-jwt", "auth", "JWT bearer login for CI/automation with connected app and private key.", "sf org login jwt", False),
    CommandDoc("org-list", "read", "List locally authenticated orgs without using a default org for work.", "sf org list", False),
    CommandDoc("org-inspect", "read", "Display compact org identity and sandbox/production status.", "sf org display + data query Organization", True),
    CommandDoc("org-limits", "read", "Read API/org limits for the target org.", "sf limits api display", True),
    CommandDoc("schema-sobject-list", "read", "List available sObjects with optional category.", "sf sobject list", True),
    CommandDoc("schema-sobject-describe", "read", "Describe one sObject compactly.", "sf sobject describe", True),
    CommandDoc("metadata-list", "read", "List metadata members for one metadata type.", "sf org list metadata", True),
    CommandDoc("metadata-retrieve", "read", "Retrieve named metadata such as ApexClass:MyClass.", "sf project retrieve start --metadata", True),
    CommandDoc("metadata-retrieve-manifest", "read", "Retrieve metadata from a package.xml manifest.", "sf project retrieve start --manifest", True),
    CommandDoc("deploy-preview", "read", "Preview a deploy without changing the org.", "sf project deploy preview", True),
    CommandDoc("deploy-validate", "execute", "Validate a deployment without committing metadata. Blocked on production.", "sf project deploy validate", True),
    CommandDoc("deploy-start", "write", "Deploy source metadata. Blocked on production.", "sf project deploy start", True),
    CommandDoc("deploy-report", "read", "Read deployment status by job id.", "sf project deploy report", True),
    CommandDoc("data-query", "read", "Run SOQL with explicit fields and compact JSON output.", "sf data query", True),
    CommandDoc("data-record-get", "read", "Read one record by sObject and record id.", "sf data get record", True),
    CommandDoc("data-record-create", "write", "Create one record. Blocked on production.", "sf data create record", True),
    CommandDoc("data-record-update", "write", "Update one record. Blocked on production.", "sf data update record", True),
    CommandDoc("data-record-delete", "write", "Delete one record. Blocked on production.", "sf data delete record", True),
    CommandDoc("access-inspect", "read", "Inspect current user access for least-privilege planning.", "sf data query User + PermissionSetAssignment + ObjectPermissions + FieldPermissions", True),
    CommandDoc("apex-test-run", "execute", "Run Apex tests. Blocked on production.", "sf apex run test", True),
    CommandDoc("apex-test-report", "read", "Read an Apex test run report.", "sf apex get test", True),
    CommandDoc("apex-log-list", "read", "List Apex debug logs.", "sf apex list log", True),
    CommandDoc("apex-log-get", "read", "Fetch one Apex debug log.", "sf apex get log", True),
    CommandDoc("apex-run", "execute", "Execute anonymous Apex from a file. Blocked on production.", "sf apex run", True),
    CommandDoc("package-installed-list", "read", "List installed packages.", "sf package installed list", True),
    CommandDoc("package-install", "write", "Install a package. Blocked on production.", "sf package install", True),
    CommandDoc("package-uninstall", "write", "Uninstall a package. Blocked on production.", "sf package uninstall", True),
    CommandDoc("user-display", "read", "Display user information.", "sf org display user", True),
    CommandDoc("permset-assign", "write", "Assign a permission set. Blocked on production.", "sf org assign permset", True),
    CommandDoc("local-manifest-generate", "local", "Generate a local package.xml manifest.", "sf project generate manifest", False),
    CommandDoc("safe-run", "dynamic", "Run any official sf command with compact output, alias enforcement, and production guardrails.", "sf <official-command>", False),
    CommandDoc("catalog-refresh", "local", "Generate compact documentation for all installed official sf commands.", "sf commands --json", False),
]
DOCS = {command.name: command for command in COMMANDS}

READ_VERBS = {
    "display",
    "describe",
    "get",
    "info",
    "list",
    "open",
    "preview",
    "query",
    "report",
    "resume",
    "status",
    "version",
}
WRITE_VERBS = {
    "activate",
    "assign",
    "clone",
    "create",
    "deactivate",
    "delete",
    "deploy",
    "disable",
    "enable",
    "install",
    "publish",
    "reset",
    "start",
    "unassign",
    "uninstall",
    "update",
    "upgrade",
    "upsert",
}
EXECUTE_VERBS = {"run", "test", "validate"}
LOCAL_PREFIXES = {"autocomplete", "commands", "completion", "config", "plugins", "schema", "version"}
AUTH_PARTS = {"auth", "login", "logout"}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if SECRET_KEYS.search(str(key)) else redact(inner)
            for key, inner in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, str):
        value = re.sub(r"00D[A-Za-z0-9]{12,}", "[REDACTED_ORG_ID]", value)
        value = re.sub(r"(?i)(sid|sessionId|access_token)=([^&\s]+)", r"\1=[REDACTED]", value)
        value = re.sub(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+", r"\1[REDACTED]", value)
        value = re.sub(r"(?i)(force://[^:\s]+:)[^@\s]+(@)", r"\1[REDACTED]\2", value)
    return value


def redact_cli_args(tokens: list[str]) -> list[str]:
    redacted: list[str] = []
    redact_next = False
    for token in tokens:
        if redact_next:
            redacted.append("[REDACTED]")
            redact_next = False
            continue
        if token in SENSITIVE_VALUE_FLAGS:
            redacted.append(token)
            redact_next = True
            continue
        matched = next((flag for flag in SENSITIVE_VALUE_FLAGS if token.startswith(f"{flag}=")), None)
        if matched:
            redacted.append(f"{matched}=[REDACTED]")
            continue
        redacted.append(str(redact(token)))
    return redacted


def compact(value: Any, max_list: int) -> Any:
    if isinstance(value, list):
        items = [compact(item, max_list) for item in value[:max_list]]
        if len(value) > max_list:
            items.append({"_truncated": len(value) - max_list})
        return items
    if isinstance(value, dict):
        return {key: compact(inner, max_list) for key, inner in value.items()}
    return value


def get_path(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def select_paths(payload: Any, selector: str | None) -> Any:
    if not selector:
        return payload
    return {path: get_path(payload, path) for path in [item.strip() for item in selector.split(",") if item.strip()]}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sf_binary() -> str:
    override = os.environ.get("SF_AGENT_SF_BIN")
    if override:
        return override
    if os.name == "nt":
        for name in ("sf.cmd", "sf.exe", "sf"):
            candidate = shutil.which(name)
            if candidate:
                return candidate
        appdata = os.environ.get("APPDATA")
        if appdata:
            npm_cmd = Path(appdata) / "npm" / "sf.cmd"
            try:
                exists = npm_cmd.exists()
            except OSError:
                exists = False
            if exists:
                return str(npm_cmd)
        return "sf.cmd"
    return shutil.which("sf") or "sf"


def sf_run(sf_args: list[str], args: argparse.Namespace, allow_non_json: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sf_binary(), *sf_args]
    if not allow_non_json and "--json" not in command:
        command.append("--json")
    if getattr(args, "dry_run", False):
        return subprocess.CompletedProcess(
            command,
            0,
            json.dumps({"dry_run": True, "sf_command": redact_cli_args(command)}),
            "",
        )
    try:
        return subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    except FileNotFoundError as exc:
        raise SystemExit("Salesforce CLI 'sf' was not found. Install the official Salesforce CLI before connecting to an org.") from exc


def emit_result(completed: subprocess.CompletedProcess[str], args: argparse.Namespace) -> int:
    output = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        payload = json.loads(output)
        payload = compact(redact(select_paths(payload, getattr(args, "select", None))), args.max_list)
        text = json.dumps(payload, indent=2, sort_keys=True)
    except json.JSONDecodeError:
        text = str(redact(output))
    if len(text) > args.max_chars:
        text = text[: args.max_chars] + f"\n... [truncated to {args.max_chars} chars]"
    print(text)
    return completed.returncode


def emit_payload(payload: Any, args: argparse.Namespace, returncode: int = 0) -> int:
    payload = compact(redact(select_paths(payload, getattr(args, "select", None))), args.max_list)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if len(text) > args.max_chars:
        text = text[: args.max_chars] + f"\n... [truncated to {args.max_chars} chars]"
    print(text)
    return returncode


def require_alias(args: argparse.Namespace) -> str:
    target_org = getattr(args, "target_org", None)
    if not target_org:
        raise SystemExit("Missing --target-org. Ask the user for the Salesforce org alias before connecting.")
    return target_org


def canonical_official_command_id(sf_args: list[str]) -> str:
    command_parts = []
    for token in sf_args:
        if token == "--":
            continue
        if token.startswith("-"):
            break
        command_parts.append(token)
    if len(command_parts) == 1 and ":" in command_parts[0]:
        return command_parts[0]
    return ":".join(command_parts)


def extract_flag_value(tokens: list[str], long_name: str, short_name: str | None = None) -> str | None:
    names = {long_name}
    if short_name:
        names.add(short_name)
    for index, token in enumerate(tokens):
        if token in names and index + 1 < len(tokens):
            return tokens[index + 1]
        for name in names:
            prefix = f"{name}="
            if token.startswith(prefix):
                return token[len(prefix) :]
    return None


def has_flag(tokens: list[str], long_name: str, short_name: str | None = None) -> bool:
    names = {long_name}
    if short_name:
        names.add(short_name)
    return any(token in names or any(token.startswith(f"{name}=") for name in names) for token in tokens)


def classify_official_safety(command_id: str, connects_to_org: bool = False) -> str:
    parts = [part for part in command_id.replace(" ", ":").split(":") if part]
    part_set = set(parts)
    if not parts:
        return "unknown"
    if parts[0] in LOCAL_PREFIXES:
        return "local"
    if part_set & AUTH_PARTS:
        return "auth"
    if "retrieve" in part_set:
        return "read"
    if "preview" in part_set or "report" in part_set:
        return "read"
    if {"deploy", "validate"}.issubset(part_set):
        return "execute"
    if "test" in part_set and "run" in part_set:
        return "execute"
    if "apex" in part_set and "run" in part_set:
        return "execute"
    if part_set & READ_VERBS:
        return "read"
    if part_set & WRITE_VERBS:
        return "write"
    if part_set & EXECUTE_VERBS:
        return "execute"
    if "generate" in part_set:
        return "execute" if connects_to_org else "local"
    return "read"


def is_destructive_operation(command_id: str, sf_args: list[str]) -> bool:
    normalized = command_id.replace(" ", ":").replace("-", ":")
    parts = [part for part in normalized.split(":") if part]
    if parts and parts[-1] in {"report", "list", "get", "display", "preview", "status"}:
        return False
    destructive_terms = {"delete", "uninstall", "purge", "truncate", "hard-delete", "harddelete"}
    if set(parts) & destructive_terms:
        return True
    lowered = " ".join(sf_args).lower()
    return any(term in lowered for term in ("destructivechanges", "destructive changes", "purge-on-delete", "hard-delete"))


def is_secret_exposure_operation(command_id: str, sf_args: list[str]) -> bool:
    normalized = command_id.replace(" ", ":").replace("-", ":")
    parts = {part for part in normalized.split(":") if part}
    lowered = " ".join(sf_args).lower()
    if {"auth", "show", "access", "token"} <= parts:
        return True
    if {"login", "access", "token"} <= parts:
        return True
    if "sfdx-url" in lowered or "auth-url" in lowered or "access-token" in lowered:
        return True
    if ("org:display" in command_id or "force:org:display" in command_id) and has_flag(sf_args, "--verbose"):
        return True
    return any(token in SENSITIVE_VALUE_FLAGS for token in sf_args)


def require_delete_approval(operation: str, args: argparse.Namespace, sf_args: list[str] | None = None) -> None:
    if not is_destructive_operation(operation, sf_args or []):
        return
    approval = getattr(args, "delete_approval", None)
    if approval != DELETE_APPROVAL_PHRASE:
        raise SystemExit(
            "Blocked destructive operation. Ask the user for explicit approval before deleting data or metadata, "
            f"then pass --delete-approval \"{DELETE_APPROVAL_PHRASE}\"."
        )


def require_secret_approval(operation: str, args: argparse.Namespace, sf_args: list[str] | None = None) -> None:
    if not is_secret_exposure_operation(operation, sf_args or []):
        return
    approval = getattr(args, "secret_approval", None)
    if approval != SECRET_APPROVAL_PHRASE:
        raise SystemExit(
            "Blocked secret-exposure operation. Inform the user that the command can expose or handle "
            "Salesforce credentials, access tokens, auth URLs, private keys, or session material. "
            f"Run it only after explicit approval with --secret-approval \"{SECRET_APPROVAL_PHRASE}\"."
        )


def command_likely_connects(command_id: str, sf_args: list[str], target_org: str | None) -> bool:
    if target_org:
        return True
    parts = set(command_id.split(":"))
    if parts & {"data", "metadata", "org", "package", "apex", "agent", "limits", "sobject"}:
        return True
    return has_flag(sf_args, "--target-org", "-o") or has_flag(sf_args, "--target-dev-hub", "-v")


def detect_is_scratch_or_sandbox_from_org_list(target_org: str, args: argparse.Namespace) -> bool | None:
    completed = sf_run(["org", "list"], args)
    if completed.returncode != 0:
        return None
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    result = payload.get("result", {})
    buckets = ("scratchOrgs", "sandboxes", "nonScratchOrgs", "other")
    for bucket in buckets:
        orgs = result.get(bucket, [])
        if not isinstance(orgs, list):
            continue
        for org in orgs:
            if not isinstance(org, dict):
                continue
            identifiers = {str(org.get("alias") or ""), str(org.get("username") or ""), str(org.get("orgId") or "")}
            if target_org in identifiers:
                if org.get("isScratch") is True or bucket == "scratchOrgs":
                    return True
                if org.get("isSandbox") is True or bucket == "sandboxes":
                    return True
                if org.get("isSandbox") is False:
                    return False
    return None


def detect_is_non_production(target_org: str, args: argparse.Namespace) -> bool:
    local_status = detect_is_scratch_or_sandbox_from_org_list(target_org, args)
    if local_status is not None:
        return local_status
    check_args = ["data", "query", "--target-org", target_org, "--query", PROD_CHECK_QUERY]
    completed = sf_run(check_args, args)
    if completed.returncode != 0:
        raise SystemExit(
            "Cannot determine whether the target org is production. "
            "Write/execute operations are blocked until Organization.IsSandbox can be read."
        )
    payload = json.loads(completed.stdout)
    records = payload.get("result", {}).get("records", [])
    if not records:
        raise SystemExit("Cannot determine org type from Organization query. Write/execute operation blocked.")
    return bool(records[0].get("IsSandbox"))


def enforce_safety(command_name: str, args: argparse.Namespace) -> None:
    doc = DOCS[command_name]
    if doc.requires_alias:
        require_alias(args)
    if doc.safety not in {"write", "execute"}:
        return
    target_org = require_alias(args)
    if getattr(args, "dry_run", False):
        return
    if not detect_is_non_production(target_org, args):
        raise SystemExit(
            f"Blocked: {command_name} is a {doc.safety} operation and target org '{target_org}' is production. "
            "Production orgs are read-only for this agent CLI. Use a Salesforce sandbox or scratch org for write tests."
        )


def enforce_dynamic_safety(command_id: str, safety: str, target_org: str | None, args: argparse.Namespace) -> None:
    if safety not in {"write", "execute"}:
        return
    if not target_org:
        raise SystemExit("Missing --target-org. Ask the user for the Salesforce org alias before connecting.")
    if getattr(args, "dry_run", False):
        return
    if not detect_is_non_production(target_org, args):
        raise SystemExit(
            f"Blocked: {command_id} is classified as {safety} and target org '{target_org}' is production. "
            "Production orgs are read-only for this agent CLI. Use a Salesforce sandbox or scratch org for write tests."
        )


def common_org(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target-org", help="Salesforce org alias. Ask the user; do not use a default org.")


def add_source_flags(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-dir", action="append", help="Source directory. Repeat for multiple dirs.")
    group.add_argument("--manifest", help="package.xml manifest path.")


def source_args(args: argparse.Namespace) -> list[str]:
    result: list[str] = []
    if getattr(args, "source_dir", None):
        for source_dir in args.source_dir:
            result.extend(["--source-dir", source_dir])
    if getattr(args, "manifest", None):
        result.extend(["--manifest", args.manifest])
    return result


def with_common_deploy_args(result: list[str], args: argparse.Namespace) -> list[str]:
    if getattr(args, "test_level", None):
        result.extend(["--test-level", args.test_level])
    if getattr(args, "tests", None):
        for test in args.tests:
            result.extend(["--tests", test])
    if getattr(args, "wait", None) is not None:
        result.extend(["--wait", str(args.wait)])
    return result


def soql_literal(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def soql_in(values: list[str]) -> str:
    return "(" + ", ".join(soql_literal(value) for value in values) + ")"


def build_user_where(args: argparse.Namespace) -> str:
    clauses: list[str] = []
    if getattr(args, "username", None):
        clauses.append(f"Username IN {soql_in(args.username)}")
    if getattr(args, "user_id", None):
        clauses.append(f"Id IN {soql_in(args.user_id)}")
    if getattr(args, "where", None):
        clauses.append(f"({args.where})")
    if not clauses:
        raise SystemExit("access-inspect requires --username, --user-id, or --where. Ask the user which users/personas to inspect.")
    return " AND ".join(clauses)


def query_result(target_org: str, query: str, args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    completed = sf_run(["data", "query", "--target-org", target_org, "--query", query], args)
    output = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        payload = json.loads(output)
        result = payload.get("result", {})
    except json.JSONDecodeError:
        result = {"error": output}
    return result, completed.returncode


def result_records(result: dict[str, Any]) -> list[dict[str, Any]]:
    records = result.get("records", [])
    return records if isinstance(records, list) else []


def permission_source_label(record: dict[str, Any]) -> str:
    permission_set = record.get("PermissionSet")
    if isinstance(permission_set, dict):
        return str(permission_set.get("Label") or permission_set.get("Name") or record.get("PermissionSetId"))
    return str(record.get("PermissionSetId") or record.get("ParentId") or "unknown")


def explain_access(payload: dict[str, Any], sobjects: list[str] | None) -> list[dict[str, Any]]:
    assignments = result_records(payload.get("permission_set_assignments", {}))
    object_permissions = result_records(payload.get("object_permissions", {}))
    field_permissions = result_records(payload.get("field_permissions", {}))
    assignment_by_ps = {
        assignment.get("PermissionSetId"): assignment
        for assignment in assignments
        if assignment.get("PermissionSetId")
    }
    allowed_sobjects = set(sobjects or [])
    explanations: list[dict[str, Any]] = []
    for permission in object_permissions:
        if allowed_sobjects and permission.get("SobjectType") not in allowed_sobjects:
            continue
        grants = [
            flag
            for flag in (
                "PermissionsRead",
                "PermissionsCreate",
                "PermissionsEdit",
                "PermissionsDelete",
                "PermissionsViewAllRecords",
                "PermissionsModifyAllRecords",
            )
            if permission.get(flag)
        ]
        if not grants:
            continue
        source = assignment_by_ps.get(permission.get("ParentId"), permission)
        explanations.append(
            {
                "type": "object",
                "sobject": permission.get("SobjectType"),
                "grants": grants,
                "source": permission_source_label(source),
                "source_id": permission.get("ParentId"),
            }
        )
    for permission in field_permissions:
        if allowed_sobjects and permission.get("SobjectType") not in allowed_sobjects:
            continue
        grants = [flag for flag in ("PermissionsRead", "PermissionsEdit") if permission.get(flag)]
        if not grants:
            continue
        source = assignment_by_ps.get(permission.get("ParentId"), permission)
        explanations.append(
            {
                "type": "field",
                "field": permission.get("Field"),
                "grants": grants,
                "source": permission_source_label(source),
                "source_id": permission.get("ParentId"),
            }
        )
    return explanations


def access_inspect(args: argparse.Namespace) -> int:
    target_org = require_alias(args)
    user_where = build_user_where(args)
    user_query = (
        "SELECT Id, Username, Name, IsActive, UserType, ProfileId, Profile.Name, UserRoleId, UserRole.Name "
        f"FROM User WHERE {user_where} LIMIT {args.limit}"
    )
    if args.dry_run:
        payload = {
            "dry_run": True,
            "access_inspect": [
                {"name": "users", "sf_command": [sf_binary(), "data", "query", "--target-org", target_org, "--query", user_query, "--json"]},
                {
                    "name": "permission_set_assignments",
                    "query_template": "SELECT Id, AssigneeId, PermissionSetId, PermissionSet.Name, PermissionSet.Label, PermissionSet.IsOwnedByProfile, PermissionSetGroupId FROM PermissionSetAssignment WHERE AssigneeId IN (<User.Id values>)",
                },
                {
                    "name": "permission_set_license_assignments",
                    "query_template": "SELECT Id, AssigneeId, PermissionSetLicenseId FROM PermissionSetLicenseAssign WHERE AssigneeId IN (<User.Id values>)",
                },
                {
                    "name": "object_and_field_permissions",
                    "query_template": "Queried only when --sobject is provided; filters ObjectPermissions and FieldPermissions by inspected PermissionSetId values.",
                },
            ],
        }
        return emit_payload(payload, args)

    users, user_code = query_result(target_org, user_query, args)
    user_records = result_records(users)
    user_ids = sorted({record.get("Id") for record in user_records if record.get("Id")})
    payload: dict[str, Any] = {
        "least_privilege_note": "Grant only permissions needed for the approved task. Ask the user when permission scope is unclear.",
        "users": users,
    }
    returncode = user_code
    if not user_ids:
        payload["notes"] = ["No users matched the access-inspect filter."]
        return emit_payload(payload, args, returncode)

    user_ids_clause = soql_in(user_ids)
    psa_query = (
        "SELECT Id, AssigneeId, PermissionSetId, PermissionSet.Name, PermissionSet.Label, "
        "PermissionSet.IsOwnedByProfile, PermissionSetGroupId "
        f"FROM PermissionSetAssignment WHERE AssigneeId IN {user_ids_clause}"
    )
    assignments, assignment_code = query_result(target_org, psa_query, args)
    payload["permission_set_assignments"] = assignments
    returncode = max(returncode, assignment_code)

    psl_query = f"SELECT Id, AssigneeId, PermissionSetLicenseId FROM PermissionSetLicenseAssign WHERE AssigneeId IN {user_ids_clause}"
    license_assignments, license_code = query_result(target_org, psl_query, args)
    payload["permission_set_license_assignments"] = license_assignments
    returncode = max(returncode, license_code)

    assignment_records = result_records(assignments)
    permission_set_ids = sorted({record.get("PermissionSetId") for record in assignment_records if record.get("PermissionSetId")})
    permission_set_group_ids = sorted({record.get("PermissionSetGroupId") for record in assignment_records if record.get("PermissionSetGroupId")})

    if permission_set_group_ids:
        psg_clause = soql_in(permission_set_group_ids)
        groups, group_code = query_result(target_org, f"SELECT Id, DeveloperName, MasterLabel, Status FROM PermissionSetGroup WHERE Id IN {psg_clause}", args)
        payload["permission_set_groups"] = groups
        returncode = max(returncode, group_code)
        component_query = (
            "SELECT PermissionSetGroupId, PermissionSetId, PermissionSet.Name, PermissionSet.Label "
            f"FROM PermissionSetGroupComponent WHERE PermissionSetGroupId IN {psg_clause}"
        )
        components, component_code = query_result(target_org, component_query, args)
        payload["permission_set_group_components"] = components
        returncode = max(returncode, component_code)

    if args.sobject and permission_set_ids:
        parent_clause = soql_in(permission_set_ids)
        sobject_clause = soql_in(args.sobject)
        object_query = (
            "SELECT ParentId, SobjectType, PermissionsRead, PermissionsCreate, PermissionsEdit, PermissionsDelete, "
            "PermissionsViewAllRecords, PermissionsModifyAllRecords "
            f"FROM ObjectPermissions WHERE ParentId IN {parent_clause} AND SobjectType IN {sobject_clause} "
            f"LIMIT {args.permission_limit}"
        )
        object_permissions, object_code = query_result(target_org, object_query, args)
        payload["object_permissions"] = object_permissions
        returncode = max(returncode, object_code)
        field_query = (
            "SELECT ParentId, SobjectType, Field, PermissionsRead, PermissionsEdit "
            f"FROM FieldPermissions WHERE ParentId IN {parent_clause} AND SobjectType IN {sobject_clause} "
            f"LIMIT {args.permission_limit}"
        )
        field_permissions, field_code = query_result(target_org, field_query, args)
        payload["field_permissions"] = field_permissions
        returncode = max(returncode, field_code)
    elif not args.sobject:
        payload["notes"] = ["ObjectPermissions and FieldPermissions skipped. Pass --sobject for affected objects to inspect CRUD/FLS."]

    payload["access_explanations"] = explain_access(payload, args.sobject)
    return emit_payload(payload, args, returncode)


def flag_values(tokens: list[str], names: set[str]) -> list[str]:
    values = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        matched = next((name for name in names if token == name), None)
        if matched and index + 1 < len(tokens):
            values.append(tokens[index + 1])
            index += 2
            continue
        for name in names:
            prefix = f"{name}="
            if token.startswith(prefix):
                values.append(token[len(prefix) :])
        index += 1
    return values


def deploy_result_summary(completed: subprocess.CompletedProcess[str]) -> str:
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return "Deploy completed."
    result = payload.get("result", {})
    parts = []
    for key in ("id", "status", "success", "checkOnly"):
        if key in result:
            parts.append(f"{key}={result[key]}")
    return ", ".join(parts) or "Deploy completed."


def append_deploy_history(command_id: str, sf_args: list[str], args: argparse.Namespace, completed: subprocess.CompletedProcess[str]) -> None:
    if getattr(args, "dry_run", False):
        return
    if completed.returncode != 0 or command_id != "project:deploy:start":
        return
    target_org = getattr(args, "target_org", None) or extract_flag_value(sf_args, "--target-org", "-o") or "unknown"
    artifacts = flag_values(sf_args, {"--source-dir", "--manifest", "--metadata"})
    artifact_text = ", ".join(artifacts[:10]) if artifacts else "unspecified"
    command_text = "sf " + " ".join(redact_cli_args(sf_args))
    summary = deploy_result_summary(completed)
    requirements = getattr(args, "requirements", None)
    changed_metadata = getattr(args, "changed_metadata", None) or []
    if not requirements or not changed_metadata:
        raise SystemExit("Deploy history requires --requirements and at least one --changed-metadata value.")
    history_script = Path(__file__).with_name("knowledge_history.py")
    history_command = [
        sys.executable,
        str(history_script),
        "--project-root",
        str(Path.cwd()),
        "--action",
        "deploy",
        "--requirements",
        requirements,
        "--target-org",
        target_org,
        "--summary",
        f"{summary}; artifacts={artifact_text}",
        "--result",
        "deploy succeeded",
        "--command",
        command_text,
    ]
    for item in changed_metadata:
        history_command.extend(["--metadata", item])
    completed_history = subprocess.run(history_command, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    if completed_history.stdout.strip():
        print(completed_history.stdout.strip())
    if completed_history.returncode != 0:
        raise SystemExit(completed_history.stderr or "Failed to record deploy history.")


def require_deploy_history_details(command_id: str, args: argparse.Namespace) -> None:
    if getattr(args, "dry_run", False) or command_id != "project:deploy:start":
        return
    if not getattr(args, "requirements", None):
        raise SystemExit("Deploy requires --requirements so Knowledge history records why metadata changed.")
    if not getattr(args, "changed_metadata", None):
        raise SystemExit("Deploy requires at least one --changed-metadata so Knowledge history records all modified metadata.")


def run_simple(command_name: str, sf_args: list[str], args: argparse.Namespace) -> int:
    if command_name == "deploy-start":
        require_deploy_history_details("project:deploy:start", args)
    require_delete_approval(command_name, args, sf_args)
    enforce_safety(command_name, args)
    completed = sf_run(sf_args, args)
    code = emit_result(completed, args)
    if command_name == "deploy-start":
        append_deploy_history("project:deploy:start", sf_args, args, completed)
    return code


def docs(_: argparse.Namespace) -> int:
    payload = [
        {
            "name": command.name,
            "safety": command.safety,
            "requires_alias": command.requires_alias,
            "maps_to": command.maps_to,
            "description": command.description,
        }
        for command in COMMANDS
    ]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def safe_run(args: argparse.Namespace) -> int:
    sf_args = list(args.sf_args)
    if sf_args and sf_args[0] == "--":
        sf_args = sf_args[1:]
    if not sf_args:
        raise SystemExit("Provide an official sf command after `--`, for example: safe-run --target-org dev -- data query --query \"SELECT Id FROM Account LIMIT 1\"")

    command_id = canonical_official_command_id(sf_args)
    target_org = args.target_org or extract_flag_value(sf_args, "--target-org", "-o")
    connects = command_likely_connects(command_id, sf_args, target_org)
    safety = args.safety or classify_official_safety(command_id, connects_to_org=connects)
    target_org = args.target_org or extract_flag_value(sf_args, "--target-org", "-o")

    if connects and not target_org and safety not in {"auth", "local"}:
        raise SystemExit("Missing --target-org. Ask the user for the Salesforce org alias before connecting.")

    if target_org and not has_flag(sf_args, "--target-org", "-o") and safety not in {"auth", "local"}:
        sf_args.extend(["--target-org", target_org])

    require_deploy_history_details(command_id, args)
    require_delete_approval(command_id, args, sf_args)
    require_secret_approval(command_id, args, sf_args)
    enforce_dynamic_safety(command_id, safety, target_org, args)
    if args.dry_run:
        dry_command = [sf_binary(), *sf_args]
        if not args.raw and "--json" not in dry_command:
            dry_command.append("--json")
        payload = {
            "dry_run": True,
            "classified_safety": safety,
            "command_id": command_id,
            "sf_command": redact_cli_args(dry_command),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    completed = sf_run(sf_args, args, allow_non_json=args.raw)
    code = emit_result(completed, args)
    append_deploy_history(command_id, sf_args, args, completed)
    return code


def catalog_refresh(args: argparse.Namespace) -> int:
    script_path = Path(__file__).with_name("sf_catalog_build.py")
    completed = subprocess.run(
        [sys.executable, str(script_path), "--output-dir", args.output_dir],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if completed.stdout.strip():
        print(completed.stdout.strip())
    if completed.stderr.strip():
        print(completed.stderr.strip(), file=sys.stderr)
    return completed.returncode


def org_inspect(args: argparse.Namespace) -> int:
    target_org = require_alias(args)
    display = sf_run(["org", "display", "--target-org", target_org], args)
    if display.returncode != 0:
        return emit_result(display, args)
    sandbox = sf_run(["data", "query", "--target-org", target_org, "--query", PROD_CHECK_QUERY], args)
    payload = {
        "org_display": json.loads(display.stdout).get("result", {}),
        "organization": json.loads(sandbox.stdout).get("result", {}) if sandbox.returncode == 0 else {"error": sandbox.stderr},
    }
    print(json.dumps(compact(redact(payload), args.max_list), indent=2, sort_keys=True)[: args.max_chars])
    return 0 if sandbox.returncode == 0 else sandbox.returncode


def metadata_list(args: argparse.Namespace) -> int:
    enforce_safety("metadata-list", args)
    sf_args = ["org", "list", "metadata", "--target-org", args.target_org, "--metadata-type", args.metadata_type]
    if args.folder:
        sf_args.extend(["--folder", args.folder])
    completed = sf_run(sf_args, args)
    if args.raw:
        return emit_result(completed, args)
    output = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return emit_result(completed, args)
    records = payload.get("result", [])
    if isinstance(records, list):
        payload["result"] = [
            {
                key: record.get(key)
                for key in (
                    "fullName",
                    "type",
                    "fileName",
                    "namespacePrefix",
                    "createdDate",
                    "lastModifiedDate",
                )
                if isinstance(record, dict) and record.get(key) not in (None, "")
            }
            for record in records
        ]
        payload["summary"] = {"metadataType": args.metadata_type, "count": len(records)}
    return emit_payload(payload, args, completed.returncode)


def compact_describe_result(payload: dict[str, Any], field_limit: int) -> dict[str, Any]:
    result = payload.get("result", {})
    if not isinstance(result, dict):
        return payload
    fields = result.get("fields", [])
    child_relationships = result.get("childRelationships", [])
    record_type_infos = result.get("recordTypeInfos", [])
    compact_fields: list[dict[str, Any]] = []
    if isinstance(fields, list):
        for field in fields[:field_limit]:
            if not isinstance(field, dict):
                continue
            compact_fields.append(
                {
                    key: field.get(key)
                    for key in (
                        "name",
                        "label",
                        "type",
                        "custom",
                        "nillable",
                        "createable",
                        "updateable",
                        "calculated",
                        "referenceTo",
                        "relationshipName",
                    )
                    if field.get(key) not in (None, "", [])
                }
            )
    compact_result = {
        "name": result.get("name"),
        "label": result.get("label"),
        "custom": result.get("custom"),
        "keyPrefix": result.get("keyPrefix"),
        "createable": result.get("createable"),
        "updateable": result.get("updateable"),
        "deletable": result.get("deletable"),
        "queryable": result.get("queryable"),
        "searchable": result.get("searchable"),
        "fieldCount": len(fields) if isinstance(fields, list) else None,
        "childRelationshipCount": len(child_relationships) if isinstance(child_relationships, list) else None,
        "recordTypeCount": len(record_type_infos) if isinstance(record_type_infos, list) else None,
        "fields": compact_fields,
    }
    payload["result"] = {key: value for key, value in compact_result.items() if value is not None}
    payload["summary"] = {
        "mode": "compact",
        "fieldLimit": field_limit,
        "note": "Use --raw only when a full describe is explicitly required.",
    }
    return payload


def schema_sobject_describe(args: argparse.Namespace) -> int:
    enforce_safety("schema-sobject-describe", args)
    completed = sf_run(
        ["sobject", "describe", "--target-org", args.target_org, "--sobject", args.sobject],
        args,
    )
    if args.raw:
        return emit_result(completed, args)
    output = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return emit_result(completed, args)
    payload = compact_describe_result(payload, args.field_limit)
    return emit_payload(payload, args, completed.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Token-efficient Salesforce CLI facade for AI agents.")
    parser.add_argument("--dry-run", action="store_true", help="Print the mapped sf command without executing it.")
    parser.add_argument("--raw", action="store_true", help="Do not append --json or parse JSON.")
    parser.add_argument("--select", help="Comma-separated JSON paths to keep in output.")
    parser.add_argument("--max-chars", type=int, default=12000, help="Maximum output characters.")
    parser.add_argument("--max-list", type=int, default=20, help="Maximum list items before truncation.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("commands", help="List documented agent CLI commands.").set_defaults(func=docs)

    p = sub.add_parser("safe-run", help=DOCS["safe-run"].description)
    p.add_argument("--target-org", help="Salesforce org alias to append when the official command supports target-org.")
    p.add_argument("--safety", choices=["read", "write", "execute", "auth", "local"], help="Override automatic safety classification.")
    p.add_argument("--requirements", help="Requirement that caused a deploy; required for `project deploy start`.")
    p.add_argument("--changed-metadata", action="append", help="Modified metadata; required and repeatable for `project deploy start`.")
    p.add_argument("--delete-approval", help=f"Required exact phrase for destructive operations: {DELETE_APPROVAL_PHRASE}")
    p.add_argument("--secret-approval", help=f"Required exact phrase for commands that can expose secrets: {SECRET_APPROVAL_PHRASE}")
    p.add_argument("sf_args", nargs=argparse.REMAINDER)
    p.set_defaults(func=safe_run)

    p = sub.add_parser("catalog-refresh", help=DOCS["catalog-refresh"].description)
    p.add_argument("--output-dir", default=str(Path(__file__).resolve().parent.parent / "references"))
    p.set_defaults(func=catalog_refresh)

    p = sub.add_parser("auth-web", help=DOCS["auth-web"].description)
    p.add_argument("--alias", required=True)
    p.add_argument("--instance-url", default="https://login.salesforce.com")
    p.set_defaults(func=lambda a: run_simple("auth-web", ["org", "login", "web", "--alias", a.alias, "--instance-url", a.instance_url], a))

    p = sub.add_parser("auth-device", help=DOCS["auth-device"].description)
    p.add_argument("--alias", required=True)
    p.add_argument("--instance-url", default="https://login.salesforce.com")
    p.set_defaults(func=lambda a: run_simple("auth-device", ["org", "login", "device", "--alias", a.alias, "--instance-url", a.instance_url], a))

    p = sub.add_parser("auth-jwt", help=DOCS["auth-jwt"].description)
    p.add_argument("--alias", required=True)
    p.add_argument("--username", required=True)
    p.add_argument("--client-id", required=True)
    p.add_argument("--jwt-key-file", required=True)
    p.add_argument("--instance-url", default="https://login.salesforce.com")
    p.set_defaults(
        func=lambda a: run_simple(
            "auth-jwt",
            [
                "org",
                "login",
                "jwt",
                "--alias",
                a.alias,
                "--username",
                a.username,
                "--client-id",
                a.client_id,
                "--jwt-key-file",
                a.jwt_key_file,
                "--instance-url",
                a.instance_url,
            ],
            a,
        )
    )

    sub.add_parser("org-list", help=DOCS["org-list"].description).set_defaults(func=lambda a: run_simple("org-list", ["org", "list"], a))

    p = sub.add_parser("org-inspect", help=DOCS["org-inspect"].description)
    common_org(p)
    p.set_defaults(func=org_inspect)

    p = sub.add_parser("org-limits", help=DOCS["org-limits"].description)
    common_org(p)
    p.set_defaults(func=lambda a: run_simple("org-limits", ["limits", "api", "display", "--target-org", a.target_org], a))

    p = sub.add_parser("schema-sobject-list", help=DOCS["schema-sobject-list"].description)
    common_org(p)
    p.add_argument("--sobject-type", choices=["all", "custom", "standard"], default="all")
    p.set_defaults(func=lambda a: run_simple("schema-sobject-list", ["sobject", "list", "--target-org", a.target_org, "--sobject", a.sobject_type], a))

    p = sub.add_parser("schema-sobject-describe", help=DOCS["schema-sobject-describe"].description)
    common_org(p)
    p.add_argument("--sobject", required=True)
    p.add_argument("--field-limit", type=int, default=12, help="Fields to include in compact describe output.")
    p.set_defaults(func=schema_sobject_describe)

    p = sub.add_parser("metadata-list", help=DOCS["metadata-list"].description)
    common_org(p)
    p.add_argument("--metadata-type", required=True)
    p.add_argument("--folder")
    p.set_defaults(func=metadata_list)

    p = sub.add_parser("metadata-retrieve", help=DOCS["metadata-retrieve"].description)
    common_org(p)
    p.add_argument("--metadata", action="append", required=True, help="Metadata selector, for example ApexClass:MyClass.")
    p.set_defaults(
        func=lambda a: run_simple(
            "metadata-retrieve",
            ["project", "retrieve", "start", "--target-org", a.target_org] + [item for meta in a.metadata for item in ("--metadata", meta)],
            a,
        )
    )

    p = sub.add_parser("metadata-retrieve-manifest", help=DOCS["metadata-retrieve-manifest"].description)
    common_org(p)
    p.add_argument("--manifest", required=True)
    p.set_defaults(func=lambda a: run_simple("metadata-retrieve-manifest", ["project", "retrieve", "start", "--target-org", a.target_org, "--manifest", a.manifest], a))

    for name, sf_tail in [
        ("deploy-preview", ["project", "deploy", "preview"]),
        ("deploy-validate", ["project", "deploy", "validate"]),
        ("deploy-start", ["project", "deploy", "start"]),
    ]:
        p = sub.add_parser(name, help=DOCS[name].description)
        common_org(p)
        add_source_flags(p)
        p.add_argument("--test-level")
        p.add_argument("--tests", action="append")
        p.add_argument("--wait", type=int, default=30)
        if name == "deploy-start":
            p.add_argument("--requirements", help="Requirement that caused the deployed metadata changes.")
            p.add_argument("--changed-metadata", action="append", help="Modified metadata, for example ApexClass:AccountService. Repeat for all changed metadata.")
            p.add_argument("--delete-approval", help=f"Required exact phrase when deploying destructive changes: {DELETE_APPROVAL_PHRASE}")
        p.set_defaults(func=lambda a, n=name, tail=sf_tail: run_simple(n, with_common_deploy_args(tail + ["--target-org", a.target_org] + source_args(a), a), a))

    p = sub.add_parser("deploy-report", help=DOCS["deploy-report"].description)
    common_org(p)
    p.add_argument("--job-id", required=True)
    p.set_defaults(func=lambda a: run_simple("deploy-report", ["project", "deploy", "report", "--target-org", a.target_org, "--job-id", a.job_id], a))

    p = sub.add_parser("data-query", help=DOCS["data-query"].description)
    common_org(p)
    p.add_argument("--query", required=True)
    p.add_argument("--tooling", action="store_true")
    p.set_defaults(
        func=lambda a: run_simple(
            "data-query",
            ["data", "query", "--target-org", a.target_org, "--query", a.query] + (["--use-tooling-api"] if a.tooling else []),
            a,
        )
    )

    p = sub.add_parser("data-record-get", help=DOCS["data-record-get"].description)
    common_org(p)
    p.add_argument("--sobject", required=True)
    p.add_argument("--record-id", required=True)
    p.set_defaults(func=lambda a: run_simple("data-record-get", ["data", "get", "record", "--target-org", a.target_org, "--sobject", a.sobject, "--record-id", a.record_id], a))

    p = sub.add_parser("data-record-create", help=DOCS["data-record-create"].description)
    common_org(p)
    p.add_argument("--sobject", required=True)
    p.add_argument("--values", required=True, help='Field values, for example "Name=Acme Rating=Hot".')
    p.set_defaults(func=lambda a: run_simple("data-record-create", ["data", "create", "record", "--target-org", a.target_org, "--sobject", a.sobject, "--values", a.values], a))

    p = sub.add_parser("data-record-update", help=DOCS["data-record-update"].description)
    common_org(p)
    p.add_argument("--sobject", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--values", required=True)
    p.set_defaults(func=lambda a: run_simple("data-record-update", ["data", "update", "record", "--target-org", a.target_org, "--sobject", a.sobject, "--record-id", a.record_id, "--values", a.values], a))

    p = sub.add_parser("data-record-delete", help=DOCS["data-record-delete"].description)
    common_org(p)
    p.add_argument("--sobject", required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--delete-approval", help=f"Required exact phrase: {DELETE_APPROVAL_PHRASE}")
    p.set_defaults(func=lambda a: run_simple("data-record-delete", ["data", "delete", "record", "--target-org", a.target_org, "--sobject", a.sobject, "--record-id", a.record_id], a))

    p = sub.add_parser("access-inspect", help=DOCS["access-inspect"].description)
    common_org(p)
    p.add_argument("--username", action="append", help="Username to inspect. Repeat for multiple users.")
    p.add_argument("--user-id", action="append", help="User Id to inspect. Repeat for multiple users.")
    p.add_argument("--where", help="SOQL condition for target users, for example IsActive = true AND Profile.Name = 'Sales'.")
    p.add_argument("--sobject", action="append", help="Affected sObject API name for CRUD/FLS inspection. Repeat for multiple objects.")
    p.add_argument("--limit", type=int, default=25, help="Maximum users to inspect.")
    p.add_argument("--permission-limit", type=int, default=200, help="Maximum ObjectPermissions/FieldPermissions rows.")
    p.set_defaults(func=access_inspect)

    p = sub.add_parser("apex-test-run", help=DOCS["apex-test-run"].description)
    common_org(p)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--tests", action="append")
    group.add_argument("--suite-names", action="append")
    p.add_argument("--code-coverage", action="store_true")
    p.add_argument("--wait", type=int, default=30)
    p.set_defaults(
        func=lambda a: run_simple(
            "apex-test-run",
            ["apex", "run", "test", "--target-org", a.target_org, "--result-format", "json", "--wait", str(a.wait)]
            + ([item for test in (a.tests or []) for item in ("--tests", test)])
            + ([item for suite in (a.suite_names or []) for item in ("--suite-names", suite)])
            + (["--code-coverage"] if a.code_coverage else []),
            a,
        )
    )

    p = sub.add_parser("apex-test-report", help=DOCS["apex-test-report"].description)
    common_org(p)
    p.add_argument("--test-run-id", required=True)
    p.set_defaults(func=lambda a: run_simple("apex-test-report", ["apex", "get", "test", "--target-org", a.target_org, "--test-run-id", a.test_run_id, "--result-format", "json"], a))

    p = sub.add_parser("apex-log-list", help=DOCS["apex-log-list"].description)
    common_org(p)
    p.set_defaults(func=lambda a: run_simple("apex-log-list", ["apex", "list", "log", "--target-org", a.target_org], a))

    p = sub.add_parser("apex-log-get", help=DOCS["apex-log-get"].description)
    common_org(p)
    p.add_argument("--log-id", required=True)
    p.set_defaults(func=lambda a: run_simple("apex-log-get", ["apex", "get", "log", "--target-org", a.target_org, "--log-id", a.log_id], a))

    p = sub.add_parser("apex-run", help=DOCS["apex-run"].description)
    common_org(p)
    p.add_argument("--file", required=True)
    p.set_defaults(func=lambda a: run_simple("apex-run", ["apex", "run", "--target-org", a.target_org, "--file", a.file], a))

    p = sub.add_parser("package-installed-list", help=DOCS["package-installed-list"].description)
    common_org(p)
    p.set_defaults(func=lambda a: run_simple("package-installed-list", ["package", "installed", "list", "--target-org", a.target_org], a))

    p = sub.add_parser("package-install", help=DOCS["package-install"].description)
    common_org(p)
    p.add_argument("--package", required=True)
    p.add_argument("--wait", type=int, default=30)
    p.add_argument("--publish-wait", type=int, default=10)
    p.set_defaults(func=lambda a: run_simple("package-install", ["package", "install", "--target-org", a.target_org, "--package", a.package, "--wait", str(a.wait), "--publish-wait", str(a.publish_wait), "--no-prompt"], a))

    p = sub.add_parser("package-uninstall", help=DOCS["package-uninstall"].description)
    common_org(p)
    p.add_argument("--package", required=True)
    p.add_argument("--wait", type=int, default=30)
    p.add_argument("--delete-approval", help=f"Required exact phrase: {DELETE_APPROVAL_PHRASE}")
    p.set_defaults(func=lambda a: run_simple("package-uninstall", ["package", "uninstall", "--target-org", a.target_org, "--package", a.package, "--wait", str(a.wait), "--no-prompt"], a))

    p = sub.add_parser("user-display", help=DOCS["user-display"].description)
    common_org(p)
    p.add_argument("--target-user")
    p.set_defaults(func=lambda a: run_simple("user-display", ["org", "display", "user", "--target-org", a.target_org] + (["--target-user", a.target_user] if a.target_user else []), a))

    p = sub.add_parser("permset-assign", help=DOCS["permset-assign"].description)
    common_org(p)
    p.add_argument("--name", required=True)
    p.add_argument("--on-behalf-of")
    p.set_defaults(func=lambda a: run_simple("permset-assign", ["org", "assign", "permset", "--target-org", a.target_org, "--name", a.name] + (["--on-behalf-of", a.on_behalf_of] if a.on_behalf_of else []), a))

    p = sub.add_parser("local-manifest-generate", help=DOCS["local-manifest-generate"].description)
    p.add_argument("--metadata", action="append")
    p.add_argument("--source-dir", action="append")
    p.add_argument("--output-dir", default="manifest")
    p.set_defaults(
        func=lambda a: run_simple(
            "local-manifest-generate",
            ["project", "generate", "manifest", "--output-dir", a.output_dir]
            + ([item for metadata in (a.metadata or []) for item in ("--metadata", metadata)])
            + ([item for source_dir in (a.source_dir or []) for item in ("--source-dir", source_dir)]),
            a,
        )
    )

    return parser


def normalize_global_flags(argv: list[str]) -> list[str]:
    """Allow global flags before or after the subcommand."""
    value_flags = {"--select", "--max-chars", "--max-list"}
    switch_flags = {"--dry-run", "--raw"}
    global_args: list[str] = []
    rest: list[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token in value_flags and index + 1 < len(argv):
            global_args.extend([token, argv[index + 1]])
            index += 2
        elif token in switch_flags:
            global_args.append(token)
            index += 1
        else:
            rest.append(token)
            index += 1
    return [*global_args, *rest]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args(normalize_global_flags(sys.argv[1:]))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
