"""Registry for Salesforce CLI facade commands exposed to agents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any


REGISTRY_NAME = "agent-tool-registry.json"
DEFAULT_TOOLSETS = {
    "core": {"auth-web", "auth-device", "auth-jwt", "org-list", "org-inspect", "org-limits"},
    "schema": {"schema-sobject-list", "schema-sobject-describe", "data-query"},
    "data-read": {"data-query", "data-record-get"},
    "metadata": {"metadata-list", "metadata-retrieve", "metadata-retrieve-manifest"},
    "deploy": {"deploy-preview", "deploy-validate", "deploy-start", "deploy-report"},
    "permissions": {"access-inspect", "user-display", "permset-assign"},
    "apex": {"apex-test-run", "apex-test-report", "apex-log-list", "apex-log-get", "apex-run"},
    "packages": {"package-installed-list", "package-install", "package-uninstall"},
    "local": {"local-manifest-generate", "catalog-refresh"},
}


@dataclass(frozen=True)
class Tool:
    name: str
    category: str
    safety: str
    description: str
    maps_to: str
    requires_alias: bool
    production: str
    arguments: dict[str, Any]
    output: dict[str, Any]
    example: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Tool":
        return cls(
            name=str(payload["name"]),
            category=str(payload.get("category", "core")),
            safety=str(payload.get("safety", "read")),
            description=str(payload.get("description", "")),
            maps_to=str(payload.get("maps_to", "")),
            requires_alias=bool(payload.get("requires_alias", False)),
            production=str(payload.get("production", "read-only")),
            arguments=dict(payload.get("arguments", {})),
            output=dict(payload.get("output", {})),
            example=dict(payload.get("example", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "safety": self.safety,
            "requires_alias": self.requires_alias,
            "production": self.production,
            "maps_to": self.maps_to,
            "description": self.description,
            "arguments": self.arguments,
            "output": self.output,
            "example": self.example,
        }


def load_registry(root: Path | None = None) -> dict[str, Any]:
    if root:
        project_registry = root / "references" / REGISTRY_NAME
        if project_registry.exists():
            return json.loads(project_registry.read_text(encoding="utf-8"))
    package = resources.files("salesforce_agent_optimizer").joinpath("templates", "references", REGISTRY_NAME)
    return json.loads(package.read_text(encoding="utf-8"))


def registry_tools(root: Path | None = None) -> list[Tool]:
    payload = load_registry(root)
    return [Tool.from_dict(item) for item in payload.get("tools", [])]


def get_tool(name: str, root: Path | None = None) -> Tool:
    for tool in registry_tools(root):
        if tool.name == name:
            return tool
    raise KeyError(f"Unknown sfao command tool: {name}")


def search_tools(query: str = "", toolset: str | None = None, root: Path | None = None) -> list[Tool]:
    terms = [term.lower() for term in query.split() if term.strip()]
    allowed = DEFAULT_TOOLSETS.get(toolset or "", set())
    results: list[tuple[int, Tool]] = []
    for tool in registry_tools(root):
        if allowed and tool.name not in allowed:
            continue
        haystack = " ".join(
            [
                tool.name,
                tool.category,
                tool.safety,
                tool.description,
                tool.maps_to,
                " ".join(tool.arguments.keys()),
            ]
        ).lower()
        score = sum(1 for term in terms if term in haystack) if terms else 1
        if score:
            results.append((score, tool))
    results.sort(key=lambda item: (-item[0], item[1].category, item[1].name))
    return [tool for _, tool in results]


def payload_example(name: str, root: Path | None = None) -> dict[str, Any]:
    tool = get_tool(name, root)
    return {
        "tool": tool.name,
        "dry_run": True,
        "target_org": "ASK_USER_FOR_ALIAS" if tool.requires_alias else None,
        "options": tool.example.get("options", {}),
        "global": {
            "max_chars": 6000,
            "max_list": 10,
            "select": tool.output.get("recommended_select"),
        },
    }
