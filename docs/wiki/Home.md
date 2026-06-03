# Salesforce AI Agent Optimizer

Salesforce AI Agent Optimizer is a public, MIT-licensed skill and toolkit for AI agents working on Salesforce projects.

It helps Codex, Claude Code, GitHub Copilot, and similar agents plan and implement Salesforce work with:

- Salesforce-first solution design.
- Configuration before custom code.
- Minimal, reviewable patches.
- Token-efficient Salesforce CLI usage.
- Local project Knowledge generated from metadata.
- Product and AppExchange package context before planning.
- Metadata dependency planning.
- Validation handoff and retry discipline.
- Deploy and remote push history tracking.
- End-of-development handoff files: release notes, technical specifications, impact assessment, user testing, and manual procedures.

The Codex skill name remains `salesforce-agent-optimizer`. The GitHub repository name is `salesforce-ai-agent-optimizer` for clearer discovery by humans, search engines, and AI agents.

## Start Here

- Install from GitHub: `https://github.com/lucabenedettini/salesforce-ai-agent-optimizer`
- Current version: `0.1.0`
- Version policy: see `VERSIONING.md`
- Change history: see `CHANGELOG.md`

## Core Command

Use `/sf-init-project-skill` to build or refresh `.salesforce-agent-knowledge/` for a Salesforce project.

Before planning, an agent should:

1. Identify products/packages from `references/products-packages/index.md`.
2. Read only relevant product/package files.
3. Read `references/metadata-dependencies.md`.
4. Read the local project Knowledge.
5. Inspect source metadata before modifying.

At the end of development, the agent asks whether to generate delivery artifacts using `references/completion-artifacts.md`.
