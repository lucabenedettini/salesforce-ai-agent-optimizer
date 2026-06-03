# Security Policy

## Supported Versions

Security fixes are applied to the latest released version of Salesforce AI Agent Optimizer.

## Reporting A Vulnerability

Report vulnerabilities through GitHub private vulnerability reporting or GitHub Security Advisories for this repository. Do not open public issues that include Salesforce org credentials, session IDs, access tokens, private keys, customer data, production metadata, or record samples containing personal data.

If a report requires reproduction details, provide the smallest safe example:

- Skill version and commit.
- Operating system and Python version.
- Command or agent surface involved.
- Redacted logs or compact JSON output.
- Whether a production org, sandbox, scratch org, or local-only project was involved.

## Salesforce Safety Expectations

- Never include Salesforce secrets in issues, pull requests, logs, screenshots, or Knowledge files.
- Production orgs must remain read-only through the CLI facade.
- Destructive data or metadata operations require separate explicit user approval for the exact target org and scope.
- When in doubt, stop and ask for clarification instead of guessing access, delete scope, org behavior, or package state.
