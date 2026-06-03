# Nome del prodotto/pacchetto: Zoom for Lightning

## Breve descrizione sintetica
Integration package for using Zoom meetings, telephony or collaboration features from Salesforce Lightning.

## Oggetti principali
- Event, Task, Lead, Contact, Account, Opportunity, Case.
- Zoom managed package objects for meeting/phone integration and logs.
- Connected app/auth records and integration user.

## Funzionalita principali
- Create or join Zoom meetings from Salesforce.
- Log meeting or call activity.
- Surface Zoom productivity tools in Lightning pages.

## Configurazioni principali
- Zoom account connection and user mapping.
- Lightning components, actions, page layouts.
- Permission sets and OAuth/connected app settings.
- Activity sync and logging options.

## Best practice
- Confirm user identity mapping between Zoom and Salesforce.
- Avoid duplicate activity logging with other CTI/calendar tools.
- Test privacy, recording visibility and meeting data access.
- Keep integration permissions least-privileged.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
