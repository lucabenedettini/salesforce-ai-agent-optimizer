# Salesforce Agent CLI Commands

## Policy

Use `scripts/sf_agent_cli.py` before direct `sf` calls whenever an agent connects to Salesforce for metadata or data.

Rules:

- Ask the user for the org alias before using metadata or data commands.
- Require `--target-org`; do not rely on a default org.
- Authenticate only with `auth-web`, `auth-device`, or `auth-jwt`.
- Do not expose auth-url import, passwords, session IDs, access tokens, or installation keys in output.
- Before write or execute commands, query `Organization.IsSandbox`.
- If `IsSandbox=false` or the org type cannot be determined, block write/execute commands.
- Production orgs are read-only.
- If Salesforce CLI is not discoverable in `PATH`, set `SF_AGENT_SF_BIN` to the full `sf`, `sf.cmd`, or `sf.exe` path.
- Use `--select`, explicit SOQL fields, specific metadata selectors, and bounded output.

## Printing Press Design Applied

This facade follows the `cli-printing-press` playbook for agent-native CLIs: compound commands, local context/Knowledge, compact high-signal output, dry-run support, and flags designed for repeated agent use. It remains a facade over official Salesforce `sf` commands so deployment/auth semantics stay Salesforce-native.

## Commands

### `safe-run`

Run any installed official Salesforce CLI command through the agent facade. Use this when the command is documented in `sf-official-command-catalog.md` but does not have a first-class facade command.

Rules:

- Pass the official command after `--`.
- Provide `--target-org <alias>` when the command connects to Salesforce.
- The facade appends `--json` unless `--raw` is used.
- The facade classifies safety and blocks `write`/`execute` commands on production.
- If the official command is `project deploy start` and succeeds, the facade appends deploy history.

```bash
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- data query --query "SELECT Id, Name FROM Account LIMIT 20" --select result.records
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- project retrieve preview --concise
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox --requirements "Add priority tracking to Account" --changed-metadata CustomField:Account.Priority__c -- project deploy start --source-dir force-app
```

### `catalog-refresh`

Regenerate the compact one-by-one catalog from the installed `sf commands --json` output.

```bash
python scripts/sf_agent_cli.py catalog-refresh
```

Outputs:

- `references/sf-official-command-catalog.md`
- `references/sf-official-command-catalog.json`

### `commands`

List the documented facade commands as JSON.

```bash
python scripts/sf_agent_cli.py commands
```

### `auth-web`

Secure interactive OAuth login for a human user.

Maps to: `sf org login web`

```bash
python scripts/sf_agent_cli.py auth-web --alias dev-sandbox --instance-url https://test.salesforce.com
```

### `auth-device`

Secure device-code login when browser login is not practical.

Maps to: `sf org login device`

```bash
python scripts/sf_agent_cli.py auth-device --alias dev-sandbox --instance-url https://test.salesforce.com
```

### `auth-jwt`

JWT bearer login for CI/automation with a connected app and private key.

Maps to: `sf org login jwt`

```bash
python scripts/sf_agent_cli.py auth-jwt --alias ci-sandbox --username bot@example.com --client-id 3MV... --jwt-key-file server.key --instance-url https://test.salesforce.com
```

### `org-list`

List locally authenticated orgs.

Maps to: `sf org list`

```bash
python scripts/sf_agent_cli.py org-list --select result.nonScratchOrgs
```

### `org-inspect`

Read compact org identity plus `Organization.IsSandbox`.

Maps to: `sf org display` and `sf data query`

```bash
python scripts/sf_agent_cli.py org-inspect --target-org dev-sandbox --select org_display.username,organization.records.0.IsSandbox
```

### `org-limits`

Read API/org limits.

Maps to: `sf limits api display`

```bash
python scripts/sf_agent_cli.py org-limits --target-org dev-sandbox
```

### `schema-sobject-list`

List available sObjects.

Maps to: `sf sobject list`

```bash
python scripts/sf_agent_cli.py schema-sobject-list --target-org dev-sandbox --sobject-type custom
```

### `schema-sobject-describe`

Describe one sObject.

Maps to: `sf sobject describe`

```bash
python scripts/sf_agent_cli.py schema-sobject-describe --target-org dev-sandbox --sobject Account --select result.fields
```

### `metadata-list`

List metadata members for one metadata type.

Maps to: `sf org list metadata`

```bash
python scripts/sf_agent_cli.py metadata-list --target-org dev-sandbox --metadata-type ApexClass
```

### `metadata-retrieve`

Retrieve named metadata with narrow selectors.

Maps to: `sf project retrieve start --metadata`

```bash
python scripts/sf_agent_cli.py metadata-retrieve --target-org dev-sandbox --metadata ApexClass:MyClass --metadata CustomObject:Account
```

### `metadata-retrieve-manifest`

Retrieve metadata from a package.xml manifest.

Maps to: `sf project retrieve start --manifest`

```bash
python scripts/sf_agent_cli.py metadata-retrieve-manifest --target-org dev-sandbox --manifest manifest/package.xml
```

### `deploy-preview`

Preview deployment impact without changing the org.

Maps to: `sf project deploy preview`

```bash
python scripts/sf_agent_cli.py deploy-preview --target-org dev-sandbox --source-dir force-app
```

### `deploy-validate`

Validate a deployment without committing metadata. Blocked on production.

Maps to: `sf project deploy validate`

```bash
python scripts/sf_agent_cli.py deploy-validate --target-org dev-sandbox --source-dir force-app --test-level RunLocalTests
```

### `deploy-start`

Deploy source metadata. Blocked on production.

Maps to: `sf project deploy start`

```bash
python scripts/sf_agent_cli.py deploy-start --target-org dev-sandbox --source-dir force-app --test-level RunSpecifiedTests --tests AccountServiceTest --requirements "Add priority tracking to Account" --changed-metadata CustomField:Account.Priority__c
```

Requires `--requirements` and one `--changed-metadata` for each modified metadata artifact. On success, appends a compact row to `.salesforce-agent-knowledge/history/project-history.md` and a detailed event file under `.salesforce-agent-knowledge/history/events/`.

## Git Push Recording

Use `scripts/git_knowledge_push.py` for approved remote branch pushes so Knowledge history stays complete:

```bash
python scripts/git_knowledge_push.py --project-root . --remote origin --branch feature/account-priority --requirements "Add priority tracking to Account" --metadata CustomField:Account.Priority__c
```

The wrapper records `git-push` history with requirements, all modified metadata, remote, branch, and commit; commits that Knowledge history; then runs `git push` so the remote branch contains the history entry. Use `--no-commit-history` only when the user explicitly wants local-only history for the current push.

If a direct `git push` is used, immediately call:

```bash
python scripts/knowledge_history.py --project-root . --action git-push --requirements "Add priority tracking to Account" --metadata CustomField:Account.Priority__c --remote origin --branch feature/account-priority --result "push succeeded"
```

Then commit and push the resulting `.salesforce-agent-knowledge/` history update.

### `deploy-report`

Read deployment status by job id.

Maps to: `sf project deploy report`

```bash
python scripts/sf_agent_cli.py deploy-report --target-org dev-sandbox --job-id 0Af...
```

### `data-query`

Run SOQL with explicit fields. Read-only.

Maps to: `sf data query`

```bash
python scripts/sf_agent_cli.py data-query --target-org dev-sandbox --query "SELECT Id, Name FROM Account LIMIT 20" --select result.records
```

### `data-record-get`

Read one record by sObject and record id.

Maps to: `sf data get record`

```bash
python scripts/sf_agent_cli.py data-record-get --target-org dev-sandbox --sobject Account --record-id 001...
```

### `data-record-create`

Create one record. Blocked on production.

Maps to: `sf data create record`

```bash
python scripts/sf_agent_cli.py data-record-create --target-org dev-sandbox --sobject Account --values "Name=Acme"
```

### `data-record-update`

Update one record. Blocked on production.

Maps to: `sf data update record`

```bash
python scripts/sf_agent_cli.py data-record-update --target-org dev-sandbox --sobject Account --record-id 001... --values "Rating=Hot"
```

### `data-record-delete`

Delete one record. Blocked on production.

Maps to: `sf data delete record`

```bash
python scripts/sf_agent_cli.py data-record-delete --target-org dev-sandbox --sobject Account --record-id 001...
```

### `apex-test-run`

Run Apex tests. Blocked on production.

Maps to: `sf apex run test`

```bash
python scripts/sf_agent_cli.py apex-test-run --target-org dev-sandbox --tests AccountServiceTest --code-coverage
```

### `apex-test-report`

Read Apex test run results.

Maps to: `sf apex get test`

```bash
python scripts/sf_agent_cli.py apex-test-report --target-org dev-sandbox --test-run-id 707...
```

### `apex-log-list`

List Apex debug logs.

Maps to: `sf apex list log`

```bash
python scripts/sf_agent_cli.py apex-log-list --target-org dev-sandbox
```

### `apex-log-get`

Fetch one Apex debug log.

Maps to: `sf apex get log`

```bash
python scripts/sf_agent_cli.py apex-log-get --target-org dev-sandbox --log-id 07L...
```

### `apex-run`

Execute anonymous Apex from a file. Blocked on production.

Maps to: `sf apex run`

```bash
python scripts/sf_agent_cli.py apex-run --target-org dev-sandbox --file scripts/anonymous.apex
```

### `package-installed-list`

List installed packages.

Maps to: `sf package installed list`

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org dev-sandbox
```

### `package-install`

Install a package. Blocked on production.

Maps to: `sf package install`

```bash
python scripts/sf_agent_cli.py package-install --target-org dev-sandbox --package 04t...
```

### `package-uninstall`

Uninstall a package. Blocked on production.

Maps to: `sf package uninstall`

```bash
python scripts/sf_agent_cli.py package-uninstall --target-org dev-sandbox --package 04t...
```

### `user-display`

Display Salesforce user information.

Maps to: `sf org display user`

```bash
python scripts/sf_agent_cli.py user-display --target-org dev-sandbox
```

### `permset-assign`

Assign a permission set. Blocked on production.

Maps to: `sf org assign permset`

```bash
python scripts/sf_agent_cli.py permset-assign --target-org dev-sandbox --name Sales_User
```

### `local-manifest-generate`

Generate a local package.xml manifest. Does not connect to an org.

Maps to: `sf project generate manifest`

```bash
python scripts/sf_agent_cli.py local-manifest-generate --metadata ApexClass:MyClass --output-dir manifest
```

## Extending The Facade

When an agent needs an official Salesforce CLI command that is not listed:

1. Check the latest official Salesforce CLI reference.
2. Check `references/sf-official-command-catalog.md` generated from the installed CLI.
3. Use `safe-run` when a first-class wrapper is not necessary.
4. Add a minimal facade command to `scripts/sf_agent_cli.py` only for repeated workflows.
5. Mark safety as `read`, `write`, `execute`, `auth`, or `local`.
6. Require `--target-org` for org access.
7. Block `write` and `execute` commands on production.
8. Add one section to this file documenting the command.
