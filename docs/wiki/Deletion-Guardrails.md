# Deletion Guardrails

Salesforce AI Agent Optimizer never deletes Salesforce data or metadata automatically.

## Explicit Approval

Every destructive action requires separate user approval for the exact scope:

- Data delete.
- Metadata delete.
- Package uninstall.
- Source delete.
- Purge or hard delete.
- Deploy with `destructiveChanges.xml`.

CLI execution through `scripts/sf_agent_cli.py` requires:

```bash
--delete-approval "I explicitly approve this deletion"
```

General plan approval is not enough.

## Planning Rule

If evidence is missing, the agent must not invent. It must ask the user or present scenarios with tradeoffs.

## Production

Production orgs remain read-only through the Salesforce CLI facade.

Canonical rules live in `references/deletion-guardrails.md`.
