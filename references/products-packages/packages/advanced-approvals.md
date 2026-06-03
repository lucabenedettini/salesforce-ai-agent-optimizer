# Nome del prodotto/pacchetto: Advanced Approvals

## Breve descrizione sintetica
Salesforce CPQ managed package capability for advanced quote approval rules, approval chains, approvers and approval automation.

## Oggetti principali
- CPQ quote and quote line objects, Opportunity, Account, User and Group.
- Advanced Approval managed objects for approval rules, conditions, chains, variables, approvers and approval records.
- Exact API names and namespace depend on package version; inspect installed metadata before planning.

## Funzionalita principali
- Multi-step approval chains.
- Conditional approval rules based on quote, line, account, discount or custom fields.
- Dynamic approver selection and approval notifications.
- Approval status tracking and quote locking behavior.

## Configurazioni principali
- Approval rules, conditions, chains, approval step order and variables.
- Approver records/groups, submitter access and email templates.
- Quote fields used by criteria, CPQ package settings and permission sets.
- Page layouts, Lightning pages, buttons/actions and automation around submission.

## Best practice
- Model approval policy before configuring rules.
- Keep criteria fields indexed/maintainable and avoid duplicated logic across rules.
- Test skip paths, rejection, recall, resubmission, parallel chains and delegated approvers.
- Plan CPQ, permission, email template, layout and automation dependencies together.
