# Version Updates

Use `/sf-version-update-skill` to refresh Salesforce release, API, SOAP API, Metadata API, LWC API, product, and managed package version context.

## Current Snapshot

Verified on 2026-06-03:

- Salesforce release reference: Summer '26.
- Current Platform API version: 67.0.
- Current Metadata API version: 67.0.
- Current SOAP API version: 67.0.
- SOAP API `login()` is unavailable in API versions 65.0 and later.
- Salesforce has announced SOAP API `login()` retirement for versions 31.0 through 64.0 with Summer '27.

## Managed Packages

Managed package versions are target-org-specific. The agent must not assume a public latest package version is installed. When package version evidence matters, ask for the org alias and inspect installed packages.

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

## Update Command

The command reads `references/version-update.md`, searches official Salesforce sources only, and updates:

- `references/salesforce-version.json`
- `references/salesforce-current-version.md`
- other product/package, README, wiki, or source files only when version-sensitive guidance changed

Canonical rules live in `references/version-update.md`.
