"""CLI facade over the Salesforce Agent Optimizer tool registry."""

from __future__ import annotations

import json
import subprocess
import sys
from importlib import resources
from pathlib import Path
from typing import Any

from .command_registry import payload_example, search_tools


GLOBAL_OPTIONS = {"max_chars", "max_list", "select", "raw", "dry_run"}


def search_payload(query: str, toolset: str | None, root: Path, limit: int) -> dict[str, Any]:
    tools = search_tools(query, toolset=toolset, root=root)
    return {
        "query": query,
        "toolset": toolset,
        "count": min(len(tools), limit),
        "tools": [tool.to_dict() for tool in tools[:limit]],
    }


def load_payload(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


def command_script(root: Path) -> Path:
    root = root.resolve()
    local = root / "scripts" / "sf_agent_cli.py"
    if local.exists():
        return local
    return Path(
        str(
            resources.files("salesforce_agent_optimizer").joinpath(
                "templates", "scripts", "sf_agent_cli.py"
            )
        )
    )


def append_option(args: list[str], name: str, value: Any) -> None:
    flag = "--" + name.replace("_", "-")
    if value is None:
        return
    if isinstance(value, bool):
        if value:
            args.append(flag)
        return
    if isinstance(value, list):
        for item in value:
            args.extend([flag, str(item)])
        return
    args.extend([flag, str(value)])


def build_wrapper_args(payload: dict[str, Any]) -> list[str]:
    tool = payload.get("tool")
    if not tool:
        raise ValueError("Payload requires a 'tool' value.")

    wrapper_args: list[str] = []
    if payload.get("dry_run", False):
        wrapper_args.append("--dry-run")

    global_options = dict(payload.get("global", {}))
    for key in ("select", "max_chars", "max_list"):
        append_option(wrapper_args, key, global_options.get(key))
    if global_options.get("raw"):
        wrapper_args.append("--raw")

    wrapper_args.append(str(tool))
    target_org = payload.get("target_org")
    if target_org and target_org != "ASK_USER_FOR_ALIAS":
        wrapper_args.extend(["--target-org", str(target_org)])

    options = dict(payload.get("options", {}))
    if tool == "safe-run":
        sf_args = options.pop("sf_args", [])
        for key, value in options.items():
            append_option(wrapper_args, key, value)
        wrapper_args.append("--")
        wrapper_args.extend(str(item) for item in sf_args)
        return wrapper_args

    for key, value in options.items():
        append_option(wrapper_args, key, value)
    return wrapper_args


def execute_payload(
    payload: dict[str, Any],
    root: Path,
    *,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    root = root.resolve()
    script = command_script(root)
    if not script.exists():
        return subprocess.CompletedProcess(
            [sys.executable, str(script)],
            1,
            "",
            "sf_agent_cli.py not found. Run `sfao install --project --platform all` first.\n",
        )
    args = [sys.executable, str(script), *build_wrapper_args(payload)]
    return subprocess.run(
        args,
        cwd=cwd or root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def example_payload(name: str, root: Path) -> dict[str, Any]:
    return payload_example(name, root=root)
