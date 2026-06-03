# Nome del prodotto/pacchetto: Salesforce Platform & Data

## Breve descrizione sintetica
Piattaforma per custom app, metadata, automation, security, integration, APIs, data model and low-code/pro-code development.

## Oggetti principali
- CustomObject, CustomField, RecordType, GlobalValueSet, Layout, FlexiPage.
- Flow, ApexClass, ApexTrigger, LightningComponentBundle, PermissionSet.
- NamedCredential, ExternalCredential, ConnectedApp, CustomMetadata, PlatformEvent.

## Funzionalita principali
- Data modeling, declarative automation and custom UI.
- Apex, LWC, API integration and event-driven architecture.
- Security, sharing, deployment and governance.

## Configurazioni principali
- Objects, fields, record types, layouts, Lightning pages, apps and tabs.
- Flows, validation rules, duplicate rules, sharing and permission sets.
- Named credentials, connected apps, platform events, custom metadata.
- CI/CD, source tracking, tests and deployment validation.

## Best practice
- Prefer standard metadata and Flow before Apex when maintainable.
- Keep source metadata and Knowledge synchronized.
- Plan dependency order before deployment.
- Test CRUD/FLS, sharing, limits and rollback for every custom change.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. Verificare la release della target org e la disponibilita' effettiva delle funzionalita'; per prodotti distribuiti anche come managed package o add-on, verificare la versione installata nella org quando rilevante.
