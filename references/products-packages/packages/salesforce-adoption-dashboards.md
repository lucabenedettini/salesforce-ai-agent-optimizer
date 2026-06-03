# Nome del prodotto/pacchetto: Salesforce Adoption Dashboards

## Breve descrizione sintetica
Pacchetto Salesforce Labs gratuito per analizzare login, utilizzo funzionalita e adozione degli utenti.

## Oggetti principali
- User, LoginHistory, EventLogFile where available.
- Report, Dashboard, Folder and package report types.
- Managed package metadata; inspect installed namespace/version.

## Funzionalita principali
- Dashboard di adozione utenti.
- Trend su login e utilizzo funzionalita.
- Report per monitorare produttivita e engagement.

## Configurazioni principali
- Report folders, dashboard folders and visibility.
- Permission sets/profiles for report and dashboard access.
- Scheduled refresh and dashboard subscriptions.

## Best practice
- Verificare che i dati di login/report siano accessibili agli utenti target.
- Non modificare direttamente componenti managed se non previsto.
- Usare i risultati come input per enablement, non come unico indicatore di adozione.
- Controllare sharing di report e dashboard prima del rilascio.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
