# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer 是一个 MIT 许可的 `sfao` CLI 和 agent skill，面向 Codex、Claude Code 与 GitHub Copilot。

当前版本：`2.1.1`

它帮助 AI agent 在 Salesforce 项目中执行 Salesforce-first 规划、配置优先于自定义代码、最小且可回滚的变更、本地 Knowledge、token-efficient Salesforce CLI 使用、least privilege、显式 org alias、`package.xml` 管理和破坏性操作 guardrail。

## Quick Start

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao knowledge init --project-root .
sfao doctor
```

推荐使用 `uv tool install` 或 `python -m pipx install` 进行隔离 CLI 安装。需要把 `sfao` 安装到当前 Python 环境时，也可以使用 `python -m pip install`。

## Install

```bash
uv tool install salesforce-agent-optimizer
sfao install
sfao validate
```

替代方式：

```bash
python -m pipx install salesforce-agent-optimizer
python -m pip install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
uv tool install git+https://github.com/lucabenedettini/salesforce-ai-agent-optimizer.git
```

`sfao install` 会为所有支持的 agent 安装 project-scoped adapters。只有需要用户级 Codex/Claude 安装时才使用 `sfao install --user --platform all`。

## Main Commands

| Command | 功能与使用时机 | Principle |
| --- | --- | --- |
| `sfao version` | 显示已安装版本。安装或升级后使用。 | 版本清晰。 |
| `sfao install` | 在当前 repo 安装 project-scoped agent adapters。每个 Salesforce 项目首次使用。 | 低摩擦安装。 |
| `sfao install --project --platform all` | 显式安装 Codex、Claude Code、GitHub Copilot adapters。repo onboarding 时使用。 | Agent 兼容性。 |
| `sfao update --project --platform all` | 升级包后刷新生成的 adapters 与 templates。 | 安全升级。 |
| `sfao uninstall --project --platform all --yes` | 只删除 SFAO 生成文件。移除项目 skill 时使用。 | 可逆变更。 |
| `sfao doctor` | 检查 Python、OS、Git、Salesforce CLI、adapters、PATH 与验证状态。安装/升级后或 skill 不可见时使用。 | 早期诊断。 |
| `sfao doctor --verbose` | 输出详细诊断。排查 warnings 时使用。 | 透明分析。 |
| `sfao validate` | 验证 skill 文件、版本、生成 adapters、格式和 Salesforce metadata guardrails。commit/release 前使用。 | 质量门禁。 |
| `sfao validate --json` | 输出机器可读验证结果。CI 或 agent validation 阶段使用。 | 自动化友好。 |
| `sfao knowledge init --project-root .` | 创建紧凑的本地 Salesforce 项目 Knowledge。第一次 planning 前使用。 | 先 Knowledge，后原始 metadata。 |
| `sfao knowledge refresh --project-root .` | metadata 变更后刷新 Knowledge。 | 新鲜 planning evidence。 |
| `sfao knowledge init --project-root . --scan-root` | 执行有意的广范围扫描。仅在 `packageDirectories` 不够时使用。 | Token-efficient scope。 |
| `sfao knowledge doctor --project-root .` | 检查 Knowledge 结构。Knowledge 缺失或 stale 时使用。 | 可靠本地上下文。 |
| `sfao memory init --project-root .` | 创建 curated project memory。开始沉淀项目经验时使用。 | 紧凑持久记忆。 |
| `sfao memory add --project-root . --task-type bugfix --summary "..."` | 添加已脱敏的 lesson、decision、risk 或 follow-up。实现或验证后使用。 | 不存原始日志，不存 secrets。 |
| `sfao memory compact --project-root . --max-bytes 60000` | 保持 memory 小而有用。memory 过大时使用。 | Token efficiency。 |
| `sfao memory doctor --project-root .` | 验证 memory 结构与脱敏。planning 前依赖 memory 时使用。 | Privacy-safe memory。 |
| `sfao version-context scaffold` | 缺失时创建 version-context 文件。初始化 references 时使用。 | 官方来源准备。 |
| `sfao version-context update` | 从 Salesforce 官方来源刷新 release/API context。上下文 stale 或 release-sensitive 时使用。 | 不编造行为。 |
| `sfao version-context validate --max-age-days 90` | 检查 version-context 新鲜度。验证或 release-sensitive planning 前使用。 | 当前 API evidence。 |
| `sfao command search "permission account"` | 搜索内部安全 Salesforce CLI facade registry。运行 org 命令前使用。 | 先发现，后执行。 |
| `sfao command payload-example access-inspect` | 输出注册命令的紧凑 payload 示例。避免编造 flags 时使用。 | Schema-guided commands。 |
| `sfao command execute --payload payload.json` | 通过 guardrails 执行注册命令。需要 org 时必须使用显式 alias。 | 安全 Salesforce CLI facade。 |
| `sfao soql build --object Account --fields Id,Name` | 构建聚焦 SOQL 和 `data-query` payload。查询 org data 前使用。 | 最小数据读取。 |
| `sfao permissions explain --input access.json` | 基于 `access-inspect` 输出解释访问证据。least-privilege planning 时使用。 | 可解释访问。 |
| `sfao live-test --target-org <alias>` | 对真实 org 执行 opt-in 检查。write/destructive suite 只可在明确 sandbox/scratch alias 下使用。 | 经同意的真实验证。 |

执行 org 操作前，agent 必须请求显式 org alias。通过 skill guardrail，生产 org 对写入和破坏性操作保持 read-only。

## Agent Workflow

安装后的 agent 对信息查询、bugfix、实现、架构、review、org inspection 和 release work 都必须使用相同的可见阶段：

1. `Request review`
2. `Planning evidence`
3. `Approval`
4. `Implementation`
5. `Validation`
6. `Completion`

每个阶段都必须说明正在使用或计划使用的 tool/command。访问 Salesforce CLI 时，必须展示简洁的 `sfao`、`scripts/sf_agent_cli.py` 或 `sf` 命令形式，并隐藏 alias/secrets 中的敏感信息。

对于纯说明性问题，如果不涉及项目决策、org 访问、metadata 检查、deploy、数据操作、secrets、破坏性操作、release-sensitive 判断、实现或 bugfix，agent 可以使用紧凑模式：`Request review`、`Evidence`、`Answer`、`Validation`。

## Safety

- 优先使用 Salesforce configuration、Flow、permission set、UI API/LDS、named credential 和 managed package，再考虑自定义代码。
- 修改 Salesforce metadata 前先查询本地 Knowledge。
- 使用 `.salesforce-agent-knowledge/memory.md` 保存项目本地的持久决策、经验、风险和 follow-up。它是 curated planning knowledge，不是原始日志，不能包含 secrets、客户数据、原始记录或大日志。
- Knowledge 默认使用 Salesforce DX `packageDirectories`；只有需要有意进行全项目扫描时才使用 `--scan-root`。
- Apex、LWC、Flow、SOQL、deploy 和 data operations 的专项 guidance 只在相关任务中加载。
- 外部 Salesforce skills 只能作为已安装时的可选参考，不能绕过 SFAO guardrails。
- `safe-run --safety` 不能降低自动风险分类。
- 在访问、sharing、UI、package、integration 或 automation 变更前应用 least privilege。
- 除非用户要求广泛分析或任务确实需要，不要检索或解析全部 org metadata。
- 未获得针对确切范围的单独批准，不得删除数据或 metadata。
- 未获得针对确切范围的单独批准，不得暴露 Salesforce secrets 或客户数据。
- 对新增或修改的 metadata 生成 `package.xml`。
- 实现后询问是否生成 release notes、technical specifications、impact assessment、user testing 和 manual procedures。

## Update

```bash
uv tool upgrade salesforce-agent-optimizer
sfao update --project --platform all
sfao doctor
```

替代方式：

```bash
python -m pipx upgrade salesforce-agent-optimizer
python -m pip install --upgrade salesforce-agent-optimizer
```

## Uninstall

```bash
sfao uninstall --project --platform all --yes
uv tool uninstall salesforce-agent-optimizer
```

替代方式：

```bash
python -m pipx uninstall salesforce-agent-optimizer
```

## More Documentation

安装、命令、troubleshooting、publishing、release 和 versioning 的详细文档位于 `docs/wiki/`。

## License

MIT。任何人都可以在 `LICENSE` 条款下使用、复制、修改、分发和 fork 本仓库。
