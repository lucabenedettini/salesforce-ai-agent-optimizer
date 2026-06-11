# Versioning Policy

This repository starts at version `0.0.1` and uses a simple semantic versioning policy:

- Patch version (`0.0.x`): bug fixes, documentation corrections, small safety fixes, compatibility fixes, and typo corrections.
- Minor version (`0.x.0`): new feature, new product/package reference, new command, new validation behavior, or minor refactor that preserves the public workflow.
- Major version (`x.0.0`): extensive refactor, many new capabilities, breaking workflow changes, changed installation model, or large redesign of the skill structure.

Every version update must include:

- `VERSION` updated to the new version.
- `CHANGELOG.md` entry with date, change type, and specific details.
- Git tag `v<version>`.
- GitHub release `v<version>` when published.

## Current Version

- `2.2.4`: project install path hotfix for root-level `references/` and `scripts/`, plus adapter-local fallback instructions for agents that resolve resources from skill folders.
- `2.2.3`: local report and validation hardening patch for observable project health, command hints, destructive wording, routing efficiency, and Agentforce documentation consistency.
- `1.2.2`: privacy and portability bugfix that removes local machine paths from distributed resources and makes `sfao doctor` PATH diagnostics generic.
- `1.2.1`: command usability bugfix for PATH-safe pipx/pip update docs and visible Knowledge/version-context progress output.
- `1.2.0`: Field Service Mobile and mobile Flow planning reference with mandatory web/mobile and online/offline specification preflight for larger work.
- `1.1.1`: installer bugfix that makes bare `sfao install` project-scoped by default and copies Copilot-local `references/` and `scripts/`.
- `1.1.0`: Copilot project-skill compatibility and lightweight Salesforce metadata micro-validators for Apex, Flow, LWC, permissions, and `package.xml`.
- `1.0.5`: installer update bugfix that lets `sfao update` add newly introduced managed templates, including evals, to existing project installs.
- `1.0.4`: installer and planning bugfix that merges Copilot guidance into existing agent files, installs evals, and adds mandatory multi-country/multi-currency planning checks.
- `1.0.3`: Copilot compliance bugfix that makes mandatory phase gates visible as an operational response contract before metadata parsing or implementation.
- `1.0.2`: instruction-flow bugfix that makes request review, planning, implementation decision, validation, failure handling, and completion gates mandatory for all Salesforce project requests.
- `1.0.1`: public distribution bugfix for isolated `sfao validate` runs from PyPI, `uv`, and `pipx` installs without development-only dependencies.
- `1.0.0`: major public distribution release with stable `sfao` install, update, uninstall, Knowledge, version-context, validation, build, release, and PyPI Trusted Publishing workflows.
- `0.6.1`: packaging and installer hotfix for `pip`, `pipx`, `uv`, the `sfao` CLI, packaged templates, release artifacts, and installer validation.
- `0.6.0`: instruction architecture refactor with concise routing, generated agent adapters, trigger evals, pytest coverage, and public maintenance files.
- `0.5.1`: compatibility hotfix for valid skill frontmatter, native Codex/Claude Code/GitHub Copilot install targets, local validation, and minimal cross-platform CI.

## Examples

- `0.0.2`: fix Windows path handling in one script.
- `0.1.0`: add a new product/package reference set.
- `1.0.0`: redesign the skill workflow, CLI facade, and Knowledge format together.
