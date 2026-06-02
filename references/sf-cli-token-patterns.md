# Salesforce CLI Token Patterns

## Use The Agent Facade First

Prefer `scripts/sf_agent_cli.py` for Salesforce org operations. It wraps the official `sf` CLI with compact output, explicit alias requirements, secure auth commands, and production read-only guardrails.

Use `scripts/sf_min.py` only as a compact fallback for a read-only official `sf` command that has not yet been added to `sf_agent_cli.py`.

## Token-Efficient Rules

- Use `--json` whenever supported.
- Select only the JSON paths needed for the next decision.
- Prefer command-specific flags such as `--metadata`, `--source-dir`, `--target-org`, `--tests`, and `--test-level`.
- Avoid `sf commands`, broad metadata retrieval, full org describe, or full package listings unless the task needs them.
- Use SOQL with explicit fields and selective WHERE clauses.
- Redact access tokens, session IDs, auth URLs, client secrets, named credential secrets, and cookies before returning output.
- Summarize large arrays by count plus first few relevant items.

## Wrapper Strategy

Use `scripts/sf_agent_cli.py`:

- Ask the user for the org alias before metadata or data access.
- Authenticate with `auth-web`, `auth-device`, or `auth-jwt`.
- Never use default orgs for agent work.
- Let the facade block write/execute operations on production orgs.
- Use `--select`, narrow SOQL, and narrow metadata selectors.
- Use `safe-run` for installed official `sf` commands that are not exposed as first-class facade commands.
- Run `catalog-refresh` after upgrading Salesforce CLI to regenerate `sf-official-command-catalog.md` and `.json`.

Use `scripts/sf_min.py` fallback:

- Pass the `sf` command after the script name.
- The script appends `--json` when the command does not already specify it.
- Use `--select path1,path2` to keep only needed JSON paths.
- Use `--max-chars N` to cap output.
- Use `--raw` only when JSON output is unsupported or harmful.

## Rewrite Decision

Only create a custom Salesforce CLI plugin or rewrite a command when all are true:

- The workflow is repeated across projects or agents.
- The official CLI output cannot be reduced enough with `--json`, selectors, or local filtering.
- The custom command has one distinct task and stable flags.
- JSON output has a stable schema.
- The command does not hide errors or alter deploy/test semantics.

If rewriting, follow Salesforce CLI plugin conventions: kebab-case long flags, one task per command, `--json` support, stable JSON schema, and standard org/api-version flags where applicable. Add the rewritten command to `scripts/sf_agent_cli.py` and document it in `references/sf-agent-cli-commands.md`.
