# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer is an MIT-licensed Salesforce Agent Skill packaged as the
`sfao` command for Codex, Claude Code, and GitHub Copilot.

Current version: `1.2.1`

It installs agent instructions that enforce Salesforce-first solutioning,
configuration before custom code, minimal reversible changes, token-efficient
Knowledge, least-privilege planning, explicit org aliases, package.xml awareness,
and destructive-operation guardrails.

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

Use `uv tool install` or `pipx install` for CLI isolation. Plain `pip install`
works, but isolated tool installers usually avoid PATH and dependency friction.
`sfao install` without flags installs into the current project; use `--user`
only when you intentionally want a HOME-scoped install.

## Install

Recommended:

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao doctor
```

Alternative:

```bash
python -m pipx install salesforce-agent-optimizer
sfao install
sfao doctor
```

Install directly from GitHub before or outside PyPI publication:

```bash
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
sfao install
sfao doctor
```

Plain `pip` is acceptable when you intentionally want the command in the active
Python environment:

```bash
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
sfao install
sfao doctor
```

## Main `sfao` Commands

| Command | What it does |
| --- | --- |
| `sfao version` | Prints the installed Salesforce Agent Optimizer version. |
| `sfao install` | Installs all project-scoped adapters and local resources in the current project. |
| `sfao install --project --platform all` | Installs Codex, Claude Code, and GitHub Copilot adapters in the current project. |
| `sfao install --user --platform all` | Installs user-scoped Codex and Claude Code files under HOME. |
| `sfao install --project --platform codex` | Installs only the Codex project skill under `.agents/skills/`. |
| `sfao install --project --platform claude` | Installs only the Claude Code project skill under `.claude/skills/`. |
| `sfao install --project --platform copilot` | Installs GitHub Copilot project skill, repository instructions, path instructions, and `AGENTS.md`. |
| `sfao update --project --platform all` | Updates generated/managed files and adds newly introduced managed templates; user-edited fully generated files are skipped. |
| `sfao uninstall --project --platform all --yes` | Removes only generated adapter files; project folders and user-owned files are kept. |
| `sfao doctor` | Checks the local environment, installed adapters, Salesforce CLI availability, and common PATH issues. |
| `sfao doctor --verbose` | Prints full diagnostic details. |
| `sfao doctor --json` | Prints compact machine-readable diagnostics. |
| `sfao validate` | Validates installed files or the source tree, including frontmatter, YAML, TOML, JSON, Python, versions, newline shape, and lightweight Salesforce metadata checks. |
| `sfao validate --verbose` | Prints validation details useful for troubleshooting. |
| `sfao validate --json` | Prints compact machine-readable validation results. |
| `sfao knowledge init --project-root .` | Creates `.salesforce-agent-knowledge/` for a Salesforce project. |
| `sfao knowledge refresh --project-root .` | Refreshes local Knowledge after metadata changes and prints progress unless `--json` is used. |
| `sfao knowledge doctor --project-root .` | Checks whether local Knowledge exists and is usable. |
| `sfao knowledge refresh --project-root . --target-org <alias>` | Optionally enriches Knowledge from an org. The alias must be explicit. |
| `sfao version-context scaffold` | Creates local Salesforce release/API context files if missing. |
| `sfao version-context update` | Refreshes concise Salesforce release/API/package guidance from official Salesforce sources and prints progress unless `--json` is used. |
| `sfao version-context validate` | Checks version-context files for required content. |

## What Gets Installed

For Codex:

```text
.agents/skills/salesforce-agent-optimizer/SKILL.md
.agents/skills/salesforce-agent-optimizer/references/
.agents/skills/salesforce-agent-optimizer/scripts/
.agents/skills/salesforce-agent-optimizer/agents/openai.yaml
```

For Claude Code:

```text
.claude/skills/salesforce-agent-optimizer/SKILL.md
.claude/skills/salesforce-agent-optimizer/references/
.claude/skills/salesforce-agent-optimizer/scripts/
```

For GitHub Copilot:

```text
AGENTS.md
.github/skills/salesforce-agent-optimizer/SKILL.md
.github/skills/salesforce-agent-optimizer/references/
.github/skills/salesforce-agent-optimizer/scripts/
.github/copilot-instructions.md
.github/instructions/salesforce-agent-optimizer.instructions.md
```

For trigger evals:

```text
evals/salesforce-agent-optimizer-trigger-evals.json
```

Generated files contain this marker:

```md
<!-- Generated by salesforce-agent-optimizer. Managed by sfao. -->
```

`sfao` never overwrites or removes user-owned files silently. When `AGENTS.md`,
`AGENT.md`, `agent.md`, `agents.md`, or `.github/copilot-instructions.md`
already exists, `sfao` adds or updates a managed Salesforce Agent Optimizer
section and keeps the rest of the file intact.

## Agent Workflow

After installation, the agent instructions require the same phase-gated workflow
for metadata information requests, bugfixes, new implementations, architecture
work, reviews, release work, and org inspection:

1. Review the request and restate scope, products/packages, org/environment, and acceptance criteria.
2. Plan from relevant references, local Knowledge, metadata dependencies, least privilege, multi-country/multi-currency impact, and official Salesforce context when needed.
3. Ask for approval before file, metadata, org, deployable, or destructive changes.
4. Implement only approved minimal changes, or mark implementation as `not required` for information-only requests.
5. Generate `package.xml` when metadata is added or modified.
6. Validate before the final answer.
7. Return to planning after failed approval, tests, or validation; stop after three unsuccessful cycles.
8. Summarize evidence, changes or no-change result, validation, risks, and ask whether to push and to which branch when repository changes exist.

## Knowledge And Version Context

Create or refresh compact local Salesforce project Knowledge:

```bash
sfao knowledge init --project-root .
sfao knowledge refresh --project-root .
sfao knowledge doctor --project-root .
```

Non-JSON Knowledge commands print progress to the terminal while scanning,
summarizing, and writing metadata pages. Use `--json` for compact automation output.

Refresh Salesforce release/API/package context:

```bash
sfao version-context scaffold
sfao version-context update
sfao version-context validate
```

Non-JSON version-context commands print progress while writing files and checking
official Salesforce sources. Use `sfao version-context update --offline` to skip
network checks.

Org access is never implicit. When a command needs Salesforce org metadata or
data, the agent must ask for an explicit alias. Production orgs are read-only
through the skill guardrails.

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Alternative:

```bash
python -m pipx upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Plain `pip`:

```bash
python -m pip install --upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

Alternative:

```bash
sfao uninstall --project --platform all --yes
python -m pipx uninstall salesforce-agent-optimizer
```

## Privacy And Safety

- Do not commit Salesforce credentials, `.sf/`, `.sfdx/`, auth files, tokens, private keys, or local secrets.
- Least privilege is required during planning: inspect current access before granting permissions and grant only the minimum access needed.
- Destructive data or metadata operations require explicit approval for the exact scope.
- Destructive CLI operations require the exact approval phrase `I explicitly approve this deletion`.
- Knowledge stores compact summaries and hashes, not raw secrets.

## Troubleshooting

`sfao: command not found`

- Run `uv tool update-shell`, open a new terminal, or add the tool bin directory to PATH.
- On Windows, check the user Scripts directory printed by `pip`.

`uv: command not found`

- Install `uv`, or use `python -m pipx install salesforce-agent-optimizer`.

`pipx: command not found`

- Use `python -m pipx ...`.
- If the module is missing, install it with `python -m pip install --user pipx`, then run `python -m pipx ensurepath`.

`pip upgrade` is not a command

- Use `python -m pip install --upgrade salesforce-agent-optimizer`.

PyPI package not found

- Use the GitHub install command until the package is published on PyPI.

Salesforce CLI `sf` not found

- Install the official Salesforce CLI and verify `sf --version`.

Skill not visible in Codex, Claude Code, or GitHub Copilot

- Run the matching `sfao install --project --platform ...` command again.
- Restart the agent surface if it caches instructions.
- Run `sfao doctor` and `sfao validate`.
- For Copilot, verify `.github/skills/salesforce-agent-optimizer/SKILL.md` exists.

Stale generated files or version mismatch

- Run `sfao update --project --platform all`.
- Run `sfao validate --verbose`.

## More Documentation

End-user and maintainer details live in the wiki source under `docs/wiki/`:

- `docs/wiki/Home.md`
- `docs/wiki/Installation.md`
- `docs/wiki/Packaging-And-Publishing.md`
- `docs/wiki/Principles.md`
- `docs/wiki/Testing-And-Manifests.md`
- `docs/wiki/Versioning.md`

Build, release, publishing, and package-maintenance details are intentionally kept
out of this README so the user-facing install path stays short.

## License

MIT. Anyone can use, copy, modify, distribute, and fork this repository under
the terms of `LICENSE`.
