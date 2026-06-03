#!/usr/bin/env python3
"""Build release ZIP, checksums, and manifest for Salesforce Agent Optimizer."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SKILL_NAME = "salesforce-agent-optimizer"


def read_version() -> str:
    return (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_skill_zip(version: str) -> Path:
    template_root = ROOT / "src" / "salesforce_agent_optimizer" / "templates"
    zip_path = DIST / f"salesforce-agent-optimizer-{version}-skill.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(template_root.rglob("*")):
            if path.is_file():
                relative = path.relative_to(template_root).as_posix()
                archive.write(path, f"{SKILL_NAME}/{relative}")
    return zip_path


def build_manifest(version: str, artifacts: list[Path]) -> Path:
    payload = {
        "name": "salesforce-agent-optimizer",
        "version": version,
        "min_python": "3.10",
        "supported_installers": ["uv", "pipx", "pip"],
        "supported_agents": ["codex", "claude", "copilot"],
        "supported_platforms": ["windows", "macos", "linux"],
        "commands": ["sfao install", "sfao doctor", "sfao validate"],
        "skill_paths": {
            "codex_repo": ".agents/skills/salesforce-agent-optimizer",
            "codex_user": "$HOME/.agents/skills/salesforce-agent-optimizer",
            "claude_repo": ".claude/skills/salesforce-agent-optimizer",
            "copilot_repo": ".github",
        },
        "artifacts": [
            {
                "file": artifact.name,
                "sha256": sha256(artifact),
                "size": artifact.stat().st_size,
            }
            for artifact in artifacts
        ],
    }
    path = DIST / "release-manifest.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_checksums(artifacts: list[Path]) -> Path:
    path = DIST / "SHA256SUMS"
    lines = [f"{sha256(artifact)}  {artifact.name}" for artifact in sorted(artifacts)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def main() -> int:
    DIST.mkdir(exist_ok=True)
    version = read_version()
    skill_zip = build_skill_zip(version)
    artifacts = sorted(path for path in DIST.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if skill_zip not in artifacts:
        artifacts.append(skill_zip)
    manifest = build_manifest(version, artifacts)
    checksums = write_checksums(sorted(artifacts + [manifest]))
    print(f"Built {skill_zip.relative_to(ROOT)}")
    print(f"Built {manifest.relative_to(ROOT)}")
    print(f"Built {checksums.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
