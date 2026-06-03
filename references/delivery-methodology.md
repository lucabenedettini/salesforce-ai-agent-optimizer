# Delivery Methodology

## Loop Contract

Use this workflow for Salesforce implementation, architecture, debugging, migration, or release tasks. Track `cycle_count`, starting at 1. A cycle becomes unsuccessful when the user rejects the plan, tests fail, validation fails, or the implemented change no longer matches the approved plan.

Maximum: 3 unsuccessful cycles. On the fourth unsuccessful cycle, stop implementation and return to requirement explanation before proposing another plan.

## Phase 1: Request Review

Restate:

- User request.
- Salesforce product area and metadata/code area.
- Known target org or environment.
- Expected business outcome.
- Acceptance criteria, if available.

Ask questions only when needed. Prefer 1-3 high-value questions. Do not ask about details that can be discovered from the repository or safe read-only org inspection.

## Phase 2: Evidence And Planning

Consult project Knowledge first:

- Read `references/products-packages/index.md` and identify relevant Salesforce products, AppExchange packages, or mobile-development surfaces by brief description.
- Read only the matching product/package files under `references/products-packages/products/` or `references/products-packages/packages/`.
- Read `references/metadata-dependencies.md` and use it as the dependency checklist for the plan.
- Read `references/testing-and-manifest-guardrails.md` when the task touches Apex, Flow, automation, UI metadata, integrations, access, or deployable metadata.
- Read `.salesforce-agent-knowledge/index.md` before planning any modification.
- Read `.salesforce-agent-knowledge/markdown-index.md` when the exact metadata page is not obvious.
- Read the relevant per-metadata Markdown files under `.salesforce-agent-knowledge/metadata/` before opening raw source.
- Read `.salesforce-agent-knowledge/history/project-history.md` for previous deployed changes to the same artifacts.
- Read the relevant wiki pages under `.salesforce-agent-knowledge/wiki/` only when a higher-level summary is needed.
- If the folder is missing, stale, or the user invokes `/sf-init-project-skill`, run `scripts/sf_knowledge_init.py --project-root <project-root> --refresh` before planning, unless the user asked for a quick answer that does not touch the project.
- Use the Knowledge to decide what to inspect next; verify against source metadata files before making changes.

Inspect the smallest useful surface:

- Changed/touched files, metadata folders, package directories, or manifests.
- Relevant objects, fields, flows, Apex, LWC, permission sets, named credentials, custom metadata, and package dependencies.
- Targeted org data through compact CLI output when needed.

Verify official guidance when needed:

- If the agent does not know an official Salesforce behavior, cannot find it locally, suspects release-specific behavior, or wants confirmation before recommending a solution, search online in official Salesforce sources only.
- Prefer the latest available version of Salesforce documentation and release guidance.
- Use documentation pages before blog posts when both cover the same behavior.
- Cite or summarize only the specific rule that affects the plan; do not paste large documentation excerpts.

Then produce a plan with:

- Requirement summary.
- Products/packages identified and product/package reference files read.
- Configuration-first solution.
- Custom code only if justified.
- Exact files/metadata expected to change.
- Metadata dependency impact: permissions, permission set groups, users, fields, layouts, Lightning pages, record types, picklist values, automation, code, integrations, sharing, reports, dashboards, and mobile exposure where relevant.
- Test/validation plan, including Apex coverage expectations and tests for Flow or other testable metadata where Salesforce/project capabilities support them.
- Task list with type (`configuration` or `customization`), explanation, owner/role if known, and estimated execution time.
- Risks, rollback, and assumptions.

At the end of planning, ask whether the user wants an optional PDF containing all planned configuration/customization tasks, task explanations, metadata dependencies, and estimated execution time.

Ask for explicit approval before making file or org metadata changes.

## Phase 3: Implementation

After approval:

- Modify only approved files/metadata.
- Keep patches minimal.
- Preserve existing project conventions.
- Do not broaden scope because adjacent issues are visible.
- If a materially better plan appears during implementation, stop and ask for approval on the revised plan.

At the end of development, before optional handoff files and before validation handoff, generate a `package.xml` containing every metadata component added or modified for the approved request.

- Read `references/testing-and-manifest-guardrails.md`.
- Prefer `scripts/generate_package_manifest.py`.
- Default output: `release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml`.
- Use explicit `--metadata Type:Member` values when git status cannot map all changed metadata.
- Do not include deleted metadata in `package.xml`; plan `destructiveChanges.xml` separately with explicit approval when deletion deploys are required.
- Do not overwrite an existing broad `manifest/package.xml` unless the user approved that exact overwrite.

At the end of development, before validation handoff, read `references/completion-artifacts.md` and ask whether the user wants one or more end-of-development files:

- `release-notes.md`: all metadata added, modified, and removed.
- `technical-specifications.md`: requirements and how they were satisfied with added, modified, and removed metadata.
- `impact-assessment.md`: all pre-existing points modified or impacted.
- `user-testing.md`: Salesforce user tests for the new requirements.
- `manual-procedures.md`: post-deploy manual steps such as configuration records, custom settings, custom metadata records, users, permission set assignments, permission set group assignments, public groups, queues, licenses, named credential secrets, scheduled jobs, and data loads.

Generate only the files the user approves and save them in the user-approved folder. Default to `release-artifacts/<yyyy-mm-dd>-<short-change-name>/`.

## Phase 4: Validation Handoff

Create a compact handoff for a validation subagent:

```text
Validate this Salesforce change.
Requirements:
- ...
Approved plan:
- ...
Changed artifacts:
- ...
Assumptions:
- ...
Commands/tests to run:
- ...
Risks to inspect:
- ...
Return: pass/fail, evidence, defects, missing tests, and recommended next plan if failing.
```

Use an actual subagent when available. If no subagent capability exists in the current platform, run the tests/static checks yourself and save the standalone validation prompt so the user can run it in a separate agent.

Do not pass hidden conclusions to the subagent. Pass requirements, diffs/artifacts, commands, and risks.

## Phase 5: Failure Handling

If validation or tests fail:

1. Summarize the failure evidence.
2. Increment `cycle_count`.
3. Return to Phase 2 with a revised minimal plan.
4. Ask for approval again before modifying.

If approval is not given:

1. Summarize what was rejected or changed.
2. Increment `cycle_count`.
3. Return to Phase 2 and propose a revised plan.

If `cycle_count` exceeds 3, stop and restart from Phase 1. Explain that the previous loop produced too much churn and that requirements need to be clarified again.

## Phase 6: Completion And Push

When validation passes:

- Summarize final requirements and changes.
- List validation evidence and any remaining risk.
- If changes were deployed, ensure `.salesforce-agent-knowledge/history/project-history.md` contains an event with the requirement and all modified metadata; if it does not, append one with `scripts/knowledge_history.py --action deploy` before final reporting.
- Ask whether the user wants a push, and ask which branch should receive it.
- Do not push until the user confirms both intent and branch.
- If the user approves a remote push, use `scripts/git_knowledge_push.py --branch <branch> --requirements <requirement> --metadata <metadata>` so the Knowledge push event is written, committed, and included on the remote branch. If a direct `git push` is used, immediately record the push with `scripts/knowledge_history.py --action git-push` and push the resulting Knowledge commit too.
