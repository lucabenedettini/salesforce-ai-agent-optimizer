# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer is an MIT-licensed `sfao` CLI and agent skill for Codex, Claude Code, and GitHub Copilot.

Current version: `2.2.4`

It helps AI agents work on Salesforce projects with Salesforce-first planning, configuration before custom code, minimal reversible changes, local Knowledge, token-efficient Salesforce CLI usage, least-privilege checks, explicit org aliases, package.xml awareness, and destructive-operation guardrails.

Specialized Salesforce guidance includes Apex, LWC, Flow, SOQL, deploy, data operations, and Agentforce; each file is loaded only when relevant and coordinates with the existing SFAO references.

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

`sfao install` installs project-scoped adapters for all supported agents. It also installs managed root-level `references/` and `scripts/`; agents use those first and fall back to the adapter-local skill folders when needed. Use `sfao install --user --platform all` only when you want a user-scoped Codex/Claude install.

## Main Commands

| Command | What it does and when to use it | Principle |
| --- | --- | --- |
| `sfao version` | Prints the installed package version. Use after install or upgrade. | Version clarity. |
| `sfao install` | Installs project-scoped adapters for supported agents in the current repo. Use once per Salesforce project. | Frictionless setup. |
| `sfao install --project --platform all` | Explicit project install for Codex, Claude Code, and GitHub Copilot. Use when onboarding a repo. | Agent compatibility. |
| `sfao update --project --platform all` | Refreshes managed generated adapters and templates after upgrading the package. | Safe upgrade. |
| `sfao uninstall --project --platform all --yes` | Removes generated SFAO adapter files only. Use when removing the skill from a project. | Reversible changes. |
| `sfao doctor` | Checks Python, OS, Git, Salesforce CLI, installed adapters, PATH, and validation status. Use after install/update or when the skill is not visible. | Early diagnostics. |
| `sfao doctor --verbose` | Shows detailed diagnostics. Use when troubleshooting warnings. | Transparent failure analysis. |
| `sfao validate` | Validates skill files, versions, generated adapters, formats, and Salesforce metadata guardrails. Use before commits/releases. | Quality gate. |
| `sfao validate --json` | Emits machine-readable validation. Use in CI or agent validation steps. | Automation-friendly output. |
| `sfao report --project-root .` | Writes a local Markdown health snapshot for adapters, Knowledge, memory, guardrails, guidance, evals, and version context. Use before planning or handoff. | Observable local state. |
| `sfao knowledge init --project-root .` | Builds compact local Salesforce project Knowledge. Use before the first planning pass in a repo. | Knowledge before raw metadata. |
| `sfao knowledge refresh --project-root .` | Refreshes Knowledge after metadata changes. Use after meaningful Salesforce source changes. | Fresh planning evidence. |
| `sfao knowledge init --project-root . --scan-root` | Performs an intentional broad project scan. Use only when packageDirectories are not enough. | Token-efficient scope control. |
| `sfao knowledge doctor --project-root .` | Checks Knowledge structure. Use when the agent reports missing or stale Knowledge. | Reliable local context. |
| `sfao memory init --project-root .` | Creates curated project memory. Use when starting durable project learning. | Compact durable memory. |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | Adds a redacted durable lesson, decision, risk, or follow-up. Use after implementation or validation. | No raw logs, no secrets. |
| `sfao memory compact --project-root . --max-bytes 60000` | Keeps memory small and useful. Use when memory grows too large. | Token efficiency. |
| `sfao memory doctor --project-root .` | Validates memory structure and redaction. Use before relying on memory for planning. | Privacy-safe memory. |
| `sfao version-context scaffold` | Creates version-context reference files if missing. Use when bootstrapping references. | Official-source readiness. |
| `sfao version-context update` | Refreshes Salesforce release/API context from official Salesforce sources. Use when version context is stale or release-sensitive. | No invented behavior. |
| `sfao version-context validate --max-age-days 90` | Checks version-context freshness. Use in validation or before release-sensitive planning. | Current API evidence. |
| `sfao command search "permission account"` | Searches the internal safe Salesforce CLI facade registry. Use before running org commands. | Discover before execute. |
| `sfao command payload-example access-inspect` | Prints a compact payload example for a registered command. Use to avoid invented flags. | Schema-guided commands. |
| `sfao command execute --payload payload.json` | Executes one registered facade command through compact guardrails. Use only with explicit org alias where required. | Safe Salesforce CLI facade. |
| `sfao soql build --object Account --fields Id,Name` | Builds focused SOQL and a ready data-query payload. Use before querying org data. | Minimal data retrieval. |
| `sfao permissions explain --input access.json` | Summarizes access evidence from `access-inspect` output. Use for least-privilege planning. | Explainable access. |
| `sfao live-test --target-org <alias>` | Runs opt-in checks against a real org. Use only with an explicit non-production/scratch org alias for write/destructive suites. | Real validation with consent. |

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

For simple explanation-only questions with no project decision, org access, metadata inspection, deploy, data operation, secret exposure, destructive action, release-sensitive claim, implementation, or bugfix, agents may use compact information-only mode: `Request review`, `Evidence`, `Answer`, `Validation`.

## Safety

- Prefer Salesforce configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before custom code.
- Inspect local Knowledge before changing Salesforce metadata.
- Use project memory at `.salesforce-agent-knowledge/memory.md` for durable decisions, lessons, risks, and follow-ups. It is project-local curated planning knowledge, not a raw log, and must not contain secrets, customer data, raw records, or large logs.
- Knowledge scans Salesforce DX `packageDirectories` by default when available; use `sfao knowledge init --project-root . --scan-root` only for an intentional broad scan.
- Specialized Apex, LWC, Flow, SOQL, deploy, data operations, and Agentforce guidance is loaded only when relevant.
- External Salesforce skills are optional references only when already available and can never bypass SFAO guardrails.
- `safe-run --safety` cannot downgrade the automatic risk classification.
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
