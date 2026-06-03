from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from conftest import ROOT


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


self_test = load_module("self_test_for_pytest", ROOT / "scripts" / "self_test.py")
manifest = load_module("generate_package_manifest_for_pytest", ROOT / "scripts" / "generate_package_manifest.py")


def test_package_manifest_generation() -> None:
    result = self_test.test_package_manifest_generation()
    assert result["exists"]
    assert result["has_apex_class"]
    assert result["has_custom_field"]
    assert result["has_flow"]


def test_knowledge_init_on_temporary_salesforce_project() -> None:
    result = self_test.test_init_generates_metadata_docs()
    assert result["metadata_doc_count"] == 3
    assert result["markdown_index"]
    assert result["history"]


def test_destructive_command_guardrails() -> None:
    result = self_test.test_agent_cli_guardrails()
    assert result["delete_missing_approval_blocked"]
    assert result["safe_run_delete_missing_approval_blocked"]
    assert result["sf_min_destructive_blocked"]


def test_windows_path_metadata_mapping() -> None:
    assert manifest.metadata_from_source_path(
        r"force-app\main\default\objects\Account\fields\Priority__c.field-meta.xml"
    ) == ("CustomField", "Account.Priority__c")
    assert manifest.metadata_from_source_path(
        r"force-app\main\default\classes\AccountService.cls"
    ) == ("ApexClass", "AccountService")
    assert manifest.metadata_from_source_path(
        r"force-app\main\default\lwc\accountSummary\accountSummary.js"
    ) == ("LightningComponentBundle", "accountSummary")
