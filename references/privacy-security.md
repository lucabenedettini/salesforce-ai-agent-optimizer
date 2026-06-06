# Privacy And Security Guardrails

Use this reference whenever a Salesforce request can touch org access, customer data, personal data, auth material, integrations, connected apps, named credentials, exports, Knowledge generation, AI/data activation, analytics, Experience/guest access, or release documentation.

## Non-Negotiable Rules

- Inform the user before risky operations and ask explicit approval for the exact scope.
- Never expose Salesforce credentials, access tokens, auth URLs, refresh tokens, session IDs, private keys, connected-app secrets, named credential secrets, cookies, or customer data unless the user explicitly approves that exact exposure and no safer option is sufficient.
- Prefer read-only, narrow, redacted, aggregate, or metadata-only inspection before reading records or secrets.
- Do not store secrets, raw customer data, screenshots with personal data, org auth files, `.sf/`, `.sfdx/`, exports, or record samples in repository files, Knowledge, release artifacts, logs, issues, or prompts.
- Production orgs remain read-only through the Salesforce CLI facade.
- Destructive operations also require `references/deletion-guardrails.md` and separate destructive approval.

## Approval Phrases

For destructive data or metadata operations through `scripts/sf_agent_cli.py`:

```text
I explicitly approve this deletion
```

For commands that can expose or handle Salesforce secrets through `safe-run`:

```text
I explicitly approve exposing Salesforce secrets
```

General approval for a plan is not approval to expose secrets, export data, delete data, delete metadata, uninstall packages, or run destructive manifests.

## Planning Checklist

- Identify data classification: metadata only, synthetic data, business data, personal data, sensitive personal data, credentials, secrets, or regulated data.
- Identify the minimum org alias, object, record set, user/persona, metadata component, package, integration, or file scope required.
- Prefer counts, schema, permissions, dependency summaries, and sampled redacted records over full exports.
- Use `--select`, `--max-list`, `--max-chars`, narrow SOQL fields, selective `WHERE` clauses, and metadata selectors.
- Redact usernames, emails, tokens, session IDs, auth URLs, org IDs, record IDs, endpoint secrets, and customer values when they are not required for the decision.
- Keep Knowledge token-efficient and safe: store summaries, metadata names, dependencies, and decisions; do not store secrets or raw business records.
- For integrations, prefer Named Credentials, External Credentials, least-privilege integration users, certificate rotation, and secret storage outside source control.
- For Experience Cloud, guest access, analytics, AI, Data 360/Data Cloud, Marketing Cloud, or mobile/offline sync, review data exposure, consent, retention, sharing, and offline storage before planning.

## Salesforce CLI Use

- Use `scripts/sf_agent_cli.py` before direct `sf` commands.
- Ask for an explicit org alias before org access; never rely on the default org.
- Use `org-inspect` before write/execute planning to verify sandbox/scratch vs production.
- Use `safe-run` only when a first-class facade command does not exist.
- `safe-run` blocks secret-exposure commands such as access-token display, auth URL handling, and verbose org display unless the exact secret approval phrase is provided.
- Do not run broad retrieves, full describes, full exports, or full metadata catalogs unless the user asks for broad analysis or the planning evidence proves it is necessary.

## Official References

- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure
- Salesforce CLI command reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Salesforce Metadata API deploy and destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
