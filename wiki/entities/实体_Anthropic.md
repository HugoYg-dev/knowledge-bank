---
type: "entity"
tags:
  - "AI-Agent/skill"
  - "LLM/arch"
  - "AI-Agent/coding"
summary: "Anthropic 为由前 OpenAI 研究员创立的安全导向前沿 AI 研究实验室，研发 Claude 系列模型、Agent Skills 元工具架构、AI-Native SDLC 方法论与三层安全规则防护体系。"
sources:
  - "wiki/sources/代码强化学习的双刃剑_前沿模型为何集体走向作弊.md"
  - "wiki/sources/Claude_Agent_Skills_从第一性原理深入剖析.md"
  - "wiki/sources/Anthropic 重磅发布：AI Native 软件开发方法论.md"
  - "wiki/sources/A_guide_to_the_anatomy_of_effective_commerce_agents.md"
updated: "2026-09-15"
---
# 实体：Anthropic

## 概述

**Anthropic** 是一家专注于 AI 安全与前沿大模型研发的公司，由 Dario Amodei 等前 OpenAI 研究团队于 2021 年联合创立。

## 关键技术贡献

- **Claude 系列模型**：Claude 3/3.5/3.7 系列旗舰模型。
- **Agent Skills 架构**：在 Claude Code 中开创了通过提示词模板与元工具扩展智能体能力的 Agent Skills 设计范式。
- **接种提示词（Inoculation Prompting）**：针对强化学习 Reward Hacking 提出在训练数据中嵌入接种提示词重构语义，防范作弊与对齐假象。
- **AI-Native SDLC 方法论与三层规则体系**：提出以版本控制产物驱动的闭环自转（The Loop）重构研发流程，确立 `CLAUDE.md`（项目总则）、`Skill`（任务规程）与 `Hook`（确定性硬门禁）的三层防御体系，倡导计划先行（Plan Mode）与子智能体（Subagents）上下文解耦。
- **电商智能体系统工程与表现层工具化**：针对高耦合长程交易场景，系统化确立了单模型结合技能架构（Skills over Subagents）、表现层工具化（[[concepts/概念_Presentation_Tools|Presentation Tools]]）、三段式 Prompt Caching、异步三层记忆与 Harness 确定性安全门禁（Staging 机制与服务端白名单 ID）的完整落地规范。

## 来源

- [[sources/代码强化学习的双刃剑_前沿模型为何集体走向作弊]]
- [[sources/Claude_Agent_Skills_从第一性原理深入剖析]]
- [[sources/Anthropic 重磅发布：AI Native 软件开发方法论]]
- [[sources/A_guide_to_the_anatomy_of_effective_commerce_agents]]
