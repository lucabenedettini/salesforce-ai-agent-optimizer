# Salesforce Agent Optimizer For Claude Code

Use the local `salesforce-agent-optimizer` skill when working on Salesforce architecture, solution design, Apex, LWC, Flow, metadata, DevOps, or org inspection.

Follow these rules:

- Restate the request, ask clarifying questions only when needed, plan changes, and ask for approval before modifying files or org metadata.
- Treat `/sf-init-project-skill` as a command to inspect Salesforce metadata and build or refresh `.salesforce-agent-knowledge/` with `scripts/sf_knowledge_init.py`.
- Treat `/sf-version-update-skill` as a command to search official Salesforce sources for the latest production release/API/SOAP/package guidance and update `references/salesforce-current-version.md` plus related resources.
- Before every modification, consult `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, relevant metadata pages under `metadata/`, and `history/project-history.md`; if missing or stale, run `/sf-init-project-skill` or ask whether to refresh.
- Before planning, identify relevant Salesforce products/packages using `references/products-packages/index.md`, read the matching product/package files, and use `references/metadata-dependencies.md` to plan access, field, layout, Lightning page, record type, picklist, automation, code, integration, sharing, analytics, package, and mobile dependencies.
- Before release-sensitive API, SOAP, Metadata API, LWC API, Apex/Flow version, or package planning, read `references/salesforce-current-version.md`; refresh it if stale.
- For Salesforce org access, use `scripts/sf_agent_cli.py`; ask for the org alias, authenticate with `auth-web`, `auth-device`, or `auth-jwt`, use `safe-run` for official commands without a first-class wrapper, and never perform write/execute commands on production.
- Prefer Salesforce configuration and standard product capabilities before custom code.
- Make minimal patches and avoid unrelated refactors.
- Never invent missing Salesforce facts; if evidence is unclear, ask the user or present scenarios with tradeoffs.
- Never delete data or metadata automatically. Read `references/deletion-guardrails.md` and get separate explicit approval for the exact destructive scope before any delete, uninstall, purge, hard delete, source delete, or destructiveChanges deploy.
- Inspect only the org metadata needed for the task.
- Use `scripts/sf_min.py` only as read-only compact fallback for official `sf` commands not yet exposed by the facade.
- Load `references/sf-agent-cli-commands.md`, `references/knowledge-init.md`, `references/delivery-methodology.md`, `references/architecture-solution.md`, `references/backend-apex.md`, `references/frontend-lwc.md`, or `references/sf-cli-token-patterns.md` only when relevant.
- After approved implementation, summarize requirements/changes and pass them to a validation subagent when available; if validation fails or approval is denied, replan with a maximum of three unsuccessful cycles.
- Enforce testing guardrails: changed Apex must be at least 80% covered, preferably 90%-100%, and Flow or other testable metadata must be tested where Salesforce/project capabilities support it.
- At the end of implementation, generate `package.xml` for all added or modified metadata using `scripts/generate_package_manifest.py` when possible.
- At the end of development, ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedure files; use `references/completion-artifacts.md` if the user approves.
- At the end of planning, ask whether the user wants an optional PDF with all configuration/customization tasks, explanations, dependencies, and time estimates.
- After successful deploys, ensure `.salesforce-agent-knowledge/history/project-history.md` records the requirement and all modified metadata.
- For approved remote branch pushes, use `scripts/git_knowledge_push.py` so Knowledge history is committed and included on the remote branch.
- When validation passes, ask whether to push and which branch to use.
