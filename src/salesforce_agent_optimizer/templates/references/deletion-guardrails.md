# Deletion Guardrails

Use these rules for every Salesforce data deletion, metadata deletion, package uninstall, destructive change, source delete, purge, hard delete, bulk delete, cleanup job, or automation that can remove records or metadata.

## Absolute Rule

Never delete data or metadata automatically. The agent must ask for explicit user approval for each destructive action, even in a sandbox.

Explicit approval must name:

- Target org alias and whether it is sandbox or production.
- Exact records, object/query scope, metadata components, package, or destructive manifest.
- Reason for deletion.
- Expected impact and dependencies.
- Backup/export/recovery plan.
- Validation and rollback or restore options.

Use this approval wording for CLI execution through `scripts/sf_agent_cli.py`:

```text
I explicitly approve this deletion
```

Do not treat general plan approval, previous approval, approval for another environment, or approval for a different metadata/data scope as deletion approval.

## Planning Unknowns

Do not invent missing evidence. If the agent is unsure:

- Ask the user for the missing fact; or
- Present clear scenarios with tradeoffs and ask the user to choose.

Examples:

- If record IDs are unknown, ask whether to run a read-only query and show the candidate records before deletion.
- If metadata dependencies are uncertain, inspect dependencies or present deletion vs deactivation vs keep-as-is scenarios.
- If package uninstall impact is uncertain, inspect installed package details and package dependencies before asking for approval.
- If production impact is possible, stop write/delete execution. Production remains read-only for this skill's CLI facade.

## Preferred Alternatives

Prefer non-destructive options where they satisfy the requirement:

- Deactivate automation instead of deleting it.
- Remove access or visibility instead of deleting fields/objects.
- Archive, export, or mark records inactive instead of deleting records.
- Use retention policies or platform-native lifecycle features where available.
- Keep a deprecated metadata component with clear naming and documentation when immediate deletion is risky.

## Metadata Deletions

- Do not include deleted metadata in `package.xml`.
- Use `destructiveChanges.xml` only after explicit deletion approval.
- Include dependency review for permissions, layouts, Lightning pages, record types, picklists, Flow, Apex, reports, dashboards, integrations, managed packages, and mobile exposure.
- Run deploy validation first where possible, but validation is not approval to execute deletion.

## Data Deletions

- Use read-only queries first to identify the exact record set.
- Show count, sample IDs/names, filters, owner/date criteria, and dependency risks before asking for approval.
- Export or document backup options before deleting.
- Avoid hard delete unless the user explicitly requests hard delete and accepts loss of Recycle Bin recovery.

## Official References

- Salesforce GraphQL API record deletion: https://developer.salesforce.com/docs/platform/graphql/guide/mutations-delete.html
- LWC `deleteRecord(recordId)`: https://developer.salesforce.com/docs/platform/lwc/guide/reference-delete-record.html
- Salesforce CLI command reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata deploy/destructive changes guidance: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
