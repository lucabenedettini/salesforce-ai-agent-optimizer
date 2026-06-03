# Installation

## Codex

Ask Codex:

```text
Install the Salesforce AI Agent Optimizer skill from https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

The installer command is:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Restart Codex after installation.

## Claude Code

Clone or download the repository, then:

- Merge `agents/claude-code.md` into `CLAUDE.md`.
- Copy `agents/sf-init-project-skill.md` to `.claude/commands/sf-init-project-skill.md`.
- Copy `agents/sf-version-update-skill.md` to `.claude/commands/sf-version-update-skill.md`.

## GitHub Copilot

Clone or download the repository, then:

- Merge `agents/github-copilot-instructions.md` into `.github/copilot-instructions.md`.
- Or place it at `.github/instructions/salesforce-agent-optimizer.instructions.md` for scoped instructions.

## Prerequisites

- Python 3.10+.
- Git.
- Salesforce CLI for org operations.
- Explicit authenticated org aliases for Salesforce access.
- Sandbox org for write/execute operations; production orgs are read-only.
