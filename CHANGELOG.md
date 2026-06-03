# Changelog

All notable changes to Salesforce AI Agent Optimizer are recorded here.

This project starts at `0.0.1`. Version bumps follow `VERSIONING.md`:

- Patch: bug fix or small correction.
- Minor: new feature or minor refactor.
- Major: extensive refactor or many added capabilities.

## [0.6.1] - 2026-06-03

### Added

- Added Python package metadata for installation through `pip`, `pipx`, and `uv`.
- Added the `sfao` CLI entry point.
- Added `sfao install`, `sfao doctor`, `sfao validate`, and `sfao version`.
- Added project-scoped installation for Codex, Claude Code, and GitHub Copilot.
- Added package templates for installable agent adapters.
- Added build and release documentation.
- Added release manifest and checksum generation support.

### Fixed

- Fixed multiline formatting validation for Markdown, YAML, TOML, JSON, and Python files where required.
- Fixed `SKILL.md` frontmatter validation through reusable package validation code.
- Fixed generated Codex and Claude skill shims to include managed-file markers.
- Fixed `agents/openai.yaml` version alignment through generated adapter synchronization.
- Added validation against collapsed files, missing final newlines, CRLF drift, and stale generated adapters.

### Preserved

- Existing Salesforce delivery methodology.
- Configuration-first solutioning.
- Minimal-change approach.
- Token-efficiency principles.
- package.xml awareness.
- Destructive-operation guardrails.

## 0.6.0 - 2026-06-03

### Added

- Added `references/routing.md` so agents can load only the task-relevant Salesforce guidance before planning.
- Added `references/agent-instruction-spine.md` as the canonical lightweight instruction spine for generated agent adapters.
- Added `scripts/sync_agent_instructions.py` to synchronize `AGENTS.md`, Codex repo shims, Claude Code shims, GitHub Copilot instructions, and `agents/openai.yaml`.
- Added `evals/trigger-evals.json` with realistic should-trigger and should-not-trigger prompts.
- Added pytest coverage for skill validation, adapter synchronization, package manifest generation, Knowledge init, destructive guardrails, and Windows path metadata mapping.
- Added `SECURITY.md`, `CONTRIBUTING.md`, and GitHub issue templates for public repository maintenance.

### Changed

- Refactored `SKILL.md` into a concise router that preserves the Salesforce-first, token-efficient, least-privilege, deletion-safe workflow while moving detailed guidance into `references/`.
- Deduplicated long agent-specific instructions by generating them from canonical sources.
- Updated CI to run pytest across Windows, macOS, and Linux with Python 3.10, 3.11, and 3.12.
- Updated README files, wiki source pages, versioning files, and adapter metadata for version `0.6.0`.

## 0.5.1 - 2026-06-03

### Added

- Added compatibility-hotfix validation with `scripts/validate_skill.py` for SKILL frontmatter, YAML, JSON, Python compile checks, required native-agent files, final newlines, and one-line collapse detection.
- Added native installation targets for Codex (`.agents/skills/salesforce-agent-optimizer/SKILL.md`), Claude Code (`.claude/skills/salesforce-agent-optimizer/SKILL.md`), and GitHub Copilot (`AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/salesforce-agent-optimizer.instructions.md`).
- Added minimal cross-platform GitHub Actions validation on Windows, macOS, and Linux with Python 3.10, 3.11, and 3.12.
- Added `pyproject.toml` with Python `>=3.10` and optional dev dependencies.

### Changed

- Fixed `SKILL.md` frontmatter to include concise description, `license: MIT`, compatibility metadata, and `metadata.version` matching `VERSION`.
- Updated `agents/openai.yaml`, `references/agent-installation.md`, README files, VERSIONING, and wiki version notes for installability and version `0.5.1`.

## 0.5.0 - 2026-06-03

### Added

- Added mandatory least-privilege planning guardrails for Salesforce access, sharing, integration, package, automation, and UI exposure decisions.
- Added `references/least-privilege-planning.md` with current-org access inspection, persona-based planning, uncertainty handling, and official Salesforce source links.
- Added read-only `access-inspect` to `scripts/sf_agent_cli.py` for compact inspection of users, permission set assignments, permission set groups, permission set licenses, and relevant CRUD/FLS.
- Added Spanish README and self-test coverage for multilingual README least-privilege alignment.

### Changed

- Updated delivery methodology, metadata dependency planning, architecture guidance, agent adapters, README files, wiki sources, and official-source links so access changes are planned from current org evidence.

## 0.4.0 - 2026-06-03

### Added

- Added mandatory destructive-operation guardrails for Salesforce data deletes, metadata deletes, package uninstalls, source deletes, purge/hard-delete operations, and destructive changes.
- Added `references/deletion-guardrails.md` with explicit approval, evidence, backup, rollback, and uncertainty-handling rules.
- Updated `scripts/sf_agent_cli.py` to block destructive commands unless `--delete-approval "I explicitly approve this deletion"` is provided.
- Added self-tests for destructive-operation approval enforcement.
- Added English, Italian, and Simplified Chinese README files and a self-test that keeps their version and delete guardrail references aligned.

### Changed

- Reworked README content for token efficiency and clearer public installation guidance.
- Updated delivery methodology, agent adapters, official sources, manifest rules, and completion artifacts to avoid invented facts and to require user choice when planning evidence is uncertain.

## 0.3.0 - 2026-06-03

### Added

- Added `/sf-version-update-skill` to refresh Salesforce release, API, SOAP API, Metadata API, LWC API, product, and package version context from official Salesforce sources.
- Added `references/salesforce-version.json` and `references/salesforce-current-version.md` with Summer '26 / API 67.0 version context, SOAP API guardrails, project API version rules, and package version policy.
- Added `references/version-update.md` and `scripts/sf_version_update.py` to make version context refresh repeatable.
- Updated product/package planning to read current Salesforce version context and to treat managed package versions as target-org-specific.
- Updated `generate_package_manifest.py` so fallback manifest API version comes from `references/salesforce-version.json`.
- Added portable `/sf-version-update-skill` adapter and updated Codex, Claude Code, GitHub Copilot, README, and wiki guidance.

## 0.2.0 - 2026-06-03

### Added

- Added testing guardrails for changed Apex, Flow, and other testable Salesforce metadata.
- Added required end-of-implementation `package.xml` generation for all added or modified metadata.
- Added `scripts/generate_package_manifest.py` to create compact Salesforce Metadata API manifests from explicit metadata, changed files, git status, or git refs.
- Added `references/testing-and-manifest-guardrails.md` with coverage thresholds, Flow/testable metadata guidance, official Salesforce references, and package.xml rules.
- Updated delivery methodology, completion artifacts, adapters, README, and wiki source pages for the new testing and manifest workflow.

## 0.1.0 - 2026-06-03

### Added

- Added end-of-development completion artifact workflow.
- Added `references/completion-artifacts.md` with required structures for `release-notes.md`, `technical-specifications.md`, `impact-assessment.md`, `user-testing.md`, and `manual-procedures.md`.
- Updated delivery methodology so agents ask whether to generate completion artifacts after development and before validation handoff.
- Updated Claude Code and GitHub Copilot adapters to follow the completion artifact prompt.

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
