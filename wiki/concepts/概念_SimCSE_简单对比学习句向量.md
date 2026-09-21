---
type: concept
tags:
- RAG/embedding
- DeepLearning
summary: SimCSE 是基于对比学习的句向量优化方法，是缓解 概念BERT各向异性 的无监督优化代表。核心发现：利用预训练模型自带的 Dropout mask
  作为"增广手段"，得到的句向量质量远好于传统文本增广方法。
sources:
- wiki/sources/一文详尽之Embedding.md
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-09-21'
aliases:
- SimCSE
- Simple Contrastive Sentence Embeddings
- 对比学习句向量
- 概念_SimCSE
---

# 概念_SimCSE_简单对比学习句向量


## 定义

SimCSE 是基于对比学习的句向量优化方法，是缓解 [[概念_BERT各向异性]] 的无监督优化代表。核心发现：利用预训练模型自带的 Dropout mask 作为"增广手段"，得到的句向量质量远好于传统文本增广方法。

## 无监督版本

1. 利用模型中的 Dropout mask，对每个样例进行两次前向传播，得到两个不同 embeddings
2. 同一样例得到的向量对作为正样本对
3. 同一 batch 中所有其他样例产生的 embeddings 作为负样本
4. 通过拉近正样本对距离、推开负样本来训练

## 有监督版本

- 利用 NLI 标注数据集
- 每个样例与其 entailment 作为正样本对
- 同 batch 其他样例的 entailment 作为负样本
- 该样例对应的 contradiction 作为 hard negative

## 对比学习思想

- 将语义上接近的邻居拉到一起，将非邻居推开，学习有效表征
- 相比 SBERT 的有监督训练，无监督 SimCSE 可基于文本语料自动生成训练数据，解决数据标注依赖问题
- 传统文本增广手段：转译、删除、插入、调换顺序等

## 关联

- 相关概念：[[概念_BERT各向异性]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_Embedding与向量检索]]、[[概念_向量化召回改写]]
- 来源：[[一文详尽之Embedding]]、[[美团搜索查询改写实践]]