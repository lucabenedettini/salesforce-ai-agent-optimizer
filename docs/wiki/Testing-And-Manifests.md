# Testing And Manifests

Salesforce AI Agent Optimizer now includes explicit testing and package manifest guardrails.

## Testing Guardrails

- Changed Apex must be at least 80% covered.
- Prefer 90%-100% coverage for new, critical, reusable, security, integration, async, invocable, and trigger-handler Apex.
- Coverage is not enough by itself: assertions must prove behavior.
- Flow and other testable metadata must be tested when Salesforce and the project support it.
- Unsupported automatic tests must be replaced by documented manual user tests and a clear reason.

## Required Package Manifest

At the end of implementation, the agent must generate a `package.xml` with every metadata component added or modified for the approved request.

Default location:

```text
release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml
```

Preferred command:

```bash
python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml --from-git-status
```

Deleted metadata is not included in `package.xml`; destructive deploys require `destructiveChanges.xml` and explicit approval.

Canonical rules live in `references/testing-and-manifest-guardrails.md`.
