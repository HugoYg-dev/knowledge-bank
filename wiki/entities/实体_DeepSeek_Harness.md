---
type: entity
tags:
- AI-Agent/coding
summary: DeepSeek 开源的基于 Cordis 微内核的智能体 SDK 与应用框架，采用命令式插件与“一切皆插件”架构，支持 Agent Loop 运行时热替换、四大预设模式、权威
  Session Log 与自进化（Self-Harness）。
sources:
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
updated: '2026-09-07'
---

# 实体：DeepSeek Harness

## 简介
**DeepSeek Harness（DSH）** 是由 [[entities/实体_DeepSeek-V3|DeepSeek]] 团队开源的生产级智能体构建、运行与扩展框架（SDK & Application Framework）。项目包含超过 230 个 workspace 成员包，建立在 [[entities/实体_Cordis|Cordis]] 微内核之上，贯彻“一切皆插件（Everything is a plugin）”的设计哲学，将模型、工具、会话、循环、界面和安全策略解耦为可插拔组件。

## 核心架构与设计原则

1. **命令式微内核与三层解构**：
   - 相比于 [[entities/实体_Codex|Codex]] 等采用外部进程与静态配置的声明式模型，DSH 采用**命令式插件模型**：插件直接运行在 Harness 进程内，持有内部状态并支持直接函数调用；
   - 系统运行于 Cordis Context 之上，将所有能力解耦为**接口（Interface）**、**实现（Implementation）**与**消费者（Consumer / Model Tool）**三层（如 Bash 接口 vs 本地进程实现 vs 模型 Tool Schema）；
   - 通过 `cordis.yml` 进行声明式组装，支持针对不同部署环境灵活替换模型适配器、存储后端与沙箱策略。
2. **Agent Loop 作为可插拔插件（运行时热替换）**：
   - 传统 Harness（如 Codex）将 `run_turn()` 控制流硬编码在核心二进制中，仅开放预设 Hook；
   - DSH 将 Agent Loop 置于 `packages/core/agent-loop` 中，自身即为普通插件，对外提供 `ctx.agentLoop` 服务，声明依赖 `ctx.systemPrompt` 与 `ctx.tools`。开发者或 AI 可通过实现相同接口的插件将其整体热替换（如切换单 Agent 循环为多 Agent 协作循环或并行流式调度），框架自动平滑撤销旧监听并切换新依赖。
3. **为 Agent 自进化（Self-Harness）提供物理插槽**：
   - DSH 复杂的命令式微内核架构（副作用跟踪、依赖响应、事务性 HMR）核心战略价值在于为 Agent 自我演化提供底层基础设施。
   - 当 Agent 在运行中自主编写新工具插件或新 Loop 代码时，框架可在不重启进程的前提下热加载，并在代码出错时通过事务性 HMR 回滚到稳定状态；同时 TypeScript 插件体系为大模型提供了完全可见的接口与上下文。
4. **四大预设运行模式**：
   - **标准模式**：全功能通用编码智能体，具备文件、Shell、搜索、Skills、子智能体与工作流；
   - **PTC 模式（Programmatic Tool Calling）**：通过 Code Mode SDK 编写 TypeScript 脚本，在单次 `run_code` 中批处理多步工具调用，大幅节省交互轮次与 Token；
   - **极简模式**：仅提供持久 Bash 与 `str_replace_editor` 双工具，降低上下文负担；
   - **创造模式**：基于自指 Cordis 机制，智能体可检查自身运行时插件树，动态挂载与卸载临时插件，实现受控的自修改与自进化（Self-Harness）。
5. **生命周期交通规则与调度器**：
   - 交互严格拆分为 Turn 与 Step；
   - 工具执行经前置策略、单调不可逆守卫、安全屏障（连续只读调用并行、修改状态调用独占屏障）与后置处理；
   - 支持消息排队与带回执确认的实时转向（Steering）。
6. **权威 Session Log（事件溯源唯一事实源）**：
   - 确立“凡是模型看见的，都必须能从日志中重建”原则；
   - 环境变量、Prompt 组装、流式 Chunk、工具调用/结果、权限切换全量写入追加式事件流，作为 Web/TUI 界面、持久化（JSONL/SQLite）、Resume 和 Fork 的统一事实源。
7. **Fail-Closed 深度安全体系**：
   - 默认采用 `workspace-write` 沙箱模式，将文件修改与 Shell 限制在工作区及安全临时目录；
   - 配合 `ask` 审批策略；遵循“失败关闭”原则（隔离无法确认时拒绝执行）。
8. **多形态交付**：
   - 提供 Web UI（127.0.0.1:3080）、终端 TUI、Headless 自动化模式及 ACP 协议 / JSON-RPC / Python SDK 入口。

9. **组合优先与生态解耦（vs LangChain）**：
   - LangChain 采用“框架优先”理念，高层抽象沉重且升级容易破坏兼容性；DSH 采用“组合优先”理念，依托 Cordis 元框架将适配器、注册表、循环逻辑全量插件化，无特权核心，模块可独立测试与热插拔。
10. **Meta-Harness 分布式调度**：
   - Harness 负责单个智能体实例内的模型交互、工具执行与会话状态；上层通过 **Meta-Harness** 统一管理多个 Harness 实例，执行算力资源调度、任务分发与跨实例状态同步。

## 关联页面
- **微内核底座**：[[entities/实体_Cordis|Cordis]]
- **所属团队**：[[entities/实体_DeepSeek|DeepSeek]]
- **同类智能体系统**：[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]
- **核心概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]、[[concepts/概念_Agent内存与状态管理|Agent 内存与状态管理]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]
- **支撑来源**：
  - [[sources/刚刚，DeepSeek Harness震撼开源：一切皆插件|刚刚，DeepSeek Harness震撼开源：一切皆插件]]
  - [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
