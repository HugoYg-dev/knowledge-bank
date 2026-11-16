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
- wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md
updated: '2026-11-16'
aliases:
- MRL
- Matryoshka Representation Learning
- 俄罗斯套娃表示学习
- 套娃表示学习
- 概念_MRL套娃表示学习
---

# 概念_Matryoshka表示学习


## 定义

Matryoshka Representation Learning (MRL，俄罗斯套娃表示学习，Kusupati 等，NeurIPS 2022) 是一种嵌入训练方法，通过以嵌套方式对 $O(\log(d))$ 低维前缀向量进行显式优化，在同一个高维向量中学习不同容量的表征。名称来源于"俄罗斯套娃"——嵌入的前 $m$ 维本身就是一个信息丰富的低维表征。

## 核心原理

- 训练时不仅对全尺寸嵌入计算损失，还对多种前缀截断维度（如 $64, 128, 256, 512, 1024, 1536$）分别计算对比学习损失并加权求和：
  $$\mathcal{L}_{MRL} = \sum_{m \in \mathcal{M}} w_m \mathcal{L}(z_{1:m})$$
- 迫使模型将最高频、最具区分度的全局语义特征优先编码在嵌入前端，将细粒度微观修饰沉淀在后部维度，形成从粗到细的嵌套表征。

## 关键效果

- ImageNet-1K 分类：精度与基线相同时表征大小最多可缩小 14 倍
- 检索：128 倍理论加速（FLOPS），14 倍墙上时钟加速，精度与单次检索相当
- 嵌入大小只有 8.3% 时仍保持 98.37% 的性能（标准模型为 96.46%）
- **工业界 MTEB 实证**：OpenAI `text-embedding-3-large` 截断至 256 维时在 MTEB 评测中的得分仍优于 1536 维的上一代旗舰 `text-embedding-ada-002`，存储与内存计算开销降低约 6 倍

## 训练实现（Sentence Transformers）

- 使用 `MatryoshkaLoss` 包裹基础损失函数（如 `CoSENTLoss`、`MultipleNegativesRankingLoss`）
- 通过 `matryoshka_dims` 指定截断维度列表
- 训练时间不显著增加

## 使用方式

- 正常 encode 得到完整嵌入后，直接切片截断：`embeddings[..., :matryoshka_dim]`（推理期零微调开销）
- 截断后需重新归一化（如原嵌入已归一化）
- 推理速度不变（下游任务加速）

## 应用场景与正交压缩组合

- **筛选和重新排序（两阶段检索）**：先用低维前缀（如 256 维）配合 HNSW 快速粗排候选 Top-K，再用高维完整向量精排重打分（Rescore）
- **性能-精度权衡**：根据存储/速度/精度需求动态选择维度（API 可直接通过 `dimensions` 参数指定）
- **正交压缩叠加**：MRL 维度截断可与 [[concepts/概念_Quantized_Embedding_量化向量嵌入|SQ 标量量化]] 或 [[concepts/概念_Binary_Embedding_二进制向量嵌入|BQ 二值量化]] 自由叠加（如 MRL 256 维 + Int8 量化），实现维度与位宽双重压缩
- 必须选用 MRL 训练的模型，普通模型硬截断会崩

## 代表模型

- OpenAI `text-embedding-3-small` / `text-embedding-3-large`（原生 MRL）
- Cohere `embed-english-v3.0` / `embed-multilingual-v3.0`
- BAAI BGE 系列、`nomic-ai/nomic-embed-text-v1.5`、`tomaarsen/mpnet-base-nli-matryoshka`

## 关联

- 相关概念：[[概念_Embedding与向量检索]]、[[概念_Dense_Embedding_稠密向量嵌入]]、[[concepts/概念_PCA_主成分分析|概念_主成分分析_PCA]]、[[concepts/概念_Quantized_Embedding_量化向量嵌入|概念_Quantized_Embedding]]、[[concepts/概念_Binary_Embedding_二进制向量嵌入|概念_Binary_Embedding]]、[[concepts/概念_向量量化|概念_向量量化]]
- 实体：[[实体_Sentence_Transformers]]
- 来源：[[MRL_俄罗斯套娃表示学习]]、[[Matryoshka嵌入模型概述_HuggingFace]]、[[从BM25到Multi-Vector_6种Embedding演进路线]]、[[wiki/sources/2026-09-04_5-embedding-compression-techniques_1a06e32ac6088201.md]]