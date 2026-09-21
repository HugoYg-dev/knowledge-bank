---
type: entity
tags:
- LLM/hallucination
- AI-Agent/coding
summary: OpenAI 前 VP、安全研究负责人，Thinking Machines Lab 联合创始人，Lil'Log 作者，提出 Agent 架构公式与
  Harness Engineering 理论。
sources:
- wiki/sources/大模型幻觉陷阱_AGI之路04期.md
- wiki/sources/翁荔_LLM外在幻觉_原因检测抵抗.md
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
updated: '2026-07-22'
---

# 实体：翁荔（Lilian Weng）

OpenAI 前 VP、安全研究负责人，Thinking Machines Lab 联合创始人，Lil'Log 作者。

## 基本信息

- 北大毕业，2018 年加入 OpenAI，曾任 OpenAI 安全研究 VP
- GPT-4 项目主要参与者：预训练、强化学习 & 对齐、模型安全
- 2026 年联合创办 Thinking Machines Lab

## 代表性贡献

### Agent 架构公式（2023）
- 提出 Agent = 大模型 + 记忆 + 主动规划 + 工具使用
- 被誉为"有关 Agent 最经典和被广泛引用的综述之一"

### LLM 外在幻觉 Blog（2024）
- 原文：https://lilianweng.github.io/posts/2024-07-07-hallucination/
- 提出外在幻觉（extrinsic hallucination）概念
- 详解产幻原因、检测方法（FActScore/SAFE）与抵抗方法（RARR/CoVe/FLAME）

### Harness Engineering 综述（2026）
- 原文：https://lilianweng.github.io/posts/2026-07-04-harness/
- 为 Harness Engineering 正名，提出递归自我改进（RSI）的近路不是改模型权重而是优化 Harness 外壳
- 总结三大设计模式、五级优化阶梯与自我改进工程闭环（STOP、Self-Harness 等）

## 相关资源

- [[OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]] — Harness Engineering 综述摘要
- [[翁荔_LLM外在幻觉_原因检测抵抗]] — 幻觉 Blog source 页
- [[概念_Harness_Engineering_宿主编排工程]] — Harness Engineering 概念
- [[概念_LLM外在幻觉与上下文内幻觉]] — 幻觉定义框架