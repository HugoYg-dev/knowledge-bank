---
type: source
tags:
- AI-Agent/skill
- AI-Agent/coding
summary: 解析 Anthropic 官方为 Claude Code 开发的 13 个第一方领域知识插件，说明如何将静态规范转化为动态运行时检查与分阶段工程引导。
sources:
- raw/articles/Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝.md
updated: '2026-07-02'
---

# Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝

## 核心贡献与摘要

Anthropic 官方为 Claude Code 提供了 13 个深度集成的第一方插件（位于 `plugins/` 目录），通过 `/plugin install` 命令管理。与原子化的社区 Skill（告诉 Agent 能做什么）不同，**领域知识插件的核心是解决“Agent 应该知道什么”**，将原本静态保存在 `CLAUDE.md` 等文档中的业务规则与代码架构规范，转化为动态的运行时检查（Hooks、专门 Agent 与命令）。

## 关键要点与引文

1. **从静态约束到动态拦截**：
   虽然 `CLAUDE.md` 能作为项目上下文注入，但它无法主动扫描代码库或在 PR 合并前自动审查。插件机制结合 Hooks 和 Agent 实现了实时守护（如 `security-guidance` 在 PreToolUse 阶段静默拦截风险，`code-review` 对照 `CLAUDE.md` 逐条检查 PR）。
2. **核心插件全景与工程实践**：
   - `/code-review`：多 Agent 并行执行本地 diff 审查，结合 `REVIEW.md` 与 `CLAUDE.md` 给出精确到行号的审查发现。
   - `/feature-dev`：严格的 7 阶段结构化开发流程（需求澄清 → 探索 → 提问 → 架构设计 → 实现 → 审查 → 总结），强制规定“回答完全部问题之前不得进入设计阶段，审查通过之前不合并”。
3. **组合架构设计**：
   各个领域知识插件可无缝组合，形成强大的 Harness 支撑系统。

## 关联实体与概念

- 概念关联：[[概念_私域知识工程]]、[[概念_上下文工程]]、[[概念_Spec_Driven_Development_规范驱动开发]]
- 实体关联：[[实体_Anthropic_Research系统]]

---
> 📎 **物理文献**：[[raw/articles/Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝.md]]