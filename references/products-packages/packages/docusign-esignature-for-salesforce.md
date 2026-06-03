# Nome del prodotto/pacchetto: Docusign eSignature for Salesforce

## Breve descrizione sintetica
Pacchetto per inviare, firmare, tracciare e salvare accordi Docusign direttamente da Salesforce.

## Oggetti principali
- Account, Contact, Opportunity, Quote, Contract, Document objects.
- Docusign managed package objects for envelopes, recipients, templates and status.
- Files, ContentDocument, ContentVersion and integration user.

## Funzionalita principali
- Invio buste di firma da record Salesforce.
- Tracking dello stato firma.
- Template, recipient mapping and document storage.
- Automazioni post-firma.

## Configurazioni principali
- Docusign connection, account mapping and authentication.
- Send buttons/actions, page layouts, Lightning components.
- Template mapping, recipient roles, status updates.
- Permission sets, named credentials/connected app where applicable.

## Best practice
- Validare accesso a documenti e record prima di inviare envelope.
- Separare template logic da automazioni Salesforce quando possibile.
- Testare status callback, error handling e retry.
- Non salvare credenziali o token in metadata o Knowledge.
