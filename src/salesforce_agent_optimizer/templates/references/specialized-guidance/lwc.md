# LWC Guidance

Read this for Lightning Web Components, UI exposure, client-side data access, and UX changes.

## Non-Negotiable Checks

- Prefer LDS, UI API, wire adapters, and base Lightning components where possible.
- Use Apex only when standard UI/data APIs cannot meet the requirement.
- Validate `.js-meta.xml` targets, exposure, objects, pages, and form factors.
- Preserve accessibility: labels, keyboard use, focus, semantic markup, and error state.
- Use SLDS classes and styling hooks before hardcoded colors or layout hacks.
- Avoid rerender loops, broad reactive state, and unnecessary server calls.
- Keep event contracts explicit and documented in component boundaries.
- Do not expose secrets, private data, or unauthorized fields in client code.

## Minimal Planning Evidence

- Knowledge page for the component and related Apex/classes.
- Target pages, objects, app builders, Lightning pages, mobile surface, and permissions.
- Data access path: LDS/UI API, GraphQL/UI API, Apex, or integration.
- Browser/mobile behavior and offline impact when applicable.

## Preferred Approach

- Configuration and Lightning App Builder first.
- Base components before custom markup.
- LDS/UI API before Apex.
- Small component changes before new component trees.

## Validation Expectations

- Run existing Jest tests when the project uses Jest or the user asks for it.
- Validate local lint/build/test commands when available.
- Verify target exposure and permissions.
- For mobile, check form factor and offline constraints.

## SFAO Command Hints

- `sfao command search "schema describe" --toolset schema`
- `sfao soql build --sobject Account --field Id --field Name --limit 10`

## Output Hint

Name the UI surface, data access method, and validation command in the plan.
