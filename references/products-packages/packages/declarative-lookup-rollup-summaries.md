# Nome del prodotto/pacchetto: Declarative Lookup Rollup Summaries (DLRS)

## Breve descrizione sintetica
Pacchetto per creare rollup declarativi su relazioni lookup e mantenere campi parent aggiornati.

## Oggetti principali
- Parent object and child object involved in lookup relationship.
- Rollup definition objects from DLRS managed package.
- Apex triggers/classes generated or managed by DLRS, depending on mode.

## Funzionalita principali
- Count, sum, min, max and concatenate rollups.
- Real-time, scheduled or developer-triggered calculations.
- Filtered rollups over lookup relationships.

## Configurazioni principali
- Rollup definitions, parent/child fields, relationship field.
- Calculation mode and scheduled jobs.
- Permissions for setup/admin users.
- Trigger deployment or package automation settings.

## Best practice
- Prefer standard rollup summaries on master-detail when available.
- Test bulk updates and recalculation before production.
- Check recursion, trigger order and performance impact.
- Document which parent fields are DLRS-managed.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
