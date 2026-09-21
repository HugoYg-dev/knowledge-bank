---
type: concept
tags:
- AI-Agent/multi-agent
summary: 多智能体系统核心模式：主智能体（orchestrator）负责规划分解，子智能体（worker）并行执行，适合需要大量并行化的复杂任务
sources:
- wiki/sources/Anthropic再发Agent神文_像人类工程师一样思考解决长程任务难题.md
- wiki/sources/Anthropic多智能体研究系统构建.md
- wiki/sources/OpenAI_构建AI智能体实用指南.md
updated: '2026-09-21'
aliases:
- orchestrator-worker
- Orchestrator-Worker
- 主从编排模式
- 概念_orchestrator-worker模式
---

# 概念_Orchestrator_Worker_编排工模式

多智能体系统的主流架构模式，由一个主智能体（orchestrator/lead agent）负责任务分解与协调，多个专职子智能体（worker/subagent）并行执行具体任务。

## 基本结构

```
用户查询
  ↓
LeadResearcher（orchestrator）
  ├── 规划 → Memory（持久化计划）
  ├── 分解任务 → Subagent 1（并行）
  ├── 分解任务 → Subagent 2（并行）
  └── 分解任务 → Subagent N（并行）
         ↓ 汇总
  CitationAgent / 后处理
         ↓
      最终输出
```

## 为什么有效

- **并行上下文窗口**：每个子智能体有独立上下文，可同时探索不同方向
- **压缩效果**：子智能体探索后将最重要内容返回主智能体，而非传递全量信息
- **关注点分离**：不同工具、prompt、探索路径互相隔离
- **token 扩展**：BrowseComp 分析：token 用量解释 80% 性能差异；多智能体有效扩展 token 使用

## 效果数据（Anthropic Research 系统）

- 多智能体 vs 单智能体 Claude Opus 4：性能提升 **90.2%**
- 复杂查询研究时间缩短最高 **90%**（并行工具调用）
- token 消耗：多智能体约为 chat 的 **15×**

## 关键设计决策

**任务分配质量**：子智能体需要明确的目标、输出格式、工具/数据源指引、任务边界；否则会重复工作或遗漏

**规模与查询复杂度匹配**：
- 简单事实：1 个智能体，3-10 次工具调用
- 直接对比：2-4 个子智能体，10-15 次调用
- 复杂研究：10+ 子智能体

**子智能体输出落盘**：写入文件系统，传轻量引用给主智能体，避免多级传话信息损耗

**同步 vs 异步执行**：当前通常同步（等待一批子智能体完成再继续），异步执行可进一步提升并行度但增加协调复杂度

## 适用 vs 不适用场景

| 适合 | 不适合 |
|------|--------|
| 大量可并行化任务 | 智能体间强依赖 |
| 信息超单上下文窗口 | 需共享同一上下文 |
| 接入大量复杂工具 | 大多数编码任务 |
| 开放性研究探索 | 低价值高 token 消耗场景 |

## 相关概念

- [[概念_多智能体协调]]
- [[概念_Agent感知记忆推理三能力]]

## 来源

- [[Anthropic多智能体研究系统构建]]