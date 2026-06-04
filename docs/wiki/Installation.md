# Installation

Use `sfao` as the primary installation path. It copies packaged templates into
the current project without symlinks and without silently overwriting user-owned
files.

## Recommended User Install

```bash
uv tool install salesforce-agent-optimizer
sfao install --project --platform all
sfao doctor
```

Alternative:

```bash
pipx install salesforce-agent-optimizer
sfao install --project --platform all
sfao doctor
```

Before PyPI publication, install from GitHub:

```bash
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
sfao install --project --platform all
sfao doctor
```

## Main Install Targets

All supported agents:

```bash
sfao install --project --platform all
```

Only Codex:

```bash
sfao install --project --platform codex
```

Only Claude Code:

```bash
sfao install --project --platform claude
```

Only GitHub Copilot:

```bash
sfao install --project --platform copilot
```

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
.github/copilot-instructions.md
.github/instructions/salesforce-agent-optimizer.instructions.md
```

Trigger evals:

```text
evals/salesforce-agent-optimizer-trigger-evals.json
```

When `AGENTS.md`, `AGENT.md`, `agent.md`, `agents.md`, or
`.github/copilot-instructions.md` already exists, `sfao` inserts or updates a
managed Salesforce Agent Optimizer section instead of overwriting the file.
User-owned content outside the managed section is preserved.

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

`sfao update` updates only generated files that still contain the managed-file
marker. User-edited files are skipped and reported.

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

`sfao uninstall` removes only generated files. It keeps user-owned files and
project folders.

## Manual Fallback

Codex can still install directly from the public repository:

```text
Install the Salesforce AI Agent Optimizer skill from https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Installer script fallback:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Claude Code can use `.claude/skills/salesforce-agent-optimizer/SKILL.md`.

GitHub Copilot can use `AGENTS.md`, `.github/copilot-instructions.md`, and
`.github/instructions/salesforce-agent-optimizer.instructions.md`.

## Prerequisites

- Python 3.10+.
- Git.
- Salesforce CLI for org operations.
- Explicit authenticated org aliases for Salesforce access.
- Sandbox org for write or execute operations; production orgs are read-only
  through the skill guardrails.
