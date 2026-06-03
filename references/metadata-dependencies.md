# Salesforce Metadata Dependency Planning

Use this reference before planning any Salesforce change. Treat metadata as a dependency graph: a safe plan names the primary artifact, related metadata, access model, UI exposure, automation impact, data impact, and deployment order.

## Required Planning Checks

- Identify all products and packages involved using `references/products-packages/index.md`.
- Read the matching product/package files before proposing a plan.
- Inspect the Knowledge metadata pages and source files for every artifact in the dependency path.
- Prefer configuration dependencies over custom code when they solve the same requirement.
- Include dependency risks and validation commands in the plan.

## Access Dependencies

- `User` records receive access through `PermissionSetAssignment`, permission set groups, profiles, roles, queues, public groups, territories, and license assignments.
- Permission set groups depend on member permission sets and muting permission sets.
- Permission sets and profiles can include object permissions, field permissions, Apex class access, Flow access, tab visibility, custom permissions, app visibility, connected app access, and setup entity access.
- Plan changes to users, permission sets, groups, custom permissions, licenses, profiles, and sharing together.

## Data Model Dependencies

- Custom objects depend on fields, relationships, validation rules, indexes, search layouts, compact layouts, record types, business processes, list views, and tabs.
- Fields can affect layouts, Lightning pages, reports, formulas, flows, Apex, validation rules, duplicate rules, matching rules, integrations, and package mappings.
- Picklist values can be global value sets, local value sets, restricted values, dependent values, or record-type-specific values.
- Record types depend on picklist value availability, page layout assignment, business process, Lightning record page activation, assignment rules, and automation conditions.

## UI Dependencies

- Page layouts depend on fields, buttons, actions, related lists, record types, and profile or app assignments.
- Lightning pages (`FlexiPage`) depend on object context, record type activation, app activation, component visibility rules, custom components, dynamic forms, actions, and mobile form factors.
- Quick actions, global actions, tabs, Lightning apps, utility bars, navigation items, compact layouts, and mobile navigation can all expose or hide the same business capability.
- Always check desktop and mobile exposure when a requirement changes user interaction.

## Automation Dependencies

- Flows can depend on objects, fields, record types, custom metadata, custom labels, email templates, queues, Apex actions, subflows, platform events, approval states, and entry criteria.
- Approval processes and Advanced Approvals depend on submitter access, approver users/groups, quote/order objects, email templates, criteria fields, and record locking behavior.
- Assignment rules, escalation rules, auto-response rules, duplicate rules, matching rules, and validation rules can change behavior even when no code changes.

## Code Dependencies

- Apex triggers, classes, batch jobs, queueables, schedulables, invocable methods, and tests can depend on fields, record types, sharing, CRUD/FLS, custom metadata, named credentials, platform events, and package objects.
- LWC and Aura components can depend on Apex classes, Lightning Data Service, UI API, GraphQL wire adapter, message channels, labels, static resources, custom permissions, and page activation.
- Plan tests for both unit behavior and permission-aware execution.

## Integration Dependencies

- Named credentials depend on external credentials, principals, permission sets, auth providers, certificates, connected apps, remote site settings, and secrets managed outside source control.
- APIs can depend on external IDs, duplicate rules, validation rules, field-level security, sharing, platform events, CDC, bulk limits, and integration user access.
- Never store secrets in Knowledge, source metadata, README, or history.

## Sharing And Visibility Dependencies

- Organization-wide defaults, role hierarchy, sharing rules, owner-based sharing, criteria-based sharing, teams, territories, queues, groups, restriction rules, scoping rules, and manual sharing can combine.
- Report and dashboard visibility depends on folders, report types, object access, field access, row-level sharing, and dashboard running user.

## Deployment Order

Prefer this order when applicable:

1. Licenses, packages, connected apps, named/external credentials, auth providers.
2. Data model: objects, fields, value sets, record types, tabs.
3. Security: profiles, permission sets, permission set groups, custom permissions.
4. Automation and code: flows, Apex, validation/duplicate/assignment rules.
5. UI: layouts, Lightning pages, apps, actions, navigation, mobile settings.
6. Reports, dashboards, analytics, sample data, and post-deploy assignments.

If the project already has a deployment convention, follow the project convention and use this order as a risk checklist.
