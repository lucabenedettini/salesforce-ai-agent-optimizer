# Data Operations Guidance

Read this for data CRUD, data loads, exports/imports, test data, and cleanup.

## Non-Negotiable Checks

- Distinguish script generation from remote org execution.
- Remote org data operations need explicit alias and approval.
- Production data changes are blocked/not allowed through SFAO guardrails.
- Use synthetic data for testing unless the user explicitly authorizes real data reads.
- Describe first when schema or required fields are uncertain.
- Create a cleanup plan for test data.
- Destructive data delete requires separate explicit approval for exact records/scope.
- Do not export/store customer data in repo, Knowledge, memory, docs, screenshots, or logs.
- Redact IDs, emails, names, and sensitive values unless essential and approved.

## Minimal Planning Evidence

- Target org alias and production/sandbox status.
- Object schema, required fields, validation rules, triggers/flows, duplicate rules.
- Data volume and filter scope.
- Permission/access check for the acting user or integration user.

## Preferred Approach

- Prefer local synthetic payloads for tests.
- Use narrow SOQL selectors and `LIMIT`.
- Use create/update/delete only through SFAO facade guardrails.
- Avoid bulk operations unless the user asked and rollback is defined.

## Validation Expectations

- Dry-run or preview command shape first.
- Confirm created records with a compact query only when needed.
- Clean up test data with explicit approval for deletes.
- Record durable lessons in memory without raw data.

## SFAO Command Hints

- `python scripts/sf_agent_cli.py data-query --target-org <alias> --query "<SOQL>" --max-list 5`
- `python scripts/sf_agent_cli.py data-record-create --target-org <alias> --sobject Account --values "Name=ACC Test"`
- `python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id <id> --delete-approval "I explicitly approve this deletion"`

## Output Hint

State whether the step is local script generation or remote org execution.
