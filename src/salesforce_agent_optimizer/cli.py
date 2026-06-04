"""Command-line interface for Salesforce Agent Optimizer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .doctor import format_report, report_to_json, run_doctor
from .installer import install, project_destination, uninstall, update, user_destination
from .knowledge import format_knowledge_report, run_knowledge
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
        report = run_doctor(args.root)
        print(report_to_json(report) if args.json else format_report(report, verbose=args.verbose), end="")
        return 1 if report.has_errors else 0
    if args.command == "validate":
        result = validate_auto(args.root, expected_version=__version__)
        if args.json:
            print(json.dumps(result.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            output = format_validation_result(result, verbose=args.verbose)
            stream = sys.stdout if result.ok else sys.stderr
            print(output, end="", file=stream)
        return 0 if result.ok else 1
    if args.command == "knowledge":
        report = run_knowledge(
            args.knowledge_command,
            args.project_root,
            target_org=args.target_org,
            max_items=args.max_items,
        )
        if args.json:
            print(json.dumps(report.to_dict(), separators=(",", ":"), sort_keys=True))
        else:
            print(format_knowledge_report(report, verbose=args.verbose), end="")
        return 0 if report.ok else 1
    if args.command == "version-context":
        if args.version_context_command == "scaffold":
            report = version_context_scaffold(args.root)
        elif args.version_context_command == "update":
            report = version_context_update(args.root, offline=args.offline)
        else:
            report = version_context_validate(args.root)
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
