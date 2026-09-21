---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: HyDE（Hypothetical Document Embedding，假设文档嵌入）是一种 Query Translation 方法，核心思想是通过生成"假设文档"，将查询从抽象的自然语言问题转化为检索系统能高效处理的表示。特别适用于复杂问题处理。
sources:
- wiki/sources/DMQR-RAG_多样查询改写.md
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/OpenAI_LLM应用最佳实践.md
- wiki/sources/RAG_12痛点与解决方案.md
- wiki/sources/RAG查询翻译_Query_Translation.md
- wiki/sources/RAG高级优化_检索策略Fusion_HyDE.md
- wiki/sources/提升RAG问答质量的技术路线.md
- wiki/sources/腾讯查询优化四大类综述.md
updated: '2026-09-21'
aliases:
- HyDE
- Hypothetical Document Embeddings
- 假设文档嵌入
- 概念_HyDE
---

# 概念_HyDE_假设文档嵌入


## 定义

HyDE（Hypothetical Document Embedding，假设文档嵌入）是一种 Query Translation 方法，核心思想是通过生成"假设文档"，将查询从抽象的自然语言问题转化为检索系统能高效处理的表示。特别适用于复杂问题处理。

## 流程

1. **输入问题**：用户输入自然语言问题
2. **生成假设文档**：用生成模型（如 GPT）生成一个可能的回答（假设答案），提供强语义上下文，即使可能并不完全正确
3. **检索相关文档**：将假设文档嵌入向量空间或提取关键词作为检索输入
4. **生成最终答案**：结合检索文档和原始问题生成回答

## 补充：零样本场景增强（来源：检索策略Fusion_HyDE）

本文进一步描述 HyDE 尤其增强零样本场景中的密集检索：
1. 查询扩展：LLM 根据用户查询生成假设答案或文档
2. 增强嵌入：嵌入假设文档，创建更丰富的语义搜索空间
3. 相似性搜索：用嵌入查找数据库中最相关的实际文档
4. 知情生成：检索文档 + 原始查询生成最终响应

## 关联

- 相关概念：[[概念_Query_Translation_查询改写与翻译]]、[[概念_混合检索]]、[[概念_Agentic_RAG_智能体检索增强生成]]
- 实体：[[实体_Elasticsearch]]
- 来源：[[RAG查询翻译_Query_Translation]]、[[RAG高级优化_检索策略Fusion_HyDE]]、RAG综述_中科院2025、[[ES企业AI搜索实践]]、[[RAG_12痛点与解决方案]]、[[DMQR-RAG_多样查询改写]]、[[提升RAG问答质量的技术路线]]