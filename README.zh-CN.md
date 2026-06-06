# Salesforce Agent Optimizer

[English](README.md) | [Italiano](README.it.md) | [Espanol](README.es.md) | [Simplified Chinese](README.zh-CN.md)

Salesforce Agent Optimizer 是一个 MIT 许可的 `sfao` CLI 和 agent skill，面向 Codex、Claude Code 与 GitHub Copilot。

当前版本：`2.0.0`

它帮助 AI agent 在 Salesforce 项目中执行 Salesforce-first 规划、配置优先于自定义代码、最小且可回滚的变更、本地 Knowledge、token-efficient Salesforce CLI 使用、最小权限、显式 org alias、`package.xml` 管理和破坏性操作 guardrail。

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

`sfao install` 会为所有支持的 agent 安装 project-scoped adapters。只有在需要用户级 Codex/Claude 安装时才使用 `sfao install --user --platform all`。

## Main Commands

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
sfao knowledge doctor --project-root .
sfao version-context scaffold
sfao version-context update
sfao version-context validate
```

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

## Safety

- 优先使用 Salesforce configuration、Flow、permission set、UI API/LDS、named credential 和 managed package，再考虑自定义代码。
- 修改 Salesforce metadata 前先查询本地 Knowledge。
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
