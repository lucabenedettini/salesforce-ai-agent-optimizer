from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from conftest import ROOT

from salesforce_agent_optimizer import __version__
from salesforce_agent_optimizer.installer import install, uninstall, update
from salesforce_agent_optimizer.validation import GENERATED_MARKER, parse_frontmatter, validate_source_tree


def run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    src = str(ROOT / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "salesforce_agent_optimizer.cli", *args],
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def test_package_import_and_version() -> None:
    assert __version__ == (ROOT / "VERSION").read_text(encoding="utf-8").strip()


def test_cli_entry_point_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'sfao = "salesforce_agent_optimizer.cli:main"' in pyproject


def test_sfao_version() -> None:
    completed = run_cli(["version"], ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "salesforce-agent-optimizer 1.0.0" in completed.stdout


def test_sfao_validate_and_doctor() -> None:
    validate = run_cli(["validate", "--json", "--root", str(ROOT)], ROOT)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert json.loads(validate.stdout)["ok"]

    doctor = run_cli(["doctor", "--json", "--root", str(ROOT)], ROOT)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    payload = json.loads(doctor.stdout)
    assert payload["Core"][0]["detail"].endswith("v1.0.0")

    compact = run_cli(["doctor", "--root", str(ROOT)], ROOT)
    assert compact.returncode == 0, compact.stdout + compact.stderr
    assert "Use --verbose" in compact.stdout


def test_sfao_install_project_all_and_validate(tmp_path: Path) -> None:
    completed = run_cli(["install", "--project", "--platform", "all"], tmp_path)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    expected = [
        tmp_path / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        tmp_path / ".claude" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        tmp_path / "AGENTS.md",
        tmp_path / ".github" / "copilot-instructions.md",
        tmp_path / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
    ]
    for path in expected:
        assert path.exists(), path
        assert GENERATED_MARKER in path.read_text(encoding="utf-8")
        assert b"\r\n" not in path.read_bytes()
    validate = run_cli(["validate", "--json"], tmp_path)
    assert validate.returncode == 0, validate.stdout + validate.stderr


def test_sfao_install_individual_platforms(tmp_path: Path) -> None:
    codex = tmp_path / "codex"
    claude = tmp_path / "claude"
    copilot = tmp_path / "copilot"
    codex.mkdir()
    claude.mkdir()
    copilot.mkdir()
    assert run_cli(["install", "--project", "--platform", "codex"], codex).returncode == 0
    assert (codex / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md").exists()
    assert run_cli(["install", "--project", "--platform", "claude"], claude).returncode == 0
    assert (claude / ".claude" / "skills" / "salesforce-agent-optimizer" / "SKILL.md").exists()
    assert run_cli(["install", "--project", "--platform", "copilot"], copilot).returncode == 0
    assert (copilot / ".github" / "copilot-instructions.md").exists()


def test_existing_non_generated_files_are_not_overwritten(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("user content\n", encoding="utf-8", newline="\n")
    report = install(tmp_path, project=True, platform="copilot")
    assert report.ok
    assert report.skipped
    assert target.read_text(encoding="utf-8") == "user content\n"


def test_update_updates_generated_files_and_skips_user_edits(tmp_path: Path) -> None:
    report = install(tmp_path, project=True, platform="copilot")
    assert report.ok
    generated = tmp_path / ".github" / "copilot-instructions.md"
    original = generated.read_text(encoding="utf-8")
    generated.write_text(original + "\n<!-- local edit -->\n", encoding="utf-8", newline="\n")
    update_report = update(tmp_path, project=True, platform="copilot")
    assert update_report.ok
    assert any("local edits" in warning for warning in update_report.warnings)
    assert "<!-- local edit -->" in generated.read_text(encoding="utf-8")


def test_uninstall_removes_only_generated_files(tmp_path: Path) -> None:
    install(tmp_path, project=True, platform="all")
    user_file = tmp_path / ".github" / "USER.md"
    user_file.write_text("keep me\n", encoding="utf-8", newline="\n")
    report = uninstall(tmp_path, project=True, platform="all", yes=True)
    assert report.ok, report.to_dict()
    assert not (tmp_path / "AGENTS.md").exists()
    assert not (tmp_path / ".agents" / "skills" / "salesforce-agent-optimizer").exists()
    assert user_file.exists()
    assert (tmp_path / ".github").exists()


def test_uninstall_skips_non_generated_files(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("user content\n", encoding="utf-8", newline="\n")
    report = uninstall(tmp_path, project=True, platform="copilot", yes=True)
    assert report.ok
    assert target.exists()
    assert report.skipped


def test_versions_align() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version = "1\.0\.0"$', pyproject, re.MULTILINE)
    skill_data, _, _ = parse_frontmatter(ROOT / "SKILL.md")
    assert skill_data["metadata"]["version"] == version
    codex_data, _, _ = parse_frontmatter(
        ROOT / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md"
    )
    assert codex_data["metadata"]["version"] == version


def test_source_generated_files_have_markers() -> None:
    files = [
        ROOT / "AGENTS.md",
        ROOT / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        ROOT / ".claude" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        ROOT / ".github" / "copilot-instructions.md",
        ROOT / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
    ]
    for path in files:
        assert GENERATED_MARKER in path.read_text(encoding="utf-8")


def test_source_validation_catches_text_shape() -> None:
    result = validate_source_tree(ROOT)
    assert result.ok, result.to_dict()


def test_wheel_includes_templates(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    completed = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    wheels = list(dist.glob("*.whl"))
    assert len(wheels) == 1
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())
    required = {
        "salesforce_agent_optimizer/templates/SKILL.md",
        "salesforce_agent_optimizer/templates/AGENTS.md",
        "salesforce_agent_optimizer/templates/agents/openai.yaml",
        "salesforce_agent_optimizer/templates/references/routing.md",
        "salesforce_agent_optimizer/templates/scripts/sf_agent_cli.py",
        "salesforce_agent_optimizer/templates/codex/SKILL.md",
        "salesforce_agent_optimizer/templates/claude/SKILL.md",
        "salesforce_agent_optimizer/templates/github/copilot-instructions.md",
        "salesforce_agent_optimizer/templates/github/instructions/salesforce-agent-optimizer.instructions.md",
    }
    assert required <= names


def test_knowledge_commands(tmp_path: Path) -> None:
    source = ROOT / "tests" / "fixtures" / "sfdx-project"
    project = tmp_path / "sfdx-project"
    shutil.copytree(source, project)
    init = run_cli(["knowledge", "init", "--project-root", str(project), "--json"], ROOT)
    assert init.returncode == 0, init.stdout + init.stderr
    payload = json.loads(init.stdout)
    assert payload["entry_count"] >= 3
    assert (project / ".salesforce-agent-knowledge" / "index.json").exists()
    refresh = run_cli(["knowledge", "refresh", "--project-root", str(project)], ROOT)
    assert refresh.returncode == 0, refresh.stdout + refresh.stderr
    doctor = run_cli(["knowledge", "doctor", "--project-root", str(project), "--json"], ROOT)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    assert json.loads(doctor.stdout)["ok"]


def test_version_context_commands(tmp_path: Path) -> None:
    scaffold = run_cli(["version-context", "scaffold", "--root", str(tmp_path), "--json"], ROOT)
    assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr
    update_result = run_cli(
        ["version-context", "update", "--root", str(tmp_path), "--offline", "--json"],
        ROOT,
    )
    assert update_result.returncode == 0, update_result.stdout + update_result.stderr
    validate = run_cli(["version-context", "validate", "--root", str(tmp_path), "--json"], ROOT)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert json.loads(validate.stdout)["ok"]


def test_release_manifest_and_workflow_requirements() -> None:
    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    completed = subprocess.run(
        [sys.executable, "scripts/build_release_artifacts.py"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    manifest = json.loads((dist / "release-manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == "1.0.0"
    assert "sfao update" in manifest["commands"]
    assert "sfao uninstall" in manifest["commands"]
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "PUBLISH_TO_PYPI" in workflow
    assert "PYPI_API_TOKEN" not in workflow
    assert "id-token: write" in workflow
    assert "name: pypi" in workflow
    assert "python-package-distributions" in workflow


def test_validate_json_is_compact() -> None:
    completed = run_cli(["validate", "--json", "--root", str(ROOT)], ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "\n  " not in completed.stdout
