"""Salesforce Agent Optimizer package."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


PACKAGE_NAME = "salesforce-agent-optimizer"


def get_version() -> str:
    """Return the installed package version."""
    source_version = Path(__file__).resolve().parents[2] / "VERSION"
    if source_version.exists():
        return source_version.read_text(encoding="utf-8").strip()
    try:
        return version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "0.0.0+local"


__version__ = get_version()
