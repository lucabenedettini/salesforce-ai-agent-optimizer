---
applyTo: "**/{force-app/**,src/**,*.cls,*.trigger,*.apex,*.js,*.html,*.css,*.xml,*.flow-meta.xml,*.object-meta.xml,*.field-meta.xml,sfdx-project.json,package.xml}"
---

# Salesforce Agent Optimizer

Apply these instructions to Salesforce metadata, Apex, LWC, Flow, and project configuration.

- Use `AGENTS.md` and `SKILL.md` as the canonical workflow.
- Read focused references from `references/` only when relevant.
- Prefer Salesforce configuration and standard product capabilities before custom code.
- Plan access with least privilege and current-org evidence when permissions are in scope.
- Account for metadata dependencies across permissions, fields, layouts, Lightning pages, record types, picklists, Flow, Apex, integrations, sharing, reports, dashboards, packages, and mobile exposure.
- Keep changes minimal and generate `package.xml` for added or modified metadata.
- Never perform destructive data or metadata actions without explicit separate approval.
