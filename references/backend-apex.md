# Backend Apex Guidelines

## Minimal Custom Code Rule

Before writing Apex, confirm that Flow, validation rules, formula fields, standard duplicate rules, assignment/escalation rules, approvals, invocable actions, or package features are insufficient. State the gap in one sentence.

Before changing Apex `apiVersion`, read `references/salesforce-current-version.md`, verify current Salesforce release behavior, and include compatibility tests in the plan.

## Apex Checklist

- Bulkify every entry point. Handle 0, 1, 200, and larger async batches.
- Keep SOQL, DML, callouts, and expensive describe calls out of loops.
- Query only needed fields and use selective filters for large data volumes.
- Use maps/sets for joins and deduplication.
- Keep triggers thin; use one trigger per object and delegate to handler/service classes.
- Avoid hard-coded IDs and names that vary by org; use custom metadata, custom settings only for legacy needs, custom permissions, or describe lookups.
- Enforce security intentionally: `with sharing`, inherited sharing, `WITH USER_MODE`, user-mode DML, `Security.stripInaccessible`, or explicit checks as appropriate.
- Use named credentials/external credentials for callouts.
- Prefer Queueable for async orchestration, Batch Apex for large datasets, Platform Events for decoupling, and scheduled jobs only when cadence matters.
- Return typed errors to LWC/Flow and avoid leaking internal details.

## Tests

Tests should prove behavior, not just coverage:

- Use test data factories when local patterns exist.
- Include bulk scenarios and negative paths.
- Assert security/permission-sensitive behavior where relevant.
- Use `Test.startTest()` and `Test.stopTest()` around async/limit-sensitive execution.
- Avoid `SeeAllData=true` 
- Test changed Apex at least 80% of code lines, with 90%-100% preferred for new, critical, reusable, integration, security, async, invocable, and trigger-handler code.
- Treat coverage as a gate, not proof. Assertions must prove positive, negative, bulk, security, and async behavior where relevant.

## Review Heuristics

Reject or revise code that:

- Performs queries/DML in loops.
- Has multiple triggers on the same object without consolidation strategy.
- Swallows exceptions silently.
- Depends on profile names or production IDs.
- Uses static recursion flags that block legitimate multi-pass operations.
- Exposes `@AuraEnabled` methods without sharing/security review.
