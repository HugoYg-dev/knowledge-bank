---
type: entity
tags:
- AI-Agent/multi-agent
summary: Anthropic 多智能体研究系统，Claude Research 功能的底层架构，orchestrator-worker 模式实现
sources:
- wiki/sources/Anthropic x ClaudeCode 官方插件：AI Agent 的领域知识插件——鸟窝.md
- wiki/sources/Anthropic再发Agent神文_像人类工程师一样思考解决长程任务难题.md
- wiki/sources/Anthropic多智能体研究系统构建.md
- wiki/sources/MCP五大原语与Web化.md
- wiki/sources/MCP遇上代码执行.md
- wiki/sources/从提示员到系统架构师：Loop Engineering 的范式跃迁.md
updated: '2026-06-29'
---
# 实体_Anthropic_Research系统

Anthropic 为 Claude 构建的多智能体研究功能（Claude Research），支持跨 Web、Google Workspace 和各类集成进行复杂任务研究。

## 架构组件

- **LeadResearcher**：主智能体，使用 Claude Opus 4，负责规划、任务分解、汇总
- **Subagents**：子智能体，使用 Claude Sonnet 4，并行执行具体搜索任务
- **CitationAgent**：专职处理引用，定位具体引用位置
- **Memory**：外部持久化存储，保存研究计划（防上下文超限丢失）

## 关键数据

- 多智能体 vs 单智能体 Claude Opus 4：提升 **90.2%**
- 并行化后复杂查询研究时间缩短最高 **90%**
- token 消耗约为 chat 的 15×

## 开发团队

Jeremy Hadfield, Barry Zhang, Kenneth Lien, Florian Scholz, Jeremy Fox, Daniel Ford 及 Anthropic Apps 工程团队

## 开源资源

- Cookbook 提示词示例：https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents/prompts

## 相关概念

- [[概念_Orchestrator_Worker_编排工模式]]
- [[概念_多智能体协调]]
- [[概念_Agent思考工具]]

## 来源

- [[Anthropic多智能体研究系统构建]]