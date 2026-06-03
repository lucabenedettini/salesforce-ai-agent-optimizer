# Salesforce Version Update Workflow

Read this file when the user invokes `/sf-version-update-skill`, runs `sfao version-context update`, or asks to refresh Salesforce release, API, SOAP API, LWC API, Metadata API, or managed package version context.

## Goal

Update the skill's version-sensitive resources with the latest production Salesforce technical and functional information, while avoiding stale or invented package versions.

## Required Online Research

Search online in official Salesforce sources only. Prefer:

- Salesforce Release Notes for the latest production release.
- API Release Notes.
- SOAP API Release Notes.
- SOAP API retirement/help articles.
- SOAP API, REST API, Metadata API, Tooling API, GraphQL API, UI API, LWC, Flow, Apex, Data Cloud, Agentforce, and packaging official docs when relevant.
- Official product/package release notes for Salesforce-owned products or packages.

Do not use blogs, Stack Exchange, AppExchange reviews, vendor marketing pages, or AI summaries as source of truth unless the user explicitly asks for broader research. If a Salesforce Help page is hard to scrape, use the visible search result, release-note page title, and official URL, then mark details that need manual confirmation.

## Version Facts To Capture

Capture:

- Verification date.
- Current Salesforce production release name.
- Current Platform API version.
- Current Metadata API version.
- Current SOAP API version.
- SOAP API authentication/retirement changes.
- LWC API version requirements and compatibility notes.
- Metadata coverage/report status when relevant.
- API end-of-life or retirement windows.
- Functional release items that affect agents, metadata, Apex, Flow, LWC, integrations, packaging, and Data Cloud.

For managed packages:

- Do not assume a global current package version.
- If the task involves a target org, ask for the org alias and use `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result`.
- If no org alias is available, update only the package version policy and official source links. Mark installed package versions as `Target org required`.
- For Salesforce-owned packages with official release notes, record the official release-note source but still verify the installed version in the target org before planning.

## Update Targets

Update at minimum:

- `references/salesforce-version.json`
- `references/salesforce-current-version.md`
- `references/official-salesforce-sources.md` when new official sources are needed
- `references/products-packages/index.md` if package/product version policy changes
- Product/package files only when there is a specific official version-sensitive change for that product/package
- `README.md` and `docs/wiki/` when user-facing behavior or current public version changes
- `scripts/generate_package_manifest.py` only if the fallback API version logic changes

Use the public CLI to scaffold, update, and validate version context:

```bash
sfao version-context scaffold
sfao version-context update
sfao version-context validate
```

## Validation

After updating resources:

- Run `python scripts/self_test.py --json`.
- Run the Codex skill validator.
- Search for stale explicit API versions in changed files.
- Confirm package files do not claim an installed package version unless it came from org evidence or official package release notes.
- Summarize official sources, changed files, assumptions, and any `Target org required` items.
