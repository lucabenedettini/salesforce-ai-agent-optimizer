# Agent Installation

## Codex

Install as a repo-local skill under:

```text
.agents/skills/salesforce-agent-optimizer
```

Install as a user skill under:

```text
$HOME/.agents/skills/salesforce-agent-optimizer
```

Codex reads `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/` as the native skill package. Invoke with:

```text
Use $salesforce-agent-optimizer to review this Salesforce solution and produce a minimal patch.
```

For public GitHub installation, ask the agent to install from:

```text
https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

When installing from this public repository, agents can use:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

## Claude Code

Claude Code can discover the skill from:

```text
.claude/skills/salesforce-agent-optimizer/SKILL.md
```

Keep the root `SKILL.md`, `references/`, and `scripts/` folders available in the repository so Claude Code can load them on demand. You can also copy `agents/claude-code.md` into `CLAUDE.md` or `./.claude/CLAUDE.md`.

For slash commands, copy:

- `agents/sf-init-project-skill.md` to `.claude/commands/sf-init-project-skill.md`
- `agents/sf-version-update-skill.md` to `.claude/commands/sf-version-update-skill.md`

## GitHub Copilot

GitHub Copilot consumes repository custom instructions, not the Codex skill format directly. Use:

- `AGENTS.md` as the universal instruction spine.
- `.github/copilot-instructions.md` for repository-wide guidance.
- `.github/instructions/salesforce-agent-optimizer.instructions.md` for scoped Salesforce metadata, Apex, LWC, Flow, and `sfdx-project.json` guidance.

Keep the skill folder in the repository when teams need the Salesforce references and CLI wrappers.

## Adapter Synchronization

Agent-specific instruction files are generated from `references/agent-instruction-spine.md`. After changing core routing or installation guidance, run:

```bash
python scripts/sync_agent_instructions.py
python scripts/sync_agent_instructions.py --check
```

Generated files include `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/salesforce-agent-optimizer.instructions.md`, `.agents/skills/salesforce-agent-optimizer/SKILL.md`, `.claude/skills/salesforce-agent-optimizer/SKILL.md`, `agents/claude-code.md`, `agents/github-copilot-instructions.md`, and `agents/openai.yaml`.

## Shared Repository Layout

Recommended portable layout:

```text
.agents/skills/
  salesforce-agent-optimizer/
    SKILL.md
    agents/
    references/
    scripts/
```

For existing Salesforce repositories, place the skill under `.agents/skills/salesforce-agent-optimizer/` and point each agent's instruction file to it.

## `/sf-init-project-skill` Command

Where the agent supports custom slash commands, map `/sf-init-project-skill` to `agents/sf-init-project-skill.md`. Otherwise, treat the user text `/sf-init-project-skill` as an instruction to run `scripts/sf_knowledge_init.py --project-root <project-root> --refresh`.

## `/sf-version-update-skill` Command

Where the agent supports custom slash commands, map `/sf-version-update-skill` to `agents/sf-version-update-skill.md`. Otherwise, treat the user text `/sf-version-update-skill` as an instruction to read `references/version-update.md`, search official Salesforce sources for the latest production release/API/SOAP/package guidance, and update the version context resources.
