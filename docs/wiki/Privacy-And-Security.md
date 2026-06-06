# Privacy And Security

Salesforce Agent Optimizer treats privacy and security as delivery gates, not as final review notes.

## Operating Model

- Agents must inform the user before risky operations.
- File changes, org writes, deploys, and metadata changes require approval through the normal planning gate.
- Destructive operations require a separate approval for the exact target org and scope.
- Secret exposure requires a separate approval for the exact secret scope.
- Production orgs remain read-only through the Salesforce CLI facade.

## Sensitive Scopes

The agent must apply privacy/security planning before:

- Org access, SOQL data reads, exports, Knowledge generation, or documentation that can include customer data.
- Auth, access token, auth URL, JWT, private key, connected app, named credential, session, or cookie handling.
- Deploys, package install/uninstall, data writes, destructive changes, source delete, purge, or hard delete.
- Experience Cloud, guest users, integrations, analytics, AI, Data 360/Data Cloud, Marketing Cloud, mobile, or offline sync.

## Consent Phrases

For destructive operations:

```text
I explicitly approve this deletion
```

For commands that can expose or handle Salesforce secrets:

```text
I explicitly approve exposing Salesforce secrets
```

General plan approval is not enough for either scope.

## Data Minimization

The skill pushes agents to use:

- Explicit org aliases.
- Narrow SOQL fields and selective `WHERE` clauses.
- Metadata selectors instead of broad retrieves.
- `--select`, `--max-list`, and `--max-chars`.
- Redacted summaries instead of raw logs or raw record samples.
- Local Knowledge summaries instead of storing business records or secrets.

## CLI Facade Enforcement

`scripts/sf_agent_cli.py` enforces:

- Alias requirement for org commands.
- Production write/execute blocking.
- Destructive approval for delete/uninstall/purge/hard-delete/destructiveChanges.
- Secret approval for access-token/auth URL/private-key/session-material exposure through `safe-run`.
- Redaction for output, dry-run command previews, and deploy history.

## What Must Never Be Committed

- `.sf/`, `.sfdx/`, auth files, scratch org credentials, exports, access tokens, refresh tokens, session IDs, auth URLs, private keys, connected-app secrets, named credential secrets, cookies, customer records, or unredacted screenshots.

## Official Basis

- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure
- Salesforce CLI command reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata deploy and destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
