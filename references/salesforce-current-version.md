# Salesforce Current Version Context

Last verified: 2026-06-06

## Current Production Reference

> Freshness warning: these release/API values are local context values generated for planning. Release-sensitive behavior must be verified against current official Salesforce documentation, and the target org release can differ during phased rollouts.

- Current Salesforce release reference: Summer '26.
- Current Salesforce Platform API version: 67.0.
- Current Metadata API version: 67.0.
- Current SOAP API version: 67.0.

Confirm the target org release before changing project sourceApiVersion because Salesforce releases roll out by org and instance.

## SOAP API Guardrails

- SOAP API login() is unavailable in API versions 65.0 and later. Salesforce has announced retirement for login() in SOAP API versions 31.0 through 64.0 with Summer '27.
- Prefer OAuth, External Client Apps, JWT bearer, named credentials, or current Salesforce-supported auth patterns.

## Project API Version Rules

- Read `sfdx-project.json` first and preserve `sourceApiVersion` unless the user approves an upgrade.
- Treat API upgrades as functional changes requiring planning and tests.
- For LWC, update component `apiVersion` only after compatibility checks.

## Managed Package Version Rules

Do not assume managed package versions from public docs. Inspect installed packages in the target org and use official package release notes only when available.

## Official Source Check Summary


## Sources

- Salesforce Summer '26 Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5
- Salesforce Summer '26 API Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.rn_api.htm&language=en_US&type=5
- Salesforce Summer '26 SOAP API Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.rn_api_soap.htm&language=en_US&type=5
- Platform SOAP API login() Retirement: https://help.salesforce.com/s/articleView?id=005132110&language=en_US&type=1
- Salesforce API and Data Loader versions: https://help.salesforce.com/s/articleView?id=000349115&language=en_US&type=1
- Version Lightning Web Components: https://developer.salesforce.com/docs/platform/lwc/guide/create-version-components.html
