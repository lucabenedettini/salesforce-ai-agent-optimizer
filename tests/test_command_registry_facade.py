from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

from salesforce_agent_optimizer.command_facade import build_wrapper_args
from salesforce_agent_optimizer.command_registry import get_tool, payload_example, search_tools
from salesforce_agent_optimizer.permission_analyzer import analyze_access
from salesforce_agent_optimizer.soql import build_soql


def run_cli(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    full_env = os.environ.copy()
    full_env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + full_env.get("PYTHONPATH", "")
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, "-m", "salesforce_agent_optimizer.cli", *args],
        cwd=cwd,
        env=full_env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def test_registry_contains_all_existing_wrapper_tools() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/sf_agent_cli.py", "commands"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    wrapper_names = {item["name"] for item in json.loads(completed.stdout)}
    registry_names = {tool.name for tool in search_tools("", root=ROOT)}

    assert wrapper_names <= registry_names
    assert get_tool("access-inspect", root=ROOT).requires_alias
    assert get_tool("deploy-start", root=ROOT).production == "blocked"
    assert get_tool("data-record-delete", root=ROOT).safety == "destructive"


def test_registry_search_and_payload_example_are_compact() -> None:
    results = search_tools("permission user access", toolset="permissions", root=ROOT)
    assert results
    assert results[0].category == "permissions"
    example = payload_example("access-inspect", root=ROOT)
    assert example["tool"] == "access-inspect"
    assert example["target_org"] == "ASK_USER_FOR_ALIAS"
    assert example["dry_run"]


def test_sfao_command_search_and_payload_example() -> None:
    search = run_cli(["command", "search", "deploy", "--toolset", "deploy", "--json"], ROOT)
    assert search.returncode == 0, search.stdout + search.stderr
    payload = json.loads(search.stdout)
    assert payload["tools"]
    assert all(tool["category"] == "deploy" for tool in payload["tools"])

    example = run_cli(["command", "payload-example", "data-query", "--json"], ROOT)
    assert example.returncode == 0, example.stdout + example.stderr
    assert json.loads(example.stdout)["tool"] == "data-query"


def test_command_facade_builds_wrapper_args() -> None:
    payload = {
        "tool": "data-query",
        "dry_run": True,
        "target_org": "dev",
        "options": {"query": "SELECT Id FROM Account LIMIT 1", "tooling": True},
        "global": {"select": "result.records", "max_chars": 2000, "max_list": 5},
    }
    args = build_wrapper_args(payload)
    assert args[:7] == ["--dry-run", "--select", "result.records", "--max-chars", "2000", "--max-list", "5"]
    assert args[-6:] == [
        "data-query",
        "--target-org",
        "dev",
        "--query",
        "SELECT Id FROM Account LIMIT 1",
        "--tooling",
    ]


def test_sfao_command_execute_dry_run_does_not_require_real_sf() -> None:
    payload = json.dumps(
        {
            "tool": "data-query",
            "dry_run": True,
            "target_org": "dev",
            "options": {"query": "SELECT Id FROM Account LIMIT 1"},
            "global": {"select": "dry_run,sf_command", "max_chars": 2000, "max_list": 5},
        }
    )
    completed = run_cli(["command", "execute", "--payload", payload, "--root", str(ROOT)], ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    output = json.loads(completed.stdout)
    assert output["dry_run"]
    assert "data" in output["sf_command"]
    assert "query" in output["sf_command"]


def test_schema_sobject_list_maps_to_current_salesforce_cli_flag() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/sf_agent_cli.py",
            "--dry-run",
            "schema-sobject-list",
            "--target-org",
            "dev",
            "--sobject-type",
            "custom",
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert "--sobject" in payload["sf_command"]
    assert "--sobject-type" not in payload["sf_command"]


def test_metadata_list_compacts_noisy_metadata_records(tmp_path: Path) -> None:
    mock_sf = make_metadata_mock_sf(tmp_path)
    env = os.environ.copy()
    env["SF_AGENT_SF_BIN"] = str(mock_sf)
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/sf_agent_cli.py",
            "metadata-list",
            "--target-org",
            "dev",
            "--metadata-type",
            "CustomObject",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["summary"]["count"] == 1
    assert payload["result"][0]["fullName"] == "Invoice__c"
    assert "createdByName" not in payload["result"][0]
    assert "lastModifiedByName" not in payload["result"][0]


def test_schema_describe_compacts_fields_by_default(tmp_path: Path) -> None:
    mock_sf = make_describe_mock_sf(tmp_path)
    env = os.environ.copy()
    env["SF_AGENT_SF_BIN"] = str(mock_sf)
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/sf_agent_cli.py",
            "schema-sobject-describe",
            "--target-org",
            "dev",
            "--sobject",
            "Account",
            "--field-limit",
            "1",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["summary"]["mode"] == "compact"
    assert payload["result"]["fieldCount"] == 2
    assert len(payload["result"]["fields"]) == 1
    assert "picklistValues" not in payload["result"]["fields"][0]


def test_sfao_command_execute_blocks_production_writes_with_mocked_sf(tmp_path: Path) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=False)
    payload = json.dumps(
        {
            "tool": "data-record-create",
            "target_org": "prod",
            "options": {"sobject": "Account", "values": "Name=Blocked"},
        }
    )
    completed = run_cli(
        ["command", "execute", "--payload", payload, "--root", str(ROOT)],
        ROOT,
        env={"SF_AGENT_SF_BIN": str(mock_sf)},
    )
    assert completed.returncode != 0
    assert "production" in completed.stderr.lower()


def test_soql_builder_validates_fields_from_describe(tmp_path: Path) -> None:
    describe = tmp_path / "account-describe.json"
    describe.write_text(
        json.dumps({"result": {"fields": [{"name": "Id"}, {"name": "Name"}, {"name": "Rating"}]}}),
        encoding="utf-8",
    )
    result = build_soql(
        "Account",
        ["Id", "Name"],
        where="Name != null",
        order_by="Name ASC",
        limit=25,
        describe_path=describe,
    )
    assert result["query"] == "SELECT Id, Name FROM Account WHERE Name != null ORDER BY Name ASC LIMIT 25"
    assert result["next_command"]["tool"] == "data-query"


def test_permission_analyzer_explains_object_and_field_access() -> None:
    payload = {
        "users": {"records": [{"Id": "0051", "Username": "user@example.com", "Name": "User"}]},
        "permission_set_assignments": {
            "records": [
                {
                    "PermissionSetId": "0PS1",
                    "PermissionSet": {"Name": "Invoice_User", "Label": "Invoice User"},
                }
            ]
        },
        "permission_set_groups": {"records": [{"Id": "0PG1", "DeveloperName": "BackOffice"}]},
        "permission_set_group_components": {"records": [{"PermissionSetGroupId": "0PG1"}]},
        "object_permissions": {
            "records": [
                {
                    "ParentId": "0PS1",
                    "SobjectType": "Invoice__c",
                    "PermissionsRead": True,
                    "PermissionsEdit": True,
                }
            ]
        },
        "field_permissions": {
            "records": [
                {
                    "ParentId": "0PS1",
                    "SobjectType": "Invoice__c",
                    "Field": "Invoice__c.Amount__c",
                    "PermissionsRead": True,
                    "PermissionsEdit": False,
                }
            ]
        },
    }
    result = analyze_access(payload, sobject="Invoice__c")
    assert result["assignment_count"] == 1
    assert result["permission_set_group_count"] == 1
    assert len(result["access_explanations"]) == 2
    assert result["access_explanations"][0]["source"] == "Invoice User"


def make_mock_sf(tmp_path: Path, is_sandbox: bool) -> Path:
    if os.name == "nt":
        script = tmp_path / "sf.cmd"
        script.write_text(
            "@echo off\r\n"
            f"echo {{\"result\":{{\"records\":[{{\"IsSandbox\":{str(is_sandbox).lower()}}}]}}}}\r\n",
            encoding="utf-8",
        )
        return script
    script = tmp_path / "sf"
    script.write_text(
        "#!/usr/bin/env sh\n"
        f"printf '%s\\n' '{{\"result\":{{\"records\":[{{\"IsSandbox\":{str(is_sandbox).lower()}}}]}}}}'\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


def make_metadata_mock_sf(tmp_path: Path) -> Path:
    payload = {
        "result": [
            {
                "fullName": "Invoice__c",
                "type": "CustomObject",
                "fileName": "objects/Invoice__c.object",
                "createdByName": "Noisy User",
                "lastModifiedByName": "Noisy User",
                "createdDate": "2026-01-01T00:00:00.000Z",
                "lastModifiedDate": "2026-01-02T00:00:00.000Z",
            }
        ]
    }
    text = json.dumps(payload)
    if os.name == "nt":
        script = tmp_path / "sf.cmd"
        script.write_text(f"@echo off\r\necho {text}\r\n", encoding="utf-8")
        return script
    script = tmp_path / "sf"
    script.write_text("#!/usr/bin/env sh\nprintf '%s\\n' " + repr(text) + "\n", encoding="utf-8")
    script.chmod(0o755)
    return script


def make_describe_mock_sf(tmp_path: Path) -> Path:
    payload = {
        "result": {
            "name": "Account",
            "label": "Account",
            "custom": False,
            "createable": True,
            "updateable": True,
            "deletable": True,
            "queryable": True,
            "fields": [
                {
                    "name": "Name",
                    "label": "Account Name",
                    "type": "string",
                    "createable": True,
                    "updateable": True,
                    "picklistValues": [{"label": "Noisy", "value": "Noisy"}],
                },
                {"name": "OwnerId", "label": "Owner", "type": "reference", "referenceTo": ["User"]},
            ],
            "childRelationships": [{"relationshipName": "Contacts"}],
            "recordTypeInfos": [{"name": "Master"}],
        }
    }
    text = json.dumps(payload)
    if os.name == "nt":
        script = tmp_path / "sf.cmd"
        script.write_text(f"@echo off\r\necho {text}\r\n", encoding="utf-8")
        return script
    script = tmp_path / "sf"
    script.write_text("#!/usr/bin/env sh\nprintf '%s\\n' " + repr(text) + "\n", encoding="utf-8")
    script.chmod(0o755)
    return script
