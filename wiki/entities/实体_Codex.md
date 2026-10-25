---
type: entity
tags:
- AI-Agent/coding
summary: OpenAI 推出的代码生成与编码智能体系统，代表了典型的声明式插件架构（静态文件/MCP配置/外部进程调度）与硬编码控制流设计；2026-07 起其桌面 App 成为新 ChatGPT 桌面端的基座。
sources:
- wiki/sources/Firecrawl 新工具开源，anydoc，将各种输入转换为md.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
- wiki/sources/万字复盘Codex_模型公司如何做产品的典型故事.md
updated: '2026-10-25'
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
6. **方法论启示**：Codex 逃开「创新者的窘境」（模型能力每次跃迁都撑破原交互界面、催生新产品形态）的原因：OpenAI 允许多团队如「创业公司组合」并行探索再合并 + Codex 在 ChatGPT 主线之外独立迭代 + 「用 AI 开发 AI」使几个人几周内即可做出新产品入口。

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
- [[sources/万字复盘Codex_模型公司如何做产品的典型故事|万字复盘 Codex：一个在模型公司如何做产品的「典型」故事]]
