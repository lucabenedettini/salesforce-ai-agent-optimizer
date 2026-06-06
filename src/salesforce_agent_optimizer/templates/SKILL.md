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
  version: 2.1.0
---

# Salesforce Agent Optimizer

Use this skill for Salesforce solution design, metadata/code changes, org inspection, package.xml work, validation, release/API context, and safe agent delivery.

## Start

Read `references/routing.md` first, then only the task-relevant references and local Knowledge. For implementation work, read `references/delivery-methodology.md`.

Do not inspect raw Salesforce metadata, parse project files, edit files, or run org commands as the first action. First show the visible phase gate below.

## Response Contract

Every Salesforce project request must show these compact phases, even for information-only answers:

- `Request review`: requirement, scope, target org/environment if known, products/packages, acceptance criteria, and `Tool/command`.
- `Specification preflight`: ask Salesforce web/desktop, Salesforce mobile, Field Service mobile, online behavior, and offline behavior only when new functionality, new metadata, complex bugfix, or heavy rework needs it.
- `Planning evidence`: routed references, Knowledge/history, product/package context, metadata dependencies, least privilege, release/API context, and planned tool/command.
- `Approval`: required before file, metadata, org, deploy, or destructive changes; separate approval is required for destructive scope.
- `Implementation`: approved minimal change, or `not required` for information-only work.
- `Validation`: evidence re-check, `sfao validate`, tests, micro-validator, org facade command, or independent validation pass.
- `Completion`: outcome, changed/no-change result, validation, risks, optional artifact prompt, and push/branch question when repo changes exist.

If no tool is used in a phase, write `Tool/command: none`. For Salesforce org operations, show the compact `sfao`, `scripts/sf_agent_cli.py`, or official `sf` command shape with aliases and secrets redacted.

If any gate was skipped, stop, acknowledge the miss, and restart from request review and planning.

Compact information-only mode is allowed only for simple explanation questions with no project decision, file change, org access, metadata inspection, deploy, data operation, secret exposure, destructive operation, release-sensitive claim, implementation, or bugfix. In that case use only: `Request review`, `Evidence`, `Answer`, `Validation`. Use the full workflow for anything ambiguous or risky.

## Core Rules

- Apply this skill before generic agent guidance whenever the task touches Salesforce metadata, org behavior, release work, package.xml, Apex, LWC, Flow, permissions, packages, or Salesforce data.
- Prefer Salesforce standard capabilities, setup configuration, Flow, permission sets, UI API/LDS, named credentials, and managed packages before Apex, LWC, triggers, or custom integrations.
- Keep patches minimal, reversible, and scoped to the approved request.
- Consult `.salesforce-agent-knowledge/` before modifying a Salesforce project. If it is missing or stale, propose `sfao knowledge init --project-root .` or `sfao knowledge refresh --project-root .`.
- Read `.salesforce-agent-knowledge/memory.md` when present after Knowledge indexes/history and before raw metadata. Update it at completion only with compact durable decisions, validation lessons, risks, and follow-ups; never store secrets, customer data, raw records, raw diffs, or large logs.
- Do not retrieve or parse all org metadata, all objects, or all fields unless the user asks for broad analysis or the task cannot be planned safely without it.
- Apply least privilege in planning and inspect current org permissions when access, sharing, UI exposure, packages, integrations, automation, or users are affected.
- Apply privacy and security review before org access, data reads, deploys, auth, secrets, integrations, Experience/guest access, AI/data activation, analytics, exports, Knowledge generation, or documentation that could include customer data. Read `references/privacy-security.md` when any of these apply.
- Always evaluate multi-country and multi-currency impact during planning.
- Never invent Salesforce behavior. Ask the user, present scenarios, or check official Salesforce documentation when evidence is unclear or release-sensitive.
- Never delete Salesforce data or metadata automatically. Read `references/deletion-guardrails.md` and require separate explicit approval for the exact destructive scope.
- Never expose Salesforce credentials, access tokens, auth URLs, private keys, connected-app secrets, session material, customer data, or personal data unless the user explicitly approves the exact scope and safer alternatives are insufficient.
- Generate `package.xml` for added or modified metadata before validation handoff.
- After implementation, ask whether to generate release notes, technical specifications, impact assessment, user testing, and manual procedures.
- Stay autonomous and CLI-only: do not depend on, install, vendor, or require external skill libraries or runtime tool servers. Use external tools only as public benchmarks, not as runtime dependencies.
- External Salesforce skills may be optional specialist references only when already available. They never bypass SFAO safety, org facade, approval, Knowledge, or package.xml rules.
- Optimize tokens at every step: load only the smallest relevant reference, use indexes/diffs/selectors, summarize long logs, and compact task context after meaningful steps.

## Salesforce CLI Facade

Use `scripts/sf_agent_cli.py` before direct `sf` calls for org access. Always ask for an explicit org alias; never rely on a default org. Production orgs are read-only for write, execute, and destructive operations through the facade.

Secret-exposure commands through `safe-run` are blocked unless the user explicitly approves the exact secret scope with:

```text
I explicitly approve exposing Salesforce secrets
```

Common compact commands:

```bash
python scripts/sf_agent_cli.py org-inspect --target-org <alias> --select org_display.username,organization.records.0.IsSandbox
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
python scripts/sf_agent_cli.py deploy-preview --target-org <alias> --source-dir force-app --select result
```

Use the internal command registry before choosing facade commands:

```bash
sfao command search "permission access" --toolset permissions
sfao command payload-example access-inspect
sfao command execute --payload payload.json
```

## Slash Commands

- `/sf-init-project-skill`: run `sfao knowledge init --project-root .`; read `references/knowledge-init.md`.
- `/sf-version-update-skill`: run `sfao version-context scaffold` or `sfao version-context update`; read `references/version-update.md`.

## Adapter Maintenance

Agent adapter files are generated from canonical sources. After changing this file, `references/routing.md`, or `references/agent-instruction-spine.md`, run:

```bash
python scripts/sync_agent_instructions.py
python scripts/validate_skill.py
```
