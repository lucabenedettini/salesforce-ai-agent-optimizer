# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer e' una CLI `sfao` e una skill per Codex, Claude Code e GitHub Copilot, distribuita con licenza MIT.

Versione corrente: `2.2.3`

Aiuta gli agenti AI sui progetti Salesforce con pianificazione Salesforce-first, configurazione prima del codice custom, modifiche minime e reversibili, Knowledge locale, uso token-efficient della Salesforce CLI, least privilege, alias org espliciti, consapevolezza di `package.xml` e guardrail per operazioni distruttive.

La guidance Salesforce specializzata include Apex, LWC, Flow, SOQL, deploy, data operations e Agentforce; ogni file viene caricato solo quando rilevante e coordina le reference SFAO esistenti.

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

Usa `uv tool install` o `python -m pipx install` per installazioni CLI isolate. `python -m pip install` funziona quando vuoi `sfao` nell'ambiente Python attivo.

## Installazione

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao validate
```

Alternative:

```bash
python -m pipx install salesforce-agent-optimizer
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
```

`sfao install` installa adapter project-scoped per tutti gli agenti supportati. Usa `sfao install --user --platform all` solo quando vuoi un'installazione Codex/Claude a livello utente.

## Comandi Principali

| Comando | Cosa fa e quando usarlo | Principio |
| --- | --- | --- |
| `sfao version` | Mostra la versione installata. Usalo dopo install o upgrade. | Chiarezza versione. |
| `sfao install` | Installa nel repo gli adapter project-scoped per gli agenti supportati. Usalo una volta per progetto Salesforce. | Setup senza attrito. |
| `sfao install --project --platform all` | Install esplicito per Codex, Claude Code e GitHub Copilot. Usalo in onboarding repo. | Compatibilita' agenti. |
| `sfao update --project --platform all` | Aggiorna adapter e template generati dopo upgrade del pacchetto. | Upgrade sicuro. |
| `sfao uninstall --project --platform all --yes` | Rimuove solo i file SFAO generati. Usalo per disinstallare la skill dal progetto. | Modifiche reversibili. |
| `sfao doctor` | Controlla Python, OS, Git, Salesforce CLI, adapter, PATH e validazione. Usalo dopo install/update o se la skill non appare. | Diagnosi anticipata. |
| `sfao doctor --verbose` | Mostra diagnostica dettagliata. Usalo per investigare warning. | Analisi trasparente. |
| `sfao validate` | Valida file skill, versioni, adapter generati, formati e guardrail metadata Salesforce. Usalo prima di commit/release. | Quality gate. |
| `sfao validate --json` | Produce validazione machine-readable. Usalo in CI o nelle fasi agent. | Output automatizzabile. |
| `sfao report --project-root .` | Scrive un health snapshot Markdown locale per adapter, Knowledge, memory, guardrail, guidance, eval e version context. Usalo prima del planning o handoff. | Stato locale osservabile. |
| `sfao knowledge init --project-root .` | Crea Knowledge locale compatta del progetto Salesforce. Usalo prima del primo planning. | Knowledge prima dei metadata grezzi. |
| `sfao knowledge refresh --project-root .` | Aggiorna la Knowledge dopo modifiche metadata. | Evidenza di planning aggiornata. |
| `sfao knowledge init --project-root . --scan-root` | Esegue una scansione ampia intenzionale. Usalo solo se `packageDirectories` non basta. | Scope token-efficient. |
| `sfao knowledge doctor --project-root .` | Controlla la struttura della Knowledge. Usalo se l'agente segnala Knowledge mancante o stale. | Contesto locale affidabile. |
| `sfao memory init --project-root .` | Crea memoria curata di progetto. Usalo per apprendimento durevole. | Memoria compatta. |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | Aggiunge una lezione, decisione, rischio o follow-up redatto. Usalo dopo implementazione o validazione. | Niente log grezzi, niente segreti. |
| `sfao memory compact --project-root . --max-bytes 60000` | Mantiene la memoria piccola e utile. Usalo quando cresce troppo. | Efficienza token. |
| `sfao memory doctor --project-root .` | Valida struttura e redazione della memoria. Usalo prima di usarla nel planning. | Memoria privacy-safe. |
| `sfao version-context scaffold` | Crea i file version-context se mancano. Usalo per bootstrap delle reference. | Prontezza fonti ufficiali. |
| `sfao version-context update` | Aggiorna release/API context da fonti ufficiali Salesforce. Usalo quando il contesto e' stale o release-sensitive. | Non inventare behavior. |
| `sfao version-context validate --max-age-days 90` | Controlla freschezza del version-context. Usalo in validazione o planning sensibile alla release. | Evidenza API corrente. |
| `sfao command search "permission account"` | Cerca nel registry interno sicuro della Salesforce CLI facade. Usalo prima di comandi org. | Scoprire prima di eseguire. |
| `sfao command payload-example access-inspect` | Mostra un payload compatto per un comando registrato. Usalo per evitare flag inventati. | Comandi guidati da schema. |
| `sfao command execute --payload payload.json` | Esegue un comando registrato tramite guardrail compatti. Usalo solo con alias org esplicito quando richiesto. | Salesforce CLI facade sicura. |
| `sfao soql build --object Account --fields Id,Name` | Costruisce SOQL focalizzato e payload `data-query`. Usalo prima di interrogare dati org. | Recupero dati minimo. |
| `sfao permissions explain --input access.json` | Sintetizza evidenza accessi da output `access-inspect`. Usalo per least-privilege planning. | Accessi spiegabili. |
| `sfao live-test --target-org <alias>` | Esegue test opt-in contro org reale. Usa write/destructive suite solo con alias sandbox/scratch esplicito. | Validazione reale con consenso. |

Per operazioni org l'agente deve chiedere un alias esplicito. Le org di produzione sono read-only tramite i guardrail della skill.

## Workflow Agente

Gli agenti installati devono seguire le stesse fasi visibili per richieste informative, bugfix, implementazioni, architettura, review, ispezione org e release:

1. `Request review`
2. `Planning evidence`
3. `Approval`
4. `Implementation`
5. `Validation`
6. `Completion`

Durante ogni fase l'agente deve indicare il tool o comando che sta usando o pianificando. Per accesso Salesforce CLI deve mostrare la forma compatta del comando `sfao`, `scripts/sf_agent_cli.py` o `sf`, con alias e segreti redatti.

Per domande solo informative, senza decisioni di progetto, org access, ispezione metadata, deploy, operazioni dati, segreti, azioni distruttive, claim release-sensitive, implementazione o bugfix, l'agente puo' usare la modalita' compatta: `Request review`, `Evidence`, `Answer`, `Validation`.

## Sicurezza

- Preferire configurazione Salesforce, Flow, permission set, UI API/LDS, named credential e managed package prima del codice custom.
- Consultare la Knowledge locale prima di modificare metadata Salesforce.
- Usare `.salesforce-agent-knowledge/memory.md` per decisioni durevoli, lezioni, rischi e follow-up. E' memoria curata di progetto, non un log grezzo, e non deve contenere segreti, dati cliente, record grezzi o log grandi.
- La Knowledge usa di default le `packageDirectories` Salesforce DX quando disponibili; usare `--scan-root` solo per una scansione ampia intenzionale.
- La guida specializzata Apex, LWC, Flow, SOQL, deploy, data operations e Agentforce viene caricata solo quando rilevante.
- Skill Salesforce esterne sono solo riferimenti opzionali se gia' disponibili e non possono bypassare i guardrail SFAO.
- `safe-run --safety` non puo' abbassare la classificazione automatica del rischio.
- Applicare least privilege prima di modifiche ad accessi, sharing, UI, package, integrazioni o automazioni.
- Non recuperare o parsare tutti i metadata org salvo richiesta ampia o necessita' reale.
- Non cancellare dati o metadata senza approvazione separata sullo scope esatto.
- Non esporre segreti Salesforce o dati cliente senza approvazione separata sullo scope esatto.
- Generare `package.xml` per metadata aggiunti o modificati.
- Dopo l'implementazione chiedere se generare release note, specifiche tecniche, impact assessment, user testing e manual procedure.

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Alternative:

```bash
python -m pipx upgrade salesforce-agent-optimizer
python -m pip install --upgrade salesforce-agent-optimizer
```

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

Alternativa:

```bash
python -m pipx uninstall salesforce-agent-optimizer
```

## Altra Documentazione

Dettagli di installazione, comandi, troubleshooting, publishing, release e versioning sono in `docs/wiki/`.

## Licenza

MIT. Chiunque puo' usare, copiare, modificare, distribuire e forkare questo repository secondo i termini di `LICENSE`.
