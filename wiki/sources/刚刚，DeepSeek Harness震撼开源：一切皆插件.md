---
type: source
tags:
- AI-Agent/coding
summary: DeepSeek 开源基于 Cordis 微内核的智能体框架 DeepSeek Harness，主张一切皆插件、权威 Session Log 事件源与严格生命周期调度管控。
sources:
- raw/articles/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
updated: '2026-08-20'
---

# 来源摘要：刚刚，DeepSeek Harness震撼开源：一切皆插件

## 来源元信息
- **标题**：刚刚，DeepSeek Harness震撼开源：一切皆插件
- **作者**：机器之心（编辑 Panda）
- **发布日期**：2026-08-13
- **原文链接**：https://mp.weixin.qq.com/s/mcVfdDVUVlEYJj61sJWKZA
- **开源仓库**：https://github.com/deepseek-ai/deepseek-harness

## 核心要点 (Key Takeaways)
1. **智能体 SDK 与微内核定位**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness]] 并非单一模型或简单 API 客户端，而是一套构建、运行和扩展智能体的工程 SDK 与应用框架（monorepo 包含 230+ workspace 模块）。项目基于 [[entities/实体_Cordis|Cordis]] 微内核，提出“一切皆插件（甚至 Agent Loop 本身也是插件）”的核心设计理念。
2. **三层能力解构与声明式装配**：将所有智能体能力严密解耦为**接口（Interface）**、**实现（Implementation）**与**消费者（Consumer / Model Tool）**三层。通过 `cordis.yml` 配置文件进行声明式组装，支持替换模型、沙箱、存储与安全策略，支持配置补丁与环境变量密钥解析（`$DSH_HOME/.credentials.yaml`）。
3. **四种 Agent 预设模式**：
   - **标准模式**：通用编码 Agent，配备文件编辑、Shell、搜索、Skills、计划/目标、子智能体与工作流；
   - **PTC 模式（Programmatic Tool Calling）**：通过 Code Mode SDK 让模型编写 TypeScript 代码并在单次 `run_code` 中批处理多步操作，大幅降低往返 Token 开销；
   - **极简模式**：仅提供持久 Bash 与 `str_replace_editor` 双工具，减少上下文负担；
   - **创造模式**：基于自指 Cordis 运行时检查与动态插件实验，允许智能体在受控边界内检查插件树并动态挂载/卸载临时插件以改装自身。
4. **生命周期交通规则与并发调度**：将交互划分为 Turn 与 Step 生命周期。工具调用执行前置策略、单调不可逆安全守卫、执行包装与后置处理；调度器支持连续只读任务并发执行，写操作则作为独占屏障（Barrier）；支持运行中消息排队与带回执的实时转向（Steering）。
5. **权威会话日志（Session Log 即唯一事实源）**：确立“凡是模型看见的内容，都必须能够从日志中重建”原则。系统环境、提示词组装、流式 Chunk、工具调用/结果、压缩事件与权限切换均作为事件写入追加式会话流，UI、持久化（JSONL/SQLite）、Resume、Fork 和回放均由此唯一事件源派生。
6. **深度安全策略与 Fail-Closed 原则**：默认采用 `workspace-write` 沙箱模式，将写操作和 Shell 严格限制在当前工作区与允许的临时目录；关键操作配合 `ask` 审批策略；遵循“失败关闭（Fail-Closed）”原则（无法确认隔离生效时拒绝执行而非退化运行）。
7. **多智能体作用域与工作流状态**：主 Agent 可将任务委派给子 Agent（支持全新实例、Fork 边界或 ACP 子进程），子 Agent 具有独立的上下文层与工具权限作用域；提供目标（Goal）、计划（Plan）、待办（Todo）和后台任务（Background Task）四大协作状态。

## 关键技术与机制解析

### 1. 微内核插件架构（Cordis Context）
DeepSeek Harness 将系统抽象为一个 Cordis Context，不同包向 Context 注册服务、事件和能力：
- `packages/core/`：定义 Session、System Prompt、Tools、Agent 及 Agent Loop；
- 能力包体系：`packages/llm/`（适配器）、`packages/shell/`、`packages/fs/`、`packages/lsp/`、`packages/web/`、`packages/skill/`、`packages/subagent/`、`packages/workflow/` 等；
- 论文支撑：《A Programming Paradigm for Spatiotemporal Composability》（时空可组合性编程范式）。

### 2. 产品形态多端矩阵
通过同一套 Harness 宿主与不同 Bundle 组装，输出：
- **Web UI**（默认监听 127.0.0.1:3080，含会话侧栏、权限选择、计划模式与工具卡片）；
- **TUI**（终端交互界面）；
- **Headless 模式**（单任务运行后打印结果退出，适合 CI/脚本）；
- **自动化协议**（ACP 协议服务与 JSON-RPC / Python SDK 入口）。

## 关联实体与概念
- **相关实体**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]、[[entities/实体_Cordis|Cordis]]、[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]、[[entities/实体_DeepSeek-V3|DeepSeek-V3]]、[[entities/实体_DeepSeek-R1|DeepSeek-R1]]
- **相关概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]、[[concepts/概念_Agent内存与状态管理|Agent 内存与状态管理]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]、[[concepts/概念_上下文工程|上下文工程]]

> 📎 **物理文献**：[[raw/articles/刚刚，DeepSeek Harness震撼开源：一切皆插件.md]]
