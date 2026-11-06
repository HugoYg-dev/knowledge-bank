---
type: entity
tags:
- AI-Agent/coding
summary: OpenAI 推出的代码生成与编码智能体系统，采用 118 个 Rust Crate 模块化解耦与 Op/Event 双向事件驱动架构；沉淀了从声明式插件到全新 Token Budget 跨窗口短期记忆与两阶段长期记忆体系；2026-07 起其桌面 App 成为新 ChatGPT 桌面端的基座。
sources:
- wiki/sources/Firecrawl 新工具开源，anydoc，将各种输入转换为md.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
- wiki/sources/万字复盘Codex_模型公司如何做产品的典型故事.md
- wiki/sources/深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路.md
updated: '2026-11-06'
timeline:
- field: "product_status"
  value: "Codex 桌面 App 并入 ChatGPT，成为新 ChatGPT 桌面 App 的基座（底层应用名仍为 com.openai.codex）"
  valid_from: "2026-07-09"
  valid_to: null
  observed_at: "2026-10-21"
  sources:
    - "wiki/sources/万字复盘Codex_模型公司如何做产品的典型故事.md"
---
# 实体：Codex

## 简介

**Codex** 是由 OpenAI 推出的代码生成模型与编码智能体系统（涵盖早期 Codex 代码模型以及后续集成于 ChatGPT / OpenAI 编码智能体客户端的完整 Harness 实现）。在开源智能体架构对比中，Codex 常作为开源可逐行分析的基准，代表了经典的**声明式插件模型（Declarative Plugin Model）**。

## 产品演化史：从边缘标签页到 ChatGPT 底座（2021–2026）

据 [2026-10-21 来源] 的万字复盘（Every CEO Dan Shipper 深访 Tibo、Alexander Embiricos、Mia Glaese 等核心成员）：

1. **多起点与内部赛马（2021–2025 初）**：第一代 Codex 发布于 2021 年（公开代码微调的 GPT-3，为初代 GitHub Copilot 供能）；o1 推理模型（2024-09 预览）让编程重回 OpenAI 最高优先级，多条内部路线（Embiricos 的人机协作构想、Tibo 在 OpenAI Monorepo 上「自举」训练内部编程 Agent、Scientist Assistant 等）于 2025 年初合并为跨学科完整团队（产品+工程+研究）。
2. **Codex Cloud 折戟（2025-05-16）**：约七周开发的云端异步 Agent 产品，内部成功但外部未找到 PMF——外部用户需数小时重建云端配置、无法中途打断、模型也不够聪明；工程负责人跳槽 Cursor，据报道 OpenAI 曾达成的 30 亿美元收购 Windsurf 协议同年 7 月告吹。曾于 2025-04-16 发布的开源 Codex CLI 仅是两人支线项目（默认跑 o4-mini 通用模型）。
3. **转向本地与 Rust 重写底层 Agent（2025 暮春–夏）**：Tibo 接手后放弃云端优先，用 Rust 彻底重写底层 Agent 并与终端界面解耦，使同一套 Agent 引擎此后可进入 CLI、编辑器扩展、桌面/移动 App、云端与 ChatGPT；GPT-5（2025-08 底）发布后推出 VS Code / Cursor 扩展，2025-10 使用量增长超十倍，编辑器扩展超过终端成为第一入口。
4. **桌面 App 取消代码编辑器（2025 Q4）**：原生桌面 App 灵感来自聊天产品而非 VS Code（侧边栏按项目组织任务、多 Agent 各自在独立代码副本上并行）；最冒险的决定是不内置代码编辑器——「用 Agent 写代码的体验必须足够好，好到开发者不会想念编辑器」，避免做成功能不完整的 VS Code。
5. **专属模型线与地位反转（2025-11 起）**：Codex 模型线与 ChatGPT 主模型分离，可独立快速迭代——GPT-5.1 Codex Max（2025-11-19，连续写几小时代码）、GPT-5.2 Codex（2025-12-18，大型代码库跨文件修改）、GPT-5.3 Codex（2026-02 初，训练首次不再只围绕编程、面向知识工作）；桌面 App 2026-02-02 公开发布，2026-03-19 周用户超 200 万，2026-06 超 500 万（约 1/5 为知识工作者），2026-07-09 并入成为新 ChatGPT 桌面 App 基座。团队下一步计划转向异步、重新托管回云端（回到 2025 春失败的愿景）。
38	6. **方法论启示**：Codex 逃开「创新者的窘境」（模型能力每次跃迁都撑破原交互界面、催生新产品形态）的原因：OpenAI 允许多团队如「创业公司组合」并行探索再合并 + Codex 在 ChatGPT 主线之外独立迭代 + 「用 AI 开发 AI」使几个人几周内即可做出新产品入口。
39	
40	## 核心 Harness 架构深度解析（118 Crate 模块化与事件驱动）
41	
42	据 2026 年 10 月千问团队对 Codex 开源 Harness（Codex CLI）的逐行源码深度解析，其工程架构呈现高度成熟的系统级设计：
43	
44	### 1. 118 个 Rust Crate 模块化解耦与强制解耦法则
45	Codex 将整个系统切分为约 **118 个独立的 Rust Crate（子模块）**，并在其 `AGENTS.md` 中立下严苛的工程纪律：**“Resist adding code to codex-core”（禁止往 codex-core 里面写代码）**。
46	- **解耦意图**：作为最核心模块，`codex-core` 极易随着需求增加而恶性膨胀。强制将新功能、协议与扩展下沉到专门的 Crate，保证了“高内聚、低耦合”；且开发者修改单一 Crate 仅需局部增量编译，极大优化了工程构建效率。
47	- **核心 Crate 职责划分**：
48	  - `codex-core`：Agent 运行核心，集中管理 Session 会话上下文、三层主 Loop、工具分发执行与状态机；
49	  - `codex-protocol`：底层数据定义层，精确抽象用户交互的 `Op`（Operation）与 Agent 响应的 `Event` 协议契约；
50	  - `codex-api`：OpenAI Response API 的封装层，提供 HTTP 与 WebSocket 双传输通道；
51	  - `codex-app-server`：核心协议服务层，对外暴露出统一的 **JSON-RPC** 接口，使无论 TUI 终端还是 Desktop 桌面端均通过同一套底层协议服务驱动；
52	  - `codex-rollout`：会话持久化与 Agent Trace 层，将全量会话轨迹序列化为磁盘文件或 SQLite 数据库；
53	  - `codex-arg0`：利用系统入口参数传参机制（如传入 `codex`、`codex-linux-sandbox`、`apply-patch`），使程序在启动瞬间感知自身角色定位与沙箱职责；
54	  - `codex-tui` 与 `codex-exec`：分别负责终端富文本交互界面与脚本/CLI 无头执行前端。
55	
56	### 2. 双向事件驱动模型（Op 与 Event）
57	- **客户端 $\to$ Agent（Op 信封机制）**：用户操作被封装在 `Submission` 信封中发送为 `Op`，主要包含 `TurnInput`（开启新轮）、`Interrupt`（打断工作）、`Compact`（手动压缩）与 `Shutdown`（关闭会话）；
58	- **Agent $\to$ 客户端（Event 消息流）**：Agent 的一切行为均通过强类型 `Event` 实时回传，如 `TurnStarted`、`TurnComplete`、`AgentMessage`（回复）、`AgentReasoning`（思考过程）、`ExecCommandBegin` / `OutputDelta`（命令执行与实时流输出）及 `TokenCount`（用量更新），实现端到端的透明事件流追踪。
59	
60	### 3. 三层嵌套循环架构（Task $\to$ Turn $\to$ Sampling）
61	- **Task Loop（外层）**：负责接收和排队用户的具体业务需求，处理消息 Pending 与长任务生命周期；
62	- **Turn Loop（中层 / Run Turn）**：管理单轮对话与上下文压缩（单次压缩亦作为一个独立 Turn 执行）；
63	- **Sampling Loop（内层）**：对应单次模型推理请求、单次工具调用或文字生成步骤（对标 DSH 的 Step）。
64	
65	### 4. 工具并发执行与有序拼装（FuturesOrdered）
66	当模型在一次响应中返回多个并行工具调用时，Codex 利用 Rust 的 `FuturesOrdered` 队列在底层**并发执行**各工具以最大化吞吐速度；但在将执行结果回写组装回模型上下文时，**严格保持与模型调用一致的原始时序**。这种“底层并发跑、顶层有序拼”的工程设计，既消除了网络/执行等待，又杜绝了上下文乱序引发的模型理解困惑。
67	
68	### 5. World State 环境状态 Diff 补丁
69	面对 Shell 权限、环境变量与 `AGENTS.md` 规则等高频变动，Codex 将世界切分为带稳定 ID 的类型化 Section。环境变化时，不将全量规则重读进上下文，而是**仅向上下文注入 Diff 增量补丁语句**。该设计不仅极大节省了 Context Window，更避免了打断 Prefix KV Cache 的哈希前缀，保护了模型的首字生成延迟。
70	
71	### 6. SubAgent 精细化协同与 Mailbox 机制
72	- **Fork Turns 三大派生策略**：
73	  1. **全部继承**：完整克隆父对话上下文与历史，作为“影分身”并行加速无串联任务；
74	  2. **继承最近三轮**：仅保留近期交互信息，隔离早期杂音，适合局部任务探索；
75	  3. **无上下文（None）**：完全空白上下文，执行需彻底上下文隔离的高危或独立子任务。
76	- **Mailbox 异步通信原语**：
77	  1. **Send Message**：仅将消息放入信箱，不打断目标运行，待目标开启新轮时自动投递；
78	  2. **Follow-up Task**：目标空闲时直接唤醒开启新轮；目标运行中则在当前步（Sampling）边界安全投递，兼顾实时性与执行完整性。
79	
80	## 记忆体系与上下文压缩演进：从 Handover Document 到 Token Budget
81	
82	### 1. 传统 Compaction 创新：交接文档（Handover Document）策略
83	在早期与常规上下文压缩中，Codex 设定 80% Token 阈值，或在模型切换、切入更小窗口模型时触发。与常见将前 N 轮做干瘪 Summary 的压缩不同，Codex 在 Prompt 中要求压缩模型撰写一份面向下一任接手者的**“交接文档（Handover Document）”**。模型以“向协作者交接工作”的心态梳理当前进展、剩余任务、修改文件与约束，大幅提升了压缩上下文的结构完整性；同时从最早消息开始压缩，使后续轮次能快速建立并复用新的 Prefix KV Cache。
84	
85	### 2. 跨会话长期记忆（Two-Stage Memory & Decay）
86	- **逐会话提取（Rollout Extraction）**：会话结束后从持久层 `codex-rollout` 抽取重要事实与用户特征，脱敏后存入数据库；
87	- **全局巩固（Global Consolidation）**：在磁盘上维护 Top-N 核心事实，依据运行中被用户再次提及的引用频次（Citation Count）动态排序。高频事实持续保留，低频事实自然衰退遗忘，构成具备自进化特征的长期可遗忘记忆。
88	
89	### 3. 全新 Token Budget 跨窗口短期记忆（2026-08 突破性架构）
90	针对传统 Compaction 容易“猜错重要信息导致不可逆遗忘”的根本缺陷，Codex 引入了全新的 **Token Budget** 机制，将压缩问题转化为模型自主管理的跨窗口状态衔接：
91	- **清爽新窗口（Fresh Context Window）**：触发窗口容量阈值时，不再执行破坏性内容压缩，而是直接开启一个带有自增序号的全新空白 Context Window；
92	- **三大跨窗口衔接支柱**：
93	  1. **Thread Hint（便签连接）**：新窗口启动时，系统自动提取约 4000+ 字节的背景提示注入新窗口 Developer Message，交代上一窗口的大致任务定位；
94	  2. **Notes（虚拟文件系统笔记本）**：由服务端托管的 Agent 私人笔记本（并非物理磁盘），向 Agent 提供 `List`、`Read`、`Search`、`Append`、`Write` 工具。Agent 在执行中随时自主记录修改点、卡点、测试结果；新窗口运行时，按需列出并读取自己需要的特定笔记，实现零信息损失的渐进式回忆；
95	  3. **History（完整 Agent Trace 追溯）**：完整归档所有历史对话条目，提供列表、全文读取与搜索工具，供 Agent 遇到疑问时随时穿透检索确切的历史执行细节。
96	- **双机制正交分工**：长期 Memory 负责跨 Session 的长期经验与偏好沉淀；Token Budget 负责单 Session 内跨 Context Window 的复杂任务断点续传，两者在生命周期与工程定位上严格正交。
97	
98	## 架构特征：声明式插件模型
99	
100	1. **静态文件与声明性资源**：
101	   - Codex 的插件系统基于磁盘文件系统构建。插件以文件夹形式组织，包含 Markdown 格式的 Skill 描述文件、启动 MCP（Model Context Protocol）Server 的 JSON 配置、以及事件触发时执行的 Shell 脚本；
102	   - 插件本身不向 Harness 核心进程注入运行代码，Harness 仅按需读取配置并由操作系统拉起独立的子进程，插件间相互独立解耦。
103	2. **轻量与低门槛**：
104	   - 编写插件门槛极低，只需放置格式正确的静态文件；更新或替换工具（如从 [[entities/实体_Tavily|Tavily]] 切换到 Brave Search）仅需修改配置并重启子进程（2–3 秒完成），用户无感。
105	3. **控制流硬编码与扩展边界**：
106	   - 核心控制流 `run_turn()` 编译在 Rust 核心二进制中：严格按“采样前压缩 $\rightarrow$ 上下文组装 $\rightarrow$ 模型请求 $\rightarrow$ 工具执行”串行运转；
107	   - 外部扩展仅限于预设的 Contributor Trait 和 Hook 插槽（如请求前后微调 Prompt），无法在运行时动态将控制流重构为多 Agent 协作循环或并行流式循环。
108	
109	## 与 DSH 命令式模型的对比
110	
111	| 架构维度 | Codex（声明式） | DeepSeek DSH（命令式） |
112	| :--- | :--- | :--- |
113	| **模块化组织** | 118 个 Rust Crate 模块解耦（`Resist adding code to codex-core`） | 统一微内核插件生态（`一切皆插件`） |
114	| **插件形态** | 磁盘文件 + 外部独立进程 | 进程内 TypeScript 状态对象 |
115	| **状态持久性** | `codex-rollout` 持久化 + Token Budget（Notes/History） | 进程内跨 Turn 状态维护与依赖注入 |
116	| **上下文管理** | Handover Document 压缩 + Token Budget 跨窗口衔接 | 运行时丢弃历史 + 进程内状态重构 |
117	| **Agent Loop** | 三层循环（Task $\to$ Turn $\to$ Sampling）硬编码控制流 | `ctx.agentLoop` 作为可热替换插件 |
118	| **适用场景** | 日常辅助编码、常规工具与 Skill 调度、工业级多端一致性 | 复杂运行时状态管理、Agent 自主代码修改与自进化 |
119	
120	## 关联页面
121	- **同类编码系统**：[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]
122	- **核心概念**：[[concepts/概念_Harness_Engineering_宿主编排工程|Harness Engineering]]、[[concepts/概念_上下文工程|上下文工程 (Context Engineering)]]、[[concepts/概念_Agent三层记忆体系|Agent 三层记忆体系]]、[[concepts/概念_RSI递归自我改进|Self-Harness (RSI 自进化)]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]
123	- **相关工具**：[[entities/实体_Tavily|Tavily]]
124	
125	## 来源与参考
126	- [[sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重|OpenAI前VP Lilian Weng：AI自我改进的近路不是改权重]]
127	- [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
128	- [[sources/万字复盘Codex_模型公司如何做产品的典型故事|万字复盘 Codex：一个在模型公司如何做产品的「典型」故事]]
129	- [[wiki/sources/深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路.md|深度解析 Codex Harness 架构及其全新上下文压缩记忆体系的设计思路]]
