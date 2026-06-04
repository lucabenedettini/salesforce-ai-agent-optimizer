# Field Service Mobile And Mobile Flow

Use this reference when the request mentions Field Service Mobile, Field Service mobile flows, technician mobile work, mobile offline behavior, briefcases, sync, service reports, work orders, service appointments, or mobile-only Field Service defects.

## Purpose

Field Service Mobile work must be planned as a mobile execution surface, not as a smaller copy of desktop Salesforce. Before planning, confirm whether the solution must support Salesforce web/desktop, Salesforce mobile, Field Service mobile, online use, offline use, or a degraded offline mode.

## Specification Preflight

For new functionality, new metadata, complex bugfixes, or heavy rework, ask these questions before planning when the answer is not already explicit:

- Must this work in Salesforce web/desktop, Salesforce mobile, Field Service mobile, or all of them?
- Must the same process work online, offline, or with a reduced offline path?

Keep the question compact. If the user cannot answer yet, present scenarios with tradeoffs and plan the safest configuration-first option.

## Planning Checklist

- Read `references/products-packages/products/salesforce-field-service.md`.
- Read `references/products-packages/products/mobile-development.md`.
- Read `references/metadata-dependencies.md` for object, field, layout, Lightning page, permission, record type, picklist, Flow, and mobile exposure dependencies.
- Read `references/least-privilege-planning.md`; verify technician, dispatcher, back-office, and integration user access with the target org alias when access changes are involved.
- Read `references/salesforce-current-version.md`; use official Salesforce docs when mobile/offline behavior is release-sensitive or unclear.
- Inspect Field Service package/version and mobile configuration only through compact read-only commands until the user approves implementation.

## Best Practices

- Prefer configuration, Field Service settings, mobile app configuration, briefcases, permissions, layouts, actions, and Field Service mobile flows before Apex or custom mobile code.
- Design the offline data shape first: objects, fields, related records, record counts, sync direction, conflict behavior, and device performance.
- Keep mobile flows short, deterministic, and tolerant of cached data.
- Use data fields that are available offline for branching; avoid depending on metadata that briefcases cannot prime.
- Separate desktop-only and mobile/offline logic when the same Flow would require unsupported mobile behavior.
- Validate on a real device or supported mobile test path before release; desktop Flow success is not enough.
- For multi-country or multi-currency Field Service, verify locale, language, address, territory, tax, service report, currency, price book, inventory, and compliance differences before planning.

## Field Service Mobile Flow Limits To Check

- CRM Core App screen flows are not supported in the Field Service mobile app; use Field Service mobile flows for Field Service mobile execution.
- Offline Flow behavior can differ from online behavior because the app runs locally and syncs later.
- Record-triggered Flow and validation errors may surface after sync as upload errors, not during the mobile flow screen execution.
- Record Type based logic is unsafe for offline Field Service mobile flows unless the specific record metadata is already cached; prefer primed data fields for offline branching.
- Compound fields cannot be used directly in mobile flows; plan with component fields such as city, country, street, latitude, or longitude.
- Some formula functions, operators, rich text behavior, paused flows, email alerts, conditional visibility, and `In`/`Not In` operators have mobile/offline limitations.
- New records created locally can miss server-generated values, such as auto numbers, until sync completes.
- Empty assignment values can behave differently on mobile than in Flow Builder on web.
- Each create, update, or delete action in a Field Service mobile flow can be processed as a separate transaction; do not assume desktop-style transactional grouping.
- Some service report, inventory, related list, and briefcase behaviors have offline-specific limits; verify the exact feature before promising parity.

## Validation

- Re-check the planned mobile surface: web/desktop, Salesforce mobile, Field Service mobile.
- Re-check online/offline expectations and any degraded offline behavior.
- Validate data priming, sync, conflict handling, and upload error paths when offline is in scope.
- Validate permissions with least privilege for each persona.
- Validate Flow behavior on the mobile target, not only in desktop Flow Builder.
- Include `package.xml` for added or modified metadata before validation handoff.

## Official Sources

- Salesforce Help: Field Service Mobile Offline Considerations: https://help.salesforce.com/s/articleView?id=service.mfs_offline_considerations.htm&language=en_US&type=5
- Salesforce Help: Get Started with Field Service Mobile Offline: https://help.salesforce.com/s/articleView?id=service.mfs_offline_get_started.htm&language=en_US&type=5
- Salesforce Help: Field Service Mobile App Limitations: https://help.salesforce.com/s/articleView?id=sf.mfs_limits.htm&language=en_US&type=5
- Salesforce Help: Field Service Mobile Record Type logic in offline Flow configurations: https://help.salesforce.com/s/articleView?id=000395466&language=en_US&type=1
- Salesforce Help: Field Service Mobile Flow record-triggered Flow error behavior: https://help.salesforce.com/s/articleView?id=005232956&language=en_US&type=1
- Salesforce Developers: Mobile and Offline Developer Guide: https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/mobile_offline.pdf
