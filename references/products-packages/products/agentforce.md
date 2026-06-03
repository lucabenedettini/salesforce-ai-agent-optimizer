# Nome del prodotto/pacchetto: Agentforce

## Breve descrizione sintetica
Piattaforma Salesforce per creare, testare, distribuire e governare agenti AI con azioni, dati, guardrail e integrazioni.

## Oggetti principali
- Agent topics, actions, instructions, agent configuration metadata.
- Flow, Apex invocable actions, prompt templates, data sources, Data 360 objects.
- Permission sets, connected apps, named credentials, audit/log objects.

## Funzionalita principali
- Creazione e orchestrazione di agenti AI.
- Azioni low-code/pro-code.
- Grounding su dati Salesforce e sistemi esterni.
- Guardrail, testing, monitoring e lifecycle management.

## Configurazioni principali
- Agent definitions, topics, actions, instructions.
- Accesso dati tramite permission set, Data 360, Apex, Flow, named credentials.
- Canali di esposizione: Service, Sales, Slack, Experience Cloud o custom UI.
- Logging, test set, supervision e fallback umano.

## Best practice
- Definire scope, dati autorizzati e azioni consentite prima di configurare l'agente.
- Usare azioni deterministiche per operazioni critiche e LLM solo dove serve ragionamento flessibile.
- Validare permessi, FLS, sharing e audit trail.
- Testare casi positivi, negativi, escalation e prompt injection.
