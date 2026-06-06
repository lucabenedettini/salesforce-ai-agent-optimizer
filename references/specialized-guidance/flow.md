# Flow Guidance

## When To Read

Read this file only when the current task involves Screen Flow, Autolaunched Flow, Record-Triggered Flow, Scheduled Flow, Field Service Mobile Flow, Flow calling Apex, Flow deployment, Flow activation, or Flow fault-path issues.

## Combine With Existing References

- `references/testing-and-manifest-guardrails.md` for package.xml, validation, and deploy readiness.
- `references/metadata-dependencies.md` for related metadata, object, field, permission, and automation dependencies.
- `references/least-privilege-planning.md` for access and permission impact.
- `references/field-service-mobile-flow.md` only when Field Service Mobile or offline behavior is involved.

## Non-Negotiable Checks

- Prefer Flow/configuration before Apex when suitable.
- Define Flow type and runtime surface.
- Define entry criteria and avoid broad triggers that run unnecessarily.
- Consider bulk, recursion, order-of-execution, and record-trigger interaction.
- Add or preserve fault paths for record operations, callouts, actions, and Apex.
- Check permissions, field access, validation rules, duplicate rules, approvals, and Apex dependencies.
- Keep activation/deployment strategy explicit.
- Consider mobile/offline behavior when Field Service or mobile is involved.
- Identify package.xml impact.

## Minimal Planning Evidence

- Relevant Knowledge Flow page and project memory/history.
- Local Flow metadata, trigger object, fields, record types, and picklists.
- Running user/context and permission assumptions.
- Called subflows, Apex, actions, prompts, integrations, or email alerts.
- Mobile/offline constraints when relevant.
- Validation target and activation/deployment plan.

## Preferred Approach

- Keep Flow simple, readable, and narrowly scoped.
- Prefer before-save Flow for simple same-record field updates.
- Avoid mixing unrelated responsibilities in one Flow.
- Use subflows only when reuse or readability improves.
- Use Custom Metadata for variable business rules.
- Do not manually edit XML broadly unless fixing targeted validation/deployment errors.
- Deploy safely and activate deliberately.

## Validation Expectations

- Validate metadata and entry criteria.
- Review permissions/FLS and fault paths.
- Run Flow tests when present or feasible; otherwise define a manual smoke path.
- Validate deploy before deploy start.
- Document activation/post-deploy steps.
- Update package.xml for changed Flow metadata.

## SFAO Command Hints

- `sfao command search "deploy validate" --toolset deploy`
- `python scripts/sf_agent_cli.py deploy-validate --target-org <alias> --source-dir force-app`

## Mini-Rubric

- Flow type and runtime surface clear: yes/no
- Entry criteria clear: yes/no
- Fault path considered: yes/no
- Permissions/FLS considered: yes/no
- Activation/deployment strategy clear: yes/no
- Mobile/offline considered when relevant: yes/no
- package.xml impact clear: yes/no
- Memory update needed or handled: yes/no

## Output Hint

State activation plan separately from metadata deployment.
