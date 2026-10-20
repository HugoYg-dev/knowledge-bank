---
type: concept
tags:
- AI-Agent/context-engineering
summary: 相对于 Vibe Coding（Prompt → Code），规范驱动开发先生成结构化规范再生成代码：
sources:
- wiki/sources/Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝.md
- wiki/sources/浅谈上下文工程_Claude_Code_Manus_Kiro.md
- wiki/sources/强烈推荐mattpocock(grill-me)系列skill，分享下我的使用心得.md
updated: '2026-10-20'
aliases:
- Spec-Driven Development
- SDD
- 规范驱动开发
- 概念_Spec_Driven_Development
---

# 概念：Spec-Driven Development（规范驱动开发）

## 定义

相对于 Vibe Coding（Prompt → Code），规范驱动开发先生成结构化规范再生成代码：

**Prompt → Requirements → Design → Tasks → Code**

## Vibe Coding 的局限

1. 要求用户写高质量prompt不现实
2. 快速迭代生成的代码缺乏文档、单元测试、架构约束，引入技术债务
3. 开发者不完全理解生成代码，难以调试维护

## Spec-Driven 的优势

- 优先定义需求文档、系统设计和任务清单，逻辑清晰，与业务目标对齐
- 标准化利于针对性训练和调优大模型返回
- 标准化利于构建完善的上下文（数据、实体、交互）
- 对大项目维护和多人协作更有帮助

## Kiro 的实现

- **requirement.md**：EARS格式（`WHEN [condition] THE SYSTEM SHALL [behavior]`），由LLM根据需求生成，可二次确认修改
- **design.md**：架构设计/模块拆分/接口/数据库表结构/前端实现
- **tasks.md**：开发过程分解为TODO列表，点击按钮启动Task开发，实时更新回溯状态

## Matt Pocock 的工程化实现路径

在开源的 `mattpocock/skills` 体系中，[[entities/实体_Matt_Pocock|Matt Pocock]] 设计了一套标准化的工程化路径，将规范驱动开发与会话隔离解耦结合：

1. **步骤 0（设置标准 `/setup-matt-pocock-skills`）**：项目初始化时固化术语库、文档布局与 Issue 规范；
2. **步骤 1（对齐共识 `/grill-with-docs`）**：通过苏格拉底式提问拷问用户意图，生成共识记录；
3. **步骤 2（落实设计 `/to-spec`）**：把分散的共识整理为正式的设计架构文档（Spec）；
4. **步骤 3（任务拆分 `/to-ticket`）**：将 Spec 拆分成为可独立完成且带依赖拓扑的 Tickets；
5. **步骤 4（TDD 实现 `/implement`）**：在干净的 New Session 中驱动测试先行开发；
6. **步骤 5（双智能体审查 `/code-review`）**：拉起 2 个 Subagent 分别检查代码规范与设计契合度。

## 与上下文工程的关系

规范文档作为长期记忆注入上下文，确保Agent在整个开发过程中保持对需求和架构的一致理解。

## 来源

- [[浅谈上下文工程_Claude_Code_Manus_Kiro]]
- [[sources/强烈推荐mattpocock(grill-me)系列skill，分享下我的使用心得]]