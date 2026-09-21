---
type: concept
tags:
- AI-Agent/coding
summary: 来源：万字长文深入浅出教你优雅开发复杂AIAgent
sources:
- wiki/sources/AI_Agent与AI_Workflow的区别和深度解析.md
- wiki/sources/Agent系统开发经验.md
- wiki/sources/Claude_Agent_Skills_从第一性原理深入剖析.md
- wiki/sources/OpenAI_构建AI智能体实用指南.md
updated: '2026-06-29'
---


# 概念：Agent 开发范式三级进化

**来源**：万字长文深入浅出教你优雅开发复杂AI_Agent

AI Agent 开发模式从简单到复杂的三个阶段，每个阶段解决不同层次的问题。

## Level 1：LLM Agent

聊天机器人形态，通过 Prompt 工程赋予人设，结合多模态/ASR/TTS。2023 年主流，主要用于社交娱乐（角色扮演/陪伴/占卜）。

局限：幻觉、随机性、不可控，难承载严肃场景。

## Level 2：AI Agent

`Agent = LLM + 记忆 + 规划技能 + 工具使用`，2024 年中起向"好用"迈进。

- **规划**：自主拆解任务步骤；预定义工作流（Dify/Coze）结合意图识别提升稳定性
- **记忆**：长期记忆保持上下文连贯性，避免多轮信息丢失
- **工具**：LLM 连接外部世界的关键，MCP 定义工具开发范式

局限：单 Agent 难同时精通所有领域（AI 画图/编程/解题各不同执行流程）。

## Level 3：Multi-Agent

多专业化 Agent 协作网络，每个 Agent 专注特定领域，通过任务分发与协同处理复杂综合性任务。

核心优势：
- **任务聚焦**：单 Agent 专注特定任务，比多工具选择更高效
- **独立优化**：可单独改进单个 Agent 不影响整体
- **问题拆解**：复杂任务分解为可处理子任务

**Human in the Loop**：人类作为特殊 Agent 参与，提供专业判断、质量把控、异常处理、持续优化。

## 关联

- [[概念_Orchestrator_Worker_编排工模式]]
- [[概念_多智能体协调]]
- [[概念_HITL_MCP_人机协同协议架构]]