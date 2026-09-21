---
type: concept
tags:
- AI-Agent/context-engineering
summary: 相对于 Vibe Coding（Prompt → Code），规范驱动开发先生成结构化规范再生成代码：
sources:
- wiki/sources/Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝.md
- wiki/sources/浅谈上下文工程_Claude_Code_Manus_Kiro.md
updated: '2026-09-21'
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

## 与上下文工程的关系

规范文档作为长期记忆注入上下文，确保Agent在整个开发过程中保持对需求和架构的一致理解。

## 来源

- [[浅谈上下文工程_Claude_Code_Manus_Kiro]]