# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer es una CLI `sfao` y una skill para Codex, Claude Code y GitHub Copilot, publicada con licencia MIT.

Version actual: `2.2.4`

Ayuda a los agentes AI en proyectos Salesforce con planificacion Salesforce-first, configuracion antes que codigo custom, cambios minimos y reversibles, Knowledge local, uso eficiente de tokens con Salesforce CLI, least privilege, alias de org explicitos, conciencia de `package.xml` y guardrails para operaciones destructivas.

La guia Salesforce especializada incluye Apex, LWC, Flow, SOQL, deploy, data operations y Agentforce; cada archivo se carga solo cuando es relevante y coordina las referencias SFAO existentes.

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

`sfao install` instala adaptadores project-scoped para todos los agentes soportados. Tambien instala `references/` y `scripts/` gestionados en la raiz del proyecto; los agentes los usan primero y hacen fallback a las carpetas locales de la skill dentro del adaptador cuando sea necesario. Usa `sfao install --user --platform all` solo cuando quieres una instalacion Codex/Claude a nivel usuario.

## Comandos Principales

| Comando | Que hace y cuando usarlo | Principio |
| --- | --- | --- |
| `sfao version` | Muestra la version instalada. Usalo despues de install o upgrade. | Claridad de version. |
| `sfao install` | Instala adapters project-scoped para los agentes soportados. Usalo una vez por proyecto Salesforce. | Setup sin friccion. |
| `sfao install --project --platform all` | Instalacion explicita para Codex, Claude Code y GitHub Copilot. Usalo al incorporar un repo. | Compatibilidad de agentes. |
| `sfao update --project --platform all` | Actualiza adapters y templates generados despues de subir version del paquete. | Upgrade seguro. |
| `sfao uninstall --project --platform all --yes` | Elimina solo archivos SFAO generados. Usalo para quitar la skill del proyecto. | Cambios reversibles. |
| `sfao doctor` | Revisa Python, OS, Git, Salesforce CLI, adapters, PATH y validacion. Usalo despues de install/update o si la skill no aparece. | Diagnostico temprano. |
| `sfao doctor --verbose` | Muestra diagnostico detallado. Usalo para investigar warnings. | Analisis transparente. |
| `sfao validate` | Valida archivos skill, versiones, adapters generados, formatos y guardrails de metadata Salesforce. Usalo antes de commit/release. | Quality gate. |
| `sfao validate --json` | Produce validacion machine-readable. Usalo en CI o fases del agente. | Salida automatizable. |
| `sfao report --project-root .` | Escribe un health snapshot Markdown local para adapters, Knowledge, memory, guardrails, guidance, evals y version context. Usalo antes de planificar o hacer handoff. | Estado local observable. |
| `sfao knowledge init --project-root .` | Crea Knowledge local compacta del proyecto Salesforce. Usalo antes del primer planning. | Knowledge antes de metadata bruta. |
| `sfao knowledge refresh --project-root .` | Actualiza Knowledge despues de cambios metadata. | Evidencia de planning fresca. |
| `sfao knowledge init --project-root . --scan-root` | Ejecuta un escaneo amplio intencional. Usalo solo si `packageDirectories` no basta. | Scope eficiente en tokens. |
| `sfao knowledge doctor --project-root .` | Verifica estructura de Knowledge. Usalo si el agente reporta Knowledge faltante o stale. | Contexto local confiable. |
| `sfao memory init --project-root .` | Crea memoria curada de proyecto. Usalo para aprendizaje duradero. | Memoria compacta. |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | Agrega una leccion, decision, riesgo o follow-up redactado. Usalo tras implementacion o validacion. | Sin logs brutos ni secretos. |
| `sfao memory compact --project-root . --max-bytes 60000` | Mantiene la memoria pequena y util. Usalo cuando crece demasiado. | Eficiencia de tokens. |
| `sfao memory doctor --project-root .` | Valida estructura y redaccion de memoria. Usalo antes de usarla en planning. | Memoria privacy-safe. |
| `sfao version-context scaffold` | Crea archivos version-context si faltan. Usalo para bootstrap de referencias. | Preparacion de fuentes oficiales. |
| `sfao version-context update` | Actualiza release/API context desde fuentes oficiales Salesforce. Usalo cuando el contexto esta stale o es sensible a release. | No inventar comportamiento. |
| `sfao version-context validate --max-age-days 90` | Revisa frescura del version-context. Usalo en validacion o planning sensible a release. | Evidencia API actual. |
| `sfao command search "permission account"` | Busca en el registry interno seguro de la Salesforce CLI facade. Usalo antes de comandos org. | Descubrir antes de ejecutar. |
| `sfao command payload-example access-inspect` | Muestra un payload compacto para un comando registrado. Usalo para evitar flags inventados. | Comandos guiados por schema. |
| `sfao command execute --payload payload.json` | Ejecuta un comando registrado mediante guardrails compactos. Usalo solo con alias org explicito cuando sea requerido. | Salesforce CLI facade segura. |
| `sfao soql build --object Account --fields Id,Name` | Construye SOQL focalizado y payload `data-query`. Usalo antes de consultar datos org. | Recuperacion minima de datos. |
| `sfao permissions explain --input access.json` | Resume evidencia de acceso desde output `access-inspect`. Usalo para least-privilege planning. | Acceso explicable. |
| `sfao live-test --target-org <alias>` | Ejecuta pruebas opt-in contra org real. Usa write/destructive suite solo con alias sandbox/scratch explicito. | Validacion real con consentimiento. |

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
- La guia especializada Apex, LWC, Flow, SOQL, deploy, data operations y Agentforce se carga solo cuando es relevante.
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
