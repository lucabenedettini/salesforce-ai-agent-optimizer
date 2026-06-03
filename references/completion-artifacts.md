# Completion Artifacts

At the end of the development phase, before validation handoff or final delivery, first generate the required `package.xml` described in `references/testing-and-manifest-guardrails.md`. Then ask the user whether to generate optional delivery files. Generate optional files only after the user confirms which files are wanted and where to place them.

Default folder when the user does not specify one:

```text
release-artifacts/<yyyy-mm-dd>-<short-change-name>/
```

Use Markdown by default because it is diffable, reviewable, and easy to convert to PDF or DOCX later.

The required `package.xml` should be saved in the same default folder unless the project has an approved release-manifest convention.

## Required Prompt

After generating `package.xml`, ask:

```text
Vuoi generare uno o piu' artefatti di fine sviluppo?
- release-notes.md
- technical-specifications.md
- impact-assessment.md
- user-testing.md
- manual-procedures.md
Dimmi quali vuoi generare e in quale cartella salvarli.
```

If the user asks for all files, generate all five.

## Metadata Change Classification

Every artifact that references metadata must classify each artifact as:

- Added
- Modified
- Removed
- Not changed but impacted

Use explicit metadata names such as:

- `CustomObject:Invoice__c`
- `CustomField:Account.Priority__c`
- `Flow:Account_Onboarding`
- `ApexClass:AccountService`
- `PermissionSet:Sales_Manager`
- `FlexiPage:Account_Record_Page`

If metadata cannot be known exactly, state the assumption and mark it as `To verify`.

## `release-notes.md`

Purpose: concise release summary for business, admin, and delivery stakeholders.

Required sections:

- `# Release Notes`
- `## Summary`
- `## Requirements Delivered`
- `## Metadata Added`
- `## Metadata Modified`
- `## Metadata Removed`
- `## User-Visible Changes`
- `## Validation Summary`
- `## Known Limitations Or Follow-Ups`
- `## Deployment Notes`

## `technical-specifications.md`

Purpose: technical traceability from requirements to implementation.

Required sections:

- `# Technical Specifications`
- `## Requirements`
- `## Requirement Fulfillment Matrix`
- `## Metadata Added`
- `## Metadata Modified`
- `## Metadata Removed`
- `## Configuration Decisions`
- `## Customization Decisions`
- `## Dependencies`
- `## Security And Access`
- `## Validation And Test Evidence`
- `## Assumptions`

The requirement fulfillment matrix must map each requirement to the metadata/configuration/customization that satisfies it.

## `impact-assessment.md`

Purpose: explain all pre-existing areas changed or impacted.

Required sections:

- `# Impact Assessment`
- `## Pre-Existing Metadata Modified`
- `## Pre-Existing Automations Impacted`
- `## Access And Security Impact`
- `## Data Model Impact`
- `## UI And User Experience Impact`
- `## Integration Impact`
- `## Reporting And Analytics Impact`
- `## Mobile Impact`
- `## Package/Product Impact`
- `## Risks And Mitigations`
- `## Rollback Considerations`

Include `Not changed but impacted` items when a dependency changes behavior without editing that artifact directly.

## `user-testing.md`

Purpose: guide users through Salesforce UI tests for the new or changed requirements.

Required sections:

- `# User Testing`
- `## Test Personas`
- `## Test Data Needed`
- `## Test Scenarios`
- `## Expected Results`
- `## Negative Tests`
- `## Mobile Tests`
- `## Permission/Access Tests`
- `## Regression Tests`
- `## Sign-Off Checklist`

Write tests in user language, not only technical language. Include navigation paths when known.

## `manual-procedures.md`

Purpose: list manual post-deploy steps that cannot be safely or fully deployed as metadata.

Required sections:

- `# Manual Procedures`
- `## Post-Deploy Checklist`
- `## Configuration Records To Create Or Update`
- `## Custom Settings`
- `## Custom Metadata Records`
- `## Users To Create Or Update`
- `## Permission Set Assignments`
- `## Permission Set Group Assignments`
- `## Public Groups`
- `## Queues`
- `## Licenses Or Package Assignments`
- `## Named Credential Or External Credential Secrets`
- `## Scheduled Jobs Or Batch Jobs`
- `## Data Loads Or Data Fixes`
- `## Verification Steps`
- `## Owner And Timing`

Never include secrets. For secrets, state where the authorized admin must enter them manually.

## Quality Rules

- Do not invent metadata. Use repository diff, Knowledge history, generated `package.xml`, deploy manifest, Salesforce CLI output, and user-approved plan.
- Keep files concise but complete enough for handoff.
- Mark unknowns explicitly as `To verify`.
- Include added, modified, removed metadata in every relevant file.
- Link to Knowledge history when available.
