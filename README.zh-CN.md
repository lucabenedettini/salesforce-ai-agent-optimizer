# Salesforce AI Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | 简体中文

Salesforce AI Agent Optimizer 是一个采用 MIT 许可证的公开 AI Agent 技能包，用于 Salesforce 项目。它帮助 Codex、Claude Code、GitHub Copilot 以及类似 Agent 规划、实现、验证、打包和记录 Salesforce 变更，同时保持上下文精简并应用强安全护栏。

公开仓库名称是 **Salesforce AI Agent Optimizer**。Codex 技能名称保持为 `salesforce-agent-optimizer`。

当前版本：`0.4.0`

## 核心原则

- Salesforce 优先：优先使用标准能力、配置、Flow、Permission Set、LDS/UI API、Named Credential 和托管包能力，再考虑自定义 Apex、LWC、Trigger 或集成。
- Token 高效：使用渐进式披露、本地 Knowledge、紧凑 CLI 输出、定向源码读取和最小补丁。
- 本地 Knowledge：`/sf-init-project-skill` 会创建面向 Agent 的紧凑 Markdown 元数据索引，灵感来自 LLM wiki 模式。
- Agent 原生 CLI：`scripts/sf_agent_cli.py` 封装官方 Salesforce CLI，提供显式 org alias、紧凑 JSON、敏感信息脱敏、dry-run、生产只读和删除审批 enforcement。
- 不编造：如果证据不足，Agent 必须询问用户，或给出多个场景和取舍让用户选择。

## 安全护栏

- 通过 facade 执行时，生产 org 对 write、execute 和 destructive 操作保持只读。
- 所有 org、data、metadata 命令都必须使用显式 target org alias。
- 破坏性操作绝不能自动执行。数据删除、元数据删除、package uninstall、source delete、purge、hard delete、`destructiveChanges.xml` 部署，都必须针对精确范围获得单独用户审批。
- 用户批准后，CLI 仍会要求提供以下精确 flag：

```bash
--delete-approval "I explicitly approve this deletion"
```

- 被删除的元数据应放在 `destructiveChanges.xml`，不要放进 `package.xml`。
- 如果记录范围、元数据依赖、package 版本或 org 行为不明确，Agent 必须询问用户或提供选项。

## 主要命令

创建或刷新项目 Knowledge：

```text
/sf-init-project-skill
```

从 Salesforce 官方来源刷新 release/API/SOAP/package 版本上下文：

```text
/sf-version-update-skill
```

运行本地测试：

```bash
python scripts/self_test.py --json
```

为新增或修改的元数据生成 package manifest：

```bash
python scripts/generate_package_manifest.py --project-root . --output release-artifacts/<date>-<change>/package.xml --from-git-status
```

查看目标 org 中已安装的 package：

```bash
python scripts/sf_agent_cli.py package-installed-list --target-org <alias> --select result
```

只有在明确审批后才删除记录：

```bash
python scripts/sf_agent_cli.py data-record-delete --target-org <alias> --sobject Account --record-id 001... --delete-approval "I explicitly approve this deletion"
```

## 安装

向 Codex 提出请求：

```text
Install the Salesforce AI Agent Optimizer skill from https://github.com/lucabenedettini/salesforce-ai-agent-optimizer
```

Codex 安装命令：

```bash
python <codex-home>/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo lucabenedettini/salesforce-ai-agent-optimizer --path . --name salesforce-agent-optimizer
```

Claude Code：

- 将 `agents/claude-code.md` 合并到 `CLAUDE.md`。
- 将 `agents/sf-init-project-skill.md` 复制到 `.claude/commands/sf-init-project-skill.md`。
- 将 `agents/sf-version-update-skill.md` 复制到 `.claude/commands/sf-version-update-skill.md`。

GitHub Copilot：

- 将 `agents/github-copilot-instructions.md` 合并到 `.github/copilot-instructions.md`，或使用 `.github/instructions/salesforce-agent-optimizer.instructions.md`。

## 前置条件

- Python 3.10+。
- Git。
- 用于 Knowledge、deploy、retrieve 或 manifest 工作流的 Salesforce DX 项目。
- 用于 org 操作的官方 Salesforce CLI，命令名为 `sf`。
- 已认证的 org alias。Agent 必须询问 alias，不能依赖 default org。
- write/execute 操作需要 sandbox。生产环境只读。

可选：

- PyYAML，用于 Codex skill 校验。
- Node.js/npm，用于 `npm install -g @salesforce/cli`。
- Go 和 `cli-printing-press`，仅用于 CLI 实验。

## 版本上下文

已在 2026-06-03 验证：

- Salesforce release：Summer '26。
- Platform API、Metadata API、SOAP API：`67.0`。
- SOAP API `login()` 在 API `65.0+` 中不可用；Salesforce 已宣布在 Summer '27 退役 API `31.0-64.0` 的 SOAP `login()`。
- 托管包版本取决于目标 org。不要假设 namespace、对象名称或功能可用性，先检查已安装 package。

权威资源：

- `references/salesforce-current-version.md`
- `references/salesforce-version.json`
- `references/version-update.md`

## 验证与交付

交付方法要求：

- 复述用户请求。
- 只在必要时提出聚焦问题。
- 识别相关 Salesforce 产品、package 和元数据依赖。
- 规划最小变更并请求批准。
- 对破坏性操作单独请求审批。
- 只实现已批准的工作。
- 为新增或修改的元数据生成 `package.xml`。
- 提供 release notes、technical specifications、impact assessment、user testing 和 manual procedures 的可选生成。
- 使用测试或验证子 Agent 进行验证。
- 验证通过后再询问是否 push 以及 push 到哪个 branch。

## 关键文件

- `SKILL.md`：核心技能说明。
- `agents/`：Codex、Claude Code、GitHub Copilot 和 slash command 适配器。
- `references/`：Salesforce 架构、产品、CLI、测试、删除、版本和交付的渐进式参考资料。
- `scripts/sf_agent_cli.py`：安全 Salesforce CLI facade。
- `scripts/sf_knowledge_init.py`：本地元数据 Knowledge 生成器。
- `scripts/generate_package_manifest.py`：`package.xml` 生成器。
- `scripts/git_knowledge_push.py`：带 Knowledge history 的远程 push。
- `scripts/self_test.py`：跨平台本地测试。

## 官方来源

- Salesforce CLI: https://developer.salesforce.com/tools/salesforcecli
- Salesforce CLI reference: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- Metadata API deploy and destructive changes: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy.htm
- GraphQL delete record: https://developer.salesforce.com/docs/platform/graphql/guide/mutations-delete.html
- LWC `deleteRecord`: https://developer.salesforce.com/docs/platform/lwc/guide/reference-delete-record.html
- Salesforce release notes: https://help.salesforce.com/s/articleView?id=release-notes.salesforce_release_notes.htm&language=en_US&type=5

## 许可证

MIT。任何人都可以在 `LICENSE` 条款下使用、复制、修改、分发和 fork 本仓库。
