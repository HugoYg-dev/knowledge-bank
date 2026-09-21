---
type: entity
tags:
- RAG/embedding
- Skill/python
summary: 基于 Python/PyTorch 的句向量模型训练与嵌入计算推理框架（sbert）。
sources:
- wiki/sources/Agent Loop使用语义早停比max_iterations硬截断节省38% Token 且质量不降.md
- wiki/sources/Matryoshka嵌入模型概述_HuggingFace.md
- wiki/sources/一文详尽之Embedding.md
- wiki/sources/为什么用Qwen3_embedding和rerank.md
- wiki/sources/美团搜索查询改写实践.md
updated: '2026-07-01'
---

## 简介

Sentence Transformers（sbert.net）是一个常用于训练和使用嵌入模型的 Python 框架，提供句向量编码、相似度计算与模型训练能力。

## 核心 API

- `SentenceTransformer(model_name)`：加载模型
- `model.encode(texts)`：编码文本为向量；支持 `prompt_name="query"` 传入 instruct
- `util.cos_sim(a, b)`：计算余弦相似度
- `model.fit(...)`：训练

## Matryoshka 支持

- 实现了 `MatryoshkaLoss`，包裹基础损失函数（`CoSENTLoss`、`MultipleNegativesRankingLoss`）
- 通过 `matryoshka_dims` 指定多个截断维度
- 训练时间不显著增加
- 推理时切片截断：`embeddings[..., :matryoshka_dim]`

## 维护方

- UKPLab（GitHub: https://github.com/UKPLab/sentence-transformers）

## 关联

- 相关概念：[[概念_Matryoshka表示学习]]、[[概念_Instruct_Embedding_指令增强向量嵌入]]、[[概念_Sentence_BERT_孪生网络句向量]]、[[概念_Embedding与向量检索]]
- 实体：[[实体_Qwen3_Embedding]]
- 来源：[[Matryoshka嵌入模型概述_HuggingFace]]、[[一文详尽之Embedding]]、[[为什么用Qwen3_embedding和rerank]]
