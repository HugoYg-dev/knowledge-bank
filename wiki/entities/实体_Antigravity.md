---
type: entity
tags:
- AI-Agent/coding
- AI-Agent/context-engineering
summary: Google 推出的专业级 AI Coding Agent 与开发环境（CLI 工具 agy），支持深度项目编排、Hooks 扩展机制与长程会话管理。
sources:
- wiki/sources/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案.md
updated: '2026-11-16'
---

# 实体：Antigravity

## 简介

**Antigravity** 是 Google 推出的专业级 AI 编程助手与智能体开发套件（包含核心命令行工具 `agy` 与深度集成的桌面开发环境）。它与 [[entities/实体_Claude_Code|Claude Code]]、[[entities/实体_Codex|Codex]] 并列为主流的高自主性 AI Coding Agent 基础设施。

## 核心系统架构与交互机制

### 1. 运行时会话管理与日志流水
- **会话持久化**：以会话 ID（`conversation-id`）为单位存储于 `~/.gemini/antigravity-cli/brain/<cid>/` 目录；
- **真实流水记录**：通过 `.system_generated/logs/transcript_full.jsonl` 逐步（`step_index`）无损记录所有交互步骤，包含 `USER_INPUT`、模型思维过程与工具调用轨迹；
- **分叉机制（/fork）**：支持从现有会话分叉创建新分支，分叉后新分支从分叉步号开始记录独立会话。

### 2. Hooks 扩展机制与生命周期
Antigravity 提供了强大的零侵入扩展机制（配置文件为 `~/.gemini/config/hooks.json`），允许开发者在 Agent 关键生命周期注入自定义逻辑：
- **`PreInvocation` 钩子**：在每次模型推理前触发，支持动态向当前上下文中注入指令或状态（如 `injectSteps -> systemMessage`）；
- **应用场景**：可用于实现 [[concepts/概念_Post_Compact_Rehydration_压缩后状态回水|Post-Compact Rehydration]]（压缩后无损状态回水）、工作区安全规则前置拦截与外部状态同步。

### 3. 上下文压缩机制（Compaction）
- **触发阈值**：当上下文窗口累计达到约 256K tokens（262,144）或用户输入 `/compact` 时触发；
- **表现形态**：生成 `type == "CHECKPOINT"` 记录，并以一段 `<CONTEXT_SUMMARY>` 概括历史，可通过外挂回水机制进一步消除压缩带来的上下文衰退（Context Rot）。

## 关联

- [[entities/实体_Claude_Code|实体_Claude_Code]]
- [[entities/实体_Codex|实体_Codex]]
- [[concepts/概念_Post_Compact_Rehydration_压缩后状态回水|概念_Post_Compact_Rehydration_压缩后状态回水]]
- [[concepts/概念_上下文工程|概念_上下文工程]]
- [[sources/Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案|Antigravity CLI 压缩后无损回水（Post-Compact Rehydration）与跨 fork 溯源方案]]
