---
type: "entity"
tags: ["AI-Agent/coding", "Skill/claude-code"]
summary: "知名 TypeScript 专家与 AI Coding Agent 工作流设计者，构建了以文档驱动、任务拆分与 Smart Zone 控制为核心的开源 Agent Skill 体系（mattpocock/skills）。"
sources: ["wiki/sources/强烈推荐mattpocock(grill-me)系列skill，分享下我的使用心得.md"]
updated: "2026-10-20"
---

# 实体：Matt Pocock

## 简介

**Matt Pocock** 是知名的 TypeScript 开发者、技术教育家（Total TypeScript 创始人），并在 AI 编码智能体（Coding Agents）领域构建了一套备受推崇的工程化 Skill 体系（开源于 `mattpocock/skills`）。他针对大语言模型在软件开发中容易注意力涣散、上下文膨胀和需求走偏的问题，设计了一整套文档驱动与智能体协同工作流。

## 核心工程哲学与贡献

### 1. 规范与文档驱动开发（Spec-Driven Agentic Engineering）
主张在 AI Agent 开始编写代码之前，必须经过严格的共识对齐与需求收敛：
- `/setup-matt-pocock-skills`：配置项目基准、术语库与 Issue 追踪环境。
- `/grill-with-docs`：通过深度追问用户意图，达成并记录初步共识。
- `/to-spec`：将零散共识收敛为形式化的工程规范文档（Spec）。
- `/to-ticket`：将 Spec 拆分为具有明确依赖关系的子工单（Tickets）。

### 2. Smart Zone 上下文分区理论
强调尽管现代 LLM 支持百千级别 Token 上下文，但在实际复杂工程任务中，可靠的推理黄金区间（Smart Zone）通常处于 200K Tokens 以内。为了防止 [[concepts/概念_Context_Rot_上下文衰退|Context Rot（上下文衰退）]]：
- 建议将前期共识与设计收敛在同一会话中；
- 将具体工单分配至完全独立的干净会话（New Session）中执行，依托磁盘文档作为单点真实来源，消除长会话历史包袱。

### 3. 多智能体对抗与隔离审查
在代码实现后，通过 `/code-review` 派生双子智能体（Subagents）分别审查代码实现规范与设计意图契合度，通过角色隔离避免编写智能体的自我验证盲区。

## 关联页面

- **核心概念**：[[concepts/概念_Spec_Driven_Development_规范驱动开发|Spec-Driven Development（规范驱动开发）]]、[[concepts/概念_Context_Rot_上下文衰退|Context Rot（上下文衰退 / Smart Zone）]]、[[concepts/概念_Agent_Skills元工具架构|Agent Skills 元工具架构]]、[[concepts/概念_Claude_Code多智能体协同机制|Claude Code 多智能体协同机制]]
- **相关工具**：[[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]]

## 来源与参考

- [[wiki/sources/强烈推荐mattpocock(grill-me)系列skill，分享下我的使用心得.md]]
