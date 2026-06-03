# Project Principles

## Salesforce Optimization

Use Salesforce as a metadata-driven platform first. Prefer standard product capabilities, setup configuration, Flow, permission sets, UI API, Lightning Data Service, named credentials, managed packages, and Salesforce Well-Architected guidance before proposing custom Apex, LWC, triggers, or bespoke integrations.

## Token Optimization

AI agents should spend context on decisions, not noise. The skill uses progressive disclosure, local Knowledge, Markdown indexes, compact CLI output, `--select` filters, bounded JSON, redaction, and minimal source inspection to reduce token usage.

## LLM Wiki Pattern

The Knowledge system follows the LLM Wiki idea popularized by Andrej Karpathy: raw source files remain the source of truth, while a compact Markdown wiki stores summaries, links, hashes, indexes, history, and navigation optimized for repeated agent work.

## Printing Press CLI Pattern

The Salesforce CLI facade follows the `cli-printing-press` style: agent-native commands, compact output, dry-run support, explicit target org aliases, safe defaults, and predictable wrappers around official Salesforce CLI operations.

## Minimal Patch Discipline

Agents should change the fewest files and metadata artifacts needed to satisfy the approved requirement. Broad refactors require explicit justification and approval.

## Dependency-Aware Planning

Salesforce metadata is a graph. Plans must account for permission sets, permission set groups, users, fields, layouts, Lightning pages, record types, picklist values, automation, code, integrations, sharing, analytics, packages, and mobile exposure.

## Least-Privilege Planning

Every plan must apply least privilege and grant only the minimum access needed for the approved business task. Before proposing permission changes, agents inspect current target-org access for affected users/personas with `scripts/sf_agent_cli.py access-inspect` or equivalent narrow SOQL. If the correct permission boundary is unclear, agents ask the user or present scoped scenarios instead of guessing.

## Version Freshness

Salesforce release, API, SOAP API, Metadata API, LWC API, and managed package versions affect behavior. Agents must use current official Salesforce version context, refresh it with `/sf-version-update-skill` when stale, and verify managed package versions in the target org.

## Destructive Safety

Agents must never delete Salesforce data or metadata automatically. Destructive operations require separate explicit approval for the exact target org and scope. Missing facts must be resolved by asking the user or offering scenarios, not by guessing.

## Human Approval And Validation

Agents must restate the request, ask focused questions only when needed, plan before changing, ask for approval, validate with tests or a subagent when available, and retry failed plans no more than three times before returning to requirements.

## Testable Metadata Discipline

Agents must test what Salesforce and the project make testable. Changed Apex requires at least 80% coverage and should target 90%-100%; Flow and other metadata with supported automated or meaningful manual validation must be covered before final delivery.

## Manifest Discipline

Every implemented request must produce a `package.xml` for added or modified metadata before validation handoff. This makes deployment scope explicit and keeps review focused on the approved change.

## Handoff Completeness

At the end of development, agents should ask whether the user wants release notes, technical specifications, impact assessment, user testing, and manual procedure files. These artifacts make Salesforce changes easier to review, deploy, test, audit, and operate after release.
