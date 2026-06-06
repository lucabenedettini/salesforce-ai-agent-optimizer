# Flow Guidance

Read this for Flow, automation, validation rules, process migration, and Flow tests.

## Non-Negotiable Checks

- Prefer Flow/configuration before Apex when suitable.
- Define runtime surface: desktop, Salesforce mobile, Field Service mobile, or all.
- Define online, offline, or degraded offline behavior when mobile/Field Service can matter.
- Avoid broad manual XML edits unless fixing known validation/deployment errors.
- Plan activation strategy; do not activate risky automation without approval.
- Validate entry criteria, fault paths, permissions, field dependencies, and record-trigger order.
- Check related validation rules, duplicate rules, assignment rules, approval processes, and Apex.
- Test Flow where Salesforce/project capabilities support it.

## Minimal Planning Evidence

- Knowledge Flow page and project memory/history.
- Trigger object, record types, fields, picklists, permissions, and user personas.
- Existing active versions and deployment activation approach.
- Mobile/offline dependency evidence when relevant.

## Preferred Approach

- Small Flow edits before rework.
- Subflows only when reuse or readability improves.
- Custom Metadata for variable business rules.
- Fault paths and user-safe errors for external/action failures.

## Validation Expectations

- Run Flow tests when present or feasible.
- Validate deploy before deploy start.
- Check package.xml includes changed Flow metadata.
- For Field Service Mobile/offline, verify supported elements and sync behavior.

## SFAO Command Hints

- `sfao command search "deploy validate" --toolset deploy`
- `python scripts/sf_agent_cli.py deploy-validate --target-org <alias> --source-dir force-app`

## Output Hint

State activation plan separately from metadata deployment.
