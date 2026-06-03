# Architecture And Solution Design

## Decision Order

1. Confirm business capability, users, data ownership, volumes, compliance, and release constraints.
2. Read `references/salesforce-current-version.md` when API, SOAP, Metadata API, LWC API, package, or release behavior can affect the design.
3. Check whether standard Salesforce capability, setup configuration, Flow, OmniStudio, Experience Cloud, Service/Sales Cloud feature, Data Cloud, or a managed package can satisfy the need.
4. Use custom code only when configuration cannot meet behavior, performance, transactionality, UX, integration, or governance requirements.
5. Prefer reversible decisions and metadata that admins can reason about.

## Well-Architected Checks

Trusted:
- Enforce least privilege with permission sets, permission set groups, sharing, restriction rules, scopes, named credentials, and secure guest access.
- Avoid exposing sensitive fields through Apex, LWC, reports, Experience Cloud, or integration payloads.
- Include auditability, monitoring, rollback, backup, and data retention.

Easy:
- Reduce user clicks, cognitive load, duplicate data entry, and hidden automation side effects.
- Prefer clear ownership, documented automation entry points, and predictable deployment.
- Keep support paths simple for admins and service teams.

Adaptable:
- Avoid hard-coded IDs, profile dependencies, object-specific assumptions, and brittle integration mappings.
- Use custom metadata, custom permissions, named credentials, platform events, and invocable actions where they reduce future change cost.
- Design around expected data volumes, LDV, API limits, async limits, and release cadence.

## Output Shape

For a design, return:

- Recommendation: concise chosen path.
- Products/packages: detected products/packages and reference files read.
- Why configuration first: what standard/declarative features cover.
- Custom gap: only if custom work remains.
- Architecture: data, automation, security, integration, deployment, mobile exposure if relevant.
- Metadata dependencies: access, data model, UI, automation, code, integrations, sharing, analytics, and package dependencies.
- Risks and limits: concrete Salesforce constraints.
- Validation: how to prove it in sandbox and production.

## Red Flags

- Apex trigger requested before Flow/configuration has been evaluated.
- Multiple automation types on the same object without an ordering strategy.
- Profiles used as the primary access-control artifact for new capability.
- Hard-coded org IDs, record type IDs, queue IDs, pricebook IDs, or endpoints.
- Large data operations without selectivity, async design, or retry/monitoring plan.
- Integration authentication without named credentials or external credentials.
- Planning a field, record type, picklist, layout, Lightning page, permission set, or package change as if it were isolated metadata.
