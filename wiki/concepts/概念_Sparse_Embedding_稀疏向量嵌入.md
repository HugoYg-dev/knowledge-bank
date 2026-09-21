---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: Sparse Embedding（关键词式稀疏向量）将文本表示为高维稀疏向量，绝大部分位置为 0，仅关键词对应维度被激活。
sources:
- wiki/sources/ES企业AI搜索实践.md
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
updated: '2026-09-21'
aliases:
- Sparse Embedding
- 稀疏向量
- 稀疏嵌入
- 概念_Sparse_Embedding
---

# 概念_Sparse_Embedding_稀疏向量嵌入


## 定义

Sparse Embedding（关键词式稀疏向量）将文本表示为高维稀疏向量，绝大部分位置为 0，仅关键词对应维度被激活。

## 特点

- 典型实现：TF-IDF、BM25、SPLADE
- 向量形态：50000+ 维，>95% 位置为 0
- 相似度计算：余弦或点积，仅激活维度参与运算
- 优点：关键词命中精度极高，可解释性强（能直接看到哪一词得分）
- 痛点：只做精确关键词匹配，同义词/句式变化即失效；高维稀疏导致存储索引膨胀

## 适用场景

- 关键词精确匹配场景首选
- 案例：新闻版权去重，BM25 检索准确率达 98%

## 关联

- 相关概念：[[概念_BM25_最佳匹配25算法]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_Fusion_Retrieval_融合检索]]
- 来源：[[从BM25到Multi-Vector_6种Embedding演进路线]]