# Salesforce AI Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | Espanol | [简体中文](README.zh-CN.md)

[![Validate Skill](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/actions/workflows/validate.yml/badge.svg)](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/lucabenedettini/salesforce-ai-agent-optimizer)](https://github.com/lucabenedettini/salesforce-ai-agent-optimizer/releases)
[![Agents](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20GitHub%20Copilot-blue)](#instalacion)

Salesforce AI Agent Optimizer es una skill publica con licencia MIT para agentes AI que trabajan en proyectos Salesforce. Ayuda a Codex, Claude Code, GitHub Copilot y agentes similares a planificar, implementar, validar, empaquetar y documentar cambios Salesforce con uso compacto de contexto y guardrails fuertes.

El repositorio publico se llama **Salesforce AI Agent Optimizer**. El nombre de la skill Codex sigue siendo `salesforce-agent-optimizer`.

Version actual: `1.0.1`

## Principios

- Salesforce first: preferir capacidades estandar, configuracion, Flow, permission sets, LDS/UI API, named credentials y managed packages antes que Apex, LWC, triggers o integraciones custom.
- Eficiencia de tokens: usar progressive disclosure, Knowledge local indexada, salida CLI compacta, lecturas dirigidas y parches minimos.
- Knowledge local: `/sf-init-project-skill` crea un indice Markdown compacto de metadata del proyecto, inspirado en el patron LLM wiki.
- CLI agent-native: `scripts/sf_agent_cli.py` envuelve la Salesforce CLI oficial con alias explicitos, JSON compacto, redaccion de secretos, dry-run, produccion read-only y bloqueo de deletes sin aprobacion.
- Least privilege: durante la planificacion el agente debe inspeccionar los permisos actuales en la org para users/personas afectados y conceder solo el acceso minimo necesario.
- No inventar: si falta evidencia, el agente debe preguntar al user o presentar escenarios con tradeoffs.

## Guardrails De Seguridad

- Las orgs de produccion son read-only para operaciones write, execute y destructive mediante la facade.
- Cada comando org/data/metadata requiere un alias org explicito.
- Las operaciones destructivas nunca son automaticas. Data delete, metadata delete, package uninstall, source delete, purge, hard delete y despliegues con `destructiveChanges.xml` requieren aprobacion separada sobre el scope exacto.
- La CLI bloquea comandos destructivos sin este flag exacto tras la aprobacion user:

```bash
--delete-approval "I explicitly approve this deletion"
```

- La metadata eliminada va en `destructiveChanges.xml`, no en `package.xml`.
- Si record set, dependencias metadata, version package, permisos o comportamiento org no estan claros, el agente debe preguntar o presentar opciones.

## Comandos Principales

Crear o refrescar Knowledge:

```text
/sf-init-project-skill
```

Actualizar contexto de version Salesforce release/API/SOAP/package desde fuentes oficiales:

```text
/sf-version-update-skill
```

Ejecutar tests locales:

```bash
python scripts/sync_agent_instructions.py --check
python scripts/validate_skill.py
python scripts/self_test.py --json
python -m pytest
```

Generar manifest para metadata agregada o modificada:

```bash
python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<date>-<change>/package.xml --from-git-status
```

Leer packages instalados en una org:

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

Inspeccionar acceso actual antes de planificar permisos:

```bash
python scripts/sf_agent_cli.py access-inspect --target-org <alias> --username user@example.com --sobject Account --select users.records,permission_set_assignments.records,object_permissions.records,field_permissions.records
```

Borrar un record solo tras aprobacion explicita:

```bash
python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id 001... --delete-approval "I explicitly approve this deletion"
```

## Instalacion

Pide a Codex:

```text
Install the Salesforce AI Agent Optimizer skill from https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Comando installer Codex:

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Rutas nativas Codex:

- Skill de repo: `.agents/skills/salesforce-agent-optimizer`
- Skill de user: `$HOME/.agents/skills/salesforce-agent-optimizer`

Claude Code:

- Instala o conserva la skill en `.claude/skills/salesforce-agent-optimizer/SKILL.md`.
- Opcionalmente fusiona `agents/claude-code.md` en `CLAUDE.md`.
- Copia `agents/sf-init-project-skill.md` en `.claude/commands/sf-init-project-skill.md`.
- Copia `agents/sf-version-update-skill.md` en `.claude/commands/sf-version-update-skill.md`.

GitHub Copilot:

- Usa `AGENTS.md`, `.github/copilot-instructions.md` y `.github/instructions/salesforce-agent-optimizer.instructions.md`.

## Prerrequisitos

- Python 3.10+.
- Git.
- Proyecto Salesforce DX para Knowledge metadata, deploy, retrieve o manifest.
- Salesforce CLI oficial disponible como `sf`.
- Alias org autenticados. El agente debe pedir los alias y no usar default org.
- Sandbox para operaciones write/execute. Produccion es read-only.

Opcional:

- PyYAML para validar skills Codex.
- Node.js/npm para instalar Salesforce CLI con `npm install -g @salesforce/cli`.
- Go y `cli-printing-press` solo para experimentacion CLI.

## Contexto Version

Verificado el 2026-06-03:

- Salesforce release: Summer '26.
- Platform API, Metadata API, SOAP API: `67.0`.
- SOAP API `login()` no esta disponible en API `65.0+`; Salesforce anuncio el retirement de SOAP `login()` para API `31.0-64.0` con Summer '27.
- Las versiones de managed packages son especificas de la target org. Inspecciona packages instalados antes de asumir namespace, objetos o features.

## Validacion Y Handoff

La metodologia requiere resumir la solicitud, hacer preguntas solo cuando sean necesarias, identificar productos/packages y dependencias, aplicar least privilege, planificar cambios minimos, pedir aprobacion, generar `package.xml`, ofrecer artefactos de entrega, validar con tests o subagent, y preguntar si hacer push y a que branch solo cuando la validacion pase.

## Fuentes Oficiales

- Salesforce CLI: https://developer.salesforce.com/tools/salesforcecli
- Salesforce CLI reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata API deploy and destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
- Salesforce Well-Architected Secure: https://architect.salesforce.com/docs/architect/well-architected/guide/secure
- Salesforce release notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5

## Licencia

MIT. Cualquier persona puede usar, copiar, modificar, distribuir y forkear este repositorio bajo los terminos de `LICENSE`.
