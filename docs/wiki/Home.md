# Salesforce AI Agent Optimizer

Salesforce AI Agent Optimizer is a public, MIT-licensed skill and toolkit for AI agents working on Salesforce projects.

It helps Codex, Claude Code, GitHub Copilot, and similar agents plan and implement Salesforce work with:

- Salesforce-first solution design.
- Configuration before custom code.
- Minimal, reviewable patches.
- Token-efficient Salesforce CLI usage.
- Local project Knowledge generated from metadata.
- Product and AppExchange package context before planning.
- Current Salesforce release/API/SOAP/package version context with `/sf-version-update-skill`.
- Metadata dependency planning.
- Least-privilege planning with current-org access inspection before permission changes.
- Testing guardrails for Apex, Flow, and other testable metadata.
- Required package.xml generation for added or modified metadata.
- Destructive-operation approval guardrails for data and metadata deletion.
- Native Codex, Claude Code, and GitHub Copilot install targets.
- Validation handoff and retry discipline.
- Deploy and remote push history tracking.
- End-of-development handoff files: release notes, technical specifications, impact assessment, user testing, and manual procedures.

The Codex skill name remains `salesforce-agent-optimizer`. The GitHub repository name is `salesforce-ai-agent-optimizer` for clearer discovery by humans, search engines, and AI agents.

## Start Here

- Install from GitHub: `https://github.com/lucabenedettini/salesforce-ai-agent-optimizer`
- Current version: `0.6.1`
- Version policy: see `VERSIONING.md`
- Change history: see `CHANGELOG.md`

## Core Command

Use `/sf-init-project-skill` to build or refresh `.salesforce-agent-knowledge/` for a Salesforce project.

Use `/sf-version-update-skill` to refresh Salesforce release/API/SOAP/package guidance from official Salesforce sources.

Before planning, an agent should:

1. Start from `references/routing.md` and load only task-relevant references.
2. Identify products/packages from `references/products-packages/index.md`.
3. Read `references/salesforce-current-version.md` for release/API/package-sensitive work.
4. Read only relevant product/package files.
5. Read `references/metadata-dependencies.md`.
6. Read `references/least-privilege-planning.md` for access, sharing, UI, integration, automation, or package exposure.
7. Read the local project Knowledge.
8. Inspect source metadata and targeted org access before modifying.

Agent adapters are synchronized from `references/agent-instruction-spine.md` with:

```bash
python scripts/sync_agent_instructions.py --check
```

At the end of development, the agent asks whether to generate delivery artifacts using `references/completion-artifacts.md`.

Before validation handoff, the agent generates `package.xml` using `references/testing-and-manifest-guardrails.md`.

Before any destructive action, the agent reads `references/deletion-guardrails.md` and gets separate explicit approval.
