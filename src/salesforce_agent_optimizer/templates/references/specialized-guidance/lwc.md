# LWC Guidance

## When To Read

Read this file only when the current task involves LWC bundles, Lightning UI, LDS/UI API, Apex-backed UI, GraphQL wire use, Lightning Message Service, Flow screen components, or App Builder/Experience/Record Page exposure.

## Combine With Existing References

- `references/frontend-lwc.md` for project frontend delivery guidance.
- `references/testing-and-manifest-guardrails.md` for package.xml and validation.
- `references/least-privilege-planning.md` for permission and access impact.
- `references/privacy-security.md` when UI state, logs, exports, or customer data are involved.

## Non-Negotiable Checks

- Prefer base Lightning components, LDS, UI API, and platform patterns before custom code.
- Use Apex only when LDS/UI API/GraphQL cannot satisfy the requirement.
- Respect FLS/sharing through platform services and backend behavior.
- Use SLDS-compatible styling; avoid hardcoded colors and layout assumptions.
- Preserve accessibility: labels, keyboard support, focus behavior, semantic markup, and ARIA when needed.
- Avoid rerender loops in lifecycle hooks and unnecessary server calls.
- Keep event contracts explicit.
- Do not expose sensitive data in client state, browser logs, URLs, or markup.
- Validate `.js-meta.xml` target exposure and package.xml impact.

## Minimal Planning Evidence

- Relevant Knowledge page and project memory/history.
- Component bundle files and `.js-meta.xml`.
- Target surface: record page, app page, Experience Cloud, Flow screen, mobile, or utility.
- Data source: LDS/UI API, GraphQL/UI API, Apex, Flow, message channel, or integration.
- Permission assumptions, accessibility needs, and state requirements.

## Preferred Approach

- Use Lightning App Builder/configuration before code when sufficient.
- Use LDS/base components for record-centric UI.
- Use wire adapters for reactive reads and imperative calls for explicit actions.
- Keep components small and composable.
- Push business logic to Apex only when platform services are insufficient.
- Do not create custom UI controls when platform components are enough.

## Validation Expectations

- Confirm the component compiles with the project build/lint path when available.
- Verify `.js-meta.xml` targets, objects, pages, and form factors.
- Run Jest only when the project already uses it or the task requires it.
- Include a manual UI smoke path and accessibility check.
- Update package.xml when metadata changed.

## SFAO Command Hints

- `sfao command search "schema describe" --toolset schema`
- `sfao soql build --object Account --fields Id,Name --limit 10`

## Mini-Rubric

- LDS/UI API/base components considered: yes/no
- Apex use justified: yes/no
- Accessibility considered: yes/no
- `.js-meta.xml` exposure checked: yes/no
- Event/data contract clear: yes/no
- Sensitive data exposure checked: yes/no
- Validation path clear: yes/no

## Output Hint

Name the UI surface, data access method, permission impact, and validation path in the plan.
