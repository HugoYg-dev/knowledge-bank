---
type: source
tags:
- RSI
- AI-Agent/coding
summary: Lilian Weng 新文剖析 Harness Engineering（外壳工程）：指出递归自我改进（RSI）近期的近路不是改模型权重，而是围绕模型搭建的
  Harness 系统，总结了三大设计模式、五级优化阶梯与自我改进工程闭环。
sources:
- raw/articles/OpenAI前VP Lilian Weng 新长文：AI 自我改进的近路，不是改权重.md
updated: '2026-07-22'
---

# OpenAI前VP Lilian Weng 新长文：AI 自我改进的近路，不是改权重

## 来源信息

- **原标题**：OpenAI前VP Lilian Weng 新长文：AI 自我改进的近路，不是改权重
- **作者**：[[entities/实体_翁荔_Lilian_Weng|Lilian Weng]]（Mountain Gu 导读简评）
- **发布日期**：2026-07-04（博文） / 2026-07-07（微信导读）
- **原始链接**：[Lil'Log - Harness Engineering for Self-Improvement](https://lilianweng.github.io/posts/2026-07-04-harness/)

---

## 核心要点

1. **RSI 路径范式重塑**：流传 60 年的[[concepts/概念_RSI递归自我改进|递归自我改进（RSI）]]智能爆炸剧本（I.J. Good 1965 / Yudkowsky 2008）需要理性降温。近期的 RSI 不太可能从模型直接改写自身权重开始，而是从模型外层的“壳”——[[concepts/概念_Harness_Engineering|Harness Engineering（外壳工程）]] 开始。
2. **Harness 系统的第一性原理定义**：Harness 是围绕基础模型（Raw Model）的那套系统，负责编排执行、思考规划、工具行动、上下文感知与管理、产物存储及结果评估。Harness 之于大模型如同操作系统之于硬件。在真实世界上下文中，Harness 的设计与模型的原始智能同等重要。
3. **当下 Harness 的三大设计模式**：
   - **工作流自动化**：目标导向的计划-执行-观察-改进循环，让模型分析自身的轨迹与失败。
   - **文件系统即持久记忆**：将实验日志、代码 diff、错误追踪落盘为物理文件，利用 bash 接口管理长距离上下文。
   - **子代理与后台任务**：主代理派生子代理并行工作，搭配显式进程管理（启动、日志检查、取消与结果合并）。
4. **Agent 优化的五级演进阶梯**：
   优化对象由浅入深层层递进：**优化提示词 $\rightarrow$ 优化结构化上下文 $\rightarrow$ 优化工作流 $\rightarrow$ 优化 Harness 代码 $\rightarrow$ 优化“优化器”代码**。到达阶梯尽头即系统自己修改自身 Harness。
5. **自我改进的 Harness 工程闭环**：
   - **STOP (2023)**：让改进器改进自身，自动涌现遗传算法与模拟退火，但也揭示了**基座模型能力的底线要求**（弱模型如 GPT-3.5 越改越差）。
   - **[[concepts/概念_Self-Harness|Self-Harness (2026)]]**：形成“弱点挖掘—修改提议—保留集验证”工程闭环，确保解决弱点且不出现性能回归。
   - **Darwin Gödel Machine & AlphaEvolve (2025)**：让 Agent 进化自身代码库或生成代码 diff，在 SWE-bench Verified 与矩阵乘法/GPU kernel 优化中超越人类手工打造的 Agent。
6. **自我改进面向的七大硬骨头**：
   - 弱/模糊评估器（难以评估研究品味与长期价值）；
   - 模型不擅长认输（训练数据缺乏失败经验导致难以修剪搜索空间）；
   - 多样性坍塌（过度收敛于已知高分模式）；
   - Reward Hacking（需将评估器与权限放在循环外部）；
   - 仓库长期健康无人管（可维护性与兼容性不在沙箱奖励中）；
   - **人类角色的定位**：人类应该在技术栈上往上走（设计目标与上下文），而非被请出循环。

---

## 关联实体与概念

### 关键实体
- [[entities/实体_翁荔_Lilian_Weng|Lilian Weng]] — 前 OpenAI 安全研究 VP，Thinking Machines Lab 联合创始人，Lil'Log 作者
- [[entities/实体_Thinking_Machines_Lab|Thinking Machines Lab]] — Lilian Weng 联合创办的 AI 实验室
- [[entities/实体_Claude_Code|Claude Code]] — Anthropic 推出的 CLI 编码智能体，Harness 典范
- [[entities/实体_Codex|Codex]] — OpenAI 推出的编码智能体系统

### 关键概念
- [[concepts/概念_Harness_Engineering|Harness Engineering]] — 围绕大模型的宿主与编排系统工程
- [[concepts/概念_RSI递归自我改进|RSI 递归自我改进]] — 系统自动优化机制
- [[concepts/概念_Harness优化阶梯|Harness 优化阶梯]] — Prompt 到 Optimizer 代码的五级演进
- [[concepts/概念_Self-Harness|Self-Harness]] — 弱点挖掘与保留集验证的自我改进闭环

---

> 📎 **物理文献**：[[raw/articles/OpenAI前VP Lilian Weng 新长文：AI 自我改进的近路，不是改权重.md]]
