# Salesforce Current Version Context

Last verified: 2026-06-05

## Current Production Reference

- Current Salesforce release reference: Summer '26.
- Current Salesforce Platform API version: 67.0.
- Current Metadata API version for new manifests when no project version exists: 67.0.
- Current SOAP API version reference: 67.0.

Production rollout can vary by org and instance. Before changing a project `sourceApiVersion`, package manifest version, LWC `apiVersion`, Apex class version, or integration endpoint, confirm the target org release and run the relevant tests.

## SOAP API Guardrails

- Do not design new authentication around SOAP `login()`.
- SOAP API `login()` is unavailable in API versions 65.0 and later.
- Salesforce has announced retirement of SOAP API `login()` in versions 31.0 through 64.0 with Summer '27.
- Prefer OAuth, External Client Apps, JWT bearer, named credentials, or other current Salesforce-supported auth patterns.

## Project API Version Rules

- Read `sfdx-project.json` first. Preserve the existing `sourceApiVersion` unless the task explicitly requires an upgrade or the user approves one.
- Use the current API version for new sample manifests only when the project has no version.
- Upgrading API versions can change runtime or compile behavior for Apex, LWC, Flow, metadata deployments, integrations, and security defaults. Plan and test it as a change, not as formatting.
- For LWC, Salesforce validates `apiVersion` and the latest valid API version is the current Salesforce release. Update component API versions when modifying components and after compatibility checks.

## Managed Package Version Rules

Managed package versions are org-specific. Do not assume a public latest version is installed in the user's org.

Before package-specific planning, ask for the org alias when package evidence is needed and run:

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

Record package name, namespace, installed version name/number, subscriber package version id when available, target org, and verification date in the plan or Knowledge. Use official package release notes only when they exist and are clearly tied to the installed version.

## Sources

- Salesforce Summer '26 Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5
- Salesforce Summer '26 API Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.rn_api.htm&language=en_US&type=5
- Salesforce Summer '26 SOAP API Release Notes: https://help.salesforce.com/s/articleView?id=release-notes.rn_api_soap.htm&language=en_US&type=5
- Platform SOAP API login() Retirement: https://help.salesforce.com/s/articleView?id=005132110&language=en_US&type=1
- Salesforce API and Data Loader versions: https://help.salesforce.com/s/articleView?id=000349115&language=en_US&type=1
- LWC component versioning: https://developer.salesforce.com/docs/platform/lwc/guide/create-version-components.html
