---
type: concept
tags:
- RAG/retrieval
summary: ColBERT（Contextualized Late Interaction over BERT）是一种基于细粒度 token 级嵌入相似性计算的检索方法。相比将整篇文档/块压缩成单一向量，ColBERT
  对每个 token 进行嵌入，实现更精细的匹配。
sources:
- wiki/sources/ColBERTv2残差压缩演进.md
- wiki/sources/ColBERT原理与延迟交互机制.md
- wiki/sources/RAG系统设计_语义搜索与KG驱动选型.md
- wiki/sources/RAG索引进阶_Indexing.md
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
- wiki/sources/提升RAG问答质量的技术路线.md
updated: '2026-09-21'
aliases:
- ColBERT
- Contextualized Late Interaction over BERT
- 延迟交互检索
- 多向量延迟交互
- 概念_ColBERT
---

# 概念_ColBERT_多向量延迟交互检索


## 定义

ColBERT（Contextualized Late Interaction over BERT）是一种基于细粒度 token 级嵌入相似性计算的检索方法。相比将整篇文档/块压缩成单一向量，ColBERT 对每个 token 进行嵌入，实现更精细的匹配。

## 步骤与原理

1. **Token 级别相似度计算**：对查询和文档中的每个 token 分别计算上下文嵌入
2. **最大池化（MaxSim）操作**：对查询中每个 token，取其与文档中所有 token 的最大相似度
3. **选择最相关文档**：基于 MaxSim 得分排序选取

## 为什么有效

- **关注细粒度匹配**：即使查询中只有部分 token 能匹配，这些匹配也能显著影响最终得分
- **兼顾上下文信息**：token 嵌入是基于上下文生成的（BERT），捕捉更丰富语义
- **鲁棒性**：不依赖严格字面匹配，能处理词法变体、同义词、句子结构变化

## 延迟交互（Late Interaction）

- 与"早期交互"（编码阶段即融合 query+doc，如 BERT Cross-Encoder）对比：延迟交互让 query 和 doc 独立编码，把交互推迟到相似度计算阶段
- 优势：文档向量可离线预计算并存入索引（如 FAISS），在线检索仅需编码 query 并执行 MaxSim，复杂度远低于交互模型
- 精度接近交叉编码器（rerank 模型），但查询延迟从数秒降至几十毫秒
- 实验（BGEM3FlagModel）：query "What is BGE M3?"(8 token) vs doc "Definition of BM25"(7 token)，归一化得分 0.4768 与官方 colbert_score 完全一致；稠密向量余弦相似度 0.4103，ColBERT 因取 token 级最大相似度而得分更高

## 开源实现

- GitHub: https://github.com/stanford-futuredata/ColBERT
- 论文（ColBERTv2）: https://arxiv.org/abs/2112.01488

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_RAPTOR_递归树状检索索引]]、[[概念_Multi_Representation_Indexing_多表征索引]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[概念_ColBERTv2残差压缩]]
- 实体：[[实体_ColBERT]]、[[实体_BGE-M3]]
- 来源：[[RAG索引进阶_Indexing]]、[[从BM25到Multi-Vector_6种Embedding演进路线]]、[[ColBERT原理与延迟交互机制]]、[[ColBERTv2残差压缩演进]]、[[提升RAG问答质量的技术路线]]