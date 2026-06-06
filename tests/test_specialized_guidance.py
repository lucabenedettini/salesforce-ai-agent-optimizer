from __future__ import annotations

import re
from pathlib import Path

from conftest import ROOT


TARGET_VERSION = "2.2.2"
SPECIALIZED_DIR = ROOT / "src" / "salesforce_agent_optimizer" / "templates" / "references" / "specialized-guidance"
TEMPLATE_REFERENCES = ROOT / "src" / "salesforce_agent_optimizer" / "templates" / "references"
REQUIRED_HEADINGS = [
    "## When To Read",
    "## Combine With Existing References",
    "## Non-Negotiable Checks",
    "## Minimal Planning Evidence",
    "## Preferred Approach",
    "## Validation Expectations",
    "## SFAO Command Hints",
    "## Mini-Rubric",
    "## Output Hint",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def specialized_area_files() -> list[Path]:
    return sorted(path for path in SPECIALIZED_DIR.glob("*.md") if path.name != "index.md")


def combine_with_section(text: str) -> str:
    match = re.search(
        r"(?ms)^## Combine With Existing References\s*(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1).strip() if match else ""


def markdown_reference_paths(text: str) -> set[str]:
    return set(re.findall(r"`(references/[^`]+?\.md)`", text))


def test_version_metadata_is_aligned_to_2_2_2() -> None:
    assert read(ROOT / "VERSION").strip() == TARGET_VERSION
    assert f'version = "{TARGET_VERSION}"' in read(ROOT / "pyproject.toml")
    assert f"version: {TARGET_VERSION}" in read(ROOT / "SKILL.md")
    assert f"## [{TARGET_VERSION}]" in read(ROOT / "CHANGELOG.md")


def test_agentforce_guidance_exists_and_has_required_sections() -> None:
    agentforce = SPECIALIZED_DIR / "agentforce.md"
    text = read(agentforce)
    assert agentforce.exists()
    for heading in REQUIRED_HEADINGS:
        assert heading in text
    assert "Agent/topic/action/prompt identified: yes/no" in text


def test_routing_and_index_include_agentforce() -> None:
    routing = read(TEMPLATE_REFERENCES / "routing.md")
    index = read(SPECIALIZED_DIR / "index.md")
    assert "references/specialized-guidance/agentforce.md" in routing
    assert "Agentforce" in routing
    assert "Agentforce" in index
    assert "Do not load this whole folder by default" in index


def test_specialized_guidance_files_have_required_structure_and_size() -> None:
    files = specialized_area_files()
    assert (SPECIALIZED_DIR / "agentforce.md") in files
    for path in files:
        text = read(path)
        for heading in REQUIRED_HEADINGS:
            assert heading in text, f"{path.name} missing {heading}"
        assert len(text.splitlines()) <= 220, f"{path.name} is too large"


def test_specialized_guidance_reference_paths_exist() -> None:
    for path in specialized_area_files():
        section = combine_with_section(read(path))
        assert section, f"{path.name} missing Combine With section"
        for reference in markdown_reference_paths(section):
            assert (ROOT / reference).exists(), f"{path.name} links missing root {reference}"
            assert (TEMPLATE_REFERENCES.parent / reference).exists(), (
                f"{path.name} links missing template {reference}"
            )


def test_routing_reference_paths_exist() -> None:
    for routing in (ROOT / "references" / "routing.md", TEMPLATE_REFERENCES / "routing.md"):
        base = ROOT if routing.parts[-3:] != ("templates", "references", "routing.md") else TEMPLATE_REFERENCES.parent
        for reference in markdown_reference_paths(read(routing)):
            assert (base / reference).exists(), f"{routing} links missing {reference}"


def test_specialized_guidance_preserves_guardrails_and_external_boundary() -> None:
    skill_suffix = "sf" + "-skills"
    prohibited = [
        "forcedotcom/" + skill_suffix,
        skill_suffix,
        "bypass SFAO guardrails",
        "ignore SFAO guardrails",
        "skip SFAO guardrails",
        "automatic install of external skills",
        "install external skills automatically",
    ]
    for path in specialized_area_files():
        text = read(path)
        for phrase in prohibited:
            assert phrase not in text, f"{path.name} contains prohibited phrase {phrase}"
