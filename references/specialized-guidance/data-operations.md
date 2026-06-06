# Data Operations Guidance

## When To Read

Read this file only when the current task involves test data, data create/update/delete/upsert, imports, exports, cleanup scripts, anonymous Apex for data setup, or bulk operations.

## Combine With Existing References

- `references/privacy-security.md` for customer data, exports, logs, and sensitive data handling.
- `references/deletion-guardrails.md` when delete, purge, hard delete, or destructive cleanup is involved.
- `references/sf-agent-cli-commands.md` for compact Salesforce CLI data command shapes.
- `references/least-privilege-planning.md` for access and user permission impact.

## Non-Negotiable Checks

- Distinguish script generation from remote org execution.
- Require explicit org alias for remote data operations.
- Block production data mutation through SFAO guardrails.
- Use synthetic/non-sensitive data for tests.
- Do not commit raw customer data to repo, Knowledge, memory, docs, logs, or screenshots.
- Describe/check schema when required fields, picklists, or relationships are uncertain.
- Define cleanup plan for created data.
- Require separate explicit approval for destructive data operations.
- Use bulk mechanisms only when volume requires them.
- Verify required fields and picklist values before remote execution.

## Minimal Planning Evidence

- Target objects and operation type.
- Target org alias for remote execution.
- Volume and filter scope.
- Parent-child dependencies, required fields, and picklist values.
- Cleanup strategy and permission/access assumptions.

## Preferred Approach

- Generate local scripts or payloads first when possible.
- Use small, reversible, synthetic data sets.
- Use narrow SOQL selectors and `LIMIT` for verification.
- Prefer CLI for simple operations and Apex only when orchestration requires it.
- Avoid storing exports; if unavoidable, require explicit scope and retention plan.

## Validation Expectations

- Report record counts and created/updated IDs only when safe.
- Confirm cleanup commands and destructive approval if deletes are needed.
- Verify no sensitive data was stored.
- Update memory only for durable decisions or lessons, never raw data.

## SFAO Command Hints

- `python scripts/sf_agent_cli.py data-query --target-org <alias> --query "<SOQL>" --max-list 5`
- `python scripts/sf_agent_cli.py data-record-create --target-org <alias> --sobject Account --values "Name=ACC Test"`
- `python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id <id> --delete-approval "I explicitly approve this deletion"`

## Mini-Rubric

- Script generation vs remote execution distinguished: yes/no
- Org alias required for remote operations: yes/no
- Production data mutation blocked: yes/no
- Synthetic/non-sensitive data only: yes/no
- Schema assumptions checked: yes/no
- Cleanup plan identified: yes/no
- Destructive approval required when applicable: yes/no

## Output Hint

State whether the step is local script generation or remote org execution.
