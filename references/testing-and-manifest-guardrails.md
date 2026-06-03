# Testing And Package Manifest Guardrails

Read this file during planning, implementation closeout, and validation for Salesforce changes that touch Apex, Flow, metadata automation, UI metadata, integrations, access, or deployable metadata.

Official references:

- Apex testing and code coverage: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_code_coverage_intro.htm
- Run and manage application unit tests, including Apex and Flow tests when supported: https://help.salesforce.com/s/articleView?id=platform.code_run_tests.htm&type=5
- Metadata API deploy manifest/package.xml structure: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm

## Test Guardrail

- Apex must meet at least 80% coverage for changed Apex classes/triggers. Prefer 90%-100% coverage for changed code and do not treat line coverage as a substitute for meaningful assertions.
- If changed Apex cannot reach 80%, stop before final validation unless the user explicitly accepts a documented exception and the org still satisfies Salesforce deploy requirements.
- Prefer 90%-100% coverage for critical or reusable service classes, trigger handlers, security logic, integrations, async jobs, invocable actions, and package-facing APIs.
- Test every metadata type that is testable in the project and Salesforce feature set. Examples:
  - Flow: create, update, or run automated Flow tests when the Flow type and org features support it. Cover main, alternate, fault, and negative paths where practical.
  - LWC: run Jest or local component tests when the project includes them; otherwise include manual UI and accessibility validation.
  - Validation rules, formulas, record types, picklists, page layouts, Lightning pages, permissions, and sharing: include data/setup validation or user-testing steps that prove the behavior.
  - Apex callouts, named credentials, integrations, scheduled jobs, batch/queueable work, and platform events: use mocks or safe validation steps and document external dependencies.
- Validation handoff must list what was automatically tested, what was manually tested, and what remains untested with a reason.

## Required `package.xml`

At the end of the implementation phase, before validation handoff, generate a `package.xml` that includes every metadata component added or modified for the approved request.

Use the official Metadata API manifest shape:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>ComponentName</members>
        <name>MetadataType</name>
    </types>
    <version>67.0</version>
</Package>
```

Rules:

- Include added and modified metadata only.
- Do not include deleted metadata in `package.xml`; use `destructiveChanges.xml` for deletions and ask for explicit approval before destructive deploy work.
- Use explicit metadata members such as `ApexClass:AccountService`, `Flow:Account_Onboarding`, `CustomField:Account.Priority__c`, and `PermissionSet:Sales_Manager`.
- Use the project's `sfdx-project.json` `sourceApiVersion` when available, otherwise use `references/salesforce-current-version.md` for the current Metadata API version.
- Default output path: `release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml`.
- Follow an existing project release-manifest convention only when it is clear and safe. Do not overwrite an existing broad `manifest/package.xml` unless the user approved that exact overwrite.

Preferred generator:

```bash
python scripts/generate_package_manifest.py --project-root <project-root> --output release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml --metadata ApexClass:AccountService --metadata Flow:Account_Onboarding
```

For uncommitted local source-format changes:

```bash
python scripts/generate_package_manifest.py --project-root <project-root> --output release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml --from-git-status
```

If the generator cannot map a changed metadata-looking path, stop and resolve the missing mapping or pass explicit `--metadata Type:Member` values before validation.
