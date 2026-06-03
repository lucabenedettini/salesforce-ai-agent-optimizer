# Nome del prodotto/pacchetto: FieldSpy: Field Usage Report

## Breve descrizione sintetica
Package for analyzing field population and usage to support cleanup of unused or low-value fields.

## Oggetti principali
- CustomObject, CustomField and target business objects being analyzed.
- Package result/configuration objects; inspect installed metadata.
- Reports, dashboards or analysis records where included.

## Funzionalita principali
- Field population analysis.
- Cleanup support for unused fields.
- Usage visibility for admins and architects.

## Configurazioni principali
- Object selection, scan settings and result visibility.
- Package permissions and admin app access.
- Reports/dashboards for results.

## Best practice
- Do not delete fields based only on population percentage.
- Check dependencies in layouts, Lightning pages, Flow, Apex, reports and integrations.
- Export or archive data before destructive cleanup.
- Use deprecation phases before deletion.
