from __future__ import annotations

import re
from pathlib import Path

from conftest import ROOT

from salesforce_agent_optimizer.validation import (
    ValidationResult,
    validate_destructive_hints,
    validate_no_broad_specialized_loading,
    validate_no_guardrail_bypass,
    validate_routing_references,
    validate_sfao_command_hints,
    validate_specialized_guidance_directory,
)


TARGET_VERSION = "2.2.3"
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


def guidance_text(command_hint: str = "- `sfao validate`") -> str:
    return (
        "# Test Guidance\n\n"
        "## When To Read\n\nUse for tests.\n\n"
        "## Combine With Existing References\n\n"
        "- `references/privacy-security.md`\n\n"
        "## Non-Negotiable Checks\n\n- Keep guardrails.\n\n"
        "## Minimal Planning Evidence\n\n- Evidence.\n\n"
        "## Preferred Approach\n\n- Minimal.\n\n"
        "## Validation Expectations\n\n- Validate.\n\n"
        "## SFAO Command Hints\n\n"
        f"{command_hint}\n\n"
        "## Mini-Rubric\n\n- Safe: yes/no\n\n"
        "## Output Hint\n\nState concise evidence.\n"
    )


def test_unknown_sfao_command_hint_fails_validation() -> None:
    result = ValidationResult()
    validate_sfao_command_hints(
        guidance_text("- `sfao magic-optimize --all`"),
        Path("references/specialized-guidance/test.md"),
        result,
    )
    assert not result.ok
    assert "unknown sfao command: magic-optimize" in "\n".join(result.errors)


def test_valid_sfao_command_hints_pass_validation() -> None:
    result = ValidationResult()
    validate_sfao_command_hints(
        guidance_text(
            "- `sfao knowledge refresh --project-root .`\n"
            "- `sfao report --project-root .`\n"
            "- `sfao command search \"deploy\" --toolset deploy`"
        ),
        Path("references/specialized-guidance/test.md"),
        result,
    )
    assert result.ok, result.to_dict()


def test_destructive_command_hint_without_approval_fails_validation() -> None:
    result = ValidationResult()
    validate_destructive_hints(
        guidance_text(
            "- `python scripts/sf_agent_cli.py data-record-delete --target-org dev "
            "--sobject Account --record-id 001`"
        ),
        Path("references/specialized-guidance/test.md"),
        result,
    )
    assert not result.ok
    assert "destructive command hints without approval wording" in "\n".join(result.errors)


def test_destructive_command_hint_with_approval_passes_validation() -> None:
    result = ValidationResult()
    validate_destructive_hints(
        guidance_text(
            "- `python scripts/sf_agent_cli.py data-record-delete --target-org dev "
            "--sobject Account --record-id 001 --delete-approval "
            "\"I explicitly approve this deletion\"`"
        ),
        Path("references/specialized-guidance/test.md"),
        result,
    )
    assert result.ok, result.to_dict()


def test_routing_path_references_must_exist(tmp_path: Path) -> None:
    references = tmp_path / "references"
    references.mkdir()
    (references / "routing.md").write_text(
        (
            "| Request signal | Read these files |\n"
            "| --- | --- |\n"
            "| Agentforce | `references/specialized-guidance/agentforce.md`, "
            "`references/missing.md` |\n"
        ),
        encoding="utf-8",
    )
    guidance = references / "specialized-guidance"
    guidance.mkdir()
    (guidance / "agentforce.md").write_text("# Agentforce\n", encoding="utf-8")

    result = ValidationResult()
    validate_routing_references(tmp_path, result)

    assert not result.ok
    assert "references missing file: references/missing.md" in "\n".join(result.errors)


def test_guidance_cannot_instruct_bypassing_sfao_guardrails() -> None:
    result = ValidationResult()
    validate_no_guardrail_bypass(
        "Do not skip SFAO guardrails.",
        Path("references/specialized-guidance/test.md"),
        result,
    )
    assert not result.ok
    assert "skip SFAO guardrails" in "\n".join(result.errors)


def test_routing_cannot_load_all_specialized_guidance_by_default() -> None:
    result = ValidationResult()
    validate_no_broad_specialized_loading(
        "For every request, read all specialized guidance before planning.",
        Path("references/routing.md"),
        result,
    )
    assert not result.ok
    assert "load too much specialized guidance" in "\n".join(result.errors)


def test_specialized_guidance_directory_enforces_line_threshold(tmp_path: Path) -> None:
    references = tmp_path / "references"
    guidance = references / "specialized-guidance"
    guidance.mkdir(parents=True)
    (references / "privacy-security.md").write_text("# Privacy\n", encoding="utf-8")
    (guidance / "index.md").write_text(
        (
            "# Index\n\n"
            "Agentforce guidance: `agentforce.md`.\n"
            "Do not load this whole folder by default.\n"
            "Core SFAO safety always wins.\n"
        ),
        encoding="utf-8",
    )
    oversized = guidance_text() + "\n".join("- filler" for _ in range(230)) + "\n"
    (guidance / "agentforce.md").write_text(oversized, encoding="utf-8")

    result = ValidationResult()
    validate_specialized_guidance_directory(
        guidance,
        references,
        result,
        "references/specialized-guidance",
    )

    assert not result.ok
    assert "exceeds 220 lines" in "\n".join(result.errors)


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
