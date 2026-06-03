# Salesforce Products And Packages Index

Before planning, identify likely products and packages from the user's request, project metadata, installed packages, object names, namespaces, app names, and brief descriptions below. Then read `references/salesforce-current-version.md`, only the matching product/package files, and `references/metadata-dependencies.md`.

Version rule: current Salesforce API/SOAP/Metadata/LWC guidance lives in `references/salesforce-current-version.md`. Managed package versions are target-org-specific; ask for the org alias and inspect installed packages before assuming package object names, namespace behavior, or feature availability.

## Product Signals

| Product | Brief signal | File |
|---|---|---|
| Agentforce | AI agents, topics, actions, instructions, copilots, agent lifecycle. | `products/agentforce.md` |
| Sales Cloud | Leads, opportunities, accounts, forecasting, pipeline, sales productivity. | `products/sales-cloud.md` |
| Service Cloud | Cases, support, entitlement, knowledge, service console, omni-channel. | `products/service-cloud.md` |
| Marketing Cloud | Journeys, campaigns, audience activation, email, SMS, marketing automation. | `products/marketing-cloud.md` |
| Commerce Cloud | Digital commerce, carts, storefronts, pricing, checkout, orders. | `products/commerce-cloud.md` |
| Data 360 / Data Cloud | Data unification, identity resolution, calculated insights, segments. | `products/data-360-data-cloud.md` |
| Salesforce Platform & Data | Custom apps, metadata, automation, security, APIs, data model. | `products/salesforce-platform-data.md` |
| Tableau | Analytics, dashboards, visual exploration, embedded analytics. | `products/tableau.md` |
| MuleSoft | APIs, integration, Anypoint, connectors, orchestration. | `products/mulesoft.md` |
| Slack | Collaboration, Salesforce channels, workflows, approvals in Slack. | `products/slack.md` |
| Industry Clouds | Industry data models, packaged processes, regulatory workflows. | `products/industry-clouds.md` |
| Experience Cloud | Portals, partner/customer sites, digital experiences, guest access. | `products/experience-cloud.md` |
| Einstein AI | Predictive/generative AI, scoring, recommendations, AI features. | `products/einstein-ai.md` |
| Net Zero Cloud | Sustainability, emissions accounting, ESG reporting. | `products/net-zero-cloud.md` |
| Partner / PRM | Partner lifecycle, channel sales, deal registration, partner portal. | `products/partner-prm.md` |
| Success Plans / Professional Services | Adoption, support, enablement, governance, delivery services. | `products/success-plans-professional-services.md` |
| Salesforce CPQ | Quotes, quote lines, product rules, price rules, contracts, renewals. | `products/salesforce-cpq.md` |
| Salesforce Field Service | Work orders, service appointments, resources, territories, dispatch, mobile field work. | `products/salesforce-field-service.md` |
| Mobile Development | Salesforce mobile app, mobile-ready LWC, offline, Mobile SDK. | `products/mobile-development.md` |

## Package Signals

| Package | Brief signal | File |
|---|---|---|
| Salesforce Adoption Dashboards | User login/adoption dashboard package from Salesforce Labs. | `packages/salesforce-adoption-dashboards.md` |
| Docusign eSignature for Salesforce | Send, sign, track, and store agreements from Salesforce. | `packages/docusign-esignature-for-salesforce.md` |
| Declarative Lookup Rollup Summaries (DLRS) | Declarative rollups across lookup relationships. | `packages/declarative-lookup-rollup-summaries.md` |
| Org Check | Org technical debt and configuration analysis. | `packages/org-check.md` |
| Query Studio for Marketing Cloud | SQL query execution in Marketing Cloud. | `packages/query-studio-for-marketing-cloud.md` |
| Zoom for Lightning | Zoom meeting/phone integration in Salesforce. | `packages/zoom-for-lightning.md` |
| FieldSpy | Field usage analysis and cleanup support. | `packages/fieldspy-field-usage-report.md` |
| User Access and Permissions Assistant | Permission analysis and reporting. | `packages/user-access-and-permissions-assistant.md` |
| LinkedIn Sales Navigator for Salesforce | LinkedIn account/contact insights inside Salesforce. | `packages/linkedin-sales-navigator-for-salesforce.md` |
| Box Intelligent Content Management | File collaboration, content workflows, e-sign related work. | `packages/box-intelligent-content-management.md` |
| Advanced Approvals | Salesforce CPQ advanced approval rules, chains, approvers, and quote approvals. | `packages/advanced-approvals.md` |
