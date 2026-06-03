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

- `0.5.1`: compatibility hotfix for valid skill frontmatter, native Codex/Claude Code/GitHub Copilot install targets, local validation, and minimal cross-platform CI.

## Examples

- `0.0.2`: fix Windows path handling in one script.
- `0.1.0`: add a new product/package reference set.
- `1.0.0`: redesign the skill workflow, CLI facade, and Knowledge format together.
