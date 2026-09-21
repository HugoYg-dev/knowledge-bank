---
type: concept
tags:
- AI-Agent/coding
summary: 围绕基础大模型构建的宿主与编排系统（Harness Engineering），负责编排执行、思考规划、工具行动、上下文感知管理、产物存储与评估。
sources:
- wiki/sources/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a.md
- wiki/sources/2026-07-03_Prompt,-context,-harness-&-loop-engineering_19f29f.md
- wiki/sources/2026-07-27_Agent-memory-and-state-are-not-the-same-thing!_19fa57.md
- wiki/sources/2026-07-27_Graph-engineering-clearly-explained_19fa57.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/搜索没有变便宜，但 Agent 把它拆成了新的供应链.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
- wiki/sources/阿里高德 LongHorizon-Harness 框架：使用审计状态机重构Agent执行流程.md
updated: '2026-09-21'
aliases:
- Harness Engineering
- 宿主系统工程
- 宿主编排工程
- 外壳工程
- 概念_Harness_Engineering
---

# 概念：Harness Engineering

## 定义

**Harness Engineering（外壳工程 / 宿主工程）** 是围绕基础模型（Raw Model）构建的那套系统工程。它编排 Agent 的执行逻辑，决定模型如何思考规划、调用工具行动、感知管理上下文、存储中间产物以及评估输出结果。

在行业中存在一个经典共识：**“如果你不是模型，你就是 Harness（If you’re not the model, you’re the harness）”**。

Beren Millidge 将其进行了精确的硬件系统类比：
- **Raw LLM**：CPU（无 RAM、无 Disk、无 I/O）
- **Context Window（上下文窗口）**：RAM（高速但空间受限）
- **External Databases（外部数据库）**：Disk（容量大但速度慢）
- **Tool Integrations（工具集成）**：Device Drivers（设备驱动）
- **Harness（宿主系统）**：Operating System（操作系统 / OS），负责调度和管理上述所有部件，如同 Lilian Weng 所说，它封装了复杂的底层逻辑，保持接口规范简洁。

## Harness 的三大设计模式

1. **工作流自动化（Workflow Automation）**：目标导向的计划-执行-观察-改进循环，驱动模型自主分析运行轨迹与失败原因。
2. **文件系统即持久记忆（Filesystem as Persistent Memory）**：避开受限的上下文窗口，将实验日志、代码 diff、错误追踪落盘为物理文件，利用 shell/bash 标准接口进行读写。
3. **子代理与后台任务（Sub-agents & Background Tasks）**：主代理派生子代理进行并行任务分工，配套显式的进程管理（启动、查看日志、取消、合并结果）。

## 编码智能体标准工具箱

一个完备的编码 Harness 包含：文件系统工具（glob/grep/read/write/edit）、shell/git、MCP 协议组件、搜索与浏览器、后台任务与子代理委托。

## 可靠执行控制

生产级 Harness 必须明确将**状态（State）与记忆（Memory）解耦管理**。状态绑定于当前 Run，通过在每个超级步骤（Superstep）后写入 Checkpoint 记录执行进度以防意外崩溃，支持中断恢复和新分支分叉（Fork）；而记忆则跨 Runs 留存，多智能体协同下需通过 Scope 机制进行隔离（如 `memory.scope("/agent")`）以防认知冲突。详见 [[概念_Agent内存与状态管理]]。

### 分层早停与防路径震荡控制

在生产级 Agent Loop 设计中，Harness 需具备细粒度的运行时控制机制：
1. **分层早停（Hierarchical Early Stopping）**：由“模型 Thought 置信度打分”、“连续步信息增益（Embedding 相似度）”和“任务类型步数上限”构成；关键依赖工具返回的**确定性硬信号**（明确答案、非空数据、单元测试通过）作为早停终极锚点，防范模型置信度幻觉。
2. **失败记忆（Failure Memory）遏制路径震荡**：针对反复调用相同失败 Action 的问题，Harness 在内存中维护带滑动时间窗口（TTL）的 `(tool_name, params_hash)` 失败字典；当窗口期内相同工具及参数连续失败达阈值（如 $\ge 2$ 次），强行阻断执行并注入反思提示词，驱动 Agent 探索替代分支。
3. **无人值守安全审批矩阵**：将操作分级为只读（自动执行）、低风险（异步报告与事后复核）与高风险（阻断等待人工确认），配合全局 Token/资金预算限额与高危模式自动熔断。

## 生产级 Harness 的 11 大核心组件

根据业界前沿实践（如 Anthropic Claude Code、OpenAI Agents SDK 等），一个生产级的 Harness 包含以下 11 个核心模块：

1. **Orchestration Loop（编排循环）**：系统的“心脏”，实现 Thought-Action-Observation (TAO) / ReAct 心跳循环，管理 Turn 轮次。
2. **Tools（工具层）**：定义工具 Schema（参数与描述），负责沙箱执行、结果捕获与格式化反馈。
3. **Memory（记忆层）**：包含单会话短期记忆（聊天历史）和跨会话长期记忆（如 `CLAUDE.md` 项目索引、JSON Store 等）。
4. **Context Management（上下文管理）**：对抗“上下文 rot（退化）”，通过压缩历史、Observation 遮蔽、懒加载等手段筛选最高信号的 Token。
5. **Prompt Construction（提示词构建）**：分层堆叠系统提示词、工具定义、记忆文件和历史，保证关键上下文放置在两端。
6. **Output Parsing（输出解析）**：配合原生工具调用（tool_calls），基于 Pydantic 等 Schema 进行强约束解析，辅以重试机制。
7. **State Management（状态管理）**：利用图/字典维护运行状态，支持 super-step 级别的 Checkpoint 与断点恢复。
8. **Error Handling（错误处理）**：对故障进行分类处理（瞬时退避重试、LLM 反馈可恢复、用户干预、确定性崩溃），防范 Compound Error。
9. **Guardrails（护栏与安全）**：输入/输出/工具执行的多级审核与 tripwire 瞬间熔断机制，实现权限隔离。
10. **Verification Loops（校验回路）**：整合静态测试/Lint/推理校验，给 Agent 自我纠错与验证机会，能显著提升交付质量。
11. **Subagent Orchestration（子代理编排）**：支持 Fork（同上下文拷贝）、Teammate（多终端协作）与 Worktree（独立 Git 分支隔离）等协同模式。

## Ralph Loop 工程协作模式

针对长生命周期且跨 context window 的复杂任务，业界提出了 **Ralph Loop（双阶段协作模式）**：
1. **Initializer Agent（初始化阶段）**：负责一次性地设置开发脚手架，包括运行初始化脚本、建立进度追踪文件（Progress File）、列出功能清单，以及提交初始 Git commit。
2. **Coding Agent（增量迭代阶段）**：在后续的每个会话中，该 Agent 通过读取物理文件（Git 日志、进度文件）来恢复上下文，挑选优先级最高且未完成的任务进行编码、验证与 Commit，并在退出前更新进度摘要。

该模式利用**物理文件系统（Filesystem）**作为跨上下文窗口的连续性载体，极大地增强了智能体长周期复杂任务的完成率。

## 现代 Harness 架构演进：微内核、插件模型与权威事件流

随着以 [[entities/实体_DeepSeek_Harness|DeepSeek Harness]] 与 [[entities/实体_Codex|Codex]] 为代表的现代生产级智能体框架开源，Harness Engineering 进一步确立了以下关键架构范式：

1. **声明式 vs 命令式两种插件世界观**：
   - **声明式模型（如 Codex）**：插件为磁盘静态资源（Markdown Skill、MCP JSON 配置、外部 Shell 脚本），由操作系统管理外部进程生命周期。门槛低且简单，但无法在 Harness 进程内注册带状态服务；
   - **命令式微内核模型（如 DSH / Cordis）**：插件直接运行在 Harness 进程中，持有内部状态并支持跨插件直接函数调用与依赖注入。依托 [[entities/实体_Cordis|Cordis]] 运行时的副作用跟踪、撤销条（Disposer）与事务性 HMR（热模块替换），保障进程内热更新不留悬空引用。
2. **一切皆插件与 Agent Loop 控制流解耦**：
   - 将能力严格拆分为**接口（Interface）**、**实现（Implementation）**与**消费者（Model Tool）**三层；
   - 传统 Harness（如 Codex）将 `run_turn()` 控制流硬编码在核心二进制中，仅提供固定 Hook 插槽；而现代微内核 Harness 将 Agent Loop 自身解耦为可插拔插件（如 DSH `ctx.agentLoop`），允许在运行时动态将控制流替换为多 Agent 协作循环或并行流式调度，为 [[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness（外壳自进化）]] 提供了物理插槽。
3. **权威会话流（Session Log 即唯一事实源）**：
   - 坚持“凡是模型看见的内容，都必须能从日志中重建”原则。系统提示词组装、环境变量、流式 Chunk、工具调用与结果、权限切换全量写入追加式事件流，作为界面回放、持久化（JSONL/SQLite）、Resume 和 Fork 的统一事实基础，彻底解决调试与审计黑盒难题。
4. **运行时交通规则与单调安全守卫**：
   - 交互严格拆解为 Turn 与 Step；
   - 工具调用经过前置策略、单调不可逆守卫（被拒绝的操作不得被后续插件重新放行）、执行包装与后置处理；
   - 调度器允许连续只读调用并行，写操作自动成为独占屏障（Barrier）；支持运行中消息排队与带回执的实时转向（Steering）。
5. **PTC 模式（Programmatic Tool Calling）**：
   - 通过 Code Mode SDK 向模型暴露代码运行环境，模型可编写 TypeScript/Python 脚本在单次 `run_code` 中批处理多步工具调用，显著削减多轮往返的 Token 与延迟开销。
6. **Fail-Closed 默认安全原则**：
   - 默认采用 `workspace-write` 沙箱并配合审批机制；当系统无法确认隔离策略完全生效时，主动拒绝执行（Fail-Closed）而非静默降级为无保护运行。


## MEA 循环与审计驱动状态转换（LongHorizon-Harness 范式）

针对长时跨界面/长链路复杂任务，[[entities/实体_LongHorizon-Harness|LongHorizon-Harness]] 提出了突破传统单会话轨迹中心模型的 **Manage-Execute-Audit (MEA)** 状态机范式：

1. **从“长上下文轨迹”转向“审计状态机”**：
   - 传统单会话 Harness 将执行、状态记录与自评全揉在同一条不断变长的轨迹中，引发 Compounding Errors（滚雪球偏差）、Goal Drift（目标漂移）与 [[concepts/概念_Context_Rot_上下文衰退|Context Rot]]。
   - MEA 循环将长任务重定义为**环境状态转换管理**：每轮抛弃上一轮高噪声的原始工具轨迹，仅跨轮沉淀由 Requirement、Artifact、Fact 构成的受审计状态账本。
2. **三角色结构隔离与外层包裹定位**：
   - **Manager**：持有状态账本与原始需求，无环境直接操作权限，动态生成有界子任务契约（Subtask Contract）；
   - **Executor**：唯一被允许修改环境的主体，在每轮全新受限上下文中运行，包裹 [[entities/实体_Claude_Code|Claude Code]] 或 [[entities/实体_Codex|Codex]] 作为底层执行引擎；
   - **Auditor**：仅具只读权限，从外部物理环境重新取证，基于完成度（Completion）、完整性（Integrity）与契约合规（Contract Audit）三维控制信号硬性决定是否提交状态；
   - **定位边界**：底层 Coding Agent 负责单轮将代码/操作做出来，MEA 外层循环负责把守状态门禁，决定哪些局部产物有资格累积进长期可信进度。

## 代表实践

- [[entities/实体_Claude_Code|Claude Code]]：Anthropic CLI 编码智能体，高度集成了 Harness 工程哲学。
- [[entities/实体_Codex|Codex]]：OpenAI 编码智能体系统，代表了经典的声明式插件模型。
- [[entities/实体_DeepSeek_Harness|DeepSeek Harness (DSH)]]：DeepSeek 开源的命令式微内核智能体框架。
- [[entities/实体_LongHorizon-Harness|LongHorizon-Harness]]：阿里高德开源的审计状态机长时 Agent 编排框架，通过 MEA 三角色解耦与外层契约包裹底层 Coding Agent。

## 来源与参考

- [[sources/刚刚，DeepSeek Harness震撼开源：一切皆插件|刚刚，DeepSeek Harness震撼开源：一切皆插件]]
- [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
- [[OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]]
- [[concepts/概念_RSI递归自我改进]]
- [[concepts/概念_Harness优化阶梯]]
- [[concepts/概念_Self_Harness_自主进化宿主系统|Self-Harness]]
- [[sources/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a|The Anatomy of an Agent Harness]]
- [[sources/2026-07-27_Agent-memory-and-state-are-not-the-same-thing!_19fa57|Agent memory and state are not the same thing!]]
- [[wiki/sources/阿里高德 LongHorizon-Harness 框架：使用审计状态机重构Agent执行流程.md]]
