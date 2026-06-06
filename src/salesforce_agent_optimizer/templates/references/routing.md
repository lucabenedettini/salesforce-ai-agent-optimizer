# Routing

Read this file before planning. Load only the references needed for the current request.

| Request signal | Read these files |
| --- | --- |
| Any Salesforce implementation, review, debug, migration, or release task | `references/delivery-methodology.md`, `.salesforce-agent-knowledge/index.md` when present |
| Product or AppExchange package mentioned or implied | `references/products-packages/index.md`, then only matching files under `references/products-packages/products/` or `references/products-packages/packages/` |
| Metadata dependency planning, security model, layouts, pages, record types, picklists, sharing, analytics, mobile exposure | `references/metadata-dependencies.md`, `references/least-privilege-planning.md` |
| Least-privilege access, permission sets, permission set groups, users, sharing, integration users, package permissions | `references/least-privilege-planning.md`, `references/sf-agent-cli-commands.md` |
| Privacy, secrets, tokens, customer data, personal data, exports, auth URLs, connected apps, named credentials, Knowledge/documentation data exposure | `references/privacy-security.md`, `references/least-privilege-planning.md`, `references/sf-cli-token-patterns.md` |
| Org inspection, Salesforce CLI, auth, deploy, retrieve, SOQL, installed packages, compact output | `references/sf-agent-cli-commands.md`, `references/sf-cli-token-patterns.md` |
| Apex, triggers, async Apex, invocable Apex, backend security, bulkification, Apex tests | `references/backend-apex.md`, `references/testing-and-manifest-guardrails.md` |
| LWC, Aura, Lightning UI, UI API, LDS, frontend security, accessibility, performance | `references/frontend-lwc.md`, `references/testing-and-manifest-guardrails.md` |
| Flow, automation, validation rules, testable metadata | `references/testing-and-manifest-guardrails.md`, `references/metadata-dependencies.md`; add `references/field-service-mobile-flow.md` when Flow can run in Field Service Mobile or offline |
| Architecture, discovery, solution definition, integration patterns, governance | `references/architecture-solution.md`, `references/official-salesforce-sources.md` when behavior is uncertain |
| Salesforce CPQ | `references/products-packages/products/salesforce-cpq.md`, `references/metadata-dependencies.md`, `references/least-privilege-planning.md` |
| Salesforce Field Service | `references/products-packages/products/salesforce-field-service.md`, `references/field-service-mobile-flow.md`, `references/products-packages/products/mobile-development.md`, `references/metadata-dependencies.md` |
| Advanced Approvals | `references/products-packages/packages/advanced-approvals.md`, `references/products-packages/products/salesforce-cpq.md`, `references/metadata-dependencies.md` |
| Field Service Mobile, Field Service mobile flows, technician mobile work, briefcases, sync, online/offline behavior | `references/field-service-mobile-flow.md`, `references/products-packages/products/salesforce-field-service.md`, `references/products-packages/products/mobile-development.md`, `references/metadata-dependencies.md`, `references/least-privilege-planning.md` |
| Mobile development or Salesforce mobile app behavior | `references/products-packages/products/mobile-development.md`, `references/field-service-mobile-flow.md` when Field Service is involved, `references/frontend-lwc.md`, `references/metadata-dependencies.md` |
| Data delete, metadata delete, source delete, purge, hard delete, package uninstall, destructiveChanges | `references/deletion-guardrails.md`, `references/testing-and-manifest-guardrails.md` |
| package.xml, deploy manifest, deleted metadata scope, release artifact scope | `references/testing-and-manifest-guardrails.md`, `references/deletion-guardrails.md` when deletes are involved |
| Release/API/SOAP/Metadata API/LWC API/sourceApiVersion/package version context | `references/salesforce-current-version.md`; run `sfao version-context update` with `references/version-update.md` when stale |
| Project Knowledge build or refresh | `references/knowledge-init.md` |
| Release notes, technical specifications, impact assessment, user testing, manual procedures | `references/completion-artifacts.md` |
| Installability across Codex, Claude Code, GitHub Copilot | `references/agent-installation.md`, `references/agent-instruction-spine.md` |
| Official Salesforce confirmation needed | `references/official-salesforce-sources.md`, then official Salesforce docs only |

When no row clearly fits, read `references/delivery-methodology.md` and ask the user for the missing product, org, permission, or acceptance-criteria detail.
