from __future__ import annotations

import subprocess
import sys

from conftest import ROOT


def test_validate_skill_script_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_skill.py"), "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert '"ok": true' in completed.stdout


def test_sync_agent_instructions_check_passes() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_agent_instructions.py"), "--check", "--json"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert '"stale": false' in completed.stdout
