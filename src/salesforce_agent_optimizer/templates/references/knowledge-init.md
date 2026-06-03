# `/sf-init-project-skill` Metadata Knowledge

## Purpose

Use `/sf-init-project-skill` to build or refresh a compact indexed Knowledge layer for a Salesforce project. The Knowledge is inspired by Andrej Karpathy's LLM Wiki pattern: keep raw sources as source of truth, compile a persistent Markdown wiki, maintain an index and log, and query the wiki before re-reading raw sources from scratch.

## When To Run

- The user invokes `/sf-init-project-skill`.
- The Salesforce project has no `.salesforce-agent-knowledge/` folder.
- The Knowledge is stale after metadata changes, package changes, branch switches, or org refreshes.
- The user asks to refresh or enrich the metadata inspection.

## Command

Run from the skill folder or call the script by absolute path:

```bash
python scripts/sf_knowledge_init.py --project-root <salesforce-project-root> --refresh
```

Optional:

```bash
python scripts/sf_knowledge_init.py --project-root <salesforce-project-root> --metadata-types ApexClass,Flow,CustomObject
python scripts/sf_knowledge_init.py --project-root <salesforce-project-root> --knowledge-dir .my-salesforce-knowledge
```

## Generated Folder

```text
.salesforce-agent-knowledge/
  AGENTS.md
  config.json
  index.json
  index.md
  markdown-index.md
  log.md
  sources.json
  history/
    project-history.md
  metadata/
    ApexClass/
      MyClass-<hash>.md
    CustomObject/
      Account-<hash>.md
  wiki/
    overview.md
    metadata-catalog.md
    data-model.md
    automation.md
    apex.md
    lwc.md
    security.md
    integrations.md
```

## Editable Metadata List

The user can edit `.salesforce-agent-knowledge/config.json` to add or remove metadata types and path patterns. Preserve user edits on refresh. If a project has special metadata directories, managed package conventions, or generated source folders, add them there.

## Per-Metadata Markdown Format

`/sf-init-project-skill` creates one Markdown file for each indexed metadata artifact under `.salesforce-agent-knowledge/metadata/<MetadataType>/`.

Every metadata page uses the same compact structure:

- `# <MetadataType>: <Name>`
- `## File`: Knowledge file path, source file path, generated timestamp.
- `## Brief Description`: short agent-readable description.
- `## Essential Content`: only the fields that matter for planning.
- `## Links`: index, markdown index, metadata catalog, and related metadata pages.
- `## Agent Notes`: reminders to verify source before editing.

This keeps retrieval cheap: agents should open the metadata page first, then source files only when needed.

## Markdown Index

`markdown-index.md` lists every Markdown file in the Knowledge folder. Use it when the agent needs a direct jump table across metadata pages, wiki summaries, and history.

## Project History

`history/project-history.md` records compact change, deploy, and remote-branch push history. Each history row links to a detailed event file under `history/events/`.

Every history event must include:

- the requirement or user request that caused the change;
- every metadata artifact modified, using names such as `ApexClass:AccountService` or `CustomField:Account.Priority__c`;
- deploy target org or push remote/branch when applicable;
- command/result summary.

The agent CLI appends deploy events after successful `deploy-start` operations. Remote branch pushes must use `scripts/git_knowledge_push.py`, which records and commits the push history before pushing so the remote branch contains the Knowledge update. If a direct `git push` is used, record with `scripts/knowledge_history.py --action git-push`, commit the Knowledge history, and push that commit too.

Agents must consult this history before planning changes that touch previously deployed artifacts.

## Query Rule Before Modification

Before planning or modifying:

1. Read `.salesforce-agent-knowledge/index.md`.
2. Read `.salesforce-agent-knowledge/markdown-index.md` when the exact metadata page is not obvious.
3. Read the relevant metadata page under `.salesforce-agent-knowledge/metadata/`.
4. Read `.salesforce-agent-knowledge/history/project-history.md` for prior deployed changes.
5. Open source metadata files referenced by the Knowledge before editing.
6. If the Knowledge conflicts with source files, trust source files and run `/sf-init-project-skill` after the change.

## Knowledge Principles

- Source-first: do not copy raw metadata into the Knowledge unless explicitly needed; store paths, hashes, summaries, and relationships.
- Compiled: keep summaries, cross-references, counts, and risks in Markdown pages so future agents do not re-derive context.
- Indexed: keep `index.md`, `markdown-index.md`, and `index.json` for agent reading and tool/search workflows.
- Logged: append refresh/query events to `log.md`; append change, deploy, and remote push events to `history/project-history.md` and `history/events/`.
- Refreshable: `/sf-init-project-skill` can be safely run again after metadata changes.
- Minimal context: read the index first, then only the wiki pages and source files relevant to the user request.
