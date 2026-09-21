---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: Step-back 提示（退步提示 / Step-Back Prompting）是一种 Query Translation 方法，当问题太具体时退一步生成更广泛、更通用的查询，帮助检索相关的背景信息。通过考虑高层次概念和原则来解决复杂问题。
sources:
- wiki/sources/RAG技巧与底层代码剖析.md
- wiki/sources/RAG查询翻译_Query_Translation.md
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
- wiki/sources/RAG高级优化_query转换之路.md
- wiki/sources/提升RAG问答质量的技术路线.md
- wiki/sources/腾讯查询优化四大类综述.md
updated: '2026-09-21'
aliases:
- Step-back
- Step Back
- 回退提示
- 概念_Step-back提示
---

# 概念_Step_Back_回退提示


## 定义

Step-back 提示（退步提示 / Step-Back Prompting）是一种 Query Translation 方法，当问题太具体时退一步生成更广泛、更通用的查询，帮助检索相关的背景信息。通过考虑高层次概念和原则来解决复杂问题。

## 核心思想

"抽象的目的不是为了让你更迷糊，而是创建了绝对精确的新的语义层次。"

## 目的

- 从具体问题退一步到更广泛的上下文
- 检索更多背景信息
- 提高召回率和上下文覆盖率

## 示例

- 原始："气候变化对环境的影响是什么?"
- Step-back："气候变化的一般影响是什么?"

## 实现

使用 Prompt 指导 LLM 生成更广泛的查询：
```
You are an AI assistant tasked with generating broader, more general queries
to improve context retrieval in a RAG system.
Given the original query, generate a step-back query that is more general
and can help retrieve relevant background information.
```

## 关联

- 上层概念：[[概念_Query_Translation_查询改写与翻译]]
- 相关概念：[[概念_查询重写]]、[[概念_子查询分解]]
- 来源：[[RAG高级优化_query转换之路]]、[[RAG查询翻译_Query_Translation]]