# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer æ˜¯ä¸€ä¸ª MIT è®¸å¯çš„ `sfao` CLI å’Œ agent skillï¼Œé¢å‘ Codexã€Claude Code ä¸Ž GitHub Copilotã€‚

å½“å‰ç‰ˆæœ¬ï¼š`2.2.4`

å®ƒå¸®åŠ© AI agent åœ¨ Salesforce é¡¹ç›®ä¸­æ‰§è¡Œ Salesforce-first è§„åˆ’ã€é…ç½®ä¼˜å…ˆäºŽè‡ªå®šä¹‰ä»£ç ã€æœ€å°ä¸”å¯å›žæ»šçš„å˜æ›´ã€æœ¬åœ° Knowledgeã€token-efficient Salesforce CLI ä½¿ç”¨ã€least privilegeã€æ˜¾å¼ org aliasã€`package.xml` ç®¡ç†å’Œç ´åæ€§æ“ä½œ guardrailã€‚

Specialized Salesforce guidance includes Apex, LWC, Flow, SOQL, deploy, data operations, and Agentforce; each file is loaded only when relevant and coordinates with the existing SFAO references.

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

æŽ¨èä½¿ç”¨ `uv tool install` æˆ– `python -m pipx install` è¿›è¡Œéš”ç¦» CLI å®‰è£…ã€‚éœ€è¦æŠŠ `sfao` å®‰è£…åˆ°å½“å‰ Python çŽ¯å¢ƒæ—¶ï¼Œä¹Ÿå¯ä»¥ä½¿ç”¨ `python -m pip install`ã€‚

## Install

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao validate
```

æ›¿ä»£æ–¹å¼ï¼š

```bash
python -m pipx install salesforce-agent-optimizer
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
```

`sfao install` ä¼šä¸ºæ‰€æœ‰æ”¯æŒçš„ agent å®‰è£… project-scoped adaptersï¼Œå¹¶åœ¨é¡¹ç›®æ ¹ç›®å½•å®‰è£…æ‰˜ç®¡çš„ `references/` å’Œ `scripts/`ï¼›agent ä¼šä¼˜å…ˆä½¿ç”¨è¿™äº›æ ¹ç›®å½•èµ„æºï¼Œå¹¶åœ¨éœ€è¦æ—¶å›žé€€åˆ° adapter å†…çš„ skill æœ¬åœ°ç›®å½•ã€‚åªæœ‰éœ€è¦ç”¨æˆ·çº§ Codex/Claude å®‰è£…æ—¶æ‰ä½¿ç”¨ `sfao install --user --platform all`ã€‚

## Main Commands

| Command | åŠŸèƒ½ä¸Žä½¿ç”¨æ—¶æœº | Principle |
| --- | --- | --- |
| `sfao version` | æ˜¾ç¤ºå·²å®‰è£…ç‰ˆæœ¬ã€‚å®‰è£…æˆ–å‡çº§åŽä½¿ç”¨ã€‚ | ç‰ˆæœ¬æ¸…æ™°ã€‚ |
| `sfao install` | åœ¨å½“å‰ repo å®‰è£… project-scoped agent adaptersã€‚æ¯ä¸ª Salesforce é¡¹ç›®é¦–æ¬¡ä½¿ç”¨ã€‚ | ä½Žæ‘©æ“¦å®‰è£…ã€‚ |
| `sfao install --project --platform all` | æ˜¾å¼å®‰è£… Codexã€Claude Codeã€GitHub Copilot adaptersã€‚repo onboarding æ—¶ä½¿ç”¨ã€‚ | Agent å…¼å®¹æ€§ã€‚ |
| `sfao update --project --platform all` | å‡çº§åŒ…åŽåˆ·æ–°ç”Ÿæˆçš„ adapters ä¸Ž templatesã€‚ | å®‰å…¨å‡çº§ã€‚ |
| `sfao uninstall --project --platform all --yes` | åªåˆ é™¤ SFAO ç”Ÿæˆæ–‡ä»¶ã€‚ç§»é™¤é¡¹ç›® skill æ—¶ä½¿ç”¨ã€‚ | å¯é€†å˜æ›´ã€‚ |
| `sfao doctor` | æ£€æŸ¥ Pythonã€OSã€Gitã€Salesforce CLIã€adaptersã€PATH ä¸ŽéªŒè¯çŠ¶æ€ã€‚å®‰è£…/å‡çº§åŽæˆ– skill ä¸å¯è§æ—¶ä½¿ç”¨ã€‚ | æ—©æœŸè¯Šæ–­ã€‚ |
| `sfao doctor --verbose` | è¾“å‡ºè¯¦ç»†è¯Šæ–­ã€‚æŽ’æŸ¥ warnings æ—¶ä½¿ç”¨ã€‚ | é€æ˜Žåˆ†æžã€‚ |
| `sfao validate` | éªŒè¯ skill æ–‡ä»¶ã€ç‰ˆæœ¬ã€ç”Ÿæˆ adaptersã€æ ¼å¼å’Œ Salesforce metadata guardrailsã€‚commit/release å‰ä½¿ç”¨ã€‚ | è´¨é‡é—¨ç¦ã€‚ |
| `sfao validate --json` | è¾“å‡ºæœºå™¨å¯è¯»éªŒè¯ç»“æžœã€‚CI æˆ– agent validation é˜¶æ®µä½¿ç”¨ã€‚ | è‡ªåŠ¨åŒ–å‹å¥½ã€‚ |
| `sfao report --project-root .` | ç”Ÿæˆæœ¬åœ° Markdown health snapshotï¼Œè¦†ç›– adaptersã€Knowledgeã€memoryã€guardrailsã€guidanceã€evals ä¸Ž version contextã€‚planning æˆ– handoff å‰ä½¿ç”¨ã€‚ | å¯è§‚å¯Ÿçš„æœ¬åœ°çŠ¶æ€ã€‚ |
| `sfao knowledge init --project-root .` | åˆ›å»ºç´§å‡‘çš„æœ¬åœ° Salesforce é¡¹ç›® Knowledgeã€‚ç¬¬ä¸€æ¬¡ planning å‰ä½¿ç”¨ã€‚ | å…ˆ Knowledgeï¼ŒåŽåŽŸå§‹ metadataã€‚ |
| `sfao knowledge refresh --project-root .` | metadata å˜æ›´åŽåˆ·æ–° Knowledgeã€‚ | æ–°é²œ planning evidenceã€‚ |
| `sfao knowledge init --project-root . --scan-root` | æ‰§è¡Œæœ‰æ„çš„å¹¿èŒƒå›´æ‰«æã€‚ä»…åœ¨ `packageDirectories` ä¸å¤Ÿæ—¶ä½¿ç”¨ã€‚ | Token-efficient scopeã€‚ |
| `sfao knowledge doctor --project-root .` | æ£€æŸ¥ Knowledge ç»“æž„ã€‚Knowledge ç¼ºå¤±æˆ– stale æ—¶ä½¿ç”¨ã€‚ | å¯é æœ¬åœ°ä¸Šä¸‹æ–‡ã€‚ |
| `sfao memory init --project-root .` | åˆ›å»º curated project memoryã€‚å¼€å§‹æ²‰æ·€é¡¹ç›®ç»éªŒæ—¶ä½¿ç”¨ã€‚ | ç´§å‡‘æŒä¹…è®°å¿†ã€‚ |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | æ·»åŠ å·²è„±æ•çš„ lessonã€decisionã€risk æˆ– follow-upã€‚å®žçŽ°æˆ–éªŒè¯åŽä½¿ç”¨ã€‚ | ä¸å­˜åŽŸå§‹æ—¥å¿—ï¼Œä¸å­˜ secretsã€‚ |
| `sfao memory compact --project-root . --max-bytes 60000` | ä¿æŒ memory å°è€Œæœ‰ç”¨ã€‚memory è¿‡å¤§æ—¶ä½¿ç”¨ã€‚ | Token efficiencyã€‚ |
| `sfao memory doctor --project-root .` | éªŒè¯ memory ç»“æž„ä¸Žè„±æ•ã€‚planning å‰ä¾èµ– memory æ—¶ä½¿ç”¨ã€‚ | Privacy-safe memoryã€‚ |
| `sfao version-context scaffold` | ç¼ºå¤±æ—¶åˆ›å»º version-context æ–‡ä»¶ã€‚åˆå§‹åŒ– references æ—¶ä½¿ç”¨ã€‚ | å®˜æ–¹æ¥æºå‡†å¤‡ã€‚ |
| `sfao version-context update` | ä»Ž Salesforce å®˜æ–¹æ¥æºåˆ·æ–° release/API contextã€‚ä¸Šä¸‹æ–‡ stale æˆ– release-sensitive æ—¶ä½¿ç”¨ã€‚ | ä¸ç¼–é€ è¡Œä¸ºã€‚ |
| `sfao version-context validate --max-age-days 90` | æ£€æŸ¥ version-context æ–°é²œåº¦ã€‚éªŒè¯æˆ– release-sensitive planning å‰ä½¿ç”¨ã€‚ | å½“å‰ API evidenceã€‚ |
| `sfao command search "permission account"` | æœç´¢å†…éƒ¨å®‰å…¨ Salesforce CLI facade registryã€‚è¿è¡Œ org å‘½ä»¤å‰ä½¿ç”¨ã€‚ | å…ˆå‘çŽ°ï¼ŒåŽæ‰§è¡Œã€‚ |
| `sfao command payload-example access-inspect` | è¾“å‡ºæ³¨å†Œå‘½ä»¤çš„ç´§å‡‘ payload ç¤ºä¾‹ã€‚é¿å…ç¼–é€  flags æ—¶ä½¿ç”¨ã€‚ | Schema-guided commandsã€‚ |
| `sfao command execute --payload payload.json` | é€šè¿‡ guardrails æ‰§è¡Œæ³¨å†Œå‘½ä»¤ã€‚éœ€è¦ org æ—¶å¿…é¡»ä½¿ç”¨æ˜¾å¼ aliasã€‚ | å®‰å…¨ Salesforce CLI facadeã€‚ |
| `sfao soql build --object Account --fields Id,Name` | æž„å»ºèšç„¦ SOQL å’Œ `data-query` payloadã€‚æŸ¥è¯¢ org data å‰ä½¿ç”¨ã€‚ | æœ€å°æ•°æ®è¯»å–ã€‚ |
| `sfao permissions explain --input access.json` | åŸºäºŽ `access-inspect` è¾“å‡ºè§£é‡Šè®¿é—®è¯æ®ã€‚least-privilege planning æ—¶ä½¿ç”¨ã€‚ | å¯è§£é‡Šè®¿é—®ã€‚ |
| `sfao live-test --target-org <alias>` | å¯¹çœŸå®ž org æ‰§è¡Œ opt-in æ£€æŸ¥ã€‚write/destructive suite åªå¯åœ¨æ˜Žç¡® sandbox/scratch alias ä¸‹ä½¿ç”¨ã€‚ | ç»åŒæ„çš„çœŸå®žéªŒè¯ã€‚ |

æ‰§è¡Œ org æ“ä½œå‰ï¼Œagent å¿…é¡»è¯·æ±‚æ˜¾å¼ org aliasã€‚é€šè¿‡ skill guardrailï¼Œç”Ÿäº§ org å¯¹å†™å…¥å’Œç ´åæ€§æ“ä½œä¿æŒ read-onlyã€‚

## Agent Workflow

å®‰è£…åŽçš„ agent å¯¹ä¿¡æ¯æŸ¥è¯¢ã€bugfixã€å®žçŽ°ã€æž¶æž„ã€reviewã€org inspection å’Œ release work éƒ½å¿…é¡»ä½¿ç”¨ç›¸åŒçš„å¯è§é˜¶æ®µï¼š

1. `Request review`
2. `Planning evidence`
3. `Approval`
4. `Implementation`
5. `Validation`
6. `Completion`

æ¯ä¸ªé˜¶æ®µéƒ½å¿…é¡»è¯´æ˜Žæ­£åœ¨ä½¿ç”¨æˆ–è®¡åˆ’ä½¿ç”¨çš„ tool/commandã€‚è®¿é—® Salesforce CLI æ—¶ï¼Œå¿…é¡»å±•ç¤ºç®€æ´çš„ `sfao`ã€`scripts/sf_agent_cli.py` æˆ– `sf` å‘½ä»¤å½¢å¼ï¼Œå¹¶éšè— alias/secrets ä¸­çš„æ•æ„Ÿä¿¡æ¯ã€‚

å¯¹äºŽçº¯è¯´æ˜Žæ€§é—®é¢˜ï¼Œå¦‚æžœä¸æ¶‰åŠé¡¹ç›®å†³ç­–ã€org è®¿é—®ã€metadata æ£€æŸ¥ã€deployã€æ•°æ®æ“ä½œã€secretsã€ç ´åæ€§æ“ä½œã€release-sensitive åˆ¤æ–­ã€å®žçŽ°æˆ– bugfixï¼Œagent å¯ä»¥ä½¿ç”¨ç´§å‡‘æ¨¡å¼ï¼š`Request review`ã€`Evidence`ã€`Answer`ã€`Validation`ã€‚

## Safety

- ä¼˜å…ˆä½¿ç”¨ Salesforce configurationã€Flowã€permission setã€UI API/LDSã€named credential å’Œ managed packageï¼Œå†è€ƒè™‘è‡ªå®šä¹‰ä»£ç ã€‚
- ä¿®æ”¹ Salesforce metadata å‰å…ˆæŸ¥è¯¢æœ¬åœ° Knowledgeã€‚
- ä½¿ç”¨ `.salesforce-agent-knowledge/memory.md` ä¿å­˜é¡¹ç›®æœ¬åœ°çš„æŒä¹…å†³ç­–ã€ç»éªŒã€é£Žé™©å’Œ follow-upã€‚å®ƒæ˜¯ curated planning knowledgeï¼Œä¸æ˜¯åŽŸå§‹æ—¥å¿—ï¼Œä¸èƒ½åŒ…å« secretsã€å®¢æˆ·æ•°æ®ã€åŽŸå§‹è®°å½•æˆ–å¤§æ—¥å¿—ã€‚
- Knowledge é»˜è®¤ä½¿ç”¨ Salesforce DX `packageDirectories`ï¼›åªæœ‰éœ€è¦æœ‰æ„è¿›è¡Œå…¨é¡¹ç›®æ‰«ææ—¶æ‰ä½¿ç”¨ `--scan-root`ã€‚
- Apexã€LWCã€Flowã€SOQLã€deployã€data operations å’Œ Agentforce çš„ä¸“é¡¹ guidance åªåœ¨ç›¸å…³ä»»åŠ¡ä¸­åŠ è½½ã€‚
- å¤–éƒ¨ Salesforce skills åªèƒ½ä½œä¸ºå·²å®‰è£…æ—¶çš„å¯é€‰å‚è€ƒï¼Œä¸èƒ½ç»•è¿‡ SFAO guardrailsã€‚
- `safe-run --safety` ä¸èƒ½é™ä½Žè‡ªåŠ¨é£Žé™©åˆ†ç±»ã€‚
- åœ¨è®¿é—®ã€sharingã€UIã€packageã€integration æˆ– automation å˜æ›´å‰åº”ç”¨ least privilegeã€‚
- é™¤éžç”¨æˆ·è¦æ±‚å¹¿æ³›åˆ†æžæˆ–ä»»åŠ¡ç¡®å®žéœ€è¦ï¼Œä¸è¦æ£€ç´¢æˆ–è§£æžå…¨éƒ¨ org metadataã€‚
- æœªèŽ·å¾—é’ˆå¯¹ç¡®åˆ‡èŒƒå›´çš„å•ç‹¬æ‰¹å‡†ï¼Œä¸å¾—åˆ é™¤æ•°æ®æˆ– metadataã€‚
- æœªèŽ·å¾—é’ˆå¯¹ç¡®åˆ‡èŒƒå›´çš„å•ç‹¬æ‰¹å‡†ï¼Œä¸å¾—æš´éœ² Salesforce secrets æˆ–å®¢æˆ·æ•°æ®ã€‚
- å¯¹æ–°å¢žæˆ–ä¿®æ”¹çš„ metadata ç”Ÿæˆ `package.xml`ã€‚
- å®žçŽ°åŽè¯¢é—®æ˜¯å¦ç”Ÿæˆ release notesã€technical specificationsã€impact assessmentã€user testing å’Œ manual proceduresã€‚

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

æ›¿ä»£æ–¹å¼ï¼š

```bash
python -m pipx upgrade salesforce-agent-optimizer
python -m pip install --upgrade salesforce-agent-optimizer
```

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

æ›¿ä»£æ–¹å¼ï¼š

```bash
python -m pipx uninstall salesforce-agent-optimizer
```

## More Documentation

å®‰è£…ã€å‘½ä»¤ã€troubleshootingã€publishingã€release å’Œ versioning çš„è¯¦ç»†æ–‡æ¡£ä½äºŽ `docs/wiki/`ã€‚

## License

MITã€‚ä»»ä½•äººéƒ½å¯ä»¥åœ¨ `LICENSE` æ¡æ¬¾ä¸‹ä½¿ç”¨ã€å¤åˆ¶ã€ä¿®æ”¹ã€åˆ†å‘å’Œ fork æœ¬ä»“åº“ã€‚
