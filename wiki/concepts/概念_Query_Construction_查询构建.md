---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: Query Construction（查询构造）是根据用户输入的自然语言问题，通过语义解析、上下文理解以及路由后的结果，生成特定领域数据源所需的查询语句或格式化内容。目标是最大化数据源检索的准确性和相关性。
sources:
- wiki/sources/RAG查询构造_Query_Construction.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- Query Construction
- 查询构建
- 查询构造
- 概念_Query_Construction
---

# 概念_Query_Construction_查询构建


## 定义

Query Construction（查询构造）是根据用户输入的自然语言问题，通过语义解析、上下文理解以及路由后的结果，生成特定领域数据源所需的查询语句或格式化内容。目标是最大化数据源检索的准确性和相关性。

## 核心场景

- 许多 Vector Store 都有 meta data（元数据）
- 将自然语言转成可用于 meta data 过滤的结构化查询
- 示例："Videos on chat langchain published after 2024" → 结构化查询（content_search + publication_date 过滤）

## 实现方式

1. 为结构化搜索查询定义 schema（架构）
2. 编写 Prompt 让 LLM 将自然语言转成合适的结构化查询
3. 支持对 content/title 做非结构化搜索 + 对 view count、publication date、length 做范围过滤

## 关联

- 相关概念：[[概念_RAG_Routing_检索智能路由]]、[[概念_RAG基础流程]]、[[概念_向量数据库]]
- 来源：[[RAG查询构造_Query_Construction]]、[[提升RAG问答质量的技术路线]]