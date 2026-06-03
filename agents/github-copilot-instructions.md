# Salesforce Agent Optimizer

When assisting in this repository on Salesforce work, follow the local `.agent-skills/salesforce-agent-optimizer` or `salesforce-agent-optimizer` guidance.

- Restate the user's Salesforce request, ask focused clarification questions only when needed, plan changes, and ask for approval before modifying files or org metadata.
- Treat `/sf-init-project-skill` as a request to inspect Salesforce metadata and build or refresh `.salesforce-agent-knowledge/`.
- Treat `/sf-version-update-skill` as a request to search official Salesforce sources for the latest production release/API/SOAP/package guidance and update `references/salesforce-current-version.md` plus related resources.
- Before every modification, consult `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, relevant metadata pages under `metadata/`, and `history/project-history.md`; if missing or stale, refresh the Knowledge or ask whether to refresh.
- Before planning, identify relevant Salesforce products/packages using `references/products-packages/index.md`, read the matching product/package files, and use `references/metadata-dependencies.md` to plan access, field, layout, Lightning page, record type, picklist, automation, code, integration, sharing, analytics, package, and mobile dependencies.
- Before release-sensitive API, SOAP, Metadata API, LWC API, Apex/Flow version, or package planning, read `references/salesforce-current-version.md`; refresh it if stale.
- For Salesforce org access, use `scripts/sf_agent_cli.py`; ask for the org alias, authenticate with `auth-web`, `auth-device`, or `auth-jwt`, use `safe-run` for official commands without a first-class wrapper, and never perform write/execute commands on production.
- Prefer configuration, standard Salesforce features, Flow, LDS/UI API, permission sets, named credentials, and managed package capabilities before custom Apex/LWC.
- Keep patches minimal and scoped to the requested behavior.
- Never invent missing Salesforce facts; if evidence is unclear, ask the user or present scenarios with tradeoffs.
- Never delete data or metadata automatically. Read `references/deletion-guardrails.md` and get separate explicit approval for the exact destructive scope before any delete, uninstall, purge, hard delete, source delete, or destructiveChanges deploy.
- For Apex, enforce bulk safety, sharing/security, governor-limit awareness, and meaningful tests.
- Changed Apex must be at least 80% covered, preferably 90%-100%, and Flow or other testable metadata must be tested where Salesforce/project capabilities support it.
- For LWC, prefer Lightning base components, LDS/UI API, accessible SLDS-based UI, and efficient data loading.
- Use Salesforce CLI with JSON and compact filtered output; avoid pasting broad org metadata or noisy command output.
- After approved implementation, summarize requirements/changes and pass them to a validation subagent when available; if validation or tests fail, replan with a maximum of three unsuccessful cycles.
- At the end of implementation, generate `package.xml` for all added or modified metadata using `scripts/generate_package_manifest.py` when possible.
- At the end of development, ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedure files; use `references/completion-artifacts.md` if the user approves.
- At the end of planning, ask whether the user wants an optional PDF with all configuration/customization tasks, explanations, dependencies, and time estimates.
- After successful deploys, ensure `.salesforce-agent-knowledge/history/project-history.md` records the requirement and all modified metadata.
- For approved remote branch pushes, use `scripts/git_knowledge_push.py` so Knowledge history is committed and included on the remote branch.
- When validation passes, ask whether to push and which branch to use.
- Make architecture tradeoffs explicit using trusted, easy, and adaptable outcomes.
