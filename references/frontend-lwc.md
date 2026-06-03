# Frontend LWC Guidelines

## Data Access Order

1. Lightning base components and record forms.
2. Lightning Data Service and `lightning/ui*Api` wire adapters.
3. GraphQL wire adapter for appropriate multi-object read use cases.
4. Apex only when the UI needs custom transaction logic, complex server-side aggregation, callouts, or behavior unavailable through UI API/LDS.

## Component Design

- Keep components focused and composable.
- Use SLDS and Lightning base components before custom markup.
- Preserve accessibility: labels, keyboard navigation, focus states, assistive text, and semantic structure.
- Avoid imperative DOM manipulation unless a documented LWC pattern requires it.
- Minimize tracked state and derived state; compute values where clear.
- Avoid unnecessary rerenders, broad wire refreshes, and large client-side transforms.
- Treat wire/Apex data as immutable; clone before mutation.
- Handle loading, empty, error, and permission-denied states.

## Security And Performance

- Assume Lightning Web Security is active.
- Avoid unsafe third-party scripts; justify and isolate any library.
- Use cacheable Apex only for read-only methods.
- Prefer pagination, lazy loading, and narrow fields for large datasets.
- Avoid exposing fields or records the user cannot access.

## Tests

- Run LWC Jest/component tests when the project has them.
- If no frontend test framework exists, include manual UI, accessibility, permission, and regression checks in the validation handoff.
- Include changed LWC bundles in the generated `package.xml`.

## Review Heuristics

Revise components that:

- Call Apex for simple record CRUD that LDS can handle.
- Hide errors in console-only logging.
- Depend on DOM selectors across component boundaries.
- Duplicate SLDS/base component functionality with fragile custom UI.
- Fetch more fields or records than the UI renders.
