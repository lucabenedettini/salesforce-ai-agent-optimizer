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
