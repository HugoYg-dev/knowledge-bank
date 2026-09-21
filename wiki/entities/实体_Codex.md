---
type: entity
tags:
- AI-Agent/coding
summary: OpenAI 推出的代码生成与编码智能体系统，代表了典型的声明式插件架构（静态文件/MCP配置/外部进程调度）与硬编码控制流设计。
sources:
- wiki/sources/Firecrawl 新工具开源，anydoc，将各种输入转换为md.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
updated: '2026-08-20'
---
# 实体：Codex

## 简介

**Codex** 是由 OpenAI 推出的代码生成模型与编码智能体系统（涵盖早期 Codex 代码模型以及后续集成于 ChatGPT / OpenAI 编码智能体客户端的完整 Harness 实现）。在开源智能体架构对比中，Codex 常作为开源可逐行分析的基准，代表了经典的**声明式插件模型（Declarative Plugin Model）**。

## 架构特征：声明式插件模型

1. **静态文件与声明性资源**：
   - Codex 的插件系统基于磁盘文件系统构建。插件以文件夹形式组织，包含 Markdown 格式的 Skill 描述文件、启动 MCP（Model Context Protocol）Server 的 JSON 配置、以及事件触发时执行的 Shell 脚本；
   - 插件本身不向 Harness 核心进程注入运行代码，Harness 仅按需读取配置并由操作系统拉起独立的子进程，插件间相互独立解耦。
2. **轻量与低门槛**：
   - 编写插件门槛极低，只需放置格式正确的静态文件；更新或替换工具（如从 [[entities/实体_Tavily|Tavily]] 切换到 Brave Search）仅需修改配置并重启子进程（2–3 秒完成），用户无感。
3. **控制流硬编码与扩展边界**：
   - 核心控制流 `run_turn()` 编译在 Rust 核心二进制中：严格按“采样前压缩 $\rightarrow$ 上下文组装 $\rightarrow$ 模型请求 $\rightarrow$ 工具执行”串行运转；
   - 外部扩展仅限于预设的 Contributor Trait 和 Hook 插槽（如请求前后微调 Prompt），无法在运行时动态将控制流重构为多 Agent 协作循环或并行流式循环。

## 与 DSH 命令式模型的对比

| 架构维度 | Codex（声明式） | DeepSeek DSH（命令式） |
| :--- | :--- | :--- |
| **插件形态** | 磁盘文件 + 外部独立进程 | 进程内 TypeScript 状态对象 |
| **状态持久性** | 无状态或子进程自管 | 进程内跨 Turn 状态维护与依赖注入 |
| **Agent Loop** | `run_turn()` 硬编码控制流 | `ctx.agentLoop` 作为可热替换插件 |
| **适用场景** | 日常辅助编码、常规工具与 Skill 调度 | 复杂运行时状态管理、Agent 自主代码修改与自进化 |

## 关联页面
- **同类编码系统**：[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]
- **核心概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]
- **相关工具**：[[entities/实体_Tavily|Tavily]]

## 来源与参考
- [[sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重|OpenAI前VP Lilian Weng：AI自我改进的近路不是改权重]]
- [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
