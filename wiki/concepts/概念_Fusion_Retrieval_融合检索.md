---
type: concept
tags:
- RAG/retrieval
summary: 融合检索（Fusion Retrieval）是一种文档搜索方法，结合基于向量的语义检索和基于 BM25 的关键字匹配检索。通过加权组合两种方法的得分，在概念相似性和关键字相关性之间取得平衡。
sources:
- wiki/sources/RAG高级优化_检索策略Fusion_HyDE.md
updated: '2026-09-21'
aliases:
- Fusion Retrieval
- 融合检索
- 混合检索
- 概念_Fusion_Retrieval
---

# 概念_Fusion_Retrieval_融合检索


## 定义

融合检索（Fusion Retrieval）是一种文档搜索方法，结合基于向量的语义检索和基于 BM25 的关键字匹配检索。通过加权组合两种方法的得分，在概念相似性和关键字相关性之间取得平衡。

## 流程

1. 接受查询，分别执行向量检索和 BM25 检索
2. 向量得分和 BM25 得分各自 min-max 归一化到 [0, 1]
3. 计算加权组合：`combined = alpha * vector_scores + (1-alpha) * bm25_scores`
4. 按综合得分排序，返回 top-k 文档

## 关键参数

- **alpha**：控制向量检索与关键字检索的权重平衡（0~1）
  - alpha=1：纯向量检索
  - alpha=0：纯 BM25 检索
  - alpha=0.5：各占一半（默认）

## 优点

- 同时捕获概念相似度和精确关键字匹配
- alpha 参数灵活调整，适配不同用例
- 减轻单一方法弱点，处理更大范围查询
- 易适配不同向量存储或关键字检索后端

## 与 RAG-Fusion 区别

- Fusion Retrieval：关注检索阶段两种检索方式的分数融合
- RAG-Fusion：关注多查询扩展 + RRF 排序融合

## 关联

- 相关概念：[[概念_BM25_最佳匹配25算法]]、[[概念_Embedding与向量检索]]、[[概念_RAG_Fusion_多查询融合生成]]、[[概念_RRF_互易秩融合]]
- 来源：[[RAG高级优化_检索策略Fusion_HyDE]]