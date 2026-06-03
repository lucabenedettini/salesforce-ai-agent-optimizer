---
name: salesforce-agent-optimizer
description: Salesforce Agent Skill for Codex, Claude Code, and GitHub Copilot. Use for Salesforce architecture, metadata, Apex, LWC, Flow, DevOps, package.xml, release/API context, org inspection, least-privilege access planning, destructive-operation guardrails, configuration-first solutioning, minimal patches, and token-efficient validation.
license: MIT
compatibility:
  agents:
    - Codex
    - Claude Code
    - GitHub Copilot
  platforms:
    - Windows
    - macOS
    - Linux
  prerequisites:
    - Python 3.10+
    - Git
    - Salesforce CLI
metadata:
  version: 1.0.1
---

# Salesforce Agent Optimizer

Use this skill for Salesforce solution design, implementation, review, validation, metadata/package.xml work, org inspection, release/API version context, and safe agent delivery.

## First Reads

Start with `references/routing.md`. Load only the rows needed for the user's request, then read `references/delivery-methodology.md` for implementation work.

For every Salesforce task:

- Prefer Salesforce standard capabilities, setup configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before Apex, LWC, triggers, or custom integrations.
- Keep patches minimal, reversible, and scoped to the approved request.
- Consult `.salesforce-agent-knowledge/` before modifying a project; run `/sf-init-project-skill` when Knowledge is missing, stale, or requested.
- Apply least privilege in planning and inspect current org permissions when access, sharing, UI exposure, packages, integrations, automation, or users are affected.
- Never invent Salesforce behavior. Ask the user or present scenarios when product behavior, package version, org state, record scope, or permission scope is unclear.
- Never delete Salesforce data or metadata automatically. Read `references/deletion-guardrails.md` and require separate explicit approval for the exact destructive scope.
- Use official Salesforce documentation when local guidance is missing, uncertain, or release-sensitive.
- Optimize tokens at every step: load only the smallest relevant reference, summarize long logs, prefer diffs and paths over pasted files, and compact task context after each meaningful iteration.

## Delivery Loop

Use this compact loop unless the user asks for analysis only:

1. Restate the request, target org/environment, products/packages, and acceptance criteria.
2. Read `references/routing.md`, product/package references, project Knowledge, history, dependency guidance, least-privilege guidance, and version guidance as needed.
3. Plan configuration-first changes, custom work only when justified, metadata dependencies, tests, package.xml scope, risks, rollback, estimates, and destructive-approval needs.
4. Ask whether the user wants an optional PDF of planned tasks and estimates.
5. Ask for approval before file or org metadata changes; ask separately for destructive approval.
6. Implement only the approved minimal changes.
7. Generate `package.xml` for added or modified metadata before validation handoff.
8. Ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedure files.
9. Validate with tests or an independent validation subagent. If validation or approval fails, replan; stop after three unsuccessful cycles and restart from requirements.
10. After successful validation, record deploy/push history in Knowledge when applicable, then ask whether to push and which branch.

After each meaningful step, compact the current task context with: goal, state, changed files, commands executed, validation status, risks, and next minimal action. Remove repeated explanations, raw logs when summaries are enough, duplicate file contents, stale assumptions, and irrelevant metadata. Preserve safety warnings, validation errors, permission impacts, destructive-operation scope, and package.xml/deployment scope.

## Salesforce CLI

Use `scripts/sf_agent_cli.py` for org access. Always ask for an explicit org alias; never rely on a default org. Production orgs are read-only for write, execute, and destructive operations through the facade.

Common compact commands:

```bash
python scripts/sf_agent_cli.py org-inspect --target-org <alias> --select org_display.username,organization.records.0.IsSandbox
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
python scripts/sf_agent_cli.py deploy-preview --target-org <alias> --source-dir force-app --select result
```

## Slash Commands

- `/sf-init-project-skill`: wrapper for `sfao knowledge init --project-root .`; read `references/knowledge-init.md`.
- `/sf-version-update-skill`: wrapper for `sfao version-context scaffold` and `sfao version-context update`; read `references/version-update.md`.

## Adapter Maintenance

Agent-specific instruction files are generated from canonical sources. After changing `SKILL.md`, `references/routing.md`, or `references/agent-instruction-spine.md`, run:

```bash
python scripts/sync_agent_instructions.py
python scripts/validate_skill.py
```
