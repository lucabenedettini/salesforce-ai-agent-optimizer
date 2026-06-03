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

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
