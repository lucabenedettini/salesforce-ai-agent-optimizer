# Salesforce Agent Optimizer

Use this repository as a lightweight Salesforce Agent Skill for Codex, Claude Code, GitHub Copilot, and compatible coding agents.

Canonical instructions live in `SKILL.md`. Load only the reference files needed for the current Salesforce task.

Core rules:

- Prefer Salesforce standard features, configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before custom Apex, LWC, triggers, or integrations.
- Keep patches minimal, reversible, and scoped to the approved request.
- Before planning, identify relevant products/packages, metadata dependencies, least-privilege access impact, and current project Knowledge when available.
- Never invent Salesforce behavior. Ask the user or present scenarios when evidence is missing.
- Never delete Salesforce data or metadata automatically. Follow `references/deletion-guardrails.md` and require explicit deletion approval.
- Use `scripts/sf_agent_cli.py` for org access: explicit org alias, compact redacted JSON, production read-only protection, and targeted output.
- Generate `package.xml` for added or modified metadata before validation handoff.
- Validate with tests or an independent validation pass before asking whether to push.

Useful entry points:

- Delivery loop: `references/delivery-methodology.md`
- Metadata dependencies: `references/metadata-dependencies.md`
- Least privilege: `references/least-privilege-planning.md`
- CLI facade: `references/sf-agent-cli-commands.md`
- Testing and manifests: `references/testing-and-manifest-guardrails.md`
- Current Salesforce version context: `references/salesforce-current-version.md`
