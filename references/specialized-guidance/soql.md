# SOQL Guidance

## When To Read

Read this file only when the current task involves SOQL/SOSL query design, query optimization, relationship queries, aggregate queries, query embedded in Apex, or query used by data read/export.

## Combine With Existing References

- `references/sf-agent-cli-commands.md` for compact Salesforce CLI query command shapes.
- `references/privacy-security.md` when query output, exports, customer data, or sensitive fields are involved.
- `references/least-privilege-planning.md` when query access moves into Apex, LWC, Flow, or integration users.

## Non-Negotiable Checks

- Do not use `SELECT *` thinking.
- Select only fields needed for the question or behavior.
- Filter in SOQL rather than post-filtering when possible.
- Justify relationship direction and depth.
- Use aggregate queries for counts/summaries when record payloads are unnecessary.
- Use bind variables for user input in Apex.
- Define security/user-mode expectations when embedded in Apex.
- Consider selective filters and indexed fields when volume matters.
- Avoid leading wildcards when performance matters.
- Use `LIMIT` and `ORDER BY` deliberately.
- Do not export sensitive data without explicit approval.

## Minimal Planning Evidence

- Target object and required fields.
- Filter criteria and expected volume.
- Relationship direction and depth.
- Consuming context: Apex, CLI, export, UI, automation, or integration.
- FLS/access assumptions when user-visible.

## Preferred Approach

- Start with the simplest correct query.
- Add only needed fields and relationships.
- Use semi-joins or anti-joins when they reduce payload and match the requirement.
- Use aggregates instead of loading records for summaries.
- Use the SFAO SOQL helper when available.

## Validation Expectations

- Validate syntax and field existence from local metadata or org describe when needed.
- Use query plan/performance review only when volume/performance risk justifies it.
- Confirm no sensitive export or storage unless explicitly approved.
- For Apex queries, run tests covering empty, one, and many records when behavior changes.

## SFAO Command Hints

- `sfao soql build --object Account --fields Id,Name --where "Name LIKE 'ACC%'"`
- `python scripts/sf_agent_cli.py data-query --target-org <alias> --query "<SOQL>" --max-list 5`

## Mini-Rubric

- Fields minimized: yes/no
- Filters/selectivity considered: yes/no
- Relationship depth justified: yes/no
- Security context considered: yes/no
- Expected volume considered: yes/no
- Execution path identified: yes/no

## Output Hint

Show the query shape, selected fields, and why each field is needed.
