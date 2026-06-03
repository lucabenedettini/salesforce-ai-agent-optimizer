# `/sf-version-update-skill`

Refresh Salesforce release, API, SOAP API, Metadata API, LWC API, product, and managed package version context for this skill.

Steps:

1. Read `references/version-update.md`.
2. Search online in official Salesforce sources only and identify the latest production Salesforce release and current API versions.
3. Capture technical and functional changes that affect agents, metadata, Apex, Flow, LWC, integrations, packaging, Data Cloud, Agentforce, and package planning.
4. Run `sfao version-context scaffold`, then `sfao version-context update`.
5. Update `references/official-salesforce-sources.md`, `references/products-packages/index.md`, product/package files, README, and wiki pages only where version-sensitive information changed.
6. For managed packages, do not invent a global latest installed version. Ask for the target org alias and inspect installed packages when org-specific package version evidence is needed.
7. Run `sfao version-context validate`, then validation, and summarize official sources, files updated, assumptions, and any target-org package version checks still required.
