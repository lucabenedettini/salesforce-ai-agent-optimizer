# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer is an MIT-licensed `sfao` CLI and agent skill for Codex, Claude Code, and GitHub Copilot.

Current version: `2.0.0`

It helps AI agents work on Salesforce projects with Salesforce-first planning, configuration before custom code, minimal reversible changes, local Knowledge, token-efficient Salesforce CLI usage, least-privilege checks, explicit org aliases, package.xml awareness, and destructive-operation guardrails.

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

Use `uv tool install` or `python -m pipx install` for isolated CLI installs. Plain `python -m pip install` also works when you intentionally want `sfao` in the active Python environment.

## Install

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao validate
```

Alternatives:

```bash
python -m pipx install salesforce-agent-optimizer
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
```

`sfao install` installs project-scoped adapters for all supported agents. Use `sfao install --user --platform all` only when you want a user-scoped Codex/Claude install.

## Main Commands

```bash
sfao version
sfao install
sfao install --project --platform all
sfao update --project --platform all
sfao uninstall --project --platform all --yes
sfao doctor
sfao doctor --verbose
sfao validate
sfao validate --json
sfao knowledge init --project-root .
sfao knowledge refresh --project-root .
sfao knowledge doctor --project-root .
sfao version-context scaffold
sfao version-context update
sfao version-context validate
```

For org operations the agent must ask for an explicit org alias. Production orgs are read-only through the skill guardrails.

## Agent Workflow

Installed agents must follow the same visible phases for information requests, bugfixes, implementation, architecture, reviews, org inspection, and release work:

1. `Request review`
2. `Planning evidence`
3. `Approval`
4. `Implementation`
5. `Validation`
6. `Completion`

During each phase the agent must state the tool or command it is using or planning. For Salesforce CLI access it must show the compact `sfao`, `scripts/sf_agent_cli.py`, or official `sf` command shape with aliases and secrets redacted.

## Safety

- Prefer Salesforce configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before custom code.
- Inspect local Knowledge before changing Salesforce metadata.
- Apply least privilege before access, sharing, UI, package, integration, or automation changes.
- Do not retrieve or parse all org metadata unless the user asks for broad analysis or the task requires it.
- Never delete data or metadata without separate explicit approval for the exact scope.
- Never expose Salesforce secrets or customer data without separate explicit approval for the exact scope.
- Generate `package.xml` for added or modified metadata.
- Ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedures after implementation.

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Alternatives:

```bash
python -m pipx upgrade salesforce-agent-optimizer
python -m pip install --upgrade salesforce-agent-optimizer
```

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

Alternative:

```bash
python -m pipx uninstall salesforce-agent-optimizer
```

## More Documentation

Detailed installation, command behavior, troubleshooting, publishing, release, and versioning docs live in `docs/wiki/`.

## License

MIT. Anyone can use, copy, modify, distribute, and fork this repository under the terms of `LICENSE`.
