# Memory And Specialized Guidance

Salesforce Agent Optimizer uses three layers of local planning context:

- Knowledge indexes: compact generated metadata summaries.
- Project history: chronological deploy/push/change events.
- Project memory: curated durable facts, decisions, validation lessons, risks, and follow-ups.

## Project Memory

Memory lives at:

```text
.salesforce-agent-knowledge/memory.md
```

It is created by:

```bash
sfao knowledge init --project-root .
sfao memory init --project-root .
```

Add compact entries:

```bash
sfao memory add --project-root . --task-type bugfix --summary "Fixed Work Order status rule" --metadata Flow:Work_Order_Status_Check --validation "Flow test reviewed"
```

Compact deterministically:

```bash
sfao memory compact --project-root . --max-bytes 60000
sfao memory doctor --project-root .
```

Memory must not store secrets, auth URLs, tokens, customer data, raw records, screenshots with
PII, large logs, or raw diffs.

## Knowledge Scan Scope

When `sfdx-project.json` contains valid `packageDirectories`, SFAO scans those package
directories by default. This avoids expensive monorepo-wide scans.

Force a broad scan only when needed:

```bash
sfao knowledge init --project-root . --scan-root
sfao knowledge refresh --project-root . --scan-root
```

## Specialized Guidance

The `references/specialized-guidance/` folder contains small task-specific checklists:

- `apex.md`
- `lwc.md`
- `flow.md`
- `soql.md`
- `deploy.md`
- `data-operations.md`

Agents should load only the relevant file selected by `references/routing.md`.

## External Skills

External Salesforce skills may be consulted only when already installed and relevant. They are
optional specialist references. They must not bypass SFAO safety, org alias rules, production
read-only policy, deletion approval, secret approval, Knowledge-first planning, or package.xml
requirements.

## Iterative Tool Workflows

Repeated tool workflows need:

- a clear completion condition;
- a small iteration cap, default 10;
- truthful tool-result reporting;
- a stop when risk, ambiguity, cost, or unavailable tooling appears.
