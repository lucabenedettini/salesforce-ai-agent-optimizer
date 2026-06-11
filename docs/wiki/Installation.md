# Installation

Use `sfao` as the primary installation path. It copies packaged templates into
the current project without symlinks and without silently overwriting user-owned
files.

## Recommended Project Install

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

Before PyPI publication, install from GitHub:

```bash
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
sfao install
sfao doctor
```

Plain `pip` is acceptable when the active Python environment is intentional:

```bash
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
sfao install
sfao doctor
```

## Main Install Targets

All supported agents:

```bash
sfao install
```

Equivalent explicit command:

```bash
sfao install --project --platform all
```

User-scoped Codex and Claude Code files:

```bash
sfao install --user --platform all
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

Project-root resources used by the instruction spine:

```text
references/
scripts/
```

Agents resolve `references/...` and `scripts/...` from the project root first. If those copies are unavailable, they fall back to the active adapter's local skill folders below.

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

PATH-safe `pipx` update:

```bash
python -m pipx upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Plain `pip` update:

```bash
python -m pip install --upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

`sfao update` refreshes generated or managed sections and installs newly introduced managed templates, such as eval files, when they are missing from an existing project install.

`sfao update` updates only generated files that still contain the managed-file
marker. User-edited files are skipped and reported.

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

PATH-safe `pipx` uninstall:

```bash
sfao uninstall --project --platform all --yes
python -m pipx uninstall salesforce-agent-optimizer
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

GitHub Copilot can use `AGENTS.md`, `.github/copilot-instructions.md`,
`.github/instructions/salesforce-agent-optimizer.instructions.md`, and the
project-scoped `.github/skills/salesforce-agent-optimizer/SKILL.md`.

## Prerequisites

- Python 3.10+.
- Git.
- Salesforce CLI for org operations.
- Explicit authenticated org aliases for Salesforce access.
- Sandbox org for write or execute operations; production orgs are read-only
  through the skill guardrails.

## Command Notes

- `pip upgrade` is not a valid command. Use `python -m pip install --upgrade salesforce-agent-optimizer`.
- If `pipx` is installed but not on PATH, use `python -m pipx ...`.
- If the `pipx` module is missing, run `python -m pip install --user pipx` and then `python -m pipx ensurepath`.
- `sfao knowledge init`, `sfao knowledge refresh`, and `sfao version-context update` print progress in non-JSON mode. Use `--json` for compact automation output.
