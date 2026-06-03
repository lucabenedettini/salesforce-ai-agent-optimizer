---
name: salesforce-agent-optimizer
description: Repository-local Salesforce Agent Skill shim for Codex. Use the root SKILL.md plus references and scripts for Salesforce planning, implementation, validation, package.xml, org inspection, least privilege, and destructive-operation guardrails.
license: MIT
compatibility:
  agents:
    - Codex
  platforms:
    - Windows
    - macOS
    - Linux
  prerequisites:
    - Python 3.10+
    - Git
    - Salesforce CLI
metadata:
  version: 0.5.1
---

# Salesforce Agent Optimizer Repo Skill

This is the repository-native Codex discovery entry. The canonical skill is at `../../../SKILL.md`.

When this skill is selected:

- Read `../../../SKILL.md` first.
- Use `../../../references/` only as needed for the task.
- Use `../../../scripts/` for deterministic Salesforce CLI, Knowledge, manifest, history, and validation workflows.
- Keep context compact and preserve the Salesforce-first, least-privilege, minimal-patch, destructive-guardrail behavior.
