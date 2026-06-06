# Deploy Guidance

## When To Read

Read this file only when the current task involves package.xml, metadata deploy/retrieve, release planning, dry-run validation, destructive changes, deployment sequencing, or post-deploy manual steps.

## Combine With Existing References

- `references/testing-and-manifest-guardrails.md` for package.xml, tests, validation, and deploy readiness.
- `references/deletion-guardrails.md` when destructive changes, deletes, purges, or package uninstall are involved.
- `references/metadata-dependencies.md` for dependency ordering and metadata impact.
- `references/completion-artifacts.md` for release notes, impact assessment, UAT, and manual procedures.

## Non-Negotiable Checks

- Use the smallest correct deploy scope.
- Generate package.xml for changed metadata.
- Validate/dry-run before real deploy.
- Require an explicit target org alias.
- Respect production write guardrails.
- Choose test level deliberately.
- Consider dependency order before deploy.
- Keep destructive changes separate and separately approved.
- Document post-deploy manual steps.
- Consider rollback or recovery path.

## Minimal Planning Evidence

- Changed metadata list.
- package.xml contents and API version.
- Target org alias/environment.
- Test level and target tests.
- Dependency order and destructive scope if any.
- Manual publish/activation or post-deploy steps.

## Preferred Approach

- Validate first.
- Deploy the smallest approved scope.
- Deploy dependencies before dependents.
- Handle Flow activation deliberately.
- Keep destructive changes separate from additive/modify deploys.
- Record deploy rationale/history when applicable.

## Validation Expectations

- Capture dry-run result, test result, and deploy report compactly.
- Confirm package.xml matches changed metadata.
- Run smoke checks for affected surfaces.
- Update memory/history when a durable decision or deploy result matters.

## SFAO Command Hints

- `sfao command search "deploy" --toolset deploy`
- `python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<change>/package.xml`
- `python scripts/sf_agent_cli.py deploy-preview --target-org <alias> --manifest <package.xml>`
- `python scripts/sf_agent_cli.py deploy-validate --target-org <alias> --manifest <package.xml>`

## Mini-Rubric

- Smallest deploy scope: yes/no
- package.xml updated: yes/no
- Dry-run/validate path identified: yes/no
- Production write guardrail respected: yes/no
- Test level clear: yes/no
- Destructive changes separated: yes/no
- Post-deploy steps identified: yes/no

## Output Hint

List package.xml members, tests, manual steps, rollback, and explicit approvals.
