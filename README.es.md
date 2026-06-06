# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer es una CLI `sfao` y una skill para Codex, Claude Code y GitHub Copilot, publicada con licencia MIT.

Version actual: `2.1.0`

Ayuda a los agentes AI en proyectos Salesforce con planificacion Salesforce-first, configuracion antes que codigo custom, cambios minimos y reversibles, Knowledge local, uso eficiente de tokens con Salesforce CLI, least privilege, alias de org explicitos, conciencia de `package.xml` y guardrails para operaciones destructivas.

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

Usa `uv tool install` o `python -m pipx install` para instalaciones CLI aisladas. `python -m pip install` tambien funciona cuando quieres `sfao` en el entorno Python activo.

## Instalacion

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao validate
```

Alternativas:

```bash
python -m pipx install salesforce-agent-optimizer
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
```

`sfao install` instala adaptadores project-scoped para todos los agentes soportados. Usa `sfao install --user --platform all` solo cuando quieres una instalacion Codex/Claude a nivel usuario.

## Comandos Principales

```bash
sfao version
sfao install
sfao install --project --platform all
sfao update --project --platform all
sfao uninstall --project --platform all --yes
sfao doctor
sfao doctor --verbose
sfao validate
sfao validate --json
sfao knowledge init --project-root .
sfao knowledge refresh --project-root .
sfao knowledge init --project-root . --scan-root
sfao knowledge doctor --project-root .
sfao memory init --project-root .
sfao memory add --project-root . --task-type bugfix --summary "..."
sfao memory compact --project-root . --max-bytes 60000
sfao memory doctor --project-root .
sfao version-context scaffold
sfao version-context update
sfao version-context validate --max-age-days 90
```

Para operaciones con org, el agente debe pedir un alias explicito. Las orgs de produccion son read-only mediante los guardrails de la skill.

## Flujo Del Agente

Los agentes instalados deben seguir las mismas fases visibles para preguntas informativas, bugfixes, implementaciones, arquitectura, reviews, inspeccion de org y releases:

1. `Request review`
2. `Planning evidence`
3. `Approval`
4. `Implementation`
5. `Validation`
6. `Completion`

En cada fase el agente debe indicar el tool o comando que esta usando o planeando. Para acceso Salesforce CLI debe mostrar la forma compacta del comando `sfao`, `scripts/sf_agent_cli.py` o `sf`, con alias y secretos redactados.

Para preguntas solo informativas, sin decision de proyecto, acceso a org, inspeccion de metadata, deploy, operaciones de datos, secretos, acciones destructivas, afirmaciones sensibles a release, implementacion o bugfix, el agente puede usar modo compacto: `Request review`, `Evidence`, `Answer`, `Validation`.

## Seguridad

- Preferir configuracion Salesforce, Flow, permission sets, UI API/LDS, named credentials y managed packages antes que codigo custom.
- Consultar la Knowledge local antes de cambiar metadata Salesforce.
- Usar `.salesforce-agent-knowledge/memory.md` para decisiones duraderas, lecciones, riesgos y follow-ups. Es memoria curada del proyecto, no un log bruto, y no debe contener secretos, datos de cliente, registros brutos ni logs grandes.
- Knowledge usa por defecto las `packageDirectories` de Salesforce DX cuando existen; usar `--scan-root` solo para un escaneo amplio intencional.
- La guia especializada Apex, LWC, Flow, SOQL, deploy y data operations se carga solo cuando es relevante.
- Skills Salesforce externas son referencias opcionales si ya estan disponibles y nunca pueden saltarse los guardrails SFAO.
- `safe-run --safety` no puede bajar la clasificacion automatica de riesgo.
- Aplicar least privilege antes de cambios en acceso, sharing, UI, packages, integraciones o automatizaciones.
- No recuperar ni parsear todos los metadata de la org salvo peticion amplia o necesidad real.
- No borrar datos o metadata sin aprobacion separada para el alcance exacto.
- No exponer secretos Salesforce ni datos de cliente sin aprobacion separada para el alcance exacto.
- Generar `package.xml` para metadata agregados o modificados.
- Despues de implementar, preguntar si se deben generar release notes, especificaciones tecnicas, impact assessment, user testing y manual procedures.

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

Alternativas:

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

## Mas Documentacion

Los detalles de instalacion, comandos, troubleshooting, publishing, release y versioning estan en `docs/wiki/`.

## Licencia

MIT. Cualquiera puede usar, copiar, modificar, distribuir y hacer fork de este repositorio bajo los terminos de `LICENSE`.
