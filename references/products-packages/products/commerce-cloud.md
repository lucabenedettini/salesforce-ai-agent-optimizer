# Nome del prodotto/pacchetto: Commerce Cloud

## Breve descrizione sintetica
Soluzione Salesforce per storefront, catalogo, carrello, pricing, checkout, ordine e commerce B2B/B2C.

## Oggetti principali
- Product2, Pricebook2, PricebookEntry, Order, OrderItem, Account, Contact.
- Cart, WebStore, BuyerGroup, ProductCategory, Catalog, entitlement records where enabled.
- Integration objects for payment, tax, shipping and ERP sync.

## Funzionalita principali
- Catalog management, storefront, cart e checkout.
- Pricing, promotions, buyer groups e order capture.
- Integrazioni con payment, tax, fulfillment e ERP.

## Configurazioni principali
- Web store, catalog, category, product, pricebook e buyer group.
- Checkout flow, payment gateway, shipping/tax integrations.
- Experience Cloud site, guest/user access, sharing and security.
- Order management integration and lifecycle automation.

## Best practice
- Separare catalogo, pricing, entitlement e fulfillment ownership.
- Testare guest access, sharing e performance storefront.
- Pianificare sincronizzazione product/order con sistemi esterni.
- Trattare checkout, pagamento e tax come flussi ad alto rischio.

## Contesto versione
Prima della pianificazione leggere `references/salesforce-current-version.md`. Verificare la release della target org e la disponibilita' effettiva delle funzionalita'; per prodotti distribuiti anche come managed package o add-on, verificare la versione installata nella org quando rilevante.
