# Deploy Guidance

Read this for deploys, package.xml, release validation, rollback, and destructive changes.

## Non-Negotiable Checks

- Use the smallest deploy scope that satisfies the approved requirement.
- Generate package.xml for added or modified metadata.
- Keep destructive changes separate and separately approved.
- Run dry-run/preview/validate before deploy start.
- Production writes are blocked by SFAO guardrails.
- Choose test level deliberately and list targeted tests.
- Respect deploy order: schema, permissions, Apex, Flow draft/activation, UI exposure.
- Track manual post-deploy steps separately.

## Minimal Planning Evidence

- Changed metadata list from git, Knowledge, or explicit metadata arguments.
- package.xml contents and API version.
- Target org alias and production/sandbox status.
- Test classes/Flow tests and rollback path.
- Permission and dependency impact.

## Preferred Approach

- Validate first.
- Deploy only approved files/metadata.
- Avoid broad source-dir deploys when a manifest or focused source list is safer.
- Use post-deploy manual procedures for secrets, users, assignments, scheduled jobs, and data.

## Validation Expectations

- `sfao validate`
- `python scripts/validate_skill.py --json` for this repo.
- `python scripts/sf_agent_cli.py deploy-validate --target-org <alias> ...` for org validation.
- Review deploy report compactly if validation returns a job id.

## SFAO Command Hints

- `sfao command search "deploy" --toolset deploy`
- `python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<change>/package.xml`
- `python scripts/sf_agent_cli.py deploy-preview --target-org <alias> --manifest <package.xml>`

## Output Hint

List package.xml members, tests, manual steps, rollback, and explicit approvals.
