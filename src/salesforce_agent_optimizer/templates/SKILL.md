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
  version: 1.2.2
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

## Mandatory Phase Gates

For every Salesforce project request, run the functional phases below. Do not skip them for metadata-information questions, bugfixes, new metadata implementations, architecture work, reviews, or release tasks. Keep each phase compact, but make the phase outcome visible to the user.

Non-negotiable preflight:

- Do not inspect raw Salesforce metadata, parse project files, edit files, or run org commands as the first action. First show a compact phase-gate response with request review, planned references/Knowledge to consult, implementation status, and approval need.
- Before planning or answering, read `references/routing.md`, then the smallest relevant references, `.salesforce-agent-knowledge/markdown-index.md` or `.salesforce-agent-knowledge/index.json` when present, and project history when present.
- If Knowledge is missing or stale, state that and propose `sfao knowledge init --project-root .` or `sfao knowledge refresh --project-root .`.
- Before planning new functionality, new metadata, complex bugfixes, or heavy rework, ask whether the solution must cover Salesforce web/desktop, Salesforce mobile, Field Service mobile, online use, and offline use when the request does not say so.
- Every response must make the current phase visible with short labels: `Request review`, `Planning evidence`, `Approval`, `Implementation`, `Validation`, and `Completion`. For information-only requests, write `Implementation: not required`.
- After implementation, explicitly ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedures.
- If these gates were skipped, stop, acknowledge the miss, and restart from request review and planning.

1. Request review: restate the request, target org/environment, products/packages, scope, and acceptance criteria. Ask only high-value questions that cannot be discovered safely.
2. Planning: read the routed references, project Knowledge, metadata history, product/package context, dependencies, least-privilege guidance, and release/API context needed for the task. Always evaluate whether the project or requirement is multi-country or multi-currency and account for locale, currency, Advanced Currency Management, price books, tax, translations, compliance, and country-specific automation when relevant. When Field Service Mobile, mobile flows, briefcases, sync, or offline behavior can matter, read `references/field-service-mobile-flow.md`. Produce a configuration-first plan, including evidence sources and web/mobile plus online/offline coverage. For information-only requests, plan the answer path and state that no implementation is expected.
3. Approval gate: ask for approval before any file, metadata, org, or deployable change. Ask separately for destructive operations. If no implementation is needed, say so and continue to validation.
4. Implementation: implement only the approved minimal changes. If the request is information-only, mark this phase as `not required`.
5. Manifest/artifact gate: when metadata is added or modified, generate `package.xml` before validation handoff. Ask about optional release notes, technical specs, impact assessment, user testing, and manual procedures after implementation.
6. Validation: validate the result before final answer. For information-only requests, re-check the cited metadata/Knowledge/source evidence. For implementation requests, run tests/static checks or an independent validation pass.
   Use `sfao validate` when available to run lightweight checks for Apex, Flow, LWC, permissions, and `package.xml` in Salesforce DX projects.
7. Failure loop: if approval, tests, or validation fail, return to planning with a smaller revised plan. Stop after three unsuccessful cycles and restart from requirements.
8. Completion: summarize final requirements, evidence, changes or no-change result, validation, risks, and ask whether to push and which branch when repository changes exist.

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
