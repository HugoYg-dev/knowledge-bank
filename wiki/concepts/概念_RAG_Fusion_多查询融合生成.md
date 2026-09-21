---
type: concept
tags:
- RAG/retrieval
- RAG/query
summary: RAG Fusion 是一种在生成阶段融合检索结果的策略，关注如何从多个检索到的文档中综合信息生成高质量回答。过程与 Multi-Query 相似，但对检索到的多篇文档进行筛选过滤之后再输入
  LLM。
sources:
- wiki/sources/DMQR-RAG_多样查询改写.md
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/RAG查询翻译_Query_Translation.md
- wiki/sources/RAG检索_Retrieval入门到精通.md
- wiki/sources/RAG高级优化_检索策略Fusion_HyDE.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- RAG Fusion
- RAG-Fusion
- 融合RAG
- 多查询融合
- 概念_RAG_Fusion
---

# 概念_RAG_Fusion_多查询融合生成


## 定义

RAG Fusion 是一种在生成阶段融合检索结果的策略，关注如何从多个检索到的文档中综合信息生成高质量回答。过程与 Multi-Query 相似，但对检索到的多篇文档进行筛选过滤之后再输入 LLM。

## 流程

1. 根据原始问题生成多个（文中为 4 个）相关问题
2. 分别检索
3. 使用 **Reciprocal Rank Fusion (RRF)** 对检索结果排序过滤
4. 组成最终 RAG 管道

## 与 Multi-Query 区别

- Multi-Query：检索阶段生成多查询，去重合并
- RAG Fusion：对检索结果用 RRF 筛选过滤后再输入 LLM

## 关联

- 相关概念：[[概念_Query_Translation_查询改写与翻译]]、[[概念_RRF_互易秩融合]]、[[概念_DMQR_RAG_动态多查询改写检索]]
- 来源：[[RAG查询翻译_Query_Translation]]、[[DMQR-RAG_多样查询改写]]、[[提升RAG问答质量的技术路线]]