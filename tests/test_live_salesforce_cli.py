from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROOT

from salesforce_agent_optimizer.live_tests import WRITE_CONFIRMATION, run_live_tests


def test_live_test_uses_mocked_salesforce_cli(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=True)
    monkeypatch.setenv("SF_AGENT_SF_BIN", str(mock_sf))

    report = run_live_tests("dev", ROOT)

    assert report.ok, report.to_dict()
    assert report.sandbox is True
    assert report.read_only
    assert {result.name for result in report.results} >= {
        "org-inspect",
        "org-limits",
        "schema-sobject-describe-account",
        "data-query-user",
        "package-installed-list",
    }
    assert all(result.stdout_chars > 0 for result in report.results)


def test_live_test_blocks_write_without_confirmation(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=True)
    monkeypatch.setenv("SF_AGENT_SF_BIN", str(mock_sf))

    report = run_live_tests("dev", ROOT, include_write=True)

    assert not report.ok
    assert any("Live write tests require exact confirmation" in error for error in report.errors)


def test_live_test_runs_reversible_write_suite_with_mocked_sandbox(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=True)
    monkeypatch.setenv("SF_AGENT_SF_BIN", str(mock_sf))

    report = run_live_tests(
        "dev",
        ROOT,
        include_write=True,
        write_confirmation=WRITE_CONFIRMATION,
    )

    assert report.ok, report.to_dict()
    names = {result.name for result in report.results}
    assert "write-data-record-create-account" in names
    assert "write-data-record-update-account" in names
    assert "write-data-record-get-account" in names
    assert "destructive-data-record-delete-account" in names
    assert "write-metadata-deploy-validation-rule" in names
    assert "metadata-validation-rule-blocks-invalid-account" in names
    assert "destructive-metadata-delete-validation-rule" in names
    assert "write-data-record-create-bad_sfao_metadata_test_after_delete" in names


def test_live_test_write_suite_is_blocked_on_mocked_production(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=False)
    monkeypatch.setenv("SF_AGENT_SF_BIN", str(mock_sf))

    report = run_live_tests(
        "prod",
        ROOT,
        include_write=True,
        write_confirmation=WRITE_CONFIRMATION,
    )

    assert not report.ok
    assert any("production" in error.lower() for error in report.errors)


@pytest.mark.skipif(not os.environ.get("SFAO_LIVE_TARGET_ORG"), reason="SFAO_LIVE_TARGET_ORG not set")
def test_live_read_only_suite_against_real_org() -> None:
    target_org = os.environ["SFAO_LIVE_TARGET_ORG"]
    report = run_live_tests(target_org, ROOT, max_chars=4000, max_list=5)

    assert report.ok, report.to_dict()
    assert report.results
    assert all(result.selected_output_chars <= 4000 for result in report.results)


def test_sfao_live_test_cli_with_mocked_salesforce_cli(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    mock_sf = make_mock_sf(tmp_path, is_sandbox=False)
    monkeypatch.setenv("SF_AGENT_SF_BIN", str(mock_sf))
    completed = run_cli(["live-test", "--target-org", "prod", "--root", str(ROOT), "--json"], ROOT)

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["sandbox"] is False
    assert payload["read_only"] is True


def run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
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


def make_mock_sf(tmp_path: Path, is_sandbox: bool) -> Path:
    mock_py = tmp_path / "mock_sf.py"
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps({"validation_rule": False}), encoding="utf-8")
    mock_py.write_text(
        f"""
from __future__ import annotations

import json
import sys
from pathlib import Path

STATE = Path({str(state_file)!r})
IS_SANDBOX = {is_sandbox!r}


def emit(payload, code=0):
    print(json.dumps(payload))
    raise SystemExit(code)


def read_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def write_state(payload):
    STATE.write_text(json.dumps(payload), encoding="utf-8")


args = sys.argv[1:]
joined = " ".join(args)
if args[:2] == ["org", "list"]:
    emit({{"result": {{"nonScratchOrgs": [{{"alias": "dev", "isSandbox": IS_SANDBOX}}], "scratchOrgs": [{{"alias": "dev", "isScratch": IS_SANDBOX}}]}}}})
if args[:2] == ["org", "display"]:
    emit({{"result": {{"alias": "dev", "username": "user@example.com"}}}})
if args[:2] == ["data", "query"] and "FROM Organization" in joined:
    emit({{"result": {{"records": [{{"IsSandbox": IS_SANDBOX, "OrganizationType": "Sandbox" if IS_SANDBOX else "Production"}}], "totalSize": 1}}}})
if args[:3] == ["project", "deploy", "start"]:
    state = read_state()
    deleted = "--post-destructive-changes" in args
    state["validation_rule"] = not deleted
    write_state(state)
    emit({{"result": {{"status": "Succeeded", "success": True, "files": [{{"fullName": "Account.SFAO_Account_Name_Starts_ACC", "type": "ValidationRule", "state": "Deleted" if deleted else "Created"}}]}}}})
if args[:3] == ["data", "create", "record"]:
    state = read_state()
    if "BAD_SFAO_Metadata_Test" in joined and state.get("validation_rule"):
        emit({{"message": "Account Name must start with ACC.", "name": "FIELD_CUSTOM_VALIDATION_EXCEPTION", "status": 1}}, 1)
    emit({{"result": {{"id": "001000000000001AAA", "success": True}}}})
if args[:3] == ["data", "delete", "record"]:
    emit({{"result": {{"id": "001000000000001AAA", "success": True}}}})
emit({{"result": {{"alias": "dev", "username": "user@example.com", "id": "001000000000001AAA", "success": True, "records": [{{"IsSandbox": IS_SANDBOX, "OrganizationType": "Sandbox" if IS_SANDBOX else "Production"}}], "fields": [{{"name": "Id"}}, {{"name": "Name"}}, {{"name": "OwnerId"}}], "totalSize": 1}}}})
""",
        encoding="utf-8",
    )
    if os.name == "nt":
        script = tmp_path / "sf.cmd"
        script.write_text(f'@echo off\r\n"{sys.executable}" "{mock_py}" %*\r\n', encoding="utf-8")
        return script
    script = tmp_path / "sf"
    script.write_text(f"#!/usr/bin/env sh\n{sys.executable!r} {str(mock_py)!r} \"$@\"\n", encoding="utf-8")
    script.chmod(0o755)
    return script
