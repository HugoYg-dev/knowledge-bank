---
type: entity
tags:
- RAG/retrieval
summary: Cohere 提供的重排序（Rerank）API 服务，用于向量检索后的候选文档精排。
sources:
- wiki/sources/RAG_12痛点与解决方案.md
updated: '2026-07-01'
---

> [!note] 说明
> 注：本页 confidence 为 medium，全文仅作为痛点 2 的方案之一简要提及。

## 简介

Cohere Rerank 是 Cohere 提供的重排序 API 服务，用于对向量检索返回的候选文档按相关性进行精排。

## 应用（12 RAG 痛点文章）

- 先检索 top-10 节点，再用 CohereRerank 返回 top-2，实现精确检索
- LlamaIndex 集成：作为 `node_postprocessors` 传入 query_engine
- 可微调自定义 Cohere Reranker 获得更好检索性能

## 关联

- 相关概念：[[概念_Rerank_重排序]]、[[概念_检索后处理]]
- 来源：[[RAG_12痛点与解决方案]]
