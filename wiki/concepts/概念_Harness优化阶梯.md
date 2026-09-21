---
type: concept
tags:
- RSI
- AI-Agent/context-engineering
summary: Agent 系统优化对象的五级演进阶梯：Prompt -> 结构化上下文 -> 工作流 -> Harness 代码 -> 优化器代码。
sources:
- wiki/sources/OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重.md
updated: '2026-08-04'
---
# 概念：Harness优化阶梯

## 阶梯层级拆解

Agent 系统的优化对象呈现由浅入深、自动化程度递增的五级阶梯：

| 阶梯层级 | 优化目标 | 典型代表 / 机制 |
| --- | --- | --- |
| **Level 1: 提示词优化** | 优化静态系统提示词 | Manual Prompting / Few-shot |
| **Level 2: 结构化上下文优化** | 动态管理上下文内容与格式 | ACE (战术手册)、MCE (双层上下文优化) |
| **Level 3: 工作流优化** | 搜索与重构 Agent 步骤流 | AFlow (MCTS 搜索工作流图结构) |
| **Level 4: Harness 代码优化** | 直接修改系统宿主代码 | Self-Harness、Darwin Gödel Machine |
| **Level 5: 优化器代码优化** | 优化“自我改进算法”本身 | STOP (让改进器修改自身，自动涌现遗传/退火算法) |

## 阶梯演进意义

到达 Level 4 与 Level 5 意味着系统具备了修改自身[[concepts/概念_Harness_Engineering_宿主编排工程|Harness]]与优化算法的能力，形成了完整的[[concepts/概念_RSI递归自我改进|递归自我改进（RSI）]]工程落地路径。

## 来源与参考

- [[OpenAI前VP_Lilian_Weng_AI自我改进的近路不是改权重]]
- [[concepts/概念_Harness_Engineering_宿主编排工程]]
- [[sources/2026-04-06_The-Anatomy-of-an-Agent-Harness_19d64a|The Anatomy of an Agent Harness]]
