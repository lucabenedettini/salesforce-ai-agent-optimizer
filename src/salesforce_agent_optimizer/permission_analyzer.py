"""Permission analyzer v2 for compact least-privilege explanations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


OBJECT_FLAGS = [
    "PermissionsRead",
    "PermissionsCreate",
    "PermissionsEdit",
    "PermissionsDelete",
    "PermissionsViewAllRecords",
    "PermissionsModifyAllRecords",
]
FIELD_FLAGS = ["PermissionsRead", "PermissionsEdit"]


def _records(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key, {})
    if isinstance(value, dict):
        records = value.get("records", [])
        return records if isinstance(records, list) else []
    return value if isinstance(value, list) else []


def _label(record: dict[str, Any]) -> str:
    permission_set = record.get("PermissionSet")
    if isinstance(permission_set, dict):
        return str(permission_set.get("Label") or permission_set.get("Name") or record.get("PermissionSetId"))
    return str(record.get("PermissionSetId") or record.get("ParentId") or "unknown")


def analyze_access(payload: dict[str, Any], sobject: str | None = None, field: str | None = None) -> dict[str, Any]:
    users = _records(payload, "users")
    assignments = _records(payload, "permission_set_assignments")
    object_permissions = _records(payload, "object_permissions")
    field_permissions = _records(payload, "field_permissions")
    groups = _records(payload, "permission_set_groups")
    components = _records(payload, "permission_set_group_components")

    explanations: list[dict[str, Any]] = []
    assignment_by_ps = {
        assignment.get("PermissionSetId"): assignment
        for assignment in assignments
        if assignment.get("PermissionSetId")
    }
    for permission in object_permissions:
        if sobject and permission.get("SobjectType") != sobject:
            continue
        grants = [flag for flag in OBJECT_FLAGS if permission.get(flag)]
        if not grants:
            continue
        assignment = assignment_by_ps.get(permission.get("ParentId"), {})
        explanations.append(
            {
                "type": "object",
                "sobject": permission.get("SobjectType"),
                "grants": grants,
                "source": _label(assignment or permission),
                "source_id": permission.get("ParentId"),
                "least_privilege_note": _risk_note(grants),
            }
        )

    for permission in field_permissions:
        if sobject and permission.get("SobjectType") != sobject:
            continue
        if field and permission.get("Field") != field:
            continue
        grants = [flag for flag in FIELD_FLAGS if permission.get(flag)]
        if not grants:
            continue
        assignment = assignment_by_ps.get(permission.get("ParentId"), {})
        explanations.append(
            {
                "type": "field",
                "field": permission.get("Field"),
                "grants": grants,
                "source": _label(assignment or permission),
                "source_id": permission.get("ParentId"),
                "least_privilege_note": "Field edit access should be granted only when the approved workflow writes this field."
                if "PermissionsEdit" in grants
                else "Read-only field access is preferred when edit is not required.",
            }
        )

    return {
        "users": [
            {
                "id": user.get("Id"),
                "username": user.get("Username"),
                "name": user.get("Name"),
                "is_active": user.get("IsActive"),
                "profile": (user.get("Profile") or {}).get("Name") if isinstance(user.get("Profile"), dict) else None,
            }
            for user in users
        ],
        "assignment_count": len(assignments),
        "permission_set_group_count": len(groups),
        "permission_set_group_component_count": len(components),
        "filter": {"sobject": sobject, "field": field},
        "access_explanations": explanations,
        "planning_note": (
            "Use this as evidence only. If the required permission scope is unclear, ask the user before granting access."
        ),
    }


def _risk_note(grants: list[str]) -> str:
    if "PermissionsModifyAllRecords" in grants or "PermissionsViewAllRecords" in grants:
        return "High-scope access found. Prefer narrower CRUD/FLS, sharing, or targeted permission sets."
    if "PermissionsDelete" in grants:
        return "Delete access is destructive. Require explicit business justification and approval."
    if "PermissionsEdit" in grants or "PermissionsCreate" in grants:
        return "Write access should match only the approved create/edit workflow."
    return "Read access is the least risky object grant."


def analyze_access_file(path: Path, sobject: str | None = None, field: str | None = None) -> dict[str, Any]:
    return analyze_access(json.loads(path.read_text(encoding="utf-8")), sobject=sobject, field=field)
