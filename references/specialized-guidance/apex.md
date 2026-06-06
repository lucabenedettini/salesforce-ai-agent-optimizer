# Apex Guidance

## When To Read

Read this file only when the current task involves Apex classes, triggers, invocable Apex, async Apex, Apex tests, backend security, or service/selector/domain patterns already used by the project.

## Combine With Existing References

- `references/backend-apex.md` for project Apex delivery guidance.
- `references/testing-and-manifest-guardrails.md` for tests, package.xml, and validation.
- `references/least-privilege-planning.md` for permission and access impact.
- `references/privacy-security.md` when logs, secrets, integrations, or customer data are involved.

## Non-Negotiable Checks

- Choose `with sharing`, `inherited sharing`, or justify `without sharing` explicitly.
- Enforce CRUD/FLS/user-mode behavior where user data access matters.
- Keep SOQL and DML outside loops.
- Plan bulk behavior for triggers, batches, queues, and imports.
- Consider governor-limit impact before adding queries, DML, callouts, or async chains.
- Do not hardcode IDs, usernames, org URLs, secrets, or environment-specific values.
- Use Custom Metadata, Custom Settings, or Custom Labels for configurable values.
- Use Named Credentials or External Credentials for callouts.
- Do not put PII, tokens, auth URLs, or customer data in logs.
- Provide clear error handling and user-safe messages.
- Identify tests for changed behavior and package.xml impact.

## Minimal Planning Evidence

- Relevant Knowledge page and project memory/history entry.
- Touched class, trigger, and `*-meta.xml` files.
- Calling surface: trigger, LWC, Flow, API, batch, queueable, schedulable, or test utility.
- Affected objects, fields, permission assumptions, and expected data volume.
- Existing test classes and related package.xml members.

## Preferred Approach

- Prefer Flow/configuration before Apex when the logic is declarative, transparent, and testable.
- Keep Apex cohesive, minimal, bulk-safe, and aligned to existing project architecture.
- Avoid introducing new frameworks unless the project already uses them.
- Prefer Queueable for queued, chainable work when appropriate.
- Use selectors/services/domain layers only when they reduce duplication or match the existing pattern.

## Validation Expectations

- Run targeted Apex tests first; broaden only when dependency or risk requires it.
- Prefer 90-100% coverage for touched Apex; 80% is the floor.
- Run static checks when the project already has them.
- Validate deploy/package.xml when metadata changed.

## SFAO Command Hints

- `sfao command search "apex test" --toolset apex`
- `sfao command payload-example apex-test-run`
- `python scripts/sf_agent_cli.py apex-test-run --target-org <alias> --tests <TestClass>`

## Mini-Rubric

- Sharing model explicit: yes/no
- CRUD/FLS/user-mode considered: yes/no
- SOQL/DML outside loops: yes/no
- Bulk/governor-limit behavior considered: yes/no
- Tests identified: yes/no
- package.xml impact clear: yes/no
- Memory update needed or handled: yes/no

## Output Hint

State why Apex is required, the affected access model, the exact test classes, and the package.xml impact before implementation.
