# Salesforce Agent Optimizer

Use the repository Salesforce Agent Optimizer guidance for Salesforce work. Start with `AGENTS.md` and `SKILL.md`, then read only the reference files needed for the request.

Rules:

- Prefer configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before custom Apex, LWC, triggers, or integrations.
- Keep patches minimal and scoped to the approved request.
- Before planning, identify products/packages, metadata dependencies, least-privilege access impact, and current project Knowledge when available.
- Use `scripts/sf_agent_cli.py` for org access with explicit org aliases and compact redacted output.
- Production orgs are read-only through the facade.
- Never invent Salesforce behavior. Ask the user or present scenarios when evidence is unclear.
- Never delete Salesforce data or metadata automatically; follow `references/deletion-guardrails.md`.
- Generate `package.xml` for added or modified metadata before validation handoff.
