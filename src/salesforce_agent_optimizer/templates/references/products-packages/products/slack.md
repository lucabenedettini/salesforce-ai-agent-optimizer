# Nome del prodotto/pacchetto: Slack

## Breve descrizione sintetica
Collaboration platform integrated with Salesforce for channels, workflows, notifications, approvals and agent/human work.

## Oggetti principali
- Slack workspace, channel, user, app, workflow, message.
- Salesforce records surfaced through Salesforce channels and Slack apps.
- Connected app, named credential, permission set, Flow actions.

## Funzionalita principali
- Collaboration around Salesforce records.
- Notifications, approvals and workflow automation.
- Agent and human handoff inside Slack.

## Configurazioni principali
- Salesforce for Slack app, workspace connection, channel mapping.
- Slack actions in Flow, notification rules, app permissions.
- Identity mapping between Salesforce users and Slack users.
- Security, retention and compliance settings.

## Best practice
- Define which decisions can happen in Slack and which must stay in Salesforce.
- Avoid leaking sensitive record data into broad channels.
- Test user identity mapping, permissions and audit requirements.
- Keep Slack workflows simple and observable.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. Verificare la release della target org e la disponibilita' effettiva delle funzionalita'; per prodotti distribuiti anche come managed package o add-on, verificare la versione installata nella org quando rilevante.
