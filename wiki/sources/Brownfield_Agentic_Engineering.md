---
type: "source"
tags: ["AI-Agent/coding"]
summary: "Addy Osmani 阐述在老旧遗留代码库中运行 AI 智能体的棕地工程方法论：分区治理、特征化测试锁定旧行为、持久化调研产物、Harness 约束沉淀及端到端完整迁移单元"
sources: ["raw/articles/Brownfield Agentic Engineering.md"]
updated: "2026-10-12"
---

# 来源摘要：Brownfield Agentic Engineering

- **来源信息**：Addy Osmani（Elevate / Substack，2026-09-14）
- **核心议题**：针对系统年龄超过团队司龄的老旧“棕地代码库”（Brownfield Codebases），探讨如何安全、可信且低成本地引入 AI Coding 智能体，使隐性约束显性化，避免生成看似能跑但破坏架构与测试脆弱的“技术负债代码”。

## 核心要点

1. **棕地系统（Brownfield）的核心矛盾与自治边界**：
   - 棕地系统的本质特征是：**代码仓库本身已不再能完全描述系统的实际真实行为**。团队组织记忆、临时修补（duct tape）、边缘服务依赖以及跨部门契约皆存在于代码树之外。
   - 自治权必须紧跟**爆炸半径（Blast Radius）、可观测性（Observability）与可恢复性（Recoverability）**，而非取决于模型的“自信度”。

2. **Zones 分区治理模型（红黄绿三色防线）**：
   - **Green Zone（绿区）**：测试覆盖高、架构隔离好、遵循现代规范的代码模块；智能体可在紧凑循环（Tight Loop）中高自主度作业。
   - **Yellow Zone（黄区）**：代码质量参差，在智能体改动前必须先编写并锁定[[concepts/概念_Brownfield_Agentic_Engineering_棕地智能体工程|特征化测试（Characterization Tests）]]。
   - **Red Zone（红区）**：涉及鉴权、计费、核心权限、薪资结算等脆弱高敏模块；严禁无人值守重写，必须由人类结对（Pairing）或禁止智能体改动。
   - **分区三大运行铁律**：①由人类划定区域地图而非由 Agent 自由探索（防止 Agent 直奔最复杂的文件）；②区域晋级必须经过检验（如补充特征化测试并经模块负责人审查第一批 PR 后，黄区方可升为绿区）；③区域决定动词（绿区快循环、黄区测试先行、红区人机结对）。

3. **仅记录代码无法言说的事实（Write down what the code can’t say）**：
   - 智能体擅长从现有代码推断结构，不要用巨幅 Markdown 塞满上下文窗口。
   - 上下文注入应仅聚焦代码无法表达的信息：业务/团队特定权衡、反直觉实现的背景缘由、静态分析无法检查的架构规范及跨系统隐式契约。

4. **让调研产物跨会话持久留存（Durable Research Artifact）**：
   - 避免单次会话研究的“考古开销浪费”：在黄区与红区作业前，采用独立的只读阶段输出简短的**理解备忘录（Comprehension Memo）**，记录入口、所有者、调用方、现有抽象、测试、生产信号与未决问题，并要求显式引用代码行或工单。
   - 后续规划与实施从清爽的上下文（Clean Context）启动，由人类决定实施路径；实施若发现事实地图错误立即中止；审查角色与生成角色解耦。

5. **把反复出现的 Review 意见沉淀进 Harness**：
   - **“每一次重复的人工纠偏，都是 Harness 缺失的一块拼图（Every repeated correction is a missing piece of the harness）”**。
   - 明确职责层级：Instructions（指令）记录仓库特殊事实；Skills（技能）封装可复用操作（如爆炸半径检查、Schema 校验）；Harness（宿主）提供工具、权限、门禁与恢复环境。
   - 频繁出现的审查评论应下沉为 Lint 规则、Hook、类型约束或 CI 检查，避免依赖模型记忆。

6. **以特征化测试（Characterization Tests）锁定现状**：
   - 零风险起步：在重构前，首先编写特征化测试锁定现有真实行为（哪怕包含旧系统的“丑陋”逻辑，因为业务往往依赖它运行）。
   - 严禁让负责重构的同一 Agent 会话作为测试的唯一作者，防止生成看似全绿但掩盖漏洞的自洽测试。
   - 完整迁移单元（Complete Units）：一次迁移必须端到端完成，包括新路径跑通并**彻底清除旧依赖**，防止遗留代码并存导致后续 Agent 产生先例冲突认知障碍。

7. **先度量再并行化（Parallelize Last）**：
   - 盲目并发只会放大人类审查的瓶颈。评估智能体收益不应看生成的代码行数，而应追踪前置交付时间、人工审查耗时、人工干预次数、生产缺陷与回滚率等硬性工程指标。

## 关联概念与实体

- **核心概念**：[[concepts/概念_Brownfield_Agentic_Engineering_棕地智能体工程]]（遗留代码库智能体工程治理范式）、[[concepts/概念_Harness_Engineering_宿主编排工程]]（宿主编排与安全护栏）、[[concepts/概念_Loop_Engineering循环工程]]（自收敛闭环设计）
- **关联文章**：[[sources/Anthropic 重磅发布：AI Native 软件开发方法论]]、[[sources/读：读代码前先跑的五个 git 命令 - 暗无天日]]

> 📎 **物理文献**：[[raw/articles/Brownfield Agentic Engineering.md]]
