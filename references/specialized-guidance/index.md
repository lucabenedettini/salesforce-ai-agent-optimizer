# Specialized Salesforce Guidance

Read only the file that matches the current task. Do not load this whole folder by default.
Specialized guidance coordinates existing SFAO references; it does not replace core references.
Core SFAO safety always wins when there is any conflict.

- Apex, triggers, invocable Apex, backend security: `apex.md`
- LWC, Lightning UI, LDS/UI API, component exposure: `lwc.md`
- Flow, automation, validation rules, activation strategy: `flow.md`
- SOQL, query planning, selectivity, schema-driven payloads: `soql.md`
- Deploy, package.xml, release validation, rollback: `deploy.md`
- Test data, data CRUD, exports/imports, cleanup: `data-operations.md`
- Agentforce, Salesforce Agent, topics, actions, prompts, publish/activation: `agentforce.md`

Load only one specialized file unless the request clearly spans multiple areas. If a core safety reference is stricter than specialized guidance, follow the stricter core reference.
