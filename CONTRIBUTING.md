# Contributing

Thanks for helping improve Salesforce AI Agent Optimizer. Keep contributions lightweight, Salesforce-safe, and token-efficient.

## Principles

- Preserve Salesforce-first, configuration-first solutioning.
- Prefer minimal, reversible patches.
- Keep `SKILL.md` concise; move detailed guidance into focused `references/` files.
- Do not duplicate long instructions across agent adapters.
- Do not add speculative Salesforce facts. Use official Salesforce sources for release-sensitive behavior.
- Keep destructive-operation and least-privilege guardrails strict.

## Development Setup

```bash
python -m pip install --upgrade pip PyYAML pytest
```

## Required Checks

Run these before opening a pull request:

```bash
python scripts/sync_agent_instructions.py
python scripts/sync_agent_instructions.py --check
python scripts/validate_skill.py
python scripts/self_test.py --json
python -m pytest
```

## Versioning

Follow `VERSIONING.md`:

- Patch: bug fix or small correction.
- Minor: new feature, validation behavior, product/package reference, command, or minor refactor.
- Major: extensive refactor, many new capabilities, breaking workflow changes, or changed installation model.

Every release update must change `VERSION`, `CHANGELOG.md`, relevant README/wiki content, generated adapters, and tests when behavior changes.

## Pull Request Checklist

- The change is scoped to the stated requirement.
- Generated agent adapters are synchronized.
- New behavior is covered by pytest or `scripts/self_test.py`.
- README/wiki changes stay aligned across supported languages when user-facing behavior changes.
- No credentials, org data, customer data, or secrets are included.
