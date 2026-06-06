"""Token-efficient SOQL builder helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


API_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:__[cr])?$")
RELATIONSHIP_FIELD = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:__[r])?(?:\.[A-Za-z_][A-Za-z0-9_]*(?:__[cr])?)*$")


def validate_api_name(value: str, label: str) -> None:
    if not API_NAME.match(value):
        raise ValueError(f"Invalid {label}: {value}")


def validate_field(value: str) -> None:
    if not RELATIONSHIP_FIELD.match(value):
        raise ValueError(f"Invalid field or relationship path: {value}")


def describe_fields(path: Path | None) -> set[str]:
    if not path:
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    result = payload.get("result", payload)
    fields = result.get("fields", [])
    return {field["name"] for field in fields if isinstance(field, dict) and field.get("name")}


def build_soql(
    sobject: str,
    fields: list[str],
    where: str | None = None,
    order_by: str | None = None,
    limit: int = 50,
    describe_path: Path | None = None,
) -> dict[str, Any]:
    validate_api_name(sobject, "sObject")
    if not fields:
        raise ValueError("At least one field is required.")
    for field in fields:
        validate_field(field)
    known_fields = describe_fields(describe_path)
    unknown = sorted({field for field in fields if "." not in field and known_fields and field not in known_fields})
    if unknown:
        raise ValueError("Fields not found in describe payload: " + ", ".join(unknown))
    if limit < 1 or limit > 2000:
        raise ValueError("Limit must be between 1 and 2000.")
    if order_by:
        validate_field(order_by.split()[0])

    query = f"SELECT {', '.join(fields)} FROM {sobject}"
    if where:
        query += f" WHERE {where}"
    if order_by:
        query += f" ORDER BY {order_by}"
    query += f" LIMIT {limit}"
    return {
        "query": query,
        "field_count": len(fields),
        "uses_describe_validation": bool(known_fields),
        "next_command": {
            "tool": "data-query",
            "target_org": "ASK_USER_FOR_ALIAS",
            "options": {"query": query},
            "global": {"select": "result.totalSize,result.records", "max_chars": 6000, "max_list": 10},
        },
    }
