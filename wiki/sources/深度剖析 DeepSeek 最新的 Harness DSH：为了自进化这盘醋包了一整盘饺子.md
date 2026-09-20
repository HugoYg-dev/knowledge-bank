---
type: source
tags:
- RSI
- AI-Agent/coding
summary: 深度剖析 DeepSeek DSH（DeepSeek Harness）与 Cordis 运行时的命令式微内核设计：将 Agent Loop 自身作为插件解耦，配合副作用跟踪、依赖响应与事务性
  HMR，为 Agent 运行中自进化（Self-Harness）提供底层基础设施。
sources:
- raw/articles/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
updated: '2026-08-20'
---

# 来源摘要：深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子

## 1. 来源信息
- **标题**：深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子
- **作者**：[[entities/实体_鸭哥|鸭哥]]
- **发布日期**：2026-08-13
- **原文链接**：[yage.ai/share/dsh-deep-analysis-20260813.html](https://yage.ai/share/dsh-deep-analysis-20260813.html)

## 2. 核心要点
1. **两种插件世界观的根本分水岭（声明式 vs 命令式）**：
   - **Codex 的声明式模型**：插件本质是磁盘文件夹与声明性资源（Markdown skill、MCP 配置、shell 脚本），不运行在 Harness 进程内，由操作系统管理外部进程生命周期。好处是极简、门槛低；代价是插件无法在进程内注册有状态服务或修改 Harness 自身行为；
   - **DSH 的命令式模型**：插件直接运行在 Harness 进程中，持有跨 Turn 内部状态，插件间可直接进行函数调用与依赖注入。必须由底层微内核管理对象的生命周期、连接清理与引用切换。
2. **Cordis 运行时的底层支撑与下限保障**：
   - 为解决命令式模型中插件热替换造成的悬空引用与状态卡死，DSH 依托 [[entities/实体_Cordis|Cordis]] 运行时：记录装载副作用与撤销函数（Disposer）、维护插件间依赖变动通知、以及执行事务性热更新（HMR，新代码加载失败自动回滚至旧版本）；
   - DSH 虽开发门槛更高，但内建了完备的基础设施（如 `fiber.ts` 达 750 行），覆盖了并发卸载竞态、依赖链传播终止与回滚容错等复杂工程边缘坑点。
3. **日常开发的适用性边界（上限相同，下限不同）**：
   - 在不涉及进程内带状态组件热替换的常规开发中，声明式与命令式的业务上限由开发者代码质量决定；日常开发中搜索、Skill 脚本通过配置和重启进程（2–3 秒）即可满足需求，DSH 的 Cordis 机制对大多数日常开发属于无谓复杂度。
4. **核心结构性差异：Agent Loop 作为可插拔插件**：
   - Codex 的 `run_turn()` 控制流被硬编码在核心 Rust 编译产物中，仅提供固定时间点的 Hook 插槽，无法在运行时动态重构控制流骨架；
   - DSH 将 Agent Loop 置于 `packages/core/agent-loop` 中，自身即为普通插件，对外提供 `ctx.agentLoop` 服务，声明依赖 `ctx.systemPrompt` 与 `ctx.tools`。开发者或 AI 可通过实现相同接口的插件将其整体热替换（如切换为多 Agent 协作循环或并行流式调度），旧监听与服务被框架干净撤销。
5. **为“自进化 Agent（Self-Harness）”铺平物理插槽**：
   - DSH 整套重型架构的根本战略价值在于支撑 Agent 的运行时自适应与自我演化（“为了这碟醋，包了一整盘饺子”）。
   - Agent 在运行中自主生成新工具插件或整套新 Loop 代码时，Cordis 提供了无缝热加载、撤销清场、依赖自协调与出错事务回滚；且 DSH 的 TypeScript 插件架构为大模型提供了完全可见的接口规范与上下文，填补了传统 Harness 缺乏动态挂载接口的物理缺陷。

## 3. 关键架构与机制解析

### 3.1 声明式 vs 命令式架构对比矩阵
| 比较维度 | Codex（声明式模型） | DeepSeek DSH（命令式模型） |
| :--- | :--- | :--- |
| **插件载体** | 磁盘文件（Markdown Skill、MCP JSON、Shell 脚本） | 进程内 TypeScript 代码对象 |
| **运行位置** | Harness 外部独立进程 / 静态读取 | 与 Harness 运行在同一进程内 |
| **状态管理** | 无状态或由子进程自管，主进程无感知 | 在进程内持有状态，支持直接函数调用与依赖注入 |
| **热替换机制** | 修改配置后重启子进程（2–3 秒无感） | Cordis 事务性 HMR、撤销条（Disposer）清理与依赖通知 |
| **控制流灵活性** | `run_turn()` 硬编码控制流，仅支持预设 Hook | Agent Loop 自身即为插件（`ctx.agentLoop`），支持完全动态替换 |
| **开发门槛** | 极低（编写文件放入对应目录） | 较高（需注册副作用、声明依赖并理解生命周期状态机） |
| **核心优势场景** | 日常辅助编程、工具调用、轻量 Skill 扩展 | 运行时复杂状态组件替换、Agent 循环自修改与自进化 |

### 3.2 自进化 Agent（Self-Harness）闭环机制
```
[Agent 运行时触发自进化需求]
           │
           ▼
[生成新插件 / 新 Loop 代码] ──(上下文可见性: DSH 暴露 TypeScript 接口与约束)
           │
           ▼
[Cordis 动态热装载 (In-process)]
           ├── 撤销条自动记录旧状态变更
           ├── 依赖通知触发相关插件重连
           └── 事务性保护 (HMR 失败则自动 Rollback)
           │
           ▼
[零停机完成 Harness 行为演化]
```

## 4. 关联实体与概念
- **作者实体**：[[entities/实体_鸭哥|鸭哥]]
- **核心系统实体**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness (DSH)]]、[[entities/实体_Cordis|Cordis]]、[[entities/实体_Codex|Codex]]
- **核心工程概念**：[[concepts/概念_Self-Harness|Self-Harness（自主外壳进化）]]、[[concepts/概念_Harness_Engineering|Harness Engineering]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]
- **对比与参考来源**：[[sources/刚刚，DeepSeek Harness震撼开源：一切皆插件|刚刚，DeepSeek Harness震撼开源：一切皆插件]]、[[sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重|OpenAI前VP Lilian Weng：AI自我改进的近路不是改权重]]

> 📎 **物理文献**：[[raw/articles/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md]]
