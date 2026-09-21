---
type: concept
tags:
- RAG/retrieval
summary: Routing（路由）是 RAG 中根据用户查询内容智能选择最适合的检索路径或推理逻辑的过程。在多数据源、多检索器或多任务场景下显著提升系统性能和准确性。
sources:
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG挑战赛冠军方案.md
- wiki/sources/RAG路由_Routing.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- RAG Routing
- 检索路由
- 智能路由
- 概念_RAG_Routing
---

# 概念_RAG_Routing_检索智能路由


## 定义

Routing（路由）是 RAG 中根据用户查询内容智能选择最适合的检索路径或推理逻辑的过程。在多数据源、多检索器或多任务场景下显著提升系统性能和准确性。

## 两种实现类型

### Logical Routing（逻辑路由）
- 基于明确规则或分类模型对查询分流
- 将查询分类到不同的数据库、知识库或 API
- 适用于结构化问题或明确数据源场景
- 使用 `with_structured_output` 格式化为结构化数据
- 示例：根据编程语言自动选择 python_docs / js_docs / golang_docs

### Semantic Routing（语义路由）
- 基于向量化的语义相似性动态选择最优路径
- 通过嵌入技术匹配最合适的 Prompt 或检索器
- 适用于模糊查询或需要灵活响应的场景
- 示例：根据用户问题与物理/数学 Prompt 的余弦相似度选择

## 关联

- 相关概念：[[概念_RAG基础流程]]、[[概念_Query_Translation_查询改写与翻译]]、[[概念_Query_Construction_查询构建]]、[[概念_多查询路由]]、[[概念_Adaptive_RAG_自适应检索增强生成]]
- 来源：[[RAG路由_Routing]]、[[RAG_12痛点与解决方案]]、[[RAG挑战赛冠军方案]]、[[提升RAG问答质量的技术路线]]