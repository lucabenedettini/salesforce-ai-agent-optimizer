"""Command-line interface for Salesforce Agent Optimizer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .command_facade import example_payload, execute_payload, load_payload, search_payload
from .doctor import format_report, report_to_json, run_doctor
from .installer import install, project_destination, uninstall, update, user_destination
from .knowledge import format_knowledge_report, run_knowledge
from .live_tests import WRITE_CONFIRMATION, format_live_report, run_live_tests
from .memory import DEFAULT_MEMORY_MAX_BYTES, format_memory_report, run_memory
from .permission_analyzer import analyze_access_file
from .report import generate_report
from .soql import build_soql
from .validation import validate_auto
from .version_context import (
    format_report as format_version_context_report,
    scaffold as version_context_scaffold,
    update as version_context_update,
    validate as version_context_validate,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sfao", description="Salesforce Agent Optimizer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install agent skill files")
    add_scope_arguments(install_parser, "Install")
    install_parser.add_argument(
        "--platform",
        choices=["codex", "claude", "copilot", "all"],
        default="all",
        help="Agent platform to install",
    )
    install_parser.add_argument("--target", type=Path, help="Override installation root")
    install_parser.add_argument("--json", action="store_true", help="Emit compact JSON")

    update_parser = subparsers.add_parser("update", help="Update generated installed files")
    add_scope_arguments(update_parser, "Update")
    update_parser.add_argument(
        "--platform",
        choices=["codex", "claude", "copilot", "all"],
        default="all",
        help="Agent platform to update",
    )
    update_parser.add_argument("--target", type=Path, help="Override installation root")
    update_parser.add_argument("--json", action="store_true", help="Emit compact JSON")

    uninstall_parser = subparsers.add_parser("uninstall", help="Remove generated installed files")
    add_scope_arguments(uninstall_parser, "Remove")
    uninstall_parser.add_argument(
        "--platform",
        choices=["codex", "claude", "copilot", "all"],
        default="all",
        help="Agent platform to uninstall",
    )
    uninstall_parser.add_argument("--target", type=Path, help="Override installation root")
    uninstall_parser.add_argument("--yes", action="store_true", help="Confirm non-interactive uninstall")
    uninstall_parser.add_argument("--json", action="store_true", help="Emit compact JSON")

    doctor_parser = subparsers.add_parser("doctor", help="Diagnose environment and installed files")
    doctor_parser.add_argument("--json", action="store_true", help="Emit JSON")
    doctor_parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root to inspect")
    doctor_parser.add_argument("--summary", action="store_true", help="Emit compact summary")
    doctor_parser.add_argument("--compact", action="store_true", help="Emit compact summary")
    doctor_parser.add_argument("--verbose", action="store_true", help="Emit full diagnostics")

    validate_parser = subparsers.add_parser("validate", help="Validate source tree or installation")
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON")
    validate_parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root to validate")
    validate_parser.add_argument("--summary", action="store_true", help="Emit compact summary")
    validate_parser.add_argument("--compact", action="store_true", help="Emit compact summary")
    validate_parser.add_argument("--verbose", action="store_true", help="Emit validation details")

    report_parser = subparsers.add_parser("report", help="Generate a static local Markdown health report")
    report_parser.add_argument("--project-root", type=Path, default=Path.cwd())
    report_parser.add_argument("--format", choices=["md"], default="md")
    report_parser.add_argument(
        "--output",
        type=Path,
        help="Report output path. Defaults to .salesforce-agent-knowledge/reports/sfao-report.md",
    )

    command_parser = subparsers.add_parser("command", help="Search and execute registered CLI facade tools")
    command_subparsers = command_parser.add_subparsers(dest="command_action", required=True)
    command_search = command_subparsers.add_parser("search", help="Search the Salesforce CLI facade registry")
    command_search.add_argument("query", nargs="?", default="")
    command_search.add_argument("--toolset", choices=["core", "schema", "data-read", "metadata", "deploy", "permissions", "apex", "packages", "local"])
    command_search.add_argument("--root", type=Path, default=Path.cwd())
    command_search.add_argument("--limit", type=int, default=10)
    command_search.add_argument("--json", action="store_true", help="Emit compact JSON")
    command_example = command_subparsers.add_parser("payload-example", help="Print a minimal payload for one registered tool")
    command_example.add_argument("tool")
    command_example.add_argument("--root", type=Path, default=Path.cwd())
    command_example.add_argument("--json", action="store_true", help="Emit compact JSON")
    command_execute = command_subparsers.add_parser("execute", help="Execute one registered tool from a JSON payload")
    command_execute.add_argument("--payload", required=True, help="JSON string or path to a JSON file")
    command_execute.add_argument("--root", type=Path, default=Path.cwd())

    soql_parser = subparsers.add_parser("soql", help="Build compact SOQL payloads")
    soql_subparsers = soql_parser.add_subparsers(dest="soql_action", required=True)
    soql_build = soql_subparsers.add_parser("build", help="Build a focused SOQL query and data-query payload")
    soql_build.add_argument("--sobject", required=True)
    soql_build.add_argument("--field", action="append", required=True)
    soql_build.add_argument("--where")
    soql_build.add_argument("--order-by")
    soql_build.add_argument("--limit", type=int, default=50)
    soql_build.add_argument("--describe-json", type=Path)
    soql_build.add_argument("--json", action="store_true", help="Emit compact JSON")

    permissions_parser = subparsers.add_parser("permissions", help="Explain access-inspect results")
    permissions_subparsers = permissions_parser.add_subparsers(dest="permissions_action", required=True)
    permissions_explain = permissions_subparsers.add_parser("explain", help="Explain why object/field access exists")
    permissions_explain.add_argument("--input", type=Path, required=True, help="JSON output from access-inspect")
    permissions_explain.add_argument("--sobject")
    permissions_explain.add_argument("--field")
    permissions_explain.add_argument("--json", action="store_true", help="Emit compact JSON")

    live_parser = subparsers.add_parser("live-test", help="Run opt-in tests against a real Salesforce org")
    live_parser.add_argument("--target-org", required=True, help="Explicit Salesforce org alias")
    live_parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root with scripts/templates")
    live_parser.add_argument("--include-write", action="store_true", help="Request sandbox-only write tests")
    live_parser.add_argument(
        "--write-confirmation",
        help=f"Required exact phrase for write tests: {WRITE_CONFIRMATION}",
    )
    live_parser.add_argument("--max-chars", type=int, default=4000)
    live_parser.add_argument("--max-list", type=int, default=5)
    live_parser.add_argument("--json", action="store_true", help="Emit compact JSON")
    live_parser.add_argument("--verbose", action="store_true", help="Emit command notes")

    knowledge_parser = subparsers.add_parser("knowledge", help="Manage local Salesforce Knowledge")
    knowledge_subparsers = knowledge_parser.add_subparsers(dest="knowledge_command", required=True)
    for name in ("init", "refresh", "doctor"):
        parser_for_command = knowledge_subparsers.add_parser(name, help=f"Knowledge {name}")
        parser_for_command.add_argument("--project-root", type=Path, default=Path.cwd())
        parser_for_command.add_argument("--target-org", help="Explicit org alias for optional enrichment")
        parser_for_command.add_argument("--json", action="store_true", help="Emit compact JSON")
        parser_for_command.add_argument("--summary", action="store_true", help="Emit compact summary")
        parser_for_command.add_argument("--compact", action="store_true", help="Emit compact summary")
        parser_for_command.add_argument("--verbose", action="store_true", help="Emit changed paths")
        parser_for_command.add_argument("--max-items", type=int, help="Limit indexed entries")
        if name in {"init", "refresh"}:
            parser_for_command.add_argument(
                "--scan-root",
                action="store_true",
                help="Scan the whole project root instead of sfdx-project packageDirectories.",
            )

    memory_parser = subparsers.add_parser("memory", help="Manage curated project memory")
    memory_subparsers = memory_parser.add_subparsers(dest="memory_command", required=True)
    memory_init = memory_subparsers.add_parser("init", help="Create project memory.md if missing")
    memory_init.add_argument("--project-root", type=Path, default=Path.cwd())
    memory_init.add_argument("--json", action="store_true", help="Emit compact JSON")
    memory_add = memory_subparsers.add_parser("add", help="Append a compact curated memory entry")
    memory_add.add_argument("--project-root", type=Path, default=Path.cwd())
    memory_add.add_argument(
        "--task-type",
        choices=["bugfix", "development", "config", "release", "validation", "decision", "note"],
        required=True,
    )
    memory_add.add_argument("--summary", required=True)
    memory_add.add_argument("--metadata", action="append", default=[])
    memory_add.add_argument("--file", action="append", default=[])
    memory_add.add_argument("--validation")
    memory_add.add_argument("--risk")
    memory_add.add_argument("--follow-up")
    memory_add.add_argument("--decision")
    memory_add.add_argument("--json", action="store_true", help="Emit compact JSON")
    memory_compact = memory_subparsers.add_parser("compact", help="Compact project memory")
    memory_compact.add_argument("--project-root", type=Path, default=Path.cwd())
    memory_compact.add_argument("--max-bytes", type=int, default=DEFAULT_MEMORY_MAX_BYTES)
    memory_compact.add_argument("--json", action="store_true", help="Emit compact JSON")
    memory_doctor = memory_subparsers.add_parser("doctor", help="Validate project memory.md")
    memory_doctor.add_argument("--project-root", type=Path, default=Path.cwd())
    memory_doctor.add_argument("--json", action="store_true", help="Emit compact JSON")

    version_context_parser = subparsers.add_parser(
        "version-context",
        help="Manage Salesforce release and API version context",
    )
    version_context_subparsers = version_context_parser.add_subparsers(
        dest="version_context_command",
        required=True,
    )
    for name in ("scaffold", "update", "validate"):
        parser_for_command = version_context_subparsers.add_parser(
            name,
            help=f"Version-context {name}",
        )
        parser_for_command.add_argument("--root", type=Path, default=Path.cwd())
        parser_for_command.add_argument("--json", action="store_true", help="Emit compact JSON")
        parser_for_command.add_argument("--summary", action="store_true", help="Emit compact summary")
        parser_for_command.add_argument("--compact", action="store_true", help="Emit compact summary")
        parser_for_command.add_argument("--verbose", action="store_true", help="Emit details")
        if name == "update":
            parser_for_command.add_argument(
                "--offline",
                action="store_true",
                help="Use existing official-source context without network checks",
            )
        if name == "validate":
            parser_for_command.add_argument(
                "--max-age-days",
                type=int,
                default=90,
                help="Warn when last_verified_date is older than this many days.",
            )

    subparsers.add_parser("version", help="Print package version")
    return parser


def add_scope_arguments(parser: argparse.ArgumentParser, verb: str) -> None:
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--project",
        action="store_true",
        help=f"{verb} files in the current repository. This is the default.",
    )
    scope.add_argument("--user", action="store_true", help=f"{verb} user-scoped files under HOME.")


def resolve_target(args) -> tuple[Path, bool]:
    project_scope = args.project or not args.user
    target = args.target or (project_destination() if project_scope else user_destination())
    return target, project_scope


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print(f"salesforce-agent-optimizer {__version__}")
        return 0
    if args.command == "install":
        target, project_scope = resolve_target(args)
        report = install(target, project=project_scope, platform=args.platform)
        print_operation_summary("install", report, json_output=args.json)
        return 0 if report.ok else 1
    if args.command == "update":
        target, project_scope = resolve_target(args)
        report = update(target, project=project_scope, platform=args.platform)
        print_operation_summary("update", report, json_output=args.json)
        return 0 if report.ok else 1
    if args.command == "uninstall":
        target, project_scope = resolve_target(args)
        report = uninstall(target, project=project_scope, platform=args.platform, yes=args.yes)
        print_operation_summary("uninstall", report, json_output=args.json)
        return 0 if report.ok else 1
    if args.command == "doctor":
        progress = None if args.json else print_progress
        report = run_doctor(args.root, progress=progress)
        print(report_to_json(report) if args.json else format_report(report, verbose=args.verbose), end="")
        return 1 if report.has_errors else 0
    if args.command == "validate":
        progress = None if args.json else print_progress
        result = validate_auto(args.root, expected_version=__version__, progress=progress)
        if args.json:
            print(json.dumps(result.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            output = format_validation_result(result, verbose=args.verbose)
            stream = sys.stdout if result.ok else sys.stderr
            print(output, end="", file=stream)
        return 0 if result.ok else 1
    if args.command == "report":
        result = generate_report(args.project_root, output=args.output, fmt=args.format)
        if result.ok:
            try:
                display_path = result.output_path.relative_to(args.project_root.resolve())
            except ValueError:
                display_path = result.output_path
            print(f"Generated SFAO report: {display_path}")
            return 0
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.command == "command":
        if args.command_action == "search":
            payload = search_payload(args.query, args.toolset, args.root, args.limit)
            print_json_or_text(payload, args.json, title="Salesforce Agent Optimizer command registry")
            return 0
        if args.command_action == "payload-example":
            payload = example_payload(args.tool, args.root)
            print_json_or_text(payload, args.json, title=f"Payload example: {args.tool}")
            return 0
        payload = load_payload(args.payload)
        completed = execute_payload(payload, args.root)
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode
    if args.command == "soql":
        payload = build_soql(
            args.sobject,
            args.field,
            where=args.where,
            order_by=args.order_by,
            limit=args.limit,
            describe_path=args.describe_json,
        )
        print_json_or_text(payload, args.json, title="Salesforce Agent Optimizer SOQL assistant")
        return 0
    if args.command == "permissions":
        payload = analyze_access_file(args.input, sobject=args.sobject, field=args.field)
        print_json_or_text(payload, args.json, title="Salesforce Agent Optimizer permission analyzer")
        return 0
    if args.command == "live-test":
        progress = None if args.json else print_progress
        report = run_live_tests(
            args.target_org,
            args.root,
            include_write=args.include_write,
            write_confirmation=args.write_confirmation,
            max_chars=args.max_chars,
            max_list=args.max_list,
            progress=progress,
        )
        if args.json:
            print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            print(format_live_report(report, verbose=args.verbose), end="")
        return 0 if report.ok else 1
    if args.command == "knowledge":
        progress = None if args.json else print_progress
        report = run_knowledge(
            args.knowledge_command,
            args.project_root,
            target_org=args.target_org,
            max_items=args.max_items,
            scan_root=getattr(args, "scan_root", False),
            progress=progress,
        )
        if args.json:
            print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            print(format_knowledge_report(report, verbose=args.verbose), end="")
        return 0 if report.ok else 1
    if args.command == "memory":
        report = run_memory(
            args.memory_command,
            args.project_root,
            task_type=getattr(args, "task_type", None),
            summary=getattr(args, "summary", None),
            metadata=getattr(args, "metadata", None),
            files=getattr(args, "file", None),
            validation=getattr(args, "validation", None),
            risk=getattr(args, "risk", None),
            follow_up=getattr(args, "follow_up", None),
            decision=getattr(args, "decision", None),
            max_bytes=getattr(args, "max_bytes", DEFAULT_MEMORY_MAX_BYTES),
        )
        if args.json:
            print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            print(format_memory_report(report), end="")
        return 0 if report.ok else 1
    if args.command == "version-context":
        progress = None if args.json else print_progress
        if args.version_context_command == "scaffold":
            report = version_context_scaffold(args.root, progress=progress)
        elif args.version_context_command == "update":
            report = version_context_update(args.root, offline=args.offline, progress=progress)
        else:
            report = version_context_validate(
                args.root,
                max_age_days=args.max_age_days,
                progress=progress,
            )
        if args.json:
            print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            print(format_version_context_report(report, verbose=args.verbose), end="")
        return 0 if report.ok else 1
    parser.print_help()
    return 2


def format_validation_result(result, verbose: bool = False) -> str:
    status = "OK" if result.ok else "ERROR"
    lines = [f"Salesforce Agent Optimizer validation: {status}"]
    if result.warnings or result.errors:
        for error in result.errors:
            lines.append(f"ERROR: {error}")
        for warning in result.warnings:
            lines.append(f"WARN: {warning}")
    else:
        lines.append("No warnings or errors.")
    if verbose and result.ok:
        lines.append("Validated required files, versions, frontmatter, YAML, TOML, JSON, Python, and text shape.")
    return "\n".join(lines) + "\n"


def print_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def print_json_or_text(payload: dict, json_output: bool, title: str) -> None:
    if json_output:
        print(json.dumps(payload, separators=(",", ":"), sort_keys=True))
        return
    print(title)
    print(json.dumps(payload, indent=2, sort_keys=True))


def print_operation_summary(action: str, report, json_output: bool = False) -> None:
    if json_output:
        print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        return
    print(f"Salesforce Agent Optimizer {action} summary")
    for label in ("installed", "updated", "removed", "skipped", "stale", "warnings", "errors"):
        values = getattr(report, label)
        print(f"{label.title()}: {len(values)}")
        for item in values[:20]:
            print(f"- {item}")
        if len(values) > 20:
            print(f"- ... {len(values) - 20} more")
    print("Next steps:")
    print("- Run: sfao doctor")
    print("- Run: sfao validate")


if __name__ == "__main__":
    raise SystemExit(main())
