# Salesforce Agent Optimizer

Skill per agenti AI che lavorano su progetti Salesforce. Guida design, architettura, implementazione, verifica, Knowledge locale, Salesforce CLI token-efficient, deploy sicuri e push tracciati.

## Principi Di Progettazione

Questa skill e' stata costruita su quattro principi:

- Ottimizzazione Salesforce: partire da configurazione, standard product capability, Flow, permission set, UI API/LDS, named credential e pattern Well-Architected prima di proporre Apex, LWC o integrazioni custom.
- Ottimizzazione token: usare progressive disclosure, Knowledge locale, indici Markdown, output CLI filtrato, patch minimali e letture mirate invece di riversare metadata o JSON completi nel contesto dell'agente.
- LLM Wiki di Andrej Karpathy: mantenere il source metadata come verita', compilare una wiki Markdown compatta, indicizzata e refreshabile, e consultarla prima di rianalizzare il progetto da zero.
- Printing Press per CLI agent-native: usare una facade sopra Salesforce CLI con comandi composti, JSON compatto, redazione dei segreti, dry-run, alias org esplicito e guardrail produzione read-only.

## Requisiti Della Skill

La skill deve:

- far rileggere e riassumere all'agente la richiesta utente prima di agire;
- fare domande solo quando servono requisiti, org target, rischio o criteri di accettazione;
- consultare la Knowledge locale prima di pianificare o modificare;
- preferire configurazione, standard Salesforce, Flow, LDS/UI API, permission set, named credential e managed package prima di custom code;
- pianificare modifiche minimali e chiedere approvazione prima di scrivere file o metadata;
- bloccare write/execute su org di produzione;
- richiedere sempre alias org esplicito per accessi a dati o metadata Salesforce;
- usare auth sicura: `auth-web`, `auth-device`, `auth-jwt`;
- validare con test/static check/subagent quando disponibile;
- ripianificare se approvazione, test o validazione falliscono, con massimo tre cicli falliti;
- chiedere se fare push e su quale branch solo a validazione completata;
- registrare nella Knowledge deploy e push remoti con requisito e tutti i metadata modificati.

## Prerequisiti

Minimi:

- Python 3.10+.
- Git.
- Un progetto Salesforce DX quando si usa `/sf-init-project-skill`, deploy o metadata retrieval.

Per operazioni su org Salesforce:

- Salesforce CLI aggiornata e disponibile come `sf`.
- Su Windows PowerShell, se `sf.ps1` viene bloccato dalla execution policy, usare `sf.cmd`; la facade `sf_agent_cli.py` lo fa automaticamente.
- Almeno un alias org autenticato. L'agente deve chiedere l'alias all'utente, non usare default org.

Opzionali:

- Node.js/npm per installare Salesforce CLI con `npm install -g @salesforce/cli`.
- PyYAML solo per eseguire il validator ufficiale delle skill Codex.
- Go e `cli-printing-press` solo se vuoi rigenerare o sperimentare CLI agent-native; non servono per usare gli script principali.

## Licenza Pubblica

La skill e' pubblicata con licenza MIT. Chiunque puo' usarla, copiarla, modificarla, distribuirla e forkare il repository rispettando il testo in `LICENSE`.

## Changelog

Le modifiche nel tempo sono tracciate in `CHANGELOG.md`. Aggiorna quel file a ogni release o modifica pubblica rilevante.

Fonti ufficiali utili, verificate al 2026-06-02:

- Salesforce CLI: https://developer.salesforce.com/tools/salesforcecli
- Salesforce CLI reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Claude Code slash commands: https://docs.anthropic.com/en/docs/claude-code/slash-commands
- Claude Code memory/CLAUDE.md: https://code.claude.com/docs/en/memory
- GitHub Copilot custom instructions: https://docs.github.com/en/copilot/concepts/prompting/response-customization
- Codex plugins and skills: https://openai.com/academy/codex-plugins-and-skills/
- OpenAI Agent Skills catalog: https://github.com/openai/skills

## Installazione

### Installazione Da Repository GitHub

Quando il repository pubblico sara' disponibile, l'utente potra' dare all'agente AI il link del repository e chiedere:

```text
Installa la skill Salesforce Agent Optimizer da https://github.com/lucabenedettini/salesforce-agent-optimizer
```

Per Codex, l'agente deve usare la skill `skill-installer` con il repository come sorgente, path root e nome esplicito:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-agent-optimizer --path . --name salesforce-agent-optimizer
```

In alternativa, se si usa un URL GitHub con path, l'agente puo' installare dalla root del branch:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-agent-optimizer --path . --ref main --name salesforce-agent-optimizer
```

Per Claude Code e GitHub Copilot non esiste lo stesso formato di skill nativa Codex: l'agente deve clonare o scaricare il repository, poi applicare gli adapter in `agents/` come indicato sotto.

### Codex

Metti la cartella `salesforce-agent-optimizer` in:

```text
~/.codex/skills/salesforce-agent-optimizer
```

Oppure, se usi `CODEX_HOME`:

```text
$CODEX_HOME/skills/salesforce-agent-optimizer
```

Codex usera' `SKILL.md`, `agents/openai.yaml`, `references/` e `scripts/` come skill nativa.

### Claude Code

Claude Code non usa automaticamente il formato Codex `agents/openai.yaml`. Usa quindi l'adapter:

- copia o richiama `agents/claude-code.md` nel `CLAUDE.md` del progetto;
- copia `agents/sf-init-project-skill.md` in `.claude/commands/sf-init-project-skill.md`.

Le istruzioni in `CLAUDE.md` sono contesto, non enforcement tecnico: per blocchi hard usa anche policy/hook di Claude Code quando disponibili.

### GitHub Copilot

Opzione repository-wide:

```text
.github/copilot-instructions.md
```

Unisci il contenuto di `agents/github-copilot-instructions.md`.

Opzione modulare:

```text
.github/instructions/salesforce-agent-optimizer.instructions.md
```

Mantieni la cartella skill nel repository, ad esempio:

```text
.agent-skills/salesforce-agent-optimizer/
```

Copilot legge instruction file repository/path-scoped, non installa questa cartella come skill nativa. L'adapter punta Copilot alla cartella skill e mantiene le istruzioni compatte.

## Uso Principale

### Inizializzare O Aggiornare La Knowledge

Comando agente:

```text
/sf-init-project-skill
```

Nel root del progetto Salesforce:

```bash
python scripts/sf_knowledge_init.py --project-root . --refresh
```

La Knowledge viene creata in:

```text
.salesforce-agent-knowledge/
```

Contiene:

- `index.md`: ingresso principale per l'agente;
- `markdown-index.md`: indice di tutti i Markdown;
- `metadata/<Tipo>/*.md`: un file uniforme per ogni metadata;
- `history/project-history.md`: storia compatta di change, deploy e push;
- `history/events/*.md`: eventi dettagliati con requisiti e metadata modificati;
- `index.json` e `sources.json`: indici machine-readable;
- `config.json`: lista metadata modificabile dall'utente.

Prima di pianificare o modificare, l'agente deve leggere:

1. `.salesforce-agent-knowledge/index.md`
2. `.salesforce-agent-knowledge/markdown-index.md` se serve trovare il file giusto
3. il file specifico sotto `.salesforce-agent-knowledge/metadata/`
4. `.salesforce-agent-knowledge/history/project-history.md`
5. il source file originale prima di scrivere

### Usare Salesforce CLI In Modo Sicuro

Usa sempre la facade:

```bash
python scripts/sf_agent_cli.py org-inspect --target-org dev-sandbox
python scripts/sf_agent_cli.py data-query --target-org dev-sandbox --query "SELECT Id, Name FROM Account LIMIT 20" --select result.records
```

Per comandi ufficiali `sf` non esposti come wrapper dedicati:

```bash
python scripts/sf_agent_cli.py safe-run --target-org dev-sandbox -- data query --query "SELECT Id FROM Account LIMIT 1" --select result.records
```

Deploy con history obbligatoria:

```bash
python scripts/sf_agent_cli.py deploy-start --target-org dev-sandbox --source-dir force-app --requirements "Add priority tracking to Account" --changed-metadata CustomField:Account.Priority__c
```

Se mancano `--requirements` o `--changed-metadata`, il deploy viene bloccato prima della connessione.

### Push Remoto Con History Inclusa

Usa il wrapper:

```bash
python scripts/git_knowledge_push.py --project-root . --remote origin --branch feature/account-priority --requirements "Add priority tracking to Account" --metadata CustomField:Account.Priority__c
```

Il wrapper:

1. registra un evento `git-push` nella Knowledge;
2. committa la history Knowledge;
3. esegue `git push`;
4. fa arrivare la history anche sul branch remoto.

Usa `--no-commit-history` solo se l'utente vuole esplicitamente history locale per quel push.

## Sicurezza

- Produzione e' read-only per la facade.
- I comandi write/execute interrogano `Organization.IsSandbox`; se non possono determinarlo, vengono bloccati.
- Output CLI redatto per token/session/auth URL/segreti.
- Nessun default org per dati o metadata.
- SOQL sempre con campi espliciti e limiti ragionevoli.
- Non inserire segreti in Knowledge, README, history o file metadata.

## Compatibilita' OS

Supporto previsto:

- Windows 10/11 con PowerShell, cmd o Git Bash.
- macOS con shell POSIX.
- Linux con shell POSIX.

Gli script sono Python standard library e usano `pathlib`/`subprocess`, quindi non richiedono Bash o shell POSIX. Le differenze principali sono:

- Windows: la facade preferisce `sf.cmd`.
- macOS/Linux: la facade usa `sf`.
- Esempi shell possono usare `python` o `python3` in base all'installazione locale.
- I test locali usano solo repository temporanei e non richiedono una org Salesforce.
- Se Salesforce CLI non e' nel `PATH`, imposta `SF_AGENT_SF_BIN` al percorso completo di `sf`, `sf.cmd` o `sf.exe`.

## Test

Test locale completo:

```bash
python scripts/self_test.py --json
```

Copre:

- generazione `/sf-init-project-skill` con file Markdown per metadata;
- `markdown-index.md` e history;
- history con requisito e metadata;
- blocco deploy senza requisito/metadata;
- blocco accesso org senza alias;
- dry-run senza scrittura history;
- push verso remote Git temporaneo con history inclusa sul ramo remoto.

Validazione Codex skill:

```bash
python <skill-creator>/scripts/quick_validate.py <path>/salesforce-agent-optimizer
```

Richiede PyYAML nel Python usato dal validator.

## File Principali

- `SKILL.md`: istruzioni canoniche della skill.
- `LICENSE`: licenza MIT pubblica.
- `CHANGELOG.md`: storico delle modifiche e delle release.
- `agents/openai.yaml`: metadata Codex.
- `agents/claude-code.md`: adapter Claude Code.
- `agents/github-copilot-instructions.md`: adapter GitHub Copilot.
- `agents/sf-init-project-skill.md`: comando `/sf-init-project-skill` portabile.
- `scripts/sf_knowledge_init.py`: crea/aggiorna Knowledge.
- `scripts/sf_agent_cli.py`: facade sicura Salesforce CLI.
- `scripts/knowledge_history.py`: registra eventi Knowledge.
- `scripts/git_knowledge_push.py`: push remoto con history inclusa.
- `scripts/self_test.py`: test locali cross-platform.
- `references/`: guide dettagliate e catalogo comandi Salesforce CLI.

## Note Operative Per Agenti

- Leggere meno file possibile: `index.md`, pagina metadata rilevante, history, poi source.
- Non usare la Knowledge come fonte unica: il source metadata resta la verita'.
- Se la Knowledge generata da `/sf-init-project-skill` e' vecchia rispetto ai file modificati, refreshare prima di pianificare.
- Se una modifica viene deployata o pushata, la history deve spiegare il requisito e tutti i metadata modificati.
