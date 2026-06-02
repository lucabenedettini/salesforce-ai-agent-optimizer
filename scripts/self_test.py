#!/usr/bin/env python3
"""Cross-platform local tests for Salesforce Agent Optimizer scripts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run(command: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    if check and completed.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(command)}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}")
    return completed


def make_salesforce_project(root: Path) -> None:
    classes = root / "force-app" / "main" / "default" / "classes"
    account = root / "force-app" / "main" / "default" / "objects" / "Account"
    fields = account / "fields"
    classes.mkdir(parents=True)
    fields.mkdir(parents=True)
    (classes / "AccountService.cls").write_text(
        "public with sharing class AccountService { "
        "@AuraEnabled public static void touchIt() { "
        "List<Account> a = [SELECT Id FROM Account LIMIT 1]; } }",
        encoding="utf-8",
    )
    (account / "Account.object-meta.xml").write_text(
        "<CustomObject xmlns='http://soap.sforce.com/2006/04/metadata'><label>Account</label></CustomObject>",
        encoding="utf-8",
    )
    (fields / "Priority__c.field-meta.xml").write_text(
        "<CustomField xmlns='http://soap.sforce.com/2006/04/metadata'>"
        "<fullName>Priority__c</fullName><label>Priority</label><type>Text</type>"
        "</CustomField>",
        encoding="utf-8",
    )


def test_init_generates_metadata_docs() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        make_salesforce_project(root)
        run([PYTHON, str(ROOT / "scripts" / "sf_knowledge_init.py"), "--project-root", str(root), "--refresh"])
        knowledge = root / ".salesforce-agent-knowledge"
        metadata_docs = list((knowledge / "metadata").rglob("*.md"))
        checks = {
            "metadata_doc_count": len(metadata_docs),
            "markdown_index": (knowledge / "markdown-index.md").exists(),
            "history": (knowledge / "history" / "project-history.md").exists(),
            "index_links_metadata": "metadata/" in (knowledge / "index.md").read_text(encoding="utf-8"),
        }
        assert checks["metadata_doc_count"] == 3
        assert checks["markdown_index"]
        assert checks["history"]
        assert checks["index_links_metadata"]
        return checks


def test_history_records_requirements_and_metadata() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        run(
            [
                PYTHON,
                str(ROOT / "scripts" / "knowledge_history.py"),
                "--project-root",
                tmp,
                "--action",
                "deploy",
                "--requirements",
                "Add priority tracking to Account",
                "--metadata",
                "CustomField:Account.Priority__c",
                "--metadata",
                "PermissionSet:Sales_User",
                "--target-org",
                "dev-sandbox",
                "--result",
                "deploy succeeded",
            ]
        )
        knowledge = Path(tmp) / ".salesforce-agent-knowledge"
        history = (knowledge / "history" / "project-history.md").read_text(encoding="utf-8")
        events = list((knowledge / "history" / "events").glob("*.md"))
        checks = {
            "event_count": len(events),
            "has_requirement": "Add priority tracking" in history,
            "has_metadata": "CustomField:Account.Priority__c" in history,
        }
        assert checks["event_count"] == 1
        assert checks["has_requirement"]
        assert checks["has_metadata"]
        return checks


def test_agent_cli_guardrails() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        missing = run(
            [
                PYTHON,
                str(ROOT / "scripts" / "sf_agent_cli.py"),
                "deploy-start",
                "--target-org",
                "dev",
                "--source-dir",
                "force-app",
            ],
            cwd=root,
            check=False,
        )
        assert missing.returncode != 0
        assert "Deploy requires --requirements" in (missing.stdout + missing.stderr)

        dry_run = run(
            [
                PYTHON,
                str(ROOT / "scripts" / "sf_agent_cli.py"),
                "deploy-start",
                "--target-org",
                "dev",
                "--source-dir",
                "force-app",
                "--requirements",
                "Add priority tracking",
                "--changed-metadata",
                "CustomField:Account.Priority__c",
                "--dry-run",
            ],
            cwd=root,
        )
        assert '"dry_run": true' in dry_run.stdout
        assert not (root / ".salesforce-agent-knowledge").exists()

        no_alias = run(
            [
                PYTHON,
                str(ROOT / "scripts" / "sf_agent_cli.py"),
                "safe-run",
                "--",
                "data",
                "query",
                "--query",
                "SELECT Id FROM Account LIMIT 1",
                "--dry-run",
            ],
            cwd=root,
            check=False,
        )
        assert no_alias.returncode != 0
        assert "Ask the user for the Salesforce org alias" in (no_alias.stdout + no_alias.stderr)
        return {"missing_history_details_blocked": True, "dry_run_no_history": True, "missing_alias_blocked": True}


def test_git_push_records_history() -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "repo"
        remote = root / "remote.git"
        run(["git", "init", str(repo)])
        run(["git", "init", "--bare", str(remote)])
        run(["git", "config", "user.email", "agent@example.com"], cwd=repo)
        run(["git", "config", "user.name", "Agent"], cwd=repo)
        (repo / "file.txt").write_text("hello", encoding="utf-8")
        run(["git", "add", "file.txt"], cwd=repo)
        run(["git", "commit", "-m", "test"], cwd=repo)
        run(["git", "remote", "add", "origin", str(remote)], cwd=repo)
        branch = run(["git", "branch", "--show-current"], cwd=repo).stdout.strip() or "master"
        run(
            [
                PYTHON,
                str(ROOT / "scripts" / "git_knowledge_push.py"),
                "--project-root",
                str(repo),
                "--remote",
                "origin",
                "--branch",
                branch,
                "--requirements",
                "Add priority tracking",
                "--metadata",
                "CustomField:Account.Priority__c",
            ]
        )
        history = (repo / ".salesforce-agent-knowledge" / "history" / "project-history.md").read_text(encoding="utf-8")
        clone = root / "clone"
        run(["git", "clone", str(remote), str(clone)])
        remote_history = (clone / ".salesforce-agent-knowledge" / "history" / "project-history.md").read_text(encoding="utf-8")
        checks = {
            "push_recorded": "git-push" in history,
            "requirement_recorded": "Add priority tracking" in history,
            "metadata_recorded": "CustomField:Account.Priority__c" in history,
            "remote_contains_history": "CustomField:Account.Priority__c" in remote_history,
        }
        assert all(checks.values())
        return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local cross-platform tests for the Salesforce Agent Optimizer skill.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = {
        "sf_init_project_skill": test_init_generates_metadata_docs(),
        "history": test_history_records_requirements_and_metadata(),
        "agent_cli": test_agent_cli_guardrails(),
        "git_push": test_git_push_records_history(),
    }
    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        for name, result in results.items():
            print(f"{name}: ok {json.dumps(result, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
