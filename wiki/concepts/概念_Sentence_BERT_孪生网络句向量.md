---
type: concept
tags:
- RAG/embedding
- DeepLearning
summary: Sentence-BERT（SBERT）通过修改预训练 BERT 结构，并在有监督任务（自然语言推理、语义文本相似度）上微调，优化 BERT 向量直接进行相似度计算的性能。是缓解
  概念BERT各向异性 的有监督优化代表。
sources:
- wiki/sources/ColBERTv2残差压缩演进.md
- wiki/sources/ColBERT原理与延迟交互机制.md
- wiki/sources/一文详尽之Embedding.md
- wiki/sources/为什么用Qwen3_embedding和rerank.md
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-09-21'
aliases:
- Sentence-BERT
- SBERT
- 句向量BERT
- 概念_Sentence-BERT
---

# 概念_Sentence_BERT_孪生网络句向量


## 定义

Sentence-BERT（SBERT）通过修改预训练 BERT 结构，并在有监督任务（自然语言推理、语义文本相似度）上微调，优化 BERT 向量直接进行相似度计算的性能。是缓解 [[概念_BERT各向异性]] 的有监督优化代表。

## 网络结构

- 孪生(Siamese)网络 + 三级(Triplet)网络
- u、v 分别表示输入两个句子的向量表示

## 三种目标函数

1. **Classification Objective Function**：孪生网络，针对分类问题。用 |u-v| 拼接，交叉熵损失
2. **Regression Objective Function**：孪生网络，针对回归问题。直接计算 u、v 余弦相似度，MSE 损失
3. **Triplet Objective Function**：三级网络，三个句子输入（锚定句 a、肯定句 p、否定句 n），使 a 与 p 距离小于 a 与 n 距离；论文中距离度量为欧式距离，边距为 1

## 训练数据

- 使用 NLI（自然语言推理）标注数据集（SNLI、MNLI 等）
- NLI 任务判断两句逻辑关系：蕴含/矛盾/中立
- 训练出的模型展现较好的语义扩展性和鲁棒性，适合 zero-shot/few-shot

## 同期相关工作

- USE（Universal Sentence Encoder）、InferSent，共性是使用"双塔"类结构

## 关联

- 相关概念：[[概念_BERT各向异性]]、[[概念_SimCSE_简单对比学习句向量]]、[[概念_Embedding与向量检索]]、[[概念_向量化召回改写]]
- 来源：[[一文详尽之Embedding]]、[[为什么用Qwen3_embedding和rerank]]、[[美团搜索查询改写实践]]