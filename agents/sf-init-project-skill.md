# `/sf-init-project-skill`

Inspect the current Salesforce project metadata and build or refresh the local indexed Knowledge folder.

Steps:

1. Identify the Salesforce project root.
2. Run `sfao knowledge init --project-root <project-root>` or `sfao knowledge refresh --project-root <project-root>`.
3. Confirm `.salesforce-agent-knowledge/index.md`, `markdown-index.md`, `index.json`, `sources.json`, `log.md`, `history/project-history.md`, `metadata/`, and `wiki/` were created.
4. Tell the user the Knowledge was refreshed and mention that `.salesforce-agent-knowledge/config.json` can be edited to add project-specific metadata types.

Before future modifications, read `.salesforce-agent-knowledge/index.md`, the relevant metadata Markdown page, and `history/project-history.md` first. History events must capture the requirement, all modified metadata, deploys, and remote branch pushes.
