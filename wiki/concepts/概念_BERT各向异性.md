---
type: concept
tags:
- RAG/embedding
- DeepLearning
summary: BERT 各向异性（Anisotropy）指 BERT 等 Transformer 预训练模型产生的词向量在向量空间中占据一个狭窄的圆锥形体，导致余弦相似度不能很好地表达词间语义相关性。
sources:
- wiki/sources/一文详尽之Embedding.md
updated: '2026-07-06'
---

# 概念_BERT各向异性


## 定义

BERT 各向异性（Anisotropy）指 BERT 等 Transformer 预训练模型产生的词向量在向量空间中占据一个狭窄的圆锥形体，导致余弦相似度不能很好地表达词间语义相关性。

## 表现

- 高频词都靠近原点（所有词的均值），低频词远离原点
- 高频词分布紧凑，低频词分布稀疏
- 即使高频词与低频词语义等价，词频差异也带来向量距离的巨大差异
- 最终向量都挤在一起，彼此余弦相似度都很高
- 不只 BERT，GPT-2 等大多数 Transformer 架构预训练模型都有类似问题

## 问题本质

- 好的向量应同时满足 **alignment**（相似向量距离相近）和 **uniformity**（向量空间均匀分布，最好各向同性）
- 各向异性违反 uniformity，导致相似度计算失效

## 优化方法

1. **有监督优化**：通过标注语料构建双塔/单塔 BERT 微调（代表：[[概念_Sentence_BERT_孪生网络句向量]]）
2. **无监督优化**：
   - 线性变换：Bert-flow（流式生成模型映射到标准高斯分布）、Bert-whitening（白化操作）
   - 对比学习：[[概念_SimCSE_简单对比学习句向量]]（Dropout mask 增广 + 对比学习）

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_词向量]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_SimCSE_简单对比学习句向量]]
- 来源：[[一文详尽之Embedding]]