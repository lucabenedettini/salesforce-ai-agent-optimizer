# Salesforce AI Agent Optimizer

English | [Italiano](README.it.md) | [Espanol](README.es.md) | [简体中文](README.zh-CN.md)

Salesforce AI Agent Optimizer is a public MIT-licensed skill for AI agents that work on Salesforce projects. It helps Codex, Claude Code, GitHub Copilot, and similar agents plan, implement, validate, package, and document Salesforce changes with compact context usage and strong safety guardrails.

The public repository is **Salesforce AI Agent Optimizer**. The Codex skill name remains `salesforce-agent-optimizer`.

Current version: `0.5.0`

## Core Principles

- Salesforce first: prefer standard capabilities, configuration, Flow, permission sets, LDS/UI API, named credentials, and managed package features before custom Apex, LWC, triggers, or integrations.
- Token efficiency: use progressive disclosure, indexed local Knowledge, compact CLI output, targeted source reads, and minimal patches.
- Local Knowledge: `/sf-init-project-skill` builds a compact Markdown index of project metadata inspired by the LLM wiki pattern.
- Agent-native CLI: `scripts/sf_agent_cli.py` wraps official Salesforce CLI commands with aliases, compact JSON, redaction, dry-run, production read-only protection, and delete approval enforcement.
- Least privilege: planning must inspect current org permissions for affected users/personas and grant only the minimum access needed.
- No invention: when evidence is missing, the agent must ask the user or present scenarios with tradeoffs.

## Safety Guardrails

- Production orgs are read-only for write, execute, and destructive operations through the facade.
- Every org/data/metadata command requires an explicit target org alias.
- Destructive operations are never automatic. Data delete, metadata delete, package uninstall, source delete, purge, hard delete, and `destructiveChanges.xml` deploys require separate user approval for the exact scope.
- The CLI blocks destructive commands unless this exact flag is provided after user approval:

```bash
--delete-approval "I explicitly approve this deletion"
```

- Deleted metadata belongs in `destructiveChanges.xml`, not `package.xml`.
- If a record set, metadata dependency, package version, or org behavior is uncertain, the agent must ask or present options.

## Main Commands

Build or refresh project Knowledge:

```text
/sf-init-project-skill
```

Refresh Salesforce release/API/SOAP/package version context from official Salesforce sources:

```text
/sf-version-update-skill
```

Run local tests:

```bash
python scripts/self_test.py --json
```

Generate a package manifest for added or modified metadata:

```bash
python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<date>-<change>/package.xml --from-git-status
```

Inspect installed packages in a target org:

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

Inspect current user access before planning permission changes:

```bash
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
```

Delete a record only after explicit approval:

```bash
python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id 001... --delete-approval "I explicitly approve this deletion"
```

## Installation

Ask Codex:

```text
Install the Salesforce AI Agent Optimizer skill from https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Codex installer command:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Claude Code:

- Merge `agents/claude-code.md` into `CLAUDE.md`.
- Copy `agents/sf-init-project-skill.md` to `.claude/commands/sf-init-project-skill.md`.
- Copy `agents/sf-version-update-skill.md` to `.claude/commands/sf-version-update-skill.md`.

GitHub Copilot:

- Merge `agents/github-copilot-instructions.md` into `.github/copilot-instructions.md`, or use `.github/instructions/salesforce-agent-optimizer.instructions.md`.

## Prerequisites

- Python 3.10+.
- Git.
- Salesforce DX project for metadata Knowledge, deploy, retrieve, or manifest workflows.
- Official Salesforce CLI available as `sf` for org operations.
- Authenticated org aliases. The agent must ask for aliases and must not rely on default orgs.
- Sandbox org for write/execute operations. Production is read-only.

Optional:

- PyYAML for Codex skill validation.
- Node.js/npm to install Salesforce CLI with `npm install -g @salesforce/cli`.
- Go and `cli-printing-press` only for CLI experimentation.

## Version Context

Verified on 2026-06-03:

- Salesforce release: Summer '26.
- Platform API, Metadata API, SOAP API: `67.0`.
- SOAP API `login()` is unavailable in API `65.0+`; Salesforce announced retirement of SOAP `login()` for API `31.0-64.0` with Summer '27.
- Managed package versions are target-org-specific. Inspect installed packages before assuming namespace, object names, or feature availability.

Canonical resources:

- `references/salesforce-current-version.md`
- `references/salesforce-version.json`
- `references/version-update.md`

## Validation And Handoff

The delivery methodology requires:

- Restate the request.
- Ask focused questions only when needed.
- Identify relevant Salesforce products/packages and metadata dependencies.
- Plan minimal changes and ask for approval.
- Ask separately for destructive approval when needed.
- Implement only approved work.
- Generate `package.xml` for added/modified metadata.
- Offer release notes, technical specifications, impact assessment, user testing, and manual procedure files.
- Validate with tests or a validation subagent.
- Ask whether to push and which branch after validation passes.

## Key Files

- `SKILL.md`: canonical skill instructions.
- `agents/`: Codex, Claude Code, GitHub Copilot, and slash-command adapters.
- `references/`: progressive-disclosure guidance for Salesforce architecture, products, CLI, testing, deletion, versions, and delivery.
- `scripts/sf_agent_cli.py`: safe Salesforce CLI facade.
- `scripts/sf_knowledge_init.py`: local metadata Knowledge generator.
- `scripts/generate_package_manifest.py`: `package.xml` generator.
- `scripts/git_knowledge_push.py`: remote push with Knowledge history.
- `scripts/self_test.py`: cross-platform local tests.

## Official Sources

- Salesforce CLI: https://developer.salesforce.com/tools/salesforcecli
- Salesforce CLI reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata API deploy and destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
- GraphQL delete record: https://developer.salesforce.com/docs/platform/graphql/guide/mutations-delete.html
- LWC `deleteRecord`: https://developer.salesforce.com/docs/platform/lwc/guide/reference-delete-record.html
- Salesforce release notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5
- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure

## License

MIT. Everyone can use, copy, modify, distribute, and fork this repository under the terms in `LICENSE`.
