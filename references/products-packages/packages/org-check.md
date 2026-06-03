# Nome del prodotto/pacchetto: Org Check

## Breve descrizione sintetica
Salesforce Labs package for analyzing org configuration, technical debt and selected metadata risks.

## Oggetti principali
- Metadata records and setup objects inspected by the package.
- Managed package objects for scan results and configuration.
- User, PermissionSet, Profile, ApexClass, Flow, CustomObject where analyzed.

## Funzionalita principali
- Org health and technical-debt analysis.
- Metadata inventory and risk signals.
- Admin-facing reports or screens for remediation planning.

## Configurazioni principali
- Package permission sets and app access.
- Scan options, result storage and visibility.
- Report/dashboard access where included.

## Best practice
- Treat findings as planning input and verify against source metadata.
- Do not apply remediation blindly from generated results.
- Use results to prioritize cleanup in small, testable patches.
- Re-run after major refactors or package changes.
