# Salesforce Agent Optimizer For Claude Code

Use the local `salesforce-agent-optimizer` skill when working on Salesforce architecture, solution design, Apex, LWC, Flow, metadata, DevOps, or org inspection.

Follow these rules:

- Restate the request, ask clarifying questions only when needed, plan changes, and ask for approval before modifying files or org metadata.
- Treat `/sf-init-project-skill` as a command to inspect Salesforce metadata and build or refresh `.salesforce-agent-knowledge/` with `scripts/sf_knowledge_init.py`.
- Before every modification, consult `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, relevant metadata pages under `metadata/`, and `history/project-history.md`; if missing or stale, run `/sf-init-project-skill` or ask whether to refresh.
- Before planning, identify relevant Salesforce products/packages using `references/products-packages/index.md`, read the matching product/package files, and use `references/metadata-dependencies.md` to plan access, field, layout, Lightning page, record type, picklist, automation, code, integration, sharing, analytics, package, and mobile dependencies.
- For Salesforce org access, use `scripts/sf_agent_cli.py`; ask for the org alias, authenticate with `auth-web`, `auth-device`, or `auth-jwt`, use `safe-run` for official commands without a first-class wrapper, and never perform write/execute commands on production.
- Prefer Salesforce configuration and standard product capabilities before custom code.
- Make minimal patches and avoid unrelated refactors.
- Inspect only the org metadata needed for the task.
- Use `scripts/sf_min.py` only as read-only compact fallback for official `sf` commands not yet exposed by the facade.
- Load `references/sf-agent-cli-commands.md`, `references/knowledge-init.md`, `references/delivery-methodology.md`, `references/architecture-solution.md`, `references/backend-apex.md`, `references/frontend-lwc.md`, or `references/sf-cli-token-patterns.md` only when relevant.
- After approved implementation, summarize requirements/changes and pass them to a validation subagent when available; if validation fails or approval is denied, replan with a maximum of three unsuccessful cycles.
- At the end of planning, ask whether the user wants an optional PDF with all configuration/customization tasks, explanations, dependencies, and time estimates.
- After successful deploys, ensure `.salesforce-agent-knowledge/history/project-history.md` records the requirement and all modified metadata.
- For approved remote branch pushes, use `scripts/git_knowledge_push.py` so Knowledge history is committed and included on the remote branch.
- When validation passes, ask whether to push and which branch to use.
