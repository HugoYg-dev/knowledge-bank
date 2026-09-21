---
type: concept
tags:
- AI-Agent/deep-research
summary: IterResearch 是通义 DeepResearch 提出的创新 Agent 推理范式，用于解决多步研究任务中 Agent 将所有信息堆积在单一不断扩展的上下文窗口时出现的认知瓶颈和噪音污染问题。
sources:
- wiki/sources/Tongyi DeepResearch的技术报告探秘.md
- wiki/sources/通义 DeepResearch：开源 AI 智能体的新纪元.md
updated: '2026-06-29'
---


# 概念：IterResearch 范式

## 定义

IterResearch 是通义 DeepResearch 提出的创新 Agent 推理范式，用于解决多步研究任务中 Agent 将所有信息堆积在单一不断扩展的上下文窗口时出现的**认知瓶颈和噪音污染**问题。

## 与 ReAct 的对比

| 维度 | ReAct | IterResearch |
|------|-------|--------------|
| 上下文管理 | 所有工具调用结果累积在上下文（单次网页调用可占 10k+ token） | 动态维护精简工作空间，只保留上一轮最重要输出 |
| 核心输出 | 无结构化报告 | 维护持续演变的核心报告 |
| 适用场景 | 常规多轮推理 | 极端复杂的多步长程研究任务 |
| 上下文窗口利用 | 易被工具返回结果污染 | 每轮重构精简工作空间，保持认知焦点 |

## 工作机制

针对多步研究任务，IterResearch 将其解构为一系列研究回合：

1. 每一轮仅使用上一轮最重要的输出重建精简工作空间
2. 在专注工作空间中分析问题，将关键发现整合成**不断演变的核心报告**
3. 决定下一步行动：收集更多信息 or 提供最终答案
4. 这种"综合与重构"的迭代过程使 Agent 在长期任务中保持清晰认知焦点

## Research-Synthesis 框架

在 IterResearch 基础上的进一步扩展：
- 并行使用多个 IterResearch Agent 探索同一问题
- 最终整合各 Agent 的完善报告和结论
- 在有限上下文窗口内考虑更广泛的研究路径
- 效果数据（推测）：HLE 比 ReAct 高 7.9pt，BrowseComp 高 14pt

## 训练数据支撑

SFT 阶段基于 ReAct 和 IterResearch 框架通过拒绝采样构建轨迹：
- ReAct 轨迹：注入丰富推理行为，加强结构化格式遵循能力
- IterResearch 轨迹：融合推理/规划/工具使用，加强持续规划能力

## 局限性

IterResearch 模式对核心报告质量有严重依赖：若报告生成模块存在幻觉或遗漏，对整体影响可能是致命的。截至 2025-09-23，IterResearch 代码未随开源发布（仅开源 ReAct 模式）。

## 关联

- [[概念_Deep_Research_Agent_定义与分类]]
- [[概念_Context_Rot_上下文衰退]]
- [[实体_通义DeepResearch]]

## 来源

- [[通义 DeepResearch：开源 AI 智能体的新纪元]]
- [[Tongyi DeepResearch的技术报告探秘]]