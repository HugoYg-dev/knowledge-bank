---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: Query Translation（查询翻译）是 RAG 高阶技巧，针对用户 Query 模糊或复杂导致检索不准的问题（"Garbage in,
  Garbage out"），通过改写/优化/分解原始查询提升检索和生成效果。
sources:
- wiki/sources/DMQR-RAG_多样查询改写.md
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG查询翻译_Query_Translation.md
- wiki/sources/RAG高级优化_query转换之路.md
- wiki/sources/提升RAG问答质量的技术路线.md
- wiki/sources/美团搜索查询改写实践.md
- wiki/sources/腾讯查询优化四大类综述.md
updated: '2026-09-21'
aliases:
- Query Translation
- 查询翻译
- 查询转换
- 查询改写
- 概念_Query_Translation
---

# 概念_Query_Translation_查询改写与翻译


## 定义

Query Translation（查询翻译）是 RAG 高阶技巧，针对用户 Query 模糊或复杂导致检索不准的问题（"Garbage in, Garbage out"），通过改写/优化/分解原始查询提升检索和生成效果。

## 方法分类

### Re-written（改写）
对原始查询语义重写，保持核心意思不变，调整语言表述。
- **Multi-Query**：生成多个不同表述的查询，分别检索后去重合并，获得更全面的文档集合
- **RAG Fusion**：见 [[概念_RAG_Fusion_多查询融合生成]]

### Decomposition（分解）
将复杂问题拆解为多个独立子问题（sub-question）：
- **逻辑分解**：基于"且""或"等逻辑关系
- **多跳分解**：跨越多个知识领域逐步深入
- 流程一（递归求解）：前一子问题答案结合下一子问题检索文档
- 流程二（并行汇总）：分别回答后集中汇总

### Step-back Question
当问题太具体时退一步问更广泛、概括的问题，获取更大上下文。需提供 few-shot example。提高召回率和上下文覆盖率。

### HyDE
见 [[概念_HyDE_假设文档嵌入]]

## 关联

- 相关概念：[[概念_RAG_Fusion_多查询融合生成]]、[[概念_HyDE_假设文档嵌入]]、[[概念_RAG基础流程]]、[[概念_DMQR_RAG_动态多查询改写检索]]、[[概念_查询扩展]]、[[概念_查询消歧]]、[[概念_查询抽象]]、[[概念_子查询分解]]、RAG五类提升方法
- 来源：[[RAG查询翻译_Query_Translation]]、[[DMQR-RAG_多样查询改写]]、[[RAG_12痛点与解决方案]]、[[提升RAG问答质量的技术路线]]、[[腾讯查询优化四大类综述]]、RAG综述_北大AIGC2024