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

`0.1.0` adds end-of-development handoff artifact guidance.

`0.0.1` is the initial public baseline with the full skill package, CLI facade, Knowledge workflow, product/package references, metadata dependency planning, and agent adapters.
