---
type: concept
tags:
- RAG/retrieval
- RAG/embedding
summary: Matryoshka Representation Learning (MRL) 是一种嵌入训练方法，通过以嵌套方式对 O(log(d)) 低维向量进行显式优化，在同一个高维向量中学习不同容量的表征。名称来源于"俄罗斯套娃"——嵌入的前
  m 维本身就是一个信息丰富的低维表征。
sources:
- wiki/sources/MRL_俄罗斯套娃表示学习.md
- wiki/sources/Matryoshka嵌入模型概述_HuggingFace.md
- wiki/sources/从BM25到Multi-Vector_6种Embedding演进路线.md
updated: '2026-07-06'
---

# 概念_Matryoshka表示学习


## 定义

Matryoshka Representation Learning (MRL) 是一种嵌入训练方法，通过以嵌套方式对 O(log(d)) 低维向量进行显式优化，在同一个高维向量中学习不同容量的表征。名称来源于"俄罗斯套娃"——嵌入的前 m 维本身就是一个信息丰富的低维表征。

## 核心原理

- 训练时不仅对全尺寸嵌入计算损失，还对多种截断维度（如 768/512/256/128/64）分别计算损失
- 各维度损失值加在一起得到最终损失值，优化器调整模型使所有维度都有效
- 鼓励模型在嵌入的前端前置最重要信息
- 信息量随维度增加而增加，形成从粗到细的表征

## 关键效果

- ImageNet-1K 分类：精度与基线相同时表征大小最多可缩小 14 倍
- 检索：128 倍理论加速（FLOPS），14 倍墙上时钟加速，精度与单次检索相当
- 嵌入大小只有 8.3% 时仍保持 98.37% 的性能（标准模型为 96.46%）

## 训练实现（Sentence Transformers）

- 使用 `MatryoshkaLoss` 包裹基础损失函数（如 `CoSENTLoss`、`MultipleNegativesRankingLoss`）
- 通过 `matryoshka_dims` 指定截断维度列表
- 训练时间不显著增加

## 使用方式

- 正常 encode 得到完整嵌入后，切片截断：`embeddings[..., :matryoshka_dim]`
- 截断后需重新归一化（如原嵌入已归一化）
- 推理速度不变（下游任务加速）

## 应用场景

- **筛选和重新排序**：先用低维快速筛选候选，再用高维重排
- **性能-精度权衡**：根据存储/速度/精度需求动态选择维度
- 必须选用 MRL 训练的模型，普通模型硬截断会崩

## 代表模型

- OpenAI text-embedding-3-small / text-embedding-3-large
- nomic-ai/nomic-embed-text-v1.5
- tomaarsen/mpnet-base-nli-matryoshka

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Dense_Embedding_稠密向量嵌入]]
- 实体：[[实体_Sentence_Transformers]]
- 来源：[[MRL_俄罗斯套娃表示学习]]、[[Matryoshka嵌入模型概述_HuggingFace]]、[[从BM25到Multi-Vector_6种Embedding演进路线]]