# Versioning

Salesforce AI Agent Optimizer starts at version `0.0.1`.

## Rules

- Patch version (`0.0.x`): bug fixes, documentation corrections, small safety fixes, compatibility fixes, and typo corrections.
- Minor version (`0.x.0`): new feature, new product/package reference, new command, new validation behavior, or minor refactor that preserves the public workflow.
- Major version (`x.0.0`): extensive refactor, many new capabilities, breaking workflow changes, changed installation model, or large redesign of the skill structure.

## Required Release Steps

Every version update must include:

1. Update `VERSION`.
2. Add a specific `CHANGELOG.md` entry.
3. Commit the change.
4. Create tag `v<version>`.
5. Push the tag.
6. Publish a GitHub release.

## Current Version

`2.0.0` adds the CLI-only agent tool registry, command facade, dynamic toolsets, compact SOQL helper, Permission Analyzer v2 summaries, real-org `sfao live-test`, compact metadata/schema output, and expanded mocked/live validation while preserving production read-only and destructive-operation guardrails.

## Recent Stable Lines

- `1.2.x`: installer, PATH, progress, and validation fixes.
- `1.1.x`: Copilot project skill compatibility, eval installation, and metadata micro-validators.
- `1.0.x`: public distribution baseline with stable install, update, uninstall, Knowledge, version-context, validation, build, release, and PyPI workflows.
- `0.x`: early public skill architecture, guardrails, multilingual README files, and packaging foundation.

For exact historical entries, use `CHANGELOG.md`; avoid duplicating long release history in the wiki.
