# Delivery Methodology

## Loop Contract

Use this workflow for every Salesforce project request: metadata information, implementation, architecture, debugging, bugfix, migration, release, org inspection, package.xml, or review tasks. These phases are mandatory even when no implementation is needed. Track `cycle_count`, starting at 1. A cycle becomes unsuccessful when the user rejects the plan, tests fail, validation fails, or the implemented change no longer matches the approved plan.

Keep every phase token-efficient. A small metadata-information request can use a compact one-paragraph phase output, but it still needs request review, planning/evidence, implementation decision, validation, and completion.

## Compact Information-Only Mode

Use compact information-only mode only when all conditions are true:

- No file changes.
- No org access.
- No metadata inspection.
- No deploy.
- No data read/write.
- No secret exposure.
- No destructive operation.
- No release-sensitive claim requiring current docs.
- No implementation or bugfix requested.
- No project-specific decision.

Compact mode still needs this visible structure:

```text
Request review: <one line>
Evidence: <reference/source used or none>
Answer: <concise answer>
Validation: <how the answer was checked or why no check was needed>
```

Do not use compact mode for implementation, bugfix, refactor, org inspection, metadata inspection, permissions, Apex/LWC/Flow generation, deployment, package.xml, release work, security-sensitive work, destructive actions, secrets, customer data, project-specific decisions, or anything ambiguous/risky.

Every phase must include the tool or command used or planned. If no tool is used, write `Tool/command: none`. For Salesforce org operations, show the exact `sfao`, `scripts/sf_agent_cli.py`, or official `sf` command shape with aliases and secrets redacted.

Maximum: 3 unsuccessful cycles. On the fourth unsuccessful cycle, stop implementation and return to requirement explanation before proposing another plan.

Hard stop for repository agents:

- Do not open raw Salesforce metadata, parse project files, edit files, or run org commands as the first action.
- First show a compact phase-gate response with request review, planned references/Knowledge to consult, whether implementation is required, and whether approval is needed.
- Read `references/routing.md`, task-relevant references, `.salesforce-agent-knowledge/markdown-index.md` or `.salesforce-agent-knowledge/index.json` when present, and project history before inspecting raw metadata.
- Tell the user which reference files, Knowledge indexes, scripts, or Salesforce CLI facade commands are being used before running them.
- If a previous answer skipped these gates, acknowledge the miss and restart from Phase 1 instead of continuing.

## Phase 1: Request Review

Restate:

- User request.
- Salesforce product area and metadata/code area.
- Known target org or environment.
- Expected business outcome.
- Acceptance criteria, if available.
- Whether the request is information-only, bugfix, implementation, architecture, review, or release work.

Ask questions only when needed. Prefer 1-3 high-value questions. Do not ask about details that can be discovered from the repository or safe read-only org inspection.

## Specification Preflight Before Planning

Before Phase 2, pause for a compact specification check when the user asks for new functionality, new metadata, a complex bugfix, or heavy rework and the request does not already state the expected runtime surface:

- Ask whether the solution must cover Salesforce web/desktop, Salesforce mobile, Field Service mobile, or a combination.
- Ask whether the solution must support online use, offline use, or a reduced offline path.
- If Field Service Mobile or offline mobile behavior is in scope, read `references/field-service-mobile-flow.md` before planning.
- If the user cannot decide yet, present the smallest practical scenarios and ask them to choose before implementation planning.

Keep this preflight short. Do not repeat it when the answer is already explicit, when the request is information-only, or when mobile/offline behavior is clearly irrelevant.

## Phase 2: Evidence And Planning

Consult project Knowledge first:

- Read `references/products-packages/index.md` and identify relevant Salesforce products, AppExchange packages, or mobile-development surfaces by brief description.
- Read `references/salesforce-current-version.md` for release-sensitive API, SOAP, Metadata API, LWC API, Apex/Flow version, package, or `sourceApiVersion` planning.
- Read only the matching product/package files under `references/products-packages/products/` or `references/products-packages/packages/`.
- Read `references/metadata-dependencies.md` and use it as the dependency checklist for the plan.
- Read `references/least-privilege-planning.md` and apply least privilege during every planning phase, especially access, sharing, automation, integration, package, or UI exposure decisions.
- Read `references/deletion-guardrails.md` when deletion, uninstall, purge, hard delete, destructive changes, or source delete are possible.
- Read `references/privacy-security.md` when the request touches org access, customer data, personal data, auth, tokens, secrets, integrations, connected apps, named credentials, data exports, Knowledge generation, AI/data activation, analytics, Experience/guest access, or documentation that could expose sensitive information.
- Read `references/field-service-mobile-flow.md` when Field Service Mobile, Field Service mobile flows, technician mobile execution, briefcases, sync, or online/offline behavior can affect the solution.
- Read `references/testing-and-manifest-guardrails.md` when the task touches Apex, Flow, automation, UI metadata, integrations, access, or deployable metadata.
- Read `.salesforce-agent-knowledge/index.md` before planning any modification.
- Read `.salesforce-agent-knowledge/markdown-index.md` when the exact metadata page is not obvious.
- Read the relevant per-metadata Markdown files under `.salesforce-agent-knowledge/metadata/` before opening raw source.
- Read `.salesforce-agent-knowledge/history/project-history.md` for previous deployed changes to the same artifacts.
- Read `.salesforce-agent-knowledge/memory.md` when present for durable facts, decisions, validation lessons, risks, and follow-ups before opening raw source.
- Read the relevant wiki pages under `.salesforce-agent-knowledge/wiki/` only when a higher-level summary is needed.
- If the folder is missing, stale, or the user invokes `/sf-init-project-skill`, run `sfao knowledge init --project-root <project-root>` or `sfao knowledge refresh --project-root <project-root>` before planning, unless the user asked for a quick answer that does not touch the project.
- Use the Knowledge to decide what to inspect next; verify against source metadata files before making changes.
- At completion, update `.salesforce-agent-knowledge/memory.md` with compact durable decisions, lessons, risks, and follow-ups when the task creates reusable project knowledge. For information-only tasks, update memory only when the answer creates a durable project decision or reusable lesson. Never store secrets, auth URLs, tokens, customer data, raw records, screenshots with PII, large logs, or raw diffs.

Always assess multi-country and multi-currency impact before proposing the solution:

- Check whether the org, metadata, package, or requirement spans countries, legal entities, locales, languages, currencies, or region-specific processes.
- For currency-sensitive work, consider CurrencyIsoCode, corporate currency, dated exchange rates, Advanced Currency Management, CPQ price books, quotes, opportunities, reports, integrations, and data loads.
- For country-sensitive work, consider translations, address formats, tax/VAT, compliance, sharing, record types, picklist values, automation branches, validation rules, page layouts, Lightning pages, mobile exposure, and support/sales processes.
- If the project context is unclear, include a multi-country/multi-currency assumption in the plan and ask the user to confirm before implementation.

Inspect the smallest useful surface:

- Changed/touched files, metadata folders, package directories, or manifests.
- Relevant objects, fields, flows, Apex, LWC, permission sets, named credentials, custom metadata, and package dependencies.
- Targeted org data through compact CLI output when needed.
- Current org permissions for affected users/personas before planning access changes, using `scripts/sf_agent_cli.py access-inspect --target-org <alias> --username <user> --sobject <Object>` or a narrow `--where` filter. If the alias or personas are missing, ask before proposing the permission delta.
- Tool/command evidence: list the exact local files read, scripts run, and `sfao`/`scripts/sf_agent_cli.py`/`sf` commands planned or executed. Keep commands compact and redact secrets.

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
- Multi-country/multi-currency impact: org settings and metadata/data behavior that change by country, locale, language, currency, price book, tax, reporting, integration, or compliance scope.
- Specification coverage: web/desktop, Salesforce mobile, Field Service mobile, online behavior, offline behavior, or degraded offline path, with assumptions called out.
- Least-privilege access plan: personas/users inspected, current access evidence, exact proposed permission delta, and why broader permissions are not needed.
- Privacy/security plan: sensitive data or secret exposure, safer alternatives, user consent needed, redaction/retention approach, and exact command/tool scope.
- Test/validation plan, including Apex coverage expectations and tests for Flow or other testable metadata where Salesforce/project capabilities support them.
- Task list with type (`configuration` or `customization`), explanation, owner/role if known, and estimated execution time.
- Risks, rollback, and assumptions.
- Destructive action scope and separate deletion approval needs, if any.
- Implementation decision: `required`, `not required`, or `blocked pending approval/evidence`.
- Evidence that will be used to validate the answer or implementation.
- Tools and commands the agent used or will use in implementation and validation.

Do not invent missing evidence. If a plan depends on an unknown product behavior, metadata dependency, package version, record set, permission scope, user persona, or org state, ask the user for the missing fact or present multiple scenarios with tradeoffs and ask the user to choose.

At the end of planning, ask whether the user wants an optional PDF containing all planned configuration/customization tasks, task explanations, metadata dependencies, and estimated execution time.

Ask for explicit approval before making file or org metadata changes. Ask separately for deletion approval before any destructive data or metadata action; general plan approval is not enough.

## Phase 3: Implementation

After approval:

- Modify only approved files/metadata.
- Keep patches minimal.
- Preserve existing project conventions.
- Do not broaden scope because adjacent issues are visible.
- If a materially better plan appears during implementation, stop and ask for approval on the revised plan.

If implementation is not required, explicitly record `Implementation: not required` with the reason, then continue to Phase 4 validation. Do not create or edit files just to satisfy the workflow.

At the end of development, before optional handoff files and before validation handoff, generate a `package.xml` containing every metadata component added or modified for the approved request.

- Read `references/testing-and-manifest-guardrails.md`.
- Prefer `scripts/generate_package_manifest.py`.
- Default output: `release-artifacts/<yyyy-mm-dd>-<short-change-name>/package.xml`.
- Use explicit `--metadata Type:Member` values when git status cannot map all changed metadata.
- Do not include deleted metadata in `package.xml`; plan `destructiveChanges.xml` separately with explicit approval when deletion deploys are required.
- For destructive changes, follow `references/deletion-guardrails.md`; validation or preview is not approval to execute deletion.
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

For information-only metadata requests, validation means re-checking the cited project Knowledge, metadata files, official documentation, or compact org inspection result before final response. Include the evidence paths or commands checked.

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
- If no implementation was required, summarize the validated answer and evidence instead of changes.
- List validation evidence and any remaining risk.
- If changes were deployed, ensure `.salesforce-agent-knowledge/history/project-history.md` contains an event with the requirement and all modified metadata; if it does not, append one with `scripts/knowledge_history.py --action deploy` before final reporting.
- Ask whether the user wants a push, and ask which branch should receive it.
- Do not push until the user confirms both intent and branch.
- If the user approves a remote push, use `scripts/git_knowledge_push.py --branch <branch> --requirements <requirement> --metadata <metadata>` so the Knowledge push event is written, committed, and included on the remote branch. If a direct `git push` is used, immediately record the push with `scripts/knowledge_history.py --action git-push` and push the resulting Knowledge commit too.
