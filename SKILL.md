---
name: salesforce-agent-optimizer
description: Optimize AI-agent work on Salesforce orgs, products, architecture, solution design, configuration, Apex, Lightning Web Components, Flows, integrations, DevOps, and Salesforce CLI usage. Use when Codex, Claude Code, GitHub Copilot, or another coding agent must design, review, implement, debug, migrate, or inspect Salesforce solutions while following Salesforce Well-Architected guidance, preferring configuration over custom code, making minimal patches, enforcing backend/frontend best practices, using approval-gated planning, building or refreshing an indexed Salesforce metadata Knowledge with /sf-init-project-skill, consulting that Knowledge before every modification, delegating validation to a subagent when available, managing retries, asking about push branch at the end, and reducing token waste from org discovery or CLI output.
---

# Salesforce Agent Optimizer

## Operating Principles

Treat Salesforce as a metadata-driven platform first. Prefer standard features, setup configuration, Flow, permission sets, validation rules, Dynamic Forms, Lightning App Builder, standard APIs, and managed package capabilities before Apex, LWC, triggers, or bespoke integrations.

Optimize for Salesforce Well-Architected outcomes: trusted, easy, and adaptable. Make tradeoffs explicit when security, maintainability, performance, scalability, user experience, or delivery speed compete.

Keep patches minimal. Change the fewest metadata/code files that solve the stated problem. Avoid broad refactors unless needed to remove a defect or unblock a safe design.

Use org evidence before assumptions. Inspect only the metadata needed for the decision, summarize findings compactly, and avoid dumping raw CLI output into context.

Before any modification, consult the project Knowledge if it exists. If it is missing, stale, or explicitly requested by the user, run `/sf-init-project-skill` to build or refresh it.

## `/sf-init-project-skill` Metadata Knowledge

Read `references/knowledge-init.md` when the user invokes `/sf-init-project-skill`, asks to inspect Salesforce metadata, asks to refresh project Knowledge, or starts work in a Salesforce repo without an existing Knowledge index.

`/sf-init-project-skill` creates or refreshes an indexed Knowledge folder inside the Salesforce project:

```text
.salesforce-agent-knowledge/
```

Run:

```bash
python scripts/sf_knowledge_init.py --project-root <salesforce-project-root> --refresh
```

The user can update `.salesforce-agent-knowledge/config.json` to add, remove, or enrich metadata types and path patterns for the project. Treat the generated Knowledge as a compact context layer, not as a replacement for source metadata files.

Each indexed metadata artifact gets a same-format Markdown page under `.salesforce-agent-knowledge/metadata/`. The Knowledge also includes `markdown-index.md` for all Markdown files and `history/project-history.md` for compact change, deploy, and remote-branch push history. History entries must include the requirement that caused the change and all modified metadata.

## Mandatory Delivery Methodology

Read `references/delivery-methodology.md` for the full loop. Follow it for every Salesforce project task unless the user explicitly asks for analysis only.

1. Restate the user's Salesforce request and project context in concise terms.
2. Ask focused clarification questions only when requirements, target org, risk, or acceptance criteria are unclear.
3. Consult `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, relevant metadata pages, and project history before planning; if missing or stale, run `/sf-init-project-skill` or ask whether to refresh.
4. Inspect the minimum repository/org evidence needed to plan safely.
5. If official Salesforce behavior is unknown, missing, release-sensitive, or worth confirming, search online only in official Salesforce documentation and use the latest available version.
6. Plan the intended changes, including configuration-first options, custom work, tests, risks, and rollback.
7. Ask the user to approve the plan before modifying project files or org metadata.
8. After approval, implement only the approved minimal changes.
9. Summarize requirements, changes, affected artifacts, assumptions, and validation commands.
10. Pass that summary to a validation subagent when the platform supports subagents. If subagents are unavailable, create a standalone validation prompt and run the closest independent validation pass available.
11. If approval is denied, validation fails, or tests fail, return to planning with the new evidence. Allow at most three unsuccessful planning/validation cycles; after that, stop implementation and restart from a fresh requirements explanation.
12. When work is validated, ensure Knowledge history records the requirement and all modified metadata for deployed changes, then ask whether to push and which branch to use. If a remote push is approved, push through `scripts/git_knowledge_push.py` so the Knowledge history is committed and included on the remote branch.

## Token Discipline

Use `scripts/sf_agent_cli.py` for Salesforce CLI operations that connect to an org. It is an agent-native facade over the official `sf` CLI: it requires explicit org aliases, uses secure auth flows, emits compact redacted JSON, and blocks write/execute operations against production orgs.

Default to these patterns:

```bash
python scripts/sf_agent_cli.py auth-web --alias dev-sandbox --instance-url https://test.salesforce.com
python scripts/sf_agent_cli.py org-inspect --target-org dev-sandbox --select org_display.username,organization.records.0.IsSandbox
python scripts/sf_agent_cli.py data-query --target-org dev-sandbox --query "SELECT Id, Name FROM Account LIMIT 20" --select result.records
python scripts/sf_agent_cli.py deploy-preview --target-org dev-sandbox --source-dir force-app --select result
python scripts/sf_agent_cli.py deploy-start --target-org dev-sandbox --source-dir force-app --requirements "Add priority tracking to Account" --changed-metadata CustomField:Account.Priority__c --select result
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- data query --query "SELECT Id FROM Account LIMIT 1" --select result.records
```

Do not use a default org for metadata or data access. Ask the user for the org alias every time the target org is not already explicit in the current approved plan.

Do not paste full `sf` JSON, describe screens, or retrieve broad metadata unless needed. Prefer facade commands, `--metadata Type:Name`, `--source-dir` for the touched path, narrow SOQL field lists, `--select`, and bounded output.

Read `references/sf-agent-cli-commands.md` before using or extending the facade. Use `references/sf-official-command-catalog.md` only when you need the generated one-by-one catalog of installed official Salesforce CLI commands. Read `references/sf-cli-token-patterns.md` before creating new CLI wrappers or deciding whether to rewrite another Salesforce CLI command.

## Backend Guidelines

For Apex, read `references/backend-apex.md` when implementing or reviewing custom backend logic.

Always check:

- Bulk safety: no SOQL/DML/callouts in record loops; handlers accept collections.
- Limits: queries, DML, CPU, heap, queueable/future/batch constraints.
- Security: sharing model, CRUD/FLS, user-mode operations where appropriate, guest-user exposure, named credentials.
- Trigger design: one trigger per object, delegated logic, deterministic recursion control.
- Tests: meaningful assertions, positive/negative paths, bulk tests, permission-aware tests, no SeeAllData unless justified.

## Frontend Guidelines

For LWC, read `references/frontend-lwc.md` before editing user-facing components.

Prefer Lightning base components, Lightning Data Service, UI API wire adapters, GraphQL wire adapter, and standard navigation before Apex-backed bespoke UI logic. Use Apex only when data shape, transactionality, or server-side processing requires it.

Keep components small, accessible, secure under Lightning Web Security, and efficient in rerendering. Avoid custom CSS that fights SLDS unless the product need is concrete.

## Architecture And Solution Design

For architecture or discovery tasks, read `references/architecture-solution.md`.

Produce designs that include:

- Business capability and user outcome.
- Standard/configuration path first.
- Custom path only with justification.
- Data model, security model, automation model, integration pattern, lifecycle/deployment model.
- Risks, limits, operational ownership, observability, rollback, and future adaptability.

## Agent Installation Adapters

Use `references/agent-installation.md` when packaging this skill for Codex, Claude Code, or GitHub Copilot. The `agents/` folder contains compact instruction adapters:

- `agents/openai.yaml`: Codex/OpenAI UI metadata.
- `agents/claude-code.md`: Claude Code importable instruction block.
- `agents/github-copilot-instructions.md`: GitHub Copilot repository instruction block.
- `agents/sf-init-project-skill.md`: portable `/sf-init-project-skill` slash-command definition.

Keep adapters short. The canonical behavior lives in this `SKILL.md` and the `references/` files.

## Official Sources

Read `references/official-salesforce-sources.md` when you need to verify current Salesforce guidance, confirm uncertain platform behavior, or update this skill's recommendations. Prefer the latest available official Salesforce documentation.
