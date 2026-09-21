---
type: entity
tags:
- RAG/retrieval
summary: 斯坦福提出的基于 BERT 后期交互（Late Interaction）的高精度多向量检索模型。
sources:
- wiki/sources/ColBERTv2残差压缩演进.md
- wiki/sources/ColBERT原理与延迟交互机制.md
- wiki/sources/RAG索引进阶_Indexing.md
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-07-01'
---
## 简介

ColBERT（Contextualized Late Interaction over BERT）是斯坦福 FutureData 实验室提出的基于 BERT 的细粒度检索模型，采用 token 级嵌入相似性计算（late interaction）实现高质量检索。

## 核心机制

- Token 级别相似度计算
- MaxSim 最大池化操作
- 基于上下文的 token 嵌入

详见概念页 [[概念_ColBERT_多向量延迟交互检索]]。

## 版本

- **ColBERT v1**：延迟交互原始版本，token 级 MaxSim
- **ColBERTv2**（SIGIR 2021）：引入残差压缩（k-means 聚类+残差量化），存储减少 6-10 倍，性能损失仅 1-2%；附加知识蒸馏和改进损失函数

## 资源

- 开源实现：https://github.com/stanford-futuredata/ColBERT
- 论文（ColBERTv2）：https://arxiv.org/abs/2112.01488
- LangChain 集成（RAGatouille）：https://python.langchain.com/docs/integrations/retrievers/ragatouille

## 关联

- 相关概念：[[概念_ColBERT_多向量延迟交互检索]]、[[概念_ColBERTv2残差压缩]]、[[概念_Embedding与向量检索]]
- 来源：[[RAG索引进阶_Indexing]]、[[从BM25到Multi-Vector_6种Embedding演进路线]]、[[ColBERT原理与延迟交互机制]]、[[ColBERTv2残差压缩演进]]
