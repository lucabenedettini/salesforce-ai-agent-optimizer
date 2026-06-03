# Nome del prodotto/pacchetto: Box Intelligent Content Management

## Breve descrizione sintetica
Box integration for managing content, collaboration, document workflows and file access from Salesforce.

## Oggetti principali
- Account, Opportunity, Case, Contract and other record contexts with documents.
- Files/ContentDocument where Salesforce files are involved.
- Box folder/file mapping and managed package integration objects.

## Funzionalita principali
- Link Salesforce records to Box folders/files.
- Collaborate on documents and manage content lifecycle.
- Automate folder creation, permissions and document workflows.

## Configurazioni principali
- Box connection, user mapping and folder templates.
- Lightning components, actions and page layout placement.
- Permission sets, connected app/auth settings and security policies.
- Record-to-folder mapping and automation.

## Best practice
- Define document system of record before syncing or linking files.
- Verify Box permissions and Salesforce sharing do not conflict.
- Test folder creation and ownership for private records.
- Avoid storing sensitive files in broadly shared folders.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. La versione installata del managed package e' specifica della target org: chiedere l'alias org e usare `scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result` prima di assumere namespace, oggetti, feature o comportamento disponibili.
