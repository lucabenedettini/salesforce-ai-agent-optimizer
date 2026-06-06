# SOQL Guidance

Read this for SOQL design, query fixes, schema-driven planning, and compact data reads.

## Non-Negotiable Checks

- Never use `SELECT *` thinking.
- Select only fields needed for the question or behavior.
- Keep relationship queries only as deep as needed.
- Filter in SOQL instead of Apex when selective and safe.
- Consider indexed/selective filters for high-volume objects.
- Use bind variables for user input in Apex.
- Apply user-mode/security expectations when SOQL is embedded in Apex.
- Avoid exporting customer data into repo, Knowledge, memory, or logs.

## Minimal Planning Evidence

- SObject describe when schema is uncertain.
- Required fields, relationship names, picklists, record types, and FLS expectations.
- Data volume/selectivity risk when the query can run on large tables.
- Target alias and approval for org data reads.

## Preferred Approach

- Build a narrow query first.
- Use schema describe only for the object/fields needed.
- Use `LIMIT` for exploration.
- Prefer compact JSON selectors over full query payloads.

## Validation Expectations

- Validate field names and relationship paths before recommending Apex/query changes.
- For Apex, run tests that cover empty, one, and many records.
- Confirm FLS/CRUD strategy when query results are user-visible.

## SFAO Command Hints

- `sfao soql build --sobject Account --field Id --field Name --where "Name LIKE 'ACC%'"`
- `python scripts/sf_agent_cli.py data-query --target-org <alias> --query "<SOQL>" --max-list 5`

## Output Hint

Show the query shape, selected fields, and why each field is needed.
