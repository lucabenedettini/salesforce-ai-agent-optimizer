# Nome del prodotto/pacchetto: Salesforce CPQ

## Breve descrizione sintetica
Managed package for configure-price-quote processes: product selection, pricing, discounting, quote lines, templates, contracts and renewals.

## Oggetti principali
- Standard: Account, Opportunity, Product2, Pricebook2, PricebookEntry, Quote, Contract.
- CPQ managed objects commonly include quote, quote line, product option, product rule, price rule, discount schedule, quote template and subscription objects.
- Namespaces and exact object API names depend on package version; inspect installed metadata before planning.

## Funzionalita principali
- Quote Line Editor, product configuration, bundles and options.
- Product rules, price rules, discount schedules and approvals.
- Quote document generation, contracts, amendments and renewals.

## Configurazioni principali
- Products, bundles, options, features, configuration attributes.
- Price books, pricing methods, price rules, discount schedules.
- Product rules, guided selling, quote templates and output documents.
- Permission sets, field sets, page layouts, custom settings and package settings.

## Best practice
- Prefer CPQ rules and configuration before Apex custom pricing.
- Plan dependencies across products, price books, fields, field sets, layouts and approval criteria.
- Test QLE performance, calculation sequence and amendment/renewal scenarios.
- Never assume package object names; inspect namespace and installed metadata.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. Verificare la release della target org e la disponibilita' effettiva delle funzionalita'; per prodotti distribuiti anche come managed package o add-on, verificare la versione installata nella org quando rilevante.
