---
type: "concept"
tags: ["AI-Agent/coding"]
summary: "在系统行为超出代码描述的老旧遗留（棕地）系统中安全引入 AI 编码智能体的工程方法论，核心涵盖红黄绿三色分区治理、特征化测试锁定旧行为、持久化调研备忘录与 Harness 约束沉淀"
aliases:
  - "Brownfield Agentic Engineering"
  - "棕地智能体工程"
  - "棕地系统智能体工程"
  - "Brownfield"
  - "概念_Brownfield_Agentic_Engineering"
sources: ["wiki/sources/Brownfield_Agentic_Engineering.md"]
updated: "2026-10-12"
---

# 概念：Brownfield Agentic Engineering 棕地智能体工程

## 定义

**Brownfield Agentic Engineering（棕地智能体工程）** 是指在存在大量历史技术负债、系统行为无法完全被现有代码表达的老旧遗留系统（Brownfield Codebases）中，规范化、可信化引入 AI 编码智能体（Coding Agents）的系统工程方法论。

在老旧系统中，组织记忆、临时粘合层（duct tape）、边缘服务依赖和跨团队默契常常游离于 Git 代码树之外。如果直接让智能体在无约束环境下自由作业，虽然可能产出“表面可运行”的代码，却往往伴随着错误的系统架构设计和脆弱自洽的假测试。棕地智能体工程的核心使命在于：**使隐藏约束显性化，让低成本变更变得可靠可信**。

## 核心机制与治理体系

### 1. Zones 分区治理模型

依据爆炸半径（Blast Radius）、可观测性与架构隔离程度，由人工对代码库显式划分三色安全防线：

- **Green Zone（绿区）**：测试健全、解耦充分、遵循现代规范的模块。智能体可在此展开紧凑自主循环（Tight Loop）。
- **Yellow Zone（黄区）**：质量参差、规范混杂。智能体改动前必须先行编写并锁定特征化测试（Characterization Tests）。
- **Red Zone（红区）**：涉及鉴权认证、计费、核心权限控制、工资结算等高敏命脉模块。严禁无人值守自动化改动，必须由人类工程师实时结对（Pairing）或直接禁止智能体改动。
- **治理铁律**：由人类定义区域地图（防止模型挑最复杂的代码改动）；区域移动必须凭借扎实测试和负责人审查由黄升绿；区域严格决定智能体操作动词。

### 2. 特征化测试锁定（Characterization Testing）

在对老旧遗留模块进行重构或让智能体改造前，必须首先构建**特征化测试（Characterization Tests）**：
- 目标是机械化钉死并锁定系统当前（哪怕包含历史遗留缺陷）的实际运行行为，防止模型在自洽的绿灯测试下误伤真实生产逻辑。
- **作者隔离原则**：禁止让负责重构的同一智能体上下文独立编写验收测试，测试必须由独立只读阶段或人类工程师预先建立。

### 3. 持久化调研产物（Durable Research Artifact）

- **理解备忘录（Comprehension Memo）**：在对复杂模块改动前，先由只读智能体输出包含入口点、调用链、模块所有者、现有抽象、线上信号及未决问题的持久化备忘录，且所有主张必须引用具体文件与行号。
- **清爽上下文规划**：后续实施从干净的 Context 启动，避免长会话上下文污染与注意力衰减，实施阶段一旦发现事实备忘录与代码现状不符必须立即中止。

### 4. Harness 约束沉淀与完整迁移单元

- **纠偏沉淀法则**：每一次重复出现的人工 Review 纠偏，都是 Harness 缺失的组件。应将其原子化下沉为 Lint 规则、Git Hook、类型契约或 CI 门禁，避免寄希望于大模型记住长文本规范。
- **完整迁移单元（Complete Units）**：一次迁移必须端到端彻底闭环，确保新路径跑通且**老旧依赖被彻底物理移除**；杜绝遗留半吊子过渡代码造成后续智能体产生规则混淆与迁移盲区（Migration Blindness）。

## 关联概念与实体

- **核心关联**：[[concepts/概念_Harness_Engineering_宿主编排工程]]（宿主环境与护栏体系）、[[concepts/概念_Loop_Engineering循环工程]]（自收敛闭环）
- **方法论前序**：[[sources/Anthropic 重磅发布：AI Native 软件开发方法论]]（AI-Native SDLC）
- **来源文献**：[[sources/Brownfield_Agentic_Engineering]]
