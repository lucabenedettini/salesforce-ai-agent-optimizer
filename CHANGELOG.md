# Changelog

All notable changes to Salesforce AI Agent Optimizer are recorded here.

This project starts at `0.0.1`. Version bumps follow `VERSIONING.md`:

- Patch: bug fix or small correction.
- Minor: new feature or minor refactor.
- Major: extensive refactor or many added capabilities.

## 0.0.1 - 2026-06-03

Initial public baseline.

### Added

- Created the `salesforce-agent-optimizer` Codex skill package.
- Added public repository packaging with MIT license, README, changelog, version file, and GitHub installation instructions.
- Added versioning policy with `VERSIONING.md`, `VERSION`, tag/release requirements, and patch/minor/major bump rules.
- Added project wiki source pages under `docs/wiki/` for overview, principles, installation, and versioning.
- Added Salesforce delivery methodology with request restatement, focused clarification, approval-gated planning, minimal implementation, validation handoff, retry limit, final push confirmation, and optional PDF task estimate prompt after planning.
- Added `/sf-init-project-skill` command adapter to build or refresh `.salesforce-agent-knowledge/`.
- Added Knowledge generation with indexed Markdown metadata pages, wiki pages, `markdown-index.md`, machine-readable indexes, and project history.
- Added deploy and remote push history tracking with requirements and modified metadata.
- Added token-efficient Salesforce CLI facade with explicit org alias handling, secure auth commands, compact redacted JSON output, dry-run support, production read-only guardrails, and `safe-run` for official `sf` commands.
- Generated a compact Salesforce CLI command catalog from installed Salesforce CLI commands.
- Added Salesforce architecture, backend Apex, frontend LWC, official-source, token-discipline, metadata dependency, and product/package planning references.
- Added product/package Markdown references for core Salesforce products, Salesforce CPQ, Salesforce Field Service, mobile development, popular AppExchange packages, and Advanced Approvals.
- Added adapters for Codex, Claude Code, and GitHub Copilot.
- Added cross-platform local self-tests for Windows, macOS, and Linux assumptions.

### Versioning

- Set initial version to `0.0.1`.
- Future bug fixes increment patch version.
- Future features or minor refactors increment minor version.
- Future extensive refactors or many added capabilities increment major version.
