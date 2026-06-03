"""Command-line interface for Salesforce Agent Optimizer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .doctor import format_report, report_to_json, run_doctor
from .installer import install, project_destination, user_destination
from .validation import validate_auto


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sfao", description="Salesforce Agent Optimizer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install agent skill files")
    install_parser.add_argument("--project", action="store_true", help="Install into the current repository")
    install_parser.add_argument(
        "--platform",
        choices=["codex", "claude", "copilot", "all"],
        default="all",
        help="Agent platform to install",
    )
    install_parser.add_argument("--target", type=Path, help="Override installation root")

    doctor_parser = subparsers.add_parser("doctor", help="Diagnose environment and installed files")
    doctor_parser.add_argument("--json", action="store_true", help="Emit JSON")
    doctor_parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root to inspect")

    validate_parser = subparsers.add_parser("validate", help="Validate source tree or installation")
    validate_parser.add_argument("--json", action="store_true", help="Emit JSON")
    validate_parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root to validate")

    subparsers.add_parser("version", help="Print package version")
    subparsers.add_parser("update", help="Update generated installed files")
    subparsers.add_parser("uninstall", help="Remove installed generated files")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "version":
        print(f"salesforce-agent-optimizer {__version__}")
        return 0
    if args.command == "install":
        target = args.target or (project_destination() if args.project else user_destination())
        report = install(target, project=args.project, platform=args.platform)
        print_install_summary(report)
        return 0 if report.ok else 1
    if args.command == "doctor":
        report = run_doctor(args.root)
        print(report_to_json(report) if args.json else format_report(report), end="")
        return 1 if report.has_errors else 0
    if args.command == "validate":
        result = validate_auto(args.root, expected_version=__version__)
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        elif result.ok:
            print("Salesforce Agent Optimizer validation passed.")
            for warning in result.warnings:
                print(f"WARN: {warning}")
        else:
            for error in result.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            for warning in result.warnings:
                print(f"WARN: {warning}", file=sys.stderr)
        return 0 if result.ok else 1
    if args.command == "update":
        print("sfao update is planned but not yet implemented safely. Re-run sfao install for now.")
        return 2
    if args.command == "uninstall":
        print("sfao uninstall is planned but not yet implemented safely. Remove generated files manually for now.")
        return 2
    parser.print_help()
    return 2


def print_install_summary(report) -> None:
    print("Salesforce Agent Optimizer install summary")
    for label in ("installed", "updated", "skipped", "warnings", "errors"):
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
