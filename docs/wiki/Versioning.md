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

`0.5.0` adds least-privilege planning guardrails, Spanish README, and the read-only `access-inspect` command for current-org permission evidence.

`0.4.0` adds destructive-operation approval guardrails, CLI enforcement for delete/uninstall/destructive commands, and English/Italian/Simplified Chinese README files.

`0.3.0` adds `/sf-version-update-skill`, current Salesforce release/API/SOAP/package version context, and repeatable version-resource refresh.

`0.2.0` adds testing guardrails for Apex, Flow, and other testable metadata plus required `package.xml` generation for added or modified metadata.

`0.1.0` adds end-of-development handoff artifact guidance.

`0.0.1` is the initial public baseline with the full skill package, CLI facade, Knowledge workflow, product/package references, metadata dependency planning, and agent adapters.
