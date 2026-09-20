---
type: concept
tags:
- RSI
- AI-Agent/coding
summary: 将 AI 自我改进做成工程闭环的范式，通过“弱点挖掘—修改提议—保留集验证”或基于微内核的运行时热插拔（如 DSH Agent Loop 插件化）确保
  Harness 代码持续进化且无性能回归。
sources:
- wiki/sources/刚刚，DeepSeek Harness震撼开源：一切皆插件.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
- wiki/sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子.md
updated: '2026-08-20'
---

# 概念：Self-Harness

## 定义

**Self-Harness（自主外壳进化闭环）** 是一种将 [[concepts/概念_RSI递归自我改进|RSI（Recursive Self-Improvement）]] 落地为严格工程实践的范式。它让 Agent 系统在不更改模型权重的前提下，自动诊断自身在长程任务中的弱点并重构 [[concepts/概念_Harness_Engineering|Harness]] 宿主系统代码或在运行时动态替换控制流组件。

---

## 两种主要实现路径

### 1. 离线/静态三步工程闭环（Standard Holdout Loop）
1. **弱点挖掘（Weakness Mining）**：自动化聚合分析历史失败轨迹与报错模式，定位 Harness 的机制与提示词缺陷。
2. **修改提议（Modification Proposal）**：由模型针对缺陷提出具有严格边界的 Harness 代码修改（diff）。
3. **保留集验证（Holdout Verification）**：在保留的独立验证集上测试修改——必须**既解决弱点模式，又不产生全局回归**，才允许自动合并进入生产代码库。

### 2. 运行时动态插件热插拔范式（Runtime Self-Evolution）
- **微内核物理插槽支持**：以 [[entities/实体_DeepSeek_Harness|DeepSeek Harness (DSH)]] 为代表，通过 [[entities/实体_Cordis|Cordis]] 微内核将 Agent Loop 自身解耦为可插拔插件（`ctx.agentLoop`）。
- **运行中自改装机制**：
  1. 智能体在执行任务时，可读取暴露在外的 TypeScript 插件接口与生命周期约束；
  2. 针对特定任务自主生成数十行工具代码或数百行全新控制流 Loop 代码；
  3. 框架利用撤销条（Disposer）管理、依赖变动通知与事务性 HMR 进行进程内平滑热装载，若新代码出错则自动回滚至稳定版本，实现零停机、无残留的自适应演化。

---

## 代表工作与技术演进

- **DeepSeek Harness DSH (2026)**：通过 Cordis 命令式微内核将 Agent Loop 本身作为插件解耦，提供事务性 HMR 与依赖响应，为 Agent 运行中自我演化提供底层基础设施。
- **Self-Harness (Zhang et al. 2026)**：标准弱点-提议-保留集验证闭环。
- **Darwin Gödel Machine (2025)**：Agent 进化自身代码库，SWE-bench Verified 达 50%。
- **AlphaEvolve (2025)**：进化搜索 + 冻结 LLM 生成 diff，优化 GPU kernel 与矩阵乘法。

---

## 关联页面与系统
- **核心系统**：[[entities/实体_DeepSeek_Harness|DeepSeek Harness]]、[[entities/实体_Cordis|Cordis]]、[[entities/实体_Codex|Codex]]、[[entities/实体_Claude_Code|Claude Code]]
- **相关概念**：[[concepts/概念_Harness_Engineering|Harness Engineering]]、[[concepts/概念_Loop_Engineering循环工程|Loop Engineering 循环工程]]、[[concepts/概念_RSI递归自我改进|RSI 递归自我改进]]

---

## 来源与参考
- [[sources/刚刚，DeepSeek Harness震撼开源：一切皆插件|刚刚，DeepSeek Harness震撼开源：一切皆插件]]
- [[sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重|OpenAI前VP Lilian Weng：AI自我改进的近路不是改权重]]
- [[sources/深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子|深度剖析 DeepSeek 最新的 Harness DSH：为了自进化这盘醋包了一整盘饺子]]
