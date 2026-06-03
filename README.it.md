# Salesforce AI Agent Optimizer

[English](README.md) | Italiano | [Espanol](README.es.md) | [简体中文](README.zh-CN.md)

[![Validate Skill](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/actions/workflows/validate.yml/badge.svg)](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/lucabenedettini/salesforce-ai-agent-optimizer)](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/releases)
[![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20GitHub%20Copilot-blue)](#installazione)

Salesforce AI Agent Optimizer e' una skill pubblica con licenza MIT per agenti AI che lavorano su progetti Salesforce. Aiuta Codex, Claude Code, GitHub Copilot e agenti simili a pianificare, implementare, validare, pacchettizzare e documentare modifiche Salesforce usando poco contesto e guardrail di sicurezza forti.

Il repository pubblico si chiama **Salesforce AI Agent Optimizer**. Il nome della skill Codex resta `salesforce-agent-optimizer`.

Versione corrente: `0.6.1`

## Principi

- Salesforce first: preferire capability standard, configurazione, Flow, permission set, LDS/UI API, named credential e managed package prima di Apex, LWC, trigger o integrazioni custom.
- Efficienza token: usare progressive disclosure, Knowledge locale indicizzata, output CLI compatto, letture mirate e patch minimali.
- Knowledge locale: `/sf-init-project-skill` crea un indice Markdown compatto dei metadata del progetto, ispirato al pattern LLM wiki.
- CLI agent-native: `scripts/sf_agent_cli.py` avvolge la Salesforce CLI ufficiale con alias espliciti, JSON compatto, redazione segreti, dry-run, produzione read-only e blocco delete senza approvazione.
- Least privilege: in pianificazione l'agente deve ispezionare i permessi attuali nella org per user/personas coinvolti e concedere solo l'accesso minimo necessario.
- Niente invenzioni: se manca evidenza, l'agente deve chiedere allo user o presentare scenari con pro e contro.

## Guardrail Di Sicurezza

- Le org di produzione sono read-only per operazioni write, execute e destructive tramite la facade.
- Ogni comando org/data/metadata richiede alias org esplicito.
- Le operazioni distruttive non sono mai automatiche. Delete dati, delete metadata, package uninstall, source delete, purge, hard delete e deploy con `destructiveChanges.xml` richiedono approvazione separata sullo scope esatto.
- La CLI blocca comandi distruttivi senza questo flag esatto dopo l'approvazione user:

```bash
--delete-approval "I explicitly approve this deletion"
```

- I metadata rimossi vanno in `destructiveChanges.xml`, non in `package.xml`.
- Se record set, dipendenze metadata, versione package o comportamento org non sono chiari, l'agente deve chiedere o presentare opzioni.

## Comandi Principali

Creare o aggiornare la Knowledge:

```text
/sf-init-project-skill
```

Aggiornare il contesto versione Salesforce release/API/SOAP/package da fonti ufficiali:

```text
/sf-version-update-skill
```

Eseguire i test locali:

```bash
python scripts/sync_agent_instructions.py --check
python scripts/validate_skill.py
python scripts/self_test.py --json
python -m pytest
```

Generare il manifest per metadata aggiunti o modificati:

```bash
python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<date>-<change>/package.xml --from-git-status
```

Leggere i package installati in una org:

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

Ispezionare l'accesso attuale prima di pianificare permessi:

```bash
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
```

Cancellare un record solo dopo approvazione esplicita:

```bash
python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id 001... --delete-approval "I explicitly approve this deletion"
```

## Installazione

Chiedi a Codex:

```text
Installa la skill Salesforce AI Agent Optimizer da https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Comando installer Codex:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Path nativi Codex:

- Skill repo: `.agents/skills/salesforce-agent-optimizer`
- Skill user: `$HOME/.agents/skills/salesforce-agent-optimizer`

Claude Code:

- Installa o mantieni la skill in `.claude/skills/salesforce-agent-optimizer/SKILL.md`.
- Opzionalmente unisci `agents/claude-code.md` in `CLAUDE.md`.
- Copia `agents/sf-init-project-skill.md` in `.claude/commands/sf-init-project-skill.md`.
- Copia `agents/sf-version-update-skill.md` in `.claude/commands/sf-version-update-skill.md`.

GitHub Copilot:

- Usa `AGENTS.md`, `.github/copilot-instructions.md` e `.github/instructions/salesforce-agent-optimizer.instructions.md`.

## Prerequisiti

- Python 3.10+.
- Git.
- Progetto Salesforce DX per Knowledge metadata, deploy, retrieve o manifest.
- Salesforce CLI ufficiale disponibile come `sf` per operazioni su org.
- Alias org autenticati. L'agente deve chiedere gli alias e non usare default org.
- Sandbox per operazioni write/execute. Produzione e' read-only.

Opzionali:

- PyYAML per validare skill Codex.
- Node.js/npm per installare Salesforce CLI con `npm install -g @salesforce/cli`.
- Go e `cli-printing-press` solo per sperimentare sulla CLI.

## Contesto Versione

Verificato il 2026-06-03:

- Salesforce release: Summer '26.
- Platform API, Metadata API, SOAP API: `67.0`.
- SOAP API `login()` non e' disponibile in API `65.0+`; Salesforce ha annunciato il retirement di SOAP `login()` per API `31.0-64.0` con Summer '27.
- Le versioni managed package sono specifiche della target org. Ispezionare i package installati prima di assumere namespace, oggetti o feature.

Risorse canoniche:

- `references/salesforce-current-version.md`
- `references/salesforce-version.json`
- `references/version-update.md`

## Validazione E Handoff

La metodologia richiede:

- Riassumere la richiesta.
- Fare domande mirate solo quando servono.
- Identificare prodotti/pacchetti Salesforce e dipendenze metadata.
- Pianificare modifiche minimali e chiedere approvazione.
- Chiedere approvazione distruttiva separata quando serve.
- Implementare solo lavoro approvato.
- Generare `package.xml` per metadata aggiunti/modificati.
- Offrire release notes, specifiche tecniche, impact assessment, user testing e manual procedures.
- Validare con test o subagent di validazione.
- Chiedere se fare push e su quale branch solo dopo validazione superata.

## File Principali

- `SKILL.md`: istruzioni canoniche.
- `agents/`: adapter Codex, Claude Code, GitHub Copilot e slash command.
- `references/`: guide progressive per architettura Salesforce, prodotti, CLI, test, delete, versioni e delivery.
- `references/routing.md`: mappa compatta per caricare solo le referenze necessarie.
- `scripts/sf_agent_cli.py`: facade sicura Salesforce CLI.
- `scripts/sync_agent_instructions.py`: generatore degli adapter per agenti.
- `scripts/sf_knowledge_init.py`: generatore Knowledge metadata.
- `scripts/generate_package_manifest.py`: generatore `package.xml`.
- `scripts/git_knowledge_push.py`: push remoto con history Knowledge.
- `scripts/self_test.py`: test locali cross-platform.
- `evals/trigger-evals.json`: esempi di attivazione e non attivazione della skill.

## Fonti Ufficiali

- Salesforce CLI: https://developer.salesforce.com/tools/salesforcecli
- Salesforce CLI reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata API deploy e destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
- GraphQL delete record: https://developer.salesforce.com/docs/platform/graphql/guide/mutations-delete.html
- LWC `deleteRecord`: https://developer.salesforce.com/docs/platform/lwc/guide/reference-delete-record.html
- Salesforce release notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5
- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure

## Licenza

MIT. Chiunque puo' usare, copiare, modificare, distribuire e forkare questo repository rispettando `LICENSE`.
