# Changelog

All notable changes to Salesforce Agent Optimizer are recorded here.

## 0.1.0 - 2026-06-02

- Created the `salesforce-agent-optimizer` Codex skill.
- Added Salesforce delivery methodology with request restatement, focused clarification, approval-gated planning, minimal implementation, validation handoff, retry limit, and final push confirmation.
- Added Salesforce architecture, backend Apex, frontend LWC, official-source, and token-discipline references.
- Added `/sf-init-project-skill` command adapter to build or refresh `.salesforce-agent-knowledge/`.
- Added Knowledge generation with indexed Markdown metadata pages, wiki pages, `markdown-index.md`, machine-readable indexes, and project history.
- Added deploy and remote push history tracking with requirements and modified metadata.
- Added token-efficient Salesforce CLI facade with explicit org alias handling, secure auth commands, compact redacted JSON output, dry-run support, production read-only guardrails, and `safe-run` for official `sf` commands.
- Generated a compact Salesforce CLI command catalog from installed Salesforce CLI commands.
- Added adapters for Codex, Claude Code, and GitHub Copilot.
- Added cross-platform local self-tests for Windows, macOS, and Linux assumptions.
- Added public README, MIT license, and GitHub publishing guidance.
