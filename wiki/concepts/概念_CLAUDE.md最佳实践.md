---
type: "concept"
tags:
  - "AI-Agent/coding"
summary: "编写 CLAUDE.md 工程宪法以约束 Agent 行为的高级指南与规范范式，在 AI-Native SDLC 中充当全局指导性基础规则"
sources:
  - "wiki/sources/写好CLAUDE.md_HumanLayer最佳实践.md"
  - "wiki/sources/Anthropic 重磅发布：AI Native 软件开发方法论.md"
updated: "2026-09-07"
---
# 概念：CLAUDE.md最佳实践

## 定义
CLAUDE.md 是在 AI Agent 代码生成和协助场景下，为 LLM（如 Claude Code/Antigravity）提供核心指令、项目架构和行为约束的“宪法级”文件。最佳实践包括定义清晰的单向推导链、严格约束动刀边界以及规范化输出。

## 核心要点
- **明确权限边界**：清晰定义 Agent 可以做什么（如调用特定脚本）和绝对禁止做什么（如物理删除底层原始数据）。
- **统一工具箱调用**：针对常见任务（如 Lint 或清理）明确规定调用特定的自动化脚本，避免大模型自行臆造清理逻辑。
- **模板与约束**：为生成不同类型文档或代码提供强类型的格式模板和段落结构约束，减少输出的随机性和发散。

## 与 Skill、Hook 的三层协同体系
根据 Anthropic 发布的 [[concepts/概念_AI_Native_SDLC_AI原生软件开发生命周期|AI-Native SDLC 方法论]]，团队工程规则分为清晰的三层防线：
1. **基础指南层（CLAUDE.md）**：位于项目根目录，规定工程全貌、构建与测试指令、目录职责与避坑清单，AI 开工前必读，属于全局指导性规则。
2. **专项操作层（Skill）**：聚焦具体某一类垂直任务的操作规程（如“对外接口鉴权”、“数据库迁移 SOP”），按需加载，属于操作级指导性规则。
3. **确定性门禁层（Hook）**：按操作自动触发的拦截脚本（如修改敏感文件、泄露密钥、未经批准执行发布），直接在终端层级硬性阻断，属于不可逾越的强制性安全底线。

## 关联实体 / 概念
- 实体：[[entities/实体_Anthropic]]、[[entities/实体_Claude_Code]]
- 概念：[[concepts/概念_AI_Native_SDLC_AI原生软件开发生命周期]]、[[concepts/概念_HITL_MCP_人机协同协议架构]]

## 来源
- [[sources/写好CLAUDE.md_HumanLayer最佳实践]]
- [[sources/Anthropic 重磅发布：AI Native 软件开发方法论]]
