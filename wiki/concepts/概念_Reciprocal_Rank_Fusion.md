---
type: concept
tags:
- RAG/retrieval
summary: 互易秩融合（Reciprocal Rank Fusion, RRF）是一种排序融合算法，将多个排序结果合并为一个综合排序。核心思想是对每个文档在各排序中的排名取倒数并累加，排名靠前的文档获得更高分数。
sources:
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/RAG查询翻译_Query_Translation.md
- wiki/sources/RAG检索_Retrieval入门到精通.md
- wiki/sources/RAG高级优化_检索策略Fusion_HyDE.md
- wiki/sources/提升RAG问答质量的技术路线.md
- wiki/sources/高德地图AI应用开发岗一面，我跪了！！！.md
- wiki/sources/阿里千问 zvec-grep：让代码搜索变成 AI Agent 基础设施.md
updated: "2026-09-07"
---

# 概念_Reciprocal_Rank_Fusion


## 定义

互易秩融合（Reciprocal Rank Fusion, RRF）是一种排序融合算法，将多个排序结果合并为一个综合排序。核心思想是对每个文档在各排序中的排名取倒数并累加，排名靠前的文档获得更高分数。

## 公式

对文档 d 在多个排序 R₁, R₂, ... 中的综合得分：

```
score(d) = Σ 1 / (k + rank_i(d) + 1)
```

- k：平滑常数，默认 60
- rank_i(d)：文档 d 在第 i 个排序中的排名（从 0 开始）

## 特点

- 无需归一化各检索方法的原始分数
- 对排名前列的文档给予更大权重
- 平滑常数 k 避免排名第一的文档权重过大
- 适用于合并来自不同检索系统/不同查询的结果

## 工程调参

- `k=60` 是常用默认值而非固定规则，应在业务评测集上验证。
- 不同检索源可以加权，但权重过大会使其他召回路线失去作用；高德面试复盘提到地名库精确匹配可以获得更高权重，具体值需由线上 A/B 测试确定。

## 应用场景

- RAG-Fusion：多个查询变体的检索结果用 RRF 融合
- 混合检索：向量 + 关键字检索结果融合
- **代码搜索与 Agent 检索基础设施**：在 [[entities/实体_zvec-grep|zvec-grep (zg)]] 中，RRF 用于融合 BM25 词法检索排名与 Dense Vector 语义检索排名。由于 BM25 分数与余弦相似度分数来自不同度量体系无法直接线性加权，RRF 通过对文档在各列表中的位置取倒数累加（`1 / (k + rank)`），使兼具高语义相关度与确切关键字标识符的代码片段稳定排在最前列。

## 关联

- 相关概念：[[概念_RAG_Fusion]]、[[概念_Fusion_Retrieval]]、[[概念_混合检索]]
- 实体：[[实体_Elasticsearch]]、[[entities/实体_zvec-grep|实体_zvec-grep]]
- 来源：[[sources/阿里千问 zvec-grep：让代码搜索变成 AI Agent 基础设施]]、[[RAG高级优化_检索策略Fusion_HyDE]]、[[ES企业AI搜索实践]]
