"""Opt-in live Salesforce org tests for the CLI facade."""

from __future__ import annotations

import json
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .command_facade import execute_payload


WRITE_CONFIRMATION = "I understand this will write test data to a sandbox"
DELETE_APPROVAL = "I explicitly approve this deletion"
VALIDATION_RULE_FULL_NAME = "Account.SFAO_Account_Name_Starts_ACC"
VALIDATION_RULE_FILE = "SFAO_Account_Name_Starts_ACC.validationRule-meta.xml"


@dataclass
class LiveCommandResult:
    name: str
    ok: bool
    returncode: int
    elapsed_ms: int
    stdout_chars: int
    stderr_chars: int
    selected_output_chars: int
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "returncode": self.returncode,
            "elapsed_ms": self.elapsed_ms,
            "stdout_chars": self.stdout_chars,
            "stderr_chars": self.stderr_chars,
            "selected_output_chars": self.selected_output_chars,
            "note": self.note,
        }


@dataclass
class LiveTestReport:
    target_org: str
    ok: bool
    read_only: bool
    sandbox: bool | None
    results: list[LiveCommandResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_org": self.target_org,
            "ok": self.ok,
            "read_only": self.read_only,
            "sandbox": self.sandbox,
            "results": [result.to_dict() for result in self.results],
            "warnings": self.warnings,
            "errors": self.errors,
            "totals": {
                "commands": len(self.results),
                "elapsed_ms": sum(result.elapsed_ms for result in self.results),
                "stdout_chars": sum(result.stdout_chars for result in self.results),
                "selected_output_chars": sum(result.selected_output_chars for result in self.results),
            },
        }


def read_suite(target_org: str, max_chars: int, max_list: int) -> list[dict[str, Any]]:
    global_opts = {"max_chars": max_chars, "max_list": max_list}
    return [
        {
            "name": "org-inspect",
            "tool": "org-inspect",
            "target_org": target_org,
            "global": {
                **global_opts,
                "select": "org_display.alias,org_display.username,organization.records.0.IsSandbox,organization.records.0.OrganizationType",
            },
        },
        {
            "name": "org-limits",
            "tool": "org-limits",
            "target_org": target_org,
            "global": {**global_opts, "select": "result.DailyApiRequests,result.ConcurrentAsyncGetReportInstances"},
        },
        {
            "name": "schema-sobject-describe-account",
            "tool": "schema-sobject-describe",
            "target_org": target_org,
            "options": {"sobject": "Account"},
            "global": {**global_opts, "select": "result.name,result.fields.0,result.fields.1,result.fields.2"},
        },
        {
            "name": "data-query-user",
            "tool": "data-query",
            "target_org": target_org,
            "options": {"query": "SELECT Id, Username, IsActive FROM User WHERE IsActive = true LIMIT 1"},
            "global": {**global_opts, "select": "result.totalSize,result.records"},
        },
        {
            "name": "package-installed-list",
            "tool": "package-installed-list",
            "target_org": target_org,
            "global": {**global_opts, "select": "result.0,result.1,result.2"},
        },
    ]


def detect_sandbox(results: list[LiveCommandResult], payloads: list[str]) -> bool | None:
    for result, output in zip(results, payloads, strict=False):
        if result.name != "org-inspect" or not result.ok:
            continue
        try:
            payload = json.loads(output)
        except json.JSONDecodeError:
            return None
        value = payload.get("organization.records.0.IsSandbox")
        if isinstance(value, bool):
            return value
        organization = payload.get("organization", {})
        if isinstance(organization, dict):
            records = organization.get("records", [])
            if records and isinstance(records[0].get("IsSandbox"), bool):
                return records[0]["IsSandbox"]
    return None


def run_live_tests(
    target_org: str,
    root: Path,
    *,
    include_write: bool = False,
    write_confirmation: str | None = None,
    max_chars: int = 4000,
    max_list: int = 5,
    progress=None,
) -> LiveTestReport:
    payloads = read_suite(target_org, max_chars=max_chars, max_list=max_list)
    results: list[LiveCommandResult] = []
    stdout_payloads: list[str] = []
    for index, payload in enumerate(payloads, start=1):
        if progress:
            progress(f"sfao live-test: running {payload['name']} ({index}/{len(payloads)})")
        result = run_payload(root, payload)
        results.append(result)
        stdout_payloads.append(getattr(result, "_stdout", ""))

    sandbox = detect_sandbox(results, stdout_payloads)
    warnings: list[str] = []
    errors = [result.note for result in results if not result.ok]

    if include_write:
        if write_confirmation != WRITE_CONFIRMATION:
            errors.append(
                "Live write tests require exact confirmation: "
                f'--write-confirmation "{WRITE_CONFIRMATION}"'
            )
        else:
            write_results, write_errors = run_write_suite(target_org, root, max_chars, max_list, progress)
            results.extend(write_results)
            errors.extend(write_errors)
            metadata_results, metadata_errors = run_metadata_write_suite(
                target_org,
                root,
                max_chars,
                max_list,
                progress,
            )
            results.extend(metadata_results)
            errors.extend(metadata_errors)

    optimize_notes = optimization_notes(results)
    warnings.extend(optimize_notes)
    return LiveTestReport(
        target_org=target_org,
        ok=not errors and all(result.ok for result in results),
        read_only=not include_write,
        sandbox=sandbox,
        results=results,
        warnings=warnings,
        errors=errors,
    )


def run_write_suite(
    target_org: str,
    root: Path,
    max_chars: int,
    max_list: int,
    progress=None,
) -> tuple[list[LiveCommandResult], list[str]]:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    account_name = f"SFAO_Live_Test_{stamp}"
    updated_name = f"{account_name}_Updated"
    global_opts = {"max_chars": max_chars, "max_list": max_list, "select": "result.id,result.success"}
    results: list[LiveCommandResult] = []
    errors: list[str] = []

    create_payload = {
        "name": "write-data-record-create-account",
        "tool": "data-record-create",
        "target_org": target_org,
        "options": {"sobject": "Account", "values": f"Name={account_name}"},
        "global": global_opts,
    }
    if progress:
        progress("sfao live-test: running write-data-record-create-account")
    create_result = run_payload(root, create_payload)
    results.append(create_result)
    record_id = parse_created_id(getattr(create_result, "_stdout", ""))
    if not create_result.ok or not record_id:
        errors.append(create_result.note or "Could not create Account test record or parse created record id.")
        return results, errors

    try:
        follow_up_payloads = [
            {
                "name": "write-data-record-update-account",
                "tool": "data-record-update",
                "target_org": target_org,
                "options": {"sobject": "Account", "record_id": record_id, "values": f"Name={updated_name}"},
                "global": global_opts,
            },
            {
                "name": "write-data-record-get-account",
                "tool": "data-record-get",
                "target_org": target_org,
                "options": {"sobject": "Account", "record_id": record_id},
                "global": {"max_chars": max_chars, "max_list": max_list, "select": "result.fields.Name,result.fields.Id"},
            },
        ]
        for payload in follow_up_payloads:
            if progress:
                progress(f"sfao live-test: running {payload['name']}")
            result = run_payload(root, payload)
            results.append(result)
            if not result.ok:
                errors.append(result.note or f"{result.name} failed.")
    finally:
        delete_payload = {
            "name": "destructive-data-record-delete-account",
            "tool": "data-record-delete",
            "target_org": target_org,
            "options": {
                "sobject": "Account",
                "record_id": record_id,
                "delete_approval": DELETE_APPROVAL,
            },
            "global": global_opts,
        }
        if progress:
            progress("sfao live-test: running destructive-data-record-delete-account")
        delete_result = run_payload(root, delete_payload)
        results.append(delete_result)
        if not delete_result.ok:
            errors.append(delete_result.note or "Could not delete Account test record.")
    return results, errors


def run_metadata_write_suite(
    target_org: str,
    root: Path,
    max_chars: int,
    max_list: int,
    progress=None,
) -> tuple[list[LiveCommandResult], list[str]]:
    results: list[LiveCommandResult] = []
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="sfao-live-metadata-") as temp_root:
        project = Path(temp_root)
        write_validation_rule_project(project)
        global_opts = {"max_chars": max_chars, "max_list": max_list, "select": "result.status,result.success,result.files"}

        deploy_payload = {
            "name": "write-metadata-deploy-validation-rule",
            "tool": "deploy-start",
            "target_org": target_org,
            "options": {
                "source_dir": [str(project / "force-app")],
                "wait": "10",
                "requirements": "Live metadata test: create temporary Account validation rule requiring ACC prefix",
                "changed_metadata": [f"ValidationRule:{VALIDATION_RULE_FULL_NAME}"],
            },
            "global": global_opts,
        }
        if progress:
            progress("sfao live-test: running write-metadata-deploy-validation-rule")
        deploy_result = run_payload(root, deploy_payload, cwd=project)
        results.append(deploy_result)
        if not deploy_result.ok:
            errors.append(deploy_result.note or "Could not deploy temporary Account validation rule.")
            return results, errors

        bad_payload = {
            "name": "metadata-validation-rule-blocks-invalid-account",
            "tool": "data-record-create",
            "target_org": target_org,
            "options": {"sobject": "Account", "values": "Name=BAD_SFAO_Metadata_Test"},
            "global": {"max_chars": max_chars, "max_list": max_list},
        }
        if progress:
            progress("sfao live-test: running metadata-validation-rule-blocks-invalid-account")
        bad_result = run_payload(root, bad_payload, cwd=project)
        bad_result.ok = bad_result.returncode != 0 and "Account Name must start with ACC" in getattr(
            bad_result,
            "_stdout",
            "",
        )
        if bad_result.ok:
            bad_result.note = "Expected validation rule failure observed."
        results.append(bad_result)
        if not bad_result.ok:
            errors.append("Temporary validation rule did not block an Account name without ACC prefix.")

        good_record_id = create_and_delete_account(
            target_org,
            root,
            project,
            "ACC_SFAO_Metadata_Test",
            max_chars,
            max_list,
            results,
            errors,
            progress,
        )

        destructive_payload = {
            "name": "destructive-metadata-delete-validation-rule",
            "tool": "safe-run",
            "target_org": target_org,
            "options": {
                "delete_approval": DELETE_APPROVAL,
                "requirements": "Live metadata test cleanup: delete temporary Account validation rule",
                "changed_metadata": [f"ValidationRule:{VALIDATION_RULE_FULL_NAME}"],
                "sf_args": [
                    "project",
                    "deploy",
                    "start",
                    "--manifest",
                    str(project / "manifest" / "package-empty.xml"),
                    "--post-destructive-changes",
                    str(project / "manifest" / "destructiveChanges.xml"),
                    "--wait",
                    "10",
                ],
            },
            "global": global_opts,
        }
        if progress:
            progress("sfao live-test: running destructive-metadata-delete-validation-rule")
        delete_result = run_payload(root, destructive_payload, cwd=project)
        results.append(delete_result)
        if not delete_result.ok:
            errors.append(delete_result.note or "Could not delete temporary Account validation rule.")
            return results, errors

        after_delete_id = create_and_delete_account(
            target_org,
            root,
            project,
            "BAD_SFAO_Metadata_Test_After_Delete",
            max_chars,
            max_list,
            results,
            errors,
            progress,
        )
        if not after_delete_id:
            errors.append("Account create after validation rule deletion failed; destructive cleanup is suspect.")

        if not good_record_id:
            errors.append("Could not complete positive Account create/delete while validation rule existed.")

    return results, errors


def create_and_delete_account(
    target_org: str,
    root: Path,
    cwd: Path,
    account_name: str,
    max_chars: int,
    max_list: int,
    results: list[LiveCommandResult],
    errors: list[str],
    progress=None,
) -> str | None:
    create_payload = {
        "name": f"write-data-record-create-{account_name.lower()}",
        "tool": "data-record-create",
        "target_org": target_org,
        "options": {"sobject": "Account", "values": f"Name={account_name}"},
        "global": {"max_chars": max_chars, "max_list": max_list, "select": "result.id,result.success"},
    }
    if progress:
        progress(f"sfao live-test: running {create_payload['name']}")
    create_result = run_payload(root, create_payload, cwd=cwd)
    results.append(create_result)
    record_id = parse_created_id(getattr(create_result, "_stdout", ""))
    if not create_result.ok or not record_id:
        errors.append(create_result.note or f"Could not create Account test record {account_name}.")
        return None

    delete_payload = {
        "name": f"destructive-data-record-delete-{account_name.lower()}",
        "tool": "data-record-delete",
        "target_org": target_org,
        "options": {"sobject": "Account", "record_id": record_id, "delete_approval": DELETE_APPROVAL},
        "global": {"max_chars": max_chars, "max_list": max_list, "select": "result.id,result.success"},
    }
    if progress:
        progress(f"sfao live-test: running {delete_payload['name']}")
    delete_result = run_payload(root, delete_payload, cwd=cwd)
    results.append(delete_result)
    if not delete_result.ok:
        errors.append(delete_result.note or f"Could not delete Account test record {record_id}.")
    return record_id


def write_validation_rule_project(project: Path) -> None:
    rule_dir = project / "force-app" / "main" / "default" / "objects" / "Account" / "validationRules"
    manifest_dir = project / "manifest"
    rule_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (project / "sfdx-project.json").write_text(
        json.dumps(
            {
                "packageDirectories": [{"path": "force-app", "default": True}],
                "name": "sfao-live-metadata-test",
                "namespace": "",
                "sourceApiVersion": "66.0",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (rule_dir / VALIDATION_RULE_FILE).write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>SFAO_Account_Name_Starts_ACC</fullName>
    <active>true</active>
    <description>Temporary SFAO live metadata test. Account names must start with ACC.</description>
    <errorConditionFormula>NOT(BEGINS(Name, "ACC"))</errorConditionFormula>
    <errorMessage>Account Name must start with ACC.</errorMessage>
</ValidationRule>
""",
        encoding="utf-8",
    )
    package_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>{VALIDATION_RULE_FULL_NAME}</members>
        <name>ValidationRule</name>
    </types>
    <version>66.0</version>
</Package>
"""
    (manifest_dir / "package.xml").write_text(package_xml, encoding="utf-8")
    (manifest_dir / "destructiveChanges.xml").write_text(package_xml, encoding="utf-8")
    (manifest_dir / "package-empty.xml").write_text(
        """<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <version>66.0</version>
</Package>
""",
        encoding="utf-8",
    )


def run_payload(root: Path, payload: dict[str, Any], *, cwd: Path | None = None) -> LiveCommandResult:
    start = time.perf_counter()
    completed = execute_payload(payload, root, cwd=cwd)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    stdout_chars = len(completed.stdout)
    stderr_chars = len(completed.stderr)
    selected_output_chars = compact_length(completed.stdout)
    note = completed.stderr.strip()[:300] if completed.returncode else ""
    result = LiveCommandResult(
        name=str(payload["name"]),
        ok=completed.returncode == 0,
        returncode=completed.returncode,
        elapsed_ms=elapsed_ms,
        stdout_chars=stdout_chars,
        stderr_chars=stderr_chars,
        selected_output_chars=selected_output_chars,
        note=note,
    )
    setattr(result, "_stdout", completed.stdout)
    return result


def compact_length(stdout: str) -> int:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return len(stdout)
    return len(json.dumps(payload, separators=(",", ":"), sort_keys=True))


def parse_created_id(stdout: str) -> str | None:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    result = payload.get("result", {})
    if isinstance(result, dict):
        value = result.get("id") or result.get("Id")
        if value:
            return str(value)
    value = payload.get("result.id")
    return str(value) if value else None


def optimization_notes(results: list[LiveCommandResult]) -> list[str]:
    notes: list[str] = []
    for result in results:
        if result.stdout_chars > 5000:
            notes.append(f"{result.name}: output above 5000 chars; add a narrower --select or lower --max-list.")
        if result.elapsed_ms > 10000:
            notes.append(f"{result.name}: slower than 10s; consider a narrower query, selector, or metadata scope.")
    return notes


def format_live_report(report: LiveTestReport, verbose: bool = False) -> str:
    status = "OK" if report.ok else "ERROR"
    lines = [f"Salesforce Agent Optimizer live-test: {status}"]
    lines.append(f"- target org: {report.target_org}")
    lines.append(f"- mode: {'read-only' if report.read_only else 'read/write requested'}")
    lines.append(f"- sandbox: {report.sandbox if report.sandbox is not None else 'unknown'}")
    for result in report.results:
        line = (
            f"- {result.name}: {'OK' if result.ok else 'ERROR'} "
            f"{result.elapsed_ms}ms, stdout={result.stdout_chars}, compact={result.selected_output_chars}"
        )
        lines.append(line)
        if verbose and result.note:
            lines.append(f"  note: {result.note}")
    for warning in report.warnings:
        lines.append(f"WARN: {warning}")
    for error in report.errors:
        lines.append(f"ERROR: {error}")
    return "\n".join(lines) + "\n"
