from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

from salesforce_agent_optimizer.report import generate_report


def run_cli(args: list[str], cwd: Path, path_value: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    if path_value is not None:
        env["PATH"] = path_value
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


def test_sfao_report_creates_default_markdown(tmp_path: Path) -> None:
    completed = run_cli(["report", "--project-root", str(tmp_path)], ROOT)

    assert completed.returncode == 0, completed.stdout + completed.stderr
    report = tmp_path / ".salesforce-agent-knowledge" / "reports" / "sfao-report.md"
    assert report.exists()
    text = report.read_text(encoding="utf-8")
    for section in (
        "# Salesforce Agent Optimizer Report",
        "## Summary",
        "## Version",
        "## Installation Status",
        "## Knowledge Status",
        "## Memory Status",
        "## Guardrails",
        "## Specialized Guidance",
        "## Eval Coverage",
        "## Version Context",
        "## Warnings",
        "## Suggested Commands",
    ):
        assert section in text
    assert "Generated SFAO report:" in completed.stdout


def test_sfao_report_writes_requested_output(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "custom.md"
    result = generate_report(tmp_path, output=output)

    assert result.ok, result.to_dict()
    assert output.exists()
    assert "## Summary" in output.read_text(encoding="utf-8")


def test_sfao_report_works_when_knowledge_is_missing(tmp_path: Path) -> None:
    result = generate_report(tmp_path)
    text = result.output_path.read_text(encoding="utf-8")

    assert result.ok, result.to_dict()
    assert "- Initialized: `no`" in text
    assert "sfao knowledge init --project-root ." in text


def test_sfao_report_detects_missing_memory(tmp_path: Path) -> None:
    result = generate_report(tmp_path)
    text = result.output_path.read_text(encoding="utf-8")

    assert result.ok, result.to_dict()
    assert "- Memory file: `missing`" in text
    assert "sfao memory init --project-root ." in text


def test_sfao_report_lists_static_guardrails(tmp_path: Path) -> None:
    result = generate_report(tmp_path)
    text = result.output_path.read_text(encoding="utf-8")

    assert result.ok, result.to_dict()
    assert "Explicit org alias before org access: active" in text
    assert "Production read-only for write/execute: active" in text
    assert "Destructive operation approval: active" in text
    assert "`safe-run --safety` cannot downgrade automatic classification: active" in text


def test_sfao_report_lists_specialized_guidance_from_project_references(tmp_path: Path) -> None:
    guidance = tmp_path / "references" / "specialized-guidance"
    guidance.mkdir(parents=True)
    for filename in (
        "apex.md",
        "lwc.md",
        "flow.md",
        "soql.md",
        "deploy.md",
        "data-operations.md",
        "agentforce.md",
        "index.md",
    ):
        (guidance / filename).write_text("# Guidance\n", encoding="utf-8")

    result = generate_report(tmp_path)
    text = result.output_path.read_text(encoding="utf-8")

    assert result.ok, result.to_dict()
    assert "| Agentforce | present |" in text
    assert "| Data operations | present |" in text


def test_sfao_report_lists_existing_eval_coverage_only(tmp_path: Path) -> None:
    evals = tmp_path / "evals"
    evals.mkdir()
    (evals / "salesforce-agent-optimizer-quality-evals.json").write_text(
        '{"examples":[{"prompt":"p"},{"prompt":"q"}]}\n',
        encoding="utf-8",
    )

    result = generate_report(tmp_path)
    text = result.output_path.read_text(encoding="utf-8")

    assert result.ok, result.to_dict()
    assert "| evals/salesforce-agent-optimizer-quality-evals.json | present | 2 |" in text
    assert "| evals/salesforce-agent-optimizer-trigger-evals.json | missing | 0 |" in text


def test_sfao_report_does_not_require_salesforce_cli(tmp_path: Path) -> None:
    completed = run_cli(["report", "--project-root", str(tmp_path)], ROOT, path_value="")

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (tmp_path / ".salesforce-agent-knowledge" / "reports" / "sfao-report.md").exists()


def test_sfao_report_does_not_modify_existing_knowledge_or_memory(tmp_path: Path) -> None:
    knowledge = tmp_path / ".salesforce-agent-knowledge"
    history = knowledge / "history"
    history.mkdir(parents=True)
    files = {
        knowledge / "index.md": "# Index\n",
        knowledge / "config.json": "{}\n",
        history / "project-history.md": "# History\n",
        knowledge / "memory.md": (
            "# Salesforce Agent Project Memory\n\n"
            "## Current Project Facts\n- A\n"
            "## Durable Decisions\n- A\n"
            "## Recent Bugfixes\n- A\n"
            "## Recent Developments\n- A\n"
            "## Validation Lessons\n- A\n"
            "## Risks And Follow-ups\n- A\n"
            "## Deprecated Or Superseded Notes\n- A\n"
        ),
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    before = {path: path.read_text(encoding="utf-8") for path in files}

    result = generate_report(tmp_path)

    assert result.ok, result.to_dict()
    after = {path: path.read_text(encoding="utf-8") for path in files}
    assert after == before
