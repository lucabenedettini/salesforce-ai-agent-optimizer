#!/usr/bin/env python3
"""Push a branch and record the push in Salesforce Agent Knowledge history."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str], cwd: Path, dry_run: bool) -> subprocess.CompletedProcess[str]:
    if dry_run:
        print(" ".join(command))
        return subprocess.CompletedProcess(command, 0, "", "")
    return subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def git_value(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def print_completed(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout.strip():
        print(completed.stdout.strip())
    if completed.stderr.strip():
        print(completed.stderr.strip(), file=sys.stderr)


def record_history(args: argparse.Namespace, root: Path, remote_branch: str, command: list[str], result: str) -> int:
    commit = git_value(["git", "rev-parse", "HEAD"], root)
    history_script = Path(__file__).with_name("knowledge_history.py")
    history_command = [
        sys.executable,
        str(history_script),
        "--project-root",
        str(root),
        "--action",
        "git-push",
        "--requirements",
        args.requirements,
        "--remote",
        args.remote,
        "--branch",
        remote_branch,
        "--commit",
        commit,
        "--summary",
        args.summary or f"Push {args.branch} to {args.remote}/{remote_branch}.",
        "--result",
        result,
        "--command",
        " ".join(command),
    ]
    for item in args.metadata:
        history_command.extend(["--metadata", item])
    history = subprocess.run(history_command, cwd=root, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
    print_completed(history)
    return history.returncode


def commit_history(root: Path, branch: str, dry_run: bool) -> int:
    paths = [
        ".salesforce-agent-knowledge/history/project-history.md",
        ".salesforce-agent-knowledge/history/events",
        ".salesforce-agent-knowledge/markdown-index.md",
    ]
    if dry_run:
        print("git add " + " ".join(paths))
        print(f"git commit -m \"Record Knowledge history for {branch} push\"")
        return 0
    add = run(["git", "add", *paths], root, dry_run=False)
    print_completed(add)
    if add.returncode != 0:
        return add.returncode
    diff = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *paths], cwd=root, check=False)
    if diff.returncode == 0:
        return 0
    commit = run(["git", "commit", "-m", f"Record Knowledge history for {branch} push"], root, dry_run=False)
    print_completed(commit)
    return commit.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Push a remote branch and record the push in Knowledge history.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--remote-branch")
    parser.add_argument("--set-upstream", action="store_true")
    parser.add_argument("--requirements", required=True)
    parser.add_argument("--metadata", action="append", required=True)
    parser.add_argument("--summary")
    parser.add_argument("--no-commit-history", action="store_true", help="Record local history without committing it before push. Remote branch will not include the new history entry until a later commit/push.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    remote_branch = args.remote_branch or args.branch
    command = ["git", "push"]
    if args.set_upstream:
        command.append("--set-upstream")
    command.extend([args.remote, f"{args.branch}:{remote_branch}"])

    if not args.dry_run:
        history_code = record_history(args, root, remote_branch, command, "prepared for remote push")
        if history_code != 0:
            return history_code
        if not args.no_commit_history:
            commit_code = commit_history(root, remote_branch, dry_run=False)
            if commit_code != 0:
                return commit_code

    completed = run(command, root, args.dry_run)
    print_completed(completed)
    if completed.returncode != 0:
        return completed.returncode
    if args.dry_run:
        return 0

    return record_history(args, root, remote_branch, command, "push succeeded") if args.no_commit_history else 0


if __name__ == "__main__":
    raise SystemExit(main())
