# Agent Installation

## Codex

Install by placing the `salesforce-agent-optimizer` folder under `$CODEX_HOME/skills` or `~/.codex/skills`. Codex reads `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/` as the native skill package. Invoke with:

```text
Use $salesforce-agent-optimizer to review this Salesforce solution and produce a minimal patch.
```

For public GitHub installation, ask the agent to install from:

```text
https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Codex agents should use:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

## Claude Code

Claude Code does not consume `agents/openai.yaml` as a native Codex skill. Copy `agents/claude-code.md` into `CLAUDE.md` or `./.claude/CLAUDE.md`, or reference it from the team instruction set. Keep the `references/` and `scripts/` folders available in the repository so Claude Code can load them on demand.

For slash commands, copy `agents/sf-init-project-skill.md` to `.claude/commands/sf-init-project-skill.md`.

## GitHub Copilot

GitHub Copilot consumes repository custom instructions, not the Codex skill format directly. Copy `agents/github-copilot-instructions.md` into `.github/copilot-instructions.md`, or merge it with existing repository instructions. For scoped guidance, use `.github/instructions/salesforce-agent-optimizer.instructions.md`. Keep the skill folder in the repository when teams need the Salesforce references and CLI wrappers.

## Shared Repository Layout

Recommended portable layout:

```text
agent-skills/
  salesforce-agent-optimizer/
    SKILL.md
    agents/
    references/
    scripts/
```

For existing Salesforce repositories, place this folder under `.agent-skills/salesforce-agent-optimizer/` and point each agent's instruction file to it.

## `/sf-init-project-skill` Command

Where the agent supports custom slash commands, map `/sf-init-project-skill` to `agents/sf-init-project-skill.md`. Otherwise, treat the user text `/sf-init-project-skill` as an instruction to run `scripts/sf_knowledge_init.py --project-root <project-root> --refresh`.
