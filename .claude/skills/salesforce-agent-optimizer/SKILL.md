---
name: salesforce-agent-optimizer
description: Claude Code Salesforce Agent Skill shim. Use the root Salesforce Agent Optimizer guidance for Salesforce architecture, metadata, Apex, LWC, Flow, package.xml, org inspection, least privilege, and destructive-operation guardrails.
license: MIT
compatibility:
  agents:
    - Claude Code
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

# Salesforce Agent Optimizer For Claude Code

Read `../../../SKILL.md` as the canonical instruction file and use `../../../references/` plus `../../../scripts/` on demand.

Follow the same compact workflow:

- Restate the Salesforce request and ask only necessary questions.
- Plan from project Knowledge, product/package context, metadata dependencies, and least-privilege evidence.
- Prefer configuration and standard Salesforce capabilities before custom code.
- Ask for approval before changes and separate explicit approval before destructive actions.
- Validate changes, generate `package.xml` for added/modified metadata, and ask whether to push only after validation passes.
