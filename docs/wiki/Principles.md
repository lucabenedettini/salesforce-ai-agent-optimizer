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

## Human Approval And Validation

Agents must restate the request, ask focused questions only when needed, plan before changing, ask for approval, validate with tests or a subagent when available, and retry failed plans no more than three times before returning to requirements.

## Handoff Completeness

At the end of development, agents should ask whether the user wants release notes, technical specifications, impact assessment, user testing, and manual procedure files. These artifacts make Salesforce changes easier to review, deploy, test, audit, and operate after release.
