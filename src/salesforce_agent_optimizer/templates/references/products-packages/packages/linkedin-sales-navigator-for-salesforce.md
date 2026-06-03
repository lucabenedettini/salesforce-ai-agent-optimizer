# Nome del prodotto/pacchetto: LinkedIn Sales Navigator for Salesforce

## Breve descrizione sintetica
Integration package that embeds LinkedIn Sales Navigator insights in Salesforce sales workflows.

## Oggetti principali
- Lead, Contact, Account, Opportunity, User.
- LinkedIn integration mapping/configuration objects from package.
- Activities or sync records depending on configuration.

## Funzionalita principali
- LinkedIn profile/account insights in Salesforce.
- Lead and account matching.
- CRM sync and sales intelligence views.

## Configurazioni principali
- LinkedIn/Salesforce connection and user entitlement.
- Field/page layout or Lightning component placement.
- CRM sync settings and data validation options.
- Permission sets and app access.

## Best practice
- Confirm license prerequisites before planning UI changes.
- Test matching behavior and duplicate impact.
- Keep LinkedIn data usage aligned with privacy and contract terms.
- Avoid overwriting CRM source-of-truth fields without governance.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
