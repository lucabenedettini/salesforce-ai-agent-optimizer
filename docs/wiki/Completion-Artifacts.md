# Completion Artifacts

At the end of development, the agent asks whether to generate optional handoff files.

## Files

- `release-notes.md`: metadata added, modified, and removed.
- `technical-specifications.md`: requirements and how they were satisfied with metadata/configuration/customization.
- `impact-assessment.md`: pre-existing Salesforce areas modified or impacted.
- `user-testing.md`: Salesforce UI tests users can run for the new requirements.
- `manual-procedures.md`: manual post-deploy steps such as configuration records, custom settings, custom metadata records, users, permission set assignments, permission set group assignments, public groups, queues, licenses, named credential secrets, scheduled jobs, and data loads.

## Default Folder

```text
release-artifacts/<yyyy-mm-dd>-<short-change-name>/
```

## Source Of Truth

The canonical template rules live in `references/completion-artifacts.md`.
