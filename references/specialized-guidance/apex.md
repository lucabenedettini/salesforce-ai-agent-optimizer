# Apex Guidance

Read this for Apex classes, triggers, invocable Apex, async Apex, Apex tests, and backend security.

## Non-Negotiable Checks

- Choose `with sharing` or `inherited sharing` deliberately; justify `without sharing`.
- Enforce CRUD/FLS/user-mode behavior where user data access matters.
- Keep SOQL and DML outside loops.
- Bulkify for trigger and batch-sized inputs.
- Use Custom Metadata, Custom Settings, or Custom Labels for configurable values.
- Use Named Credentials or External Credentials for callouts.
- Do not hardcode IDs, usernames, org URLs, secrets, or environment-specific values.
- Do not put PII, tokens, auth URLs, or customer data in logs.
- Prefer Queueable over older async patterns when a queued, chainable job is appropriate.
- Apply least privilege for every class exposed to users, Flow, LWC, APIs, or integration users.

## Minimal Planning Evidence

- Relevant Knowledge page and history/memory entry.
- Class/trigger source and metadata file.
- Calling surface: trigger, Flow, LWC, API, scheduled job, batch, queueable, test utility.
- Affected objects, fields, permission sets, sharing assumptions, and data volume.
- Current API version and target org behavior if release-sensitive.

## Preferred Approach

- Prefer Flow/configuration before Apex when logic is declarative, transparent, and testable.
- Keep Apex small, cohesive, bulk-safe, and reversible.
- Use selectors/services only if the project already uses that pattern or duplication demands it.
- Use explicit error handling and user-safe messages.

## Validation Expectations

- Add or update focused tests for the changed behavior.
- Prefer 90-100% coverage for touched Apex; 80% is the floor, not the target.
- Run targeted tests first; broaden only when dependencies justify it.
- Run static checks when the project already has them.

## SFAO Command Hints

- `sfao command search "apex test" --toolset apex`
- `sfao command payload-example apex-test-run`
- `python scripts/sf_agent_cli.py apex-test-run --target-org <alias> --tests <TestClass>`

## Output Hint

State why Apex is required and list the exact test classes before implementation.
