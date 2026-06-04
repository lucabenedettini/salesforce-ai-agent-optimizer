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

import salesforce_agent_optimizer.validation as validation_module
from salesforce_agent_optimizer import __version__
from salesforce_agent_optimizer.installer import SECTION_BEGIN, SECTION_END, install, uninstall, update
from salesforce_agent_optimizer.validation import (
    GENERATED_MARKER,
    ValidationResult,
    parse_frontmatter,
    validate_generated_sync,
    validate_salesforce_metadata,
    validate_source_tree,
)


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


def test_readmes_document_main_sfao_commands_without_maintainer_noise() -> None:
    readmes = [
        ROOT / "README.md",
        ROOT / "README.it.md",
        ROOT / "README.es.md",
        ROOT / "README.zh-CN.md",
    ]
    required_commands = [
        "sfao version",
        "sfao install --project --platform all",
        "sfao install --project --platform codex",
        "sfao install --project --platform claude",
        "sfao install --project --platform copilot",
        "sfao update --project --platform all",
        "sfao uninstall --project --platform all --yes",
        "sfao doctor",
        "sfao doctor --verbose",
        "sfao doctor --json",
        "sfao validate",
        "sfao validate --verbose",
        "sfao validate --json",
        "sfao knowledge init --project-root .",
        "sfao knowledge refresh --project-root .",
        "sfao knowledge doctor --project-root .",
        "sfao version-context scaffold",
        "sfao version-context update",
        "sfao version-context validate",
    ]
    maintainer_only_fragments = [
        "python -m build",
        "python -m pytest",
        "python scripts/self_test.py",
        "python scripts/sync_agent_instructions.py",
        "python scripts/validate_skill.py",
        "python -m twine",
        "git tag v",
    ]
    for path in readmes:
        readme = path.read_text(encoding="utf-8")
        for command in required_commands:
            assert command in readme, f"{path.name} missing {command}"
        for fragment in maintainer_only_fragments:
            assert fragment not in readme, f"{path.name} contains maintainer-only {fragment}"


def test_sfao_version() -> None:
    completed = run_cli(["version"], ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "salesforce-agent-optimizer 1.1.0" in completed.stdout


def test_sfao_validate_and_doctor() -> None:
    validate = run_cli(["validate", "--json", "--root", str(ROOT)], ROOT)
    assert validate.returncode == 0, validate.stdout + validate.stderr
    assert json.loads(validate.stdout)["ok"]

    doctor = run_cli(["doctor", "--json", "--root", str(ROOT)], ROOT)
    assert doctor.returncode == 0, doctor.stdout + doctor.stderr
    payload = json.loads(doctor.stdout)
    assert payload["Core"][0]["detail"].endswith("v1.1.0")

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
        tmp_path / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        tmp_path / ".github" / "copilot-instructions.md",
        tmp_path / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
        tmp_path / "evals" / "salesforce-agent-optimizer-trigger-evals.json",
    ]
    for path in expected:
        assert path.exists(), path
        if path.suffix != ".json":
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
    assert (copilot / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md").exists()
    assert (copilot / ".github" / "copilot-instructions.md").exists()


def test_existing_non_generated_files_are_not_overwritten(tmp_path: Path) -> None:
    target = tmp_path / "AGENTS.md"
    target.write_text("user content\n", encoding="utf-8", newline="\n")
    report = install(tmp_path, project=True, platform="copilot")
    assert report.ok
    assert not report.skipped
    text = target.read_text(encoding="utf-8")
    assert "user content\n" in text
    assert GENERATED_MARKER in text
    assert SECTION_BEGIN in text
    assert SECTION_END in text


def test_existing_copilot_files_are_merged_and_updated(tmp_path: Path) -> None:
    agents = tmp_path / "agent.md"
    copilot = tmp_path / ".github" / "copilot-instructions.md"
    copilot.parent.mkdir(parents=True)
    agents.write_text("existing agent guidance\n", encoding="utf-8", newline="\n")
    copilot.write_text("existing copilot guidance\n", encoding="utf-8", newline="\n")

    report = install(tmp_path, project=True, platform="copilot")
    assert report.ok, report.to_dict()
    assert (tmp_path / "evals" / "salesforce-agent-optimizer-trigger-evals.json").exists()
    for path, existing in (
        (agents, "existing agent guidance"),
        (copilot, "existing copilot guidance"),
    ):
        text = path.read_text(encoding="utf-8")
        assert existing in text
        assert "Salesforce Agent Optimizer" in text
        assert SECTION_BEGIN in text
        assert SECTION_END in text

    update_report = update(tmp_path, project=True, platform="copilot")
    assert update_report.ok, update_report.to_dict()
    assert "existing copilot guidance" in copilot.read_text(encoding="utf-8")


def test_update_installs_new_missing_managed_templates(tmp_path: Path) -> None:
    report = install(tmp_path, project=True, platform="copilot")
    assert report.ok, report.to_dict()
    eval_file = tmp_path / "evals" / "salesforce-agent-optimizer-trigger-evals.json"
    copilot_skill = tmp_path / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md"
    eval_file.unlink()
    copilot_skill.unlink()

    update_report = update(tmp_path, project=True, platform="copilot")

    assert update_report.ok, update_report.to_dict()
    assert eval_file.exists()
    assert copilot_skill.exists()
    assert any(path.endswith("salesforce-agent-optimizer-trigger-evals.json") for path in update_report.installed)
    assert any(path.endswith(".github/skills/salesforce-agent-optimizer/SKILL.md") for path in update_report.installed)


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
    install(tmp_path, project=True, platform="copilot")
    report = uninstall(tmp_path, project=True, platform="copilot", yes=True)
    assert report.ok
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "user content\n"


def test_versions_align() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^version = "1\.1\.0"$', pyproject, re.MULTILINE)
    skill_data, _, _ = parse_frontmatter(ROOT / "SKILL.md")
    assert skill_data["metadata"]["version"] == version
    codex_data, _, _ = parse_frontmatter(
        ROOT / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md"
    )
    assert codex_data["metadata"]["version"] == version
    copilot_data, _, _ = parse_frontmatter(
        ROOT / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md"
    )
    assert copilot_data["metadata"]["version"] == version


def test_source_generated_files_have_markers() -> None:
    files = [
        ROOT / "AGENTS.md",
        ROOT / ".agents" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        ROOT / ".claude" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        ROOT / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md",
        ROOT / ".github" / "copilot-instructions.md",
        ROOT / ".github" / "instructions" / "salesforce-agent-optimizer.instructions.md",
    ]
    for path in files:
        assert GENERATED_MARKER in path.read_text(encoding="utf-8")


def test_copilot_instructions_enforce_mandatory_phase_gates() -> None:
    text = "\n".join(
        [
            (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8"),
            (
                ROOT / ".github" / "skills" / "salesforce-agent-optimizer" / "SKILL.md"
            ).read_text(encoding="utf-8"),
        ]
    )
    required = [
        "Copilot compliance gate",
        "Do not inspect raw Salesforce metadata",
        "Do not skip directly to metadata parsing",
        "references/routing.md",
        ".salesforce-agent-knowledge/markdown-index.md",
        ".salesforce-agent-knowledge/index.json",
        "Request review",
        "Planning evidence",
        "Mandatory phase gates",
        "metadata information",
        "bugfix",
        "new metadata implementation",
        "approval gate",
        "Implementation: not required",
        "validate before final response",
        "Stop after three unsuccessful cycles",
        "release notes",
        "technical specifications",
        "impact assessment",
        "user testing",
        "manual procedures",
        "multi-country",
        "multi-currency",
        "Advanced Currency Management",
        "Minimum visible response skeleton",
        "Approval",
        "Completion",
    ]
    for phrase in required:
        assert phrase in text


def test_salesforce_micro_validators_warn_on_risky_metadata(tmp_path: Path) -> None:
    (tmp_path / "sfdx-project.json").write_text('{"packageDirectories":[]}\n', encoding="utf-8")
    classes = tmp_path / "force-app" / "main" / "default" / "classes"
    flows = tmp_path / "force-app" / "main" / "default" / "flows"
    permissions = tmp_path / "force-app" / "main" / "default" / "permissionsets"
    manifest = tmp_path / "manifest"
    for directory in (classes, flows, permissions, manifest):
        directory.mkdir(parents=True)
    (classes / "InvoiceService.cls").write_text(
        "public without sharing class InvoiceService { public void run(){ System.debug('x'); } }\n",
        encoding="utf-8",
    )
    (classes / "InvoiceService.cls-meta.xml").write_text(
        "<ApexClass><apiVersion>67.0</apiVersion><status>Active</status></ApexClass>\n",
        encoding="utf-8",
    )
    (flows / "Invoice.flow-meta.xml").write_text(
        "<Flow><status>Active</status></Flow>\n",
        encoding="utf-8",
    )
    (permissions / "Risk.permissionset-meta.xml").write_text(
        (
            "<PermissionSet>"
            "<userPermissions><name>ModifyAllData</name><enabled>true</enabled></userPermissions>"
            "<objectPermissions><object>Invoice__c</object><allowDelete>true</allowDelete>"
            "</objectPermissions></PermissionSet>\n"
        ),
        encoding="utf-8",
    )
    (manifest / "package.xml").write_text(
        "<Package><types><members>*</members><name>ApexClass</name></types></Package>\n",
        encoding="utf-8",
    )
    (manifest / "destructiveChanges.xml").write_text("<Package></Package>\n", encoding="utf-8")

    result = ValidationResult()
    validate_salesforce_metadata(tmp_path, result)

    assert result.ok, result.to_dict()
    warnings = "\n".join(result.warnings)
    assert "without sharing" in warnings
    assert "System.debug" in warnings
    assert "no obvious matching test class" in warnings
    assert "Flow is Active" in warnings
    assert "High-risk user permission enabled (ModifyAllData)" in warnings
    assert "allowDelete" in warnings
    assert "wildcard member" in warnings
    assert "Destructive metadata file requires separate explicit user approval" in warnings


def test_salesforce_micro_validators_error_on_broken_metadata(tmp_path: Path) -> None:
    (tmp_path / "sfdx-project.json").write_text('{"packageDirectories":[]}\n', encoding="utf-8")
    trigger_dir = tmp_path / "force-app" / "main" / "default" / "triggers"
    lwc_dir = tmp_path / "force-app" / "main" / "default" / "lwc" / "brokenCard"
    manifest = tmp_path / "manifest"
    trigger_dir.mkdir(parents=True)
    lwc_dir.mkdir(parents=True)
    manifest.mkdir()
    (trigger_dir / "InvoiceTrigger.trigger").write_text(
        "trigger InvoiceTrigger on Invoice__c (before insert) {}\n",
        encoding="utf-8",
    )
    (lwc_dir / "brokenCard.js").write_text("export default class BrokenCard {}\n", encoding="utf-8")
    (manifest / "package.xml").write_text("<Package>\n", encoding="utf-8")

    result = ValidationResult()
    validate_salesforce_metadata(tmp_path, result)

    assert not result.ok
    errors = "\n".join(result.errors)
    assert "Apex trigger missing metadata file" in errors
    assert "LWC component missing js-meta.xml" in errors
    assert "Invalid package.xml XML" in errors


def test_source_validation_catches_text_shape() -> None:
    result = validate_source_tree(ROOT)
    assert result.ok, result.to_dict()


def test_generated_sync_validation_without_pyyaml(monkeypatch) -> None:
    monkeypatch.setattr(validation_module, "yaml", None)
    result = ValidationResult()
    validate_generated_sync(ROOT, result)
    assert result.ok, result.to_dict()
    assert not result.warnings


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
        "salesforce_agent_optimizer/templates/evals/trigger-evals.json",
        "salesforce_agent_optimizer/templates/references/routing.md",
        "salesforce_agent_optimizer/templates/scripts/sf_agent_cli.py",
        "salesforce_agent_optimizer/templates/codex/SKILL.md",
        "salesforce_agent_optimizer/templates/claude/SKILL.md",
        "salesforce_agent_optimizer/templates/github/skills/salesforce-agent-optimizer/SKILL.md",
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
    assert manifest["version"] == "1.1.0"
    assert "sfao update" in manifest["commands"]
    assert "sfao uninstall" in manifest["commands"]
    assert manifest["skill_paths"]["copilot_repo_skill"] == ".github/skills/salesforce-agent-optimizer"
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
