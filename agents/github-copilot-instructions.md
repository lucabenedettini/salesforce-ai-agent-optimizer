# Salesforce Agent Optimizer

When assisting in this repository on Salesforce work, follow the local `.agent-skills/salesforce-agent-optimizer` or `salesforce-agent-optimizer` guidance.

- Restate the user's Salesforce request, ask focused clarification questions only when needed, plan changes, and ask for approval before modifying files or org metadata.
- Treat `/sf-init-project-skill` as a request to inspect Salesforce metadata and build or refresh `.salesforce-agent-knowledge/`.
- Before every modification, consult `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, relevant metadata pages under `metadata/`, and `history/project-history.md`; if missing or stale, refresh the Knowledge or ask whether to refresh.
- Before planning, identify relevant Salesforce products/packages using `references/products-packages/index.md`, read the matching product/package files, and use `references/metadata-dependencies.md` to plan access, field, layout, Lightning page, record type, picklist, automation, code, integration, sharing, analytics, package, and mobile dependencies.
- For Salesforce org access, use `scripts/sf_agent_cli.py`; ask for the org alias, authenticate with `auth-web`, `auth-device`, or `auth-jwt`, use `safe-run` for official commands without a first-class wrapper, and never perform write/execute commands on production.
- Prefer configuration, standard Salesforce features, Flow, LDS/UI API, permission sets, named credentials, and managed package capabilities before custom Apex/LWC.
- Keep patches minimal and scoped to the requested behavior.
- For Apex, enforce bulk safety, sharing/security, governor-limit awareness, and meaningful tests.
- For LWC, prefer Lightning base components, LDS/UI API, accessible SLDS-based UI, and efficient data loading.
- Use Salesforce CLI with JSON and compact filtered output; avoid pasting broad org metadata or noisy command output.
- After approved implementation, summarize requirements/changes and pass them to a validation subagent when available; if validation or tests fail, replan with a maximum of three unsuccessful cycles.
- At the end of planning, ask whether the user wants an optional PDF with all configuration/customization tasks, explanations, dependencies, and time estimates.
- After successful deploys, ensure `.salesforce-agent-knowledge/history/project-history.md` records the requirement and all modified metadata.
- For approved remote branch pushes, use `scripts/git_knowledge_push.py` so Knowledge history is committed and included on the remote branch.
- When validation passes, ask whether to push and which branch to use.
- Make architecture tradeoffs explicit using trusted, easy, and adaptable outcomes.
