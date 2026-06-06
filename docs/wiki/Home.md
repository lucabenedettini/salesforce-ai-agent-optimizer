# Salesforce AI Agent Optimizer

Salesforce AI Agent Optimizer is a public, MIT-licensed skill and toolkit for AI agents working on Salesforce projects.

It helps Codex, Claude Code, GitHub Copilot, and similar agents plan and implement Salesforce work with:

- Salesforce-first solution design.
- Configuration before custom code.
- Minimal, reviewable patches.
- Token-efficient Salesforce CLI usage.
- Local project Knowledge generated from metadata.
- Curated project memory for durable decisions, lessons, risks, and follow-ups.
- Product and AppExchange package context before planning.
- Current Salesforce release/API/SOAP/package version context with `sfao version-context`.
- Metadata dependency planning.
- Least-privilege planning with current-org access inspection before permission changes.
- Privacy/security planning for secrets, customer data, org access, exports, integrations, and Knowledge.
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
- Current version: `2.1.0`
- Version policy: see `VERSIONING.md`
- Change history: see `CHANGELOG.md`
- End-user install guide: see `Installation.md`
- Memory and specialized guidance: see `Memory-And-Guidance.md`
- Privacy and security model: see `Privacy-And-Security.md`
- Maintainer packaging and publishing guide: see `Packaging-And-Publishing.md`

## Core Commands

Install all agent adapters:

```bash
sfao install --project --platform all
```

Build or refresh `.salesforce-agent-knowledge/` for a Salesforce project:

```bash
sfao knowledge init --project-root .
sfao knowledge refresh --project-root .
sfao memory init --project-root .
sfao memory doctor --project-root .
```

These commands print progress in non-JSON mode while scanning, summarizing, and
writing metadata Knowledge files.

Refresh Salesforce release/API/SOAP/package guidance from official Salesforce sources:

```bash
sfao version-context scaffold
sfao version-context update
```

Use `sfao version-context update --offline` to skip network checks. Non-JSON
mode prints progress while checking official Salesforce sources.

Before planning, an agent should:

1. Start from `references/routing.md` and load only task-relevant references.
2. Identify products/packages from `references/products-packages/index.md`.
3. Read `references/salesforce-current-version.md` for release/API/package-sensitive work.
4. Read only relevant product/package files.
5. Read `references/metadata-dependencies.md`.
6. Read `references/least-privilege-planning.md` for access, sharing, UI, integration, automation, or package exposure.
7. Read the local project Knowledge, project history, and `memory.md` when present.
8. Inspect source metadata and targeted org access before modifying.

Agent adapters are synchronized from `references/agent-instruction-spine.md` with:

```bash
python scripts/sync_agent_instructions.py --check
```

At the end of development, the agent asks whether to generate delivery artifacts using `references/completion-artifacts.md`.

Before validation handoff, the agent generates `package.xml` using `references/testing-and-manifest-guardrails.md`.

Before any destructive action, the agent reads `references/deletion-guardrails.md` and gets separate explicit approval.

## Agent Response Contract

For every Salesforce project request, the installed agent must show the current phase:

- `Request review`
- `Planning evidence`
- `Approval`
- `Implementation`
- `Validation`
- `Completion`

Every phase must also name the tool or command used or planned. If no tool is used, the agent writes `Tool/command: none`.

For Salesforce org access, the agent must show the compact command shape, for example:

```bash
sfao command search "permission account" --toolset permissions
python scripts/sf_agent_cli.py org-inspect --target-org <alias> --select org_display.username,organization.records.0.IsSandbox
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username <user> --sobject Account
```

Aliases are allowed; secrets, tokens, auth URLs, passwords, and private keys must be redacted.

## `sfao` Command Summary

| Command | Purpose |
| --- | --- |
| `sfao version` | Print installed package version. |
| `sfao install` | Install all project-scoped adapters in the current project. |
| `sfao update --project --platform all` | Refresh managed adapters and newly introduced templates. |
| `sfao uninstall --project --platform all --yes` | Remove generated adapter files only. |
| `sfao doctor` | Diagnose package, OS, Git, Salesforce CLI, adapters, PATH, and validation status. |
| `sfao validate` | Validate source/install shape, versions, frontmatter, YAML/TOML/JSON/Python, generated adapters, and Salesforce metadata guardrails. |
| `sfao knowledge init --project-root .` | Build compact local Salesforce project Knowledge. |
| `sfao knowledge refresh --project-root .` | Refresh Knowledge after metadata changes. |
| `sfao memory init --project-root .` | Create curated project memory. |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | Add a compact durable memory entry. |
| `sfao memory compact --project-root .` | Keep project memory token-efficient. |
| `sfao memory doctor --project-root .` | Validate memory structure and secret redaction. |
| `sfao version-context update` | Refresh release/API/package context from official Salesforce sources. |
| `sfao command search` | Find a safe Salesforce CLI facade command from the internal registry. |
| `sfao command payload-example` | Show a compact payload for a facade command. |
| `sfao command execute` | Execute a registry payload through the Salesforce CLI facade. |
| `sfao soql build` | Build focused SOQL plus a ready-to-run `data-query` payload. |
| `sfao permissions explain` | Summarize why access exists from `access-inspect` output. |
| `sfao live-test` | Run opt-in real-org CLI facade validation; write/destructive tests require sandbox/scratch evidence and explicit confirmation. |

## Installed Paths

Codex:

```text
.agents/skills/salesforce-agent-optimizer/SKILL.md
.agents/skills/salesforce-agent-optimizer/references/
.agents/skills/salesforce-agent-optimizer/scripts/
.agents/skills/salesforce-agent-optimizer/agents/openai.yaml
```

Claude Code:

```text
.claude/skills/salesforce-agent-optimizer/SKILL.md
.claude/skills/salesforce-agent-optimizer/references/
.claude/skills/salesforce-agent-optimizer/scripts/
```

GitHub Copilot:

```text
AGENTS.md
.github/skills/salesforce-agent-optimizer/SKILL.md
.github/skills/salesforce-agent-optimizer/references/
.github/skills/salesforce-agent-optimizer/scripts/
.github/copilot-instructions.md
.github/instructions/salesforce-agent-optimizer.instructions.md
```

Trigger evals:

```text
evals/salesforce-agent-optimizer-trigger-evals.json
evals/salesforce-agent-optimizer-quality-evals.json
```
